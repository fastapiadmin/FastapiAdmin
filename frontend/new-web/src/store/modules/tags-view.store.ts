/**
 * 标签页状态管理模块
 *
 * 提供标签页的状态管理和缓存机制
 *
 * ## 主要功能
 *
 * - 已访问视图列表管理
 * - 缓存视图列表管理
 * - 添加、删除、更新标签页
 * - 关闭当前标签页并跳转
 * - 关闭其他标签页/关闭左侧/关闭右侧
 * - 固定标签页支持
 *
 * ## 使用场景
 *
 * - 多标签页导航
 * - 页面缓存管理
 * - 标签页右键菜单操作
 * - 路由切换时的标签状态同步
 *
 * ## 核心特性
 *
 * - 支持固定标签（affix）
 * - 支持keepAlive缓存
 * - 关闭标签时自动跳转上一个标签
 * - 区分已访问视图和缓存视图
 *
 * @module store/modules/tags-view.store
 * @author FastapiAdmin Team
 */
import { defineStore } from "pinia";
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { store } from "@/store";

export const useTagsViewStore = defineStore(
  "tagsViewStore",
  () => {
    const visitedViews = ref<TagView[]>([]);
    const cachedViews = ref<string[]>([]);
    const router = useRouter();
    const route = useRoute();

    /**
     * 添加已访问视图到已访问视图列表中
     */
    function addVisitedView(view: TagView) {
      // 如果已经存在于已访问的视图列表中或者是重定向地址，则不再添加
      if (view.path.startsWith("/redirect")) {
        return;
      }
      if (visitedViews.value.some((v) => v.name === view.name)) {
        return;
      }
      // 如果视图是固定的（affix），则在已访问的视图列表的开头添加
      if (view.affix) {
        visitedViews.value.unshift(view);
      } else {
        // 如果视图不是固定的，则在已访问的视图列表的末尾添加
        visitedViews.value.push(view);
      }
    }

    /**
     * 添加缓存视图到缓存视图列表中
     */
    function addCachedView(view: TagView) {
      const viewName = view.name;
      // 如果缓存视图名称已经存在于缓存视图列表中，则不再添加
      if (cachedViews.value.includes(viewName)) {
        return;
      }

      // 如果视图需要缓存（keepAlive），则将其路由名称添加到缓存视图列表中
      if (view.keepAlive) {
        cachedViews.value.push(viewName);
      }
    }

    /**
     * 从已访问视图列表中删除指定的视图
     */
    function delVisitedView(view: TagView) {
      return new Promise((resolve) => {
        for (const [i, v] of visitedViews.value.entries()) {
          // 找到与指定视图路径匹配的视图，在已访问视图列表中删除该视图
          if (v.path === view.path) {
            visitedViews.value.splice(i, 1);
            break;
          }
        }
        resolve([...visitedViews.value]);
      });
    }

    function delCachedView(view: TagView) {
      const viewName = view.name;
      return new Promise((resolve) => {
        const index = cachedViews.value.indexOf(viewName);
        if (index > -1) {
          cachedViews.value.splice(index, 1);
        }
        resolve([...cachedViews.value]);
      });
    }
    function delOtherVisitedViews(view: TagView) {
      return new Promise((resolve) => {
        visitedViews.value = visitedViews.value.filter((v) => {
          return v?.affix || v.path === view.path;
        });
        resolve([...visitedViews.value]);
      });
    }

    function delOtherCachedViews(view: TagView) {
      const viewName = view.name as string;
      return new Promise((resolve) => {
        const index = cachedViews.value.indexOf(viewName);
        if (index > -1) {
          cachedViews.value = cachedViews.value.slice(index, index + 1);
        } else {
          // if index = -1, there is no cached tags
          cachedViews.value = [];
        }
        resolve([...cachedViews.value]);
      });
    }

    function updateVisitedView(view: TagView) {
      for (let v of visitedViews.value) {
        if (v.path === view.path) {
          v = Object.assign(v, view);
          break;
        }
      }
    }

    function addView(view: TagView) {
      addVisitedView(view);
      addCachedView(view);
    }

    function delView(view: TagView) {
      return new Promise((resolve) => {
        delVisitedView(view);
        delCachedView(view);
        resolve({
          visitedViews: [...visitedViews.value],
          cachedViews: [...cachedViews.value],
        });
      });
    }

    function delOtherViews(view: TagView) {
      return new Promise((resolve) => {
        delOtherVisitedViews(view);
        delOtherCachedViews(view);
        resolve({
          visitedViews: [...visitedViews.value],
          cachedViews: [...cachedViews.value],
        });
      });
    }

    function delLeftViews(view: TagView) {
      return new Promise((resolve) => {
        const currIndex = visitedViews.value.findIndex((v) => v.path === view.path);
        if (currIndex === -1) {
          return;
        }
        visitedViews.value = visitedViews.value.filter((item, index) => {
          if (index >= currIndex || item?.affix) {
            return true;
          }

          const cacheIndex = cachedViews.value.indexOf(item.name);
          if (cacheIndex > -1) {
            cachedViews.value.splice(cacheIndex, 1);
          }
          return false;
        });
        resolve({
          visitedViews: [...visitedViews.value],
        });
      });
    }

    function delRightViews(view: TagView) {
      return new Promise((resolve) => {
        const currIndex = visitedViews.value.findIndex((v) => v.path === view.path);
        if (currIndex === -1) {
          return;
        }
        visitedViews.value = visitedViews.value.filter((item, index) => {
          if (index <= currIndex || item?.affix) {
            return true;
          }
        });
        resolve({
          visitedViews: [...visitedViews.value],
        });
      });
    }

    function delAllViews() {
      return new Promise((resolve) => {
        const affixTags = visitedViews.value.filter((tag) => tag?.affix);
        visitedViews.value = affixTags;
        cachedViews.value = [];
        resolve({
          visitedViews: [...visitedViews.value],
          cachedViews: [...cachedViews.value],
        });
      });
    }

    function delAllVisitedViews() {
      return new Promise((resolve) => {
        const affixTags = visitedViews.value.filter((tag) => tag?.affix);
        visitedViews.value = affixTags;
        resolve([...visitedViews.value]);
      });
    }

    function delAllCachedViews() {
      return new Promise((resolve) => {
        cachedViews.value = [];
        resolve([...cachedViews.value]);
      });
    }

    /**
     * 关闭当前tagView
     */
    function closeCurrentView() {
      const tags: TagView = {
        name: route.name as string,
        title: route.meta.title as string,
        path: route.path,
        fullPath: route.fullPath,
        affix: route.meta?.affix,
        keepAlive: route.meta?.keepAlive,
        query: route.query,
      };
      delView(tags).then((res: any) => {
        if (isActive(tags)) {
          toLastView(res.visitedViews, tags);
        }
      });
    }

    function isActive(tag: TagView) {
      return tag.path === route.path;
    }

    function toLastView(visitedViews: TagView[], view?: TagView) {
      const latestView = visitedViews.slice(-1)[0];
      if (latestView && latestView.fullPath) {
        router.push(latestView.fullPath);
      } else {
        // now the default is to redirect to the home page if there is no tags-view,
        // you can adjust it according to your needs.
        const vn = view?.name != null ? String(view.name) : "";
        if (
          vn === "Home" ||
          vn === "Workplace" ||
          vn === "Dashboard" ||
          vn.startsWith("Dashboard")
        ) {
          // to reload home page
          if (view?.fullPath) {
            router.replace("/redirect" + view.fullPath);
          } else {
            router.push("/");
          }
        } else {
          router.push("/");
        }
      }
    }

    return {
      visitedViews,
      cachedViews,
      addVisitedView,
      addCachedView,
      delVisitedView,
      delCachedView,
      delOtherVisitedViews,
      delOtherCachedViews,
      updateVisitedView,
      addView,
      delView,
      delOtherViews,
      delLeftViews,
      delRightViews,
      delAllViews,
      delAllVisitedViews,
      delAllCachedViews,
      closeCurrentView,
      isActive,
      toLastView,
    };
  },
  {
    persist: true,
  }
);

export function useTagsViewStoreHook() {
  return useTagsViewStore(store);
}
