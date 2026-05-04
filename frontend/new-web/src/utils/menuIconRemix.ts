import {
  elementMenuIconToEpIconify,
  isElementPlusStoredIcon,
  isIconifyStoredIcon,
  resolveElementPlusIconComponent,
} from "@/utils/menuIcon";

/**
 * 历史：本地 `assets/icons/*.svg` 文件名作菜单存值，配合 `i-svg:` 类展示。
 * 现统一映射为 Iconify Remix Icon（`ri:`），由 `ArtSvgIcon` 渲染。
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
  visitor: "ri:user-heart-line",
  vite: "ri:rocket-line",
  vue: "ri:vuejs-line",
  wechat: "ri:wechat-fill",
  xml: "ri:code-s-slash-line",
  people: "ri:team-line",

  "menu-about": "ri:information-line",
  "menu-analyse": "ri:line-chart-line",
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
  "menu-result": "ri:bar-chart-box-line",
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
export function resolveIconForArtSvgIcon(stored?: string | null): string {
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
