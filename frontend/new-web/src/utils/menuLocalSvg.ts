/**
 * 本地 SVG：`assets/icons/*.svg` 文件名 → Vite 静态 URL。
 * 菜单等处若仅依赖 Tailwind 动态类 `` `i-svg:${name}` ``，构建时往往扫描不到类名，导致样式缺失；
 * 运行时通过 glob + ?url 保证一定能加载到资源。
 */
const raw = import.meta.glob("../assets/icons/*.svg", {
  eager: true,
  query: "?url",
  import: "default",
}) as Record<string, string>;

const urlByExactName = new Map<string, string>();

for (const [fullPath, url] of Object.entries(raw)) {
  const m = fullPath.match(/\/([^/]+)\.svg$/);
  if (m) {
    urlByExactName.set(m[1], url);
  }
}

export function resolveMenuLocalSvgUrl(iconBasename: string): string | undefined {
  const key = iconBasename.trim();
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
