<!-- 字典数据 -->
<template>
  <EnhancedDrawer
    v-model="drawerVisible"
    :title="'【' + dictLabel + '】字典数据'"
    direction="rtl"
    :size="drawerSize"
  >
    <div class="drawer-content">
      <CrudSearch
        ref="searchRef"
        :search-config="searchConfig"
        @query-click="handleQueryClick"
        @reset-click="handleResetClick"
      />

      <CrudContent ref="contentRef" :content-config="contentConfig">
        <template #toolbar="{ toolbarRight, onToolbar, removeIds, cols }">
          <CrudToolbarLeft
            :remove-ids="removeIds"
            :perm-create="['module_system:dict_data:create']"
            :perm-delete="['module_system:dict_data:delete']"
            :perm-patch="['module_system:dict_data:patch']"
            @add="handleOpenDialog('create')"
            @delete="onToolbar('delete')"
            @more="handleMoreClick"
          />
          <div class="data-table__toolbar--right">
            <CrudToolbarActions :buttons="toolbarRight" :cols="cols" :on-toolbar="onToolbar">
              <template #prepend>
                <el-tooltip content="导出">
                  <el-button
                    v-hasPerm="['module_system:dict_data:export']"
                    type="warning"
                    icon="download"
                    circle
                    @click="handleOpenExportsModal"
                  />
                </el-tooltip>
              </template>
            </CrudToolbarActions>
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
                v-if="contentCols.find((col) => col.prop === 'dict_label')?.show"
                label="标签"
                prop="dict_label"
                min-width="150"
                show-overflow-tooltip
              />
              <el-table-column
                v-if="contentCols.find((col) => col.prop === 'status')?.show"
                label="状态"
                prop="status"
                min-width="100"
                show-overflow-tooltip
              >
                <template #default="scope">
                  <el-tag :type="scope.row.status === '0' ? 'success' : 'danger'">
                    {{ scope.row.status === "0" ? "启用" : "停用" }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column
                v-if="contentCols.find((col) => col.prop === 'dict_type')?.show"
                label="类型"
                prop="dict_type"
                min-width="180"
                show-overflow-tooltip
              >
                <template #default="scope">
                  <el-tag type="primary">{{ scope.row.dict_type }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column
                v-if="contentCols.find((col) => col.prop === 'dict_value')?.show"
                label="值"
                prop="dict_value"
                min-width="100"
                show-overflow-tooltip
              />
              <el-table-column
                v-if="contentCols.find((col) => col.prop === 'css_class')?.show"
                label="样式属性"
                prop="css_class"
                min-width="100"
                show-overflow-tooltip
              />
              <el-table-column
                v-if="contentCols.find((col) => col.prop === 'list_class')?.show"
                label="列表类样式"
                prop="list_class"
                min-width="100"
                show-overflow-tooltip
              />
              <el-table-column
                v-if="contentCols.find((col) => col.prop === 'dict_sort')?.show"
                label="排序"
                prop="dict_sort"
                min-width="60"
              />
              <el-table-column
                v-if="contentCols.find((col) => col.prop === 'is_default')?.show"
                label="是否默认"
                prop="is_default"
                min-width="100"
              >
                <template #default="scope">
                  <el-tag v-if="scope.row.is_default" type="success">是</el-tag>
                  <el-tag v-else type="danger">否</el-tag>
                </template>
              </el-table-column>
              <el-table-column
                v-if="contentCols.find((col) => col.prop === 'description')?.show"
                label="描述"
                prop="description"
                min-width="100"
                show-overflow-tooltip
              />
              <el-table-column
                v-if="contentCols.find((col) => col.prop === 'created_time')?.show"
                label="创建时间"
                prop="created_time"
                min-width="200"
                sortable
              />
              <el-table-column
                v-if="contentCols.find((col) => col.prop === 'updated_time')?.show"
                label="更新时间"
                prop="updated_time"
                min-width="200"
                sortable
              />
              <el-table-column
                v-if="contentCols.find((col) => col.prop === 'operation')?.show"
                fixed="right"
                label="操作"
                align="center"
                min-width="200"
              >
                <template #default="scope">
                  <el-button
                    v-hasPerm="['module_system:dict_data:detail']"
                    type="info"
                    size="small"
                    link
                    icon="View"
                    @click="handleOpenDialog('detail', scope.row.id)"
                  >
                    详情
                  </el-button>
                  <el-button
                    v-hasPerm="['module_system:dict_data:update']"
                    type="primary"
                    size="small"
                    link
                    icon="edit"
                    @click="handleOpenDialog('update', scope.row.id)"
                  >
                    编辑
                  </el-button>
                  <el-button
                    v-hasPerm="['module_system:dict_data:delete']"
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
      </CrudContent>

      <EnhancedDialog
        v-model="dialogVisible.visible"
        :title="dialogVisible.title"
        @close="handleCloseDialog"
      >
        <template v-if="dialogVisible.type === 'detail'">
          <el-descriptions :column="4" border>
            <el-descriptions-item label="数据标签" :span="2">
              {{ detailFormData.dict_label }}
            </el-descriptions-item>
            <el-descriptions-item label="数据类型" :span="2">
              {{ detailFormData.dict_type }}
            </el-descriptions-item>
            <el-descriptions-item label="数据值" :span="2">
              {{ detailFormData.dict_value }}
            </el-descriptions-item>
            <el-descriptions-item label="样式属性" :span="2">
              {{ detailFormData.css_class }}
            </el-descriptions-item>
            <el-descriptions-item label="列表样式属性" :span="2">
              {{ detailFormData.list_class }}
            </el-descriptions-item>
            <el-descriptions-item label="是否默认" :span="2">
              <el-tag v-if="detailFormData.is_default" type="success">是</el-tag>
              <el-tag v-else type="danger">否</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="状态" :span="2">
              <el-tag v-if="detailFormData.status === '0'" type="success">启用</el-tag>
              <el-tag v-else type="danger">停用</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="排序" :span="2">
              {{ detailFormData.dict_sort }}
            </el-descriptions-item>
            <el-descriptions-item label="描述" :span="2">
              {{ detailFormData.description }}
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
          >
            <el-form-item label="数据类型" prop="dict_type">
              <el-input
                v-model="formData.dict_type"
                placeholder="请输入数据类型"
                :maxlength="50"
                :disabled="true"
              />
            </el-form-item>
            <el-form-item label="数据标签" prop="dict_label">
              <el-input
                v-model="formData.dict_label"
                placeholder="请输入数据标签"
                :maxlength="255"
              />
            </el-form-item>
            <el-form-item label="数据值" prop="dict_value">
              <el-input v-model="formData.dict_value" placeholder="请输入数据值" :maxlength="255" />
            </el-form-item>
            <el-form-item label="样式属性" prop="css_class">
              <el-select
                v-model="formData.css_class"
                placeholder="请选择常用颜色或输入自定义"
                clearable
                filterable
                allow-create
                default-first-option
              >
                <el-option value="primary" label="主要(primary)">
                  <span class="tag-option-preview" :style="getTagPreviewStyle('primary')">
                    主要(primary)
                  </span>
                </el-option>
                <el-option value="success" label="成功(success)">
                  <span class="tag-option-preview" :style="getTagPreviewStyle('success')">
                    成功(success)
                  </span>
                </el-option>
                <el-option value="warning" label="警告(warning)">
                  <span class="tag-option-preview" :style="getTagPreviewStyle('warning')">
                    警告(warning)
                  </span>
                </el-option>
                <el-option value="danger" label="危险(danger)">
                  <span class="tag-option-preview" :style="getTagPreviewStyle('danger')">
                    危险(danger)
                  </span>
                </el-option>
                <el-option value="info" label="信息(info)">
                  <span class="tag-option-preview" :style="getTagPreviewStyle('info')">
                    信息(info)
                  </span>
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="列表类样式" prop="list_class">
              <el-select v-model="formData.list_class" placeholder="请选择列表类样式" clearable>
                <el-option value="default" label="默认(default)">
                  <span class="tag-option-preview tag-option-preview--default">默认(default)</span>
                </el-option>
                <el-option value="primary" label="主要(primary)">
                  <span class="tag-option-preview" :style="getTagPreviewStyle('primary')">
                    主要(primary)
                  </span>
                </el-option>
                <el-option value="success" label="成功(success)">
                  <span class="tag-option-preview" :style="getTagPreviewStyle('success')">
                    成功(success)
                  </span>
                </el-option>
                <el-option value="warning" label="警告(warning)">
                  <span class="tag-option-preview" :style="getTagPreviewStyle('warning')">
                    警告(warning)
                  </span>
                </el-option>
                <el-option value="danger" label="危险(danger)">
                  <span class="tag-option-preview" :style="getTagPreviewStyle('danger')">
                    危险(danger)
                  </span>
                </el-option>
                <el-option value="info" label="信息(info)">
                  <span class="tag-option-preview" :style="getTagPreviewStyle('info')">
                    信息(info)
                  </span>
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="是否默认" prop="is_default">
              <el-radio-group v-model="formData.is_default">
                <el-radio :value="true">是</el-radio>
                <el-radio :value="false">否</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="排序" prop="dict_sort">
              <el-input-number v-model="formData.dict_sort" controls-position="right" :min="1" />
            </el-form-item>
            <el-form-item label="状态" prop="status">
              <el-switch
                v-model="formData.status"
                inline-prompt
                :active-value="'0'"
                :inactive-value="'1'"
              />
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
            <el-button v-if="dialogVisible.type !== 'detail'" type="primary" @click="handleSubmit">
              确定
            </el-button>
            <el-button v-else type="primary" @click="handleCloseDialog">确定</el-button>
          </div>
        </template>
      </EnhancedDialog>

      <CrudExportModal
        v-model="exportsDialogVisible"
        :content-config="curdContentConfig"
        :query-params="exportQueryParams"
        :page-data="exportPageData"
        :selection-data="exportSelectionData"
      />
    </div>
  </EnhancedDrawer>
</template>

<script setup lang="ts">
import DictAPI, { DictDataTable, DictDataForm, DictDataPageQuery } from "@/api/module_system/dict";
import { useDictStore } from "@/store";
import { useAppStore } from "@/store/modules/app.store";
import { DeviceEnum } from "@/enums/settings/device.enum";
import CrudExportModal from "@/components/CURD/CrudExportModal.vue";
import CrudToolbarLeft from "@/components/CURD/CrudToolbarLeft.vue";
import { CrudToolbarActions } from "@/components/Crud";
import CrudSearch from "@/components/CURD/CrudSearch.vue";
import CrudContent from "@/components/CURD/CrudContent.vue";
import EnhancedDialog from "@/components/Core/overlays/EnhancedDialog.vue";
import EnhancedDrawer from "@/components/Core/overlays/EnhancedDrawer.vue";
import type { ISearchConfig, IContentConfig, IObject } from "@/components/Crud/types";
import { useCrudList } from "@/components/Crud/useCrudList";
import { computed, ref, reactive, unref } from "vue";
import { fetchAllPages } from "@/utils/fetchAllPages";

const props = defineProps({
  dictType: {
    type: String,
    required: true,
  },
  dictLabel: {
    type: String,
    required: true,
  },
  dictTypeId: {
    type: Number,
    required: true,
  },
});

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

const drawerVisible = defineModel<boolean>({ required: true });

const appStore = useAppStore();
const dictStore = useDictStore();
const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "80%" : "60%"));

