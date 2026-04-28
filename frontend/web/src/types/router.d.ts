import 'vue-router';
import { RouteRecordRaw } from 'vue-router';

declare module 'vue-router' {
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
     * 是否在面包屑导航中隐藏
     * true 隐藏, false 显示
     * @default false
     */
    breadcrumb?: boolean;
  }
}

export interface RouteMeta extends Record<string | number | symbol, unknown> {
  /** 路由标题 */
  title: string;
  /** 路由图标 */
  icon?: string;
  /** 是否显示徽章 */
  showBadge?: boolean;
  /** 文本徽章 */
  showTextBadge?: string;
  /** 是否在菜单中隐藏 */
  isHide?: boolean;
  /** 是否在标签页中隐藏 */
  isHideTab?: boolean;
  /** 外部链接 */
  link?: string;
  /** 是否为iframe */
  isIframe?: boolean;
  /** 是否缓存 */
  keepAlive?: boolean;
  /** 操作权限 */
  authList?: Array<{
    title: string;
    authMark: string;
  }>;
  /** 是否为一级菜单 */
  isFirstLevel?: boolean;
  /** 角色权限 */
  roles?: string[];
  /** 是否固定标签页 */
  fixedTab?: boolean;
  /** 激活菜单路径 */
  activePath?: string;
  /** 是否为全屏页面 */
  isFullPage?: boolean;
  /** 是否为权限按钮行 */
  isAuthButton?: boolean;
  /** 权限标识 */
  authMark?: string;
  /** 父级路径 */
  parentPath?: string;
}

export interface AppRouteRecord extends Omit<RouteRecordRaw, 'meta' | 'children' | 'component'> {
  id?: number;
  meta: RouteMeta;
  children?: AppRouteRecord[];
  component?: string | (() => Promise<any>);
}
