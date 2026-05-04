import { AppRouteRecord } from "@/types/router";
import { widgetsRoutes } from "./widgets";
import { systemRoutes } from "./system";
import { exceptionRoutes } from "./exception";

/**
 * 导出所有模块化路由
 */
export const routeModules: AppRouteRecord[] = [widgetsRoutes, systemRoutes, exceptionRoutes];
