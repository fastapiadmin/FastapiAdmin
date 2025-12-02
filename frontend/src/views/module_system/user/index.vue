<!-- 用户管理 -->
<template>
  <div class="app-container">
    <el-row :gutter="12">
      <!-- 部门树 -->
      <el-col :lg="4" :xs="24">
        <DeptTree v-model="queryFormData.dept_id" class="h-full" @node-click="handleQuery" />
      </el-col>

      <!-- 用户列表 -->
      <el-col :lg="20" :xs="24">
        <!-- 搜索区域 -->
        <div class="search-container">
          <el-form
            ref="queryFormRef"
            :model="queryFormData"
            :inline="true"
            label-suffix=":"
            @submit.prevent="handleQuery"
          >
            <el-form-item prop="username" label="账号">
              <el-input v-model="queryFormData.username" placeholder="请输入账号" clearable />
            </el-form-item>
            <el-form-item prop="name" label="用户名">
              <el-input v-model="queryFormData.name" placeholder="请输入用户名" clearable />
            </el-form-item>
            <el-form-item prop="status" label="状态">
              <el-select
                v-model="queryFormData.status"
                placeholder="请选择状态"
                style="width: 167.5px"
                clearable
              >
                <el-option value="0" label="启用" />
                <el-option value="1" label="停用" />
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
                v-hasPerm="['module_system:user:query']"
                type="primary"
                icon="search"
                native-type="submit"
              >
                查询
              </el-button>
              <el-button
                v-hasPerm="['module_system:user:query']"
                icon="refresh"
                @click="handleResetQuery"
              >
                重置
              </el-button>
              <!-- 展开/收起 -->
              <template v-if="isExpandable">
                <el-link
                  class="ml-3"
                  type="primary"
                  underline="never"
                  @click="isExpand = !isExpand"
                >
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

        <el-card class="data-table">
          <template #header>
            <div class="card-header">
              <span>
                <el-tooltip content="用户管理系统用户">
                  <QuestionFilled class="w-4 h-4 mx-1" />
                </el-tooltip>
                用户列表
              </span>
            </div>
          </template>

          <!-- 功能区域 -->
          <div class="data-table__toolbar">
            <div class="data-table__toolbar--left">
              <el-row :gutter="10">
                <el-col :span="1.5">
                  <el-button
                    v-hasPerm="['module_system:user:create']"
                    type="success"
                    icon="plus"
                    @click="handleOpenDialog('create')"
                  >
                    新增
                  </el-button>
                </el-col>
                <el-col :span="1.5">
                  <el-button
                    v-hasPerm="['module_system:user:delete']"
                    type="danger"
                    icon="delete"
                    :disabled="selectIds.length === 0"
                    @click="handleDelete(selectIds)"
                  >
                    批量删除
                  </el-button>
                </el-col>
                <el-col :span="1.5">
                  <el-dropdown v-hasPerm="['module_system:user:patch']" trigger="click">
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
                  <el-tooltip content="导入">
                    <el-button
                      v-hasPerm="['module_system:user:import']"
                      type="info"
                      icon="upload"
                      circle
                      @click="handleOpenImportDialog"
                    />
                  </el-tooltip>
                </el-col>
                <el-col :span="1.5">
                  <el-tooltip content="导出">
                    <el-button
                      v-hasPerm="['module_system:user:export']"
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
                      v-hasPerm="['module_system:user:query']"
                      type="default"
                      icon="refresh"
                      circle
                      @click="handleRefresh"
                    />
                  </el-tooltip>
                </el-col>
              </el-row>
            </div>
          </div>

          <!-- 表格区域 -->
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
            <el-table-column type="selection" min-width="55" align="center" />
            <el-table-column type="index" fixed label="序号" min-width="60">
              <template #default="scope">
                {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
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
                  {{ scope.row.status === '0' ? "启用" : "停用" }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="是否超管" prop="is_superuser" min-width="100">
              <template #default="scope">
                <el-tag :type="scope.row.is_superuser ? 'success' : 'info'">
                  {{ scope.row.is_superuser ? "是" : "否" }}
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

            <el-table-column label="手机号" prop="mobile" min-width="160" />
            <el-table-column label="邮箱" prop="email" min-width="160" />
            <el-table-column label="创建时间" prop="created_time" min-width="200" />
            <el-table-column label="更新时间" prop="updated_time" min-width="200" />
            <el-table-column label="创建人" prop="created_id" min-width="120">
              <template #default="scope">
                {{ scope.row.created_by?.name }}
              </template>
            </el-table-column>
            <el-table-column label="更新人" prop="updated_id" min-width="120">
              <template #default="scope">
                {{ scope.row.updated_by?.name }}
              </template>
            </el-table-column>
            <el-table-column fixed="right" label="操作" align="center" min-width="280">
              <template #default="scope">
                <el-button
                  v-hasPerm="['module_system:user:update']"
                  type="warning"
                  icon="RefreshLeft"
                  size="small"
                  link
                  :disabled="scope.row.is_superuser === true"
                  @click="
                    scope.row.is_superuser === true
                      ? ElMessage.warning('系统超管角色，不可操作')
                      : hancleResetPassword(scope.row)
                  "
                >
                  重置密码
                </el-button>
                <el-button
                  v-hasPerm="['module_system:user:detail']"
                  type="info"
                  size="small"
                  link
                  icon="document"
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
                  @click="
                    scope.row.is_superuser === true
                      ? ElMessage.warning('系统超管角色，不可操作')
                      : handleOpenDialog('update', scope.row.id)
                  "
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
                  @click="
                    scope.row.is_superuser === true
                      ? ElMessage.warning('系统超管角色，不可操作')
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
      </el-col>
    </el-row>

    <!-- 弹窗区域 -->
    <el-drawer
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      append-to-body
      :size="drawerSize"
      @close="handleCloseDialog"
    >
      <!-- 详情 -->
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
            <el-tag :type="detailFormData.status ? 'success' : 'danger'">
              {{ detailFormData.status ? "启用" : "停用" }}
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

          <el-form-item label="密码" prop="password">
            <el-input
              v-model="formData.password"
              :readonly="!!formData.id"
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
          <el-button
            v-if="dialogVisible.type === 'create' || dialogVisible.type === 'update'"
            type="primary"
            @click="handleSubmit"
          >
            确定
          </el-button>
          <el-button v-else type="primary" @click="handleCloseDialog">确定</el-button>
          <el-button @click="handleCloseDialog">取消</el-button>
        </div>
      </template>
    </el-drawer>

    <!-- 导入弹窗 -->
    <ImportModal
      v-model="importDialogVisible"
      :content-config="curdContentConfig"
      @upload="handleUpload"
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
import { formatToDateTime } from "@/utils/dateUtil";

import DeptTree from "./components/DeptTree.vue";
import UserTableSelect from "./components/UserTableSelect.vue";
import { useUserStore } from "@/store";
import ImportModal from "@/components/CURD/ImportModal.vue";
import ExportModal from "@/components/CURD/ExportModal.vue";
import type { IContentConfig } from "@/components/CURD/types";
import { QuestionFilled, ArrowUp, ArrowDown } from "@element-plus/icons-vue";

const appStore = useAppStore();

const queryFormRef = ref();
const dataFormRef = ref();
const total = ref(0);
const loading = ref(false);
const isExpand = ref(false);
const isExpandable = ref(true);
const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "450px" : "90%"));
const selectionRows = ref<UserInfo[]>([]);
// 选中的用户ID
const selectIds = ref<number[]>([]);
// 部门下拉数据源
const deptOptions = ref<OptionType[]>();
// 角色下拉数据源
const roleOptions = ref<Array<{ value: number; label: string; disabled?: boolean }>>();
// 岗位下拉数据源
const positionOptions = ref<Array<{ value: number; label: string; disabled?: boolean }>>();
// 导入弹窗显示状态
const importDialogVisible = ref(false);
// 导出弹窗显示状态
const exportsDialogVisible = ref(false);
// 分页表单
const pageTableData = ref<UserInfo[]>([]);
// 详情表单
const detailFormData = ref<UserInfo>({});

