<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form :inline="true">
        <el-form-item label="批次ID"><el-input-number v-model="searchForm.batch_id" :min="0" style="width: 120px" /></el-form-item>
        <el-form-item label="用户ID"><el-input-number v-model="searchForm.user_id" :min="0" style="width: 120px" /></el-form-item>
        <el-form-item><el-button type="primary" @click="fetchData"><i-ep-search />搜索</el-button></el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card" shadow="never">
      <template #header>
        <div class="card-header"><span class="title">志愿服务时长列表</span></div>
      </template>
      <el-table v-loading="loading" :data="tableData" stripe border>
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="user_name" label="姓名" width="100" />
        <el-table-column prop="student_number" label="学号" width="120" />
        <el-table-column prop="activity_name" label="活动名称" min-width="150" />
        <el-table-column prop="activity_date" label="活动日期" width="110" />
        <el-table-column prop="service_hours" label="服务时长(h)" width="100" align="center" />
        <el-table-column prop="second_class_credit" label="二课堂学分" width="100" align="center" />
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }"><el-tag :type="row.status === 'published' ? 'success' : row.status === 'approved' ? 'primary' : 'info'">{{ getStatusLabel(row.status) }}</el-tag></template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { VolunteerAPI, type VolunteerHourItem } from "@/api/module_campus_return/volunteer";

const loading = ref(false);
const tableData = ref<VolunteerHourItem[]>([]);
const searchForm = reactive({ batch_id: undefined as number | undefined, user_id: undefined as number | undefined });

const getStatusLabel = (status: string) => ({ pending: "待审核", approved: "已审核", published: "已发布" }[status] || status);

const fetchData = async () => {
  loading.value = true;
  try { tableData.value = await VolunteerAPI.listHours(searchForm) || []; }
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
