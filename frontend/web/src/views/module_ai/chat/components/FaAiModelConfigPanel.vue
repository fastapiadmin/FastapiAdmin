<template>
  <FaDrawer
    v-model="drawerVisible"
    :title="$t('common.aiConfig.title')"
    size="60%"
    destroy-on-close
  >
    <div class="ai-model-config">
      <div v-if="loading" class="loading-tip">
        <ElIcon class="is-loading"><Loading /></ElIcon>
        <span>{{ $t("common.aiConfig.loading") }}</span>
      </div>
      <template v-else>
        <!-- 顶部状态栏 -->
        <div class="status-bar">
          <div class="status-info">
            <span class="status-title">{{ $t("common.aiConfig.current") }}</span>
            <ElTag :type="activeId ? 'primary' : 'info'" effect="dark" size="small">
              <ElIcon class="tag-icon"
                ><FaSvgIcon v-if="activeId" icon="ri:checkbox-circle-line" /><Cpu v-else
              /></ElIcon>
              <span>{{ activeModelName }}</span>
            </ElTag>
          </div>
          <ElButton
            v-if="items.length > 0"
            :disabled="!activeId"
            size="small"
            plain
            @click="handleUseDefault"
          >
            <ElIcon><RefreshLeft /></ElIcon>
            <span>{{ $t("common.aiConfig.restore") }}</span>
          </ElButton>
        </div>

        <!-- 配置列表 -->
        <div class="config-section">
          <div class="section-header">
            <div class="header-left">
              <span class="section-title">{{ $t("common.aiConfig.configuredModels") }}</span>
              <ElTag v-if="items.length > 0" size="small" effect="plain" type="info">
                {{ items.length }} {{ $t("common.aiConfig.countUnit") }}
              </ElTag>
            </div>
          </div>

          <!-- 空状态 - 统一 FaEmptyState -->
          <FaEmptyState
            v-if="items.length === 0"
            icon="ri:cpu-line"
            :title="$t('common.aiConfig.emptyTitle')"
            :description="$t('common.aiConfig.emptyDesc')"
          >
            <ElButton type="primary" size="large" :icon="Plus" @click="openCreate">
              {{ $t("common.aiConfig.addNow") }}
            </ElButton>
          </FaEmptyState>

          <!-- 列表 -->
          <div v-else class="config-list">
            <TransitionGroup name="list" tag="div" class="list-inner">
              <div
                v-for="item in items"
                :key="item.id"
                class="config-item"
                :class="{
                  active: item.id === activeId,
                  expanded: expandedId === item.id,
                  flash: flashId === item.id,
                }"
                @click="handleItemClick(item)"
              >
                <div class="config-item-main">
                  <div class="item-icon-wrap">
                    <ElIcon class="item-icon" :size="18">
                      <FaSvgIcon v-if="item.id === activeId" icon="ri:checkbox-circle-line" />
                      <ChatLineSquare v-else />
                    </ElIcon>
                  </div>
                  <div class="item-content">
                    <div class="item-row1">
                      <span class="item-name">{{ item.name }}</span>
                      <ElTag v-if="item.id === activeId" type="success" size="small" effect="light">
                        {{ $t("common.aiConfig.inUse") }}
                      </ElTag>
                    </div>
                    <div class="item-model">{{ item.model_id }}</div>
                  </div>
                  <div class="item-actions" @click.stop>
                    <ElTooltip
                      :content="$t('common.aiConfig.expand')"
                      placement="top"
                      :show-after="200"
                    >
                      <ElButton text circle size="small" @click="toggleExpand(item.id)">
                        <ElIcon :class="{ rotated: expandedId === item.id }">
                          <ArrowDown />
                        </ElIcon>
                      </ElButton>
                    </ElTooltip>
                    <ElTooltip
                      :content="$t('common.aiConfig.hintEdit')"
                      placement="top"
                      :show-after="200"
                    >
                      <ElButton text circle size="small" :icon="Edit" @click="openEdit(item)" />
                    </ElTooltip>
                    <ElTooltip
                      :content="$t('common.aiConfig.hintDelete')"
                      placement="top"
                      :show-after="200"
                    >
                      <ElButton
                        text
                        circle
                        size="small"
                        :icon="Delete"
                        @click="handleDelete(item)"
                      />
                    </ElTooltip>
                  </div>
                </div>
                <!-- 展开详情 -->
                <div v-show="expandedId === item.id" class="item-detail">
                  <div class="detail-row">
                    <span class="detail-label">Base URL</span>
                    <span class="detail-value">{{ item.base_url }}</span>
                  </div>
                  <div class="detail-row">
                    <span class="detail-label">API Key</span>
                    <div class="api-key-wrap">
                      <span class="detail-value api-key">
                        {{ showKeyId === item.id ? item.api_key : `****${maskKey(item.api_key)}` }}
                      </span>
                      <ElButton
                        text
                        size="small"
                        @click="showKeyId = showKeyId === item.id ? null : item.id"
                      >
                        <ElIcon
                          ><FaSvgIcon v-if="showKeyId !== item.id" icon="ri:eye-line" /><Hide
                            v-else
                        /></ElIcon>
                      </ElButton>
                      <ElButton
                        text
                        size="small"
                        :disabled="!item.api_key"
                        @click="copyKey(item.api_key)"
                      >
                        <ElIcon><FaSvgIcon icon="ri:file-copy-line" /></ElIcon>
                      </ElButton>
                    </div>
                  </div>
                  <div class="detail-row">
                    <span class="detail-label">Temperature</span>
                    <span class="detail-value">{{ item.temperature.toFixed(1) }}</span>
                  </div>
                  <div v-if="item.created_time" class="detail-row">
                    <span class="detail-label">{{ $t("common.aiConfig.addedAt") }}</span>
                    <span class="detail-value">{{ item.created_time }}</span>
                  </div>
                </div>
              </div>
            </TransitionGroup>
          </div>
        </div>

        <!-- 底部固定添加按钮 - 始终可见 -->
        <div v-if="items.length > 0" class="footer-add">
          <ElButton type="primary" :icon="Plus" class="add-btn" @click="openCreate">
            {{ $t("common.aiConfig.addModel") }}
          </ElButton>
        </div>
      </template>

      <!-- 新增/编辑弹窗 -->
      <FaDialog
        v-model="dialogVisible"
        :title="form.id ? $t('common.aiConfig.editModel') : $t('common.aiConfig.newModel')"
        :close-on-click-modal="false"
        size="sm"
      >
        <ElForm
          ref="formRef"
          :model="form"
          :rules="rules"
          label-width="96px"
          label-position="right"
          @submit.prevent="handleSave"
        >
          <ElFormItem :label="$t('common.aiConfig.configName')" prop="name">
            <ElInput
              v-model="form.name"
              :placeholder="$t('common.aiConfig.namePlaceholder')"
              maxlength="50"
              show-word-limit
              clearable
              autofocus
            />
          </ElFormItem>
          <ElFormItem label="Base URL" prop="base_url">
            <ElInput v-model="form.base_url" placeholder="https://api.openai.com/v1" clearable>
              <template #append>
                <ElDropdown trigger="click" @command="(v: string) => (form.base_url = v)">
                  <ElButton text size="small">
                    {{ $t("common.aiConfig.presetLabel") }}
                    <ElIcon><ArrowDown /></ElIcon>
                  </ElButton>
                  <template #dropdown>
                    <ElDropdownMenu>
                      <ElDropdownItem
                        v-for="preset in baseUrlPresets"
                        :key="preset.label"
                        :command="preset.url"
                      >
                        <div class="preset-item">
                          <span class="preset-label">{{ preset.label }}</span>
                          <span class="preset-url">{{ preset.url }}</span>
                        </div>
                      </ElDropdownItem>
                    </ElDropdownMenu>
                  </template>
                </ElDropdown>
              </template>
            </ElInput>
          </ElFormItem>
          <ElFormItem label="API Key" prop="api_key">
            <ElInput
              v-model="form.api_key"
              type="password"
              placeholder="sk-..."
              show-password
              clearable
            />
          </ElFormItem>
          <ElFormItem :label="$t('common.aiConfig.modelId')" prop="model_id">
            <div class="w-full">
              <div class="flex items-center gap-2">
                <ElInput
                  v-model="form.model_id"
                  :placeholder="$t('common.aiConfig.modelPlaceholder')"
                  clearable
                  class="flex-1"
                />
                <ElButton :loading="probingModels" @click="fetchAvailableModels">{{
                  $t("common.aiConfig.fetchModels")
                }}</ElButton>
                <ElButton :loading="testingConnection" @click="testConnection">{{
                  $t("common.aiConfig.testConnection")
                }}</ElButton>
              </div>
              <div v-if="availableModels.length" class="mt-1.5 flex flex-wrap gap-1">
                <ElTag
                  v-for="m in availableModels"
                  :key="m.id"
                  size="small"
                  class="cursor-pointer"
                  @click="form.model_id = m.id"
                >
                  {{ m.id }}
                </ElTag>
              </div>
            </div>
          </ElFormItem>
          <ElFormItem label="Temperature" prop="temperature">
            <ElSlider
              v-model="form.temperature"
              :min="0"
              :max="2"
              :step="0.1"
              show-input
              :show-input-controls="false"
            />
            <div class="form-tip">{{ $t("common.aiConfig.creativityTip") }}</div>
          </ElFormItem>
        </ElForm>
        <template #footer>
          <ElButton @click="dialogVisible = false">{{ $t("common.aiConfig.cancel") }}</ElButton>
          <ElButton type="primary" :loading="saving" @click="handleSave">
            <ElIcon><FaSvgIcon icon="ri:check-line" /></ElIcon>
            <span>{{
              form.id ? $t("common.aiConfig.save") : $t("common.aiConfig.addAndUse")
            }}</span>
          </ElButton>
        </template>
      </FaDialog>
    </div>
  </FaDrawer>
