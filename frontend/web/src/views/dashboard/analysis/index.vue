<template>
  <div>
    <!-- 业务分析模块 -->
    <ElRow :gutter="20">
      <ElCol :xl="14" :lg="15" :xs="24"><TodaySales /></ElCol>
      <ElCol :xl="10" :lg="9" :xs="24"><VisitorInsights /></ElCol>
    </ElRow>

    <ElRow :gutter="20">
      <ElCol :xl="10" :lg="10" :xs="24"><TotalRevenue /></ElCol>
      <ElCol :xl="7" :lg="7" :xs="24"><CustomerSatisfaction /></ElCol>
      <ElCol :xl="7" :lg="7" :xs="24"><TargetVsReality /></ElCol>
    </ElRow>

    <ElRow :gutter="20">
      <ElCol :xl="10" :lg="10" :xs="24"><TopProducts /></ElCol>
      <ElCol :xl="7" :lg="7" :xs="24"><SalesMappingByCountry /></ElCol>
      <ElCol :xl="7" :lg="7" :xs="24"><VolumeServiceLevel /></ElCol>
    </ElRow>

    <!-- 卡片组件演示区 ← workplace -->
    <div class="console-cards-showcase border-g-200 mt-4">
      <div class="py-5">
        <h2 class="page-title">统计卡片（文字）</h2>
        <ElRow :gutter="20">
          <ElCol
            v-for="card in statsCards"
            :key="`t-${card.id}`"
            :xs="24"
            :sm="12"
            :md="6"
            class="mb-5"
          >
            <FaStatsCard
              :icon="card.icon"
              :iconStyle="card.iconStyle"
              :title="card.title"
              :description="card.description"
              :showArrow="card.showArrow"
            />
          </ElCol>
        </ElRow>

        <h2 class="page-title">统计卡片（数字滚动）</h2>
        <ElRow :gutter="20">
          <ElCol
            v-for="card in statsCards"
            :key="`n-${card.id}`"
            :xs="24"
            :sm="12"
            :md="6"
            class="mb-5"
          >
            <FaStatsCard
              :icon="card.icon"
              :iconStyle="card.iconStyle"
              :title="card.title"
              :description="card.description"
              :count="card.count"
              :decimals="0"
              :showArrow="card.showArrow"
              separator=","
            />
          </ElCol>
        </ElRow>

        <h2 class="page-title">统计卡片（自定义样式）</h2>
        <ElRow :gutter="20">
          <ElCol
            v-for="card in statsCards"
            :key="`c-${card.id}`"
            :xs="24"
            :sm="12"
            :md="6"
            class="mb-5"
          >
            <FaStatsCard
              :icon="card.icon"
              :iconStyle="card.customIconStyle"
              :boxStyle="card.boxStyle"
              :title="card.title"
              :description="card.description"
              :textColor="card.textColor"
              :showArrow="card.showArrow"
            />
          </ElCol>
        </ElRow>

        <h2 class="page-title">进度卡片</h2>
        <ElRow :gutter="20">
          <ElCol
            v-for="card in progressCards"
            :key="`p-${card.id}`"
            :xs="24"
            :sm="12"
            :md="6"
            class="mb-5"
          >
            <FaProgressCard :percentage="card.percentage" :title="card.title" :color="card.color" />
          </ElCol>
        </ElRow>

        <h2 class="page-title">进度卡片（icon）</h2>
        <ElRow :gutter="20">
          <ElCol
            v-for="card in progressCards"
            :key="`pi-${card.id}`"
            :xs="24"
            :sm="12"
            :md="6"
            class="mb-5"
          >
            <FaProgressCard
              :percentage="card.percentage"
              :title="card.title"
              :color="card.color"
              :icon="card.icon"
              :iconStyle="card.iconStyle"
            />
          </ElCol>
        </ElRow>

        <h2 class="page-title">图表卡片</h2>
        <ElRow :gutter="20">
          <ElCol :xs="24" :sm="12" :md="6" class="mb-5">
            <FaLineChartCard
              :isMiniChart="true"
              :value="2545"
              label="新用户"
              date="过去7天"
              :percentage="1.2"
              :height="9.5"
              :chartData="[120, 132, 101, 134, 90, 230, 210]"
            />
          </ElCol>
          <ElCol :xs="24" :sm="12" :md="6" class="mb-5">
            <FaBarChartCard
              :isMiniChart="true"
              :value="15480"
              label="浏览量"
              date="过去14天"
              :percentage="-4.15"
              :height="9.5"
              barWidth="45%"
              :chartData="[120, 100, 150, 140, 90, 120, 130]"
            />
          </ElCol>
          <ElCol :xs="24" :sm="12" :md="6" class="mb-5">
            <FaLineChartCard
              :isMiniChart="true"
              :value="2545"
              label="粉丝数"
              date="过去30天"
              :percentage="1.2"
              :height="9.5"
              :showAreaColor="true"
              :chartData="[150, 180, 160, 200, 180, 220, 240]"
            />
          </ElCol>
          <ElCol :xs="24" :sm="12" :md="6" class="mb-5">
            <FaDonutChartCard
              :value="36358"
              title="粉丝量"
              :percentage="18"
              percentageLabel="较去年"
              :data="[50, 40]"
              :height="9.5"
              currentValue="2022"
              previousValue="2021"
              :radius="['50%', '70%']"
            />
          </ElCol>
        </ElRow>

        <h2 class="page-title">图表卡片（大）</h2>
        <ElRow :gutter="20">
          <ElCol :xs="24" :sm="12" :md="6" class="mb-5">
            <FaLineChartCard
              :value="2545"
              label="新用户"
              :percentage="1.2"
              :height="11"
              :chartData="[120, 132, 101, 134, 90, 230, 210]"
            />
          </ElCol>
          <ElCol :xs="24" :sm="12" :md="6" class="mb-5">
            <FaBarChartCard
              :value="15480"
              label="浏览量"
              :percentage="-4.15"
              :height="11"
              :chartData="[120, 100, 150, 140, 90, 120, 130, 110]"
            />
          </ElCol>
          <ElCol :xs="24" :sm="12" :md="6" class="mb-5">
            <FaLineChartCard
              :value="2545"
              label="粉丝数"
              :percentage="1.2"
              :height="11"
              :showAreaColor="true"
              :chartData="[150, 180, 160, 200, 180, 220, 240]"
            />
          </ElCol>
          <ElCol :xs="24" :sm="12" :md="6" class="mb-5">
            <FaDonutChartCard
              :value="36358"
              title="粉丝量"
              :percentage="-18"
              percentageLabel="较2021年"
              :data="[70, 30]"
              :height="11"
              currentValue="12月"
              previousValue="11月"
            />
          </ElCol>
        </ElRow>

        <h2 class="page-title">数据列表卡片</h2>
        <ElRow :gutter="20">
          <ElCol :xs="24" :sm="12" :lg="8" class="mb-5">
            <FaDataListCard :list="dataList" title="待办事项" subtitle="今日待处理任务" />
          </ElCol>
          <ElCol :xs="24" :sm="12" :lg="8" class="mb-5">
            <FaDataListCard
              :maxCount="4"
              :list="dataList"
              title="最近活动"
              subtitle="近期活动列表"
              :showMoreButton="true"
              @more="handleMore"
            />
          </ElCol>
          <ElCol :xs="24" :sm="12" :lg="8" class="mb-5">
            <FaTimelineListCard :list="timelineData" title="最近交易" subtitle="2024年12月20日" />
          </ElCol>
        </ElRow>

        <h2 class="page-title">图片卡片</h2>
        <ElRow :gutter="20">
          <ElCol v-for="card in imageCards" :key="card.id" :xs="24" :sm="12" :md="6" class="mb-5">
            <FaImageCard
              :imageUrl="card.imageUrl"
              :title="card.title"
              :category="card.category"
              :readTime="card.readTime"
              :views="card.views"
              :comments="card.comments"
              :date="card.date"
              @click="handleImageCardClick(card)"
            />
          </ElCol>
        </ElRow>

        <h2 class="page-title">基础 & 自定义按钮+背景色</h2>
        <ElRow :gutter="20">
          <ElCol :xs="24" :sm="12" :md="12" class="mb-5">
            <FaBasicBanner
              title="数据中心运行状态"
              subtitle="系统访问量同比增长 23%，所有服务运行稳定，数据监控正常。"
            />
          </ElCol>
          <ElCol :xs="24" :sm="12" :md="12" class="mb-5">
            <FaBasicBanner
              title="欢迎使用 Art Design Pro"
              subtitle="基于 Vue 3 + TypeScript + Element Plus 构建的现代化管理系统。"
              titleColor="#333"
              subtitleColor="#666"
              boxStyle="bg-[#D4F1F7]!"
              :buttonConfig="{
                show: true,
                text: '开始探索',
                color: 'var(--fa-success)',
                textColor: '#fff',
                radius: '6px',
              }"
              @buttonClick="handleBannerDemoClick"
            />
          </ElCol>
        </ElRow>

        <h2 class="page-title">卡片横幅</h2>
        <ElRow :gutter="20">
          <ElCol :xs="24" :sm="12" :md="12" :lg="6" class="mb-5">
            <FaCardBanner
              title="系统运行正常"
              description="所有核心服务运行稳定，响应时间在正常范围内。"
            />
          </ElCol>
          <ElCol :xs="24" :sm="12" :md="12" :lg="6" class="mb-5">
            <FaCardBanner
              :image="bannerIcon2"
              title="重要消息通知"
              description="您有 3 条待处理的重要消息，请及时查看。"
              :button="{
                show: true,
                text: '查看详情',
                color: 'var(--fa-warning)',
                textColor: '#fff',
              }"
            />
          </ElCol>
          <ElCol :xs="24" :sm="12" :md="12" :lg="6" class="mb-5">
            <FaCardBanner
              :image="bannerIcon3"
              title="数据分析报告"
              description="本周业务数据分析报告已完成，请查看关键指标。"
              :button="{
                show: true,
                text: '下载报告',
                color: 'var(--fa-error)',
                textColor: '#fff',
              }"
            />
          </ElCol>
          <ElCol :xs="24" :sm="12" :md="12" :lg="6" class="mb-5">
            <FaCardBanner
              :image="bannerIcon4"
              title="版本更新提醒"
              description="Art Design Pro v2.1.0 已发布，包含性能优化和新功能。"
              :button="{
                show: true,
                text: '立即更新',
                color: 'var(--theme-color)',
                textColor: '#fff',
              }"
              :cancelButton="{ show: true, text: '稍后提醒', color: '#eee', textColor: '#333' }"
              @click="handleBannerDemoConfirm"
              @cancel="handleBannerDemoCancel"
            />
          </ElCol>
        </ElRow>
      </div>
    </div>

    <!-- 图表演示区 -->
    <ElRow :gutter="20">
      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5"><span class="text-base font-medium">柱状图（单数据）</span></div>
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
          <div class="pb-3.5"><span class="text-base font-medium">柱状图（多组数据）</span></div>
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
          <div class="pb-3.5"><span class="text-base font-medium">柱状图（堆叠）</span></div>
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
          <div class="pb-3.5"><span class="text-base font-medium">折线图</span></div>
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
          <div class="pb-3.5"><span class="text-base font-medium">折线图（渐变）</span></div>
          <FaLineChart
            :data="[28, 45, 82, 35, 100, 32, 55]"
            :xAxisData="['一月', '二月', '三月', '四月', '五月', '六月', '七月']"
            :showAreaColor="true"
          />
        </div>
      </ElCol>
      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5"><span class="text-base font-medium">折线图（多组）</span></div>
          <FaLineChart
            :data="multiLineData"
            :xAxisData="['1月', '2月', '3月', '4月', '5月', '6月']"
            :showLegend="true"
          />
        </div>
      </ElCol>
      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5"><span class="text-base font-medium">柱状图（水平）</span></div>
          <FaHBarChart
            :data="[50, 80, 120, 90, 60]"
            :xAxisData="['产品A', '产品B', '产品C', '产品D', '产品E']"
          />
        </div>
      </ElCol>
      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5"><span class="text-base font-medium">柱状图（水平多组）</span></div>
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
          <div class="pb-3.5"><span class="text-base font-medium">柱状图（水平堆叠）</span></div>
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
          <div class="pb-3.5"><span class="text-base font-medium">环形图</span></div>
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
          <div class="pb-3.5"><span class="text-base font-medium">环形图（中心文字）</span></div>
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
            :showLegend="true"
            legendPosition="bottom"
            centerText="¥300,458"
          />
        </div>
      </ElCol>
      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5"><span class="text-base font-medium">饼图</span></div>
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
          <div class="pb-3.5"><span class="text-base font-medium">散点图</span></div>
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
          <div class="pb-3.5"><span class="text-base font-medium">雷达图</span></div>
          <FaRadarChart
            :indicator="[
              { name: '销售', max: 100 },
              { name: '管理', max: 100 },
              { name: '技术', max: 100 },
              { name: '客服', max: 100 },
              { name: '开发', max: 100 },
            ]"
            :data="[
              { name: '预算分配', value: [80, 70, 90, 85, 75] },
              { name: '实际开销', value: [70, 75, 85, 80, 70] },
            ]"
          />
        </div>
      </ElCol>
      <ElCol :xs="24" :md="12" :lg="8" class="mb-5">
        <div class="fa-card">
          <div class="pb-3.5"><span class="text-base font-medium">K线图</span></div>
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
          <div class="pb-3.5"><span class="text-base font-medium">双向堆叠柱状图</span></div>
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

    <!-- 地图 -->
    <div class="page-content" element-loading-text="加载中...">
      <FaMapChart />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { LineDataItem } from "@/types/component/chart";
