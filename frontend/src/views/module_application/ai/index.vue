<template>
  <div class="chatgpt-container">
    <!-- 主聊天区域 -->
    <div class="main-chat">
      <!-- 顶部导航栏 -->
      <div class="chat-navbar">
        <div class="navbar-left">
          <h2>FA智能助手</h2>
        </div>
        <div class="navbar-right">
          <div class="connection-status">
            <el-icon :class="['status-icon', connectionStatus]">
              <Connection v-if="connectionStatus === 'connected'" />
              <Loading v-else-if="connectionStatus === 'connecting'" />
              <Warning v-else />
            </el-icon>
            <span class="status-text">{{ connectionStatusText }}</span>
          </div>
          <el-button v-if="messages.length > 0" text :icon="Delete" @click="clearCurrentChat">
            清空对话
          </el-button>
          <el-button text :icon="Setting" @click="toggleConnection">
            {{ isConnected ? "断开连接" : "重新连接" }}
          </el-button>
        </div>
      </div>

      <!-- 聊天消息区域 -->
      <div ref="messagesContainer" class="chat-messages">
        <!-- 欢迎界面 -->
        <div v-if="messages.length === 0" class="welcome-screen">
          <div class="welcome-content">
            <div class="ai-logo">
              <el-icon size="64"><ChatDotRound /></el-icon>
            </div>
            <h1>FA智能助手</h1>
            <p class="welcome-subtitle">
              我是您的专属AI助手，可以帮您回答问题、处理任务和进行智能对话
            </p>

            <div class="example-prompts">
              <div class="prompt-card" @click="setPrompt('请介绍一下FastApiAdmin系统')">
                <h4>系统介绍</h4>
                <p>请介绍一下FastApiAdmin系统</p>
              </div>
              <div class="prompt-card" @click="setPrompt('如何在系统中创建新的模块？')">
                <h4>开发指导</h4>
                <p>如何在系统中创建新的模块？</p>
              </div>
              <div class="prompt-card" @click="setPrompt('系统的权限管理是如何工作的？')">
                <h4>权限管理</h4>
                <p>FA系统的权限管理是如何工作的？</p>
              </div>
              <div class="prompt-card" @click="setPrompt('如何优化FA系统的性能？')">
                <h4>性能优化</h4>
                <p>如何优化系统的性能？</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 消息列表 -->
        <div v-else class="messages-list">
          <div
            v-for="message in messages"
            :key="message.id"
            :class="['message-group', message.type]"
          >
            <div class="message-avatar">
              <div v-if="message.type === 'user'" class="user-avatar">
                <el-icon><User /></el-icon>
              </div>
              <div v-else class="ai-avatar">
                <el-icon><ChatDotRound /></el-icon>
              </div>
            </div>
            <div class="message-content">
              <div class="message-header">
                <strong class="sender-name">
                  {{ message.type === "user" ? "You" : "FA助手" }}
                </strong>
              </div>
              <div class="message-body">
                <div
                  v-if="message.type === 'assistant' && message.loading"
                  class="typing-indicator"
                >
                  <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
                <div v-else class="message-text" v-html="formatMessage(message.content)"></div>
              </div>
              <div v-if="!message.loading" class="message-actions">
                <el-button
                  text
                  size="small"
                  :icon="CopyDocument"
                  @click="copyMessage(message.content)"
                ></el-button>
                <el-button
                  v-if="message.type === 'assistant'"
                  text
                  size="small"
                  :icon="RefreshLeft"
                ></el-button>
              </div>
            </div>
          </div>
        </div>

        <!-- 错误提示 -->
        <div v-if="error" class="error-banner">
          <el-alert :title="error" type="error" :closable="true" show-icon @close="error = ''" />
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="chat-input">
        <div class="input-wrapper">
          <div class="input-container">
            <el-input
              v-model="inputMessage"
              :placeholder="isConnected ? '向FA助手发送消息...' : '请先连接到服务器'"
              :disabled="!isConnected || sending"
              type="textarea"
              :rows="1"
              :autosize="{ minRows: 1, maxRows: 6 }"
              resize="none"
              class="message-input"
              @keydown.enter.exact.prevent="sendMessage"
              @keydown.shift.enter.exact="inputMessage += '\n'"
            />
            <el-button
              :disabled="!inputMessage.trim() || !isConnected || sending"
              :loading="sending"
              class="send-button"
              type="primary"
              circle
              @click="sendMessage"
            >
              <el-icon><Promotion /></el-icon>
            </el-button>
          </div>
          <div class="input-footer">
            <span class="input-hint">按 Enter 发送消息，Shift + Enter 换行</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, computed } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import {
  ChatDotRound,
  User,
  Delete,
  Promotion,
  Connection,
  Loading,
  Warning,
  Setting,
  CopyDocument,
  RefreshLeft,
} from "@element-plus/icons-vue";

