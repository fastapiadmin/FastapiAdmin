<!-- 演示示例：CrudLayout + CrudSearch + CrudContent（配置驱动列表 + 自定义工具栏） -->
<template>
  <CrudLayout>
    <template #search>
      <CrudSearch
        ref="searchRef"
        :search-config="searchConfig"
        @query-click="handleQueryClick"
        @reset-click="handleResetClick"
      />
    </template>

    <CrudContent
      ref="contentRef"
      :content-config="contentConfig"
      @add-click="handleOpenDialog('create')"
    >
      <!-- Art 栈：右侧刷新/列设置等为 ArtTableHeader 内置；导入导出放在左侧插槽与示例一致 -->
      <template #toolbar="{ onToolbar, removeIds }">
        <CrudToolbarLeft
          :remove-ids="removeIds"
          :perm-create="['module_example:demo:create']"
          :perm-delete="['module_example:demo:delete']"
          :perm-patch="['module_example:demo:patch']"
          @add="handleOpenDialog('create')"
          @delete="onToolbar('delete')"
          @more="handleMoreClick"
        />
        <el-button
          v-hasPerm="['module_example:demo:import']"
          type="info"
          @click="onToolbar('import')"
        >
          <template #icon>
            <Upload />
          </template>
          导入
        </el-button>
        <el-button
          v-hasPerm="['module_example:demo:export']"
          type="warning"
          @click="onToolbar('export')"
        >
          <template #icon>
            <Download />
          </template>
          导出
        </el-button>
      </template>

      <!-- 自定义列（templet: custom） -->
      <template #status="{ row }">
        <el-tag :type="row.status ? 'success' : 'info'">
          {{ row.status ? "启用" : "停用" }}
        </el-tag>
      </template>
      <template #d="{ row }">
        <el-tag :type="row.d ? 'success' : 'danger'">
          {{ row.d ? "是" : "否" }}
        </el-tag>
      </template>
      <template #created_id="{ row }">
        <el-tag>{{ row.created_by?.name }}</el-tag>
      </template>
      <template #updated_id="{ row }">
        <el-tag>{{ row.updated_by?.name }}</el-tag>
      </template>
      <template #i="{ row }">
        <JsonPretty v-if="row.i != null" :value="row.i" height="120px" />
        <span v-else class="text-g-500">—</span>
      </template>
      <template #operation="{ row }">
        <el-button
          v-hasPerm="['module_example:demo:detail']"
          type="info"
          size="small"
          link
          :icon="View"
          @click="handleOpenDialog('detail', row.id)"
        >
          详情
        </el-button>
        <el-button
          v-hasPerm="['module_example:demo:update']"
          type="primary"
          size="small"
          link
          :icon="Edit"
          @click="handleOpenDialog('update', row.id)"
        >
          编辑
        </el-button>
        <el-button
          v-hasPerm="['module_example:demo:delete']"
          type="danger"
          size="small"
          link
          :icon="Delete"
          @click="handleRowDelete(row.id)"
        >
          删除
        </el-button>
      </template>
    </CrudContent>

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
  </CrudLayout>
</template>

<script setup lang="ts">
defineOptions({
  name: "Demo",
  inheritAttrs: false,
});

import { ref, reactive, onMounted, markRaw, nextTick } from "vue";
import { Delete, Download, Edit, Upload, View } from "@element-plus/icons-vue";
import { fetchAllPages } from "@/utils/fetchAllPages";
import { ElMessageBox } from "element-plus";
import { ResultEnum } from "@/enums/api/result.enum";
import DemoAPI, { DemoTable, DemoForm, DemoPageQuery } from "@/api/module_example/demo";
import {
  CrudLayout,
  CrudToolbarLeft,
  CrudContent,
  CrudSearch,
  useCrudList,
} from "@/components/Crud";
import EnhancedDialog from "@/components/Core/overlays/EnhancedDialog.vue";
import UserTableSelect from "@/views/module_system/user/components/UserTableSelect.vue";
import type { IContentConfig, ISearchConfig } from "@/components/Crud";
import JsonPretty from "@/components/JsonPretty/index.vue";

const { searchRef, contentRef, handleQueryClick, handleResetClick, refreshList } = useCrudList();

function triggerUserSearch() {
  nextTick(() => refreshList());
}

