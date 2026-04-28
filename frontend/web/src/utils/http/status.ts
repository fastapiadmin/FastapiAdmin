/**
 * HTTP 状态码枚举
 *
 * 定义标准的 HTTP 状态码，用于区分 HTTP 协议层面的响应状态
 *
 * @module utils/http/status
 */
export enum ApiStatus {
  /** 请求成功 */
  success = 200,
  /** 客户端请求错误 */
  error = 400,
  /** 未授权，需要登录 */
  unauthorized = 401,
  /** 禁止访问，权限不足 */
  forbidden = 403,
  /** 请求的资源不存在 */
  notFound = 404,
  /** 请求方法不允许 */
  methodNotAllowed = 405,
  /** 请求超时 */
  requestTimeout = 408,
  /** 服务器内部错误 */
  internalServerError = 500,
  /** 服务器未实现该功能 */
  notImplemented = 501,
  /** 网关错误 */
  badGateway = 502,
  /** 服务不可用 */
  serviceUnavailable = 503,
  /** 网关超时 */
  gatewayTimeout = 504,
  /** HTTP 版本不支持 */
  httpVersionNotSupported = 505,
}

/**
 * 业务响应码枚举
 *
 * 定义后端接口返回的业务状态码，用于区分业务处理结果
 * 与 ApiStatus（HTTP 状态码）不同，这是接口 data 字段中的 code 值
 */
export { ResultEnum } from '@/enums/api/result.enum';