</template>

<script setup lang="ts">
import { ElMessage } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";
import {
  Plus,
  Edit,
  Delete,
  Cpu,
  ChatLineSquare,
  ArrowDown,
  RefreshLeft,
  Loading,
  Hide,
} from "@element-plus/icons-vue";
import AiChatAPI, {
  type AiModelConfigInput,
  type AiModelConfigItem,
  type AiModelConfigList,
  type AiModelOption,
} from "@/api/module_ai/chat";
import FaDialog from "@/components/modal/fa-dialog/index.vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n();

const emit = defineEmits<{
  (e: "changed"): void;
  (e: "update:modelValue", value: boolean): void;
}>();

interface Props {
  modelValue?: boolean;
}

const props = withDefaults(defineProps<Props>(), { modelValue: false });
const drawerVisible = computed({
  get: () => props.modelValue,
  set: (val: boolean) => emit("update:modelValue", val),
});

const loading = ref(false);
const saving = ref(false);
const items = ref<AiModelConfigItem[]>([]);
const activeId = ref<string | null>(null);
const expandedId = ref<string | null>(null);
const showKeyId = ref<string | null>(null);
const flashId = ref<string | null>(null);
const dialogVisible = ref(false);

const formRef = ref<FormInstance>();
const form = reactive<AiModelConfigItem>({
  id: "",
  name: "",
  base_url: "",
  api_key: "",
  model_id: "",
  temperature: 0.7,
  created_time: null,
});

