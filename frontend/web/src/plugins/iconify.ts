/**
 * 本地注册 Iconify 图标集，实现离线显示（不再从 CDN 加载）
 *
 * 优化策略：图标集改为异步加载，避免首屏阻塞
 * 通过 initIconifyAsync() 在 App.vue 中提前触发预加载
 */
import { addCollection } from "@iconify/vue";

// 缓存已加载的图标集
const loadedCollections = new Set<string>();

// 动态加载单个图标集
async function loadCollection(
  name: string,
  loader: () => Promise<{ default: any }>
): Promise<void> {
  if (loadedCollections.has(name)) return;
  try {
    const { default: collection } = await loader();
    addCollection(collection);
    loadedCollections.add(name);
  } catch (error) {
    console.error(`[Iconify] 加载图标集 ${name} 失败:`, error);
  }
}

/**
 * 异步加载完整图标集
 * 在 App.vue onMounted 中调用，利用空闲时间预加载
 */
export async function initIconifyAsync(): Promise<void> {
  await Promise.all([
    loadCollection("ri", () => import("@iconify-json/ri/icons.json")),
    loadCollection("svg-spinners", () => import("@iconify-json/svg-spinners/icons.json")),
    loadCollection("line-md", () => import("@iconify-json/line-md/icons.json")),
  ]);
}
