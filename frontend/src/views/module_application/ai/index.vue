<template>
  <div class="app-container">
    <el-container class="main-chat">
      <el-aside class="sidebar-container" :class="{ collapsed: isSidebarCollapsed }">
        <Sidebar
          ref="sidebarRef"
          :current-session-id="currentSessionId"
          :is-collapsed="isSidebarCollapsed"
          @select-session="handleSelectSession"
          @new-session="handleNewSession"
        />
      </el-aside>
      <el-container class="chat-container">
        <el-header class="chat-header">
          <ChatNavbar
            :connection-status="connectionStatus"
            :is-connected="isConnected"
            :message-count="messages.length"
            :is-sidebar-collapsed="isSidebarCollapsed"
            @clear-chat="handleClearChat"
            @toggle-connection="toggleConnection"
            @toggle-sidebar="toggleSidebar"
          />
        </el-header>
        <el-main class="chat-main">
          <ChatMessages
            ref="chatMessagesRef"
            :messages="messages"
            :error="error"
            @prompt-click="handlePromptClick"
            @error-close="error = ''"
          />
        </el-main>
        <el-footer class="chat-footer">
          <ChatInput
            :disabled="!isConnected"
            :sending="sending"
            :is-connected="isConnected"
            @send="handleSendMessage"
          />
        </el-footer>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import ChatNavbar from "./components/ChatNavbar.vue";
import ChatMessages from "./components/ChatMessages.vue";
import ChatInput from "./components/ChatInput.vue";
import Sidebar from "./components/Sidebar.vue";
import AiAPI, { ChatMessage, ChatSession, UploadedFile } from "@/api/module_application/ai";
import { Auth } from "@/utils/auth";

const messages = ref<ChatMessage[]>([]);
const sending = ref(false);
const isConnected = ref(false);
const connectionStatus = ref<"connected" | "connecting" | "disconnected">("disconnected");
const error = ref<string>("");
const chatMessagesRef = ref<{ scrollToBottom: () => void }>();
const sidebarRef = ref<{ loadSessions: () => void }>();
const currentSessionId = ref<number | null>(null);
const isSidebarCollapsed = ref(false);

let ws: WebSocket | null = null;
const WS_URL = import.meta.env.VITE_APP_WS_ENDPOINT;

const connectWebSocket = () => {
  if (ws?.readyState === WebSocket.OPEN) {
    return;
  }

  connectionStatus.value = "connecting";
  error.value = "";

  try {
    // WebSocket连接不支持直接设置请求头
    // 这里使用URL参数传递token，后端需要相应处理
    const url = new URL("/api/v1/application/ai/ws", WS_URL);
    const token = Auth.getAccessToken();
    if (token) {
      url.searchParams.append("token", token);
    }

    ws = new WebSocket(url.toString());

    ws.onopen = () => {
      console.log("WebSocket 连接已建立");
      isConnected.value = true;
      connectionStatus.value = "connected";
      ElMessage.success("连接成功");
    };

    ws.onmessage = (event) => {
      handleWebSocketMessage({ content: event.data });
    };

    ws.onclose = (event) => {
      console.log("WebSocket 连接已关闭", event.code, event.reason);
      isConnected.value = false;
      connectionStatus.value = "disconnected";
      finishLoadingMessages();
    };

    ws.onerror = (err) => {
      console.error("WebSocket 错误:", err);
      isConnected.value = false;
      connectionStatus.value = "disconnected";
      ElMessage.error("连接失败，请检查服务器状态");
      finishLoadingMessages();
    };
  } catch (err) {
    console.error("创建 WebSocket 连接失败:", err);
    connectionStatus.value = "disconnected";
    error.value = "无法创建连接";
  }
};

const disconnectWebSocket = () => {
  if (ws) {
    ws.close(1000, "用户主动断开");
    ws = null;
  }
  isConnected.value = false;
  connectionStatus.value = "disconnected";
  finishLoadingMessages();
};

const toggleConnection = () => {
  if (isConnected.value) {
    disconnectWebSocket();
    ElMessage.info("已断开连接");
  } else {
    connectWebSocket();
  }
};

const handleWebSocketMessage = (data: any) => {
  const lastMessage = messages.value[messages.value.length - 1];

  if (lastMessage && lastMessage.type === "assistant" && lastMessage.loading) {
    lastMessage.content += data.content || data.message || "";
  } else {
    addMessage("assistant", data.content || data.message || "收到回复");
  }

  chatMessagesRef.value?.scrollToBottom();
};

