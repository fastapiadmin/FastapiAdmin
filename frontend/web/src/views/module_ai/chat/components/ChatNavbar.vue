<template>
  <div class="chat-navbar">
    <div class="navbar-left">
      <button class="collapse-btn" @click="toggleSidebar">
        <ArtSvgIcon
          v-if="!props.isSidebarCollapsed"
          :icon="resolveIconForArtSvgIcon('layout_leftbar_close_line')"
          class="size-6"
        />
        <ArtSvgIcon
          v-else
          :icon="resolveIconForArtSvgIcon('layout_leftbar_open_line')"
          class="size-6"
        />
      </button>
    </div>
    <div class="navbar-right">
      <ElButton text :icon="Setting" @click="handleToggleConnection">
        {{ isConnected ? "断开连接" : "重新连接" }}
      </ElButton>
      <ElTag
        class="connection-status"
        effect="plain"
        :type="connectionStatus === 'connected' ? 'success' : 'danger'"
      >
        <ElIcon :class="['status-icon', connectionStatus]">
          <Connection v-if="connectionStatus === 'connected'" />
          <Loading v-else-if="connectionStatus === 'connecting'" />
          <Warning v-else />
        </ElIcon>
        <span class="status-text">{{ connectionStatusText }}</span>
      </ElTag>
      <ElButton v-if="hasMessages" text :icon="Delete" @click="handleClearChat">清空对话</ElButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import ArtSvgIcon from "@/components/Core/base/art-svg-icon/index.vue";
import { resolveIconForArtSvgIcon } from "@utils/menuIcon/remix";
import { computed } from "vue";
import { Connection, Loading, Warning, Delete, Setting } from "@element-plus/icons-vue";

interface Props {
  connectionStatus: "connected" | "connecting" | "disconnected";
  isConnected: boolean;
  messageCount: number;
  isSidebarCollapsed?: boolean;
}

interface Emits {
  (e: "clear-chat"): void;
  (e: "toggle-connection"): void;
  (e: "toggle-sidebar"): void;
}

const props = withDefaults(defineProps<Props>(), {
  isSidebarCollapsed: false,
});
const emit = defineEmits<Emits>();

const connectionStatusText = computed(() => {
  switch (props.connectionStatus) {
    case "connected":
      return "已连接";
    case "connecting":
      return "连接中...";
    case "disconnected":
      return "未连接";
    default:
      return "未知状态";
  }
});

const hasMessages = computed(() => props.messageCount > 0);

const handleClearChat = () => {
  emit("clear-chat");
};

const handleToggleConnection = () => {
  emit("toggle-connection");
};

const toggleSidebar = () => {
  emit("toggle-sidebar");
};
</script>

<style lang="scss" scoped>
.chat-navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;

  .navbar-left {
    display: flex;
    gap: 12px;
    align-items: center;

    .collapse-btn {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 32px;
      height: 32px;
      padding: 0;
      color: var(--el-text-color-regular);
      cursor: pointer;
      background: transparent;
      border: none;
      border-radius: 4px;
      transition:
        background-color 0.2s,
        color 0.2s;

      &:hover {
        color: var(--el-color-primary);
        background: var(--el-color-primary-light-9);
      }

      &:focus-visible {
        outline: 2px solid var(--el-color-primary);
        outline-offset: 2px;
      }

      /* UnoCSS 图标 SVG 多随 currentColor */
      & > div {
        color: inherit;
      }

      .collapse-icon {
        width: 20px;
        height: 20px;
        color: inherit;
      }
    }
  }

  .navbar-right {
    display: flex;
    flex-wrap: nowrap;
    gap: 12px;
    align-items: center;

    /* EP 相邻按钮自带 margin-left，叠在 flex gap 上会导致间距忽大忽小 */
    :deep(.el-button) {
      margin: 0;
    }

    .connection-status {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 32px;
      padding: 0 12px;
      margin: 0;
      font-size: 14px;
      line-height: 1;

      :deep(.el-tag__content) {
        display: inline-flex;
        gap: 6px;
        align-items: center;
      }

      .status-icon {
        &.connected {
          color: var(--el-color-success);
        }

        &.connecting {
          color: var(--el-color-warning);
        }

        &.disconnected {
          color: var(--el-color-danger);
        }
      }

      .status-text {
        color: var(--el-text-color-secondary);
      }
    }
  }
}
</style>
