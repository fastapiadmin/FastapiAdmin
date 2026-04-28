<template>
  <div class="app-container">
    <PageSearch
      ref="searchRef"
      :search-config="searchConfig"
      @query-click="handleQueryClick"
      @reset-click="handleResetClick"
    />

    <PageContent ref="contentRef" :content-config="contentConfig" @add-click="handleCreate">
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
            <el-table-column type="selection" align="center" min-width="55" />
            <el-table-column type="index" fixed label="序号" min-width="60">
              <template #default="scope">
                {{ (pagination.currentPage - 1) * pagination.pageSize + scope.$index + 1 }}
              </template>
            </el-table-column>
            <el-table-column label="ID" prop="id" min-width="80" />
            <el-table-column label="名称" prop="name" min-width="160" show-overflow-tooltip />
            <el-table-column label="编码" prop="code" min-width="120" show-overflow-tooltip />
            <el-table-column label="状态" prop="status" min-width="100">
              <template #default="scope">
                <el-tag :type="getStatusType(scope.row.status) as any">
                  {{ getStatusText(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="描述"
              prop="description"
              min-width="160"
              show-overflow-tooltip
            />
            <el-table-column label="创建时间" prop="created_time" min-width="180" />

            <OperationColumn :list-data-length="data.length">
              <template #default="scope">
                <el-space class="flex">
                  <el-button
                    v-if="scope.row.status === 'draft'"
                    v-hasPerm="['module_task:workflow:definition:update']"
                    type="success"
                    size="small"
                    link
                    icon="upload"
                    @click="handlePublish(scope.row)"
                  >
                    发布
                  </el-button>
                  <el-dropdown
                    v-if="scope.row.status === 'published'"
                    v-hasPerm="['module_task:workflow:definition:execute']"
                    @command="(e: string) => handleExecute(e, scope.row)"
                  >
                    <el-button type="warning" size="small" link icon="video-play">
                      执行
                      <el-icon><ArrowDown /></el-icon>
                    </el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="execute">立即执行</el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                  <el-button
                    v-hasPerm="['module_task:workflow:definition:update']"
                    type="primary"
                    size="small"
                    link
                    icon="edit"
                    @click="handleEdit(scope.row)"
                  >
                    编辑
                  </el-button>
                  <el-button
                    v-hasPerm="['module_task:workflow:definition:delete']"
                    type="danger"
                    size="small"
                    link
                    icon="delete"
                    @click="handleRowDelete(scope.row.id)"
                  >
                    删除
                  </el-button>
                </el-space>
              </template>
            </OperationColumn>
          </el-table>
        </div>
      </template>
    </PageContent>

    <WorkflowDesignDrawer
      v-model:visible="createVisible"
      :workflow="selectedWorkflow"
      @refresh="refreshList"
    />
  </div>
</template>

<script lang="ts" setup>
  defineOptions({
    name: 'WorkflowDefinition',
    inheritAttrs: false,
  });

  import { ElMessage, ElMessageBox } from 'element-plus';
  import { ArrowDown } from '@element-plus/icons-vue';
  import PageSearch from '@/components/CURD/PageSearch.vue';
  import PageContent from '@/components/CURD/PageContent.vue';
  import type { IContentConfig, ISearchConfig } from '@/components/CURD/types';
  import { useCrudList } from '@/components/CURD/useCrudList';
  import OperationColumn from '@/components/OperationColumn/index.vue';
  import WorkflowDefinitionAPI, {
    type WorkflowTable,
    type WorkflowPageQuery,
  } from '@/api/module_task/workflow/definition';
  import WorkflowDesignDrawer from '../components/WorkflowDesignDrawer.vue';
  import { onMounted, reactive, ref } from 'vue';

  const { searchRef, contentRef, handleQueryClick, handleResetClick, refreshList } = useCrudList();

  const selectedWorkflow = ref<WorkflowTable>();
  const createVisible = ref(false);

  const searchConfig = reactive<ISearchConfig>({
    permPrefix: 'module_task:workflow:definition',
    colon: true,
    isExpandable: true,
    showNumber: 2,
    form: { labelWidth: 'auto' },
    formItems: [
      {
        prop: 'name',
        label: '流程名称',
        type: 'input',
        attrs: { placeholder: '请输入流程名称', clearable: true },
      },
      {
        prop: 'code',
        label: '流程编码',
        type: 'input',
        attrs: { placeholder: '请输入流程编码', clearable: true },
      },
      {
        prop: 'status',
        label: '状态',
        type: 'select',
        options: [
          { label: '草稿', value: 'draft' },
          { label: '已发布', value: 'published' },
          { label: '已归档', value: 'archived' },
        ],
        attrs: { placeholder: '请选择状态', clearable: true, style: { width: '170px' } },
      },
    ],
  });

  function normalizeWorkflowQuery(params: Record<string, unknown>): WorkflowPageQuery {
    const p = { ...params } as Record<string, unknown>;
    if (p.status === '' || p.status === null) p.status = undefined;
    return p as unknown as WorkflowPageQuery;
  }

  const contentConfig = reactive<IContentConfig<WorkflowPageQuery>>({
    permPrefix: 'module_task:workflow:definition',
    title: '工作流管理',
    tooltip: '流程编排列表，支持发布与执行',
    cols: [],
    hideColumnFilter: true,
    toolbar: [
      { name: 'add', text: '新增', attrs: { icon: 'plus', type: 'success' }, perm: 'create' },
      'delete',
    ],
    defaultToolbar: ['refresh'],
    initialFetch: false,
    pagination: {
      pageSize: 10,
      pageSizes: [10, 20, 30, 50],
    },
    request: { page_no: 'page_no', page_size: 'page_size' },
    indexAction: async (params) => {
      const res = await WorkflowDefinitionAPI.getWorkflowList(
        normalizeWorkflowQuery(params as unknown as Record<string, unknown>)
      );
      return {
        total: res.data.data.total,
        list: res.data.data.items,
      };
    },
    deleteAction: (ids) =>
      WorkflowDefinitionAPI.deleteWorkflow(
        ids
          .split(',')
          .map((s) => Number(s.trim()))
          .filter((n) => !Number.isNaN(n) && n > 0)
      ),
    deleteConfirm: {
      title: '警告',
      message: '确认删除选中的工作流吗？',
      type: 'warning',
    },
  });

  function handleRowDelete(id?: number) {
    if (id == null) return;
    contentRef.value?.handleDelete(id);
  }

  function handleCreate() {
    selectedWorkflow.value = undefined;
    createVisible.value = true;
  }

  function handleEdit(record: WorkflowTable) {
    selectedWorkflow.value = record;
    createVisible.value = true;
  }

  function getStatusType(status: string) {
    const typeMap: Record<string, string> = {
      draft: 'info',
      published: 'success',
      archived: 'warning',
    };
    return typeMap[status] || '';
  }

  function getStatusText(status: string) {
    const textMap: Record<string, string> = {
      draft: '草稿',
      published: '已发布',
      archived: '已归档',
    };
    return textMap[status] || status;
  }

  function handlePublish(record: WorkflowTable) {
    ElMessageBox.confirm('确定要发布此工作流吗？发布后可执行。', '确认发布', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
      .then(async () => {
        try {
          if (!record.id) {
            ElMessage.error('工作流ID不存在');
            return;
          }
          await WorkflowDefinitionAPI.publishWorkflow(record.id, {});
          ElMessage.success('发布成功');
          refreshList();
        } catch {
          ElMessage.error('发布失败');
        }
      })
      .catch(() => {});
  }

  function handleExecute(action: string, record: WorkflowTable) {
    if (action !== 'execute') return;
    ElMessageBox.confirm('确定要立即执行此工作流吗？', '确认执行', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
      .then(async () => {
        try {
          if (!record.id) {
            ElMessage.error('工作流ID不存在');
            return;
          }
          const res = await WorkflowDefinitionAPI.executeWorkflow({
            workflow_id: record.id,
            variables: {},
          });
          if (res.data?.data) {
            const result = res.data.data;
            ElMessage.success(`工作流执行${result.status === 'completed' ? '成功' : '失败'}`);
          }
          refreshList();
        } catch {
          ElMessage.error('执行失败');
        }
      })
      .catch(() => {});
  }

  onMounted(() => {
    refreshList();
  });
</script>

<style scoped lang="scss"></style>
