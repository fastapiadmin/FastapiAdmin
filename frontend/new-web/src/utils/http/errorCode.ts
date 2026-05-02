/**
 * 错误码映射模块
 *
 * 定义 HTTP 状态码对应的错误提示信息
 *
 * @module utils/errorCode
 */

/** 错误码映射类型 */
interface ErrorCodeMap {
  [key: string]: string;
}

/**
 * HTTP 状态码与错误信息的映射表
 *
 * 包含常见的 HTTP 错误状态码及其对应的中文提示信息
 *
 * @example
 * ```typescript
 * import errorCode from '@/utils/errorCode';
 * console.log(errorCode['401']); // "认证失败，无法访问系统资源"
 * ```
 */
const errorCode: ErrorCodeMap = {
  "401": "认证失败，无法访问系统资源",
  "403": "当前操作没有权限",
  "404": "访问资源不存在",
  default: "系统未知错误，请反馈给管理员",
};

export default errorCode;