const handleSendMessage = async (message: string, files?: UploadedFile[]) => {
  if ((!message && !files) || !isConnected.value || sending.value) {
    return;
  }

  const lastMessage = messages.value[messages.value.length - 1];
  if (lastMessage && lastMessage.type === "assistant" && lastMessage.loading) {
    lastMessage.loading = false;
  }

  // 如果没有当前会话，先创建会话
  if (!currentSessionId.value) {
    try {
      // 使用第一条消息的前20个字符作为会话标题
      const title = message.substring(0, 20) + (message.length > 20 ? "..." : "");
      const res = await AiAPI.createSession({ title });
      if (res.data?.code === 0 || res.data?.success === true) {
        currentSessionId.value = res.data.data.id ?? null;
        sidebarRef.value?.loadSessions();
      } else {
        throw new Error("创建会话失败");
      }
    } catch (err) {
      console.error("创建会话失败:", err);
      ElMessage.error("创建会话失败，请重试");
      return;
    }
  }

  addMessage("user", message, files);

  const loadingMessage: ChatMessage = {
    id: generateId(),
    type: "assistant",
    content: "",
    timestamp: Date.now(),
    loading: true,
  };
  messages.value.push(loadingMessage);

  sending.value = true;
  chatMessagesRef.value?.scrollToBottom();

  try {
    if (ws?.readyState === WebSocket.OPEN) {
      const payload = {
        message,
        session_id: currentSessionId.value,
        files: files?.map((f) => ({
          name: f.name,
          type: f.type,
          size: f.size,
        })),
      };
      ws.send(JSON.stringify(payload));
    } else {
      throw new Error("WebSocket 连接未建立");
    }
  } catch (err) {
    console.error("发送消息失败:", err);
    messages.value.pop();
    error.value = "发送消息失败，请检查连接状态";
    ElMessage.error("发送失败");
  } finally {
    sending.value = false;
  }
};

const addMessage = (type: "user" | "assistant", content: string, files?: UploadedFile[]) => {
  const message: ChatMessage = {
    id: generateId(),
    type,
    content,
    timestamp: Date.now(),
    collapsed: content.length > 200,
    files,
  };
  messages.value.push(message);
};

const handleClearChat = async () => {
  try {
    await ElMessageBox.confirm("确定要清空当前对话吗？此操作不可恢复。", "确认清空", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    messages.value = [];
    ElMessage.success("对话已清空");
  } catch {
    ElMessage.info("已取消清空对话");
  }
};

const handlePromptClick = (prompt: string) => {
  handleSendMessage(prompt);
};

const finishLoadingMessages = () => {
  messages.value.forEach((message) => {
    if (message.type === "assistant" && message.loading) {
      message.loading = false;
      message.collapsed = message.content.length > 200;
    }
  });
};

const generateId = () => {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
};

const handleSelectSession = async (session: ChatSession) => {
  currentSessionId.value = session.id;
  messages.value = [];
  await loadMessages(session.id);
  ElMessage.success(`已切换到会话：${session.title}`);
};

const handleNewSession = async () => {
  currentSessionId.value = null;
  messages.value = [];
  ElMessage.success("已开启新对话");
};

const loadMessages = async (sessionId: number) => {
  try {
    const res = await AiAPI.getMessagesBySession(sessionId, { page_no: 1, page_size: 100 });
    if (res.data?.code === 0 || res.data?.success === true) {
      const apiMessages = res.data.data?.items || [];
      messages.value = apiMessages.map((msg: any) => ({
        id: msg.id.toString(),
        type: msg.type as "user" | "assistant",
        content: msg.content,
        timestamp: msg.timestamp,
        collapsed: msg.content.length > 200,
        files: msg.files?.map((f: any) => ({
          id: generateId(),
          name: f.name || "",
          size: f.size || 0,
          type: f.type || "",
        })),
      }));
    }
  } catch (error) {
    console.error("加载消息失败:", error);
  }
};

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;
};

onMounted(() => {
  connectWebSocket();
});

onUnmounted(() => {
  disconnectWebSocket();
});
</script>

<style lang="scss" scoped>
.main-chat {
  height: 100%;
  overflow: hidden;

  .sidebar-container {
    width: 200px;
    background: var(--el-bg-color);
    transition: width 0.3s ease;

    &.collapsed {
      width: 64px;
    }
  }

  .chat-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
  }

  .chat-header {
    height: auto;
    padding: 0;
    background: var(--el-bg-color);
  }

  .chat-main {
    flex: 1;
    padding: 0;
    overflow: hidden;
  }

  .chat-footer {
    height: auto;
    min-height: 80px;
    padding: 0;
    background: var(--el-bg-color);
    border-top: 1px solid var(--el-border-color-light);
  }
}
</style>
