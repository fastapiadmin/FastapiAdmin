<script setup lang="ts">
import { defineStore } from 'pinia'

definePage({
  name: 'pinia',
  style: {
    navigationBarTitleText: 'Pinia 演示',
  },
})

const { success: showSuccess } = useGlobalToast()

// 定义一个基础的计数器store
const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)

  function increment() {
    count.value++
  }

  function decrement() {
    count.value--
  }

  function reset() {
    count.value = 0
  }

  return {
    count,
    doubleCount,
    increment,
    decrement,
    reset,
  }
})

// 定义一个用户信息store（演示持久化）
const useUserStore = defineStore('user', () => {
  const userInfo = ref({
    name: '',
    email: '',
    avatar: '',
    theme: 'light',
  })

  const isLoggedIn = computed(() => !!userInfo.value.name)

  function setUserInfo(info: Partial<typeof userInfo.value>) {
    userInfo.value = { ...userInfo.value, ...info }
  }

  function clearUserInfo() {
    userInfo.value = {
      name: '',
      email: '',
      avatar: '',
      theme: 'light',
    }
  }

  function toggleTheme() {
    userInfo.value.theme = userInfo.value.theme === 'light' ? 'dark' : 'light'
  }

  return {
    userInfo,
    isLoggedIn,
    setUserInfo,
    clearUserInfo,
    toggleTheme,
  }
})

// 定义一个临时store（不持久化）
const useTempStore = defineStore('temp', () => {
  const tempData = ref({
    message: '',
    timestamp: Date.now(),
  })

  function setMessage(msg: string) {
    tempData.value.message = msg
    tempData.value.timestamp = Date.now()
  }

  function clearMessage() {
    tempData.value.message = ''
    tempData.value.timestamp = Date.now()
  }

  return {
    tempData,
    setMessage,
    clearMessage,
  }
})

// 使用stores
const counterStore = useCounterStore()
const userStore = useUserStore()
const tempStore = useTempStore()

// 表单数据
const userForm = ref({
  name: '',
  email: '',
})

const tempMessage = ref('')

// 复制代码到剪贴板
function copyCode(code: string) {
  uni.setClipboardData({
    data: code,
    showToast: false,
    success: () => {
      uni.hideToast()
      showSuccess({ msg: '代码已复制到剪贴板' })
    },
  })
}

// 保存用户信息
function saveUserInfo() {
  if (!userForm.value.name) {
    uni.showToast({
      title: '请输入用户名',
      icon: 'none',
    })
    return
  }

  userStore.setUserInfo({
    name: userForm.value.name,
    email: userForm.value.email,
    avatar: '😆',
  })

  showSuccess({ msg: '用户信息已保存（会持久化）' })
}

// 设置临时消息
function setTempMessage() {
  if (!tempMessage.value) {
    uni.showToast({
      title: '请输入消息内容',
      icon: 'none',
    })
    return
  }

  tempStore.setMessage(tempMessage.value)
  tempMessage.value = ''
  showSuccess({ msg: '临时消息已设置（不会持久化）' })
}

// 链接导航处理
function handleNavigate(url: string) {
  // #ifdef H5
  window.open(url, '_blank')
  // #endif
  // #ifndef H5
  uni.setClipboardData({
    data: url,
    showToast: false,
    success: () => {
      uni.hideToast()
      showSuccess({ msg: `${url} 已复制到剪贴板` })
    },
  })
  // #endif
}
</script>

