/**
 * HTTP：Axios 实例、约定常量、错误类型与拦截器（单文件聚合）
 */

import axios, {
  type AxiosError,
  type AxiosInstance,
  type AxiosRequestConfig,
  type AxiosResponse,
  type InternalAxiosRequestConfig,
} from "axios";
import qs from "qs";
import { ElMessage } from "element-plus";
import { ResultEnum } from "@/enums/api/result.enum";
import { Auth } from "@/utils/auth";
import { redirectToLogin } from "@/utils/auth";
import { $t } from "@/locales";
import AuthAPI from "@/api/module_system/auth";

// --- 配置常量 -----------------------------------------------------------------

/** 跳过鉴权标记：接口 headers.Authorization 设为该值时不带 token 请求 */
export const NO_AUTH_FLAG = "no-auth";

export interface ExtendedRequestConfig extends AxiosRequestConfig {
  skipAuth?: boolean;
  showSuccessMessage?: boolean;
  showErrorMessage?: boolean;
}

// --- 语义状态码与 HttpError ----------------------------------------------------

export enum ApiStatus {
  success = 200,
  error = 400,
  unauthorized = 401,
  forbidden = 403,
  notFound = 404,
  methodNotAllowed = 405,
  requestTimeout = 408,
  internalServerError = 500,
  notImplemented = 501,
  badGateway = 502,
  serviceUnavailable = 503,
  gatewayTimeout = 504,
  httpVersionNotSupported = 505,
}

export interface ErrorLogData {
  code: number;
  message: string;
  data?: unknown;
  timestamp: string;
  url?: string;
  method?: string;
  stack?: string;
}

export class HttpError extends Error {
  public readonly code: number;
  public readonly data?: unknown;
  public readonly timestamp: string;
  public readonly url?: string;
  public readonly method?: string;

  constructor(
    message: string,
    code: number,
    options?: {
      data?: unknown;
      url?: string;
      method?: string;
    }
  ) {
    super(message);
    this.name = "HttpError";
    this.code = code;
    this.data = options?.data;
    this.timestamp = new Date().toISOString();
    this.url = options?.url;
    this.method = options?.method;
  }

  public toLogData(): ErrorLogData {
    return {
      code: this.code,
      message: this.message,
      data: this.data,
      timestamp: this.timestamp,
      url: this.url,
      method: this.method,
      stack: this.stack,
    };
  }
}

const getErrorMessage = (status: number): string => {
  const errorMap: Record<number, string> = {
    [ApiStatus.unauthorized]: "httpMsg.unauthorized",
    [ApiStatus.forbidden]: "httpMsg.forbidden",
    [ApiStatus.notFound]: "httpMsg.notFound",
    [ApiStatus.methodNotAllowed]: "httpMsg.methodNotAllowed",
    [ApiStatus.requestTimeout]: "httpMsg.requestTimeout",
    [ApiStatus.internalServerError]: "httpMsg.internalServerError",
    [ApiStatus.badGateway]: "httpMsg.badGateway",
    [ApiStatus.serviceUnavailable]: "httpMsg.serviceUnavailable",
    [ApiStatus.gatewayTimeout]: "httpMsg.gatewayTimeout",
  };

  return $t(errorMap[status] || "httpMsg.internalServerError");
};

export function handleError(error: AxiosError<ApiResponse>): never {
  if (error.code === "ERR_CANCELED") {
    console.warn("Request cancelled:", error.message);
    throw new HttpError($t("httpMsg.requestCancelled"), ApiStatus.error);
  }

  const statusCode = error.response?.status;
  const errorMessage = error.response?.data?.msg || error.message;
  const requestConfig = error.config;

  if (!error.response) {
    throw new HttpError($t("httpMsg.networkError"), ApiStatus.error, {
      url: requestConfig?.url,
      method: requestConfig?.method?.toUpperCase(),
    });
  }

  const message = statusCode
    ? getErrorMessage(statusCode)
    : errorMessage || $t("httpMsg.requestFailed");
  throw new HttpError(message, statusCode || ApiStatus.error, {
    data: error.response.data,
    url: requestConfig?.url,
    method: requestConfig?.method?.toUpperCase(),
  });
}

