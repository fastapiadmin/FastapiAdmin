/**
 * 国际化工具函数模块
 *
 * 提供路由标题翻译等国际化相关工具函数
 *
 * @module utils/i18n
 */

import i18n from "@/locales/index";

/**
 * 翻译路由标题
 *
 * 根据路由元信息中的 title 字段进行国际化翻译
 * 主要用于面包屑导航、侧边栏菜单和标签页的标题显示
 *
 * @param {any} title - 路由标题，可以是字符串或其他类型
 * @returns {string} 翻译后的标题，如果没有找到翻译则返回原始标题
 *
 * @example
 * ```typescript
 * import { translateRouteTitle } from '@/utils/i18n';
 *
 * // 在路由守卫中使用
 * const title = translateRouteTitle(route.meta.title);
 * document.title = title;
 * ```
 */
export function translateRouteTitle(title: any): string {
  // 如果 title 不是字符串，直接返回原始值
  if (typeof title !== "string") {
    return String(title);
  }

  // 判断是否存在国际化配置，如果没有则返回原始标题
  const hasKey = i18n.global.te("route." + title);
  if (hasKey) {
    // 使用类型断言解决类型兼容性问题
    const translateFn = i18n.global.t as (key: string) => string;
    const translatedTitle = translateFn("route." + title);
    return translatedTitle;
  }

  return title;
}
