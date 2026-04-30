<script setup lang="ts">
definePage({
  name: 'demo-object',
  style: {
    navigationBarTitleText: '对象路径跳转',
  },
})

const router = useRouter()
const route = useRoute()

function goBack() {
  router.back()
}

function pushToParams() {
  router.push({ name: 'demo-params', params: { username: 'eduardo' } })
}

function pushToQuery() {
  router.push({ path: '/subPages/router/demo-query', query: { keyword: 'vue', type: 'framework' } })
}
</script>

<template>
  <view class="min-h-screen bg-gray-100 py-3 dark:bg-[var(--wot-dark-background)]">
    <!-- 头部 -->
    <view class="mx-3 mb-3">
      <view class="rounded-3 bg-white px-5 py-6 text-center dark:bg-[var(--wot-dark-background2)]">
        <view class="mb-3 text-8">
          🎯
        </view>
        <view class="mb-2 text-5 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
          对象路径跳转演示
        </view>
        <view class="text-3.5 text-gray-600 dark:text-[var(--wot-dark-color2)]">
          使用 router.push({ path: '/path' }) 进行跳转
        </view>
      </view>
    </view>

    <!-- 跳转信息 -->
    <demo-block title="跳转信息" transparent>
      <view class="rounded-3 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
        <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
          当前页面信息
        </view>
        <view class="space-y-2">
          <view class="flex items-center justify-between border-b border-gray-100 py-2 dark:border-[var(--wot-dark-border)]">
            <text class="text-3.5 text-gray-600 dark:text-[var(--wot-dark-color2)]">
              路径:
            </text>
            <text class="text-3.5 text-gray-800 font-mono dark:text-[var(--wot-dark-color)]">
              {{ route.path }}
            </text>
          </view>
          <view class="flex items-center justify-between border-b border-gray-100 py-2 dark:border-[var(--wot-dark-border)]">
            <text class="text-3.5 text-gray-600 dark:text-[var(--wot-dark-color2)]">
              跳转方式:
            </text>
            <text class="text-3.5 text-gray-800 dark:text-[var(--wot-dark-color)]">
              对象路径
            </text>
          </view>
          <view class="flex items-center justify-between py-2">
            <text class="text-3.5 text-gray-600 dark:text-[var(--wot-dark-color2)]">
              代码:
            </text>
            <text class="text-3.5 text-gray-800 font-mono dark:text-[var(--wot-dark-color)]">
              router.push({ path: '/subPages/router/demo-object' })
            </text>
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 参数传递演示 -->
    <demo-block title="参数传递演示" transparent>
      <view class="space-y-3">
        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            params 参数传递
          </view>
          <view class="mb-3 text-3.5 text-gray-600 dark:text-[var(--wot-dark-color2)]">
            使用 name + params 组合传递参数
          </view>
          <view class="mb-3 border border-gray-200 rounded-2 bg-gray-50 p-3 dark:border-[var(--wot-dark-border)] dark:bg-[var(--wot-dark-background3)]">
            <text class="text-3 text-gray-700 font-mono dark:text-[var(--wot-dark-color)]">
              router.push({ name: 'demo-params', params: { username: 'eduardo' } })
            </text>
          </view>
          <wd-button type="primary" block @click="pushToParams">
            跳转并传递 params
          </wd-button>
        </view>

        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            query 参数传递
          </view>
          <view class="mb-3 text-3.5 text-gray-600 dark:text-[var(--wot-dark-color2)]">
            使用 path + query 组合传递参数
          </view>
          <view class="mb-3 border border-gray-200 rounded-2 bg-gray-50 p-3 dark:border-[var(--wot-dark-border)] dark:bg-[var(--wot-dark-background3)]">
            <text class="text-3 text-gray-700 font-mono dark:text-[var(--wot-dark-color)]">
              router.push({ path: '/demo-query', query: { keyword: 'vue' } })
            </text>
          </view>
          <wd-button type="success" block @click="pushToQuery">
            跳转并传递 query
          </wd-button>
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
