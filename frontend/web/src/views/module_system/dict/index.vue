<!-- 字典管理：左侧字典类型列表 + 右侧字典数据面板 -->
<template>
  <div class="fa-full-height">
    <FaWorkbench :side-width="380">
      <template #side>
        <FaSidePanel title="字典类型" class="dict-type-panel">
          <template #search>
            <div class="dict-filter">
              <ElInput
                v-model="searchForm.dict_name"
                size="small"
                placeholder="字典名称"
                clearable
                aria-label="字典名称"
                @keyup.enter="applyDictSearch"
              />
              <ElInput
                v-model="searchForm.dict_type"
                size="small"
                placeholder="字典类型"
                clearable
                aria-label="字典类型"
                @keyup.enter="applyDictSearch"
              />
              <div class="dict-filter-actions">
                <ElButton size="small" text @click="resetDictSearch">重置</ElButton>
                <ElButton size="small" type="primary" @click="applyDictSearch">查询</ElButton>
              </div>
            </div>
          </template>
          <template #actions>
            <ElButton
              v-hasPerm="['module_system:dict_type:create']"
              type="primary"
              size="small"
              plain
              @click="handleAdd"
            >
              新增
            </ElButton>
          </template>
          <div v-if="!data.length" class="dict-type-empty">暂无字典类型</div>
          <div
            v-for="row in data"
            :key="row.id"
            class="dict-type-row"
            :class="{ 'is-active': row.id === currentDictTypeId }"
            @click="handleDictTypeRowClick(row)"
          >
            <div class="min-w-0 flex-1">
              <div class="dict-type-name">{{ row.dict_name }}</div>
              <div class="dict-type-code">{{ row.dict_type }}</div>
            </div>
            <ElDropdown
              trigger="click"
              @command="(cmd) => runDictTypeAction(row, String(cmd))"
              @click.stop
            >
              <button type="button" class="dict-type-more" aria-label="更多操作">
                <ElIcon><FaSvgIcon icon="ri:more-2-fill" /></ElIcon>
              </button>
              <template #dropdown>
                <ElDropdownMenu>
                  <ElDropdownItem
                    v-for="act in buildDictRowActions(row)"
                    :key="act.key"
                    :command="act.key"
                  >
                    {{ act.label }}
                  </ElDropdownItem>
                </ElDropdownMenu>
              </template>
            </ElDropdown>
          </div>
        </FaSidePanel>
      </template>

      <div class="fa-card dict-data-card">
        <DictDataPanel
          :key="currentDictTypeId"
          :dict-type="currentDictType"
          :dict-label="currentDictLabel"
          :dict-type-id="currentDictTypeId"
        />
      </div>
    </FaWorkbench>

    <!-- Dict Type CRUD Dialogs -->
    <FaDialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      :form-mode="dialogVisible.type"
      :confirm-loading="submitLoading"
      @cancel="handleCloseDialog"
      @close="handleCloseDialog"
      @confirm="handleSubmit()"
      size="md"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <FaDescriptions
          :column="4"
          :data="detailFormData"
          :items="dictDetailItems"
          max-height="70vh"
        >
          <template #dict_type="{ row }">
            <FaStatusTag type="primary" :label="(row as unknown as DictTable)?.dict_type" />
          </template>
        </FaDescriptions>
      </template>
      <template v-else>
        <FaForm
          :key="dictFormRenderKey"
          scrollbar
          max-height="70vh"
          ref="dataFormRef"
          v-model="formData"
          :items="dictDialogFormItems"
          :rules="rules"
          label-suffix=":"
          :label-width="96"
          label-position="right"
          :span="24"
          :gutter="16"
          :show-reset="false"
          :show-submit="false"
          class="crud-dialog-art-form"
        >
        </FaForm>
      </template>
    </FaDialog>
  </div>
</template>

<script setup lang="ts">
import { useCrudForm } from "@/hooks/core/useCrudForm";
import DictAPI, { type DictForm, type DictTable } from "@/api/module_system/dict";
import { useDictStore } from "@stores";
import { renderTableOperationCell, resolveStatusColumns, type TableOperationAction } from "@utils";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import FaForm from "@/components/forms/fa-form/index.vue";
import DictDataPanel from "./components/DictDataPanel.vue";
import FaStatusTag from "@/components/display/fa-status-tag/index.vue";
import FaDescriptions from "@/components/display/fa-descriptions/index.vue";

defineOptions({
  name: "Dict",
  inheritAttrs: false,
});

type DictTypeSearchForm = {
  dict_name?: string;
  dict_type?: string;
};

const dictStore = useDictStore();

const searchForm = ref<DictTypeSearchForm>({
  dict_name: undefined,
  dict_type: undefined,
});

const createLoading = ref(false);
const statusUpdating = ref<Set<number>>(new Set());

// ─── 对话框状态 ───
const { dialogVisible } = useCrudDialog();

const detailFormData = ref<DictTable>({});

