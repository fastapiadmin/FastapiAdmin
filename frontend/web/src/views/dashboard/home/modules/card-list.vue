<template>
  <ElRow :gutter="16">
    <ElCol v-for="item in dataList" :key="item.des" :sm="12" :md="8" :lg="8" class="mb-5">
      <div class="fa-card relative flex flex-col justify-center h-30 px-5">
        <div class="flex items-center justify-between">
          <span class="text-sm text-g-600">{{ item.des }}</span>
          <ElTag v-if="item.tag" :type="item.tagType || 'danger'" size="small">
            {{ item.tag }}
          </ElTag>
        </div>

        <div class="flex items-center justify-between mt-2">
          <div class="flex items-center gap-2">
            <span v-if="item.animatedCount" class="text-lg font-medium">
              {{ item.animatedCount }}
            </span>
            <FaCountTo v-else class="text-lg font-medium" :target="item.num" :duration="1300" />
            <span v-if="item.status" class="text-xs" :class="item.statusColor || 'text-success'">
              <ElIcon v-if="item.statusIcon"><component :is="item.statusIcon" /></ElIcon>
              {{ item.status }}
            </span>
          </div>
          <div
            v-if="item.icon"
            class="size-10 rounded-xl flex items-center justify-center"
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
import { Connection } from "@element-plus/icons-vue";
import { checkPerm } from "@/utils/checkPerm";
import DashboardAPI from "@/api/module_monitor/dashboard";
import type { DashboardStats } from "@/api/module_monitor/dashboard";

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
  animatedCount?: number;
}

const now = new Date();
const pad = (n: number) => String(n).padStart(2, "0");
const timeStr = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;

const dataList = ref<CardDataItem[]>([
  {
    des: "在线用户",
    icon: "ri:group-line",
    iconBg: "bg-danger/10",
    iconColor: "text-danger",
    animateIcon: true,
    num: 0,
    rich: true,
    tag: "实时",
    tagType: "danger",
    status: "已连接",
    statusColor: "text-success",
    statusIcon: markRaw(Connection),
    updateTime: timeStr,
  },
  {
    des: "注册用户",
    icon: "ri:bar-chart-grouped-line",
    iconBg: "bg-success/10",
    iconColor: "text-success",
    num: 0,
    rich: true,
    animatedCount: 0,
    totalLabel: "总用户",
    totalValue: 0,
  },
  {
    des: "今日登录",
    icon: "ri:eye-line",
    iconBg: "bg-primary/10",
    iconColor: "text-primary",
    num: 0,
    rich: true,
    animatedCount: 0,
    totalLabel: "唯一用户",
    totalValue: 0,
  },
]);

async function loadStats() {
  // 无权限则跳过 API 调用，避免 403 错误
  if (!checkPerm("module_monitor:dashboard:query")) return;

  try {
    const { data: res } = await DashboardAPI.getStats();
    const stats = res?.data as DashboardStats | undefined;
    if (!stats) return;

    const now2 = new Date();
    const ts = `${now2.getFullYear()}-${pad(now2.getMonth() + 1)}-${pad(now2.getDate())} ${pad(now2.getHours())}:${pad(now2.getMinutes())}:${pad(now2.getSeconds())}`;

    // 在线用户（第1个卡片）
    dataList.value[0]!.num = stats.online_users;
    dataList.value[0]!.updateTime = ts;

    // 注册用户（第2个卡片）
    dataList.value[1]!.num = stats.total_users;
    dataList.value[1]!.totalValue = `本周 +${stats.week_user_created}`;
    dataList.value[1]!.animatedCount = stats.total_users;

    // 今日登录（第3个卡片）
    dataList.value[2]!.num = stats.today_login_count;
    dataList.value[2]!.totalValue = stats.today_unique_users;
    dataList.value[2]!.animatedCount = stats.today_login_count;
  } catch {
    // 接口错误不影响页面渲染
  }
}

onMounted(() => {
  loadStats();
});
</script>

<style scoped>
.card-row {
  row-gap: 16px;
}
</style>
