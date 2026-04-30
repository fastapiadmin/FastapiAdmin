// 导出类型
import type { CustomRequestOptions, IResponse } from './types'
// 导出请求适配器
import { http as alovaHttp } from './adapters/alova'

import { http as nativeHttp } from './adapters/http'

// 导出默认请求实例（默认使用 alova 请求实例）
export const http = alovaHttp

// 导出所有类型
export type { CustomRequestOptions, IResponse }

// 导出请求适配器，允许手动选择使用哪种请求方式
export { alovaHttp, nativeHttp }
