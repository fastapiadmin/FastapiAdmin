<!-- 字典 -->
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
      @add-click="handleOpenDialog('create')"
    >
      <!-- 与 PageContent 默认结构一致：不再套一层 data-table__toolbar（外层已由组件提供） -->
      <template #toolbar="{ toolbarRight, onToolbar, removeIds, cols }">
        <CrudToolbarLeft
          :remove-ids="removeIds"
          :perm-create="['module_system:dict_type:create']"
          :perm-delete="['module_system:dict_type:delete']"
          :perm-patch="['module_system:dict_type:patch']"
          @add="handleOpenDialog('create')"
          @delete="onToolbar('delete')"
          @more="handleMoreClick"
        />
        <div class="data-table__toolbar--right">
          <CrudToolbarRight :buttons="toolbarRight" :cols="cols" :on-toolbar="onToolbar">
            <template #prepend>
              <el-tooltip content="导出">
                <el-button
                  v-hasPerm="['module_system:dict_type:export']"
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
              v-if="contentCols.find((col) => col.prop === 'dict_name')?.show"
              key="dict_name"
              label="字典名称"
              prop="dict_name"
              min-width="140"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'dict_type')?.show"
              key="dict_type"
              label="字典类型"
              prop="dict_type"
              min-width="180"
            >
              <template #default="scope">
                <el-tag type="primary">{{ scope.row.dict_type }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'status')?.show"
              key="status"
              label="状态"
              prop="status"
              min-width="80"
            >
              <template #default="scope">
                <el-tag :type="scope.row.status === '0' ? 'success' : 'danger'">
                  {{ scope.row.status === '0' ? '启用' : '停用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'description')?.show"
              key="description"
              label="描述"
              prop="description"
              min-width="140"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'created_time')?.show"
              key="created_time"
              label="创建时间"
              prop="created_time"
              min-width="200"
              sortable
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'updated_time')?.show"
              key="updated_time"
              label="更新时间"
              prop="updated_time"
              min-width="200"
              sortable
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'operation')?.show"
              fixed="right"
              label="操作"
              align="center"
              min-width="260"
            >
              <template #default="scope">
                <el-button
                  v-hasPerm="['module_system:dict_data:query']"
                  type="warning"
                  size="small"
                  link
                  icon="Document"
                  @click="handleDictDataDrawer(scope.row)"
                >
                  字典
                </el-button>
                <el-button
                  v-hasPerm="['module_system:dict_type:detail']"
                  type="info"
                  size="small"
                  link
                  icon="View"
                  @click="handleOpenDialog('detail', scope.row.id)"
                >
                  详情
                </el-button>
                <el-button
                  v-hasPerm="['module_system:dict_type:update']"
                  type="primary"
                  size="small"
                  link
                  icon="edit"
                  @click="handleOpenDialog('update', scope.row.id)"
                >
                  编辑
                </el-button>
                <el-button
                  v-hasPerm="['module_system:dict_type:delete']"
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
      @close="handleCloseDialog"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <el-descriptions :column="4" border>
          <el-descriptions-item label="字典名称" :span="2">
            {{ detailFormData.dict_name }}
          </el-descriptions-item>
          <el-descriptions-item label="字典类型" :span="2">
            <el-tag type="primary">{{ detailFormData.dict_type }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态" :span="2">
            <el-tag v-if="detailFormData.status === '0'" type="success">启用</el-tag>
            <el-tag v-else type="danger">停用</el-tag>
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
          <el-form-item label="字典名称" prop="dict_name">
            <el-input v-model="formData.dict_name" placeholder="请输入字典名称" :maxlength="50" />
          </el-form-item>
          <el-form-item label="字典类型" prop="dict_type">
            <el-input v-model="formData.dict_type" placeholder="请输入字典类型" :maxlength="50" />
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
          <el-button v-if="dialogVisible.type !== 'detail'" type="primary" @click="handleSubmit">
            确定
          </el-button>
          <el-button v-else type="primary" @click="handleCloseDialog">确定</el-button>
        </div>
      </template>
    </EnhancedDialog>

    <ExportModal
      v-model="exportsDialogVisible"
      :content-config="curdContentConfig"
      :query-params="exportQueryParams"
      :page-data="exportPageData"
      :selection-data="exportSelectionData"
    />
    <DataDrawer
      v-if="drawerVisible"
      v-model="drawerVisible"
      :dict-type="currentDictType"
      :dict-label="currentDictLabel"
      :dict-type-id="currentDictTypeId"
    />
  </div>
</template>

<script setup lang="ts">
  defineOptions({
    name: 'Dict',
    inheritAttrs: false,
  });

  import DictAPI, { DictTable, DictForm, DictPageQuery } from '@/api/module_system/dict';
  import { useDictStore } from '@/store';
  import DataDrawer from '@/views/module_system/dict/components/DataDrawer.vue';
  import ExportModal from '@/components/CURD/ExportModal.vue';
  import CrudToolbarLeft from '@/components/CURD/CrudToolbarLeft.vue';
  import CrudToolbarRight from '@/components/CURD/CrudToolbarRight.vue';
  import PageSearch from '@/components/CURD/PageSearch.vue';
  import PageContent from '@/components/CURD/PageContent.vue';
  import EnhancedDialog from '@/components/CURD/EnhancedDialog.vue';
  import type { ISearchConfig, IContentConfig } from '@/components/CURD/types';
  import { useCrudList } from '@/components/CURD/useCrudList';
  import { computed, ref, reactive, unref } from 'vue';
  import { fetchAllPages } from '@/utils/fetchAllPages';

  const { searchRef, contentRef, handleQueryClick, handleResetClick, refreshList } = useCrudList();
  const dataFormRef = ref();

  const searchConfig = reactive<ISearchConfig>({
    permPrefix: 'module_system:dict_type',
    colon: true,
    isExpandable: true,
    showNumber: 2,
    form: { labelWidth: 'auto' },
    formItems: [
      {
        prop: 'dict_name',
        label: '字典名称',
        type: 'input',
        attrs: { placeholder: '请输入字典名称', clearable: true },
      },
      {
        prop: 'dict_type',
        label: '字典类型',
        type: 'input',
        attrs: { placeholder: '请输入字典类型', clearable: true },
      },
      {
        prop: 'status',
        label: '状态',
        type: 'select',
        options: [
          { label: '启用', value: '0' },
          { label: '停用', value: '1' },
        ],
        attrs: { placeholder: '请选择状态', clearable: true, style: { width: '167.5px' } },
      },
      {
        prop: 'created_time',
        label: '创建时间',
        type: 'date-picker',
        attrs: {
          type: 'datetimerange',
          rangeSeparator: '至',
          startPlaceholder: '开始日期',
          endPlaceholder: '结束日期',
          format: 'YYYY-MM-DD HH:mm:ss',
          valueFormat: 'YYYY-MM-DD HH:mm:ss',
          style: { width: '340px' },
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
    { prop: 'selection', label: '选择框', show: true },
    { prop: 'index', label: '序号', show: true },
    { prop: 'dict_name', label: '字典名称', show: true },
    { prop: 'dict_type', label: '字典类型', show: true },
    { prop: 'status', label: '状态', show: true },
    { prop: 'description', label: '描述', show: true },
    { prop: 'created_time', label: '创建时间', show: true },
    { prop: 'updated_time', label: '更新时间', show: true },
    { prop: 'operation', label: '操作', show: true },
  ]);

  const dictStore = useDictStore();

  const contentConfig = reactive<IContentConfig<DictPageQuery>>({
    permPrefix: 'module_system:dict_type',
    pk: 'id',
    cols: contentCols as IContentConfig['cols'],
    hideColumnFilter: false,
    toolbar: [],
    defaultToolbar: ['refresh', 'filter'],
    pagination: {
      pageSize: 10,
      pageSizes: [10, 20, 30, 50],
    },
    request: { page_no: 'page_no', page_size: 'page_size' },
    indexAction: async (params) => {
      const res = await DictAPI.listDictType(params as DictPageQuery);
      return {
        total: res.data.data.total,
        list: res.data.data.items,
      };
    },
    deleteAction: async (ids) => {
      await DictAPI.deleteDictType(
        ids
          .split(',')
          .map((s) => Number(s.trim()))
          .filter((n) => !Number.isNaN(n))
      );
      dictStore.clearDictData();
      const dictTypes = Object.keys(dictStore.dictData);
      if (dictTypes.length > 0) {
        await dictStore.getDict(dictTypes);
      }
    },
    deleteConfirm: {
      title: '警告',
      message: '确认删除该项数据?',
      type: 'warning',
    },
  });

  const detailFormData = ref<DictTable>({});

  const formData = reactive<DictForm>({
    id: undefined,
    dict_name: '',
    dict_type: '',
    status: '0',
    description: undefined,
  });

  const dialogVisible = reactive({
    title: '',
    visible: false,
    type: 'create' as 'create' | 'update' | 'detail',
  });

  const rules = reactive({
    dict_name: [{ required: true, message: '请输入字典名称', trigger: 'blur' }],
    dict_type: [{ required: true, message: '请选择字典类型', trigger: 'blur' }],
    status: [{ required: true, message: '请选择字典状态', trigger: 'blur' }],
  });

  const initialFormData: DictForm = {
    id: undefined,
    dict_name: '',
    dict_type: '',
    status: '0',
    description: undefined,
  };

  const exportsDialogVisible = ref(false);

  const exportQueryParams = computed(() => searchRef.value?.getQueryParams() ?? {});

  const exportPageData = computed(() => {
    const pd = contentRef.value?.pageData;
    return (unref(pd) ?? []) as DictTable[];
  });

  const exportSelectionData = computed(
    () => (contentRef.value?.getSelectionData() ?? []) as DictTable[]
  );

  const exportColumns = [
    { prop: 'dict_name', label: '字典名称' },
    { prop: 'dict_type', label: '字典类型' },
    { prop: 'status', label: '状态' },
    { prop: 'description', label: '描述' },
    { prop: 'created_time', label: '创建时间' },
    { prop: 'updated_time', label: '更新时间' },
  ];

  const curdContentConfig = {
    permPrefix: 'module_system:dict_type',
    cols: exportColumns as any,
    exportsAction: async (params: any) => {
      const query: Record<string, unknown> = { ...params };
      if (typeof query.status === 'string') query.status = query.status === 'true';
      return fetchAllPages({
        initialQuery: query,
        fetchPage: async (q) => {
          const res = await DictAPI.listDictType(q as unknown as DictPageQuery);
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
    Object.assign(formData, initialFormData);
  }

  async function handleCloseDialog() {
    dialogVisible.visible = false;
    await resetForm();
  }

  async function handleOpenDialog(type: 'create' | 'update' | 'detail', id?: number) {
    dialogVisible.type = type;
    if (id) {
      const response = await DictAPI.detailDictType(id);
      if (type === 'detail') {
        dialogVisible.title = '字典详情';
        Object.assign(detailFormData.value, response.data.data);
      } else if (type === 'update') {
        dialogVisible.title = '修改字典';
        Object.assign(formData, response.data.data);
      }
    } else {
      dialogVisible.title = '新增字典';
      formData.id = undefined;
    }
    dialogVisible.visible = true;
  }

  async function handleSubmit() {
    dataFormRef.value.validate(async (valid: any) => {
      if (valid) {
        const id = formData.id;
        try {
          if (id) {
            await DictAPI.updateDictType(id, { id, ...formData });
          } else {
            await DictAPI.createDictType(formData);
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
    const rows = contentRef.value?.getSelectionData() as DictTable[] | undefined;
    const ids = (rows ?? []).map((r) => r.id).filter((id): id is number => id != null);
    if (!ids.length) {
      ElMessage.warning('请先选择要操作的数据');
      return;
    }
    ElMessageBox.confirm(`确认${status === '0' ? '启用' : '停用'}该项数据?`, '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
      .then(async () => {
        try {
          await DictAPI.batchDictType({ ids, status });
          refreshList();
          dictStore.clearDictData();
          const dictTypes = Object.keys(dictStore.dictData);
          if (dictTypes.length > 0) {
            await dictStore.getDict(dictTypes);
          }
        } catch (error: any) {
          console.error(error);
        }
      })
      .catch(() => {
        ElMessageBox.close();
      });
  }

  const drawerVisible = ref(false);
  const currentDictType = ref('');
  const currentDictLabel = ref('');
  const currentDictTypeId = ref(1);

  function handleDictDataDrawer(dictType: DictTable) {
    currentDictType.value = dictType.dict_type || '';
    currentDictLabel.value = dictType.dict_name || '';
    currentDictTypeId.value = dictType.id || 0;
    drawerVisible.value = true;
  }
</script>
