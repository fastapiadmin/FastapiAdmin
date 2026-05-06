/**
 * 组件加载器
 *
 * 负责动态加载 Vue 组件
 *
 * @module router/core/ComponentLoader
 * @author FastapiAdmin Team
 */

import { h } from "vue";
import { ROUTE_COMPONENT_LAYOUT } from "@/router/routes/staticRoutes";

export class ComponentLoader {
  private modules: Record<string, () => Promise<any>>;

  constructor() {
    // 动态导入 views 目录下所有 .vue 组件
    this.modules = import.meta.glob("../../views/**/*.vue");
  }

  /**
   * 加载组件
   */
  load(componentPath: string): () => Promise<any> {
    if (!componentPath) {
      return this.createEmptyComponent();
    }

    /** 布局别名指向 `@/layouts/index.vue`（勿写成 `/layouts/index`，会在 views 下误解析） */
    if (componentPath === ROUTE_COMPONENT_LAYOUT || componentPath === "/layouts/index") {
      return this.loadLayout();
    }

    const normalized = componentPath.startsWith("/")
      ? componentPath
      : `/${componentPath.replace(/^\/+/, "")}`;

    // 构建可能的路径（后端常为 dashboard/workplace，需补前导 /）
    const fullPath = `../../views${normalized}.vue`;
    const fullPathWithIndex = `../../views${normalized}/index.vue`;

    // 先尝试直接路径，再尝试添加/index的路径
    const module = this.modules[fullPath] || this.modules[fullPathWithIndex];

    if (!module) {
      console.error(
        `[ComponentLoader] 未找到组件: ${componentPath}，尝试过的路径: ${fullPath} 和 ${fullPathWithIndex}`
      );
      return this.createErrorComponent(componentPath);
    }

    return module;
  }

  /**
   * 加载布局组件
   */
  loadLayout(): () => Promise<any> {
    return () => import("@/layouts/index.vue");
  }

  /**
   * 加载 iframe 组件
   */
  loadIframe(): () => Promise<any> {
    return () => import("@/views/outside/Iframe.vue");
  }

  /**
   * 创建空组件
   */
  private createEmptyComponent(): () => Promise<any> {
    return () =>
      Promise.resolve({
        render() {
          return h("div", {});
        },
      });
  }

  /**
   * 创建错误提示组件
   */
  private createErrorComponent(componentPath: string): () => Promise<any> {
    return () =>
      Promise.resolve({
        render() {
          return h("div", { class: "route-error" }, `组件未找到: ${componentPath}`);
        },
      });
  }
}