// 消息接口
interface ChatMessage {
  id: string;
  type: "user" | "assistant";
  content: string;
  timestamp: number;
  loading?: boolean;
}

// 响应式数据
const messages = ref<ChatMessage[]>([]);
const inputMessage = ref("");
const sending = ref(false);
const isConnected = ref(false);
const connectionStatus = ref<"connected" | "connecting" | "disconnected">("disconnected");
const error = ref("");
const messagesContainer = ref<HTMLElement>();

// WebSocket 连接
let ws: WebSocket | null = null;
const WS_URL = import.meta.env.VITE_APP_WS_ENDPOINT + "/api/v1/application/ai/ws";

// 计算属性
const connectionStatusText = computed(() => {
  switch (connectionStatus.value) {
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

// WebSocket 连接管理
const connectWebSocket = () => {
  if (ws?.readyState === WebSocket.OPEN) {
    return;
  }

  connectionStatus.value = "connecting";
  error.value = "";

  try {
    ws = new WebSocket(WS_URL);

    ws.onopen = () => {
      console.log("WebSocket 连接已建立");
      isConnected.value = true;
      connectionStatus.value = "connected";
      ElMessage.success("连接成功");
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
      } catch (err) {
        console.error("解析消息失败:", err);
        handleWebSocketMessage({ content: event.data });
      }
    };

    ws.onclose = (event) => {
      console.log("WebSocket 连接已关闭", event.code, event.reason);
      isConnected.value = false;
      connectionStatus.value = "disconnected";
    };

    ws.onerror = (error) => {
      console.error("WebSocket 错误:", error);
      isConnected.value = false;
      connectionStatus.value = "disconnected";
      ElMessage.error("连接失败，请检查服务器状态");
    };
  } catch (err) {
    console.error("创建 WebSocket 连接失败:", err);
    connectionStatus.value = "disconnected";
    error.value = "无法创建连接";
  }
};

// 断开连接
const disconnectWebSocket = () => {
  if (ws) {
    ws.close(1000, "用户主动断开");
    ws = null;
  }
  isConnected.value = false;
  connectionStatus.value = "disconnected";
};

// 切换连接状态
const toggleConnection = () => {
  if (isConnected.value) {
    disconnectWebSocket();
    ElMessage.info("已断开连接");
  } else {
    connectWebSocket();
  }
};

// 处理 WebSocket 消息
const handleWebSocketMessage = (data: any) => {
  // 查找最后一个助手消息
  const lastMessage = messages.value[messages.value.length - 1];

  if (lastMessage && lastMessage.type === "assistant" && lastMessage.loading) {
    // 更新加载中的消息
    lastMessage.content = data.content || data.message || "收到回复";
    lastMessage.loading = false;
  } else {
    // 添加新的助手消息
    addMessage("assistant", data.content || data.message || "收到回复");
  }

  scrollToBottom();
};

// 发送消息
const sendMessage = async () => {
  const message = inputMessage.value.trim();
  if (!message || !isConnected.value || sending.value) {
    return;
  }

  // 添加用户消息
  addMessage("user", message);
  inputMessage.value = "";

  // 添加加载中的助手消息
  const loadingMessage: ChatMessage = {
    id: generateId(),
    type: "assistant",
    content: "",
    timestamp: Date.now(),
    loading: true,
  };
  messages.value.push(loadingMessage);

  sending.value = true;
  scrollToBottom();

  try {
    // 发送消息到 WebSocket
    if (ws?.readyState === WebSocket.OPEN) {
      const payload = {
        message,
        timestamp: Date.now(),
      };
      ws.send(JSON.stringify(payload));
    } else {
      throw new Error("WebSocket 连接未建立");
    }
  } catch (err) {
    console.error("发送消息失败:", err);
    // 移除加载消息并显示错误
    messages.value.pop();
    error.value = "发送消息失败，请检查连接状态";
    ElMessage.error("发送失败");
  } finally {
    sending.value = false;
  }
};

// 添加消息
const addMessage = (type: "user" | "assistant", content: string) => {
  const message: ChatMessage = {
    id: generateId(),
    type,
    content,
    timestamp: Date.now(),
  };
  messages.value.push(message);
  nextTick(() => scrollToBottom());
};

const clearCurrentChat = async () => {
  try {
    await ElMessageBox.confirm("确定要清空当前对话吗？此操作不可恢复。", "确认清空", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });

    messages.value = [];
    ElMessage.success("对话已清空");
  } catch {
    // 用户取消
  }
};

// 设置提示词
const setPrompt = (prompt: string) => {
  inputMessage.value = prompt;
};

// 复制消息
const copyMessage = async (content: string) => {
  try {
    await navigator.clipboard.writeText(content);
    ElMessage.success("已复制到剪贴板");
  } catch {
    // 降级方案
    const textArea = document.createElement("textarea");
    textArea.value = content;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand("copy");
    document.body.removeChild(textArea);
    ElMessage.success("已复制到剪贴板");
  }
};

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
};

