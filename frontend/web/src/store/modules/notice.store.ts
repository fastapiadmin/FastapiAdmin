import { store } from '@/store';
import NoticeAPI, { NoticeTable } from '@/api/module_system/notice';

export const useNoticeStore = defineStore('notice', {
  state: () => ({
    noticeList: [] as NoticeTable[],
    total: 0,
    isNoticeLoaded: false,
    // 已读通知ID集合（前端持久化，避免刷新后重复展示）
    readIds: [] as number[],
  }),
  actions: {
    async getNotice() {
      const response = await NoticeAPI.listNoticeAvailable();
      const items = response.data.data.items || [];
      // 过滤掉已读的通知
      const readSet = new Set(this.readIds);
      const filtered = items.filter(
        (item) => item.id !== undefined && !readSet.has(item.id as number)
      );
      this.noticeList = filtered;
      this.total = filtered.length;
      this.isNoticeLoaded = true;
    },
    // 标记单条通知为已读
    markAsRead(id?: number) {
      if (id === undefined) return;
      if (!this.readIds.includes(id)) {
        this.readIds.push(id);
      }
      // 同步过滤当前列表
      this.noticeList = this.noticeList.filter((item) => item.id !== id);
      this.total = this.noticeList.length;
    },
    // 标记当前列表全部为已读
    markAllAsRead(ids: number[] = []) {
      const targets = ids.length
        ? ids
        : this.noticeList.map((item) => item.id!).filter((id): id is number => id !== undefined);
      const readSet = new Set(this.readIds);
      targets.forEach((id) => {
        if (!readSet.has(id)) this.readIds.push(id);
      });
      // 同步过滤当前列表
      this.noticeList = this.noticeList.filter(
        (item) => item.id !== undefined && !this.readIds.includes(item.id as number)
      );
      this.total = this.noticeList.length;
    },
    clearUserInfo() {
      this.noticeList = [];
      this.total = 0;
      this.isNoticeLoaded = false;
      this.readIds = [];
    },
  },
  persist: true,
});

export function useNoticeStoreHook() {
  return useNoticeStore(store);
}
