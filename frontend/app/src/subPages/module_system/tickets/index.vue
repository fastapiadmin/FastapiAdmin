<script setup lang="ts">
import type { TicketForm, TicketItem } from '@/api/module_system/ticket'
import { onLoad, onPullDownRefresh } from '@dcloudio/uni-app'
import { computed, reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { TicketAPI } from '@/api/module_system/ticket'
import { useI18nNavTitle } from '@/composables/useI18nNavTitle'

definePage({ name: 'work-tickets', style: { navigationBarTitleText: '工单管理', enablePullDownRefresh: true } })
useI18nNavTitle('tickets.title')

const { t } = useI18n()
const router = useRouter()
const toast = useToast()
const dialog = useGlobalDialog()
const searchTitle = ref('')
const showForm = ref(false)
const formTitle = ref('')
const currentId = ref<number>()
const initForm: TicketForm = { title: '', ticket_content: '', ticket_type: '', status: undefined, description: '' }
const formData = reactive<TicketForm>({ ...initForm })
const showPickerType = ref(false)
const showPickerStatus = ref(false)

const TYPE_OPTIONS = [
  { value: 'suggestion', labelKey: 'common.type.suggestion' },
  { value: 'bug', labelKey: 'common.type.bug' },
  { value: 'optimize', labelKey: 'common.type.optimize' },
  { value: 'other', labelKey: 'common.type.other' },
]

const STATUS_OPTIONS = [
  { value: 0, labelKey: 'common.status.pending' },
  { value: 1, labelKey: 'common.status.processing' },
  { value: 2, labelKey: 'common.status.completed' },
  { value: 3, labelKey: 'common.status.closed' },
]

/** 顶部状态筛选 Tab */
const TAB_OPTIONS = [
  { titleKey: 'common.all', value: undefined },
  { titleKey: 'common.status.pending', value: 0 },
  { titleKey: 'common.status.processing', value: 1 },
  { titleKey: 'common.status.completed', value: 2 },
  { titleKey: 'common.status.closed', value: 3 },
]
const activeTab = ref<number | string>(0)
const activeStatus = ref<number | undefined>()
/** 类型筛选（wd-drop-menu 下拉，标题栏紧凑、展开面板全宽） */
const typeFilter = ref<string | number>('')
const TYPE_FILTER_OPTIONS = computed(() => [
  { label: t('tickets.allType'), value: '' },
  ...TYPE_OPTIONS.map(o => ({ label: t(o.labelKey), value: o.value })),
])

interface PickerConfirmEvent { value: Array<string | number>, selectedOptions: any[] }
function handleTypeConfirm(e: PickerConfirmEvent) {
  const item = TYPE_OPTIONS.find(o => o.value === e.value[0])
  if (item)
    formData.ticket_type = item.value
  showPickerType.value = false
}
function handleStatusConfirm(e: PickerConfirmEvent) {
  const item = STATUS_OPTIONS.find(o => o.value === e.value[0])
  if (item)
    formData.status = item.value
  showPickerStatus.value = false
}

/** 工单状态：数字 → StatusBadge 内置 key，由 StatusBadge 的 map prop 一次性映射 */
const TICKET_STATUS_MAP: Record<number, string> = { 0: 'pending', 1: 'processing', 2: 'completed', 3: 'closed' }
function typeLabel(type?: string) {
  const opt = TYPE_OPTIONS.find(o => o.value === type)
  return opt ? t(opt.labelKey) : (type || '')
}
function statusLabel(status: number | string | undefined) {
  const opt = STATUS_OPTIONS.find(o => o.value === Number(status))
  return opt ? t(opt.labelKey) : ''
}
const typePickerColumns = computed(() => [TYPE_OPTIONS.map(o => ({ value: o.value, label: t(o.labelKey) }))])
const statusPickerColumns = computed(() => [STATUS_OPTIONS.map(o => ({ value: o.value, label: t(o.labelKey) }))])

const { list, total, loading, error, loadData, reload, refreshData, toFirst, loadNext } = useListPage<TicketItem>({
  fetcher: p => TicketAPI.getPage({
    ...p,
    title: searchTitle.value || undefined,
    status: activeStatus.value,
    ticket_type: typeFilter.value === '' ? undefined : String(typeFilter.value),
  }),
  onError: () => toast.error(t('common.loadFailed')),
})

/** 是否存在筛选条件（用于空状态文案区分） */
const hasFilter = computed(() => !!searchTitle.value || !!typeFilter.value || activeStatus.value !== undefined)

function handleTypeFilter(e: { value: string | number }) {
  typeFilter.value = e.value
  toFirst()
}

function handleTabChange(e: { index: number }) {
  activeStatus.value = TAB_OPTIONS[e.index]?.value
  toFirst()
}

function onSearch() {
  toFirst()
}
function onClearSearch() {
  searchTitle.value = ''
  toFirst()
}
function resetForm() {
  Object.assign(formData, { ...initForm })
}
function openCreate() {
  formTitle.value = t('tickets.create')
  currentId.value = undefined
  resetForm()
  showForm.value = true
}
function navigateToDetail(id: number) {
  router.push({ name: 'work-ticket-detail', query: { id: String(id) } })
}
/** 左滑删除：wd-swipe-action 展开后点击右侧按钮触发 */
function onSwipeRight(item: TicketItem, e: { value: string }) {
  if (e.value === 'right')
    handleDelete(item.id!)
}
async function handleSubmit() {
  if (!formData.title.trim()) {
    toast.warning(t('tickets.titleRequired'))
    return
  }
  loading.value = true
  try {
    if (currentId.value) {
      await TicketAPI.update(currentId.value, { ...formData })
      toast.success(t('common.updateSuccess'))
      showForm.value = false
      refreshData()
    }
    else {
      await TicketAPI.create({ ...formData })
      toast.success(t('common.createSuccess'))
      showForm.value = false
      reload()
    }
  }
  catch { toast.error(t('common.operationFailed')) }
  finally { loading.value = false }
}
function handleDelete(id: number) {
  dialog.confirm({
    title: t('common.title'),
    msg: t('common.deleteConfirm'),
    success: async ({ action }) => {
      if (action === 'confirm') {
        try {
          await TicketAPI.remove([id])
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
  <view class="page-wraper pb-6">
    <!-- 查询区：搜索 + 类型下拉 / 状态筛选（不再用 wd-row，避免负外边距撑出横向滚动） -->
    <view class="mx-4 pt-3">
      <wd-search
        v-model="searchTitle"
        class="fa-search"
        :placeholder="t('tickets.searchPlaceholder')"
        placeholder-left
        @search="onSearch"
        @clear="onClearSearch"
      >
        <template #suffix>
          <wd-drop-menu custom-class="ticket-type-filter" :z-index="20">
            <wd-drop-menu-item v-model="typeFilter" :options="TYPE_FILTER_OPTIONS" :title="t('tickets.typeFilter')" @change="handleTypeFilter" />
          </wd-drop-menu>
        </template>
      </wd-search>
    </view>
    <wd-tabs v-model="activeTab" line-theme="text" sticky :offset-top="0" class="ticket-tabs mt-3" @change="handleTabChange">
      <wd-tab v-for="opt in TAB_OPTIONS" :key="opt.titleKey" :title="t(opt.titleKey)" />
    </wd-tabs>

    <!-- 卡片列表（左滑删除） -->
    <SkeletonPage v-if="loading && list.length === 0" :rows="5" />
    <template v-else>
      <view class="mx-4 mt-3">
        <view v-if="error && !loading && list.length === 0" class="flex flex-col items-center gap-3 py-12">
          <wd-icon name="no-result" size="48px" color="var(--wot-text-auxiliary)" />
          <wd-text class="wot-text-text-secondary text-3" :text="t('common.loadFailed')" />
          <wd-button size="small" type="primary" plain @click="reload">
            {{ t('common.retry') }}
          </wd-button>
        </view>
        <wd-empty v-else-if="!loading && list.length === 0" :tip="hasFilter ? t('tickets.emptyWithFilter') : t('tickets.empty')" />
        <view v-else class="ticket-list overflow-hidden rounded-4">
          <wd-swipe-action
            v-for="(item, index) in list"
            :key="item.id"
            @click="onSwipeRight(item, $event)"
          >
            <template #right>
              <view class="wot-bg-danger-main h-full flex items-center justify-center px-6" style="color: #fff;">
                <wd-text class="text-3" :text="t('common.delete')" />
              </view>
            </template>
            <view
              class="ticket-row"
              :class="{ 'ticket-row--last': index === list.length - 1 }"
              @click="navigateToDetail(item.id!)"
            >
              <view class="flex items-center justify-between gap-2">
                <text class="ticket-title">
                  {{ item.title }}
                </text>
                <StatusBadge :status="item.status" :map="TICKET_STATUS_MAP" />
              </view>
              <view class="mt-1 flex items-center gap-1.5">
                <text class="ticket-meta">
                  {{ typeLabel(item.ticket_type) }}
                </text>
                <text v-if="item.created_time" class="ticket-meta">
                  · {{ item.created_time.slice(0, 10) }}
                </text>
                <text class="ticket-meta ticket-id">
                  #{{ item.id }}
                </text>
              </view>
              <text v-if="item.ticket_content" class="ticket-desc">
                {{ item.ticket_content }}
              </text>
            </view>
          </wd-swipe-action>
        </view>
      </view>
      <!-- 触底加载更多提示 -->
      <wd-loading v-if="loading && list.length > 0" size="20px" class="mx-auto my-2 block" />
      <wd-text v-else-if="total > 0 && list.length >= total" class="wot-text-text-auxiliary my-2 block text-center text-3" :text="t('common.noMore')" />
      <!-- 底部安全区（全面屏 Home 条避让） -->
      <wd-gap height="100rpx" safe-area-bottom />
    </template>

    <!-- 新增悬浮按钮（bottom gap 上移避让 Home 条） -->
    <wd-fab v-if="!showForm" position="right-bottom" :expandable="false" :gap="{ bottom: 40 }" @click="openCreate" />

    <!-- 表单弹窗 -->
    <wd-popup v-model="showForm" position="bottom" round custom-style="max-height: 80vh; overflow-y: auto;" @close="showForm = false">
      <view class="p-xl">
        <wd-navbar :title="formTitle" left-arrow @click-left="showForm = false" />
        <wd-form :model="formData" class="mt-lg">
          <wd-form-item :label="t('tickets.formTitle')" border>
            <wd-input v-model="formData.title" :placeholder="t('common.placeholder')" />
          </wd-form-item>
          <wd-form-item :label="t('tickets.content')" border>
            <wd-textarea v-model="formData.ticket_content" :placeholder="t('common.placeholder')" />
          </wd-form-item>
          <wd-form-item :label="t('tickets.type')" border>
            <view class="flex-1" aria-role="button" :aria-label="t('tickets.type')" @click="showPickerType = true">
              <wd-cell :value="typeLabel(formData.ticket_type) || t('common.selectPlaceholder')" is-link :border="false" />
            </view>
            <wd-picker :visible="showPickerType" :columns="typePickerColumns" @confirm="handleTypeConfirm" @cancel="showPickerType = false" />
          </wd-form-item>
          <wd-form-item v-if="currentId" :label="t('common.field.status')" border>
            <view class="flex-1" aria-role="button" :aria-label="t('common.field.status')" @click="showPickerStatus = true">
              <wd-cell :value="statusLabel(formData.status) || t('common.selectPlaceholder')" is-link :border="false" />
            </view>
            <wd-picker :visible="showPickerStatus" :columns="statusPickerColumns" @confirm="handleStatusConfirm" @cancel="showPickerStatus = false" />
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

<style lang="scss">
/* 工单状态页签：5 个状态在 375px 下保持单行可读 */
/* 类型筛选：与搜索框同高同圆角的独立胶囊按钮，避免出现第二块白色方块 */
.ticket-type-filter {
  display: inline-flex;
  height: 44px;
  flex-shrink: 0;
  align-items: center;
  box-sizing: border-box;
  padding: 0 12px;
  margin-left: 8px;
  background: var(--wot-filled-oppo);
  border: 1px solid var(--wot-border-main);
  border-radius: 12px;
}

.ticket-tabs {
  --wot-tabs-nav-item-font-size: 13px;
  --wot-tabs-nav-item-padding: 13px 6px;
  border-bottom: 1px solid var(--wot-border-main);
}

.ticket-list {
  background: var(--wot-filled-content);
  border: 1px solid var(--wot-border-main);
}

.ticket-row {
  padding: 12px 16px;
  border-bottom: 1px solid var(--wot-border-main);
}

.ticket-row--last {
  border-bottom: none;
}

.ticket-title {
  display: block;
  flex: 1;
  min-width: 0;
  overflow: hidden;
  color: var(--wot-text-main);
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.ticket-meta {
  color: var(--wot-text-auxiliary);
  font-size: 12px;
}

.ticket-id {
  margin-left: auto;
}

.ticket-desc {
  display: block;
  margin-top: 6px;
  overflow: hidden;
  color: var(--wot-text-secondary);
  font-size: 12px;
  white-space: nowrap;
  text-overflow: ellipsis;
}
</style>
