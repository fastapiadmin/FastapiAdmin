/**
 * 组件加载器
 *
 * 负责动态加载 Vue 组件
 *
 * @module router/core/ComponentLoader
 * @author FastapiAdmin Team
 */

import { defineComponent, h, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { IframeRouteManager } from "@/router/core/IframeRouteManager";
import {
  ROUTE_COMPONENT_LAYOUT,
  ROUTE_COMPONENT_NESTED_PARENT,
} from "@/router/routes/staticRoutes";

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

    /** 多级目录父级占位：返回内联 RouterView（不依赖 views 文件） */
    if (componentPath === ROUTE_COMPONENT_NESTED_PARENT) {
      return this.loadNestedParent();
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
    return () =>
      Promise.resolve(
        defineComponent({
          name: "IframeView",
          setup() {
            const route = useRoute();
            const isLoading = ref(true);
            const iframeUrl = ref("");
            const iframeRef = ref<HTMLIFrameElement | null>(null);

            onMounted(() => {
              const iframeRoute = IframeRouteManager.getInstance().findByPath(route.path);
              if (iframeRoute?.meta) {
                iframeUrl.value = (iframeRoute.meta as any).link || "";
              }
            });

            const handleIframeLoad = () => {
              isLoading.value = false;
            };

            return () =>
              h("div", { class: "box-border w-full h-full", "v-loading": isLoading.value }, [
                h("iframe", {
                  ref: iframeRef,
                  src: iframeUrl.value,
                  frameborder: "0",
                  class: "w-full h-full min-h-[calc(100vh-120px)] border-none",
                  onLoad: handleIframeLoad,
                }),
              ]);
          },
        })
      );
  }

  /**
   * 加载多级目录父级占位组件（内联 RouterView）
   */
  loadNestedParent(): () => Promise<any> {
    return () =>
      Promise.resolve(
        defineComponent({
          name: "NestedRouterParent",
          setup() {
            // 直接返回 RouterView，避免创建额外 views 占位文件
            return () => h("router-view");
          },
        })
      );
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
