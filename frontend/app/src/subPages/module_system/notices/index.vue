<script setup lang="ts">
import type { NoticeForm, NoticeItem } from '@/api/module_system/notice'
import { onLoad, onPullDownRefresh } from '@dcloudio/uni-app'
import { reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { formatMessage } from '@/locales/format'
import { NoticeAPI } from '@/api/module_system/notice'
import { useI18nNavTitle } from '@/composables/useI18nNavTitle'

definePage({ name: 'work-notices', style: { navigationBarTitleText: '通知公告', enablePullDownRefresh: true } })
useI18nNavTitle('notices.title')

const { t } = useI18n()
const toast = useToast()
const searchTitle = ref('')
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

const { list, total, loading, error, loadData, reload, refreshData, toFirst, loadNext } = useListPage<NoticeItem>({
  fetcher: p => NoticeAPI.getPage({ ...p, notice_title: searchTitle.value || undefined }),
  onError: () => toast.error(t('common.loadFailed')),
})

/** 我已读的公告 id：未读的行标题前带红点 */
const readIds = ref<Set<number>>(new Set())
const unreadCount = ref(0)

function isUnread(item: NoticeItem) {
  return item.id != null && !readIds.value.has(item.id)
}

/** 拉取已读状态（失败不影响列表浏览） */
async function loadReadState() {
  try {
    const [ids, unread] = await Promise.all([NoticeAPI.getReadIds(), NoticeAPI.getUnreadCount()])
    readIds.value = new Set(ids ?? [])
    unreadCount.value = unread?.unread ?? 0
  }
  catch {
    readIds.value = new Set()
    unreadCount.value = 0
  }
}

/** 标记单条已读：本地先变，再落库；失败不回滚（下次进入会重新拉） */
async function markOneRead(id?: number) {
  if (id == null || readIds.value.has(id))
    return
  readIds.value = new Set([...readIds.value, id])
  unreadCount.value = Math.max(0, unreadCount.value - 1)
  try {
    const res = await NoticeAPI.markRead([id])
    unreadCount.value = res?.unread ?? unreadCount.value
  }
  catch { /* 已读记录失败不打断浏览 */ }
}

/** 全部已读 */
async function markAllRead() {
  if (unreadCount.value === 0)
    return
  try {
    const res = await NoticeAPI.markRead()
    unreadCount.value = res?.unread ?? 0
    readIds.value = new Set(list.value.map(item => item.id).filter((id): id is number => id != null))
    toast.success(t('notices.markAllReadSuccess'))
  }
  catch { toast.error(t('common.operationFailed')) }
}
const showForm = ref(false)
const formTitle = ref('')
const currentId = ref<number>()
const formData = reactive<NoticeForm>({ notice_title: '', notice_content: '', notice_type: '1', status: 0, description: '' })

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
function onSwipeAction(item: NoticeItem, e: { value: string }) {
  if (e.value === 'right')
    handleDelete(item.id!)
}
function handleDelete(id: number, after?: () => void) {
  dialog.confirm({
    title: t('common.title'),
    msg: t('common.deleteConfirm'),
    success: async ({ action }) => {
      if (action === 'confirm') {
        try {
          await NoticeAPI.remove([id])
          toast.success(t('common.deleteSuccess'))
          after?.()
          refreshData()
        }
        catch { toast.error(t('common.deleteFailed')) }
      }
    },
  })
}
function deleteCurrent() {
  if (currentId.value == null)
    return
  handleDelete(currentId.value, () => {
    showForm.value = false
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
onLoad(() => {
  loadData()
  loadReadState()
})
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
    <view class="mx-4 mb-2 mt-3 flex items-center justify-between px-1">
      <wd-text class="wot-text-text-secondary text-3" :text="formatMessage(t, 'notices.count', { count: total })" />
      <view v-if="unreadCount > 0" class="flex items-center gap-3">
        <wd-text class="wot-text-danger-main text-3" :text="formatMessage(t, 'notices.unreadCount', { count: unreadCount })" />
        <view class="tap-target" aria-role="button" :aria-label="t('notices.markAllRead')" @click="markAllRead">
          <wd-text class="wot-text-primary-6 text-3" :text="t('notices.markAllRead')" />
        </view>
      </view>
    </view>

    <SkeletonPage v-if="loading && list.length === 0" :rows="5" search />
    <template v-else>
      <view class="mx-4">
        <view v-if="error && !loading && list.length === 0" class="flex flex-col items-center gap-3 py-12">
          <wd-icon name="no-result" size="48px" color="var(--wot-text-auxiliary)" />
          <wd-text class="wot-text-text-secondary text-3" :text="t('common.loadFailed')" />
          <wd-button size="small" type="primary" plain @click="reload">
            {{ t('common.retry') }}
          </wd-button>
        </view>
        <wd-empty v-else-if="!loading && list.length === 0" :tip="searchTitle ? t('notices.emptyWithFilter') : t('notices.empty')" />
        <view v-else class="notice-list overflow-hidden rounded-3">
          <wd-swipe-action
            v-for="(item, index) in list"
            :key="item.id"
            @click="onSwipeAction(item, $event)"
          >
            <template #right>
              <view class="wot-bg-danger-main h-full flex items-center justify-center px-6" style="color: #fff;">
                <wd-text class="text-3" :text="t('common.delete')" />
              </view>
            </template>
            <view
              class="notice-row"
              :class="{ 'notice-row--last': index === list.length - 1 }"
              @click="markOneRead(item.id); openEdit(item.id!)"
            >
              <view class="flex items-start gap-2.5">
                <view v-if="isUnread(item)" class="notice-dot mt-2" />
                <view class="min-w-0 flex-1">
                  <view class="flex items-start justify-between gap-2">
                    <text class="notice-title">
                      {{ item.notice_title }}
                    </text>
                    <text class="notice-date">
                      {{ (item.created_time || '').slice(0, 10) }}
                    </text>
                  </view>
                  <view class="mt-1.5 flex items-center justify-between gap-2">
                    <text class="notice-desc">
                      {{ item.description || item.notice_content || '' }}
                    </text>
                    <StatusBadge :status="item.status" :map="NOTICE_STATUS_MAP" />
                  </view>
                </view>
                <wd-icon name="arrow-right" size="16px" color="var(--wot-text-auxiliary)" class="mt-1 shrink-0" />
              </view>
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

    <!-- 新增悬浮按钮 -->
    <wd-fab v-if="!showForm" position="right-bottom" :expandable="false" :gap="{ bottom: 40 }" @click="openCreate" />

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
          <wd-button v-if="currentId" block variant="plain" type="danger" @click="deleteCurrent">
            {{ t('common.delete') }}
          </wd-button>
          <wd-button block type="primary" :loading="loading" @click="handleSubmit">
            {{ t('common.save') }}
          </wd-button>
        </view>
      </view>
    </wd-popup>
  </view>
</template>

<style lang="scss" scoped>
.notice-list {
  background: var(--wot-filled-content);
  border: 1px solid var(--wot-border-main);
}

.notice-row {
  padding: 12px 16px;
  border-bottom: 1px solid var(--wot-border-main);
}

.notice-row--last {
  border-bottom: none;
}

.notice-title {
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

.notice-date {
  flex-shrink: 0;
  color: var(--wot-text-auxiliary);
  font-size: 12px;
  line-height: 20px;
}

.notice-desc {
  display: block;
  flex: 1;
  min-width: 0;
  overflow: hidden;
  color: var(--wot-text-auxiliary);
  font-size: 12px;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.notice-dot {
  width: 8px;
  height: 8px;
  flex-shrink: 0;
  border-radius: 50%;
  background: var(--wot-danger-main);
}
</style>
