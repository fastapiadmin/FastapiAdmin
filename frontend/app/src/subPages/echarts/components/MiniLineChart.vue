<script setup lang="ts">
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([
  GridComponent,
  TooltipComponent,
  LineChart,
  CanvasRenderer,
])

const option = ref({
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(50,50,50,0.8)',
    borderColor: 'transparent',
    textStyle: {
      color: '#fff',
      fontSize: 12,
      // #ifdef MP-WEIXIN
      // 临时解决微信小程序 tooltip 文字阴影问题
      textShadowBlur: 1,
      // #endif
    },
    formatter: (params: any) => {
      const param = params[0]
      return `${param.name}<br/>${param.seriesName}: ${param.value}`
    },
  },
  grid: {
    left: '8%',
    right: '8%',
    top: '25%',
    bottom: '15%',
    containLabel: true,
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'],
    axisLabel: {
      fontSize: 10,
      color: '#666',
    },
    axisLine: {
      lineStyle: {
        color: '#e0e0e0',
      },
    },
    axisTick: {
      show: false,
    },
  },
  yAxis: {
    type: 'value',
    axisLabel: {
      fontSize: 10,
      color: '#666',
    },
    axisLine: {
      show: false,
    },
    axisTick: {
      show: false,
    },
    splitLine: {
      lineStyle: {
        color: '#f0f0f0',
        type: 'dashed',
      },
    },
  },
  series: [
    {
      name: '访问量',
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      lineStyle: {
        width: 3,
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 1,
          y2: 0,
          colorStops: [
            {
              offset: 0,
              color: '#5470c6',
            },
            {
              offset: 1,
              color: '#91cc75',
            },
          ],
        },
      },
      itemStyle: {
        color: '#5470c6',
        borderWidth: 2,
        borderColor: '#fff',
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            {
              offset: 0,
              color: 'rgba(84, 112, 198, 0.3)',
            },
            {
              offset: 1,
              color: 'rgba(84, 112, 198, 0.05)',
            },
          ],
        },
      },
      data: [120, 80, 150, 200, 180, 250, 160],
    },
  ],
})
</script>

<template>
  <uni-echarts custom-class="h-300px" :option="option" />
</template>
