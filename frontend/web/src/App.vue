<template>
  <ElConfigProvider
    :size="size"
    :locale="locale"
    :z-index="3000"
    :card="{
      shadow: 'never',
    }"
  >
    <ElWatermark
      :font="{ color: fontColor }"
      :content="showWatermark ? watermarkContent : ''"
      :z-index="9999"
      class="wh-full"
    >
      <RouterView></RouterView>

      <!-- AI 助手 -->
      <FaAiAssistant v-if="enableAiAssistant" />
    </ElWatermark>
  </ElConfigProvider>
</template>

<script setup lang="ts">
import { computed, onBeforeMount, onErrorCaptured, onMounted, onUnmounted } from "vue";
import { ElMessage } from "element-plus";
import { useWindowSize } from "@vueuse/core";
import { useAppStore, useUserStore } from "./store";
import { useSettingsStore } from "./store/modules/setting.store";
import { defaultSettings } from "./config/setting";
import { ComponentSize } from "./enums/settings/layout.enum";
import { MOBILE_BREAKPOINT } from "./utils/constants/definitions";
import { hexToRgba, toggleTransition } from "./utils/ui";
import { initializeTheme } from "./hooks/core/useTheme";
import { useAppBootstrap } from "@/hooks/core/useAppBootstrap";
import { ThemeMode } from "./enums";
import en from "element-plus/es/locale/lang/en";
import zhCn from "element-plus/es/locale/lang/zh-cn";
import { router } from "@/router";
import { ElNotification } from "element-plus";
import { initIconifyAsync } from "./plugins/iconify";

const appStore = useAppStore();
const settingsStore = useSettingsStore();
const userStore = useUserStore();
const { width } = useWindowSize();

// H5 用小尺寸，桌面用用户设置的大小
const size = computed(() => {
  if (width.value < MOBILE_BREAKPOINT) return "small" as ComponentSize;
  return appStore.size as ComponentSize;
});
const showWatermark = computed(() => settingsStore.showWatermark);
const watermarkContent = defaultSettings.watermarkContent;

// 根据语言设置返回对应的语言包
const locale = computed(() => {
  return appStore.language === "en" ? en : zhCn;
});

// 只有在启用 AI 助手且用户已登录时才显示
const enableAiAssistant = computed(() => {
  const isEnabled = settingsStore.userEnableAi;
  const isLoggedIn = userStore.basicInfo && Object.keys(userStore.basicInfo).length > 0;
  return isEnabled && isLoggedIn;
});

// 水印文字默认使用当前主题色（半透明），随主题色设置变化
const fontColor = computed(() => {
  const hex = settingsStore.themeColor || defaultSettings.themeColor;
  const alpha = settingsStore.theme === ThemeMode.DARK ? 0.22 : 0.16;
  try {
    return hexToRgba(hex, alpha).rgba;
  } catch {
    return hexToRgba(defaultSettings.themeColor, alpha).rgba;
  }
});

/**
 * 应用根组件生命周期：
 *
 * onBeforeMount
 *   1. toggleTransition(true)  —— 临时禁用页面过渡，避免主题切换时的闪烁
 *   2. initializeTheme()       —— 加载主题配色(CSS 变量)、暗色模式 class、auto 监听
 *
 * onMounted
 *   1. bootstrap()                                —— 存储检查 → 过渡恢复 → 版本升级 → 站点配置
 *   2. 监听 "app:storage-invalidated" 事件        —— 存储异常时由 storage 模块派发
 */
onBeforeMount(() => {
  toggleTransition(true);
  initializeTheme();
});

// 存储失效时跳转登录页（由 storage 模块 detect 到异常后派发）
const handleStorageInvalidated = () => {
  router.push({ name: "Login" });
};

const { bootstrap } = useAppBootstrap();

// ── 全局键盘快捷键 ──
const handleGlobalKeydown = (e: KeyboardEvent) => {
  const isMac = navigator.userAgent.includes("Mac");
  const modKey = isMac ? e.metaKey : e.ctrlKey;

  // Ctrl+S / Cmd+S：提交弹窗表单
  if (modKey && e.key === "s") {
    // 优先触发 useCrudForm 中已注册的键盘监听（由其自行 e.preventDefault）
    // 兜底：查找可见 dialog/drawer 中的确认按钮
    const confirmBtn = document.querySelector<HTMLElement>(
      [
        ".el-dialog:not(.is-hidden) .el-dialog__footer .el-button--primary",
        ".el-overlay-dialog:not(.is-hidden) .el-dialog__footer .el-button--primary",
        ".el-drawer:not(.is-hidden) .el-drawer__footer .el-button--primary",
      ].join(", ")
    );
    if (confirmBtn && document.querySelector(".el-overlay-dialog")) {
      confirmBtn.click();
    }
    // useCrudForm 中的 useFormKeyboardSubmit 已自行 e.preventDefault，此处也调用防止默认
    e.preventDefault();
    return;
  }

  // Ctrl+F / Cmd+F：聚焦搜索输入框
  if (modKey && e.key === "f") {
    const searchInput = document.querySelector<HTMLElement>(".fa-search-bar input");
    if (searchInput) {
      e.preventDefault();
      searchInput.focus();
    }
    return;
  }

  // ESC：由 ElDialog / ElDrawer 内置逻辑处理，此处不做额外干预
};
window.addEventListener("keydown", handleGlobalKeydown);

const handleOffline = () => {
  ElNotification({
    title: "网络已断开",
    message: "请检查您的网络连接",
    type: "error",
    duration: 0,
  });
};

const handleOnline = () => {
  ElMessage.success("网络已恢复");
};

onMounted(() => {
  bootstrap();

  // 存储检测到异常并已清除数据 → 由路由守卫完成登出清理
  window.addEventListener("app:storage-invalidated", handleStorageInvalidated);

  // 全局网络状态监听
  window.addEventListener("offline", handleOffline);
  window.addEventListener("online", handleOnline);

  // 异步加载图标集，避免阻塞首屏
  initIconifyAsync();
});

onUnmounted(() => {
  window.removeEventListener("app:storage-invalidated", handleStorageInvalidated);
  window.removeEventListener("keydown", handleGlobalKeydown);
  window.removeEventListener("offline", handleOffline);
  window.removeEventListener("online", handleOnline);
});

// ─── 全局错误边界 ───
onErrorCaptured((err, _instance, info) => {
  console.error(`[ErrorBoundary] ${info}:`, err);
  // 开发环境弹窗提示，生产环境静默上报
  if (import.meta.env.DEV) {
    ElNotification({
      title: "组件渲染异常",
      message: `${info}: ${err instanceof Error ? err.message : String(err)}`,
      type: "error",
      duration: 5000,
    });
  }
  return false; // 阻止异常向上冒泡
});
</script>
