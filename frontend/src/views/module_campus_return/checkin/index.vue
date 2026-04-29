<template>
  <div class="app-container">
    <el-card shadow="never">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="打卡记录" name="checkin">
          <el-form :inline="true" style="margin-bottom: 16px">
            <el-form-item label="批次ID"><el-input-number v-model="checkinSearch.batch_id" :min="0" style="width: 120px" /></el-form-item>
            <el-form-item><el-button type="primary" @click="fetchCheckin"><i-ep-search />搜索</el-button></el-form-item>
          </el-form>
          <el-table v-loading="checkinLoading" :data="checkinData" stripe border>
            <el-table-column type="index" label="序号" width="60" align="center" />
            <el-table-column prop="checkin_type" label="打卡类型" width="100" align="center">
              <template #default="{ row }">{{ getCheckinTypeLabel(row.checkin_type) }}</template>
            </el-table-column>
            <el-table-column prop="checkin_time" label="打卡时间" width="160" />
            <el-table-column prop="location_name" label="位置" min-width="150" show-overflow-tooltip />
            <el-table-column prop="address" label="地址" min-width="200" show-overflow-tooltip />
            <el-table-column prop="status" label="状态" width="100" align="center">
              <template #default="{ row }"><el-tag :type="row.status === 'approved' ? 'success' : row.status === 'rejected' ? 'danger' : 'warning'">{{ getStatusLabel(row.status) }}</el-tag></template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="总结报告" name="summary">
          <el-form :inline="true" style="margin-bottom: 16px">
            <el-form-item label="批次ID"><el-input-number v-model="summarySearch.batch_id" :min="0" style="width: 120px" /></el-form-item>
            <el-form-item><el-button type="primary" @click="fetchSummary"><i-ep-search />搜索</el-button></el-form-item>
          </el-form>
          <el-table v-loading="summaryLoading" :data="summaryData" stripe border>
            <el-table-column type="index" label="序号" width="60" align="center" />
            <el-table-column prop="activity_name" label="活动名称" min-width="150" />
            <el-table-column prop="activity_date" label="活动日期" width="110" />
            <el-table-column prop="audience_count" label="受众人数" width="100" align="center" />
            <el-table-column prop="status" label="状态" width="100" align="center">
              <template #default="{ row }"><el-tag :type="getSummaryStatusType(row.status)">{{ getSummaryStatusLabel(row.status) }}</el-tag></template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { CheckInAPI, type CheckInItem, type SummaryItem } from "@/api/module_campus_return/checkin";

const activeTab = ref("checkin");
const checkinLoading = ref(false);
const summaryLoading = ref(false);
const checkinData = ref<CheckInItem[]>([]);
const summaryData = ref<SummaryItem[]>([]);
const checkinSearch = reactive({ batch_id: undefined as number | undefined });
const summarySearch = reactive({ batch_id: undefined as number | undefined });

const getCheckinTypeLabel = (type: string) => ({ location: "位置打卡", photo: "照片打卡", report: "报告打卡" }[type] || type);
const getStatusLabel = (status: string) => ({ pending: "待审核", approved: "已通过", rejected: "已拒绝" }[status] || status);
const getSummaryStatusType = (status: string) => ({ draft: "info", submitted: "warning", approved: "success" }[status] || "info");
const getSummaryStatusLabel = (status: string) => ({ draft: "草稿", submitted: "已提交", approved: "已审核" }[status] || status);

const fetchCheckin = async () => {
  checkinLoading.value = true;
  try { checkinData.value = await CheckInAPI.listCheckin(checkinSearch) || []; }
  finally { checkinLoading.value = false; }
};

const fetchSummary = async () => {
  summaryLoading.value = true;
  try { summaryData.value = await CheckInAPI.listSummary(summarySearch.batch_id) || []; }
  finally { summaryLoading.value = false; }
};

onMounted(() => { fetchCheckin(); fetchSummary(); });
</script>

<style scoped>
</style>
