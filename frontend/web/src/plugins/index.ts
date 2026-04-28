import type { App } from 'vue';

import { initDirectives } from '@/directives';
import { initRouter } from '@/router';
import { initStore } from '@/store';
import { initElIcons } from './icons';
import { initPermission } from './permission';
import { initI18n } from './i18n';
import { initCodeMirror } from './codemirror';
import { initElementPlus } from './elementPlus';

export default {
  install(app: App<Element>) {
    // 自定义指令(directive)
    initDirectives(app);
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
    initCodeMirror(app);
    // 注册 ElementPlus
    initElementPlus(app);
  },
};

/**
 * 插件统一导出
 * 集中管理第三方库的封装和配置
 */

export * from './echarts';
