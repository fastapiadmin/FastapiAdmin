<!-- 用户管理 -->
<template>
  <div class="app-container">
    <el-row class="page-row" :gutter="12" justify="start">
      <el-col :span="4" class="dept-col">
        <DeptTree v-model="deptFilterId" class="w-full h-full" @node-click="handleDeptNodeClick" />
      </el-col>

      <el-col :span="20" class="right-col">
        <PageSearch
          ref="searchRef"
          :search-config="searchConfig"
          @query-click="handleQueryClick"
          @reset-click="handleResetClick"
        />

        <PageContent ref="contentRef" class="flex-1 min-h-0" :content-config="contentConfig">
          <template #toolbar="{ toolbarRight, onToolbar, removeIds, cols }">
            <CrudToolbarLeft
              :remove-ids="removeIds"
              :perm-create="['module_system:user:create']"
              :perm-delete="['module_system:user:delete']"
              :perm-patch="['module_system:user:patch']"
              :delete-loading="submitLoading"
              @add="handleOpenDialog('create')"
              @delete="onToolbar('delete')"
              @more="handleMoreClick"
            />
            <div class="data-table__toolbar--right">
              <CrudToolbarRight :buttons="toolbarRight" :cols="cols" :on-toolbar="onToolbar">
                <template #prepend>
                  <el-tooltip content="导入">
                    <el-button
                      v-hasPerm="['module_system:user:import']"
                      type="info"
                      icon="upload"
                      circle
                      @click="handleOpenImportDialog"
                    />
                  </el-tooltip>
                  <el-tooltip content="导出">
                    <el-button
                      v-hasPerm="['module_system:user:export']"
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
                <el-table-column type="selection" min-width="55" align="center" />
                <el-table-column fixed label="序号" min-width="60">
                  <template #default="scope">
                    {{ (pagination.currentPage - 1) * pagination.pageSize + scope.$index + 1 }}
                  </template>
                </el-table-column>
                <el-table-column label="头像" prop="avatar" min-width="80" align="center">
                  <template #default="scope">
                    <template v-if="scope.row.avatar">
                      <el-avatar size="small" :src="scope.row.avatar" />
                    </template>
                    <template v-else>
                      <el-avatar size="small" icon="UserFilled" />
                    </template>
                  </template>
                </el-table-column>
                <el-table-column label="账号" prop="username" min-width="100" />
                <el-table-column label="用户名" prop="name" min-width="100" />
                <el-table-column label="状态" prop="status" min-width="100">
                  <template #default="scope">
                    <el-tag :type="scope.row.status === '0' ? 'success' : 'danger'">
                      {{ scope.row.status === "0" ? "启用" : "停用" }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="部门" prop="dept" min-width="100">
                  <template #default="scope">
                    {{ scope.row.dept ? scope.row.dept.name : "" }}
                  </template>
                </el-table-column>
                <el-table-column label="性别" prop="gender" min-width="100">
                  <template #default="scope">
                    <el-tag v-if="scope.row.gender === '0'" type="success">男</el-tag>
                    <el-tag v-else-if="scope.row.gender === '1'" type="warning">女</el-tag>
                    <el-tag v-else type="info">未知</el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="创建时间" prop="created_time" min-width="160" />
                <el-table-column label="更新时间" prop="updated_time" min-width="160" />
                <el-table-column label="操作" fixed="right" align="center" min-width="280">
                  <template #default="scope">
                    <el-button
                      v-hasPerm="['module_system:user:update']"
                      type="warning"
                      icon="RefreshLeft"
                      size="small"
                      link
                      :disabled="scope.row.is_superuser === true"
                      @click="hancleResetPassword(scope.row)"
                    >
                      重置密码
                    </el-button>
                    <el-button
                      v-hasPerm="['module_system:user:detail']"
                      type="info"
                      size="small"
                      link
                      icon="View"
                      @click="handleOpenDialog('detail', scope.row.id)"
                    >
                      详情
                    </el-button>
                    <el-button
                      v-hasPerm="['module_system:user:update']"
                      type="primary"
                      size="small"
                      link
                      icon="edit"
                      :disabled="scope.row.is_superuser === true"
                      @click="handleOpenDialog('update', scope.row.id)"
                    >
                      编辑
                    </el-button>
                    <el-button
                      v-hasPerm="['module_system:user:delete']"
                      type="danger"
                      size="small"
                      link
                      icon="delete"
                      :disabled="scope.row.is_superuser === true"
                      @click="handleRowDelete(scope.row.id)"
                    >
                      删除
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </template>
        </PageContent>
      </el-col>
    </el-row>

    <EnhancedDrawer
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      append-to-body
      :size="drawerSize"
      @close="handleCloseDialog"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="编号" :span="2">
            {{ detailFormData.id }}
          </el-descriptions-item>
          <el-descriptions-item label="头像" :span="2">
            <template v-if="detailFormData.avatar">
              <el-avatar :src="detailFormData.avatar" size="small"></el-avatar>
            </template>
            <template v-else>
              <el-avatar icon="UserFilled" size="small"></el-avatar>
            </template>
          </el-descriptions-item>
          <el-descriptions-item label="账号" :span="2">
            {{ detailFormData.username }}
          </el-descriptions-item>
          <el-descriptions-item label="用户名" :span="2">
            {{ detailFormData.name }}
          </el-descriptions-item>
          <el-descriptions-item label="性别" :span="2">
            <el-tag v-if="detailFormData.gender === '0'" type="success">男</el-tag>
            <el-tag v-else-if="detailFormData.gender === '1'" type="warning">女</el-tag>
            <el-tag v-else type="info">未知</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="部门" :span="2">
            {{ detailFormData.dept ? detailFormData.dept.name : "" }}
          </el-descriptions-item>
          <el-descriptions-item label="角色" :span="2">
            {{
              detailFormData.roles ? detailFormData.roles.map((item) => item.name).join("、") : ""
            }}
          </el-descriptions-item>
          <el-descriptions-item label="岗位" :span="2">
            {{
              detailFormData.positions
                ? detailFormData.positions.map((item) => item.name).join("、")
                : ""
            }}
          </el-descriptions-item>
          <el-descriptions-item label="邮箱" :span="2">
            {{ detailFormData.email }}
          </el-descriptions-item>
          <el-descriptions-item label="手机号" :span="2">
            {{ detailFormData.mobile }}
          </el-descriptions-item>
          <el-descriptions-item label="是否超管" :span="2">
            <el-tag :type="detailFormData.is_superuser ? 'success' : 'info'">
              {{ detailFormData.is_superuser ? "是" : "否" }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态" :span="2">
            <el-tag :type="detailFormData.status === '0' ? 'success' : 'danger'">
              {{ detailFormData.status === "0" ? "启用" : "停用" }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="上次登录时间" :span="2">
            {{ detailFormData.last_login }}
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
      <template v-else>
        <el-form
          ref="dataFormRef"
          :model="formData"
          :rules="rules"
          label-suffix=":"
          label-width="auto"
          label-position="right"
        >
          <el-form-item label="账号" prop="username">
            <el-input
              v-model="formData.username"
              :disabled="!!formData.id"
              placeholder="请输入账号"
            />
          </el-form-item>

          <el-form-item label="用户名" prop="name">
            <el-input v-model="formData.name" placeholder="请输入用户名" />
          </el-form-item>

          <el-form-item label="性别" prop="gender">
            <el-select v-model="formData.gender" placeholder="请选择性别">
              <el-option label="男" value="0" />
              <el-option label="女" value="1" />
              <el-option label="未知" value="2" />
            </el-select>
          </el-form-item>

          <el-form-item label="手机号" prop="mobile">
            <el-input v-model="formData.mobile" placeholder="请输入手机号码" maxlength="11" />
          </el-form-item>

          <el-form-item label="邮箱" prop="email">
            <el-input v-model="formData.email" placeholder="请输入邮箱" maxlength="50" />
          </el-form-item>

          <el-form-item label="部门" prop="dept_id">
            <el-tree-select
              v-model="formData.dept_id"
              placeholder="请选择上级部门"
              :data="deptOptions"
              :props="{ children: 'children', label: 'label', disabled: 'disabled' }"
              filterable
              check-strictly
              :render-after-expand="false"
            />
          </el-form-item>

          <el-form-item label="角色" prop="role_ids">
            <el-select v-model="formData.role_ids" multiple placeholder="请选择角色">
              <el-option
                v-for="item in roleOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
                :disabled="item.disabled"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="岗位" prop="position_ids">
            <el-select v-model="formData.position_ids" multiple placeholder="请选择岗位">
              <el-option
                v-for="item in positionOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
                :disabled="item.disabled"
              />
            </el-select>
          </el-form-item>

          <el-form-item v-if="!formData.id" label="密码" prop="password">
            <el-input
              v-model="formData.password"
              placeholder="请输入密码"
              type="password"
              show-password
              clearable
            />
          </el-form-item>

          <el-form-item label="是否超管" prop="is_superuser">
            <el-switch v-model="formData.is_superuser" />
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
            v-if="dialogVisible.type === 'create' || dialogVisible.type === 'update'"
            type="primary"
            :loading="submitLoading"
            @click="handleSubmit"
          >
            确定
          </el-button>
          <el-button v-else type="primary" @click="handleCloseDialog">确定</el-button>
        </div>
      </template>
    </EnhancedDrawer>

    <ImportModal
      v-model="importDialogVisible"
      :content-config="curdContentConfig"
      :loading="uploadLoading"
      @upload="handleUpload"
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
  name: "User",
  inheritAttrs: false,
});

import { useAppStore } from "@/store/modules/app.store";
import { DeviceEnum } from "@/enums/settings/device.enum";
import { ResultEnum } from "@/enums/api/result.enum";

import UserAPI, {
  type UserForm,
  type UserInfo,
  type UserPageQuery,
} from "@/api/module_system/user";
import { formatTree } from "@/utils/common";
import PositionAPI from "@/api/module_system/position";
import DeptAPI from "@/api/module_system/dept";
import RoleAPI from "@/api/module_system/role";

import DeptTree from "./components/DeptTree.vue";
import UserTableSelect from "./components/UserTableSelect.vue";
import { useUserStore } from "@/store";
import ImportModal from "@/components/CURD/ImportModal.vue";
import ExportModal from "@/components/CURD/ExportModal.vue";
import CrudToolbarLeft from "@/components/CURD/CrudToolbarLeft.vue";
import CrudToolbarRight from "@/components/CURD/CrudToolbarRight.vue";
import PageSearch from "@/components/CURD/PageSearch.vue";
import PageContent from "@/components/CURD/PageContent.vue";
import EnhancedDrawer from "@/components/CURD/EnhancedDrawer.vue";
import type { IContentConfig, ISearchConfig } from "@/components/CURD/types";
import { ref, reactive, computed, markRaw, nextTick, unref } from "vue";
import { fetchAllPages } from "@/utils/fetchAllPages";

const appStore = useAppStore();

const searchRef = ref<InstanceType<typeof PageSearch>>();
const contentRef = ref<InstanceType<typeof PageContent>>();
const dataFormRef = ref();
const submitLoading = ref(false);
const uploadLoading = ref(false);
const deptFilterId = ref<number | undefined>(undefined);

const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "450px" : "90%"));
const deptOptions = ref<OptionType[]>();
const roleOptions = ref<Array<{ value: number; label: string; disabled?: boolean }>>();
const positionOptions = ref<Array<{ value: number; label: string; disabled?: boolean }>>();
const importDialogVisible = ref(false);
const exportsDialogVisible = ref(false);
const detailFormData = ref<UserInfo>({});

