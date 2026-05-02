<!-- 菜单组件 -->
<template>
  <el-menu
    ref="menuRef"
    :default-active="activeMenuPath"
    :collapse="!appStore.sidebar.opened"
    :background-color="menuThemeProps.backgroundColor"
    :text-color="menuThemeProps.textColor"
    :active-text-color="menuThemeProps.activeTextColor"
    :popper-effect="theme"
    :unique-opened="false"
    :collapse-transition="false"
    :mode="menuMode"
  >
    <!-- 菜单项 -->
    <MenuItem
      v-for="route in data"
      :key="route.path"
      :item="route"
      :base-path="menuParentBasePath"
    />
  </el-menu>
</template>

<script lang="ts" setup>
import { computed, nextTick, PropType, ref, watch } from "vue";
import type { MenuInstance } from "element-plus";
import { useRoute } from "vue-router";
import type { RouteRecordRaw } from "vue-router";
import { SidebarColor } from "@/enums/settings/theme.enum";
import { useSettingsStore, useAppStore } from "@/store";
import MenuItem from "./components/MenuItem.vue";
import variables from "@/styles/variables.module.scss";

const props = defineProps({
  data: {
    type: Array as PropType<RouteRecordRaw[]>,
    default: () => [],
  },
  basePath: {
    type: String,
    required: true,
    example: "/system",
  },
  menuMode: {
    type: String as PropType<"vertical" | "horizontal">,
    default: "vertical",
    validator: (value: string) => ["vertical", "horizontal"].includes(value),
  },
});

const settingsStore = useSettingsStore();
const appStore = useAppStore();
const currentRoute = useRoute();
const menuRef = ref<MenuInstance | null>(null);

// 获取主题
const theme = computed(() => settingsStore.theme);

// 获取浅色主题下的侧边栏配色方案
const sidebarColorScheme = computed(() => settingsStore.sidebarColorScheme);

// 菜单主题属性
const menuThemeProps = computed(() => {
  const isDarkOrClassicBlue =
    theme.value === "dark" || sidebarColorScheme.value === SidebarColor.CLASSIC_BLUE;

  return {
    backgroundColor: isDarkOrClassicBlue ? variables["menu-background"] : undefined,
    textColor: isDarkOrClassicBlue ? variables["menu-text"] : undefined,
    activeTextColor: isDarkOrClassicBlue ? variables["menu-active-text"] : undefined,
  };
});

function normalizeMenuPath(p: string): string {
  if (!p) return "";
  if (/^https?:\/\//i.test(p) || p.startsWith("//")) return p;
  const s = p.trim();
  if (s === "/") return "/";
  return s.replace(/\/+$/, "") || "/";
}

/**
 * 与 MenuItem 叶子项 index 一致：叶子用 router.resolve 得到 path，与 route.path 相同；
 * default-active 用当前 route.path（及 meta.activeMenu）即可对齐。
 */
const activeMenuPath = computed((): string => {
  const r = currentRoute;
  if (r.meta?.activeMenu && typeof r.meta.activeMenu === "string") {
    return normalizeMenuPath(r.meta.activeMenu);
  }
  return normalizeMenuPath(r.path);
});

/**
 * 侧栏树根前缀：左侧布局 base-path 为空时规范为 "/"，再与每项 path 拼接。
 * 勿用 resolveFullPath(route.path) 作为根 MenuItem 的 base-path，否则会与 item.path 再拼一次导致错位。
 */
const menuParentBasePath = computed(() => {
  const b = props.basePath;
  if (b === undefined || b === null || b === "") return "/";
  const t = b.replace(/\/+$/, "");
  return t || "/";
});

function syncMenuActive(val: string) {
  menuRef.value?.updateActiveIndex(val);
}

// 仅 nextTick 一次同步；若侧栏 default-active 偶发与路由不同步，可恢复为多次 syncMenuActive（见本文件 git 历史）
watch(
  activeMenuPath,
  (val) => {
    nextTick(() => syncMenuActive(val));
  },
  { immediate: true, flush: "post" }
);

// 父级激活样式由 Element Plus 在子项激活时为 el-sub-menu 添加 .is-active，MenuItem 内样式已覆盖标题颜色
</script>
