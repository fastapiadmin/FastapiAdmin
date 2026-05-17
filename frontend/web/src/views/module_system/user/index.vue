<!-- 用户管理：左部门树 + 右 Art 表格 -->
<template>
  <div class="fa-full-height user-manage-page">
    <div
      class="user-manage-body box-border flex gap-4 h-full max-md:block max-md:gap-0 max-md:h-auto"
    >
      <div class="user-dept-panel shrink-0 w-58 h-full max-md:w-full max-md:h-auto max-md:mb-5">
        <ElCard class="tree-card fa-card-xs flex flex-col h-full mt-0" shadow="hover">
          <template #header>
            <b>部门</b>
          </template>
          <ElScrollbar class="dept-tree-scroll min-h-0 flex-1">
            <FaDeptTree
              v-model="deptFilterId"
              class="dept-tree-inner"
              @node-click="handleDeptNodeClick"
            />
          </ElScrollbar>
        </ElCard>
      </div>

      <div class="user-main-panel flex flex-col grow min-w-0 min-h-0">
        <FaSearchBar
          v-show="showSearchBar"
          ref="searchBarRef"
          v-model="searchForm"
          :items="userSearchItems"
          :rules="searchBarRules"
          :is-expand="false"
          :show-expand="true"
          :show-reset="true"
          :show-search="true"
          :disabled-search="false"
          :default-expanded="false"
          @search="handleSearchBarSearch"
          @reset="onResetSearch"
        >
          <template #created_id>
            <FaUserTableSelect
              :model-value="searchForm.created_id == null ? undefined : searchForm.created_id"
              @update:model-value="(v: number | undefined) => (searchForm.created_id = v)"
              @confirm-click="afterUserSelectSearch"
              @clear-click="afterUserSelectSearch"
            />
          </template>
        </FaSearchBar>

        <ElCard
          shadow="hover"
          class="fa-table-card"
          :style="{ 'margin-top': showSearchBar ? '12px' : '0' }"
        >
          <FaTableHeader
            v-model:columns="columnChecks"
            v-model:showSearchBar="showSearchBar"
            :loading="loading"
            @refresh="refreshData"
          >
            <template #left>
              <FaTableHeaderLeft
                :remove-ids="selectedIds"
                :perm-create="['module_system:user:create']"
                :perm-import="['module_system:user:import']"
                :perm-export="['module_system:user:export']"
                :perm-delete="['module_system:user:delete']"
                :perm-patch="['module_system:user:patch']"
                :import-loading="uploadLoading"
                :delete-loading="batchDeleting"
                @add="handleOpenDialog('create')"
                @import="openImport"
                @export="openExport"
                @delete="handleBatchDelete"
                @more="handleMoreClick"
              />
            </template>
          </FaTableHeader>

          <FaTable
            ref="faTableRef"
            row-key="id"
            :loading="loading"
            :data="data"
            :columns="columns"
            :pagination="pagination"
            @selection-change="onTableSelectionChange"
            @pagination:size-change="handleSizeChange"
            @pagination:current-change="handleCurrentChange"
          />
        </ElCard>
      </div>
    </div>

    <FaDrawer
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      append-to-body
      :size="drawerSize"
      :form-mode="dialogVisible.type"
      :confirm-loading="submitLoading"
      @cancel="handleCloseDialog"
      @confirm="dialogVisible.type === 'detail' ? handleCloseDialog() : handleSubmit()"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <FaDescriptions
          :column="2"
          :data="detailFormData"
          :items="userDetailItems"
          :scrollbar="false"
        >
          <!-- 头像 → 自定义渲染 -->
          <template #avatar="{ row }">
            <ElAvatar v-if="row?.avatar" :src="row?.avatar as string" size="small" />
            <ElAvatar v-else icon="UserFilled" size="small" />
          </template>
          <!-- 性别 → 三种状态 Tag -->
          <template #gender="{ row }">
            <ElTag v-if="row?.gender === '0'" type="success">男</ElTag>
            <ElTag v-else-if="row?.gender === '1'" type="warning">女</ElTag>
            <ElTag v-else type="info">未知</ElTag>
          </template>
          <!-- 角色 → 数组 join 渲染 -->
          <template #roles="{ row }">
            {{ row?.roles ? (row.roles as any[]).map((item: any) => item.name).join("、") : "" }}
          </template>
          <!-- 岗位 → 数组 join 渲染 -->
          <template #positions="{ row }">
            {{
              row?.positions
                ? (row.positions as any[]).map((item: any) => item.name).join("、")
                : ""
            }}
          </template>
        </FaDescriptions>
      </template>
      <template v-else>
        <FaForm
          :key="userFormRenderKey"
          ref="dataFormRef"
          v-model="formData"
          :items="userDialogFormItems"
          :rules="rules"
          label-suffix=":"
          :label-width="'auto'"
          label-position="right"
          :span="24"
          :gutter="16"
          :show-reset="false"
          :show-submit="false"
          class="crud-dialog-art-form"
        >
          <template #dept_id>
            <ElTreeSelect
              v-model="formData.dept_id"
              placeholder="请选择上级部门"
              :data="deptOptions"
              :props="{ children: 'children', label: 'label', disabled: 'disabled' }"
              filterable
              check-strictly
              :render-after-expand="false"
            />
          </template>
          <template #role_ids>
            <ElSelect v-model="formData.role_ids" multiple placeholder="请选择角色">
              <ElOption
                v-for="item in roleOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
                :disabled="item.disabled"
              />
            </ElSelect>
          </template>
          <template #position_ids>
            <ElSelect v-model="formData.position_ids" multiple placeholder="请选择岗位">
              <ElOption
                v-for="item in positionOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
                :disabled="item.disabled"
              />
            </ElSelect>
          </template>
        </FaForm>
      </template>
    </FaDrawer>

    <FaImportDialog
      v-model="importVisible"
      :content-config="userImportContentConfig"
      default-template-file-name="user_import_template.xlsx"
      :loading="uploadLoading"
      @upload="handleImportUpload"
    />

    <FaExportDialog
      v-model="exportVisible"
      :content-config="userExportContentConfig"
      :query-params="exportQueryParams"
      :page-data="data"
      :selection-data="selectedRows"
    />
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "User",
  inheritAttrs: false,
});

