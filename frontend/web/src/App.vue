<template>
  <ElConfigProvider
    :locale="locales"
    :size="size"
    :z-index="3000"
    :card="{
      shadow: 'never',
    }"
  >
    <!-- 开启水印 -->
    <ElWatermark
      :font="{ color: fontColor }"
      :content="showWatermark ? watermarkContent : ''"
      :z-index="9999"
      class="wh-full"
    >
      <RouterView />

      <!-- AI 助手 -->
      <AiAssistant v-if="enableAiAssistant" />
    </ElWatermark>
  </ElConfigProvider>

  <!-- <ElConfigProvider
    size="default"
    :locale="locales[language]"
    :z-index="3000"
    :card="{
      shadow: 'never'
    }"
  >
    <RouterView></RouterView>
  </ElConfigProvider> -->
</template>

<script setup lang="ts">
  // import { useUserStore } from './store/modules/user'
  // import zh from 'element-plus/es/locale/lang/zh-cn'
  // import en from 'element-plus/es/locale/lang/en'
  // import { systemUpgrade } from './utils/sys'
  // import { toggleTransition } from './utils/ui/animation'
  // import { checkStorageCompatibility } from './utils/storage'
  // import { initializeTheme } from './hooks/core/useTheme'

  // const userStore = useUserStore()
  // const { language } = storeToRefs(userStore)

  // const locales = {
  //   zh: zh,
  //   en: en
  // }

  // onBeforeMount(() => {
  //   toggleTransition(true)
  //   initializeTheme()
  // })

  // onMounted(() => {
  //   checkStorageCompatibility()
  //   toggleTransition(false)
  //   systemUpgrade()
  // })

  import { useAppStore, useSettingsStore, useUserStore } from '@/store';
  import { defaultSettings } from '@/settings';
  import { ThemeMode } from '@/enums/settings/theme.enum';
  import { ComponentSize } from '@/enums/settings/layout.enum';
  import AiAssistant from '@/components/AiAssistant/index.vue';

  const appStore = useAppStore();
  const settingsStore = useSettingsStore();
  const userStore = useUserStore();

  const locales = computed(() => appStore.locale);
  const size = computed(() => appStore.size as ComponentSize);
  const showWatermark = computed(() => settingsStore.showWatermark);
  const watermarkContent = defaultSettings.watermarkContent;

  // 只有在启用 AI 助手且用户已登录时才显示
  // 使用 userInfo 作为响应式依赖，当用户退出登录时会自动更新
  const enableAiAssistant = computed(() => {
    const isEnabled = settingsStore.userEnableAi;
    const isLoggedIn = userStore.basicInfo && Object.keys(userStore.basicInfo).length > 0;
    return isEnabled && isLoggedIn;
  });

  // 明亮/暗黑主题水印字体颜色适配
  const fontColor = computed(() => {
    return settingsStore.theme === ThemeMode.DARK
      ? 'rgba(255, 255, 255, .15)'
      : 'rgba(0, 0, 0, .15)';
  });
</script>
