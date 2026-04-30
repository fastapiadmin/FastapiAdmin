<script setup lang="ts">
import { ScatterChart } from 'echarts/charts'
import { DatasetComponent, GridComponent, LegendComponent, TooltipComponent } from 'echarts/components'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([
  GridComponent,
  LegendComponent,
  TooltipComponent,
  DatasetComponent,
  ScatterChart,
  CanvasRenderer,
])

const option = ref({
  tooltip: {
    trigger: 'item',
    formatter: (params: any) => {
      return `${params.seriesName}<br/>身高: ${params.value[0]}cm<br/>体重: ${params.value[1]}kg`
    },
  },
  legend: {
    data: ['男性', '女性'],
    top: 30,
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true,
  },
  xAxis: {
    type: 'value',
    name: '身高(cm)',
    nameLocation: 'middle',
    nameGap: 30,
    min: 150,
    max: 190,
    splitLine: {
      lineStyle: {
        type: 'dashed',
      },
    },
  },
  yAxis: {
    type: 'value',
    name: '体重(kg)',
    nameLocation: 'middle',
    nameGap: 30,
    min: 40,
    max: 90,
    splitLine: {
      lineStyle: {
        type: 'dashed',
      },
    },
  },
  series: [
    {
      name: '男性',
      type: 'scatter',
      data: [
        [175, 70],
        [180, 75],
        [170, 65],
        [185, 80],
        [172, 68],
        [178, 72],
        [182, 78],
        [168, 62],
        [176, 71],
        [174, 69],
      ],
      symbolSize: 8,
      itemStyle: {
        color: '#5470c6',
        opacity: 0.8,
      },
      emphasis: {
        itemStyle: {
          borderColor: '#5470c6',
          borderWidth: 2,
        },
      },
    },
    {
      name: '女性',
      type: 'scatter',
      data: [
        [160, 50],
        [165, 55],
        [158, 48],
        [170, 60],
        [162, 52],
        [168, 58],
        [155, 45],
        [172, 62],
        [164, 54],
        [166, 56],
      ],
      symbolSize: 8,
      itemStyle: {
        color: '#91cc75',
        opacity: 0.8,
      },
      emphasis: {
        itemStyle: {
          borderColor: '#91cc75',
          borderWidth: 2,
        },
      },
    },
  ],
})
</script>

<template>
  <uni-echarts custom-class="h-300px" :option="option" />
</template>
