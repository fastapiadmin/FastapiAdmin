import axios, {
  type InternalAxiosRequestConfig,
  type AxiosResponse,
  type AxiosInstance,
  type AxiosError,
} from "axios";
import qs from "qs";
import { useUserStoreHook } from "@/store/modules/user.store";
import { ResultEnum } from "@/enums/api/result.enum";
import { Auth } from "@/utils/auth";
import router from "@/router";

/**
 * 创建 HTTP 请求实例
 */
const httpRequest: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_APP_BASE_API,
  timeout: import.meta.env.VITE_TIMEOUT,
  headers: { "Content-Type": "application/json;charset=utf-8" },
  paramsSerializer: (params) => qs.stringify(params, { indices: false }),
});

/**
 * 请求拦截器 - 添加 Authorization 头
 */
httpRequest.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const accessToken = Auth.getAccessToken();

    // 如果 Authorization 设置为 no-auth，则不携带 Token
    if (!config.headers.Authorization && accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    } else {
      delete config.headers.Authorization;
    }

    return config;
  },
  (error) => {
    ElMessage.error(error);
    return Promise.reject(error);
  }
);

/**
 * 响应拦截器 - 统一处理响应和错误
 */
httpRequest.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    // 如果响应是二进制流，则直接返回（用于文件下载、Excel 导出等）
    if (response.config.responseType === "blob") {
      return response;
    }

    const data = response.data;

    // 检查请求是否失败
    if (data.code !== ResultEnum.SUCCESS) {
      ElMessage.error(data.msg);
      return Promise.reject(response);
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
  },
  async (error: AxiosError<ApiResponse>) => {
    // 处理网络错误（连接拒绝、超时等）
    if (!error.response) {
      let errorMessage = "网络连接异常";

      // 根据错误类型提供更友好的提示
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

    // 处理blob类型的错误响应
    if (error.response?.config.responseType === "blob" && error.response.data instanceof Blob) {
      try {
        // 将blob转换为JSON
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
        // 如果无法解析为JSON，则使用默认错误处理
        ElMessage.error("数据解析失败");
        return Promise.reject(new Error("数据解析失败"));
      }
    }

    if (data?.code === ResultEnum.TOKEN_EXPIRED) {
      await redirectToLogin("登录已过期，请重新登录");
      return Promise.reject(new Error(data.msg));
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

/**
 * 重定向到登录页面
 */
async function redirectToLogin(message: string = "请重新登录"): Promise<void> {
  try {
    ElNotification({
      title: "提示",
      message,
      type: "warning",
      duration: 3000,
    });

    await useUserStoreHook().resetAllState();

    // 跳转到登录页，保留当前路由用于登录后跳转
    const currentPath = router.currentRoute.value.fullPath;
    await router.push(`/login?redirect=${encodeURIComponent(currentPath)}`);
  } catch (error: any) {
    ElMessage.error(error.message);
  }
}

export default httpRequest;
