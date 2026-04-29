<!-- 招生宣传活动 - 活动撰写 -->
<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="80px">
        <el-form-item label="文档编号" prop="document_no">
          <el-input
            v-model="searchForm.document_no"
            placeholder="请输入文档编号"
            clearable
            style="width: 150px"
          />
        </el-form-item>
        <el-form-item label="文档类型" prop="document_type">
          <el-select
            v-model="searchForm.document_type"
            placeholder="请选择类型"
            clearable
            style="width: 140px"
          >
            <el-option label="新闻稿" value="news" />
            <el-option label="宣传稿" value="publicity" />
            <el-option label="邀请函" value="invitation" />
            <el-option label="通知" value="notice" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="作者" prop="author_name">
          <el-input
            v-model="searchForm.author_name"
            placeholder="请输入作者"
            clearable
            style="width: 120px"
          />
        </el-form-item>
        <el-form-item label="文档状态" prop="document_status">
          <el-select
            v-model="searchForm.document_status"
            placeholder="请选择状态"
            clearable
            style="width: 140px"
          >
            <el-option label="草稿" value="draft" />
            <el-option label="待发布" value="pending" />
            <el-option label="已发布" value="published" />
            <el-option label="已归档" value="archived" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <i-ep-search />
            搜索
          </el-button>
          <el-button @click="handleReset">
            <i-ep-refresh />
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">活动撰写列表</span>
          <div class="operations">
            <el-button
              v-permission="['module_promotion:document:create']"
              type="primary"
              @click="handleCreate"
            >
              <i-ep-plus />
              新增
            </el-button>
            <el-button
              v-permission="['module_promotion:document:delete']"
              type="danger"
              :disabled="!selectedIds.length"
              @click="handleBatchDelete"
            >
              <i-ep-delete />
              批量删除
            </el-button>
          </div>
        </div>
      </template>

      <el-table
        v-loading="loading"
        :data="tableData"
        stripe
        border
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="document_no" label="文档编号" width="150" />
        <el-table-column prop="document_title" label="文档标题" min-width="200" show-overflow-tooltip>
          <template #default="{ row }">
            <el-link type="primary" @click="handleView(row)">{{ row.document_title || "-" }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="document_type" label="文档类型" width="100">
          <template #default="{ row }">
            <el-tag>{{ getTypeLabel(row.document_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="author_name" label="作者" width="100" />
        <el-table-column prop="ai_generation_status" label="AI状态" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.ai_generation_status" :type="getAiStatusType(row.ai_generation_status)">
              {{ getAiStatusLabel(row.ai_generation_status) }}
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="document_status" label="文档状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.document_status)">
              {{ getStatusLabel(row.document_status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button
              v-permission="['module_promotion:document:detail']"
              link
              type="primary"
              @click="handleView(row)"
            >
              详情
            </el-button>
            <el-button
              v-permission="['module_promotion:document:update']"
              link
              type="primary"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              v-permission="['module_promotion:document:generate']"
              link
              type="success"
              :disabled="row.ai_generation_status === 'generating'"
              @click="handleGenerateWechat(row)"
            >
              AI生成
            </el-button>
            <el-button
              v-permission="['module_promotion:document:delete']"
              link
              type="danger"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailDialog.visible" title="活动撰写详情" width="800px">
      <el-descriptions v-if="detailDialog.data" :column="2" border>
        <el-descriptions-item label="文档编号">
          {{ detailDialog.data.document_no }}
        </el-descriptions-item>
        <el-descriptions-item label="文档类型">
          <el-tag>{{ getTypeLabel(detailDialog.data.document_type) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="文档标题" :span="2">
          {{ detailDialog.data.document_title || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="活动名称">
          {{ detailDialog.data.activity_name || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="作者">
          {{ detailDialog.data.author_name || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="AI生成状态">
          <el-tag v-if="detailDialog.data.ai_generation_status" :type="getAiStatusType(detailDialog.data.ai_generation_status)">
            {{ getAiStatusLabel(detailDialog.data.ai_generation_status) }}
          </el-tag>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="文档状态">
          <el-tag :type="getStatusType(detailDialog.data.document_status)">
            {{ getStatusLabel(detailDialog.data.document_status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="浏览次数">
          {{ detailDialog.data.view_count || 0 }}
        </el-descriptions-item>
        <el-descriptions-item label="关键词" :span="2">
          {{ detailDialog.data.keywords || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="文档摘要" :span="2">
          {{ detailDialog.data.document_summary || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="文档内容" :span="2">
          <div style="white-space: pre-wrap; max-height: 200px; overflow-y: auto">
            {{ detailDialog.data.document_content || "-" }}
          </div>
        </el-descriptions-item>
        <el-descriptions-item label="微信公众号内容" :span="2">
          <div v-if="detailDialog.data.wechat_formatted_content" style="max-height: 300px; overflow-y: auto">
            <div v-html="detailDialog.data.wechat_formatted_content"></div>
          </div>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">
          {{ detailDialog.data.remark || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">
          {{ detailDialog.data.created_time }}
        </el-descriptions-item>
        <el-descriptions-item label="更新时间">
          {{ detailDialog.data.updated_time }}
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 新增/编辑弹窗 -->
    <el-dialog
      v-model="formDialog.visible"
      :title="formDialog.type === 'create' ? '新增活动撰写' : '编辑活动撰写'"
      width="650px"
    >
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="活动名称" prop="activity_name">
          <el-input v-model="form.activity_name" placeholder="请输入活动名称" />
        </el-form-item>
        <el-form-item label="文档标题" prop="document_title">
          <el-input v-model="form.document_title" placeholder="请输入文档标题" />
        </el-form-item>
        <el-form-item label="文档类型" prop="document_type">
          <el-select v-model="form.document_type" placeholder="请选择文档类型" style="width: 100%">
            <el-option label="新闻稿" value="news" />
            <el-option label="宣传稿" value="publicity" />
            <el-option label="邀请函" value="invitation" />
            <el-option label="通知" value="notice" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="作者ID" prop="author_id">
          <el-input-number
            v-model="form.author_id"
            :min="0"
            placeholder="作者ID"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="作者" prop="author_name">
          <el-input v-model="form.author_name" placeholder="请输入作者" />
        </el-form-item>
        <el-form-item label="关键词" prop="keywords">
          <el-input v-model="form.keywords" placeholder="请输入关键词，多个用逗号分隔" />
        </el-form-item>
        <el-form-item label="文档摘要" prop="document_summary">
          <el-input v-model="form.document_summary" type="textarea" :rows="2" placeholder="请输入文档摘要" />
        </el-form-item>
        <el-form-item label="文档内容" prop="document_content">
          <el-input
            v-model="form.document_content"
            type="textarea"
            :rows="6"
            placeholder="请输入文档内容"
          />
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
import DocumentAPI from "@/api/module_promotion/document";
import type { DocumentItem, DocumentForm, DocumentQuery } from "@/api/module_promotion/document";

const loading = ref(false);
const tableData = ref<DocumentItem[]>([]);
const selectedIds = ref<number[]>([]);

const searchFormRef = ref<FormInstance>();
const searchForm = reactive<DocumentQuery>({
  document_no: "",
  document_type: "",
  author_name: "",
  document_status: "",
});

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

const detailDialog = reactive({
  visible: false,
  data: null as DocumentItem | null,
});

const formDialog = reactive({
  visible: false,
  type: "create" as "create" | "edit",
  id: null as number | null,
});

const formRef = ref<FormInstance>();
const form = reactive<DocumentForm>({
  activity_name: "",
  document_type: "news",
  document_title: "",
  author_id: undefined,
  author_name: "",
  keywords: "",
  document_summary: "",
  document_content: "",
  remark: "",
});

const formRules: FormRules = {
  document_title: [{ required: true, message: "请输入文档标题", trigger: "blur" }],
  document_type: [{ required: true, message: "请选择文档类型", trigger: "change" }],
};

function getTypeLabel(type: string): string {
  const map: Record<string, string> = {
    news: "新闻稿",
    publicity: "宣传稿",
    invitation: "邀请函",
    notice: "通知",
    other: "其他",
  };
  return map[type] || type;
}

function getStatusLabel(status: string): string {
  const map: Record<string, string> = {
    draft: "草稿",
    pending: "待发布",
    published: "已发布",
    archived: "已归档",
  };
  return map[status] || status;
}

function getStatusType(status: string): string {
  const map: Record<string, string> = {
    draft: "info",
    pending: "warning",
    published: "success",
    archived: "info",
  };
  return map[status] || "info";
}

function getAiStatusLabel(status: string): string {
  const map: Record<string, string> = {
    pending: "待生成",
    generating: "生成中",
    success: "已生成",
    failed: "失败",
  };
  return map[status] || status;
}

function getAiStatusType(status: string): string {
  const map: Record<string, string> = {
    pending: "info",
    generating: "warning",
    success: "success",
    failed: "danger",
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
    const res = await DocumentAPI.getList(params);
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

function handleSelectionChange(selection: DocumentItem[]) {
  selectedIds.value = selection.map((item) => item.id);
}

function handleCreate() {
  formDialog.type = "create";
  formDialog.id = null;
  Object.assign(form, {
    activity_name: "",
    document_type: "news",
    document_title: "",
    author_id: undefined,
    author_name: "",
    keywords: "",
    document_summary: "",
    document_content: "",
    remark: "",
  });
  formDialog.visible = true;
}

function handleEdit(row: DocumentItem) {
  formDialog.type = "edit";
  formDialog.id = row.id;
  Object.assign(form, row);
  formDialog.visible = true;
}

async function handleView(row: DocumentItem) {
  try {
    const res = await DocumentAPI.getDetail(row.id);
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

async function handleGenerateWechat(row: DocumentItem) {
  if (!row.document_content) {
    ElMessage.warning("文档内容为空，无法生成");
    return;
  }
  try {
    await ElMessageBox.confirm("确定要AI生成微信公众号内容吗？", "提示", {
      type: "info",
    });
    const res = await DocumentAPI.generateWechatContent(row.id);
    if (res.data.code === 0) {
      ElMessage.success("生成成功");
      fetchData();
      if (detailDialog.visible && detailDialog.data?.id === row.id) {
        detailDialog.data = res.data.data;
      }
    } else {
      ElMessage.error(res.data.msg || "生成失败");
    }
  } catch {
    // 用户取消
  }
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false);
  if (!valid) return;

  try {
    if (formDialog.type === "create") {
      const res = await DocumentAPI.create(form);
      if (res.data.code === 0) {
        ElMessage.success("创建成功");
        formDialog.visible = false;
        fetchData();
      } else {
        ElMessage.error(res.data.msg || "创建失败");
      }
    } else {
      const res = await DocumentAPI.update(formDialog.id!, form);
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

async function handleDelete(row: DocumentItem) {
  try {
    await ElMessageBox.confirm("确定要删除该活动撰写吗？", "提示", {
      type: "warning",
    });
    const res = await DocumentAPI.delete(row.id);
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
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedIds.value.length} 个活动撰写吗？`,
      "提示",
      {
        type: "warning",
      }
    );
    const res = await DocumentAPI.batchDelete(selectedIds.value);
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
