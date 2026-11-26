<script setup lang="ts">
import type { SwiperItem } from '@wot-ui/ui/components/wd-swiper/types'
import type { DashboardStats, LoginTrendItem } from '@/api/module_monitor/dashboard'
import type { NoticeItem } from '@/api/module_system/notice'
import { onPullDownRefresh, onReady } from '@dcloudio/uni-app'
import { nextTick } from 'vue'
import { LineChart } from 'echarts/charts'
import { GridComponent, LegendComponent, TooltipComponent } from 'echarts/components'
import * as echarts from 'echarts/core'
import { LegacyGridContainLabel } from 'echarts/features'
import { CanvasRenderer } from 'echarts/renderers'
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { formatMessage } from '@/locales/format'
import { DashboardAPI } from '@/api/module_monitor/dashboard'
import { NoticeAPI } from '@/api/module_system/notice'
import { TicketAPI } from '@/api/module_system/ticket'
import { useI18nNavTitle } from '@/composables/useI18nNavTitle'
import { useShare } from '@/composables/useShare'
import { useTabbarActive } from '@/composables/useTabbarActive'
import { useThemeStore } from '@/store/themeStore'
import { useUserStore } from '@/store/userStore'

const { t, locale } = useI18n()
const userStore = useUserStore()
const themeStore = useThemeStore()

/** 主题主色（primary6）→ rgba，供 echarts 面积渐变使用（echarts 无法直接消费 CSS 变量） */
function hexToRgba(hex: string, alpha: number): string {
  const r = Number.parseInt(hex.slice(1, 3), 16)
  const g = Number.parseInt(hex.slice(3, 5), 16)
  const b = Number.parseInt(hex.slice(5, 7), 16)
  return `rgba(${r}, ${g}, ${b}, ${alpha})`
}

useShare(() => ({
  title: formatMessage(t, 'index.shareTitle', { greeting: t(`index.${getGreeting()}`), name: userStore.userInfo?.name || t('common.admin') }),
  path: '/pages/index/index',
}))

echarts.use([
  GridComponent,
  LegendComponent,
  TooltipComponent,
  LegacyGridContainLabel,
  LineChart,
  CanvasRenderer,
])

definePage({
  name: 'home',
  layout: 'tabbar',
  style: { navigationBarTitleText: '工作台概览' },
})
useI18nNavTitle('index.navTitle')

let _router: ReturnType<typeof useRouter> | null = null
function getRouter() {
  if (!_router) {
    try {
      _router = useRouter()
    }
    catch {}
  }
  return _router
}

const loading = ref(false)
const statsError = ref(false)
const bannerPaused = ref(false)
const dashboardStats = ref<DashboardStats | null>(null)
const pendingTickets = ref(0)
const recentNotices = ref<NoticeItem[]>([])

/** 最新公告标题（通知栏展示，无公告则隐藏通知栏） */
const latestNotice = computed(() => recentNotices.value[0]?.notice_title || t('index.welcomeDefault'))

/** 通知栏背景/文字跟随主题色（CSS 变量无法直接取主色透明值，用 JS 计算） */
const noticeBarColors = computed(() => {
  const shades = themeStore.currentThemeColor.primaryShades
  const main = themeStore.isDark ? shades.primary5 : shades.primary6
  return {
    color: main,
    background: hexToRgba(main, themeStore.isDark ? 0.16 : 0.1),
  }
})

/** 页面滚动距离（供 wd-backtop 判断显示） */
const scrollTop = ref(0)
/** 趋势图是原生 canvas，滚动到 tabbar 下方时会盖住导航；完全进入可视区才渲染 */
const chartSafe = ref(true)
const windowHeight = ref(0)
let lastChartCheck = 0

/** 原生 canvas 会盖住 tabbar：用视口坐标判断，进入底部 60px 区域前移除 canvas */
function updateChartSafe() {
  const query = uni.createSelectorQuery()
  query.select('#monitor-chart').boundingClientRect((rect) => {
    const box = rect as UniApp.NodeInfo | null
    if (!box || !windowHeight.value)
      return
    chartSafe.value = (box.bottom ?? 0) <= windowHeight.value - 60
  }).exec()
}

onPageScroll((e) => {
  scrollTop.value = e.scrollTop
  const now = Date.now()
  if (now - lastChartCheck > 100) {
    lastChartCheck = now
    updateChartSafe()
  }
})

