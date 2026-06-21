<template>
  <div class="panel p1">
    <div class="panel-hd"><span class="dot green" />系统负载</div>
    <div class="gauge-row">
      <div v-for="g in gauges" :key="g.label" class="gauge-item">
        <div :ref="(el) => setGaugeRef(g.label, el)" class="chart-box-xs" />
        <span class="gauge-label">{{ g.label }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from "vue";
import * as echarts from "echarts";

defineOptions({ name: "SystemGauges" });

const gaugeRefs: Record<string, HTMLDivElement> = {};
const charts: echarts.ECharts[] = [];
let timer = 0;

const gauges = [
  { label: "CPU", value: 42 },
  { label: "内存", value: 61 },
  { label: "磁盘", value: 35 },
];

function setGaugeRef(label: string, el: unknown) {
  if (el instanceof HTMLDivElement) gaugeRefs[label] = el;
}

function waitForSize(el: HTMLDivElement): Promise<void> {
  return new Promise((resolve) => {
    if (el.clientWidth > 0 && el.clientHeight > 0) {
      resolve();
      return;
    }
    const check = () => {
      if (el.clientWidth > 0 && el.clientHeight > 0) {
        resolve();
      } else {
        requestAnimationFrame(check);
      }
    };
    requestAnimationFrame(check);
  });
}

async function initGauges() {
  const entries = Object.entries(gaugeRefs);
  await Promise.all(entries.map(([, el]) => waitForSize(el)));

  entries.forEach(([, el]) => {
    const chart = echarts.init(el);
    charts.push(chart);
    chart.setOption({
      series: [
        {
          type: "gauge",
          radius: "90%",
          center: ["50%", "60%"],
          startAngle: 210,
          endAngle: -30,
          min: 0,
          max: 100,
          detail: {
            formatter: "{value}%",
            fontSize: 12,
            color: "#e0e6ff",
            offsetCenter: [0, "65%"],
          },
          data: [{ value: 0 }],
          axisLine: {
            lineStyle: {
              width: 6,
              color: [
                [0.3, "#10b981"],
                [0.7, "#f59e0b"],
                [1, "#ef4444"],
              ],
            },
          },
          axisTick: { show: false },
          splitLine: { show: false },
          axisLabel: { show: false },
          pointer: { length: "55%", width: 3, itemStyle: { color: "#e0e6ff" } },
        },
      ],
    });
  });
}

function handleResize() {
  charts.forEach((c) => {
    if (!c.isDisposed()) c.resize();
  });
}

function tick() {
  const v = [
    clamp(gauges[0]!.value + (Math.random() - 0.5) * 8, 10, 90),
    clamp(gauges[1]!.value + (Math.random() - 0.5) * 6, 20, 95),
    clamp(gauges[2]!.value + (Math.random() - 0.5) * 3, 15, 85),
  ];
  gauges[0]!.value = Math.round(v[0]!);
  gauges[1]!.value = Math.round(v[1]!);
  gauges[2]!.value = Math.round(v[2]!);
  charts.forEach((c, i) => {
    if (!c.isDisposed()) c.setOption({ series: [{ data: [{ value: gauges[i]!.value }] }] });
  });
}

function clamp(v: number, min: number, max: number) {
  return Math.max(min, Math.min(max, v));
}

onMounted(() => {
  initGauges().then(() => {
    timer = window.setInterval(tick, 2000);
  });
  window.addEventListener("resize", handleResize);
});

onUnmounted(() => {
  clearInterval(timer);
  window.removeEventListener("resize", handleResize);
  charts.forEach((c) => c.dispose());
});
</script>

<style scoped>
.gauge-row {
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: space-around;
}

.gauge-item {
  display: flex;
  flex: 1;
  flex-direction: column;
  text-align: center;
}

.gauge-label {
  display: block;
  flex-shrink: 0;
  margin-top: -6px;
  font-size: 12px;
  opacity: 0.5;
}

.chart-box-xs {
  flex: 1;
  width: 100%;
  min-height: 0;
}
</style>
