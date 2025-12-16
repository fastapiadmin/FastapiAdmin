<template>
  <div ref="tags-container" class="tags-container">
    <!-- 向左移动按钮 -->
    <el-icon class="btn" @click="scrollLeft">
      <DArrowLeft />
    </el-icon>

    <!-- 标签导航容器 -->
    <nav role="navigation" class="scroll-wrapper">
      <el-scrollbar ref="scrollbarRef" class="scroll-container" @wheel="handleScroll">
        <VueDraggable v-model="visitedViews" :animation="150">
          <router-link
            v-for="tag in displayedViews"
            :key="tag.fullPath"
            :class="['tags-item', { active: tagsViewStore.isActive(tag) }]"
            :to="{ path: tag.path, query: tag.query }"
            @click="tagSwitchSource = 'tab'"
            @click.middle="handleMiddleClick(tag)"
          >
            <!-- 为所有标签添加右键菜单 -->
            <el-dropdown
              trigger="contextmenu"
              @visible-change="(visible) => onContextMenuVisibleChange(visible, tag)"
              @click.stop
            >
              <span class="tag-text">{{ translateRouteTitle(tag.title) }}</span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="refreshSelectedTag(tag)">
                    <el-icon>
                      <Refresh />
                    </el-icon>
                    {{ t("navbar.refresh") }}
                  </el-dropdown-item>

                  <el-dropdown-item
                    :disabled="tag.affix || visitedViews.length <= 1"
                    @click="closeSelectedTag(tag)"
                  >
                    <el-icon>
                      <Close />
                    </el-icon>
                    {{ t("navbar.close") }}
                  </el-dropdown-item>

                  <el-dropdown-item :disabled="isFirstView(tag)" @click="closeLeftTags(tag)">
                    <el-icon>
                      <Back />
                    </el-icon>
                    {{ t("navbar.closeLeft") }}
                  </el-dropdown-item>

                  <el-dropdown-item :disabled="isLastView(tag)" @click="closeRightTags(tag)">
                    <el-icon>
                      <Right />
                    </el-icon>
                    {{ t("navbar.closeRight") }}
                  </el-dropdown-item>

                  <el-dropdown-item
                    :disabled="visitedViews.length <= 1"
                    @click="closeOtherTags(tag)"
                  >
                    <el-icon>
                      <Remove />
                    </el-icon>
                    {{ t("navbar.closeOther") }}
                  </el-dropdown-item>

                  <el-dropdown-item :disabled="visitedViews.length <= 1" @click="closeAllTags(tag)">
                    <el-icon>
                      <Minus />
                    </el-icon>
                    {{ t("navbar.closeAll") }}
                  </el-dropdown-item>

                  <!-- 收藏到快速开始 -->
                  <el-dropdown-item divided @click="toggleQuickStart(tag)">
                    <el-icon>
                      <Star v-if="!isQuickLinkExists(tag)" />
                      <StarFilled v-else />
                    </el-icon>
                    {{ isQuickLinkExists(tag) ? "取消收藏" : "收藏" }}
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>

            <span
              v-if="!tag.affix"
              class="tag-close-btn"
              @click.prevent.stop="closeSelectedTag(tag)"
            >
              <el-icon>
                <Close />
              </el-icon>
            </span>
          </router-link>
        </VueDraggable>
      </el-scrollbar>
    </nav>

    <!-- 向右移动按钮 -->
    <el-icon class="btn" @click="scrollRight">
      <DArrowRight />
    </el-icon>

    <!-- 刷新按钮 -->
    <el-icon class="btn" @click="handleAction('refreshCache')">
      <RefreshRight />
    </el-icon>

    <!-- 设置按钮 -->
    <el-dropdown class="btn" trigger="click">
      <el-icon>
        <Setting />
      </el-icon>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item @click="handleAction('refresh')">
            <el-icon>
              <Refresh />
            </el-icon>
            {{ t("navbar.refresh") }}
          </el-dropdown-item>

          <el-dropdown-item v-if="!selectedTag?.affix" @click="handleAction('close')">
            <el-icon>
              <Close />
            </el-icon>
            {{ t("navbar.close") }}
          </el-dropdown-item>

          <el-dropdown-item
            :disabled="isFirstView(routePathMap.get(route.path))"
            @click="handleAction('closeLeft')"
          >
            <el-icon>
              <Back />
            </el-icon>
            {{ t("navbar.closeLeft") }}
          </el-dropdown-item>

          <el-dropdown-item
            :disabled="isLastView(routePathMap.get(route.path))"
            @click="handleAction('closeRight')"
          >
            <el-icon>
              <Right />
            </el-icon>
            {{ t("navbar.closeRight") }}
          </el-dropdown-item>

          <el-dropdown-item
            :disabled="visitedViews.length <= 1"
            @click="handleAction('closeOther')"
          >
            <el-icon>
              <Remove />
            </el-icon>
            {{ t("navbar.closeOther") }}
          </el-dropdown-item>

          <el-dropdown-item @click="handleAction('closeAll')">
            <el-icon>
              <Minus />
            </el-icon>
            {{ t("navbar.closeAll") }}
          </el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter, type RouteRecordRaw } from "vue-router";
