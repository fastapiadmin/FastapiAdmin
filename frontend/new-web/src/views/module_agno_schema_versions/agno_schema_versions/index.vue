<!-- Agno 知识库表结构版本（对应 DB：ai.agno_schema_versions） -->
<template>
  <div class="app-container">
    <el-card shadow="never">
      <template #header>
        <span>Schema 版本</span>
      </template>
      <el-alert
        type="info"
        :closable="false"
        show-icon
        class="mb-4"
        title="当前仓库未接入该菜单的后端列表接口；下列为占位表格列，接口就绪后可在本页接入请求逻辑。"
      />
      <el-table :data="tableData" border stripe style="width: 100%" v-loading="loading">
        <template #empty>
          <el-empty description="暂无数据（待后端提供分页列表接口）" />
        </template>
        <el-table-column prop="table_name" label="表名" min-width="220" show-overflow-tooltip />
        <el-table-column prop="version" label="版本" min-width="140" show-overflow-tooltip />
        <el-table-column prop="created_at" label="创建时间" min-width="180" show-overflow-tooltip />
        <el-table-column prop="updated_at" label="更新时间" min-width="180" show-overflow-tooltip />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";

defineOptions({
  name: "AgnoSchemaVersions",
  inheritAttrs: false,
});

/** 与 ai.agno_schema_versions 字段对齐的占位类型 */
interface SchemaVersionRow {
  table_name?: string;
  version?: string;
  created_at?: string;
  updated_at?: string;
}

const loading = ref(false);
const tableData = ref<SchemaVersionRow[]>([]);

onMounted(() => {
  // 后端增加 CRUD 后：在此调用分页列表 API，失败时用 ElMessage 提示即可
  tableData.value = [];
});
</script>