function triggerUserSearch() {
  nextTick(() => {
    contentRef.value?.fetchPageData(getMergedListParams(), true);
  });
}

const searchConfig = reactive<ISearchConfig>({
  permPrefix: "module_system:user",
  colon: true,
  isExpandable: true,
  showNumber: 3,
  form: { labelWidth: "auto" },
  formItems: [
    {
      prop: "username",
      label: "账号",
      type: "input",
      attrs: { placeholder: "请输入账号", clearable: true },
    },
    {
      prop: "name",
      label: "用户名",
      type: "input",
      attrs: { placeholder: "请输入用户名", clearable: true },
    },
    {
      prop: "status",
      label: "状态",
      type: "select",
      options: [
        { label: "启用", value: "0" },
        { label: "停用", value: "1" },
      ],
      attrs: { placeholder: "请选择状态", clearable: true, style: { width: "167.5px" } },
    },
    {
      prop: "created_id",
      label: "创建人",
      type: "user-table-select",
      initialValue: null,
      events: {
        "confirm-click": triggerUserSearch,
        "clear-click": triggerUserSearch,
      },
    },
  ],
  customComponents: {
    "user-table-select": markRaw(UserTableSelect),
  },
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
  { prop: "avatar", label: "头像", show: true },
  { prop: "username", label: "账号", show: true },
  { prop: "name", label: "用户名", show: true },
  { prop: "status", label: "状态", show: true },
  { prop: "dept", label: "部门", show: true },
  { prop: "gender", label: "性别", show: true },
  { prop: "created_time", label: "创建时间", show: true },
  { prop: "updated_time", label: "更新时间", show: true },
  { prop: "operation", label: "操作", show: true },
]);

