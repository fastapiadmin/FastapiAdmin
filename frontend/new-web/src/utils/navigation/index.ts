/** Navigation helpers (flattened). */

import type { RouteLocationNormalized, RouteRecordRaw } from "vue-router";
import { router } from "@/router";
import type { AppRouteRecord, AppRouteRecord as AppRouteRecordFromTypes } from "@/types";
import i18n, { $t } from "@/locales";
import AppConfig from "@/config";
import { useWorktabStore } from "@/store/modules/worktab.store";
import { useSettingsStore } from "@/store/modules/setting.store";
import { IframeRouteManager } from "@/router/core";
import { useCommon } from "@/hooks/core/useCommon";

export type AppRouteRecordRaw = RouteRecordRaw & { hidden?: boolean };

export const setPageTitle = (to: RouteLocationNormalized): void => {
  const { title } = to.meta;
  if (!title) return;

  setTimeout(() => {
    document.title = `${formatMenuTitle(String(title))} - ${AppConfig.systemInfo.name}`;
  }, 150);
};

export const formatMenuTitle = (title: string): string => {
  if (!title) return "";

  if (title.startsWith("menus.")) {
    if (i18n.global.te(title)) return $t(title);
    return title.split(".").pop() || title;
  }

  return title;
};

export function isIframe(url: string): boolean {
  return url.startsWith("/outside/iframe/");
}

export const isNavigableMenuItem = (menuItem: AppRouteRecordFromTypes): boolean => {
  if (!menuItem.path || !menuItem.path.trim()) return false;
  return !menuItem.meta?.isHide;
};

const normalizePath = (path: string): string => (path.startsWith("/") ? path : `/${path}`);

export const getFirstMenuPath = (menuList: AppRouteRecordFromTypes[]): string => {
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

export const setWorktab = (to: RouteLocationNormalized): void => {
  const worktabStore = useWorktabStore();
  const { meta, path, name, params, query } = to;
  if (meta.isHideTab) return;

  if (isIframe(path)) {
    const iframeRoute = IframeRouteManager.getInstance().findByPath(to.path);
    if (!iframeRoute?.meta) return;

    worktabStore.openTab({
      title: iframeRoute.meta.title,
      icon: meta.icon as string,
      path,
      name: name as string,
      keepAlive: meta.keepAlive as boolean,
      params,
      query,
    });

    return;
  }

  if (useSettingsStore().showWorkTab || path === useCommon().homePath.value) {
    worktabStore.openTab({
      title: meta.title as string,
      icon: meta.icon as string,
      path,
      name: name as string,
      keepAlive: meta.keepAlive as boolean,
      params,
      query,
      fixedTab: meta.fixedTab as boolean,
    });
  }
};
