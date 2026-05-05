/**
 * 公共路由别名
 * 存放系统级公共路由路径，如布局容器、登录页等
 */
export enum RoutesAlias {
  Layout = "/index/index", // 布局容器
  /** 嵌套目录父级：仅渲染子路由，避免二层及以下重复使用完整 Layout */
  NestedRouterParent = "/nested/router-view-parent",
  Login = "/auth/login", // 登录页
}
