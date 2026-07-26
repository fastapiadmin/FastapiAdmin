<template>
  <div class="panel p1">
    <div class="panel-hd"><span class="dot accent" />今日概览</div>
    <div class="overview-grid">
      <div v-for="item in data" :key="item.label" class="ov-card">
        <div class="ov-label">{{ item.label }}</div>
        <div class="ov-value" :style="{ color: item.color }">
          <span class="ov-count">{{ item.value }}</span>
          <span class="ov-unit">{{ item.unit }}</span>
        </div>
        <div class="ov-change" :class="item.up ? 'up' : 'down'">
          {{ item.up ? "▲" : "▼" }} {{ item.change }}
          <span class="ov-compare">较昨日</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted, onUnmounted } from "vue";

defineOptions({ name: "TodayOverview" });

const data = reactive([
  {
    label: "总销售额",
    value: "99.9",
    unit: "万",
    color: "#00d4ff",
    change: "12.5%",
    up: true,
    base: 999000,
  },
  {
    label: "订单量",
    value: "2,356",
    unit: "",
    color: "#7c3aed",
    change: "8.2%",
    up: true,
    base: 2356,
  },
  {
    label: "活跃用户",
    value: "1,286",
    unit: "",
    color: "#10b981",
    change: "3.1%",
    up: true,
    base: 1286,
  },
  {
    label: "转化率",
    value: "3.82",
    unit: "%",
    color: "#f59e0b",
    change: "1.2%",
    up: false,
    base: 3.82,
  },
]);

let timer = 0;

function tick() {
  const orders = data[1]!.base + Math.round((Math.random() - 0.5) * 80);
  const users = data[2]!.base + Math.round((Math.random() - 0.5) * 60);
  data[0]!.base = orders * 420 + Math.round(Math.random() * 10000);
  data[1]!.base = orders;
  data[2]!.base = users;
  data[3]!.base = +(3.5 + Math.random() * 2).toFixed(2);
  data[0]!.value = (data[0]!.base / 10000).toFixed(1);
  data[1]!.value = data[1]!.base.toLocaleString();
  data[2]!.value = data[2]!.base.toLocaleString();
  data[3]!.value = data[3]!.base.toFixed(2);
  for (const d of data) {
    d.change = (Math.random() * 15 - 3).toFixed(1) + "%";
    d.up = Math.random() > 0.4;
  }
}

onMounted(() => {
  tick();
  timer = window.setInterval(tick, 4000);
});
onUnmounted(() => clearInterval(timer));
</script>

<style scoped>
.overview-grid {
  display: grid;
  flex: 1;
  grid-template-rows: 1fr 1fr;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
}

.ov-card {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 10px 12px;
  background: linear-gradient(135deg, rgb(0 212 255 / 4%) 0%, rgb(0 20 60 / 30%) 100%);
  border: 1px solid rgb(0 180 255 / 6%);
  border-radius: 8px;
}

.ov-label {
  margin-bottom: 2px;
  font-size: 10px;
  opacity: 0.35;
}

.ov-value {
  display: flex;
  gap: 3px;
  align-items: baseline;
  margin-bottom: 3px;
}

.ov-count {
  font-size: 20px;
  font-weight: 700;
  line-height: 1;
}

.ov-unit {
  font-size: 11px;
  opacity: 0.5;
}

.ov-change {
  font-size: 10px;
}

.ov-change.up {
  color: #10b981;
}

.ov-change.down {
  color: #f59e0b;
}

.ov-compare {
  margin-left: 3px;
  opacity: 0.4;
}
</style>
