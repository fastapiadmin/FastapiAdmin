/**
 * Vue 应用插件注册 —— **唯一入口**：`initPlugins`（由 `main.ts` 调用）
 *
 * 约定：
 * - 凡对 `app.use(...)` 的封装，在本目录下独立文件导出 `initXxx(app)`（与 `icons.ts` 一致）。
 * - `echarts.ts` 为图表按需注册模块，供 `import { echarts } from '@/plugins/echarts'`，不由 `initPlugins` 挂载。
 * - 通用下载工具见 `@utils/download`，不属于 Vue 插件。
 */

export * from "./echarts";

import type { App } from "vue";
import { initGlobDirectives } from "@/directives";
import { initI18n } from "@/locales";
import { initRouter } from "@/router";
import { initStore } from "@stores";
import { initErrorHandle } from "@utils/sys";
import { initCodeMirror } from "./codemirror";
import { initElementPlus } from "./element-plus";
import { initElIcons } from "./icons";
import { initTerminal } from "./terminal";

export function initPlugins(app: App<Element>): void {
  initElIcons(app);
  initStore(app);
  initRouter(app);
  initGlobDirectives(app);
  initErrorHandle(app);
  initTerminal(app);
  initI18n(app);
  initCodeMirror(app);
  initElementPlus(app);
}
