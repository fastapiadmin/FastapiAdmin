import type { App } from "vue";
import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import { router } from "@/router";
import { resetDynamicRoutesSync } from "@/router/guards/beforeEach";
import { useUserStore } from "./modules/user.store";
import { useDictStore } from "./modules/dict.store";
import { useNoticeStore } from "./modules/notice.store";
import { useConfigStore } from "./modules/config.store";
import { useTagsViewStore } from "./modules/tags-view.store";

const store = createPinia();

store.use(piniaPluginPersistedstate);

export function initStore(app: App<Element>) {
  app.use(store);
}

export * from "./modules/app.store";
export * from "./modules/config.store";
export * from "./modules/dict.store";
export * from "./modules/lock.store";
export * from "./modules/menu.store";
export * from "./modules/notice.store";
export * from "./modules/setting.store";
export * from "./modules/table.store";
export * from "./modules/tags-view.store";
export * from "./modules/user.store";
export * from "./modules/worktab.store";

export { store };
export { useUserStore, useDictStore, useNoticeStore, useConfigStore, useTagsViewStore };

export interface RefreshCacheOptions {
  dictTypes?: string[];
  refreshUser?: boolean;
  refreshRoutes?: boolean;
  refreshConfig?: boolean;
  refreshNotice?: boolean;
  clearTags?: boolean;
  clearDictBefore?: boolean;
}

export async function refreshAppCaches(opts: RefreshCacheOptions = {}) {
  const {
    dictTypes,
    refreshUser = true,
    refreshRoutes = true,
    refreshConfig = true,
    refreshNotice = true,
    clearTags = false,
    clearDictBefore = false,
  } = opts;

  const userStore = useUserStore(store);
  const dictStore = useDictStore(store);
  const noticeStore = useNoticeStore(store);
  const configStore = useConfigStore(store);
  const tagsViewStore = useTagsViewStore(store);

  const tasks: Promise<any>[] = [];

  if (refreshUser) {
    tasks.push(userStore.getUserInfo());
  }
  if (refreshConfig) {
    tasks.push(configStore.getConfig(true));
  }
  if (refreshNotice) {
    tasks.push(noticeStore.getNotice());
  }
  if (dictTypes && dictTypes.length > 0) {
    if (clearDictBefore) dictStore.clearDictData();
    tasks.push(dictStore.getDict(dictTypes));
  }

  await Promise.allSettled(tasks);

  if (refreshRoutes) {
    resetDynamicRoutesSync();
    await router.replace({
      path: router.currentRoute.value.path,
      query: router.currentRoute.value.query,
      hash: router.currentRoute.value.hash,
    });
  }

  if (clearTags) {
    await tagsViewStore.delAllViews();
  }
}