const NAV_LIST = [
  { icon: 'notification', titleKey: 'common.nav.notices', name: 'work-notices', color: 'var(--fa-icon-blue)', soft: 'fa-soft' },
  { icon: 'message', titleKey: 'common.nav.tickets', name: 'work-tickets', color: 'var(--fa-icon-violet)', soft: 'fa-soft-violet' },
  { icon: 'interaction', titleKey: 'common.nav.aiChat', name: 'work-chat', color: 'var(--fa-icon-blue)', soft: 'fa-soft' },
  { icon: 'robot', titleKey: 'common.nav.aiModels', name: 'work-ai-models', color: 'var(--fa-icon-violet)', soft: 'fa-soft-violet' },
]

/** 轮播 Banner 条目 */
interface BannerItem extends SwiperItem {
  key: string
  tag: string
  cls: string
  title: string
  subtitle: string
  desc: string
  cta: string
  onClick: () => void
}

/**
 * 顶部轮播 Banner（轮播图风格首页核心）：
 * 1. 今日问候  2. 待办工单  3. 数据概览
 */
const banners = computed<BannerItem[]>(() => [
  {
    key: 'greet',
    tag: t('index.today'),
    cls: 'banner-slide--greet',
    title: `${t(`index.${getGreeting()}`)}，${userStore.userInfo?.name || t('common.admin')}`,
    subtitle: getDateString(),
    desc: t('index.welcomeBack'),
    cta: t('index.dataTitle'),
    onClick: () => scrollToMonitor(),
  },
  {
    key: 'ticket',
    tag: t('index.todo'),
    cls: pendingTickets.value > 0 ? 'banner-slide--ticket' : 'banner-slide--ticket-empty',
    title: pendingTickets.value > 0 ? formatMessage(t, 'index.pendingCount', { count: pendingTickets.value }) : t('index.allDone'),
    subtitle: pendingTickets.value > 0 ? t('index.todoSubtitle') : t('index.doneSubtitle'),
    desc: t('index.ticketDesc'),
    cta: pendingTickets.value > 0 ? t('index.goHandle') : t('index.viewTickets'),
    onClick: () => navigateTo('work-tickets'),
  },
  {
    key: 'stats',
    tag: t('index.data'),
    cls: 'banner-slide--stats',
    title: t('index.dataTitle'),
    subtitle: t('index.dataSubtitle'),
    desc: formatMessage(t, 'index.dataDesc', {
      total: dashboardStats.value?.total_users ?? '-',
      online: dashboardStats.value?.online_users ?? '-',
      today: dashboardStats.value?.today_login_count ?? '-',
    }),
    cta: t('index.viewDetail'),
    onClick: () => scrollToMonitor(),
  },
])

function navigateTo(name: string) {
  const r = getRouter()
  if (r)
    r.push({ name })
}

// ===== 系统监控（原数据概览 dashboard 合并） =====

/** 近7天登录趋势（后端 monitor/online/stats 返回，含今日） */
const loginTrend = ref<LoginTrendItem[]>([])

/** 登录趋势折线图（真实数据：登录次数 / 独立访客 / 新增用户） */
const loginTrendOption = computed(() => {
  const days = loginTrend.value.length > 0
    ? loginTrend.value.map(i => i.day.slice(5)) // 仅显示 MM-DD
    : []
  const logins = loginTrend.value.map(i => i.logins)
  const uniques = loginTrend.value.map(i => i.unique_users)
  const news = loginTrend.value.map(i => i.new_users)
  /** 主题主色（跟随主题色切换），图表品牌感与全局换肤一致 */
  const primaryColor = themeStore.currentThemeColor.primaryShades.primary6
  /** 暗色模式下图表文字/网格线换亮色，保证深色卡片上可读 */
  const isDark = themeStore.isDark
  const axisTextColor = isDark ? '#A3AAB8' : '#6B7280'
  const legendTextColor = isDark ? '#C3C9D3' : '#4B5563'
  const splitLineColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(128, 128, 128, 0.12)'
  return {
    tooltip: {
      trigger: 'axis',
      textStyle: { fontSize: 12 },
    },
    legend: {
      top: 0,
      right: 0,
      itemWidth: 10,
      itemHeight: 10,
      itemGap: 8,
      textStyle: { fontSize: 12, color: legendTextColor },
      data: [t('index.loginCount'), t('index.visitor'), t('index.newUser')],
    },
    grid: { left: 8, right: 8, top: 34, bottom: 0, containLabel: true },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: days,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { fontSize: 12, color: axisTextColor },
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { fontSize: 12, color: axisTextColor },
      splitLine: { lineStyle: { color: splitLineColor, type: 'dashed' } },
    },
    series: [
      {
        name: t('index.loginCount'),
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 5,
        data: logins,
        lineStyle: { width: 3, color: primaryColor },
        itemStyle: { color: primaryColor },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: hexToRgba(primaryColor, 0.28) },
              { offset: 1, color: hexToRgba(primaryColor, 0.02) },
            ],
          },
        },
      },
      {
        name: t('index.visitor'),
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 5,
        data: uniques,
        lineStyle: { width: 2.5, color: '#10B981' },
        itemStyle: { color: '#10B981' },
      },
      {
        name: t('index.newUser'),
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 5,
        data: news,
        lineStyle: { width: 2.5, color: '#F59E0B' },
        itemStyle: { color: '#F59E0B' },
      },
    ],
  }
})