import { UserFilled } from "@element-plus/icons-vue";
import { ElAvatar } from "element-plus";
import { DeviceEnum } from "@/enums/settings/device.enum";
import { ResultEnum } from "@/enums/api/result.enum";
import { useTable } from "@/hooks/core/useTable";
import { useImportExport } from "@/hooks/core/useImportExport";
import { useTableSelection } from "@/hooks/core/useTableSelection";
import { useCrudDialog } from "@/hooks/core/useCrudDialog";
import { confirmDelete, confirmBatchDelete, confirmToggleStatus } from "@/hooks/core/useConfirm";
import { cleanEmptyArrayParams, stripPaginationParams } from "@/utils/query";
import UserAPI, {
  type UserForm,
  type UserInfo,
  type UserPageQuery,
} from "@/api/module_system/user";
import { formatTree, renderTableOperationCell, type TableOperationAction } from "@utils";
import PositionAPI from "@/api/module_system/position";
import DeptAPI from "@/api/module_system/dept";
import RoleAPI from "@/api/module_system/role";
import { useAppStore, useUserStore } from "@stores";
import { useAuth } from "@/hooks/core/useAuth";
import type { ColumnOption } from "@/types/component";
import FaUserTableSelect from "@/components/forms/fa-search-bar/FaUserTableSelect.vue";
import type { DescriptionsItem } from "@/components/others/fa-descriptions/index.vue";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import type { IContentConfig, IObject } from "@/components/modal/types";
import FaSearchBar from "@/components/forms/fa-search-bar/index.vue";
import FaForm from "@/components/forms/fa-form/index.vue";
import FaDeptTree from "./components/FaDeptTree.vue";
import { ElTag, ElMessage, ElMessageBox } from "element-plus";

