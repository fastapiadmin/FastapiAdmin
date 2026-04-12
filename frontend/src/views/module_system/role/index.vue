<!-- 角色管理 -->
<template>
  <div class="app-container">
    <PageSearch
      ref="searchRef"
      :search-config="searchConfig"
      @query-click="handleQueryClick"
      @reset-click="handleResetClick"
    />

    <PageContent ref="contentRef" :content-config="contentConfig">
      <template #toolbar="{ toolbarRight, onToolbar, removeIds, cols }">
        <CrudToolbarLeft
          :remove-ids="removeIds"
          :perm-create="['module_system:role:create']"
          :perm-delete="['module_system:role:delete']"
          :perm-patch="['module_system:role:patch']"
          @add="handleOpenDialog('create')"
          @delete="onToolbar('delete')"
          @more="handleMoreClick"
        />
        <div class="data-table__toolbar--right">
          <CrudToolbarRight :buttons="toolbarRight" :cols="cols" :on-toolbar="onToolbar">
            <template #prepend>
              <el-tooltip content="导出">
                <el-button
                  v-hasPerm="['module_system:role:export']"
                  type="warning"
                  icon="download"
                  circle
                  @click="handleOpenExportsModal"
                />
              </el-tooltip>
            </template>
          </CrudToolbarRight>
        </div>
      </template>

      <template #table="{ data, loading, tableRef, onSelectionChange, pagination }">
        <div class="data-table__content">
          <el-table
            :ref="tableRef as any"
            v-loading="loading"
            row-key="id"
            :data="data"
            height="100%"
            border
            stripe
            @selection-change="onSelectionChange"
          >
            <template #empty>
              <el-empty :image-size="80" description="暂无数据" />
            </template>
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'selection')?.show"
              type="selection"
              width="55"
              align="center"
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'index')?.show"
              fixed
              label="序号"
              width="60"
            >
              <template #default="scope">
                {{ (pagination.currentPage - 1) * pagination.pageSize + scope.$index + 1 }}
              </template>
            </el-table-column>
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'name')?.show"
              key="name"
              label="角色名称"
              prop="name"
              min-width="100"
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'code')?.show"
              key="code"
              label="角色编码"
              prop="code"
              min-width="100"
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'data_scope')?.show"
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
              v-if="contentCols.find((col) => col.prop === 'depts')?.show"
              key="depts"
              label="所属部门"
              prop="depts"
              min-width="200"
            >
              <template #default="scope">
                <template v-if="scope.row.depts && scope.row.depts.length > 0">
                  <el-tag
                    v-for="dept in scope.row.depts.slice(0, 3)"
                    :key="dept.id"
                    type="info"
                    style="margin-right: 4px; margin-bottom: 4px"
                  >
                    {{ dept.name }}
                  </el-tag>
                  <el-tag v-if="scope.row.depts.length > 3" type="info" style="margin-bottom: 4px">
                    +{{ scope.row.depts.length - 3 }}
                  </el-tag>
                </template>
                <span v-else style="color: var(--el-text-color-placeholder)">-</span>
              </template>
            </el-table-column>
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'order')?.show"
              key="order"
              label="排序"
              prop="order"
              min-width="80"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'status')?.show"
              key="status"
              label="状态"
              prop="status"
              min-width="80"
            >
              <template #default="scope">
                <el-tag :type="scope.row.status === '0' ? 'success' : 'danger'">
                  {{ scope.row.status === "0" ? "启用" : "停用" }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'description')?.show"
              key="description"
              label="描述"
              prop="description"
              min-width="100"
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'created_time')?.show"
              key="created_time"
              label="创建时间"
              prop="created_time"
              min-width="200"
              sortable
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'updated_time')?.show"
              key="updated_time"
              label="更新时间"
              prop="updated_time"
              min-width="200"
              sortable
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'operation')?.show"
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
                  v-hasPerm="['module_system:role:detail']"
                  type="info"
                  size="small"
                  link
                  icon="View"
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
                      : handleRowDelete(scope.row.id)
                  "
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </template>
    </PageContent>

    <EnhancedDialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      @close="handleCloseDialog"
    >
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
          <el-descriptions-item label="所属部门" :span="2">
            <template v-if="detailFormData.depts && detailFormData.depts.length > 0">
              <el-tag
                v-for="dept in detailFormData.depts"
                :key="dept.id"
                type="info"
                style="margin-right: 4px; margin-bottom: 4px"
              >
                {{ dept.name }}
              </el-tag>
            </template>
            <span v-else style="color: var(--el-text-color-placeholder)">-</span>
          </el-descriptions-item>
          <el-descriptions-item label="状态" :span="2">
            <el-tag :type="detailFormData.status === '0' ? 'success' : 'danger'">
              {{ detailFormData.status === "0" ? "启用" : "停用" }}
            </el-tag>
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
            <el-input
              v-model="formData.code"
              placeholder="字母开头，2-16位字母/数字/下划线"
              maxlength="16"
              show-word-limit
            />
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
          <el-button @click="handleCloseDialog">取消</el-button>
          <el-button
            v-if="dialogVisible.type !== 'detail'"
            type="primary"
            :loading="submitLoading"
            @click="handleSubmit"
          >
            确定
          </el-button>
          <el-button v-else type="primary" @click="handleCloseDialog">确定</el-button>
        </div>
      </template>
    </EnhancedDialog>

    <PermissonDrawer
      v-if="drawerVisible"
      v-model="drawerVisible"
      :role-name="checkedRole.name"
      :role-id="checkedRole.id"
      @saved="refreshList"
    />

    <ExportModal
      v-model="exportsDialogVisible"
      :content-config="curdContentConfig"
      :query-params="exportQueryParams"
      :page-data="exportPageData"
      :selection-data="exportSelectionData"
    />
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "Role",
  inheritAttrs: false,
});