/** 滚动定位到系统监控区块（dashboard 合并后无独立页面，Banner 点击改为页内定位） */
function scrollToMonitor() {
  const query = uni.createSelectorQuery()
  query.select('#monitor-section').boundingClientRect()
  query.exec((res) => {
    const rect = res[0] as UniApp.NodeInfo | null
    if (rect && typeof rect.top === 'number') {
      uni.pageScrollTo({
        scrollTop: Math.max(rect.top + scrollTop.value - 12, 0),
        duration: 300,
      })
    }
  })
}

async function loadData() {
  loading.value = true
  try {
    const [statsRes, ticketRes] = await Promise.allSettled([
      DashboardAPI.getStats(),
      TicketAPI.getPage({ page_no: 1, page_size: 1, status: '0' }),
    ])
    statsError.value = statsRes.status === 'rejected'
    if (statsRes.status === 'fulfilled') {
      dashboardStats.value = statsRes.value
      loginTrend.value = statsRes.value.login_trend || []
      nextTick(updateChartSafe)
    }
    if (ticketRes.status === 'fulfilled')
      pendingTickets.value = ticketRes.value.total || 0
  }
  catch { /* silent */ }
  finally {
    loading.value = false
  }
}

async function loadNotices() {
  try {
    const res = await NoticeAPI.getPage({ page_no: 1, page_size: 3, status: 1 })
    recentNotices.value = res.items || []
  }
  catch { /* silent */ }
}

onReady(() => {
  const info = typeof (uni as any).getWindowInfo === 'function' ? (uni as any).getWindowInfo() : uni.getSystemInfoSync()
  windowHeight.value = info.windowHeight ?? 0
  Promise.all([loadData(), loadNotices()])
})

onPullDownRefresh(async () => {
  await Promise.all([loadData(), loadNotices()])
  uni.stopPullDownRefresh()
})

useTabbarActive('pages/index/index', 'index')

/** 星期名称常量：日期格式化是本地化逻辑而非模板文案，script 中不走 i18n */
const WEEK_ZH = ['日', '一', '二', '三', '四', '五', '六']
const WEEK_EN = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

function getDateString() {
  const now = new Date()
  const y = now.getFullYear()
  const m = now.getMonth() + 1
  const d = now.getDate()
  return locale.value.startsWith('zh')
    ? `${y}年${m}月${d}日 星期${WEEK_ZH[now.getDay()]}`
    : `${WEEK_EN[now.getDay()]}, ${m}/${d}/${y}`
}

function getGreeting() {
  const hour = new Date().getHours()
  if (hour < 6)
    return 'night'
  if (hour < 9)
    return 'morning'
  if (hour < 12)
    return 'forenoon'
  if (hour < 14)
    return 'noon'
  if (hour < 18)
    return 'afternoon'
  return 'evening'
}
</script>

