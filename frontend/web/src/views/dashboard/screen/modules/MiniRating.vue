<template>
  <div class="mini-chart-panel">
    <div class="mc-hd">用户综合评分</div>
    <div class="mc-value" style="color: #f43f5e">{{ val }}<span class="mc-unit">分</span></div>
    <div ref="chartRef" class="mc-chart" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { echarts } from "@/plugins/echarts";

defineOptions({ name: "MiniRating" });

const chartRef = ref<HTMLDivElement>();
let chart: echarts.ECharts | null = null;
let timer = 0;
const val = ref(92);

const indicators = [
  { name: "商品质量", max: 100 },
  { name: "服务态度", max: 100 },
  { name: "物流速度", max: 100 },
  { name: "性价比", max: 100 },
  { name: "包装完好", max: 100 },
];

function initChart(dom: HTMLDivElement) {
  chart = echarts.init(dom);
  chart.setOption({
    radar: {
      center: ["50%", "56%"],
      radius: "60%",
      indicator: indicators,
      axisName: { color: "#94a3b8", fontSize: 7 },
      splitArea: { areaStyle: { color: ["rgba(244,63,94,0.02)", "rgba(244,63,94,0.02)"] } },
      splitLine: { lineStyle: { color: "#1a2050" } },
      axisLine: { lineStyle: { color: "#1a2050" } },
    },
    series: [
      {
        type: "radar",
        symbol: "none",
        lineStyle: { color: "#f43f5e", width: 1.5 },
        areaStyle: { color: "rgba(244,63,94,0.1)" },
        data: [{ value: [96, 91, 88, 85, 94] }],
      },
    ],
  });
}

function tick() {
  if (!chart || chart.isDisposed()) return;
  const v = indicators.map(() => Math.round(80 + Math.random() * 20));
  const avg = Math.round(v.reduce((a, b) => a + b, 0) / v.length);
  val.value = avg;
  chart.setOption({ series: [{ data: [{ value: v }] }] });
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
  border-top: 1px solid rgb(244 63 94 / 40%);
  border-left: 1px solid rgb(244 63 94 / 40%);
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
