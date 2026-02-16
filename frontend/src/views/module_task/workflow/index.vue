<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div v-show="visible" class="search-container">
      <el-form
        ref="queryFormRef"
        :model="searchForm"
        label-suffix=":"
        :inline="true"
        @submit.prevent="handleQuery"
      >
        <el-form-item prop="name" label="流程名称">
          <el-input v-model="searchForm.name" placeholder="请输入流程名称" clearable />
        </el-form-item>
        <el-form-item prop="code" label="流程编码">
          <el-input v-model="searchForm.code" placeholder="请输入流程编码" clearable />
        </el-form-item>
        <el-form-item prop="category" label="流程分类">
          <el-select
            v-model="searchForm.category"
            placeholder="请选择流程分类"
            clearable
            style="width: 150px"
          >
            <el-option label="数据处理" value="data" />
            <el-option label="业务流程" value="business" />
            <el-option label="通知流程" value="notification" />
            <el-option label="审批流程" value="approval" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button
            v-hasPerm="['module_task:workflow:query']"
            type="primary"
            icon="search"
            @click="handleQuery"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_task:workflow:query']"
            icon="refresh"
            @click="handleResetQuery"
          >
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-card class="data-table">
      <template #header>
        <div class="card-header">
          <el-space>
            工作流管理
            <el-tooltip content="工作流管理列表">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
          </el-space>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--left">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_task:workflow:create']"
                type="success"
                icon="plus"
                @click="handleCreate"
              >
                新增
              </el-button>
            </el-col>
          </el-row>
        </div>
        <div class="data-table__toolbar--right">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-tooltip content="搜索显示/隐藏">
                <el-button
                  v-hasPerm="['*:*:*']"
                  type="info"
                  icon="search"
                  circle
                  @click="visible = !visible"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-tooltip content="刷新">
                <el-button
                  v-hasPerm="['module_task:workflow:query']"
                  type="primary"
                  icon="refresh"
                  circle
                  @click="handleRefresh"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-popover placement="bottom" trigger="click">
                <template #reference>
                  <el-button type="danger" icon="operation" circle></el-button>
                </template>
                <el-scrollbar max-height="350px">
                  <template v-for="column in tableColumns" :key="column.prop">
                    <el-checkbox v-if="column.prop" v-model="column.show" :label="column.label" />
                  </template>
                </el-scrollbar>
              </el-popover>
            </el-col>
          </el-row>
        </div>
      </div>

      <el-table
        ref="tableRef"
        v-loading="loading"
        :data="dataSource"
        highlight-current-row
        class="data-table__content"
        height="450"
        max-height="450"
        border
        stripe
        @sort-change="handleTableChange"
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="流程名称" width="200" />
        <el-table-column prop="code" label="流程编码" width="150" />
        <el-table-column prop="category" label="流程分类" width="120">
          <template #default="{ row }">
            <el-tag :type="getCategoryType(row.category) as any">
              {{ getCategoryText(row.category) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status) as any">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_time" label="创建时间" width="180" />
        <el-table-column label="操作" width="300" fixed="right" align="center">
          <template #default="{ row }">
            <el-space class="flex">
              <el-button type="primary" size="small" link icon="edit" @click="handleEdit(row)">
                编辑
              </el-button>
              <el-button type="danger" size="small" link icon="delete" @click="handleDelete(row)">
                删除
              </el-button>
              <el-button
                type="primary"
                size="small"
                link
                icon="document"
                @click="handleViewRuns(row)"
              >
                执行记录
              </el-button>
              <el-dropdown @command="(e) => handleExecute(e, row)">
                <el-button type="primary" size="small" link icon="video-play">
                  执行
                  <el-icon><ArrowDown /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="execute">立即执行</el-dropdown-item>
                    <el-dropdown-item command="pause">暂停</el-dropdown-item>
                    <el-dropdown-item command="resume">恢复</el-dropdown-item>
                    <el-dropdown-item command="terminate">终止</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </el-space>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页区域 -->
      <template #footer>
        <pagination
          v-model:total="workflowPagination.total"
          v-model:page="workflowPagination.page_no"
          v-model:limit="workflowPagination.page_size"
          @pagination="loadData"
        />
      </template>
    </el-card>

    <WorkflowDesignDrawer
      v-model:visible="createVisible"
      :workflow="selectedWorkflow"
      @refresh="handleRefresh"
    />

    <WorkflowRunDrawer v-model:visible="runListVisible" :workflow-name="selectedWorkflowName" />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { ArrowDown } from "@element-plus/icons-vue";
import WorkflowAPI, {
  type WorkflowTable,
  type WorkflowPageQuery,
} from "@/api/module_task/workflow";
import WorkflowDesignDrawer from "./components/WorkflowDesignDrawer.vue";
import WorkflowRunDrawer from "./components/WorkflowRunDrawer.vue";

const visible = ref(true);
const loading = ref(false);
const dataSource = ref<WorkflowTable[]>([]);
const selectedWorkflow = ref<WorkflowTable>();
const selectedWorkflowName = ref<string>();
const createVisible = ref(false);
const runListVisible = ref(false);

const searchForm = reactive<Partial<WorkflowPageQuery>>({
  name: undefined,
  code: undefined,
  category: undefined,
});

const workflowPagination = reactive({
  page_no: 1,
  page_size: 10,
  total: 0,
});

// 表格列配置
const tableColumns = ref([
  { prop: "selection", label: "选择框", show: true },
  { prop: "index", label: "序号", show: true },
  { prop: "name", label: "名称", show: true },
  { prop: "code", label: "代码", show: true },
  { prop: "category", label: "分类", show: true },
  { prop: "description", label: "描述", show: true },
  { prop: "status", label: "状态", show: true },
  { prop: "created_time", label: "创建时间", show: true },
]);

const loadData = async () => {
  loading.value = true;
  try {
    const params: WorkflowPageQuery = {
      page_no: workflowPagination.page_no,
      page_size: workflowPagination.page_size,
      ...searchForm,
    };
    const res = await WorkflowAPI.getWorkflowList(params);
    if (res.data && res.data.data) {
      dataSource.value = res.data.data.items || [];
      workflowPagination.total = res.data.data.total || 0;
    }
  } catch {
    ElMessage.error("加载数据失败");
  } finally {
    loading.value = false;
  }
};

const handleQuery = () => {
  workflowPagination.page_no = 1;
  loadData();
};

const handleResetQuery = () => {
  Object.assign(searchForm, {
    name: undefined,
    code: undefined,
    category: undefined,
  });
  handleQuery();
};

const handleTableChange = () => {
  loadData();
};

const handleCreate = () => {
  selectedWorkflow.value = undefined;
  createVisible.value = true;
};

const handleEdit = (record: WorkflowTable) => {
  selectedWorkflow.value = record;
  createVisible.value = true;
};

const handleExecute = async (action: string, record: WorkflowTable) => {
  const actionTextMap: Record<string, string> = {
    execute: "立即执行",
    pause: "暂停",
    resume: "恢复",
    terminate: "终止",
  };
  const actionText = actionTextMap[action];

  ElMessageBox.confirm(`确定要${actionText}此工作流吗？`, "确认操作", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        if (!record.id) {
          ElMessage.error("工作流ID不存在");
          return;
        }

        if (action === "execute") {
          await WorkflowAPI.executeWorkflow({
            workflow_id: record.id,
            variables: {},
          });
          ElMessage.success("工作流执行成功");
        } else if (action === "pause") {
          await WorkflowAPI.pauseWorkflow(record.id);
          ElMessage.success("工作流已暂停");
        } else if (action === "resume") {
          await WorkflowAPI.resumeWorkflow(record.id);
          ElMessage.success("工作流已恢复");
        } else if (action === "terminate") {
          await WorkflowAPI.terminateWorkflow(record.id);
          ElMessage.success("工作流已终止");
        }
        loadData();
      } catch {
        ElMessage.error(`${actionText}失败`);
      }
    })
    .catch();
};