<template>
  <view class="tabbar-wraper pt-3">
    <!-- 顶部通知栏：接入最新一条公告（无公告自动隐藏），点击进入公告列表 -->
    <view class="mx-4">
      <wd-notice-bar
        :text="latestNotice"
        closable
        type="info"
        prefix="notification"
        custom-class="home-notice"
        custom-style="margin-bottom: 24px; border-radius: 12px;"
        :color="noticeBarColors.color"
        :background-color="noticeBarColors.background"
        @click="navigateTo('work-notices')"
      />
    </view>

    <!-- 轮播 Banner -->
    <view class="mx-4 mb-6">
      <wd-swiper
        :list="banners"
        height="120"
        radius="16"
        :interval="4500"
        :autoplay="!bannerPaused"
        :loop="true"
        adjust-height="none"
      >
        <template #default="{ index }">
          <view class="banner-slide" :class="banners[index].cls" aria-role="button" :aria-label="banners[index].title" @click="banners[index].onClick">
            <view class="banner-slide__scrim" />
            <view class="banner-slide__body">
              <view class="banner-slide__tag">
                <wd-tag size="small" round bg-color="rgba(15, 23, 42, 0.38)" color="#FFFFFF">
                  {{ banners[index].tag }}
                </wd-tag>
              </view>
              <view class="banner-slide__title">
                {{ banners[index].title }}
              </view>
              <view class="banner-slide__subtitle">
                {{ banners[index].subtitle }}
              </view>
              <view class="banner-slide__desc">
                {{ banners[index].desc }}
              </view>
            </view>
            <view class="banner-slide__cta">
              <text class="banner-slide__cta-text">
                {{ banners[index].cta }}
              </text>
              <text class="banner-slide__cta-arrow">
                ›
              </text>
            </view>
          </view>
        </template>
        <template #indicator="{ current, total }">
          <view class="banner-dots">
            <view
              v-for="i in total"
              :key="i"
              class="banner-dots__dot"
              :class="{ 'is-active': i === current + 1 }"
            />
          </view>
          <view
            class="banner-pause"
            aria-role="button"
            :aria-label="bannerPaused ? t('index.playBanner') : t('index.pauseBanner')"
            @click.stop="bannerPaused = !bannerPaused"
          >
            <wd-icon :name="bannerPaused ? 'play' : 'pause'" size="14px" color="#FFFFFF" />
          </view>
        </template>
      </wd-swiper>
    </view>

    <!-- 快捷入口 -->
    <view class="wot-bg-filled-oppo mx-4 mb-6 rounded-4 p-3">
      <wd-grid :column="4" :border="false" clickable>
        <wd-grid-item
          v-for="item in NAV_LIST"
          :key="item.name"
          @click="navigateTo(item.name)"
        >
          <view class="w-full flex flex-col items-center">
            <view
              class="h-11 w-11 flex items-center justify-center rounded-xl"
              :class="item.soft"
            >
              <wd-icon :name="item.icon" size="20px" :color="item.color" />
            </view>
            <view class="wot-text-text-secondary mt-1 w-full text-center text-3">
              {{ t(item.titleKey) }}
            </view>
          </view>
        </wd-grid-item>
      </wd-grid>
    </view>

    <!-- 运营概览 -->
    <view class="section-head">
      <view class="section-head__bar" />
      <text class="section-head__title">{{ t('index.opsOverview') }}</text>
    </view>
    <view v-if="statsError" class="home-error mx-4 mb-6">
      <text class="home-error__text">
        {{ t('index.loadFailed') }}
      </text>
      <view
        class="home-error__action tap-target"
        aria-role="button"
        :aria-label="t('common.retry')"
        @click="loadData"
      >
        {{ t('common.retry') }}
      </view>
    </view>
    <SkeletonPage v-if="loading && !dashboardStats" :rows="3" />
    <view v-else-if="dashboardStats" class="mx-4">
      <wd-row :gutter="12">
        <wd-col :span="8">
          <view class="stat-card wot-bg-filled-oppo">
            <view class="stat-card__icon fa-soft">
              <wd-icon name="user-group" size="20px" color="var(--wot-primary-6)" />
            </view>
            <text v-if="dashboardStats?.total_users != null" class="stat-count wot-text-primary-6">{{ dashboardStats.total_users }}</text>
            <view v-else class="wot-text-text-main text-5 font-bold">
              -
            </view>
            <view class="wot-text-text-secondary mt-1 text-3">
              {{ t('index.registered') }}
            </view>
            <view class="wot-text-text-auxiliary mt-0.5 text-3">
              {{ formatMessage(t, 'index.weekNew', { count: dashboardStats?.week_user_created ?? 0 }) }}
            </view>
          </view>
        </wd-col>
        <wd-col :span="8">
          <view class="stat-card wot-bg-filled-oppo">
            <view class="stat-card__icon wot-bg-success-surface">
              <wd-icon name="eye" size="20px" color="var(--fa-success-text)" />
            </view>
            <text v-if="dashboardStats?.online_users != null" class="stat-count fa-text-success">{{ dashboardStats.online_users }}</text>
            <view v-else class="wot-text-text-main text-5 font-bold">
              -
            </view>
            <view class="wot-text-text-secondary mt-1 text-3">
              {{ t('index.online') }}
            </view>
            <view class="wot-text-text-auxiliary mt-0.5 text-3">
              {{ t('index.currentOnline') }}
            </view>
          </view>
        </wd-col>
        <wd-col :span="8">
          <view class="stat-card wot-bg-filled-oppo">
            <view class="stat-card__icon wot-bg-warning-surface">
              <wd-icon name="clock-circle" size="20px" color="var(--fa-warning-text)" />
            </view>
            <text v-if="dashboardStats?.today_login_count != null" class="stat-count fa-text-warning">{{ dashboardStats.today_login_count }}</text>
            <view v-else class="wot-text-text-main text-5 font-bold">
              -
            </view>
            <view class="wot-text-text-secondary mt-1 text-3">
              {{ t('index.todayLogin') }}
            </view>
            <view class="wot-text-text-auxiliary mt-0.5 text-3">
              {{ formatMessage(t, 'index.independentUser', { count: dashboardStats?.today_unique_users ?? 0 }) }}
            </view>
          </view>
        </wd-col>
      </wd-row>
    </view>

    <!-- 系统监控（原数据概览 dashboard 合并，Banner 点击可滚动到此区块） -->
    <view v-if="loginTrend.length" id="monitor-section" class="mt-2">
      <view class="section-head">
        <view class="section-head__bar" />
        <text class="section-head__title">{{ t('index.sysMonitor') }}</text>
      </view>

      <!-- 登录趋势折线图 -->
      <view class="wot-bg-filled-oppo mx-4 mb-6 rounded-4 p-4">
        <view class="mb-4 flex items-center gap-2">
          <wd-text class="wot-text-text-main text-3.5" :text="t('index.loginTrend')" bold />
        </view>
        <view id="monitor-chart" class="h-52 w-full">
          <uni-echarts v-show="chartSafe" custom-class="h-full w-full" :option="loginTrendOption" />
        </view>
      </view>
    </view>

    <!-- 最新公告 -->
    <view v-if="recentNotices.length > 0" class="section-head section-head--between">
      <view class="flex min-w-0 items-center gap-2">
        <view class="section-head__bar" />
        <text class="section-head__title">{{ t('index.latestNotice') }}</text>
      </view>
      <view
        class="tap-target"
        aria-role="button"
        :aria-label="t('common.all')"
        @click="navigateTo('work-notices')"
      >
        <wd-text class="text-3" :text="t('common.all')" type="primary" />
      </view>
    </view>
    <view v-if="recentNotices.length > 0" class="mx-4">
      <wd-cell-group border custom-class="rounded-4! overflow-hidden">
        <wd-cell
          v-for="item in recentNotices"
          :key="item.id"
          :title="item.notice_title"
          is-link
          @click="navigateTo('work-notices')"
        >
          <template #label>
            <view class="wot-text-text-auxiliary mt-1 text-3">
              {{ item.created_time || '' }}
            </view>
          </template>
        </wd-cell>
      </wd-cell-group>
    </view>

    <wd-backtop :scroll-top="scrollTop" :top="80" />
  </view>
