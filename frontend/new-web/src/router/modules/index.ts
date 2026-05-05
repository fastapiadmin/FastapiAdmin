import { AppRouteRecord } from "@/types/router";
import { widgetsRoutes } from "./widgets";
import { exceptionRoutes } from "./exception";

/**
 * 导出所有模块化路由（业务菜单由后端动态下发；此处仅演示组件库与异常分组）
 */
export const routeModules: AppRouteRecord[] = [widgetsRoutes, exceptionRoutes];