const { hasAuth } = useAuth();
const appStore = useAppStore();
const userStore = useUserStore();

type UserSearchForm = {
  username?: string;
  name?: string;
  status?: string;
  created_id?: number;
  created_time?: string[];
};

function buildUserReplaceParams(u: UserSearchForm): Record<string, unknown> {
  return {
    username: u.username,
    name: u.name,
    status: u.status,
    created_id: u.created_id,
    created_time:
      Array.isArray(u.created_time) && u.created_time.length === 2 ? u.created_time : undefined,
  };
}

function fetchUserTableList(params: Record<string, unknown>) {
  return UserAPI.listUser({
    page_no: 1,
    page_size: 10,
    ...params,
    dept_id:
      deptFilterId.value !== undefined && deptFilterId.value !== null && deptFilterId.value !== ""
        ? Number(deptFilterId.value)
        : undefined,
  });
}

function buildUserRowActions(
  row: UserInfo,
  ctx: {
    onResetPwd: (row: UserInfo) => void;
    onDetail: (id: number) => void;
    onEdit: (id: number) => void;
    onDelete: (id: number) => void;
  }
): TableOperationAction[] {
  const sys = row.is_superuser === true;
  const all: TableOperationAction[] = [
    {
      key: "resetPwd",
      label: "重置密码",
      artType: "edit",
      icon: "ri:refresh-line",
      perm: "module_system:user:update",
      disabled: sys,
      run: () => {
        if (sys) return;
        ctx.onResetPwd(row);
      },
    },
    {
      key: "detail",
      label: "详情",
      artType: "view",
      perm: "module_system:user:detail",
      run: () => ctx.onDetail(row.id!),
    },
    {
      key: "edit",
      label: "编辑",
      artType: "edit",
      perm: "module_system:user:update",
      disabled: sys,
      run: () => {
        if (sys) return;
        ctx.onEdit(row.id!);
      },
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      perm: "module_system:user:delete",
      disabled: sys,
      run: () => {
        if (sys) return;
        ctx.onDelete(row.id!);
      },
    },
  ];
  return all.filter((a) => a.perm != null && hasAuth(a.perm));
}

function formatUserOperationCell(row: UserInfo, ctx: Parameters<typeof buildUserRowActions>[1]) {
  const actions = buildUserRowActions(row, ctx);
  return renderTableOperationCell(actions, {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1 user-table-actions",
  });
}

const dataFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const userFormRenderKey = ref(0);
const submitLoading = ref(false);
const uploadLoading = ref(false);
const deptFilterId = ref<string | number | undefined>(undefined);

const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "450px" : "90%"));
const deptOptions = ref<OptionType[]>();
const roleOptions = ref<Array<{ value: number; label: string; disabled?: boolean }>>();
const positionOptions = ref<Array<{ value: number; label: string; disabled?: boolean }>>();
const { importVisible, exportVisible, openImport, openExport } = useImportExport();
const detailFormData = ref<UserInfo>({});

// 用户详情描述项配置 —— 数据驱动 + 关键字段用具名插槽覆盖
const userDetailItems: DescriptionsItem[] = [
  { label: "编号", prop: "id" },
  { label: "头像", prop: "avatar", slot: "avatar" }, // 自定义插槽渲染
  { label: "账号", prop: "username" },
  { label: "用户名", prop: "name" },
  { label: "性别", prop: "gender", slot: "gender" }, // 三种状态 Tag
  { label: "部门", prop: "dept.name" }, // 嵌套属性 a.b.c
  { label: "角色", prop: "roles", slot: "roles" }, // 数组 join 渲染
  { label: "岗位", prop: "positions", slot: "positions" }, // 数组 join 渲染
  { label: "邮箱", prop: "email" },
  { label: "手机号", prop: "mobile" },
  {
    label: "是否超管",
    prop: "is_superuser",
    tag: {
      map: { true: { type: "success", text: "是" }, false: { type: "info", text: "否" } },
    },
  },
  {
    label: "状态",
    prop: "status",
    tag: {
      map: { "0": { type: "success", text: "启用" }, "1": { type: "danger", text: "停用" } },
    },
  },
  { label: "上次登录时间", prop: "last_login" },
  { label: "创建人", prop: "created_by.name" },
  { label: "更新人", prop: "updated_by.name" },
  { label: "创建时间", prop: "created_time" },
  { label: "更新时间", prop: "updated_time" },
  { label: "描述", prop: "description", span: 4 },
];

