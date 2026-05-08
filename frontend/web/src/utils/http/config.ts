/**
 * Axios 默认配置与请求相关类型
 */

import type { AxiosRequestConfig } from "axios";
import * as qs from "qs";

export const defaultConfig: AxiosRequestConfig = {
  baseURL: import.meta.env.VITE_APP_BASE_API,
  timeout: Number(import.meta.env.VITE_TIMEOUT) || 15000,
  headers: { "Content-Type": "application/json;charset=utf-8" },
  paramsSerializer: (params) => qs.stringify(params, { indices: false }),
};

/** 跳过鉴权：与单接口 `headers.Authorization` 约定一致 */
export const NO_AUTH_FLAG = "no-auth";

export type HttpMethod = "GET" | "POST" | "PUT" | "DELETE" | "PATCH" | "HEAD" | "OPTIONS";

export interface ExtendedRequestConfig extends AxiosRequestConfig {
  skipAuth?: boolean;
  showSuccessMessage?: boolean;
  showErrorMessage?: boolean;
}