// 模型探测：拉取可用模型 / 连通性测试（按表单中填写、尚未保存的参数）
const probingModels = ref(false);
const testingConnection = ref(false);
const availableModels = ref<AiModelOption[]>([]);

async function fetchAvailableModels() {
  if (!form.base_url || !form.api_key) {
    ElMessage.warning(t("common.aiConfig.needBase"));
    return;
  }
  probingModels.value = true;
  try {
    const res = await AiChatAPI.listAvailableModels({
      base_url: form.base_url,
      api_key: form.api_key,
    });
    availableModels.value = res.data.data || [];
    if (availableModels.value.length) {
      ElMessage.success(t("common.aiConfig.fetched", { n: availableModels.value.length }));
    } else {
      ElMessage.warning(t("common.aiConfig.noModels"));
    }
  } catch {
    // 统一错误提示已由 http 层处理
  } finally {
    probingModels.value = false;
  }
}

async function testConnection() {
  if (!form.base_url || !form.api_key || !form.model_id) {
    ElMessage.warning(t("common.aiConfig.needAll"));
    return;
  }
  testingConnection.value = true;
  try {
    const res = await AiChatAPI.testModelConnection({
      base_url: form.base_url,
      api_key: form.api_key,
      model_id: form.model_id,
    });
    ElMessage.success(t("common.aiConfig.connected", { ms: res.data.data?.latency_ms ?? "-" }));
  } catch {
    // 统一错误提示已由 http 层处理
  } finally {
    testingConnection.value = false;
  }
}

