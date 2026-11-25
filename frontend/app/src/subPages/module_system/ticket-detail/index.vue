<script setup lang="ts">
import type { TicketComment, TicketItem } from '@/api/module_system/ticket'
import { onLoad, onPullDownRefresh } from '@dcloudio/uni-app'
import { reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { TicketAPI } from '@/api/module_system/ticket'
import { useI18nNavTitle } from '@/composables/useI18nNavTitle'
import { useShare } from '@/composables/useShare'
import { MARKDOWN_TAG_STYLE } from '@/constants/markdown.constant'

const { t } = useI18n()
const ticket = ref<TicketItem | null>(null)
const ticketId = ref(0)

useShare(() => ({
  title: ticket.value ? t('ticketDetail.shareTitle', { title: ticket.value.title }) : t('ticketDetail.title'),
  path: `/subPages/module_system/ticket-detail/index?id=${ticketId.value}`,
}))

definePage({
  name: 'work-ticket-detail',
  style: { navigationBarTitleText: '工单详情', enablePullDownRefresh: true },
})
useI18nNavTitle('ticketDetail.title')

const toast = useToast()
const loading = ref(false)
const loadError = ref(false)
const notFound = ref(false)
const commentsLoading = ref(false)
const commentsError = ref(false)
const comments = ref<TicketComment[]>([])
const commentTotal = ref(0)
const commentPage = reactive({ page_no: 1, page_size: 20 })
const commentText = ref('')
const submitting = ref(false)
const previewRef = ref<{ open: (options: { images: string[], startPosition?: number }) => void }>()

async function loadTicket() {
  if (!ticketId.value) {
    notFound.value = true
    return
  }
  loading.value = true
  loadError.value = false
  notFound.value = false
  try {
    const res = await TicketAPI.getDetail(ticketId.value)
    ticket.value = res || null
    notFound.value = !res
  }
  catch {
    // 全局 http 层已提示具体错误；页面保留可重试的错误态，而不是伪装成“不存在”
    loadError.value = true
  }
  finally {
    loading.value = false
  }
}

/**
 * 加载评论。
 * reset=true 时从第 1 页重新加载并替换；否则把新一页追加到现有列表。
 * 旧实现每次都用 res.items 覆盖，导致“加载更多”永远只显示最后一页。
 */
async function loadComments(reset = false) {
  if (!ticketId.value || commentsLoading.value)
    return
  if (reset) {
    commentPage.page_no = 1
    comments.value = []
  }
  commentsLoading.value = true
  commentsError.value = false
  try {
    const res = await TicketAPI.getComments(ticketId.value, { page_no: commentPage.page_no, page_size: commentPage.page_size })
    const items = res.items || []
    comments.value = reset ? items : [...comments.value, ...items]
    commentTotal.value = res.total || 0
  }
  catch (e) {
    commentsError.value = true
    // 追加失败时回退页码，避免下次“加载更多”直接跳过失败页
    if (!reset)
      commentPage.page_no = Math.max(1, commentPage.page_no - 1)
    console.error(t('common.loadFailed'), e)
  }
  finally {
    commentsLoading.value = false
  }
}

function loadMoreComments() {
  if (commentsLoading.value || comments.value.length >= commentTotal.value)
    return
  commentPage.page_no += 1
  loadComments(false)
}

async function retryLoad() {
  await Promise.all([loadTicket(), loadComments(true)])
}

async function submitComment() {
  if (!commentText.value.trim())
    return toast.warning(t('ticketDetail.commentRequired'))
  submitting.value = true
  try {
    await TicketAPI.createComment(ticketId.value, { content: commentText.value.trim() })
    commentText.value = ''
    toast.success(t('ticketDetail.commentSuccess'))
    loadComments(true)
  }
  catch {
    toast.error(t('ticketDetail.commentFailed'))
  }
  finally {
    submitting.value = false
  }
}

function getTypeLabel(type?: string) {
  const map: Record<string, string> = {
    suggestion: 'common.type.suggestion',
    bug: 'common.type.bug',
    optimize: 'common.type.optimize',
    other: 'common.type.other',
  }
  return t(map[type || ''] || 'common.type.other')
}
function getTypeColor(type?: string) {
  const map: Record<string, string> = { suggestion: 'var(--wot-blue-6)', bug: 'var(--wot-danger-main)', optimize: 'var(--wot-orange-6)', other: 'var(--wot-text-auxiliary)' }
  return map[type || ''] || 'var(--wot-text-auxiliary)'
}
function getTypeBg(type?: string) {
  const map: Record<string, string> = { suggestion: 'var(--wot-blue-2)', bug: 'var(--wot-red-2)', optimize: 'var(--wot-orange-2)', other: 'var(--wot-coolgrey-2)' }
  return map[type || ''] || 'var(--wot-coolgrey-2)'
}
function getStatusLabel(status?: string | number) {
  const map: Record<string, string> = { 0: 'pending', 1: 'processing', 2: 'completed', 3: 'closed' }
  return t(`common.status.${map[String(status ?? '')] || 'unknown'}`)
}
function getStatusColor(status?: string | number) {
  const map: Record<string, string> = { 0: 'var(--wot-orange-6)', 1: 'var(--wot-blue-6)', 2: 'var(--wot-success-main)', 3: 'var(--wot-text-auxiliary)' }
  return map[String(status ?? '')] || 'var(--wot-text-auxiliary)'
}
function getStatusBg(status?: string | number) {
  const map: Record<string, string> = { 0: 'var(--wot-orange-2)', 1: 'var(--wot-blue-2)', 2: 'var(--wot-green-2)', 3: 'var(--wot-coolgrey-2)' }
  return map[String(status ?? '')] || 'var(--wot-coolgrey-2)'
}
function parseImages(images?: string): string[] {
  if (!images)
    return []
  try {
    return JSON.parse(images)
  }
  catch {
    return []
  }
}

function previewImages(images: string[], current: number) {
  previewRef.value?.open({ images, startPosition: current })
}

onPullDownRefresh(async () => {
  try {
    await Promise.all([loadTicket(), loadComments(true)])
  }
  finally {
    uni.stopPullDownRefresh()
  }
})

onLoad((options) => {
  ticketId.value = Number(options?.id || 0)
  if (!ticketId.value) {
    notFound.value = true
    return
  }
  loadTicket()
  loadComments(true)
})
</script>

<template>
  <view class="page-wraper" style="padding-bottom: calc(140rpx + env(safe-area-inset-bottom));">
    <SkeletonPage v-if="loading && !ticket" :rows="5" />

    <template v-else-if="ticket">
      <!-- Ticket Header -->
      <view class="wot-bg-filled-oppo mx-4 mb-4 rounded-3 p-4">
        <wd-text class="wot-text-text-main block text-4" :text="ticket.title || t('ticketDetail.unnamed')" bold />
        <view class="mt-3 flex gap-2">
          <wd-tag size="small" round :bg-color="getTypeBg(ticket.ticket_type)" :color="getTypeColor(ticket.ticket_type)">
            {{ getTypeLabel(ticket.ticket_type) }}
          </wd-tag>
          <wd-tag size="small" round :bg-color="getStatusBg(ticket.status)" :color="getStatusColor(ticket.status)">
            {{ getStatusLabel(ticket.status) }}
          </wd-tag>
        </view>
      </view>

      <!-- Ticket Status Steps -->
      <view class="wot-bg-filled-oppo mx-4 mb-4 rounded-3 p-4">
        <wd-text class="wot-text-text-main mb-4 block text-3.5" :text="t('ticketDetail.progress')" bold />
        <wd-steps :active="Number(ticket.status ?? 0)" align-center>
          <wd-step :title="t('common.status.pending')" />
          <wd-step :title="t('common.status.processing')" />
          <wd-step :title="t('common.status.completed')" />
          <wd-step :title="t('common.status.closed')" />
        </wd-steps>
      </view>

      <!-- Ticket Info -->
      <view class="mx-4 mb-4">
        <wd-cell-group border custom-class="rounded-3! overflow-hidden">
          <wd-cell :title="t('ticketDetail.createdAt')" :value="ticket.created_time || '—'" />
          <wd-cell :title="t('ticketDetail.handler')" :value="ticket.assigned_by?.name || t('ticketDetail.unassigned')" />
          <wd-cell :title="t('ticketDetail.updatedAt')" :value="ticket.updated_time || '—'" />
        </wd-cell-group>
      </view>

      <!-- Ticket Content -->
      <view v-if="ticket.ticket_content || ticket.summary" class="wot-bg-filled-oppo mx-4 mb-4 rounded-3 p-4">
        <wd-text class="wot-text-text-main block text-3.5" :text="t('ticketDetail.content')" bold />
        <view class="mt-3">
          <mp-html :content="ticket.summary || ticket.ticket_content" markdown :tag-style="MARKDOWN_TAG_STYLE" />
        </view>
      </view>

      <!-- Images -->
      <view v-if="parseImages(ticket.images).length > 0" class="wot-bg-filled-oppo mx-4 mb-4 rounded-3 p-4">
        <wd-text class="wot-text-text-main block text-3.5" :text="t('ticketDetail.attachments')" bold />
        <view class="mt-3 flex flex-wrap gap-3">
          <wd-img
            v-for="(img, idx) in parseImages(ticket.images)"
            :key="img"
            :src="img"
            width="200rpx"
            height="200rpx"
            radius="16rpx"
            mode="aspectFill"
            lazy-load
            @click="previewImages(parseImages(ticket.images), idx)"
          />
        </view>
      </view>

      <!-- Reply -->
      <view v-if="ticket.reply" class="wot-bg-filled-oppo mx-4 mb-4 rounded-3 p-4">
        <wd-text class="wot-text-text-main block text-3.5" :text="t('ticketDetail.replies')" bold />
        <view class="wot-bg-primary-1 mt-3 rounded-lg p-3">
          <mp-html :content="ticket.reply" markdown :tag-style="MARKDOWN_TAG_STYLE" />
        </view>
      </view>

      <!-- Comments -->
      <view class="wot-bg-filled-oppo mx-4 mb-4 rounded-3 p-4">
        <wd-text class="wot-text-text-main block text-3.5" :text="t('ticketDetail.comments', { count: commentTotal })" bold />
        <view class="mt-3">
          <wd-loading v-if="commentsLoading && comments.length === 0" size="20px" class="mx-auto my-4 block" />
          <view v-else-if="commentsError" class="flex flex-col items-center gap-2 py-4">
            <wd-text class="wot-text-text-auxiliary text-3" :text="t('ticketDetail.commentsLoadFailed')" />
            <wd-button size="small" plain @click="loadComments(true)">
              {{ t('common.retry') }}
            </wd-button>
          </view>
          <view v-else-if="comments.length === 0" class="flex flex-col items-center gap-2 py-4">
            <wd-icon name="message" size="28px" color="var(--wot-text-auxiliary)" />
            <wd-text class="wot-text-text-auxiliary text-3" :text="t('ticketDetail.emptyComments')" />
          </view>
          <view v-else class="flex flex-col gap-4">
            <view v-for="comment in comments" :key="comment.id" class="flex gap-3">
              <wd-avatar
                size="32px"
                round
                :text="(comment.username || t('ticketDetail.anonymous')).charAt(0)"
              />
              <view class="min-w-0 flex-1">
                <view class="flex items-center gap-3">
                  <wd-text class="wot-text-text-main text-3 font-semibold" :text="comment.username || t('ticketDetail.anonymous')" />
                  <wd-text class="wot-text-text-auxiliary text-3" :text="comment.created_time || ''" />
                </view>
                <wd-text class="wot-text-text-secondary mt-1 block text-3 leading-relaxed" :text="comment.content" />
              </view>
            </view>

            <view
              v-if="commentTotal > comments.length"
              class="tap-target mx-auto"
              aria-role="button"
              :aria-label="t('ticketDetail.loadMore')"
              @click="loadMoreComments"
            >
              <wd-text class="text-3" :text="t('ticketDetail.loadMore')" type="primary" />
            </view>
          </view>
        </view>
      </view>
    </template>

    <view v-else-if="loadError" class="mx-4 flex flex-col items-center gap-3 py-12">
      <wd-icon name="no-result" size="40px" color="var(--wot-text-auxiliary)" />
      <wd-text class="wot-text-text-secondary text-3.5" :text="t('ticketDetail.loadFailed')" />
      <wd-button size="small" plain @click="retryLoad">
        {{ t('common.retry') }}
      </wd-button>
    </view>

    <wd-empty v-else :tip="t('ticketDetail.notFound')" />

    <!-- 图片预览 -->
    <wd-image-preview ref="previewRef" />

    <!-- Comment Input -->
    <view
      v-if="ticket"
      class="wot-bg-filled-oppo fixed inset-x-0 bottom-0 flex items-center gap-3 px-4 py-3"
      style="z-index: 100; border-top: 1rpx solid var(--wot-border-main, #EAECF0); padding-bottom: calc(12px + env(safe-area-inset-bottom));"
    >
      <wd-input
        v-model="commentText"
        :placeholder="t('ticketDetail.commentPlaceholder')"
        clearable
        class="flex-1"
      />
      <wd-button
        size="small"
        type="primary"
        :loading="submitting"
        :disabled="!commentText.trim()"
        @click="submitComment"
      >
        {{ t('common.send') }}
      </wd-button>
    </view>
  </view>
</template>
