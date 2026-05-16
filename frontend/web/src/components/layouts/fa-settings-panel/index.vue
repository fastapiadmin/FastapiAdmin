<!-- 设置面板 -->
<template>
  <div class="layout-settings">
    <FaSettingDrawer v-model="showDrawer" @open="handleOpen" @close="handleClose">
      <!-- 头部关闭按钮 -->
      <FaSettingHeader @close="closeDrawer" />
      <!-- 主题风格 -->
      <FaThemeSettings />
      <!-- 菜单布局 -->
      <FaMenuLayoutSettings />
      <!-- 菜单风格 -->
      <FaMenuStyleSettings />
      <!-- 系统主题色 -->
      <FaColorSettings />
      <!-- 盒子样式 -->
      <FaBoxStyleSettings />
      <!-- 容器宽度 -->
      <FaContainerSettings />
      <!-- 基础配置 -->
      <FaBasicSettings />
      <!-- 操作按钮 -->
      <FaSettingActions />
    </FaSettingDrawer>
  </div>
</template>

<script setup lang="ts">
import { useSettingsPanel } from "./composables/useSettingsPanel";

defineOptions({ name: "FaSettingsPanel" });

interface Props {
  /** 是否打开 */
  open?: boolean;
}

const props = defineProps<Props>();

// 使用设置面板逻辑
const settingsPanel = useSettingsPanel();
const { showDrawer } = settingsPanel;

// 获取各种处理器
const { handleOpen, handleClose, closeDrawer } = settingsPanel.useDrawerControl();
const { initializeSettings, cleanupSettings } = settingsPanel.useSettingsInitializer();

// 监听 props 变化
settingsPanel.usePropsWatcher(props);

onMounted(() => {
  initializeSettings();
});

onUnmounted(() => {
  cleanupSettings();
});
</script>

<style lang="scss">
@use "@styles/fa-settings-panel";
</style>
