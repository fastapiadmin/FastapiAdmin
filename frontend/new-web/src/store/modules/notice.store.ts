/**
 * 通知状态管理模块
 *
 * 提供系统通知的状态管理和持久化
 *
 * ## 主要功能
 *
 * - 通知列表获取和管理
 * - 已读通知标记
 * - 批量标记已读
 * - 通知数量统计
 * - 已读状态持久化
 *
 * ## 使用场景
 *
 * - 通知中心展示
 * - 未读通知提醒
 * - 通知阅读状态跟踪
 * - 登录后的通知加载
 *
 * ## 持久化
 *
 * - 使用 localStorage 存储
 * - 已读通知ID集合持久化
 * - 刷新页面后保留已读状态
 *
 * @module store/modules/notice.store
 * @author FastapiAdmin Team
 */
import { store } from "@/store";
import NoticeAPI, { NoticeTable } from "@/api/module_system/notice";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useNoticeStore = defineStore(
  "noticeStore",
  () => {
    // 通知列表
    const noticeList = ref<NoticeTable[]>([]);
    // 通知总数
    const total = ref(0);
    // 是否已加载通知
    const isNoticeLoaded = ref(false);
    // 已读通知ID集合（前端持久化，避免刷新后重复展示）
    const readIds = ref<number[]>([]);

    /**
     * 获取通知列表
     */
    async function getNotice() {
      const response = await NoticeAPI.listNoticeAvailable();
      const items = response.data.data.items || [];
      // 过滤掉已读的通知
      const readSet = new Set(readIds.value);
      const filtered = items.filter(
        (item: NoticeTable) => item.id !== undefined && !readSet.has(item.id as number)
      );
      noticeList.value = filtered;
      total.value = filtered.length;
      isNoticeLoaded.value = true;
    }

    /**
     * 标记单条通知为已读
     * @param id 通知ID
     */
    const markAsRead = (id?: number) => {
      if (id === undefined) return;
      if (!readIds.value.includes(id)) {
        readIds.value.push(id);
      }
      // 同步过滤当前列表
      noticeList.value = noticeList.value.filter((item) => item.id !== id);
      total.value = noticeList.value.length;
    };

    /**
     * 标记当前列表全部为已读
     * @param ids 指定的通知ID数组，不传则标记所有
     */
    const markAllAsRead = (ids: number[] = []) => {
      const targets = ids.length
        ? ids
        : noticeList.value.map((item) => item.id!).filter((id): id is number => id !== undefined);
      const readSet = new Set(readIds.value);
      targets.forEach((id) => {
        if (!readSet.has(id)) readIds.value.push(id);
      });
      // 同步过滤当前列表
      noticeList.value = noticeList.value.filter(
        (item) => item.id !== undefined && !readIds.value.includes(item.id as number)
      );
      total.value = noticeList.value.length;
    };

    /**
     * 清空用户通知信息（用于登出）
     */
    const clearUserInfo = () => {
      noticeList.value = [];
      total.value = 0;
      isNoticeLoaded.value = false;
      readIds.value = [];
    };

    return {
      noticeList,
      total,
      isNoticeLoaded,
      readIds,
      getNotice,
      markAsRead,
      markAllAsRead,
      clearUserInfo,
    };
  },
  {
    persist: true,
  }
);

export function useNoticeStoreHook() {
  return useNoticeStore(store);
}
