<!-- 字典数据抽屉：Art 搜索 + useTable；固定 dict_type / dict_type_id 由父级传入 -->
<template>
  <FaDrawer
    v-model="drawerVisible"
    :title="'【' + dictLabel + '】字典数据'"
    direction="rtl"
    :size="drawerSize"
  >
    <div class="drawer-content">
      <FaSearchBar
        v-show="showSearchBar"
        ref="searchBarRef"
        v-model="searchForm"
        :items="dictDataSearchItems"
        :rules="searchBarRules"
        :is-expand="false"
        :show-expand="true"
        :show-reset="true"
        :show-search="true"
        :disabled-search="false"
        :default-expanded="false"
        @search="handleSearchBarSearch"
        @reset="onResetSearch"
      />

      <ElCard
        class="fa-table-card drawer-table-card"
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
              :perm-create="['module_system:dict_data:create']"
              :perm-export="['module_system:dict_data:export']"
              :perm-delete="['module_system:dict_data:delete']"
              :perm-patch="['module_system:dict_data:patch']"
              :delete-loading="batchDeleting"
              @add="handleOpenDialog('create')"
              @export="openExportModal"
              @delete="handleBatchDelete"
              @more="handleMoreClick"
            />
          </template>
        </FaTableHeader>

        <FaTable
          ref="faTableRef"
          :loading="loading"
          :data="data"
          :columns="columns"
          :pagination="pagination"
          @selection-change="onTableSelectionChange"
          @pagination:size-change="handleSizeChange"
          @pagination:current-change="handleCurrentChange"
        />
      </ElCard>

      <FaDialog
        v-model="dialogVisible.visible"
        :title="dialogVisible.title"
        width="720px"
        dialog-class="crud-embed-dialog"
        modal-class="crud-embed-dialog"
        @close="handleCloseDialog"
      >
        <template v-if="dialogVisible.type === 'detail'">
          <ElScrollbar max-height="70vh" :view-style="{ overflowX: 'hidden' }">
            <ElDescriptions :column="2" border>
              <ElDescriptionsItem label="数据标签" :span="2">
                {{ detailFormData.dict_label }}
              </ElDescriptionsItem>
              <ElDescriptionsItem label="数据类型" :span="2">
                {{ detailFormData.dict_type }}
              </ElDescriptionsItem>
              <ElDescriptionsItem label="数据值" :span="2">
                {{ detailFormData.dict_value }}
              </ElDescriptionsItem>
              <ElDescriptionsItem label="样式属性" :span="2">
                {{ detailFormData.css_class }}
              </ElDescriptionsItem>
              <ElDescriptionsItem label="列表样式属性" :span="2">
                {{ detailFormData.list_class }}
              </ElDescriptionsItem>
              <ElDescriptionsItem label="是否默认" :span="2">
                <ElTag v-if="detailFormData.is_default" type="success">是</ElTag>
                <ElTag v-else type="danger">否</ElTag>
              </ElDescriptionsItem>
              <ElDescriptionsItem label="状态" :span="2">
                <ElTag v-if="detailFormData.status === '0'" type="success">启用</ElTag>
                <ElTag v-else type="danger">停用</ElTag>
              </ElDescriptionsItem>
              <ElDescriptionsItem label="排序" :span="2">
                {{ detailFormData.dict_sort }}
              </ElDescriptionsItem>
              <ElDescriptionsItem label="描述" :span="2">
                {{ detailFormData.description }}
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
            <FaForm
              :key="dictDataFormRenderKey"
              ref="dataFormRef"
              v-model="formData"
              :items="dictDataDialogFormItems"
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
              <template #css_class>
                <ElSelect
                  v-model="formData.css_class"
                  placeholder="请选择常用颜色或输入自定义"
                  clearable
                  filterable
                  allow-create
                  default-first-option
                >
                  <ElOption value="primary" label="主要(primary)">
                    <span class="tag-option-preview" :style="getTagPreviewStyle('primary')">
                      主要(primary)
                    </span>
                  </ElOption>
                  <ElOption value="success" label="成功(success)">
                    <span class="tag-option-preview" :style="getTagPreviewStyle('success')">
                      成功(success)
                    </span>
                  </ElOption>
                  <ElOption value="warning" label="警告(warning)">
                    <span class="tag-option-preview" :style="getTagPreviewStyle('warning')">
                      警告(warning)
                    </span>
                  </ElOption>
                  <ElOption value="danger" label="危险(danger)">
                    <span class="tag-option-preview" :style="getTagPreviewStyle('danger')">
                      危险(danger)
                    </span>
                  </ElOption>
                  <ElOption value="info" label="信息(info)">
                    <span class="tag-option-preview" :style="getTagPreviewStyle('info')">
                      信息(info)
                    </span>
                  </ElOption>
                </ElSelect>
              </template>
              <template #list_class>
                <ElSelect v-model="formData.list_class" placeholder="请选择列表类样式" clearable>
                  <ElOption value="default" label="默认(default)">
                    <span class="tag-option-preview tag-option-preview--default">
                      默认(default)
                    </span>
                  </ElOption>
                  <ElOption value="primary" label="主要(primary)">
                    <span class="tag-option-preview" :style="getTagPreviewStyle('primary')">
                      主要(primary)
                    </span>
                  </ElOption>
                  <ElOption value="success" label="成功(success)">
                    <span class="tag-option-preview" :style="getTagPreviewStyle('success')">
                      成功(success)
                    </span>
                  </ElOption>
                  <ElOption value="warning" label="警告(warning)">
                    <span class="tag-option-preview" :style="getTagPreviewStyle('warning')">
                      警告(warning)
                    </span>
                  </ElOption>
                  <ElOption value="danger" label="危险(danger)">
                    <span class="tag-option-preview" :style="getTagPreviewStyle('danger')">
                      危险(danger)
                    </span>
                  </ElOption>
                  <ElOption value="info" label="信息(info)">
                    <span class="tag-option-preview" :style="getTagPreviewStyle('info')">
                      信息(info)
                    </span>
                  </ElOption>
                </ElSelect>
              </template>
              <template #is_default>
                <ElRadioGroup v-model="formData.is_default">
                  <ElRadio :value="true">是</ElRadio>
                  <ElRadio :value="false">否</ElRadio>
                </ElRadioGroup>
              </template>
              <template #status>
                <ElSwitch
                  v-model="formData.status"
                  inline-prompt
                  :active-value="'0'"
                  :inactive-value="'1'"
                />
              </template>
            </FaForm>
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
      </FaDialog>

      <FaExportDialog
        v-model="exportModalVisible"
        :content-config="dictDataExportContentConfig"
        :query-params="exportQueryParams"
        :page-data="data"
        :selection-data="selectedRows"
      />
    </div>
  </FaDrawer>
