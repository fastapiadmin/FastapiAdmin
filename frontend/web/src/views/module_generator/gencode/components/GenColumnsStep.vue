<template>
  <div class="elTableCustom">
    <el-alert
      v-if="info.sub && !info.master_sub_hint && info.sub_table_name"
      class="mb-3"
      type="success"
      :closable="false"
      show-icon
      title="当前已启用主子表：以下为「主表」字段配置；子表字段来自数据库结构，保存后可在预览中查看子表生成代码。"
    />
    <el-alert
      v-else-if="info.master_sub_hint"
      class="mb-3"
      type="warning"
      :closable="false"
      show-icon
      :title="info.master_sub_hint"
    />
    <p class="gencode-columns-tip">
      菜单与路由、接口路径的对应见「基础配置」第一步中的折叠「对照」表。
    </p>
    <el-alert
      v-if="columnKeyword.trim() && displayColumns.length === 0 && (info.columns?.length ?? 0) > 0"
      class="mb-2"
      type="warning"
      :closable="false"
      show-icon
      title="无匹配列，请调整筛选词或清空筛选框"
    />
    <div class="mb-2 flex flex-wrap items-center gap-2">
      <el-input
        v-model="columnKeyword"
        clearable
        placeholder="筛选列名或注释"
        class="gencode-column-filter"
        :prefix-icon="Search"
      />
      <span class="gencode-bulk-hint">批量设置：</span>
      <el-space size="small">
        <el-dropdown>
          <el-button size="small" type="primary" plain>查询</el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="bulkSet('is_query', true)">全选</el-dropdown-item>
              <el-dropdown-item @click="bulkSet('is_query', false)">全不选</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-dropdown>
          <el-button size="small" type="success" plain>列表</el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="bulkSet('is_list', true)">全选</el-dropdown-item>
              <el-dropdown-item @click="bulkSet('is_list', false)">全不选</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-dropdown>
          <el-button size="small" type="warning" plain>新增</el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="bulkSet('is_insert', true)">全选</el-dropdown-item>
              <el-dropdown-item @click="bulkSet('is_insert', false)">全不选</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-dropdown>
          <el-button size="small" type="danger" plain>编辑</el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="bulkSet('is_edit', true)">全选</el-dropdown-item>
              <el-dropdown-item @click="bulkSet('is_edit', false)">全不选</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-space>
    </div>
    <div class="data-table__content">
      <el-table
        ref="dragTable"
        v-loading="loading"
        :data="displayColumns"
        row-key="id"
        :height="tableHeight"
        highlight-current-row
        border
        stripe
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column label="拖拽" width="56" fixed align="center">
          <template #default>
            <span
              class="gencode-drag-handle"
              :class="{ disabled: !!columnKeyword.trim() }"
              title="拖拽排序（筛选时禁用）"
            >
              <el-icon><Rank /></el-icon>
            </span>
          </template>
        </el-table-column>
        <el-table-column label="序号" type="index" width="60" fixed />
        <el-table-column
          label="列名"
          prop="column_name"
          min-width="60"
          :show-overflow-tooltip="true"
        />
        <el-table-column
          label="类型"
          prop="column_type"
          min-width="60"
          :show-overflow-tooltip="true"
        />
        <el-table-column label="长度" prop="column_length" width="80" :show-overflow-tooltip="true">
          <template #default="scope">
            <el-input v-model="scope.row.column_length" :disabled="!!scope.row.is_pk" />
          </template>
        </el-table-column>
        <el-table-column label="注释" min-width="60">
          <template #default="scope">
            <el-input v-model="scope.row.column_comment"></el-input>
          </template>
        </el-table-column>
        <el-table-column label="后端类型" min-width="60">
          <template #default="scope">
            <el-select v-model="scope.row.python_type">
              <el-option label="str" value="str" />
              <el-option label="int" value="int" />
              <el-option label="float" value="float" />
              <el-option label="Decimal" value="Decimal" />
              <el-option label="date" value="date" />
              <el-option label="time" value="time" />
              <el-option label="datetime" value="datetime" />
              <el-option label="bytes" value="bytes" />
              <el-option label="dict" value="dict" />
              <el-option label="list" value="list" />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="后端属性" min-width="60">
          <template #default="scope">
            <el-input v-model="scope.row.python_field"></el-input>
          </template>
        </el-table-column>
        <el-table-column label="新增" width="60">
          <template #default="scope">
            <el-checkbox v-model="scope.row.is_insert" />
          </template>
        </el-table-column>
        <el-table-column label="编辑" width="60">
          <template #default="scope">
            <el-checkbox v-model="scope.row.is_edit" />
          </template>
        </el-table-column>
        <el-table-column label="列表" width="60">
          <template #default="scope">
            <el-checkbox v-model="scope.row.is_list" />
          </template>
        </el-table-column>
        <el-table-column label="查询" width="60">
          <template #default="scope">
            <el-checkbox v-model="scope.row.is_query" />
          </template>
        </el-table-column>
        <el-table-column label="查询方式" min-width="60">
          <template #default="scope">
            <el-select v-model="scope.row.query_type">
              <el-option label="=" value="EQ" />
              <el-option label="!=" value="NE" />
              <el-option label=">" value="GT" />
              <el-option label=">=" value="GTE" />
              <el-option label="<" value="LT" />
              <el-option label="<=" value="LTE" />
              <el-option label="LIKE" value="LIKE" />
              <el-option label="BETWEEN" value="BETWEEN" />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column
          label="默认值"
          prop="column_default"
          min-width="60"
          :show-overflow-tooltip="true"
        >
          <template #default="scope">
            <el-input v-model="scope.row.column_default" :disabled="!!scope.row.is_pk" />
          </template>
        </el-table-column>
        <el-table-column label="自增" width="60">
          <template #default="scope">
            <el-checkbox v-model="scope.row.is_increment" />
          </template>
        </el-table-column>
        <el-table-column label="可空" width="60">
          <template #default="scope">
            <el-checkbox v-model="scope.row.is_nullable" />
          </template>
        </el-table-column>
        <el-table-column label="唯一" width="60">
          <template #default="scope">
            <el-checkbox v-model="scope.row.is_unique" />
          </template>
        </el-table-column>
        <el-table-column label="主键" width="60">
          <template #default="scope">
            <el-checkbox v-model="scope.row.is_pk" />
          </template>
        </el-table-column>
        <el-table-column label="表单类型">
          <template #default="scope">
            <el-select v-model="scope.row.html_type">
              <el-option label="文本框" value="input" />
              <el-option label="文本域" value="textarea" />
              <el-option label="下拉框" value="select" />
              <el-option label="单选框" value="radio" />
              <el-option label="复选框" value="checkbox" />
              <el-option label="日期控件" value="datetime" />
              <el-option label="图片上传" value="imageUpload" />
              <el-option label="文件上传" value="fileUpload" />
              <el-option label="富文本控件" value="editor" />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="字典类型" fixed="right">
          <template #default="scope">
            <el-select v-model="scope.row.dict_type" clearable filterable placeholder="请选择">
              <el-option
                v-for="dict in dictOptions"
                :key="dict.dict_type"
                :label="dict.dict_name"
                :value="dict.dict_type || ''"
              >
                <span style="float: left">{{ dict.dict_name }}</span>
                <span style="float: right; font-size: 13px; color: #8492a6">
                  {{ dict.dict_type }}
                </span>
              </el-option>
            </el-select>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch, nextTick } from "vue";