import { ElMessage, ElMessageBox } from "element-plus";
import { ref, reactive, computed, unref } from "vue";
import { fetchAllPages } from "@/utils/fetchAllPages";
import RoleAPI, { RoleTable, RoleForm, TablePageQuery } from "@/api/module_system/role";
import { useUserStore } from "@/store";
import ExportModal from "@/components/CURD/ExportModal.vue";
import CrudToolbarLeft from "@/components/CURD/CrudToolbarLeft.vue";
import CrudToolbarRight from "@/components/CURD/CrudToolbarRight.vue";
import PageSearch from "@/components/CURD/PageSearch.vue";
import PageContent from "@/components/CURD/PageContent.vue";
import EnhancedDialog from "@/components/CURD/EnhancedDialog.vue";
import PermissonDrawer from "./components/PermissonDrawer.vue";
import { useCrudList } from "@/components/CURD/useCrudList";
import type { IContentConfig, ISearchConfig } from "@/components/CURD/types";

const { searchRef, contentRef, handleQueryClick, handleResetClick, refreshList } = useCrudList();
const dataFormRef = ref();
const submitLoading = ref(false);

const searchConfig = reactive<ISearchConfig>({
  permPrefix: "module_system:role",
  colon: true,
  isExpandable: true,
  showNumber: 2,
  form: { labelWidth: "auto" },
  formItems: [
    {
      prop: "name",
      label: "角色名称",
      type: "input",
      attrs: { placeholder: "请输入角色名称", clearable: true },
    },
    {
      prop: "status",
      label: "状态",
      type: "select",
      options: [
        { label: "启用", value: "true" },
        { label: "停用", value: "false" },
      ],
      attrs: { placeholder: "请选择状态", clearable: true, style: { width: "167.5px" } },
    },
    {
      prop: "created_time",
      label: "创建时间",
      type: "date-picker",
      initialValue: [],
      attrs: {
        type: "datetimerange",
        valueFormat: "YYYY-MM-DD HH:mm:ss",
        rangeSeparator: "至",
        startPlaceholder: "开始日期",
        endPlaceholder: "结束日期",
        style: { width: "340px" },
      },
    },
  ],
});

const contentCols = reactive<
  Array<{
    prop?: string;
    label?: string;
    show?: boolean;
  }>
>([
  { prop: "selection", label: "选择框", show: true },
  { prop: "index", label: "序号", show: true },
  { prop: "name", label: "角色名称", show: true },
  { prop: "data_scope", label: "数据权限", show: true },
  { prop: "depts", label: "所属部门", show: true },
  { prop: "order", label: "排序", show: true },
  { prop: "code", label: "角色编码", show: true },
  { prop: "status", label: "状态", show: true },
  { prop: "description", label: "描述", show: true },
  { prop: "created_time", label: "创建时间", show: true },
  { prop: "updated_time", label: "更新时间", show: true },
  { prop: "operation", label: "操作", show: true },
]);

const contentConfig = reactive<IContentConfig<TablePageQuery>>({
  permPrefix: "module_system:role",
  pk: "id",
  cols: contentCols as IContentConfig["cols"],
  hideColumnFilter: false,
  toolbar: [],
  defaultToolbar: ["search", "refresh", "filter"],
  pagination: {
    pageSize: 10,
    pageSizes: [10, 20, 30, 50],
  },
  request: { page_no: "page_no", page_size: "page_size" },
  indexAction: async (params) => {
    const res = await RoleAPI.listRole(params as TablePageQuery);
    return {
      total: res.data.data.total,
      list: res.data.data.items,
    };
  },
  deleteAction: async (ids) => {
    await RoleAPI.deleteRole(
      ids
        .split(",")
        .map((s) => Number(s.trim()))
        .filter((n) => !Number.isNaN(n))
    );
    const userStore = useUserStore();
    await userStore.getUserInfo();
  },
  deleteConfirm: {
    title: "警告",
    message: "确认删除该项数据?",
    type: "warning",
  },
});

