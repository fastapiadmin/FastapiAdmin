/**
 * Axios 实例与请求 / 响应拦截器
 */

import axios, {
  type AxiosInstance,
  type AxiosResponse,
  type AxiosError,
  type InternalAxiosRequestConfig,
} from "axios";
import { ElMessage } from "element-plus";
import { Auth, redirectToLogin } from "@/utils/auth";
import { ResultEnum } from "@/enums/api/result.enum";
import { $t } from "@/locales";
import { defaultConfig, NO_AUTH_FLAG } from "./config";

const handleRequest = (config: InternalAxiosRequestConfig) => {
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
};

const handleRequestError = (error: unknown) => {
  const msg = error instanceof Error ? error.message : String(error);
  ElMessage.error(msg);
  return Promise.reject(error);
};

const handleResponse = (response: AxiosResponse<ApiResponse>) => {
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
};

const handleResponseError = async (error: AxiosError<ApiResponse>) => {
  if (!error.response) {
    let errorMessage = $t("httpMsg.networkError");
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
      }
      if (jsonData.code === ResultEnum.EXCEPTION) {
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
    return Promise.reject(new Error("Unauthorized"));
  }

  if (data?.code === ResultEnum.TOKEN_EXPIRED) {
    await redirectToLogin("登录已过期，请重新登录");
    return Promise.reject(new Error(data.msg));
  }
  if (data?.code === ResultEnum.ERROR) {
    ElMessage.error(data.msg || "请求错误");
    return Promise.reject(new Error(data.msg || "请求错误"));
  }
  if (data?.code === ResultEnum.UNAUTHORIZED) {
    ElMessage.error(data.msg || "暂无权限");
    return Promise.reject(new Error(data.msg || "请求错误"));
  }
  if (data?.code === ResultEnum.EXCEPTION) {
    ElMessage.error(data.msg || "服务异常");
    return Promise.reject(new Error(data.msg || "服务异常"));
  }

  ElMessage.error("请求处理失败，请稍后重试");
  return Promise.reject(new Error("请求处理失败"));
};

const httpRequest: AxiosInstance = axios.create(defaultConfig);

httpRequest.interceptors.request.use(handleRequest, handleRequestError);
httpRequest.interceptors.response.use(handleResponse, handleResponseError);

export default httpRequest;
