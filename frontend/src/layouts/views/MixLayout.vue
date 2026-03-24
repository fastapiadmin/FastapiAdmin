<template>
  <BaseLayout>
    <!-- 顶部菜单栏 -->
    <div class="layout__header">
      <div class="layout__header-content">
        <!-- Logo区域 -->
        <div v-if="isShowLogo" class="layout__header-logo">
          <AppLogo :collapse="isLogoCollapsed" />
        </div>

        <!-- 顶部菜单区域 -->
        <div class="layout__header-menu">
          <MixTopMenu />
        </div>

        <!-- 右侧操作区域 -->
        <div class="layout__header-actions">
          <NavbarActions />
        </div>
      </div>
    </div>

    <!-- 主内容区容器 -->
    <div class="layout__container">
      <!-- 左侧菜单栏 -->
      <div class="layout__sidebar--left" :class="{ 'layout__sidebar--collapsed': !isSidebarOpen }">
        <el-scrollbar>
          <el-menu
            :default-active="activeLeftMenuPath"
            :collapse="!isSidebarOpen"
            :collapse-transition="false"
            :unique-opened="false"
            background-color="var(--layout-menu-bg)"
            text-color="var(--layout-menu-text)"
            active-text-color="var(--layout-menu-active-text)"
          >
            <MenuItem
              v-for="item in sideMenuRoutes"
              :key="item.path"
              :item="item"
              :base-path="resolvePath(item.path)"
            />
          </el-menu>
        </el-scrollbar>
        <!-- 侧边栏切换按钮 -->
        <div class="layout__sidebar-toggle">
          <Hamburger :is-active="isSidebarOpen" @toggle-click="toggleSidebar" />
        </div>
      </div>

      <!-- 主内容区 -->
      <div :class="{ hasTagsView: isShowTagsView }" class="layout__main">
        <TagsView v-if="isShowTagsView" />
        <AppMain />
      </div>
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";
import { useWindowSize } from "@vueuse/core";
import { useLayout } from "../composables/useLayout";
import { useLayoutMenu } from "../composables/useLayoutMenu";
import BaseLayout from "./BaseLayout.vue";
import AppLogo from "../components/AppLogo/index.vue";
import MixTopMenu from "../components/Menu/MixTopMenu.vue";
import NavbarActions from "../components/NavBar/components/NavbarActions.vue";
import TagsView from "../components/TagsView/index.vue";
import AppMain from "../components/AppMain/index.vue";
import MenuItem from "../components/Menu/components/MenuItem.vue";
import Hamburger from "@/components/Hamburger/index.vue";
import { isExternal } from "@/utils/index";
import { computed, watch } from "vue";
import { useAppStore, usePermissionStore } from "@/store";

const route = useRoute();

// 布局相关参数
const { isShowTagsView, isShowLogo, isSidebarOpen, toggleSidebar } = useLayout();

// 菜单相关
const { sideMenuRoutes, activeTopMenuPath } = useLayoutMenu();

// 响应式窗口尺寸
const { width } = useWindowSize();

// 只有在小屏设备（移动设备）时才折叠Logo（只显示图标，隐藏文字）
const isLogoCollapsed = computed(() => width.value < 768);

// 当前激活的菜单
const activeLeftMenuPath = computed(() => {
  const { meta, path } = route;
  // 如果设置了activeMenu，则使用
  if (meta?.activeMenu && typeof meta.activeMenu === "string") {
    return meta.activeMenu;
  }
  return path;
});

/**
 * 解析路径 - 混合模式下，左侧菜单是从顶级菜单下的子菜单开始的
 * 所以需要拼接顶级菜单路径
 */
function resolvePath(routePath: string) {
  if (isExternal(routePath)) {
    return routePath;
  }

  if (routePath.startsWith("/")) {
    return routePath;
  }
  return `${activeTopMenuPath.value}/${routePath}`;
}

watch(
  () => route.path,
  (newPath) => {
    // 获取顶级路径
    const topMenuPath =
      newPath.split("/").filter(Boolean).length > 1 ? newPath.match(/^\/[^/]+/)?.[0] || "/" : "/";

    // 如果当前路径属于当前激活的顶部菜单
    if (newPath.startsWith(activeTopMenuPath.value)) {
      // no-op
    }

    // 仅在顶级路径实际变化时才执行更新
    else if (topMenuPath !== activeTopMenuPath.value) {
      // 主动更新顶部菜单和左侧菜单
      const appStore = useAppStore();
      const permissionStore = usePermissionStore();

      appStore.activeTopMenu(topMenuPath);
      permissionStore.setMixLayoutSideMenus(topMenuPath);
    }
  },
  { immediate: true }
);
</script>

<style lang="scss" scoped>
.layout {
  &__header {
    position: sticky;
    top: 0;
    z-index: 999;
    width: 100%;
    height: $navbar-height;
    color: var(--layout-header-text);
    background-color: var(--layout-header-bg);
    border-bottom: 1px solid var(--layout-header-border);

    &-content {
      display: flex;
      align-items: center;
      height: 100%;
      padding: 0;
    }

    &-logo {
      display: flex;
      flex-shrink: 0;
      align-items: center;
      justify-content: center;
      height: 100%;
    }

    &-menu {
      display: flex;
      flex: 1;
      align-items: center;
      min-width: 0;
      height: 100%;
      overflow: hidden;

      :deep(.el-menu) {
        height: 100%;
        background-color: transparent;
        border: none;
      }

      :deep(.el-menu--horizontal) {
        display: flex;
        align-items: center;
        height: 100%;

        .el-menu-item {
          height: 100%;
          line-height: $navbar-height;
          border-bottom: none;

          &.is-active {
            color: var(--layout-menu-active-text);
            background-color: var(--layout-menu-active-bg);
            border-bottom: 2px solid var(--layout-menu-active-text);
          }
        }
      }
    }

    &-actions {
      display: flex;
      flex-shrink: 0;
      align-items: center;
      height: 100%;
    }
  }

  &__container {
    display: flex;
    height: calc(100vh - $navbar-height);
    padding-top: 0;

    .layout__sidebar--left {
      position: relative;
      width: $sidebar-width;
      height: 100%;
      background-color: var(--layout-menu-bg);
      transition: width 0.28s;

      &.layout__sidebar--collapsed {
        width: $sidebar-width-collapsed !important;
      }

      :deep(.el-scrollbar) {
        height: calc(100vh - $navbar-height - 50px);
      }

      :deep(.el-menu) {
        height: 100%;
        border: none;
      }

      .layout__sidebar-toggle {
        position: absolute;
        bottom: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 50px;
        line-height: 50px;
        background-color: var(--layout-menu-bg);
        box-shadow: 0 0 6px -2px var(--el-color-primary);
      }
    }

    .layout__main {
      flex: 1;
      min-width: 0;
      height: 100%;
      margin-left: 0;
      overflow-y: auto;
      background-color: var(--layout-content-canvas, var(--layout-content-bg));
    }
  }
}

/* 移动端样式 */
:deep(.mobile) {
  .layout__container {
    .layout__sidebar--left {
      position: fixed;
      top: $navbar-height;
      bottom: 0;
      left: 0;
      z-index: 1000;
      transition: transform 0.28s;
    }
  }

  &.hideSidebar {
    .layout__sidebar--left {
      width: $sidebar-width !important;
      transform: translateX(-$sidebar-width);
    }
  }
}

:deep(.hasTagsView) {
  .app-main {
    height: calc(100vh - $navbar-height - $tags-view-height) !important;
  }
}
</style>
