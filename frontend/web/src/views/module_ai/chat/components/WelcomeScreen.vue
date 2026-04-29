<template>
  <div class="welcome-screen">
    <div class="welcome-content">
      <div class="ai-logo">
        <el-icon size="64"><ChatDotRound /></el-icon>
      </div>
      <h1>FA智能助手</h1>
      <p class="welcome-subtitle">我是您的专属AI助手，可以帮您回答问题、处理任务和进行智能对话</p>

      <div class="example-prompts">
        <div
          v-for="card in promptCards"
          :key="card.prompt"
          class="prompt-card"
          role="button"
          tabindex="0"
          @click="handlePromptClick(card.prompt)"
          @keydown.enter.prevent="handlePromptClick(card.prompt)"
          @keydown.space.prevent="handlePromptClick(card.prompt)"
        >
          <h4>{{ card.title }}</h4>
          <p>{{ card.body }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ChatDotRound } from "@element-plus/icons-vue";

interface Emits {
  (e: "prompt-click", prompt: string): void;
}

const emit = defineEmits<Emits>();

const promptCards = [
  { title: "系统介绍", body: "请介绍一下FastApiAdmin系统", prompt: "请介绍一下FastApiAdmin系统" },
  { title: "开发指导", body: "如何在系统中创建新的模块？", prompt: "如何在系统中创建新的模块？" },
  {
    title: "权限管理",
    body: "FA系统的权限管理是如何工作的？",
    prompt: "系统的权限管理是如何工作的？",
  },
  { title: "性能优化", body: "如何优化系统的性能？", prompt: "如何优化FA系统的性能？" },
];

const handlePromptClick = (prompt: string) => {
  emit("prompt-click", prompt);
};
</script>

<style lang="scss" scoped>
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
        background: var(--el-bg-color-overlay);
        border: 1px solid var(--el-border-color-light);
        border-radius: 12px;
        transition:
          border-color 0.2s ease,
          box-shadow 0.2s ease,
          transform 0.2s ease;

        &:hover {
          border-color: var(--el-color-primary);
          box-shadow: var(--el-box-shadow-light);
          transform: translateY(-2px);
        }

        &:focus-visible {
          outline: 2px solid var(--el-color-primary);
          outline-offset: 2px;
          border-color: var(--el-color-primary);
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
</style>
