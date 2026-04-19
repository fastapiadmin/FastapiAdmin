<!-- 招生宣传活动 - 活动申请审批 -->
<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="90px">
        <el-form-item label="活动名称" prop="activity_name">
          <el-input v-model="searchForm.activity_name" placeholder="请输入活动名称" clearable style="width: 180px" />
        </el-form-item>
        <el-form-item label="活动编号" prop="activity_no">
          <el-input v-model="searchForm.activity_no" placeholder="请输入活动编号" clearable style="width: 150px" />
        </el-form-item>
        <el-form-item label="申请状态" prop="apply_status">
          <el-select v-model="searchForm.apply_status" placeholder="请选择状态" clearable style="width: 140px">
            <el-option label="待审批" value="pending" />
            <el-option label="已通过" value="approved" />
            <el-option label="已拒绝" value="rejected" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch"><i-ep-search /> 搜索</el-button>
          <el-button @click="handleReset"><i-ep-refresh /> 重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">活动申请列表</span>
          <div class="operations">
            <el-button v-permission="['module_promotion:activity_apply:create']" type="primary" @click="handleCreate"><i-ep-plus /> 新增</el-button>
            <el-button v-permission="['module_promotion:activity_apply:delete']" type="danger" :disabled="!selectedIds.length" @click="handleBatchDelete"><i-ep-delete /> 批量删除</el-button>
          </div>
        </div>
      </template>

      <el-table v-loading="loading" :data="tableData" stripe border @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="activity_no" label="活动编号" width="150" />
        <el-table-column prop="activity_name" label="活动名称" min-width="180" show-overflow-tooltip>
          <template #default="{ row }">
            <el-link type="primary" @click="handleView(row)">{{ row.activity_name || '-' }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="activity_type" label="活动类型" width="100">
          <template #default="{ row }">
            <el-tag>{{ getTypeLabel(row.activity_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="target_school_name" label="目标学校" width="150" show-overflow-tooltip />
        <el-table-column prop="planned_date" label="计划日期" width="110" />
        <el-table-column prop="expected_headcount" label="预计人数" width="100" />
        <el-table-column prop="expected_budget" label="预计预算" width="100">
          <template #default="{ row }">
            {{ row.expected_budget ? `¥${row.expected_budget}` : '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="apply_status" label="申请状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.apply_status)">{{ getStatusLabel(row.apply_status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button v-permission="['module_promotion:activity_apply:detail']" link type="primary" @click="handleView(row)">详情</el-button>
            <el-button v-permission="['module_promotion:activity_apply:update']" link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button v-permission="['module_promotion:activity_apply:approve']" link type="success" :disabled="row.apply_status !== 'pending'" @click="handleApprove(row)">审批</el-button>
            <el-button v-permission="['module_promotion:activity_apply:delete']" link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination v-model:current-page="pagination.page" v-model:page-size="pagination.pageSize" :total="pagination.total" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" @size-change="handleSizeChange" @current-change="handlePageChange" />
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailDialog.visible" title="活动申请详情" width="650px">
      <el-descriptions :column="2" border v-if="detailDialog.data">
        <el-descriptions-item label="活动编号">{{ detailDialog.data.activity_no }}</el-descriptions-item>
        <el-descriptions-item label="申请状态">
          <el-tag :type="getStatusType(detailDialog.data.apply_status)">{{ getStatusLabel(detailDialog.data.apply_status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="活动名称" :span="2">{{ detailDialog.data.activity_name }}</el-descriptions-item>
        <el-descriptions-item label="活动类型">
          <el-tag>{{ getTypeLabel(detailDialog.data.activity_type) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="目标学校">{{ detailDialog.data.target_school_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="计划日期">{{ detailDialog.data.planned_date || '-' }}</el-descriptions-item>
        <el-descriptions-item label="结束日期">{{ detailDialog.data.end_date || '-' }}</el-descriptions-item>
        <el-descriptions-item label="预计人数">{{ detailDialog.data.expected_headcount || '-' }}</el-descriptions-item>
        <el-descriptions-item label="预计预算">{{ detailDialog.data.expected_budget ? `¥${detailDialog.data.expected_budget}` : '-' }}</el-descriptions-item>
        <el-descriptions-item label="联系人">{{ detailDialog.data.contact_person || '-' }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ detailDialog.data.contact_phone || '-' }}</el-descriptions-item>
        <el-descriptions-item label="活动描述" :span="2">{{ detailDialog.data.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ detailDialog.data.created_time }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ detailDialog.data.updated_time }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="formDialog.visible" :title="formDialog.type === 'create' ? '新增活动申请' : '编辑活动申请'" width="600px">
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="活动名称" prop="activity_name">
          <el-input v-model="form.activity_name" placeholder="请输入活动名称" />
        </el-form-item>
        <el-form-item label="活动类型" prop="activity_type">
          <el-select v-model="form.activity_type" placeholder="请选择活动类型" style="width: 100%">
            <el-option label="宣讲会" value="lecture" />
            <el-option label="咨询会" value="consultation" />
            <el-option label="展会" value="exhibition" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="目标学校" prop="target_school_id">
          <el-input-number v-model="form.target_school_id" :min="0" placeholder="目标学校ID" style="width: 100%" />
        </el-form-item>
        <el-form-item label="计划日期" prop="planned_date">
          <el-date-picker v-model="form.planned_date" type="date" placeholder="选择计划日期" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker v-model="form.end_date" type="date" placeholder="选择结束日期" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="预计人数" prop="expected_headcount">
          <el-input-number v-model="form.expected_headcount" :min="0" style="width: 100%" />
        </el-form-item>
        <el-form-item label="预计预算" prop="expected_budget">
          <el-input-number v-model="form.expected_budget" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>
        <el-form-item label="联系人" prop="contact_person">
          <el-input v-model="form.contact_person" placeholder="请输入联系人" />
        </el-form-item>
        <el-form-item label="联系电话" prop="contact_phone">
          <el-input v-model="form.contact_phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="活动描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入活动描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="formDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 审批弹窗 -->
    <el-dialog v-model="approveDialog.visible" title="活动申请审批" width="500px">
      <el-form ref="approveFormRef" :model="approveForm" label-width="80px">
        <el-form-item label="审批结果">
          <el-radio-group v-model="approveForm.approved">
            <el-radio :value="true">通过</el-radio>
            <el-radio :value="false">拒绝</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="审批意见">
          <el-input v-model="approveForm.comment" type="textarea" :rows="3" placeholder="请输入审批意见" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="approveDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleApproveSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import type { FormInstance, FormRules } from "element-plus";
import { ElMessage, ElMessageBox } from "element-plus";
import ActivityApplyAPI from "@/api/module_promotion/activity_apply";
import type { ActivityApplyItem, ActivityApplyForm, ActivityApplyQuery } from "@/api/module_promotion/activity_apply";

const loading = ref(false);
const tableData = ref<ActivityApplyItem[]>([]);
const selectedIds = ref<number[]>([]);

const searchFormRef = ref<FormInstance>();
const searchForm = reactive<ActivityApplyQuery>({
  activity_name: "",
  activity_no: "",
  apply_status: "",
});

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

const detailDialog = reactive({
  visible: false,
  data: null as ActivityApplyItem | null,
});

const formDialog = reactive({
  visible: false,
  type: "create" as "create" | "edit",
  id: null as number | null,
});

const approveDialog = reactive({
  visible: false,
  id: null as number | null,
});

const formRef = ref<FormInstance>();
const approveFormRef = ref<FormInstance>();
const form = reactive<ActivityApplyForm>({
  activity_name: "",
  activity_type: "lecture",
  activity_no: "",
  target_school_id: undefined,
  target_school_name: "",
  planned_date: "",
  end_date: "",
  expected_headcount: 0,
  expected_budget: 0,
  contact_person: "",
  contact_phone: "",
  description: "",
  apply_status: "pending",
});

const approveForm = reactive({
  approved: true,
  comment: "",
});

const formRules: FormRules = {
  activity_name: [{ required: true, message: "请输入活动名称", trigger: "blur" }],
  activity_type: [{ required: true, message: "请选择活动类型", trigger: "change" }],
};

function getTypeLabel(type: string): string {
  const map: Record<string, string> = {
    lecture: "宣讲会",
    consultation: "咨询会",
    exhibition: "展会",
    other: "其他",
  };
  return map[type] || type;
}

function getStatusLabel(status: string): string {
  const map: Record<string, string> = {
    pending: "待审批",
    approved: "已通过",
    rejected: "已拒绝",
  };
  return map[status] || status;
}

function getStatusType(status: string): string {
  const map: Record<string, string> = {
    pending: "warning",
    approved: "success",
    rejected: "danger",
  };
  return map[status] || "info";
}

async function fetchData() {
  loading.value = true;
  try {
    const params = {
      ...searchForm,
      page: pagination.page,
      pageSize: pagination.pageSize,
    };
    const res = await ActivityApplyAPI.getList(params);
    if (res.data.code === 0) {
      tableData.value = res.data.data.items || [];
      pagination.total = res.data.data.total || 0;
    } else {
      ElMessage.error(res.data.msg || "获取数据失败");
    }
  } finally {
    loading.value = false;
  }
}

function handleSearch() {
  pagination.page = 1;
  fetchData();
}

function handleReset() {
  searchFormRef.value?.resetFields();
  handleSearch();
}

function handleSizeChange() {
  pagination.page = 1;
  fetchData();
}

function handlePageChange() {
  fetchData();
}

function handleSelectionChange(selection: ActivityApplyItem[]) {
  selectedIds.value = selection.map((item) => item.id);
}

function handleCreate() {
  formDialog.type = "create";
  formDialog.id = null;
  Object.assign(form, {
    activity_name: "",
    activity_type: "lecture",
    activity_no: "",
    target_school_id: undefined,
    target_school_name: "",
    planned_date: "",
    end_date: "",
    expected_headcount: 0,
    expected_budget: 0,
    contact_person: "",
    contact_phone: "",
    description: "",
    apply_status: "pending",
  });
  formDialog.visible = true;
}

function handleEdit(row: ActivityApplyItem) {
  formDialog.type = "edit";
  formDialog.id = row.id;
  Object.assign(form, row);
  formDialog.visible = true;
}

async function handleView(row: ActivityApplyItem) {
  try {
    const res = await ActivityApplyAPI.getDetail(row.id);
    if (res.data.code === 0) {
      detailDialog.data = res.data.data;
      detailDialog.visible = true;
    } else {
      ElMessage.error(res.data.msg || "获取详情失败");
    }
  } catch {
    ElMessage.error("获取详情失败");
  }
}

function handleApprove(row: ActivityApplyItem) {
  approveDialog.id = row.id;
  approveForm.approved = true;
  approveForm.comment = "";
  approveDialog.visible = true;
}

async function handleApproveSubmit() {
  if (!approveDialog.id) return;
  try {
    const res = await ActivityApplyAPI.approve(approveDialog.id, approveForm);
    if (res.data.code === 0) {
      ElMessage.success("审批成功");
      approveDialog.visible = false;
      fetchData();
    } else {
      ElMessage.error(res.data.msg || "审批失败");
    }
  } catch {
    ElMessage.error("审批失败");
  }
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false);
  if (!valid) return;

  try {
    if (formDialog.type === "create") {
      const res = await ActivityApplyAPI.create(form);
      if (res.data.code === 0) {
        ElMessage.success("创建成功");
        formDialog.visible = false;
        fetchData();
      } else {
        ElMessage.error(res.data.msg || "创建失败");
      }
    } else {
      const res = await ActivityApplyAPI.update(formDialog.id!, form);
      if (res.data.code === 0) {
        ElMessage.success("更新成功");
        formDialog.visible = false;
        fetchData();
      } else {
        ElMessage.error(res.data.msg || "更新失败");
      }
    }
  } catch {
    ElMessage.error("操作失败");
  }
}

async function handleDelete(row: ActivityApplyItem) {
  try {
    await ElMessageBox.confirm("确定要删除该活动申请吗？", "提示", {
      type: "warning",
    });
    const res = await ActivityApplyAPI.delete(row.id);
    if (res.data.code === 0) {
      ElMessage.success("删除成功");
      fetchData();
    } else {
      ElMessage.error(res.data.msg || "删除失败");
    }
  } catch {
    // 用户取消
  }
}

async function handleBatchDelete() {
  if (!selectedIds.value.length) return;
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 个活动申请吗？`, "提示", {
      type: "warning",
    });
    const res = await ActivityApplyAPI.batchDelete(selectedIds.value);
    if (res.data.code === 0) {
      ElMessage.success("批量删除成功");
      selectedIds.value = [];
      fetchData();
    } else {
      ElMessage.error(res.data.msg || "批量删除失败");
    }
  } catch {
    // 用户取消
  }
}

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.search-card {
  margin-bottom: 16px;
}
.table-card {
  margin-bottom: 16px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.card-header .title {
  font-weight: 600;
}
.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}
</style>