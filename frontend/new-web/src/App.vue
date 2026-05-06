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
      <AiAssistant v-if="enableAiAssistant" />
    </ElWatermark>
  </ElConfigProvider>
</template>

<script setup lang="ts">
import { computed, onBeforeMount, onMounted } from "vue";
import { useAppStore, useUserStore } from "./store";
import { useSettingsStore } from "./store/modules/setting.store";
import { defaultSettings } from "./config/setting";
import { ComponentSize } from "./enums/settings/layout.enum";
import AiAssistant from "./components/AiAssistant/index.vue";
import { toggleTransition } from "./utils/ui";
import { checkStorageCompatibility } from "./utils/storage";
import { initializeTheme } from "./hooks/core/useTheme";
import { systemUpgrade } from "./utils/sys";
import { ThemeMode } from "./enums";
import en from "element-plus/es/locale/lang/en";
import zhCn from "element-plus/es/locale/lang/zh-cn";

const appStore = useAppStore();
const settingsStore = useSettingsStore();
const userStore = useUserStore();

const size = computed(() => appStore.size as ComponentSize);
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

// 明亮/暗黑主题水印字体颜色适配
const fontColor = computed(() => {
  return settingsStore.theme === ThemeMode.DARK ? "rgba(255, 255, 255, .15)" : "rgba(0, 0, 0, .15)";
});

onBeforeMount(() => {
  toggleTransition(true);
  initializeTheme();
});

onMounted(() => {
  checkStorageCompatibility();
  toggleTransition(false);
  systemUpgrade();
});
</script>
