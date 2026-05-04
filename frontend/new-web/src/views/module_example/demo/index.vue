<!-- 示例 CRUD：与角色页同一套 Art 布局；弹窗与 Crud 一致（ArtDialog + crud-embed-dialog） -->
<template>
  <div class="art-full-height">
    <ArtSearchBarWithAudit
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="demoBusinessSearchItems"
      :rules="searchBarRules"
      :is-expand="false"
      :show-expand="true"
      :show-reset="true"
      :show-search="true"
      :disabled-search="false"
      :default-expanded="false"
      @search="handleSearch"
      @reset="onResetSearch"
    />

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
            :perm-create="['module_example:demo:create']"
            :perm-import="['module_example:demo:import']"
            :perm-export="['module_example:demo:export']"
            :perm-delete="['module_example:demo:delete']"
            :perm-patch="['module_example:demo:patch']"
            :delete-loading="batchDeleting"
            @add="openEditDialog('add')"
            @import="openImportModal"
            @export="openExportModal"
            @delete="handleBatchDelete"
            @more="runBatchStatus"
          />
        </template>
      </ArtTableHeader>

      <ArtTable
        ref="artTableRef"
        :loading="loading"
        :data="data"
        :columns="columns"
        :pagination="paginationBind"
        @selection-change="onTableSelectionChange"
        @pagination:size-change="handleSizeChange"
        @pagination:current-change="handleCurrentChange"
      />
    </ElCard>

    <ArtDialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      width="920px"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      @close="handleCloseDialog"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <ElScrollbar max-height="70vh" :view-style="{ overflowX: 'hidden' }">
          <ElDescriptions :column="4" border>
            <ElDescriptionsItem label="名称" :span="2">
              {{ detailFormData.name }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="UUID" :span="2">
              {{ detailFormData.uuid }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="状态" :span="2">
              <ElTag :type="detailFormData.status === '0' ? 'success' : 'danger'">
                {{ detailFormData.status === "0" ? "启用" : "停用" }}
              </ElTag>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="整数" :span="2">
              {{ detailFormData.a }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="大整数" :span="2">
              {{ detailFormData.b }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="浮点数" :span="2">
              {{ detailFormData.c }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="布尔值" :span="2">
              <ElTag :type="detailFormData.d ? 'success' : 'danger'">
                {{ detailFormData.d ? "是" : "否" }}
              </ElTag>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="日期" :span="2">
              {{ detailFormData.e }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="时间" :span="2">
              {{ detailFormData.f }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="日期时间" :span="2">
              {{ detailFormData.g }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="长文本" :span="2">
              {{ detailFormData.h }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="元数据" :span="2">
              <JsonPretty
                v-if="detailFormData.i != null"
                :value="detailFormData.i"
                height="140px"
              />
            </ElDescriptionsItem>
            <ElDescriptionsItem label="描述" :span="2">
              {{ detailFormData.description }}
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
          </ElDescriptions>
        </ElScrollbar>
      </template>
      <template v-else>
        <ElScrollbar max-height="70vh" :view-style="{ overflowX: 'hidden' }">
          <ElForm
            ref="dataFormRef"
            :model="formData"
            :rules="rules"
            label-suffix=":"
            label-width="auto"
            label-position="right"
            inline
          >
            <ElFormItem label="名称" prop="name">
              <ElInput v-model="formData.name" placeholder="请输入名称" :maxlength="50" />
            </ElFormItem>
            <ElFormItem label="状态" prop="status">
              <ElRadioGroup v-model="formData.status">
                <ElRadio value="0">启用</ElRadio>
                <ElRadio value="1">停用</ElRadio>
              </ElRadioGroup>
            </ElFormItem>
            <ElFormItem label="整数" prop="a">
              <ElInputNumber v-model="formData.a" placeholder="请输入整数" />
            </ElFormItem>
            <ElFormItem label="大整数" prop="b">
              <ElInputNumber v-model="formData.b" placeholder="请输入大整数" />
            </ElFormItem>
            <ElFormItem label="浮点数" prop="c">
              <ElInputNumber
                v-model="formData.c"
                placeholder="请输入浮点数"
                :step="0.01"
                :precision="2"
              />
            </ElFormItem>
            <ElFormItem label="布尔值" prop="d">
              <ElSwitch v-model="formData.d" />
            </ElFormItem>
            <ElFormItem label="日期" prop="e">
              <ElDatePicker
                v-model="formData.e"
                type="date"
                placeholder="请选择日期"
                style="width: 100%"
                value-format="YYYY-MM-DD"
              />
            </ElFormItem>
            <ElFormItem label="时间" prop="f">
              <ElTimePicker
                v-model="formData.f"
                placeholder="请选择时间"
                style="width: 100%"
                value-format="HH:mm:ss"
              />
            </ElFormItem>
            <ElFormItem label="日期时间" prop="g">
              <ElDatePicker
                v-model="formData.g"
                type="datetime"
                placeholder="请选择日期时间"
                style="width: 100%"
                value-format="YYYY-MM-DD HH:mm:ss"
              />
            </ElFormItem>
            <ElFormItem label="长文本" prop="h">
              <ElInput v-model="formData.h" :rows="4" type="textarea" placeholder="请输入长文本" />
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
            <ElFormItem label="元数据" prop="i">
              <div class="flex flex-col gap-2">
                <div
                  v-for="(item, index) in metadataList"
                  :key="index"
                  class="flex items-center gap-2"
                >
                  <ElInput v-model="item.key" placeholder="键" />
                  <ElInput v-model="item.value" placeholder="值" />
                  <ElButton
                    type="primary"
                    icon="Plus"
                    circle
                    @click="metadataList.push({ key: '', value: '' })"
                  />
                  <ElButton
                    type="danger"
                    icon="Delete"
                    circle
                    @click="metadataList.splice(index, 1)"
                  />
                </div>
                <ElButton
                  v-if="metadataList.length === 0"
                  type="primary"
                  icon="Plus"
                  @click="metadataList.push({ key: '', value: '' })"
                >
                  添加元数据
                </ElButton>
              </div>
            </ElFormItem>
          </ElForm>
        </ElScrollbar>
      </template>

      <template #footer>
        <div class="dialog-footer" style="padding-right: var(--el-dialog-padding-primary)">
          <ElButton @click="handleCloseDialog">取消</ElButton>
          <ElButton v-if="dialogVisible.type !== 'detail'" type="primary" @click="handleSubmit">
            确定
          </ElButton>
          <ElButton v-else type="primary" @click="handleCloseDialog">确定</ElButton>
        </div>
      </template>
    </ArtDialog>

    <ArtImportDialog
      v-model="importModalVisible"
      :content-config="demoImportContentConfig"
      default-template-file-name="demo_import_template.xlsx"
      @upload="handleCrudImportUpload"
    />

    <ArtExportDialog
      v-model="exportModalVisible"
      :content-config="demoExportContentConfig"
      :query-params="exportQueryParams"
      :page-data="data"
      :selection-data="selectedRows"
    />
  </div>
</template>

<script setup lang="ts">
import { h, computed, ref } from "vue";
import { ButtonMoreItem } from "@/components/Core/forms/art-button-more/index.vue";
import { useTable } from "@/hooks/core/useTable";
import ArtTableHeaderLeft from "@/components/Core/tables/art-table-header-left/index.vue";
import ArtImportDialog from "@/components/Core/modal/art-import-dialog/index.vue";
import ArtExportDialog from "@/components/Core/modal/art-export-dialog/index.vue";
import type { IContentConfig, IObject } from "@/components/Core/modal/types";
import ArtButtonMore from "@/components/Core/forms/art-button-more/index.vue";
import ArtSearchBarWithAudit from "@/components/Core/forms/art-search-bar/ArtSearchBarWithAudit.vue";
import type { AuditSearchFormParams } from "@/components/Core/forms/art-search-bar/auditSearchFormItems";
import ArtDialog from "@/components/Core/modal/art-dialog/index.vue";
import JsonPretty from "@/components/JsonPretty/index.vue";
import type { ColumnOption } from "@/types/component";
import DemoAPI, {
  type DemoForm,
  type DemoPageQuery,
  type DemoTable,
} from "@/api/module_example/demo";
import { ElMessage, ElMessageBox, ElTag } from "element-plus";
import { ResultEnum } from "@/enums/api/result.enum";

defineOptions({
  name: "Demo",
  inheritAttrs: false,
});

type DemoSearchFormParams = { name?: string; status?: string } & AuditSearchFormParams;

function normalizeDemoQuery(params: Record<string, unknown>): DemoPageQuery {
  const p = { ...params } as Record<string, unknown>;
  if (Array.isArray(p.created_time) && p.created_time.length === 0) p.created_time = undefined;
  if (Array.isArray(p.updated_time) && p.updated_time.length === 0) p.updated_time = undefined;
  return p as unknown as DemoPageQuery;
}

const searchForm = ref<DemoSearchFormParams>({
  name: undefined,
  status: undefined,
  created_id: undefined,
  updated_id: undefined,
  created_time: [],
  updated_time: [],
});

/** 搜索区域默认展开展示 */
const showSearchBar = ref(true);

const searchBarRef = ref<InstanceType<typeof ArtSearchBarWithAudit> | null>(null);
const searchBarRules: Record<string, unknown> = {};
const statusOptions = ref([
  { label: "启用", value: "0" },
  { label: "停用", value: "1" },
]);
/** 名称、状态；创建人/更新人/时间由 ArtSearchBarWithAudit 追加 */
const demoBusinessSearchItems = computed(() => [
  {
    label: "名称",
    key: "name",
    type: "input",
    placeholder: "请输入名称",
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
]);

const artTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const selectedRows = ref<DemoTable[]>([]);
const selectedIds = computed(() =>
  selectedRows.value.map((r) => r.id).filter((id): id is number => id != null && !Number.isNaN(id))
);
const batchDeleting = ref(false);

function onTableSelectionChange(rows: DemoTable[]) {
  selectedRows.value = rows;
}

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
    apiFn: DemoAPI.getDemoList,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: (): ColumnOption<DemoTable>[] => [
      { type: "selection", width: 48, fixed: "left" },
      { prop: "id", label: "ID", width: 72 },
      { prop: "name", label: "名称", minWidth: 120, showOverflowTooltip: true },
      { prop: "uuid", label: "UUID", minWidth: 168, showOverflowTooltip: true },
      {
        prop: "status",
        label: "状态",
        width: 88,
        formatter: (row: DemoTable) => {
          const ok = row.status === "0";
          const cfg = ok
            ? { type: "success" as const, text: "启用" }
            : { type: "info" as const, text: "停用" };
          return h(ElTag, { type: cfg.type }, () => cfg.text);
        },
      },
      { prop: "a", label: "整数", minWidth: 88, showOverflowTooltip: true },
      { prop: "b", label: "大整数", minWidth: 100, showOverflowTooltip: true },
      { prop: "c", label: "浮点数", minWidth: 88, showOverflowTooltip: true },
      {
        prop: "d",
        label: "布尔",
        width: 80,
        formatter: (row: DemoTable) =>
          h(ElTag, { type: row.d ? "success" : "danger" }, () => (row.d ? "是" : "否")),
      },
      { prop: "e", label: "日期", minWidth: 112, showOverflowTooltip: true },
      { prop: "f", label: "时间", minWidth: 96, showOverflowTooltip: true },
      { prop: "g", label: "日期时间", minWidth: 168, showOverflowTooltip: true },
      { prop: "h", label: "长文本", minWidth: 120, showOverflowTooltip: true },
      {
        prop: "i",
        label: "元数据",
        minWidth: 160,
        formatter: (row: DemoTable) => {
          if (row.i == null) return h("span", { class: "text-g-500" }, "—");
          return h(JsonPretty, { value: row.i, height: "120px" });
        },
      },
      { prop: "description", label: "描述", minWidth: 120, showOverflowTooltip: true },
      { prop: "created_time", label: "创建时间", width: 168, showOverflowTooltip: true },
      { prop: "updated_time", label: "更新时间", width: 168, showOverflowTooltip: true },
      {
        prop: "created_by",
        label: "创建人",
        minWidth: 100,
        formatter: (row: DemoTable) => row.created_by?.name ?? "—",
      },
      {
        prop: "updated_by",
        label: "更新人",
        minWidth: 100,
        formatter: (row: DemoTable) => row.updated_by?.name ?? "—",
      },
      {
        prop: "operation",
        label: "操作",
        width: 102,
        fixed: "right",
        formatter: (row: DemoTable) =>
          h("div", [
            h(ArtButtonMore, {
              list: [
                { key: "detail", label: "详情", icon: "ri:file-list-3-line" },
                { key: "edit", label: "编辑", icon: "ri:edit-2-line" },
                { key: "delete", label: "删除", icon: "ri:delete-bin-4-line", color: "#f56c6c" },
              ],
              onClick: (item: ButtonMoreItem) => buttonMoreClick(item, row),
            }),
          ]),
      },
    ],
  },
});

/** 供 CrudImportModal / CrudExportModal 的列配置（与 CrudContent.cols 结构一致） */
const demoCrudCols = computed(() =>
  columns.value.map((c: ColumnOption<DemoTable>) => {
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
  return normalizeDemoQuery(sp);
});

const demoImportContentConfig = computed<IContentConfig>(() => ({
  permPrefix: "module_example:demo",
  cols: demoCrudCols.value,
  indexAction: async () => ({}) as any,
  importTemplate: () => DemoAPI.downloadTemplateDemo(),
}));

const demoExportContentConfig = computed(() => ({
  permPrefix: "module_example:demo",
  cols: demoCrudCols.value,
  exportsBlobAction: async (params: IObject) => {
    const merged = normalizeDemoQuery({
      ...(exportQueryParams.value as unknown as Record<string, unknown>),
      ...params,
    } as Record<string, unknown>);
    const res = await DemoAPI.exportDemo(merged as DemoPageQuery);
    return res.data as Blob;
  },
}));

const paginationBind = computed(() => {
  const p = pagination as unknown as {
    current?: number;
    size?: number;
    total?: number;
    page_no?: number;
    page_size?: number;
  };
  return {
    current: p.current ?? p.page_no ?? 1,
    size: p.size ?? p.page_size ?? 20,
    total: p.total ?? 0,
  };
});

const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
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

const rules = reactive({
  name: [{ required: true, message: "请输入名称", trigger: "blur" }],
  status: [{ required: true, message: "请选择状态", trigger: "blur" }],
});

const dataFormRef = ref();
const metadataList = ref<{ key: string; value: string }[]>([]);

const importModalVisible = ref(false);
const exportModalVisible = ref(false);

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

const handleSearch = async (params: DemoSearchFormParams) => {
  await searchBarRef.value?.validate();
  replaceSearchParams({
    name: params.name,
    status: params.status,
    created_id: params.created_id ?? undefined,
    updated_id: params.updated_id ?? undefined,
    created_time:
      Array.isArray(params.created_time) && params.created_time.length === 2
        ? params.created_time
        : undefined,
    updated_time:
      Array.isArray(params.updated_time) && params.updated_time.length === 2
        ? params.updated_time
        : undefined,
  } as Record<string, unknown>);
  getData();
};

const onResetSearch = async () => {
  searchForm.value = {
    name: undefined,
    status: undefined,
    created_id: undefined,
    updated_id: undefined,
    created_time: [],
    updated_time: [],
  };
  await resetSearchParams();
};

const buttonMoreClick = (item: ButtonMoreItem, row: DemoTable) => {
  switch (item.key) {
    case "detail":
      openDetailDialog(row);
      break;
    case "edit":
      openEditDialog("edit", row);
      break;
    case "delete":
      deleteDemoRow(row);
      break;
  }
};

async function openDetailDialog(row: DemoTable) {
  if (!row.id) return;
  const response = await DemoAPI.getDemoDetail(row.id);
  dialogVisible.type = "detail";
  dialogVisible.title = "详情";
  detailFormData.value = response.data.data ?? { ...row };
  dialogVisible.visible = true;
}

async function openEditDialog(type: "add" | "edit", row?: DemoTable) {
  dialogVisible.type = type === "add" ? "create" : "update";
  if (type === "add") {
    dialogVisible.title = "新增示例";
    Object.assign(formData, initialFormData);
    formData.id = undefined;
    metadataList.value = [];
  } else if (row?.id) {
    dialogVisible.title = "修改";
    const response = await DemoAPI.getDemoDetail(row.id);
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
  dialogVisible.visible = true;
}

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
  await resetForm();
}

async function handleSubmit() {
  dataFormRef.value.validate(async (valid: boolean) => {
    if (!valid) return;
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
        await refreshUpdate();
      } else {
        await DemoAPI.createDemo(submitData);
        await refreshCreate();
      }
      dialogVisible.visible = false;
      await resetForm();
    } catch (error: unknown) {
      console.error(error);
    }
  });
}

const deleteDemoRow = (row: DemoTable) => {
  if (!row.id) return;
  ElMessageBox.confirm(`确定删除「${row.name ?? row.id}」吗？此操作不可恢复！`, "删除确认", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await DemoAPI.deleteDemo([row.id!]);
      ElMessage.success("删除成功");
      artTableRef.value?.elTableRef?.clearSelection();
      await refreshRemove();
    })
    .catch(() => {
      ElMessage.info("已取消删除");
    });
};

function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  ElMessageBox.confirm(`确定删除选中的 ${ids.length} 条数据吗？此操作不可恢复！`, "批量删除", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        batchDeleting.value = true;
        await DemoAPI.deleteDemo(ids);
        ElMessage.success("删除成功");
        artTableRef.value?.elTableRef?.clearSelection();
        await refreshRemove();
      } finally {
        batchDeleting.value = false;
      }
    })
    .catch(() => {
      ElMessage.info("已取消删除");
    });
}

function runBatchStatus(status: string) {
  const ids = selectedIds.value;
  if (ids.length === 0) {
    ElMessage.warning("请先在列表中勾选数据");
    return;
  }
  ElMessageBox.confirm(
    `确认对选中的 ${ids.length} 条数据${status === "0" ? "启用" : "停用"}？`,
    "批量设置",
    { confirmButtonText: "确定", cancelButtonText: "取消", type: "warning" }
  )
    .then(async () => {
      await DemoAPI.batchDemo({ ids, status });
      ElMessage.success("操作成功");
      artTableRef.value?.elTableRef?.clearSelection();
      await refreshData();
    })
    .catch(() => {});
}

function openImportModal() {
  importModalVisible.value = true;
}

function handleCrudImportUpload(formData: FormData) {
  DemoAPI.importDemo(formData)
    .then((res) => {
      if (res.data.code !== ResultEnum.SUCCESS) {
        ElMessage.error(res.data.msg || "导入失败");
        return;
      }
      ElMessage.success(res.data.msg || "导入成功");
      importModalVisible.value = false;
      return refreshData();
    })
    .catch(console.error);
}

function openExportModal() {
  exportModalVisible.value = true;
}
</script>
