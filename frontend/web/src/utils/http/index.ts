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

// --- 配置常量 -----------------------------------------------------------------

/** 跳过鉴权：与单接口 `headers.Authorization` 约定一致 */
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

    const status = error.response.status;

    const hasApiCode =
      data !== undefined &&
      data !== null &&
      typeof data === "object" &&
      "code" in data &&
      typeof (data as ApiResponse).code === "number";

    if (status === 401 && !hasApiCode) {
      await redirectToLogin("登录已失效，请重新登录");
      return Promise.reject(new HttpError("Unauthorized", ApiStatus.unauthorized));
    }

    if (data?.code === ResultEnum.TOKEN_EXPIRED) {
      await redirectToLogin("登录已过期，请重新登录");
      const msg = data.msg || "登录已过期，请重新登录";
      return Promise.reject(new HttpError(msg, ApiStatus.unauthorized));
    } else if (data?.code === ResultEnum.ERROR) {
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