// 分页查询参数
const queryFormData = reactive<UserPageQuery>({
  page_no: 1,
  page_size: 10,
  username: undefined,
  name: undefined,
  status: undefined,
  dept_id: undefined,
  created_time: undefined,
  created_id: undefined,
  updated_id: undefined,
});

// 表单
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
  is_superuser: false, //默认不是超管
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

// 日期范围临时变量
const dateRange = ref<[Date, Date] | []>([]);

// 仅用于导出字段的列（排除非数据列及嵌套对象列）
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

// 导入/导出配置
const curdContentConfig = {
  permPrefix: "module_system:user",
  cols: exportColumns as any,
  importTemplate: () => UserAPI.downloadTemplateUser(),
  exportsAction: async (params: any) => {
    const query: any = { ...params };
    if (typeof query.status === "string") {
      query.status = query.status === "true";
    }
    query.page_no = 1;
    query.page_size = 9999;
    const all: any[] = [];
    while (true) {
      const res = await UserAPI.listUser(query);
      const items = res.data?.data?.items || [];
      const total = res.data?.data?.total || 0;
      all.push(...items);
      if (all.length >= total || items.length === 0) break;
      query.page_no += 1;
    }
    return all;
  },
} as unknown as IContentConfig;

// 选择创建人后触发查询
function handleConfirm() {
  handleQuery();
}

