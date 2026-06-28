<!-- 左侧菜单 或 双列菜单 -->
<template>
  <div
    class="layout-sidebar"
    v-if="showLeftMenu || isDualMenu"
    :class="{ 'no-border': menuList.length === 0 }"
  >
    <!-- 双列菜单（左侧） -->
    <div
      v-if="isDualMenu"
      class="dual-menu-left"
      :style="{ width: dualMenuShowText ? '80px' : '64px', background: getMenuTheme.background }"
    >
      <FaLogo v-if="showAppLogo" class="logo" :src="sidebarLogoSrc" @click="navigateToHome" />

      <ElScrollbar :style="{ height: 'calc(100% - 135px)' }">
        <ul>
          <li v-for="menu in firstLevelMenus" :key="menu.path" @click="handleMenuJump(menu, true)">
            <ElTooltip
              class="box-item"
              effect="dark"
              :content="$t(menu.meta.title)"
              placement="right"
              :offset="15"
              :hide-after="0"
              :disabled="dualMenuShowText"
            >
              <div
                :class="{
                  'is-active': menu.meta.isFirstLevel
                    ? menu.path === route.path
                    : menu.path === firstLevelMenuPath,
                }"
                :style="{
                  height: dualMenuShowText ? '60px' : '46px',
                }"
              >
                <FaMenuRouteIcon
                  class="menu-icon text-g-700 dark:text-g-800"
                  :icon="menu.meta.icon"
                  :style="{
                    marginBottom: dualMenuShowText ? '5px' : '0',
                  }"
                />
                <span v-if="dualMenuShowText" class="text-md text-g-700">
                  {{ $t(menu.meta.title) }}
                </span>
                <div v-if="menu.meta.showBadge" class="fa-badge fa-badge-dual" />
              </div>
            </ElTooltip>
          </li>
        </ul>
      </ElScrollbar>

      <FaIconButton
        class="switch-btn size-10"
        icon="ri:arrow-left-right-fill"
        @click="toggleDualMenuMode"
      />
    </div>

    <!-- 左侧菜单 || 双列菜单（右侧） -->
    <div
      v-show="menuList.length > 0"
      class="menu-left"
      :class="`menu-left-${getMenuTheme.theme} menu-left-${!menuOpen ? 'close' : 'open'}`"
      :style="{ background: getMenuTheme.background }"
    >
      <!-- Logo、系统名称（开关同时控制 Logo 与标题） -->
      <div
        v-if="showAppLogo"
        class="header"
        @click="navigateToHome"
        :style="{
          background: getMenuTheme.background,
        }"
      >
        <FaLogo v-if="!isDualMenu" class="logo" :src="sidebarLogoSrc" />

        <p
          :class="{ 'is-dual-menu-name': isDualMenu }"
          :style="{
            color: getMenuTheme.systemNameColor,
            opacity: !menuOpen ? 0 : 1,
          }"
        >
          {{ sidebarTitle }}
        </p>
      </div>
      <ElScrollbar :style="scrollbarStyle">
        <ElMenu
          :class="'el-menu-' + getMenuTheme.theme"
          :collapse="!menuOpen"
          :default-active="routerPath"
          :text-color="getMenuTheme.textColor"
          :unique-opened="uniqueOpened"
          :background-color="getMenuTheme.background"
          :default-openeds="defaultOpenedMenus"
          :popper-class="`menu-left-popper menu-left-${getMenuTheme.theme}-popper`"
          :show-timeout="50"
          :hide-timeout="50"
        >
          <SidebarSubmenu :list="menuList" :theme="getMenuTheme" @close="handleMenuClose" />
        </ElMenu>
      </ElScrollbar>

      <!-- 双列菜单右侧折叠按钮 -->
      <div class="dual-menu-collapse-btn" v-if="isDualMenu" @click="toggleMenuVisibility">
        <FaSvgIcon
          class="text-g-500/70"
          :icon="menuOpen ? 'ri:arrow-left-wide-fill' : 'ri:arrow-right-wide-fill'"
        />
      </div>

      <div
        class="menu-model"
        @click="toggleMenuVisibility"
        :style="{
          opacity: !menuOpen ? 0 : 1,
          transform: showMobileModal ? 'scale(1)' : 'scale(0)',
        }"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import AppConfig from "@/config";
import { useConfigStore, useSettingsStore, useMenuStore } from "@stores";
import { MenuTypeEnum, MenuWidth } from "@/enums/appEnum";
import { isIframe, handleMenuJump } from "@utils";
import SidebarSubmenu from "./widgets/FaSidebarSubmenu.vue";
import { useCommon } from "@/hooks/core/useCommon";
import { useWindowSize, useTimeoutFn } from "@vueuse/core";
import { MOBILE_BREAKPOINT } from "@utils/constants";

