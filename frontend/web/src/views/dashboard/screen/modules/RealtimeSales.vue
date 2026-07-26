<template>
  <div class="panel p1">
    <div class="panel-hd"><span class="dot accent" />实时销售分时</div>
    <div ref="chartRef" class="chart-box" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { echarts } from "@/plugins/echarts";

defineOptions({ name: "RealtimeSales" });

const chartRef = ref<HTMLDivElement>();
let chart: echarts.ECharts | null = null;
let timer = 0;

const textStyle = { color: "#94a3b8" };
const hours = [
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
  "18:00",
  "19:00",
  "20:00",
];

function initChart(dom: HTMLDivElement) {
  chart = echarts.init(dom);
  chart.setOption({
    grid: { top: 20, right: 30, bottom: 30, left: 55 },
    xAxis: {
      type: "category",
      data: hours,
      axisLine: { lineStyle: { color: "#1a2050" } },
      axisLabel: { ...textStyle, rotate: 30 },
    },
    yAxis: {
      type: "value",
      name: "万元",
      nameTextStyle: { color: "#94a3b8", fontSize: 11 },
      splitLine: { lineStyle: { color: "#1a2050", type: "dashed" } },
      axisLabel: textStyle,
    },
    tooltip: {
      trigger: "axis" as const,
      backgroundColor: "#0f143c",
      borderColor: "#1a2050",
      textStyle: { color: "#e0e6ff" },
    },
    legend: { textStyle, top: 0 },
    series: [
      {
        name: "销售额",
        type: "bar",
        barWidth: "60%",
        itemStyle: {
          borderRadius: [4, 4, 0, 0],
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: "#00d4ff" },
            { offset: 1, color: "rgba(0,212,255,0.25)" },
          ]),
        },
        data: [2.1, 3.5, 4.2, 5.8, 3.2, 2.8, 4.5, 5.1, 6.3, 8.2, 4.8, 3.2, 2.5],
      },
      {
        name: "订单数",
        type: "line",
        smooth: true,
        symbol: "circle",
        symbolSize: 5,
        lineStyle: { color: "#f59e0b", width: 2 },
        itemStyle: { color: "#f59e0b" },
        data: [18, 32, 45, 52, 35, 28, 42, 48, 55, 72, 48, 35, 22],
      },
    ],
  });
}

function handleResize() {
  if (chart && !chart.isDisposed()) chart.resize();
}

function tick() {
  if (!chart || chart.isDisposed()) return;
  const sales = hours.map(() => +(1.5 + Math.random() * 7).toFixed(1));
  const orders = hours.map(() => Math.round(15 + Math.random() * 60));
  chart.setOption({ series: [{ data: sales }, { data: orders }] });
}

onMounted(() => {
  const el = chartRef.value;
  if (!el) return;

  const observer = new ResizeObserver((entries) => {
    const entry = entries[0];
    if (entry && entry.contentRect.width > 0 && entry.contentRect.height > 0) {
      observer.disconnect();
      initChart(el);
      timer = window.setInterval(tick, 3500);
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
