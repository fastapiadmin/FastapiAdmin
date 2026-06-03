<!-- 招生咨询会 - 全网抓取（超级管理员） -->
<template>
  <div class="app-container">
    <el-card class="action-card" shadow="never">
      <div class="action-header">
        <div>
          <h3 class="title">全网抓取</h3>
          <p class="hint">
            支持 Excel 批量导入或自动抓取；已审核的抓取数据全平台用户可见
          </p>
        </div>
        <div class="action-buttons">
          <el-button
            v-permission="['module_consultation:info_collection:crawl']"
            @click="handleDownloadTemplate"
          >
            <i-ep-download />
            下载模板
          </el-button>
          <el-button
            v-permission="['module_consultation:info_collection:crawl']"
            type="primary"
            @click="importDialogVisible = true"
          >
            <i-ep-upload />
            Excel 导入
          </el-button>
          <el-button
            v-permission="['module_consultation:info_collection:crawl']"
            type="success"
            :loading="crawlLoading"
            @click="handleCrawl"
          >
            <i-ep-refresh />
            立即抓取
          </el-button>
        </div>
      </div>
      <el-descriptions v-if="lastStats" :column="4" border class="stats">
        <el-descriptions-item v-if="lastStats.total_fetched !== undefined" label="最近抓取">
          {{ lastStats.total_fetched }}
        </el-descriptions-item>
        <el-descriptions-item label="保存成功">
          {{ lastStats.total_saved }}
        </el-descriptions-item>
        <el-descriptions-item label="跳过重复">
          {{ lastStats.total_skipped }}
        </el-descriptions-item>
        <el-descriptions-item v-if="lastStats.total_failed" label="失败行数">
          {{ lastStats.total_failed }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card class="table-card" shadow="never">
      <template #header>
        <span class="title">抓取记录列表</span>
      </template>

      <el-table v-loading="loading" :data="tableData" stripe border>
        <el-table-column prop="excel_serial_no" label="序号" width="70" align="center" />
        <el-table-column prop="province" label="省份" width="80" />
        <el-table-column prop="guidance_unit" label="指导单位" min-width="120" show-overflow-tooltip />
        <el-table-column prop="organizer" label="承办单位" min-width="140" show-overflow-tooltip />
        <el-table-column prop="route_arrangement" label="线路" width="90" />
        <el-table-column prop="event_time_text" label="时间" width="110" show-overflow-tooltip />
        <el-table-column prop="address" label="地点" min-width="140" show-overflow-tooltip />
        <el-table-column prop="is_participating" label="是否参加" width="90" />
        <el-table-column prop="status" label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleView(row)">详情</el-button>
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

    <el-dialog v-model="importDialogVisible" title="Excel 导入" width="520px" destroy-on-close>
      <el-upload
        ref="uploadRef"
        v-model:file-list="importFileList"
        drag
        :limit="1"
        accept=".xlsx,.xls"
        :auto-upload="false"
      >
        <el-icon class="el-icon--upload"><i-ep-upload-filled /></el-icon>
        <div class="el-upload__text">将 Excel 拖到此处，或<em>点击上传</em></div>
        <template #tip>
          <div class="el-upload__tip">列名须与模板一致，支持 .xlsx / .xls</div>
        </template>
      </el-upload>
      <template #footer>
        <el-button @click="importDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="importLoading" @click="handleImport">
          开始导入
        </el-button>
      </template>
    </el-dialog>

    <ConsultationFormDialog
      v-model:visible="formDialog.visible"
      :type="formDialog.type"
      :data="formDialog.data"
      @success="handleFormSuccess"
    />

    <ReviewDialog
      v-model:visible="reviewDialog.visible"
      :type="reviewDialog.type"
      :data="reviewDialog.data"
      @success="handleReviewSuccess"
    />

    <DetailDialog v-model:visible="detailDialog.visible" :data="detailDialog.data" />
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from "vue";
import { ElMessage } from "element-plus";
import type { UploadUserFile } from "element-plus";
import ConsultationInfoAPI from "@/api/module_consultation/consultation";
import type {
  ConsultationInfoItem,
  ConsultationInfoQuery,
  CrawlResult,
  ExcelImportResult,
} from "@/api/module_consultation/consultation";
import ConsultationFormDialog from "../consultation/components/ConsultationFormDialog.vue";
import ReviewDialog from "../consultation/components/ReviewDialog.vue";
import DetailDialog from "../consultation/components/DetailDialog.vue";

const crawlLoading = ref(false);
const importLoading = ref(false);
const importDialogVisible = ref(false);
const importFileList = ref<UploadUserFile[]>([]);
const loading = ref(false);
const tableData = ref<ConsultationInfoItem[]>([]);
const lastStats = ref<(CrawlResult & ExcelImportResult) | null>(null);

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

const formDialog = reactive({
  visible: false,
  type: "edit" as "create" | "edit",
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

const fetchList = async () => {
  loading.value = true;
  try {
    const params: ConsultationInfoQuery = {
      page_no: pagination.page,
      page_size: pagination.pageSize,
      source_type: "crawler",
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

const handleCrawl = async () => {
  crawlLoading.value = true;
  try {
    const res = await ConsultationInfoAPI.crawl();
    if (res.data?.data) {
      lastStats.value = res.data.data;
      ElMessage.success(
        `抓取完成：共抓取 ${res.data.data.total_fetched} 条，保存 ${res.data.data.total_saved} 条，跳过重复 ${res.data.data.total_skipped} 条`
      );
      fetchList();
    }
  } catch (error) {
    console.error("抓取失败:", error);
  } finally {
    crawlLoading.value = false;
  }
};

const saveBlob = (blob: Blob, fileName: string) => {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};

const handleDownloadTemplate = async () => {
  try {
    const res = await ConsultationInfoAPI.downloadImportTemplate();
    const blob = res.data instanceof Blob ? res.data : new Blob([res.data as BlobPart]);
    saveBlob(blob, "全网抓取导入模板.xlsx");
  } catch (error) {
    console.error("下载模板失败:", error);
  }
};

const handleImport = async () => {
  const file = importFileList.value[0]?.raw;
  if (!file) {
    ElMessage.warning("请选择 Excel 文件");
    return;
  }
  importLoading.value = true;
  try {
    const res = await ConsultationInfoAPI.importExcel(file);
    if (res.data?.data) {
      lastStats.value = res.data.data;
      const d = res.data.data;
      let msg = `导入完成：有效 ${d.total_rows} 行，保存 ${d.total_saved} 条，跳过 ${d.total_skipped} 条`;
      if (d.total_failed) {
        msg += `，失败 ${d.total_failed} 条`;
      }
      ElMessage.success(msg);
      if (d.errors?.length) {
        console.warn("导入错误明细:", d.errors);
      }
      importDialogVisible.value = false;
      importFileList.value = [];
      fetchList();
    }
  } catch (error) {
    console.error("导入失败:", error);
  } finally {
    importLoading.value = false;
  }
};

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

const handleSizeChange = (size: number) => {
  pagination.pageSize = size;
  fetchList();
};

const handlePageChange = (page: number) => {
  pagination.page = page;
  fetchList();
};

const handleView = (row: ConsultationInfoItem) => {
  detailDialog.data = row;
  detailDialog.visible = true;
};

const handleEdit = (row: ConsultationInfoItem) => {
  formDialog.type = "edit";
  formDialog.data = row;
  formDialog.visible = true;
};

const handleFormSuccess = () => {
  formDialog.visible = false;
  fetchList();
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

const handleReviewSuccess = () => {
  reviewDialog.visible = false;
  fetchList();
};

onMounted(() => {
  fetchList();
});
</script>

<style lang="scss" scoped>
.action-card {
  margin-bottom: 16px;

  .action-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 16px;

    .title {
      margin: 0 0 8px;
      font-size: 16px;
      font-weight: 600;
    }

    .hint {
      margin: 0;
      font-size: 13px;
      color: var(--el-text-color-secondary);
    }

    .action-buttons {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
  }

  .stats {
    margin-top: 8px;
  }
}

.table-card {
  .title {
    font-size: 16px;
    font-weight: 600;
  }
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}
</style>
