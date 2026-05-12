<!-- 分析页：业务图表模块 + 图表组件演示 -->
<template>
  <div>
    <ElRow :gutter="20">
      <ElCol :xl="14" :lg="15" :xs="24">
        <TodaySales />
      </ElCol>
      <ElCol :xl="10" :lg="9" :xs="24">
        <VisitorInsights />
      </ElCol>
    </ElRow>

    <ElRow :gutter="20">
      <ElCol :xl="10" :lg="10" :xs="24">
        <TotalRevenue />
      </ElCol>
      <ElCol :xl="7" :lg="7" :xs="24">
        <CustomerSatisfaction />
      </ElCol>
      <ElCol :xl="7" :lg="7" :xs="24">
        <TargetVsReality />
      </ElCol>
    </ElRow>

    <ElRow :gutter="20">
      <ElCol :xl="10" :lg="10" :xs="24">
        <TopProducts />
      </ElCol>
      <ElCol :xl="7" :lg="7" :xs="24">
        <SalesMappingByCountry />
      </ElCol>
      <ElCol :xl="7" :lg="7" :xs="24">
        <VolumeServiceLevel />
      </ElCol>
    </ElRow>

    <ElRow :gutter="20">
      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5">
            <span class="text-base font-medium">柱状图（单数据）</span>
          </div>
          <FaBarChart
            :data="singleBarData"
            :xAxisData="xAxisData"
            :showLegend="true"
            legendPosition="right"
          />
        </div>
      </ElCol>
      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5">
            <span class="text-base font-medium">柱状图（多组数据）</span>
          </div>
          <FaBarChart
            :data="multiBarData"
            :xAxisData="xAxisData"
            :showLegend="true"
            barWidth="26%"
          />
        </div>
      </ElCol>
      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5">
            <span class="text-base font-medium">柱状图（堆叠）</span>
          </div>
          <FaBarChart
            :data="stackBarData"
            :xAxisData="stackXAxisData"
            :showLegend="true"
            :stack="true"
            barWidth="26%"
          />
        </div>
      </ElCol>
      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5">
            <span class="text-base font-medium">折线图</span>
          </div>
          <FaLineChart
            :data="[58, 15, 82, 35, 120, 62, 45]"
            :xAxisData="['一月', '二月', '三月', '四月', '五月', '六月', '七月']"
            symbol="none"
            :symbolSize="7"
          />
        </div>
      </ElCol>
      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5">
            <span class="text-base font-medium">折线图（渐变背景）</span>
          </div>
          <FaLineChart
            :data="[28, 45, 82, 35, 100, 32, 55]"
            :xAxisData="['一月', '二月', '三月', '四月', '五月', '六月', '七月']"
            :showAreaColor="true"
          />
        </div>
      </ElCol>
      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5">
            <span class="text-base font-medium">折线图（多组数据）</span>
          </div>
          <FaLineChart
            :data="multiLineData"
            :xAxisData="['1月', '2月', '3月', '4月', '5月', '6月']"
            :showLegend="true"
          />
        </div>
      </ElCol>

      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5">
            <span class="text-base font-medium">柱状图（水平）</span>
          </div>
          <FaHBarChart
            :data="[50, 80, 120, 90, 60]"
            :xAxisData="['产品A', '产品B', '产品C', '产品D', '产品E']"
          />
        </div>
      </ElCol>
      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5">
            <span class="text-base font-medium">柱状图（水平）</span>
          </div>

          <FaHBarChart
            :data="[
              { name: '系列1', data: [10, 20, 30] },
              { name: '系列2', data: [15, 25, 35] },
            ]"
            :xAxisData="['类目1', '类目2', '类目3']"
            :showLegend="true"
            barWidth="30%"
          />
        </div>
      </ElCol>
      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5">
            <span class="text-base font-medium">柱状图（水平堆叠）</span>
          </div>
          <FaHBarChart
            :data="[
              { name: '系列1', data: [10, 20, 30] },
              { name: '系列2', data: [15, 25, 35] },
            ]"
            :xAxisData="['类目1', '类目2', '类目3']"
            :showLegend="true"
            :stack="true"
            barWidth="30%"
          />
        </div>
      </ElCol>

      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5">
            <span class="text-base font-medium">环形图</span>
          </div>
          <FaRingChart
            :data="[
              { value: 35, name: '分类A' },
              { value: 28, name: '分类B' },
              { value: 42, name: '分类C' },
            ]"
            :radius="['54%', '70%']"
            legendPosition="bottom"
          />
        </div>
      </ElCol>

      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5">
            <span class="text-base font-medium">环形图</span>
          </div>
          <FaRingChart
            :data="[
              { value: 35, name: '分类A' },
              { value: 28, name: '分类B' },
              { value: 42, name: '分类C' },
              { value: 32, name: '分类D' },
              { value: 26, name: '分类E' },
              { value: 37, name: '分类F' },
            ]"
            :radius="['54%', '70%']"
            :borderRadius="0"
            :showLegend="true"
            legendPosition="bottom"
            centerText="¥300,458"
          />
        </div>
      </ElCol>
      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5">
            <span class="text-base font-medium">饼图</span>
          </div>
          <FaRingChart
            :data="[
              { value: 30, name: '分类A' },
              { value: 25, name: '分类B' },
              { value: 45, name: '分类C' },
            ]"
            :radius="['0%', '70%']"
            :showLegend="true"
            legendPosition="right"
          />
        </div>
      </ElCol>
      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5">
            <span class="text-base font-medium">散点图</span>
          </div>
          <FaScatterChart
            :data="[
              { value: [1, 3] },
              { value: [2, 4] },
              { value: [3, 5] },
              { value: [4, 6] },
              { value: [5, 7] },
              { value: [6, 8] },
              { value: [7, 7] },
              { value: [8, 9] },
              { value: [9, 8] },
              { value: [10, 6] },
              { value: [11, 7] },
              { value: [12, 8] },
            ]"
          />
        </div>
      </ElCol>

      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5">
            <span class="text-base font-medium">雷达图</span>
          </div>
          <FaRadarChart
            :indicator="[
              { name: '销售', max: 100 },
              { name: '管理', max: 100 },
              { name: '技术', max: 100 },
              { name: '客服', max: 100 },
              { name: '开发', max: 100 },
            ]"
            :data="[
              {
                name: '预算分配',
                value: [80, 70, 90, 85, 75],
              },
              {
                name: '实际开销',
                value: [70, 75, 85, 80, 70],
              },
            ]"
          />
        </div>
      </ElCol>
      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5">
            <span class="text-base font-medium">k线图</span>
          </div>
          <FaKLineChart
            :data="[
              { time: '2024-01-01', open: 20, close: 23, high: 25, low: 18 },
              { time: '2024-01-02', open: 23, close: 21, high: 24, low: 20 },
              { time: '2024-01-03', open: 21, close: 25, high: 26, low: 21 },
            ]"
            :showDataZoom="false"
            :dataZoomStart="0"
            :dataZoomEnd="100"
          />
        </div>
      </ElCol>
      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5">
            <span class="text-base font-medium">双向堆叠柱状图</span>
          </div>
          <FaDualBarCompareChart
            :positiveData="[50, 28, 80, 65, 68, 70, 60, 55]"
            :negativeData="[50, 28, 40, 45, 38, 50, 42, 48]"
            :xAxisData="[
              '0-4岁',
              '5-14岁',
              '15-24岁',
              '25-34岁',
              '35-44岁',
              '45-54岁',
              '55-64岁',
              '65岁以上',
            ]"
            positiveName="男性年龄分布"
            negativeName="女性年龄分布"
          />
        </div>
      </ElCol>
    </ElRow>

    <div class="page-content" element-loading-text="加载中...">
      <FaMapChart />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { LineDataItem } from "@/types/component/chart";
