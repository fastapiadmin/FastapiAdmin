<!-- 招生宣传活动 - 物料管理 -->
<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="80px">
        <el-form-item label="物料名称" prop="name">
          <el-input
            v-model="searchForm.name"
            placeholder="请输入物料名称"
            clearable
            style="width: 180px"
          />
        </el-form-item>
        <el-form-item label="物料类型" prop="material_type">
          <el-select
            v-model="searchForm.material_type"
            placeholder="请选择类型"
            clearable
            style="width: 140px"
          >
            <el-option label="宣传册" value="brochure" />
            <el-option label="易拉宝" value="banner" />
            <el-option label="名片" value="card" />
            <el-option label="文具" value="stationery" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="存放位置" prop="storage_location">
          <el-input
            v-model="searchForm.storage_location"
            placeholder="请输入存放位置"
            clearable
            style="width: 150px"
          />
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
          <span class="title">物料列表</span>
          <div class="operations">
            <el-button
              v-permission="['module_promotion:material:create']"
              type="primary"
              @click="handleCreate"
            >
              <i-ep-plus />
              新增
            </el-button>
            <el-button
              v-permission="['module_promotion:material:delete']"
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
        <el-table-column prop="name" label="物料名称" min-width="180" show-overflow-tooltip>
          <template #default="{ row }">
            <el-link type="primary" @click="handleView(row)">
              {{ row.name || "-" }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column prop="material_type" label="物料类型" width="100">
          <template #default="{ row }">
            <el-tag>{{ getTypeLabel(row.material_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="specification" label="规格" width="120" show-overflow-tooltip />
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column
          prop="storage_location"
          label="存放位置"
          width="120"
          show-overflow-tooltip
        />
        <el-table-column prop="total_stock" label="总库存" width="100" />
        <el-table-column prop="available_stock" label="可用库存" width="100">
          <template #default="{ row }">
            <span :class="{ 'stock-low': (row.available_stock || 0) < (row.low_stock_threshold || 10) }">
              {{ row.available_stock || 0 }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="low_stock_threshold" label="预警阈值" width="80" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button
              v-permission="['module_promotion:material:detail']"
              link
              type="primary"
              @click="handleView(row)"
            >
              详情
            </el-button>
            <el-button
              v-permission="['module_promotion:material:update']"
              link
              type="primary"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              v-permission="['module_promotion:material:apply']"
              link
              type="success"
              @click="handleApply(row)"
            >
              申领
            </el-button>
            <el-button
              v-permission="['module_promotion:material:delete']"
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
    <el-dialog v-model="detailDialog.visible" title="物料详情" width="600px">
      <el-descriptions v-if="detailDialog.data" :column="2" border>
        <el-descriptions-item label="物料名称" :span="2">
          {{ detailDialog.data.name }}
        </el-descriptions-item>
        <el-descriptions-item label="物料类型">
          <el-tag>{{ getTypeLabel(detailDialog.data.material_type) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="规格">
          {{ detailDialog.data.specification || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="单位">
          {{ detailDialog.data.unit || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="存放位置" :span="2">
          {{ detailDialog.data.storage_location || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="总库存">
          {{ detailDialog.data.total_stock || 0 }}
        </el-descriptions-item>
        <el-descriptions-item label="可用库存">
          {{ detailDialog.data.available_stock || 0 }}
        </el-descriptions-item>
        <el-descriptions-item label="预警阈值">
          {{ detailDialog.data.low_stock_threshold || 10 }}
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(detailDialog.data.status)">
            {{ getStatusLabel(detailDialog.data.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">
          {{ detailDialog.data.description || "-" }}
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
      :title="formDialog.type === 'create' ? '新增物料' : '编辑物料'"
      width="550px"
    >
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="物料名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入物料名称" />
        </el-form-item>
        <el-form-item label="物料类型" prop="material_type">
          <el-select v-model="form.material_type" placeholder="请选择物料类型" style="width: 100%">
            <el-option label="宣传册" value="brochure" />
            <el-option label="易拉宝" value="banner" />
            <el-option label="名片" value="card" />
            <el-option label="文具" value="stationery" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="规格" prop="specification">
          <el-input v-model="form.specification" placeholder="请输入规格" />
        </el-form-item>
        <el-form-item label="单位" prop="unit">
          <el-input v-model="form.unit" placeholder="请输入单位" />
        </el-form-item>
        <el-form-item label="存放位置" prop="storage_location">
          <el-input v-model="form.storage_location" placeholder="请输入存放位置" />
        </el-form-item>
        <el-form-item label="总库存" prop="total_stock">
          <el-input-number v-model="form.total_stock" :min="0" style="width: 100%" />
        </el-form-item>
        <el-form-item label="可用库存" prop="available_stock">
          <el-input-number v-model="form.available_stock" :min="0" style="width: 100%" />
        </el-form-item>
        <el-form-item label="预警阈值" prop="low_stock_threshold">
          <el-input-number v-model="form.low_stock_threshold" :min="0" style="width: 100%" />
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="form.remark" type="textarea" :rows="3" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="formDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 申领弹窗 -->
    <el-dialog v-model="applyDialog.visible" title="申领物料" width="450px">
      <el-form ref="applyFormRef" :model="applyForm" :rules="applyFormRules" label-width="100px">
        <el-form-item label="物料名称">
          {{ applyDialog.materialName }}
        </el-form-item>
        <el-form-item label="可用库存">
          {{ applyDialog.availableStock }}
        </el-form-item>
        <el-form-item label="申领数量" prop="apply_quantity">
          <el-input-number v-model="applyForm.apply_quantity" :min="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="使用日期" prop="use_date">
          <el-date-picker
            v-model="applyForm.use_date"
            type="date"
            placeholder="选择使用日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="使用目的" prop="use_purpose">
          <el-input v-model="applyForm.use_purpose" placeholder="请输入使用目的" />
        </el-form-item>
        <el-form-item label="备注" prop="remarks">
          <el-input v-model="applyForm.remarks" type="textarea" :rows="2" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="applyDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleApplySubmit">确定申领</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import type { FormInstance, FormRules } from "element-plus";
import { ElMessage, ElMessageBox } from "element-plus";
import MaterialAPI from "@/api/module_promotion/material";
import type { MaterialItem, MaterialForm, MaterialQuery } from "@/api/module_promotion/material";

const loading = ref(false);
const tableData = ref<MaterialItem[]>([]);
const selectedIds = ref<number[]>([]);

const searchFormRef = ref<FormInstance>();
const searchForm = reactive<MaterialQuery>({
  name: "",
  material_type: "",
  storage_location: "",
});

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

const detailDialog = reactive({
  visible: false,
  data: null as MaterialItem | null,
});

const formDialog = reactive({
  visible: false,
  type: "create" as "create" | "edit",
  id: null as number | null,
});

const applyDialog = reactive({
  visible: false,
  materialId: null as number | null,
  materialName: "",
  availableStock: 0,
});

const applyFormRef = ref<FormInstance>();
const applyForm = reactive({
  apply_quantity: 1,
  use_date: "",
  use_purpose: "",
  remarks: "",
});

const applyFormRules: FormRules = {
  apply_quantity: [{ required: true, message: "请输入申领数量", trigger: "blur" }],
};

const formRef = ref<FormInstance>();
const form = reactive<MaterialForm>({
  name: "",
  material_type: "brochure",
  specification: "",
  unit: "",
  storage_location: "",
  total_stock: 0,
  available_stock: 0,
  low_stock_threshold: 10,
  remark: "",
});

const formRules: FormRules = {
  name: [{ required: true, message: "请输入物料名称", trigger: "blur" }],
  material_type: [{ required: true, message: "请选择物料类型", trigger: "change" }],
};

function getTypeLabel(type: string): string {
  const map: Record<string, string> = {
    brochure: "宣传册",
    banner: "易拉宝",
    card: "名片",
    stationery: "文具",
    other: "其他",
  };
  return map[type] || type;
}

function getStatusLabel(status: string): string {
  const map: Record<string, string> = {
    active: "正常",
    inactive: "禁用",
    low: "低库存",
    out: "缺货",
  };
  return map[status] || status || "正常";
}

function getStatusType(status: string): string {
  const map: Record<string, string> = {
    active: "success",
    inactive: "info",
    low: "warning",
    out: "danger",
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
    const res = await MaterialAPI.getList(params);
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

function handleSelectionChange(selection: MaterialItem[]) {
  selectedIds.value = selection.map((item) => item.id);
}

function handleCreate() {
  formDialog.type = "create";
  formDialog.id = null;
  Object.assign(form, {
    name: "",
    material_type: "brochure",
    specification: "",
    unit: "",
    storage_location: "",
    total_stock: 0,
    available_stock: 0,
    low_stock_threshold: 10,
    remark: "",
  });
  formDialog.visible = true;
}

function handleEdit(row: MaterialItem) {
  formDialog.type = "edit";
  formDialog.id = row.id;
  Object.assign(form, row);
  formDialog.visible = true;
}

async function handleView(row: MaterialItem) {
  try {
    const res = await MaterialAPI.getDetail(row.id);
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

function handleApply(row: MaterialItem) {
  applyDialog.materialId = row.id;
  applyDialog.materialName = row.name;
  applyDialog.availableStock = row.available_stock || 0;
  Object.assign(applyForm, {
    apply_quantity: 1,
    use_date: "",
    use_purpose: "",
    remarks: "",
  });
  applyDialog.visible = true;
}

async function handleApplySubmit() {
  const valid = await applyFormRef.value?.validate().catch(() => false);
  if (!valid) return;

  try {
    const res = await fetch(`/api/v1/promotion/material/apply`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        material_id: applyDialog.materialId,
        ...applyForm,
      }),
    });
    const data = await res.json();
    if (data.code === 0) {
      ElMessage.success("申领成功");
      applyDialog.visible = false;
      fetchData();
    } else {
      ElMessage.error(data.msg || "申领失败");
    }
  } catch {
    ElMessage.error("申领失败");
  }
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false);
  if (!valid) return;

  try {
    if (formDialog.type === "create") {
      const res = await MaterialAPI.create(form);
      if (res.data.code === 0) {
        ElMessage.success("创建成功");
        formDialog.visible = false;
        fetchData();
      } else {
        ElMessage.error(res.data.msg || "创建失败");
      }
    } else {
      const res = await MaterialAPI.update(formDialog.id!, form);
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

async function handleDelete(row: MaterialItem) {
  try {
    await ElMessageBox.confirm("确定要删除该物料吗？", "提示", {
      type: "warning",
    });
    const res = await MaterialAPI.delete(row.id);
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
      `确定要删除选中的 ${selectedIds.value.length} 个物料吗？`,
      "提示",
      {
        type: "warning",
      }
    );
    const res = await MaterialAPI.batchDelete(selectedIds.value);
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
.stock-low {
  color: #f56c6c;
  font-weight: bold;
}
</style>
