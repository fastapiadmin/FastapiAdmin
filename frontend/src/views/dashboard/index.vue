<template>
  <div class="dashboard-container">
    <!-- github 角标 -->
    <GithubCorner class="github-corner" />

    <el-card shadow="hover">
      <div class="flex flex-wrap">
        <!-- 左侧问候语区域 -->
        <div class="flex-1 flex items-start">
          <img
            class="w80px h80px rounded-full"
            :src="userStore.basicInfo.avatar + '?imageView2/1/w/80/h/80'"
          />
          <div class="ml-5">
            <div class="text-20px font-bold mb-5px">
              {{ timefix }}{{ userStore.basicInfo.name }}，{{ welcome }}
            </div>
            <p class="text-sm text-gray">今日天气晴朗，气温在15℃至25℃之间，东南风。</p>
          </div>
        </div>

        <!-- 右侧图标区域 - PC端 -->
        <div class="hidden sm:block">
          <div class="flex items-end space-x-6">
            <!-- 文档 -->
            <div class="flex flex-col items-center">
              <div class="font-bold color-#4080ff text-sm flex items-center">
                <el-icon class="mr-2px"><Document /></el-icon>
                文档
              </div>
              <div class="mt-3 whitespace-nowrap">
                <el-link
                  href="https://blog.csdn.net/weixin_46768253/article/details/149569141?spm=1001.2014.3001.5502"
                  target="_blank"
                >
                  <div class="i-svg:csdn text-lg" />
                </el-link>
              </div>
            </div>
            <!-- 仓库 -->
            <div class="flex flex-col items-center">
              <div class="font-bold color-#ff9a2e text-sm flex items-center">
                <el-icon class="mr-2px">
                  <Folder />
                </el-icon>
                仓库
              </div>
              <div class="mt-3 whitespace-nowrap">
                <el-link href="https://gitee.com/fastapiadmin/FastapiAdmin" target="_blank">
                  <div class="i-svg:gitee text-lg color-#F76560" />
                </el-link>
                <el-divider direction="vertical" />
                <el-link href="https://github.com/fastapiadmin/FastapiAdmin" target="_blank">
                  <div class="i-svg:github text-lg color-#4080FF" />
                </el-link>
                <el-divider direction="vertical" />
                <el-link href="https://gitcode.com/qq_36002987/FastapiAdmin" target="_blank">
                  <div class="i-svg:gitcode text-lg color-#FF9A2E" />
                </el-link>
              </div>
            </div>
          </div>
        </div>

        <!-- 移动端图标区域 -->
        <div class="w-full sm:hidden mt-3">
          <div class="flex justify-end space-x-4 overflow-x-auto">
            <!-- 仓库图标 -->
            <el-link href="https://gitee.com/fastapiadmin/FastapiAdmin" target="_blank">
              <div class="i-svg:gitee text-lg color-#F76560" />
            </el-link>
            <el-divider direction="vertical" />
            <el-link href="https://github.com/fastapiadmin/FastapiAdmin" target="_blank">
              <div class="i-svg:github text-lg color-#4080FF" />
            </el-link>
            <el-divider direction="vertical" />
            <el-link href="https://gitcode.com/qq_36002987/FastapiAdmin" target="_blank">
              <div class="i-svg:gitcode text-lg color-#FF9A2E" />
            </el-link>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 数据统计 -->
    <el-row :gutter="10" class="mt-4">
      <!-- 在线用户数量 -->
      <el-col :span="8" :xs="24" class="mb-xs-3">
        <el-card shadow="hover" class="h-full flex flex-col">
          <template #header>
            <div class="flex-x-between">
              <span class="text-gray">在线用户</span>
              <el-tag type="danger" size="small">实时</el-tag>
            </div>
          </template>

          <div class="flex-x-between mt-2 flex-1">
            <div class="flex-y-center">
              <span class="text-lg transition-all duration-300 hover:scale-110">9999</span>
              <span v-if="true" class="ml-2 text-xs text-[#67c23a]">
                <el-icon>
                  <Connection />
                </el-icon>
                已连接
              </span>
              <span v-else class="ml-2 text-xs text-[#f56c6c]">
                <el-icon>
                  <Failed />
                </el-icon>
                未连接
              </span>
            </div>
            <div class="i-svg:people w-8 h-8 animate-[pulse_2s_infinite]" />
          </div>

          <div class="flex-x-between mt-2 text-sm text-gray">
            <span>更新时间</span>
            <span>2025-07-12 00:00:00</span>
          </div>
        </el-card>
      </el-col>

      <!-- 访客数(UV) -->
      <el-col :span="8" :xs="24" class="mb-xs-3">
        <el-skeleton :loading="visitStatsLoading" :rows="5" animated>
          <template #template>
            <el-card>
              <template #header>
                <div>
                  <el-skeleton-item variant="h3" style="width: 40%" />
                  <el-skeleton-item variant="rect" style="float: right; width: 1em; height: 1em" />
                </div>
              </template>

              <div class="flex-x-between">
                <el-skeleton-item variant="text" style="width: 30%" />
                <el-skeleton-item variant="circle" style="width: 2em; height: 2em" />
              </div>
              <div class="mt-5 flex-x-between">
                <el-skeleton-item variant="text" style="width: 50%" />
                <el-skeleton-item variant="text" style="width: 1em" />
              </div>
            </el-card>
          </template>
          <template v-if="!visitStatsLoading">
            <el-card shadow="hover" class="h-full flex flex-col">
              <template #header>
                <div class="flex-x-between">
                  <span class="text-gray">访客数(UV)</span>
                  <el-tag type="success" size="small">日</el-tag>
                </div>
              </template>

              <div class="flex-x-between mt-2 flex-1">
                <div class="flex-y-center">
                  <span class="text-lg">{{ Math.round(transitionUvCount) }}</span>
                  <span
                    :class="[
                      'text-xs',
                      'ml-2',
                      computeGrowthRateClass(visitStatsData.uvGrowthRate),
                    ]"
                  >
                    <el-icon>
                      <Top v-if="visitStatsData.uvGrowthRate > 0" />
                      <Bottom v-else-if="visitStatsData.uvGrowthRate < 0" />
                    </el-icon>
                    {{ formatGrowthRate(visitStatsData.uvGrowthRate) }}
                  </span>
                </div>
                <div class="i-svg:visitor w-8 h-8" />
              </div>

              <div class="flex-x-between mt-2 text-sm text-gray">
                <span>总访客数</span>
                <span>{{ Math.round(transitionTotalUvCount) }}</span>
              </div>
            </el-card>
          </template>
        </el-skeleton>
      </el-col>

      <!-- 浏览量(PV) -->
      <el-col :span="8" :xs="24">
        <el-skeleton :loading="visitStatsLoading" :rows="5" animated>
          <template #template>
            <el-card>
              <template #header>
                <div>
                  <el-skeleton-item variant="h3" style="width: 40%" />
                  <el-skeleton-item variant="rect" style="float: right; width: 1em; height: 1em" />
                </div>
              </template>

              <div class="flex-x-between">
                <el-skeleton-item variant="text" style="width: 30%" />
                <el-skeleton-item variant="circle" style="width: 2em; height: 2em" />
              </div>
              <div class="mt-5 flex-x-between">
                <el-skeleton-item variant="text" style="width: 50%" />
                <el-skeleton-item variant="text" style="width: 1em" />
              </div>
            </el-card>
          </template>
          <template v-if="!visitStatsLoading">
            <el-card shadow="hover" class="h-full flex flex-col">
              <template #header>
                <div class="flex-x-between">
                  <span class="text-gray">浏览量(PV)</span>
                  <el-tag type="primary" size="small">日</el-tag>
                </div>
              </template>

              <div class="flex-x-between mt-2 flex-1">
                <div class="flex-y-center">
                  <span class="text-lg">{{ Math.round(transitionPvCount) }}</span>
                  <span
                    :class="[
                      'text-xs',
                      'ml-2',
                      computeGrowthRateClass(visitStatsData.pvGrowthRate),
                    ]"
                  >
                    <el-icon>
                      <Top v-if="visitStatsData.pvGrowthRate > 0" />
                      <Bottom v-else-if="visitStatsData.pvGrowthRate < 0" />
                    </el-icon>
                    {{ formatGrowthRate(visitStatsData.pvGrowthRate) }}
                  </span>
                </div>
                <div class="i-svg:browser w-8 h-8" />
              </div>

              <div class="flex-x-between mt-2 text-sm text-gray">
                <span>总浏览量</span>
                <span>{{ Math.round(transitionTotalPvCount) }}</span>
              </div>
            </el-card>
          </template>
        </el-skeleton>
      </el-col>
    </el-row>

    <el-row :gutter="10" class="mt-4">
      <!-- 访问趋势统计图 -->
      <el-col :xs="24" :span="16">
        <el-card>
          <template #header>
            <div class="flex-x-between">
              <span>访问趋势</span>
              <el-radio-group v-model="visitTrendDateRange" size="small">
                <el-radio-button :value="7">近7天</el-radio-button>
                <el-radio-button :value="30">近30天</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <ECharts :options="visitTrendChartOptions" height="400px" />
        </el-card>
      </el-col>
      <!-- 最新动态 -->
      <el-col :xs="24" :span="8">
        <el-card>
          <template #header>
            <div class="flex-x-between">
              <span class="header-title">最新动态</span>
              <el-link
                type="primary"
                underline="never"
                href="https://gitee.com/fastapiadmin/FastapiAdmin/releases"
                target="_blank"
              >
                完整记录
                <el-icon class="link-icon">
                  <TopRight />
                </el-icon>
              </el-link>
            </div>
          </template>

          <el-scrollbar height="400px">
            <el-timeline class="p-3">
              <el-timeline-item
                v-for="(item, index) in vesionList"
                :key="index"
                :timestamp="item.date"
                placement="top"
                :color="index === 0 ? '#67C23A' : '#909399'"
                :hollow="index !== 0"
                size="large"
              >
                <div class="version-item" :class="{ 'latest-item': index === 0 }">
                  <div>
                    <el-text tag="strong">{{ item.title }}</el-text>
                    <el-tag v-if="item.tag" :type="index === 0 ? 'success' : 'info'" size="small">
                      {{ item.tag }}
                    </el-tag>
                  </div>

                  <el-text class="version-content">{{ item.content }}</el-text>

                  <div v-if="item.link">
                    <el-link
                      :type="index === 0 ? 'primary' : 'info'"
                      :href="item.link"
                      target="_blank"
                      underline="never"
                    >
                      详情
                      <el-icon class="link-icon">
                        <TopRight />
                      </el-icon>
                    </el-link>
                  </div>
                </div>
              </el-timeline-item>
            </el-timeline>
          </el-scrollbar>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "Home",
  inheritAttrs: false,
});