</template>

<script setup lang="ts">
import { h, computed, ref, reactive } from "vue";
import { useTable } from "@/hooks/core/useTable";
import FaTableHeaderLeft from "@/components/tables/fa-table-header-left/index.vue";
import FaExportDialog from "@/components/modal/fa-export-dialog/index.vue";
import type { IObject } from "@/components/modal/types";
import FaSearchBar from "@/components/forms/fa-search-bar/index.vue";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import FaDialog from "@/components/modal/fa-dialog/index.vue";
import FaDrawer from "@/components/modal/fa-drawer/index.vue";
import FaForm from "@/components/forms/fa-form/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import type { ColumnOption } from "@/types/component";
import DictAPI, {
  type DictDataForm,
  type DictDataPageQuery,
  type DictDataTable,
} from "@/api/module_system/dict";
import { ElMessage, ElMessageBox, ElTag } from "element-plus";
import { useAuth } from "@/hooks/core/useAuth";
import { renderTableOperationCell, type TableOperationAction } from "@utils/table";
import { useDictStore } from "@stores";
import { useAppStore } from "@stores/modules/app.store";
import { DeviceEnum } from "@/enums/settings/device.enum";

defineOptions({ name: "DictDataDrawer", inheritAttrs: false });

const props = defineProps<{
  dictType: string;
  dictLabel: string;
  dictTypeId: number;
}>();

const drawerVisible = defineModel<boolean>({ required: true });

const TAG_TYPE_STYLE_MAP: Record<string, { background: string; color: string; border: string }> = {
  primary: {
    background: "var(--el-color-primary-light-9)",
    color: "var(--el-color-primary)",
    border: "var(--el-color-primary-light-7)",
  },
  success: {
    background: "var(--el-color-success-light-9)",
    color: "var(--el-color-success)",
    border: "var(--el-color-success-light-7)",
  },
  warning: {
    background: "var(--el-color-warning-light-9)",
    color: "var(--el-color-warning)",
    border: "var(--el-color-warning-light-7)",
  },
  danger: {
    background: "var(--el-color-danger-light-9)",
    color: "var(--el-color-danger)",
    border: "var(--el-color-danger-light-7)",
  },
  info: {
    background: "var(--el-color-info-light-9)",
    color: "var(--el-color-info)",
    border: "var(--el-color-info-light-7)",
  },
};

