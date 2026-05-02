<!-- 列表选择器 -->
<template>
  <table-select
    :text="text"
    :select-config="selectConfig"
    @confirm-click="handleConfirm"
    @clear-click="handleClearSelection"
  >
    <template #status="scope">
      <el-tag :type="scope.row[scope.prop] === '0' ? 'success' : 'danger'">
        {{ scope.row[scope.prop] === "0" ? "启用" : "停用" }}
      </el-tag>
    </template>
  </table-select>
</template>

<script setup lang="ts">
import type { ISelectConfig } from "@/components/TableSelect/index.vue";
import UserAPI from "@/api/module_system/user";

// 父组件双向绑定的值（选中用户ID）
const props = defineProps<{ modelValue?: number }>();

// 事件向上派发，支持父组件监听和 v-model（仅回传选中用户ID）
const emit = defineEmits<{
  confirmClick: [data: IUser[]];
  "update:modelValue": [val: number | undefined];
}>();

const selectConfig: ISelectConfig = {
  pk: "id",
  width: "167.5px", // 与搜索表单其他输入宽度一致
  placeholder: "请选择用户",
  popover: {
    width: 720, // 弹出层宽度，提升可用性（约 720px）
  },
  formItems: [
    {
      type: "select",
      label: "状态",
      prop: "status",
      initialValue: "0",
      attrs: {
        placeholder: "全部",
        clearable: true,
        style: {
          width: "140px",
        },
      },
      options: [
        { label: "启用", value: "0" },
        { label: "停用", value: "1" },
      ],
    },
  ],
  indexAction(params) {
    // 映射查询参数到后端接口
    const query: any = { ...params };
    // 清理空字符串/空值，避免后端 422
    Object.keys(query).forEach((k) => {
      const v = query[k];
      if (v === "" || v === null || v === undefined) {
        delete query[k];
      }
    });
    // 规范化状态为布尔值
    if (typeof query.status === "string") {
      if (query.status === "true") query.status = true;
      else if (query.status === "false") query.status = false;
    }
    // 请求用户分页列表并适配 TableSelect 需要的结构
    return UserAPI.listUser(query).then((res: any) => {
      return {
        total: res.data.data.total,
        list: res.data.data.items,
      };
    });
  },
  tableColumns: [
    { type: "selection", width: 50, align: "center" },
    { label: "编号", align: "center", prop: "id", width: 100 },
    { label: "账号", align: "center", prop: "username" },
    { label: "用户名", align: "center", prop: "name", width: 120 },
    {
      label: "状态",
      align: "center",
      prop: "status",
      templet: "custom",
      slotName: "status",
    },
  ],
};

interface IUser {
  id: number;
  username: string;
  name: string;
  mobile?: string;
  gender?: string;
  avatar?: string;
  email?: string | null;
  status?: string;
  dept_name?: string;
  role_names?: string[];
  created_time?: string;
}
const selectedUser = ref<IUser>();
function handleConfirm(data: IUser[]) {
  selectedUser.value = data[0];
  const id = selectedUser.value?.id;
  emit("update:modelValue", id);
  emit("confirmClick", data);
}
function handleClearSelection() {
  selectedUser.value = undefined;
  emit("update:modelValue", undefined);
}

// 当父组件重置 v-model（modelValue）为 undefined 时，清空本地显示
watch(
  () => props.modelValue,
  (val) => {
    if (val === undefined || val === null) {
      selectedUser.value = undefined;
    }
  }
);

const text = computed(() => {
  return selectedUser.value ? `${selectedUser.value.username} - ${selectedUser.value.name}` : "";
});
</script>
