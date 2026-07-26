<template>
  <div class="panel p1">
    <div class="panel-hd"><span class="dot accent" />订单状态</div>
    <div ref="chartRef" class="chart-box" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";

const chartRef = ref<HTMLDivElement>();
import { echarts } from "@/plugins/echarts";

defineOptions({ name: "OrderStatusChart" });

let chart: echarts.ECharts | null = null;
let timer = 0;

const textStyle = { color: "#94a3b8" };
const categories = ["待付款", "待发货", "已发货", "已完成", "已取消"];

function initChart(dom: HTMLDivElement) {
  chart = echarts.init(dom);
  chart.setOption({
    grid: { top: 20, right: 20, bottom: 30, left: 60 },
    xAxis: {
      type: "category",
      data: categories,
      axisLine: { lineStyle: { color: "#1a2050" } },
      axisLabel: textStyle,
    },
    yAxis: {
      type: "value",
      splitLine: { lineStyle: { color: "#1a2050", type: "dashed" } },
      axisLabel: textStyle,
    },
    tooltip: {
      trigger: "axis" as const,
      backgroundColor: "#0f143c",
      borderColor: "#1a2050",
      textStyle: { color: "#e0e6ff" },
    },
    series: [
      {
        type: "bar",
        data: [45, 128, 256, 892, 32],
        itemStyle: {
          borderRadius: [4, 4, 0, 0],
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: "#7c3aed" },
            { offset: 1, color: "rgba(124,58,237,0.3)" },
          ]),
        },
        barWidth: "50%",
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
  const data = [
    Math.round(20 + Math.random() * 60),
    Math.round(60 + Math.random() * 150),
    Math.round(100 + Math.random() * 300),
    Math.round(500 + Math.random() * 600),
    Math.round(10 + Math.random() * 50),
  ];
  chart.setOption({ series: [{ data }] });
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
