<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form :model="searchForm" :inline="true" label-width="80px">
        <el-form-item label="批次ID" prop="batch_id">
          <el-input-number v-model="searchForm.batch_id" :min="0" style="width: 120px" />
        </el-form-item>
        <el-form-item label="高中名称" prop="high_school_name">
          <el-input v-model="searchForm.high_school_name" placeholder="请输入" clearable style="width: 150px" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 140px">
            <el-option label="草稿" value="draft" />
            <el-option label="招募中" value="recruiting" />
            <el-option label="已满员" value="full" />
            <el-option label="已确认" value="confirmed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch"><i-ep-search />搜索</el-button>
          <el-button @click="handleReset"><i-ep-refresh />重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">团队列表</span>
          <div class="operations">
            <el-button v-permission="['module_campus_return:team:create']" type="primary" @click="handleCreate">
              <i-ep-plus />创建团队
            </el-button>
            <el-button v-permission="['module_campus_return:team:create']" type="success" @click="showJoinDialog = true">
              <i-ep-plus />加入团队
            </el-button>
          </div>
        </div>
      </template>

      <el-table v-loading="loading" :data="tableData" stripe border>
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="team_name" label="团队名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="team_code" label="邀请码" width="100" />
        <el-table-column prop="high_school_name" label="目标高中" min-width="150" />
        <el-table-column prop="batch_id" label="批次ID" width="80" align="center" />
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="max_members" label="最大人数" width="80" align="center" />
        <el-table-column prop="plan_date" label="计划日期" width="110" />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleView(row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <el-dialog v-model="formDialog.visible" title="创建团队" width="550px">
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="批次ID" prop="batch_id">
          <el-input-number v-model="form.batch_id" :min="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="团队名称" prop="team_name">
          <el-input v-model="form.team_name" placeholder="请输入团队名称" />
        </el-form-item>
        <el-form-item label="目标高中" prop="high_school_name">
          <el-input v-model="form.high_school_name" placeholder="请输入高中名称" />
        </el-form-item>
        <el-form-item label="最大人数" prop="max_members">
          <el-input-number v-model="form.max_members" :min="2" :max="20" style="width: 100%" />
        </el-form-item>
        <el-form-item label="计划日期" prop="plan_date">
          <el-date-picker v-model="form.plan_date" type="date" placeholder="选择日期" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="团队介绍" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入团队介绍" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="formDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showJoinDialog" title="加入团队" width="400px">
      <el-form-item label="邀请码">
        <el-input v-model="joinCode" placeholder="请输入团队邀请码" />
      </el-form-item>
      <template #footer>
        <el-button @click="showJoinDialog = false">取消</el-button>
        <el-button type="primary" @click="handleJoin">加入</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import type { FormInstance } from "element-plus";
import { ElMessage } from "element-plus";
import { TeamAPI, type TeamItem, type TeamForm, type TeamQuery } from "@/api/module_campus_return/team";

const loading = ref(false);
const tableData = ref<TeamItem[]>([]);
const formRef = ref<FormInstance>();
const showJoinDialog = ref(false);
const joinCode = ref("");

const searchForm = reactive<TeamQuery>({ batch_id: undefined, high_school_name: "", status: "" });
const pagination = reactive({ page: 1, pageSize: 10, total: 0 });
const formDialog = reactive<{ visible: boolean }>({ visible: false });
const form = reactive<TeamForm>({ batch_id: 0, team_name: "", high_school_name: "", max_members: 10 });
const formRules = { batch_id: [{ required: true }], team_name: [{ required: true }], high_school_name: [{ required: true }] };

const getStatusType = (status: string) => ({ draft: "info", recruiting: "success", full: "warning", confirmed: "primary", cancelled: "danger" }[status] || "info");
const getStatusLabel = (status: string) => ({ draft: "草稿", recruiting: "招募中", full: "已满员", confirmed: "已确认", cancelled: "已取消" }[status] || status);

const fetchData = async () => {
  loading.value = true;
  try {
    const res = await TeamAPI.list({ ...searchForm, page: pagination.page, pageSize: pagination.pageSize });
    tableData.value = res.list || [];
    pagination.total = res.total || 0;
  } finally { loading.value = false; }
};

const handleSearch = () => { pagination.page = 1; fetchData(); };
const handleReset = () => { searchForm.batch_id = undefined; searchForm.high_school_name = ""; searchForm.status = ""; handleSearch(); };
const handleSizeChange = () => { pagination.page = 1; fetchData(); };
const handlePageChange = () => { fetchData(); };

const handleCreate = () => { formDialog.visible = true; };
const handleSubmit = async () => {
  if (!formRef.value) return;
  await formRef.value.validate(async (valid) => {
    if (valid) {
      await TeamAPI.create(form);
      ElMessage.success("创建成功");
      formDialog.visible = false;
      fetchData();
    }
  });
};

const handleJoin = async () => {
  if (!joinCode.value) { ElMessage.warning("请输入邀请码"); return; }
  await TeamAPI.joinByCode(joinCode.value);
  ElMessage.success("加入成功");
  showJoinDialog.value = false;
  fetchData();
};

const handleView = (row: TeamItem) => { ElMessage.info(`团队: ${row.team_name}, 邀请码: ${row.team_code}`); };

onMounted(() => { fetchData(); });
</script>

<style scoped>
.search-card { margin-bottom: 16px; }
.table-card { margin-bottom: 16px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.title { font-weight: 600; }
.pagination-container { margin-top: 16px; display: flex; justify-content: flex-end; }
</style>
