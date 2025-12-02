<!-- 部门树 -->
<template>
  <el-card shadow="hover">
    <el-input v-model="deptName" placeholder="部门名称">
      <template #prefix>
        <el-icon>
          <Search />
        </el-icon>
      </template>
    </el-input>

    <el-tree
      ref="deptTreeRef"
      class="mt-2"
      :data="deptOptions"
      :props="{ children: 'children', label: 'label', disabled: 'disabled' }"
      :expand-on-click-node="false"
      :filter-node-method="handleFilter"
      default-expand-all
      @node-click="handleNodeClick"
    >
      <template #empty>
        <el-empty :image-size="80" description="暂无数据" />
      </template>
    </el-tree>
  </el-card>
</template>

<script setup lang="ts">
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

const emits = defineEmits(["node-click", "update:modelValue"]);

const deptId = useVModel(props, "modelValue", emits);

watch(deptName, (val) => {
  deptTreeRef.value!.filter(val);
});

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