import { resolve } from "path-browserify";
import { translateRouteTitle } from "@/utils/i18n";
import { refreshAppCaches, usePermissionStore, useTagsViewStore } from "@/store";
import { VueDraggable } from "vue-draggable-plus";
import { quickStartManager } from "@/utils/quickStartManager";
import { ElMessage } from "element-plus";

const { t } = useI18n();

const router = useRouter();
const route = useRoute();

// 状态管理
const permissionStore = usePermissionStore();
const tagsViewStore = useTagsViewStore();

const { visitedViews } = storeToRefs(tagsViewStore);

// 简单的标签显示逻辑
const displayedViews = computed(() => {
  return visitedViews.value;
});

// 当前选中的标签
const selectedTag = ref<TagView | null>(null);

// 滚动条引用
const scrollbarRef = ref();

// 标签切换来源跟踪
const tagSwitchSource = ref<"menu" | "tab" | null>(null);

// 路由映射缓存，提升查找性能
const routePathMap = new Map<string, TagView>();

// 更新路由映射缓存
const updateRoutePathMap = () => {
  routePathMap.clear();
  visitedViews.value.forEach((tag) => {
    routePathMap.set(tag.path, tag);
  });
};

// 判断是否为第一个标签
const isFirstView = (tag?: TagView) => {
  if (tag) {
    // 传入特定标签时使用传入的标签
    return tag.path === "/" || tag.fullPath === visitedViews.value[1]?.fullPath;
  } else {
    // 未传入标签时使用当前激活标签（向后兼容）
    const currentTag = routePathMap.get(route.path);
    if (!currentTag) return false;
    return currentTag.path === "/" || currentTag.fullPath === visitedViews.value[1]?.fullPath;
  }
};

// 判断是否为最后一个标签
const isLastView = (tag?: TagView) => {
  if (tag) {
    // 传入特定标签时使用传入的标签
    return tag.fullPath === visitedViews.value[visitedViews.value.length - 1]?.fullPath;
  } else {
    // 未传入标签时使用当前激活标签（向后兼容）
    const currentTag = routePathMap.get(route.path);
    if (!currentTag) return false;
    return currentTag.fullPath === visitedViews.value[visitedViews.value.length - 1]?.fullPath;
  }
};

/**
 * 递归提取固定标签
 */
const extractAffixTags = (routes: RouteRecordRaw[], basePath = "/"): TagView[] => {
  const affixTags: TagView[] = [];

  const traverse = (routeList: RouteRecordRaw[], currentBasePath: string) => {
    routeList.forEach((route) => {
      const fullPath = resolve(currentBasePath, route.path);

      // 如果是固定标签，添加到列表
      if (route.meta?.affix) {
        affixTags.push({
          path: fullPath,
          fullPath,
          name: String(route.name || ""),
          title: route.meta.title || "no-name",
          affix: true,
          keepAlive: route.meta.keepAlive || false,
        });
      }

      // 递归处理子路由
      if (route.children?.length) {
        traverse(route.children, fullPath);
      }
    });
  };

  traverse(routes, basePath);
  return affixTags;
};

/**
 * 初始化固定标签
 */
const initAffixTags = () => {
  const affixTags = extractAffixTags(permissionStore.routes);

  affixTags.forEach((tag) => {
    if (tag.name) {
      tagsViewStore.addVisitedView(tag);
    }
  });
};

/**
 * 添加当前路由标签
 */
