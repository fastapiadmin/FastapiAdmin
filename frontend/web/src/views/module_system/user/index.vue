<!-- 用户管理：左部门树 + 右 Art 表格 -->
<template>
  <div class="art-full-height user-manage-page">
    <div
      class="user-manage-body box-border flex gap-4 h-full max-md:block max-md:gap-0 max-md:h-auto"
    >
      <div
        class="user-dept-panel flex-shrink-0 w-58 h-full max-md:w-full max-md:h-auto max-md:mb-5"
      >
        <ElCard class="tree-card art-card-xs flex flex-col h-full mt-0" shadow="hover">
          <template #header>
            <b>部门</b>
          </template>
          <ElScrollbar class="dept-tree-scroll min-h-0 flex-1">
            <DeptTree
              v-model="deptFilterId"
              class="dept-tree-inner"
              @node-click="handleDeptNodeClick"
            />
          </ElScrollbar>
        </ElCard>
      </div>

      <div class="user-main-panel flex flex-col flex-grow min-w-0 min-h-0">
        <ArtSearchBar
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
            <UserTableSelect
              :model-value="searchForm.created_id == null ? undefined : searchForm.created_id"
              @update:model-value="(v: number | undefined) => (searchForm.created_id = v)"
              @confirm-click="afterUserSelectSearch"
              @clear-click="afterUserSelectSearch"
            />
          </template>
        </ArtSearchBar>

        <ElCard class="art-table-card" :style="{ 'margin-top': showSearchBar ? '12px' : '0' }">
          <ArtTableHeader
            v-model:columns="columnChecks"
            v-model:showSearchBar="showSearchBar"
            :loading="loading"
            @refresh="refreshData"
          >
            <template #left>
              <ArtTableHeaderLeft
                :remove-ids="selectedIds"
                :perm-create="['module_system:user:create']"
                :perm-import="['module_system:user:import']"
                :perm-export="['module_system:user:export']"
                :perm-delete="['module_system:user:delete']"
                :perm-patch="['module_system:user:patch']"
                :import-loading="uploadLoading"
                :delete-loading="batchDeleting"
                @add="handleOpenDialog('create')"
                @import="openImportModal"
                @export="openExportModal"
                @delete="handleBatchDelete"
                @more="handleMoreClick"
              />
            </template>
          </ArtTableHeader>

          <ArtTable
            ref="artTableRef"
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

    <ArtDrawer
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      append-to-body
      :size="drawerSize"
      @close="handleCloseDialog"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <ElDescriptions :column="2" border>
          <ElDescriptionsItem label="编号" :span="2">
            {{ detailFormData.id }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="头像" :span="2">
            <template v-if="detailFormData.avatar">
              <ElAvatar :src="detailFormData.avatar" size="small"></ElAvatar>
            </template>
            <template v-else>
              <ElAvatar icon="UserFilled" size="small"></ElAvatar>
            </template>
          </ElDescriptionsItem>
          <ElDescriptionsItem label="账号" :span="2">
            {{ detailFormData.username }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="用户名" :span="2">
            {{ detailFormData.name }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="性别" :span="2">
            <ElTag v-if="detailFormData.gender === '0'" type="success">男</ElTag>
            <ElTag v-else-if="detailFormData.gender === '1'" type="warning">女</ElTag>
            <ElTag v-else type="info">未知</ElTag>
          </ElDescriptionsItem>
          <ElDescriptionsItem label="部门" :span="2">
            {{ detailFormData.dept ? detailFormData.dept.name : "" }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="角色" :span="2">
            {{
              detailFormData.roles ? detailFormData.roles.map((item) => item.name).join("、") : ""
            }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="岗位" :span="2">
            {{
              detailFormData.positions
                ? detailFormData.positions.map((item) => item.name).join("、")
                : ""
            }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="邮箱" :span="2">
            {{ detailFormData.email }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="手机号" :span="2">
            {{ detailFormData.mobile }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="是否超管" :span="2">
            <ElTag :type="detailFormData.is_superuser ? 'success' : 'info'">
              {{ detailFormData.is_superuser ? "是" : "否" }}
            </ElTag>
          </ElDescriptionsItem>
          <ElDescriptionsItem label="状态" :span="2">
            <ElTag :type="detailFormData.status === '0' ? 'success' : 'danger'">
              {{ detailFormData.status === "0" ? "启用" : "停用" }}
            </ElTag>
          </ElDescriptionsItem>
          <ElDescriptionsItem label="上次登录时间" :span="2">
            {{ detailFormData.last_login }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="创建人" :span="2">
            {{ detailFormData.created_by?.name }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="更新人" :span="2">
            {{ detailFormData.updated_by?.name }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="创建时间" :span="2">
            {{ detailFormData.created_time }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="更新时间" :span="2">
            {{ detailFormData.updated_time }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="描述" :span="4">
            {{ detailFormData.description }}
          </ElDescriptionsItem>
        </ElDescriptions>
      </template>
      <template v-else>
        <ElForm
          ref="dataFormRef"
          :model="formData"
          :rules="rules"
          label-suffix=":"
          label-width="auto"
          label-position="right"
        >
          <ElFormItem label="账号" prop="username">
            <ElInput
              v-model="formData.username"
              :disabled="!!formData.id"
              placeholder="请输入账号"
            />
          </ElFormItem>

          <ElFormItem label="用户名" prop="name">
            <ElInput v-model="formData.name" placeholder="请输入用户名" />
          </ElFormItem>

          <ElFormItem label="性别" prop="gender">
            <ElSelect v-model="formData.gender" placeholder="请选择性别">
              <ElOption label="男" value="0" />
              <ElOption label="女" value="1" />
              <ElOption label="未知" value="2" />
            </ElSelect>
          </ElFormItem>

          <ElFormItem label="手机号" prop="mobile">
            <ElInput v-model="formData.mobile" placeholder="请输入手机号码" maxlength="11" />
          </ElFormItem>

          <ElFormItem label="邮箱" prop="email">
            <ElInput v-model="formData.email" placeholder="请输入邮箱" maxlength="50" />
          </ElFormItem>

          <ElFormItem label="部门" prop="dept_id">
            <ElTreeSelect
              v-model="formData.dept_id"
              placeholder="请选择上级部门"
              :data="deptOptions"
              :props="{ children: 'children', label: 'label', disabled: 'disabled' }"
              filterable
              check-strictly
              :render-after-expand="false"
            />
          </ElFormItem>

          <ElFormItem label="角色" prop="role_ids">
            <ElSelect v-model="formData.role_ids" multiple placeholder="请选择角色">
              <ElOption
                v-for="item in roleOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
                :disabled="item.disabled"
              />
            </ElSelect>
          </ElFormItem>

          <ElFormItem label="岗位" prop="position_ids">
            <ElSelect v-model="formData.position_ids" multiple placeholder="请选择岗位">
              <ElOption
                v-for="item in positionOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
                :disabled="item.disabled"
              />
            </ElSelect>
          </ElFormItem>

          <ElFormItem v-if="!formData.id" label="密码" prop="password">
            <ElInput
              v-model="formData.password"
              placeholder="请输入密码"
              type="password"
              show-password
              clearable
            />
          </ElFormItem>

          <ElFormItem label="是否超管" prop="is_superuser">
            <ElSwitch v-model="formData.is_superuser" />
          </ElFormItem>

          <ElFormItem label="状态" prop="status">
            <ElRadioGroup v-model="formData.status">
              <ElRadio value="0">启用</ElRadio>
              <ElRadio value="1">停用</ElRadio>
            </ElRadioGroup>
          </ElFormItem>

          <ElFormItem label="描述" prop="description">
            <ElInput
              v-model="formData.description"
              :rows="4"
              :maxlength="100"
              show-word-limit
              type="textarea"
              placeholder="请输入描述"
            />
          </ElFormItem>
        </ElForm>
      </template>

      <template #footer>
        <div class="dialog-footer">
          <ElButton @click="handleCloseDialog">取消</ElButton>
          <ElButton
            v-if="dialogVisible.type === 'create' || dialogVisible.type === 'update'"
            type="primary"
            :loading="submitLoading"
            @click="handleSubmit"
          >
            确定
          </ElButton>
          <ElButton v-else type="primary" @click="handleCloseDialog">确定</ElButton>
        </div>
      </template>
    </ArtDrawer>

    <ArtImportDialog
      v-model="importModalVisible"
      :content-config="userImportContentConfig"
      default-template-file-name="user_import_template.xlsx"
      :loading="uploadLoading"
      @upload="handleImportUpload"
    />

    <ArtExportDialog
      v-model="exportModalVisible"
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

import { h, ref, reactive, computed, nextTick } from "vue";
import { UserFilled } from "@element-plus/icons-vue";
import { useAppStore } from "@stores/modules/app.store";
import { DeviceEnum } from "@/enums/settings/device.enum";
import { ResultEnum } from "@/enums/api/result.enum";
import { useTable } from "@/hooks/core/useTable";
import ArtTable from "@/components/Core/tables/art-table/index.vue";
import ArtTableHeader from "@/components/Core/tables/art-table-header/index.vue";
import ArtTableHeaderLeft from "@/components/Core/tables/art-table-header-left/index.vue";
import ArtSearchBar from "@/components/Core/forms/art-search-bar/index.vue";
import type { SearchFormItem } from "@/components/Core/forms/art-search-bar/index.vue";
import ArtDrawer from "@/components/Core/modal/art-drawer/index.vue";
import ArtImportDialog from "@/components/Core/modal/art-import-dialog/index.vue";
import ArtExportDialog from "@/components/Core/modal/art-export-dialog/index.vue";
import type { IContentConfig, IObject } from "@/components/Core/modal/types";
import UserAPI, {
  type UserForm,
  type UserInfo,
  type UserPageQuery,
} from "@/api/module_system/user";
import { formatTree } from "@utils/common";
import PositionAPI from "@/api/module_system/position";
import DeptAPI from "@/api/module_system/dept";
import RoleAPI from "@/api/module_system/role";
import DeptTree from "./components/DeptTree.vue";
import UserTableSelect from "./components/UserTableSelect.vue";
import { useUserStore } from "@stores";
import { ElMessage, ElMessageBox, ElTag, ElAvatar } from "element-plus";
import { useAuth } from "@/hooks/core/useAuth";
import type { ColumnOption } from "@/types/component";
import { renderTableOperationCell, type TableOperationAction } from "@utils/table";

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

function normalizeUserQuery(params: Record<string, unknown>): UserPageQuery {
  const p = { ...params } as Record<string, unknown>;
  if (Array.isArray(p.created_time) && p.created_time.length === 0) p.created_time = undefined;
  return p as unknown as UserPageQuery;
}

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

const dataFormRef = ref();
const submitLoading = ref(false);
const uploadLoading = ref(false);
const batchDeleting = ref(false);
const deptFilterId = ref<string | number | undefined>(undefined);

const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "450px" : "90%"));
const deptOptions = ref<OptionType[]>();
const roleOptions = ref<Array<{ value: number; label: string; disabled?: boolean }>>();
const positionOptions = ref<Array<{ value: number; label: string; disabled?: boolean }>>();
const importModalVisible = ref(false);
const exportModalVisible = ref(false);
const detailFormData = ref<UserInfo>({});

const searchForm = ref<UserSearchForm>({
  username: undefined,
  name: undefined,
  status: undefined,
  created_id: undefined,
  created_time: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof ArtSearchBar> | null>(null);
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

const artTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const selectedRows = ref<UserInfo[]>([]);
const selectedIds = computed(() =>
  selectedRows.value.map((r) => r.id).filter((id): id is number => id != null && !Number.isNaN(id))
);

function onTableSelectionChange(rows: UserInfo[]) {
  selectedRows.value = rows;
}

function handleResetPassword(row: UserInfo) {
  ElMessageBox.prompt(`请输入用户【${row.username ?? ""}】的新密码`, "重置密码", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
  }).then(
    async ({ value }) => {
      if (!value || value.length < 6) {
        ElMessage.warning("密码至少需要6位字符，请重新输入");
        return;
      }
      await UserAPI.resetUserPassword({ id: row.id!, password: value });
      ElMessage.success("密码已重置");
    },
    () => {}
  );
}

function deleteUserRow(id: number) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await UserAPI.deleteUser([id]);
      const idSet = [id];
      if (userStore.basicInfo.id && idSet.includes(userStore.basicInfo.id)) {
        userStore.clearUserInfo();
      } else {
        ElMessage.success("删除成功");
      }
      artTableRef.value?.elTableRef?.clearSelection();
      await refreshRemove();
    })
    .catch(() => {});
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
  const sp = { ...(searchParams as object) } as Record<string, unknown>;
  delete sp.current;
  delete sp.size;
  delete sp.page_no;
  delete sp.page_size;
  if (
    deptFilterId.value !== undefined &&
    deptFilterId.value !== null &&
    deptFilterId.value !== ""
  ) {
    sp.dept_id = Number(deptFilterId.value);
  }
  const q = normalizeUserQuery(sp);
  if (typeof q.status === "string") {
    const s = q.status;
    if (s === "true" || s === "false") {
      (q as unknown as Record<string, unknown>).status = s === "true";
    }
  }
  return q as unknown as Record<string, unknown>;
});

const userImportContentConfig = computed<IContentConfig>(() => ({
  permPrefix: "module_system:user",
  cols: userCrudCols.value,
  indexAction: async () => ({}) as any,
  importTemplate: () => UserAPI.downloadTemplateUser(),
}));

const userExportContentConfig = computed(() => ({
  permPrefix: "module_system:user",
  cols: userCrudCols.value,
  exportsBlobAction: async (params: IObject) => {
    const merged = normalizeUserQuery({
      ...(exportQueryParams.value as Record<string, unknown>),
      ...params,
    } as Record<string, unknown>);
    if (typeof merged.status === "string") {
      const s = merged.status;
      if (s === "true" || s === "false") {
        (merged as unknown as Record<string, unknown>).status = s === "true";
      }
    }
    const res = await UserAPI.exportUser(merged as unknown as UserPageQuery);
    return res.data as Blob;
  },
}));

const formData = reactive<UserForm>({
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

const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

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

function openImportModal() {
  importModalVisible.value = true;
}

function openExportModal() {
  exportModalVisible.value = true;
}

function handleImportUpload(formDataUpload: FormData) {
  uploadLoading.value = true;
  UserAPI.importUser(formDataUpload)
    .then(async (response) => {
      if (response.data.code === ResultEnum.SUCCESS) {
        ElMessage.success(`${response.data.msg}，${response.data.data}`);
        importModalVisible.value = false;
        await refreshData();
      } else {
        ElMessage.error(response.data.msg || "导入失败");
      }
    })
    .catch((error: unknown) => {
      console.error(error);
      ElMessage.error("上传失败");
    })
    .finally(() => {
      uploadLoading.value = false;
    });
}

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
    const response = await UserAPI.detailUser(id);
    if (type === "detail") {
      dialogVisible.title = "用户详情";
      Object.assign(detailFormData.value, response.data.data ?? {});
    } else if (type === "update") {
      dialogVisible.title = "修改用户";
      Object.assign(formData, response.data.data);
      formData.role_ids = (response.data.data.roles || []).map((item) => item.id as number);
      formData.position_ids = (response.data.data.positions || []).map((item) => item.id as number);
    }
  } else {
    dialogVisible.title = "新增用户";
    formData.id = undefined;
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
  dataFormRef.value.validate(async (valid: boolean) => {
    if (!valid) return;
    submitLoading.value = true;
    const id = formData.id;
    try {
      if (id) {
        await UserAPI.updateUser(id, { id, ...formData });
        await refreshUpdate();
      } else {
        await UserAPI.createUser(formData);
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

function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  ElMessageBox.confirm(`确定删除选中的 ${ids.length} 条数据吗？`, "批量删除", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        batchDeleting.value = true;
        await UserAPI.deleteUser(ids);
        if (userStore.basicInfo.id && ids.includes(userStore.basicInfo.id)) {
          userStore.clearUserInfo();
        } else {
          ElMessage.success("删除成功");
        }
        selectedRows.value = [];
        await refreshRemove();
      } finally {
        batchDeleting.value = false;
      }
    })
    .catch(() => {});
}

function handleMoreClick(status: string) {
  const ids = selectedIds.value;
  if (!ids.length) {
    ElMessage.warning("请先选择要操作的数据");
    return;
  }
  ElMessageBox.confirm("确认启用或停用该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        batchDeleting.value = true;
        await UserAPI.batchUser({ ids, status });
        await refreshData();
      } catch (error: unknown) {
        console.error(error);
      } finally {
        batchDeleting.value = false;
      }
    })
    .catch(() => {});
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