import { Search } from "@element-plus/icons-vue";
import { useDraggable } from "vue-draggable-plus";
import type { GenTableSchema } from "@/api/module_generator/gencode";
import type { DictTable } from "@/api/module_system/dict";

defineOptions({ name: "GenColumnsStep" });

const props = defineProps<{
  info: GenTableSchema;
  dictOptions: DictTable[];
  loading: boolean;
  bulkSet: (field: string | string[], value: unknown) => void;
}>();

const columnKeyword = ref("");
const dragTable = ref<any>(null);
const dragContainer = ref<HTMLElement | null>(null);
let draggableApi: { destroy?: () => void; pause?: () => void; start?: () => void } | null = null;

// 计算表格高度：视口高度 - 顶部导航栏 - 步骤条 - 提示文字 - 筛选栏 - 底部按钮 - 边距
// 大约：60(顶部) + 60(步骤) + 30(提示) + 50(筛选) + 80(底部按钮) + 100(边距) = 380px
const tableHeight = computed(() => {
  return "calc(100vh - 300px)"; // -80 底部按钮
});

const columnsModel = computed({
  get: () => props.info.columns || [],
  set: (v) => {
    // props.info 是父组件传入的 reactive 对象，可以直接回写
    props.info.columns = v as any;
  },
});

const displayColumns = computed(() => {
  const cols = props.info.columns || [];
  const q = columnKeyword.value.trim().toLowerCase();
  if (!q) return cols;
  return cols.filter((c) => {
    const name = String(c.column_name ?? "").toLowerCase();
    const comment = String(c.column_comment ?? "").toLowerCase();
    return name.includes(q) || comment.includes(q);
  });
});

function syncSortNumbers() {
  const cols = columnsModel.value || [];
  cols.forEach((c: any, idx: number) => {
    c.sort = idx + 1;
  });
}

async function setupRowDraggable() {
  // 筛选状态下禁用拖拽：displayColumns 是子集，直接拖拽会导致索引映射混乱
  if (columnKeyword.value.trim()) {
    draggableApi?.destroy?.();
    draggableApi = null;
    dragContainer.value = null;
    return;
  }

  await nextTick();
  const el = dragTable.value?.$el as HTMLElement | undefined;
  const tbody = el?.querySelector?.(".el-table__body-wrapper tbody") as HTMLElement | null;
  if (!tbody) return;
  dragContainer.value = tbody;

  // 重新绑定
  draggableApi?.destroy?.();
  draggableApi = useDraggable(dragContainer, columnsModel, {
    animation: 150,
    draggable: "tr",
    handle: ".gencode-drag-handle:not(.disabled)",
    onEnd() {
      syncSortNumbers();
    },
  });
}

onMounted(() => {
  void setupRowDraggable();
});

watch(
  () => [columnKeyword.value, (props.info.columns || []).length],
  async () => {
    await setupRowDraggable();
  }
);

onBeforeUnmount(() => {
  draggableApi?.destroy?.();
  draggableApi = null;
});
</script>

<style scoped lang="scss">
.gencode-columns-tip {
  margin: 0 0 10px;
  font-size: 12px;
  line-height: 1.5;
  color: var(--el-text-color-secondary);
}

.gencode-column-filter {
  width: 200px;
  max-width: 100%;
}

.gencode-bulk-hint {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  user-select: none;
}

.gencode-drag-handle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 22px;
  font-size: 14px;
  line-height: 1;
  color: var(--el-text-color-secondary);
  cursor: grab;
  user-select: none;
}

.gencode-drag-handle.disabled {
  cursor: not-allowed;
  opacity: 0.35;
}
</style>