<template>
  <view class="min-h-screen bg-gray-100 py-3 dark:bg-[var(--wot-dark-background)]">
    <!-- 头部介绍 -->
    <view class="mx-3 mb-3">
      <view class="rounded-3 bg-white px-5 py-8 text-center dark:bg-[var(--wot-dark-background2)]">
        <view class="mb-3 text-10">
          🍍
        </view>
        <view class="mb-2 text-6 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
          Pinia 状态管理
        </view>
        <view class="mb-2 text-3.5 text-gray-600 leading-relaxed dark:text-[var(--wot-dark-color2)]">
          Vue 3 的直观状态管理库
        </view>
        <view class="mb-2 text-3 text-gray-500 dark:text-[var(--wot-dark-color2)]">
          轻量、类型安全、支持组合式API
        </view>
        <view class="text-3 text-gray-500 dark:text-[var(--wot-dark-color2)]">
          本项目默认持久化所有 Store 数据，开发者可以配置排除列表
        </view>
      </view>
    </view>

    <!-- 基础计数器演示 -->
    <demo-block title="基础使用 - 计数器" transparent>
      <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
        <view class="mb-4 text-center">
          <view class="mb-2 text-8 text-blue-500">
            {{ counterStore.count }}
          </view>
          <view class="text-3 text-gray-600 dark:text-[var(--wot-dark-color2)]">
            双倍值: {{ counterStore.doubleCount }}
          </view>
        </view>

        <view class="grid grid-cols-3 mb-4 gap-2">
          <wd-button type="success" size="small" @click="counterStore.increment">
            +1
          </wd-button>
          <wd-button type="warning" size="small" @click="counterStore.decrement">
            -1
          </wd-button>
          <wd-button type="info" size="small" @click="counterStore.reset">
            重置
          </wd-button>
        </view>

        <!-- 代码示例 -->
        <view class="space-y-3">
          <view class="rounded bg-gray-100 p-3 dark:bg-[var(--wot-dark-background3)]">
            <view class="mb-2 text-3 text-gray-700 font-bold dark:text-[var(--wot-dark-color)]">
              定义 Store:
            </view>
            <view
              class="text-2.5 text-gray-600 leading-relaxed font-mono dark:text-[var(--wot-dark-color2)]" @click="copyCode(`const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)

  function increment() {
    count.value++
  }

  return { count, doubleCount, increment }
})`)"
            >
              const useCounterStore = defineStore('counter', () => {\n
              &nbsp;&nbsp;const count = ref(0)\n
              &nbsp;&nbsp;const doubleCount = computed(() => count.value * 2)\n
              &nbsp;&nbsp;function increment() { count.value++ }\n
              &nbsp;&nbsp;return { count, doubleCount, increment }\n
              })
            </view>
          </view>

          <view class="rounded bg-gray-100 p-3 dark:bg-[var(--wot-dark-background3)]">
            <view class="mb-2 text-3 text-gray-700 font-bold dark:text-[var(--wot-dark-color)]">
              使用 Store:
            </view>
            <view
              class="text-2.5 text-gray-600 leading-relaxed font-mono dark:text-[var(--wot-dark-color2)]" @click="copyCode(`const counterStore = useCounterStore()