// 用户新增/编辑表单配置 —— 三个复杂字段（部门树、角色多选、岗位多选）用插槽渲染
const userDialogFormItems = computed<FormItem[]>(() => [
  {
    key: "username",
    label: "账号",
    type: "input",
    props: { placeholder: "请输入账号", disabled: !!formData.value.id },
  },
  { key: "name", label: "用户名", type: "input", props: { placeholder: "请输入用户名" } },
  {
    key: "gender",
    label: "性别",
    type: "select",
    props: {
      placeholder: "请选择性别",
      options: [
        { label: "男", value: "0" },
        { label: "女", value: "1" },
        { label: "未知", value: "2" },
      ],
    },
  },
  {
    key: "mobile",
    label: "手机号",
    type: "input",
    props: { placeholder: "请输入手机号码", maxlength: 11 },
  },
  {
    key: "email",
    label: "邮箱",
    type: "input",
    props: { placeholder: "请输入邮箱", maxlength: 50 },
  },
  { key: "dept_id", label: "部门", type: "input" /* 实际渲染由 #dept_id 插槽接管 */ },
  { key: "role_ids", label: "角色", type: "input" /* 实际渲染由 #role_ids 插槽接管 */ },
  { key: "position_ids", label: "岗位", type: "input" /* 实际渲染由 #position_ids 插槽接管 */ },
  {
    key: "password",
    label: "密码",
    type: "input",
    hidden: !!formData.value.id,
    props: { placeholder: "请输入密码", type: "password", showPassword: true, clearable: true },
  },
  { key: "is_superuser", label: "是否超管", type: "switch" },
  {
    key: "status",
    label: "状态",
    type: "radiogroup",
    props: {
      options: [
        { label: "启用", value: "0" },
        { label: "停用", value: "1" },
      ],
    },
  },
  {
    key: "description",
    label: "描述",
    type: "input",
    props: {
      type: "textarea",
      rows: 4,
      maxlength: 100,
      showWordLimit: true,
      placeholder: "请输入描述",
    },
  },
]);

const searchForm = ref<UserSearchForm>({
  username: undefined,
  name: undefined,
  status: undefined,
  created_id: undefined,
  created_time: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof FaSearchBar> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const statusOptions = ref([
  { label: "启用", value: "0" },
  { label: "停用", value: "1" },
]);

const userSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "账号",
    key: "username",
    type: "input",
    placeholder: "请输入账号",
    clearable: true,
    span: 6,
  },
  {
    label: "用户名",
    key: "name",
    type: "input",
    placeholder: "请输入用户名",
    clearable: true,
    span: 6,
  },
  {
    label: "状态",
    key: "status",
    type: "select",
    props: {
      placeholder: "请选择状态",
      options: statusOptions.value,
      clearable: true,
    },
    span: 6,
  },
  {
    label: "创建人",
    key: "created_id",
    type: "input",
    span: 6,
  },
  {
    label: "创建时间",
    key: "created_time",
    type: "datetimerange",
    span: 6,
    props: {
      type: "datetimerange",
      rangeSeparator: "至",
      startPlaceholder: "开始日期",
      endPlaceholder: "结束日期",
      format: "YYYY-MM-DD HH:mm:ss",
      valueFormat: "YYYY-MM-DD HH:mm:ss",
      style: { width: "100%" },
    },
  },
]);

const faTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const { selectedRows, selectedIds, batchDeleting, onTableSelectionChange } =
  useTableSelection<UserInfo>();

async function handleResetPassword(row: UserInfo) {
  try {
    const { value } = await ElMessageBox.prompt(
      `请输入用户【${row.username ?? ""}】的新密码`,
      "重置密码",
      { confirmButtonText: "确定", cancelButtonText: "取消" }
    );
    if (!value || value.length < 6) {
      ElMessage.warning("密码至少需要6位字符，请重新输入");
      return;
    }
    await UserAPI.resetUserPassword({ id: row.id!, password: value });
    ElMessage.success("密码已重置");
  } catch {
    // 用户取消
  }
}

async function deleteUserRow(id: number) {
  try {
    await confirmDelete();
    await UserAPI.deleteUser([id]);
    const idSet = [id];
    if (userStore.basicInfo.id && idSet.includes(userStore.basicInfo.id)) {
      userStore.clearUserInfo();
    } else {
      ElMessage.success("删除成功");
    }
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  }
}

const opCtx = {
  onResetPwd: handleResetPassword,
  onDetail: (id: number) => void handleOpenDialog("detail", id),
  onEdit: (id: number) => void handleOpenDialog("update", id),
  onDelete: deleteUserRow,
};

const {
  columns,
  columnChecks,
  data,
  loading,
  pagination,
  searchParams,
  getData,
  replaceSearchParams,
  resetSearchParams,
  handleSizeChange,
  handleCurrentChange,
  refreshData,
  refreshCreate,
  refreshUpdate,
  refreshRemove,
} = useTable({
  core: {
    apiFn: fetchUserTableList,
    apiParams: {
      page_no: 1,
      page_size: 20,
    },
    columnsFactory: (): import("@/types/component").ColumnOption<UserInfo>[] => [
      { type: "selection", width: 48, fixed: "left" },
      { type: "globalIndex", width: 56, label: "序号" },
      {
        prop: "avatar",
        label: "头像",
        width: 72,
        align: "center",
        formatter: (row: UserInfo) =>
          h(
            ElAvatar,
            {
              size: 28,
              src: row.avatar || undefined,
            },
            () => (!row.avatar ? h(UserFilled) : undefined)
          ),
      },
      { prop: "username", label: "账号", minWidth: 100, showOverflowTooltip: true },
      { prop: "name", label: "用户名", minWidth: 100, showOverflowTooltip: true },
      {
        prop: "status",
        label: "状态",
        width: 88,
        formatter: (row: UserInfo) =>
          h(ElTag, { type: row.status === "0" ? "success" : "danger" }, () =>
            row.status === "0" ? "启用" : "停用"
          ),
      },
      {
        prop: "dept",
        label: "部门",
        minWidth: 100,
        formatter: (row: UserInfo) => row.dept?.name ?? "—",
      },
      {
        prop: "gender",
        label: "性别",
        width: 88,
        formatter: (row: UserInfo) => {
          if (row.gender === "0") return h(ElTag, { type: "success" }, () => "男");
          if (row.gender === "1") return h(ElTag, { type: "warning" }, () => "女");
          return h(ElTag, { type: "info" }, () => "未知");
        },
      },
      { prop: "created_time", label: "创建时间", width: 168, showOverflowTooltip: true },
      { prop: "updated_time", label: "更新时间", width: 168, showOverflowTooltip: true },
      {
        prop: "operation",
        label: "操作",
        width: 280,
        fixed: "right",
        align: "right",
        formatter: (row: UserInfo) => formatUserOperationCell(row, opCtx),
      },
    ],
  },
});

const userCrudCols = computed(() =>
  columns.value.map((c: ColumnOption<UserInfo>) => {
    const t = (c as { type?: string }).type;
    return {
      prop: c.prop,
      label: c.label,
      type: t === "selection" ? ("selection" as const) : ("default" as const),
      show: true,
    };
  })
);

