<!-- 时间轴列表卡片 -->
<template>
  <div class="fa-card p-5 overflow-hidden" :class="autoHeight ? 'h-auto' : 'h-110'">
    <div class="pb-3.5">
      <p class="text-lg font-medium truncate" :title="title">{{ title }}</p>
      <p class="text-sm text-g-600 truncate" :title="subtitle">{{ subtitle }}</p>
    </div>
    <ElScrollbar :style="{ height: maxHeight }">
      <ElTimeline class="pl-0.5!">
        <ElTimelineItem
          v-for="item in list"
          :key="item.time"
          :timestamp="item.time"
          :placement="TIMELINE_PLACEMENT"
          :color="item.status"
          :center="true"
        >
          <div class="flex items-center gap-3">
            <div class="flex items-center gap-2">
              <span class="min-w-0 text-sm break-words">{{ item.content }}</span>
              <span v-if="item.code" class="text-sm text-theme">#{{ item.code }}</span>
            </div>
          </div>
        </ElTimelineItem>
      </ElTimeline>
    </ElScrollbar>
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: "FaTimelineListCard" });

// 常量配置
const ITEM_HEIGHT = 64;
const TIMELINE_PLACEMENT = "top";
const DEFAULT_MAX_COUNT = 5;

interface TimelineItem {
  /** 时间 */
  time: string;
  /** 状态颜色 */
  status: string;
  /** 内容 */
  content: string;
  /** 代码标识 */
  code?: string;
}

interface Props {
  /** 时间轴列表数据 */
  list: TimelineItem[];
  /** 标题 */
  title?: string;
  /** 副标题 */
  subtitle?: string;
  /** 最大显示数量 */
  maxCount?: number;
  /** 高度随内容自适应 */
  autoHeight?: boolean;
}

// Props 定义和验证
const props = withDefaults(defineProps<Props>(), {
  autoHeight: false,
  title: "",
  subtitle: "",
  maxCount: DEFAULT_MAX_COUNT,
});

// 计算最大高度
const maxHeight = computed(() => `${ITEM_HEIGHT * props.maxCount}px`);
</script>
