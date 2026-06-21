<template>
  <div class="panel p1">
    <div class="panel-hd"><span class="dot accent" />销售趋势分析</div>
    <div ref="chartRef" class="chart-box" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";

const chartRef = ref<HTMLDivElement>();
import * as echarts from "echarts";

defineOptions({ name: "SalesTrendChart" });

let chart: echarts.ECharts | null = null;
let timer = 0;

const textStyle = { color: "#94a3b8" };
const tooltip = {
  trigger: "axis" as const,
  backgroundColor: "#0f143c",
  borderColor: "#1a2050",
  textStyle: { color: "#e0e6ff" },
};
const xData = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"];

function initChart(dom: HTMLDivElement) {
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
        name: "订单金额",
        type: "bar",
        stack: "total",
        data: [120, 132, 101, 134, 190, 230, 210],
        itemStyle: { color: "#00d4ff" },
      },
      {
        name: "退款金额",
        type: "bar",
        stack: "total",
        data: [20, 32, 11, 34, 90, 30, 10],
        itemStyle: { color: "#ef4444" },
      },
      {
        name: "实际收入",
        type: "bar",
        stack: "total",
        data: [100, 100, 90, 100, 100, 200, 200],
        itemStyle: { color: "#10b981" },
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
  const d1 = xData.map(() => Math.round(80 + Math.random() * 180));
  const d2 = d1.map((v) => Math.round(v * (0.05 + Math.random() * 0.25)));
  const d3 = d1.map((v, i) => Math.round(v - d2[i]!));
  chart.setOption({ series: [{ data: d1 }, { data: d2 }, { data: d3 }] });
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