// 直接使用
counterStore.increment()
// 响应式访问
console.log(counterStore.count)`)"
            >
              const counterStore = useCounterStore()\n
              counterStore.increment() // 调用方法\n
              console.log(counterStore.count) // 访问状态
            </view>
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 用户信息演示（持久化） -->
    <demo-block title="持久化演示 - 用户信息" transparent>
      <view class="mb-3 border border-green-200 rounded-2 bg-green-50 p-3 dark:border-green-800 dark:bg-green-900/20">
        <view class="mb-1 text-3.5 text-green-700 font-bold dark:text-green-300">
          ✅ 持久化存储
        </view>
        <view class="text-3 text-green-600 leading-relaxed dark:text-green-200">
          这个 Store 的数据会自动保存到本地存储，刷新页面后数据不会丢失
        </view>
      </view>

      <view class="space-y-4">
        <!-- 当前用户信息 -->
        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            当前用户信息
          </view>

          <view v-if="userStore.isLoggedIn" class="flex items-center space-x-3">
            <view class="rounded-full text-12">
              {{ userStore.userInfo.avatar }}
            </view>
            <view class="flex-1">
              <view class="text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
                {{ userStore.userInfo.name }}
              </view>
              <view class="text-3 text-gray-600 dark:text-[var(--wot-dark-color2)]">
                {{ userStore.userInfo.email }}
              </view>
            </view>
          </view>

          <view v-else class="text-center text-gray-500 dark:text-[var(--wot-dark-color2)]">
            暂无用户信息
          </view>
        </view>

        <!-- 用户信息表单 -->
        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            设置用户信息
          </view>

          <view class="space-y-3">
            <view>
              <view class="mb-1 text-3 text-gray-700 dark:text-[var(--wot-dark-color)]">
                用户名:
              </view>
              <wd-input v-model="userForm.name" placeholder="请输入用户名" />
            </view>

            <view>
              <view class="mb-1 text-3 text-gray-700 dark:text-[var(--wot-dark-color)]">
                邮箱:
              </view>
              <wd-input v-model="userForm.email" placeholder="请输入邮箱" />
            </view>

            <view class="grid grid-cols-2 gap-2">
              <wd-button type="primary" @click="saveUserInfo">
                保存信息
              </wd-button>
              <wd-button type="error" @click="userStore.clearUserInfo">
                清除信息
              </wd-button>
            </view>
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 临时数据演示（不持久化） -->
    <demo-block title="非持久化演示 - 临时数据" transparent>
      <view class="mb-3 border border-orange-200 rounded-2 bg-orange-50 p-3 dark:border-orange-800 dark:bg-orange-900/20">
        <view class="mb-1 text-3.5 text-orange-700 font-bold dark:text-orange-300">
          ⚠️ 临时存储
        </view>
        <view class="text-3 text-orange-600 leading-relaxed dark:text-orange-200">
          这个 Store 的数据不会持久化，刷新页面后数据会丢失
        </view>
      </view>

      <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
        <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
          临时消息
        </view>

        <view v-if="tempStore.tempData.message" class="mb-4 rounded-2 bg-blue-50 p-3 dark:bg-blue-900/20">
          <view class="text-3.5 text-blue-700 font-bold dark:text-blue-300">
            {{ tempStore.tempData.message }}
          </view>
          <view class="text-2.5 text-blue-600 dark:text-blue-200">
            时间戳: {{ new Date(tempStore.tempData.timestamp).toLocaleString() }}
          </view>
        </view>

        <view v-else class="mb-4 text-center text-gray-500 dark:text-[var(--wot-dark-color2)]">
          暂无临时消息
        </view>

        <view class="space-y-3">
          <wd-input v-model="tempMessage" placeholder="请输入临时消息" />
          <view class="grid grid-cols-2 gap-2">
            <wd-button type="primary" size="small" @click="setTempMessage">
              设置消息
            </wd-button>
            <wd-button type="warning" size="small" @click="tempStore.clearMessage">
              清除消息
            </wd-button>
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 持久化原理 -->
    <demo-block title="持久化实现原理" transparent>
      <view class="space-y-4">
        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            持久化插件
          </view>
          <view class="mb-3 text-3 text-gray-600 leading-relaxed dark:text-[var(--wot-dark-color2)]">
            项目使用自定义的 Pinia 插件实现持久化，位于 <text class="text-blue-600 font-mono dark:text-blue-400">
              src/store/persist.ts
            </text>
          </view>

          <view
            class="rounded bg-gray-100 p-3 dark:bg-[var(--wot-dark-background3)]" @click="copyCode(`function persist({ store }, excludedIds) {
  // 检查是否需要排除
  if (excludedIds.includes(store.$id)) return

  // 从本地存储读取数据
  const storageState = uni.getStorageSync(store.$id)
  if (storageState) {
    store.$state = storageState
  }

  // 监听状态变化并保存
  store.$subscribe(() => {
    uni.setStorageSync(store.$id, store.$state)
  })
}`)"
          >
            <view class="mb-2 text-3 text-gray-700 font-bold dark:text-[var(--wot-dark-color)]">
              核心实现:
            </view>
            <view class="text-2.5 text-gray-600 leading-relaxed font-mono dark:text-[var(--wot-dark-color2)]">
              function persist({ store }, excludedIds) {\n
              &nbsp;&nbsp;// 检查是否需要排除\n
              &nbsp;&nbsp;if (excludedIds.includes(store.$id)) return\n
              &nbsp;&nbsp;// 从本地存储读取数据\n
              &nbsp;&nbsp;const storageState = uni.getStorageSync(store.$id)\n
              &nbsp;&nbsp;// 监听状态变化并保存\n
              &nbsp;&nbsp;store.$subscribe(() => {\n
              &nbsp;&nbsp;&nbsp;&nbsp;uni.setStorageSync(store.$id, store.$state)\n
              &nbsp;&nbsp;})\n
              }
            </view>
          </view>
        </view>

        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            排除列表
          </view>
          <view class="mb-3 text-3 text-gray-600 leading-relaxed dark:text-[var(--wot-dark-color2)]">
            可以通过排除列表控制哪些 Store 不需要持久化
          </view>

          <view
            class="rounded bg-gray-100 p-3 dark:bg-[var(--wot-dark-background3)]" @click="copyCode(`// 在 persist.ts 中配置排除列表
