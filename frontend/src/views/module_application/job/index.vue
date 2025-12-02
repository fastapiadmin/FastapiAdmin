<!-- 定时任务 -->
<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form
        ref="queryFormRef"
        :model="queryFormData"
        :inline="true"
        label-suffix=":"
        @submit.prevent="handleQuery"
      >
        <el-form-item prop="name" label="任务名称">
          <el-input v-model="queryFormData.name" placeholder="请输入任务名称" clearable />
        </el-form-item>
        <el-form-item prop="status" label="状态">
          <el-select
            v-model="queryFormData.status"
            placeholder="请选择状态"
            clearable
            style="width: 167.5px"
          >
            <el-option value="true" label="运行中" />
            <el-option value="false" label="暂停" />
          </el-select>
        </el-form-item>
        <!-- 时间范围，收起状态下隐藏 -->
        <el-form-item v-if="isExpand" prop="created_time" label="创建时间">
          <DatePicker v-model="createdDateRange" @update:model-value="handleCreatedDateRangeChange" />
        </el-form-item>
        <!-- 更新时间范围，收起状态下隐藏 -->
        <el-form-item v-if="isExpand" prop="updated_time" label="更新时间">
          <DatePicker v-model="updatedDateRange" @update:model-value="handleUpdatedDateRangeChange" />
        </el-form-item>
        <el-form-item v-if="isExpand" prop="created_id" label="创建人">
          <UserTableSelect
            v-model="queryFormData.created_id"
            @confirm-click="handleConfirm"
            @clear-click="handleQuery"
          />
        </el-form-item>
        <el-form-item v-if="isExpand" prop="updated_id" label="更新人">
          <UserTableSelect
            v-model="queryFormData.updated_id"
            @confirm-click="handleConfirm"
            @clear-click="handleQuery"
          />
        </el-form-item>
        <!-- 查询、重置、展开/收起按钮 -->
        <el-form-item class="search-buttons">
          <el-button
            v-hasPerm="['module_application:job:query']"
            type="primary"
            icon="search"
            native-type="submit"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_application:job:query']"
            icon="refresh"
            @click="handleResetQuery"
          >
            重置
          </el-button>
          <!-- 展开/收起 -->
          <template v-if="isExpandable">
            <el-link class="ml-3" type="primary" underline="never" @click="isExpand = !isExpand">
              {{ isExpand ? "收起" : "展开" }}
              <el-icon>
                <template v-if="isExpand">
                  <ArrowUp />
                </template>
                <template v-else>
                  <ArrowDown />
                </template>
              </el-icon>
            </el-link>
          </template>
        </el-form-item>
      </el-form>
    </div>

    <!-- 内容区域 -->
    <el-card class="data-table">
      <template #header>
        <div class="card-header">
          <span>
            <el-tooltip content="定时任务列表">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            定时任务列表
          </span>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--left">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_application:job:create']"
                type="success"
                icon="plus"
                @click="handleOpenDialog('create')"
              >
                新增
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_application:job:delete']"
                type="danger"
                icon="delete"
                :disabled="selectIds.length === 0"
                @click="handleDelete(selectIds)"
              >
                批量删除
              </el-button>
            </el-col>
          </el-row>
        </div>
        <div class="data-table__toolbar--right">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-tooltip content="导出">
                <el-button
                  v-hasPerm="['module_application:job:export']"
                  type="warning"
                  icon="download"
                  circle
                  @click="handleOpenExportsModal"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-tooltip content="清除">
                <el-button
                  v-hasPerm="['module_application:job:delete']"
                  type="danger"
                  icon="delete"
                  circle
                  @click="handleClear"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-tooltip content="刷新">
                <el-button type="primary" icon="refresh" circle @click="handleRefresh" />
              </el-tooltip>
            </el-col>
          </el-row>
        </div>
      </div>

      <!-- 表格区域：系统配置列表 -->
      <el-table
        ref="dataTableRef"
        v-loading="loading"
        :data="pageTableData"
        class="data-table__content"
        highlight-current-row
        :height="450"
        border
        stripe
        @selection-change="handleSelectionChange"
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column type="selection" align="center" min-width="55" />
        <el-table-column type="index" fixed label="序号" min-width="60">
          <template #default="scope">
            {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column label="任务名称" prop="name" min-width="140" />
        <el-table-column label="执行函数" prop="func" min-width="140">
          <template #default="scope">
            {{
              (dictStore.getDictLabel("sys_job_function", scope.row.func) as any)?.dict_label ||
              scope.row.func
            }}
          </template>
        </el-table-column>
        <el-table-column label="触发器" prop="trigger" min-width="100" show-overflow-tooltip>
          <template #default="scope">
            {{ (dictStore.getDictLabel("sys_job_trigger", scope.row.trigger) as any)?.dict_label }}
          </template>
        </el-table-column>
        <el-table-column label="存储器" prop="jobstore" min-width="120" show-overflow-tooltip>
          <template #default="scope">
            {{ (dictStore.getDictLabel("sys_job_store", scope.row.jobstore) as any)?.dict_label }}
          </template>
        </el-table-column>
        <el-table-column label="执行器" prop="executor" min-width="100">
          <template #default="scope">
            {{
              (dictStore.getDictLabel("sys_job_executor", scope.row.executor) as any)?.dict_label
            }}
          </template>
        </el-table-column>
        <el-table-column label="并发执行" prop="coalesce" min-width="100">
          <template #default="scope">
            <el-tag :type="scope.row.coalesce === true ? 'success' : 'danger'">
              {{ scope.row.coalesce === true ? "是" : "否" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" prop="status" min-width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === '0' ? 'success' : 'danger'">
              {{ scope.row.status === true ? "运行中" : "暂停" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="描述" prop="description" min-width="100" />
        <el-table-column label="创建时间" prop="created_time" min-width="200" sortable />
        <el-table-column label="更新时间" prop="updated_time" min-width="200" sortable />
        

        <OperationColumn :list-data-length="pageTableData.length">
          <template #default="scope">
            <div class="flex">
              <el-button
                type="warning"
                size="small"
                link
                icon="document"
                @click="handleOpenLogDrawer(scope.row.id, scope.row.name)"
              >
                日志
              </el-button>
              <el-button
                type="info"
                size="small"
                link
                icon="document"
                @click="handleOpenDialog('detail', scope.row.id)"
              >
                详情
              </el-button>
              <el-button
                v-hasPerm="['module_application:job:update']"
                type="primary"
                size="small"
                link
                icon="edit"
                @click="handleOpenDialog('update', scope.row.id)"
              >
                编辑
              </el-button>
              <el-button
                v-hasPerm="['module_application:job:delete']"
                type="danger"
                size="small"
                link
                icon="delete"
                @click="handleDelete([scope.row.id])"
              >
                删除
              </el-button>
              <el-dropdown v-hasPerm="['module_application:job:update']" trigger="click">
                <el-button type="warning" size="small" link icon="ArrowDown">更多</el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item
                      :disabled="scope.row.status === false"
                      icon="Check"
                      @click="handleOption(scope.row.id, 1)"
                    >
                      暂停
                    </el-dropdown-item>
                    <el-dropdown-item
                      :disabled="scope.row.status === true"
                      icon="CircleClose"
                      @click="handleOption(scope.row.id, 2)"
                    >
                      恢复
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </template>
        </OperationColumn>
      </el-table>

      <!-- 分页区域 -->
      <template #footer>
        <pagination
          v-model:total="total"
          v-model:page="queryFormData.page_no"
          v-model:limit="queryFormData.page_size"
          @pagination="loadingData"
        />
      </template>
    </el-card>

    <!-- 弹窗区域 -->
    <el-dialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      @close="handleCloseDialog"
    >
      <!-- 详情 -->
      <template v-if="dialogVisible.type === 'detail'">
        <el-descriptions :column="4" border>
          <el-descriptions-item label="序号" :span="2">
            {{ detailFormData.id }}
          </el-descriptions-item>
          <el-descriptions-item label="任务名称" :span="2">
            {{ detailFormData.name }}
          </el-descriptions-item>
          <el-descriptions-item label="任务函数" :span="2">
            {{
              (detailFormData.func
                ? (dictStore.getDictLabel("sys_job_function", detailFormData.func) as any)
                : undefined
              )?.dict_label || detailFormData.func
            }}
          </el-descriptions-item>
          <el-descriptions-item label="存储器" :span="2">
            {{
              (detailFormData.jobstore
                ? (dictStore.getDictLabel("sys_job_store", detailFormData.jobstore) as any)
                : undefined
              )?.dict_label || detailFormData.jobstore
            }}
          </el-descriptions-item>
          <el-descriptions-item label="执行器" :span="2">
            {{
              (detailFormData.executor
                ? (dictStore.getDictLabel("sys_job_executor", detailFormData.executor) as any)
                : undefined
              )?.dict_label || detailFormData.executor
            }}
          </el-descriptions-item>
          <el-descriptions-item label="触发器" :span="2">
            {{
              (detailFormData.trigger
                ? (dictStore.getDictLabel("sys_job_trigger", detailFormData.trigger) as any)
                : undefined
              )?.dict_label || detailFormData.trigger
            }}
          </el-descriptions-item>
          <el-descriptions-item label="位置参数" :span="2">
            {{ detailFormData.args }}
          </el-descriptions-item>
          <el-descriptions-item label="关键字参数" :span="2">
            {{ detailFormData.kwargs }}
          </el-descriptions-item>
          <el-descriptions-item label="并发执行" :span="2">
            <el-tag :type="detailFormData.coalesce ? 'success' : 'danger'">
              {{ detailFormData.coalesce ? "是" : "否" }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态" :span="2">
            <el-tag :type="detailFormData.status ? 'success' : 'danger'">
              {{ detailFormData.status ? "运行中" : "暂停" }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="最大实例数" :span="2">
            {{ detailFormData.max_instances }}
          </el-descriptions-item>
          <el-descriptions-item label="触发器参数" :span="2">
            {{ detailFormData.trigger_args }}
          </el-descriptions-item>
          <el-descriptions-item label="开始时间" :span="2">
            {{ detailFormData.start_date }}
          </el-descriptions-item>
          <el-descriptions-item label="结束时间" :span="2">
            {{ detailFormData.end_date }}
          </el-descriptions-item>
          <el-descriptions-item label="创建人" :span="2">
            {{ detailFormData.created_by?.name }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">
            {{ detailFormData.created_time }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间" :span="2">
            {{ detailFormData.updated_time }}
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="4">
            {{ detailFormData.description }}
          </el-descriptions-item>
        </el-descriptions>
      </template>
      <!-- 新增、编辑表单 -->
      <template v-else>
        <el-form
          ref="dataFormRef"
          :model="formData"
          :rules="rules"
          label-suffix=":"
          label-width="auto"
          inline
        >
          <el-form-item label="任务名称" prop="name" style="width: 40%">
            <el-input v-model="formData.name" placeholder="请输入任务名称" :maxlength="50" />
          </el-form-item>
          <el-form-item label="任务函数" prop="func" style="width: 40%">
            <el-select v-model="formData.func" placeholder="请选择任务函数">
              <el-option
                v-for="item in dictStore.getDictArray('sys_job_function')"
                :key="item.dict_value"
                :label="item.dict_label"
                :value="item.dict_value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="存储器" prop="jobstore" style="width: 40%">
            <el-select v-model="formData.jobstore" placeholder="请选择存储器">
              <el-option
                v-for="item in dictStore.getDictArray('sys_job_store')"
                :key="item.dict_value"
                :label="item.dict_label"
                :value="item.dict_value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="执行器" prop="executor" style="width: 40%">
            <el-select v-model="formData.executor" placeholder="请选择执行器">
              <el-option
                v-for="item in dictStore.getDictArray('sys_job_executor')"
                :key="item.dict_value"
                :label="item.dict_label"
                :value="item.dict_value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="位置参数" prop="args" style="width: 40%">
            <el-input v-model="formData.args" placeholder="请输入位置参数" :maxlength="50" />
          </el-form-item>
          <el-form-item label="关键字参数" prop="kwargs" style="width: 40%">
            <el-input v-model="formData.kwargs" placeholder="请输入关键字参数" :maxlength="50" />
          </el-form-item>
          <el-form-item label="并发执行" prop="coalesce" style="width: 40%">
            <el-radio-group v-model="formData.coalesce">
              <el-radio :value="true">是</el-radio>
              <el-radio :value="false">否</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="最大实例数" prop="max_instances" style="width: 40%">
            <el-input-number
              v-model="formData.max_instances"
              controls-position="right"
              :min="1"
              :max="10"
            />
          </el-form-item>
          <el-form-item label="触发器" prop="trigger" style="width: 40%">
            <el-select v-model="formData.trigger" placeholder="请选择触发器">
              <el-option
                v-for="item in dictStore.getDictArray('sys_job_trigger')"
                :key="item.dict_value"
                :label="item.dict_label"
                :value="item.dict_value"
              />
            </el-select>
          </el-form-item>
          <!-- 运行日期、间隔时间或 Cron 表达式 -->
          <el-form-item
            v-if="formData.trigger === 'date'"
            label="运行日期"
            prop="trigger_args"
            :rules="[{ required: true, message: '请选择运行日期' }]"
            style="width: 40%"
          >
            <el-date-picker
              v-model="formData.trigger_args"
              type="datetime"
              format="YYYY-MM-DD HH:mm:ss"
              value-format="YYYY-MM-DD HH:mm:ss"
              placeholder="请选择运行日期"
            />
          </el-form-item>
          <el-form-item
            v-else-if="formData.trigger === 'interval'"
            label="间隔时间"
            prop="trigger_args"
            :rules="[{ required: true, message: '请输入间隔时间', trigger: 'change' }]"
            style="width: 40%"
          >
            <el-popover
              :visible="openIntervalTab"
              width="600px"
              trigger="click"
              :persistent="false"
            >
              <template #reference>
                <el-input
                  v-model="formData.trigger_args"
                  placeholder="请输入 秒-分-时-天-周"
                  readonly
                  @click="openIntervalTab = true"
                />
              </template>
              <IntervalTab
                ref="intervalTabRef"
                :cron-value="formData.trigger_args"
                @confirm="handleIntervalConfirm"
                @cancel="openIntervalTab = false"
              />
            </el-popover>
          </el-form-item>
          <el-form-item
            v-else-if="formData.trigger === 'cron'"
            label="Cron表达式"
            prop="trigger_args"
            :rules="[
              {
                required: true,
                message: '请输入Cron表达式',
                trigger: 'change',
              },
            ]"
            style="width: 40%"
          >
            <el-popover
              :visible="openCron"
              width="600px"
              trigger="click"
              :persistent="false"
              placement="left"
            >
              <template #reference>
                <el-input
                  v-model="formData.trigger_args"
                  placeholder="请输入 * * * * * ? *"
                  readonly
                  @click="openCron = true"
                />
              </template>
              <vue3CronPlus
                i18n="cn"
                max-height="500px"
                @change="handlechangeCron"
                @close="openCron = false"
              />
            </el-popover>
          </el-form-item>
          <!-- 开始日期和结束日期 -->
          <el-form-item
            v-if="formData.trigger && formData.trigger != 'date'"
            label="开始日期"
            prop="start_date"
            :rules="[{ required: false, message: '请选择开始日期', trigger: 'blur' }]"
            style="width: 40%"
          >
            <el-date-picker
              v-model="formData.start_date"
              type="datetime"
              format="YYYY-MM-DD HH:mm:ss"
              value-format="YYYY-MM-DD HH:mm:ss"
              placeholder="请选择开始日期"
            />
          </el-form-item>
          <el-form-item
            v-if="formData.trigger && formData.trigger != 'date'"
            label="结束日期"
            prop="end_date"
            :rules="[{ required: false, message: '请选择结束日期', trigger: 'blur' }]"
            style="width: 40%"
          >
            <el-date-picker
              v-model="formData.end_date"
              type="datetime"
              format="YYYY-MM-DD HH:mm:ss"
              value-format="YYYY-MM-DD HH:mm:ss"
              placeholder="请选择结束日期"
            />
          </el-form-item>

          <el-form-item label="描述" prop="description" style="width: 85%">
            <el-input
              v-model="formData.description"
              :rows="4"
              :maxlength="100"
              show-word-limit
              type="textarea"
              placeholder="请输入描述"
            />
          </el-form-item>
        </el-form>
      </template>

      <template #footer>
        <div class="dialog-footer">
          <!-- 详情弹窗不需要确定按钮的提交逻辑 -->
          <el-button @click="handleCloseDialog">取消</el-button>
          <el-button v-if="dialogVisible.type !== 'detail'" type="primary" @click="handleSubmit">
            确定
          </el-button>
          <el-button
            v-else
            v-hasPerm="['module_application:job:query']"
            type="primary"
            @click="handleCloseDialog"
          >
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
    <JobLogDrawer
      v-if="drawerVisible"
      v-model="drawerVisible"
      :job-id="currentJobId"
      :job-name="currentJobName"
    />
    <ExportModal
      v-model="exportsDialogVisible"
      :content-config="curdContentConfig"
      :query-params="queryFormData"
      :page-data="pageTableData"
      :selection-data="selectionRows"
    />
  </div>
</template>

<script lang="ts" setup>
defineOptions({
  name: "Job",
  inheritAttrs: false,
});

import JobAPI, { JobTable, JobForm, JobPageQuery } from "@/api/module_application/job";
import IntervalTab from "@/components/IntervalTab/index.vue";
import { useDictStore } from "@/store/index";
import { vue3CronPlus } from "vue3-cron-plus";
import "vue3-cron-plus/dist/index.css"; // 引入样式
import JobLogDrawer from "@/views/module_application/job/components/JobLogDrawer.vue";
import OperationColumn from "@/components/OperationColumn/index.vue";
import ExportModal from "@/components/CURD/ExportModal.vue";
import type { IContentConfig } from "@/components/CURD/types";
import { formatToDateTime } from "@/utils/dateUtil";

const dictStore = useDictStore();

const queryFormRef = ref();
const dataFormRef = ref();
const total = ref(0);
const selectIds = ref<number[]>([]);
const loading = ref(false);

const isExpand = ref(false);
const isExpandable = ref(true);

const openCron = ref(false);

const openIntervalTab = ref(false);
const intervalTabRef = ref();

// 分页表单
const pageTableData = ref<JobTable[]>([]);

// 导出弹窗显示状态 & 选中行
const exportsDialogVisible = ref(false);
const selectionRows = ref<JobTable[]>([]);

// 详情表单
const detailFormData = ref<JobTable>({} as JobTable);

// 分页查询参数
const queryFormData = reactive<JobPageQuery>({
  page_no: 1,
  page_size: 10,
  name: undefined,
  status: undefined,
  created_time: undefined,
  created_id: undefined,
});

// 编辑表单
const formData = reactive<JobForm>({
  id: undefined,
  name: undefined,
  func: undefined,
  trigger: undefined,
  args: undefined,
  kwargs: undefined,
  coalesce: false,
  max_instances: 1,
  jobstore: undefined,
  executor: undefined,
  trigger_args: undefined,
  start_date: undefined,
  end_date: undefined,
  status: undefined,
  description: undefined,
});

// 弹窗状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail" | "log",
});

// 抽屉显隐
const drawerVisible = ref(false);

// 表单验证规则
const rules = reactive({
  name: [{ required: true, message: "请输入任务名称", trigger: "blur" }],
  func: [{ required: true, message: "请输入执行函数", trigger: "blur" }],
  trigger: [{ required: true, message: "请选择触发器", trigger: "blur" }],
  coalesce: [{ required: true, message: "请选择并发执行", trigger: "blur" }],
  jobstore: [{ required: true, message: "请选择存储器", trigger: "blur" }],
  executor: [{ required: true, message: "请选择执行器", trigger: "blur" }],
});

// 日期范围临时变量
const createdDateRange = ref<[Date, Date] | []>([]);
// 更新时间范围临时变量
const updatedDateRange = ref<[Date, Date] | []>([]);

// 处理创建时间范围变化
function handleCreatedDateRangeChange(range: [Date, Date]) {
  createdDateRange.value = range;
  if (range && range.length === 2) {
    queryFormData.created_time = [formatToDateTime(range[0]), formatToDateTime(range[1])];
  } else {
    queryFormData.created_time = undefined;
  }
}

// 处理更新时间范围变化
function handleUpdatedDateRangeChange(range: [Date, Date]) {
  updatedDateRange.value = range;
  if (range && range.length === 2) {
    queryFormData.updated_time = [formatToDateTime(range[0]), formatToDateTime(range[1])];
  } else {
    queryFormData.updated_time = undefined;
  }
}

// 列表刷新
async function handleRefresh() {
  await loadingData();
}

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    const response = await JobAPI.listJob(queryFormData);
    pageTableData.value = response.data.data.items;
    total.value = response.data.data.total;
  } catch (error: any) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

// 查询（重置页码后获取数据）
async function handleQuery() {
  queryFormData.page_no = 1;
  loadingData();
}

// 选择创建人后触发查询
function handleConfirm() {
  handleQuery();
}

// 重置查询
async function handleResetQuery() {
  queryFormRef.value.resetFields();
  queryFormData.page_no = 1;
  // 额外清空日期范围与时间查询参数
  createdDateRange.value = [];
  queryFormData.created_time = undefined;
  updatedDateRange.value = [];
  queryFormData.updated_time = undefined;
  loadingData();
}

// 定义初始表单数据常量
const initialFormData: JobForm = {
  id: undefined,
  name: undefined,
  func: undefined,
  trigger: undefined,
  args: undefined,
  kwargs: undefined,
  coalesce: false,
  max_instances: 1,
  jobstore: undefined,
  executor: undefined,
  trigger_args: undefined,
  start_date: undefined,
  end_date: undefined,
  status: undefined,
  description: undefined,
};

// 重置表单
async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  // 完全重置 formData 为初始状态
  Object.assign(formData, initialFormData);
}

// 行复选框选中项变化
async function handleSelectionChange(selection: any) {
  selectIds.value = selection.map((item: any) => item.id);
  selectionRows.value = selection;
}

// 关闭弹窗
async function handleCloseDialog() {
  dialogVisible.visible = false;
  resetForm();
}

// 打开弹窗
async function handleOpenDialog(type: "create" | "update" | "detail", id?: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await JobAPI.detailJob(id);
    if (type === "detail") {
      dialogVisible.title = "任务详情";
      Object.assign(detailFormData.value, response.data.data);
    } else if (type === "update") {
      dialogVisible.title = "修改任务";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增任务";
    formData.id = undefined;
  }
  dialogVisible.visible = true;
}

// 提交表单（防抖）
async function handleSubmit() {
  // 表单校验
  dataFormRef.value.validate(async (valid: any) => {
    if (valid) {
      loading.value = true;
      // 根据弹窗传入的参数(deatil\create\update)判断走什么逻辑
      const id = formData.id;
      if (id) {
        try {
          await JobAPI.updateJob(id, formData);
          dialogVisible.visible = false;
          resetForm();
          handleCloseDialog();
          handleResetQuery();
        } catch (error: any) {
          console.log(error);
        } finally {
          loading.value = false;
        }
      } else {
        try {
          await JobAPI.createJob(formData);
          dialogVisible.visible = false;
          resetForm();
          handleCloseDialog();
          handleResetQuery();
        } catch (error: any) {
          console.log(error);
        } finally {
          loading.value = false;
        }
      }
    }
  });
}

// 删除、批量删除
async function handleDelete(ids: number[]) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        loading.value = true;
        await JobAPI.deleteJob(ids);
        handleResetQuery();
      } catch (error: any) {
        console.error(error);
      } finally {
        loading.value = false;
      }
    })
    .catch(() => {
      ElMessageBox.close();
    });
}

