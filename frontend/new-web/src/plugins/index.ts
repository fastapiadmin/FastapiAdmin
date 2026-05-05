/**
 * 插件统一导出
 * 集中管理第三方库的封装和配置
 */

export * from "./echarts";

import type { App } from "vue";

import { initGlobDirectives } from "@/directives";
import { initI18n } from "@/locales";
import { initRouter } from "@/router";
import { initStore } from "@/store";
import { initElIcons } from "./icons";
import { initPermission } from "./permission";
import { InstallCodeMirror } from "codemirror-editor-vue3";
import ElementPlus from "element-plus";

export default {
  install(app: App<Element>) {
    // 自定义指令(directive)
    initGlobDirectives(app);
    // 路由(router)
    initRouter(app);
    // 状态管理(store)
    initStore(app);
    // 国际化
    initI18n(app);
    // Element-plus图标
    initElIcons(app);
    // 路由守卫
    initPermission(app);
    // 注册 CodeMirror
    app.use(InstallCodeMirror);
    // 注册 ElementPlus
    app.use(ElementPlus);
  },
};
