<!-- 演示示例：PageSearch + PageContent CRUD 封装 -->
<template>
  <div class="app-container">
    <PageSearch
      ref="searchRef"
      :search-config="searchConfig"
      @query-click="handleQueryClick"
      @reset-click="handleResetClick"
    />

    <PageContent
      ref="contentRef"
      :content-config="contentConfig"
      @search-click="handleToggleSearch"
      @add-click="handleOpenDialog('create')"
    >
      <!-- 与 PageContent 默认结构一致：不再套一层 data-table__toolbar（外层已由组件提供） -->
      <template #toolbar="{ toolbarRight, onToolbar, removeIds, cols }">
        <CrudToolbarLeft
          :remove-ids="removeIds"
          :perm-create="['module_example:demo:create']"
          :perm-delete="['module_example:demo:delete']"
          :perm-patch="['module_example:demo:patch']"
          @add="handleOpenDialog('create')"
          @delete="onToolbar('delete')"
          @more="handleMoreClick"
        />
        <div class="data-table__toolbar--right">
          <CrudToolbarRight :buttons="toolbarRight" :cols="cols" :on-toolbar="onToolbar" />
        </div>
      </template>

      <template #table="{ data, loading, tableRef, onSelectionChange, pagination }">
        <div class="data-table__content">
          <el-table
            :ref="tableRef as any"
            v-loading="loading"
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
              min-width="55"
              align="center"
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'index')?.show"
              fixed
              label="序号"
              min-width="60"
            >
              <template #default="scope">
                {{ (pagination.currentPage - 1) * pagination.pageSize + scope.$index + 1 }}
              </template>
            </el-table-column>
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'name')?.show"
              label="名称"
              prop="name"
              min-width="140"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'uuid')?.show"
              label="UUID"
              prop="uuid"
              min-width="180"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'status')?.show"
              label="状态"
              prop="status"
              min-width="120"
              show-overflow-tooltip
            >
              <template #default="scope">
                <el-tag :type="scope.row.status ? 'success' : 'info'">
                  {{ scope.row.status ? "启用" : "停用" }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'a')?.show"
              label="整数"
              prop="a"
              min-width="100"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'b')?.show"
              label="大整数"
              prop="b"
              min-width="120"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'c')?.show"
              label="浮点数"
              prop="c"
              min-width="100"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'd')?.show"
              label="布尔值"
              prop="d"
              min-width="100"
              show-overflow-tooltip
            >
              <template #default="scope">
                <el-tag :type="scope.row.d ? 'success' : 'danger'">
                  {{ scope.row.d ? "是" : "否" }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'e')?.show"
              label="日期"
              prop="e"
              min-width="120"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'f')?.show"
              label="时间"
              prop="f"
              min-width="120"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'g')?.show"
              label="日期时间"
              prop="g"
              min-width="180"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'h')?.show"
              label="长文本"
              prop="h"
              min-width="140"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'description')?.show"
              label="描述"
              prop="description"
              min-width="140"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'created_time')?.show"
              label="创建时间"
              prop="created_time"
              min-width="180"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'updated_time')?.show"
              label="更新时间"
              prop="updated_time"
              min-width="180"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'created_id')?.show"
              label="创建人"
              prop="created_id"
              min-width="120"
              show-overflow-tooltip
            >
              <template #default="scope">
                <el-tag>{{ scope.row.created_by?.name }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'updated_id')?.show"
              label="更新人"
              prop="updated_id"
              min-width="120"
              show-overflow-tooltip
            >
              <template #default="scope">
                <el-tag>{{ scope.row.updated_by?.name }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'operation')?.show"
              fixed="right"
              label="操作"
              align="center"
              min-width="200"
            >
              <template #default="scope">
                <el-button
                  v-hasPerm="['module_example:demo:detail']"
                  type="info"
                  size="small"
                  link
                  icon="View"
                  @click="handleOpenDialog('detail', scope.row.id)"
                >
                  详情
                </el-button>
                <el-button
                  v-hasPerm="['module_example:demo:update']"
                  type="primary"
                  size="small"
                  link
                  icon="edit"
                  @click="handleOpenDialog('update', scope.row.id)"
                >
                  编辑
                </el-button>
                <el-button
                  v-hasPerm="['module_example:demo:delete']"
                  type="danger"
                  size="small"
                  link
                  icon="delete"
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

    <EnhancedDialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      width="920px"
      @close="handleCloseDialog"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <el-descriptions :column="4" border>
          <el-descriptions-item label="名称" :span="2">
            {{ detailFormData.name }}
          </el-descriptions-item>
          <el-descriptions-item label="UUID" :span="2">
            {{ detailFormData.uuid }}
          </el-descriptions-item>
          <el-descriptions-item label="状态" :span="2">
            <el-tag :type="detailFormData.status == '0' ? 'success' : 'danger'">
              {{ detailFormData.status == "0" ? "启用" : "停用" }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="整数" :span="2">
            {{ detailFormData.a }}
          </el-descriptions-item>
          <el-descriptions-item label="大整数" :span="2">
            {{ detailFormData.b }}
          </el-descriptions-item>
          <el-descriptions-item label="浮点数" :span="2">
            {{ detailFormData.c }}
          </el-descriptions-item>
          <el-descriptions-item label="布尔值" :span="2">
            <el-tag :type="detailFormData.d ? 'success' : 'danger'">
              {{ detailFormData.d ? "是" : "否" }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="日期" :span="2">
            {{ detailFormData.e }}
          </el-descriptions-item>
          <el-descriptions-item label="时间" :span="2">
            {{ detailFormData.f }}
          </el-descriptions-item>
          <el-descriptions-item label="日期时间" :span="2">
            {{ detailFormData.g }}
          </el-descriptions-item>
          <el-descriptions-item label="长文本" :span="2">
            {{ detailFormData.h }}
          </el-descriptions-item>
          <el-descriptions-item label="元数据" :span="2">
            <JsonPretty :value="detailFormData.i" height="140px" />
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">
            {{ detailFormData.description }}
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
          inline
        >
          <el-form-item label="名称" prop="name">
            <el-input v-model="formData.name" placeholder="请输入名称" :maxlength="50" />
          </el-form-item>
          <el-form-item label="状态" prop="status">
            <el-radio-group v-model="formData.status">
              <el-radio value="0">启用</el-radio>
              <el-radio value="1">停用</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="整数" prop="a">
            <el-input-number v-model="formData.a" placeholder="请输入整数" />
          </el-form-item>
          <el-form-item label="大整数" prop="b">
            <el-input-number v-model="formData.b" placeholder="请输入大整数" />
          </el-form-item>
          <el-form-item label="浮点数" prop="c">
            <el-input-number
              v-model="formData.c"
              placeholder="请输入浮点数"
              :step="0.01"
              :precision="2"
            />
          </el-form-item>
          <el-form-item label="布尔值" prop="d">
            <el-switch v-model="formData.d" />
          </el-form-item>
          <el-form-item label="日期" prop="e">
            <el-date-picker
              v-model="formData.e"
              type="date"
              placeholder="请选择日期"
              style="width: 100%"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
          <el-form-item label="时间" prop="f">
            <el-time-picker
              v-model="formData.f"
              placeholder="请选择时间"
              style="width: 100%"
              value-format="HH:mm:ss"
            />
          </el-form-item>
          <el-form-item label="日期时间" prop="g">
            <el-date-picker
              v-model="formData.g"
              type="datetime"
              placeholder="请选择日期时间"
              style="width: 100%"
              value-format="YYYY-MM-DD HH:mm:ss"
            />
          </el-form-item>
          <el-form-item label="长文本" prop="h">
            <el-input v-model="formData.h" :rows="4" type="textarea" placeholder="请输入长文本" />
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
          <el-form-item label="元数据" prop="i">
            <div class="flex flex-col gap-2">
              <div
                v-for="(item, index) in metadataList"
                :key="index"
                class="flex items-center gap-2"
              >
                <el-input v-model="item.key" placeholder="键" />
                <el-input v-model="item.value" placeholder="值" />
                <el-button
                  type="primary"
                  icon="Plus"
                  circle
                  @click="metadataList.push({ key: '', value: '' })"
                />
                <el-button
                  type="danger"
                  icon="Delete"
                  circle
                  @click="metadataList.splice(index, 1)"
                />
              </div>
              <el-button
                v-if="metadataList.length === 0"
                type="primary"
                icon="Plus"
                @click="metadataList.push({ key: '', value: '' })"
              >
                添加元数据
              </el-button>
            </div>
          </el-form-item>
        </el-form>
      </template>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleCloseDialog">取消</el-button>
          <el-button v-if="dialogVisible.type !== 'detail'" type="primary" @click="handleSubmit">
            确定
          </el-button>
          <el-button v-else type="primary" @click="handleCloseDialog">确定</el-button>
        </div>
      </template>
    </EnhancedDialog>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "Demo",
  inheritAttrs: false,
});

