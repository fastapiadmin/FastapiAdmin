<!-- 招生宣传活动 - 行程报备 -->
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
        <el-form-item label="行程编号" prop="trip_no">
          <el-input
            v-model="searchForm.trip_no"
            placeholder="请输入行程编号"
            clearable
            style="width: 150px"
          />
        </el-form-item>
        <el-form-item label="出发城市" prop="departure_city">
          <el-input
            v-model="searchForm.departure_city"
            placeholder="请输入出发城市"
            clearable
            style="width: 120px"
          />
        </el-form-item>
        <el-form-item label="目的城市" prop="destination_city">
          <el-input
            v-model="searchForm.destination_city"
            placeholder="请输入目的城市"
            clearable
            style="width: 120px"
          />
        </el-form-item>
        <el-form-item label="状态" prop="trip_status">
          <el-select
            v-model="searchForm.trip_status"
            placeholder="请选择状态"
            clearable
            style="width: 120px"
          >
            <el-option label="待出发" value="pending" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
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
          <span class="title">行程报备列表</span>
          <div class="operations">
            <el-button
              v-permission="['module_promotion:trip:create']"
              type="primary"
              @click="handleCreate"
            >
              <i-ep-plus />
              新增
            </el-button>
            <el-button
              v-permission="['module_promotion:trip:delete']"
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
        <el-table-column prop="trip_no" label="行程编号" width="150" />
        <el-table-column
          prop="activity_name"
          label="活动名称"
          min-width="150"
          show-overflow-tooltip
        />
        <el-table-column prop="personnel_name" label="人员姓名" width="100" />
        <el-table-column prop="departure_city" label="出发城市" width="100" />
        <el-table-column prop="destination_city" label="目的城市" width="100" />
        <el-table-column prop="departure_time" label="出发时间" width="160" />
        <el-table-column prop="arrival_time" label="到达时间" width="160" />
        <el-table-column prop="transportation" label="交通方式" width="100" />
        <el-table-column prop="trip_status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.trip_status)">
              {{ getStatusLabel(row.trip_status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button
              v-permission="['module_promotion:trip:detail']"
              link
              type="primary"
              @click="handleView(row)"
            >
              详情
            </el-button>
            <el-button
              v-permission="['module_promotion:trip:update']"
              link
              type="primary"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              v-permission="['module_promotion:trip:location']"
              link
              type="success"
              @click="handleLocation(row)"
            >
              更新位置
            </el-button>
            <el-button
              v-permission="['module_promotion:trip:delete']"
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
    <el-dialog v-model="detailDialog.visible" title="行程详情" width="650px">
      <el-descriptions v-if="detailDialog.data" :column="2" border>
        <el-descriptions-item label="行程编号">
          {{ detailDialog.data.trip_no }}
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(detailDialog.data.trip_status)">
            {{ getStatusLabel(detailDialog.data.trip_status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="活动名称" :span="2">
          {{ detailDialog.data.activity_name || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="人员姓名">
          {{ detailDialog.data.personnel_name || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="交通方式">
          {{ detailDialog.data.transportation || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="出发城市">
          {{ detailDialog.data.departure_city || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="目的城市">
          {{ detailDialog.data.destination_city || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="出发时间">
          {{ detailDialog.data.departure_time || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="到达时间">
          {{ detailDialog.data.arrival_time || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="车次/航班">
          {{ detailDialog.data.transportation_no || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="酒店名称">
          {{ detailDialog.data.hotel_name || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="酒店地址" :span="2">
          {{ detailDialog.data.hotel_address || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="入住日期">
          {{ detailDialog.data.check_in_date || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="退房日期">
          {{ detailDialog.data.check_out_date || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="当前位置" :span="2">
          {{ detailDialog.data.current_address || "-" }}
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
      :title="formDialog.type === 'create' ? '新增行程' : '编辑行程'"
      width="600px"
    >
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
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
        <el-form-item label="出发城市" prop="departure_city">
          <el-input v-model="form.departure_city" placeholder="请输入出发城市" />
        </el-form-item>
        <el-form-item label="目的城市" prop="destination_city">
          <el-input v-model="form.destination_city" placeholder="请输入目的城市" />
        </el-form-item>
        <el-form-item label="出发时间" prop="departure_time">
          <el-date-picker
            v-model="form.departure_time"
            type="datetime"
            placeholder="选择出发时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="到达时间" prop="arrival_time">
          <el-date-picker
            v-model="form.arrival_time"
            type="datetime"
            placeholder="选择到达时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="交通方式" prop="transportation">
          <el-input v-model="form.transportation" placeholder="请输入交通方式" />
        </el-form-item>
        <el-form-item label="车次/航班" prop="transportation_no">
          <el-input v-model="form.transportation_no" placeholder="请输入车次/航班" />
        </el-form-item>
        <el-form-item label="酒店名称" prop="hotel_name">
          <el-input v-model="form.hotel_name" placeholder="请输入酒店名称" />
        </el-form-item>
        <el-form-item label="酒店地址" prop="hotel_address">
          <el-input v-model="form.hotel_address" placeholder="请输入酒店地址" />
        </el-form-item>
        <el-form-item label="入住日期" prop="check_in_date">
          <el-date-picker
            v-model="form.check_in_date"
            type="date"
            placeholder="选择入住日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="退房日期" prop="check_out_date">
          <el-date-picker
            v-model="form.check_out_date"
            type="date"
            placeholder="选择退房日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="状态" prop="trip_status">
          <el-select v-model="form.trip_status" placeholder="请选择状态" style="width: 100%">
            <el-option label="待出发" value="pending" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
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

    <!-- 更新位置弹窗 -->
    <el-dialog v-model="locationDialog.visible" title="更新位置" width="450px">
      <el-form ref="locationFormRef" :model="locationForm" label-width="80px">
        <el-form-item label="纬度" prop="latitude">
          <el-input-number
            v-model="locationForm.latitude"
            :precision="6"
            :step="0.000001"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="经度" prop="longitude">
          <el-input-number
            v-model="locationForm.longitude"
            :precision="6"
            :step="0.000001"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="locationForm.address" placeholder="请输入地址" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="locationDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleLocationSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import type { FormInstance, FormRules } from "element-plus";
import { ElMessage, ElMessageBox } from "element-plus";
import TripAPI from "@/api/module_promotion/trip";
import type { TripItem, TripForm, TripQuery } from "@/api/module_promotion/trip";

const loading = ref(false);
const tableData = ref<TripItem[]>([]);
const selectedIds = ref<number[]>([]);

const searchFormRef = ref<FormInstance>();
const searchForm = reactive<TripQuery>({
  activity_id: undefined,
  personnel_id: undefined,
  trip_no: "",
  departure_city: "",
  destination_city: "",
  trip_status: "",
});

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

const detailDialog = reactive({
  visible: false,
  data: null as TripItem | null,
});

const formDialog = reactive({
  visible: false,
  type: "create" as "create" | "edit",
  id: null as number | null,
});

const locationDialog = reactive({
  visible: false,
  id: null as number | null,
});

const formRef = ref<FormInstance>();
const locationFormRef = ref<FormInstance>();
const form = reactive<TripForm>({
  activity_id: undefined,
  activity_name: "",
  personnel_id: undefined,
  personnel_name: "",
  departure_city: "",
  destination_city: "",
  departure_time: "",
  arrival_time: "",
  transportation: "",
  transportation_no: "",
  hotel_name: "",
  hotel_address: "",
  check_in_date: "",
  check_out_date: "",
  trip_status: "pending",
  remark: "",
});

const locationForm = reactive({
  latitude: 0,
  longitude: 0,
  address: "",
});

const formRules: FormRules = {
  departure_city: [{ required: true, message: "请输入出发城市", trigger: "blur" }],
  destination_city: [{ required: true, message: "请输入目的城市", trigger: "blur" }],
};

function getStatusLabel(status: string): string {
  const map: Record<string, string> = {
    pending: "待出发",
    in_progress: "进行中",
    completed: "已完成",
    cancelled: "已取消",
  };
  return map[status] || status;
}

function getStatusType(status: string): string {
  const map: Record<string, string> = {
    pending: "info",
    in_progress: "warning",
    completed: "success",
    cancelled: "info",
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
    const res = await TripAPI.getList(params);
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

function handleSelectionChange(selection: TripItem[]) {
  selectedIds.value = selection.map((item) => item.id);
}

function handleCreate() {
  formDialog.type = "create";
  formDialog.id = null;
  Object.assign(form, {
    activity_id: undefined,
    activity_name: "",
    personnel_id: undefined,
    personnel_name: "",
    departure_city: "",
    destination_city: "",
    departure_time: "",
    arrival_time: "",
    transportation: "",
    transportation_no: "",
    hotel_name: "",
    hotel_address: "",
    check_in_date: "",
    check_out_date: "",
    trip_status: "pending",
    remark: "",
  });
  formDialog.visible = true;
}

function handleEdit(row: TripItem) {
  formDialog.type = "edit";
  formDialog.id = row.id;
  Object.assign(form, row);
  formDialog.visible = true;
}

function handleLocation(row: TripItem) {
  locationDialog.id = row.id;
  locationForm.latitude = row.latitude || 0;
  locationForm.longitude = row.longitude || 0;
  locationForm.address = row.current_address || "";
  locationDialog.visible = true;
}

async function handleLocationSubmit() {
  if (!locationDialog.id) return;
  try {
    const res = await TripAPI.updateLocation(locationDialog.id, locationForm);
    if (res.data.code === 0) {
      ElMessage.success("位置更新成功");
      locationDialog.visible = false;
      fetchData();
    } else {
      ElMessage.error(res.data.msg || "位置更新失败");
    }
  } catch {
    ElMessage.error("位置更新失败");
  }
}

async function handleView(row: TripItem) {
  try {
    const res = await TripAPI.getDetail(row.id);
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
      const res = await TripAPI.create(form);
      if (res.data.code === 0) {
        ElMessage.success("创建成功");
        formDialog.visible = false;
        fetchData();
      } else {
        ElMessage.error(res.data.msg || "创建失败");
      }
    } else {
      const res = await TripAPI.update(formDialog.id!, form);
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

async function handleDelete(row: TripItem) {
  try {
    await ElMessageBox.confirm("确定要删除该行程吗？", "提示", {
      type: "warning",
    });
    const res = await TripAPI.delete(row.id);
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
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 个行程吗？`, "提示", {
      type: "warning",
    });
    const res = await TripAPI.batchDelete(selectedIds.value);
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