defineOptions({ name: "FaSidebarMenu" });

const ANIMATION_DELAY = 350;
const MENU_CLOSE_WIDTH = MenuWidth.CLOSE;

const route = useRoute();
const router = useRouter();
const settingStore = useSettingsStore();
const configStore = useConfigStore();

/** 租户配置：tenant_logo / tenant_name */
const sidebarLogoSrc = computed(() => {
  const raw = configStore.configData.tenant_logo?.config_value;
  return typeof raw === "string" && raw.trim() ? raw.trim() : undefined;
});

const sidebarTitle = computed(() => {
  const raw = configStore.configData.tenant_name?.config_value;
  if (typeof raw === "string" && raw.trim()) return raw.trim();
  return AppConfig.systemInfo.name;
});

const {
  getMenuOpenWidth,
  menuType,
  uniqueOpened,
  dualMenuShowText,
  menuOpen,
  getMenuTheme,
  showAppLogo,
} = storeToRefs(settingStore);

// 组件内部状态
const defaultOpenedMenus = ref<string[]>([]);
const showMobileModal = ref(false);

// 使用 VueUse 的窗口尺寸监听
const { width } = useWindowSize();

// 菜单宽度相关
const menuopenwidth = computed(() => getMenuOpenWidth.value);
const menuclosewidth = computed(() => MENU_CLOSE_WIDTH);

// 菜单类型判断
const isTopLeftMenu = computed(() => menuType.value === MenuTypeEnum.TOP_LEFT);
const showLeftMenu = computed(
  () => menuType.value === MenuTypeEnum.LEFT || menuType.value === MenuTypeEnum.TOP_LEFT
);
const isDualMenu = computed(() => menuType.value === MenuTypeEnum.DUAL_MENU);

// 移动端屏幕判断（使用 computed 避免重复计算）
const isMobileScreen = computed(() => width.value < MOBILE_BREAKPOINT);

// 路由相关
const firstLevelMenuPath = computed(() => route.matched[0]?.path);
const routerPath = computed(() => String(route.meta.activePath || route.path));

// 菜单数据
const firstLevelMenus = computed(() => {
  return useMenuStore().menuList.filter((menu) => !menu.meta.isHide);
});

const menuList = computed(() => {
  const menuStore = useMenuStore();
  const allMenus = menuStore.menuList;

  // 如果不是顶部左侧菜单或双列菜单，直接返回完整菜单列表
  if (!isTopLeftMenu.value && !isDualMenu.value) {
    return allMenus;
  }

  // 处理 iframe 路径
  if (isIframe(route.path)) {
    return findIframeMenuList(route.path, allMenus);
  }

  // 处理一级菜单
  if (route.meta.isFirstLevel) {
    return [];
  }

  // 返回当前顶级路径对应的子菜单
  const currentTopPath = `/${route.path.split("/")[1]}`;
  let currentMenu = allMenus.find((menu) => menu.path === currentTopPath);
  if (!currentMenu && allMenus.length > 0) {
    currentMenu =
      allMenus.find((menu) => !menu.meta?.isHide && menu.children?.length) ?? allMenus[0];
  }
  const sub = currentMenu?.children ?? [];
  // 顶部+左侧 / 双列：顶级为叶子（如 /home）时右侧展示自身
  if (sub.length === 0 && currentMenu?.path && !currentMenu.meta?.isHide) {
    return [currentMenu];
  }
  return sub;
});

// 双列菜单收起时的滚动条样式
const scrollbarStyle = computed(() => {
  const isCollapsed = isDualMenu.value && !menuOpen.value;
  return {
    transform: isCollapsed ? "translateY(-50px)" : "translateY(0)",
    height: isCollapsed ? "calc(100% + 50px)" : "calc(100% - 60px)",
    transition: "transform 0.3s ease",
  };
});

/**
 * 延迟隐藏移动端模态框（使用 VueUse 的 useTimeoutFn）
 */
const { start: delayHideMobileModal } = useTimeoutFn(
  () => {
    showMobileModal.value = false;
  },
  ANIMATION_DELAY,
  { immediate: false }
);

/**
 * 查找 iframe 对应的二级菜单列表
 */
