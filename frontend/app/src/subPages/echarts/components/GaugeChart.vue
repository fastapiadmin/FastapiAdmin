<script setup lang="ts">
import { GaugeChart } from 'echarts/charts'
import { TooltipComponent } from 'echarts/components'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([
  TooltipComponent,
  GaugeChart,
  CanvasRenderer,
])

const option = ref({
  tooltip: {
    formatter: '{a} <br/>{b}: {c}%',
    textStyle: {
      // #ifdef MP-WEIXIN
      // 临时解决微信小程序 tooltip 文字阴影问题
      textShadowBlur: 1,
      // #endif
    },
  },
  series: [
    {
      name: '性能指标',
      type: 'gauge',
      center: ['50%', '60%'],
      radius: '75%',
      min: 0,
      max: 100,
      splitNumber: 10,
      axisLine: {
        lineStyle: {
          width: 10,
          color: [
            [0.3, '#ee6666'],
            [0.7, '#fac858'],
            [1, '#91cc75'],
          ],
        },
      },
      pointer: {
        itemStyle: {
          color: 'auto',
        },
      },
      axisTick: {
        distance: -30,
        length: 8,
        lineStyle: {
          color: '#fff',
          width: 2,
        },
      },
      splitLine: {
        distance: -30,
        length: 30,
        lineStyle: {
          color: '#fff',
          width: 4,
        },
      },
      axisLabel: {
        color: 'auto',
        distance: 40,
        fontSize: 12,
      },
      detail: {
        valueAnimation: true,
        formatter: '{value}%',
        color: 'auto',
        fontSize: 20,
        fontWeight: 'bold',
        offsetCenter: [0, '70%'],
      },
      data: [
        {
          value: 75,
          name: 'CPU使用率',
        },
      ],
    },
  ],
})

// 模拟数据变化
let timer: NodeJS.Timeout | null = null

onMounted(() => {
  timer = setInterval(() => {
    const newValue = Math.round(Math.random() * 100)
    option.value.series[0].data[0].value = newValue
  }, 3000)
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>

<template>
  <uni-echarts custom-class="h-300px" :option="option" />
</template>