// 常用 Base URL 预设 - 提升用户输入效率
const baseUrlPresets = [
  { label: t("common.aiConfig.presetOpenai"), url: "https://api.openai.com/v1" },
  { label: "DeepSeek", url: "https://api.deepseek.com/v1" },
  {
    label: t("common.aiConfig.presetQwen"),
    url: "https://dashscope.aliyuncs.com/compatible-mode/v1",
  },
  { label: t("common.aiConfig.presetMoonshot"), url: "https://api.moonshot.cn/v1" },
  { label: t("common.aiConfig.presetZhipu"), url: "https://open.bigmodel.cn/api/paas/v4" },
  { label: t("common.aiConfig.presetOllama"), url: "http://localhost:11434/v1" },
];

const rules: FormRules<AiModelConfigInput> = {
  name: [{ required: true, message: t("common.aiConfig.needName"), trigger: "blur" }],
  base_url: [
    { required: true, message: t("common.aiConfig.needBaseUrl"), trigger: "blur" },
    {
      validator: (_rule, value: string, callback) => {
        if (!value) return callback();
        if (!/^https?:\/\//.test(value)) {
          callback(new Error(t("common.aiConfig.needHttp")));
        } else {
          callback();
        }
      },
      trigger: "blur",
    },
  ],
  api_key: [{ required: true, message: t("common.aiConfig.needKey"), trigger: "blur" }],
  model_id: [{ required: true, message: t("common.aiConfig.needModel"), trigger: "blur" }],
  temperature: [{ required: true, message: t("common.aiConfig.needTemp"), trigger: "change" }],
};

const activeModelName = computed(() => {
  if (!activeId.value) return t("common.aiConfig.systemDefault");
  const item = items.value.find((i) => i.id === activeId.value);
  return item?.name || t("common.aiConfig.systemDefault");
});

const loadList = async () => {
  loading.value = true;
  try {
    const res = await AiChatAPI.getModelConfig();
    if (res.data?.code === 0 && res.data.data) {
      const data: AiModelConfigList = res.data.data;
      items.value = data.items || [];
      activeId.value = data.active_id;
    }
  } catch {
    ElMessage.error(t("common.aiConfig.loadFailed"));
  } finally {
    loading.value = false;
  }
};

const resetForm = () => {
  form.id = "";
  form.name = "";
  form.base_url = "";
  form.api_key = "";
  form.model_id = "";
  form.temperature = 0.7;
  form.created_time = null;
  formRef.value?.clearValidate();
};

const openCreate = () => {
  resetForm();
  dialogVisible.value = true;
};

const openEdit = (item: AiModelConfigItem) => {
  form.id = item.id;
  form.name = item.name;
  form.base_url = item.base_url;
  form.api_key = item.api_key;
  form.model_id = item.model_id;
  form.temperature = item.temperature;
  form.created_time = item.created_time;
  formRef.value?.clearValidate();
  dialogVisible.value = true;
};

