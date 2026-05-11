<script setup lang="ts">
definePage({
  name: 'styles',
  style: {
    navigationBarTitleText: 'UnoCSS 演示',
  },
})

const { success: showSuccess } = useGlobalToast()

// 演示状态
const animationState = ref(false)

// UnoCSS 核心特性
const unocssFeatures = ref([
  {
    icon: '⚡',
    title: '即时按需',
    desc: '只生成你使用的CSS',
    example: 'text-red-500 bg-blue-100',
  },
  {
    icon: '🎨',
    title: '完全可定制',
    desc: '灵活的配置和预设',
    example: 'custom-color-brand',
  },
  {
    icon: '🔧',
    title: '预设丰富',
    desc: '内置Tailwind、Windi等预设',
    example: '@unocss/preset-wind',
  },
  {
    icon: '🚀',
    title: '性能优异',
    desc: '极快的构建速度',
    example: '< 200ms',
  },
])

// 颜色系统演示
const colorCategories = ref([
  {
    name: '灰色系',
    colors: [
      { name: 'gray-50', class: 'bg-gray-50', value: '#f9fafb' },
      { name: 'gray-100', class: 'bg-gray-100', value: '#f3f4f6' },
      { name: 'gray-200', class: 'bg-gray-200', value: '#e5e7eb' },
      { name: 'gray-300', class: 'bg-gray-300', value: '#d1d5db' },
      { name: 'gray-400', class: 'bg-gray-400', value: '#9ca3af' },
      { name: 'gray-500', class: 'bg-gray-500', value: '#6b7280' },
    ],
  },
  {
    name: '主题色',
    colors: [
      { name: 'blue-500', class: 'bg-blue-500', value: '#3b82f6' },
      { name: 'green-500', class: 'bg-green-500', value: '#10b981' },
      { name: 'red-500', class: 'bg-red-500', value: '#ef4444' },
      { name: 'yellow-500', class: 'bg-yellow-500', value: '#f59e0b' },
      { name: 'purple-500', class: 'bg-purple-500', value: '#8b5cf6' },
      { name: 'pink-500', class: 'bg-pink-500', value: '#ec4899' },
    ],
  },
])

// 布局演示数据
const layoutExamples = ref([
  {
    title: 'Flex 居中',
    code: 'flex items-center justify-center',
    class: 'flex items-center justify-center h-20 bg-blue-100 rounded-2 text-blue-800',
  },
  {
    title: 'Grid 网格',
    code: 'grid grid-cols-3 gap-4',
    class: 'grid grid-cols-3 gap-2',
  },
  {
    title: 'Space Between',
    code: 'flex justify-between items-center',
    class: 'flex justify-between items-center h-16 bg-green-100 rounded-2 px-4 text-green-800',
  },
])

// 间距系统
const spacingExamples = ref([
  { name: 'p-1', value: '4px', class: 'p-1 bg-red-100 inline-block m-1 rounded' },
  { name: 'p-2', value: '8px', class: 'p-2 bg-blue-100 inline-block m-1 rounded' },
  { name: 'p-4', value: '16px', class: 'p-4 bg-green-100 inline-block m-1 rounded' },
  { name: 'p-6', value: '24px', class: 'p-6 bg-yellow-100 inline-block m-1 rounded' },
  { name: 'p-8', value: '32px', class: 'p-8 bg-purple-100 inline-block m-1 rounded' },
])

// 字体系统
const fontExamples = ref([
  { name: 'text-xs', size: '12px', class: 'text-xs' },
  { name: 'text-sm', size: '14px', class: 'text-sm' },
  { name: 'text-base', size: '16px', class: 'text-base' },
  { name: 'text-lg', size: '18px', class: 'text-lg' },
  { name: 'text-xl', size: '20px', class: 'text-xl' },
  { name: 'text-2xl', size: '24px', class: 'text-2xl' },
  { name: 'text-3xl', size: '30px', class: 'text-3xl' },
])

// 阴影和效果
const effectExamples = ref([
  { name: 'shadow-sm', class: 'shadow-sm bg-white p-4 rounded-2 mb-3' },
  { name: 'shadow', class: 'shadow bg-white p-4 rounded-2 mb-3' },
  { name: 'shadow-md', class: 'shadow-md bg-white p-4 rounded-2 mb-3' },
  { name: 'shadow-lg', class: 'shadow-lg bg-white p-4 rounded-2 mb-3' },
  { name: 'shadow-xl', class: 'shadow-xl bg-white p-4 rounded-2 mb-3' },
])