import { ref } from "vue";
import { ElMessage } from "element-plus";
import cover1 from "@imgs/cover/img1.webp";
import cover2 from "@imgs/cover/img2.webp";
import cover3 from "@imgs/cover/img3.webp";
import cover4 from "@imgs/cover/img4.webp";
import bannerIcon2 from "@imgs/3d/icon2.webp";
import bannerIcon3 from "@imgs/3d/icon3.webp";
import bannerIcon4 from "@imgs/3d/icon4.webp";

import TodaySales from "./modules/today-sales.vue";
import VisitorInsights from "./modules/visitor-insights.vue";
import TotalRevenue from "./modules/total-revenue.vue";
import CustomerSatisfaction from "./modules/customer-satisfaction.vue";
import TargetVsReality from "./modules/target-vs-reality.vue";
import TopProducts from "./modules/top-products.vue";
import SalesMappingByCountry from "./modules/sales-mapping-by-country.vue";
import VolumeServiceLevel from "./modules/volume-service-level.vue";

defineOptions({ name: "Analysis" });

const FaMapChart = defineAsyncComponent(() => import("@/components/charts/fa-map-chart/index.vue"));

// === 横幅组件演示 ===
function handleBannerDemoClick() {
  console.log("banner clicked");
}
function handleBannerDemoConfirm() {
  console.log("confirm clicked");
}
function handleBannerDemoCancel() {
  console.log("cancel clicked");
}

