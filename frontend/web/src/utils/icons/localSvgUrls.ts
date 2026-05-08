/**
 * 加载 `src/assets/images/svg/*.svg` 为 Vite 静态 URL。
 *
 * 构建时用 `import.meta.glob(..., { query: '?url' })` 固定打进产物，避免仅靠 Tailwind
 * 动态类名 `i-svg:*` 时扫描不到资源的问题。
 *
 * @module utils/icons/localSvgUrls
 */

const raw = import.meta.glob("../../assets/images/svg/*.svg", {
  eager: true,
  query: "?url",
  import: "default",
}) as Record<string, string>;

/** 文件名（不含 .svg）→ 打包后 URL */
const urlByExactName = new Map<string, string>();

for (const [fullPath, url] of Object.entries(raw)) {
  const m = fullPath.match(/\/([^/]+)\.svg$/);
  if (m) {
    urlByExactName.set(m[1], url);
  }
}

/**
 * 根据 `assets/images/svg` 下的 SVG **文件名（不含扩展名）** 解析为可给 `<img :src>` 使用的地址。
 * 支持大小写不敏感匹配（如 `Python` 与 `python.svg`）。
 *
 * @param basename 例如 `python`、`file-json`、`menu-home`
 * @returns 存在则返回 URL，否则 `undefined`
 */
export function resolveLocalIconUrl(basename: string): string | undefined {
  const key = basename.trim();
  if (!key) return undefined;

  const direct = urlByExactName.get(key);
  if (direct) return direct;

  const lower = key.toLowerCase();
  for (const [fileBase, url] of urlByExactName.entries()) {
    if (fileBase.toLowerCase() === lower) {
      return url;
    }
  }

  return undefined;
}

/** 是否能在本地 icons 目录找到对应 SVG */
export function hasLocalIconUrl(basename: string): boolean {
  return resolveLocalIconUrl(basename) !== undefined;
}

/** 当前构建中包含的所有本地 SVG 基名（不含 `.svg`），已排序 */
export function listLocalIconBasenames(): string[] {
  return [...urlByExactName.keys()].sort((a, b) => a.localeCompare(b));
}
