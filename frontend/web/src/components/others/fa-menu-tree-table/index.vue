<template>
  <div class="flex flex-col h-full">
    <!-- 搜索栏 + 操作按钮 -->
    <div class="mb-3 flex items-center gap-3 shrink-0">
      <ElInput
        v-model="filterText"
        placeholder="搜索菜单名称"
        clearable
        class="menu-tree-search-input"
        :prefix-icon="Search"
        size="small"
      />
      <ElButton type="primary" size="small" plain @click="toggleExpandAll">
        <template #icon><SwitchIcon /></template>
        {{ isExpanded ? "收起" : "展开" }}
      </ElButton>
      <ElCheckbox v-model="parentChildLinked">父子联动</ElCheckbox>
    </div>

    <!-- 菜单树 -->
    <div class="flex-1 overflow-auto" v-loading="loading">
      <ElTree
        ref="treeRef"
        node-key="id"
        :data="menuTree"
        show-checkbox
        :check-strictly="!parentChildLinked"
        :default-expand-all="isExpanded"
        :filter-node-method="filterNode"
        :props="{ children: 'children', label: 'name' }"
      >
        <template #default="{ data }">
          <div class="menu-node flex items-center gap-2">
            <FaMenuRouteIcon v-if="data.icon" :icon="data.icon" />
            <span class="node-name" :class="{ 'is-dir': data.type === 1 }">
              {{ data.name }}
            </span>
            <ElTag :type="nodeMeta(data)!.type" size="small" effect="plain" round>
              {{ nodeMeta(data)!.label }}
            </ElTag>
          </div>
        </template>
      </ElTree>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from "vue";
import { Search, Switch as SwitchIcon } from "@element-plus/icons-vue";
import FaMenuRouteIcon from "@/components/others/fa-menu-route-icon/index.vue";

defineOptions({ name: "FaMenuTreeTable" });

// ==================== 类型 ====================
interface MenuNode {
  id?: number;
  type?: number; // 1=目录 2=菜单 3=按钮 4=链接
  name?: string;
  icon?: string;
  parent_id?: number;
  children?: MenuNode[];
}

// el-tree 内部节点结构（仅用到部分字段）
interface TreeNode {
  data: MenuNode;
  checked: boolean;
  indeterminate: boolean;
  expanded?: boolean;
  childNodes: TreeNode[];
  parent: TreeNode | null;
}

interface Props {
  menuTree: MenuNode[];
  checkedIds?: number[];
  loading?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  checkedIds: () => [],
  loading: false,
});

// 节点类型常量（1=目录 2=菜单 3=按钮 4=链接）
const isLeaf = (t?: number) => t === 3 || t === 4; // 按钮 / 链接

// 节点类型 → 标签样式 / 文案
type TagType = "primary" | "success" | "warning" | "danger" | "info";
const NODE_META: Record<number, { type: TagType; label: string }> = {
  1: { type: "warning", label: "目录" },
  2: { type: "primary", label: "菜单" },
  3: { type: "success", label: "按钮" },
  4: { type: "danger", label: "链接" },
};
const nodeMeta = (n: MenuNode) => NODE_META[n.type ?? 2] ?? NODE_META[2];

// ==================== 状态 ====================
const treeRef = ref<any>(null);
const filterText = ref("");
const isExpanded = ref(true);
const parentChildLinked = ref(true);

// 工具：安全获取 el-tree 内部 nodesMap
const getNodesMap = () => treeRef.value?.store?.nodesMap as Record<number, TreeNode> | undefined;

// ==================== 搜索 / 展开 ====================
function filterNode(value: string, data: any) {
  if (!value) return true;
  return (data.name ?? "").toLowerCase().includes(value.toLowerCase());
}

function setAllExpanded(expanded: boolean) {
  nextTick(() => {
    const nodesMap = getNodesMap();
    if (!nodesMap) return;
    for (const node of Object.values(nodesMap)) {
      node.expanded = expanded;
    }
  });
}

function toggleExpandAll() {
  isExpanded.value = !isExpanded.value;
  setAllExpanded(isExpanded.value);
}

// ==================== 父级状态计算 ====================
// 单次遍历子节点：统计 fully checked + 是否存在 indeterminate
function recomputeNode(p: TreeNode) {
  let fully = 0;
  let hasIndeterminate = false;
  for (const c of p.childNodes) {
    if (c.checked) fully++;
    else if (c.indeterminate) hasIndeterminate = true;
  }
  const total = p.childNodes.length;
  p.checked = fully === total;
  p.indeterminate = (fully > 0 || hasIndeterminate) && !p.checked;
}

// ==================== 初始化 ====================
// 回显策略：只勾叶子（按钮/链接），父级状态自动向上传播半选
function initFromProps() {
  nextTick(() => {
    const tree = treeRef.value;
    const nodesMap = getNodesMap();
    if (!tree || !nodesMap) return;

    // 1. 清空
    for (const node of Object.values(nodesMap)) {
      node.checked = false;
      node.indeterminate = false;
    }

    // 2. 勾叶子 + 收集受影响父级（去重，每个父级只重算一次）
    const affected = new Set<TreeNode>();
    for (const id of props.checkedIds ?? []) {
      const node = tree.getNode(id) as TreeNode | null;
      if (!node || !isLeaf(node.data.type)) continue;
      node.checked = true;
      for (let p = node.parent; p; p = p.parent) affected.add(p);
    }

    // 3. 统一重算
    for (const p of affected) recomputeNode(p);
  });
}

// ==================== 对外 API ====================
function getCheckedIds(): number[] {
  const tree = treeRef.value;
  if (!tree) return [];
  const ids = new Set<number>();
  // 完全选中的菜单 / 按钮 / 链接
  for (const n of (tree.getCheckedNodes() ?? []) as MenuNode[]) {
    if (n.id != null && n.type !== 1) ids.add(n.id);
  }
  // 半选父级（菜单 + 目录）—— 作为父级路径传后端
  for (const n of (tree.getHalfCheckedNodes() ?? []) as MenuNode[]) {
    if (n.id != null) ids.add(n.id);
  }
  return [...ids];
}

defineExpose({ getCheckedIds, refresh: initFromProps });

// ==================== 监听 ====================
watch(
  () => [props.menuTree, props.checkedIds] as const,
  () => initFromProps(),
  { immediate: true, deep: true }
);
// 切换父子联动时重新初始化：check-strictly 改变需要重置半选状态
watch(parentChildLinked, () => initFromProps());
watch(filterText, (val) => {
  treeRef.value?.filter(val);
  if (val) {
    isExpanded.value = true;
    setAllExpanded(true);
  }
});
</script>