const contentConfig = reactive<IContentConfig<UserPageQuery>>({
  permPrefix: "module_system:user",
  pk: "id",
  cols: contentCols as IContentConfig["cols"],
  hideColumnFilter: false,
  initialFetch: false,
  toolbar: [],
  defaultToolbar: ["refresh", "filter"],
  pagination: {
    pageSize: 10,
    pageSizes: [10, 20, 30, 50],
  },
  request: { page_no: "page_no", page_size: "page_size" },
  indexAction: async (params) => {
    const res = await UserAPI.listUser(params as UserPageQuery);
    return {
      total: res.data.data.total,
      list: res.data.data.items,
    };
  },
  deleteAction: async (ids) => {
    await UserAPI.deleteUser(
      ids
        .split(",")
        .map((s) => Number(s.trim()))
        .filter((n) => !Number.isNaN(n))
    );
    const userStore = useUserStore();
    const idSet = ids.split(",").map((s) => Number(s.trim()));
    if (userStore.basicInfo.id && idSet.includes(userStore.basicInfo.id)) {
      userStore.clearUserInfo();
    }
  },
  deleteConfirm: {
    title: "警告",
    message: "确认删除该项数据?",
    type: "warning",
  },
});

function getMergedListParams(): UserPageQuery {
  const base = searchRef.value?.getQueryParams() ?? {};
  return {
    ...base,
    dept_id: deptFilterId.value,
  } as UserPageQuery;
}

