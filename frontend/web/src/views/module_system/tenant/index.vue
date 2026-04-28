<!-- 租户管理 -->
<template>
  <div class="app-container">
    <PageSearch
      ref="searchRef"
      :search-config="searchConfig"
      @query-click="handleQueryClick"
      @reset-click="handleResetClick"
    />

    <PageContent ref="contentRef" :content-config="contentConfig">
      <template #toolbar="{ toolbarRight, onToolbar, removeIds, cols }">
        <CrudToolbarLeft
          :remove-ids="removeIds"
          :perm-create="['module_system:tenant:create']"
          :perm-delete="['module_system:tenant:delete']"
          @add="handleOpenDialog('create')"
          @delete="onToolbar('delete')"
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
              v-if="contentCols.find((col) => col.prop === 'name')?.show"
              key="name"
              label="租户名称"
              prop="name"
              min-width="140"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'code')?.show"
              key="code"
              label="租户编码"
              prop="code"
              min-width="120"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'status')?.show"
              key="status"
              label="状态"
              prop="status"
              min-width="80"
              align="center"
            >
              <template #default="scope">
                <el-tag :type="scope.row.status === '0' ? 'success' : 'danger'">
                  {{ scope.row.status === '0' ? '正常' : '禁用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'start_time')?.show"
              key="start_time"
              label="开始时间"
              prop="start_time"
              min-width="180"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'end_time')?.show"
              key="end_time"
              label="结束时间"
              prop="end_time"
              min-width="180"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'description')?.show"
              key="description"
              label="描述"
              prop="description"
              min-width="150"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'created_time')?.show"
              key="created_time"
              label="创建时间"
              prop="created_time"
              min-width="180"
              show-overflow-tooltip
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
                  v-hasPerm="['module_system:tenant:query']"
                  type="info"
                  size="small"
                  link
                  icon="View"
                  @click="handleOpenDialog('detail', scope.row.id)"
                >
                  详情
                </el-button>
                <el-button
                  v-hasPerm="['module_system:tenant:update']"
                  type="primary"
                  size="small"
                  link
                  icon="edit"
                  @click="handleOpenDialog('update', scope.row.id)"
                >
                  编辑
                </el-button>
                <el-button
                  v-hasPerm="['module_system:tenant:delete']"
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
        <el-descriptions :column="2" border>
          <el-descriptions-item label="租户名称" :span="2">
            {{ detailFormData.name }}
          </el-descriptions-item>
          <el-descriptions-item label="租户编码" :span="2">
            {{ detailFormData.code }}
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="detailFormData.status === '0' ? 'success' : 'danger'">
              {{ detailFormData.status === '0' ? '正常' : '禁用' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="开始时间">
            {{ detailFormData.start_time }}
          </el-descriptions-item>
          <el-descriptions-item label="结束时间">
            {{ detailFormData.end_time }}
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">
            {{ detailFormData.description }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">
            {{ detailFormData.created_time }}
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
          <el-form-item label="租户名称" prop="name">
            <el-input v-model="formData.name" placeholder="请输入租户名称" :maxlength="100" />
          </el-form-item>
          <el-form-item label="租户编码" prop="code">
            <el-input
              v-model="formData.code"
              placeholder="字母与数字，创建后不可改"
              :maxlength="100"
              :disabled="dialogVisible.type === 'update'"
            />
          </el-form-item>
          <el-form-item label="状态" prop="status">
            <el-select v-model="formData.status" placeholder="请选择状态" style="width: 100%">
              <el-option label="正常" value="0" />
              <el-option label="禁用" value="1" />
            </el-select>
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input
              v-model="formData.description"
              type="textarea"
              :rows="3"
              placeholder="请输入描述"
              :maxlength="255"
            />
          </el-form-item>
          <el-form-item label="开始时间" prop="start_time">
            <el-date-picker
              v-model="formData.start_time"
              type="datetime"
              value-format="YYYY-MM-DD HH:mm:ss"
              placeholder="可选"
              style="width: 100%"
            />
          </el-form-item>
          <el-form-item label="结束时间" prop="end_time">
            <el-date-picker
              v-model="formData.end_time"
              type="datetime"
              value-format="YYYY-MM-DD HH:mm:ss"
              placeholder="可选"
              style="width: 100%"
            />
          </el-form-item>
        </el-form>
      </template>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleCloseDialog">取消</el-button>
          <el-button
            v-if="dialogVisible.type === 'create'"
            v-hasPerm="['module_system:tenant:create']"
            type="primary"
            :loading="submitLoading"
            @click="handleSubmit"
          >
            确定
          </el-button>
          <el-button
            v-else-if="dialogVisible.type === 'update'"
            v-hasPerm="['module_system:tenant:update']"
            type="primary"
            :loading="submitLoading"
            @click="handleSubmit"
          >
            确定
          </el-button>
          <el-button v-else type="primary" @click="handleCloseDialog">确定</el-button>
        </div>
      </template>
    </EnhancedDialog>
  </div>
</template>

<script setup lang="ts">
  import { ref, reactive } from 'vue';
  import TenantAPI, {
    TenantForm,
    TenantCreateForm,
    TenantUpdateForm,
    TenantPageQuery,
    TenantTable,
  } from '@/api/module_system/tenant';
  import CrudToolbarLeft from '@/components/CURD/CrudToolbarLeft.vue';
  import CrudToolbarRight from '@/components/CURD/CrudToolbarRight.vue';
  import PageSearch from '@/components/CURD/PageSearch.vue';
  import PageContent from '@/components/CURD/PageContent.vue';
  import EnhancedDialog from '@/components/CURD/EnhancedDialog.vue';
  import { useCrudList } from '@/components/CURD/useCrudList';
  import type { IContentConfig, ISearchConfig } from '@/components/CURD/types';

  defineOptions({
    name: 'Tenant',
    inheritAttrs: false,
  });

  const { searchRef, contentRef, handleQueryClick, handleResetClick, refreshList } = useCrudList();
  const dataFormRef = ref();
  const submitLoading = ref(false);

  const searchConfig = reactive<ISearchConfig>({
    permPrefix: 'module_system:tenant',
    colon: true,
    isExpandable: true,
    showNumber: 2,
    form: { labelWidth: 'auto' },
    formItems: [
      {
        prop: 'name',
        label: '租户名称',
        type: 'input',
        attrs: { placeholder: '请输入租户名称', clearable: true },
      },
      {
        prop: 'code',
        label: '租户编码',
        type: 'input',
        attrs: { placeholder: '请输入租户编码', clearable: true },
      },
      {
        prop: 'status',
        label: '状态',
        type: 'select',
        attrs: {
          placeholder: '请选择状态',
          clearable: true,
          options: [
            { label: '正常', value: '0' },
            { label: '禁用', value: '1' },
          ],
          style: { width: '167.5px' },
        },
      },
      {
        prop: 'created_time',
        label: '创建时间',
        type: 'date-picker',
        initialValue: [],
        attrs: {
          type: 'datetimerange',
          valueFormat: 'YYYY-MM-DD HH:mm:ss',
          rangeSeparator: '至',
          startPlaceholder: '开始日期',
          endPlaceholder: '结束日期',
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
    { prop: 'name', label: '租户名称', show: true },
    { prop: 'code', label: '租户编码', show: true },
    { prop: 'status', label: '状态', show: true },
    { prop: 'description', label: '描述', show: true },
    { prop: 'created_time', label: '创建时间', show: true },
    { prop: 'operation', label: '操作', show: true },
  ]);

  const contentConfig = reactive<IContentConfig<TenantPageQuery>>({
    permPrefix: 'module_system:tenant',
    pk: 'id',
    cols: contentCols as IContentConfig['cols'],
    hideColumnFilter: false,
    toolbar: [],
    defaultToolbar: ['import', 'export', 'refresh', 'filter'],
    pagination: {
      pageSize: 10,
      pageSizes: [10, 20, 30, 50],
    },
    request: { page_no: 'page_no', page_size: 'page_size' },
    indexAction: async (params) => {
      const res = await TenantAPI.listTenant(params as TenantPageQuery);
      return {
        total: res.data.data.total,
        list: res.data.data.items,
      };
    },
    deleteAction: async (ids) => {
      const idList = ids
        .split(',')
        .map((s) => Number(s.trim()))
        .filter((n) => !Number.isNaN(n));
      await TenantAPI.deleteTenant(idList);
    },
    deleteConfirm: {
      title: '警告',
      message: '确认删除该项数据?',
      type: 'warning',
    },
  });

  const detailFormData = ref<TenantTable>({ code: '', name: '', status: '0' });

  const currentEditId = ref<number | null>(null);

  const formData = reactive<TenantForm>({
    name: '',
    code: '',
    status: '0',
    description: '',
    start_time: undefined,
    end_time: undefined,
  });

  const dialogVisible = reactive({
    title: '',
    visible: false,
    type: 'create' as 'create' | 'update' | 'detail',
  });

  const CODE_PATTERN = /^[A-Za-z0-9]+$/;

  const validateTimeRange = (rule: any, value: any, callback: any) => {
    if (formData.start_time && formData.end_time && formData.start_time > formData.end_time) {
      callback(new Error('结束时间不能早于开始时间'));
    } else {
      callback();
    }
  };

  const rules = reactive({
    name: [{ required: true, message: '请输入租户名称', trigger: 'blur' }],
    code: [
      { required: true, message: '请输入租户编码', trigger: 'blur' },
      {
        pattern: CODE_PATTERN,
        message: '编码仅允许字母与数字',
        trigger: 'blur',
      },
    ],
    end_time: [{ validator: validateTimeRange, trigger: 'change' }],
  });

  const initialFormData: TenantForm = {
    name: '',
    code: '',
    status: '0',
    description: '',
    start_time: undefined,
    end_time: undefined,
  };

  function handleRowDelete(id: number) {
    contentRef.value?.handleDelete(id);
  }

  async function resetForm() {
    if (dataFormRef.value) {
      dataFormRef.value.resetFields();
      dataFormRef.value.clearValidate();
    }
    Object.assign(formData, initialFormData);
    currentEditId.value = null;
  }

  async function handleCloseDialog() {
    dialogVisible.visible = false;
    await resetForm();
  }

  async function handleOpenDialog(type: 'create' | 'update' | 'detail', id?: number) {
    dialogVisible.type = type;
    if (id) {
      const response = await TenantAPI.detailTenant(id);
      if (type === 'detail') {
        dialogVisible.title = '租户详情';
        Object.assign(detailFormData.value, response.data.data);
      } else if (type === 'update') {
        dialogVisible.title = '修改租户';
        Object.assign(formData, response.data.data);
        currentEditId.value = id;
      }
    } else {
      dialogVisible.title = '新增租户';
    }
    dialogVisible.visible = true;
  }

  async function handleSubmit() {
    dataFormRef.value.validate(async (valid: boolean) => {
      if (valid) {
        submitLoading.value = true;
        const id = currentEditId.value;
        try {
          if (id) {
            const payload: TenantUpdateForm = {
              name: formData.name,
              start_time: formData.start_time,
              end_time: formData.end_time,
            };
            await TenantAPI.updateTenant(id, payload);
          } else {
            const payload: TenantCreateForm = {
              name: formData.name as string,
              code: formData.code as string,
              start_time: formData.start_time,
              end_time: formData.end_time,
            };
            await TenantAPI.createTenant(payload);
          }
          dialogVisible.visible = false;
          await resetForm();
          refreshList();
        } catch (error: unknown) {
          console.error(error);
        } finally {
          submitLoading.value = false;
        }
      }
    });
  }
</script>
