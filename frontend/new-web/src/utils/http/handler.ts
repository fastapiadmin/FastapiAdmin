/**
 * HTTP 请求处理器模块
 *
 * 提供请求拦截器和响应拦截器的处理逻辑
 *
 * @module utils/http/handler
 */

import {
  type InternalAxiosRequestConfig,
  type AxiosResponse,
  type AxiosError,
  type AxiosHeaders,
} from "axios";
import { ElMessage } from "element-plus";
import { ResultEnum } from "@/enums/api/result.enum";
import { Auth } from "@/utils/auth";
import { redirectToLogin } from "@/utils/auth/authRedirect";
import { NO_AUTH_FLAG } from "./config";

/**
 * 请求拦截器处理函数
 */
export function handleRequest(config: InternalAxiosRequestConfig): InternalAxiosRequestConfig {
  const accessToken = Auth.getAccessToken();
  const auth = config.headers?.Authorization;

  // 显式跳过鉴权
  if (auth === NO_AUTH_FLAG) {
    delete config.headers?.Authorization;
    return config;
  }

  // 未手动设置 Authorization 时自动附加 Bearer
  if (!auth && accessToken) {
    if (!config.headers) {
      config.headers = {} as AxiosHeaders;
    }
    config.headers.Authorization = `Bearer ${accessToken}`;
  }

  return config;
}

/**
 * 请求错误处理函数
 */
export function handleRequestError(error: unknown): Promise<never> {
  const msg = error instanceof Error ? error.message : String(error);
  ElMessage.error(msg);
  return Promise.reject(error);
}

/**
 * 响应拦截器处理函数
 */
export function handleResponse(response: AxiosResponse<ApiResponse>): AxiosResponse<ApiResponse> {
  // 如果响应是二进制流，则直接返回（用于文件下载、Excel 导出等）
  if (response.config.responseType === "blob") {
    return response;
  }

  const { data } = response;

  // 检查请求是否失败
  if (data.code !== ResultEnum.SUCCESS) {
    ElMessage.error(data.msg);
    throw response;
  }

  // 如果请求不是 GET 请求，且不是登录或退出登录接口，请求成功时显示成功提示
  if (
    response.config.method?.toUpperCase() !== "GET" &&
    !response.config.url?.includes("login") &&
    !response.config.url?.includes("logout")
  ) {
    ElMessage.success(data.msg);
  }

  return response;
}

/**
 * 响应错误处理函数
 */
export async function handleResponseError(error: AxiosError<ApiResponse>): Promise<never> {
  // 处理网络错误（连接拒绝、超时等）
  if (!error.response) {
    const errorMessage = getNetworkErrorMessage(error);
    console.error("网络请求失败:", error);
    ElMessage.error(errorMessage);
    throw new Error(errorMessage);
  }

  const { data } = error.response;

  // 处理blob类型的错误响应
  if (error.response?.config.responseType === "blob" && error.response.data instanceof Blob) {
    throw await handleBlobError(error.response.data);
  }

  const status = error.response.status;

  /** 是否为后端约定的 JSON 业务码结构 */
  const hasApiCode =
    data !== undefined &&
    data !== null &&
    typeof data === "object" &&
    "code" in data &&
    typeof (data as ApiResponse).code === "number";

  // HTTP 401 且无约定 body：按登录失效处理
  if (status === 401 && !hasApiCode) {
    await redirectToLogin("登录已失效，请重新登录");
    throw new Error("Unauthorized");
  }

  // 根据业务码处理错误
  throw await handleBusinessError(data);
}

/**
 * 获取网络错误消息
 */
function getNetworkErrorMessage(error: AxiosError): string {
  if (error.message?.includes("ECONNREFUSED")) {
    return "服务器连接失败，请检查后端服务是否正常运行";
  } else if (error.message?.includes("timeout")) {
    return "请求超时，请稍后重试";
  } else if (error.message?.includes("Network Error")) {
    return "网络连接错误，请检查您的网络设置";
  }
  return "网络连接异常";
}

/**
 * 处理 Blob 类型的错误响应
 */
async function handleBlobError(blobData: Blob): Promise<Error> {
  try {
    const text = await new Response(blobData).text();
    const jsonData: ApiResponse = JSON.parse(text);

    if (jsonData.code === ResultEnum.ERROR) {
      ElMessage.error(jsonData.msg || "请求错误");
      return new Error(jsonData.msg || "请求错误");
    } else if (jsonData.code === ResultEnum.EXCEPTION) {
      ElMessage.error(jsonData.msg || "服务异常");
      return new Error(jsonData.msg || "服务异常");
    }
  } catch (e) {
    console.error("请求异常:", e);
    ElMessage.error("数据解析失败");
    return new Error("数据解析失败");
  }

  ElMessage.error("请求处理失败，请稍后重试");
  return new Error("请求处理失败");
}

/**
 * 处理业务错误码
 */
async function handleBusinessError(data: ApiResponse | undefined): Promise<Error> {
  if (data?.code === ResultEnum.TOKEN_EXPIRED) {
    await redirectToLogin("登录已过期，请重新登录");
    return new Error(data.msg);
  } else if (data?.code === ResultEnum.ERROR) {
    ElMessage.error(data.msg || "请求错误");
    return new Error(data.msg || "请求错误");
  } else if (data?.code === ResultEnum.UNAUTHORIZED) {
    ElMessage.error(data.msg || "暂无权限");
    return new Error(data.msg || "请求错误");
  } else if (data?.code === ResultEnum.EXCEPTION) {
    ElMessage.error(data.msg || "服务异常");
    return new Error(data.msg || "服务异常");
  } else {
    ElMessage.error("请求处理失败，请稍后重试");
    return new Error("请求处理失败");
  }
}
