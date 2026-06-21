<template>
  <div class="panel p1">
    <div class="panel-hd"><span class="dot accent" />访问趋势</div>
    <div ref="chartRef" class="chart-box" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";

const chartRef = ref<HTMLDivElement>();
import * as echarts from "echarts";

defineOptions({ name: "VisitTrendChart" });

let chart: echarts.ECharts | null = null;
let timer = 0;

const textStyle = { color: "#94a3b8" };
const tooltip = {
  trigger: "axis" as const,
  backgroundColor: "#0f143c",
  borderColor: "#1a2050",
  textStyle: { color: "#e0e6ff" },
};
const xData = [
  "00:00",
  "02:00",
  "04:00",
  "06:00",
  "08:00",
  "10:00",
  "12:00",
  "14:00",
  "16:00",
  "18:00",
  "20:00",
  "22:00",
];
let pv = [120, 85, 60, 45, 200, 380, 450, 520, 480, 380, 300, 200];
let uv = [80, 55, 40, 30, 140, 260, 320, 380, 350, 270, 220, 150];

function initChart(dom: HTMLDivElement) {
  if (!dom) return;
  chart = echarts.init(dom);
  chart.setOption({
    grid: { top: 20, right: 30, bottom: 30, left: 50 },
    xAxis: {
      type: "category",
      data: xData,
      axisLine: { lineStyle: { color: "#1a2050" } },
      axisLabel: textStyle,
    },
    yAxis: {
      type: "value",
      splitLine: { lineStyle: { color: "#1a2050", type: "dashed" } },
      axisLabel: textStyle,
    },
    tooltip,
    legend: { textStyle, top: 0 },
    series: [
      {
        name: "PV",
        type: "line",
        smooth: true,
        symbol: "circle",
        symbolSize: 6,
        lineStyle: { color: "#00d4ff", width: 2 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: "rgba(0,212,255,0.3)" },
            { offset: 1, color: "rgba(0,212,255,0.02)" },
          ]),
        },
        itemStyle: { color: "#00d4ff" },
        data: pv,
      },
      {
        name: "UV",
        type: "line",
        smooth: true,
        symbol: "circle",
        symbolSize: 6,
        lineStyle: { color: "#7c3aed", width: 2 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: "rgba(124,58,237,0.3)" },
            { offset: 1, color: "rgba(124,58,237,0.02)" },
          ]),
        },
        itemStyle: { color: "#7c3aed" },
        data: uv,
      },
    ],
  });
}

function handleResize() {
  if (!chart || chart.isDisposed()) return;
  chart.resize();
}

function tick() {
  if (!chart || chart.isDisposed()) return;
  pv.push(Math.round(pv[pv.length - 1]! * (0.85 + Math.random() * 0.3)));
  uv.push(Math.round(uv[uv.length - 1]! * (0.85 + Math.random() * 0.3)));
  pv.shift();
  uv.shift();
  chart.setOption({
    series: [{ data: pv }, { data: uv }],
  });
}

onMounted(() => {
  const el = chartRef.value;
  if (!el) return;

  const observer = new ResizeObserver((entries) => {
    const entry = entries[0];
    if (entry && entry.contentRect.width > 0 && entry.contentRect.height > 0) {
      observer.disconnect();
      initChart(el);
      timer = window.setInterval(tick, 3000);
    }
  });
  observer.observe(el);
  window.addEventListener("resize", handleResize);
});

onUnmounted(() => {
  clearInterval(timer);
  window.removeEventListener("resize", handleResize);
  chart?.dispose();
});
</script>

<style scoped>
.chart-box {
  flex: 1;
  width: 100%;
  min-height: 0;
}
</style>
