<script lang="ts" setup>
const props = defineProps({
  // 标题
  title: {
    type: String,
    default: '',
  },
  // 自定义类名
  customClass: {
    type: String,
    default: '',
  },
  // 垂直间距
  ver: {
    type: [Number, String],
    default: 10,
  },
  // 水平间距
  hor: {
    type: [Number, String],
    default: 15,
  },
  // 是否透明
  transparent: {
    type: Boolean,
    default: false,
  },
})

const style = computed(() => {
  return `margin: 0 ${props.hor}px;padding:${props.ver}px 0;`
})
</script>

<script lang="ts">
export default {
  options: {
    addGlobalClass: true,
    virtualHost: true,
    styleIsolation: 'shared',
  },
}
</script>

<template>
  <view
    class="mb-3 box-border w-full px-3 text-gray-500 last:mb-0 dark:text-gray-300"
    :class="[
      transparent ? '' : 'bg-white dark:bg-[var(--wot-dark-background2)]',
      customClass,
    ]"
  >
    <view class="px-4 py-3 text-26rpx">
      {{ title }}
    </view>
    <view :style="transparent ? '' : style">
      <slot />
    </view>
  </view>
</template>
