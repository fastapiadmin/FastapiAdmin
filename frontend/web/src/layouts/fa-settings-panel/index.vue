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

const props = withDefaults(defineProps<Props>(), {
  open: false,
});

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
@use "@styles/core/mixin.scss" as *;

/* 设置抽屉模态框样式 */
.setting-modal {
  background: transparent !important;

  .el-drawer {
    // 背景滤镜效果
    background: var(--fa-drawer-bg) !important;
    box-shadow: 0 0 30px rgb(0 0 0 / 10%) !important;

    @include backdropBlur();

    .setting-box-wrap {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      width: calc(100% + 15px);
      margin-bottom: 10px;

      .setting-item {
        box-sizing: border-box;
        width: calc(33.333% - 15px);
        margin-right: 15px;
        text-align: center;

        .box {
          position: relative;
          box-sizing: border-box;
          display: flex;
          height: 52px;
          overflow: hidden;
          cursor: pointer;
          border: 2px solid var(--default-border);
          border-radius: 8px;
          box-shadow: 0 0 8px 0 rgb(0 0 0 / 10%);
          transition: box-shadow 0.1s;

          &.mt-16 {
            margin-top: 16px;
          }

          &.is-active {
            border: 2px solid var(--theme-color);
          }

          img {
            width: 100%;
            height: 100%;
          }
        }

        .name {
          margin-top: 6px;
          font-size: 14px;
          text-align: center;
        }
      }
    }
  }

  // 去除滚动条
  .el-drawer__body::-webkit-scrollbar {
    width: 0 !important;
  }
}

.dark {
  .setting-modal {
    .el-drawer {
      background: var(--fa-drawer-bg) !important;

      .setting-item {
        .box {
          border: 2px solid transparent;
        }
      }
    }
  }
}

/* 去除火狐浏览器滚动条 */
:deep(.el-drawer__body) {
  scrollbar-width: none;
}

/* // 移动端隐藏 */
@media screen and (width <= 800px) {
  .mobile-hide {
    display: none !important;
  }
}
</style>
