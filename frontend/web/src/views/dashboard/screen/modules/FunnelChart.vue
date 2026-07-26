<template>
  <div class="panel p1">
    <div class="panel-hd"><span class="dot purple" />用户转化漏斗</div>
    <div class="funnel-list">
      <div v-for="(item, i) in data" :key="item.label" class="fn-item">
        <div class="fn-row">
          <span class="fn-idx" :style="{ background: colors[i] }">{{ i + 1 }}</span>
          <span class="fn-label">{{ item.label }}</span>
          <span class="fn-val">{{ item.value }}</span>
          <span class="fn-rate" :style="{ color: colors[i] }">转化率 {{ item.rate }}%</span>
        </div>
        <div class="fn-bar-wrap">
          <div class="fn-bar" :style="{ width: item.pct + '%', background: colors[i] }" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted, onUnmounted } from "vue";

defineOptions({ name: "FunnelChart" });

const colors = ["#00d4ff", "#7c3aed", "#10b981", "#f59e0b"];

const data = reactive([
  { label: "曝光", value: "12,850", rate: 100, pct: 100 },
  { label: "点击", value: "4,320", rate: 34, pct: 34 },
  { label: "下单", value: "1,845", rate: 14, pct: 14 },
  { label: "支付", value: "963", rate: 8, pct: 8 },
]);

let timer = 0;

function tick() {
  const bases = [12850, 4320, 1845, 963];
  const vals = bases.map((b, i) => Math.round(b + (Math.random() - 0.5) * b * 0.08 * (4 - i)));
  const max = vals[0]!;
  data.forEach((item, i) => {
    item.value = vals[i]!.toLocaleString();
    item.rate = Math.round((vals[i]! / max) * 100);
    item.pct = (vals[i]! / max) * 100;
  });
}

onMounted(() => {
  tick();
  timer = window.setInterval(tick, 5000);
});
onUnmounted(() => clearInterval(timer));
</script>

<style scoped>
.funnel-list {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 5px;
  justify-content: center;
}

.fn-item {
  padding: 2px 0;
}

.fn-row {
  display: flex;
  gap: 6px;
  align-items: center;
  margin-bottom: 3px;
  font-size: 10px;
}

.fn-idx {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 14px;
  height: 14px;
  font-size: 8px;
  font-weight: 700;
  color: #fff;
  border-radius: 3px;
}

.fn-label {
  flex-shrink: 0;
  width: 28px;
  opacity: 0.5;
}

.fn-val {
  flex: 1;
  font-variant-numeric: tabular-nums;
  text-align: right;
  opacity: 0.8;
}

.fn-rate {
  flex-shrink: 0;
  width: 54px;
  font-size: 9px;
  font-weight: 600;
  text-align: right;
}

.fn-bar-wrap {
  height: 3px;
  overflow: hidden;
  background: rgb(26 40 80 / 40%);
  border-radius: 2px;
}

.fn-bar {
  height: 100%;
  border-radius: 2px;
  transition: width 0.8s;
}
</style>
