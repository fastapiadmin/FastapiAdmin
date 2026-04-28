<template>
  <BaseLayout>
    <!-- 顶部菜单栏 -->
    <div class="layout__header">
      <div class="layout__header-left">
        <!-- Logo区域 -->
        <div v-if="isShowLogo" class="layout__header-logo">
          <AppLogo :collapse="isLogoCollapsed" />
        </div>

        <!-- 顶部菜单区域 -->
        <div class="layout__header-menu">
          <BasicMenu :data="topMenuItems" menu-mode="horizontal" base-path="" />
        </div>

        <!-- 右侧操作区域 -->
        <div class="layout__header-right">
          <NavbarActions />
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div :class="{ hasTagsView: isShowTagsView }" class="layout__main">
      <TagsView v-if="isShowTagsView" />
      <AppMain />
    </div>
  </BaseLayout>
</template>

<script setup lang="ts">
  import { computed } from 'vue';
  import { useWindowSize } from '@vueuse/core';
  import { useLayout } from '../composables/useLayout';
  import { usePermissionStore } from '@/store';
  import BaseLayout from './BaseLayout.vue';
  import AppLogo from '../components/AppLogo/index.vue';
  import BasicMenu from '../components/Menu/BasicMenu.vue';
  import NavbarActions from '../components/NavBar/components/NavbarActions.vue';
  import TagsView from '../components/TagsView/index.vue';
  import AppMain from '../components/AppMain/index.vue';

  // 布局相关参数
  const { isShowTagsView, isShowLogo } = useLayout();

  // 菜单相关
  const permissionStore = usePermissionStore();
  const topMenuItems = computed(() => {
    return permissionStore.routes.filter((item) => !item.meta?.hidden);
  });

  // 响应式窗口尺寸
  const { width } = useWindowSize();

  // 只有在小屏设备（移动设备）时才折叠Logo（只显示图标，隐藏文字）
  const isLogoCollapsed = computed(() => width.value < 768);
</script>

<style lang="scss" scoped>
  .layout {
    &__header {
      position: sticky;
      top: 0;
      z-index: 999;
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      height: $navbar-height;
      background-color: var(--layout-header-bg, var(--menu-background));

      &-left {
        display: flex;
        flex: 1;
        align-items: center;
        min-width: 0;
        height: 100%;
      }

      &-logo {
        display: flex;
        flex-shrink: 0;
        align-items: center;
        height: 100%;

        :deep(.logo) {
          height: $navbar-height;
        }
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
          flex: 1;
          min-width: 0;
          height: $navbar-height;
          overflow: hidden;
          line-height: $navbar-height;
          background-color: transparent;
          border: none;

          .el-menu-item {
            height: $navbar-height;
            line-height: $navbar-height;
          }

          .el-sub-menu {
            .el-sub-menu__title {
              height: $navbar-height;
              line-height: $navbar-height;
            }

            &.has-active-child {
              .el-sub-menu__title {
                color: var(--el-color-primary) !important;
                border-bottom: 2px solid var(--el-color-primary) !important;

                .menu-icon {
                  color: var(--el-color-primary) !important;
                }
              }
            }
          }

          .el-menu--popup {
            min-width: 160px;
          }
        }
      }

      &-right {
        display: flex;
        flex-shrink: 0;
        align-items: center;
        height: 100%;
        padding-left: 12px;
      }
    }

    &__main {
      height: calc(100vh - $navbar-height);
      overflow-y: auto;
    }
  }

  // 当存在TagsView时的样式调整
  .hasTagsView {
    :deep(.app-main) {
      height: calc(100vh - $navbar-height - $tags-view-height) !important;
    }
  }
</style>
