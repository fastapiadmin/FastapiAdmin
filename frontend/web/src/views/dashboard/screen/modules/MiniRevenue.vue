<template>
  <div class="mini-chart-panel">
    <div class="mc-hd">当日交易额</div>
    <div class="mc-value" style="color: #00d4ff">¥{{ val }}<span class="mc-unit">万</span></div>
    <div ref="chartRef" class="mc-chart" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { echarts } from "@/plugins/echarts";

defineOptions({ name: "MiniRevenue" });

const chartRef = ref<HTMLDivElement>();
let chart: echarts.ECharts | null = null;
let timer = 0;
const val = ref(128.6);

function initChart(dom: HTMLDivElement) {
  chart = echarts.init(dom);
  chart.setOption({
    series: [
      {
        type: "gauge",
        startAngle: 210,
        endAngle: -30,
        center: ["50%", "58%"],
        radius: "78%",
        min: 0,
        max: 200,
        axisLine: {
          lineStyle: {
            width: 6,
            color: [
              [0.5, "#00d4ff"],
              [0.8, "#7c3aed"],
              [1, "#ef4444"],
            ],
          },
        },
        pointer: { length: "55%", width: 3, itemStyle: { color: "#00d4ff" } },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { show: false },
        detail: {
          valueAnimation: true,
          fontSize: 14,
          fontWeight: 700,
          color: "#00d4ff",
          offsetCenter: [0, "42%"],
          formatter: "",
        },
        data: [{ value: 128.6 }],
      },
    ],
  });
}

function tick() {
  if (!chart || chart.isDisposed()) return;
  const n = +(105 + Math.random() * 50).toFixed(1);
  val.value = n;
  chart.setOption({ series: [{ data: [{ value: n }] }] });
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
});
onUnmounted(() => {
  clearInterval(timer);
  chart?.dispose();
});
</script>

<style scoped>
.mini-chart-panel {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 10px 12px;
  overflow: hidden;
  background: linear-gradient(180deg, rgb(0 30 80 / 55%) 0%, rgb(6 11 36 / 70%) 100%);
  border: 1px solid var(--border, rgb(0 180 255 / 12%));
  border-radius: 10px;
}

.mini-chart-panel::after {
  position: absolute;
  top: 4px;
  left: 4px;
  width: 6px;
  height: 6px;
  content: "";
  border-top: 1px solid rgb(0 212 255 / 40%);
  border-left: 1px solid rgb(0 212 255 / 40%);
}

.mc-hd {
  margin-bottom: 2px;
  font-size: 10px;
  opacity: 0.35;
}

.mc-value {
  margin-bottom: 0;
  font-size: 16px;
  font-weight: 700;
  line-height: 1;
}

.mc-unit {
  margin-left: 2px;
  font-size: 9px;
  font-weight: 400;
  opacity: 0.4;
}

.mc-chart {
  flex: 1;
  min-height: 0;
}
</style>
