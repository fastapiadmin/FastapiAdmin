<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div v-show="visible" class="search-container">
      <el-form
        ref="queryFormRef"
        :model="searchForm"
        label-suffix=":"
        :inline="true"
        @submit.prevent="handleQuery"
      >
        <el-form-item prop="name" label="节点名称">
          <el-input v-model="searchForm.name" placeholder="请输入节点名称" clearable />
        </el-form-item>
        <el-form-item prop="code" label="节点编码">
          <el-input v-model="searchForm.code" placeholder="请输入节点编码" clearable />
        </el-form-item>
        <el-form-item>
          <el-button
            v-hasPerm="['module_task:node:query']"
            type="primary"
            icon="search"
            @click="handleQuery"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_task:node:query']"
            icon="refresh"
            @click="handleResetQuery"
          >
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-card class="data-table">
      <template #header>
        <div class="card-header">
          <el-space>
            节点列表
            <el-tooltip content="节点列表">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
          </el-space>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--left">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_task:node:create']"
                type="success"
                icon="plus"
                @click="handleCreateType"
              >
                新增
              </el-button>
            </el-col>
          </el-row>
        </div>
        <div class="data-table__toolbar--right">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-tooltip content="搜索显示/隐藏">
                <el-button
                  v-hasPerm="['*:*:*']"
                  type="info"
                  icon="search"
                  circle
                  @click="visible = !visible"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-tooltip content="刷新">
                <el-button
                  v-hasPerm="['module_task:node:query']"
                  type="primary"
                  icon="refresh"
                  circle
                  @click="handleRefresh"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-popover placement="bottom" trigger="click">
                <template #reference>
                  <el-button type="danger" icon="operation" circle></el-button>
                </template>
                <el-scrollbar max-height="350px">
                  <template v-for="column in tableColumns" :key="column.prop">
                    <el-checkbox v-if="column.prop" v-model="column.show" :label="column.label" />
                  </template>
                </el-scrollbar>
              </el-popover>
            </el-col>
          </el-row>
        </div>
      </div>

      <el-table
        ref="tableRef"
        v-loading="typeLoading"
        :data="typeDataSource"
        highlight-current-row
        lass="data-table__content"
        height="450"
        max-height="450"
        border
        stripe
        @sort-change="handleTypeTableChange"
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="节点名称" width="150" />
        <el-table-column prop="code" label="节点编码" width="150" />
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
        <el-table-column prop="created_time" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right" align="center">
          <template #default="{ row }">
            <el-button type="info" size="small" link icon="view" @click="handleDetailType(row)">
              详情
            </el-button>
            <el-button type="primary" size="small" link icon="edit" @click="handleEditType(row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" link icon="delete" @click="handleDeleteType(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页区域 -->
      <template #footer>
        <pagination
          v-model:total="typePagination.total"
          v-model:page="typePagination.page_no"
          v-model:limit="typePagination.page_size"
          @pagination="loadNodeTypes"
        />
      </template>
    </el-card>

    <NodeTypeFormModal
      v-model:visible="typeFormVisible"
      :node-type="selectedNodeType"
      @refresh="loadNodeTypes"
    />

    <el-dialog v-model="detailVisible" title="节点详情" width="600px">
      <el-descriptions v-if="selectedNodeDetail" :column="2" border>
        <el-descriptions-item label="节点ID">
          {{ selectedNodeDetail.id }}
        </el-descriptions-item>
        <el-descriptions-item label="节点编码">
          {{ selectedNodeDetail.code }}
        </el-descriptions-item>
        <el-descriptions-item label="节点名称">
          {{ selectedNodeDetail.name }}
        </el-descriptions-item>
        <el-descriptions-item label="节点分类">
          {{ selectedNodeDetail.category }}
        </el-descriptions-item>
        <el-descriptions-item label="是否系统节点" :span="2">
          <el-tag :type="selectedNodeDetail.is_system ? 'success' : 'info'">
            {{ selectedNodeDetail.is_system ? "是" : "否" }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="是否激活" :span="2">
          <el-tag :type="selectedNodeDetail.is_active ? 'success' : 'danger'">
            {{ selectedNodeDetail.is_active ? "是" : "否" }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="排序" :span="2">
          {{ selectedNodeDetail.sort_order }}
        </el-descriptions-item>
        <el-descriptions-item label="处理器" :span="2">
          {{ selectedNodeDetail.handler }}
        </el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">
          {{ selectedNodeDetail.description }}
        </el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="detailVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import NodeAPI, { type NodeType, type NodeTypePageQuery } from "@/api/module_task/node";
import NodeTypeFormModal from "./components/NodeTypeFormModal.vue";

const searchForm = reactive<Partial<NodeTypePageQuery>>({
  name: undefined,
  code: undefined,
});

const visible = ref(true);
const typeDataSource = ref<NodeType[]>([]);
const typeLoading = ref(false);
const typePagination = reactive({
  page_no: 1,
  page_size: 10,
  total: 0,
});

const typeFormVisible = ref(false);
const selectedNodeType = ref<NodeType>();
const detailVisible = ref(false);
const selectedNodeDetail = ref<NodeType>();

const tableColumns = ref([
  { prop: "selection", label: "选择框", show: true },
  { prop: "index", label: "序号", show: true },
  { prop: "code", label: "节点编码", show: true },
  { prop: "name", label: "节点名称", show: true },
  { prop: "category", label: "节点分类", show: true },
  { prop: "is_system", label: "是否系统节点", show: true },
  { prop: "is_active", label: "是否激活", show: true },
  { prop: "sort_order", label: "排序", show: true },
  { prop: "handler", label: "处理器", show: true },
  { prop: "description", label: "描述", show: true },
  { prop: "operation", label: "操作", show: true },
]);

const loadNodeTypes = async () => {
  typeLoading.value = true;
  try {
    const params: NodeTypePageQuery = {
      page_no: typePagination.page_no,
      page_size: typePagination.page_size,
      ...searchForm,
    };
    const res = await NodeAPI.getNodeTypes(params);
    if (res.data && res.data.data) {
      typeDataSource.value = res.data.data.items || [];
      typePagination.total = res.data.data.total || 0;
    }
  } catch {
    ElMessage.error("加载节点类型失败");
  } finally {
    typeLoading.value = false;
  }
};

const handleQuery = () => {
  typePagination.page_no = 1;
  loadNodeTypes();
};

const handleResetQuery = () => {
  Object.assign(searchForm, {
    name: undefined,
    code: undefined,
  });
  handleQuery();
};

const handleTypeTableChange = () => {
  loadNodeTypes();
};

const handleCreateType = () => {
  selectedNodeType.value = undefined;
  typeFormVisible.value = true;
};

const handleDetailType = async (record: NodeType) => {
  try {
    const res = await NodeAPI.getNodeTypeDetail(record.id!);
    if (res.data && res.data.data) {
      selectedNodeDetail.value = res.data.data;
      detailVisible.value = true;
    }
  } catch {
    ElMessage.error("获取节点详情失败");
  }
};

const handleEditType = (record: NodeType) => {
  selectedNodeType.value = record;
  typeFormVisible.value = true;
};

const handleDeleteType = async (record: NodeType) => {
  try {
    await ElMessageBox.confirm(`确定要删除节点类型 "${record.name}" 吗？`, "确认删除", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });

    if (!record.id) {
      ElMessage.error("节点类型ID不存在");
      return;
    }
    await NodeAPI.deleteNodeType([record.id]);
    ElMessage.success("删除成功");
    loadNodeTypes();
  } catch (error) {
    if (error !== "cancel") {
      ElMessage.error("删除失败");
    }
  }
};

const handleRefresh = () => {
  loadNodeTypes();
};

onMounted(() => {
  loadNodeTypes();
});
</script>

<style scoped lang="scss">
.app-container {
  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
}

.data-table__content {
  margin-top: 16px;
}
</style>
