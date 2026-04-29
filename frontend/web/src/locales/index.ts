/**
 * 国际化配置
 *
 * 基于 vue-i18n 实现的多语言国际化解决方案。
 * 支持中文和英文切换，自动从本地存储恢复用户的语言偏好。
 *
 * ## 主要功能
 *
 * - 多语言支持 - 支持中文（简体）和英文两种语言
 * - 语言切换 - 运行时动态切换语言，无需刷新页面
 * - 持久化存储 - 自动保存和恢复用户的语言偏好
 * - 全局注入 - 在任何组件中都可以使用 $t 函数进行翻译
 * - 类型安全 - 提供 TypeScript 类型支持
 *
 * ## 支持的语言
 *
 * - zh: 简体中文
 * - en: English
 *
 * @module locales
 * @author Fastapi Admin Team
 */
import type { App } from "vue";
import { createI18n } from "vue-i18n";
import { useAppStoreHook } from "@/store/modules/app.store";
// 本地语言包
import enLocale from "./langs/en.json";
import zhCnLocale from "./langs/zh.json";

const appStore = useAppStoreHook();

const messages = {
  zh: {
    ...zhCnLocale,
  },
  en: {
    ...enLocale,
  },
};

const i18n = createI18n({
  legacy: false,
  locale: appStore.language,
  messages,
  globalInjection: true,
});

// 全局注册 i18n
export function initI18n(app: App<Element>) {
  app.use(i18n);
}

export default i18n;
