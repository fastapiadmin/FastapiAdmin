<script setup lang="ts">
import { useToast } from 'wot-design-uni'

definePage({
  name: 'skills',
  layout: 'default',
  style: {
    navigationBarTitleText: 'Agent Skills',
    navigationBarBackgroundColor: '#f9fafb',
    navigationBarTextStyle: 'black',
  },
})

const toast = useToast()

const skills = [
  {
    name: 'alova-api-module',
    desc: '快速创建 Alova 请求模块和 Mock 数据',
    icon: 'swap',
    color: '#007AFF',
  },
  {
    name: 'global-feedback',
    desc: '全局反馈组件（Toast/Message/Loading）使用指南',
    icon: 'chat',
    color: '#34C759',
  },
  {
    name: 'pinia-store-generator',
    desc: '创建符合项目规范的 Pinia Store',
    icon: 'folder',
    color: '#FFCC00',
  },
  {
    name: 'uni-page-generator',
    desc: '基于项目规范快速生成 uni-app 页面',
    icon: 'file',
    color: '#FF9500',
  },
  {
    name: 'vue-composable-creator',
    desc: '快速创建 Vue 3 组合式函数',
    icon: 'setting',
    color: '#5856D6',
  },
  {
    name: 'wot-router-usage',
    desc: '@wot-ui/router 轻量级路由库使用指南',
    icon: 'location',
    color: '#FF2D55',
  },
]

function handleClick(skill: string) {
  toast.success(`已选择: ${skill}`)
}

function getIconBg(color: string) {
  // Simple hex to rgba with low opacity
  const r = Number.parseInt(color.slice(1, 3), 16)
  const g = Number.parseInt(color.slice(3, 5), 16)
  const b = Number.parseInt(color.slice(5, 7), 16)
  return `rgba(${r}, ${g}, ${b}, 0.1)`
}
</script>

<template>
  <view class="pb-safe box-border min-h-screen bg-[#f9fafb]">
    <!-- Header -->
    <view class="px-6 pb-6 pt-8">
      <view class="mb-2 text-3xl text-gray-900 font-bold leading-tight">
        Agent Skills
      </view>
      <view class="text-base text-gray-500 leading-relaxed">
        利用智能工具赋能开发效率，<br>打造极致开发体验。
      </view>
    </view>

    <!-- Content -->
    <view class="px-5 space-y-4">
      <view
        v-for="(skill, index) in skills"
        :key="skill.name"
        class="group relative animate-fade-in-up overflow-hidden rounded-[24px] bg-white p-5 shadow-sm transition-all duration-300 active:scale-[0.98]"
        :style="{ animationDelay: `${index * 100}ms` }"
        @click="handleClick(skill.name)"
      >
        <view class="flex items-start gap-4">
          <!-- Icon Container -->
          <view
            class="h-14 w-14 flex shrink-0 items-center justify-center rounded-[18px] transition-transform duration-300 group-active:scale-110"
            :style="{ backgroundColor: getIconBg(skill.color) }"
          >
            <wd-icon
              :name="skill.icon"
              size="28px"
              :color="skill.color"
              custom-style="display: block;"
            />
          </view>

          <!-- Text Content -->
          <view class="min-w-0 flex-1 pt-0.5">
            <view class="flex items-center justify-between">
              <view class="truncate pr-2 text-lg text-gray-900 font-bold">
                {{ skill.name }}
              </view>
              <wd-icon name="arrow-right" color="#E5E7EB" size="20px" />
            </view>
            <view class="line-clamp-2 mt-1 text-sm text-gray-500 leading-relaxed">
              {{ skill.desc }}
            </view>
          </view>
        </view>

        <!-- Decoration (optional glow or highlight) -->
        <view
          class="pointer-events-none absolute h-24 w-24 rounded-full opacity-[0.03] -bottom-4 -right-4"
          :style="{ backgroundColor: skill.color }"
        />
      </view>
    </view>

    <wd-toast />
  </view>
</template>

<style scoped>
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  opacity: 0; /* meaningful for delay */
  animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Utilities */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pb-safe {
  padding-bottom: constant(safe-area-inset-bottom);
  padding-bottom: env(safe-area-inset-bottom);
}
</style>