function handleQueryClick() {
  contentRef.value?.fetchPageData(getMergedListParams(), true);
}

function handleResetClick() {
  deptFilterId.value = undefined;
  contentRef.value?.fetchPageData(getMergedListParams(), true);
}

function handleDeptNodeClick() {
  contentRef.value?.fetchPageData(getMergedListParams(), true);
}

function refreshList() {
  contentRef.value?.fetchPageData(getMergedListParams(), true);
}

function handleRowDelete(id: number) {
  contentRef.value?.handleDelete(id);
}

const exportQueryParams = computed(() => getMergedListParams());

const exportPageData = computed(() => (unref(contentRef.value?.pageData) ?? []) as UserInfo[]);

const exportSelectionData = computed(
  () => (contentRef.value?.getSelectionData() ?? []) as UserInfo[]
);

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

const exportColumns = [
  { prop: "username", label: "账号" },
  { prop: "name", label: "名称" },
  { prop: "status", label: "状态" },
  { prop: "gender", label: "性别" },
  { prop: "email", label: "邮箱" },
  { prop: "mobile", label: "手机号" },
  { prop: "is_superuser", label: "是否超管" },
  { prop: "description", label: "描述" },
  { prop: "created_time", label: "创建时间" },
  { prop: "updated_time", label: "更新时间" },
];