const handleSave = async () => {
  if (!formRef.value || saving.value) return;
  try {
    await formRef.value.validate();
  } catch {
    return;
  }
  saving.value = true;
  try {
    const payload: AiModelConfigInput = {
      name: form.name,
      base_url: form.base_url,
      api_key: form.api_key,
      model_id: form.model_id,
      temperature: form.temperature,
    };
    let res;
    if (form.id) {
      res = await AiChatAPI.updateModelConfig(form.id, payload);
    } else {
      res = await AiChatAPI.createModelConfig(payload);
    }
    if (res.data?.code === 0) {
      const newId = form.id || res.data.data?.id;
      dialogVisible.value = false;
      if (!form.id && newId) {
        await AiChatAPI.activateModelConfig(newId);
      }
      resetForm();
      emit("changed");
      await loadList();
      if (newId) flashHighlight(newId);
      ElMessage.success(form.id ? t("common.aiConfig.saved") : t("common.aiConfig.added"));
    } else {
      ElMessage.error(res.data?.msg || t("common.aiConfig.saveFailed"));
    }
  } catch {
    ElMessage.error(t("common.aiConfig.saveFailed"));
  } finally {
    saving.value = false;
  }
};

const flashHighlight = (id: string) => {
  flashId.value = id;
  setTimeout(() => {
    flashId.value = null;
  }, 1500);
};

const handleItemClick = async (item: AiModelConfigItem) => {
  if (item.id === activeId.value) {
    toggleExpand(item.id);
    return;
  }
  try {
    const res = await AiChatAPI.activateModelConfig(item.id);
    if (res.data?.code === 0) {
      activeId.value = item.id;
      emit("changed");
    } else {
      ElMessage.error(res.data?.msg || t("common.aiConfig.switchFailed"));
    }
  } catch {
    ElMessage.error(t("common.aiConfig.switchFailed"));
  }
};

const handleUseDefault = async () => {
  try {
    const res = await AiChatAPI.activateModelConfig("");
    if (res.data?.code === 0) {
      activeId.value = null;
      emit("changed");
    } else {
      ElMessage.error(res.data?.msg || t("common.aiConfig.opFailed"));
    }
  } catch {
    ElMessage.error(t("common.aiConfig.opFailed"));
  }
};

const handleDelete = async (item: AiModelConfigItem) => {
  try {
    await confirmDelete(t("common.aiConfig.deleteConfirm", { name: item.name }));
  } catch {
    return;
  }
  try {
    const res = await AiChatAPI.deleteModelConfig(item.id);
    if (res.data?.code === 0) {
      ElMessage.success(t("common.aiConfig.deleted"));
      if (form.id === item.id) dialogVisible.value = false;
      if (expandedId.value === item.id) expandedId.value = null;
      emit("changed");
      await loadList();
    } else {
      ElMessage.error(res.data?.msg || t("common.aiConfig.deleteFailed"));
    }
  } catch {
    ElMessage.error(t("common.aiConfig.deleteFailed"));
  }
};

const toggleExpand = (id: string) => {
  expandedId.value = expandedId.value === id ? null : id;
  if (expandedId.value !== id) showKeyId.value = null;
};

const copyKey = async (key: string) => {
  if (!key) return;
  try {
    await navigator.clipboard.writeText(key);
    ElMessage.success(t("common.aiConfig.copied"));
  } catch {
    ElMessage.error(t("common.aiConfig.copyFailed"));
  }
};

const maskKey = (key: string): string => {
  if (!key) return "";
  return key.length <= 4 ? key : key.slice(-4);
};

defineExpose({ refresh: loadList });
onMounted(loadList);
</script>

<style lang="scss" scoped>
.ai-model-config {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.loading-tip {
  display: flex;
  gap: 8px;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  font-size: 13px;
  color: var(--el-text-color-secondary);
}

/* 顶部状态栏 */
.status-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: var(--el-fill-color-blank);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 8px;
}

