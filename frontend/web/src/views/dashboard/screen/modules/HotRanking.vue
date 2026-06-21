<template>
  <div class="panel p1">
    <div class="panel-hd">
      <span class="dot warn" />热门排行
      <span class="rank-badge">实时</span>
    </div>
    <div class="rank-list">
      <div v-for="(item, i) in list" :key="item.name" class="rank-row">
        <span class="rank-idx" :class="'top' + (i + 1)">{{ i + 1 }}</span>
        <span class="rank-name">{{ item.name }}</span>
        <span class="rank-bar-wrap">
          <span
            class="rank-bar"
            :style="{ width: item.ratio * 100 + '%', background: item.color }"
          />
        </span>
        <span class="rank-val">{{ item.value }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted, onUnmounted } from "vue";

defineOptions({ name: "HotRanking" });

const colors = [
  "#00d4ff",
  "#7c3aed",
  "#10b981",
  "#f59e0b",
  "#ef4444",
  "#ec4899",
  "#06b6d4",
  "#f97316",
];

const list = reactive([
  { name: "iPhone 15 Pro", value: "892单", ratio: 0, color: colors[0] },
  { name: "MacBook Air M3", value: "651单", ratio: 0, color: colors[1] },
  { name: "AirPods Pro 2", value: "534单", ratio: 0, color: colors[2] },
  { name: "iPad Mini 7", value: "412单", ratio: 0, color: colors[3] },
  { name: "Apple Watch S9", value: "298单", ratio: 0, color: colors[4] },
  { name: "Samsung S24 Ultra", value: "187单", ratio: 0, color: colors[5] },
  { name: "华为 Mate 60 Pro", value: "165单", ratio: 0, color: colors[6] },
  { name: "Sony WH-1000XM5", value: "142单", ratio: 0, color: colors[7] },
]);

let timer = 0;

function tick() {
  const vals = list.map(() => Math.round(100 + Math.random() * 800));
  const max = Math.max(...vals);
  list.forEach((item, i) => {
    item.value = vals[i]! + "单";
    item.ratio = vals[i]! / max;
  });
  list.sort((a, b) => parseInt(b.value) - parseInt(a.value));
}

onMounted(() => {
  tick();
  timer = window.setInterval(tick, 5000);
});
onUnmounted(() => clearInterval(timer));
</script>

<style scoped>
.rank-list {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 5px;
  overflow: auto;
}

.rank-row {
  display: flex;
  gap: 8px;
  align-items: center;
  font-size: 11px;
}

.rank-idx {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  font-size: 10px;
  font-weight: 700;
  background: rgb(26 40 80 / 60%);
  border-radius: 4px;
}

.rank-idx.top1 {
  color: #00d4ff;
  background: rgb(0 212 255 / 20%);
}

.rank-idx.top2 {
  color: #7c3aed;
  background: rgb(124 58 237 / 20%);
}

.rank-idx.top3 {
  color: #10b981;
  background: rgb(16 185 129 / 20%);
}

.rank-name {
  flex-shrink: 0;
  width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.rank-bar-wrap {
  flex: 1;
  height: 5px;
  overflow: hidden;
  background: rgb(26 40 80 / 40%);
  border-radius: 3px;
}

.rank-bar {
  display: block;
  height: 100%;
  border-radius: 3px;
  transition: width 0.6s;
}

.rank-val {
  flex-shrink: 0;
  font-size: 11px;
  font-variant-numeric: tabular-nums;
  opacity: 0.7;
}

.rank-badge {
  padding: 2px 8px;
  margin-left: auto;
  font-size: 10px;
  color: #f59e0b;
  background: rgb(245 158 11 / 15%);
  border-radius: 10px;
  opacity: 0.5;
  animation: blink 2s infinite;
}
@keyframes blink {
  0%,
  100% {
    opacity: 0.5;
  }

  50% {
    opacity: 1;
  }
}
</style>
