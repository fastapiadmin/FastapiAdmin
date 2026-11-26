<script setup lang="ts">
import type { ChatMessage, ChatSession } from '@/api/module_ai/chat'
import { onLoad, onUnload } from '@dcloudio/uni-app'
import { computed, nextTick, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { formatMessage } from '@/locales/format'
import { ChatAPI } from '@/api/module_ai/chat'
import { useAiChat } from '@/composables/useAiChat'
import { useI18nNavTitle } from '@/composables/useI18nNavTitle'
import { useShare } from '@/composables/useShare'
import { MARKDOWN_TAG_STYLE } from '@/constants/markdown.constant'

const { t } = useI18n()

useShare({
  title: t('chat.shareTitle'),
  path: '/subPages/module_ai/chat/index',
})

definePage({ name: 'work-chat', style: { navigationBarTitleText: 'AI 助手' } })
useI18nNavTitle('chat.title')

const toast = useToast()
const sessions = ref<ChatSession[]>([])
const currentSession = ref<number | null>(null)
const currentTitle = ref(t('chat.title'))
const messages = ref<ChatMessage[]>([])
const inputText = ref('')
const loading = ref(false)
const sessionsError = ref(false)
const messagesError = ref(false)
const showSessions = ref(false)

/** 流式对话（WebSocket） */
const streamChat = useAiChat()
const streaming = streamChat.isStreaming

// ===== 消息窗口化渲染 =====
// 长会话只渲染最近 MAX_VISIBLE_MESSAGES 条，避免消息过多时 DOM 节点与 setData 数据量膨胀导致卡顿；
// 通过"加载更早消息"按步长扩大渲染窗口，保持浏览位置不跳变。
const MAX_VISIBLE_MESSAGES = 60
const INCREMENT = 40
const messageWindow = ref(MAX_VISIBLE_MESSAGES)
const scrollTarget = ref('')
const visibleMessages = computed(() => messages.value.slice(-messageWindow.value))
const hasOlderMessages = computed(() => messages.value.length > messageWindow.value)

function loadOlderMessages() {
  messageWindow.value += INCREMENT
  // 滚动到新增窗口边界，保持已读消息位置不跳变
  scrollTarget.value = `msg-${INCREMENT - 1}`
  nextTick(() => {
    scrollTarget.value = ''
  })
}

function resetWindow() {
  messageWindow.value = MAX_VISIBLE_MESSAGES
  scrollTarget.value = ''
}

function formatSessionTime(value?: string | number) {
  if (!value)
    return ''
  const raw = String(value)
  const numeric = /^\d+$/.test(raw)
  const date = numeric
    ? new Date(Number(raw) * (raw.length === 10 ? 1000 : 1))
    : new Date(raw)
  if (Number.isNaN(date.getTime()))
    return raw
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`
}

async function loadSessions() {
  loading.value = true
  sessionsError.value = false
  try {
    const res = await ChatAPI.getSessions()
    sessions.value = res.items || []
  }
  catch {
    sessions.value = []
    sessionsError.value = true
    toast.error(t('chat.loadSessionsFailed'))
  }
  finally { loading.value = false }
}

async function createSession() {
  try {
    const res = await ChatAPI.createSession(t('chat.newSession'))
    // 兼容后端可能返回 { data: ChatSession } 或直接 ChatSession 两种结构
    const newSession = (res as { data?: ChatSession })?.data ?? (res as ChatSession)
    if (newSession?.id) {
      sessions.value.unshift(newSession)
      selectSession(newSession.id, newSession.title)
    }
    toast.success(t('chat.newSessionSuccess'))
  }
  catch { toast.error(t('chat.createFailed')) }
}

async function selectSession(id: number, title?: string) {
  currentSession.value = id
  currentTitle.value = title || formatMessage(t, 'chat.sessionId', { id })
  showSessions.value = false
  loading.value = true
  messagesError.value = false
  try {
    const detail = await ChatAPI.getDetail(id)
    // 兼容后端可能返回 { messages: [] } 或 { data: { messages: [] } } 两种结构
    const detailRes = detail as { messages?: ChatMessage[], data?: { messages?: ChatMessage[] } }
    const msgs = detailRes?.messages || detailRes?.data?.messages || []
    resetWindow()
    messages.value = msgs.length
      ? msgs.map(m => ({ role: m.role || 'ai', content: m.content || '', time: String(m.created_at || m.time || '') }))
      : [{ role: 'ai', content: t('chat.welcome') }]
  }
  catch {
    messages.value = []
    messagesError.value = true
    toast.error(t('chat.loadMessagesFailed'))
  }
  finally { loading.value = false }
}

function retryMessages() {
  if (currentSession.value)
    selectSession(currentSession.value, currentTitle.value)
}

async function deleteSession(id: number) {
  uni.showModal({
    title: t('common.title'),
    content: t('chat.deleteConfirm'),
    success: async (r) => {
      if (r.confirm) {
        try {
          await ChatAPI.removeSession([id])
          sessions.value = sessions.value.filter(s => s.id !== id)
          if (currentSession.value === id) {
            currentSession.value = null
            currentTitle.value = t('chat.title')
            messages.value = [{ role: 'ai', content: t('chat.welcome') }]
          }
          toast.success(t('chat.deleted'))
        }
        catch { toast.error(t('chat.deleteFailed')) }
      }
    },
  })
}

async function sendMessage() {
  const text = inputText.value.trim()
  if (!text || streaming.value)
    return
  // 无会话时自动创建，避免"请先创建会话"的额外步骤
  let sid = currentSession.value
  if (!sid) {
    try {
      const res = await ChatAPI.createSession()
      // 兼容后端可能返回 { data: ChatSession } 或直接 ChatSession 两种结构
      const newSession = (res as { data?: ChatSession })?.data ?? (res as ChatSession)
      if (newSession?.id) {
        sessions.value.unshift(newSession)
        sid = newSession.id
        currentSession.value = sid
        currentTitle.value = newSession.title || t('chat.title')
      }
      else {
        return toast.error(t('chat.createFailed'))
      }
    }
    catch {
      return toast.error(t('chat.createFailed'))
    }
  }

  messages.value.push({ role: 'user', content: text, time: new Date().toLocaleTimeString() })
  inputText.value = ''
  // 占位 AI 消息，流式分片实时追加（打字机效果）
  const aiMsg: ChatMessage = { role: 'ai', content: '', time: new Date().toLocaleTimeString() }
  messages.value.push(aiMsg)
  scrollToBottom()

  try {
    await streamChat.sendMessage({ message: text, session_id: String(sid) }, {
      onChunk: (chunk) => {
        aiMsg.content += chunk
        scrollToBottom()
      },
      onDone: () => {
        if (!aiMsg.content)
          aiMsg.content = t('chat.noReply')
      },
      onError: (err) => {
        aiMsg.content = err || t('chat.requestFailed')
      },
    })
  }
  finally {
    streaming.value = false
  }
}

/** 停止当前生成 */
function stopGenerate() {
  streamChat.stop()
}

/** 滚动到最新一条消息 */
function scrollToBottom() {
  scrollTarget.value = `msg-${visibleMessages.value.length - 1}`
  nextTick(() => {
    scrollTarget.value = ''
  })
}

onUnload(() => {
  streamChat.close()
})

onLoad(() => {
  loadSessions()
  messages.value = [{ role: 'ai', content: t('chat.welcome') }]
})
</script>

<template>
  <view class="page-wraper" style="display:flex;flex-direction:column;position:relative;height:calc(100vh - var(--window-top, 0px));overflow:hidden;">
    <!-- 会话操作条：原生导航已提供页面标题，这里不再重复画标题栏 -->
    <view class="chat-toolbar wot-bg-filled-oppo wot-border-border-main">
      <view
        class="tap-target chat-toolbar__action"
        aria-role="button"
        :aria-label="t('chat.sessionList')"
        @click="showSessions = !showSessions"
      >
        <wd-icon name="menu" size="18px" color="var(--wot-text-main)" />
        <text class="chat-toolbar__label">{{ t('chat.sessionList') }}</text>
      </view>
      <view
        class="tap-target chat-toolbar__action"
        aria-role="button"
        :aria-label="t('chat.newSession')"
        @click="createSession"
      >
        <wd-icon name="plus" size="18px" color="var(--wot-primary-6)" />
        <text class="chat-toolbar__label chat-toolbar__label--primary">{{ t('chat.new') }}</text>
      </view>
    </view>

    <!-- Session panel overlay -->
    <view v-if="showSessions" class="session-overlay wot-bg-filled-oppo" style="position:absolute;top:44px;left:0;right:0;bottom:0;z-index:100;overflow-y:auto;">
      <view class="p-sm">
        <view class="mb-md flex items-center justify-between px-xs">
          <wd-text class="text-lg" :text="t('chat.sessionList')" bold />
          <wd-button size="small" type="primary" @click="createSession">
            {{ t('chat.new') }}
          </wd-button>
        </view>
        <SkeletonPage v-if="loading && sessions.length === 0" />
        <view v-else-if="sessionsError && sessions.length === 0" class="flex flex-col items-center gap-3 py-12">
          <wd-icon name="no-result" size="48px" color="var(--wot-text-auxiliary)" />
          <wd-text class="wot-text-text-secondary text-3" :text="t('chat.loadSessionsFailed')" />
          <wd-button size="small" type="primary" @click="loadSessions">
            {{ t('common.retry') }}
          </wd-button>
        </view>
        <template v-else>
          <view v-for="s in sessions" :key="s.id" class="admin-card">
            <wd-cell :title="s.title" :label="formatSessionTime(s.created_at)" center is-link @click="selectSession(s.id, s.title)">
              <template #default>
                <view class="icon-action" aria-role="button" :aria-label="t('common.delete')" @click.stop="deleteSession(s.id)">
                  <wd-icon name="delete" size="18px" color="var(--wot-danger-main)" />
                </view>
              </template>
            </wd-cell>
          </view>
          <wd-empty v-if="!loading && sessions.length === 0" :tip="t('chat.empty')" />
        </template>
      </view>
    </view>

    <!-- Messages -->
    <scroll-view
      scroll-y
      class="chat-messages wot-p-tight"
      style="flex:1;min-height:0;"
      :scroll-into-view="scrollTarget || `msg-${visibleMessages.length - 1}`"
      :scroll-with-animation="true"
    >
      <view v-if="messagesError" class="flex flex-col items-center gap-3 py-12">
        <wd-icon name="no-result" size="48px" color="var(--wot-text-auxiliary)" />
        <wd-text class="wot-text-text-secondary text-3" :text="t('chat.loadMessagesFailed')" />
        <wd-button size="small" type="primary" @click="retryMessages">
          {{ t('common.retry') }}
        </wd-button>
      </view>
      <!-- 窗口化渲染：仅渲染最近 N 条消息，支持加载更早消息 -->
      <view v-if="!messagesError && hasOlderMessages" style="padding:16rpx 0;text-align:center;">
        <wd-button size="small" variant="plain" @click="loadOlderMessages">
          {{ formatMessage(t, 'chat.loadMore', { count: messages.length - visibleMessages.length }) }}
        </wd-button>
      </view>
      <template v-if="!messagesError">
        <view v-for="(msg, i) in visibleMessages" :id="`msg-${i}`" :key="i" style="margin-bottom:24rpx;">
          <view class="flex items-start gap-sm" :class="msg.role === 'user' ? 'flex-row-reverse' : ''">
            <view
              v-if="msg.role === 'user'"
              class="h-8 w-8 flex shrink-0 items-center justify-center rounded-full"
              style="background: linear-gradient(135deg, var(--wot-primary-6), var(--wot-primary-7));"
            >
              <wd-icon name="user" size="18px" color="#FFFFFF" />
            </view>
            <wd-avatar v-else size="32px" shape="round" src="/static/logo.png" />
            <view
              class="max-w-[72%] break-words px-3 py-2"
              :class="msg.role === 'user' ? 'wot-bg-primary-6 wot-text-text-white' : 'wot-bg-filled-oppo wot-text-text-main wot-border-border-main'"
              :style="{
                borderRadius: msg.role === 'user' ? '16rpx 16rpx 4rpx 16rpx' : '16rpx 16rpx 16rpx 4rpx',
                border: msg.role === 'user' ? 'none' : '1px solid var(--wot-border-main)',
              }"
            >
              <!-- AI 消息渲染 markdown；用户消息保持纯文本 -->
              <template v-if="msg.role !== 'user'">
                <wd-loading v-if="streaming && !msg.content" />
                <mp-html v-else :content="msg.content" markdown :tag-style="MARKDOWN_TAG_STYLE" />
              </template>
              <wd-text v-else style="white-space:pre-wrap;font-size:var(--font-sm);line-height:1.7;" :text="msg.content" />
              <wd-text v-if="msg.time" style="font-size:var(--font-xs);opacity:0.75;margin-top:8rpx;display:block;" :style="msg.role === 'user' ? 'text-align:right' : 'text-align:left'" :text="msg.time" />
            </view>
          </view>
        </view>
      </template>
    </scroll-view>

    <!-- Input -->
    <view class="wot-bg-filled-oppo wot-border-border-main wot-p-tight" style="border-top:1px solid;padding-bottom:calc(24rpx + env(safe-area-inset-bottom, 0px));">
      <view class="flex items-center gap-sm">
        <wd-input v-model="inputText" :placeholder="t('chat.inputPlaceholder')" :disabled="streaming" class="flex-1" confirm-type="send" @confirm="sendMessage" />
        <wd-button v-if="streaming" type="danger" variant="plain" @click="stopGenerate">
          {{ t('chat.stop') }}
        </wd-button>
        <wd-button v-else :disabled="!inputText.trim()" type="primary" @click="sendMessage">
          {{ t('common.send') }}
        </wd-button>
      </view>
    </view>
  </view>
</template>

<style lang="scss" scoped>
.chat-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
  padding: 0 8px;
  border-bottom: 1px solid var(--wot-border-main);
}

.chat-toolbar__action {
  gap: 6px;
}

.chat-toolbar__label {
  font-size: var(--font-xs);
  color: var(--wot-text-secondary);
}

.chat-toolbar__label--primary {
  color: var(--wot-primary-6);
}
</style>
