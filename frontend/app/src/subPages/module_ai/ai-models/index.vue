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
  <view class="page-wraper">
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
        <wd-cell-group v-else border custom-class="rounded-3! overflow-hidden">
          <wd-cell :title="t('aiModels.groupTitle')" :value="formatMessage(t, 'aiModels.count', { count: models.length })" border />
          <wd-cell v-for="model in models" :key="model.config_id" center>
            <template #title>
              <wd-text class="wot-text-text-main truncate text-3.5 font-medium" :text="model.name || t('aiModels.unnamed')" />
            </template>
            <template #label>
              <view class="flex flex-col">
                <wd-text class="wot-text-text-auxiliary truncate text-3" :text="`${model.model_id} · ${t('aiModels.temperature')} ${model.temperature ?? '—'}`" />
                <wd-text class="wot-text-text-auxiliary truncate text-3" :text="model.base_url" />
              </view>
            </template>
            <template #default>
              <view class="flex items-center gap-2">
                <wd-tag v-if="model.config_id === activeId" size="small" type="success" round>
                  {{ t('aiModels.inUse') }}
                </wd-tag>
                <wd-button
                  v-else
                  size="small"
                  type="primary"
                  variant="plain"
                  custom-style="min-height: 44px;"
                  @click.stop="handleActivate(model.config_id)"
                >
                  {{ t('aiModels.activate') }}
                </wd-button>
                <view class="icon-action" aria-role="button" :aria-label="t('common.edit')" @click.stop="openEdit(model)">
                  <wd-icon name="edit" size="18px" color="var(--wot-text-auxiliary)" />
                </view>
                <view class="icon-action" aria-role="button" :aria-label="t('common.delete')" @click.stop="handleDelete(model.config_id)">
                  <wd-icon name="delete" size="18px" color="var(--wot-danger-main)" />
                </view>
              </view>
            </template>
          </wd-cell>
        </wd-cell-group>
      </view>
    </template>

    <!-- 新增悬浮按钮（bottom gap 上移避让 Home 条） -->
    <wd-fab v-if="!showForm" position="right-bottom" :expandable="false" :gap="{ bottom: 40 }" @click="openCreate" />

    <!-- Form Popup -->
    <wd-popup v-model="showForm" position="bottom" round custom-style="max-height: 80vh; overflow-y: auto;" @close="showForm = false">
      <view class="p-xl">
        <wd-navbar :title="formTitle" left-arrow @click-left="showForm = false" />
        <wd-form :model="form" class="mt-lg">
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
        <view class="mt-xl flex gap-3">
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