import { dayjs } from "element-plus";
import { useUserStore } from "@/store/modules/user.store";
import { formatGrowthRate } from "@/utils";
import { useTransition } from "@vueuse/core";
import { Connection, Failed } from "@element-plus/icons-vue";
import { greetings } from "@/utils/common";

const timefix = greetings();
const welcome = "祝你开心每一天！";

interface VersionItem {
  id: string;
  title: string; // 版本标题（如：v2.4.0）
  date: string; // 发布时间
  content: string; // 版本描述
  link: string; // 详情链接
  tag?: string; // 版本标签（可选）
}

const userStore = useUserStore();

// 当前通知公告列表
const vesionList = ref<VersionItem[]>([
  {
    id: "1",
    title: "v3.2.1",
    date: dayjs().format("YYYY-MM-DD HH:mm:ss"),
    content: "优化性能，修复若干小bug。",
    link: "https://gitee.com/fastapiadmin/FastapiAdmin/releases",
    tag: "更新",
  },
  {
    id: "2",
    title: "v3.2.0",
    date: dayjs().subtract(1, "day").format("YYYY-MM-DD HH:mm:ss"),
    content: "新增用户行为分析功能。",
    link: "https://gitee.com/fastapiadmin/FastapiAdmin/releases",
    tag: "新功能",
  },
  {
    id: "3",
    title: "v3.1.0",
    date: dayjs().subtract(3, "day").format("YYYY-MM-DD HH:mm:ss"),
    content: "优化权限管理系统。",
    link: "https://gitee.com/fastapiadmin/FastapiAdmin/releases",
    tag: "优化",
  },
]);

