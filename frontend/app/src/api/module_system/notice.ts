import type { BatchSetStatus } from './user'
import { http } from '@/http'

const SYSTEM_BASE = '/system'

/**
 * 公告管理 API
 * 与 web 端 module_system/notice.ts 对齐（完整字段定义）
 */
export const NoticeAPI = {
  getPage(params?: Record<string, any>) {
    return http.Get<PageResult<NoticeItem>>(`${SYSTEM_BASE}/notice/list`, params)
  },
  getDetail(id: number) {
    const method = http.Get<NoticeItem>(`${SYSTEM_BASE}/notice/detail/${id}`)
    method.config.cacheFor = 0
    return method
  },
  create(data: NoticeForm): Promise<NoticeItem> {
    return http.Post(`${SYSTEM_BASE}/notice/create`, data)
  },
  update(id: number, data: NoticeForm): Promise<NoticeItem> {
    return http.Put(`${SYSTEM_BASE}/notice/update/${id}`, data)
  },
  remove(ids: number[]): Promise<void> {
    return http.Delete(`${SYSTEM_BASE}/notice/delete`, ids)
  },
  batchStatus(data: BatchSetStatus): Promise<void> {
    return http.Patch(`${SYSTEM_BASE}/notice/status/batch`, data)
  },
  /** 我的未读公告数（首页公告条红点） */
  getUnreadCount(): Promise<{ unread: number }> {
    return http.Get(`${SYSTEM_BASE}/notice/unread-count`)
  },
  /** 我已读的公告 id（列表标未读） */
  getReadIds(): Promise<number[]> {
    return http.Get(`${SYSTEM_BASE}/notice/read-ids`)
  },
  /** 标记已读（不传 noticeIds 表示全部），返回剩余未读数 */
  markRead(noticeIds?: number[]): Promise<{ unread: number }> {
    return http.Post(`${SYSTEM_BASE}/notice/read`, noticeIds ? { notice_ids: noticeIds } : {})
  },

  getAvailable(): Promise<NoticeItem[]> {
    return http.Get(`${SYSTEM_BASE}/notice/available`)
  },
}

export interface NoticeForm extends BaseFormType {
  notice_title?: string
  notice_type?: string
  notice_content?: string
  status?: number
  description?: string
}

export interface NoticeItem extends BaseType, NoticeForm {}
