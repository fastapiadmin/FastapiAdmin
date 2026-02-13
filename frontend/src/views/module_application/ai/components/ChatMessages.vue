<template>
  <div ref="messagesContainer" class="chat-messages">
    <WelcomeScreen v-if="messages.length === 0" @prompt-click="handlePromptClick" />
    <div v-else class="messages-list">
      <MessageItem
        v-for="message in messages"
        :key="message.id"
        :message="message"
        @toggle-fold="handleToggleFold(message)"
      />
    </div>
    <div v-if="error" class="error-banner">
      <el-alert :title="error" type="error" :closable="true" show-icon @close="handleErrorClose" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, watch } from "vue";
import WelcomeScreen from "./WelcomeScreen.vue";
import MessageItem from "./MessageItem.vue";
import type { ChatMessage } from "@/api/module_application/ai";

interface Props {
  messages: ChatMessage[];
  error: string;
}

interface Emits {
  (e: "prompt-click", prompt: string): void;
  (e: "error-close"): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const messagesContainer = ref<HTMLElement>();

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
};

watch(
  () => props.messages,
  () => {
    scrollToBottom();
  },
  { deep: true }
);

const handlePromptClick = (prompt: string) => {
  emit("prompt-click", prompt);
};

const handleToggleFold = (message: ChatMessage) => {
  message.collapsed = !message.collapsed;
};

const handleErrorClose = () => {
  emit("error-close");
};

defineExpose({
  scrollToBottom,
});
</script>

<style lang="scss" scoped>
.chat-messages {
  height: 100%;
  overflow-y: auto;
  background: var(--el-bg-color);

  .messages-list {
    max-width: 800px;
    padding: 24px;
    margin: 0 auto;
  }

  .error-banner {
    position: fixed;
    bottom: 140px;
    left: 50%;
    z-index: 1000;
    padding: 0 24px;
    transform: translateX(-50%);
  }
}
</style>
