/**
 * 主题工具函数模块
 *
 * 提供主题相关的工具函数，包括颜色处理和主题切换功能
 *
 * ## 主要功能
 *
 * - 主题色生成
 * - CSS 变量应用
 * - 暗黑模式切换
 * - 侧边栏颜色方案切换
 *
 * @module utils/theme
 */

import { ThemeMode } from "@/enums";
import { getDarkColor, getLightColor } from "./colors";

/**
 * 生成主题色变体
 *
 * 根据主题色和主题模式生成一系列颜色变体，用于 CSS 变量
 *
 * @param {string} primary - 主题色，十六进制格式
 * @param {ThemeMode} theme - 主题模式，LIGHT 或 DARK
 * @returns {Record<string, string>} 颜色映射对象
 *
 * @example
 * ```typescript
 * const colors = generateThemeColors('#1890ff', ThemeMode.LIGHT);
 * // colors.primary -> '#1890ff'
 * // colors['primary-light-1'] -> 变浅10%的颜色
 * ```
 */
export function generateThemeColors(primary: string, theme: ThemeMode): Record<string, string> {
  const colors: Record<string, string> = {
    primary,
  };

  // 生成浅色变体 (primary-light-1 到 primary-light-9)
  for (let i = 1; i <= 9; i++) {
    colors[`primary-light-${i}`] =
      theme === ThemeMode.LIGHT
        ? `${getLightColor(primary, i / 10)}`
        : `${getDarkColor(primary, i / 10)}`;
  }

  // 生成深色变体
  colors["primary-dark-2"] =
    theme === ThemeMode.LIGHT ? `${getLightColor(primary, 0.2)}` : `${getDarkColor(primary, 0.3)}`;

  return colors;
}

/**
 * 将颜色应用到 DOM
 *
 * 将颜色对象中的所有颜色设置为 CSS 变量
 *
 * @param {Record<string, string>} colors - 颜色映射对象
 *
 * @example
 * ```typescript
 * applyTheme({ primary: '#1890ff', 'primary-light-1': '#40a9ff' });
 * // 会设置 --el-color-primary 和 --el-color-primary-light-1 等 CSS 变量
 * ```
 */
export function applyTheme(colors: Record<string, string>): void {
  const el = document.documentElement;

  Object.entries(colors).forEach(([key, value]) => {
    el.style.setProperty(`--el-color-${key}`, value);
  });

  // 确保主题色立即生效，强制重新渲染
  requestAnimationFrame(() => {
    el.style.setProperty("--theme-update-trigger", Date.now().toString());
  });
}

/**
 * 切换暗黑模式
 *
 * 通过添加或移除 CSS 类来切换暗黑模式
 *
 * @param {boolean} isDark - 是否启用暗黑模式
 *
 * @example
 * ```typescript
 * toggleDarkMode(true);  // 启用暗黑模式
 * toggleDarkMode(false); // 禁用暗黑模式
 * ```
 */
export function toggleDarkMode(isDark: boolean): void {
  if (isDark) {
    document.documentElement.classList.add(ThemeMode.DARK);
  } else {
    document.documentElement.classList.remove(ThemeMode.DARK);
  }
}

/**
 * 切换侧边栏颜色方案
 *
 * 通过添加或移除 CSS 类来切换侧边栏的深蓝色颜色方案
 *
 * @param {boolean} isBlueSidebar - 是否启用深蓝色侧边栏
 *
 * @example
 * ```typescript
 * toggleSidebarColor(true);  // 启用深蓝色侧边栏
 * toggleSidebarColor(false); // 禁用深蓝色侧边栏
 * ```
 */
export function toggleSidebarColor(isBlueSidebar: boolean): void {
  if (isBlueSidebar) {
    document.documentElement.classList.add("sidebar-color-blue");
  } else {
    document.documentElement.classList.remove("sidebar-color-blue");
  }
}