const addCurrentTag = () => {
  if (!route.meta?.title) return;

  // 检查标签是否已存在
  const existingTag = visitedViews.value.find((tag) => tag.path === route.path);

  if (existingTag) {
    // 如果标签已存在，根据来源决定是否移动位置
    if (!existingTag.affix) {
      if (tagSwitchSource.value === "menu") {
        // 通过菜单点击：移动到最新位置
        const index = visitedViews.value.findIndex((tag) => tag.path === route.path);
        if (index !== -1) {
          const tag = visitedViews.value.splice(index, 1)[0];
          visitedViews.value.push(tag);
        }
      }
      // 通过标签容器点击：不移动位置，只激活
    }
  } else {
    // 添加新标签
    tagsViewStore.addView({
      name: route.name as string,
      title: route.meta.title,
      path: route.path,
      fullPath: route.fullPath,
      icon: (route as any).icon || route.meta?.icon,
      affix: route.meta.affix || false,
      keepAlive: route.meta.keepAlive || false,
      query: route.query,
    });
  }

  // 根据来源决定是否滚动
  if (tagSwitchSource.value === "menu") {
    // 通过菜单点击：滚动到最新标签
    nextTick(() => {
      autoScrollToLatestTag();
    });
  }
  // 通过标签容器点击：不滚动，保持当前位置

  // 重置来源状态
  tagSwitchSource.value = null;
};

/**
 * 更新当前标签
 */
const updateCurrentTag = () => {
  nextTick(() => {
    const currentTag = routePathMap.get(route.path);

    if (currentTag && currentTag.fullPath !== route.fullPath) {
      tagsViewStore.updateVisitedView({
        name: route.name as string,
        title: route.meta?.title || "",
        path: route.path,
        fullPath: route.fullPath,
        icon: (route as any).icon || route.meta?.icon,
        affix: route.meta?.affix || false,
        keepAlive: route.meta?.keepAlive || false,
        query: route.query,
      });
    }
  });
};

/**
 * 处理中键点击
 */
const handleMiddleClick = (tag: TagView) => {
  if (!tag.affix) {
    closeSelectedTag(tag);
  }
};

/**
 * 处理滚轮事件（优化后）
 */
const handleScroll = (event: WheelEvent) => {
  const scrollWrapper = scrollbarRef.value?.wrapRef;
  if (!scrollWrapper) return;

  // 检查是否有水平或垂直滚动
  const hasHorizontalScroll = scrollWrapper.scrollWidth > scrollWrapper.clientWidth;
  const hasVerticalScroll = scrollWrapper.scrollHeight > scrollWrapper.clientHeight;

  if (!hasHorizontalScroll && !hasVerticalScroll) return;

  const deltaY = event.deltaY || -(event as any).wheelDelta || 0;
  const deltaX = event.deltaX || 0;

  // 计算新的滚动位置
  const newScrollLeft = Math.max(
    0,
    Math.min(
      scrollWrapper.scrollWidth - scrollWrapper.clientWidth,
      scrollWrapper.scrollLeft + deltaX
    )
  );
  const newScrollTop = Math.max(
    0,
    Math.min(
      scrollWrapper.scrollHeight - scrollWrapper.clientHeight,
      scrollWrapper.scrollTop + deltaY
    )
  );

  scrollbarRef.value.setScrollLeft(newScrollLeft);
  scrollbarRef.value.setScrollTop(newScrollTop); // 新增垂直滚动支持
};

/**
 * 刷新标签
 */
const refreshSelectedTag = (tag: TagView | null) => {
  if (!tag) return;
  // 总是使用当前路由对应的标签
  // const currentTag = routePathMap.value.get(route.path);
  // if (!currentTag) return;

  tagsViewStore.delCachedView(tag);
  nextTick(() => {
    router.replace("/redirect" + tag.fullPath);
  });
};

/**
 * 关闭标签
 */
const closeSelectedTag = (tag: TagView | null) => {
  // 如果传入了具体的标签，使用传入的标签；否则使用当前路由对应的标签
  const targetTag = tag || routePathMap.get(route.path);
  if (!targetTag) return;

  tagsViewStore.delView(targetTag).then((result: any) => {
    if (tagsViewStore.isActive(targetTag)) {
      tagsViewStore.toLastView(result.visitedViews, targetTag);
    }
    // 关闭标签后重置滚动状态，以便下次可以重新判断是否需要滚动
    nextTick(() => {
      resetScrollState();
    });
  });
};

