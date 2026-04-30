// src/types/env.d.ts
/**
 * 环境变量类型声明
 */
interface ImportMetaEnv {
  /**
   * 应用端口
   */
  readonly VITE_APP_PORT: number
  /** 超时时间 */
  readonly VITE_TIMEOUT: number
  /** API基础路径 */
  readonly VITE_APP_BASE_API: string
  /** API服务器URL */
  readonly VITE_API_BASE_URL: string
  /** 环境 */
  readonly VITE_APP_ENV: string
  /** 项目名称 */
  readonly VITE_APP_TITLE: string
  /** WebSocket 端点 */
  readonly VITE_APP_WS_ENDPOINT?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