import { ref, reactive, onMounted, markRaw, nextTick } from "vue";
import { fetchAllPages } from "@/utils/fetchAllPages";
import { ElMessageBox } from "element-plus";
import { ResultEnum } from "@/enums/api/result.enum";
import DemoAPI, { DemoTable, DemoForm, DemoPageQuery } from "@/api/module_example/demo";
import CrudToolbarLeft from "@/components/CURD/CrudToolbarLeft.vue";
import CrudToolbarRight from "@/components/CURD/CrudToolbarRight.vue";
import PageSearch from "@/components/CURD/PageSearch.vue";
import PageContent from "@/components/CURD/PageContent.vue";
import EnhancedDialog from "@/components/CURD/EnhancedDialog.vue";
import { useCrudList } from "@/components/CURD/useCrudList";
import UserTableSelect from "@/views/module_system/user/components/UserTableSelect.vue";
import type { IContentConfig, ISearchConfig } from "@/components/CURD/types";
import JsonPretty from "@/components/JsonPretty/index.vue";

const { searchRef, contentRef, handleQueryClick, handleResetClick, refreshList } = useCrudList();

function triggerUserSearch() {
  nextTick(() => refreshList());
}

const searchConfig = reactive<ISearchConfig>({
  permPrefix: "module_example:demo",
  colon: true,
  isExpandable: true,
  showNumber: 2,
  showToggle: false,
  form: { labelWidth: "auto" },
  formItems: [
    {
      prop: "name",
      label: "名称",
      type: "input",
      attrs: { placeholder: "请输入名称", clearable: true },
    },
    {
      prop: "status",
      label: "状态",
      type: "select",
      options: [
        { label: "启用", value: "0" },
        { label: "停用", value: "1" },
      ],
      attrs: { placeholder: "请选择状态", clearable: true, style: { width: "170px" } },
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
    {
      prop: "updated_id",
      label: "更新人",
      type: "user-table-select",
      initialValue: null,
      events: {
        "confirm-click": triggerUserSearch,
        "clear-click": triggerUserSearch,
      },
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
        startPlaceholder: "开始",
        endPlaceholder: "结束",
      },
    },
    {
      prop: "updated_time",
      label: "更新时间",
      type: "date-picker",
      initialValue: [],
      attrs: {
        type: "datetimerange",
        valueFormat: "YYYY-MM-DD HH:mm:ss",
        rangeSeparator: "至",
        startPlaceholder: "开始",
        endPlaceholder: "结束",
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
  { prop: "name", label: "名称", show: true },
  { prop: "uuid", label: "UUID", show: true },
  { prop: "status", label: "状态", show: true },
  { prop: "a", label: "整数", show: true },
  { prop: "b", label: "大整数", show: true },
  { prop: "c", label: "浮点数", show: true },
  { prop: "d", label: "布尔值", show: true },
  { prop: "e", label: "日期", show: true },
  { prop: "f", label: "时间", show: true },
  { prop: "g", label: "日期时间", show: true },
  { prop: "h", label: "长文本", show: true },
  { prop: "i", label: "元数据", show: true },
  { prop: "description", label: "描述", show: true },
  { prop: "created_time", label: "创建时间", show: true },
  { prop: "updated_time", label: "更新时间", show: true },
  { prop: "created_id", label: "创建人", show: true },
  { prop: "updated_id", label: "更新人", show: true },
  { prop: "operation", label: "操作", show: true },
]);

function normalizeDemoQuery(params: Record<string, unknown>) {
  const p = { ...params } as Record<string, unknown>;
  if (Array.isArray(p.created_time) && p.created_time.length === 0) p.created_time = undefined;
  if (Array.isArray(p.updated_time) && p.updated_time.length === 0) p.updated_time = undefined;
  return p as unknown as DemoPageQuery;
}

const contentConfig = reactive<IContentConfig<DemoPageQuery>>({
  permPrefix: "module_example:demo",
  hideColumnFilter: false,
  initialFetch: false,
  cols: contentCols as IContentConfig["cols"],
  toolbar: [],
  defaultToolbar: ["import", "export", "search", "refresh", "filter"],
  pagination: {
    pageSize: 10,
    pageSizes: [10, 20, 30, 50],
  },
  request: { page_no: "page_no", page_size: "page_size" },
  indexAction: async (params) => {
    const res = await DemoAPI.getDemoList(
      normalizeDemoQuery(params as unknown as Record<string, unknown>)
    );
    return {
      total: res.data.data.total,
      list: res.data.data.items,
    };
  },
  deleteAction: (ids) =>
    DemoAPI.deleteDemo(
      ids
        .split(",")
        .map((s) => Number(s.trim()))
        .filter((n) => !Number.isNaN(n) && n > 0)
    ),
  importTemplate: () => DemoAPI.downloadTemplateDemo(),
  importAction: (file: File) => {
    const fd = new FormData();
    fd.append("file", file);
    return DemoAPI.importDemo(fd).then((res) => {
      if (res.data.code !== ResultEnum.SUCCESS) {
        return Promise.reject(new Error(res.data.msg));
      }
    });
  },
  exportsAction: async (params: DemoPageQuery) => {
    const query: Record<string, unknown> = { ...params };
    if (typeof query.status === "string") {
      query.status = query.status === "true";
    }
    return fetchAllPages<DemoTable>({
      pageSize: 9999,
      initialQuery: query,
      fetchPage: async (q) => {
        const res = await DemoAPI.getDemoList(
          normalizeDemoQuery(q as unknown as Record<string, unknown>)
        );
        return {
          total: res.data?.data?.total ?? 0,
          list: res.data?.data?.items ?? [],
        };
      },
    });
  },
});

const detailFormData = ref<DemoTable>({});

const formData = reactive<DemoForm>({
  id: undefined,
  name: "",
  status: "0",
  description: undefined,
  a: undefined,
  b: undefined,
  c: undefined,
  d: true,
  e: undefined,
  f: undefined,
  g: undefined,
  h: undefined,
  i: undefined,
});

const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

const rules = reactive({
  name: [{ required: true, message: "请输入名称", trigger: "blur" }],
  status: [{ required: true, message: "请选择状态", trigger: "blur" }],
});

const dataFormRef = ref();

const metadataList = ref<{ key: string; value: string }[]>([]);

function handleToggleSearch() {
  searchRef.value?.toggleVisible();
}

function handleRowDelete(id: number) {
  contentRef.value?.handleDelete(id);
}

const initialFormData: DemoForm = {
  id: undefined,
  name: "",
  status: "0",
  description: undefined,
  a: undefined,
  b: undefined,
  c: undefined,
  d: true,
  e: undefined,
  f: undefined,
  g: undefined,
  h: undefined,
  i: undefined,
};

async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  Object.assign(formData, initialFormData);
  metadataList.value = [];
}

async function handleCloseDialog() {
  dialogVisible.visible = false;
  resetForm();
}

async function handleOpenDialog(type: "create" | "update" | "detail", id?: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await DemoAPI.getDemoDetail(id);
    if (type === "detail") {
      dialogVisible.title = "详情";
      Object.assign(detailFormData.value, response.data.data);
    } else if (type === "update") {
      dialogVisible.title = "修改";
      Object.assign(formData, response.data.data);
      if (formData.i && typeof formData.i === "object") {
        metadataList.value = Object.entries(formData.i).map(([key, value]) => ({
          key,
          value: String(value),
        }));
      } else {
        metadataList.value = [];
      }
    }
  } else {
    dialogVisible.title = "新增示例";
    formData.id = undefined;
    metadataList.value = [];
  }
  dialogVisible.visible = true;
}

async function handleSubmit() {
  dataFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      const submitData = { ...formData };
      if (metadataList.value.length > 0) {
        const metadataObj: Record<string, string> = {};
        metadataList.value.forEach((item) => {
          if (item.key.trim()) {
            metadataObj[item.key.trim()] = item.value;
          }
        });
        submitData.i = Object.keys(metadataObj).length > 0 ? metadataObj : undefined;
      } else {
        submitData.i = undefined;
      }
      const id = formData.id;
      try {
        if (id) {
          await DemoAPI.updateDemo(id, { id, ...submitData });
        } else {
          await DemoAPI.createDemo(submitData);
        }
        dialogVisible.visible = false;
        await resetForm();
        refreshList();
      } catch (error: unknown) {
        console.error(error);
      }
    }
  });
}

async function handleMoreClick(status: string) {
  const rows = contentRef.value?.getSelectionData() ?? [];
  const ids = rows.map((r: { id?: number }) => r.id).filter(Boolean) as number[];
  if (!ids.length) return;
  ElMessageBox.confirm(`确认${status === "0" ? "启用" : "停用"}该项数据?`, "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        await DemoAPI.batchDemo({ ids, status });
        refreshList();
      } catch (error: unknown) {
        console.error(error);
      }
    })
    .catch(() => {
      ElMessageBox.close();
    });
}

onMounted(() => {
  refreshList();
});
</script>

<style lang="scss" scoped></style>
