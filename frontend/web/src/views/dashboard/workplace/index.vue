<template>
  <div class="flex flex-col relative last:mb-0">
    <FaDashboardSkeleton v-if="loading" />
    <template v-else>
      <ElRow :gutter="24">
        <ElCol :sm="12" :md="12" :lg="6" class="mb-5"><TotalOrderVolume /></ElCol>
        <ElCol :sm="12" :md="12" :lg="6" class="mb-5"><TotalProducts /></ElCol>
        <ElCol :sm="24" :md="12" :lg="6" class="mb-5"><ProductSales /></ElCol>
        <ElCol :sm="24" :md="12" :lg="6" class="mb-5"><SalesGrowth /></ElCol>
      </ElRow>

      <ElRow :gutter="24">
        <ElCol :span="24" class="mb-5"><CartConversionRate /></ElCol>
      </ElRow>

      <ElRow :gutter="24">
        <ElCol :sm="12" :md="12" :lg="6" class="mb-5"><SalesTrend /></ElCol>
        <ElCol :sm="12" :md="12" :lg="6" class="mb-5"><SalesClassification /></ElCol>
        <ElCol :sm="24" :md="12" :lg="6" class="mb-5"><HotCommodity /></ElCol>
        <ElCol :sm="24" :md="12" :lg="6" class="mb-5"><AnnualSales /></ElCol>
      </ElRow>

      <ElRow :gutter="24">
        <ElCol :sm="24" :md="12" :lg="12" class="mb-5"><ActiveUser /></ElCol>
        <ElCol :sm="24" :md="12" :lg="12" class="mb-5"><SalesOverview /></ElCol>
      </ElRow>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import FaDashboardSkeleton from "@/components/skeleton/fa-dashboard-skeleton.vue";
import ActiveUser from "./modules/active-user.vue";
import SalesOverview from "./modules/sales-overview.vue";
import TotalOrderVolume from "./modules/total-order-volume.vue";
import TotalProducts from "./modules/total-products.vue";
import SalesTrend from "./modules/sales-trend.vue";
import SalesClassification from "./modules/sales-classification.vue";
import HotCommodity from "./modules/hot-commodity.vue";
import AnnualSales from "./modules/annual-sales.vue";
import ProductSales from "./modules/product-sales.vue";
import SalesGrowth from "./modules/sales-growth.vue";
import CartConversionRate from "./modules/cart-conversion-rate.vue";

defineOptions({ name: "DashboardWorkplace" });

const loading = ref(true);
onMounted(() => {
  loading.value = false;
});
</script>