const { searchRef, contentRef, handleQueryClick, handleResetClick, refreshList } = useCrudList();
const dataFormRef = ref();

const searchConfig = reactive<ISearchConfig>({
  permPrefix: "module_system:dict_data",
  colon: true,
  isExpandable: true,
  showNumber: 2,
  form: { labelWidth: "auto" },
  formItems: [
    {
      prop: "dict_label",
      label: "字典数据标签",
      type: "input",
      attrs: { placeholder: "请输入字典标签", clearable: true },
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
      prop: "created_time",
      label: "创建时间",
      type: "date-picker",
      attrs: {
        type: "datetimerange",
        rangeSeparator: "至",
        startPlaceholder: "开始日期",
        endPlaceholder: "结束日期",
        format: "YYYY-MM-DD HH:mm:ss",
        valueFormat: "YYYY-MM-DD HH:mm:ss",
        style: { width: "340px" },
      },
    },
  ],
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
  { prop: "dict_label", label: "标签", show: true },
  { prop: "status", label: "状态", show: true },
  { prop: "dict_type", label: "类型", show: true },
  { prop: "dict_value", label: "值", show: true },
  { prop: "css_class", label: "样式属性", show: true },
  { prop: "list_class", label: "列表类样式", show: true },
  { prop: "dict_sort", label: "排序", show: true },
  { prop: "is_default", label: "是否默认", show: true },
  { prop: "description", label: "描述", show: true },
  { prop: "created_time", label: "创建时间", show: true },
  { prop: "updated_time", label: "更新时间", show: true },
  { prop: "operation", label: "操作", show: true },
]);

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

