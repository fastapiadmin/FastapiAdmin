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
        <div class="card-header"><span class="title">高中对接列表</span></div>
      </template>
      <el-table v-loading="loading" :data="tableData" stripe border>
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="high_school_name" label="高中名称" min-width="150" />
        <el-table-column prop="contact_name" label="联系人" width="100" />
        <el-table-column prop="scheduled_date" label="预定日期" width="110" />
        <el-table-column prop="venue" label="场地" min-width="150" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }"><el-tag :type="getStatusType(row.status)">{{ getStatusLabel(row.status) }}</el-tag></template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { HighSchoolAPI, type HighSchoolDockingItem } from "@/api/module_campus_return/highschool";

const loading = ref(false);
const tableData = ref<HighSchoolDockingItem[]>([]);
const searchForm = reactive({ batch_id: undefined as number | undefined });

const getStatusType = (status: string) => ({ pending: "warning", confirmed: "success", completed: "info", cancelled: "danger" }[status] || "info");
const getStatusLabel = (status: string) => ({ pending: "待确认", confirmed: "已确认", completed: "已完成", cancelled: "已取消" }[status] || status);

const fetchData = async () => {
  loading.value = true;
  try { tableData.value = await HighSchoolAPI.listDocking(searchForm.batch_id) || []; }
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
