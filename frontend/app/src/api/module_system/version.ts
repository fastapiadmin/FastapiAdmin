import { http } from '@/http'

const SYSTEM_BASE = '/system'

export interface VersionItem {
  id: number
  version: string
  title: string
  date: string
  content?: string | null
  description?: string | null
  sort?: number
  status?: number
  require_re_login?: boolean
}

/** 版本更新日志（公开接口，无需登录） */
export const VersionAPI = {
  getPublished(): Promise<VersionItem[]> {
    return http.Get<VersionItem[]>(`${SYSTEM_BASE}/versions/published`)
  },
}