// 格式化消息内容
const formatMessage = (content: string) => {
  if (!content) return "";

  // 简单的 Markdown 支持
  return content
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/`(.*?)`/g, "<code>$1</code>")
    .replace(/\n/g, "<br>");
};

// 生成唯一ID
const generateId = () => {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
};

// 生命周期
onMounted(() => {
  connectWebSocket();
});

onUnmounted(() => {
  disconnectWebSocket();
});
</script>

<style lang="scss" scoped>
.chatgpt-container {
  display: flex;
  height: calc(100vh - 120px);
  overflow: hidden;
  background: var(--el-bg-color);
}

// 主聊天区域
.main-chat {
  position: relative;
  display: flex;
  flex: 1;
  flex-direction: column;
  overflow: hidden;

  .chat-navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 24px;
    background: var(--el-bg-color);
    border-bottom: 1px solid var(--el-border-color-light);

    .navbar-left {
      h2 {
        margin: 0;
        font-size: 18px;
        font-weight: 600;
        color: var(--el-text-color-primary);
      }
    }

    .navbar-right {
      display: flex;
      gap: 16px;
      align-items: center;

      .connection-status {
        display: flex;
        gap: 8px;
        align-items: center;
        font-size: 12px;

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

  .chat-messages {
    flex: 1;
    padding-bottom: 120px; // 为底部输入框留出空间
    overflow-y: auto;
    background: var(--el-bg-color);

    // 欢迎界面
    .welcome-screen {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
      padding: 32px;
      text-align: center;

      .welcome-content {
        max-width: 800px;

        .ai-logo {
          margin-bottom: 24px;
          color: var(--el-color-primary);
        }

        h1 {
          margin: 0 0 16px;
          font-size: 32px;
          font-weight: 600;
          color: var(--el-text-color-primary);
        }

        .welcome-subtitle {
          margin-bottom: 32px;
          font-size: 16px;
          line-height: 1.5;
          color: var(--el-text-color-secondary);
        }

        .example-prompts {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
          gap: 16px;
          max-width: 600px;

          .prompt-card {
            padding: 20px;
            text-align: left;
            cursor: pointer;
            background: var(--el-bg-color-page);
            border: 1px solid var(--el-border-color-light);
            border-radius: 12px;
            transition: all 0.2s ease;

            &:hover {
              border-color: var(--el-color-primary);
              box-shadow: var(--el-box-shadow-light);
              transform: translateY(-2px);
            }

            h4 {
              margin: 0 0 8px;
              font-size: 14px;
              font-weight: 600;
              color: var(--el-text-color-primary);
            }

            p {
              margin: 0;
              font-size: 13px;
              line-height: 1.4;
              color: var(--el-text-color-secondary);
            }
          }
        }
      }
    }

    // 消息列表
    .messages-list {
      max-width: 800px;
      padding: 24px;
      margin: 0 auto;

      .message-group {
        display: flex;
        gap: 16px;
        margin-bottom: 32px;

        .message-avatar {
          flex-shrink: 0;

          .user-avatar {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            font-size: 14px;
            color: white;
            background: var(--el-color-primary);
            border-radius: 6px;
          }

          .ai-avatar {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            font-size: 14px;
            color: white;
            background: var(--el-color-success);
            border-radius: 6px;
          }
        }

        .message-content {
          flex: 1;
          min-width: 0;

          .message-header {
            margin-bottom: 8px;

            .sender-name {
              font-size: 14px;
              font-weight: 600;
              color: var(--el-text-color-primary);
            }
          }

          .message-body {
            .message-text {
              font-size: 15px;
              line-height: 1.6;
              color: var(--el-text-color-primary);
              word-wrap: break-word;

              :deep(p) {
                margin: 0 0 12px;

                &:last-child {
                  margin-bottom: 0;
                }
              }

              :deep(code) {
                padding: 2px 6px;
                font-family: "JetBrains Mono", "Courier New", monospace;
                font-size: 14px;
                background: var(--el-fill-color-light);
                border-radius: 4px;
              }

              :deep(pre) {
                padding: 16px;
                margin: 12px 0;
                overflow-x: auto;
                background: var(--el-fill-color-light);
                border-radius: 8px;

                code {
                  padding: 0;
                  background: none;
                }
              }

              :deep(strong) {
                font-weight: 600;
              }

              :deep(em) {
                font-style: italic;
              }

              :deep(ul),
              :deep(ol) {
                padding-left: 20px;
                margin: 12px 0;
              }

              :deep(li) {
                margin: 4px 0;
              }
            }

            .typing-indicator {
              display: flex;
              gap: 8px;
              align-items: center;
              color: var(--el-text-color-secondary);

              .typing-dots {
                display: flex;
                gap: 4px;

                span {
                  width: 8px;
                  height: 8px;
                  background: var(--el-text-color-secondary);
                  border-radius: 50%;
                  animation: typing 1.4s infinite;

                  &:nth-child(2) {
                    animation-delay: 0.2s;
                  }
                  &:nth-child(3) {
                    animation-delay: 0.4s;
                  }
                }
              }
            }
          }

          .message-actions {
            display: flex;
            gap: 4px;
            margin-top: 8px;
            opacity: 0;
            transition: opacity 0.2s ease;

            .el-button {
              min-height: auto;
              padding: 4px 8px;
            }
          }

          &:hover .message-actions {
            opacity: 1;
          }
        }
      }
    }

    .error-banner {
      padding: 16px 24px;
    }
  }

  // 输入区域
  .chat-input {
    position: fixed;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 10;
    padding: 16px 24px 24px;
    background: var(--el-bg-color);
    border-top: 1px solid var(--el-border-color-light);

    .input-wrapper {
      max-width: 800px;
      margin: 0 auto;

      .input-container {
        position: relative;
        background: var(--el-bg-color-page);
        border: 1px solid var(--el-border-color);
        border-radius: 12px;
        box-shadow: var(--el-box-shadow-light);
        transition: border-color 0.2s ease;

        &:focus-within {
          border-color: var(--el-color-primary);
          box-shadow: var(--el-box-shadow);
        }

        .message-input {
          :deep(.el-textarea__inner) {
            padding: 16px 60px 16px 16px;
            font-size: 15px;
            line-height: 1.5;
            resize: none;
            background: transparent;
            border: none;
            box-shadow: none;

            &:focus {
              border: none;
              box-shadow: none;
            }
          }
        }

        .send-button {
          position: absolute;
          right: 12px;
          bottom: 12px;
          width: 32px;
          height: 32px;
          min-height: 32px;
          padding: 0;
        }
      }

      .input-footer {
        display: flex;
        justify-content: center;
        margin-top: 12px;

        .input-hint {
          font-size: 12px;
          color: var(--el-text-color-secondary);
        }
      }
    }
  }
}

@keyframes typing {
  0%,
  20% {
    opacity: 0.4;
    transform: scale(0.8);
  }
  50% {
    opacity: 1;
    transform: scale(1);
  }
  80%,
  100% {
    opacity: 0.4;
    transform: scale(0.8);
  }
}

// 滚动条样式
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: transparent;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: var(--el-fill-color);
  border-radius: 3px;

  &:hover {
    background: var(--el-fill-color-dark);
  }
}
</style>