const searchConfig = reactive<ISearchConfig>({
  permPrefix: "module_example:demo",
  colon: true,
  /** 与 examples/forms/search-bar 一致：ArtSearchBar + art-card-xs */
  searchVariant: "art",
  isExpandable: true,
  showNumber: 3,
  artSearchSpan: 6,
  /** 与 ArtSearchBar 默认一致；勿用 labelWidth:auto 否则标签区忽宽忽窄 */
  form: { labelWidth: "70px", labelPosition: "right" },
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
      attrs: { placeholder: "请选择状态", clearable: true },
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

const contentCols = reactive<IContentConfig["cols"]>([
  { type: "selection", label: "选择框", width: 55, align: "center", show: true },
  { type: "index", label: "序号", width: 60, fixed: true, show: true },
  { prop: "name", label: "名称", minWidth: 140, show: true, "show-overflow-tooltip": true },
  { prop: "uuid", label: "UUID", minWidth: 180, show: true, "show-overflow-tooltip": true },
  {
    prop: "status",
    label: "状态",
    minWidth: 120,
    show: true,
    templet: "custom",
    slotName: "status",
    "show-overflow-tooltip": true,
  },
  { prop: "a", label: "整数", minWidth: 100, show: true, "show-overflow-tooltip": true },
  { prop: "b", label: "大整数", minWidth: 120, show: true, "show-overflow-tooltip": true },
  { prop: "c", label: "浮点数", minWidth: 100, show: true, "show-overflow-tooltip": true },
  {
    prop: "d",
    label: "布尔值",
    minWidth: 100,
    show: true,
    templet: "custom",
    slotName: "d",
    "show-overflow-tooltip": true,
  },
  { prop: "e", label: "日期", minWidth: 120, show: true, "show-overflow-tooltip": true },
  { prop: "f", label: "时间", minWidth: 120, show: true, "show-overflow-tooltip": true },
  { prop: "g", label: "日期时间", minWidth: 180, show: true, "show-overflow-tooltip": true },
  { prop: "h", label: "长文本", minWidth: 140, show: true, "show-overflow-tooltip": true },
  {
    prop: "i",
    label: "元数据",
    minWidth: 160,
    show: true,
    templet: "custom",
    slotName: "i",
  },
  { prop: "description", label: "描述", minWidth: 140, show: true, "show-overflow-tooltip": true },
  {
    prop: "created_time",
    label: "创建时间",
    minWidth: 180,
    show: true,
    "show-overflow-tooltip": true,
  },
  {
    prop: "updated_time",
    label: "更新时间",
    minWidth: 180,
    show: true,
    "show-overflow-tooltip": true,
  },
  {
    prop: "created_id",
    label: "创建人",
    minWidth: 120,
    show: true,
    templet: "custom",
    slotName: "created_id",
    "show-overflow-tooltip": true,
  },
  {
    prop: "updated_id",
    label: "更新人",
    minWidth: 120,
    show: true,
    templet: "custom",
    slotName: "updated_id",
    "show-overflow-tooltip": true,
  },
  {
    prop: "operation",
    label: "操作",
    fixed: "right",
    align: "center",
    minWidth: 200,
    show: true,
    templet: "custom",
    slotName: "operation",
  },
]);

function normalizeDemoQuery(params: Record<string, unknown>) {
  const p = { ...params } as Record<string, unknown>;
  if (Array.isArray(p.created_time) && p.created_time.length === 0) p.created_time = undefined;
  if (Array.isArray(p.updated_time) && p.updated_time.length === 0) p.updated_time = undefined;
  return p as unknown as DemoPageQuery;
}

const contentConfig = reactive<IContentConfig<DemoPageQuery>>({
  permPrefix: "module_example:demo",
  /** 与 examples/tables 高级示例一致：ArtTableHeader + ArtTable + 内嵌分页 */
  tableVariant: "art",
  hideColumnFilter: true,
  initialFetch: false,
  cols: contentCols,
  toolbar: [],
  table: {
    border: true,
    stripe: true,
    fit: true,
    style: { width: "100%" },
  },
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
        const items = (res.data?.data?.items ?? []) as DemoTable[];
        return {
          total: res.data?.data?.total ?? 0,
          list: items,
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
