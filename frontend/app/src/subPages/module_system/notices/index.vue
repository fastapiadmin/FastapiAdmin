<script setup lang="ts">
import type { NoticeForm, NoticeItem } from '@/api/module_system/notice'
import { onLoad, onPullDownRefresh } from '@dcloudio/uni-app'
import { reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { NoticeAPI } from '@/api/module_system/notice'
import { useI18nNavTitle } from '@/composables/useI18nNavTitle'

definePage({ name: 'work-notices', style: { navigationBarTitleText: '通知公告', enablePullDownRefresh: true } })
useI18nNavTitle('notices.title')

const { t } = useI18n()
const toast = useToast()
const searchTitle = ref('')
const showForm = ref(false)
const formTitle = ref('')
const currentId = ref<number>()
const formData = reactive<NoticeForm>({ notice_title: '', notice_content: '', notice_type: '1', status: 0, description: '' })

const NOTICE_TYPE_OPTIONS = [
  { value: '1', labelKey: 'notices.notice' },
  { value: '2', labelKey: 'notices.announce' },
]
const STATUS_OPTIONS = [
  { value: 0, labelKey: 'common.status.draft' },
  { value: 1, labelKey: 'common.status.published' },
  { value: 2, labelKey: 'common.status.archived' },
]

/** 公告状态：数字 → StatusBadge 内置 key，由 StatusBadge 的 map prop 一次性映射 */
const NOTICE_STATUS_MAP: Record<string, string> = { 0: 'draft', 1: 'published', 2: 'archived' }

const { list, total, loading, loadData, reload, refreshData, toFirst, loadNext } = useListPage<NoticeItem>({
  fetcher: p => NoticeAPI.getPage({ ...p, notice_title: searchTitle.value || undefined }),
  onError: () => toast.error(t('common.loadFailed')),
})

function onSearch() {
  toFirst()
}
function onReset() {
  searchTitle.value = ''
  toFirst()
}
function resetForm() {
  Object.assign(formData, { notice_title: '', notice_content: '', notice_type: '1', status: 0, description: '' })
}
function openCreate() {
  formTitle.value = t('notices.createTitle')
  currentId.value = undefined
  resetForm()
  showForm.value = true
}
async function openEdit(id: number) {
  formTitle.value = t('notices.editTitle')
  currentId.value = id
  try {
    const detail = await NoticeAPI.getDetail(id)
    Object.assign(formData, {
      notice_title: detail.notice_title || '',
      notice_content: detail.notice_content || '',
      notice_type: detail.notice_type || '1',
      status: detail.status ?? 0,
      description: detail.description || '',
    })
    showForm.value = true
  }
  catch { toast.error(t('notices.detailFailed')) }
}
async function handleSubmit() {
  loading.value = true
  try {
    if (currentId.value) {
      await NoticeAPI.update(currentId.value, formData)
      toast.success(t('common.updateSuccess'))
      showForm.value = false
      refreshData()
    }
    else {
      await NoticeAPI.create(formData)
      toast.success(t('common.createSuccess'))
      showForm.value = false
      reload()
    }
  }
  catch { toast.error(t('common.operationFailed')) }
  finally { loading.value = false }
}
const dialog = useGlobalDialog()
function handleDelete(id: number) {
  dialog.confirm({
    title: t('common.title'),
    msg: t('common.deleteConfirm'),
    success: async ({ action }) => {
      if (action === 'confirm') {
        try {
          await NoticeAPI.remove([id])
          toast.success(t('common.deleteSuccess'))
          refreshData()
        }
        catch { toast.error(t('common.deleteFailed')) }
      }
    },
  })
}

onReachBottom(() => {
  if (!loading.value)
    loadNext()
})
onPullDownRefresh(async () => {
  try {
    await refreshData()
  }
  finally {
    uni.stopPullDownRefresh()
  }
})
onLoad(() => loadData())
</script>

<template>
  <view class="page-wraper">
    <!-- 搜索栏（微信原生风格） -->
    <wd-search
      v-model="searchTitle"
      :placeholder="t('notices.searchPlaceholder')"
      hide-cancel
      @search="onSearch"
      @clear="onReset"
    />

    <!-- 列表头部：总数 -->
    <view class="mx-3 mb-2 mt-3 flex items-center justify-between px-1">
      <wd-text class="wot-text-text-secondary text-3" :text="t('notices.count', { count: total })" />
    </view>

    <SkeletonPage v-if="loading && list.length === 0" :rows="5" search />
    <template v-else>
      <view class="mx-3">
        <wd-empty v-if="!loading && list.length === 0" :tip="searchTitle ? t('notices.emptyWithFilter') : t('notices.empty')" />
        <wd-cell-group v-else border custom-class="rounded-2! overflow-hidden">
          <wd-cell v-for="item in list" :key="item.id" center is-link @click="openEdit(item.id!)">
            <template #title>
              <view class="min-w-0 flex-1">
                <view class="flex items-center justify-between gap-2">
                  <wd-text class="wot-text-text-main truncate text-3.5 font-medium" :text="item.notice_title" />
                  <wd-text class="wot-text-text-auxiliary shrink-0 text-2.5" :text="(item.created_time || '').slice(0, 10)" />
                </view>
                <view class="mt-1 flex items-center justify-between gap-2">
                  <wd-text class="wot-text-text-auxiliary truncate text-2.5" :text="item.description || ''" />
                  <view class="flex shrink-0 items-center gap-2">
                    <StatusBadge :status="item.status" :map="NOTICE_STATUS_MAP" />
                    <wd-icon name="delete" size="18px" color="var(--wot-danger-main)" @click.stop="handleDelete(item.id!)" />
                  </view>
                </view>
              </view>
            </template>
          </wd-cell>
        </wd-cell-group>
      </view>
      <!-- 触底加载更多提示 -->
      <wd-loading v-if="loading && list.length > 0" size="20px" class="mx-auto my-2 block" />
      <wd-text v-else-if="total > 0 && list.length >= total" class="wot-text-text-auxiliary my-2 block text-center text-2.5" :text="t('common.noMore')" />
      <!-- 底部安全区（全面屏 Home 条避让） -->
      <wd-gap height="100rpx" safe-area-bottom />
    </template>

    <!-- 新增悬浮按钮 -->
    <wd-fab position="right-bottom" :expandable="false" :gap="{ bottom: 40 }" @click="openCreate" />

    <!-- 表单弹窗 -->
    <wd-popup v-model="showForm" position="bottom" round custom-style="max-height: 80vh; overflow-y: auto;" @close="showForm = false">
      <view class="p-xl">
        <wd-navbar :title="formTitle" left-arrow @click-left="showForm = false" />
        <wd-form :model="formData" class="mt-lg">
          <wd-form-item :label="t('notices.formTitle')" prop="notice_title" border>
            <wd-input v-model="formData.notice_title" :placeholder="t('common.placeholder')" />
          </wd-form-item>
          <wd-form-item :label="t('notices.content')" prop="notice_content" border>
            <wd-textarea v-model="formData.notice_content" :placeholder="t('notices.contentPlaceholder')" />
          </wd-form-item>
          <wd-form-item :label="t('notices.type')" border>
            <wd-radio-group v-model="formData.notice_type" direction="horizontal">
              <wd-radio v-for="opt in NOTICE_TYPE_OPTIONS" :key="opt.value" :value="opt.value">
                {{ t(opt.labelKey) }}
              </wd-radio>
            </wd-radio-group>
          </wd-form-item>
          <wd-form-item :label="t('common.field.status')" border>
            <wd-radio-group v-model="formData.status" direction="horizontal">
              <wd-radio v-for="opt in STATUS_OPTIONS" :key="opt.value" :value="opt.value">
                {{ t(opt.labelKey) }}
              </wd-radio>
            </wd-radio-group>
          </wd-form-item>
          <wd-form-item :label="t('common.field.remark')" border>
            <wd-textarea v-model="formData.description" :placeholder="t('common.placeholder')" />
          </wd-form-item>
        </wd-form>
        <view class="mt-xl flex gap-3">
          <wd-button block variant="plain" @click="showForm = false">
            {{ t('common.cancel') }}
          </wd-button>
          <wd-button block type="primary" :loading="loading" @click="handleSubmit">
            {{ t('common.save') }}
          </wd-button>
        </view>
      </view>
    </wd-popup>
  </view>
</template>
