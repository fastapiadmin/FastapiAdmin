<template>
  <div class="workplace-container">
    <!-- 电商模块 -->
    <div class="card-group">
      <ElRow :gutter="20">
        <ElCol :sm="24" :md="24" :lg="16"><Banner /></ElCol>
        <ElCol :sm="12" :md="12" :lg="4"><TotalOrderVolume /></ElCol>
        <ElCol :sm="12" :md="12" :lg="4"><TotalProducts /></ElCol>
      </ElRow>
      <ElRow :gutter="20">
        <ElCol :sm="12" :md="12" :lg="8"><SalesTrend /></ElCol>
        <ElCol :sm="12" :md="12" :lg="8"><SalesClassification /></ElCol>
        <ElCol :sm="24" :md="24" :lg="8">
          <ElRow :gutter="20" class="card-row">
            <ElCol :sm="24" :md="12" :lg="12"><ProductSales /></ElCol>
            <ElCol :sm="24" :md="12" :lg="12"><SalesGrowth /></ElCol>
            <ElCol :span="24"><CartConversionRate /></ElCol>
          </ElRow>
        </ElCol>
      </ElRow>
    </div>

    <!-- 用户分析 -->
    <div class="card-group">
      <ElRow :gutter="20">
        <ElCol :sm="24" :md="12" :lg="10"><ActiveUser /></ElCol>
        <ElCol :sm="24" :md="12" :lg="14"><SalesOverview /></ElCol>
      </ElRow>
      <ElRow :gutter="20">
        <ElCol :sm="24" :md="24" :lg="12"><NewUser /></ElCol>
        <ElCol :sm="24" :md="12" :lg="6"><Dynamic /></ElCol>
        <ElCol :sm="24" :md="12" :lg="6"><TodoList /></ElCol>
      </ElRow>
      <ElRow :gutter="20">
        <ElCol :sm="24" :md="12" :lg="8"><HotCommodity /></ElCol>
        <ElCol :sm="24" :md="12" :lg="8"><AnnualSales /></ElCol>
        <ElCol :sm="24" :md="24" :lg="8"><TransactionList /></ElCol>
      </ElRow>
      <ElRow :gutter="20">
        <ElCol :md="24" :lg="8"><RecentTransaction /></ElCol>
        <ElCol :md="24" :lg="16" class="no-margin-bottom"><HotProductsList /></ElCol>
      </ElRow>
    </div>
  </div>
</template>

<script setup lang="ts">
import ActiveUser from "./modules/active-user.vue";
import SalesOverview from "./modules/sales-overview.vue";
import NewUser from "./modules/new-user.vue";
import Dynamic from "./modules/dynamic-stats.vue";
import TodoList from "./modules/todo-list.vue";

import Banner from "../home/modules/banner.vue";
import TotalOrderVolume from "../home/modules/total-order-volume.vue";
import TotalProducts from "../home/modules/total-products.vue";
import SalesTrend from "../home/modules/sales-trend.vue";
import SalesClassification from "../home/modules/sales-classification.vue";
import TransactionList from "../home/modules/transaction-list.vue";
import HotCommodity from "../home/modules/hot-commodity.vue";
import RecentTransaction from "../home/modules/recent-transaction.vue";
import AnnualSales from "../home/modules/annual-sales.vue";
import ProductSales from "../home/modules/product-sales.vue";
import SalesGrowth from "../home/modules/sales-growth.vue";
import CartConversionRate from "../home/modules/cart-conversion-rate.vue";
import HotProductsList from "../home/modules/hot-products-list.vue";

defineOptions({ name: "Console" });
</script>

<style scoped>
@reference "@styles/core/tailwind.css";

:deep(.el-card) {
  --el-card-border-radius: calc(var(--custom-radius) + 2px);

  border: 1px solid var(--fa-card-border);
}

.workplace-container {
  display: flex;
  flex-direction: column;

  > * {
    margin-bottom: 16px;
  }

  > :last-child {
    margin-bottom: 0;
  }

  &::after {
    display: block;
    flex-shrink: 0;
    height: 16px;
    content: "";
  }
}

.card-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card-row {
  row-gap: 16px;
}
</style>
