<template>
  <div class="panel p1">
    <div class="panel-hd"><span class="dot purple" />业绩目标达成率</div>
    <div ref="chartRef" class="chart-box" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { echarts } from "@/plugins/echarts";

defineOptions({ name: "TargetReality" });

const chartRef = ref<HTMLDivElement>();
let chart: echarts.ECharts | null = null;
let timer = 0;

const categories = ["华东区", "华南区", "华北区", "西南区"];
const textStyle = { color: "#94a3b8", fontSize: 10 };

function initChart(dom: HTMLDivElement) {
  chart = echarts.init(dom);
  chart.setOption({
    grid: { top: 5, right: 30, bottom: 10, left: 10, outerBounds: true },
    xAxis: {
      type: "value",
      max: 150,
      splitLine: { lineStyle: { color: "#1a2050" } },
      axisLabel: textStyle,
    },
    yAxis: {
      type: "category",
      data: categories,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: textStyle,
    },
    legend: {
      textStyle: { color: "#94a3b8", fontSize: 10 },
      top: 0,
      right: 0,
      itemWidth: 10,
      itemHeight: 8,
    },
    series: [
      {
        name: "目标",
        type: "bar",
        barWidth: 8,
        itemStyle: {
          borderRadius: [0, 2, 2, 0],
          color: "rgba(0,212,255,0.35)",
          borderColor: "#00d4ff",
          borderWidth: 1,
        },
        data: [120, 100, 80, 60],
      },
      {
        name: "已完成",
        type: "bar",
        barWidth: 8,
        itemStyle: { borderRadius: [0, 2, 2, 0], color: "#7c3aed" },
        data: [112, 88, 75, 52],
      },
    ],
  });
}

function handleResize() {
  if (chart && !chart.isDisposed()) chart.resize();
}

function tick() {
  if (!chart || chart.isDisposed()) return;
  const targets = [120, 100, 80, 60];
  const actual = targets.map((t) => Math.round(t * (0.7 + Math.random() * 0.25)));
  chart.setOption({ series: [{}, { data: actual }] });
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
