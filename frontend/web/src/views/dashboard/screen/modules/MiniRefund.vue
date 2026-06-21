<template>
  <div class="mini-chart-panel">
    <div class="mc-hd">售后退款率</div>
    <div class="mc-value" style="color: #f59e0b">{{ val }}<span class="mc-unit">%</span></div>
    <div ref="chartRef" class="mc-chart" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import * as echarts from "echarts";

defineOptions({ name: "MiniRefund" });

const chartRef = ref<HTMLDivElement>();
let chart: echarts.ECharts | null = null;
let timer = 0;
const val = ref(2.1);

function initChart(dom: HTMLDivElement) {
  chart = echarts.init(dom);
  chart.setOption({
    grid: { top: 8, right: 4, bottom: 2, left: 2 },
    xAxis: {
      type: "category",
      show: false,
      data: ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
    },
    yAxis: { type: "value", show: false, min: 0, max: 4 },
    series: [
      {
        type: "bar",
        barWidth: 5,
        barGap: "30%",
        itemStyle: {
          borderRadius: [2, 2, 0, 0],
          color: (p: any) => (p.dataIndex < 5 ? "#f59e0b" : "#ef4444"),
        },
        data: [2.4, 2.2, 2.5, 2.1, 2.3, 2.0, 2.1],
      },
    ],
  });
}

function tick() {
  if (!chart || chart.isDisposed()) return;
  const n = +(1.5 + Math.random() * 1.5).toFixed(1);
  val.value = n;
  const d = chart.getOption() as { series: [{ data: number[] }] };
  const arr = d.series[0].data;
  arr.push(n);
  arr.shift();
  chart.setOption({ series: [{ data: arr }] });
}

onMounted(() => {
  const el = chartRef.value;
  if (!el) return;

  const observer = new ResizeObserver((entries) => {
    const entry = entries[0];
    if (entry && entry.contentRect.width > 0 && entry.contentRect.height > 0) {
      observer.disconnect();
      initChart(el);
      timer = window.setInterval(tick, 5000);
    }
  });
  observer.observe(el);
});
onUnmounted(() => {
  clearInterval(timer);
  chart?.dispose();
});
</script>

<style scoped>
.mini-chart-panel {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 10px 12px;
  overflow: hidden;
  background: linear-gradient(180deg, rgb(0 30 80 / 55%) 0%, rgb(6 11 36 / 70%) 100%);
  border: 1px solid var(--border, rgb(0 180 255 / 12%));
  border-radius: 10px;
}

.mini-chart-panel::after {
  position: absolute;
  top: 4px;
  left: 4px;
  width: 6px;
  height: 6px;
  content: "";
  border-top: 1px solid rgb(245 158 11 / 40%);
  border-left: 1px solid rgb(245 158 11 / 40%);
}

.mc-hd {
  margin-bottom: 2px;
  font-size: 10px;
  opacity: 0.35;
}

.mc-value {
  margin-bottom: 0;
  font-size: 16px;
  font-weight: 700;
  line-height: 1;
}

.mc-unit {
  margin-left: 2px;
  font-size: 9px;
  font-weight: 400;
  opacity: 0.4;
}

.mc-chart {
  flex: 1;
  min-height: 0;
}
</style>
