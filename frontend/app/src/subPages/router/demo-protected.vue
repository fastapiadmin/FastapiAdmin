<script setup lang="ts">
definePage({
  name: 'demo-protected',
  style: {
    navigationBarTitleText: '受保护页面',
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
          🔒
        </view>
        <view class="mb-2 text-5 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
          受保护的页面
        </view>
        <view class="text-3.5 text-gray-600 dark:text-[var(--wot-dark-color2)]">
          这个页面被路由守卫保护，只有登录用户才能访问
        </view>
      </view>
    </view>

    <!-- 内容 -->
    <demo-block title="守卫拦截成功" transparent>
      <view class="border border-green-200 rounded-2 bg-green-50 p-4 dark:bg-green-900/20">
        <view class="mb-2 text-4 text-green-700 font-bold dark:text-green-300">
          🎉 恭喜！
        </view>
        <view class="text-3.5 text-green-600 leading-relaxed dark:text-green-200">
          如果你能看到这个页面，说明路由守卫验证通过了！\n
          但实际上，这个页面被配置为需要登录才能访问，\n
          守卫应该会拦截并重定向你到首页。
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
