<template>
  <div class="panel p1 col-3">
    <div class="panel-hd"><span class="dot purple" />热销产品 TOP5</div>
    <div class="product-list">
      <div v-for="(p, i) in topProducts" :key="p.name" class="product-row">
        <span class="product-rank flex-cc" :class="'rank-' + (i + 1)">{{ i + 1 }}</span>
        <div class="product-info">
          <span class="product-name">{{ p.name }}</span>
          <span class="product-category">{{ p.category }}</span>
        </div>
        <span class="product-sales">¥{{ formatNumber(p.sales) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

defineOptions({ name: "TopProductList" });

const topProducts = ref([
  { name: "企业版 License", category: "软件服务", sales: 45200 },
  { name: "高级数据分析", category: "数据服务", sales: 32800 },
  { name: "API 接口调用", category: "接口服务", sales: 28600 },
  { name: "技术支持服务", category: "服务", sales: 15600 },
  { name: "定制开发", category: "定制", sales: 12400 },
]);

function formatNumber(num: number): string {
  return num.toLocaleString();
}
</script>

<style scoped>
.product-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow: auto;
}

.product-row {
  display: flex;
  gap: 8px;
  align-items: center;
  padding: 10px;
  background: rgb(12 18 48 / 60%);
  border-radius: 8px;
}

.product-rank {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  font-size: 10px;
  font-weight: 700;
  background: rgb(26 32 80 / 60%);
  border-radius: 50%;
}

.product-rank.rank-1 {
  color: #fff;
  background: #ef4444;
}

.product-rank.rank-2 {
  color: #fff;
  background: #f59e0b;
}

.product-rank.rank-3 {
  color: #fff;
  background: #3b82f6;
}

.product-info {
  flex: 1;
  min-width: 0;
}

.product-name {
  display: block;
  font-size: 13px;
  font-weight: 500;
}

.product-category {
  display: block;
  font-size: 11px;
  opacity: 0.5;
}

.product-sales {
  font-size: 14px;
  font-weight: 600;
  color: #00d4ff;
}
</style>
