<!-- 招生咨询会 - 行程方案管理 -->
<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="80px">
        <el-form-item label="方案名称" prop="name">
          <el-input v-model="searchForm.name" placeholder="请输入方案名称" clearable style="width: 200px" />
        </el-form-item>
        <el-form-item label="高校ID" prop="university_id">
          <el-input-number v-model="searchForm.university_id" :min="1" style="width: 150px" />
        </el-form-item>
        <el-form-item label="招生组ID" prop="team_id">
          <el-input-number v-model="searchForm.team_id" :min="1" style="width: 150px" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable style="width: 150px">
            <el-option label="草稿" value="draft" />
            <el-option label="已确认" value="confirmed" />
            <el-option label="执行中" value="executed" />
            <el-option label="已完成" value="completed" />
            <el-option label="已归档" value="archived" />
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
          <span class="title">行程方案列表</span>
          <div class="operations">
            <el-button v-permission="['module_consultation:itinerary:create']" type="primary" @click="handleCreate"><i-ep-plus /> 新增</el-button>
            <el-button v-permission="['module_consultation:itinerary:delete']" type="danger" :disabled="!selectedIds.length" @click="handleBatchDelete"><i-ep-delete /> 批量删除</el-button>
          </div>
        </div>
      </template>

      <el-table v-loading="loading" :data="tableData" stripe border @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="name" label="方案名称" min-width="180" show-overflow-tooltip>
          <template #default="{ row }">
            <el-link type="primary" @click="handleView(row)">{{ row.name }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="university_id" label="高校ID" width="100" />
        <el-table-column prop="team_id" label="招生组ID" width="100" />
        <el-table-column prop="start_date" label="开始日期" width="120" />
        <el-table-column prop="end_date" label="结束日期" width="120" />
        <el-table-column prop="consultation_ids" label="咨询会数量" width="100" align="center">
          <template #default="{ row }">{{ row.consultation_ids?.length || 0 }}</template>
        </el-table-column>
        <el-table-column prop="estimated_cost" label="预计费用" width="100" align="center">
          <template #default="{ row }">{{ row.estimated_cost !== null ? `¥${row.estimated_cost}` : '-' }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_synced" label="已同步" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_synced ? 'success' : 'info'">{{ row.is_synced ? '是' : '否' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="300" fixed="right">
          <template #default="{ row }">
            <el-button v-permission="['module_consultation:itinerary:detail']" link type="primary" @click="handleView(row)">详情</el-button>
            <el-button v-permission="['module_consultation:itinerary:update']" link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button v-if="row.status === 'draft'" v-permission="['module_consultation:itinerary:update']" link type="success" @click="handleConfirm(row)">确认</el-button>
            <el-button v-if="row.status === 'confirmed'" v-permission="['module_consultation:itinerary:update']" link type="warning" @click="handleExecute(row)">执行</el-button>
            <el-button v-permission="['module_consultation:itinerary:update']" link type="info" @click="handleOptimize(row)">优化</el-button>
            <el-button v-permission="['module_consultation:itinerary:delete']" link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination v-model:current-page="pagination.page" v-model:page-size="pagination.pageSize" :total="pagination.total" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" @size-change="handleSizeChange" @current-change="handlePageChange" />
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailDialog.visible" title="行程方案详情" width="700px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="方案名称" :span="2">{{ detailDialog.data?.name }}</el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">{{ detailDialog.data?.description }}</el-descriptions-item>
        <el-descriptions-item label="高校ID">{{ detailDialog.data?.university_id }}</el-descriptions-item>
        <el-descriptions-item label="招生组ID">{{ detailDialog.data?.team_id }}</el-descriptions-item>
        <el-descriptions-item label="开始日期">{{ detailDialog.data?.start_date }}</el-descriptions-item>
        <el-descriptions-item label="结束日期">{{ detailDialog.data?.end_date }}</el-descriptions-item>
        <el-descriptions-item label="咨询会数量">{{ detailDialog.data?.consultation_ids?.length || 0 }}</el-descriptions-item>
        <el-descriptions-item label="总距离">{{ detailDialog.data?.total_distance }} km</el-descriptions-item>
        <el-descriptions-item label="预计时长">{{ detailDialog.data?.estimated_duration }} 小时</el-descriptions-item>
        <el-descriptions-item label="预计费用">¥{{ detailDialog.data?.estimated_cost }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(detailDialog.data?.status)">{{ getStatusLabel(detailDialog.data?.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="已同步">
          <el-tag :type="detailDialog.data?.is_synced ? 'success' : 'info'">{{ detailDialog.data?.is_synced ? '是' : '否' }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="咨询会IDs" :span="2">{{ detailDialog.data?.consultation_ids?.join(', ') }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="formDialog.visible" :title="formDialog.type === 'create' ? '新增行程方案' : '编辑行程方案'" width="600px">
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="方案名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入方案名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="高校ID" prop="university_id">
          <el-input-number v-model="form.university_id" :min="1" style="width: 200px" />
        </el-form-item>
        <el-form-item label="招生组ID" prop="team_id">
          <el-input-number v-model="form.team_id" :min="1" style="width: 200px" />
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker v-model="form.start_date" type="date" placeholder="选择开始日期" value-format="YYYY-MM-DD" style="width: 200px" />
        </el-form-item>
        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker v-model="form.end_date" type="date" placeholder="选择结束日期" value-format="YYYY-MM-DD" style="width: 200px" />
        </el-form-item>
        <el-form-item label="预计距离(km)" prop="total_distance">
          <el-input-number v-model="form.total_distance" :min="0" :precision="1" style="width: 200px" />
        </el-form-item>
        <el-form-item label="预计时长(小时)" prop="estimated_duration">
          <el-input-number v-model="form.estimated_duration" :min="0" style="width: 200px" />
        </el-form-item>
        <el-form-item label="预计费用" prop="estimated_cost">
          <el-input-number v-model="form.estimated_cost" :min="0" :precision="2" style="width: 200px" />
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
import { reactive, ref, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";
import ItineraryAPI from "@/api/module_consultation/itinerary";
import type { ItineraryItem, ItineraryQuery } from "@/api/module_consultation/itinerary";

const searchForm = reactive<ItineraryQuery>({ name: undefined, university_id: undefined, team_id: undefined, status: undefined });
const loading = ref(false);
const tableData = ref<ItineraryItem[]>([]);
const selectedIds = ref<number[]>([]);
const pagination = reactive({ page: 1, pageSize: 10, total: 0 });

const formDialog = reactive({ visible: false, type: "create" as "create" | "edit", data: undefined as ItineraryItem | undefined });
const detailDialog = reactive({ visible: false, data: undefined as ItineraryItem | undefined });
const formRef = ref<FormInstance>();

const form = reactive<any>({ name: "", description: "", university_id: undefined, team_id: undefined, start_date: "", end_date: "", total_distance: undefined, estimated_duration: undefined, estimated_cost: undefined });
const formRules: FormRules = { name: [{ required: true, message: "请输入方案名称", trigger: "blur" }], start_date: [{ required: true, message: "请选择开始日期", trigger: "change" }], end_date: [{ required: true, message: "请选择结束日期", trigger: "change" }] };

const fetchList = async () => {
  loading.value = true;
  try {
    const params = { page_no: pagination.page, page_size: pagination.pageSize, ...searchForm };
    const res = await ItineraryAPI.getList(params);
    if (res.data?.data) { tableData.value = res.data.data.items || []; pagination.total = res.data.data.total || 0; }
  } finally { loading.value = false; }
};

const handleSearch = () => { pagination.page = 1; fetchList(); };
const handleReset = () => { Object.assign(searchForm, { name: undefined, university_id: undefined, team_id: undefined, status: undefined }); handleSearch(); };
const handleSelectionChange = (selection: ItineraryItem[]) => { selectedIds.value = selection.map(item => item.id!); };
const handleSizeChange = (size: number) => { pagination.pageSize = size; fetchList(); };
const handlePageChange = (page: number) => { pagination.page = page; fetchList(); };

const getStatusType = (status: string) => ({ draft: "info", confirmed: "success", executed: "warning", completed: "success", archived: "" }[status] || "info");
const getStatusLabel = (status: string) => ({ draft: "草稿", confirmed: "已确认", executed: "执行中", completed: "已完成", archived: "已归档" }[status] || status);

const handleCreate = () => { formDialog.type = "create"; Object.assign(form, { name: "", description: "", university_id: undefined, team_id: undefined, start_date: "", end_date: "", total_distance: undefined, estimated_duration: undefined, estimated_cost: undefined }); formDialog.visible = true; };
const handleView = (row: ItineraryItem) => { detailDialog.data = row; detailDialog.visible = true; };
const handleEdit = (row: ItineraryItem) => { formDialog.type = "edit"; formDialog.data = row; Object.assign(form, row); formDialog.visible = true; };

const handleSubmit = async () => {
  if (!formRef.value) return;
  await formRef.value.validate(async (valid) => {
    if (valid) {
      if (formDialog.type === "create") { await ItineraryAPI.create(form); ElMessage.success("创建成功"); }
      else { await ItineraryAPI.update(formDialog.data!.id!, form); ElMessage.success("更新成功"); }
      formDialog.visible = false;
      fetchList();
    }
  });
};

const handleDelete = (row: ItineraryItem) => { ElMessageBox.confirm(`确定要删除 "${row.name}" 吗？`, "删除确认", { confirmButtonText: "确定", cancelButtonText: "取消", type: "warning" }).then(async () => { await ItineraryAPI.delete(row.id!); ElMessage.success("删除成功"); fetchList(); }).catch(() => {}); };

const handleBatchDelete = () => {
  if (!selectedIds.value.length) { ElMessage.warning("请选择要删除的记录"); return; }
  ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 条记录吗？`, "批量删除确认", { confirmButtonText: "确定", cancelButtonText: "取消", type: "warning" }).then(async () => { await ItineraryAPI.batchDelete(selectedIds.value); ElMessage.success("批量删除成功"); fetchList(); }).catch(() => {});
};

const handleConfirm = (row: ItineraryItem) => { ElMessageBox.confirm(`确定要确认行程方案 "${row.name}" 吗？`, "确认", { confirmButtonText: "确定", cancelButtonText: "取消", type: "info" }).then(async () => { await ItineraryAPI.confirm(row.id!); ElMessage.success("已确认"); fetchList(); }).catch(() => {}); };
const handleExecute = (row: ItineraryItem) => { ElMessageBox.confirm(`确定要执行行程方案 "${row.name}" 吗？`, "执行", { confirmButtonText: "确定", cancelButtonText: "取消", type: "info" }).then(async () => { await ItineraryAPI.execute(row.id!); ElMessage.success("已开始执行"); fetchList(); }).catch(() => {}); };
const handleOptimize = (row: ItineraryItem) => { ElMessageBox.confirm(`确定要优化行程方案 "${row.name}" 的路线吗？`, "优化路线", { confirmButtonText: "确定", cancelButtonText: "取消", type: "info" }).then(async () => { await ItineraryAPI.optimizeRoute(row.id!); ElMessage.success("路线已优化"); fetchList(); }).catch(() => {}); };

onMounted(() => { fetchList(); });
</script>

<style lang="scss" scoped>
.search-card { margin-bottom: 16px; }
.table-card { .card-header { display: flex; justify-content: space-between; align-items: center; .title { font-size: 16px; font-weight: 600; } .operations { display: flex; gap: 8px; } } }
.pagination-container { display: flex; justify-content: flex-end; padding-top: 16px; }
</style>
