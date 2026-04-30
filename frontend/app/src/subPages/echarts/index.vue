<script setup lang="ts">
import BarChart from './components/BarChart.vue'
import DonutChart from './components/DonutChart.vue'
import FunnelChart from './components/FunnelChart.vue'
import GaugeChart from './components/GaugeChart.vue'
import LineChart from './components/LineChart.vue'
import LiquidFillChart from './components/LiquidFillChart.vue'
import MiniLineChart from './components/MiniLineChart.vue'
import PieChart from './components/PieChart.vue'
import RadarChart from './components/RadarChart.vue'
import ScatterChart from './components/ScatterChart.vue'
import StackedBarChart from './components/StackedBarChart.vue'

definePage({
  name: 'echarts',
  style: {
    navigationBarTitleText: 'Echarts 演示',
  },
})

const router = useRouter()

function navigateToAsync() {
  router.push({
    name: 'echartsAsync',
  })
}
</script>

<template>
  <view class="bg-gray-50 p-5">
    <!-- 异步 Echarts 入口 -->
    <view class="mb-5 rounded-3 bg-white p-3 shadow-sm">
      <view
        class="rounded-2 bg-blue-500 px-6 py-3 text-white font-medium transition-colors hover:bg-blue-600"
        @click="navigateToAsync"
      >
        查看异步 Echarts 示例
      </view>
    </view>
    <!-- 饼图 -->
    <view class="mb-5 rounded-3 bg-white p-5 shadow-sm">
      <view class="mb-5 text-center text-base text-gray-800 font-medium">
        饼图示例
      </view>
      <PieChart />
    </view>

    <!-- 柱状图 -->
    <view class="mb-5 rounded-3 bg-white p-5 shadow-sm">
      <view class="mb-5 text-center text-base text-gray-800 font-medium">
        柱状图示例
      </view>
      <BarChart />
    </view>

    <!-- 折线图 -->
    <view class="mb-5 rounded-3 bg-white p-5 shadow-sm">
      <view class="mb-5 text-center text-base text-gray-800 font-medium">
        折线图示例
      </view>
      <LineChart />
    </view>

    <!-- 雷达图 -->
    <view class="mb-5 rounded-3 bg-white p-5 shadow-sm">
      <view class="mb-5 text-center text-base text-gray-800 font-medium">
        雷达图示例
      </view>
      <RadarChart />
    </view>

    <!-- 散点图 -->
    <view class="mb-5 rounded-3 bg-white p-5 shadow-sm">
      <view class="mb-5 text-center text-base text-gray-800 font-medium">
        散点图示例
      </view>
      <ScatterChart />
    </view>

    <!-- 环形图 -->
    <view class="mb-5 rounded-3 bg-white p-5 shadow-sm">
      <view class="mb-5 text-center text-base text-gray-800 font-medium">
        环形图示例
      </view>
      <DonutChart />
    </view>

    <!-- 漏斗图 -->
    <view class="mb-5 rounded-3 bg-white p-5 shadow-sm">
      <view class="mb-5 text-center text-base text-gray-800 font-medium">
        漏斗图示例
      </view>
      <FunnelChart />
    </view>

    <!-- 仪表盘图 -->
    <view class="mb-5 rounded-3 bg-white p-5 shadow-sm">
      <view class="mb-5 text-center text-base text-gray-800 font-medium">
        仪表盘示例
      </view>
      <GaugeChart />
    </view>

    <!-- 迷你折线图 -->
    <view class="mb-5 rounded-3 bg-white p-5 shadow-sm">
      <view class="mb-5 text-center text-base text-gray-800 font-medium">
        迷你折线图示例
      </view>
      <MiniLineChart />
    </view>

    <!-- 堆叠柱状图 -->
    <view class="mb-5 rounded-3 bg-white p-5 shadow-sm">
      <view class="mb-5 text-center text-base text-gray-800 font-medium">
        堆叠柱状图示例
      </view>
      <StackedBarChart />
    </view>

    <!-- 水球图 -->
    <view class="mb-5 rounded-3 bg-white p-5 shadow-sm">
      <view class="mb-5 text-center text-base text-gray-800 font-medium">
        水球图示例
      </view>
      <LiquidFillChart />
    </view>
  </view>
</template>
