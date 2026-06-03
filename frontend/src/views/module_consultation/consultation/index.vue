<!-- 招生咨询会 - 咨询会信息管理 -->
<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <el-card class="search-card" shadow="never">
      <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="90px">
        <el-form-item label="省份" prop="province">
          <el-input
            v-model="searchForm.province"
            placeholder="省份"
            clearable
            style="width: 120px"
          />
        </el-form-item>
        <el-form-item label="指导单位" prop="guidance_unit">
          <el-input
            v-model="searchForm.guidance_unit"
            placeholder="指导单位"
            clearable
            style="width: 160px"
          />
        </el-form-item>
        <el-form-item label="承办单位" prop="organizer">
          <el-input
            v-model="searchForm.organizer"
            placeholder="承办单位"
            clearable
            style="width: 160px"
          />
        </el-form-item>
        <el-form-item label="线路" prop="route_arrangement">
          <el-input
            v-model="searchForm.route_arrangement"
            placeholder="线路安排"
            clearable
            style="width: 120px"
          />
        </el-form-item>
        <el-form-item label="标题" prop="title">
          <el-input
            v-model="searchForm.title"
            placeholder="标题"
            clearable
            style="width: 160px"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select
            v-model="searchForm.status"
            placeholder="请选择状态"
            clearable
            style="width: 150px"
          >
            <el-option label="待审核" value="pending" />
            <el-option label="已审核" value="approved" />
            <el-option label="已拒绝" value="rejected" />
            <el-option label="已过期" value="expired" />
          </el-select>
        </el-form-item>
        <el-form-item label="信息来源" prop="source_type">
          <el-select
            v-model="searchForm.source_type"
            placeholder="请选择来源"
            clearable
            style="width: 150px"
          >
            <el-option label="全网抓取" value="crawler" />
            <el-option label="第三方上传" value="upload" />
            <el-option label="手动录入" value="manual" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date_range">
          <el-date-picker
            v-model="searchForm.start_date_range"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
            style="width: 240px"
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

    <!-- 操作按钮区域 -->
    <el-card class="table-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">咨询会信息列表</span>
          <div class="operations">
            <el-button
              v-permission="['module_consultation:info_collection:create']"
              type="primary"
              @click="handleCreate"
            >
              <i-ep-plus />
              新增
            </el-button>
            <el-button
              v-permission="['module_consultation:info_collection:delete']"
              type="danger"
              :disabled="!selectedIds.length"
              @click="handleBatchDelete"
            >
              <i-ep-delete />
              批量删除
            </el-button>
            <el-button @click="handleExport">
              <i-ep-download />
              导出
            </el-button>
          </div>
        </div>
      </template>

      <!-- 数据表格 -->
      <el-table
        v-loading="loading"
        :data="tableData"
        stripe
        border
        highlight-current-row
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column prop="excel_serial_no" label="序号" width="70" align="center" />
        <el-table-column prop="province" label="省份" width="80" />
        <el-table-column
          prop="guidance_unit"
          label="指导单位"
          min-width="120"
          show-overflow-tooltip
        />
        <el-table-column prop="organizer" label="承办单位" min-width="140" show-overflow-tooltip>
          <template #default="{ row }">
            <el-link type="primary" @click="handleView(row)">{{ row.organizer }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="route_arrangement" label="线路" width="90" show-overflow-tooltip />
        <el-table-column
          prop="event_time_text"
          label="时间"
          width="110"
          show-overflow-tooltip
        />
        <el-table-column prop="address" label="地点" min-width="140" show-overflow-tooltip />
        <el-table-column prop="is_participating" label="是否参加" width="90" />
        <el-table-column prop="source_type" label="信息来源" width="100">
          <template #default="{ row }">
            <el-tag :type="getSourceTypeType(row.source_type)">
              {{ getSourceTypeLabel(row.source_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="compliance_score" label="合规评分" width="100" align="center">
          <template #default="{ row }">
            <el-tag
              v-if="row.compliance_score !== null && row.compliance_score !== undefined"
              :type="getComplianceType(row.compliance_score)"
            >
              {{ row.compliance_score }}
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button
              v-permission="['module_consultation:info_collection:update']"
              link
              type="primary"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              v-if="row.status === 'pending'"
              v-permission="['module_consultation:info_collection:approve']"
              link
              type="success"
              @click="handleApprove(row)"
            >
              通过
            </el-button>
            <el-button
              v-if="row.status === 'pending'"
              v-permission="['module_consultation:info_collection:approve']"
              link
              type="danger"
              @click="handleReject(row)"
            >
              拒绝
            </el-button>
            <el-button
              v-if="!row.is_archived"
              v-permission="['module_consultation:info_collection:archive']"
              link
              type="warning"
              @click="handleArchive(row)"
            >
              归档
            </el-button>
            <el-button
              v-permission="['module_consultation:info_collection:delete']"
              link
              type="danger"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
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

    <!-- 新增/编辑弹窗 -->
    <ConsultationFormDialog
      v-model:visible="formDialog.visible"
      :type="formDialog.type"
      :data="formDialog.data"
      @success="handleFormSuccess"
    />

    <!-- 审核弹窗 -->
    <ReviewDialog
      v-model:visible="reviewDialog.visible"
      :type="reviewDialog.type"
      :data="reviewDialog.data"
      @success="handleReviewSuccess"
    />

    <!-- 详情弹窗 -->
    <DetailDialog v-model:visible="detailDialog.visible" :data="detailDialog.data" />
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import ConsultationInfoAPI from "@/api/module_consultation/consultation";
import type {
  ConsultationInfoItem,
  ConsultationInfoQuery,
} from "@/api/module_consultation/consultation";

// 组件
import ConsultationFormDialog from "./components/ConsultationFormDialog.vue";
import ReviewDialog from "./components/ReviewDialog.vue";
import DetailDialog from "./components/DetailDialog.vue";

// 搜索表单
interface SearchForm {
  province?: string;
  guidance_unit?: string;
  organizer?: string;
  route_arrangement?: string;
  title?: string;
  status?: string;
  source_type?: string;
  start_date_range?: string[];
}

const searchForm = reactive<SearchForm>({
  province: undefined,
  guidance_unit: undefined,
  organizer: undefined,
  route_arrangement: undefined,
  title: undefined,
  status: undefined,
  source_type: undefined,
  start_date_range: undefined,
});

// 表格数据
const loading = ref(false);
const tableData = ref<ConsultationInfoItem[]>([]);
const selectedIds = ref<number[]>([]);

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

// 弹窗控制
const formDialog = reactive({
  visible: false,
  type: "create" as "create" | "edit",
  data: undefined as ConsultationInfoItem | undefined,
});

const reviewDialog = reactive({
  visible: false,
  type: "approve" as "approve" | "reject",
  data: undefined as ConsultationInfoItem | undefined,
});

const detailDialog = reactive({
  visible: false,
  data: undefined as ConsultationInfoItem | undefined,
});

// 获取列表数据
const fetchList = async () => {
  loading.value = true;
  try {
    const params: ConsultationInfoQuery = {
      page_no: pagination.page,
      page_size: pagination.pageSize,
      province: searchForm.province,
      guidance_unit: searchForm.guidance_unit,
      organizer: searchForm.organizer,
      route_arrangement: searchForm.route_arrangement,
      title: searchForm.title,
      status: searchForm.status,
      source_type: searchForm.source_type,
      start_date_begin: searchForm.start_date_range?.[0],
      start_date_end: searchForm.start_date_range?.[1],
    };

    const res = await ConsultationInfoAPI.getList(params);
    if (res.data?.data) {
      tableData.value = res.data.data.items || [];
      pagination.total = res.data.data.total || 0;
    }
  } finally {
    loading.value = false;
  }
};

// 搜索
const handleSearch = () => {
  pagination.page = 1;
  fetchList();
};

// 重置
const handleReset = () => {
  Object.assign(searchForm, {
    province: undefined,
    guidance_unit: undefined,
    organizer: undefined,
    route_arrangement: undefined,
    title: undefined,
    status: undefined,
    source_type: undefined,
    start_date_range: undefined,
  });
  handleSearch();
};

// 多选变化
const handleSelectionChange = (selection: ConsultationInfoItem[]) => {
  selectedIds.value = selection.map((item) => item.id!);
};

// 分页变化
const handleSizeChange = (size: number) => {
  pagination.pageSize = size;
  fetchList();
};

const handlePageChange = (page: number) => {
  pagination.page = page;
  fetchList();
};

// 状态相关
type TagType = "primary" | "success" | "warning" | "info" | "danger";

const getStatusType = (status: string): TagType => {
  const map: Record<string, TagType> = {
    pending: "warning",
    approved: "success",
    rejected: "danger",
    expired: "info",
  };
  return map[status] || "info";
};

const getStatusLabel = (status: string): string => {
  const map: Record<string, string> = {
    pending: "待审核",
    approved: "已审核",
    rejected: "已拒绝",
    expired: "已过期",
  };
  return map[status] || status;
};

const getSourceTypeType = (type: string): TagType => {
  const map: Record<string, TagType> = {
    crawler: "primary",
    upload: "success",
    manual: "warning",
  };
  return map[type] || "info";
};

const getSourceTypeLabel = (type: string): string => {
  const map: Record<string, string> = {
    crawler: "全网抓取",
    upload: "第三方上传",
    manual: "手动录入",
  };
  return map[type] || type;
};

const getComplianceType = (score: number): TagType => {
  if (score >= 8) return "success";
  if (score >= 6) return "warning";
  return "danger";
};

// 操作按钮
const handleCreate = () => {
  formDialog.type = "create";
  formDialog.data = undefined;
  formDialog.visible = true;
};

const loadDetail = async (id: number) => {
  const res = await ConsultationInfoAPI.getDetail(id);
  return res.data?.data;
};

const handleEdit = async (row: ConsultationInfoItem) => {
  formDialog.type = "edit";
  formDialog.data = (await loadDetail(row.id!)) || row;
  formDialog.visible = true;
};

const handleView = async (row: ConsultationInfoItem) => {
  detailDialog.data = (await loadDetail(row.id!)) || row;
  detailDialog.visible = true;
};

const handleDelete = (row: ConsultationInfoItem) => {
  ElMessageBox.confirm(`确定要删除 "${row.title}" 吗？删除后不可恢复！`, "删除确认", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await ConsultationInfoAPI.delete(row.id!);
      ElMessage.success("删除成功");
      fetchList();
    })
    .catch(() => {});
};

const handleBatchDelete = () => {
  if (!selectedIds.value.length) {
    ElMessage.warning("请选择要删除的记录");
    return;
  }
  ElMessageBox.confirm(
    `确定要删除选中的 ${selectedIds.value.length} 条记录吗？删除后不可恢复！`,
    "批量删除确认",
    {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    }
  )
    .then(async () => {
      await ConsultationInfoAPI.batchDelete(selectedIds.value);
      ElMessage.success("批量删除成功");
      fetchList();
    })
    .catch(() => {});
};

const handleApprove = (row: ConsultationInfoItem) => {
  reviewDialog.type = "approve";
  reviewDialog.data = row;
  reviewDialog.visible = true;
};

const handleReject = (row: ConsultationInfoItem) => {
  reviewDialog.type = "reject";
  reviewDialog.data = row;
  reviewDialog.visible = true;
};

const handleArchive = (row: ConsultationInfoItem) => {
  ElMessageBox.confirm(`确定要归档 "${row.title}" 吗？归档后将被移入历史记录。`, "归档确认", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await ConsultationInfoAPI.archive(row.id!);
      ElMessage.success("归档成功");
      fetchList();
    })
    .catch(() => {});
};

const handleExport = () => {
  ElMessage.info("导出功能开发中...");
};

// 表单成功回调
const handleFormSuccess = () => {
  formDialog.visible = false;
  fetchList();
};

// 审核成功回调
const handleReviewSuccess = () => {
  reviewDialog.visible = false;
  fetchList();
};

// 初始化
onMounted(() => {
  fetchList();
});
</script>

<style lang="scss" scoped>
.search-card {
  margin-bottom: 16px;
}

.table-card {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .title {
      font-size: 16px;
      font-weight: 600;
    }

    .operations {
      display: flex;
      gap: 8px;
    }
  }
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  padding-top: 16px;
}
</style>
