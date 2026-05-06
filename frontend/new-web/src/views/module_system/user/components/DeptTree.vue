<!-- 部门树（无外层卡片，由用户页左侧 ElCard 统一包裹） -->
<template>
  <div class="dept-tree-root">
    <div class="dept-tree-toolbar">
      <ElInput
        v-model="deptName"
        class="dept-tree-search"
        placeholder="部门名称"
        size="small"
        clearable
      >
        <template #prefix>
          <ElIcon class="dept-tree-search__prefix-icon">
            <Search />
          </ElIcon>
        </template>
        <template #suffix>
          <ElTooltip :content="treeExpanded ? '收起全部' : '展开全部'" placement="top">
            <span
              class="dept-tree-expand-trigger"
              role="button"
              tabindex="0"
              @click.stop="toggleTreeExpandAll"
              @keydown.enter.prevent="toggleTreeExpandAll"
            >
              <ElIcon :size="15">
                <Switch />
              </ElIcon>
            </span>
          </ElTooltip>
        </template>
      </ElInput>
    </div>

    <ElTree
      ref="deptTreeRef"
      class="dept-tree-body"
      node-key="value"
      :data="deptOptions"
      :props="{ children: 'children', label: 'label', disabled: 'disabled' }"
      :expand-on-click-node="false"
      :filter-node-method="handleFilter"
      default-expand-all
      @node-click="handleNodeClick"
    >
      <template #empty>
        <ElEmpty :image-size="80" description="暂无数据" />
      </template>
    </ElTree>
  </div>
</template>

<script setup lang="ts">
import { Search, Switch } from "@element-plus/icons-vue";
import DeptAPI, { DeptPageQuery } from "@/api/module_system/dept";
import { formatTree } from "@/utils/common";
import type { FilterNodeMethodFunction, TreeInstance } from "element-plus";

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: undefined,
  },
});

const deptOptions = ref<OptionType[]>([]); // 部门列表
const deptTreeRef = ref<TreeInstance>(); // 部门树
const deptName = ref(); // 部门名称
/** 与「全部展开」状态同步，用于按钮提示（手动展开单节点后可能不完全一致） */
const treeExpanded = ref(true);

const emits = defineEmits(["node-click", "update:modelValue"]);

const deptId = useVModel(props, "modelValue", emits);

watch(deptName, (val) => {
  deptTreeRef.value?.filter(val);
});

type TreeStoreNode = {
  childNodes?: TreeStoreNode[];
  expand: () => void;
  collapse: () => void;
};

function getTreeRoot() {
  const tree = deptTreeRef.value as TreeInstance & { store?: { root: TreeStoreNode } };
  return tree?.store?.root;
}

/** 展开整棵树 */
function expandAllTreeNodes() {
  const root = getTreeRoot();
  if (!root) return;
  const walk = (node: TreeStoreNode) => {
    node.childNodes?.forEach((child) => {
      if (child.childNodes?.length) {
        child.expand();
        walk(child);
      }
    });
  };
  walk(root);
}

/** 收起整棵树 */
function collapseAllTreeNodes() {
  const root = getTreeRoot();
  if (!root) return;
  const walk = (node: TreeStoreNode) => {
    node.childNodes?.forEach((child) => {
      walk(child);
      child.collapse();
    });
  };
  walk(root);
}

function toggleTreeExpandAll() {
  if (treeExpanded.value) {
    collapseAllTreeNodes();
    treeExpanded.value = false;
  } else {
    expandAllTreeNodes();
    treeExpanded.value = true;
  }
}

interface Tree {
  [key: string]: any;
}

/**
 * 部门筛选
 */
const handleFilter: FilterNodeMethodFunction = (value: string, data: Tree) => {
  if (!value) return true;
  return data.label.includes(value);
};

/** 部门树节点 Click */
function handleNodeClick(data: { [key: string]: any }) {
  deptId.value = data.value;
  emits("node-click");
}

const queryFormData = reactive<DeptPageQuery>({
  name: undefined,
  status: undefined,
  created_time: undefined,
});

const loading = ref(true);

onBeforeMount(() => {
  loading.value = true;
  DeptAPI.listDept(queryFormData)
    .then((response) => {
      deptOptions.value = formatTree(response.data.data);
    })
    .finally(() => {
      loading.value = false;
    });
});
</script>

<style scoped lang="scss">
.dept-tree-root {
  box-sizing: border-box;
  padding: 16px 6px 12px 10px;
}

.dept-tree-toolbar {
  display: flex;
  align-items: stretch;

  .dept-tree-search {
    flex: 1;
    min-width: 0;
  }

  .dept-tree-search__prefix-icon {
    color: var(--el-text-color-placeholder);
  }

  .dept-tree-expand-trigger {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-right: -2px;
    padding: 2px;
    color: var(--el-text-color-secondary);
    vertical-align: middle;
    cursor: pointer;
    border-radius: var(--el-border-radius-small);
    transition:
      color 0.15s ease,
      background-color 0.15s ease;

    &:hover {
      color: var(--el-color-primary);
      background-color: var(--el-fill-color-light);
    }

    &:focus-visible {
      outline: 2px solid var(--el-color-primary-light-5);
      outline-offset: 1px;
    }
  }
}

.dept-tree-body {
  margin-top: 10px;
}
</style>
