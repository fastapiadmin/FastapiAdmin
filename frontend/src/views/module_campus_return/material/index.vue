<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form :inline="true">
        <el-form-item label="批次ID"><el-input-number v-model="searchForm.batch_id" :min="0" style="width: 120px" /></el-form-item>
        <el-form-item><el-button type="primary" @click="fetchData"><i-ep-search />搜索</el-button></el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card" shadow="never">
      <template #header>
        <div class="card-header"><span class="title">物料列表</span></div>
      </template>
      <el-table v-loading="loading" :data="tableData" stripe border>
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="material_name" label="物料名称" min-width="150" />
        <el-table-column prop="material_type" label="物料类型" width="120" />
        <el-table-column prop="total_quantity" label="总数量" width="100" align="center" />
        <el-table-column prop="available_quantity" label="可用数量" width="100" align="center" />
        <el-table-column prop="unit" label="单位" width="80" align="center" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { MaterialAPI, type MaterialItem } from "@/api/module_campus_return/material";

const loading = ref(false);
const tableData = ref<MaterialItem[]>([]);
const searchForm = reactive({ batch_id: undefined as number | undefined });

const fetchData = async () => {
  loading.value = true;
  try { tableData.value = await MaterialAPI.list(searchForm.batch_id) || []; }
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
