<!-- 招生咨询会 - 行程方案管理 -->
<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="80px">
        <el-form-item label="咨询会ID" prop="consultation_id">
          <el-input-number v-model="searchForm.consultation_id" :min="1" style="width: 120px" />
        </el-form-item>
        <el-form-item label="招生组ID" prop="team_id">
          <el-input-number v-model="searchForm.team_id" :min="1" style="width: 120px" />
        </el-form-item>
        <el-form-item label="方案名称" prop="itinerary_name">
          <el-input v-model="searchForm.itinerary_name" placeholder="请输入方案名称" clearable style="width: 180px" />
        </el-form-item>
        <el-form-item label="状态" prop="itinerary_status">
          <el-select v-model="searchForm.itinerary_status" placeholder="请选择状态" clearable style="width: 120px">
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
        <el-table-column prop="consultation_id" label="咨询会ID" width="100" />
        <el-table-column prop="team_id" label="招生组ID" width="100" />
        <el-table-column prop="itinerary_name" label="方案名称" min-width="150" show-overflow-tooltip>
          <template #default="{ row }">
            <el-link type="primary" @click="handleView(row)">{{ row.itinerary_name || '-' }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="start_date" label="开始日期" width="110" />
        <el-table-column prop="end_date" label="结束日期" width="110" />
        <el-table-column prop="departure_city" label="出发城市" width="100" />
        <el-table-column prop="destination_city" label="目的城市" width="100" />
        <el-table-column prop="itinerary_status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.itinerary_status)">{{ getStatusLabel(row.itinerary_status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_synced" label="已同步" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_synced ? 'success' : 'info'" size="small">{{ row.is_synced ? '是' : '否' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-permission="['module_consultation:itinerary:detail']" link type="primary" @click="handleView(row)">详情</el-button>
            <el-button v-permission="['module_consultation:itinerary:update']" link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button v-permission="['module_consultation:itinerary:delete']" link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination v-model:current-page="pagination.page" v-model:page-size="pagination.pageSize" :total="pagination.total" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" @size-change="handleSizeChange" @current-change="handlePageChange" />
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailDialog.visible" title="行程方案详情" width="600px">
      <el-descriptions :column="2" border v-if="detailDialog.data">
        <el-descriptions-item label="咨询会ID">{{ detailDialog.data.consultation_id }}</el-descriptions-item>
        <el-descriptions-item label="招生组ID">{{ detailDialog.data.team_id || '-' }}</el-descriptions-item>
        <el-descriptions-item label="方案名称" :span="2">{{ detailDialog.data.itinerary_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="开始日期">{{ detailDialog.data.start_date }}</el-descriptions-item>
        <el-descriptions-item label="结束日期">{{ detailDialog.data.end_date || '-' }}</el-descriptions-item>
        <el-descriptions-item label="出发城市">{{ detailDialog.data.departure_city || '-' }}</el-descriptions-item>
        <el-descriptions-item label="目的城市">{{ detailDialog.data.destination_city || '-' }}</el-descriptions-item>
        <el-descriptions-item label="交通方式">{{ detailDialog.data.transportation || '-' }}</el-descriptions-item>
        <el-descriptions-item label="车次/航班">{{ detailDialog.data.transportation_no || '-' }}</el-descriptions-item>
        <el-descriptions-item label="出发时间">{{ detailDialog.data.departure_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="到达时间">{{ detailDialog.data.arrival_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="酒店名称" :span="2">{{ detailDialog.data.hotel_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="酒店地址" :span="2">{{ detailDialog.data.hotel_address || '-' }}</el-descriptions-item>
        <el-descriptions-item label="入住日期">{{ detailDialog.data.check_in_date || '-' }}</el-descriptions-item>
        <el-descriptions-item label="退房日期">{{ detailDialog.data.check_out_date || '-' }}</el-descriptions-item>
        <el-descriptions-item label="房间号">{{ detailDialog.data.room_number || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(detailDialog.data.itinerary_status)">{{ getStatusLabel(detailDialog.data.itinerary_status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="已同步">
          <el-tag :type="detailDialog.data.is_synced ? 'success' : 'info'">{{ detailDialog.data.is_synced ? '是' : '否' }}</el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="formDialog.visible" :title="formDialog.type === 'create' ? '新增行程方案' : '编辑行程方案'" width="550px">
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="咨询会ID" prop="consultation_id">
          <el-input-number v-model="form.consultation_id" :min="1" style="width: 200px" />
        </el-form-item>
        <el-form-item label="招生组ID" prop="team_id">
          <el-input-number v-model="form.team_id" :min="1" style="width: 200px" />
        </el-form-item>
        <el-form-item label="方案名称" prop="itinerary_name">
          <el-input v-model="form.itinerary_name" placeholder="请输入方案名称" />
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker v-model="form.start_date" type="date" placeholder="选择开始日期" value-format="YYYY-MM-DD" style="width: 200px" />
        </el-form-item>
        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker v-model="form.end_date" type="date" placeholder="选择结束日期" value-format="YYYY-MM-DD" style="width: 200px" />
        </el-form-item>
        <el-form-item label="出发城市" prop="departure_city">
          <el-input v-model="form.departure_city" placeholder="请输入出发城市" />
        </el-form-item>
        <el-form-item label="目的城市" prop="destination_city">
          <el-input v-model="form.destination_city" placeholder="请输入目的城市" />
        </el-form-item>
        <el-form-item label="交通方式" prop="transportation">
          <el-input v-model="form.transportation" placeholder="请输入交通方式" />
        </el-form-item>
        <el-form-item label="车次/航班" prop="transportation_no">
          <el-input v-model="form.transportation_no" placeholder="请输入车次/航班" />
        </el-form-item>
        <el-form-item label="出发时间" prop="departure_time">
          <el-date-picker v-model="form.departure_time" type="datetime" placeholder="选择出发时间" value-format="YYYY-MM-DD HH:mm:ss" style="width: 200px" />
        </el-form-item>
        <el-form-item label="到达时间" prop="arrival_time">
          <el-date-picker v-model="form.arrival_time" type="datetime" placeholder="选择到达时间" value-format="YYYY-MM-DD HH:mm:ss" style="width: 200px" />
        </el-form-item>
        <el-form-item label="酒店名称" prop="hotel_name">
          <el-input v-model="form.hotel_name" placeholder="请输入酒店名称" />
        </el-form-item>
        <el-form-item label="酒店地址" prop="hotel_address">
          <el-input v-model="form.hotel_address" placeholder="请输入酒店地址" />
        </el-form-item>
        <el-form-item label="入住日期" prop="check_in_date">
          <el-date-picker v-model="form.check_in_date" type="date" placeholder="选择入住日期" value-format="YYYY-MM-DD" style="width: 200px" />
        </el-form-item>
        <el-form-item label="退房日期" prop="check_out_date">
          <el-date-picker v-model="form.check_out_date" type="date" placeholder="选择退房日期" value-format="YYYY-MM-DD" style="width: 200px" />
        </el-form-item>
        <el-form-item label="房间号" prop="room_number">
          <el-input v-model="form.room_number" placeholder="请输入房间号" />
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

const searchForm = reactive<ItineraryQuery>({ consultation_id: undefined, team_id: undefined, itinerary_name: undefined, itinerary_status: undefined });
const loading = ref(false);
const tableData = ref<ItineraryItem[]>([]);
const selectedIds = ref<number[]>([]);
const pagination = reactive({ page: 1, pageSize: 10, total: 0 });

const formDialog = reactive({ visible: false, type: "create" as "create" | "edit", data: undefined as ItineraryItem | undefined });
const detailDialog = reactive({ visible: false, data: undefined as ItineraryItem | undefined });
const formRef = ref<FormInstance>();

const form = reactive<any>({
  consultation_id: undefined,
  team_id: undefined,
  itinerary_name: "",
  start_date: "",
  end_date: "",
  departure_city: "",
  destination_city: "",
  transportation: "",
  departure_time: "",
  arrival_time: "",
  transportation_no: "",
  hotel_name: "",
  hotel_address: "",
  check_in_date: "",
  check_out_date: "",
  room_number: "",
});

const formRules: FormRules = {
  consultation_id: [{ required: true, message: "请输入咨询会ID", trigger: "blur" }],
  start_date: [{ required: true, message: "请选择开始日期", trigger: "change" }],
};

const fetchList = async () => {
  loading.value = true;
  try {
    const params = { page_no: pagination.page, page_size: pagination.pageSize, ...searchForm };
    const res = await ItineraryAPI.getList(params);
    if (res.data?.data) { tableData.value = res.data.data.items || []; pagination.total = res.data.data.total || 0; }
  } finally { loading.value = false; }
};

const handleSearch = () => { pagination.page = 1; fetchList(); };
const handleReset = () => { Object.assign(searchForm, { consultation_id: undefined, team_id: undefined, itinerary_name: undefined, itinerary_status: undefined }); handleSearch(); };
const handleSelectionChange = (selection: ItineraryItem[]) => { selectedIds.value = selection.map(item => item.id!); };
const handleSizeChange = (size: number) => { pagination.pageSize = size; fetchList(); };
const handlePageChange = (page: number) => { pagination.page = page; fetchList(); };

const getStatusType = (status: string) => { if (status === "draft") return "info"; if (status === "confirmed") return "success"; if (status === "executed") return "warning"; if (status === "completed") return "success"; return ""; };
const getStatusLabel = (status: string) => { if (status === "draft") return "草稿"; if (status === "confirmed") return "已确认"; if (status === "executed") return "执行中"; if (status === "completed") return "已完成"; if (status === "archived") return "已归档"; return status; };

const handleCreate = () => {
  formDialog.type = "create";
  Object.assign(form, {
    consultation_id: undefined,
    team_id: undefined,
    itinerary_name: "",
    start_date: "",
    end_date: "",
    departure_city: "",
    destination_city: "",
    transportation: "",
    departure_time: "",
    arrival_time: "",
    transportation_no: "",
    hotel_name: "",
    hotel_address: "",
    check_in_date: "",
    check_out_date: "",
    room_number: "",
  });
  formDialog.visible = true;
};

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

const handleDelete = (row: ItineraryItem) => {
  ElMessageBox.confirm(`确定要删除这条行程方案吗？`, "删除确认", { confirmButtonText: "确定", cancelButtonText: "取消", type: "warning" })
    .then(async () => { await ItineraryAPI.delete(row.id!); ElMessage.success("删除成功"); fetchList(); }).catch(() => {});
};

const handleBatchDelete = () => {
  if (!selectedIds.value.length) { ElMessage.warning("请选择要删除的记录"); return; }
  ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 条记录吗？`, "批量删除确认", { confirmButtonText: "确定", cancelButtonText: "取消", type: "warning" })
    .then(async () => { await ItineraryAPI.batchDelete(selectedIds.value); ElMessage.success("批量删除成功"); fetchList(); }).catch(() => {});
};

onMounted(() => { fetchList(); });
</script>

<style lang="scss" scoped>
.search-card { margin-bottom: 16px; }
.table-card { .card-header { display: flex; justify-content: space-between; align-items: center; .title { font-size: 16px; font-weight: 600; } .operations { display: flex; gap: 8px; } } }
.pagination-container { display: flex; justify-content: flex-end; padding-top: 16px; }
</style>