export function showError(error: HttpError, showMessage: boolean = true): void {
  if (showMessage) {
    ElMessage.error(error.message);
  }
  console.error("[HTTP Error]", error.toLogData());
}

export function showSuccess(message: string, showMessage: boolean = true): void {
  if (showMessage) {
    ElMessage.success(message);
  }
}

export const isHttpError = (error: unknown): error is HttpError => {
  return error instanceof HttpError;
};

// --- Token 刷新去重 -----------------------------------------------------------

/**
 * token 刷新进行中标识，避免并发 401 触发多次 refresh 请求。
 * 配合 pendingRequests 队列，刷新成功后统一重放等待中的请求。
 */
let isRefreshing = false;
let pendingRequests: Array<{
  config: InternalAxiosRequestConfig;
  resolve: (value: any) => void;
  reject: (reason?: any) => void;
}> = [];

function onRefreshed(newToken: string) {
  const list = pendingRequests;
  pendingRequests = [];
  list.forEach(({ config, resolve }) => {
    config.headers.Authorization = `Bearer ${newToken}`;
    resolve(request(config));
  });
}

function onRefreshFailed() {
  pendingRequests.forEach(({ reject }) => reject(new Error("Token refresh failed")));
  pendingRequests = [];
}

// --- Axios 实例 ---------------------------------------------------------------

const request: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_APP_BASE_API,
  timeout: Number(import.meta.env.VITE_TIMEOUT) || 15000,
  headers: { "Content-Type": "application/json;charset=utf-8" },
  paramsSerializer: (params) => qs.stringify(params, { indices: false }),
});

request.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const accessToken = Auth.getAccessToken();
    const auth = config.headers.Authorization;

    if (auth === NO_AUTH_FLAG) {
      delete config.headers.Authorization;
      return config;
    }

    if (!auth && accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }

    return config;
  },
  (error) => {
    const msg = error instanceof Error ? error.message : String(error);
    ElMessage.error(msg);
    return Promise.reject(error);
  }
);

/**
 * 响应拦截器 —— 三层处理逻辑：
 *
 * 1. 成功响应（response）
 *    - blob 直通（文件下载不经过 JSON 解析）
 *    - 检查业务 code，非 SUCCESS 时报错
 *    - 非 GET 且非 login/logout 接口成功时显示成功消息
 *
 * 2. 网络错误（无 response）
 *    - 区分 ECONNREFUSED / timeout / Network Error，给出中文提示
 *
 * 3. 业务/鉴权错误（有 response）
 *    - Blob 响应错误 → 尝试解析 JSON 提取 msg
 *    - 401 / TOKEN_EXPIRED → 静默刷新 token，成功后重放待处理请求
 *    - 其他业务错误 → 按 code 分类提示
 */