const findIframeMenuList = (currentPath: string, menuList: any[]) => {
  // 递归查找包含当前路径的菜单项
  const hasPath = (items: any[]): boolean => {
    for (const item of items) {
      if (item.path === currentPath) {
        return true;
      }
      if (item.children && hasPath(item.children)) {
        return true;
      }
    }
    return false;
  };

  // 遍历一级菜单查找匹配的子菜单
  for (const menu of menuList) {
    if (menu.children && hasPath(menu.children)) {
      return menu.children;
    }
  }
  return [];
};

const { homePath } = useCommon();

/**
 * 导航到首页
 */
const navigateToHome = (): void => {
  router.push(homePath.value);
};

/**
 * 切换菜单显示/隐藏
 */
const toggleMenuVisibility = (): void => {
  settingStore.setMenuOpen(!menuOpen.value);

  // 移动端模态框控制逻辑
  if (isMobileScreen.value) {
    if (!menuOpen.value) {
      // 菜单即将打开，立即显示模态框
      showMobileModal.value = true;
    } else {
      // 菜单即将关闭，延迟隐藏模态框确保动画完成
      delayHideMobileModal();
    }
  }
};

/**
 * 处理菜单关闭（来自子组件）
 */
const handleMenuClose = (): void => {
  if (isMobileScreen.value) {
    settingStore.setMenuOpen(false);
    delayHideMobileModal();
  }
};

/**
 * 切换双列菜单模式
 */
const toggleDualMenuMode = (): void => {
  settingStore.setDualMenuShowText(!dualMenuShowText.value);
};

/**
 * 监听窗口尺寸变化，自动处理移动端菜单
 */
watch(width, (newWidth) => {
  if (newWidth < MOBILE_BREAKPOINT) {
    settingStore.setMenuOpen(false);
    if (!menuOpen.value) {
      showMobileModal.value = false;
    }
  } else {
    showMobileModal.value = false;
  }
});

/**
 * 监听菜单开关状态变化
 */
watch(menuOpen, (isMenuOpen: boolean) => {
  if (!isMobileScreen.value) {
    // 大屏幕设备上，模态框始终隐藏
    showMobileModal.value = false;
  } else {
    // 小屏幕设备上，根据菜单状态控制模态框
    if (isMenuOpen) {
      // 菜单打开时立即显示模态框
      showMobileModal.value = true;
    } else {
      // 菜单关闭时延迟隐藏模态框，确保动画完成
      delayHideMobileModal();
    }
  }
});
</script>

<style lang="scss" scoped>
.layout-sidebar {
  display: flex;
  height: 100vh;
  user-select: none;
  scrollbar-width: none;
  border-right: 1px solid var(--fa-card-border);

  &.no-border {
    border-right: none !important;
  }

  :deep(.el-scrollbar__bar.is-vertical) {
    width: 4px;
  }

  :deep(.el-scrollbar__thumb) {
    right: -2px;
    background-color: var(--fa-gray-400);
    border-radius: 2px;
  }

  .dual-menu-left {
    position: relative;
    width: 80px;
    height: 100%;
    border-right: 1px solid var(--fa-card-border) !important;
    transition: width 0.25s;

    .logo {
      margin: auto;
      margin-top: 12px;
      margin-bottom: 3px;
      cursor: pointer;
    }

    ul {
      li {
        > div {
          position: relative;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          margin: 8px;
          overflow: hidden;
          text-align: center;
          cursor: pointer;
          border-radius: 5px;

          .art-svg-icon {
            display: block;
            margin: 0 auto;
            font-size: 20px;
          }

          span {
            display: -webkit-box;
            width: 100%;
            overflow: hidden;
            text-overflow: ellipsis;
            -webkit-line-clamp: 1;
            line-clamp: 1;
            font-size: 12px;
            -webkit-box-orient: vertical;
          }

          &.is-active {
            background: var(--el-color-primary-light-9);

            .art-svg-icon,
            span {
              color: var(--theme-color) !important;
            }
          }
        }
      }
    }

    .switch-btn {
      position: absolute;
      right: 0;
      bottom: 15px;
      left: 0;
      margin: auto;
    }
  }

  .menu-left {
    position: relative;
    box-sizing: border-box;
    height: 100vh;

    @media only screen and (width <= 640px) {
      height: 100dvh;
    }

    .el-menu {
      height: 100%;
    }

    &:hover {
      .dual-menu-collapse-btn {
        opacity: 1 !important;
      }
    }

    .dual-menu-collapse-btn {
      position: absolute;
      top: 50%;
      right: -11px;
      z-index: 10;
      width: 11px;
      height: 50px;
      cursor: pointer;
      background-color: var(--default-box-color);
      border: 1px solid var(--fa-card-border);
      border-radius: 0 15px 15px 0;
      opacity: 0;
      transform: translateY(-50%);
      transition: opacity 0.2s;

      &:hover {
        .art-svg-icon {
          color: var(--fa-gray-800) !important;
        }
      }

      .art-svg-icon {
        position: absolute;
        top: 0;
        bottom: 0;
        left: -4px;
        margin: auto;
        transition: all 0.3s;
      }
    }
  }

  .header {
    position: relative;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    width: 100%;
    height: 60px;
    overflow: hidden;
    line-height: 60px;
    cursor: pointer;

    .logo {
      margin-left: 22px;
    }

    p {
      position: absolute;
      top: 0;
      bottom: 0;
      left: 58px;
      box-sizing: border-box;
      margin-left: 10px;
      font-size: 18px;

      &.is-dual-menu-name {
        left: 25px;
        margin: auto;
      }
    }
  }

  .el-menu {
    box-sizing: border-box;

    /* 防止菜单内的滚动影响整个页面滚动 */
    overscroll-behavior: contain;
    scrollbar-width: none;
    border-right: 0;
    -ms-scroll-chaining: contain;

    &::-webkit-scrollbar {
      width: 0 !important;
    }
  }

  .menu-model {
    display: none;
  }
}

