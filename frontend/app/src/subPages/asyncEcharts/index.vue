<script setup lang="ts">
import BarChart from '@/subPages/echarts/components/BarChart.vue'
import DonutChart from '@/subPages/echarts/components/DonutChart.vue'
import FunnelChart from '@/subPages/echarts/components/FunnelChart.vue'
import GaugeChart from '@/subPages/echarts/components/GaugeChart.vue'
import LineChart from '@/subPages/echarts/components/LineChart.vue'
import LiquidFillChart from '@/subPages/echarts/components/LiquidFillChart.vue'
import MiniLineChart from '@/subPages/echarts/components/MiniLineChart.vue'
import PieChart from '@/subPages/echarts/components/PieChart.vue'
import RadarChart from '@/subPages/echarts/components/RadarChart.vue'
import ScatterChart from '@/subPages/echarts/components/ScatterChart.vue'
import StackedBarChart from '@/subPages/echarts/components/StackedBarChart.vue'

defineOptions({
  componentPlaceholder: {
    BarChart: 'view',
    DonutChart: 'view',
    FunnelChart: 'view',
    GaugeChart: 'view',
    LineChart: 'view',
    LiquidFillChart: 'view',
    MiniLineChart: 'view',
    PieChart: 'view',
    RadarChart: 'view',
    ScatterChart: 'view',
    StackedBarChart: 'view',
  },
})

definePage({
  name: 'echartsAsync',
  style: {
    navigationBarTitleText: 'echarts 异步跨包示例',
  },
})
</script>

<template>
  <view class="bg-gray-50 p-5">
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