request.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    if (response.config.responseType === "blob") {
      return response;
    }

    const data = response.data;

    if (data.code !== ResultEnum.SUCCESS) {
      ElMessage.error(data.msg);
      return Promise.reject(response);
    }

    if (
      response.config.method?.toUpperCase() !== "GET" &&
      !response.config.url?.includes("login") &&
      !response.config.url?.includes("logout")
    ) {
      ElMessage.success(data.msg);
    }

    return response;
  },
  async (error: AxiosError<ApiResponse>) => {
    // ── 网络错误（无响应体） ──
    if (!error.response) {
      let errorMessage = "网络连接异常";

      if (error.message?.includes("ECONNREFUSED")) {
        errorMessage = "服务器连接失败，请检查后端服务是否正常运行";
      } else if (error.message?.includes("timeout")) {
        errorMessage = "请求超时，请稍后重试";
      } else if (error.message?.includes("Network Error")) {
        errorMessage = "网络连接错误，请检查您的网络设置";
      }

      console.error("网络请求失败:", error);
      ElMessage.error(errorMessage);
      return Promise.reject(new Error(errorMessage));
    }

    const data = error.response?.data;

    // ── Blob 响应错误（文件下载场景） ──
    if (error.response?.config.responseType === "blob" && error.response.data instanceof Blob) {
      try {
        const text = await new Response(error.response.data).text();
        const jsonData: ApiResponse = JSON.parse(text);

        if (jsonData.code === ResultEnum.ERROR) {
          ElMessage.error(jsonData.msg || "请求错误");
          return Promise.reject(new Error(jsonData.msg || "请求错误"));
        } else if (jsonData.code === ResultEnum.EXCEPTION) {
          ElMessage.error(jsonData.msg || "服务异常");
          return Promise.reject(new Error(jsonData.msg || "服务异常"));
        }
      } catch (e) {
        console.error("请求异常:", e);
        ElMessage.error("数据解析失败");
        return Promise.reject(new Error("数据解析失败"));
      }
    }

    // ── 鉴权错误（401 / TOKEN_EXPIRED）：静默续期 ──
    const status = error.response.status;

    const hasApiCode =
      data !== undefined &&
      data !== null &&
      typeof data === "object" &&
      "code" in data &&
      typeof (data as ApiResponse).code === "number";

    if ((status === 401 && !hasApiCode) || data?.code === ResultEnum.TOKEN_EXPIRED) {
      const config = error.config as InternalAxiosRequestConfig | undefined;

      // 若 refresh 接口自身返回 401，不再递归续期，直接跳转登录
      if (!config || config.url?.includes("auth/token/refresh")) {
        await redirectToLogin("登录状态异常，请重新登录");
        return Promise.reject(new HttpError("Unauthorized", ApiStatus.unauthorized));
      }

      // 首次 401：发起 refresh；后续并发 401 入队等待
      if (!isRefreshing) {
        isRefreshing = true;
        try {
          // 直接请求刷新令牌接口，避免动态导入 user.store 造成循环依赖
          const refreshResp = await AuthAPI.refreshToken({
            refresh_token: Auth.getRefreshToken(),
          });
          const tokenData = refreshResp.data.data;
          Auth.setTokens(tokenData.access_token, tokenData.refresh_token, Auth.getRememberMe());
          isRefreshing = false;
          const newToken = Auth.getAccessToken();
          // 重放等待队列中的所有请求
          onRefreshed(newToken);
          // 用新 token 重试当前请求
          config.headers.Authorization = `Bearer ${newToken}`;
          return request(config);
        } catch {
          isRefreshing = false;
          // refresh 失败：拒绝队列中所有等待请求 + 跳转登录
          onRefreshFailed();
          const msg = data?.msg || "登录已失效，请重新登录";
          await redirectToLogin(msg);
          return Promise.reject(new HttpError(msg, ApiStatus.unauthorized));
        }
      } else {
        // 已有 refresh 进行中，将当前请求加入等待队列，刷新完成后自动重放
        return new Promise((resolve, reject) => {
          pendingRequests.push({ config: config!, resolve, reject });
        });
      }
    }

    // ── 业务错误（按 code 分类） ──
    if (data?.code === ResultEnum.ERROR) {
      ElMessage.error(data.msg || "请求错误");
      return Promise.reject(new Error(data.msg || "请求错误"));
    } else if (data?.code === ResultEnum.UNAUTHORIZED) {
      ElMessage.error(data.msg || "暂无权限");
      return Promise.reject(new Error(data.msg || "请求错误"));
    } else if (data?.code === ResultEnum.EXCEPTION) {
      ElMessage.error(data.msg || "服务异常");
      return Promise.reject(new Error(data.msg || "服务异常"));
    } else {
      ElMessage.error("请求处理失败，请稍后重试");
      return Promise.reject(new Error("请求处理失败"));
    }
  }
);

export default request;

export type { AxiosInstance } from "axios";