</template>

<style lang="scss" scoped>
.home-error {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 12px 16px;
  border-radius: var(--fa-radius-md, 12px);
  background: var(--wot-danger-surface, #FFF0EE);
  color: #B42318;
  font-size: 12px;
}

.wot-theme-dark .home-error {
  background: rgba(241, 70, 70, 0.18);
  color: #FFB4AC;
}

.home-error__action {
  font-weight: 500;
}

/* ===== 运营概览指标卡片（图标徽章 + 数据层级） ===== */
.stat-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  box-sizing: border-box;
  padding: 16px;
  border-radius: var(--fa-radius-lg, 16px);
  overflow: hidden;

  /* 图标徽章 */
  &__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 10px;
    margin-bottom: 12px;
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
  }

  /* 数字区域（直接输出数字，避免自定义组件在 MP 下渲染异常） */
  .stat-count {
    font-size: 40rpx;
    font-weight: 700;
    line-height: 1.2;
  }
}

/* ===== 轮播 Banner（渐变装饰 + 文字布局，其余布局全部走 UnoCSS 原子类） ===== */
.banner-slide {
  position: relative;
  width: 100%;
  height: 100%;
  /* box-sizing: border-box 让 padding 算入 height，避免 flex item 溢出 swiper-item 导致内容偏上 + 底部裁切（微信 swiper-item 高度固定 100% 与 H5 swiper-item 行为不同所致） */
  box-sizing: border-box;
  padding: 36rpx 40rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #FFFFFF;
  overflow: hidden;

  /* 深色遮罩：保证白色标题/副标题在橙、绿、浅紫渐变上仍达到 WCAG AA */
  &__scrim {
    position: absolute;
    inset: 0;
    z-index: 0;
    background: rgba(15, 23, 42, 0.58);
    pointer-events: none;
  }

  /* 装饰圆环（极光浮动动效） */
  &::before {
    content: '';
    position: absolute;
    right: -80rpx;
    top: -80rpx;
    width: 300rpx;
    height: 300rpx;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.10);
    animation: banner-orbit 7s ease-in-out infinite;
  }

  &::after {
    content: '';
    position: absolute;
    right: 40rpx;
    bottom: -120rpx;
    width: 240rpx;
    height: 240rpx;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.08);
    animation: banner-orbit 9s ease-in-out infinite reverse;
  }

  /* 极光呼吸：装饰圆环缓慢浮动，增强 Banner 层次感（transform 动画，真机性能友好） */
  @keyframes banner-orbit {
    0%, 100% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-14rpx) scale(1.06); }
  }

  /* 问候 Banner：品牌卡，跟随主题色（primary），与用户卡/图表主色换肤一致；下方 ticket/stats 为语义色保留 */
  &--greet { background: linear-gradient(135deg, var(--fa-brand-blue, #4F6BFF), var(--fa-brand-violet, #6D5BFF)); }
  &--ticket { background: linear-gradient(135deg, var(--wot-orange-6), var(--wot-orange-4)); }
  &--ticket-empty { background: linear-gradient(135deg, var(--wot-green-6), var(--wot-green-4)); }
  &--stats { background: linear-gradient(135deg, var(--wot-purple-6), var(--wot-purple-4)); }

  &__body {
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    flex: 1;
    min-width: 0;
  }

  &__tag {
    align-self: flex-start;
    margin-bottom: 20rpx;
  }

  &__title {
    font-size: 40rpx;
    font-weight: 700;
    line-height: 1.3;
    margin-bottom: 8rpx;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  &__subtitle {
    font-size: 24rpx;
    color: rgba(255, 255, 255, 0.95);
    margin-bottom: 8rpx;
  }

  &__desc {
    font-size: 24rpx;
    color: rgba(255, 255, 255, 0.95);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  &__cta {
    position: relative;
    z-index: 1;
    flex-shrink: 0;
    margin-left: 24rpx;
    display: flex;
    align-items: center;
    gap: 8rpx;
    padding: 16rpx 24rpx;
    border-radius: 9999rpx;
    background: rgba(15, 23, 42, 0.38);
    border: 2rpx solid rgba(255, 255, 255, 0.35);

    &-text {
      font-size: 24rpx;
      font-weight: 500;
      color: #FFFFFF;
      white-space: nowrap;
    }

    &-arrow {
      font-size: 28rpx;
      font-weight: 400;
      color: #FFFFFF;
      line-height: 1;
    }
  }
}

.banner-pause {
  position: absolute;
  right: 16rpx;
  top: 16rpx;
  z-index: 3;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(15, 23, 42, 0.38);
}

.banner-dots {
  position: absolute;
  right: 24rpx;
  bottom: 16rpx;
  display: flex;
  align-items: center;
  gap: 8rpx;

  &__dot {
    width: 10rpx;
    height: 10rpx;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.45);
    transition: all 0.3s ease;

    &.is-active {
      width: 28rpx;
      border-radius: 9999rpx;
      background: #FFFFFF;
    }
  }
}
</style>
