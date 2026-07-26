<template>
  <div class="panel p1">
    <div class="panel-hd"><span class="dot accent" />交易渠道占比</div>
    <div ref="chartRef" class="chart-box" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { echarts } from "@/plugins/echarts";

defineOptions({ name: "ChannelDonut" });

const chartRef = ref<HTMLDivElement>();
let chart: echarts.ECharts | null = null;
let timer = 0;

function initChart(dom: HTMLDivElement) {
  chart = echarts.init(dom);
  chart.setOption({
    tooltip: {
      trigger: "item" as const,
      backgroundColor: "#0f143c",
      borderColor: "#1a2050",
      textStyle: { color: "#e0e6ff", fontSize: 10 },
      formatter: "{b}: {c}万 ({d}%)",
    },
    legend: {
      bottom: 0,
      textStyle: { color: "#94a3b8", fontSize: 9 },
      itemWidth: 8,
      itemHeight: 8,
    },
    series: [
      {
        type: "pie",
        radius: ["50%", "70%"],
        center: ["50%", "45%"],
        label: { show: false },
        emphasis: {
          scaleSize: 6,
          label: { show: true, fontSize: 10, color: "#94a3b8", formatter: "{b}\n{d}%" },
        },
        itemStyle: { borderColor: "#060b24", borderWidth: 2 },
        data: [
          { value: 48.5, name: "微信支付", itemStyle: { color: "#00d4ff" } },
          { value: 28.3, name: "支付宝", itemStyle: { color: "#7c3aed" } },
          { value: 15.2, name: "银联云闪付", itemStyle: { color: "#10b981" } },
          { value: 8.0, name: "其他", itemStyle: { color: "#f59e0b" } },
        ],
      },
    ],
  });
}

function handleResize() {
  if (chart && !chart.isDisposed()) chart.resize();
}

function tick() {
  if (!chart || chart.isDisposed()) return;
  const r1 = +(40 + Math.random() * 15).toFixed(1);
  const r2 = +(22 + Math.random() * 12).toFixed(1);
  const r3 = +(10 + Math.random() * 10).toFixed(1);
  const r4 = +(100 - +r1 - +r2 - +r3).toFixed(1);
  chart.setOption({
    series: [{ data: [{ value: r1 }, { value: r2 }, { value: r3 }, { value: r4 }] }],
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
