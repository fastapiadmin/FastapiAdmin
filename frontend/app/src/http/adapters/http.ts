import type { CustomRequestOptions, IResponse } from '../types'
import { useUserStore } from '@/store/userStore'
import { toLoginPage } from '@/utils/toLoginPage'
import { ResultEnum } from '../tools/enum'

// 配置 baseURL
const BASE_URL = import.meta.env.VITE_API_BASE_URL || ''
const API_PREFIX = import.meta.env.VITE_APP_BASE_API || ''

export function http<T>(options: CustomRequestOptions) {
  // 1. 返回 Promise 对象
  return new Promise<T>((resolve, reject) => {
    // 如果 url 不包含 http:// 或 https://，则添加 baseURL 和 API_PREFIX
    let url = options.url
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      url = `${BASE_URL}${API_PREFIX}${url}`
    }

    uni.request({
      ...options,
      url,
      dataType: 'json',
      // #ifndef MP-WEIXIN
      responseType: 'json',
      // #endif
      // 响应成功
      success: async (res) => {
        const userStore = useUserStore()
        const responseData = res.data as IResponse<T>
        const { code } = responseData

        // 检查是否是401错误（包括HTTP状态码401或业务码401）
        const isTokenExpired = res.statusCode === 401 || code === 401

        if (isTokenExpired) {
          // 清理用户信息，跳转到登录页
          userStore.clearAll()
          userStore.logout()
          toLoginPage()
          return reject(res)
        }

        // 处理其他成功状态（HTTP状态码200-299）
        if (res.statusCode >= 200 && res.statusCode < 300) {
          // 处理业务逻辑错误
          if (code !== ResultEnum.Success0) {
            uni.showToast({
              icon: 'error',
              title: responseData.msg || responseData.message || '请求错误',
            })
            return reject(responseData)
          }
          return resolve(responseData.data)
        }

        // 处理其他错误
        if (!options.hideErrorToast) {
          uni.showToast({
            icon: 'error',
            title: (res.data as any).msg || '请求错误',
          })
        }
        reject(res)
      },
      // 响应失败
      fail(err) {
        uni.showToast({
          icon: 'none',
          title: '网络错误，换个网络试试',
        })
        reject(err)
      },
    })
  })
}

/**
 * GET 请求
 * @param url 后台地址
 * @param query 请求query参数
 * @param header 请求头，默认为json格式
 * @returns 返回包含响应数据的 Promise
 */
export function httpGet<T>(
  url: string,
  query?: Record<string, any>,
  header?: Record<string, any>,
  options?: Partial<CustomRequestOptions>,
) {
  return http<T>({
    url,
    query,
    method: 'GET',
    header,
    ...options,
  })
}

/**
 * POST 请求
 * @param url 后台地址
 * @param data 请求body参数
 * @param query 请求query参数，post请求也支持query，很多微信接口都需要
 * @param header 请求头，默认为json格式
 * @returns 返回包含响应数据的 Promise
 */
export function httpPost<T>(
  url: string,
  data?: Record<string, any>,
  query?: Record<string, any>,
  header?: Record<string, any>,
  options?: Partial<CustomRequestOptions>,
) {
  return http<T>({
    url,
    query,
    data,
    method: 'POST',
    header,
    ...options,
  })
}
/**
 * PUT 请求
 */
export function httpPut<T>(
  url: string,
  data?: Record<string, any>,
  query?: Record<string, any>,
  header?: Record<string, any>,
  options?: Partial<CustomRequestOptions>,
) {
  return http<T>({
    url,
    data,
    query,
    method: 'PUT',
    header,
    ...options,
  })
}

/**
 * DELETE 请求（无请求体，仅 query）
 */
export function httpDelete<T>(
  url: string,
  query?: Record<string, any>,
  header?: Record<string, any>,
  options?: Partial<CustomRequestOptions>,
) {
  return http<T>({
    url,
    query,
    method: 'DELETE',
    header,
    ...options,
  })
}

// 支持与 axios 类似的API调用
http.get = httpGet
http.post = httpPost
http.put = httpPut
http.delete = httpDelete

// 支持与 AlovaJS 类似的API调用
http.Get = httpGet
http.Post = httpPost
http.Put = httpPut
http.Delete = httpDelete
