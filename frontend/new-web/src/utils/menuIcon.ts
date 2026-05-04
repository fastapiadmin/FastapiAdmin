import type { Component } from "vue";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";

/**
 * 菜单 / IconSelect 共用的图标存值约定（与 `components/IconSelect` 一致）：
 * - Element Plus：`el-icon-{组件名}`，或与 `@element-plus/icons-vue` 导出键一致的裸名（如 `PieChart`，兼容旧库手写）
 * - 历史自定义 SVG 文件名：原 `assets/icons` + `i-svg:` 展示，现由 `menuIconRemix.resolveIconForArtSvgIcon` 映射为 Iconify（默认 Remix `ri:`）
 * - Iconify：`collection:name`（含冒号，如 `ri:home-line`）
 */

export function isElementPlusStoredIcon(icon?: string | null): boolean {
  const s = icon?.trim();
  return !!s && s.startsWith("el-icon");
}

/** 与历史 `MenuSearch` 中 `resolveEpMenuIcon` 一致：`pie-chart` → `PieChart` */
function kebabSnakeBodyToPascalKey(body: string): string {
  return body
    .split(/[-_]/)
    .filter(Boolean)
    .map((seg) => seg.charAt(0).toUpperCase() + seg.slice(1).toLowerCase())
    .join("");
}

/**
 * 解析为 Element Plus 图标组件；否则 null（再走 Iconify / Remix 映射）。
 * 对齐旧版 `layouts/old/components/Menu/components/MenuItemContent.vue`（el-icon / 自定义文件名）
 * 及 `MenuSearch` 里对 `el-icon-*` 主体的 Pascal 推导。
 */
export function resolveElementPlusIconComponent(icon?: string | null): Component | null {
  const ic = icon?.trim();
  if (!ic) return null;

  const body = isElementPlusStoredIcon(ic) ? ic.replace(/^el-icon-?/i, "").trim() : ic;

  if (!body) return null;

  const mod = ElementPlusIconsVue as Record<string, Component | undefined>;

  let comp = mod[body];
  if (comp) return comp;

  if (/[-_]/.test(body)) {
    const pascal = kebabSnakeBodyToPascalKey(body);
    comp = mod[pascal];
    if (comp) return comp;
  }

  return null;
}

/** Iconify 完整 id（侧栏 ArtSvgIcon 使用） */
export function isIconifyStoredIcon(icon?: string | null): boolean {
  const s = icon?.trim();
  return !!s && s.includes(":");
}

function pascalOrPlainToKebab(name: string): string {
  const trimmed = name.trim();
  if (!trimmed) return "";

  if (!/[A-Z]/.test(trimmed)) {
    return trimmed.replace(/_/g, "-").toLowerCase();
  }

  return trimmed
    .replace(/([a-z\d])([A-Z])/g, "$1-$2")
    .replace(/([A-Z]+)([A-Z][a-z])/g, "$1-$2")
    .toLowerCase();
}

/**
 * `el-icon-Xxx` 无法映射到 EP 组件时的兜底，转为 Iconify `ep:`（与 Element Plus 图标集对应）
 */
export function elementMenuIconToEpIconify(icon: string): string {
  const name = icon.replace(/^el-icon-/i, "").trim();
  const kebab = pascalOrPlainToKebab(name);
  return kebab ? `ep:${kebab}` : "ep:menu";
}
