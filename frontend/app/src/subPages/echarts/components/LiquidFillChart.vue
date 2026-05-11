<script setup lang="ts">
import { PieChart } from 'echarts/charts'
import { TooltipComponent } from 'echarts/components'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([
  TooltipComponent,
  PieChart,
  CanvasRenderer,
])

const progress = ref(68)

const option = computed(() => ({
  tooltip: {
    // formatter: () => `完成度: ${progress.value}%`,
    textStyle: {
      // #ifdef MP-WEIXIN
      // 临时解决微信小程序 tooltip 文字阴影问题
      textShadowBlur: 1,
      // #endif
    },
  },
  graphic: [
    {
      type: 'text',
      left: 'center',
      top: 'center',
      style: {
        text: `完成度：${progress.value}%`,
        fontSize: 24,
        fontWeight: 'bold',
        fill: '#5470c6',
      },
    },
  ],
  series: [
    {
      type: 'pie',
      radius: ['60%', '80%'],
      center: ['50%', '50%'],
      startAngle: 90,
      clockwise: true,
      silent: true,
      label: {
        show: false,
      },
      labelLine: {
        show: false,
      },
      data: [
        {
          value: progress.value,
          itemStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
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
            borderRadius: 10,
          },
        },
        {
          value: 100 - progress.value,
          itemStyle: {
            color: '#f0f0f0',
            borderRadius: 10,
          },
        },
      ],
    },
    // 内圆背景
    {
      type: 'pie',
      radius: ['0%', '58%'],
      center: ['50%', '50%'],
      silent: true,
      label: {
        show: false,
      },
      labelLine: {
        show: false,
      },
      data: [
        {
          value: 100,
          itemStyle: {
            color: {
              type: 'radial',
              x: 0.5,
              y: 0.5,
              r: 0.5,
              colorStops: [
                {
                  offset: 0,
                  color: 'rgba(84, 112, 198, 0.1)',
                },
                {
                  offset: 1,
                  color: 'rgba(84, 112, 198, 0.05)',
                },
              ],
            },
          },
        },
      ],
    },
  ],
}))

// 模拟进度变化
let timer: NodeJS.Timeout | null = null

onMounted(() => {
  timer = setInterval(() => {
    progress.value = Math.round(Math.random() * 100)
  }, 4000)
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