persist(context, ['global-register', 'temp'])`)"
          >
            <view class="text-2.5 text-gray-600 leading-relaxed font-mono dark:text-[var(--wot-dark-color2)]">
              // 当前排除的 Store ID:\n
              ['global-register', 'temp']
            </view>
          </view>
        </view>

        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            使用说明
          </view>
          <view class="text-3 text-gray-600 leading-relaxed space-y-2 dark:text-[var(--wot-dark-color2)]">
            <view>
              • <text class="text-green-600 font-bold dark:text-green-400">
                自动持久化
              </text>：默认情况下，所有 Store 都会自动持久化
            </view>
            <view>
              • <text class="text-orange-600 font-bold dark:text-orange-400">
                排除机制
              </text>：通过 Store ID 控制哪些不需要持久化
            </view>
            <view>
              • <text class="text-blue-600 font-bold dark:text-blue-400">
                深拷贝保护
              </text>：使用深拷贝避免引用问题
            </view>
            <view>
              • <text class="text-purple-600 font-bold dark:text-purple-400">
                自动恢复
              </text>：页面刷新时自动从本地存储恢复数据
            </view>
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 最佳实践 -->
    <demo-block title="最佳实践" transparent>
      <view class="space-y-3">
        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 flex items-center">
            <view class="mr-2 text-6">
              💡
            </view>
            <view class="text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
              Store 设计建议
            </view>
          </view>
          <view class="text-3 text-gray-600 leading-relaxed space-y-2 dark:text-[var(--wot-dark-color2)]">
            <view>• 使用组合式 API 风格定义 Store</view>
            <view>• 合理拆分 Store，避免单个 Store 过于庞大</view>
            <view>• 使用 TypeScript 获得更好的类型支持</view>
            <view>• 为 Store 提供清晰的命名和注释</view>
          </view>
        </view>

        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 flex items-center">
            <view class="mr-2 text-6">
              🔒
            </view>
            <view class="text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
              持久化建议
            </view>
          </view>
          <view class="text-3 text-gray-600 leading-relaxed space-y-2 dark:text-[var(--wot-dark-color2)]">
            <view>• 敏感数据（如密码）不要持久化存储</view>
            <view>• 大量数据考虑使用数据库而非本地存储</view>
            <view>• 临时状态（如加载状态）不需要持久化</view>
            <view>• 定期清理无用的持久化数据</view>
          </view>
        </view>

        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 flex items-center">
            <view class="mr-2 text-6">
              ⚡
            </view>
            <view class="text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
              性能优化
            </view>
          </view>
          <view class="text-3 text-gray-600 leading-relaxed space-y-2 dark:text-[var(--wot-dark-color2)]">
            <view>• 避免在 Store 中存储大量数据</view>
            <view>• 使用 computed 缓存复杂计算结果</view>
            <view>• 合理使用 $subscribe 监听状态变化</view>
            <view>• 考虑使用 $patch 批量更新状态</view>
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 相关链接 -->
    <demo-block title="相关链接" transparent>
      <wd-cell-group border custom-class="rounded-2! overflow-hidden">
        <wd-cell title="📚 Pinia 官方文档" value="状态管理库" is-link @click="handleNavigate('https://pinia.vuejs.org/zh/')" />
        <wd-cell title="🎯 Vue 3 文档" value="组合式 API" is-link @click="handleNavigate('https://cn.vuejs.org/guide/extras/composition-api-faq.html')" />
        <wd-cell title="🔧 uni-app 存储" value="本地存储 API" is-link @click="handleNavigate('https://uniapp.dcloud.net.cn/api/storage/storage.html')" />
      </wd-cell-group>
    </demo-block>
  </view>
</template>