// 处理日期范围变化
function handleDateRangeChange(range: [Date, Date]) {
  dateRange.value = range;
  if (range && range.length === 2) {
    queryFormData.created_time = [formatToDateTime(range[0]), formatToDateTime(range[1])];
  } else {
    queryFormData.created_time = undefined;
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
    const response = await UserAPI.listUser(queryFormData);
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
  // 重置表单字段
  queryFormRef.value.resetFields();
  // 额外清空不在 model 内的扩展查询项（如日期范围）
  dateRange.value = [];
  queryFormData.created_time = undefined;
  // 清空部门并重置页码
  queryFormData.dept_id = undefined;
  // 清空创建人
  queryFormData.created_id = undefined;
  queryFormData.page_no = 1;
  // 重新加载数据
  loadingData();
}

// 定义初始表单数据常量
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
  is_superuser: false, //默认不是超管
  status: '0',
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

// 选中项发生变化
async function handleSelectionChange(selection: any) {
  selectIds.value = selection.map((item: any) => item.id);
  selectionRows.value = selection;
}

// 重置密码
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

// 关闭弹窗
async function handleCloseDialog() {
  dialogVisible.visible = false;
  resetForm();
}

// 打开弹窗
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
      // 确保角色和岗位ID正确设置
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

  // 获取部门树
  const deptResponse = await DeptAPI.listDept(queryFormData);
  const treeData = deptResponse.data.data;
  deptOptions.value = formatTree(treeData);

  // 获取角色列表
  const roleResponse = await RoleAPI.listRole();
  roleOptions.value = roleResponse.data.data.items
    .filter((item) => item.id !== undefined && item.name !== undefined)
    .map((item) => ({
      value: item.id as number,
      label: item.name as string,
      disabled: item.status === "1",
    }))
    .filter((opt) => !opt.disabled);

  // 获取岗位列表
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

// 提交表单（防抖）
async function handleSubmit() {
  // 表单校验
  dataFormRef.value.validate(async (valid: any) => {
    if (valid) {
      loading.value = true;
      // 根据弹窗传入的参数(deatil\create\update)判断走什么逻辑
      const id = formData.id;
      try {
        if (id) {
          await UserAPI.updateUser(id, { id, ...formData });
        } else {
          await UserAPI.createUser(formData);
        }
        dialogVisible.visible = false;
        resetForm();
        handleResetQuery();
        // 如果当前编辑的是登录用户，更新全局用户状态
        const userStore = useUserStore();
        if (id === userStore.basicInfo.id) {
          await userStore.getUserInfo();
        }
      } catch (error: any) {
        console.error(error);
      } finally {
        loading.value = false;
      }
    }
  });
}

// 导出已改为通过导出弹窗 ExportModal 统一处理

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
        await UserAPI.deleteUser(ids);
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

// 批量启用/停用
async function handleMoreClick(status: string) {
  if (selectIds.value.length) {
    ElMessageBox.confirm("确认启用或停用该项数据?", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    })
      .then(async () => {
        try {
          loading.value = true;
          await UserAPI.batchUser({ ids: selectIds.value, status });
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

// 打开导入弹窗
function handleOpenImportDialog() {
  importDialogVisible.value = true;
}

// 打开导出弹窗
function handleOpenExportsModal() {
  exportsDialogVisible.value = true;
}

const emit = defineEmits(["import-success"]);

// 上传文件
const handleUpload = async (formData: FormData) => {
  try {
    const response = await UserAPI.importUser(formData);
    if (response.data.code === ResultEnum.SUCCESS) {
      ElMessage.success(`${response.data.msg}，${response.data.data}`);
      importDialogVisible.value = false;
      await handleQuery();
      emit("import-success");
    }
  } catch (error: any) {
    console.error(error);
    ElMessage.error("上传失败：" + error);
  }
};

onMounted(() => {
  handleQuery();
});
</script>