const handleViewRuns = (record: WorkflowTable) => {
  selectedWorkflowName.value = record.name;
  runListVisible.value = true;
};

const handleDelete = (record: WorkflowTable) => {
  ElMessageBox.confirm("确定要删除此工作流吗？", "确认删除", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        if (!record.id) {
          ElMessage.error("工作流ID不存在");
          return;
        }
        await WorkflowAPI.deleteWorkflow([record.id]);
        ElMessage.success("删除成功");
        loadData();
      } catch {
        ElMessage.error("删除失败");
      }
    })
    .catch();
};

const handleRefresh = () => {
  loadData();
};

const getCategoryType = (category: string) => {
  const typeMap: Record<string, string> = {
    data: "",
    business: "success",
    notification: "warning",
    approval: "danger",
  };
  return typeMap[category] || "";
};

const getCategoryText = (category: string) => {
  const textMap: Record<string, string> = {
    data: "数据处理",
    business: "业务流程",
    notification: "通知流程",
    approval: "审批流程",
  };
  return textMap[category] || category;
};

const getStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    draft: "info",
    published: "success",
    archived: "warning",
  };
  return typeMap[status] || "";
};

const getStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    draft: "草稿",
    published: "已发布",
    archived: "已归档",
  };
  return textMap[status] || status;
};

onMounted(() => {
  loadData();
});
</script>

<style scoped lang="scss"></style>