/**
 * 关闭左侧标签
 */
const closeLeftTags = (tag?: TagView) => {
  const targetTag = tag || selectedTag.value || routePathMap.get(route.path);
  if (!targetTag) return;

  tagsViewStore.delLeftViews(targetTag).then((result: any) => {
    const hasCurrentRoute = result.visitedViews.some((item: TagView) => item.path === route.path);

    if (!hasCurrentRoute) {
      tagsViewStore.toLastView(result.visitedViews);
    }
    // 关闭标签后重置滚动状态
    nextTick(() => {
      resetScrollState();
    });
  });
};

/**
 * 关闭右侧标签
 */
const closeRightTags = (tag?: TagView) => {
  const targetTag = tag || selectedTag.value || routePathMap.get(route.path);
  if (!targetTag) return;

  tagsViewStore.delRightViews(targetTag).then((result: any) => {
    const hasCurrentRoute = result.visitedViews.some((item: TagView) => item.path === route.path);

    if (!hasCurrentRoute) {
      tagsViewStore.toLastView(result.visitedViews);
    }
    // 关闭标签后重置滚动状态
    nextTick(() => {
      resetScrollState();
    });
  });
};

/**
 * 关闭其他标签
 */
const closeOtherTags = (tag?: TagView) => {
  const targetTag = tag || selectedTag.value || routePathMap.get(route.path);
  if (!targetTag) return;

  router.push(targetTag);
  tagsViewStore.delOtherViews(targetTag).then(() => {
    updateCurrentTag();
    // 关闭标签后重置滚动状态
    nextTick(() => {
      resetScrollState();
    });
  });
};

/**
 * 关闭所有标签
 */
const closeAllTags = (tag?: TagView) => {
  tagsViewStore.delAllViews().then((result: any) => {
    tagsViewStore.toLastView(result.visitedViews, tag || undefined);
    // 关闭所有标签后重置滚动状态
    nextTick(() => {
      resetScrollState();
    });
  });
};

/**
 * 统一处理标签操作
 */
const handleAction = async (action: string) => {
  // 总是使用当前路由对应的标签
  const currentTag = routePathMap.get(route.path);
  if (!currentTag) return;

  switch (action) {
    case "refresh":
      refreshSelectedTag(currentTag);
      break;
    case "close":
      closeSelectedTag(currentTag);
      break;
    case "closeRight":
      closeRightTags();
      break;
    case "closeLeft":
      closeLeftTags();
      break;
    case "closeOther":
      closeOtherTags();
      break;
    case "closeAll":
      closeAllTags(currentTag);
      break;
    case "refreshCache":
      try {
        // 1) 刷新服务端缓存（用户/权限/配置/公告/按需字典）并重建路由
        await refreshAppCaches();
        // 2) 软刷新当前页面，重新加载组件
        refreshSelectedTag(currentTag);
        // 3) 提示成功
        ElMessage.success(t("navbar.refreshCache") + "完成");
      } catch (error) {
        console.error("刷新缓存失败:", error);
        ElMessage.error("刷新失败");
      }
      break;
    default:
      console.warn(`Unknown action: ${action}`);
  }
};

/**
 * 右键菜单显示状态变化处理函数
 */
const onContextMenuVisibleChange = (visible: boolean, tag?: TagView) => {
  if (visible) {
    // 设置当前右键点击的标签
    selectedTag.value = tag || routePathMap.get(route.path) || null;
  } else {
    // 关闭菜单时清空选择
    selectedTag.value = null;
  }
};

/**
 * 切换快速开始收藏状态
 */
const toggleQuickStart = (tag: TagView) => {
  try {
    const href = tag.fullPath || tag.path;
    const isExists = quickStartManager.isLinkExists(href);

    if (isExists) {
      // 取消收藏：找到对应的链接并删除
      const links = quickStartManager.getQuickLinks();
      const targetLink = links.find((link) => link.href === href);
      if (targetLink?.id) {
        quickStartManager.removeQuickLink(targetLink.id);
        ElMessage.success(`已取消收藏：${tag.title}`);
      }
    } else {
      // 添加收藏
      const quickLink = quickStartManager.createQuickLinkFromRoute(tag);
      quickStartManager.addQuickLink(quickLink);
      ElMessage.success(`已收藏：${tag.title}`);
    }
  } catch (error) {
    console.error("Failed to toggle quick start:", error);
    ElMessage.error("操作失败");
  }
};

