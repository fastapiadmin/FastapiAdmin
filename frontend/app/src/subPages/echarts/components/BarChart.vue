<!--
 * @Author: weisheng
 * @Date: 2025-09-15 18:51:03
 * @LastEditTime: 2025-09-16 13:12:22
 * @LastEditors: weisheng
 * @Description:
 * @FilePath: /wot-starter/src/subPages/echarts/components/BarChart.vue
 * 记得注释
-->
<script setup lang="ts">
import { BarChart } from 'echarts/charts'
import { DatasetComponent, GridComponent, LegendComponent, TooltipComponent } from 'echarts/components'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([
  GridComponent,
  LegendComponent,
  TooltipComponent,
  DatasetComponent,
  BarChart,
  CanvasRenderer,
])

const option = ref({
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow',
    },
  },
  legend: {
    data: ['销售额', '利润'],
    top: 30,
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true,
  },
  xAxis: {
    type: 'category',
    data: ['1月', '2月', '3月', '4月', '5月', '6月'],
  },
  yAxis: {
    type: 'value',
  },
  series: [
    {
      name: '销售额',
      type: 'bar',
      data: [120, 200, 150, 80, 70, 110],
      itemStyle: {
        color: '#5470c6',
      },
    },
    {
      name: '利润',
      type: 'bar',
      data: [20, 40, 30, 15, 12, 22],
      itemStyle: {
        color: '#91cc75',
      },
    },
  ],
})
</script>

<template>
  <uni-echarts custom-class="h-300px" :option="option" />
</template>