@media only screen and (width <= 800px) {
  .layout-sidebar {
    width: 0;

    .header {
      height: 50px;
      line-height: 50px;
    }

    .el-menu {
      height: calc(100vh - 60px);
    }

    .el-menu--collapse {
      width: 0;
    }

    /* 折叠状态下的header样式 */
    .menu-left-close .header {
      .logo {
        display: none;
      }

      p {
        left: 16px;
        font-size: 0;
        opacity: 0 !important;
      }
    }

    .menu-model {
      position: fixed;
      top: 0;
      left: 0;
      z-index: -1;
      display: block;
      width: 100%;
      height: 100vh;
      background: var(--fa-overlay-heavy);
      transition: opacity 0.2s ease-in-out;
    }
  }
}

@media only screen and (width <= 640px) {
  .layout-sidebar {
    border-right: 0 !important;
  }
}

.dark {
  .layout-sidebar {
    border-right: 1px solid var(--fa-dark-border-subtle);

    :deep(.el-scrollbar__thumb) {
      background-color: var(--fa-scrollbar-thumb);
    }

    .dual-menu-left {
      border-right: 1px solid var(--fa-dark-border-subtle) !important;
    }
  }
}
</style>

<style lang="scss">
@use "@styles/core/mixin.scss" as *;

/* 菜单样式变量 */
$menu-height: 42px;
$menu-icon-size: 20px;
$menu-font-size: 14px;
$hover-bg-color: var(--el-color-primary-light-9);
$popup-menu-height: 40px;
$popup-menu-padding: 8px;
$popup-menu-margin: 5px;
$popup-menu-radius: 6px;

/* 通用菜单项样式 */
@mixin menu-item-base {
  width: calc(100% - 16px);
  margin-left: 8px;
  border-radius: 6px;

  .menu-icon {
    margin-left: -7px;
  }
}

/* 通用 hover 样式 */
@mixin menu-hover($bg-color) {
  .el-sub-menu__title:hover,
  .el-menu-item:not(.is-active):hover {
    background: $bg-color !important;
  }
}

/* 通用选中样式 */
@mixin menu-active($color, $bg-color, $icon-color: var(--theme-color)) {
  .el-menu-item.is-active {
    color: $color !important;
    background-color: $bg-color;

    .menu-icon {
      .art-svg-icon {
        color: $icon-color !important;
      }
    }
  }
}

/* 弹窗菜单项样式 */
@mixin popup-menu-item {
  height: $popup-menu-height;
  margin-bottom: $popup-menu-margin;
  border-radius: $popup-menu-radius;

  .menu-icon {
    margin-right: 5px;
  }

  &:last-of-type {
    margin-bottom: 0;
  }
}

/* 主题菜单通用样式（合并 design 和 dark 主题的共同逻辑） */
@mixin theme-menu-base {
  .el-sub-menu__title,
  .el-menu-item {
    @include menu-item-base;
  }
}

/* 弹窗菜单通用样式 */
@mixin popup-menu-base($hover-bg, $active-color, $active-bg) {
  .el-menu--popup {
    padding: $popup-menu-padding;

    .el-sub-menu__title:hover,
    .el-menu-item:hover {
      background-color: $hover-bg !important;
      border-radius: $popup-menu-radius;
    }

    .el-menu-item {
      @include popup-menu-item;

      &.is-active {
        color: $active-color !important;
        background-color: $active-bg !important;
      }
    }

    .el-sub-menu {
      @include popup-menu-item;

      height: $popup-menu-height !important;

      .el-sub-menu__title {
        height: $popup-menu-height !important;
        border-radius: $popup-menu-radius;
      }
    }
  }
}

