<!-- 招生宣传活动 - 活动打卡 -->
<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="80px">
        <el-form-item label="活动ID" prop="activity_id">
          <el-input-number v-model="searchForm.activity_id" :min="1" style="width: 120px" />
        </el-form-item>
        <el-form-item label="人员ID" prop="personnel_id">
          <el-input-number v-model="searchForm.personnel_id" :min="1" style="width: 120px" />
        </el-form-item>
        <el-form-item label="打卡类型" prop="checkin_type">
          <el-select
            v-model="searchForm.checkin_type"
            placeholder="请选择类型"
            clearable
            style="width: 140px"
          >
            <el-option label="上班打卡" value="check_in" />
            <el-option label="下班打卡" value="check_out" />
            <el-option label="位置打卡" value="location" />
            <el-option label="照片打卡" value="photo" />
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
          <span class="title">活动打卡列表</span>
          <div class="operations">
            <el-button
              v-permission="['module_promotion:checkin:create']"
              type="primary"
              @click="handleCreate"
            >
              <i-ep-plus />
              新增
            </el-button>
            <el-button
              v-permission="['module_promotion:checkin:delete']"
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
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="checkin_time" label="打卡时间" width="160" />
        <el-table-column prop="checkin_type" label="打卡类型" width="100">
          <template #default="{ row }">
            <el-tag>{{ getTypeLabel(row.checkin_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="location" label="打卡位置" min-width="150" show-overflow-tooltip />
        <el-table-column prop="latitude" label="纬度" width="120" />
        <el-table-column prop="longitude" label="经度" width="120" />
        <el-table-column prop="gps_validated" label="GPS验证" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.gps_validated !== undefined" :type="row.gps_validated === 1 ? 'success' : 'danger'">
              {{ row.gps_validated === 1 ? "通过" : "未通过" }}
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="gps_distance" label="距离(米)" width="100">
          <template #default="{ row }">
            {{ row.gps_distance !== undefined ? row.gps_distance : "-" }}
          </template>
        </el-table-column>
        <el-table-column prop="remarks" label="备注" min-width="100" show-overflow-tooltip />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              v-permission="['module_promotion:checkin:detail']"
              link
              type="primary"
              @click="handleView(row)"
            >
              详情
            </el-button>
            <el-button
              v-permission="['module_promotion:checkin:gps_validate']"
              link
              type="success"
              @click="handleGpsValidate(row)"
            >
              GPS验证
            </el-button>
            <el-button
              v-permission="['module_promotion:checkin:delete']"
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
    <el-dialog v-model="detailDialog.visible" title="活动打卡详情" width="600px">
      <el-descriptions v-if="detailDialog.data" :column="2" border>
        <el-descriptions-item label="ID">
          {{ detailDialog.data.id }}
        </el-descriptions-item>
        <el-descriptions-item label="活动ID">
          {{ detailDialog.data.activity_id || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="人员ID">
          {{ detailDialog.data.personnel_id || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="打卡时间">
          {{ detailDialog.data.checkin_time || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="打卡类型">
          <el-tag>{{ getTypeLabel(detailDialog.data.checkin_type) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="打卡位置" :span="2">
          {{ detailDialog.data.location || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="纬度">
          {{ detailDialog.data.latitude || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="经度">
          {{ detailDialog.data.longitude || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="目标纬度">
          {{ detailDialog.data.target_latitude || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="目标经度">
          {{ detailDialog.data.target_longitude || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="允许半径(米)">
          {{ detailDialog.data.allowed_radius || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="GPS验证">
          <el-tag v-if="detailDialog.data.gps_validated !== undefined" :type="detailDialog.data.gps_validated === 1 ? 'success' : 'danger'">
            {{ detailDialog.data.gps_validated === 1 ? "通过" : "未通过" }}
          </el-tag>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="GPS距离(米)">
          {{ detailDialog.data.gps_distance || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">
          {{ detailDialog.data.remarks || "-" }}
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
      :title="formDialog.type === 'create' ? '新增打卡' : '编辑打卡'"
      width="600px"
    >
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="110px">
        <el-form-item label="活动ID" prop="activity_id">
          <el-input-number
            v-model="form.activity_id"
            :min="0"
            placeholder="活动ID"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="人员ID" prop="personnel_id">
          <el-input-number
            v-model="form.personnel_id"
            :min="0"
            placeholder="人员ID"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="打卡时间" prop="checkin_time">
          <el-date-picker
            v-model="form.checkin_time"
            type="datetime"
            placeholder="选择打卡时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="打卡类型" prop="checkin_type">
          <el-select v-model="form.checkin_type" placeholder="请选择打卡类型" style="width: 100%">
            <el-option label="上班打卡" value="check_in" />
            <el-option label="下班打卡" value="check_out" />
            <el-option label="位置打卡" value="location" />
            <el-option label="照片打卡" value="photo" />
          </el-select>
        </el-form-item>
        <el-form-item label="打卡位置" prop="location">
          <el-input v-model="form.location" placeholder="请输入打卡位置" />
        </el-form-item>
        <el-form-item label="纬度" prop="latitude">
          <el-input-number
            v-model="form.latitude"
            :precision="6"
            :step="0.000001"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="经度" prop="longitude">
          <el-input-number
            v-model="form.longitude"
            :precision="6"
            :step="0.000001"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="目标纬度" prop="target_latitude">
          <el-input-number
            v-model="form.target_latitude"
            :precision="6"
            :step="0.000001"
            style="width: 100%"
            placeholder="目标地点纬度"
          />
        </el-form-item>
        <el-form-item label="目标经度" prop="target_longitude">
          <el-input-number
            v-model="form.target_longitude"
            :precision="6"
            :step="0.000001"
            style="width: 100%"
            placeholder="目标地点经度"
          />
        </el-form-item>
        <el-form-item label="允许半径(米)" prop="allowed_radius">
          <el-input-number
            v-model="form.allowed_radius"
            :min="0"
            :step="10"
            style="width: 100%"
            placeholder="允许打卡半径"
          />
        </el-form-item>
        <el-form-item label="备注" prop="remarks">
          <el-input
            v-model="form.remarks"
            type="textarea"
            :rows="3"
            placeholder="请输入备注"
          />
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
import CheckinAPI from "@/api/module_promotion/checkin";
import type { CheckinItem, CheckinForm, CheckinQuery } from "@/api/module_promotion/checkin";

const loading = ref(false);
const tableData = ref<CheckinItem[]>([]);
const selectedIds = ref<number[]>([]);

const searchFormRef = ref<FormInstance>();
const searchForm = reactive<CheckinQuery>({
  activity_id: undefined,
  personnel_id: undefined,
  checkin_type: "",
});

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

const detailDialog = reactive({
  visible: false,
  data: null as CheckinItem | null,
});

const formDialog = reactive({
  visible: false,
  type: "create" as "create" | "edit",
  id: null as number | null,
});

const formRef = ref<FormInstance>();
const form = reactive<CheckinForm>({
  activity_id: undefined,
  personnel_id: undefined,
  checkin_time: "",
  checkin_type: "location",
  location: "",
  latitude: undefined,
  longitude: undefined,
  target_latitude: undefined,
  target_longitude: undefined,
  allowed_radius: 500,
  remarks: "",
});

const formRules: FormRules = {
  checkin_type: [{ required: true, message: "请选择打卡类型", trigger: "change" }],
};

function getTypeLabel(type: string): string {
  const map: Record<string, string> = {
    check_in: "上班打卡",
    check_out: "下班打卡",
    location: "位置打卡",
    photo: "照片打卡",
  };
  return map[type] || type;
}

async function fetchData() {
  loading.value = true;
  try {
    const params = {
      ...searchForm,
      page: pagination.page,
      pageSize: pagination.pageSize,
    };
    const res = await CheckinAPI.getList(params);
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

function handleSelectionChange(selection: CheckinItem[]) {
  selectedIds.value = selection.map((item) => item.id);
}

function handleCreate() {
  formDialog.type = "create";
  formDialog.id = null;
  Object.assign(form, {
    activity_id: undefined,
    personnel_id: undefined,
    checkin_time: "",
    checkin_type: "location",
    location: "",
    latitude: undefined,
    longitude: undefined,
    target_latitude: undefined,
    target_longitude: undefined,
    allowed_radius: 500,
    remarks: "",
  });
  formDialog.visible = true;
}

async function handleView(row: CheckinItem) {
  try {
    const res = await CheckinAPI.getDetail(row.id);
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

async function handleGpsValidate(row: CheckinItem) {
  try {
    const res = await CheckinAPI.gpsValidate(row.id);
    if (res.data.code === 0) {
      ElMessage.success(res.data.msg || "GPS验证成功");
      fetchData();
      if (detailDialog.visible && detailDialog.data?.id === row.id) {
        detailDialog.data = res.data.data;
      }
    } else {
      ElMessage.error(res.data.msg || "GPS验证失败");
    }
  } catch {
    ElMessage.error("GPS验证失败");
  }
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false);
  if (!valid) return;

  try {
    if (formDialog.type === "create") {
      const res = await CheckinAPI.create(form);
      if (res.data.code === 0) {
        ElMessage.success("创建成功");
        formDialog.visible = false;
        fetchData();
      } else {
        ElMessage.error(res.data.msg || "创建失败");
      }
    } else {
      const res = await CheckinAPI.update(formDialog.id!, form);
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

async function handleDelete(row: CheckinItem) {
  try {
    await ElMessageBox.confirm("确定要删除该打卡记录吗？", "提示", {
      type: "warning",
    });
    const res = await CheckinAPI.delete(row.id);
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
      `确定要删除选中的 ${selectedIds.value.length} 个打卡记录吗？`,
      "提示",
      {
        type: "warning",
      }
    );
    const res = await CheckinAPI.batchDelete(selectedIds.value);
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
