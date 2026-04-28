<template>
  <BaseLayout>
    <!-- 顶部菜单栏 -->
    <div class="layout__header" :class="{ 'layout__header--with-tags': isShowTagsView }">
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
          <!-- 仅切换顶级模块时重建侧栏，避免 :key=route.path 导致每次路由变化整表重建、展开态丢失 -->
          <BasicMenu :key="mixSideMenuKey" :data="sideMenuRoutes" :base-path="leftMenuBasePath" />
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
  import { useRoute } from 'vue-router';
  import { useWindowSize } from '@vueuse/core';
  import { useLayout } from '../composables/useLayout';
  import { useLayoutMenu } from '../composables/useLayoutMenu';
  import BaseLayout from './BaseLayout.vue';
  import AppLogo from '../components/AppLogo/index.vue';
  import MixTopMenu from '../components/Menu/MixTopMenu.vue';
  import NavbarActions from '../components/NavBar/components/NavbarActions.vue';
  import TagsView from '../components/TagsView/index.vue';
  import AppMain from '../components/AppMain/index.vue';
  import BasicMenu from '../components/Menu/BasicMenu.vue';
  import Hamburger from '@/components/Hamburger/index.vue';
  import { computed } from 'vue';

  const route = useRoute();

  // 布局相关参数
  const { isShowTagsView, isShowLogo, isSidebarOpen, toggleSidebar } = useLayout();

  // 菜单相关
  const { sideMenuRoutes, activeTopMenuPath } = useLayoutMenu();

  // 响应式窗口尺寸
  const { width } = useWindowSize();

  // 只有在小屏设备（移动设备）时才折叠Logo（只显示图标，隐藏文字）
  const isLogoCollapsed = computed(() => width.value < 768);

  // 混合布局左侧菜单 basePath 兜底，避免初始化时 activeTopMenuPath 为空导致路径拼接异常
  const leftMenuBasePath = computed(() => {
    if (activeTopMenuPath.value) return activeTopMenuPath.value;
    return route.path.match(/^\/[^/]+/)?.[0] || '/';
  });

  /** 与顶部一级模块一致，同模块内路由切换不重建侧栏（保留展开）；切换模块时重建 */
  const mixSideMenuKey = computed(() => activeTopMenuPath.value || leftMenuBasePath.value);
</script>

<style lang="scss" scoped>
  .layout {
    &__header {
      position: sticky;
      top: 0;
      z-index: 999;
      width: 100%;
      height: $navbar-height;
      color: var(--menu-text);
      background-color: var(--layout-header-bg, var(--menu-background));
      border-bottom: 1px solid var(--el-border-color-light);

      &--with-tags {
        border-bottom: none;
      }

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
        background-color: var(--menu-background);
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
          background-color: var(--menu-background);
          box-shadow: var(--el-box-shadow-light);
        }
      }

      .layout__main {
        flex: 1;
        min-width: 0;
        height: 100%;
        margin-left: 0;
        overflow-y: auto;
        background-color: var(--el-bg-color-page);
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