const appStore = useAppStore();
const dictStore = useDictStore();
const { hasAuth } = useAuth();
const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "80%" : "60%"));

function getTagPreviewStyle(value?: string) {
  const preset = value ? TAG_TYPE_STYLE_MAP[value] : undefined;
  if (preset) {
    return {
      backgroundColor: preset.background,
      color: preset.color,
      borderColor: preset.border,
    };
  }
  if (!value) return {};
  return {
    backgroundColor: value,
    color: "#fff",
    borderColor: value,
  };
}

type DictDataSearchForm = {
  dict_label?: string;
  status?: string;
  created_time?: string[];
};

function normalizeDictDataQuery(params: Record<string, unknown>): DictDataPageQuery {
  const p = { ...params } as Record<string, unknown>;
  if (Array.isArray(p.created_time) && p.created_time.length === 0) p.created_time = undefined;
  if (Array.isArray(p.updated_time) && p.updated_time.length === 0) p.updated_time = undefined;
  return p as unknown as DictDataPageQuery;
}

async function fetchDictDataListMerged(params: Record<string, unknown>) {
  const q: DictDataPageQuery = {
    page_no: Number(params.current) || Number(params.page_no) || 1,
    page_size: Number(params.size) || Number(params.page_size) || 20,
    dict_label: params.dict_label as string | undefined,
    dict_type: props.dictType,
    dict_type_id: props.dictTypeId,
    status:
      params.status !== undefined && params.status !== null && params.status !== ""
        ? String(params.status)
        : undefined,
    created_time: Array.isArray(params.created_time)
      ? (params.created_time as string[])
      : undefined,
    updated_time: Array.isArray(params.updated_time)
      ? (params.updated_time as string[])
      : undefined,
  };
  return DictAPI.listDictData(q);
}

const searchForm = ref<DictDataSearchForm>({
  dict_label: undefined,
  status: undefined,
  created_time: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof FaSearchBar> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const statusOptions = ref([
  { label: "启用", value: "0" },
  { label: "停用", value: "1" },
]);

const dictDataSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "字典标签",
    key: "dict_label",
    type: "input",
    placeholder: "请输入字典标签",
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
const selectedRows = ref<DictDataTable[]>([]);
const selectedIds = computed(() =>
  selectedRows.value.map((r) => r.id).filter((id): id is number => id != null && !Number.isNaN(id))
);
const batchDeleting = ref(false);

function onTableSelectionChange(rows: DictDataTable[]) {
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
    apiFn: fetchDictDataListMerged,
    apiParams: {
      page_no: 1,
      page_size: 20,
      dict_type: props.dictType,
      dict_type_id: props.dictTypeId,
    },
    columnsFactory: (): ColumnOption<DictDataTable>[] => [
      { type: "selection", width: 48, fixed: "left" },
      { prop: "dict_label", label: "标签", minWidth: 150, showOverflowTooltip: true },
      {
        prop: "status",
        label: "状态",
        width: 100,
        formatter: (row: DictDataTable) => {
          const ok = row.status === "0";
          const cfg = ok
            ? { type: "success" as const, text: "启用" }
            : { type: "danger" as const, text: "停用" };
          return h(ElTag, { type: cfg.type }, () => cfg.text);
        },
      },
      {
        prop: "dict_type",
        label: "类型",
        minWidth: 180,
        formatter: (row: DictDataTable) => h(ElTag, { type: "primary" }, () => row.dict_type ?? ""),
      },
      { prop: "dict_value", label: "值", minWidth: 100, showOverflowTooltip: true },
      { prop: "css_class", label: "样式属性", minWidth: 100, showOverflowTooltip: true },
      { prop: "list_class", label: "列表类样式", minWidth: 100, showOverflowTooltip: true },
      { prop: "dict_sort", label: "排序", width: 72 },
      {
        prop: "is_default",
        label: "是否默认",
        width: 100,
        formatter: (row: DictDataTable) =>
          h(ElTag, { type: row.is_default ? "success" : "danger" }, () =>
            row.is_default ? "是" : "否"
          ),
      },
      { prop: "description", label: "描述", minWidth: 100, showOverflowTooltip: true },
      { prop: "created_time", label: "创建时间", width: 168, showOverflowTooltip: true },
      { prop: "updated_time", label: "更新时间", width: 168, showOverflowTooltip: true },
      {
        prop: "operation",
        label: "操作",
        width: 220,
        fixed: "right",
        align: "right",
        formatter: (row: DictDataTable) => formatDictDataOperationCell(row),
      },
    ],
  },
});

