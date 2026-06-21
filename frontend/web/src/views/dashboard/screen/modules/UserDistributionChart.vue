<template>
  <div class="panel p1">
    <div class="panel-hd"><span class="dot purple" />用户分布</div>
    <div ref="chartRef" class="chart-box-sm" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";

const chartRef = ref<HTMLDivElement>();
import * as echarts from "echarts";

defineOptions({ name: "UserDistributionChart" });

let chart: echarts.ECharts | null = null;
let timer = 0;

const textStyle = { color: "#94a3b8" };
const names = ["管理员", "普通用户", "访客", "其他"];

function initChart(dom: HTMLDivElement) {
  chart = echarts.init(dom);
  chart.setOption({
    series: [
      {
        type: "pie",
        radius: ["55%", "80%"],
        center: ["50%", "55%"],
        label: { show: false },
        data: [
          { value: 620, name: "管理员", itemStyle: { color: "#00d4ff" } },
          { value: 450, name: "普通用户", itemStyle: { color: "#7c3aed" } },
          { value: 180, name: "访客", itemStyle: { color: "#f59e0b" } },
          { value: 292, name: "其他", itemStyle: { color: "#10b981" } },
        ],
      },
    ],
    tooltip: {
      trigger: "item",
      backgroundColor: "#0f143c",
      borderColor: "#1a2050",
      textStyle: { color: "#e0e6ff" },
    },
    legend: {
      orient: "vertical",
      right: 10,
      top: "center",
      textStyle,
      itemWidth: 10,
      itemHeight: 10,
    },
  });
}

function handleResize() {
  if (!chart || chart.isDisposed()) return;
  chart.resize();
}

function tick() {
  if (!chart || chart.isDisposed()) return;
  const data = names.map((name) => ({
    value: Math.round(100 + Math.random() * 600),
    name,
    itemStyle: (
      chart as unknown as {
        getOption: () => { series: [{ data: { name: string; itemStyle?: unknown }[] }] };
      }
    )
      .getOption()
      .series[0].data?.find((d: { name: string }) => d.name === name)?.itemStyle,
  }));
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
.chart-box-sm {
  flex: 1;
  width: 100%;
  min-height: 0;
}
</style>
