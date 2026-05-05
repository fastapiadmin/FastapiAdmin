/**
 * HTTP 请求配置模块
 *
 * 集中管理 HTTP 请求的配置参数
 *
 * @module utils/http/config
 */

import { type AxiosRequestConfig } from "axios";
import * as qs from "qs";

/**
 * 默认请求配置
 */
export const defaultConfig: AxiosRequestConfig = {
  baseURL: import.meta.env.VITE_APP_BASE_API,
  timeout: Number(import.meta.env.VITE_TIMEOUT) || 15000,
  headers: { "Content-Type": "application/json;charset=utf-8" },
  paramsSerializer: (params) => qs.stringify(params, { indices: false }),
};

/**
 * 跳过鉴权的标识
 */
export const NO_AUTH_FLAG = "no-auth";

/**
 * 请求方法类型
 */
export type HttpMethod = "GET" | "POST" | "PUT" | "DELETE" | "PATCH" | "HEAD" | "OPTIONS";

/**
 * 扩展的请求配置
 */
export interface ExtendedRequestConfig extends AxiosRequestConfig {
  /** 是否跳过鉴权 */
  skipAuth?: boolean;
  /** 是否显示成功消息 */
  showSuccessMessage?: boolean;
  /** 是否显示错误消息 */
  showErrorMessage?: boolean;
}