function mergeDictQuery(params: IObject): DictDataPageQuery {
  return {
    ...params,
    dict_type: props.dictType,
    dict_type_id: props.dictTypeId,
  } as DictDataPageQuery;
}

const contentConfig = reactive<IContentConfig<DictDataPageQuery>>({
  permPrefix: "module_system:dict_data",
  pk: "id",
  cols: contentCols as IContentConfig["cols"],
  hideColumnFilter: false,
  toolbar: [],
  defaultToolbar: ["refresh", "filter"],
  pagination: {
    pageSize: 10,
    pageSizes: [10, 20, 30, 50],
  },
  request: { page_no: "page_no", page_size: "page_size" },
  indexAction: async (params) => {
    const res = await DictAPI.listDictData(mergeDictQuery(params as IObject));
    return {
      total: res.data.data.total,
      list: res.data.data.items,
    };
  },
  deleteAction: async (ids) => {
    await DictAPI.deleteDictData(
      ids
        .split(",")
        .map((s) => Number(s.trim()))
        .filter((n) => !Number.isNaN(n))
    );
    dictStore.clearDictData();
    if (props.dictType) {
      await dictStore.getDict([props.dictType]);
    }
  },
  deleteConfirm: {
    title: "警告",
    message: "确认删除该项数据?",
    type: "warning",
  },
});