import TodaySales from "./modules/today-sales.vue";
import VisitorInsights from "./modules/visitor-insights.vue";
import TotalRevenue from "./modules/total-revenue.vue";
import CustomerSatisfaction from "./modules/customer-satisfaction.vue";
import TargetVsReality from "./modules/target-vs-reality.vue";
import TopProducts from "./modules/top-products.vue";
import SalesMappingByCountry from "./modules/sales-mapping-by-country.vue";
import VolumeServiceLevel from "./modules/volume-service-level.vue";
import { defineAsyncComponent } from "vue";

defineOptions({ name: "Analysis" });

/**
 * 异步加载地图组件
 * 减少初始加载体积
 */
const FaMapChart = defineAsyncComponent(() => import("@/components/charts/fa-map-chart/index.vue"));

/**
 * 多组数据折线图示例数据
 */
const multiLineData: LineDataItem[] = [
  {
    name: "销售额",
    data: [120, 132, 101, 134, 90, 130],
    areaStyle: {
      startOpacity: 0.1,
      endOpacity: 0,
    },
  },
  {
    name: "利润",
    data: [80, 92, 71, 94, 60, 80],
    areaStyle: {
      startOpacity: 0.1,
      endOpacity: 0,
    },
  },
];

const singleBarData = ref([120, 200, 150, 80, 70, 110, 130]);
const xAxisData = ref(["周一", "周二", "周三", "周四", "周五", "周六", "周日"]);

const multiBarData = ref([
  { name: "销售额", data: [120, 200, 150, 80, 70, 110, 130] },
  { name: "利润", data: [20, 50, 30, 15, 10, 25, 35] },
]);

const stackBarData = ref([
  { name: "Q1", data: [20, 25, 30, 35, 40], stack: "total" },
  { name: "Q2", data: [30, 35, 40, 45, 50], stack: "total" },
]);

const stackXAxisData = ref(["产品A", "产品B", "产品C", "产品D", "产品E"]);
</script>

<style scoped>
@reference "@styles/core/tailwind.css";

.page-title {
  @apply my-5 text-xl font-medium first:mt-0;
}

.fa-card {
  @apply p-5;
}
</style>
