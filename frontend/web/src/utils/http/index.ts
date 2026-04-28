/**
 * HTTP 请求封装模块
 *
 * 基于 Axios 封装的 HTTP 请求工具，提供统一的请求/响应处理
 *
 * @module utils/http
 */
import axios, { AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import qs from 'qs';
import { useUserStore } from '@/store/modules/user';
import { ApiStatus, ResultEnum } from './status';
import { HttpError, showError } from './error';
import { $t } from '@/locales';

const REQUEST_TIMEOUT = 15000;
const MAX_RETRIES = 0;
const RETRY_DELAY = 1000;

export interface HttpRequestConfig extends AxiosRequestConfig {
  showErrorMessage?: boolean;
  showSuccessMessage?: boolean;
}

const { VITE_APP_BASE_API, VITE_TIMEOUT } = import.meta.env;

const httpRequest = axios.create({
  baseURL: VITE_APP_BASE_API,
  timeout: VITE_TIMEOUT || REQUEST_TIMEOUT,
  headers: { 'Content-Type': 'application/json;charset=utf-8' },
  paramsSerializer: (params) => qs.stringify(params, { indices: false }),
});

httpRequest.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const accessToken = useUserStore().accessToken;
    const auth = config.headers.Authorization;

    if (auth === 'no-auth') {
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

httpRequest.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    if (response.config.responseType === 'blob') {
      return response;
    }

    const { code, msg } = response.data;

    if (code !== ResultEnum.SUCCESS) {
      ElMessage.error(msg);
      return Promise.reject(response);
    }

    const method = response.config.method?.toUpperCase();
    const url = response.config.url;
    if (method !== 'GET' && !url?.includes('login') && !url?.includes('logout')) {
      if (msg) {
        ElMessage.success(msg);
      }
    }

    return response;
  },
  async (error: any) => {
    if (!error.response) {
      let errorMessage = $t('httpMsg.networkError');

      if (error.message?.includes('ECONNREFUSED')) {
        errorMessage = '服务器连接失败，请检查后端服务是否正常运行';
      } else if (error.message?.includes('timeout')) {
        errorMessage = '请求超时，请稍后重试';
      } else if (error.message?.includes('Network Error')) {
        errorMessage = '网络连接错误，请检查您的网络设置';
      }

      console.error('网络请求失败:', error);
      ElMessage.error(errorMessage);
      return Promise.reject(new Error(errorMessage));
    }

    if (error.response?.config.responseType === 'blob' && error.response.data instanceof Blob) {
      try {
        const text = await new Response(error.response.data).text();
        const jsonData: ApiResponse = JSON.parse(text);

        if (jsonData.code === ResultEnum.ERROR) {
          ElMessage.error(jsonData.msg || '请求错误');
          return Promise.reject(new Error(jsonData.msg || '请求错误'));
        } else if (jsonData.code === ResultEnum.EXCEPTION) {
          ElMessage.error(jsonData.msg || '服务异常');
          return Promise.reject(new Error(jsonData.msg || '服务异常'));
        }
      } catch (e) {
        console.error('请求异常:', e);
        ElMessage.error('数据解析失败');
        return Promise.reject(new Error('数据解析失败'));
      }
    }

    const data = error.response?.data;
    const status = error.response?.status;

    const hasApiCode =
      data !== undefined &&
      data !== null &&
      typeof data === 'object' &&
      'code' in data &&
      typeof data.code === 'number';

    if (status === 401 && !hasApiCode) {
      await redirectToLogin('登录已失效，请重新登录');
      return Promise.reject(new Error('Unauthorized'));
    }

    if (data?.code === ResultEnum.TOKEN_EXPIRED) {
      await redirectToLogin('登录已过期，请重新登录');
      return Promise.reject(new Error(data.msg));
    } else if (data?.code === ResultEnum.ERROR) {
      ElMessage.error(data.msg || '请求错误');
      return Promise.reject(new Error(data.msg || '请求错误'));
    } else if (data?.code === ResultEnum.UNAUTHORIZED) {
      ElMessage.error(data.msg || '暂无权限');
      return Promise.reject(new Error(data.msg || '请求错误'));
    } else if (data?.code === ResultEnum.EXCEPTION) {
      ElMessage.error(data.msg || '服务异常');
      return Promise.reject(new Error(data.msg || '服务异常'));
    } else {
      ElMessage.error('请求处理失败，请稍后重试');
      return Promise.reject(new Error('请求处理失败'));
    }
  }
);

function redirectToLogin(message: string) {
  useUserStore().logOut();
  window.location.href = `/login?redirect=${encodeURIComponent(window.location.hash.slice(1))}`;
  ElMessage.error(message);
}

function shouldRetry(statusCode: number) {
  return [
    ApiStatus.requestTimeout,
    ApiStatus.internalServerError,
    ApiStatus.badGateway,
    ApiStatus.serviceUnavailable,
    ApiStatus.gatewayTimeout,
  ].includes(statusCode);
}

function delay(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function retryRequest<T>(
  config: HttpRequestConfig,
  retries: number = MAX_RETRIES
): Promise<AxiosResponse<T>> {
  try {
    return await request<T>(config);
  } catch (error) {
    if (retries > 0 && error instanceof HttpError && shouldRetry(error.code)) {
      await delay(RETRY_DELAY);
      return retryRequest<T>(config, retries - 1);
    }
    throw error;
  }
}

async function request<T = any>(config: HttpRequestConfig): Promise<AxiosResponse<T>> {
  if (
    ['POST', 'PUT'].includes(config.method?.toUpperCase() || '') &&
    config.params &&
    !config.data
  ) {
    config.data = config.params;
    config.params = undefined;
  }

  try {
    const res = await httpRequest.request<T>(config);
    return res;
  } catch (error) {
    if (error instanceof HttpError && error.code !== ApiStatus.unauthorized) {
      const showMsg = config.showErrorMessage !== false;
      showError(error, showMsg);
    }
    return Promise.reject(error);
  }
}

const api = Object.assign(
  async function <T = any>(config: HttpRequestConfig): Promise<AxiosResponse<T>> {
    return retryRequest<T>(config);
  },
  {
    get<T>(config: HttpRequestConfig) {
      return retryRequest<T>({ ...config, method: 'GET' });
    },
    post<T>(config: HttpRequestConfig) {
      return retryRequest<T>({ ...config, method: 'POST' });
    },
    put<T>(config: HttpRequestConfig) {
      return retryRequest<T>({ ...config, method: 'PUT' });
    },
    del<T>(config: HttpRequestConfig) {
      return retryRequest<T>({ ...config, method: 'DELETE' });
    },
    request<T>(config: HttpRequestConfig) {
      return retryRequest<T>(config);
    },
  }
);

export default api;
export { httpRequest };
