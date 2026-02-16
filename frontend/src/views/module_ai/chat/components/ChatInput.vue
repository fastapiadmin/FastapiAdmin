<template>
  <div class="chat-input">
    <div class="input-wrapper">
      <div v-if="uploadedFiles.length > 0" class="uploaded-files">
        <div v-for="file in uploadedFiles" :key="file.id" class="file-item">
          <el-icon class="file-icon"><Document /></el-icon>
          <span class="file-name">{{ file.name }}</span>
          <el-icon class="file-remove" @click="removeFile(file.id)"><Close /></el-icon>
        </div>
      </div>
      <div class="input-container">
        <el-form>
          <el-input
            v-model="inputMessage"
            type="textarea"
            :placeholder="placeholder"
            :disabled="disabled || sending"
            :autosize="{ minRows: 1, maxRows: 6 }"
            resize="none"
            class="message-input"
            @keydown.enter.exact.prevent="handleSend"
            @keydown.shift.enter.exact="handleShiftEnter"
          />
        </el-form>
        <div class="input-footer">
          <div class="input-actions">
            <el-upload
              ref="uploadRef"
              :auto-upload="false"
              :show-file-list="false"
              :on-change="handleFileChange"
              :accept="acceptTypes"
              :multiple="true"
            >
              <el-button :icon="Paperclip" class="upload-btn" circle />
            </el-upload>
            <el-button
              :disabled="
                (!inputMessage.trim() && uploadedFiles.length === 0) || disabled || sending
              "
              :loading="sending"
              class="send-button"
              type="primary"
              circle
              @click="handleSend"
            >
              <el-icon><Promotion /></el-icon>
            </el-button>
          </div>
        </div>
      </div>
      <div class="input-hint">
        <span>按 Enter 发送消息，Shift + Enter 换行</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { Promotion, Paperclip, Document, Close } from "@element-plus/icons-vue";
import type { UploadFile } from "element-plus";
import type { UploadedFile } from "@/api/module_ai/chat_message";

interface Props {
  disabled?: boolean;
  sending?: boolean;
  isConnected?: boolean;
}

interface Emits {
  (e: "send", message: string, files?: UploadedFile[]): void;
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false,
  sending: false,
  isConnected: true,
});

const emit = defineEmits<Emits>();

const inputMessage = ref("");
const uploadedFiles = ref<UploadedFile[]>([]);

const acceptTypes = computed(() => {
  return ".pdf,.doc,.docx,.txt,.jpg,.jpeg,.png,.gif,.mp3,.wav,.mp4,.avi,.mov";
});

const placeholder = computed(() => {
  return props.isConnected ? "向FA助手发送消息..." : "请先连接到服务器";
});

const handleFileChange = (uploadFile: UploadFile) => {
  const file = uploadFile.raw;
  if (!file) return;

  const maxSize = 10 * 1024 * 1024;
  if (file.size > maxSize) {
    alert("文件大小不能超过10MB");
    return;
  }

  const uploadedFile: UploadedFile = {
    id: Date.now().toString() + Math.random().toString(36).substr(2),
    name: file.name,
    size: file.size,
    type: file.type,
    file,
  };

  uploadedFiles.value.push(uploadedFile);
};

const removeFile = (id: string) => {
  const index = uploadedFiles.value.findIndex((f) => f.id === id);
  if (index > -1) {
    uploadedFiles.value.splice(index, 1);
  }
};

const handleSend = () => {
  const message = inputMessage.value.trim();
  if ((!message && uploadedFiles.value.length === 0) || props.disabled || props.sending) {
    return;
  }
  emit("send", message, uploadedFiles.value.length > 0 ? [...uploadedFiles.value] : undefined);
  inputMessage.value = "";
  uploadedFiles.value = [];
};

const handleShiftEnter = () => {
  inputMessage.value += "\n";
};

defineExpose({
  focus: () => {
    const input = document.querySelector(".message-input textarea") as HTMLTextAreaElement;
    input?.focus();
  },
});
</script>

<style lang="scss" scoped>
.chat-input {
  .input-wrapper {
    max-width: 800px;
    padding: 20px;
    margin: 0 auto;

    .uploaded-files {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 12px;

      .file-item {
        display: flex;
        gap: 6px;
        align-items: center;
        padding: 8px 14px;
        font-size: 13px;
        background: var(--el-fill-color-light);
        border: 1px solid var(--el-border-color-light);
        border-radius: 8px;
        transition: all 0.2s ease;

        &:hover {
          background: var(--el-color-primary-light-9);
          border-color: var(--el-color-primary-light-7);
        }

        .file-icon {
          font-size: 16px;
          color: var(--el-color-primary);
        }

        .file-name {
          max-width: 180px;
          overflow: hidden;
          text-overflow: ellipsis;
          font-size: 13px;
          white-space: nowrap;
        }

        .file-remove {
          font-size: 14px;
          color: var(--el-text-color-secondary);
          cursor: pointer;
          transition: color 0.2s ease;

          &:hover {
            color: var(--el-color-danger);
          }
        }
      }
    }

    .input-container {
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 20px;
      background: var(--el-bg-color-page);
      border: 1px solid var(--el-border-color-light);
      border-radius: 16px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
      transition: all 0.2s ease;

      &:hover {
        border-color: var(--el-color-primary);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        box-shadow: var(--el-box-shadow-light);
        transform: translateY(-2px);
      }

      .message-input {
        flex: 1;
        min-width: 0;

        :deep(.el-textarea__inner) {
          padding: 0;
          line-height: 1.6;
          color: var(--el-text-color-primary);
          resize: none;
          background: transparent;
          border: none;
          box-shadow: none;
        }

        :deep(.el-textarea) {
          padding: 0;
        }
      }

      .input-footer {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-top: 8px;

        .input-actions {
          display: flex;
          gap: 10px;
          align-items: center;

          .upload-btn {
            font-size: 18px;
            color: var(--el-text-color-secondary);
            transition: all 0.2s ease;

            &:hover {
              color: var(--el-color-primary);
              transform: scale(1.05);
            }
          }

          .send-button {
            flex-shrink: 0;
            border-radius: 50%;
            box-shadow: 0 2px 6px rgba(24, 144, 255, 0.3);
            transition: all 0.2s ease;

            &:hover {
              box-shadow: 0 4px 12px rgba(24, 144, 255, 0.4);
              transform: translateY(-1px);
            }

            &:active {
              transform: translateY(0);
            }
          }
        }
      }
    }

    .input-hint {
      margin-top: 12px;
      font-size: 12px;
      font-weight: 400;
      color: var(--el-text-color-tertiary);
      text-align: center;
      letter-spacing: 0.5px;
    }
  }
}
</style>
