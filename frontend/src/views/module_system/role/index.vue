<!-- 角色管理 -->
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
        <el-form-item prop="name" label="角色名称">
          <el-input v-model="queryFormData.name" placeholder="请输入角色名称" clearable />
        </el-form-item>
        <el-form-item prop="status" label="状态">
          <el-select
            v-model="queryFormData.status"
            placeholder="请选择状态"
            style="width: 167.5px"
            clearable
          >
            <el-option value="true" label="启用" />
            <el-option value="false" label="停用" />
          </el-select>
        </el-form-item>
        <!-- 时间范围，收起状态下隐藏 -->
        <el-form-item v-if="isExpand" prop="start_time" label="创建时间">
          <DatePicker v-model="dateRange" @update:model-value="handleDateRangeChange" />
        </el-form-item>
        <el-form-item v-if="isExpand" prop="created_id" label="创建人">
          <UserTableSelect
            v-model="queryFormData.created_id"
            @confirm-click="handleConfirm"
            @clear-click="handleQuery"
          />
        </el-form-item>
        <!-- 查询、重置、展开/收起按钮 -->
        <el-form-item class="search-buttons">
          <el-button
            v-hasPerm="['module_system:role:query']"
            type="primary"
            icon="search"
            native-type="submit"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_system:role:query']"
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
            <el-tooltip content="角色管理维护系统的角色和权限。">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            角色管理列表
          </span>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--left">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_system:role:create']"
                type="success"
                icon="plus"
                @click="handleOpenDialog('create')"
              >
                新增
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_system:role:delete']"
                type="danger"
                icon="delete"
                :disabled="selectIds.length === 0"
                @click="handleDelete(selectIds)"
              >
                批量删除
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-dropdown v-hasPerm="['module_system:role:patch']" trigger="click">
                <el-button type="default" :disabled="selectIds.length === 0" icon="ArrowDown">
                  更多
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item icon="Check" @click="handleMoreClick('0')">
                      批量启用
                    </el-dropdown-item>
                    <el-dropdown-item icon="CircleClose" @click="handleMoreClick('1')">
                      批量停用
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </el-col>
          </el-row>
        </div>
        <div class="data-table__toolbar--right">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-tooltip content="导出">
                <el-button
                  v-hasPerm="['module_system:role:export']"
                  type="warning"
                  icon="download"
                  circle
                  @click="handleOpenExportsModal"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-tooltip content="刷新">
                <el-button
                  v-hasPerm="['module_system:role:query']"
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
          width="55"
          align="center"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'index')?.show"
          type="index"
          fixed
          label="序号"
          width="60"
        >
          <template #default="scope">
            {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'name')?.show"
          key="name"
          label="角色名称"
          prop="name"
          min-width="100"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'code')?.show"
          key="code"
          label="角色编码"
          prop="code"
          min-width="100"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'data_scope')?.show"
          key="data_scope"
          label="数据权限"
          prop="data_scope"
          min-width="200"
        >
          <template #default="scope">
            <el-tag v-if="scope.row.data_scope === 1" type="primary">仅本人数据权限</el-tag>
            <el-tag v-else-if="scope.row.data_scope === 2" type="info">本部门数据权限</el-tag>
            <el-tag v-else-if="scope.row.data_scope === 3" type="warning">
              本部门及以下数据权限
            </el-tag>
            <el-tag v-else-if="scope.row.data_scope === 4" type="success">全部数据权限</el-tag>
            <el-tag v-else type="danger">自定义数据权限</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'order')?.show"
          key="order"
          label="排序"
          prop="order"
          min-width="80"
          show-overflow-tooltip
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'status')?.show"
          key="status"
          label="状态"
          prop="status"
          min-width="80"
        >
          <template #default="scope">
            <el-tag :type="scope.row.status === '0' ? 'success' : 'danger'">
              {{ scope.row.status === '0' ? "启用" : "停用" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'description')?.show"
          key="description"
          label="描述"
          prop="description"
          min-width="100"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'created_time')?.show"
          key="created_time"
          label="创建时间"
          prop="created_time"
          min-width="200"
          sortable
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'updated_time')?.show"
          key="updated_time"
          label="更新时间"
          prop="updated_time"
          min-width="200"
          sortable
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'created_id')?.show"
          key="created_id"
          label="创建人"
          min-width="120"
        >
          <template #default="scope">
            {{ scope.row.created_by?.name }}
          </template>
        </el-table-column>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'updated_id')?.show"
          key="updated_id"
          label="更新人"
          min-width="120"
        >
          <template #default="scope">
            {{ scope.row.updated_by?.name }}
          </template>
        </el-table-column>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'operation')?.show"
          fixed="right"
          label="操作"
          align="center"
          min-width="280"
        >
          <template #default="scope">
            <el-button
              v-hasPerm="['module_system:role:permission']"
              type="warning"
              size="small"
              link
              icon="position"
              :disabled="scope.row.id === 1"
              @click="
                scope.row.id === 1
                  ? ElMessage.warning('系统默认角色，不可操作')
                  : handleOpenAssignPermDialog(scope.row.id, scope.row.name)
              "
            >
              分配权限
            </el-button>
            <el-button
              v-hasPerm="['module_system:role:query']"
              type="info"
              size="small"
              link
              icon="document"
              @click="handleOpenDialog('detail', scope.row.id)"
            >
              详情
            </el-button>
            <el-button
              v-hasPerm="['module_system:role:update']"
              type="primary"
              size="small"
              link
              icon="edit"
              :disabled="scope.row.id === 1"
              @click="
                scope.row.id === 1
                  ? ElMessage.warning('系统默认角色，不可操作')
                  : handleOpenDialog('update', scope.row.id)
              "
            >
              编辑
            </el-button>
            <el-button
              v-hasPerm="['module_system:role:delete']"
              type="danger"
              size="small"
              link
              icon="delete"
              :disabled="scope.row.id === 1"
              @click="
                scope.row.id === 1
                  ? ElMessage.warning('系统默认角色，不可操作')
                  : handleDelete([scope.row.id])
              "
            >
              删除
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

    <!-- 角色表单弹窗 -->
    <el-dialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      @close="handleCloseDialog"
    >
      <!-- 详情 -->
      <template v-if="dialogVisible.type === 'detail'">
        <el-descriptions :column="4" border>
          <el-descriptions-item label="角色名称" :span="2">
            {{ detailFormData.name }}
          </el-descriptions-item>
          <el-descriptions-item label="排序" :span="2">
            {{ detailFormData.order }}
          </el-descriptions-item>
          <el-descriptions-item label="角色编码" :span="2">
            {{ detailFormData.code }}
          </el-descriptions-item>
          <el-descriptions-item label="数据权限" :span="2">
            <el-tag v-if="detailFormData.data_scope === 1" type="primary">仅本人数据权限</el-tag>
            <el-tag v-else-if="detailFormData.data_scope === 2" type="info">本部门数据权限</el-tag>
            <el-tag v-else-if="detailFormData.data_scope === 3" type="warning">
              本部门及以下数据权限
            </el-tag>
            <el-tag v-else-if="detailFormData.data_scope === 4" type="success">全部数据权限</el-tag>
            <el-tag v-else type="danger">自定义数据权限</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态" :span="2">
            <el-tag :type="detailFormData.status ? 'success' : 'danger'">
              {{ detailFormData.status ? "启用" : "停用" }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="创建人" :span="2">
            {{ detailFormData.created_by?.name }}
          </el-descriptions-item>
          <el-descriptions-item label="更新人" :span="2">
            {{ detailFormData.updated_by?.name }}
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
          label-position="right"
        >
          <el-form-item label="角色名称" prop="name">
            <el-input v-model="formData.name" placeholder="请输入角色名称" />
          </el-form-item>

          <el-form-item label="排序" prop="order">
            <el-input-number
              v-model="formData.order"
              controls-position="right"
              :min="0"
              style="width: 100px"
            />
          </el-form-item>

          <el-form-item label="角色编码" prop="code">
            <el-input v-model="formData.code" placeholder="请输入角色编码" />
          </el-form-item>

          <el-form-item label="状态" prop="status">
            <el-radio-group v-model="formData.status">
              <el-radio value="0">启用</el-radio>
              <el-radio value="1">停用</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="描述" prop="description">
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
          <el-button @click="handleCloseDialog">取 消</el-button>
          <el-button type="primary" @click="handleSubmit">确 定</el-button>
        </div>
      </template>
    </el-dialog>

    <PermissonDrawer
      v-if="drawerVisible"
      v-model="drawerVisible"
      :role-name="checkedRole.name"
      :role-id="checkedRole.id"
      @saved="handleRefresh"
    />

    <!-- 导出弹窗 -->
    <ExportModal
      v-model="exportsDialogVisible"
      :content-config="curdContentConfig"
      :query-params="queryFormData"
      :page-data="pageTableData"
      :selection-data="selectionRows"
    />
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "Role",
  inheritAttrs: false,
});

