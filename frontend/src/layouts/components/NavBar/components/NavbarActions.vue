<template>
  <div ref="navbar-actions" :class="['navbar-actions', navbarActionsClass]">
    <!-- 桌面端工具项 -->
    <template v-if="isDesktop">
      <!-- 搜索 -->
      <div v-if="settingStore.showMenuSearch" class="navbar-actions__item">
        <MenuSearch />
      </div>

      <!-- 全屏 -->
      <div v-if="settingStore.showFullscreen" class="navbar-actions__item">
        <Fullscreen />
      </div>

      <!-- 布局大小 -->
      <div v-if="settingStore.showSizeSelect" class="navbar-actions__item">
        <SizeSelect />
      </div>

      <!-- 语言选择 -->
      <div v-if="settingStore.showLangSelect" class="navbar-actions__item">
        <LangSelect />
      </div>

      <!-- 通知 -->
      <div v-if="settingStore.showNotification" class="navbar-actions__item">
        <Notification />
      </div>

      <!-- 系统设置按钮 -->
      <div
        v-if="settingStore.showSettings"
        class="navbar-actions__item"
        @click="handleSettingsClick"
      >
        <div class="i-svg:setting" />
      </div>
    </template>

    <!-- 用户菜单,不管桌面还是移动端都显示 -->
    <div class="navbar-actions__item">
      <el-dropdown trigger="click">
        <div class="user-profile">
          <div class="user-profile__avatar-wrapper">
            <template v-if="userStore.basicInfo.avatar">
              <el-avatar :size="30" :src="userStore.basicInfo.avatar" />
            </template>
            <template v-else>
              <el-avatar :size="30" icon="UserFilled" />
            </template>
            <span class="user-profile__online-indicator"></span>
          </div>
          <span class="user-profile__name">{{ userStore.basicInfo.name }}</span>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="handleProfileClick">
              <el-icon><User /></el-icon>
              {{ t("navbar.profile") }}
            </el-dropdown-item>
            <el-dropdown-item @click="handleConfigClick">
              <el-icon><Setting /></el-icon>
              {{ t("navbar.config") }}
            </el-dropdown-item>
            <el-dropdown-item @click="handleDocumentClick">
              <el-icon><Document /></el-icon>
              {{ t("navbar.document") }}
            </el-dropdown-item>
            <el-dropdown-item @click="handleGiteeClick">
              <el-icon><Reading /></el-icon>
              {{ t("navbar.gitee") }}
            </el-dropdown-item>
            <el-dropdown-item @click="handleTourClick">
              <el-icon><Position /></el-icon>
              {{ t("navbar.tour") }}
            </el-dropdown-item>
            <el-dropdown-item divided @click="handlelockScreen">
              <el-icon><Lock /></el-icon>
              {{ t("navbar.lock") }}
            </el-dropdown-item>
            <el-dropdown-item @click="logout">
              <el-icon><SwitchButton /></el-icon>
              {{ t("navbar.logout") }}
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>

  <!-- 引导 -->
  <Guide v-if="guideVisible" v-model="guideVisible" @skip="handleGuideExit" />

  <!-- 锁屏弹窗 -->
  <LockDialog v-if="dialogVisible" v-model="dialogVisible" />
  <teleport to="body">
    <transition name="fade-bottom" mode="out-in">
      <LockPage v-if="getIsLock" />
    </transition>
  </teleport>

  <!-- 配置中心抽屉 -->
  <ConfigInfoDrawer v-model="drawerVisible" />
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";

import { DeviceEnum } from "@/enums/settings/device.enum";
import { useAppStore, useSettingsStore, useUserStore, useLockStore } from "@/store";
import { SidebarColor, ThemeMode } from "@/enums/settings/theme.enum";
import { LayoutMode } from "@/enums";

// 导入子组件
import MenuSearch from "@/components/MenuSearch/index.vue";
import Fullscreen from "@/components/Fullscreen/index.vue";
import SizeSelect from "@/components/SizeSelect/index.vue";
import LangSelect from "@/components/LangSelect/index.vue";
import Notification from "@/components/Notification/index.vue";
import LockDialog from "./LockDialog.vue";
import LockPage from "./LockPage.vue";
import Guide from "@/components/Guide/index.vue";
import ConfigInfoDrawer from "@/views/module_system/param/components/ConfigInfoDrawer.vue";

const { t } = useI18n();
const appStore = useAppStore();
const settingStore = useSettingsStore();
const userStore = useUserStore();

const router = useRouter();

// 是否为桌面设备
const isDesktop = computed(() => appStore.device === DeviceEnum.DESKTOP);

/**
 * 打开个人中心页面
 */
function handleProfileClick() {
  router.push({ name: "Profile" });
}

const drawerVisible = ref(false);
/**
 * 打开配置中心页面
 */
function handleConfigClick() {
  drawerVisible.value = true;
}

/**
 * 项目文档
 */
function handleDocumentClick() {
  window.open("https://service.fastapiadmin.com", "_blank");
}

/**
 * 打开系统设置页面
 */
function handleSettingsClick() {
  settingStore.settingsVisible = true;
}

/**
 * Gitee 项目地址
 */
function handleGiteeClick() {
  window.open("https://gitee.com/fastapiadmin/FastapiAdmin");
}

/**
 * 项目引导
 */
