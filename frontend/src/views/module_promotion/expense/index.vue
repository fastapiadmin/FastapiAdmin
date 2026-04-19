<!-- 招生宣传活动 - 费用报销 -->
<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="80px">
        <el-form-item label="报销单号" prop="expense_no">
          <el-input v-model="searchForm.expense_no" placeholder="请输入报销单号" clearable style="width: 150px" />
        </el-form-item>
        <el-form-item label="费用类型" prop="expense_type">
          <el-select v-model="searchForm.expense_type" placeholder="请选择类型" clearable style="width: 140px">
            <el-option label="交通" value="transport" />
            <el-option label="住宿" value="accommodation" />
            <el-option label="餐饮" value="meal" />
            <el-option label="礼品" value="gift" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="报销状态" prop="expense_status">
          <el-select v-model="searchForm.expense_status" placeholder="请选择状态" clearable style="width: 140px">
            <el-option label="待提交" value="pending" />
            <el-option label="待审批" value="submitted" />
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
          <span class="title">费用报销列表</span>
          <div class="operations">
            <el-button v-permission="['module_promotion:expense:create']" type="primary" @click="handleCreate"><i-ep-plus /> 新增</el-button>
            <el-button v-permission="['module_promotion:expense:delete']" type="danger" :disabled="!selectedIds.length" @click="handleBatchDelete"><i-ep-delete /> 批量删除</el-button>
          </div>
        </div>
      </template>

      <el-table v-loading="loading" :data="tableData" stripe border @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="expense_no" label="报销单号" width="150" />
        <el-table-column prop="expense_type" label="费用类型" width="100">
          <template #default="{ row }">
            <el-tag>{{ getTypeLabel(row.expense_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="activity_name" label="活动名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="personnel_name" label="报销人" width="100" />
        <el-table-column prop="expense_date" label="费用日期" width="110" />
        <el-table-column prop="amount" label="报销金额" width="100">
          <template #default="{ row }">
            <span class="amount">¥{{ row.amount }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="invoice_status" label="发票状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.invoice_status === 'provided' ? 'success' : 'warning'">
              {{ row.invoice_status === 'provided' ? '已提供' : '未提供' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="expense_status" label="报销状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.expense_status)">{{ getStatusLabel(row.expense_status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-permission="['module_promotion:expense:detail']" link type="primary" @click="handleView(row)">详情</el-button>
            <el-button v-permission="['module_promotion:expense:update']" link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button v-permission="['module_promotion:expense:delete']" link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination v-model:current-page="pagination.page" v-model:page-size="pagination.pageSize" :total="pagination.total" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" @size-change="handleSizeChange" @current-change="handlePageChange" />
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailDialog.visible" title="费用报销详情" width="600px">
      <el-descriptions :column="2" border v-if="detailDialog.data">
        <el-descriptions-item label="报销单号">{{ detailDialog.data.expense_no }}</el-descriptions-item>
        <el-descriptions-item label="费用类型">
          <el-tag>{{ getTypeLabel(detailDialog.data.expense_type) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="活动名称">{{ detailDialog.data.activity_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="报销人">{{ detailDialog.data.personnel_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="费用日期">{{ detailDialog.data.expense_date || '-' }}</el-descriptions-item>
        <el-descriptions-item label="报销金额">
          <span class="amount">¥{{ detailDialog.data.amount || 0 }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="发票状态">
          <el-tag :type="detailDialog.data.invoice_status === 'provided' ? 'success' : 'warning'">
            {{ detailDialog.data.invoice_status === 'provided' ? '已提供' : '未提供' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="报销状态">
          <el-tag :type="getStatusType(detailDialog.data.expense_status)">{{ getStatusLabel(detailDialog.data.expense_status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="费用描述" :span="2">{{ detailDialog.data.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ detailDialog.data.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ detailDialog.data.created_time }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ detailDialog.data.updated_time }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="formDialog.visible" :title="formDialog.type === 'create' ? '新增费用报销' : '编辑费用报销'" width="550px">
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="费用类型" prop="expense_type">
          <el-select v-model="form.expense_type" placeholder="请选择费用类型" style="width: 100%">
            <el-option label="交通" value="transport" />
            <el-option label="住宿" value="accommodation" />
            <el-option label="餐饮" value="meal" />
            <el-option label="礼品" value="gift" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="活动ID" prop="activity_id">
          <el-input-number v-model="form.activity_id" :min="0" placeholder="活动ID" style="width: 100%" />
        </el-form-item>
        <el-form-item label="人员ID" prop="personnel_id">
          <el-input-number v-model="form.personnel_id" :min="0" placeholder="人员ID" style="width: 100%" />
        </el-form-item>
        <el-form-item label="费用日期" prop="expense_date">
          <el-date-picker v-model="form.expense_date" type="date" placeholder="选择费用日期" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="报销金额" prop="amount">
          <el-input-number v-model="form.amount" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>
        <el-form-item label="费用描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入费用描述" />
        </el-form-item>
        <el-form-item label="发票状态" prop="invoice_status">
          <el-select v-model="form.invoice_status" placeholder="请选择发票状态" style="width: 100%">
            <el-option label="已提供" value="provided" />
            <el-option label="未提供" value="not_provided" />
          </el-select>
        </el-form-item>
        <el-form-item label="报销状态" prop="expense_status">
          <el-select v-model="form.expense_status" placeholder="请选择报销状态" style="width: 100%">
            <el-option label="待提交" value="pending" />
            <el-option label="待审批" value="submitted" />
            <el-option label="已通过" value="approved" />
            <el-option label="已拒绝" value="rejected" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="form.remark" type="textarea" :rows="2" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="formDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import type { FormInstance, FormRules } from "element-plus";
import { ElMessage, ElMessageBox } from "element-plus";
import ExpenseAPI from "@/api/module_promotion/expense";
import type { ExpenseItem, ExpenseForm, ExpenseQuery } from "@/api/module_promotion/expense";

const loading = ref(false);
const tableData = ref<ExpenseItem[]>([]);
const selectedIds = ref<number[]>([]);

const searchFormRef = ref<FormInstance>();
const searchForm = reactive<ExpenseQuery>({
  expense_no: "",
  expense_type: "",
  expense_status: "",
});

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

const detailDialog = reactive({
  visible: false,
  data: null as ExpenseItem | null,
});

const formDialog = reactive({
  visible: false,
  type: "create" as "create" | "edit",
  id: null as number | null,
});

const formRef = ref<FormInstance>();
const form = reactive<ExpenseForm>({
  expense_type: "other",
  activity_id: undefined,
  activity_name: "",
  personnel_id: undefined,
  personnel_name: "",
  expense_date: "",
  amount: 0,
  description: "",
  invoice_status: "not_provided",
  expense_status: "pending",
  remark: "",
});

const formRules: FormRules = {
  expense_type: [{ required: true, message: "请选择费用类型", trigger: "change" }],
  amount: [{ required: true, message: "请输入报销金额", trigger: "blur" }],
};

function getTypeLabel(type: string): string {
  const map: Record<string, string> = {
    transport: "交通",
    accommodation: "住宿",
    meal: "餐饮",
    gift: "礼品",
    other: "其他",
  };
  return map[type] || type;
}

function getStatusLabel(status: string): string {
  const map: Record<string, string> = {
    pending: "待提交",
    submitted: "待审批",
    approved: "已通过",
    rejected: "已拒绝",
  };
  return map[status] || status;
}

function getStatusType(status: string): string {
  const map: Record<string, string> = {
    pending: "info",
    submitted: "warning",
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
    const res = await ExpenseAPI.getList(params);
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

function handleSelectionChange(selection: ExpenseItem[]) {
  selectedIds.value = selection.map((item) => item.id);
}

function handleCreate() {
  formDialog.type = "create";
  formDialog.id = null;
  Object.assign(form, {
    expense_type: "other",
    activity_id: undefined,
    activity_name: "",
    personnel_id: undefined,
    personnel_name: "",
    expense_date: "",
    amount: 0,
    description: "",
    invoice_status: "not_provided",
    expense_status: "pending",
    remark: "",
  });
  formDialog.visible = true;
}

function handleEdit(row: ExpenseItem) {
  formDialog.type = "edit";
  formDialog.id = row.id;
  Object.assign(form, row);
  formDialog.visible = true;
}

async function handleView(row: ExpenseItem) {
  try {
    const res = await ExpenseAPI.getDetail(row.id);
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

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false);
  if (!valid) return;

  try {
    if (formDialog.type === "create") {
      const res = await ExpenseAPI.create(form);
      if (res.data.code === 0) {
        ElMessage.success("创建成功");
        formDialog.visible = false;
        fetchData();
      } else {
        ElMessage.error(res.data.msg || "创建失败");
      }
    } else {
      const res = await ExpenseAPI.update(formDialog.id!, form);
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

async function handleDelete(row: ExpenseItem) {
  try {
    await ElMessageBox.confirm("确定要删除该费用报销吗？", "提示", {
      type: "warning",
    });
    const res = await ExpenseAPI.delete(row.id);
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
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 个费用报销吗？`, "提示", {
      type: "warning",
    });
    const res = await ExpenseAPI.batchDelete(selectedIds.value);
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
.amount {
  color: #f56c6c;
  font-weight: bold;
}
</style>