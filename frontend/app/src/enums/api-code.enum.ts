/**
 * API响应码枚举
 */
export enum ApiCode {
  /**
   * 成功
   */
  SUCCESS = 0,

  /**
   * 通用错误
   */
  ERROR = 1,

  /**
   * 异常
   */
  EXCEPTION = -1,

  /**
   * 未授权访问
   */
  UNAUTHORIZED = 10403,

  /**
   * 令牌已过期
   */
  TOKEN_EXPIRED = 10401,

  /**
   * 参数校验失败
   */
  PARAM_INVALID = 400,

  /**
   * 资源不存在
   */
  NOT_FOUND = 404,

  /**
   * 服务器内部错误
   */
  INTERNAL_ERROR = 500,
}
