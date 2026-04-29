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
        <div class="card-header"><span class="title">保险保单列表</span></div>
      </template>
      <el-table v-loading="loading" :data="tableData" stripe border>
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="user_name" label="姓名" width="100" />
        <el-table-column prop="id_card" label="身份证号" width="180" />
        <el-table-column prop="policy_no" label="保单号" min-width="150" />
        <el-table-column prop="insurance_company" label="保险公司" min-width="120" />
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }"><el-tag :type="row.status === 'active' ? 'success' : row.status === 'expired' ? 'info' : 'warning'">{{ getStatusLabel(row.status) }}</el-tag></template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { InsuranceAPI, type InsurancePolicyItem } from "@/api/module_campus_return/insurance";

const loading = ref(false);
const tableData = ref<InsurancePolicyItem[]>([]);
const searchForm = reactive({ batch_id: undefined as number | undefined });

const getStatusLabel = (status: string) => ({ pending: "待生效", active: "生效中", expired: "已过期" }[status] || status);

const fetchData = async () => {
  loading.value = true;
  try { tableData.value = await InsuranceAPI.listPolicies(searchForm.batch_id) || []; }
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
