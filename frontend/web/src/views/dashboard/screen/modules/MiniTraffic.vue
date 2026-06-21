<template>
  <div class="mini-chart-panel">
    <div class="mc-hd">页面访问量(PV)</div>
    <div class="mc-value" style="color: #10b981">{{ val }}</div>
    <div ref="chartRef" class="mc-chart" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import * as echarts from "echarts";

defineOptions({ name: "MiniTraffic" });

const chartRef = ref<HTMLDivElement>();
let chart: echarts.ECharts | null = null;
let timer = 0;
const val = ref(5210);

function initChart(dom: HTMLDivElement) {
  chart = echarts.init(dom);
  chart.setOption({
    grid: { top: 8, right: 4, bottom: 2, left: 2 },
    xAxis: { type: "category", show: false, data: ["", "", "", "", "", ""] },
    yAxis: { type: "value", show: false },
    series: [
      {
        type: "line",
        smooth: true,
        symbol: "circle",
        symbolSize: 4,
        lineStyle: { color: "#10b981", width: 2 },
        itemStyle: { color: "#10b981" },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: "rgba(16,185,129,0.25)" },
            { offset: 1, color: "rgba(16,185,129,0)" },
          ]),
        },
        data: [3800, 4200, 4500, 4800, 5100, 5210],
      },
    ],
  });
}

function tick() {
  if (!chart || chart.isDisposed()) return;
  const n = Math.round(4000 + Math.random() * 2500);
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
      timer = window.setInterval(tick, 4000);
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
  border-top: 1px solid rgb(16 185 129 / 40%);
  border-left: 1px solid rgb(16 185 129 / 40%);
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

.mc-chart {
  flex: 1;
  min-height: 0;
}
</style>
