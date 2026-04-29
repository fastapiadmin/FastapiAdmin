<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form :inline="true">
        <el-form-item label="批次ID"><el-input-number v-model="searchForm.batch_id" :min="0" style="width: 120px" /></el-form-item>
        <el-form-item label="团队ID"><el-input-number v-model="searchForm.team_id" :min="0" style="width: 120px" /></el-form-item>
        <el-form-item><el-button type="primary" @click="fetchData"><i-ep-search />搜索</el-button></el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card" shadow="never">
      <template #header>
        <div class="card-header"><span class="title">行程列表</span></div>
      </template>
      <el-table v-loading="loading" :data="tableData" stripe border>
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="trip_type" label="出行方式" width="100" align="center">
          <template #default="{ row }">{{ getTripTypeLabel(row.trip_type) }}</template>
        </el-table-column>
        <el-table-column label="出发-到达" min-width="200">
          <template #default="{ row }">{{ row.departure_city || '' }} → {{ row.arrival_city || '' }}</template>
        </el-table-column>
        <el-table-column prop="departure_time" label="出发时间" width="160" />
        <el-table-column prop="train_no" label="车次/航班" width="100" />
        <el-table-column prop="hotel_name" label="酒店" min-width="120" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }"><el-tag :type="getStatusType(row.status)">{{ getStatusLabel(row.status) }}</el-tag></template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { ItineraryAPI, type ItineraryItem } from "@/api/module_campus_return/itinerary";

const loading = ref(false);
const tableData = ref<ItineraryItem[]>([]);
const searchForm = reactive({ batch_id: undefined as number | undefined, team_id: undefined as number | undefined });

const getTripTypeLabel = (type: string) => ({ train: "火车", plane: "飞机", bus: "大巴", car: "自驾" }[type] || type);
const getStatusType = (status: string) => ({ planned: "info", confirmed: "success", completed: "primary", cancelled: "danger" }[status] || "info");
const getStatusLabel = (status: string) => ({ planned: "计划中", confirmed: "已确认", completed: "已完成", cancelled: "已取消" }[status] || status);

const fetchData = async () => {
  loading.value = true;
  try { tableData.value = await ItineraryAPI.list(searchForm) || []; }
  finally { loading.value = false; }
};

onMounted(() => { fetchData(); });
</script>

<style scoped>
.search-card { margin-bottom: 16px; }
.table-card { margin-bottom: 16px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.title { font-weight: 600; }
</style>