// 切换动画
function toggleAnimation() {
  animationState.value = !animationState.value
  showSuccess({ msg: `动画状态: ${animationState.value ? '开启' : '关闭'}` })
}

// 复制代码
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
          🎨
        </view>
        <view class="mb-2 text-6 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
          UnoCSS 原子化CSS
        </view>
        <view class="mb-2 text-3.5 text-gray-600 leading-relaxed dark:text-[var(--wot-dark-color2)]">
          即时按需的原子化CSS引擎
        </view>
        <view class="text-3 text-gray-500 dark:text-[var(--wot-dark-color2)]">
          具有高性能且极具灵活性的即时原子化CSS引擎
        </view>
      </view>
    </view>

    <!-- UnoCSS 核心特性 -->
    <demo-block title="UnoCSS 核心特性" transparent>
      <view class="grid grid-cols-2 gap-3">
        <view
          v-for="feature in unocssFeatures"
          :key="feature.title"
          class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]"
        >
          <view class="mb-2 text-6">
            {{ feature.icon }}
          </view>
          <view class="mb-1 text-3.5 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            {{ feature.title }}
          </view>
          <view class="mb-2 text-3 text-gray-600 leading-snug dark:text-[var(--wot-dark-color2)]">
            {{ feature.desc }}
          </view>
          <view class="rounded bg-gray-100 px-2 py-1 text-2.5 text-gray-700 font-mono dark:bg-[var(--wot-dark-background3)] dark:text-[var(--wot-dark-color2)]">
            {{ feature.example }}
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 颜色系统 -->
    <demo-block title="颜色系统" transparent>
      <view
        v-for="category in colorCategories"
        :key="category.name"
        class="mb-4 last:mb-0"
      >
        <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
          {{ category.name }}
        </view>
        <view class="grid grid-cols-3 gap-2">
          <view
            v-for="color in category.colors"
            :key="color.name"
            class="overflow-hidden rounded-2 bg-white shadow-sm dark:bg-[var(--wot-dark-background2)]"
            @click="copyCode(color.class)"
          >
            <view :class="color.class" class="h-12 w-full" />
            <view class="p-2">
              <view class="text-2.5 text-gray-800 font-mono dark:text-[var(--wot-dark-color)]">
                {{ color.name }}
              </view>
              <view class="text-2 text-gray-500 dark:text-[var(--wot-dark-color2)]">
                {{ color.value }}
              </view>
            </view>
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 布局系统 -->
    <demo-block title="布局系统" transparent>
      <view class="space-y-4">
        <view
          v-for="example in layoutExamples"
          :key="example.title"
          class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]"
        >
          <view class="mb-3 flex items-center justify-between">
            <view class="text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
              {{ example.title }}
            </view>
            <view class="rounded bg-gray-100 px-2 py-1 text-2.5 text-gray-700 font-mono dark:bg-[var(--wot-dark-background3)] dark:text-[var(--wot-dark-color2)]" @click="copyCode(example.code)">
              {{ example.code }}
            </view>
          </view>
          <view v-if="example.title === 'Flex 居中'" :class="example.class">
            <text class="text-3.5">
              居中内容
            </text>
          </view>
          <view v-else-if="example.title === 'Grid 网格'" :class="example.class">
            <view
              v-for="n in 6"
              :key="n"
              class="rounded bg-blue-100 p-2 text-center text-3 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300"
            >
              {{ n }}
            </view>
          </view>
          <view v-else :class="example.class">
            <text class="text-3.5">
              左侧
            </text>
            <text class="text-3.5">
              右侧
            </text>
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 间距系统 -->
    <demo-block title="间距系统" transparent>
      <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
        <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
          内边距 (Padding)
        </view>
        <view class="mb-4 text-3 text-gray-600 leading-relaxed dark:text-[var(--wot-dark-color2)]">
          点击下方色块复制对应的 padding 类名
        </view>
        <view class="flex flex-wrap items-center gap-2">
          <view
            v-for="spacing in spacingExamples"
            :key="spacing.name"
            :class="spacing.class"
            class="cursor-pointer"
            @click="copyCode(spacing.name)"
          >
            <text class="text-2.5 text-gray-700 font-mono">
              {{ spacing.name }}
            </text>
          </view>
        </view>
        <view class="mt-4 text-2.5 text-gray-500 dark:text-[var(--wot-dark-color2)]">
          💡 提示：p-1 = 4px, p-2 = 8px, p-4 = 16px, p-6 = 24px, p-8 = 32px
        </view>
      </view>
    </demo-block>

    <!-- 字体系统 -->
    <demo-block title="字体系统" transparent>
      <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
        <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
          字体大小
        </view>
        <view class="space-y-3">
          <view
            v-for="font in fontExamples"
            :key="font.name"
            class="flex items-center justify-between border-b border-gray-100 pb-2 last:border-b-0 dark:border-[var(--wot-dark-border)]"
            @click="copyCode(font.name)"
          >
            <text :class="font.class" class="text-gray-800 dark:text-[var(--wot-dark-color)]">
              字体演示文字
            </text>
            <view class="flex items-center space-x-2">
              <text class="text-2.5 text-gray-500 dark:text-[var(--wot-dark-color2)]">
                {{ font.size }}
              </text>
              <text class="rounded bg-gray-100 px-2 py-1 text-2.5 text-gray-700 font-mono dark:bg-[var(--wot-dark-background3)] dark:text-[var(--wot-dark-color2)]">
                {{ font.name }}
              </text>
            </view>
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 阴影效果 -->
    <demo-block title="阴影效果" transparent>
      <view class="space-y-3">
        <view
          v-for="effect in effectExamples"
          :key="effect.name"
          :class="effect.class"
          @click="copyCode(effect.name)"
        >
          <view class="flex items-center justify-between">
            <text class="text-3.5 text-gray-800">
              阴影效果演示
            </text>
            <text class="rounded bg-gray-100 px-2 py-1 text-2.5 text-gray-700 font-mono">
              {{ effect.name }}
            </text>
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 交互效果 -->
    <demo-block title="交互效果" transparent>
      <view class="space-y-4">
        <!-- 悬停效果 -->
        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            悬停效果
          </view>
          <view class="grid grid-cols-2 gap-3">
            <view class="rounded-2 bg-blue-100 p-4 text-center transition-all duration-300 active:scale-95 hover:scale-105 hover:bg-blue-200">
              <text class="text-3 text-blue-800">
                悬停变色
              </text>
            </view>
            <view class="rounded-2 bg-green-100 p-4 text-center transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
              <text class="text-3 text-green-800">
                悬停上浮
              </text>
            </view>
          </view>
          <view class="mt-3 rounded bg-gray-100 p-2 text-2.5 text-gray-700 font-mono dark:bg-[var(--wot-dark-background3)] dark:text-[var(--wot-dark-color2)]" @click="copyCode('hover:bg-blue-200 hover:scale-105 transition-all duration-300')">
            hover:bg-blue-200 hover:scale-105 transition-all duration-300
          </view>
        </view>

        <!-- 动画效果 -->
        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            动画效果
          </view>
          <wd-button type="primary" block @click="toggleAnimation">
            切换动画状态
          </wd-button>
          <view class="mt-4 flex justify-center">
            <view
              class="rounded-2 p-6 text-center transition-all duration-500 ease-in-out"
              :class="[
                animationState
                  ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white transform rotate-12 scale-110 shadow-lg'
                  : 'bg-gray-100 text-gray-800 transform rotate-0 scale-100 shadow-sm dark:bg-[var(--wot-dark-background3)] dark:text-[var(--wot-dark-color)]',
              ]"
            >
              <text class="text-4 font-bold">
                动画演示
              </text>
            </view>
          </view>
          <view class="mt-3 rounded bg-gray-100 p-2 text-2.5 text-gray-700 leading-relaxed font-mono dark:bg-[var(--wot-dark-background3)] dark:text-[var(--wot-dark-color2)]" @click="copyCode('transition-all duration-500 ease-in-out transform rotate-12 scale-110')">
            transition-all duration-500 ease-in-out\n
            transform rotate-12 scale-110
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 响应式设计 -->
    <demo-block title="响应式设计" transparent>
      <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
        <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
          响应式断点
        </view>
        <view class="mb-4 text-3 text-gray-600 leading-relaxed dark:text-[var(--wot-dark-color2)]">
          UnoCSS 支持响应式断点，可以根据屏幕尺寸应用不同样式
        </view>
        <view class="mb-4 rounded-2 bg-red-100 p-4 text-center dark:bg-red-900/30 lg:bg-yellow-100 md:bg-blue-100 sm:bg-green-100 dark:lg:bg-yellow-900/30 dark:md:bg-blue-900/30 dark:sm:bg-green-900/30">
          <text class="text-3.5 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            响应式背景色
          </text>
        </view>
        <view class="grid grid-cols-1 gap-3 lg:grid-cols-4 md:grid-cols-3 sm:grid-cols-2">
          <view
            v-for="n in 8"
            :key="n"
            class="rounded bg-purple-100 p-3 text-center text-3 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300"
          >
            项目 {{ n }}
          </view>
        </view>
        <view class="mt-4 rounded bg-gray-100 p-2 text-2.5 text-gray-700 leading-relaxed font-mono dark:bg-[var(--wot-dark-background3)] dark:text-[var(--wot-dark-color2)]" @click="copyCode('grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4')">
          grid-cols-1 sm:grid-cols-2\n
          md:grid-cols-3 lg:grid-cols-4
        </view>
      </view>
    </demo-block>

    <!-- 实用工具类 -->
    <demo-block title="实用工具类" transparent>
      <view class="space-y-4">
        <!-- 显示隐藏 -->
        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            显示/隐藏
          </view>
          <view class="mb-3 flex flex-wrap gap-2">
            <view class="rounded bg-green-100 px-3 py-2 text-3 text-green-800">
              显示 (block)
            </view>
            <view class="rounded bg-blue-100 px-3 py-2 text-3 text-blue-800">
              内联 (inline)
            </view>
            <view class="rounded bg-purple-100 px-3 py-2 text-3 text-purple-800">
              弹性 (flex)
            </view>
          </view>
          <view class="rounded bg-gray-100 p-2 text-2.5 text-gray-700 font-mono dark:bg-[var(--wot-dark-background3)] dark:text-[var(--wot-dark-color2)]" @click="copyCode('block inline flex hidden')">
            block inline flex hidden
          </view>
        </view>

        <!-- 定位 -->
        <view class="rounded-2 bg-white p-4 dark:bg-[var(--wot-dark-background2)]">
          <view class="mb-3 text-4 text-gray-800 font-bold dark:text-[var(--wot-dark-color)]">
            定位系统
          </view>
          <view class="relative h-24 rounded-2 bg-gray-100 dark:bg-[var(--wot-dark-background3)]">
            <view class="absolute left-2 top-2 rounded bg-red-500 px-2 py-1 text-2.5 text-white">
              top-2 left-2
            </view>
            <view class="absolute right-2 top-2 rounded bg-blue-500 px-2 py-1 text-2.5 text-white">
              top-2 right-2
            </view>
            <view class="absolute bottom-2 left-2 rounded bg-green-500 px-2 py-1 text-2.5 text-white">
              bottom-2 left-2
            </view>
            <view class="absolute bottom-2 right-2 rounded bg-purple-500 px-2 py-1 text-2.5 text-white">
              bottom-2 right-2
            </view>
          </view>
          <view class="mt-3 rounded bg-gray-100 p-2 text-2.5 text-gray-700 font-mono dark:bg-[var(--wot-dark-background3)] dark:text-[var(--wot-dark-color2)]" @click="copyCode('absolute relative top-2 left-2 right-2 bottom-2')">
            absolute relative top-2 left-2 right-2 bottom-2
          </view>
        </view>
      </view>
    </demo-block>

    <!-- 相关链接 -->
    <demo-block title="相关链接" transparent>
      <wd-cell-group border custom-class="rounded-2! overflow-hidden">
        <wd-cell title="📚 UnoCSS 官方文档" value="unocss.dev" is-link @click="handleNavigate('https://unocss.dev/')" />
        <wd-cell title="🐙 GitHub 仓库" value="unocss/unocss" is-link @click="handleNavigate('https://github.com/unocss/unocss')" />
        <wd-cell title="🎮 在线演练场" value="在线体验" is-link @click="handleNavigate('https://unocss.dev/play/')" />
        <wd-cell title="📖 Tailwind CSS" value="参考文档" is-link @click="handleNavigate('https://tailwindcss.com/docs')" />
        <wd-cell title="💡 最佳实践" value="使用指南" is-link @click="handleNavigate('https://unocss.dev/guide/')" />
      </wd-cell-group>
    </demo-block>
  </view>
</template>
