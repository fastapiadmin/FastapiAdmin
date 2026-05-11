/**
 * API 结果枚举
 * 定义后端 API 响应状态码
 *
 * @module enums/api/result.enum
 */

/**
 * 结果枚举 - 与后端 ResultEnum 对应
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
