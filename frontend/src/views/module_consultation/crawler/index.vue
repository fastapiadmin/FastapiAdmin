<!-- 爬虫管理 - 咨询会信息抓取管理 -->
<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <el-card class="search-card" shadow="never">
      <el-form
        ref="searchFormRef"
        :model="searchForm"
        :inline="true"
        label-width="80px"
      >
        <el-form-item label="任务名称" prop="task_name">
          <el-input
            v-model="searchForm.task_name"
            placeholder="请输入任务名称"
            clearable
            style="width: 200px"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select
            v-model="searchForm.status"
            placeholder="请选择状态"
            clearable
            style="width: 150px"
          >
            <el-option label="待执行" value="pending" />
            <el-option label="执行中" value="running" />
            <el-option label="已完成" value="completed" />
            <el-option label="失败" value="failed" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery">
            <template #icon><Search /></template>
            搜索
          </el-button>
          <el-button @click="handleReset">
            <template #icon><Refresh /></template>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 操作按钮区域 -->
    <el-card shadow="never" class="mt-4">
      <template #header>
        <div class="flex-x-between">
          <span>爬虫任务列表</span>
          <div>
            <el-button
              v-has-perm="['module_consultation:info_collection:admin']"
              type="primary"
              @click="handleTriggerCrawler"
            >
              <template #icon><Refresh /></template>
              触发抓取
            </el-button>
          </div>
        </div>
      </template>

      <!-- 数据表格 -->
      <el-table
        v-loading="loading"
        :data="tableData"
        border
        stripe
        highlight-current-row
      >
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="task_name" label="任务名称" min-width="150" />
        <el-table-column prop="source_count" label="抓取源数量" width="120" align="center" />
        <el-table-column prop="new_count" label="新增数量" width="100" align="center" />
        <el-table-column prop="update_count" label="更新数量" width="100" align="center" />
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="started_at" label="开始时间" width="160" />
        <el-table-column prop="completed_at" label="完成时间" width="160" />
        <el-table-column prop="created_time" label="创建时间" width="160" />
        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template #default="{ row }">
            <el-button
              link
              type="primary"
              size="small"
              @click="handleViewDetail(row)"
            >
              查看日志
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <pagination
        v-if="total > 0"
        v-model:total="total"
        v-model:page="queryParams.page_no"
        v-model:limit="queryParams.page_size"
        @pagination="handleQuery"
      />
    </el-card>

    <!-- 触发爬虫对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="触发爬虫抓取"
      width="500px"
      append-to-body
    >
      <el-form
        ref="formRef"
        :model="formData"
        label-width="120px"
      >
        <el-form-item label="抓取天数" prop="days_ahead">
          <el-input-number
            v-model="formData.days_ahead"
            :min="7"
            :max="90"
            :step="1"
            style="width: 200px"
          />
          <div class="form-tip">抓取未来多少天内的咨询会信息</div>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { Search, Refresh } from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";

// 搜索表单
const searchForm = reactive({
  task_name: "",
  status: "",
});

// 查询参数
const queryParams = reactive({
  page_no: 1,
  page_size: 10,
});

// 表格数据
const tableData = ref<any[]>([]);
const total = ref(0);
const loading = ref(false);

// 对话框
const dialogVisible = ref(false);
const formData = reactive({
  days_ahead: 30,
});

// 状态映射
const statusMap: Record<string, { label: string; type: any }> = {
  pending: { label: "待执行", type: "info" },
  running: { label: "执行中", type: "warning" },
  completed: { label: "已完成", type: "success" },
  failed: { label: "失败", type: "danger" },
};

const getStatusLabel = (status: string) => {
  return statusMap[status]?.label || status;
};

const getStatusType = (status: string) => {
  return statusMap[status]?.type || "info";
};

// 查询列表
const handleQuery = async () => {
  loading.value = true;
  try {
    // TODO: 调用 API 获取爬虫任务列表
    // const res = await CrawlerAPI.getList({
    //   ...searchForm,
    //   ...queryParams,
    // });
    // tableData.value = res.data.list;
    // total.value = res.data.total;

    // 模拟数据
    tableData.value = [
      {
        id: 1,
        task_name: "每日自动抓取任务",
        source_count: 5,
        new_count: 12,
        update_count: 3,
        status: "completed",
        started_at: "2026-04-26 02:00:00",
        completed_at: "2026-04-26 02:05:32",
        created_time: "2026-04-26 02:00:00",
      },
    ];
    total.value = 1;
  } finally {
    loading.value = false;
  }
};

// 重置搜索
const handleReset = () => {
  searchForm.task_name = "";
  searchForm.status = "";
  queryParams.page_no = 1;
  handleQuery();
};

// 触发爬虫
const handleTriggerCrawler = () => {
  dialogVisible.value = true;
};

// 提交触发
const handleSubmit = async () => {
  try {
    // TODO: 调用 API 触发爬虫
    // await CrawlerAPI.trigger({ days_ahead: formData.days_ahead });
    ElMessage.success("爬虫任务已触发");
    dialogVisible.value = false;
    handleQuery();
  } catch (error) {
    console.error(error);
  }
};

// 查看详情
const handleViewDetail = (row: any) => {
  ElMessage.info(`查看任务 ${row.task_name} 的日志`);
};

// 初始化
onMounted(() => {
  handleQuery();
});
</script>

<style lang="scss" scoped>
.search-card {
  :deep(.el-card__body) {
    padding-bottom: 0;
  }
}

.form-tip {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}
</style>