/**
 * 检查快速链接是否已存在
 */
const isQuickLinkExists = (tag: TagView): boolean => {
  return quickStartManager.isLinkExists(tag.fullPath || tag.path);
};

/**
 * 向左滚动标签页
 */
const scrollLeft = () => {
  const scrollWrapper = scrollbarRef.value?.wrapRef;
  if (!scrollWrapper) return;

  const newScrollLeft = Math.max(0, scrollWrapper.scrollLeft - 200);
  scrollbarRef.value.setScrollLeft(newScrollLeft);
};

/**
 * 向右滚动标签页
 */
const scrollRight = () => {
  const scrollWrapper = scrollbarRef.value?.wrapRef;
  if (!scrollWrapper) return;

  const maxScrollLeft = scrollWrapper.scrollWidth - scrollWrapper.clientWidth;
  const newScrollLeft = Math.min(maxScrollLeft, scrollWrapper.scrollLeft + 200);
  scrollbarRef.value.setScrollLeft(newScrollLeft);

  // 如果滚动到最右边，重置滚动状态以允许下次自动滚动
  if (newScrollLeft >= maxScrollLeft - 1) {
    scrollState.value.hasScrolledToLatest = false;
  }
};

/**
 * 重置滚动状态
 */
const resetScrollState = () => {
  scrollState.value.hasScrolledToLatest = false;
  scrollState.value.isContainerFull = false;
};

// 滚动状态跟踪
const scrollState = ref({
  hasScrolledToLatest: false, // 是否已经滚动到最新标签
  isContainerFull: false, // 容器是否已满
});

/**
 * 自动滚动到最新标签或确保当前激活标签可见
 */
const autoScrollToLatestTag = () => {
  const scrollWrapper = scrollbarRef.value?.wrapRef;
  if (!scrollWrapper) return;

  // 获取容器宽度和内容宽度
  const containerWidth = scrollWrapper.clientWidth;
  const contentWidth = scrollWrapper.scrollWidth;

  // 判断容器是否已满（内容宽度是否超过容器宽度）
  const isContainerFull = contentWidth > containerWidth;

  // 查找当前激活的标签元素
  const activeTagElement = document.querySelector(".tags-item.active");

  if (activeTagElement) {
    // 将Element类型断言为HTMLElement类型以访问offsetWidth属性
    const activeHtmlElement = activeTagElement as HTMLElement;
    // 计算激活标签的位置信息
    const activeTagRect = activeHtmlElement.getBoundingClientRect();
    const containerRect = scrollWrapper.getBoundingClientRect();

    // 计算标签相对于容器的位置
    const tagLeft = activeTagRect.left - containerRect.left + scrollWrapper.scrollLeft;
    const tagRight = tagLeft + activeHtmlElement.offsetWidth;

    // 检查标签是否完全在可见区域内
    if (
      tagLeft < scrollWrapper.scrollLeft ||
      tagRight > scrollWrapper.scrollLeft + containerWidth
    ) {
      // 如果标签不在可见区域内，滚动到使标签居中的位置
      const targetScrollLeft = tagLeft - (containerWidth - activeHtmlElement.offsetWidth) / 2;
      const maxScrollLeft = contentWidth - containerWidth;
      const minScrollLeft = 0;
      const clampedScrollLeft = Math.max(minScrollLeft, Math.min(maxScrollLeft, targetScrollLeft));

      scrollbarRef.value.setScrollLeft(clampedScrollLeft);
      scrollState.value.hasScrolledToLatest = true;
      scrollState.value.isContainerFull = isContainerFull;
      return;
    }
  }

  // 如果没有找到激活标签或激活标签已经在可见区域内，则使用原来的逻辑
  if (isContainerFull && !scrollState.value.hasScrolledToLatest) {
    // 计算需要滚动到的位置，确保最新标签在右侧可见
    const maxScrollLeft = contentWidth - containerWidth;
    scrollbarRef.value.setScrollLeft(maxScrollLeft);
    scrollState.value.hasScrolledToLatest = true;
    scrollState.value.isContainerFull = true;
  } else if (!isContainerFull) {
    // 如果内容宽度不超过容器宽度，滚动到最左边
    scrollbarRef.value.setScrollLeft(0);
    // 重置滚动状态
    scrollState.value.hasScrolledToLatest = false;
    scrollState.value.isContainerFull = false;
  }
};

