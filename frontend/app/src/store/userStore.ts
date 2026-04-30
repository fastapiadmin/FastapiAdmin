import type { LoginFormData, LoginResult, LogoutBody } from '@/api/auth'
import type { UserInfo } from '@/api/user'
import { defineStore } from 'pinia'
import AuthAPI from '@/api/auth'
import UserAPI from '@/api/user'
import {
  APP_ACCESS_TOKEN_KEY,
  APP_REFRESH_TOKEN_KEY,
  APP_USER_INFO,
} from '@/constants'
import { Storage } from '@/utils/storage'

export const useUserStore = defineStore('appUserInfo', {
  state: () => ({
    userInfo: Storage.get<UserInfo>(APP_USER_INFO),
    isLoggingIn: false,
  }),

  getters: {
    isLogin: state => !!state.userInfo,
  },

  // 统一的登录处理方法
  actions: {
    // 获取访问 token
    getAccessToken(): string | null {
      return Storage.get<string>(APP_ACCESS_TOKEN_KEY) || null
    },

    // 设置访问 token
    setAccessToken(token: string): void {
      Storage.set(APP_ACCESS_TOKEN_KEY, token)
    },

    // 获取刷新 token
    getRefreshToken(): string | null {
      return Storage.get<string>(APP_REFRESH_TOKEN_KEY) || null
    },

    // 设置刷新 token
    setRefreshToken(token: string): void {
      Storage.set(APP_REFRESH_TOKEN_KEY, token)
    },

    // 清除所有 token
    clearTokens(): void {
      Storage.remove(APP_ACCESS_TOKEN_KEY)
      Storage.remove(APP_REFRESH_TOKEN_KEY)
    },

    // 获取用户信息
    getUserInfo(): UserInfo | undefined {
      return Storage.get<UserInfo>(APP_USER_INFO)
    },

    // 设置用户信息
    setUserInfo(userInfo: Partial<UserInfo>): void {
      Storage.set(APP_USER_INFO, userInfo)
    },

    // 清除用户信息
    clearUserInfo(): void {
      Storage.remove(APP_USER_INFO)
    },

    // 清除所有缓存信息
    clearAll(): void {
      this.clearTokens()
      this.clearUserInfo()
    },

    // 检查用户登录状态，未登录则跳转到登录页面
    checkLogin(silent: boolean = false): boolean {
      const userStore = useUserStore()
      const accessToken = this.getAccessToken()

      // 检查 token 和用户信息是否都存在
      const isLoggedIn = !!(accessToken && userStore.userInfo)

      if (!isLoggedIn && !silent) {
        try {
          // 获取当前页面路径
          let currentPagePath = '/pages/index/index' // 默认路径

          const pages = getCurrentPages()
          if (pages && pages.length > 0) {
            const currentPage = pages[pages.length - 1]
            if (currentPage && currentPage.route) {
              currentPagePath = `/${currentPage.route}`

              // 处理页面参数 - 使用类型断言
              const pageOptions = (currentPage as any).options
              if (pageOptions && Object.keys(pageOptions).length > 0) {
                const params = new URLSearchParams(
                  pageOptions as Record<string, string>,
                )
                currentPagePath += `?${params.toString()}`
              }
            }
          }

          // 跳转到登录页面
          uni.navigateTo({
            url: `/pages/login/index?redirect=${encodeURIComponent(currentPagePath)}`,
            fail: (error) => {
              console.error('跳转登录页面失败:', error)
              // 如果 navigateTo 失败，尝试使用 reLaunch
              uni.reLaunch({
                url: '/pages/login/index',
              })
            },
          })
        }
        catch (error) {
          console.error('检查登录状态时发生错误:', error)
          // 发生错误时，尝试直接跳转到登录页
          uni.reLaunch({
            url: '/pages/login/index',
          })
        }
      }

      return isLoggedIn
    },

    // 检查用户是否已登录（静默检查，不跳转）
    isLoggedIn(): boolean {
      return this.checkLogin(true)
    },

    // 强制用户登录，清除无效的登录状态
    requireLogin(): void {
      const userStore = useUserStore()
      const accessToken = this.getAccessToken()

      if (!accessToken || !userStore.userInfo) {
        // 清除可能存在的无效状态
        this.clearTokens()
        userStore.logout()

        // 跳转到登录页
        uni.reLaunch({
          url: '/pages/login/index',
        })
      }
    },

    async handleLogin(loginFn: () => Promise<LoginResult>, loginType: string): Promise<LoginResult> {
      if (this.isLoggingIn)
        throw new Error('登录中，请稍后')

      this.isLoggingIn = true
      try {
        const result = await loginFn()
        this.setAccessToken(result.access_token)
        this.setRefreshToken(result.refresh_token)

        // 登录成功后获取用户信息
        await this.getInfo()

        return result
      }
      catch (error: any) {
        console.error(`${loginType}登录失败`, error)
        throw error
      }
      finally {
        this.isLoggingIn = false
      }
    },

    // 账号密码登录
    async login(data: LoginFormData): Promise<LoginResult> {
      return this.handleLogin(() => AuthAPI.login(data), '账号密码')
    },

    // 获取用户信息
    async getInfo(): Promise<UserInfo | null> {
      try {
        const userInfoData = await UserAPI.getCurrentUserInfo()
        this.setUserInfo(userInfoData)
        // 确保响应式数据更新
        this.userInfo = userInfoData
        return userInfoData
      }
      catch (error) {
        console.error('获取用户信息失败', error)
        return null
      }
    },

    // 登出
    async logout(): Promise<void> {
      try {
        const logoutBody: LogoutBody = {
          token: this.getAccessToken() || '',
        }
        await AuthAPI.logout(logoutBody) // 调用后台注销接口
      }
      catch (error) {
        console.error('登出失败', error)
      }
      finally {
        this.clearAll() // 清除本地的 token
        this.userInfo = {} // 清空用户信息
        // 跳转到登录页面
        uni.reLaunch({
          url: '/pages/login/index',
        })
      }
    },
  },
})
