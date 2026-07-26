<template>
  <div class="panel p1">
    <div class="panel-hd"><span class="dot accent" />地域分布</div>
    <div ref="chartRef" class="chart-box" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { echarts } from "@/plugins/echarts";

defineOptions({ name: "RegionDistributionChart" });

const chartRef = ref<HTMLDivElement>();
let chart: echarts.ECharts | null = null;

const textStyle = { color: "#94a3b8" };

function initChart() {
  if (!chartRef.value) return;
  chart = echarts.init(chartRef.value);
  chart.setOption({
    grid: { top: 20, right: 20, bottom: 30, left: 50 },
    xAxis: {
      type: "category",
      data: ["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉", "南京"],
      axisLabel: { color: "#94a3b8", rotate: 30 },
      axisLine: { lineStyle: { color: "#1a2050" } },
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
        data: [280, 220, 180, 150, 130, 95, 80, 65],
        itemStyle: {
          borderRadius: [4, 4, 0, 0],
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: "#00d4ff" },
            { offset: 1, color: "rgba(0,212,255,0.3)" },
          ]),
        },
        barWidth: 22,
      },
    ],
  });
}

function handleResize() {
  if (!chart || chart.isDisposed()) return;
  chart.resize();
}

onMounted(() => {
  const el = chartRef.value;
  if (!el) return;

  const observer = new ResizeObserver((entries) => {
    const entry = entries[0];
    if (entry && entry.contentRect.width > 0 && entry.contentRect.height > 0) {
      observer.disconnect();
      initChart();
    }
  });
  observer.observe(el);
  window.addEventListener("resize", handleResize);
});

onUnmounted(() => {
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
