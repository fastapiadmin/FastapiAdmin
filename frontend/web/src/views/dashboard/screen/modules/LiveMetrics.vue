<template>
  <div class="panel p1">
    <div class="panel-hd"><span class="dot warn" />服务健康度</div>
    <div class="metric-list">
      <div v-for="m in metrics" :key="m.label" class="metric-row">
        <div class="mr-label">{{ m.label }}</div>
        <div class="mr-value" :style="{ color: m.color }">
          {{ m.value }}<span class="mr-unit">{{ m.unit }}</span>
        </div>
        <div class="mr-bar-wrap">
          <div ref="barRefs" class="mr-bar" :style="{ width: m.pct + '%', background: m.color }" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted, onUnmounted } from "vue";

defineOptions({ name: "LiveMetrics" });

const metrics = reactive([
  { label: "QPS(每秒请求)", value: "3.2", unit: "K", color: "#00d4ff", pct: 0, base: 3200 },
  { label: "P99 耗时", value: "12", unit: "ms", color: "#7c3aed", pct: 0, base: 12 },
  { label: "错误率", value: "0.03", unit: "%", color: "#ef4444", pct: 0, base: 0.03 },
  { label: "服务可用率", value: "99.99", unit: "%", color: "#10b981", pct: 0, base: 99.99 },
]);

let timer = 0;

function tick() {
  metrics[0]!.base = Math.round(2800 + Math.random() * 800);
  metrics[1]!.base = Math.round(8 + Math.random() * 20);
  metrics[2]!.base = +(0.01 + Math.random() * 0.08).toFixed(2);
  metrics[3]!.base = +(99.95 + Math.random() * 0.05).toFixed(2);
  metrics[0]!.value = (metrics[0]!.base / 1000).toFixed(1);
  metrics[1]!.value = String(metrics[1]!.base);
  metrics[2]!.value = String(metrics[2]!.base);
  metrics[3]!.value = String(metrics[3]!.base);
  metrics[0]!.pct = (metrics[0]!.base / 4000) * 100;
  metrics[1]!.pct = (metrics[1]!.base / 30) * 100;
  metrics[2]!.pct = (metrics[2]!.base / 0.1) * 100;
  metrics[3]!.pct = (+(metrics[3]!.base - 99.9) / 0.1) * 100;
}

onMounted(() => {
  tick();
  timer = window.setInterval(tick, 3000);
});
onUnmounted(() => clearInterval(timer));
</script>

<style scoped>
.metric-list {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 4px;
  justify-content: center;
}

.metric-row {
  padding: 2px 0;
}

.mr-label {
  margin-bottom: 2px;
  font-size: 10px;
  opacity: 0.35;
}

.mr-value {
  margin-bottom: 3px;
  font-size: 18px;
  font-weight: 700;
  line-height: 1;
}

.mr-unit {
  margin-left: 2px;
  font-size: 10px;
  font-weight: 400;
  opacity: 0.4;
}

.mr-bar-wrap {
  height: 2px;
  overflow: hidden;
  background: rgb(26 40 80 / 40%);
  border-radius: 1px;
}

.mr-bar {
  height: 100%;
  border-radius: 1px;
  transition: width 0.8s;
}
</style>