const dictDataCrudCols = computed(() =>
  columns.value.map((c: ColumnOption<DictDataTable>) => {
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
  return normalizeDictDataQuery({
    ...sp,
    dict_type: props.dictType,
    dict_type_id: props.dictTypeId,
  });
});

const dictDataExportContentConfig = computed(() => ({
  permPrefix: "module_system:dict_data",
  cols: dictDataCrudCols.value,
  exportsBlobAction: async (params: IObject) => {
    const merged = normalizeDictDataQuery({
      ...(exportQueryParams.value as unknown as Record<string, unknown>),
      ...params,
      dict_type: props.dictType,
      dict_type_id: props.dictTypeId,
    } as Record<string, unknown>);
    const res = await DictAPI.exportDictData(merged as DictDataPageQuery);
    return res.data as Blob;
  },
}));

const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

const detailFormData = ref<DictDataTable>({});

const formData = ref<DictDataForm>({
  id: undefined,
  dict_sort: 1,
  dict_label: "",
  dict_value: "",
  dict_type: "",
  css_class: "",
  list_class: undefined,
  is_default: false,
  status: "0",
  description: "",
  dict_type_id: undefined,
});

const rules = reactive({
  dict_label: [{ required: true, message: "请输入字典标签", trigger: "blur" }],
  dict_type: [{ required: true, message: "请输入字典类型", trigger: "blur" }],
  dict_value: [{ required: true, message: "请输入字典键值", trigger: "blur" }],
  status: [{ required: true, message: "请选择状态", trigger: "blur" }],
  dict_sort: [{ required: true, message: "请输入排序", trigger: "blur" }],
  is_default: [{ required: true, message: "请选择是否默认", trigger: "blur" }],
});

const dataFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const dictDataFormRenderKey = ref(0);

const dictDataDialogFormItems = computed<FormItem[]>(() => [
  {
    label: "数据类型",
    key: "dict_type",
    type: "input",
    span: 24,
    props: {
      placeholder: "请输入数据类型",
      maxlength: 50,
      disabled: true,
    },
  },
  {
    label: "数据标签",
    key: "dict_label",
    type: "input",
    span: 24,
    props: { placeholder: "请输入数据标签", maxlength: 255 },
  },
  {
    label: "数据值",
    key: "dict_value",
    type: "input",
    span: 24,
    props: { placeholder: "请输入数据值", maxlength: 255 },
  },
  {
    label: "样式属性",
    key: "css_class",
    type: "input",
    span: 24,
    placeholder: "",
  },
  {
    label: "列表类样式",
    key: "list_class",
    type: "input",
    span: 24,
    placeholder: "",
  },
  {
    label: "是否默认",
    key: "is_default",
    type: "input",
    span: 24,
    placeholder: "",
  },
  {
    label: "排序",
    key: "dict_sort",
    type: "number",
    span: 24,
    props: {
      controlsPosition: "right",
      min: 1,
      style: { width: "100px" },
    },
  },
  {
    label: "状态",
    key: "status",
    type: "input",
    span: 24,
    placeholder: "",
  },
  {
    label: "描述",
    key: "description",
    type: "input",
    span: 24,
    props: {
      type: "textarea",
      rows: 4,
      maxlength: 100,
      showWordLimit: true,
      placeholder: "请输入描述",
    },
  },
]);

const initialFormData: DictDataForm = {
  id: undefined,
  dict_sort: 1,
  dict_label: "",
  dict_value: "",
  dict_type: "",
  css_class: "",
  list_class: undefined,
  is_default: false,
  status: "0",
  description: "",
  dict_type_id: props.dictTypeId,
};

const exportModalVisible = ref(false);

async function handleSearchBarSearch(params: DictDataSearchForm) {
  await searchBarRef.value?.validate?.();
  replaceSearchParams({
    dict_label: params.dict_label,
    status: params.status,
    created_time:
      Array.isArray(params.created_time) && params.created_time.length === 2
        ? params.created_time
        : undefined,
    dict_type: props.dictType,
    dict_type_id: props.dictTypeId,
  } as Record<string, unknown>);
  getData();
}

function onResetSearch() {
  searchForm.value = {
    dict_label: undefined,
    status: undefined,
    created_time: undefined,
  };
  void resetSearchParams();
}

async function resetForm() {
  dataFormRef.value?.ref?.resetFields();
  dataFormRef.value?.ref?.clearValidate();
  Object.assign(formData, {
    ...initialFormData,
    dict_type_id: props.dictTypeId,
    dict_type: props.dictType,
  });
}

async function handleCloseDialog() {
  dialogVisible.visible = false;
  await resetForm();
}

async function handleOpenDialog(type: "create" | "update" | "detail", id?: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await DictAPI.detailDictData(id);
    if (type === "detail") {
      dialogVisible.title = "字典数据详情";
      detailFormData.value = response.data.data ?? {};
    } else if (type === "update") {
      dialogVisible.title = "修改字典数据";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增字典数据";
    Object.assign(formData.value, initialFormData);
    formData.value.dict_type = props.dictType;
    formData.value.dict_type_id = props.dictTypeId;
    formData.value.status = "0";
    formData.value.id = undefined;
  }
  dictDataFormRenderKey.value += 1;
  dialogVisible.visible = true;
}

async function handleSubmit() {
  dataFormRef.value?.validate(async (valid: boolean) => {
    if (!valid) return;
    const id = formData.value.id;
    try {
      if (id) {
        await DictAPI.updateDictData(id, { id, ...formData.value });
        await refreshUpdate();
      } else {
        await DictAPI.createDictData(formData.value);
        await refreshCreate();
      }
      dialogVisible.visible = false;
      await resetForm();
      dictStore.clearDictData();
      if (formData.value.dict_type) {
        await dictStore.getDict([formData.value.dict_type]);
      }
    } catch (error: unknown) {
      console.error(error);
    }
  });
}

function buildDictDataRowActions(row: DictDataTable): TableOperationAction[] {
  const all: TableOperationAction[] = [
    {
      key: "detail",
      label: "详情",
      artType: "view",
      perm: "module_system:dict_data:detail",
      run: () => void handleOpenDialog("detail", row.id),
    },
    {
      key: "edit",
      label: "编辑",
      artType: "edit",
      icon: "ri:edit-2-line",
      perm: "module_system:dict_data:update",
      run: () => void handleOpenDialog("update", row.id),
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      icon: "ri:delete-bin-4-line",
      perm: "module_system:dict_data:delete",
      run: () => {
        if (row.id != null) deleteDictDataRow(row.id);
      },
    },
  ];
  return all.filter((a) => a.perm != null && hasAuth(a.perm));
}

function formatDictDataOperationCell(row: DictDataTable) {
  return renderTableOperationCell(buildDictDataRowActions(row), {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1 dict-data-drawer-actions",
  });
}

async function deleteDictDataRow(id: number) {
  try {
    await ElMessageBox.confirm("确认删除该项数据?", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    await DictAPI.deleteDictData([id]);
    dictStore.clearDictData();
    if (props.dictType) await dictStore.getDict([props.dictType]);
    ElMessage.success("删除成功");
    faTableRef.value?.elTableRef?.clearSelection();
    await refreshRemove();
  } catch {
    // 用户取消
  }
}

async function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  try {
    await ElMessageBox.confirm(`确定删除选中的 ${ids.length} 条数据吗？`, "批量删除", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    batchDeleting.value = true;
    await DictAPI.deleteDictData(ids);
    dictStore.clearDictData();
    if (props.dictType) await dictStore.getDict([props.dictType]);
    ElMessage.success("删除成功");
    faTableRef.value?.elTableRef?.clearSelection();
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
    await ElMessageBox.confirm(`确认${status === "0" ? "启用" : "停用"}该项数据?`, "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    await DictAPI.batchDictData({ ids, status });
    await refreshData();
    dictStore.clearDictData();
    if (props.dictType) await dictStore.getDict([props.dictType]);
  } catch {
    // 用户取消
  }
}

function openExportModal() {
  exportModalVisible.value = true;
}
</script>

<style lang="scss" scoped>
.drawer-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
}

.drawer-table-card {
  flex: 1;
  min-height: 0;
}

.tag-option-preview {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 120px;
  padding: 4px 10px;
  font-size: 12px;
  line-height: 18px;
  text-align: center;
  border: 1px solid transparent;
  border-radius: 4px;
}

.tag-option-preview--default {
  color: var(--el-text-color-regular);
  background: var(--el-fill-color-light);
  border-color: var(--el-border-color-lighter);
}

.crud-dialog-art-form :deep(.el-row > .el-col:last-child) {
  display: none;
}

.crud-dialog-art-form :deep(.el-form-item__content) {
  max-width: 100%;
}
</style>