// 监听路由变化
watch(
  route,
  () => {
    // 如果没有设置来源，则默认为菜单点击
    if (tagSwitchSource.value === null) {
      tagSwitchSource.value = "menu";
    }
    addCurrentTag();
    updateCurrentTag();
    updateRoutePathMap();
  },
  { immediate: true }
);

// 监听容器大小变化
let resizeObserver: ResizeObserver | null = null;

// 监听标签数量变化，自动滚动到最新标签（新标签添加时）
watch(
  () => visitedViews.value.length,
  () => {
    // 更新路由映射缓存
    updateRoutePathMap();

    // 只有在通过菜单添加新标签时才滚动
    if (tagSwitchSource.value === "menu") {
      nextTick(() => {
        autoScrollToLatestTag();
      });
    }
  }
);

// 监听当前路由变化，确保路由切换时自动滚动到当前标签
watch(
  () => route.path,
  () => {
    nextTick(() => {
      autoScrollToLatestTag();
    });
  }
);

// 初始化
onMounted(() => {
  initAffixTags();

  // 初始化路由映射缓存
  updateRoutePathMap();

  // 监听容器大小变化
  const tagsContainer = document.querySelector(".tags-container");
  if (tagsContainer && window.ResizeObserver) {
    resizeObserver = new ResizeObserver(() => {
      // 强制重新计算 displayedViews
      nextTick(() => {
        autoScrollToLatestTag();
      });
    });
    resizeObserver.observe(tagsContainer);
  }
});

// 清理
onUnmounted(() => {
  if (resizeObserver) {
    resizeObserver.disconnect();
  }
});
</script>

<style lang="scss" scoped>
.tags-container {
  display: flex;
  align-items: center;
  width: 100%;
  height: $tags-view-height;
  background-color: var(--el-bg-color);
  border: 1px solid var(--el-border-color-light);
  box-shadow: 0 1px 1px var(--el-box-shadow-light);

  .btn {
    top: 1px;
    left: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    width: $tags-view-height;
    height: $tags-view-height;
    cursor: pointer;
    border: 1px solid var(--el-border-color-light);

    &:hover {
      color: var(--el-color-primary);
      background-color: var(--el-fill-color-light);

      .el-icon {
        transform: scale(1.1);
      }
    }
  }

  .scroll-wrapper {
    flex: 1;
    overflow: hidden;
  }

  .scroll-container {
    white-space: nowrap;
  }

  .tags-item {
    position: relative;
    display: inline-flex;
    align-items: center;
    height: 26px;
    padding: 0 8px;
    margin-left: 5px;
    font-size: 12px;
    line-height: 26px;
    color: var(--el-text-color-primary);
    background: var(--el-bg-color);
    border: 1px solid var(--el-border-color);
    transition: all 0.2s ease;

    &:first-of-type {
      margin-left: 5px;
    }
    &:last-of-type {
      margin-right: 5px;
    }

    &:hover {
      background-color: var(--el-fill-color);
    }

    .tag-text {
      display: inline-block;
      vertical-align: middle;
    }

    .tag-close-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 16px;
      height: 16px;
      margin-left: 5px;
      font-size: 12px;
      font-weight: bold;
      color: var(--el-text-color-secondary);
      cursor: pointer;
      border-radius: 50%;
      transition: all 0.2s ease;

      &:hover {
        color: var(--el-color-white);
        background-color: var(--el-text-color-placeholder);
      }
    }

    &.active {
      color: var(--el-color-white);
      background-color: var(--el-color-primary);
      border-color: var(--el-color-primary);

      &::before {
        position: relative;
        display: inline-block;
        width: 8px;
        height: 8px;
        margin-right: 2px;
        content: "";
        background: var(--el-color-white);
        border-radius: 50%;
      }

      .tag-text {
        color: var(--el-color-white);
      }

      .tag-close-btn {
        color: var(--el-color-white);

        &:hover {
          color: var(--el-color-white);
        }
      }
    }
  }
}
</style>