.layout-sidebar {
  /* ---------------------- Modify default style ---------------------- */

  /* 菜单折叠样式 */
  .menu-left-close {
    .header {
      .logo {
        margin: 0 auto;
      }
    }
  }

  /* 菜单图标 */
  .menu-icon {
    margin-right: 8px;
    font-size: $menu-icon-size;
  }

  /* 菜单高度 */
  .el-sub-menu__title,
  .el-menu-item {
    height: $menu-height !important;
    margin-bottom: 4px;
    line-height: $menu-height !important;

    span {
      font-size: $menu-font-size !important;

      @include ellipsis();
    }
  }

  /* 右侧箭头 */
  .el-sub-menu__icon-arrow {
    width: 13px !important;
    font-size: 13px !important;
  }

  /* 菜单折叠 */
  .el-menu--collapse {
    .el-sub-menu.is-active {
      .el-sub-menu__title {
        .menu-icon {
          .art-svg-icon {
            // 选中菜单图标颜色
            color: var(--theme-color) !important;
          }
        }
      }
    }
  }

  /* ---------------------- Design theme menu ---------------------- */
  .el-menu-design {
    @include theme-menu-base;
    @include menu-active(var(--theme-color), var(--el-color-primary-light-9));
    @include menu-hover($hover-bg-color);

    .el-sub-menu__icon-arrow {
      color: var(--fa-gray-600);
    }
  }

  /* ---------------------- Dark theme menu ---------------------- */
  .el-menu-dark {
    @include theme-menu-base;
    @include menu-active(var(--fa-gray-900), var(--fa-gray-300), var(--fa-gray-900));
    @include menu-hover(var(--fa-gray-200));

    .el-sub-menu__icon-arrow {
      color: var(--fa-gray-400);
    }
  }

  /* ---------------------- Light theme menu ---------------------- */
  .el-menu-light {
    .el-sub-menu__title,
    .el-menu-item {
      .menu-icon {
        margin-left: 1px;
      }
    }

    .el-menu-item.is-active {
      background-color: var(--el-color-primary-light-9);

      .art-svg-icon {
        color: var(--theme-color) !important;
      }

      &::before {
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        content: "";
        background: var(--theme-color);
      }
    }

    @include menu-hover($hover-bg-color);

    .el-sub-menu__icon-arrow {
      color: var(--fa-gray-600);
    }
  }
}

@media only screen and (width <= 640px) {
  .layout-sidebar {
    .el-menu-design {
      > .el-sub-menu {
        margin-left: 0;
      }

      .el-sub-menu {
        width: 100% !important;
      }
    }
  }
}

/* 菜单折叠 hover 弹窗样式（浅色主题） */
.el-menu--vertical,
.el-menu--popup-container {
  @include popup-menu-base(var(--el-color-primary-light-9), var(--fa-gray-900), var(--fa-gray-200));
}

/* 暗黑模式菜单样式 */
.dark {
  .el-menu--vertical,
  .el-menu--popup-container {
    @include popup-menu-base(
      var(--el-color-primary-light-9),
      var(--fa-gray-900),
      var(--fa-gray-300)
    );
  }

  .layout-sidebar {
    /* 图标颜色、文字颜色 */
    .menu-icon .art-svg-icon,
    .menu-name {
      color: var(--fa-gray-800) !important;
    }

    /* 暗色模式：悬浮使用半透明主题色 */
    .el-menu-item:not(.is-active):hover,
    .el-sub-menu__title:not(.is-active):hover {
      background-color: color-mix(in srgb, var(--el-color-primary) 15%, transparent) !important;
    }

    /* 选中的文字颜色跟图标颜色 */
    .el-menu-item.is-active {
      span,
      .menu-icon .art-svg-icon {
        color: var(--theme-color) !important;
      }
    }

    /* 右侧箭头颜色 */
    .el-sub-menu__icon-arrow {
      color: var(--fa-gray-900);
    }
  }
}

.layout-sidebar {
  /* 展开的宽度 */
  .el-menu:not(.el-menu--collapse) {
    width: v-bind(menuopenwidth);
  }

  /* 折叠后宽度 */
  .el-menu--collapse {
    width: v-bind(menuclosewidth);
  }
}
</style>