const exportQueryParams = computed(() => {
  const sp = stripPaginationParams(searchParams);
  if (
    deptFilterId.value !== undefined &&
    deptFilterId.value !== null &&
    deptFilterId.value !== ""
  ) {
    (sp as Record<string, unknown>).dept_id = Number(deptFilterId.value);
  }
  const q = cleanEmptyArrayParams(sp) as Record<string, unknown>;
  if (typeof q.status === "string") {
    const s = q.status;
    if (s === "true" || s === "false") {
      q.status = s === "true";
    }
  }
  return q;
});

const userImportContentConfig = computed<IContentConfig>(() => ({
  permPrefix: "module_system:user",
  cols: userCrudCols.value,
  indexAction: async () => ({}),
  importTemplate: () => UserAPI.downloadTemplateUser(),
}));

const userExportContentConfig = computed(() => ({
  permPrefix: "module_system:user",
  cols: userCrudCols.value,
  exportsBlobAction: async (params: IObject) => {
    const merged = cleanEmptyArrayParams({
      ...(exportQueryParams.value as Record<string, unknown>),
      ...params,
    } as Record<string, unknown>) as Record<string, unknown>;
    if (typeof merged.status === "string") {
      const s = merged.status;
      if (s === "true" || s === "false") {
        merged.status = s === "true";
      }
    }
    const res = await UserAPI.exportUser(merged as unknown as UserPageQuery);
    return res.data as Blob;
  },
}));

const formData = ref<UserForm>({
  id: undefined,
  username: undefined,
  name: undefined,
  dept_id: undefined,
  dept_name: undefined,
  role_ids: undefined,
  role_names: undefined,
  position_ids: undefined,
  position_names: undefined,
  password: undefined,
  gender: undefined,
  email: undefined,
  mobile: undefined,
  is_superuser: false,
  status: "0",
  description: undefined,
});

const { dialogVisible } = useCrudDialog();

const rules = reactive({
  username: [{ required: true, message: "请输入账号", trigger: "blur" }],
  name: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }],
  gender: [{ required: false, message: "请选择性别", trigger: "blur" }],
  email: [
    {
      pattern: /\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}/,
      message: "请输入正确的邮箱地址",
      trigger: "blur",
    },
  ],
  mobile: [
    {
      pattern: /^1[3|4|5|6|7|8|9][0-9]\d{8}$/,
      message: "请输入正确的手机号码",
      trigger: "blur",
    },
  ],
  is_superuser: [{ required: true, message: "请选择是否超管", trigger: "blur" }],
  status: [{ required: true, message: "请选择状态", trigger: "blur" }],
});

const initialFormData: UserForm = {
  id: undefined,
  username: undefined,
  name: undefined,
  dept_id: undefined,
  dept_name: undefined,
  role_ids: undefined,
  role_names: undefined,
  position_ids: undefined,
  position_names: undefined,
  password: undefined,
  gender: undefined,
  email: undefined,
  mobile: undefined,
  is_superuser: false,
  status: "0",
  description: undefined,
};

async function handleSearchBarSearch(params: UserSearchForm) {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildUserReplaceParams(params));
  await getData();
}

async function applyUserSearchFromForm() {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildUserReplaceParams(searchForm.value));
  await getData();
}

async function afterUserSelectSearch() {
  await nextTick();
  await applyUserSearchFromForm();
}

function onResetSearch() {
  searchForm.value = {
    username: undefined,
    name: undefined,
    status: undefined,
    created_id: undefined,
    created_time: undefined,
  };
  deptFilterId.value = undefined;
  void resetSearchParams();
}

async function handleDeptNodeClick() {
  await getData();
}

async function handleImportUpload(formDataUpload: FormData) {
  uploadLoading.value = true;
  try {
    const response = await UserAPI.importUser(formDataUpload);
    if (response.data.code === ResultEnum.SUCCESS) {
      ElMessage.success(`${response.data.msg}，${response.data.data}`);
      importVisible.value = false;
      await refreshData();
    } else {
      ElMessage.error(response.data.msg || "导入失败");
    }
  } catch (error: unknown) {
    console.error(error);
    ElMessage.error("上传失败");
  } finally {
    uploadLoading.value = false;
  }
}