// 打开导出弹窗
async function handleOpenExportsModal() {
  exportsDialogVisible.value = true;
}

function handleIntervalConfirm(interval: string) {
  formData.trigger_args = interval;
  openIntervalTab.value = false;
}

const handlechangeCron = (cronStr: string) => {
  // formData.trigger_args = cronStr;
  if (typeof cronStr == "string") {
    formData.trigger_args = cronStr;
  }
};

// 清空按钮操作
const handleClear = () => {
  ElMessageBox.confirm("是否确认清空所有定时任务数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        loading.value = true;
        await JobAPI.clearJob();
        handleResetQuery();
      } catch (error: any) {
        console.error(error);
      } finally {
        loading.value = false;
      }
    })
    .catch(() => {
      ElMessageBox.close();
    });
};

// 操作按钮:操作类型 1: 暂停 2: 恢复 3: 重启（暂时移除重启）
const handleOption = (id: number, option: number) => {
  JobAPI.OptionJob({ id, option }).then(() => {
    loadingData();
  });
};

const currentJobId = ref<number>(0);
const currentJobName = ref<string>("");

function handleOpenLogDrawer(jobId: number, jobName: string) {
  currentJobId.value = jobId;
  currentJobName.value = jobName;
  drawerVisible.value = true;
}

// 导出字段
const exportColumns = [
  { prop: "name", label: "任务名称" },
  { prop: "func", label: "执行函数" },
  { prop: "trigger", label: "触发器" },
  { prop: "jobstore", label: "存储器" },
  { prop: "executor", label: "执行器" },
  { prop: "coalesce", label: "并发执行" },
  { prop: "status", label: "状态" },
  { prop: "description", label: "描述" },
  { prop: "created_time", label: "创建时间" },
  { prop: "updated_time", label: "更新时间" },
];

// 导出配置（用于导出弹窗）
const curdContentConfig = {
  permPrefix: "module_application:job",
  cols: exportColumns as any,
  exportsAction: async (params: any) => {
    const query: any = { ...params };
    if (typeof query.status === "string") query.status = query.status === "true";
    query.page_no = 1;
    query.page_size = 1000;
    const all: any[] = [];
    while (true) {
      const res = await JobAPI.listJob(query);
      const items = res.data?.data?.items || [];
      const total = res.data?.data?.total || 0;
      all.push(...items);
      if (all.length >= total || items.length === 0) break;
      query.page_no += 1;
    }
    return all;
  },
} as unknown as IContentConfig;

onMounted(async () => {
  // 加载字典数据
  await dictStore.getDict([
    "sys_job_function",
    "sys_job_executor",
    "sys_job_store",
    "sys_job_trigger",
  ]);
  // 加载表格数据
  loadingData();
});
</script>

<style lang="scss" scoped></style>