function handleRowDelete(id: number) {
  contentRef.value?.handleDelete(id);
}

const drawerVisible = ref(false);
const checkedRole = ref({ id: 0, name: "" });

const exportsDialogVisible = ref(false);

const exportQueryParams = computed(() => searchRef.value?.getQueryParams() ?? {});

const exportPageData = computed(() => (unref(contentRef.value?.pageData) ?? []) as RoleTable[]);

const exportSelectionData = computed(
  () => (contentRef.value?.getSelectionData() ?? []) as RoleTable[]
);

const exportColumns = [
  { prop: "name", label: "角色名称" },
  { prop: "code", label: "角色编码" },
  { prop: "data_scope", label: "数据权限" },
  { prop: "depts", label: "所属部门" },
  { prop: "order", label: "排序" },
  { prop: "status", label: "状态" },
  { prop: "description", label: "描述" },
  { prop: "created_time", label: "创建时间" },
  { prop: "updated_time", label: "更新时间" },
];

const curdContentConfig = {
  permPrefix: "module_system:role",
  cols: exportColumns as unknown as IContentConfig["cols"],
  exportsAction: async (params: Record<string, unknown>) => {
    const query: Record<string, unknown> = { ...params };
    if (typeof query.status === "string") {
      query.status = query.status === "true";
    }
    return fetchAllPages<RoleTable>({
      initialQuery: query,
      fetchPage: async (q) => {
        const res = await RoleAPI.listRole(q as unknown as TablePageQuery);
        return {
          total: res.data?.data?.total ?? 0,
          list: res.data?.data?.items ?? [],
        };
      },
    });
  },
} as unknown as IContentConfig;

function handleOpenExportsModal() {
  exportsDialogVisible.value = true;
}

const detailFormData = ref<RoleTable>({} as RoleTable);

const formData = reactive<RoleForm>({
  id: undefined,
  name: undefined,
  order: 1,
  code: "",
  status: "0",
  description: undefined,
});

const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

const CODE_PATTERN = /^[A-Za-z][A-Za-z0-9_]{1,15}$/;

const rules = reactive({
  name: [{ required: true, message: "请输入角色名称", trigger: "blur" }],
  code: [
    { required: true, message: "请输入角色编码", trigger: "blur" },
    {
      pattern: CODE_PATTERN,
      message: "字母开头，2-16位字母/数字/下划线",
      trigger: "blur",
    },
  ],
  order: [{ required: true, message: "请输入角色排序", trigger: "blur" }],
  status: [{ required: true, message: "请选择状态", trigger: "blur" }],
});

const initialFormData: RoleForm = {
  id: undefined,
  name: undefined,
  order: 1,
  code: "",
  status: "0",
  description: undefined,
};

async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  Object.assign(formData, initialFormData);
}

async function handleCloseDialog() {
  dialogVisible.visible = false;
  await resetForm();
}

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

async function handleSubmit() {
  dataFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      submitLoading.value = true;
      const id = formData.id;
      try {
        if (id) {
          await RoleAPI.updateRole(id, { id, ...formData });
        } else {
          await RoleAPI.createRole(formData);
        }
        dialogVisible.visible = false;
        await resetForm();
        refreshList();
        const userStore = useUserStore();
        await userStore.getUserInfo();
      } catch (error: unknown) {
        console.error(error);
      } finally {
        submitLoading.value = false;
      }
    }
  });
}

async function handleMoreClick(status: string) {
  const rows = contentRef.value?.getSelectionData() as RoleTable[] | undefined;
  const ids = (rows ?? []).map((r) => r.id).filter((id): id is number => id != null);
  if (!ids.length) {
    ElMessage.warning("请先选择要操作的数据");
    return;
  }
  ElMessageBox.confirm(`确认${status === "0" ? "启用" : "停用"}该项数据?`, "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        await RoleAPI.batchRole({ ids, status });
        refreshList();
        const userStore = useUserStore();
        await userStore.getUserInfo();
      } catch (error: unknown) {
        console.error(error);
      }
    })
    .catch(() => {
      ElMessageBox.close();
    });
}

function handleOpenAssignPermDialog(roleId: number, roleName: string) {
  checkedRole.value = { id: roleId, name: roleName };
  drawerVisible.value = true;
}
</script>
