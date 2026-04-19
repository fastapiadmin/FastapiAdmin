<!-- 招生宣传活动 - 总结上传 -->
<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="80px">
        <el-form-item label="总结单号" prop="summary_no">
          <el-input v-model="searchForm.summary_no" placeholder="请输入总结单号" clearable style="width: 150px" />
        </el-form-item>
        <el-form-item label="活动ID" prop="activity_id">
          <el-input-number v-model="searchForm.activity_id" :min="1" style="width: 120px" />
        </el-form-item>
        <el-form-item label="总结类型" prop="summary_type">
          <el-select v-model="searchForm.summary_type" placeholder="请选择类型" clearable style="width: 140px">
            <el-option label="日总结" value="daily" />
            <el-option label="周总结" value="weekly" />
            <el-option label="月总结" value="monthly" />
            <el-option label="活动总结" value="activity" />
          </el-select>
        </el-form-item>
        <el-form-item label="提交状态" prop="summary_status">
          <el-select v-model="searchForm.summary_status" placeholder="请选择状态" clearable style="width: 140px">
            <el-option label="草稿" value="draft" />
            <el-option label="已提交" value="submitted" />
            <el-option label="已审核" value="approved" />
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
          <span class="title">总结上传列表</span>
          <div class="operations">
            <el-button v-permission="['module_promotion:summary:create']" type="primary" @click="handleCreate"><i-ep-plus /> 新增</el-button>
            <el-button v-permission="['module_promotion:summary:delete']" type="danger" :disabled="!selectedIds.length" @click="handleBatchDelete"><i-ep-delete /> 批量删除</el-button>
          </div>
        </div>
      </template>

      <el-table v-loading="loading" :data="tableData" stripe border @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="summary_no" label="总结单号" width="150" />
        <el-table-column prop="activity_name" label="活动名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="summary_type" label="总结类型" width="100">
          <template #default="{ row }">
            <el-tag>{{ getTypeLabel(row.summary_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="summary_date" label="总结日期" width="110" />
        <el-table-column prop="submitter_name" label="提交人" width="100" />
        <el-table-column prop="summary_status" label="提交状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.summary_status)">{{ getStatusLabel(row.summary_status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-permission="['module_promotion:summary:detail']" link type="primary" @click="handleView(row)">详情</el-button>
            <el-button v-permission="['module_promotion:summary:update']" link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button v-permission="['module_promotion:summary:delete']" link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination v-model:current-page="pagination.page" v-model:page-size="pagination.pageSize" :total="pagination.total" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" @size-change="handleSizeChange" @current-change="handlePageChange" />
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailDialog.visible" title="总结详情" width="650px">
      <el-descriptions :column="2" border v-if="detailDialog.data">
        <el-descriptions-item label="总结单号">{{ detailDialog.data.summary_no }}</el-descriptions-item>
        <el-descriptions-item label="总结类型">
          <el-tag>{{ getTypeLabel(detailDialog.data.summary_type) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="活动名称" :span="2">{{ detailDialog.data.activity_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="总结日期">{{ detailDialog.data.summary_date || '-' }}</el-descriptions-item>
        <el-descriptions-item label="提交人">{{ detailDialog.data.submitter_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="提交状态">
          <el-tag :type="getStatusType(detailDialog.data.summary_status)">{{ getStatusLabel(detailDialog.data.summary_status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="附件" :span="2">
          <a v-if="detailDialog.data.attachment_url" :href="detailDialog.data.attachment_url" target="_blank">查看附件</a>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="总结内容" :span="2">
          <div style="white-space: pre-wrap;">{{ detailDialog.data.summary_content || '-' }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ detailDialog.data.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ detailDialog.data.created_time }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ detailDialog.data.updated_time }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="formDialog.visible" :title="formDialog.type === 'create' ? '新增总结' : '编辑总结'" width="600px">
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="活动ID" prop="activity_id">
          <el-input-number v-model="form.activity_id" :min="0" placeholder="活动ID" style="width: 100%" />
        </el-form-item>
        <el-form-item label="总结类型" prop="summary_type">
          <el-select v-model="form.summary_type" placeholder="请选择总结类型" style="width: 100%">
            <el-option label="日总结" value="daily" />
            <el-option label="周总结" value="weekly" />
            <el-option label="月总结" value="monthly" />
            <el-option label="活动总结" value="activity" />
          </el-select>
        </el-form-item>
        <el-form-item label="总结日期" prop="summary_date">
          <el-date-picker v-model="form.summary_date" type="date" placeholder="选择总结日期" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="提交人ID" prop="submitter_id">
          <el-input-number v-model="form.submitter_id" :min="0" placeholder="提交人ID" style="width: 100%" />
        </el-form-item>
        <el-form-item label="总结内容" prop="summary_content">
          <el-input v-model="form.summary_content" type="textarea" :rows="5" placeholder="请输入总结内容" />
        </el-form-item>
        <el-form-item label="附件URL" prop="attachment_url">
          <el-input v-model="form.attachment_url" placeholder="请输入附件URL" />
        </el-form-item>
        <el-form-item label="状态" prop="summary_status">
          <el-select v-model="form.summary_status" placeholder="请选择状态" style="width: 100%">
            <el-option label="草稿" value="draft" />
            <el-option label="已提交" value="submitted" />
            <el-option label="已审核" value="approved" />
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
import SummaryAPI from "@/api/module_promotion/summary";
import type { SummaryItem, SummaryForm, SummaryQuery } from "@/api/module_promotion/summary";

const loading = ref(false);
const tableData = ref<SummaryItem[]>([]);
const selectedIds = ref<number[]>([]);

const searchFormRef = ref<FormInstance>();
const searchForm = reactive<SummaryQuery>({
  summary_no: "",
  activity_id: undefined,
  summary_type: "",
  summary_status: "",
});

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

const detailDialog = reactive({
  visible: false,
  data: null as SummaryItem | null,
});

const formDialog = reactive({
  visible: false,
  type: "create" as "create" | "edit",
  id: null as number | null,
});

const formRef = ref<FormInstance>();
const form = reactive<SummaryForm>({
  activity_id: undefined,
  activity_name: "",
  summary_type: "daily",
  summary_date: "",
  submitter_id: undefined,
  submitter_name: "",
  summary_content: "",
  attachment_url: "",
  summary_status: "draft",
  remark: "",
});

const formRules: FormRules = {
  summary_type: [{ required: true, message: "请选择总结类型", trigger: "change" }],
};

function getTypeLabel(type: string): string {
  const map: Record<string, string> = {
    daily: "日总结",
    weekly: "周总结",
    monthly: "月总结",
    activity: "活动总结",
  };
  return map[type] || type;
}

function getStatusLabel(status: string): string {
  const map: Record<string, string> = {
    draft: "草稿",
    submitted: "已提交",
    approved: "已审核",
  };
  return map[status] || status;
}

function getStatusType(status: string): string {
  const map: Record<string, string> = {
    draft: "info",
    submitted: "warning",
    approved: "success",
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
    const res = await SummaryAPI.getList(params);
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

function handleSelectionChange(selection: SummaryItem[]) {
  selectedIds.value = selection.map((item) => item.id);
}

function handleCreate() {
  formDialog.type = "create";
  formDialog.id = null;
  Object.assign(form, {
    activity_id: undefined,
    activity_name: "",
    summary_type: "daily",
    summary_date: "",
    submitter_id: undefined,
    submitter_name: "",
    summary_content: "",
    attachment_url: "",
    summary_status: "draft",
    remark: "",
  });
  formDialog.visible = true;
}

function handleEdit(row: SummaryItem) {
  formDialog.type = "edit";
  formDialog.id = row.id;
  Object.assign(form, row);
  formDialog.visible = true;
}

async function handleView(row: SummaryItem) {
  try {
    const res = await SummaryAPI.getDetail(row.id);
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
      const res = await SummaryAPI.create(form);
      if (res.data.code === 0) {
        ElMessage.success("创建成功");
        formDialog.visible = false;
        fetchData();
      } else {
        ElMessage.error(res.data.msg || "创建失败");
      }
    } else {
      const res = await SummaryAPI.update(formDialog.id!, form);
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

async function handleDelete(row: SummaryItem) {
  try {
    await ElMessageBox.confirm("确定要删除该总结吗？", "提示", {
      type: "warning",
    });
    const res = await SummaryAPI.delete(row.id);
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
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 个总结吗？`, "提示", {
      type: "warning",
    });
    const res = await SummaryAPI.batchDelete(selectedIds.value);
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