const detailFormData = ref<DictDataTable>({});

const formData = reactive<DictDataForm>({
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

const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

const rules = reactive({
  dict_label: [{ required: true, message: "请输入字典标签", trigger: "blur" }],
  dict_type: [{ required: true, message: "请输入字典类型", trigger: "blur" }],
  dict_value: [{ required: true, message: "请输入字典键值", trigger: "blur" }],
  status: [{ required: true, message: "请选择状态", trigger: "blur" }],
  dict_sort: [{ required: true, message: "请输入排序", trigger: "blur" }],
  is_default: [{ required: true, message: "请选择是否默认", trigger: "blur" }],
});

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

const exportsDialogVisible = ref(false);

const exportQueryParams = computed(() => mergeDictQuery(searchRef.value?.getQueryParams() ?? {}));

const exportPageData = computed(() => {
  const pd = contentRef.value?.pageData;
  return (unref(pd) ?? []) as DictDataTable[];
});

const exportSelectionData = computed(
  () => (contentRef.value?.getSelectionData() ?? []) as DictDataTable[]
);

const exportColumns = [
  { prop: "dict_label", label: "数据标签" },
  { prop: "dict_type", label: "数据类型" },
  { prop: "dict_value", label: "数据值" },
  { prop: "css_class", label: "样式属性" },
  { prop: "list_class", label: "列表类样式" },
  { prop: "dict_sort", label: "排序" },
  { prop: "is_default", label: "是否默认" },
  { prop: "status", label: "状态" },
  { prop: "description", label: "描述" },
  { prop: "created_time", label: "创建时间" },
  { prop: "updated_time", label: "更新时间" },
];

const curdContentConfig = {
  permPrefix: "module_system:dict_data",
  cols: exportColumns as any,
  exportsAction: async (params: any) => {
    const query: Record<string, unknown> = { ...mergeDictQuery(params) };
    return fetchAllPages({
      initialQuery: query,
      fetchPage: async (q) => {
        const res = await DictAPI.listDictData(q as unknown as DictDataPageQuery);
        return {
          total: res.data?.data?.total ?? 0,
          list: res.data?.data?.items ?? [],
        };
      },
    });
  },
} as unknown as IContentConfig;

function handleOpenExportsModal() {
  exportsDialogVisible.value = true;
}

function handleRowDelete(id: number) {
  contentRef.value?.handleDelete(id);
}

async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  Object.assign(formData, { ...initialFormData, dict_type_id: props.dictTypeId });
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
      Object.assign(detailFormData.value, response.data.data);
    } else if (type === "update") {
      dialogVisible.title = "修改字典数据";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增字典数据";
    Object.assign(formData, initialFormData);
    formData.dict_type = props.dictType;
    formData.status = "0";
    formData.id = undefined;
    formData.dict_type_id = props.dictTypeId;
  }
  dialogVisible.visible = true;
}

async function handleSubmit() {
  dataFormRef.value.validate(async (valid: any) => {
    if (valid) {
      const id = formData.id;
      try {
        if (id) {
          await DictAPI.updateDictData(id, { id, ...formData });
        } else {
          await DictAPI.createDictData(formData);
        }
        dialogVisible.visible = false;
        await resetForm();
        refreshList();
        dictStore.clearDictData();
        if (formData.dict_type) {
          await dictStore.getDict([formData.dict_type]);
        }
      } catch (error: any) {
        console.error(error);
      }
    }
  });
}

async function handleMoreClick(status: string) {
  const rows = contentRef.value?.getSelectionData() as DictDataTable[] | undefined;
  const ids = (rows ?? []).map((r) => r.id).filter((id): id is number => id != null);
  if (!ids.length) {
    ElMessage.warning("请先选择要操作的数据");
    return;
  }
  ElMessageBox.confirm(`确认${status === "0" ? "启用" : "停用"}该项数据?`, "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        await DictAPI.batchDictData({ ids, status });
        refreshList();
        dictStore.clearDictData();
        if (props.dictType) {
          await dictStore.getDict([props.dictType]);
        }
      } catch (error: any) {
        console.error(error);
      }
    })
    .catch(() => {
      ElMessageBox.close();
    });
}
</script>

<style lang="scss" scoped>
.drawer-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
}

.drawer-content :deep(.el-card.data-table) {
  flex: 1;
  min-height: 0;
  margin-top: 16px;
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
</style>