const dictDetailItems: import("@/components/display/fa-descriptions/index.vue").DescriptionsItem[] =
  [
    { label: "字典名称", prop: "dict_name" },
    { label: "字典类型", prop: "dict_type", slot: "dict_type" },
    {
      label: "状态",
      prop: "status",
      tag: {
        map: { "0": { type: "success", text: "启用" }, "1": { type: "danger", text: "停用" } },
      },
    },
    { label: "描述", prop: "description", span: 4 },
    { label: "创建时间", prop: "created_time" },
    { label: "更新时间", prop: "updated_time" },
  ];

const formData = ref<DictForm>({
  id: undefined,
  dict_name: "",
  dict_type: "",
  status: 0,
  description: undefined,
});

const rules = reactive({
  dict_name: [{ required: true, message: "请输入字典名称", trigger: "blur" }],
  dict_type: [{ required: true, message: "请选择字典类型", trigger: "blur" }],
  status: [{ required: true, message: "请选择字典状态", trigger: "blur" }],
});

const dataFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const dictFormRenderKey = ref(0);

function createInitialFormData(): DictForm {
  return {
    id: undefined,
    dict_name: "",
    dict_type: "",
    status: 0,
    description: undefined,
  };
}

const initialFormData = createInitialFormData();

// ─── CRUD 表单 ───
const { submitLoading, handleCloseDialog, handleOpenDialog, handleSubmit } = useCrudForm<DictForm>({
  formData,
  initialFormData,
  dialogVisible,
  dataFormRef,
  formRenderKey: dictFormRenderKey,
  detailApi: DictAPI.detailDictType,
  createApi: DictAPI.createDictType,
  updateApi: DictAPI.updateDictType,
  titles: { create: "新增字典", update: "修改字典", detail: "字典详情" },
  detailFormData,
  onCreateSuccess: async () => {
    await refreshCreate();
  },
  onUpdateSuccess: async () => {
    await refreshUpdate();
  },
  onSubmitSuccess: async () => {
    dictStore.clearDictData();
    if (formData.value.dict_type) {
      await dictStore.getDict([formData.value.dict_type]);
    }
  },
});

async function handleAdd() {
  createLoading.value = true;
  try {
    await handleOpenDialog("create");
  } finally {
    createLoading.value = false;
  }
}