.status-info {
  display: flex;
  gap: 8px;
  align-items: center;
}

.status-title {
  font-size: 13px;
  color: var(--el-text-color-secondary);
}

.tag-icon {
  margin-right: 2px;
}

.config-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  gap: 8px;
  align-items: center;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.empty-illust {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
}

.empty-icon-bg {
  position: absolute;
  color: var(--el-color-primary-light-7);
  opacity: 0.4;
}

.empty-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.empty-desc {
  font-size: 13px;
  line-height: 1.6;
  color: var(--el-text-color-secondary);
}

/* 列表 */
.config-list {
  width: 100%;
}

.list-inner {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.config-item {
  padding: 10px 12px;
  cursor: pointer;
  background: var(--el-fill-color-blank);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 8px;
  transition:
    background-color 0.2s,
    border-color 0.2s,
    color 0.2s,
    box-shadow 0.2s,
    transform 0.2s;

  &.active {
    background: var(--el-color-primary-light-9);
    border-color: var(--el-color-primary);

    .item-icon {
      color: var(--el-color-primary);
    }

    .item-icon-wrap {
      background: var(--el-color-primary-light-7);
    }
  }

  &.expanded {
    background: var(--el-color-primary-light-9);
  }

  &:hover {
    border-color: var(--el-color-primary-light-5);

    .item-actions {
      opacity: 1;
    }
  }

  &.flash {
    animation: flash 1.5s ease;
  }
}

@keyframes flash {
  0% {
    box-shadow: 0 0 0 0 var(--el-color-primary-light-5);
  }

  30% {
    box-shadow: 0 0 0 6px var(--el-color-primary-light-7);
  }

  100% {
    box-shadow: 0 0 0 0 transparent;
  }
}

.config-item-main {
  display: flex;
  gap: 12px;
  align-items: center;
}

.item-icon-wrap {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: var(--el-fill-color-light);
  border-radius: 8px;
  transition: background 0.2s;
}

.item-icon {
  color: var(--el-text-color-secondary);
  transition: color 0.2s;
}

.item-content {
  flex: 1;
  min-width: 0;
}

.item-row1 {
  display: flex;
  gap: 8px;
  align-items: center;
}

.item-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.item-model {
  margin-top: 2px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.item-actions {
  display: flex;
  flex-shrink: 0;
  gap: 2px;
  opacity: 0;
  transition: opacity 0.2s;
}

.config-item.expanded .item-actions {
  opacity: 1;
}

.item-detail {
  padding: 12px 0 0 44px;
  margin-top: 10px;
  border-top: 1px dashed var(--el-border-color-light);
}

.detail-row {
  display: flex;
  gap: 12px;
  align-items: center;
  padding: 4px 0;
  font-size: 12px;
}

.detail-label {
  flex-shrink: 0;
  width: 80px;
  color: var(--el-text-color-secondary);
}

.detail-value {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--el-text-color-regular);
  white-space: nowrap;

  &.api-key {
    font-family: var(--el-font-family-monospace, monospace);
  }
}

.api-key-wrap {
  display: flex;
  flex: 1;
  gap: 4px;
  align-items: center;
}

/* 底部添加 */
.footer-add {
  display: flex;
  justify-content: center;
  padding: 8px 0 0;
}

.add-btn {
  width: 100%;
  border-style: dashed;
}

/* 表单提示 */
.form-tip {
  margin-top: 4px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

/* 预设选项 */
.preset-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 2px 0;
}

.preset-label {
  font-size: 13px;
  font-weight: 500;
}

.preset-url {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

/* 列表过渡 */
.list-enter-active,
.list-leave-active {
  transition:
    background-color 0.3s ease,
    border-color 0.3s ease,
    color 0.3s ease,
    box-shadow 0.3s ease,
    transform 0.3s ease;
}

.list-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.list-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

.list-move {
  transition: transform 0.3s ease;
}
</style>
