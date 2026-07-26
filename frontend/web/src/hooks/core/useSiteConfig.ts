/**
 * useSiteConfig - 站点配置初始化（标题 + favicon）。
 *
 * 从 configStore 拉取系统配置，同步到浏览器标题和 favicon。
 * 通过 watch 响应配置变更<｜image｜>（如管理员在后台修改后重新拉取时自动更新）。
 *
 * 应在 App.vue 的 onMounted 中调用。
 */

import { watch } from "vue";
import { useConfigStore } from "@stores";

const updateFavicon = (url: string) => {
  let link = document.querySelector<HTMLLinkElement>('link[rel="icon"], link[rel="shortcut icon"]');
  if (!link) {
    link = document.createElement("link");
    link.rel = "icon";
    document.head.appendChild(link);
  }
  link.href = url;
};

export function useSiteConfig() {
  const configStore = useConfigStore();

  /** 替换 document.title 中的站点名后缀 */
  const applyConfig = () => {
    const { sys_name, favicon } = configStore.configData;
    if (!sys_name?.config_value) return;
    const siteName = sys_name.config_value.trim();
    const existing = document.title;
    const dashIdx = existing.lastIndexOf(" - ");
    document.title = dashIdx > 0 ? `${existing.slice(0, dashIdx)} - ${siteName}` : siteName;
    if (favicon?.config_value) updateFavicon(favicon.config_value);
  };

  /** 初始化：优先使用缓存配置同步标题/favicon，无缓存时从接口获取 */
  const initSiteConfig = async () => {
    try {
      await configStore.getConfig();
      applyConfig();
    } catch (error) {
      console.error("[SiteConfig] 获取配置失败:", error);
    }
  };

  /** 配置更新后自动同步（管理员后台修改配置后重新拉取时） */
  watch(
    () => configStore.configData,
    () => applyConfig(),
    { deep: false }
  );

  return { initSiteConfig };
}
