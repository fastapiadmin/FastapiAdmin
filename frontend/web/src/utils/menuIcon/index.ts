import type { Component } from "vue";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";

/**
 * 菜单 / IconSelect 共用的图标存值约定（与 `components/IconSelect` 一致）：
 * - Element Plus：`el-icon-{组件名}`，或与 `@element-plus/icons-vue` 导出键一致的裸名（如 `PieChart`，兼容旧库手写）
 * - 历史自定义 SVG 文件名：原 `assets/images/svg` + `i-svg:` 展示，现由 `menuIcon/remix` 的 `resolveIconForFaSvgIcon` 映射为 Iconify（默认 Remix `ri:`）
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

/** Iconify 完整 id（侧栏 FaSvgIcon 使用） */
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

/**
 * 历史：本地 `assets/images/svg/*.svg` 文件名作菜单存值，配合 `i-svg:` 类展示。
 * 现统一映射为 Iconify Remix Icon（`ri:`），由 `FaSvgIcon` 渲染。
 */

const FILE_SUFFIX: Record<string, string> = {
  close: "ri:file-close-line",
  copy: "ri:file-copy-line",
  css: "ri:file-code-line",
  dir: "ri:folder-line",
  excel: "ri:file-excel-2-line",
  exe: "ri:file-settings-line",
  html: "ri:file-code-line",
  image: "ri:file-image-line",
  js: "ri:file-code-line",
  json: "ri:file-code-line",
  music: "ri:file-music-line",
  open: "ri:folder-open-line",
  other: "ri:file-unknow-line",
  pdf: "ri:file-pdf-line",
  ppt: "ri:file-ppt-line",
  rar: "ri:file-zip-line",
  txt: "ri:file-text-line",
  video: "ri:file-video-line",
  wps: "ri:file-word-line",
  zip: "ri:file-zip-line",
};

const REMIX_BY_NAME: Record<string, string> = {
  ai: "ri:robot-2-line",
  alipay: "ri:alipay-fill",
  api: "ri:plug-line",
  arco: "ri:circle-line",
  "avatar-man": "ri:user-line",
  "avatar-woman": "ri:user-smile-line",
  backtop: "ri:arrow-up-circle-line",
  bell: "ri:notification-3-line",
  bilibili: "ri:movie-2-line",
  browser: "ri:chrome-line",
  captcha: "ri:shield-keyhole-line",
  cascader: "ri:filter-3-line",
  client: "ri:computer-line",
  close: "ri:close-line",
  close_all: "ri:close-circle-line",
  close_left: "ri:arrow-left-s-line",
  close_other: "ri:links-line",
  close_right: "ri:arrow-right-s-line",
  cnblogs: "ri:article-line",
  code: "ri:code-s-slash-line",
  collapse: "ri:menu-fold-line",
  csdn: "ri:article-line",
  dict: "ri:book-2-line",
  document: "ri:file-text-line",
  down: "ri:arrow-down-s-line",
  download: "ri:download-cloud-line",
  enter: "ri:login-box-line",
  esc: "ri:close-line",
  file: "ri:file-text-line",
  fullscreen: "ri:fullscreen-line",
  "fullscreen-exit": "ri:fullscreen-exit-line",
  gitcode: "ri:git-repository-line",
  gitee: "ri:git-branch-line",
  github: "ri:github-fill",
  homepage: "ri:home-4-line",
  java: "ri:cup-line",
  juejin: "ri:book-read-line",
  language: "ri:translate-2",
  layout_leftbar_close_line: "ri:menu-fold-line",
  layout_leftbar_open_line: "ri:menu-unfold-line",
  menu: "ri:menu-line",
  message: "ri:message-3-line",
  monitor: "ri:computer-line",
  project: "ri:projector-line",
  python: "ri:terminal-box-line",
  qq: "ri:qq-fill",
  refresh: "ri:refresh-line",
  role: "ri:admin-line",
  search: "ri:search-line",
  setting: "ri:settings-3-line",
  size: "ri:font-size-2",
  sql: "ri:database-2-line",
  system: "ri:settings-2-line",
  table: "ri:table-line",
  time: "ri:time-line",
  todo: "ri:checkbox-line",
  tree: "ri:node-tree",
  typescript: "ri:typescript-line",
  up: "ri:arrow-up-s-line",
  upload_file: "ri:upload-cloud-2-line",
  "upload-file": "ri:upload-cloud-2-line",
  upload_folder: "ri:folder-upload-line",
  "upload-folder": "ri:folder-upload-line",
  user: "ri:user-line",
  visitor: "ri:user-hefa-line",
  vite: "ri:rocket-line",
  vue: "ri:vuejs-line",
  wechat: "ri:wechat-fill",
  xml: "ri:code-s-slash-line",
  people: "ri:team-line",

  "menu-about": "ri:information-line",
  "menu-analyse": "ri:line-chfa-line",
  "menu-crud": "ri:database-2-line",
  "menu-detail": "ri:file-list-line",
  "menu-document": "ri:file-text-line",
  "menu-error": "ri:error-warning-line",
  "menu-example": "ri:lightbulb-line",
  "menu-file": "ri:folder-2-line",
  "menu-form": "ri:file-list-3-line",
  "menu-gitee": "ri:git-branch-line",
  "menu-home": "ri:home-4-line",
  "menu-layout": "ri:layout-line",
  "menu-multi": "ri:layout-grid-line",
  "menu-result": "ri:bar-chfa-box-line",
  "menu-system": "ri:settings-3-line",
  "menu-table": "ri:table-line",
  "menu-test": "ri:test-tube-line",

  "icon-msg": "ri:message-3-line",
  "icon-notice": "ri:notification-3-line",
  "icon-num": "ri:numbers-line",
  "icon-user": "ri:user-line",
  "icon-wait": "ri:timer-line",

  "item-angular": "ri:angularjs-line",
  "item-github": "ri:github-fill",
  "item-html5": "ri:html5-fill",
  "item-js": "ri:javascript-line",
  "item-react": "ri:reactjs-line",
  "item-vue": "ri:vuejs-line",

  "ai copy": "ri:robot-2-line",
  "backtop copy": "ri:arrow-up-circle-line",
  "file copy": "ri:file-text-line",
  "vue copy": "ri:vuejs-line",
  "wechat copy": "ri:wechat-fill",
};