// 访客统计数据加载状态
const visitStatsLoading = ref(true);
// 访客统计数据
const visitStatsData = ref({
  todayUvCount: 0,
  uvGrowthRate: 0,
  totalUvCount: 0,
  todayPvCount: 0,
  pvGrowthRate: 0,
  totalPvCount: 0,
});

// 数字过渡动画
const transitionUvCount = useTransition(
  computed(() => visitStatsData.value.todayUvCount),
  {
    duration: 1000,
    transition: [0.25, 0.1, 0.25, 1.0], // CSS cubic-bezier
  }
);

const transitionTotalUvCount = useTransition(
  computed(() => visitStatsData.value.totalUvCount),
  {
    duration: 1200,
    transition: [0.25, 0.1, 0.25, 1.0],
  }
);

const transitionPvCount = useTransition(
  computed(() => visitStatsData.value.todayPvCount),
  {
    duration: 1000,
    transition: [0.25, 0.1, 0.25, 1.0],
  }
);

const transitionTotalPvCount = useTransition(
  computed(() => visitStatsData.value.totalPvCount),
  {
    duration: 1200,
    transition: [0.25, 0.1, 0.25, 1.0],
  }
);

// 访问趋势日期范围（单位：天）
const visitTrendDateRange = ref(7);
// 访问趋势图表配置
const visitTrendChartOptions = ref();

