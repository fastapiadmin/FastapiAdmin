<script lang="ts" setup>
definePage({
  name: 'settings',
  style: {
    navigationBarTitleText: '系统设置',
  },
})

// 是否正在清理
const clearing = ref(false)
// 缓存大小
const cacheSize = ref<any>('计算中...')

const {
  theme,
  toggleTheme,
  currentThemeColor,
  showThemeColorSheet,
  themeColorOptions,
  openThemeColorPicker,
  closeThemeColorPicker,
  selectThemeColor,
  setFollowSystem,
} = useManualTheme()

const isDark = computed({
  get() {
    return theme.value === 'dark'
  },
  set() {
    toggleTheme()
  },
})

// 处理主题色选择
function handleThemeColorSelect(option: any) {
  selectThemeColor(option)
}

// 获取缓存大小
async function getCacheSize() {
  try {
    // #ifdef MP-WEIXIN
    const res = await uni.getStorageInfo()
    cacheSize.value = formatSize(res.currentSize)
    // #endif
    // #ifdef H5
    cacheSize.value = formatSize(
      Object.keys(localStorage).reduce(
        (size, key) => size + localStorage[key].length,
        0,
      ),
    )
    // #endif
    if (!cacheSize.value) {
      cacheSize.value = '0B'
    }
  }
  catch (error) {
    console.error('获取缓存大小失败:', error)
    cacheSize.value = '获取失败'
  }
}

// 格式化存储大小
function formatSize(size: number) {
  if (size < 1024) {
    return `${size}B`
  }
  else if (size < 1024 * 1024) {
    return `${(size / 1024).toFixed(2)}KB`
  }
  else {
    return `${(size / 1024 / 1024).toFixed(2)}MB`
  }
}

// 处理清除缓存
async function handleClearCache() {
  if (cacheSize.value === '获取失败') {
    uni.showToast({
      title: '获取缓存信息失败，请稍后重试',
      icon: 'none',
      duration: 2000,
    })
    return
  }
  if (cacheSize.value === '0B') {
    uni.showToast({
      title: '暂无缓存需要清理',
      icon: 'none',
      duration: 2000,
    })
    return
  }
  if (clearing.value) {
    return
  }

  try {
    clearing.value = true
    // 模拟清理过程
    await new Promise(resolve => setTimeout(resolve, 1500))
    // 清除缓存
    await uni.clearStorage()
    // 更新缓存大小显示
    await getCacheSize()
    // 提示清理成功
    uni.showToast({
      title: '清理成功',
      icon: 'success',
    })
  }
  catch {
    uni.showToast({
      title: '清理失败',
      icon: 'error',
    })
  }
  finally {
    clearing.value = false
  }
}

// 页面加载时初始化
onLoad(() => {
  getCacheSize()
})
</script>

<template>
  <view class="app-container">
    <demo-block title="基础设置" transparent>
      <wd-cell-group border custom-class="rounded-2! overflow-hidden">
        <wd-cell title="暗黑模式">
          <wd-switch v-model="isDark" size="18px" />
        </wd-cell>
        <wd-cell title="跟随系统">
          <wd-button size="small" @click="setFollowSystem">
            跟随系统
          </wd-button>
        </wd-cell>
        <wd-cell title="选择主题色" is-link @click="openThemeColorPicker">
          <view class="flex items-center justify-end gap-2">
            <view
              class="h-4 w-4 rounded-full"
              :style="{ backgroundColor: currentThemeColor.primary }"
            />
            <text>{{ currentThemeColor.name }}</text>
          </view>
        </wd-cell>

        <wd-divider />
        <wd-cell
          title="清空缓存"
          icon="delete1"
          :value="cacheSize"
          clickable
          @click="handleClearCache"
        />
      </wd-cell-group>
    </demo-block>

    <!-- 主题色选择 ActionSheet -->
    <wd-action-sheet
      v-model="showThemeColorSheet"
      title="选择主题色"
      :close-on-click-action="true"
      @cancel="closeThemeColorPicker"
    >
      <view class="px-4 pb-4">
        <view
          v-for="option in themeColorOptions"
          :key="option.value"
          class="flex items-center justify-between border-b border-gray-100 py-3 last:border-b-0 dark:border-gray-700"
          @click="handleThemeColorSelect(option)"
        >
          <view class="flex items-center gap-3">
            <view
              class="h-6 w-6 border-2 border-gray-200 rounded-full dark:border-gray-600"
              :style="{ backgroundColor: option.primary }"
            />
            <text class="text-4 text-gray-800 dark:text-gray-200">
              {{ option.name }}
            </text>
          </view>
          <wd-icon
            v-if="currentThemeColor.value === option.value"
            name="check"
            :color="option.primary"
            size="20px"
          />
        </view>
      </view>
      <wd-gap :height="50" />
    </wd-action-sheet>

    <!-- 使用wot-design-uni的Loading组件 -->
    <wd-loading
      v-if="clearing"
      v-model="clearing"
      text="正在清理..."
      mask
      custom-class="loading-center"
    />
  </view>
</template>

<style lang="scss">
</style>
