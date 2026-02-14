<template>
  <div class="welcome-screen">
    <div class="welcome-content">
      <div class="ai-logo">
        <el-icon size="64"><ChatDotRound /></el-icon>
      </div>
      <h1>FA智能助手</h1>
      <p class="welcome-subtitle">我是您的专属AI助手，可以帮您回答问题、处理任务和进行智能对话</p>

      <div class="example-prompts">
        <div class="prompt-card" @click="handlePromptClick('请介绍一下FastApiAdmin系统')">
          <h4>系统介绍</h4>
          <p>请介绍一下FastApiAdmin系统</p>
        </div>
        <div class="prompt-card" @click="handlePromptClick('如何在系统中创建新的模块？')">
          <h4>开发指导</h4>
          <p>如何在系统中创建新的模块？</p>
        </div>
        <div class="prompt-card" @click="handlePromptClick('系统的权限管理是如何工作的？')">
          <h4>权限管理</h4>
          <p>FA系统的权限管理是如何工作的？</p>
        </div>
        <div class="prompt-card" @click="handlePromptClick('如何优化FA系统的性能？')">
          <h4>性能优化</h4>
          <p>如何优化系统的性能？</p>
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
</style>