import { ElMessage, ElMessageBox } from "element-plus";
import RoleAPI, { RoleTable, RoleForm, TablePageQuery } from "@/api/module_system/role";
import { useUserStore } from "@/store";
import UserTableSelect from "@/views/module_system/user/components/UserTableSelect.vue";
import ExportModal from "@/components/CURD/ExportModal.vue";
import type { IContentConfig } from "@/components/CURD/types";
import { QuestionFilled, ArrowUp, ArrowDown } from "@element-plus/icons-vue";
import { formatToDateTime } from "@/utils/dateUtil";

const queryFormRef = ref();
const dataFormRef = ref();
const selectIds = ref<number[]>([]);
const loading = ref(false);
const total = ref(0);
const isExpand = ref(false);
const isExpandable = ref(true);

// 分页表单
const pageTableData = ref<RoleTable[]>([]);

// 抽屉显隐
const drawerVisible = ref(false);

// 表格列配置
const tableColumns = ref([
  { prop: "selection", label: "选择框", show: true },
  { prop: "index", label: "序号", show: true },
  { prop: "name", label: "角色名称", show: true },
  { prop: "data_scope", label: "数据权限", show: true },
  { prop: "order", label: "排序", show: true },
  { prop: "code", label: "角色编码", show: true },
  { prop: "status", label: "状态", show: true },
  { prop: "description", label: "描述", show: true },
  { prop: "created_time", label: "创建时间", show: true },
  { prop: "updated_time", label: "更新时间", show: true },
  { prop: "created_id", label: "创建人", show: true },
  { prop: "updated_id", label: "更新人", show: true },
  { prop: "operation", label: "操作", show: true },
]);

