<!-- 在线用户 -->
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
        <el-form-item prop="ipaddr" label="IP地址">
          <el-input v-model="queryFormData.ipaddr" placeholder="请输入IP地址" clearable />
        </el-form-item>
        <el-form-item prop="name" label="用户名">
          <el-input v-model="queryFormData.name" placeholder="请输入用户名" clearable />
        </el-form-item>
        <el-form-item prop="login_location" label="登录位置">
          <el-input v-model="queryFormData.login_location" placeholder="请输入登录位置" clearable />
        </el-form-item>
        <!-- 查询、重置、展开/收起按钮 -->
        <el-form-item class="search-buttons">
          <el-button
            v-hasPerm="['module_monitor:online:query']"
            type="primary"
            icon="search"
            native-type="submit"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_monitor:online:query']"
            icon="refresh"
            @click="handleResetQuery"
          >
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 内容区域 -->
    <el-card class="data-table">
      <template #header>
        <div class="card-header">
          <span>
            <el-tooltip content="在线用户列表">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            在线用户列表
          </span>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--left">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_monitor:online:delete']"
                type="danger"
                icon="delete"
                @click="handleClear"
              >
                强退所有
              </el-button>
            </el-col>
          </el-row>
        </div>
        <div class="data-table__toolbar--right">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-tooltip content="刷新">
                <el-button
                  v-hasPerm="['module_monitor:online:delete']"
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

      <!-- 表格区域：系统配置列表 -->
      <el-table
        ref="dataTableRef"
        v-loading="loading"
        :data="pageTableData"
        highlight-current-row
        class="data-table__content"
        :height="450"
        border
        stripe
        @selection-change="handleSelectionChange"
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>

        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'selection')?.show"
          type="selection"
          min-width="55"
          align="center"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'index')?.show"
          type="index"
          fixed
          label="序号"
          min-width="60"
        >
          <template #default="scope">
            {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'session_id')?.show"
          key="session_id"
          label="会话编号"
          prop="session_id"
          min-width="250"
          show-overflow-tooltip
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'login_type')?.show"
          key="login_type"
          label="登录类型"
          prop="login_type"
          min-width="100"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'ipaddr')?.show"
          key="ipaddr"
          label="IP地址"
          prop="ipaddr"
          min-width="150"
          show-overflow-tooltip
        >
          <template #default="scope">
            <el-text>{{ scope.row.ipaddr }}</el-text>
            <CopyButton v-if="scope.row.ipaddr" :text="scope.row.ipaddr" :style="{ marginLeft: '2px' }" />
          </template>
        </el-table-column>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'name')?.show"
          key="name"
          label="用户名"
          prop="name"
          min-width="80"
          show-overflow-tooltip
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'user_name')?.show"
          key="user_name"
          label="账号"
          prop="user_name"
          min-width="80"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'login_location')?.show"
          key="login_location"
          label="登录位置"
          prop="login_location"
          min-width="280"
          show-overflow-tooltip
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'os')?.show"
          key="os"
          label="操作系统"
          prop="os"
          min-width="120"
          show-overflow-tooltip
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'login_time')?.show"
          key="login_time"
          label="登录时间"
          prop="login_time"
          min-width="180"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'operation')?.show"
          key="operation"
          fixed="right"
          label="操作"
          min-width="100"
        >
          <template #default="scope">
            <el-button
              v-hasPerm="['module_monitor:online:delete']"
              type="danger"
              size="small"
              link
              icon="delete"
              @click="handleSubmit(scope.row.session_id)"
            >
              强退
            </el-button>
          </template>
        </el-table-column>
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
  </div>
</template>

<script lang="ts" setup>
defineOptions({
  name: "Notice",
  inheritAttrs: false,
});

import OnlineAPI, {
  type OnlineUserPageQuery,
  type OnlineUserTable,
} from "@/api/module_monitor/online";

const queryFormRef = ref();
const total = ref(0);
const selectIds = ref<number[]>([]);
const loading = ref(false);

// 分页表单
const pageTableData = ref<OnlineUserTable[]>([]);

// 表格列配置
const tableColumns = ref([
  { label: "选择框", prop: "selection", show: true },
  { label: "序号", prop: "index", show: true },
  { label: "会话编号", prop: "session_id", show: true },
  { label: "登录类型", prop: "login_type", show: true },
  { label: "登录名称", prop: "name", show: true },
  { label: "用户账号", prop: "user_name", show: true },
  { label: "主机", prop: "ipaddr", show: true },
  { label: "登录地点", prop: "login_location", show: true },
  { label: "操作系统", prop: "os", show: true },
  { label: "登录时间", prop: "login_time", show: true },
  { label: "操作", prop: "operation", show: true },
]);

// 分页查询参数
const queryFormData = reactive<OnlineUserPageQuery>({
  page_no: 1,
  page_size: 10,
  name: undefined,
  login_location: undefined,
  ipaddr: undefined,
});

// 列表刷新
async function handleRefresh() {
  await loadingData();
}

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    const response = await OnlineAPI.listOnline(queryFormData);
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

// 重置查询
async function handleResetQuery() {
  queryFormRef.value.resetFields();
  queryFormData.page_no = 1;
  loadingData();
}

// 行复选框选中项变化
async function handleSelectionChange(selection: any) {
  selectIds.value = selection.map((item: any) => item.id);
}

// 强制退出
async function handleSubmit(session_id: string) {
  ElMessageBox.confirm(`确认强制退出会话 ${session_id}?`, "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        loading.value = true;
        await OnlineAPI.deleteOnline(session_id);
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

// 强退所有
async function handleClear() {
  ElMessageBox.confirm("确认强制退出所有用户?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        loading.value = true;
        await OnlineAPI.clearOnline();
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
onMounted(() => {
  loadingData();
});
</script>

<style lang="scss" scoped></style>
