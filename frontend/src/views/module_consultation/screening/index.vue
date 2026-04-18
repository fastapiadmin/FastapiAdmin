<!-- 招生咨询会 - 筛选匹配管理 -->
<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="80px">
        <el-form-item label="筛选名称" prop="name">
          <el-input v-model="searchForm.name" placeholder="请输入筛选名称" clearable style="width: 200px" />
        </el-form-item>
        <el-form-item label="是否默认" prop="is_default">
          <el-select v-model="searchForm.is_default" placeholder="请选择" clearable style="width: 120px">
            <el-option label="是" :value="true" />
            <el-option label="否" :value="false" />
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
          <span class="title">筛选条件列表</span>
          <div class="operations">
            <el-button v-permission="['module_consultation:screening:create']" type="primary" @click="handleCreate"><i-ep-plus /> 新增</el-button>
            <el-button v-permission="['module_consultation:screening:delete']" type="danger" :disabled="!selectedIds.length" @click="handleBatchDelete"><i-ep-delete /> 批量删除</el-button>
          </div>
        </div>
      </template>

      <el-table v-loading="loading" :data="tableData" stripe border @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="name" label="筛选名称" min-width="150" show-overflow-tooltip>
          <template #default="{ row }">
            <el-link type="primary" @click="handleView(row)">{{ row.name }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="province" label="省份" width="100" />
        <el-table-column prop="city" label="城市" width="100" />
        <el-table-column prop="start_date_begin" label="开始日期" width="110">
          <template #default="{ row }">{{ row.start_date_begin || '-' }}</template>
        </el-table-column>
        <el-table-column prop="start_date_end" label="结束日期" width="110">
          <template #default="{ row }">{{ row.start_date_end || '-' }}</template>
        </el-table-column>
        <el-table-column prop="organizer_type" label="主办方类型" width="120" />
        <el-table-column prop="compliance_level" label="合规等级" width="100">
          <template #default="{ row }">{{ row.compliance_level || '-' }}</template>
        </el-table-column>
        <el-table-column prop="is_default" label="默认" width="70" align="center">
          <template #default="{ row }">
            <el-tag v-if="row.is_default" type="success" size="small">是</el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button v-permission="['module_consultation:screening:detail']" link type="primary" @click="handleView(row)">详情</el-button>
            <el-button v-permission="['module_consultation:screening:update']" link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button v-permission="['module_consultation:screening:update']" link type="success" @click="handleSetDefault(row)">设为默认</el-button>
            <el-button v-permission="['module_consultation:screening:delete']" link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination v-model:current-page="pagination.page" v-model:page-size="pagination.pageSize" :total="pagination.total" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" @size-change="handleSizeChange" @current-change="handlePageChange" />
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailDialog.visible" title="筛选条件详情" width="700px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="筛选名称" :span="2">{{ detailDialog.data?.name }}</el-descriptions-item>
        <el-descriptions-item label="省份">{{ detailDialog.data?.province || '-' }}</el-descriptions-item>
        <el-descriptions-item label="城市">{{ detailDialog.data?.city || '-' }}</el-descriptions-item>
        <el-descriptions-item label="开始日期">{{ detailDialog.data?.start_date_begin || '-' }}</el-descriptions-item>
        <el-descriptions-item label="结束日期">{{ detailDialog.data?.start_date_end || '-' }}</el-descriptions-item>
        <el-descriptions-item label="主办方类型">{{ detailDialog.data?.organizer_type || '-' }}</el-descriptions-item>
        <el-descriptions-item label="高校数量">{{ detailDialog.data?.university_count_min || '-' }} - {{ detailDialog.data?.university_count_max || '-' }}</el-descriptions-item>
        <el-descriptions-item label="展位费">{{ detailDialog.data?.booth_fee_min || '-' }} - {{ detailDialog.data?.booth_fee_max || '-' }}</el-descriptions-item>
        <el-descriptions-item label="预计人数">{{ detailDialog.data?.estimated_visitors_min || '-' }} - {{ detailDialog.data?.estimated_visitors_max || '-' }}</el-descriptions-item>
        <el-descriptions-item label="合规评分">{{ detailDialog.data?.compliance_score_min || '-' }} - {{ detailDialog.data?.compliance_score_max || '-' }}</el-descriptions-item>
        <el-descriptions-item label="合规等级">{{ detailDialog.data?.compliance_level || '-' }}</el-descriptions-item>
        <el-descriptions-item label="信息来源">{{ detailDialog.data?.source_type || '-' }}</el-descriptions-item>
        <el-descriptions-item label="排序">{{ detailDialog.data?.order_by }} / {{ detailDialog.data?.order_direction }}</el-descriptions-item>
        <el-descriptions-item label="默认">
          <el-tag v-if="detailDialog.data?.is_default" type="success">是</el-tag>
          <span v-else>否</span>
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="formDialog.visible" :title="formDialog.type === 'create' ? '新增筛选条件' : '编辑筛选条件'" width="700px">
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="120px">
        <el-form-item label="筛选名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入筛选名称" />
        </el-form-item>
        <el-form-item label="省份" prop="province">
          <el-input v-model="form.province" placeholder="请输入省份" />
        </el-form-item>
        <el-form-item label="城市" prop="city">
          <el-input v-model="form.city" placeholder="请输入城市" />
        </el-form-item>
        <el-form-item label="开始日期范围" prop="start_date_begin">
          <el-date-picker v-model="form.start_date_begin" type="date" placeholder="开始日期" value-format="YYYY-MM-DD" style="width: 150px" />
          <span style="margin: 0 10px;">至</span>
          <el-date-picker v-model="form.start_date_end" type="date" placeholder="结束日期" value-format="YYYY-MM-DD" style="width: 150px" />
        </el-form-item>
        <el-form-item label="主办方类型" prop="organizer_type">
          <el-select v-model="form.organizer_type" placeholder="请选择" clearable style="width: 200px">
            <el-option label="教育部门" value="education_department" />
            <el-option label="高校" value="university" />
            <el-option label="中学" value="high_school" />
            <el-option label="机构" value="organization" />
          </el-select>
        </el-form-item>
        <el-form-item label="高校数量范围">
          <el-input-number v-model="form.university_count_min" :min="0" placeholder="最小" style="width: 120px" />
          <span style="margin: 0 10px;">-</span>
          <el-input-number v-model="form.university_count_max" :min="0" placeholder="最大" style="width: 120px" />
        </el-form-item>
        <el-form-item label="展位费范围">
          <el-input-number v-model="form.booth_fee_min" :min="0" :precision="2" placeholder="最小" style="width: 120px" />
          <span style="margin: 0 10px;">-</span>
          <el-input-number v-model="form.booth_fee_max" :min="0" :precision="2" placeholder="最大" style="width: 120px" />
        </el-form-item>
        <el-form-item label="预计人数范围">
          <el-input-number v-model="form.estimated_visitors_min" :min="0" placeholder="最小" style="width: 120px" />
          <span style="margin: 0 10px;">-</span>
          <el-input-number v-model="form.estimated_visitors_max" :min="0" placeholder="最大" style="width: 120px" />
        </el-form-item>
        <el-form-item label="合规评分范围">
          <el-input-number v-model="form.compliance_score_min" :min="0" :max="100" placeholder="最小" style="width: 120px" />
          <span style="margin: 0 10px;">-</span>
          <el-input-number v-model="form.compliance_score_max" :min="0" :max="100" placeholder="最大" style="width: 120px" />
        </el-form-item>
        <el-form-item label="合规等级" prop="compliance_level">
          <el-select v-model="form.compliance_level" placeholder="请选择" clearable style="width: 150px">
            <el-option label="高" value="high" />
            <el-option label="中" value="medium" />
            <el-option label="低" value="low" />
          </el-select>
        </el-form-item>
        <el-form-item label="信息来源" prop="source_type">
          <el-select v-model="form.source_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="全网抓取" value="crawler" />
            <el-option label="第三方上传" value="upload" />
            <el-option label="手动录入" value="manual" />
          </el-select>
        </el-form-item>
        <el-form-item label="排序字段" prop="order_by">
          <el-select v-model="form.order_by" placeholder="请选择" style="width: 150px">
            <el-option label="创建时间" value="created_time" />
            <el-option label="开始日期" value="start_date" />
            <el-option label="合规评分" value="compliance_score" />
          </el-select>
          <el-select v-model="form.order_direction" placeholder="方向" style="width: 100px; margin-left: 10px;">
            <el-option label="升序" value="asc" />
            <el-option label="降序" value="desc" />
          </el-select>
        </el-form-item>
        <el-form-item label="设为默认" prop="is_default">
          <el-switch v-model="form.is_default" />
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
import ScreeningAPI from "@/api/module_consultation/screening";
import type { ScreeningItem, ScreeningQuery } from "@/api/module_consultation/screening";

const searchForm = reactive<ScreeningQuery>({ name: undefined, is_default: undefined });
const loading = ref(false);
const tableData = ref<ScreeningItem[]>([]);
const selectedIds = ref<number[]>([]);
const pagination = reactive({ page: 1, pageSize: 10, total: 0 });

const formDialog = reactive({ visible: false, type: "create" as "create" | "edit", data: undefined as ScreeningItem | undefined });
const detailDialog = reactive({ visible: false, data: undefined as ScreeningItem | undefined });
const formRef = ref<FormInstance>();

const form = reactive<any>({
  name: "",
  province: "",
  city: "",
  start_date_begin: "",
  start_date_end: "",
  organizer_type: "",
  university_count_min: undefined,
  university_count_max: undefined,
  booth_fee_min: undefined,
  booth_fee_max: undefined,
  estimated_visitors_min: undefined,
  estimated_visitors_max: undefined,
  compliance_score_min: undefined,
  compliance_score_max: undefined,
  compliance_level: "",
  source_type: "",
  order_by: "created_time",
  order_direction: "desc",
  is_default: false,
});

const formRules: FormRules = { name: [{ required: true, message: "请输入筛选名称", trigger: "blur" }] };

const fetchList = async () => {
  loading.value = true;
  try {
    const params = { page_no: pagination.page, page_size: pagination.pageSize, ...searchForm };
    const res = await ScreeningAPI.getList(params);
    if (res.data?.data) { tableData.value = res.data.data.items || []; pagination.total = res.data.data.total || 0; }
  } finally { loading.value = false; }
};

const handleSearch = () => { pagination.page = 1; fetchList(); };
const handleReset = () => { Object.assign(searchForm, { name: undefined, is_default: undefined }); handleSearch(); };
const handleSelectionChange = (selection: ScreeningItem[]) => { selectedIds.value = selection.map(item => item.id!); };
const handleSizeChange = (size: number) => { pagination.pageSize = size; fetchList(); };
const handlePageChange = (page: number) => { pagination.page = page; fetchList(); };

const handleCreate = () => {
  formDialog.type = "create";
  Object.assign(form, { name: "", province: "", city: "", start_date_begin: "", start_date_end: "", organizer_type: "", university_count_min: undefined, university_count_max: undefined, booth_fee_min: undefined, booth_fee_max: undefined, estimated_visitors_min: undefined, estimated_visitors_max: undefined, compliance_score_min: undefined, compliance_score_max: undefined, compliance_level: "", source_type: "", order_by: "created_time", order_direction: "desc", is_default: false });
  formDialog.visible = true;
};

const handleView = (row: ScreeningItem) => { detailDialog.data = row; detailDialog.visible = true; };

const handleEdit = (row: ScreeningItem) => {
  formDialog.type = "edit";
  formDialog.data = row;
  Object.assign(form, row);
  formDialog.visible = true;
};

const handleSubmit = async () => {
  if (!formRef.value) return;
  await formRef.value.validate(async (valid) => {
    if (valid) {
      if (formDialog.type === "create") { await ScreeningAPI.create(form); ElMessage.success("创建成功"); }
      else { await ScreeningAPI.update(formDialog.data!.id!, form); ElMessage.success("更新成功"); }
      formDialog.visible = false;
      fetchList();
    }
  });
};

const handleDelete = (row: ScreeningItem) => {
  ElMessageBox.confirm(`确定要删除筛选条件 "${row.name}" 吗？`, "删除确认", { confirmButtonText: "确定", cancelButtonText: "取消", type: "warning" })
    .then(async () => { await ScreeningAPI.delete(row.id!); ElMessage.success("删除成功"); fetchList(); }).catch(() => {});
};

const handleBatchDelete = () => {
  if (!selectedIds.value.length) { ElMessage.warning("请选择要删除的记录"); return; }
  ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 条记录吗？`, "批量删除确认", { confirmButtonText: "确定", cancelButtonText: "取消", type: "warning" })
    .then(async () => { await ScreeningAPI.batchDelete(selectedIds.value); ElMessage.success("批量删除成功"); fetchList(); }).catch(() => {});
};

const handleSetDefault = (row: ScreeningItem) => {
  ElMessageBox.confirm(`确定要将 "${row.name}" 设为默认筛选条件吗？`, "设为默认", { confirmButtonText: "确定", cancelButtonText: "取消", type: "info" })
    .then(async () => { await ScreeningAPI.setDefault(row.id!); ElMessage.success("已设为默认"); fetchList(); }).catch(() => {});
};

onMounted(() => { fetchList(); });
</script>

<style lang="scss" scoped>
.search-card { margin-bottom: 16px; }
.table-card { .card-header { display: flex; justify-content: space-between; align-items: center; .title { font-size: 16px; font-weight: 600; } .operations { display: flex; gap: 8px; } } }
.pagination-container { display: flex; justify-content: flex-end; padding-top: 16px; }
</style>