const curdContentConfig = {
  permPrefix: "module_system:user",
  cols: exportColumns as unknown as IContentConfig["cols"],
  importTemplate: () => UserAPI.downloadTemplateUser(),
  exportsAction: async (params: Record<string, unknown>) => {
    const query: Record<string, unknown> = { ...params };
    if (typeof query.status === "string") {
      query.status = query.status === "true";
    }
    return fetchAllPages<UserInfo>({
      pageSize: 9999,
      initialQuery: query,
      fetchPage: async (q) => {
        const res = await UserAPI.listUser(q as unknown as UserPageQuery);
        return {
          total: res.data?.data?.total ?? 0,
          list: res.data?.data?.items ?? [],
        };
      },
    });
  },
} as unknown as IContentConfig;

function hancleResetPassword(row: UserInfo) {
  ElMessageBox.prompt("请输入用户【" + row.username + "】的新密码", "重置密码", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
  }).then(
    async ({ value }) => {
      if (!value || value.length < 6) {
        ElMessage.warning("密码至少需要6位字符，请重新输入");
        return false;
      }
      await UserAPI.resetUserPassword({ id: row.id!, password: value });
    },
    () => {
      ElMessageBox.close();
    }
  );
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

async function handleOpenDialog(type: "create" | "update" | "detail", id?: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await UserAPI.detailUser(id);
    if (type === "detail") {
      dialogVisible.title = "用户详情";
      Object.assign(detailFormData.value, response.data.data);
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
  roleOptions.value = roleResponse.data.data.items
    .filter((item) => item.id !== undefined && item.name !== undefined)
    .map((item) => ({
      value: item.id as number,
      label: item.name as string,
      disabled: item.status === "1",
    }))
    .filter((opt) => !opt.disabled);

  const positionResponse = await PositionAPI.listPosition();
  positionOptions.value = positionResponse.data.data.items
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
    if (valid) {
      submitLoading.value = true;
      const id = formData.id;
      try {
        if (id) {
          await UserAPI.updateUser(id, { id, ...formData });
        } else {
          await UserAPI.createUser(formData);
        }
        dialogVisible.visible = false;
        await resetForm();
        refreshList();
        const userStore = useUserStore();
        if (id === userStore.basicInfo.id) {
          await userStore.getUserInfo();
        }
      } catch (error: unknown) {
        console.error(error);
      } finally {
        submitLoading.value = false;
      }
    }
  });
}

async function handleMoreClick(status: string) {
  const rows = contentRef.value?.getSelectionData() as UserInfo[] | undefined;
  const ids = (rows ?? []).map((r) => r.id).filter((id): id is number => id != null);
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
        submitLoading.value = true;
        await UserAPI.batchUser({ ids, status });
        refreshList();
      } catch (error: unknown) {
        console.error(error);
      } finally {
        submitLoading.value = false;
      }
    })
    .catch(() => {
      ElMessageBox.close();
    });
}

function handleOpenImportDialog() {
  importDialogVisible.value = true;
}

function handleOpenExportsModal() {
  exportsDialogVisible.value = true;
}

const emit = defineEmits(["import-success"]);

const handleUpload = async (formDataUpload: FormData) => {
  try {
    uploadLoading.value = true;
    const response = await UserAPI.importUser(formDataUpload);
    if (response.data.code === ResultEnum.SUCCESS) {
      ElMessage.success(`${response.data.msg}，${response.data.data}`);
      importDialogVisible.value = false;
      await refreshList();
      emit("import-success");
    }
  } catch (error: unknown) {
    console.error(error);
    ElMessage.error("上传失败：" + error);
  } finally {
    uploadLoading.value = false;
  }
};

onMounted(() => {
  nextTick(() => {
    contentRef.value?.fetchPageData(getMergedListParams(), true);
  });
});
</script>

<style lang="scss" scoped>
.page-row {
  flex: 1;
  align-items: stretch;
  min-height: 0;
}

.dept-col {
  display: flex;
}

.right-col {
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.right-col :deep(.data-table) {
  flex: 1;
  min-height: 0;
}

.right-col :deep(.data-table__content) {
  min-height: 0;
}

.el-row {
  height: 100%;
}

.el-col {
  height: 100%;
}

.h-full {
  height: 100%;
}

.w-full {
  width: 100%;
}
</style>