/**
 * 更新访问趋势图表的配置项
 *
 * @param data - 访问趋势数据
 */
const updateVisitTrendChartOptions = () => {
  visitTrendChartOptions.value = {
    tooltip: {
      trigger: "axis",
    },
    legend: {
      data: ["浏览量(PV)", "访客数(UV)"],
      bottom: 0,
    },
    grid: {
      left: "1%",
      right: "5%",
      bottom: "10%",
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: Array.from({ length: visitTrendDateRange.value }, (_, index) =>
        dayjs()
          .subtract(visitTrendDateRange.value - index - 1, "day")
          .format("YYYY-MM-DD")
      ),
    },
    yAxis: {
      type: "value",
      splitLine: {
        show: true,
        lineStyle: {
          type: "dashed",
        },
      },
    },
    series: [
      {
        name: "浏览量(PV)",
        type: "line",
        data: Array.from(
          { length: visitTrendDateRange.value },
          () => Math.floor(Math.random() * 500) + 100
        ),
        areaStyle: {
          color: "rgba(64, 158, 255, 0.1)",
        },
        smooth: true,
        itemStyle: {
          color: "#4080FF",
        },
        lineStyle: {
          color: "#4080FF",
        },
      },
      {
        name: "访客数(UV)",
        type: "line",
        data: Array.from(
          { length: visitTrendDateRange.value },
          () => Math.floor(Math.random() * 200) + 50
        ),
        areaStyle: {
          color: "rgba(103, 194, 58, 0.1)",
        },
        smooth: true,
        itemStyle: {
          color: "#67C23A",
        },
        lineStyle: {
          color: "#67C23A",
        },
      },
    ],
  };
};

/**
 * 根据增长率计算对应的 CSS 类名
 *
 * @param growthRate - 增长率数值
 */
const computeGrowthRateClass = (growthRate?: number): string => {
  if (!growthRate) {
    return "text-[--el-color-info]";
  }
  if (growthRate > 0) {
    return "text-[--el-color-danger]";
  } else if (growthRate < 0) {
    return "text-[--el-color-success]";
  } else {
    return "text-[--el-color-info]";
  }
};

// 监听访问趋势日期范围的变化，重新获取趋势数据
watch(
  () => visitTrendDateRange.value,
  () => {
    updateVisitTrendChartOptions();
  },
  { immediate: true }
);

// 组件挂载后加载访客统计数据和通知公告数据
onMounted(() => {
  visitStatsLoading.value = false;
  visitStatsData.value = {
    todayUvCount: Math.floor(Math.random() * 200) + 50,
    uvGrowthRate: parseFloat((Math.random() * 20 - 10).toFixed(2)),
    totalUvCount: Math.floor(Math.random() * 5000) + 1000,
    todayPvCount: Math.floor(Math.random() * 500) + 100,
    pvGrowthRate: parseFloat((Math.random() * 20 - 10).toFixed(2)),
    totalPvCount: Math.floor(Math.random() * 20000) + 5000,
  };
  updateVisitTrendChartOptions();
});
</script>

<style lang="scss" scoped>
.dashboard-container {
  position: relative;
  padding: 16px;

  .github-corner {
    position: absolute;
    top: 0;
    right: 0;
    z-index: 1;
    border: 0;
  }

  .version-item {
    padding: 16px;
    margin-bottom: 12px;
    background: var(--el-fill-color-lighter);
    border-radius: 8px;
    transition: all 0.2s;

    &.latest-item {
      background: var(--el-color-primary-light-9);
      border: 1px solid var(--el-color-primary-light-5);
    }

    &:hover {
      transform: translateX(5px);
    }

    .version-content {
      margin-bottom: 12px;
      font-size: 13px;
      line-height: 1.5;
      color: var(--el-text-color-secondary);
    }
  }
}
</style>
