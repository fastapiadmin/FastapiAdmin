/**
 * useAppBootstrap —— 应用挂载后初始化编排。
 *
 * 统一调用所有 onMounted 阶段的初始化逻辑（存储检查、主题恢复、版本升级、站点配置），
 * 保持 App.vue 的 onMounted 为单行调用。
 */
import { useSiteConfig } from "@/hooks/core/useSiteConfig";
import { checkStorageCompatibility } from "@utils/storage";
import { toggleTransition } from "@utils/ui";
import { systemUpgrade } from "@utils/sys";

export function useAppBootstrap() {
  const { initSiteConfig } = useSiteConfig();

  const bootstrap = () => {
    checkStorageCompatibility();
    toggleTransition(false);
    systemUpgrade();
    initSiteConfig();
  };

  return { bootstrap };
}
