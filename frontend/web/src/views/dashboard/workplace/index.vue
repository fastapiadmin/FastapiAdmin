<template>
  <div class="dashboard-container">
    <!-- github 角标 -->
    <FaGithubCorner class="github-corner" />

    <ElCard shadow="hover">
      <div class="flex flex-wrap items-center gap-y-3">
        <!-- 左侧问候语区域 -->
        <div class="flex min-w-0 flex-1 items-center">
          <div class="size-20 shrink-0 rounded-full bg-g-100 flex items-center justify-center">
            <ElAvatar
              v-if="userStore.basicInfo.avatar"
              size="large"
              :src="userStore.basicInfo.avatar"
              class="workplace-hero__avatar"
            />
            <ElIcon v-else :size="40" class="text-g-600">
              <UserFilled />
            </ElIcon>
          </div>
          <div class="ml-5">
            <div class="mb-[5px] text-[20px] font-bold">
              {{ timefix }}{{ userStore.basicInfo.name }}，{{ welcome }}
            </div>
            <p class="text-sm text-g-600">今日天气晴朗，气温在15℃至25℃之间，东南风。</p>
          </div>
        </div>

        <!-- 右侧图标区域 - PC端 -->
        <div class="hidden shrink-0 sm:block">
          <div class="flex items-center space-x-6">
            <!-- 文档 -->
            <div class="flex flex-col items-center">
              <div class="flex items-center text-sm font-bold text-[#4080ff]">
                <ElIcon class="mr-0.5"><Document /></ElIcon>
                文档
              </div>
              <div class="mt-3 whitespace-nowrap">
                <ElLink
                  href="https://blog.csdn.net/weixin_46768253/article/details/149569141?spm=1001.2014.3001.5502"
                  target="_blank"
                >
                  <FaSvgIcon :icon="resolveIconForFaSvgIcon('csdn')" class="text-lg" />
                </ElLink>
              </div>
            </div>
            <!-- 仓库 -->
            <div class="flex flex-col items-center">
              <div class="flex items-center text-sm font-bold text-[#ff9a2e]">
                <ElIcon class="mr-0.5">
                  <Folder />
                </ElIcon>
                仓库
              </div>
              <div class="mt-3 whitespace-nowrap">
                <ElLink href="https://gitee.com/fastapiadmin/FastapiAdmin" target="_blank">
                  <FaSvgIcon
                    :icon="resolveIconForFaSvgIcon('gitee')"
                    class="text-lg text-[#F76560]"
                  />
                </ElLink>
                <ElDivider direction="vertical" />
                <ElLink href="https://github.com/fastapiadmin/FastapiAdmin" target="_blank">
                  <FaSvgIcon
                    :icon="resolveIconForFaSvgIcon('github')"
                    class="text-lg text-[#4080FF]"
                  />
                </ElLink>
                <ElDivider direction="vertical" />
                <ElLink href="https://gitcode.com/qq_36002987/FastapiAdmin" target="_blank">
                  <FaSvgIcon
                    :icon="resolveIconForFaSvgIcon('gitcode')"
                    class="text-lg text-[#FF9A2E]"
                  />
                </ElLink>
              </div>
            </div>
          </div>
        </div>

        <!-- 移动端图标区域 -->
        <div class="w-full sm:hidden">
          <div class="flex justify-end space-x-4 overflow-x-auto">
            <!-- 仓库图标 -->
            <ElLink href="https://gitee.com/fastapiadmin/FastapiAdmin" target="_blank">
              <FaSvgIcon :icon="resolveIconForFaSvgIcon('gitee')" class="text-lg text-[#F76560]" />
            </ElLink>
            <ElDivider direction="vertical" />
            <ElLink href="https://github.com/fastapiadmin/FastapiAdmin" target="_blank">
              <FaSvgIcon :icon="resolveIconForFaSvgIcon('github')" class="text-lg text-[#4080FF]" />
            </ElLink>
            <ElDivider direction="vertical" />
            <ElLink href="https://gitcode.com/qq_36002987/FastapiAdmin" target="_blank">
              <FaSvgIcon
                :icon="resolveIconForFaSvgIcon('gitcode')"
                class="text-lg text-[#FF9A2E]"
              />
            </ElLink>
          </div>
        </div>
      </div>
    </ElCard>

    <!-- 数据统计 -->
    <ElRow :gutter="16" class="mt-4">
      <!-- 在线用户数量 -->
      <ElCol :span="8" :xs="24" class="mb-3 sm:mb-0">
        <ElCard shadow="hover" class="h-full flex flex-col">
          <template #header>
            <div class="flex items-center justify-between">
              <span class="text-g-600">在线用户</span>
              <ElTag type="danger" size="small">实时</ElTag>
            </div>
          </template>

          <div class="flex items-center justify-between mt-2 flex-1">
            <div class="flex items-center">
              <span class="text-lg transition-all duration-300 hover:scale-110">9999</span>
              <span v-if="true" class="ml-2 text-xs text-success">
                <ElIcon>
                  <Connection />
                </ElIcon>
                已连接
              </span>
              <span v-else class="ml-2 text-xs text-danger">
                <ElIcon>
                  <Failed />
                </ElIcon>
                未连接
              </span>
            </div>
            <FaSvgIcon
              :icon="resolveIconForFaSvgIcon('people')"
              class="size-8 animate-[pulse_2s_infinite]"
            />
          </div>

          <div class="flex items-center justify-between mt-2 text-sm text-g-600">
            <span>更新时间</span>
            <span>2025-07-12 00:00:00</span>
          </div>
        </ElCard>
      </ElCol>

      <!-- 访客数(UV) -->
      <ElCol :span="8" :xs="24" class="mb-3 sm:mb-0">
        <ElSkeleton :loading="visitStatsLoading" :rows="5" animated>
          <template #template>
            <ElCard>
              <template #header>
                <div>
                  <ElSkeletonItem variant="h3" style="width: 40%" />
                  <ElSkeletonItem variant="rect" style="float: right; width: 1em; height: 1em" />
                </div>
              </template>

              <div class="flex items-center justify-between">
                <ElSkeletonItem variant="text" style="width: 30%" />
                <ElSkeletonItem variant="circle" style="width: 2em; height: 2em" />
              </div>
              <div class="mt-5 flex items-center justify-between">
                <ElSkeletonItem variant="text" style="width: 50%" />
                <ElSkeletonItem variant="text" style="width: 1em" />
              </div>
            </ElCard>
          </template>
          <template v-if="!visitStatsLoading">
            <ElCard shadow="hover" class="h-full flex flex-col">
              <template #header>
                <div class="flex items-center justify-between">
                  <span class="text-g-600">访客数(UV)</span>
                  <ElTag type="success" size="small">日</ElTag>
                </div>
              </template>

              <div class="flex items-center justify-between mt-2 flex-1">
                <div class="flex items-center">
                  <span class="text-lg">{{ Math.round(transitionUvCount) }}</span>
                  <span
                    :class="[
                      'text-xs',
                      'ml-2',
                      computeGrowthRateClass(visitStatsData.uvGrowthRate),
                    ]"
                  >
                    <ElIcon>
                      <Top v-if="visitStatsData.uvGrowthRate > 0" />
                      <Bottom v-else-if="visitStatsData.uvGrowthRate < 0" />
                    </ElIcon>
                    {{ formatGrowthRate(visitStatsData.uvGrowthRate) }}
                  </span>
                </div>
                <FaSvgIcon :icon="resolveIconForFaSvgIcon('visitor')" class="size-8" />
              </div>

              <div class="flex items-center justify-between mt-2 text-sm text-g-600">
                <span>总访客数</span>
                <span>{{ Math.round(transitionTotalUvCount) }}</span>
              </div>
            </ElCard>
          </template>
        </ElSkeleton>
      </ElCol>

      <!-- 浏览量(PV) -->
      <ElCol :span="8" :xs="24">
        <ElSkeleton :loading="visitStatsLoading" :rows="5" animated>
          <template #template>
            <ElCard>
              <template #header>
                <div>
                  <ElSkeletonItem variant="h3" style="width: 40%" />
                  <ElSkeletonItem variant="rect" style="float: right; width: 1em; height: 1em" />
                </div>
              </template>

              <div class="flex items-center justify-between">
                <ElSkeletonItem variant="text" style="width: 30%" />
                <ElSkeletonItem variant="circle" style="width: 2em; height: 2em" />
              </div>
              <div class="mt-5 flex items-center justify-between">
                <ElSkeletonItem variant="text" style="width: 50%" />
                <ElSkeletonItem variant="text" style="width: 1em" />
              </div>
            </ElCard>
          </template>
          <template v-if="!visitStatsLoading">
            <ElCard shadow="hover" class="h-full flex flex-col">
              <template #header>
                <div class="flex items-center justify-between">
                  <span class="text-g-600">浏览量(PV)</span>
                  <ElTag type="primary" size="small">日</ElTag>
                </div>
              </template>

              <div class="flex items-center justify-between mt-2 flex-1">
                <div class="flex items-center">
                  <span class="text-lg">{{ Math.round(transitionPvCount) }}</span>
                  <span
                    :class="[
                      'text-xs',
                      'ml-2',
                      computeGrowthRateClass(visitStatsData.pvGrowthRate),
                    ]"
                  >
                    <ElIcon>
                      <Top v-if="visitStatsData.pvGrowthRate > 0" />
                      <Bottom v-else-if="visitStatsData.pvGrowthRate < 0" />
                    </ElIcon>
                    {{ formatGrowthRate(visitStatsData.pvGrowthRate) }}
                  </span>
                </div>
                <FaSvgIcon :icon="resolveIconForFaSvgIcon('browser')" class="size-8" />
              </div>

              <div class="flex items-center justify-between mt-2 text-sm text-g-600">
                <span>总浏览量</span>
                <span>{{ Math.round(transitionTotalPvCount) }}</span>
              </div>
            </ElCard>
          </template>
        </ElSkeleton>
      </ElCol>
    </ElRow>

    <ElRow :gutter="16" class="mt-4">
      <!-- 访问趋势统计图 -->
      <ElCol :xs="24" :span="16">
        <ElCard>
          <template #header>
            <div class="flex items-center justify-between">
              <span>访问趋势</span>
              <ElRadioGroup v-model="visitTrendDateRange" size="small">
                <ElRadioButton :value="7">近7天</ElRadioButton>
                <ElRadioButton :value="30">近30天</ElRadioButton>
              </ElRadioGroup>
            </div>
          </template>
          <ECharts :options="visitTrendChartOptions" height="calc(100vh - 550px)" />
        </ElCard>
      </ElCol>
      <!-- 最新动态 -->
      <ElCol :xs="24" :span="8">
        <ElCard>
          <template #header>
            <div class="flex items-center justify-between">
              <span class="header-title">最新动态</span>
              <ElLink
                type="primary"
                underline="never"
                href="https://gitee.com/fastapiadmin/FastapiAdmin/releases"
                target="_blank"
              >
                完整记录
                <ElIcon class="link-icon">
                  <TopRight />
                </ElIcon>
              </ElLink>
            </div>
          </template>

          <ElScrollbar height="calc(100vh - 550px)">
            <ElTimeline class="p-2">
              <ElTimelineItem
                v-for="(item, index) in vesionList"
                :key="index"
                :timestamp="item.date"
                placement="top"
                :color="index === 0 ? '#67C23A' : '#909399'"
                :hollow="index !== 0"
              >
                <div class="version-item" :class="{ 'latest-item': index === 0 }">
                  <div class="flex items-center justify-between">
                    <ElText tag="strong">{{ item.title }}</ElText>
                    <ElTag v-if="item.tag" :type="index === 0 ? 'success' : 'info'" size="small">
                      {{ item.tag }}
                    </ElTag>
                  </div>

                  <ElText class="version-content">{{ item.content }}</ElText>

                  <div v-if="item.link">
                    <ElLink
                      :type="index === 0 ? 'primary' : 'info'"
                      :href="item.link"
                      target="_blank"
                      underline="never"
                    >
                      详情
                      <ElIcon class="link-icon">
                        <TopRight />
                      </ElIcon>
                    </ElLink>
                  </div>
                </div>
              </ElTimelineItem>
            </ElTimeline>
          </ElScrollbar>
        </ElCard>
      </ElCol>
    </ElRow>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "Workplace",
  inheritAttrs: false,
});

import { dayjs } from "element-plus";
import { useUserStore } from "@stores/modules/user.store";
import { formatGrowthRate } from "@utils";
import { useTransition } from "@vueuse/core";
import {
  Bottom,
  Connection,
  Document,
  Failed,
  Folder,
  Top,
  TopRight,
  UserFilled,
} from "@element-plus/icons-vue";
import FaSvgIcon from "@/components/base/fa-svg-icon/index.vue";
import { greetings } from "@utils/common";
import { resolveIconForFaSvgIcon } from "@utils/menuIcon/remix";

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

  .github-corner {
    position: absolute;
    top: 0;
    right: 0;
    z-index: 1;
    border: 0;
  }

  .version-item {
    padding: 10px 12px;
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
      display: block;
      margin-top: 6px;
      margin-bottom: 8px;
      font-size: 13px;
      line-height: 1.4;
      color: var(--el-text-color-secondary);
    }
  }
}
</style>
