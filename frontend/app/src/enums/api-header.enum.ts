/**
 * API 请求头相关枚举封装
 */
export enum ApiHeader {
  KEY = 'Content-Type',

  /* 表单数据 */
  FORM = 'application/x-www-form-urlencoded',

  /* JSON 数据 */
  JSON = 'application/json',

  /* 多部分数据 */
  MULTIPART = 'multipart/form-data',
}
