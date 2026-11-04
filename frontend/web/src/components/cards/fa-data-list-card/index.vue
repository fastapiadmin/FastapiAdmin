<!-- 数据列表卡片 -->
<template>
  <div class="fa-card p-5 overflow-hidden" :class="autoHeight ? 'h-auto' : 'h-110'">
    <div class="pb-3.5">
      <p class="text-lg font-medium truncate" :title="title">{{ title }}</p>
      <p class="text-sm text-g-600 truncate" :title="subtitle">{{ subtitle }}</p>
    </div>
    <ElScrollbar :style="{ height: maxHeight }">
      <div v-for="item in list" :key="item.title" class="flex items-center py-2">
        <div
          v-if="item.icon"
          class="flex items-center justify-center mr-3 size-10 rounded-lg"
          :class="item.class"
        >
          <FaSvgIcon :icon="item.icon" class="text-xl" />
        </div>
        <div class="min-w-0 flex-1">
          <div class="mb-1 text-sm truncate" :title="item.title">{{ item.title }}</div>
          <div class="text-xs text-g-500 truncate">{{ item.status }}</div>
        </div>
        <div class="ml-3 shrink-0 text-xs text-g-500">{{ item.time }}</div>
      </div>
    </ElScrollbar>
    <ElButton class="mt-6.25 w-full text-center" v-if="showMoreButton" v-ripple @click="handleMore">
      查看更多
    </ElButton>
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: "FaDataListCard" });

interface Props {
  /** 数据列表 */
  list: Activity[];
  /** 标题 */
  title: string;
  /** 副标题 */
  subtitle?: string;
  /** 最大显示数量 */
  maxCount?: number;
  /** 是否显示更多按钮 */
  showMoreButton?: boolean;
  /** 高度随内容自适应 */
  autoHeight?: boolean;
}

interface Activity {
  /** 标题 */
  title: string;
  /** 状态 */
  status: string;
  /** 时间 */
  time: string;
  /** 样式类名 */
  class: string;
  /** 图标 */
  icon: string;
}

const ITEM_HEIGHT = 70;
const DEFAULT_MAX_COUNT = 5;

const props = withDefaults(defineProps<Props>(), {
  maxCount: DEFAULT_MAX_COUNT,
});

const maxHeight = computed(() => `${ITEM_HEIGHT * props.maxCount}px`);

interface Emits {
  /** 点击更多按钮事件 */
  more: [];
}

const emit = defineEmits<Emits>();

const handleMore = () => emit("more");
</script>
