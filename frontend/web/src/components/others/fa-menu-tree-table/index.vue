<template>
  <div class="flex flex-col h-full" v-loading="loading">
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

    <ElScrollbar class="flex-1" :native="false">
      <ElTree
        ref="treeRef"
        node-key="id"
        :data="menuTree"
        show-checkbox
        :check-strictly="!parentChildLinked"
        :default-expand-all="isExpanded"
        :filter-node-method="filterNode"
        :props="{ children: 'children', label: 'name' }"
        @expand-change="handleExpandChange"
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
    </ElScrollbar>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, shallowRef } from "vue";
import { Search, Switch as SwitchIcon } from "@element-plus/icons-vue";
import FaMenuRouteIcon from "@/components/others/fa-menu-route-icon/index.vue";

defineOptions({ name: "FaMenuTreeTable" });

interface MenuNode {
  id?: number;
  type?: number; // 1=目录 2=菜单 3=按钮 4=链接
  name?: string;
  icon?: string;
  parent_id?: number;
  children?: MenuNode[];
}

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

const isLeaf = (t?: number) => t === 3 || t === 4;

type TagType = "primary" | "success" | "warning" | "danger" | "info";
const NODE_META: Record<number, { type: TagType; label: string }> = {
  1: { type: "warning", label: "目录" },
  2: { type: "primary", label: "菜单" },
  3: { type: "success", label: "按钮" },
  4: { type: "danger", label: "链接" },
};
const nodeMeta = (n: MenuNode) => NODE_META[n.type ?? 2] ?? NODE_META[2];

const treeRef = ref<any>(null);
const filterText = ref("");
const isExpanded = ref(false);
const parentChildLinked = ref(true);
const expandedKeys = shallowRef<Set<number>>(new Set());

const getNodesMap = () => treeRef.value?.store?.nodesMap as Record<number, TreeNode> | undefined;

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

function handleExpandChange(data: MenuNode, expanded: boolean) {
  if (data.id != null) {
    if (expanded) {
      expandedKeys.value.add(data.id);
    } else {
      expandedKeys.value.delete(data.id);
    }
  }
}

function expandMatchingNodes(value: string) {
  nextTick(() => {
    const tree = treeRef.value;
    if (!tree) return;
    const nodesMap = getNodesMap();
    if (!nodesMap) return;

    for (const node of Object.values(nodesMap)) {
      if ((node.data.name ?? "").toLowerCase().includes(value.toLowerCase())) {
        let p: TreeNode | null = node;
        while (p) {
          p.expanded = true;
          p = p.parent;
        }
      }
    }
  });
}

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

function initFromProps() {
  nextTick(() => {
    const tree = treeRef.value;
    const nodesMap = getNodesMap();
    if (!tree || !nodesMap) return;

    for (const node of Object.values(nodesMap)) {
      node.checked = false;
      node.indeterminate = false;
      node.expanded = expandedKeys.value.has(node.data.id ?? -1);
    }

    const affected = new Set<TreeNode>();
    for (const id of props.checkedIds ?? []) {
      const node = tree.getNode(id) as TreeNode | null;
      if (!node || !isLeaf(node.data.type)) continue;
      node.checked = true;
      for (let p = node.parent; p; p = p.parent) affected.add(p);
    }

    for (const p of affected) recomputeNode(p);
  });
}

function getCheckedIds(): number[] {
  const tree = treeRef.value;
  if (!tree) return [];
  const ids = new Set<number>();
  for (const n of (tree.getCheckedNodes() ?? []) as MenuNode[]) {
    if (n.id != null && n.type !== 1) ids.add(n.id);
  }
  for (const n of (tree.getHalfCheckedNodes() ?? []) as MenuNode[]) {
    if (n.id != null) ids.add(n.id);
  }
  return [...ids];
}

defineExpose({ getCheckedIds, refresh: initFromProps });

watch(
  () => props.menuTree,
  () => initFromProps(),
  { immediate: true }
);
watch(
  () => props.checkedIds,
  () => initFromProps()
);
watch(parentChildLinked, () => initFromProps());
watch(filterText, (val) => {
  treeRef.value?.filter(val);
  if (val) {
    expandMatchingNodes(val);
  }
});
</script>
