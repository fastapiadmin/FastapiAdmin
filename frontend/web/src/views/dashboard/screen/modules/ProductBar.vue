<template>
  <div class="panel p1">
    <div class="panel-hd"><span class="dot green" />热销品类排行 TOP6</div>
    <div ref="chartRef" class="chart-box" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { echarts } from "@/plugins/echarts";

defineOptions({ name: "ProductBar" });

const chartRef = ref<HTMLDivElement>();
let chart: echarts.ECharts | null = null;
let timer = 0;

const products = ["手机数码", "电脑办公", "家用电器", "美妆护肤", "服饰鞋包", "食品生鲜"];
const textStyle = { color: "#94a3b8", fontSize: 10 };

function initChart(dom: HTMLDivElement) {
  chart = echarts.init(dom);
  chart.setOption({
    grid: { top: 5, right: 40, bottom: 10, left: 10, outerBounds: true },
    xAxis: { type: "value", splitLine: { lineStyle: { color: "#1a2050" } }, axisLabel: textStyle },
    yAxis: {
      type: "category",
      data: products,
      inverse: true,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { ...textStyle, width: 64, overflow: "truncate" },
    },
    series: [
      {
        type: "bar",
        barWidth: 10,
        itemStyle: {
          borderRadius: [0, 3, 3, 0],
          color: (p: any) =>
            ["#00d4ff", "#7c3aed", "#10b981", "#f59e0b", "#ef4444", "#ec4899"][p.dataIndex % 6],
        },
        label: {
          show: true,
          position: "right",
          color: "#94a3b8",
          fontSize: 10,
          formatter: "{c}单",
        },
        data: [892, 651, 534, 412, 298, 187],
      },
    ],
  });
}

function handleResize() {
  if (chart && !chart.isDisposed()) chart.resize();
}

function tick() {
  if (!chart || chart.isDisposed()) return;
  const data = products.map(() => Math.round(120 + Math.random() * 800));
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
