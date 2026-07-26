<template>
  <div class="panel p1">
    <div class="panel-hd"><span class="dot green" />用户画像分析</div>
    <div ref="chartRef" class="chart-box" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { echarts } from "@/plugins/echarts";

defineOptions({ name: "UserProfile" });

const chartRef = ref<HTMLDivElement>();
let chart: echarts.ECharts | null = null;
let timer = 0;

const indicators = [
  { name: "消费力", max: 100 },
  { name: "活跃度", max: 100 },
  { name: "复购率", max: 100 },
  { name: "客单价", max: 100 },
  { name: "满意度", max: 100 },
];

function initChart(dom: HTMLDivElement) {
  chart = echarts.init(dom);
  chart.setOption({
    legend: {
      bottom: 0,
      textStyle: { color: "#94a3b8", fontSize: 8 },
      itemWidth: 8,
      itemHeight: 8,
    },
    radar: {
      center: ["50%", "48%"],
      radius: "55%",
      indicator: indicators,
      axisName: { color: "#94a3b8", fontSize: 8 },
      splitArea: { areaStyle: { color: ["rgba(0,212,255,0.02)", "rgba(0,212,255,0.02)"] } },
      splitLine: { lineStyle: { color: "#1a2050" } },
      axisLine: { lineStyle: { color: "#1a2050" } },
    },
    series: [
      {
        type: "radar",
        symbol: "circle",
        symbolSize: 3,
        lineStyle: { color: "#00d4ff", width: 2 },
        areaStyle: { color: "rgba(0,212,255,0.12)" },
        itemStyle: { color: "#00d4ff" },
        data: [{ value: [82, 78, 65, 58, 88], name: "高价值客群" }],
      },
      {
        type: "radar",
        symbol: "triangle",
        symbolSize: 3,
        lineStyle: { color: "#f59e0b", width: 1.5, type: "dashed" },
        areaStyle: { color: "rgba(245,158,11,0.06)" },
        itemStyle: { color: "#f59e0b" },
        data: [{ value: [55, 72, 48, 42, 78], name: "潜力客群" }],
      },
    ],
  });
}

function handleResize() {
  if (chart && !chart.isDisposed()) chart.resize();
}

function tick() {
  if (!chart || chart.isDisposed()) return;
  const v1 = indicators.map(() => Math.round(53 + Math.random() * 42));
  const v2 = indicators.map(() => Math.round(38 + Math.random() * 45));
  chart.setOption({ series: [{ data: [{ value: v1 }] }, { data: [{ value: v2 }] }] });
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