// 详情表单
const detailFormData = ref<RoleTable>({} as RoleTable);

// 选中的角色
const checkedRole = ref<RoleTable>({} as RoleTable);

const queryFormData = reactive<TablePageQuery>({
  page_no: 1,
  page_size: 10,
  name: "",
  status: undefined,
  created_id: undefined,
  updated_id: undefined,
  created_time: undefined,
  updated_time: undefined,
});

// 新增、编辑表单
const formData = reactive<RoleForm>({
  id: undefined,
  name: undefined,
  order: 1,
  code: undefined,
  status: '0',
  description: undefined,
});

// 弹窗状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

// 表单验证规则
const rules = reactive({
  name: [{ required: true, message: "请输入角色名称", trigger: "blur" }],
  order: [{ required: true, message: "请输入角色排序", trigger: "blur" }],
  status: [{ required: true, message: "请选择状态", trigger: "blur" }],
});

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    const response = await RoleAPI.listRole(queryFormData);
    pageTableData.value = response.data.data.items;
    total.value = response.data.data.total;
  } catch (error: any) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

// 列表刷新
async function handleRefresh() {
  await loadingData();
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

// 行复选框选中项变化
async function handleSelectionChange(selection: any) {
  selectIds.value = selection.map((item: any) => item.id);
  selectionRows.value = selection;
}

// 重置查询
async function handleResetQuery() {
  queryFormRef.value.resetFields();
  queryFormData.page_no = 1;
  // 额外清空日期范围与时间查询参数
  dateRange.value = [];
  queryFormData.created_time = undefined;
  loadingData();
}

// 定义初始表单数据常量
const initialFormData: RoleForm = {
  id: undefined,
  name: undefined,
  order: 1,
  code: undefined,
  status: '0',
  description: undefined,
};

// 日期范围临时变量
const dateRange = ref<[Date, Date] | []>([]);

// 处理日期范围变化
function handleDateRangeChange(range: [Date, Date]) {
  dateRange.value = range;
  if (range && range.length === 2) {
    queryFormData.created_time = [formatToDateTime(range[0]), formatToDateTime(range[1])];
  } else {
    queryFormData.created_time = undefined;
  }
}

// 重置表单
async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  // 完全重置 formData 为初始状态
  Object.assign(formData, initialFormData);
}

