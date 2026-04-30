<script setup lang="ts">
import { onReady, onShow } from '@dcloudio/uni-app'
import { reactive, ref } from 'vue'
import LineChart from '@/subPages/echarts/components/LineChart.vue'

defineOptions({
  componentPlaceholder: {
    LineChart: 'view',
  },
})

definePage({
  name: 'home',
  layout: 'tabbar',
  style: {
    navigationBarTitleText: '首页',
  },
})

const current = ref<number>(0)

/**
 * 访问统计数据
 */
interface VisitStatsVO {
  todayUvCount: number
  uvGrowthRate: number
  totalUvCount: number
  todayPvCount: number
  pvGrowthRate: number
  totalPvCount: number
}

/**
 * 导航项
 */
interface NavItem {
  icon: string
  title: string
  url: string
  prem: string
}

/**
 * 快捷导航列表
 */
const NAV_LIST: NavItem[] = [
  {
    icon: '/static/icons/user.png',
    title: '用户管理',
    url: '/pages/work/user/index',
    prem: 'sys:user:query',
  },
  {
    icon: '/static/icons/role.png',
    title: '角色管理',
    url: '/pages/work/role/index',
    prem: 'sys:role:query',
  },
  {
    icon: '/static/icons/notice.png',
    title: '通知公告',
    url: '/pages/work/notice/index',
    prem: 'sys:notice:query',
  },
  {
    icon: '/static/icons/setting.png',
    title: '系统配置',
    url: '/pages/work/config/index',
    prem: 'sys:config:query',
  },
]

/**
 * 默认访问统计数据
 */
const DEFAULT_VISIT_STATS: VisitStatsVO = {
  todayUvCount: 1234,
  uvGrowthRate: 15.6,
  totalUvCount: 45678,
  todayPvCount: 5678,
  pvGrowthRate: 23.4,
  totalPvCount: 123456,
}

// 通知公告文本
const NOTICE_TEXT = '通知公告: fastapp 是一个基于 Vue3 + UniApp 的前端模板项目，提供了一套完整的前端解决方案'

// 默认日期范围（天数)
const DEFAULT_DAYS_RANGE = 7

// 访问统计数据
const visitStatsData = ref<VisitStatsVO>(DEFAULT_VISIT_STATS)

// 图表数据
const chartData = ref({})

// 日期范围
const recentDaysRange = ref(DEFAULT_DAYS_RANGE)

// 轮播图列表
const swiperList = ref([
  '/static/images/banner01.jpg',
  '/static/images/banner02.jpg',
])

// 快捷导航列表
const navList = reactive(NAV_LIST)

// 导航到指定页面
function navigateTo(url: string) {
  // 避免空 URL 导航
  if (!url)
    return

  // 根据 URL 类型选择不同的导航方式
  if (
    url.startsWith('/pages/')
    && (url.includes('/index/')
      || url.includes('/mine/')
      || url.includes('/work/'))
  ) {
    uni.switchTab({
      url,
    })
  }
  else {
    uni.navigateTo({
      url,
    })
  }
}

// 生成静态的访问趋势数据
function generateStaticTrendData(days: number) {
  const ipList = []
  const pvList = []

  const today = new Date()

  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(today)
    date.setDate(today.getDate() - i)

    // 生成模拟数据
    ipList.push(Math.floor(Math.random() * 500) + 200)
    pvList.push(Math.floor(Math.random() * 1000) + 500)
  }

  return {
    ipList,
    pvList,
  }
}

// 加载访问统计数据（使用静态数据）
async function loadVisitStatsData() {
  // 模拟异步加载
  setTimeout(() => {
    visitStatsData.value = { ...DEFAULT_VISIT_STATS }
  }, 100)
}

// 加载访问趋势数据（使用静态数据）
function loadVisitTrendData() {
  // 模拟异步加载
  setTimeout(() => {
    const data = generateStaticTrendData(recentDaysRange.value)

    const res = {
      series: [
        {
          name: 'UV',
          data: data.ipList,
        },
        {
          name: 'PV',
          data: data.pvList,
        },
      ],
    }
    chartData.value = JSON.parse(JSON.stringify(res))
  }, 100)
}

onReady(() => {
  loadVisitStatsData()
  loadVisitTrendData()
})

onShow(() => {
  // 确保 tabbar 状态正确
  const pages = getCurrentPages()
  if (pages.length > 0) {
    const currentPage = pages[pages.length - 1]
    if (currentPage.route === 'pages/index/index') {
      // 通过事件通知 tabbar 布局更新状态
      uni.$emit('updateTabbar', 'index')
    }
  }
})
</script>

<template>
  <view class="app-container">
    <!-- 轮播图 -->
    <view class="swiper-container">
      <wd-swiper
        v-model:current="current"
        :list="swiperList"
        autoplay
        indicator
        image-mode="scaleToFill"
      />
    </view>

    <!-- 快捷导航 -->
    <view class="nav-grid">
      <wd-grid clickable :column="4">
        <wd-grid-item
          v-for="(item, index) in navList"
          :key="index"
          @click="navigateTo(item.url)"
        >
          <template #icon>
            <image class="icon-image" :src="item.icon" lazy-load />
          </template>
          <template #text>
            <view class="nav-title">
              <wd-text :text="item.title" />
            </view>
          </template>
        </wd-grid-item>
      </wd-grid>
    </view>

    <!-- 通知公告 -->
    <view class="notice-text">
      <wd-notice-bar
        type="warning"
        prefix="warn-bold"
        :text="NOTICE_TEXT"
      />
    </view>

    <!-- 数据统计 -->
    <view class="stats-grid">
      <view class="stats-item">
        <image class="stats-icon" src="/static/icons/visitor.png" lazy-load />
        <view class="stats-info">
          <wd-text text="访客数" />
          <view class="stats-value">
            <wd-text type="warning" :text="visitStatsData.todayUvCount" bold />
          </view>
        </view>
      </view>
      <view class="stats-item">
        <image class="stats-icon" src="/static/icons/browser.png" lazy-load />
        <view class="stats-info">
          <wd-text text="浏览量" />
          <view class="stats-value">
            <wd-text type="success" :text="visitStatsData.todayPvCount" bold />
          </view>
        </view>
      </view>
    </view>

    <!-- 访问趋势 -->
    <view class="mb-1 rounded-2 bg-gray-50 p-3 shadow-sm">
      <LineChart />
    </view>
  </view>
</template>

<style lang="scss" scoped>
.app-container {
  padding: 20rpx;

  .swiper-container {
    margin-bottom: 20rpx;
    border-radius: 16rpx;
    overflow: hidden;
  }

  .nav-grid {
    margin-bottom: 20rpx;
    border-radius: 16rpx;

    .icon-image {
      width: 64rpx;
      height: 64rpx;
      border-radius: 8rpx;
    }

    .nav-title {
      margin-bottom: 20rpx;
      border-radius: 16rpx;
      font-size: 24rpx;
      text-align: center;
      margin-top: 12rpx;
    }
  }

  .notice-text {
    margin-bottom: 20rpx;
    border-radius: 16rpx;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10rpx;
    margin-bottom: 20rpx;
  }

  .stats-item {
    display: flex;
    align-items: center;
    padding: 20rpx;
    background-color: var(--bg-color-2);
    border-radius: 16rpx;
  }

  .stats-icon {
    width: 80rpx;
    height: 80rpx;
    border-radius: 8rpx;
    margin-right: 20rpx;
  }
}
</style>
