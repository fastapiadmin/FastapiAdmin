<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useI18nNavTitle } from '@/composables/useI18nNavTitle'
import { useShare } from '@/composables/useShare'
import { useTabbarActive } from '@/composables/useTabbarActive'
import { useTicketStats } from '@/composables/useTicketStats'
import { useUserStore } from '@/store/userStore'

const { t } = useI18n()

useShare({
  title: t('work.shareTitle'),
  path: '/pages/work/index',
})

definePage({
  name: 'work',
  layout: 'tabbar',
  style: { navigationBarTitleText: '工作台' },
})
useI18nNavTitle('work.navTitle')

const router = useRouter()
const userStore = useUserStore()
const userInfo = computed(() => userStore.userInfo)
const identityText = computed(() => {
  const username = userInfo.value?.username ? `@${userInfo.value.username}` : ''
  const role = userInfo.value?.roles?.map(item => item.name).filter(Boolean).join(', ')
  return [username, role].filter(Boolean).join(' · ') || t('work.roleFallback')
})
function navigateTo(name: string) {
  router.push({ name })
}

/** 工单统计（共享缓存，与 mine 页面复用） */
const { pendingTickets, processingTickets, doneTickets, loadTicketStats } = useTicketStats()
const ticketStats = computed(() => [
  { key: 'pending', label: t('common.status.pending'), value: pendingTickets.value, color: 'var(--wot-orange-6)' },
  { key: 'processing', label: t('common.status.processing'), value: processingTickets.value, color: 'var(--wot-blue-6)' },
  { key: 'done', label: t('common.status.completed'), value: doneTickets.value, color: 'var(--wot-success-main)' },
])

useTabbarActive('pages/work/index', 'work', loadTicketStats)

const groups = [
  {
    titleKey: 'work.businessCenter',
    color: 'var(--fa-brand-blue)',
    bg: 'wot-bg-primary-1',
    items: [
      { icon: 'notification', titleKey: 'common.nav.notices', descKey: 'work.itemDesc.notices', name: 'work-notices' },
      { icon: 'message', titleKey: 'common.nav.tickets', descKey: 'work.itemDesc.tickets', name: 'work-tickets' },
    ],
  },
  {
    titleKey: 'work.devTools',
    color: 'var(--wot-purple-6)',
    bg: 'wot-bg-purple-1',
    items: [
      { icon: 'message', titleKey: 'common.nav.aiChat', descKey: 'work.itemDesc.aiChat', name: 'work-chat' },
      { icon: 'robot', titleKey: 'common.nav.aiModels', descKey: 'work.itemDesc.aiModels', name: 'work-ai-models' },
    ],
  },
]

/** 搜索关键词，本地过滤模块分组 */
const keyword = ref('')
const filteredGroups = computed(() => {
  const kw = keyword.value.trim().toLowerCase()
  if (!kw)
    return groups
  return groups
    .map(group => ({ ...group, items: group.items.filter(item => t(item.titleKey).toLowerCase().includes(kw)) }))
    .filter(group => group.items.length > 0)
})
</script>

<template>
  <view class="tabbar-wraper py-3">
    <!-- 用户信息卡（品牌渐变 + 极光装饰圆环） -->
    <view class="user-info-card mx-4 mb-6 flex items-center gap-4 rounded-3 px-5 py-6">
      <wd-avatar
        size="64px"
        round
        :src="userInfo?.avatar || ''"
        icon="user"
      />
      <view class="min-w-0 flex-1">
        <view class="text-4 text-white font-bold">
          {{ userInfo?.name || t('work.nameFallback') }}
        </view>
        <view class="mt-1 truncate text-3" style="color: rgba(255, 255, 255, 0.9);">
          {{ identityText }}
        </view>
      </view>
    </view>

    <!-- 工单概览 -->
    <view class="wot-bg-filled-oppo mx-4 mb-6 rounded-3 p-4 active:opacity-80" aria-role="button" :aria-label="t('work.viewAll')" @click="navigateTo('work-tickets')">
      <view class="flex items-center justify-between">
        <wd-text class="wot-text-text-main text-3.5" :text="t('work.ticketOverview')" bold />
        <view class="flex items-center gap-1">
          <wd-text class="wot-text-primary-6 text-3" :text="t('work.viewAll')" />
          <wd-icon name="arrow-right" size="12px" color="var(--wot-text-auxiliary)" />
        </view>
      </view>
      <view class="grid grid-cols-3 mt-3 gap-2">
        <view v-for="stat in ticketStats" :key="stat.key" class="rounded-xl bg-black/5 px-3 py-2.5">
          <view class="flex items-center gap-1.5">
            <view class="h-1.5 w-1.5 rounded-full" :style="{ backgroundColor: stat.color }" />
            <text class="wot-text-text-secondary text-3">
              {{ stat.label }}
            </text>
          </view>
          <view class="mt-1 text-5 font-bold" :style="{ color: stat.color }">
            {{ stat.value ?? '–' }}
          </view>
        </view>
      </view>
    </view>

    <!-- 模块搜索 -->
    <view class="mx-4 mb-6">
      <wd-search v-model="keyword" class="work-search" :placeholder="t('work.searchPlaceholder')" variant="light" hide-cancel />
    </view>

    <!-- 模块分组 -->
    <view v-for="(group, gi) in filteredGroups" :key="gi" class="mb-4">
      <view class="mb-2 mt-1 flex items-center gap-2 px-3">
        <view class="h-3.5 w-1 rounded-full" :style="{ backgroundColor: group.color }" />
        <wd-text class="wot-text-text-main text-3.5" :text="t(group.titleKey)" bold />
        <wd-text class="wot-text-text-auxiliary text-3" :text="group.items.length" />
      </view>
      <view class="grid grid-cols-2 mx-4 gap-3">
        <view
          v-for="item in group.items"
          :key="item.name"
          class="wot-bg-filled-oppo rounded-3 p-4 active:opacity-80"
          aria-role="button"
          :aria-label="t(item.titleKey)"
          @click="navigateTo(item.name)"
        >
          <view class="flex items-start justify-between">
            <view
              class="h-9 w-9 flex shrink-0 items-center justify-center rounded-xl"
              :class="group.bg"
            >
              <wd-icon :name="item.icon" size="18px" :color="group.color" />
            </view>
            <wd-icon name="arrow-right" size="14px" color="var(--wot-text-auxiliary)" />
          </view>
          <view class="wot-text-text-main mt-2.5 text-3.5 font-semibold">
            {{ t(item.titleKey) }}
          </view>
          <view class="wot-text-text-auxiliary mt-1 text-3 leading-snug">
            {{ t(item.descKey) }}
          </view>
        </view>
      </view>
    </view>

    <!-- 搜索无结果 -->
    <wd-empty v-if="filteredGroups.length === 0" :tip="t('work.emptyTip')" />
  </view>
</template>

<style lang="scss">
/* global work search：暗色下与卡片表面一致 */
.work-search {
  --wot-search-bg: var(--wot-filled-oppo);
  --wot-search-light-bg: var(--wot-filled-oppo);
  --wot-search-light-block-bg: var(--wot-filled-oppo);
  overflow: hidden;
  border: 2rpx solid var(--wot-border-main, #eaecef);
  border-radius: 16rpx;
}
</style>