const dictDialogFormItems = computed<FormItem[]>(() => [
  {
    label: "字典名称",
    key: "dict_name",
    span: 12,
    type: "input",
    props: { placeholder: "请输入字典名称", maxlength: 50 },
  },
  {
    label: "字典类型",
    key: "dict_type",
    span: 12,
    type: "input",
    props: { placeholder: "请输入字典类型", maxlength: 50 },
  },
  {
    label: "状态",
    key: "status",
    span: 12,
    type: "radiogroup",
    props: {
      options: [
        { label: "启用", value: 0 },
        { label: "停用", value: 1 },
      ],
    },
  },
  {
    label: "描述",
    key: "description",
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

const {
  data,
  getData,
  replaceSearchParams,
  refreshData,
  refreshCreate,
  refreshUpdate,
  refreshRemove,
} = useTable({
  core: {
    apiFn: DictAPI.listDictType,
    apiParams: {
      page_no: 1,
      page_size: 100,
    },
    columnsFactory: resolveStatusColumns<DictTable>(() => [
      { type: "globalIndex", width: 56, label: "序号" },
      { prop: "dict_name", label: "字典名称", minWidth: 100, showOverflowTooltip: true },
      {
        prop: "dict_type",
        label: "字典类型",
        minWidth: 120,
        formatter: (row: DictTable) =>
          h(FaStatusTag, { type: "primary", label: row.dict_type ?? "" }),
      },
      {
        prop: "status",
        label: "状态",
        width: 80,
        formatter: (row: DictTable) =>
          h(ElSwitch, {
            modelValue: row.status ?? 0,
            "onUpdate:modelValue": (val: string | number | boolean) =>
              handleDictTypeStatusChange(row.id!, Number(val)),
            activeValue: 0,
            inactiveValue: 1,
            loading: statusUpdating.value.has(row.id!),
            inlinePrompt: true,
          }),
      },
      {
        prop: "operation",
        label: "操作",
        width: 180,
        fixed: "right",
        align: "center",
        formatter: (row: DictTable) => formatDictOperationCell(row),
      },
    ]),
  },
});

// ─── 右侧面板状态 ───
const currentDictType = ref("");
const currentDictLabel = ref("");
const currentDictTypeId = ref(0);
const hasAutoSelected = ref(false);
const selectedDictRowId = ref<number | null>(null);

function handleDictTypeRowClick(row: DictTable) {
  selectedDictRowId.value = row.id ?? null;
  currentDictType.value = row.dict_type || "";
  currentDictLabel.value = row.dict_name || "";
  currentDictTypeId.value = row.id ?? 0;
}

async function applyDictSearch() {
  replaceSearchParams({
    dict_name: searchForm.value.dict_name,
    dict_type: searchForm.value.dict_type,
  } as Record<string, unknown>);
  await getData();
}

function resetDictSearch() {
  searchForm.value = {
    dict_name: undefined,
    dict_type: undefined,
  };
  void applyDictSearch();
}

async function handleOpenDictTypeDetail(id: number) {
  dialogVisible.title = "字典详情";
  dialogVisible.type = "detail";
  const res = await DictAPI.detailDictType(id);
  const data = (res.data?.data ?? {}) as DictTable;
  Object.assign(detailFormData.value, data);
  dialogVisible.visible = true;
}

function buildDictRowActions(row: DictTable): TableOperationAction[] {
  const all: TableOperationAction[] = [
    {
      key: "detail",
      label: "详情",
      artType: "view",
      perm: "module_system:dict_type:detail",
      run: () => void handleOpenDictTypeDetail(row.id!),
    },
    {
      key: "edit",
      label: "编辑",
      artType: "edit",
      icon: "ri:edit-2-line",
      perm: "module_system:dict_type:update",
      run: () => void handleOpenDialog("update", row.id),
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      icon: "ri:delete-bin-4-line",
      perm: "module_system:dict_type:delete",
      run: () => {
        if (row.id != null) deleteDictTypeRow(row.id, row.dict_name ?? "");
      },
    },
  ];
  return all;
}

function runDictTypeAction(row: DictTable, key: string): void {
  const action = buildDictRowActions(row).find((a) => a.key === key);
  action?.run();
  void action;
}

function formatDictOperationCell(row: DictTable) {
  return renderTableOperationCell(buildDictRowActions(row), {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1 dict-table-actions",
  });
}

async function deleteDictTypeRow(id: number, name: string) {
  try {
    await confirmDelete(`确定删除「${name}」吗？`);
    await DictAPI.deleteDictType([id]);
    dictStore.clearDictData();
    const dictTypes = Object.keys(dictStore.dictData);
    if (dictTypes.length > 0) await dictStore.getDict(dictTypes);

    // 如果删的是当前选中的行，清空右侧面板
    if (id === currentDictTypeId.value) {
      currentDictTypeId.value = 0;
      currentDictType.value = "";
      currentDictLabel.value = "";
      selectedDictRowId.value = null;
    }

    await refreshRemove();
  } catch {
    // 用户取消
  }
}

async function handleDictTypeStatusChange(id: number, newStatus: number) {
  statusUpdating.value = new Set([...statusUpdating.value, id]);
  try {
    await DictAPI.batchDictType({ ids: [id], status: newStatus });
    await refreshData();
    dictStore.clearDictData();
    const dictTypes = Object.keys(dictStore.dictData);
    if (dictTypes.length > 0) await dictStore.getDict(dictTypes);
  } catch {
    await refreshData();
  } finally {
    const next = new Set(statusUpdating.value);
    next.delete(id);
    statusUpdating.value = next;
  }
}

// 初始加载后自动选中第一行
watch(data, (newData) => {
  if (newData && newData.length > 0 && !hasAutoSelected.value) {
    const firstRow = newData[0]!;
    handleDictTypeRowClick(firstRow);
    hasAutoSelected.value = true;
  }
  if (newData && newData.length === 0) {
    currentDictTypeId.value = 0;
    currentDictType.value = "";
    currentDictLabel.value = "";
    selectedDictRowId.value = null;
  }
});
</script>

<style lang="scss" scoped>
.dict-type-panel {
  width: 100%;
  height: 100%;
}

.dict-data-card {
  box-sizing: border-box;
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
  height: 100%;
  padding: 12px 16px;
}

/* 让字典数据面板和内部表格填满右侧卡片，与常规列表页保持一致的固定表格区 */
.dict-data-card :deep(.dict-data-panel) {
  flex: 1;
  min-height: 0;
}

/* 面板内筛选 */
.dict-filter {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.dict-filter-actions {
  display: flex;
  gap: 6px;
  justify-content: flex-end;
}

/* 字典类型列表（左栏） */
.dict-type-row {
  display: flex;
  gap: 8px;
  align-items: center;
  padding: 8px;
  cursor: pointer;
  border-radius: var(--fa-radius-sm, 8px);
}

.dict-type-row:hover {
  background: var(--el-fill-color-light);
}

.dict-type-row.is-active {
  background: var(--el-color-primary-light-9);
}

.dict-type-name {
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 13px;
  color: var(--el-text-color-primary);
  white-space: nowrap;
}

.dict-type-code {
  margin-top: 2px;
  overflow: hidden;
  text-overflow: ellipsis;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 12px;
  color: var(--el-text-color-secondary);
  white-space: nowrap;
}

.dict-type-more {
  display: inline-flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  color: var(--el-text-color-secondary);
  cursor: pointer;
  background: transparent;
  border: 0;
  border-radius: var(--fa-radius-xs, 6px);
  opacity: 0;
}

.dict-type-row:hover .dict-type-more,
.dict-type-row.is-active .dict-type-more {
  opacity: 1;
}

.dict-type-more:hover {
  color: var(--el-color-primary);
  background: var(--el-fill-color);
}

.dict-type-empty {
  padding: 12px 8px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}
</style>
