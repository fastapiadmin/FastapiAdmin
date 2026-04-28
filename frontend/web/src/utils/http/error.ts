/**
 * HTTP 错误处理模块
 *
 * 提供统一的 HTTP 请求错误处理机制，包括：
 * - 自定义 HttpError 错误类，封装错误信息、状态码、时间戳等
 * - 错误拦截和转换，将 Axios 错误转换为标准的 HttpError
 * - 错误消息国际化处理，根据状态码返回对应的多语言错误提示
 * - 统一的成功/错误消息展示
 *
 * @module utils/http/error
 */
import { AxiosError } from 'axios';
import { ApiStatus, ResultEnum } from './status';
import { $t } from '@/locales';

/** 错误响应数据结构 */
export interface ErrorResponse {
  /** 错误状态码 */
  code: number;
  /** 错误消息 */
  msg: string;
  /** 错误附加数据 */
  data?: unknown;
}

/** 错误日志数据结构 */
export interface ErrorLogData {
  /** 错误状态码 */
  code: number;
  /** 错误消息 */
  message: string;
  /** 错误附加数据 */
  data?: unknown;
  /** 错误发生时间戳 */
  timestamp: string;
  /** 请求 URL */
  url?: string;
  /** 请求方法 */
  method?: string;
  /** 错误堆栈信息 */
  stack?: string;
}

/**
 * HTTP 错误类
 *
 * 封装 HTTP 请求过程中产生的错误信息，包含错误码、错误消息、请求上下文等
 * 继承自 Error 类，支持错误堆栈追踪
 */
export class HttpError extends Error {
  /** 错误状态码 */
  public readonly code: number;
  /** 错误附加数据 */
  public readonly data?: unknown;
  /** 错误发生时间戳 */
  public readonly timestamp: string;
  /** 请求 URL */
  public readonly url?: string;
  /** 请求方法 */
  public readonly method?: string;

  /**
   * 创建 HttpError 实例
   * @param message 错误消息
   * @param code 错误状态码
   * @param options 可选配置，包含 data、url、method 等附加信息
   */
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
    this.name = 'HttpError';
    this.code = code;
    this.data = options?.data;
    this.timestamp = new Date().toISOString();
    this.url = options?.url;
    this.method = options?.method;
  }

  /**
   * 将错误转换为日志数据结构
   * @returns 错误日志数据
   */
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

/**
 * 根据 HTTP 状态码获取国际化错误消息
 * @param status HTTP 状态码
 * @returns 国际化后的错误消息
 */
const getErrorMessage = (status: number): string => {
  const errorMap: Record<number, string> = {
    [ApiStatus.unauthorized]: 'httpMsg.unauthorized',
    [ApiStatus.forbidden]: 'httpMsg.forbidden',
    [ApiStatus.notFound]: 'httpMsg.notFound',
    [ApiStatus.methodNotAllowed]: 'httpMsg.methodNotAllowed',
    [ApiStatus.requestTimeout]: 'httpMsg.requestTimeout',
    [ApiStatus.internalServerError]: 'httpMsg.internalServerError',
    [ApiStatus.badGateway]: 'httpMsg.badGateway',
    [ApiStatus.serviceUnavailable]: 'httpMsg.serviceUnavailable',
    [ApiStatus.gatewayTimeout]: 'httpMsg.gatewayTimeout',
  };
  return $t(errorMap[status] || 'httpMsg.internalServerError');
};

/**
 * 处理 Axios 错误并转换为 HttpError
 *
 * @param error Axios 错误对象
 * @returns 转换后的 HttpError
 * @throws HttpError 始终抛出 HttpError 实例
 */
export function handleError(error: AxiosError<ErrorResponse>): never {
  // 处理取消的请求
  if (error.code === 'ERR_CANCELED') {
    console.warn('Request cancelled:', error.message);
    throw new HttpError($t('httpMsg.requestCancelled'), ApiStatus.error);
  }

  const statusCode = error.response?.status;
  const errorMessage = error.response?.data?.msg || error.message;
  const requestConfig = error.config;

  // 处理网络错误（无响应）
  if (!error.response) {
    let errorMsg = $t('httpMsg.networkError');
    if (error.message?.includes('ECONNREFUSED')) {
      errorMsg = '服务器连接失败，请检查后端服务是否正常运行';
    } else if (error.message?.includes('timeout')) {
      errorMsg = '请求超时，请稍后重试';
    } else if (error.message?.includes('Network Error')) {
      errorMsg = '网络连接错误，请检查您的网络设置';
    }
    throw new HttpError(errorMsg, ApiStatus.error, {
      url: requestConfig?.url,
      method: requestConfig?.method?.toUpperCase(),
    });
  }

  // 根据 HTTP 状态码获取错误消息
  const message = statusCode
    ? getErrorMessage(statusCode)
    : errorMessage || $t('httpMsg.requestFailed');
  throw new HttpError(message, statusCode || ApiStatus.error, {
    data: error.response.data,
    url: requestConfig?.url,
    method: requestConfig?.method?.toUpperCase(),
  });
}

/**
 * 显示错误消息
 *
 * @param error HttpError 实例
 * @param showMessage 是否显示错误消息弹窗，默认 true
 */
export function showError(error: HttpError, showMessage: boolean = true): void {
  if (showMessage) {
    ElMessage.error(error.message);
  }
  // 记录错误日志
  console.error('[HTTP Error]', error.toLogData());
}

/**
 * 显示成功消息
 *
 * @param message 成功消息文本
 * @param showMessage 是否显示消息弹窗，默认 true
 */
export function showSuccess(message: string, showMessage: boolean = true): void {
  if (showMessage) {
    ElMessage.success(message);
  }
}

/**
 * 类型守卫：判断是否为 HttpError 类型
 *
 * @param error 任意错误对象
 * @returns 是否为 HttpError 类型
 */
export const isHttpError = (error: unknown): error is HttpError => {
  return error instanceof HttpError;
};

/**
 * 判断业务响应码是否为成功状态
 *
 * @param code 业务响应码
 * @returns 是否为成功状态
 */
export const isApiSuccess = (code: number): boolean => {
  return code === ResultEnum.SUCCESS;
};

/**
 * 判断业务响应码是否为 Token 过期状态
 *
 * @param code 业务响应码
 * @returns 是否为 Token 过期状态
 */
export const isTokenExpired = (code: number): boolean => {
  return code === ResultEnum.TOKEN_EXPIRED;
};
