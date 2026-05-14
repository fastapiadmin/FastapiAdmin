<template>
  <ElRow :gutter="16" class="flex card-row">
    <ElCol v-for="(item, index) in dataList" :key="index" :sm="12" :md="8" :lg="8">
      <div class="fa-card relative flex flex-col justify-center h-30 px-5">
        <!-- 顶部标题行 -->
        <div class="flex items-center justify-between">
          <span class="text-sm text-g-600">{{ item.des }}</span>
          <ElTag v-if="item.tag" :type="item.tagType || 'danger'" size="small">
            {{ item.tag }}
          </ElTag>
        </div>

        <!-- 数字 + 侧边图标 -->
        <div class="flex items-center justify-between mt-2">
          <div class="flex items-center gap-2">
            <!-- 丰富卡片用 useTransition 模拟动画 -->
            <span v-if="item.animatedCount" class="text-lg font-medium">
              {{ item.animatedCount }}
            </span>
            <!-- 简单卡片用 FaCountTo -->
            <FaCountTo v-else class="text-lg font-medium" :target="item.num" :duration="1300" />
            <span v-if="item.status" class="text-xs" :class="item.statusColor || 'text-success'">
              <ElIcon v-if="item.statusIcon"><component :is="item.statusIcon" /></ElIcon>
              {{ item.status }}
            </span>
          </div>
          <div
            v-if="item.icon"
            class="size-10 rounded-xl flex-cc"
            :class="item.iconBg || 'bg-theme/10'"
          >
            <FaSvgIcon
              :icon="item.icon"
              class="text-xl"
              :class="[
                item.iconColor || 'text-theme',
                item.animateIcon ? 'animate-[pulse_2s_infinite]' : '',
              ]"
            />
          </div>
        </div>

        <!-- 底部行：变化率 + 更新时间 -->
        <div class="flex items-center justify-between mt-1 text-xs text-g-600">
          <span>
            <template v-if="item.change !== undefined">
              较上周
              <span :class="item.change.indexOf('+') === 0 ? 'text-success' : 'text-danger'">
                {{ item.change }}
              </span>
            </template>
            <template v-else-if="item.totalLabel">
              {{ item.totalLabel }}：{{ item.totalValue }}
            </template>
          </span>
          <span v-if="item.updateTime">{{ item.updateTime }}</span>
        </div>
      </div>
    </ElCol>
  </ElRow>
</template>

<script setup lang="ts">
import { ref, onMounted, markRaw, type Component } from "vue";
import { useTransition } from "@vueuse/core";
import { Connection } from "@element-plus/icons-vue";
import { computed } from "vue";

interface CardDataItem {
  des: string;
  icon: string;
  iconBg?: string;
  iconColor?: string;
  animateIcon?: boolean;
  num: number;
  change?: string;
  rich?: boolean;
  tag?: string;
  tagType?: "danger" | "success" | "warning" | "info";
  status?: string;
  statusColor?: string;
  statusIcon?: Component;
  totalLabel?: string;
  totalValue?: number | string;
  updateTime?: string;
  // 动画计数
  animatedCount?: number;
}

// 模拟访客数据（原来首页统计卡片的数据）
const visitStats = ref({
  todayUvCount: Math.floor(Math.random() * 200) + 50,
  uvGrowthRate: parseFloat((Math.random() * 20 - 10).toFixed(2)),
  totalUvCount: Math.floor(Math.random() * 5000) + 1000,
  todayPvCount: Math.floor(Math.random() * 500) + 100,
  pvGrowthRate: parseFloat((Math.random() * 20 - 10).toFixed(2)),
  totalPvCount: Math.floor(Math.random() * 20000) + 5000,
});

const transitionUvCount = useTransition(
  computed(() => visitStats.value.todayUvCount),
  {
    duration: 1000,
    transition: [0.25, 0.1, 0.25, 1.0],
  }
);
const transitionPvCount = useTransition(
  computed(() => visitStats.value.todayPvCount),
  {
    duration: 1000,
    transition: [0.25, 0.1, 0.25, 1.0],
  }
);

const dataList = ref<CardDataItem[]>([
  {
    des: "在线用户",
    icon: "ri:group-line",
    iconBg: "bg-danger/10",
    iconColor: "text-danger",
    animateIcon: true,
    num: 9999,
    rich: true,
    tag: "实时",
    tagType: "danger",
    status: "已连接",
    statusColor: "text-success",
    statusIcon: markRaw(Connection),
    updateTime: "2025-07-12 00:00:00",
  },
  {
    des: "访客数(UV)",
    icon: "ri:bar-chart-grouped-line",
    iconBg: "bg-success/10",
    iconColor: "text-success",
    num: 0,
    rich: true,
    animatedCount: 0,
    totalLabel: "总访客数",
    totalValue: 0,
  },
  {
    des: "浏览量(PV)",
    icon: "ri:eye-line",
    iconBg: "bg-primary/10",
    iconColor: "text-primary",
    num: 0,
    rich: true,
    animatedCount: 0,
    totalLabel: "总浏览量",
    totalValue: 0,
  },
  {
    des: "总访问次数",
    icon: "ri:pie-chart-line",
    num: 9120,
    change: "+20%",
  },
  {
    des: "点击量",
    icon: "ri:fire-line",
    num: 9520,
    change: "-12%",
  },
  {
    des: "新用户",
    icon: "ri:progress-2-line",
    num: 156,
    change: "+30%",
  },
]);

onMounted(() => {
  // 更新 UV/PV 动态数据
  dataList.value[1].animatedCount = Math.round(transitionUvCount.value);
  dataList.value[1].totalValue = visitStats.value.totalUvCount;
  dataList.value[2].animatedCount = Math.round(transitionPvCount.value);
  dataList.value[2].totalValue = visitStats.value.totalPvCount;

  // 生成增长率显示
  const uvRate = visitStats.value.uvGrowthRate;
  const pvRate = visitStats.value.pvGrowthRate;
  dataList.value[1].change = uvRate > 0 ? `+${uvRate}%` : `${uvRate}%`;
  dataList.value[2].change = pvRate > 0 ? `+${pvRate}%` : `${pvRate}%`;
});
</script>

<style scoped>
.card-row {
  row-gap: 16px;
}
</style>