async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  Object.assign(formData.value, initialFormData);
}

async function handleCloseDialog() {
  dialogVisible.visible = false;
  await resetForm();
}

async function handleOpenDialog(type: "create" | "update" | "detail", id?: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await UserAPI.detailUser(id);
    if (type === "detail") {
      dialogVisible.title = "用户详情";
      Object.assign(detailFormData.value, response.data.data ?? {});
    } else if (type === "update") {
      dialogVisible.title = "修改用户";
      Object.assign(formData.value, response.data.data);
      formData.value.role_ids = (response.data.data.roles || []).map((item) => item.id as number);
      formData.value.position_ids = (response.data.data.positions || []).map(
        (item) => item.id as number
      );
    }
  } else {
    dialogVisible.title = "新增用户";
    Object.assign(formData.value, initialFormData);
    formData.value.id = undefined;
    userFormRenderKey.value += 1;
  }
  dialogVisible.visible = true;
  await nextTick();
  if (dataFormRef.value) {
    dataFormRef.value.clearValidate();
  }

  const deptResponse = await DeptAPI.listDept({});
  deptOptions.value = formatTree(deptResponse.data.data);

  const roleResponse = await RoleAPI.listRole();
  const roleRows = roleResponse.data.data.items ?? [];
  roleOptions.value = roleRows
    .filter((item) => item.id !== undefined && item.name !== undefined)
    .map((item) => ({
      value: item.id as number,
      label: item.name as string,
      disabled: item.status === "1",
    }))
    .filter((opt) => !opt.disabled);

  const positionResponse = await PositionAPI.listPosition();
  const positionRows = positionResponse.data.data.items ?? [];
  positionOptions.value = positionRows
    .filter((item) => item.id !== undefined && item.name !== undefined)
    .map((item) => ({
      value: item.id as number,
      label: item.name as string,
      disabled: item.status === "1",
    }))
    .filter((opt) => !opt.disabled);
}

async function handleSubmit() {
  dataFormRef.value?.validate(async (valid: boolean) => {
    if (!valid) return;
    submitLoading.value = true;
    const id = formData.value.id;
    try {
      if (id) {
        await UserAPI.updateUser(id, { id, ...formData.value });
        await refreshUpdate();
      } else {
        await UserAPI.createUser(formData.value);
        await refreshCreate();
      }
      dialogVisible.visible = false;
      await resetForm();
      if (id === userStore.basicInfo.id) {
        await userStore.getUserInfo();
      }
    } catch (error: unknown) {
      console.error(error);
    } finally {
      submitLoading.value = false;
    }
  });
}

async function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  try {
    await confirmBatchDelete(ids.length);
    batchDeleting.value = true;
    await UserAPI.deleteUser(ids);
    if (userStore.basicInfo.id && ids.includes(userStore.basicInfo.id)) {
      userStore.clearUserInfo();
    } else {
      ElMessage.success("删除成功");
    }
    selectedRows.value = [];
    await refreshRemove();
  } catch {
    // 用户取消
  } finally {
    batchDeleting.value = false;
  }
}

async function handleMoreClick(status: string) {
  const ids = selectedIds.value;
  if (!ids.length) {
    ElMessage.warning("请先选择要操作的数据");
    return;
  }
  try {
    await confirmToggleStatus(status);
    batchDeleting.value = true;
    await UserAPI.batchUser({ ids, status });
    await refreshData();
  } catch {
    // 用户取消
  } finally {
    batchDeleting.value = false;
  }
}
</script>

<style lang="scss" scoped>
/* 左侧部门树内容区：card body 纵向 flex + 滚动条占满剩余高度（布局在 index，内边距在 DeptTree） */
.tree-card :deep(.el-card__body) {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
  padding: 0;
}
</style>