// 使用ref而不是computed，以便可以修改引导可见性
// 使用 computed 实现双向绑定，减少 watch 的使用
const guideVisible = computed({
  get: () => appStore.guideVisible,
  set: (newValue) => appStore.showGuide(newValue),
});

function handleTourClick() {
  // 如果是移动端，直接跳转到引导页面
  if (appStore.device === DeviceEnum.MOBILE) {
    router.push({ name: "Guide" });
  } else {
    guideVisible.value = true;
  }
}

// 引导结束（点击跳过或最后一步完成关闭）后，自动关闭下次登录的自动展示
function handleGuideExit() {
  // 关闭自动展示开关，确保下次登录不再自动开启
  settingStore.updateSetting("showGuide", false);
}

// 监听引导关闭（从 true -> false），也同步关闭自动展示开关
watch(
  () => guideVisible.value,
  (val, oldVal) => {
    if (oldVal && !val) {
      settingStore.updateSetting("showGuide", false);
    }
  }
);

/**
 * 锁屏
 */
const lockStore = useLockStore();
const getIsLock = computed(() => lockStore.getLockInfo?.isLock ?? false);
const dialogVisible = ref<boolean>(false);
// 锁定屏幕
const handlelockScreen = () => {
  dialogVisible.value = true;
};

// 根据主题和侧边栏配色方案选择样式类
const navbarActionsClass = computed(() => {
  const { theme, sidebarColorScheme, layout } = settingStore;

  // 暗黑主题下，所有布局都使用白色文字
  if (theme === ThemeMode.DARK) {
    return "navbar-actions--white-text";
  }

  // 明亮主题下
  if (theme === ThemeMode.LIGHT) {
    // 顶部布局和混合布局的顶部区域：
    // - 如果侧边栏是经典蓝色，使用白色文字
    // - 如果侧边栏是极简白色，使用深色文字
    if (layout === LayoutMode.TOP || layout === LayoutMode.MIX) {
      if (sidebarColorScheme === SidebarColor.CLASSIC_BLUE) {
        return "navbar-actions--white-text";
      } else {
        return "navbar-actions--dark-text";
      }
    }
  }

  return "navbar-actions--dark-text";
});

/**
 * 退出登录
 */
function logout() {
  ElMessageBox.confirm("确定注销并退出系统吗？", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
    lockScroll: false,
  })
    .then(() => {
      userStore.logout().then(() => {
        router.push(`/login`);
      });
    })
    .catch(() => {
      ElMessageBox.close();
    });
}
</script>

<style lang="scss" scoped>
.navbar-actions {
  display: flex;
  align-items: center;
  height: 100%;

  &__item {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 44px; /* 增加最小点击区域到44px，符合人机交互标准 */
    height: 100%;
    padding: 0 8px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s;

    // 确保子元素居中
    > * {
      display: flex;
      align-items: center;
      justify-content: center;
    }

    // 确保 Element Plus 组件可以正常工作
    :deep(.el-dropdown),
    :deep(.el-tooltip) {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: 100%;
    }

    :deep(.i-svg\:language) {
      flex-shrink: 0;
      width: 18px;
      height: 18px;
      font-size: 18px;
      line-height: 18px;
      background-size: 18px 18px;
    }

    // 图标样式
    :deep([class^="i-svg:"]) {
      font-size: 18px;
      line-height: 1;
      color: var(--el-text-color-regular);
      transition: color 0.3s;
    }

    &:hover {
      background: rgba(0, 0, 0, 0.04);

      :deep([class^="i-svg:"]) {
        color: var(--el-color-primary);
      }
    }
  }

  .user-profile {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 44px;
    padding: 0 8px;

    &__avatar-wrapper {
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    &__avatar {
      flex-shrink: 0;
      width: 28px;
      height: 28px;
      border-radius: 50%;
    }

    &__online-indicator {
      position: absolute;
      right: 0;
      bottom: 0;
      width: 8px;
      height: 8px;
      background-color: #50b731;
      border-radius: 50%;
      box-shadow: 0 0 2px rgba(0, 0, 0, 0.2);
    }

    &__name {
      margin-left: 8px;
      color: var(--el-text-color-regular);
      white-space: nowrap;
      transition: color 0.3s;
    }
  }
}

// 白色文字样式（用于深色背景：暗黑主题、顶部布局、混合布局）
.navbar-actions--white-text {
  .navbar-actions__item {
    :deep([class^="i-svg:"]) {
      color: rgba(255, 255, 255, 0.85);
    }

    &:hover {
      background: rgba(255, 255, 255, 0.1);

      :deep([class^="i-svg:"]) {
        color: #fff;
      }
    }
  }

  .user-profile__name {
    color: rgba(255, 255, 255, 0.85);
  }
}

// 深色文字样式（用于浅色背景：明亮主题下的左侧布局）
.navbar-actions--dark-text {
  .navbar-actions__item {
    :deep([class^="i-svg:"]) {
      color: var(--el-text-color-regular) !important;
    }

    &:hover {
      background: rgba(0, 0, 0, 0.04);

      :deep([class^="i-svg:"]) {
        color: var(--el-color-primary) !important;
      }
    }
  }

  .user-profile__name {
    color: var(--el-text-color-regular) !important;
  }
}

// 确保下拉菜单中的图标不受影响
:deep(.el-dropdown-menu) {
  [class^="i-svg:"] {
    color: var(--el-text-color-regular) !important;

    &:hover {
      color: var(--el-color-primary) !important;
    }
  }
}
</style>
