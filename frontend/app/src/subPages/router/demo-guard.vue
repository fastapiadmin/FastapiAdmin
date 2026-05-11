<script setup lang="ts">
definePage({
  name: 'demo-guard',
  style: {
    navigationBarTitleText: '导航守卫演示',
  },
})

const router = useRouter()

function goBack() {
  router.back()
}

// 演示权限拦截
function handleBeforeEach() {
  router.push({
    name: 'demo-protected',
  })
}

// 跳转到afterEach演示页面
function demoAfterEachPage() {
  router.push('/subPages/router/demo-aftereach')
}
</script>

<template>
  <view class="bg-gray-100 py-3 dark:bg-[var(--wot-dark-background)]">
    <!-- 头部 -->
    <view class="mx-3 mb-3">
      <view class="rounded-3 bg-white px-5 py-6 text-center dark:bg-[var(--wot-dark-background2)]">
        <view class="mb-3 text-8">
          🛡️
        </view>
        <view class="mb-2 text-5 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
          导航守卫演示
        </view>
        <view class="text-3.5 text-gray-600 dark:text-[var(--wot-dark-color2)]">
          演示 beforeEach 和 afterEach 守卫功能
        </view>
      </view>
    </view>

    <!-- 守卫演示 -->
    <demo-block title="守卫演示" transparent>
      <view class="space-y-3">
        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            前置导航守卫拦截
          </view>
          <view class="mb-3 text-3.5 text-gray-600 dark:text-[var(--wot-dark-color2)]">
            跳转前交互，可以拦截导航
          </view>
          <wd-button type="error" block @click="handleBeforeEach">
            📊 beforeEach 演示
          </wd-button>
        </view>

        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            后置导航钩子演示
          </view>
          <view class="mb-3 text-3.5 text-gray-600 dark:text-[var(--wot-dark-color2)]">
            跳转到专门的 afterEach 演示页面，体验页面统计、埋点上报等功能
          </view>
          <wd-button type="success" block @click="demoAfterEachPage">
            📊 afterEach 演示
          </wd-button>
        </view>
      </view>
    </demo-block>

    <!-- 操作按钮 -->
    <demo-block title="导航" transparent>
      <view class="px-3">
        <wd-button type="warning" block @click="goBack">
          返回上一页
        </wd-button>
      </view>
    </demo-block>
  </view>
</template>
