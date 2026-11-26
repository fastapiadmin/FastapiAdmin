<script setup lang="ts">
import type { AIModelConfig, AIModelForm } from '@/api/module_ai/chat'
import { onLoad, onPullDownRefresh } from '@dcloudio/uni-app'
import { computed, reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { formatMessage } from '@/locales/format'
import { ChatAPI } from '@/api/module_ai/chat'
import { useI18nNavTitle } from '@/composables/useI18nNavTitle'

definePage({
  name: 'work-ai-models',
  style: { navigationBarTitleText: 'AI 模型配置', enablePullDownRefresh: true },
})
useI18nNavTitle('aiModels.title')

const { t } = useI18n()
const toast = useToast()
const dialog = useGlobalDialog()
const loading = ref(false)
const loadError = ref(false)
const models = ref<AIModelConfig[]>([])
/** 当前激活的模型配置 id（后端通过 active_id 集中管理激活态） */
const activeId = ref<number | null>(null)

const showForm = ref(false)
const formTitle = ref(t('aiModels.createTitle'))
const editingId = ref<number | null>(null)
const submitting = ref(false)
/** 表单分组折叠：默认全部展开 */
const activeCollapse = ref<string[]>(['basic', 'advanced'])
const form = reactive<AIModelForm>({
  name: '',
  base_url: '',
  api_key: '',
  model_id: '',
  temperature: 0.7,
})

/** 温度绑定（wd-slider 需 number 类型，保留 1 位小数） */
const temperature = computed<number>({
  get: () => form.temperature ?? 0.7,
  set: (v) => {
    form.temperature = Math.round(v * 10) / 10
  },
})

async function loadModels() {
  loading.value = true
  loadError.value = false
  try {
    const res = await ChatAPI.getModels()
    // 接口返回 { items, active_id }，取 items 并过滤 null/undefined 元素
    models.value = (res.items || []).filter((m): m is AIModelConfig => m != null)
    activeId.value = res.active_id ?? null
  }
  catch {
    loadError.value = true
    toast.error(t('aiModels.loadFailed'))
  }
  finally {
    loading.value = false
    uni.stopPullDownRefresh()
  }
}

function openCreate() {
  formTitle.value = t('aiModels.createTitle')
  editingId.value = null
  Object.assign(form, { name: '', base_url: '', api_key: '', model_id: '', temperature: 0.7 })
  showForm.value = true
}

function openEdit(model: AIModelConfig) {
  formTitle.value = t('aiModels.editTitle')
  editingId.value = model.config_id
  Object.assign(form, {
    name: model.name,
    base_url: model.base_url,
    api_key: model.api_key,
    model_id: model.model_id,
    temperature: model.temperature ?? 0.7,
  })
  showForm.value = true
}

async function submitForm() {
  if (!form.name.trim())
    return toast.warning(t('aiModels.nameRequired'))
  if (!form.base_url.trim())
    return toast.warning(t('aiModels.baseUrlRequired'))
  if (!form.model_id.trim())
    return toast.warning(t('aiModels.modelIdRequired'))
  submitting.value = true
  try {
    if (editingId.value) {
      await ChatAPI.updateModel(editingId.value, { ...form })
      toast.success(t('common.updateSuccess'))
    }
    else {
      await ChatAPI.createModel({ ...form })
      toast.success(t('common.createSuccess'))
    }
    showForm.value = false
    loadModels()
  }
  catch { toast.error(t('aiModels.saveFailed')) }
  finally {
    submitting.value = false
  }
}

function handleDelete(configId: number) {
  dialog.confirm({
    title: t('common.title'),
    msg: t('aiModels.deleteConfirm'),
    success: async ({ action }) => {
      if (action !== 'confirm')
        return
      try {
        await ChatAPI.deleteModel(configId)
        toast.success(t('common.deleteSuccess'))
        loadModels()
      }
      catch { toast.error(t('common.deleteFailed')) }
    },
  })
}

function handleActivate(configId: number) {
  dialog.confirm({
    title: t('common.title'),
    msg: t('aiModels.activateConfirm'),
    success: async ({ action }) => {
      if (action !== 'confirm')
        return
      try {
        await ChatAPI.activateModel(configId)
        toast.success(t('aiModels.activated'))
        loadModels()
      }
      catch { toast.error(t('aiModels.activateFailed')) }
    },
  })
}

onPullDownRefresh(() => {
  loadModels()
})
onLoad(() => {
  loadModels()
})
</script>

<template>
  <view class="page-wraper py-3">
    <!-- List -->
    <SkeletonPage v-if="loading && models.length === 0" :rows="3" />
    <view v-else-if="loadError && models.length === 0" class="mx-4 flex flex-col items-center gap-3 py-12">
      <wd-icon name="no-result" size="48px" color="var(--wot-text-auxiliary)" />
      <wd-text class="wot-text-text-secondary text-3" :text="t('aiModels.loadFailed')" />
      <wd-button size="small" type="primary" @click="loadModels">
        {{ t('common.retry') }}
      </wd-button>
    </view>
    <template v-else>
      <view class="mx-4">
        <wd-empty v-if="!loading && models.length === 0" :tip="t('aiModels.empty')" />
        <view v-else class="model-list wot-bg-filled-oppo overflow-hidden rounded-4">
          <view class="model-list__head flex items-center justify-between">
            <text class="model-list__title">{{ t('aiModels.groupTitle') }}</text>
            <text class="model-list__count">{{ formatMessage(t, 'aiModels.count', { count: models.length }) }}</text>
          </view>
          <view v-for="model in models" :key="model.config_id" class="model-row">
            <view class="flex items-start justify-between gap-3">
              <view class="min-w-0 flex-1">
                <view class="flex min-w-0 items-center gap-2">
                  <text class="model-name truncate">{{ model.name || t('aiModels.unnamed') }}</text>
                  <wd-tag v-if="model.config_id === activeId" size="small" type="success" round>
                    {{ t('aiModels.inUse') }}
                  </wd-tag>
                  <view
                    v-else
                    class="tap-target shrink-0"
                    aria-role="button"
                    :aria-label="t('aiModels.activate')"
                    @click.stop="handleActivate(model.config_id)"
                  >
                    <wd-text class="text-3" :text="t('aiModels.activate')" type="primary" />
                  </view>
                </view>
                <view class="model-meta">
                  {{ model.model_id }} · {{ t('aiModels.temperature') }} {{ model.temperature ?? '—' }}
                </view>
                <view class="model-meta">
                  {{ model.base_url }}
                </view>
              </view>
              <view class="flex shrink-0 items-center">
                <view class="icon-action" aria-role="button" :aria-label="t('common.edit')" @click.stop="openEdit(model)">
                  <wd-icon name="edit" size="18px" color="var(--wot-text-auxiliary)" />
                </view>
                <view class="icon-action" aria-role="button" :aria-label="t('common.delete')" @click.stop="handleDelete(model.config_id)">
                  <wd-icon name="delete" size="18px" color="var(--wot-danger-main)" />
                </view>
              </view>
            </view>
          </view>
        </view>
      </view>
    </template>

    <!-- 新增悬浮按钮（bottom gap 上移避让 Home 条） -->
    <wd-fab v-if="!showForm" position="right-bottom" :expandable="false" :gap="{ bottom: 40 }" @click="openCreate" />

    <!-- Form Popup -->
    <wd-popup v-model="showForm" position="bottom" round custom-style="max-height: 80vh; overflow-y: auto;" @close="showForm = false">
      <view class="px-4 pb-4 pt-2">
        <wd-navbar :title="formTitle" left-arrow @click-left="showForm = false" />
        <wd-form :model="form" class="mt-4">
          <wd-collapse v-model="activeCollapse" :border="false">
            <wd-collapse-item :title="t('aiModels.basic')" name="basic" :border="false">
              <wd-form-item :label="t('aiModels.name')" border>
                <wd-input v-model="form.name" :placeholder="t('aiModels.namePlaceholder')" clearable />
              </wd-form-item>
              <wd-form-item :label="t('aiModels.modelId')" border>
                <wd-input v-model="form.model_id" :placeholder="t('aiModels.modelIdPlaceholder')" clearable />
              </wd-form-item>
              <wd-form-item :label="t('aiModels.baseUrl')" border>
                <wd-input v-model="form.base_url" placeholder="https://api.openai.com/v1" clearable />
              </wd-form-item>
            </wd-collapse-item>
            <wd-collapse-item :title="t('aiModels.advanced')" name="advanced" :border="false">
              <wd-form-item label="API Key" border>
                <wd-input v-model="form.api_key" placeholder="sk-..." show-password clearable />
              </wd-form-item>
              <wd-form-item :label="t('aiModels.temperatureLabel')" border>
                <view class="w-full flex items-center gap-3">
                  <wd-slider v-model="temperature" class="flex-1" :min="0" :max="2" :step="0.1" show-extreme-value active-color="var(--wot-primary-6)" />
                  <wd-text class="wot-text-text-main w-16 text-right text-3 font-semibold" :text="temperature.toFixed(1)" />
                </view>
              </wd-form-item>
            </wd-collapse-item>
          </wd-collapse>
        </wd-form>
        <view class="mt-4 flex gap-3">
          <wd-button variant="plain" block @click="showForm = false">
            {{ t('common.cancel') }}
          </wd-button>
          <wd-button block type="primary" :loading="submitting" @click="submitForm">
            {{ editingId ? t('aiModels.update') : t('aiModels.create') }}
          </wd-button>
        </view>
      </view>
    </wd-popup>
  </view>
</template>

<style lang="scss" scoped>
/* 模型行：文字列与操作列分离，长文本单行省略，不再被操作按钮挤到断词 */
.model-list {
  border: 1px solid var(--wot-border-main);
}

.model-list__head {
  padding: 12px 16px;
  border-bottom: 1px solid var(--wot-border-main);
}

.model-list__title {
  color: var(--fa-text-1);
  font-size: 15px;
  font-weight: 600;
}

.model-list__count {
  color: var(--fa-text-3);
  font-size: 12.5px;
}

.model-row {
  padding: 14px 16px;
  border-bottom: 1px solid var(--wot-border-main);
}

.model-row:last-child {
  border-bottom: none;
}

.model-name {
  min-width: 0;
  color: var(--fa-text-1);
  font-size: 15px;
  font-weight: 600;
}

.model-meta {
  margin-top: 2px;
  overflow: hidden;
  color: var(--fa-text-3);
  font-size: 12.5px;
  white-space: nowrap;
  text-overflow: ellipsis;
}
</style>
