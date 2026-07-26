import "vue-router";
import type { RouteRecordRaw } from "vue-router";

/** 路由元数据接口 */
export interface RouteMeta extends Record<string | number | symbol, unknown> {
  title: string;
  icon?: string;
  showBadge?: boolean;
  showTextBadge?: string;
  isHide?: boolean;
  isHideTab?: boolean;
  link?: string;
  isIframe?: boolean;
  keepAlive?: boolean;
  authList?: Array<{ title: string; authMark: string }>;
  isFirstLevel?: boolean;
  roles?: string[];
  fixedTab?: boolean;
  activePath?: string;
  isAuthButton?: boolean;
  authMark?: string;
  parentPath?: string;
  shellRoute?: boolean;
  remountOnFullPath?: boolean;
  scope?: "web" | "app";
}

/** 应用路由记录接口 */
export interface AppRouteRecord extends Omit<RouteRecordRaw, "meta" | "children" | "component"> {
  id?: number;
  meta: RouteMeta;
  children?: AppRouteRecord[];
  component?: string | (() => Promise<any>);
}

// from types/router/index.ts
declare module "vue-router" {
  // https://router.vuejs.org/zh/guide/advanced/meta.html#typescript
  // 可以通过扩展 RouteMeta 接口来输入 meta 字段
  interface RouteMeta {
    /**
     * 菜单名称
     * @example 'Dashboard'
     */
    title?: string;

    /**
     * 菜单图标
     * @example 'el-icon-edit'
     */
    icon?: string;

    /**
     * 是否隐藏菜单
     * true 隐藏, false 显示
     * @default false
     */
    hidden?: boolean;
    /**
     * 始终显示父级菜单，即使只有一个子菜单
     * true 显示父级菜单, false 隐藏父级菜单，显示唯一子节点
     * @default false
     */
    alwaysShow?: boolean;

    /**
     * 是否固定在页签上
     * true 固定, false 不固定
     * @default false
     */
    affix?: boolean;

    /**
     * 是否缓存页面
     * true 缓存, false 不缓存
     * @default false
     */
    keepAlive?: boolean;
    /**
     * 为 true 时 KeepAlive 子组件 `:key` 使用 `fullPath`（query/hash 变化会整页重挂载）。
     * 默认用 `name + params`，减轻 query 微调导致的重复 onMounted / useTable immediate。
     */
    remountOnFullPath?: boolean;

    /**
     * 静态壳层路由（路由已在 router 注册，菜单项仅用于跳转，无 component 字段）
     */
    shellRoute?: boolean;

    /**
     * 是否在面包屑导航中隐藏
     * true 隐藏, false 显示
     * @default false
     */
    breadcrumb?: boolean;
  }
}
