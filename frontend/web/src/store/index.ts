/**
 * Pinia Store 配置模块
 *
 * 提供全局状态管理的初始化和配置
 *
 * ## 主要功能
 *
 * - Pinia Store 实例创建
 * - 持久化插件配置（pinia-plugin-persistedstate）
 * - 版本化存储键管理
 * - 自动数据迁移（跨版本）
 * - LocalStorage 序列化配置
 * - Store 初始化函数
 *
 * ## 持久化策略
 *
 * - 使用 StorageKeyManager 生成版本化的存储键
 * - 格式：sys-v{version}-{storeId}
 * - 自动迁移旧版本数据到当前版本
 * - 使用 localStorage 作为存储介质
 *
 * @module store/index
 * @author Fastapi Admin Team
 */

import type { App } from 'vue';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate, { createPersistedState } from 'pinia-plugin-persistedstate';
import { StorageKeyManager } from '@/utils/storage/storage-key-manager';

export const store = createPinia();

// 创建存储键管理器实例
const storageKeyManager = new StorageKeyManager();
store.use(piniaPluginPersistedstate);
// 配置持久化插件
store.use(
  createPersistedState({
    key: (storeId: string) => storageKeyManager.getStorageKey(storeId),
    storage: localStorage,
    serializer: {
      serialize: JSON.stringify,
      deserialize: JSON.parse,
    },
  })
);

/**
 * 初始化 Store
 */
export function initStore(app: App<Element>): void {
  app.use(store);
}

export * from './modules/app.store';
export * from './modules/settings.store';
export * from './modules/tags-view.store';
export * from './modules/lock.store';
export * from './modules/permission.store';
export * from './modules/user.store';
export * from './modules/dict.store';
export * from './modules/config.store';
export * from './modules/notice.store';

// ------------------------------
// 🔄 刷新缓存统一入口
// ------------------------------
import router from '@/router';
import { useUserStoreHook } from './modules/user.store';
import { usePermissionStoreHook } from './modules/permission.store';
import { useDictStoreHook } from './modules/dict.store';
import { useConfigStoreHook } from './modules/config.store';
import { useNoticeStoreHook } from './modules/notice.store';
import { useTagsViewStore } from './modules/tags-view.store';

export interface RefreshCacheOptions {
  /** 需要刷新的字典类型列表，不传则不刷新字典 */
  dictTypes?: string[];
  /** 是否刷新用户信息（含角色与权限） */
  refreshUser?: boolean; // 默认 true
  /** 是否重置并重新生成动态路由 */
  refreshRoutes?: boolean; // 默认 true
  /** 是否刷新系统配置 */
  refreshConfig?: boolean; // 默认 true
  /** 是否刷新通知公告 */
  refreshNotice?: boolean; // 默认 true
  /** 是否清空标签视图（避免路由变化后出现不一致） */
  clearTags?: boolean; // 默认 false
  /** 刷新字典前是否先清空本地字典缓存 */
  clearDictBefore?: boolean; // 默认 false
}

/**
 * 一键刷新常用缓存项，可按需选择。
 * 建议：服务端数据（配置、字典、公告、用户/权限）适合刷新；UI 偏好（app/settings/lock）不刷新。
 */
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

  const userStore = useUserStoreHook();
  const permStore = usePermissionStoreHook();
  const dictStore = useDictStoreHook();
  const noticeStore = useNoticeStoreHook();
  const configStore = useConfigStoreHook();
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

  // 并行刷新服务端数据
  await Promise.allSettled(tasks);

  // 路由需要串行处理，先重置再生成
  if (refreshRoutes) {
    permStore.resetRouter();
    const dynamicRoutes = await permStore.generateRoutes();
    // 将新生成的动态路由注册到路由器，确保可用
    dynamicRoutes.forEach((route) => router.addRoute(route));
  }

  // 可选：清空标签视图，避免路由变更后的不一致
  if (clearTags) {
    await tagsViewStore.delAllViews();
  }
}
