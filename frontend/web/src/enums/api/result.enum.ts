/**
 * 响应码枚举
 */
export const enum ResultEnum {
  /**
   * 成功
   */
  SUCCESS = 0,
  /**
   * 错误
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
}
