<!-- 部门树 -->
<template>
  <ElCard shadow="hover">
    <div class="dept-tree-toolbar">
      <ElInput v-model="deptName" placeholder="部门名称" class="dept-tree-search">
        <template #prefix>
          <ElIcon>
            <Search />
          </ElIcon>
        </template>
      </ElInput>
      <ElButton
        type="primary"
        link
        size="small"
        class="dept-tree-expand-btn"
        @click="toggleTreeExpandAll"
      >
        <ElIcon :size="14">
          <Switch />
        </ElIcon>
        <span>{{ treeExpanded ? "收起" : "展开" }}</span>
      </ElButton>
    </div>

    <ElTree
      ref="deptTreeRef"
      class="mt-2"
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
  </ElCard>
</template>

<script setup lang="ts">
import { Switch } from "@element-plus/icons-vue";
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
.dept-tree-toolbar {
  display: flex;
  gap: 4px;
  align-items: center;

  .dept-tree-search {
    flex: 1;
    min-width: 0;
  }

  .dept-tree-expand-btn {
    flex-shrink: 0;
    height: auto;
    min-height: unset;
    padding: 0 4px;
    font-size: 12px;
  }
}
</style>
