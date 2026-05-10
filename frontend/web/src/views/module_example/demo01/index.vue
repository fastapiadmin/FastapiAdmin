<!-- 示例01 CRUD：与 demo 同一套 Art 布局；权限与接口为 module_example:demo01 / Demo01API -->
<template>
  <div class="art-full-height">
    <ArtSearchBarWithAudit
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="demo01BusinessSearchItems"
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
            :perm-create="['module_example:demo01:create']"
            :perm-import="['module_example:demo01:import']"
            :perm-export="['module_example:demo01:export']"
            :perm-delete="['module_example:demo01:delete']"
            :perm-patch="['module_example:demo01:patch']"
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
        :pagination="pagination"
        @selection-change="onTableSelectionChange"
        @pagination:size-change="handleSizeChange"
        @pagination:current-change="handleCurrentChange"
      />
    </ElCard>

    <ArtDialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      width="768px"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      @close="handleCloseDialog"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <ElScrollbar max-height="70vh" :view-style="{ overflowX: 'hidden' }">
          <ElDescriptions :column="2" border>
            <ElDescriptionsItem label="名称" :span="2">
              {{ detailFormData.name }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="UUID" :span="2">
              {{ detailFormData.uuid }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="状态" :span="2">
              <ElTag :type="detailFormData.status === '0' ? 'success' : 'danger'">
                {{ detailFormData.status === "0" ? "正常" : "停用" }}
              </ElTag>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="描述" :span="2">
              {{ detailFormData.description }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="创建人" :span="2">
              {{ detailFormData.created_by?.name ?? "—" }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="更新人" :span="2">
              {{ detailFormData.updated_by?.name ?? "—" }}
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
          <ArtForm
            :key="demo01FormRenderKey"
            ref="dataFormRef"
            v-model="formData"
            :items="demo01DialogFormItems"
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
            <template #status>
              <ElRadioGroup v-model="formData.status">
                <ElRadio value="0">正常</ElRadio>
                <ElRadio value="1">停用</ElRadio>
              </ElRadioGroup>
            </template>
          </ArtForm>
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
      :content-config="demo01ImportContentConfig"
      default-template-file-name="demo01_import_template.xlsx"
      @upload="handleCrudImportUpload"
    />

    <ArtExportDialog
      v-model="exportModalVisible"
      :content-config="demo01ExportContentConfig"
      :query-params="exportQueryParams"
      :page-data="data"
      :selection-data="selectedRows"
    />
  </div>
</template>

<script setup lang="ts">
import { h, computed, ref, reactive } from "vue";
import { useAuth } from "@/hooks/core/useAuth";
import { renderTableOperationCell, type TableOperationAction } from "@utils/table";
import { useTable } from "@/hooks/core/useTable";
import ArtTableHeaderLeft from "@/components/Core/tables/art-table-header-left/index.vue";
import ArtImportDialog from "@/components/Core/modal/art-import-dialog/index.vue";
import ArtExportDialog from "@/components/Core/modal/art-export-dialog/index.vue";
import type { IContentConfig, IObject } from "@/components/Core/modal/types";
import ArtSearchBarWithAudit from "@/components/Core/forms/art-search-bar/ArtSearchBarWithAudit.vue";
import type { AuditSearchFormParams } from "@/components/Core/forms/art-search-bar/auditSearchFormItems";
import ArtDialog from "@/components/Core/modal/art-dialog/index.vue";
import ArtForm from "@/components/Core/forms/art-form/index.vue";
import type { FormItem } from "@/components/Core/forms/art-form/index.vue";
import type { ColumnOption } from "@/types/component";
import Demo01API, {
  type Demo01Form,
  type Demo01PageQuery,
  type Demo01Table,
} from "@/api/module_example/demo01";
import { ElMessage, ElMessageBox, ElTag } from "element-plus";
import { ResultEnum } from "@/enums/api/result.enum";

defineOptions({
  name: "ModuleExampleDemo01",
  inheritAttrs: false,
});

const { hasAuth } = useAuth();

type Demo01SearchFormParams = {
  name?: string;
  description?: string;
  status?: string;
} & AuditSearchFormParams;

function normalizeDemo01Query(params: Record<string, unknown>): Demo01PageQuery {
  const p = { ...params } as Record<string, unknown>;
  if (Array.isArray(p.created_time) && p.created_time.length === 0) p.created_time = undefined;
  if (Array.isArray(p.updated_time) && p.updated_time.length === 0) p.updated_time = undefined;
  return p as unknown as Demo01PageQuery;
}

const searchForm = ref<Demo01SearchFormParams>({
  name: undefined,
  description: undefined,
  status: undefined,
  created_id: undefined,
  updated_id: undefined,
  created_time: [],
  updated_time: [],
});

const showSearchBar = ref(true);

const searchBarRef = ref<InstanceType<typeof ArtSearchBarWithAudit> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const statusOptions = ref([
  { label: "正常", value: "0" },
  { label: "停用", value: "1" },
]);

const demo01BusinessSearchItems = computed(() => [
  {
    label: "名称",
    key: "name",
    type: "input",
    placeholder: "请输入名称",
    clearable: true,
    span: 6,
  },
  {
    label: "描述",
    key: "description",
    type: "input",
    placeholder: "请输入描述",
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
const selectedRows = ref<Demo01Table[]>([]);
const selectedIds = computed(() =>
  selectedRows.value.map((r) => r.id).filter((id): id is number => id != null && !Number.isNaN(id))
);
const batchDeleting = ref(false);

function onTableSelectionChange(rows: Demo01Table[]) {
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
    apiFn: Demo01API.getDemo01List,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: (): ColumnOption<Demo01Table>[] => [
      { type: "selection", width: 48, fixed: "left" },
      { prop: "name", label: "名称", minWidth: 120, showOverflowTooltip: true },
      { prop: "uuid", label: "UUID", minWidth: 168, showOverflowTooltip: true },
      {
        prop: "status",
        label: "状态",
        width: 88,
        formatter: (row: Demo01Table) => {
          const ok = row.status === "0";
          const cfg = ok
            ? { type: "success" as const, text: "正常" }
            : { type: "info" as const, text: "停用" };
          return h(ElTag, { type: cfg.type }, () => cfg.text);
        },
      },
      { prop: "description", label: "描述", minWidth: 140, showOverflowTooltip: true },
      { prop: "created_time", label: "创建时间", width: 168, showOverflowTooltip: true },
      { prop: "updated_time", label: "更新时间", width: 168, showOverflowTooltip: true },
      {
        prop: "created_by",
        label: "创建人",
        minWidth: 100,
        formatter: (row: Demo01Table) => row.created_by?.name ?? "—",
      },
      {
        prop: "updated_by",
        label: "更新人",
        minWidth: 100,
        formatter: (row: Demo01Table) => row.updated_by?.name ?? "—",
      },
      {
        prop: "operation",
        label: "操作",
        width: 220,
        fixed: "right",
        align: "right",
        formatter: (row: Demo01Table) => formatDemo01OperationCell(row),
      },
    ],
  },
});

const demo01CrudCols = computed(() =>
  columns.value.map((c: ColumnOption<Demo01Table>) => {
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
  return normalizeDemo01Query(sp);
});

const demo01ImportContentConfig = computed<IContentConfig>(() => ({
  permPrefix: "module_example:demo01",
  cols: demo01CrudCols.value,
  indexAction: async () => ({}) as Demo01Table[],
  importTemplate: () => Demo01API.downloadDemo01Template(),
}));

const demo01ExportContentConfig = computed(() => ({
  permPrefix: "module_example:demo01",
  cols: demo01CrudCols.value,
  exportsBlobAction: async (params: IObject) => {
    const merged = normalizeDemo01Query({
      ...(exportQueryParams.value as unknown as Record<string, unknown>),
      ...params,
    } as Record<string, unknown>);
    const res = await Demo01API.exportDemo01(merged);
    return res.data as Blob;
  },
}));

const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

const detailFormData = ref<Demo01Table>({});

const formData = reactive<Demo01Form>({
  id: undefined,
  name: "",
  status: "0",
  description: "",
});

const rules = reactive({
  name: [{ required: true, message: "请输入名称", trigger: "blur" }],
  status: [{ required: true, message: "请选择状态", trigger: "blur" }],
});

const dataFormRef = ref<InstanceType<typeof ArtForm> | null>(null);
const demo01FormRenderKey = ref(0);

const demo01DialogFormItems = computed<FormItem[]>(() => [
  {
    label: "名称",
    key: "name",
    type: "input",
    span: 24,
    props: { placeholder: "请输入名称", clearable: true },
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
    props: { type: "textarea", rows: 4, placeholder: "请输入描述" },
  },
]);

const importModalVisible = ref(false);
const exportModalVisible = ref(false);

const initialFormData: Demo01Form = {
  id: undefined,
  name: "",
  status: "0",
  description: "",
};

const handleSearch = async (params: Demo01SearchFormParams) => {
  await searchBarRef.value?.validate();
  replaceSearchParams({
    name: params.name,
    description: params.description,
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
    description: undefined,
    status: undefined,
    created_id: undefined,
    updated_id: undefined,
    created_time: [],
    updated_time: [],
  };
  await resetSearchParams();
};

function buildDemo01RowActions(row: Demo01Table): TableOperationAction[] {
  const all: TableOperationAction[] = [
    {
      key: "detail",
      label: "详情",
      artType: "view",
      icon: "ri:file-list-3-line",
      perm: "module_example:demo01:detail",
      run: () => void openDetailDialog(row),
    },
    {
      key: "edit",
      label: "编辑",
      artType: "edit",
      icon: "ri:edit-2-line",
      perm: "module_example:demo01:update",
      run: () => void openEditDialog("edit", row),
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      icon: "ri:delete-bin-4-line",
      perm: "module_example:demo01:delete",
      run: () => deleteDemo01Row(row),
    },
  ];
  return all.filter((a) => a.perm != null && hasAuth(a.perm));
}

function formatDemo01OperationCell(row: Demo01Table) {
  return renderTableOperationCell(buildDemo01RowActions(row), {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1 demo01-table-actions",
  });
}

async function openDetailDialog(row: Demo01Table) {
  if (!row.id) return;
  const response = await Demo01API.getDemo01Detail(row.id);
  dialogVisible.type = "detail";
  dialogVisible.title = "详情";
  detailFormData.value = response.data.data ?? { ...row };
  dialogVisible.visible = true;
}

async function openEditDialog(type: "add" | "edit", row?: Demo01Table) {
  dialogVisible.type = type === "add" ? "create" : "update";
  if (type === "add") {
    dialogVisible.title = "新增示例01";
    Object.assign(formData, initialFormData);
    formData.id = undefined;
  } else if (row?.id) {
    dialogVisible.title = "修改";
    const response = await Demo01API.getDemo01Detail(row.id);
    Object.assign(formData, response.data.data);
  }
  demo01FormRenderKey.value += 1;
  dialogVisible.visible = true;
}

async function resetForm() {
  dataFormRef.value?.ref?.resetFields();
  dataFormRef.value?.ref?.clearValidate();
  Object.assign(formData, initialFormData);
}

async function handleCloseDialog() {
  dialogVisible.visible = false;
  await resetForm();
}

async function handleSubmit() {
  dataFormRef.value?.validate(async (valid: boolean) => {
    if (!valid) return;
    const id = formData.id;
    try {
      if (id) {
        await Demo01API.updateDemo01(id, { id, ...formData });
        await refreshUpdate();
      } else {
        await Demo01API.createDemo01(formData);
        await refreshCreate();
      }
      dialogVisible.visible = false;
      await resetForm();
    } catch (error: unknown) {
      console.error(error);
    }
  });
}

const deleteDemo01Row = (row: Demo01Table) => {
  if (!row.id) return;
  ElMessageBox.confirm(`确定删除「${row.name ?? row.id}」吗？此操作不可恢复！`, "删除确认", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await Demo01API.deleteDemo01([row.id!]);
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
        await Demo01API.deleteDemo01(ids);
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
      await Demo01API.batchDemo01({ ids, status });
      ElMessage.success("操作成功");
      artTableRef.value?.elTableRef?.clearSelection();
      await refreshData();
    })
    .catch(() => {});
}

function openImportModal() {
  importModalVisible.value = true;
}

function handleCrudImportUpload(formDataUpload: FormData) {
  Demo01API.importDemo01(formDataUpload)
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

<style scoped lang="scss">
.crud-dialog-art-form :deep(.el-row > .el-col:last-child) {
  display: none;
}

.crud-dialog-art-form :deep(.el-form-item__content) {
  max-width: 100%;
}
</style>
