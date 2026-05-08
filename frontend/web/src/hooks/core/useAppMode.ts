/**
 * useAppMode - 应用模式管理
 *
 * 提供应用访问模式的判断和管理功能，支持前端和后端两种权限控制模式。
 * 根据环境变量 VITE_ACCESS_MODE 自动识别当前运行模式：
 * frontend | backend | mixed（后端菜单 + 前端 builtinFrontendRoutes 合并展示）
 *
 * ## 主要功能
 *
 * 1. 模式识别 - 自动识别前端模式或后端模式
 * 2. 前端模式 - 权限由前端路由配置控制，适合小型项目或演示环境
 * 3. 后端模式 - 权限由后端接口返回的菜单数据控制，适合企业级应用
 * 4. 响应式状态 - 提供响应式的模式判断，方便在组件中使用
 *
 * @module useAppMode
 * @author FastapiAdmin Team
 */

import { computed } from "vue";

export function useAppMode() {
  const accessMode = (import.meta.env.VITE_ACCESS_MODE || "").trim();

  /** 仅前端 builtinFrontendRoutes（默认为空，壳层菜单由 mergeShellRoutesIntoMenu 补全） */
  const isFrontendMode = computed(() => accessMode === "frontend");
  /** 仅后端菜单接口 */
  const isBackendMode = computed(() => accessMode === "backend");
  /** 后端菜单与前端路由模块合并（同名路由以前端模块注册顺序中后端为先，见 MenuProcessor） */
  const isMixedMenuMode = computed(() => accessMode === "mixed");

  const currentMode = computed(() => accessMode);

  return {
    isFrontendMode,
    isBackendMode,
    isMixedMenuMode,
    currentMode,
  };
}
