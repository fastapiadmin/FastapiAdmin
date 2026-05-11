<script setup lang="ts">
import { PieChart } from 'echarts/charts'
import { DatasetComponent, LegendComponent, TooltipComponent } from 'echarts/components'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([
  LegendComponent,
  TooltipComponent,
  DatasetComponent,
  PieChart,
  CanvasRenderer,
])

const option = ref({
  legend: {
    top: 10,
    left: 'center',
  },
  tooltip: {
    trigger: 'item',
    textStyle: {
      // #ifdef MP-WEIXIN
      // 临时解决微信小程序 tooltip 文字阴影问题
      textShadowBlur: 1,
      // #endif
    },
  },
  series: [
    {
      type: 'pie',
      radius: ['30%', '52%'],
      label: {
        show: false,
        position: 'center',
      },
      itemStyle: {
        borderWidth: 2,
        borderColor: '#ffffff',
        borderRadius: 10,
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 20,
        },
      },
    },
  ],
  dataset: {
    dimensions: ['来源', '数量'],
    source: [
      ['Search Engine', 1048],
      ['Direct', 735],
      ['Email', 580],
      ['Union Ads', 484],
      ['Video Ads', 300],
    ],
  },
})
</script>

<template>
  <uni-echarts custom-class="h-300px" :option="option" />
</template>
