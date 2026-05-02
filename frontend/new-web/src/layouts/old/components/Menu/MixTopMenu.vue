<!-- 混合布局顶部菜单 -->
<template>
  <el-menu
    mode="horizontal"
    :default-active="activeTopMenuPath"
    :background-color="
      theme === 'dark' || sidebarColorScheme === SidebarColor.CLASSIC_BLUE
        ? variables['menu-background']
        : undefined
    "
    :text-color="
      theme === 'dark' || sidebarColorScheme === SidebarColor.CLASSIC_BLUE
        ? variables['menu-text']
        : undefined
    "
    :active-text-color="
      theme === 'dark' || sidebarColorScheme === SidebarColor.CLASSIC_BLUE
        ? variables['menu-active-text']
        : undefined
    "
    @select="handleTopMenuSelect"
  >
    <el-menu-item v-for="item in topMenuItems" :key="item.path" :index="item.path">
      <MenuItemContent v-if="item.meta" :icon="item.meta.icon" :title="item.meta.title" />
    </el-menu-item>
  </el-menu>
</template>

<script lang="ts" setup>
import { computed, nextTick, watch } from "vue";
import MenuItemContent from "./components/MenuItemContent.vue";

defineOptions({
  name: "MixTopMenu",
});

import { LocationQueryRaw, RouteRecordRaw, useRouter } from "vue-router";
import { usePermissionStore, useAppStore, useSettingsStore } from "@/store";
import variables from "@/styles/variables.module.scss";
import { SidebarColor } from "@/enums/settings/theme.enum";

const router = useRouter();
const appStore = useAppStore();
const permissionStore = usePermissionStore();
const settingsStore = useSettingsStore();

/**
 * 根据当前完整路径解析混合布局的「顶级」菜单 path。
 * 不能仅用第一段路径（如 /app 会误匹配 /application），应按最长前缀匹配顶级路由（BUG #7）。
 */
function resolveMixTopMenuPath(fullPath: string): string {
  const path = (fullPath.split("?")[0] || "").replace(/\/$/, "") || "/";
  const tops = permissionStore.routes.filter(
    (r) => r.path && r.path !== "/" && !(r.meta as { hidden?: boolean } | undefined)?.hidden
  );
  const sorted = [...tops].sort((a, b) => (b.path?.length || 0) - (a.path?.length || 0));
  for (const r of sorted) {
    const p = r.path || "";
    if (!p) continue;
    if (path === p || path.startsWith(`${p}/`)) return p;
  }
  const first = path.match(/^\/[^/]+/)?.[0];
  return first || "/";
}

/** 水平菜单点击后焦点留在 el-menu-item 上，:focus 样式像「悬浮背景」；仅在 @select 后 blur 一次即可 */
function blurTopMenuFocus() {
  nextTick(() => {
    requestAnimationFrame(() => {
      const ae = document.activeElement;
      if (ae instanceof HTMLElement && ae.closest?.(".layout__header-menu .el-menu")) {
        ae.blur();
      }
    });
  });
}

// 获取主题
const theme = computed(() => settingsStore.theme);

// 获取浅色主题下的侧边栏配色方案
const sidebarColorScheme = computed(() => settingsStore.sidebarColorScheme);

// 处理后的顶部菜单列表 - 智能显示唯一子菜单的标题
const topMenuItems = computed(() => {
  const topMenus = permissionStore.routes.filter((item) => !item.meta || !item.meta.hidden);
  return topMenus.map((route) => {
    // 如果路由设置了 alwaysShow=true，或者没有子菜单，直接返回原路由
    if (route.meta?.alwaysShow || !route.children || route.children.length === 0) {
      return route;
    }

    // 过滤出非隐藏的子菜单
    const visibleChildren = route.children.filter((child) => !child.meta?.hidden);

    // 如果只有一个非隐藏的子菜单，显示子菜单的信息
    if (visibleChildren.length === 1) {
      const onlyChild = visibleChildren[0];
      return {
        ...route,
        meta: {
          ...route.meta,
          title: onlyChild.meta?.title || route.meta?.title,
          icon: onlyChild.meta?.icon || route.meta?.icon,
        },
      };
    }

    // 其他情况返回原路由
    return route;
  });
});

/**
 * 处理菜单点击事件，切换顶部菜单并加载对应的左侧菜单
 * @param routePath 点击的菜单路径
 */
const handleTopMenuSelect = (routePath: string) => {
  updateMenuState(routePath);
  blurTopMenuFocus();
};

/**
 * 更新菜单状态 - 同时处理点击和路由变化情况
 * @param topMenuPath 顶级菜单路径
 * @param skipNavigation 是否跳过导航（路由变化时为true，点击菜单时为false）
 */
const updateMenuState = (topMenuPath: string, skipNavigation = false) => {
  let hasStateChanged = false;

  // 确保路径有效才更新
  if (topMenuPath) {
    // 顶部激活路径
    if (appStore.activeTopMenuPath !== topMenuPath) {
      appStore.activeTopMenu(topMenuPath);
      hasStateChanged = true;
    }

    // 混合布局左侧菜单跟随顶部菜单
    permissionStore.setMixLayoutSideMenus(topMenuPath);
  }

  // 仅在点击顶部菜单且状态发生变化时，才跳转到左侧第一个菜单
  if (!skipNavigation && hasStateChanged) {
    navigateToFirstLeftMenu(permissionStore.mixLayoutSideMenus); // 跳转到左侧第一个菜单
  }
};

/**
 * 跳转到左侧第一个可访问的菜单
 * @param menus 左侧菜单列表
 */
const navigateToFirstLeftMenu = (menus: RouteRecordRaw[]) => {
  if (menus.length === 0) return;

  const [firstMenu] = menus;

  // 如果第一个菜单有子菜单，递归跳转到第一个子菜单
  if (firstMenu.children && firstMenu.children.length > 0) {
    navigateToFirstLeftMenu(firstMenu.children as RouteRecordRaw[]);
  } else if (firstMenu.name) {
    router.push({
      name: firstMenu.name,
      query:
        typeof firstMenu.meta?.params === "object"
          ? (firstMenu.meta.params as LocationQueryRaw)
          : undefined,
    });
  }
};

// 获取当前路由路径的顶部菜单路径
const activeTopMenuPath = computed(() => appStore.activeTopMenuPath);

// 监听路由变化，同步更新顶部菜单和左侧菜单的激活状态
watch(
  () => router.currentRoute.value.path,
  (newPath) => {
    if (newPath) {
      updateMenuState(resolveMixTopMenuPath(newPath), true);
    }
  },
  { immediate: true }
);
</script>

<style lang="scss" scoped>
.el-menu {
  width: 100%;
  height: 100%;

  &--horizontal {
    height: $navbar-height !important;

    // 确保菜单项垂直居中
    :deep(.el-menu-item) {
      height: 100%;
      line-height: $navbar-height;
    }

    // 移除默认的底部边框
    &::after {
      display: none;
    }
  }
}
</style>