function remixForFileKey(key: string): string {
  const lower = key.toLowerCase();
  const rest = lower.startsWith("file-") ? lower.slice(5) : lower;
  return FILE_SUFFIX[rest] ?? "ri:file-text-line";
}

/**
 * 将历史本地 SVG 文件名解析为 Remix Icon（Iconify `ri:`）。
 */
export function localSvgNameToRemixIcon(name: string): string {
  const raw = name.trim();
  if (!raw) return "ri:apps-line";

  if (REMIX_BY_NAME[raw]) return REMIX_BY_NAME[raw];

  const lower = raw.toLowerCase();
  if (REMIX_BY_NAME[lower]) return REMIX_BY_NAME[lower];

  if (lower.startsWith("file-") || lower.startsWith("file_")) {
    return remixForFileKey(lower.replace(/_/g, "-"));
  }

  if (lower.startsWith("menu-")) {
    return REMIX_BY_NAME[lower] ?? "ri:menu-add-line";
  }

  return "ri:apps-line";
}

/**
 * 菜单 / 表格等场景：存值可能是 EP、Iconify、或历史 SVG 文件名 → 统一为 Iconify id。
 */
export function resolveIconForFaSvgIcon(stored?: string | null): string {
  const s = stored?.trim() ?? "";
  if (!s) return "ri:file-3-line";

  if (isIconifyStoredIcon(s)) return s;

  if (resolveElementPlusIconComponent(s)) {
    return elementMenuIconToEpIconify(isElementPlusStoredIcon(s) ? s : s);
  }

  if (isElementPlusStoredIcon(s)) {
    return elementMenuIconToEpIconify(s);
  }

  return localSvgNameToRemixIcon(s);
}

/**
 * 本地 SVG URL（与 `@utils/icons` 同源）。
 * @deprecated 新代码请使用 {@link resolveLocalIconUrl} from `@utils/icons`
 */
export { resolveLocalIconUrl as resolveMenuLocalSvgUrl } from "@utils/icons";
