import type { uniappRequestAdapter } from '@alova/adapter-uniapp'
import type { IResponse } from '../types'
import AdapterUniapp from '@alova/adapter-uniapp'
import { createAlova } from 'alova'
import { createServerTokenAuthentication } from 'alova/client'
import VueHook from 'alova/vue'
import { useUserStore } from '@/store/userStore'
// 移除了 @dcloudio/types 导入，该模块不存在
import { toLoginPage } from '@/utils/toLoginPage'
import { ContentTypeEnum, ResultEnum, ShowMessage } from '../tools/enum'

// 配置动态Tag
export const API_DOMAINS = {
  DEFAULT: import.meta.env.VITE_API_BASE_URL || '',
  SECONDARY: import.meta.env.VITE_SERVER_BASEURL_SECONDARY || '',
}

/**
 * 创建请求实例
 */
const { onAuthRequired, onResponseRefreshToken }
  = createServerTokenAuthentication<typeof VueHook, typeof uniappRequestAdapter>({
    // 如果下面拦截不到，请使用 refreshTokenOnSuccess by 群友@琛
    refreshTokenOnError: {
      isExpired: (error) => {
        return error.response?.status === ResultEnum.Unauthorized
      },
      handler: async () => {
        try {
          // await authLogin();
        }
        catch (error) {
          // 切换到登录页
          toLoginPage({ mode: 'reLaunch' })
          throw error
        }
      },
    },
  })

/**
 * alova 请求实例
 */
const alovaInstance = createAlova({
  baseURL: `${API_DOMAINS.DEFAULT}${import.meta.env.VITE_APP_BASE_API || ''}`,
  ...AdapterUniapp(),
  timeout: 10000,
  statesHook: VueHook,

  beforeRequest: onAuthRequired((method) => {
    // 设置默认 Content-Type
    method.config.headers = {
      ContentType: ContentTypeEnum.JSON,
      Accept: 'application/json, text/plain, */*',
      ...method.config.headers,
    }

    const { config } = method
    // 修复认证逻辑：如果 ignoreAuth 为 true，则忽略认证
    // 特殊处理验证码和登录请求，总是跳过认证
    const isCaptchaRequest = method.url.includes('/captcha/get')
    const isLoginRequest = method.url.includes('/system/auth/login')
    const shouldAuth
      = !isCaptchaRequest && !isLoginRequest && !config.meta?.ignoreAuth
    // 处理认证信息   自行处理认证问题
    if (shouldAuth) {
      const userStore = useUserStore()
      const token = userStore.getAccessToken()
      // 只在需要认证时检查 token，验证码请求跳过
      if (!token && !isCaptchaRequest) {
        throw new Error('[请求错误]：未登录')
      }
      // 设置认证头
      if (token) {
        method.config.headers.Authorization = `Bearer ${token}`
      }
    }

    // 处理动态域名
    if (config.meta?.domain) {
      method.baseURL = config.meta.domain
    }
  }),

  responded: onResponseRefreshToken((response, method) => {
    const { config } = method
    const { requestType } = config
    const { statusCode, data: rawData } = response as any

    // 处理特殊请求类型（上传/下载）
    if (requestType === 'upload' || requestType === 'download') {
      return response
    }

    // 处理 HTTP 状态码错误
    if (statusCode !== 200) {
      const errorMessage
        = rawData?.msg || rawData?.message || (rawData as any)?.error || ShowMessage(statusCode) || `HTTP请求错误[${statusCode}]`
      throw new Error(errorMessage)
    }

    // 处理业务逻辑错误
    const { code, message, msg, data } = rawData as IResponse
    // 0和200当做成功都很普遍，这里直接兼容两者，见 ResultEnum
    if (code !== ResultEnum.Success0 && code !== ResultEnum.Success200) {
      const errorMessage = msg || message || '请求错误'
      throw new Error(errorMessage)
    }
    // 处理成功响应，返回业务数据
    return data
  }),
})

export const http = alovaInstance