// 关闭弹窗
async function handleCloseDialog() {
  dialogVisible.visible = false;
  resetForm();
}

// 打开系统配置弹窗
async function handleOpenDialog(type: "create" | "update" | "detail", id?: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await RoleAPI.detailRole(id);
    if (type === "detail") {
      dialogVisible.title = "角色详情";
      Object.assign(detailFormData.value, response.data.data);
    } else if (type === "update") {
      dialogVisible.title = "修改角色";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增角色";
    formData.id = undefined;
  }
  dialogVisible.visible = true;
}

// 新增、编辑弹窗处理
async function handleSubmit() {
  // 表单校验
  dataFormRef.value.validate(async (valid: any) => {
    if (valid) {
      loading.value = true;
      // 根据弹窗传入的参数(deatil\create\update)判断走什么逻辑
      const id = formData.id;
      try {
        if (id) {
          await RoleAPI.updateRole(id, { id, ...formData });
        } else {
          await RoleAPI.createRole(formData);
        }
        dialogVisible.visible = false;
        resetForm();
        handleResetQuery();
        // 更新全局用户状态，刷新权限信息
        const userStore = useUserStore();
        await userStore.getUserInfo();
      } catch (error: any) {
        console.error(error);
      } finally {
        loading.value = false;
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
        await RoleAPI.deleteRole(ids);
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

// 导出已改为通过导出弹窗 ExportModal 统一处理
function handleOpenExportsModal() {
  exportsDialogVisible.value = true;
}

// 批量启用/停用
async function handleMoreClick(status: string) {
  if (selectIds.value.length) {
    ElMessageBox.confirm(`确认${status === "0" ? "启用" : "停用"}该项数据?`, "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    })
      .then(async () => {
        try {
          loading.value = true;
          await RoleAPI.batchRole({ ids: selectIds.value, status });
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
}

// 打开分配菜单权限弹窗
async function handleOpenAssignPermDialog(roleId: number, roleName: string) {
  if (roleId) {
    drawerVisible.value = true;
    checkedRole.value.id = roleId;
    checkedRole.value.name = roleName;
  }
}

// 导出弹窗显示状态
const exportsDialogVisible = ref(false);
const selectionRows = ref<RoleTable[]>([]);
// 导出字段
const exportColumns = [
  { prop: "name", label: "角色名称" },
  { prop: "code", label: "角色编码" },
  { prop: "data_scope", label: "数据权限" },
  { prop: "order", label: "排序" },
  { prop: "status", label: "状态" },
  { prop: "description", label: "描述" },
  { prop: "created_time", label: "创建时间" },
  { prop: "updated_time", label: "更新时间" },
];

// 导入/导出配置
const curdContentConfig = {
  permPrefix: "module_system:role",
  cols: exportColumns as any,
  exportsAction: async (params: any) => {
    const query: any = { ...params };
    if (typeof query.status === "string") {
      query.status = query.status === "true";
    }
    query.page_no = 1;
    query.page_size = 1000;
    const all: any[] = [];
    while (true) {
      const res = await RoleAPI.listRole(query);
      const items = res.data?.data?.items || [];
      const total = res.data?.data?.total || 0;
      all.push(...items);
      if (all.length >= total || items.length === 0) break;
      query.page_no += 1;
    }
    return all;
  },
} as unknown as IContentConfig;

onMounted(() => {
  loadingData();
});
</script>

<style lang="scss" scoped></style>
