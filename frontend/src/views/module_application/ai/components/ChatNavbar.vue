<template>
  <div class="chat-navbar">
    <div class="navbar-left">
      <button class="collapse-btn" @click="toggleSidebar">
        <div v-if="!props.isSidebarCollapsed" class="i-svg:layout_leftbar_close_line w-6 h-6" />
        <div v-else class="i-svg:layout_leftbar_open_line w-6 h-6" />
      </button>
    </div>
    <div class="navbar-right">
      <el-button v-if="hasMessages" text :icon="Delete" @click="handleClearChat">
        清空对话
      </el-button>
      <el-button text :icon="Setting" @click="handleToggleConnection">
        {{ isConnected ? "断开连接" : "重新连接" }}
      </el-button>
      <el-tag
        class="connection-status"
        effect="plain"
        :type="connectionStatus === 'connected' ? 'success' : 'danger'"
      >
        <el-icon :class="['status-icon', connectionStatus]">
          <Connection v-if="connectionStatus === 'connected'" />
          <Loading v-else-if="connectionStatus === 'connecting'" />
          <Warning v-else />
        </el-icon>
        <span class="status-text">{{ connectionStatusText }}</span>
      </el-tag>
    </div>
  </div>
</template>

<script setup lang="ts">
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
      cursor: pointer;
      background: transparent;
      border: none;
      border-radius: 4px;
      transition: background-color 0.2s;

      &:hover {
        background: var(--el-fill-color-light);
      }

      .collapse-icon {
        width: 20px;
        height: 20px;
        color: var(--el-text-color-regular);
      }
    }
  }

  .navbar-right {
    display: flex;
    gap: 12px;
    align-items: center;

    .connection-status {
      display: flex;
      gap: 8px;
      align-items: center;
      font-size: 14px;

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