// === 图表演示数据 ===
const multiLineData: LineDataItem[] = [
  {
    name: "销售额",
    data: [120, 132, 101, 134, 90, 130],
    areaStyle: { startOpacity: 0.1, endOpacity: 0 },
  },
  {
    name: "利润",
    data: [80, 92, 71, 94, 60, 80],
    areaStyle: { startOpacity: 0.1, endOpacity: 0 },
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

// === 卡片演示数据 ← workplace ===
const statsCards = [
  {
    id: 1,
    title: "销售产品",
    count: 1235,
    description: "鞋子、牛仔裤、派对服装、手表",
    icon: "ri:bar-chart-box-line",
    boxStyle: "bg-theme/10!",
    customIconStyle: "text-theme! text-3xl!",
    iconStyle: "bg-info",
    textColor: "var(--theme-color)",
    showArrow: false,
  },
  {
    id: 2,
    title: "活跃用户",
    count: 5000,
    description: "日活跃用户超过5,000+",
    icon: "ri:account-box-2-line",
    boxStyle: "bg-warning/10!",
    customIconStyle: "text-warning! text-3xl!",
    iconStyle: "bg-warning",
    textColor: "var(--fa-warning)",
    showArrow: false,
  },
  {
    id: 3,
    title: "总收入",
    count: 35000,
    description: "月收入超过¥350,000+",
    icon: "ri:money-cny-box-line",
    boxStyle: "bg-secondary/10!",
    customIconStyle: "text-secondary! text-3xl!",
    iconStyle: "bg-secondary",
    textColor: "var(--fa-secondary)",
    showArrow: false,
  },
  {
    id: 4,
    title: "客户评价",
    count: 4800,
    description: "平均评分4.8/5",
    icon: "ri:message-3-line",
    boxStyle: "bg-error/10!",
    customIconStyle: "text-error! text-3xl!",
    iconStyle: "bg-error",
    textColor: "var(--fa-error)",
    showArrow: false,
  },
];
const progressCards = [
  {
    id: 1,
    title: "完成进度",
    percentage: 75,
    color: "var(--fa-success)",
    icon: "ri:arrow-up-circle-line",
    iconStyle: "bg-success/12 text-success",
  },
  {
    id: 2,
    title: "项目进度",
    percentage: 65,
    color: "var(--theme-color)",
    icon: "ri:twitch-line",
    iconStyle: "bg-theme/12 text-theme",
  },
  {
    id: 3,
    title: "学习进度",
    percentage: 45,
    color: "var(--fa-error)",
    icon: "ri:game-line",
    iconStyle: "bg-error/12! text-error",
  },
  {
    id: 4,
    title: "任务进度",
    percentage: 90,
    color: "var(--fa-secondary)",
    icon: "ri:flag-2-line",
    iconStyle: "bg-secondary/12 text-secondary",
  },
];
const imageCards = [
  {
    id: 1,
    imageUrl: cover1,
    title: "AI技术在医疗领域的创新应用与发展前景",
    category: "社交",
    readTime: "2分钟",
    views: 9125,
    comments: 3,
    date: "12月19日 周一",
  },
  {
    id: 2,
    imageUrl: cover2,
    title: "大数据分析助力企业决策的实践案例",
    category: "技术",
    readTime: "3分钟",
    views: 7234,
    comments: 5,
    date: "12月20日 周二",
  },
  {
    id: 3,
    imageUrl: cover3,
    title: "区块链技术在供应链管理中的应用",
    category: "科技",
    readTime: "4分钟",
    views: 5678,
    comments: 8,
    date: "12月21日 周三",
  },
  {
    id: 4,
    imageUrl: cover4,
    title: "云计算技术发展趋势与未来展望",
    category: "云技术",
    readTime: "5分钟",
    views: 4321,
    comments: 6,
    date: "12月22日 周四",
  },
];
const dataList = [
  {
    title: "新加坡之行",
    status: "进行中",
    time: "5分钟",
    class: "bg-theme/12 text-theme",
    icon: "ri:camera-4-line",
  },
  {
    title: "归档数据",
    status: "进行中",
    time: "10分钟",
    class: "bg-secondary/12 text-secondary",
    icon: "ri:bar-chart-box-line",
  },
  {
    title: "客户会议",
    status: "待处理",
    time: "15分钟",
    class: "bg-warning/12 text-warning",
    icon: "ri:user-3-line",
  },
  {
    title: "筛选任务团队",
    status: "进行中",
    time: "20分钟",
    class: "bg-error/12 text-error",
    icon: "ri:account-circle-line",
  },
  {
    title: "发送信封给小王",
    status: "已完成",
    time: "20分钟",
    class: "bg-success/12 text-success",
    icon: "ri:message-3-line",
  },
];
const timelineData = [
  {
    time: "上午 09:30",
    status: "rgb(73, 190, 255)",
    content: "收到 John Doe 支付的 385.90 美元",
  },
  { time: "上午 10:00", status: "rgb(54, 158, 255)", content: "新销售记录", code: "ML-3467" },
  { time: "上午 12:00", status: "rgb(103, 232, 207)", content: "向 Michael 支付了 64.95 美元" },
  { time: "下午 14:30", status: "rgb(255, 193, 7)", content: "系统维护通知", code: "MT-2023" },
  {
    time: "下午 15:45",
    status: "rgb(255, 105, 105)",
    content: "紧急订单取消提醒",
    code: "OR-9876",
  },
  { time: "下午 17:00", status: "rgb(103, 232, 207)", content: "完成每日销售报表" },
];

function handleMore() {
  ElMessage.info("查看更多");
}
function handleImageCardClick(card: (typeof imageCards)[0]) {
  console.log("点击卡片:", card);
}
</script>

<style scoped>
@reference "@styles/core/tailwind.css";

:deep(.el-card) {
  --el-card-border-radius: calc(var(--custom-radius) + 2px);

  border: 1px solid var(--fa-card-border);
}

.page-title {
  @apply my-5 text-xl font-medium first:mt-0;
}

.fa-card {
  @apply p-5;
}

.console-cards-showcase {
  padding: 16px;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: var(--el-border-radius-base);
}
</style>
