import type { RouteLocationNormalized, RouteRecordRaw } from "vue-router";
import type { AppRouteRecord } from "@/types/router";
import { router } from "@/router";

import i18n, { $t } from "@/locales";
import AppConfig from "@/config";
import { useConfigStore, useSettingsStore, useWorktabStore } from "@stores";
import { IframeRouteManager } from "@/router";
import { useCommon } from "@/hooks/core/useCommon";

/**
 * 导航辅助：菜单标题格式化、外链与路由跳转、工作标签同步（`setWorktab`）、文档标题设置（`setPageTitle`）。
 *
 * 核心函数：
 * - `setPageTitle`     → 设置浏览器标题 `meta.title - 站点名`
 * - `formatMenuTitle`  → 菜单标题 i18n 解析（`menus.xxx` 键 → 翻译文本）
 * - `handleMenuJump`   → 菜单点击跳转（支持外链、iframe、子菜单递归）
 * - `setWorktab`       → 与路由同步工作栏标签页
 */
export type AppRouteRecordRaw = RouteRecordRaw & { hidden?: boolean };

/** 浏览器标题：meta.title 经 i18n 键或原文 + 站点名（优先从参数获取） */
export const setPageTitle = (to: RouteLocationNormalized): void => {
  const { title } = to.meta;
  if (!title) return;

  const configStore = useConfigStore();
  const siteName =
    configStore.configData.sys_name?.config_value?.trim() || AppConfig.systemInfo.name;

  document.title = `${formatMenuTitle(String(title))} - ${siteName}`;
};

const MENU_TITLE_KEYS: Record<string, string> = {
  首页: "common.menuTitle.home",
  仪表盘: "common.menuTitle.dashboard",
  系统管理: "common.menuTitle.system",
  监控管理: "common.menuTitle.monitor",
  接口管理: "common.menuTitle.api",
  代码生成: "common.menuTitle.generator",
  AI管理: "common.menuTitle.ai",
  任务管理: "common.menuTitle.task",
  菜单管理: "common.menuTitle.menu",
  字典管理: "common.menuTitle.dict",
  参数管理: "common.menuTitle.params",
  部门管理: "common.menuTitle.dept",
  岗位管理: "common.menuTitle.position",
  角色管理: "common.menuTitle.role",
  用户管理: "common.menuTitle.user",
  日志管理: "common.menuTitle.log",
  公告管理: "common.menuTitle.notice",
  工单管理: "common.menuTitle.ticket",
  版本管理: "common.menuTitle.version",
  在线用户: "common.menuTitle.online",
  服务器监控: "common.menuTitle.server",
  缓存监控: "common.menuTitle.cache",
  定时任务: "common.menuTitle.cron",
  存储管理: "common.menuTitle.storage",
  文件浏览: "common.menuTitle.browse",
  节点管理: "common.menuTitle.node",
  传输任务: "common.menuTitle.transfer",
  流程管理: "common.menuTitle.workflow",
  个人中心: "common.menuTitle.profile",
};

export const formatMenuTitle = (title: string): string => {
  if (!title) return "";

  if (title.startsWith("menus.")) {
    if (i18n.global.te(title)) return $t(title);
    return title.split(".").pop() || title;
  }

  const key = MENU_TITLE_KEYS[title];
  if (key && i18n.global.te(key)) return $t(key);

  return title;
};

export function isIframe(url: string): boolean {
  return url.startsWith("/outside/iframe/");
}

export const isNavigableMenuItem = (menuItem: AppRouteRecord): boolean => {
  if (!menuItem.path || !menuItem.path.trim()) return false;
  return !menuItem.meta?.isHide;
};

const normalizePath = (path: string): string => (path.startsWith("/") ? path : `/${path}`);

export const getFirstMenuPath = (menuList: AppRouteRecord[]): string => {
  if (!Array.isArray(menuList) || menuList.length === 0) return "";

  for (const menuItem of menuList) {
    if (!isNavigableMenuItem(menuItem)) continue;

    if (menuItem.children?.length) {
      const childPath = getFirstMenuPath(menuItem.children);
      if (childPath) return childPath;
    }

    return normalizePath(menuItem.path!);
  }

  return "";
};

export const openExternalLink = (link: string) => window.open(link, "_blank");

export const handleMenuJump = (item: AppRouteRecord, jumpToFirst: boolean = false) => {
  const { link, isIframe: menuIsIframe } = item.meta;
  if (link && !menuIsIframe) return openExternalLink(link);

  if (!jumpToFirst || !item.children?.length) return router.push(item.path);

  const findFirstLeafMenu = (items: AppRouteRecord[]): AppRouteRecord | undefined => {
    for (const child of items) {
      if (isNavigableMenuItem(child)) {
        return child.children?.length ? findFirstLeafMenu(child.children) || child : child;
      }
    }
    return undefined;
  };

  const firstChild = findFirstLeafMenu(item.children);
  if (!firstChild) return router.push(item.path);
  if (firstChild.meta?.link) return openExternalLink(firstChild.meta.link);
  return router.push(firstChild.path);
};

/**
 * 与路由同步工作栏：受 `meta.isHideTab`、`settings.showWorkTab`、首页路径影响。
 * - 开多标签或停留在首页：写入 `opened`（openTab）。
 * - 关多标签且非首页：仅 `syncCurrentFromRoute`，不把每一页压入 `opened`，但保证 `current` 与本次导航一致。
 */
export const setWorktab = (to: RouteLocationNormalized): void => {
  const worktabStore = useWorktabStore();
  const { meta, path, name, params, query } = to;
  if (meta.isHideTab) return;

  const routeNameStr = name != null ? String(name) : "";

  if (isIframe(path)) {
    const iframeRoute = IframeRouteManager.getInstance().findByPath(to.path);
    if (!iframeRoute?.meta) return;

    worktabStore.openTab({
      title: iframeRoute.meta.title,
      icon: meta.icon as string,
      path,
      name: routeNameStr,
      keepAlive: meta.keepAlive !== false,
      params,
      query,
    });

    return;
  }

  const tabPayload = {
    title: (meta.title as string) || "",
    icon: meta.icon as string,
    path,
    name: routeNameStr,
    keepAlive: meta.keepAlive !== false,
    params,
    query,
    fixedTab: meta.fixedTab as boolean,
  };

  if (useSettingsStore().showWorkTab || path === useCommon().homePath.value) {
    worktabStore.openTab(tabPayload);
  } else {
    worktabStore.syncCurrentFromRoute({
      path: tabPayload.path,
      name: tabPayload.name,
      title: tabPayload.title,
      icon: tabPayload.icon,
      keepAlive: tabPayload.keepAlive,
      params: tabPayload.params,
      query: tabPayload.query,
    });
  }
};
