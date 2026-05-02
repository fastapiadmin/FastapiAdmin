/**
 * HTTP 请求封装模块
 * 基于 Axios 封装的 HTTP 请求工具，提供统一的请求/响应处理
 *
 * ## 主要功能
 *
 * - 请求/响应拦截器（自动添加 Token、统一错误处理）
 * - 支持跳过鉴权（headers.Authorization = "no-auth"）
 * - 401 未授权自动重定向到登录页
 * - 统一的成功/错误消息提示
 * - 支持文件下载（blob 响应类型）
 *
 * ## 使用方式
 *
 * ```typescript
 * import httpRequest from '@/utils/http';
 *
 * // GET 请求
 * const response = await httpRequest.get('/api/users');
 *
 * // POST 请求
 * const response = await httpRequest.post('/api/users', { data: userData });
 *
 * // 跳过鉴权
 * const response = await httpRequest.get('/api/public', {
 *   headers: { Authorization: 'no-auth' }
 * });
 * ```
 *
 * @module utils/http
 */

import axios, { type AxiosInstance } from "axios";
import { defaultConfig } from "./config";
import { handleRequest, handleRequestError, handleResponse, handleResponseError } from "./handler";

/**
 * 创建 HTTP 请求实例
 */
const httpRequest: AxiosInstance = axios.create(defaultConfig);

/**
 * 请求拦截器
 */
httpRequest.interceptors.request.use(handleRequest, handleRequestError);

/**
 * 响应拦截器
 */
httpRequest.interceptors.response.use(handleResponse, handleResponseError);

export default httpRequest;

// 导出配置和类型供外部使用
export * from "./config";
export type { AxiosInstance };
