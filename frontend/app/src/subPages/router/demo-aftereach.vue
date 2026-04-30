<script setup lang="ts">
definePage({
  name: 'demo-aftereach',
  style: {
    navigationBarTitleText: 'afterEach 钩子演示',
  },
})

const router = useRouter()

function goBack() {
  router.back()
}
</script>

<template>
  <view class="min-h-screen bg-gray-100 py-3 dark:bg-[var(--wot-dark-background)]">
    <!-- 头部 -->
    <view class="mx-3 mb-3">
      <view class="rounded-3 bg-white px-5 py-6 text-center dark:bg-[var(--wot-dark-background2)]">
        <view class="mb-3 text-8">
          📊
        </view>
        <view class="mb-2 text-5 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
          afterEach 钩子演示
        </view>
        <view class="text-3.5 text-gray-600 dark:text-[var(--wot-dark-color2)]">
          这个页面用于演示 afterEach 钩子的触发
        </view>
      </view>
    </view>

    <!-- 内容 -->
    <demo-block title="afterEach 演示成功" transparent>
      <view class="border border-green-200 rounded-2 bg-green-50 p-4 dark:bg-green-900/20">
        <view class="mb-2 text-4 text-green-700 font-bold dark:text-green-300">
          🎉 恭喜！
        </view>
        <view class="text-3.5 text-green-600 leading-relaxed dark:text-green-200">
          如果你能看到这个页面，说明 afterEach 钩子已经触发了！\n
          打开浏览器控制台（F12 → Console）可以看到相关的日志输出。\n
          afterEach 钩子常用于页面统计、埋点上报等导航后处理。
        </view>
      </view>
    </demo-block>

    <!-- 操作按钮 -->
    <demo-block title="导航" transparent>
      <wd-button type="warning" block @click="goBack">
        返回上一页
      </wd-button>
    </demo-block>
  </view>
</template>
