<!-- 招生宣传活动 - 表彰评优 -->
<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="80px">
        <el-form-item label="表彰编号" prop="evaluation_no">
          <el-input v-model="searchForm.evaluation_no" placeholder="请输入表彰编号" clearable style="width: 150px" />
        </el-form-item>
        <el-form-item label="表彰类型" prop="evaluation_type">
          <el-select v-model="searchForm.evaluation_type" placeholder="请选择类型" clearable style="width: 140px">
            <el-option label="个人表彰" value="personal" />
            <el-option label="团队表彰" value="team" />
            <el-option label="优秀活动" value="activity" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="人员姓名" prop="personnel_name">
          <el-input v-model="searchForm.personnel_name" placeholder="请输入人员姓名" clearable style="width: 120px" />
        </el-form-item>
        <el-form-item label="表彰状态" prop="evaluation_status">
          <el-select v-model="searchForm.evaluation_status" placeholder="请选择状态" clearable style="width: 140px">
            <el-option label="待审核" value="pending" />
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
          <span class="title">表彰评优列表</span>
          <div class="operations">
            <el-button v-permission="['module_promotion:evaluation:create']" type="primary" @click="handleCreate"><i-ep-plus /> 新增</el-button>
            <el-button v-permission="['module_promotion:evaluation:delete']" type="danger" :disabled="!selectedIds.length" @click="handleBatchDelete"><i-ep-delete /> 批量删除</el-button>
          </div>
        </div>
      </template>

      <el-table v-loading="loading" :data="tableData" stripe border @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="evaluation_no" label="表彰编号" width="150" />
        <el-table-column prop="evaluation_type" label="表彰类型" width="100">
          <template #default="{ row }">
            <el-tag>{{ getTypeLabel(row.evaluation_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="activity_name" label="活动名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="personnel_name" label="被表彰人" width="100" />
        <el-table-column prop="evaluation_date" label="表彰日期" width="110" />
        <el-table-column prop="evaluation_score" label="评分" width="80">
          <template #default="{ row }">
            <span class="score">{{ row.evaluation_score || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="evaluation_result" label="评选结果" width="100">
          <template #default="{ row }">
            <el-tag :type="getResultType(row.evaluation_result)">{{ row.evaluation_result || '-' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="evaluation_status" label="表彰状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.evaluation_status)">{{ getStatusLabel(row.evaluation_status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-permission="['module_promotion:evaluation:detail']" link type="primary" @click="handleView(row)">详情</el-button>
            <el-button v-permission="['module_promotion:evaluation:update']" link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button v-permission="['module_promotion:evaluation:delete']" link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination v-model:current-page="pagination.page" v-model:page-size="pagination.pageSize" :total="pagination.total" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" @size-change="handleSizeChange" @current-change="handlePageChange" />
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailDialog.visible" title="表彰评优详情" width="650px">
      <el-descriptions :column="2" border v-if="detailDialog.data">
        <el-descriptions-item label="表彰编号">{{ detailDialog.data.evaluation_no }}</el-descriptions-item>
        <el-descriptions-item label="表彰类型">
          <el-tag>{{ getTypeLabel(detailDialog.data.evaluation_type) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="活动名称" :span="2">{{ detailDialog.data.activity_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="被表彰人">{{ detailDialog.data.personnel_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="表彰日期">{{ detailDialog.data.evaluation_date || '-' }}</el-descriptions-item>
        <el-descriptions-item label="评选评分">{{ detailDialog.data.evaluation_score || '-' }}</el-descriptions-item>
        <el-descriptions-item label="评选结果">
          <el-tag :type="getResultType(detailDialog.data.evaluation_result)">{{ detailDialog.data.evaluation_result || '-' }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="表彰状态">
          <el-tag :type="getStatusType(detailDialog.data.evaluation_status)">{{ getStatusLabel(detailDialog.data.evaluation_status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="附件">
          <a v-if="detailDialog.data.attachment_url" :href="detailDialog.data.attachment_url" target="_blank">查看附件</a>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="表彰内容" :span="2">
          <div style="white-space: pre-wrap;">{{ detailDialog.data.evaluation_content || '-' }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ detailDialog.data.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ detailDialog.data.created_time }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ detailDialog.data.updated_time }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="formDialog.visible" :title="formDialog.type === 'create' ? '新增表彰评优' : '编辑表彰评优'" width="600px">
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="表彰类型" prop="evaluation_type">
          <el-select v-model="form.evaluation_type" placeholder="请选择表彰类型" style="width: 100%">
            <el-option label="个人表彰" value="personal" />
            <el-option label="团队表彰" value="team" />
            <el-option label="优秀活动" value="activity" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="活动ID" prop="activity_id">
          <el-input-number v-model="form.activity_id" :min="0" placeholder="活动ID" style="width: 100%" />
        </el-form-item>
        <el-form-item label="人员ID" prop="personnel_id">
          <el-input-number v-model="form.personnel_id" :min="0" placeholder="人员ID" style="width: 100%" />
        </el-form-item>
        <el-form-item label="被表彰人" prop="personnel_name">
          <el-input v-model="form.personnel_name" placeholder="请输入被表彰人姓名" />
        </el-form-item>
        <el-form-item label="表彰日期" prop="evaluation_date">
          <el-date-picker v-model="form.evaluation_date" type="date" placeholder="选择表彰日期" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="评选评分" prop="evaluation_score">
          <el-input-number v-model="form.evaluation_score" :min="0" :max="100" :precision="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="评选结果" prop="evaluation_result">
          <el-input v-model="form.evaluation_result" placeholder="请输入评选结果，如：优秀、良好等" />
        </el-form-item>
        <el-form-item label="表彰状态" prop="evaluation_status">
          <el-select v-model="form.evaluation_status" placeholder="请选择表彰状态" style="width: 100%">
            <el-option label="待审核" value="pending" />
            <el-option label="已通过" value="approved" />
            <el-option label="已拒绝" value="rejected" />
          </el-select>
        </el-form-item>
        <el-form-item label="附件URL" prop="attachment_url">
          <el-input v-model="form.attachment_url" placeholder="请输入附件URL" />
        </el-form-item>
        <el-form-item label="表彰内容" prop="evaluation_content">
          <el-input v-model="form.evaluation_content" type="textarea" :rows="4" placeholder="请输入表彰内容" />
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
import EvaluationAPI from "@/api/module_promotion/evaluation";
import type { EvaluationItem, EvaluationForm, EvaluationQuery } from "@/api/module_promotion/evaluation";

const loading = ref(false);
const tableData = ref<EvaluationItem[]>([]);
const selectedIds = ref<number[]>([]);

const searchFormRef = ref<FormInstance>();
const searchForm = reactive<EvaluationQuery>({
  evaluation_no: "",
  evaluation_type: "",
  personnel_name: "",
  evaluation_status: "",
});

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

const detailDialog = reactive({
  visible: false,
  data: null as EvaluationItem | null,
});

const formDialog = reactive({
  visible: false,
  type: "create" as "create" | "edit",
  id: null as number | null,
});

const formRef = ref<FormInstance>();
const form = reactive<EvaluationForm>({
  evaluation_type: "personal",
  activity_id: undefined,
  activity_name: "",
  personnel_id: undefined,
  personnel_name: "",
  evaluation_date: "",
  evaluation_score: 0,
  evaluation_result: "",
  evaluation_content: "",
  attachment_url: "",
  evaluation_status: "pending",
  remark: "",
});

const formRules: FormRules = {
  evaluation_type: [{ required: true, message: "请选择表彰类型", trigger: "change" }],
  personnel_name: [{ required: true, message: "请输入被表彰人姓名", trigger: "blur" }],
};

function getTypeLabel(type: string): string {
  const map: Record<string, string> = {
    personal: "个人表彰",
    team: "团队表彰",
    activity: "优秀活动",
    other: "其他",
  };
  return map[type] || type;
}

function getStatusLabel(status: string): string {
  const map: Record<string, string> = {
    pending: "待审核",
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

function getResultType(result: string): string {
  const map: Record<string, string> = {
    优秀: "success",
    良好: "warning",
    一般: "info",
  };
  return map[result] || "info";
}

async function fetchData() {
  loading.value = true;
  try {
    const params = {
      ...searchForm,
      page: pagination.page,
      pageSize: pagination.pageSize,
    };
    const res = await EvaluationAPI.getList(params);
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

function handleSelectionChange(selection: EvaluationItem[]) {
  selectedIds.value = selection.map((item) => item.id);
}

function handleCreate() {
  formDialog.type = "create";
  formDialog.id = null;
  Object.assign(form, {
    evaluation_type: "personal",
    activity_id: undefined,
    activity_name: "",
    personnel_id: undefined,
    personnel_name: "",
    evaluation_date: "",
    evaluation_score: 0,
    evaluation_result: "",
    evaluation_content: "",
    attachment_url: "",
    evaluation_status: "pending",
    remark: "",
  });
  formDialog.visible = true;
}

function handleEdit(row: EvaluationItem) {
  formDialog.type = "edit";
  formDialog.id = row.id;
  Object.assign(form, row);
  formDialog.visible = true;
}

async function handleView(row: EvaluationItem) {
  try {
    const res = await EvaluationAPI.getDetail(row.id);
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
      const res = await EvaluationAPI.create(form);
      if (res.data.code === 0) {
        ElMessage.success("创建成功");
        formDialog.visible = false;
        fetchData();
      } else {
        ElMessage.error(res.data.msg || "创建失败");
      }
    } else {
      const res = await EvaluationAPI.update(formDialog.id!, form);
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

async function handleDelete(row: EvaluationItem) {
  try {
    await ElMessageBox.confirm("确定要删除该表彰评优吗？", "提示", {
      type: "warning",
    });
    const res = await EvaluationAPI.delete(row.id);
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
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 个表彰评优吗？`, "提示", {
      type: "warning",
    });
    const res = await EvaluationAPI.batchDelete(selectedIds.value);
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
.score {
  color: #e6a23c;
  font-weight: bold;
}
</style>