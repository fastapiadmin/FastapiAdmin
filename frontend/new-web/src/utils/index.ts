/**
 * 工具与横切能力统一导出入口
 *
 * 目录约定：按领域分子目录，各包以 `index.ts` 为入口（如 `http/`、`storage/`）。
 *
 * @module utils/index
 */

// 认证 & OAuth
export * from "./auth";
export * from "./oauth";

// 通用
export * from "./common";
export { default as download } from "./download";
export * from "./constants";
export * from "./form";
export * from "./i18n";

// 网络
export * from "./http";
export * from "./socket";

// 浏览器 / 系统
export * from "./storage";
export * from "./sys";
export * from "./ui";

// 路由与导航
export * from "./navigation";

// 数据展示
export * from "./table";

// 菜单与图标
export * from "./menuIcon";
