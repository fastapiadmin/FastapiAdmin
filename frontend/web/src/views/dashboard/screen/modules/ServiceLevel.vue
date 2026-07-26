<template>
  <div class="panel p1">
    <div class="panel-hd"><span class="dot green" />API 响应时长(均值)</div>
    <div ref="chartRef" class="chart-box" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { echarts } from "@/plugins/echarts";

defineOptions({ name: "ServiceLevel" });

const chartRef = ref<HTMLDivElement>();
let chart: echarts.ECharts | null = null;
let timer = 0;

const textStyle = { color: "#94a3b8" };
const xData = [
  "08:00",
  "09:00",
  "10:00",
  "11:00",
  "12:00",
  "13:00",
  "14:00",
  "15:00",
  "16:00",
  "17:00",
];

function initChart(dom: HTMLDivElement) {
  chart = echarts.init(dom);
  chart.setOption({
    grid: { top: 20, right: 25, bottom: 25, left: 45 },
    xAxis: {
      type: "category",
      data: xData,
      boundaryGap: false,
      axisLine: { lineStyle: { color: "#1a2050" } },
      axisLabel: { ...textStyle, rotate: 30 },
    },
    yAxis: {
      type: "value",
      name: "ms",
      nameTextStyle: { color: "#94a3b8", fontSize: 10 },
      min: 20,
      max: 80,
      interval: 15,
      splitLine: { lineStyle: { color: "#1a2050", type: "dashed" } },
      axisLabel: textStyle,
    },
    tooltip: {
      trigger: "axis" as const,
      valueFormatter: (v: any) => v + "ms",
      backgroundColor: "#0f143c",
      borderColor: "#1a2050",
      textStyle: { color: "#e0e6ff" },
    },
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
            { offset: 0, color: "rgba(16,185,129,0.2)" },
            { offset: 1, color: "rgba(16,185,129,0)" },
          ]),
        },
        data: [52, 48, 55, 42, 65, 38, 45, 51, 58, 44],
      },
      {
        type: "line",
        smooth: true,
        symbol: "diamond",
        symbolSize: 3,
        lineStyle: { color: "#f59e0b", width: 1.5, type: "dashed" },
        itemStyle: { color: "#f59e0b" },
        data: [60, 55, 62, 50, 70, 45, 52, 58, 65, 50],
      },
    ],
  });
}

function handleResize() {
  if (chart && !chart.isDisposed()) chart.resize();
}

function tick() {
  if (!chart || chart.isDisposed()) return;
  const d1 = xData.map(() => Math.round(35 + Math.random() * 35));
  const d2 = xData.map(() => Math.round(42 + Math.random() * 30));
  chart.setOption({ series: [{ data: d1 }, { data: d2 }] });
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
