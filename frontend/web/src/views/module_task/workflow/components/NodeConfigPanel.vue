<template>
  <div class="node-config-panel">
    <div class="panel-header">
      <span>节点配置</span>
      <ElButton type="text" class="close-btn" @click="handleClose">
        <ElIcon><Close /></ElIcon>
      </ElButton>
    </div>

    <div class="panel-content">
      <FaForm
        v-model="formData"
        :items="nodePanelFormItems"
        label-width="80px"
        size="small"
        label-position="right"
        :span="24"
        :gutter="12"
        :show-reset="false"
        :show-submit="false"
        class="panel-art-form"
      >
        <template #type>
          <ElSelect v-model="formData.type" placeholder="请选择节点类型" @change="handleTypeChange">
            <ElOption v-for="t in nodeTypes" :key="t.id" :label="t.name" :value="t.code" />
          </ElSelect>
        </template>
        <template #args>
          <div>
            <ElInput
              v-model="formData.args"
              placeholder="多个参数用逗号分隔，如: arg1, arg2, arg3"
            />
            <div class="field-hint">多个参数用逗号分隔</div>
          </div>
        </template>
        <template #kwargsStr>
          <div>
            <ElInput
              v-model="formData.kwargsStr"
              type="textarea"
              :rows="4"
              placeholder='JSON格式，如: {"key": "value", "count": 10}'
            />
            <div class="field-hint">JSON 格式的关键字参数</div>
          </div>
        </template>
      </FaForm>

      <div class="panel-actions">
        <ElButton type="primary" size="small" @click="handleSave">保存</ElButton>
        <ElButton type="danger" size="small" @click="handleDelete">删除节点</ElButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, computed } from "vue";
import { ElButton, ElInput, ElSelect, ElOption, ElMessage, ElIcon } from "element-plus";
import { Close } from "@element-plus/icons-vue";
import FaForm from "@/components/forms/fa-form/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import WorkflowNodeTypeAPI, {
  type WorkflowNodeTypeOption,
} from "@/api/module_task/workflow/node-type";

const props = defineProps({
  node: {
    type: Object,
    default: () => ({}),
  },
});

const emit = defineEmits(["close", "save", "delete"]);

const nodeTypes = ref<WorkflowNodeTypeOption[]>([]);

const formData = ref({
  type: props.node?.type || "",
  label: props.node?.data?.label || "",
  args: props.node?.data?.args || "",
  kwargsStr: props.node?.data?.kwargsStr || "{}",
  description: props.node?.data?.description || "",
});

const nodePanelFormItems = computed<FormItem[]>(() => [
  {
    label: "节点类型",
    key: "type",
    type: "input",
    span: 24,
    placeholder: "",
  },
  {
    label: "节点名称",
    key: "label",
    type: "input",
    span: 24,
    props: { placeholder: "请输入节点名称" },
  },
  {
    label: "位置参数",
    key: "args",
    type: "input",
    span: 24,
    placeholder: "",
  },
  {
    label: "关键字参数",
    key: "kwargsStr",
    type: "input",
    span: 24,
    placeholder: "",
  },
  {
    label: "描述",
    key: "description",
    type: "input",
    span: 24,
    props: {
      type: "textarea",
      rows: 2,
      placeholder: "请输入描述信息",
    },
  },
]);

const loadNodeTypes = async () => {
  try {
    const res = await WorkflowNodeTypeAPI.getWorkflowNodeTypeOptions();
    if (res.data) {
      nodeTypes.value = res.data.data || [];
    }
  } catch {
    ElMessage.error("加载节点类型失败");
  }
};

const handleTypeChange = async (typeCode: string) => {
  const nodeType = nodeTypes.value.find((t) => t.code === typeCode);
  if (nodeType) {
    formData.value.args = nodeType.args || "";
    formData.value.kwargsStr = nodeType.kwargs || "{}";
  }
};

watch(
  () => props.node,
  (newNode) => {
    if (newNode) {
      const kwargsData = newNode.data?.kwargs;
      let kwargsStr = "{}";
      if (kwargsData) {
        if (typeof kwargsData === "string") {
          kwargsStr = kwargsData;
        } else if (typeof kwargsData === "object") {
          kwargsStr = JSON.stringify(kwargsData, null, 2);
        }
      }

      Object.assign(formData, {
        type: newNode.type || "",
        label: newNode.data?.label || "",
        args: newNode.data?.args || "",
        kwargsStr,
        description: newNode.data?.description || "",
      });
    }
  },
  { deep: true, immediate: true }
);

function handleClose() {
  emit("close");
}

function handleSave() {
  try {
    if (formData.value.kwargsStr && formData.value.kwargsStr.trim()) {
      JSON.parse(formData.value.kwargsStr);
    }
  } catch {
    ElMessage.error("关键字参数 JSON 格式错误");
    return;
  }

  emit("save", {
    type: formData.value.type,
    label: formData.value.label,
    args: formData.value.args,
    kwargs: formData.value.kwargsStr,
    description: formData.value.description,
  });
  ElMessage.success("保存成功");
}

function handleDelete() {
  emit("delete");
}

onMounted(() => {
  loadNodeTypes();
  if (props.node?.type) {
    handleTypeChange(props.node.type);
  }
});
</script>

<style scoped>
.node-config-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  font-weight: 600;
  border-bottom: 1px solid #e5e7eb;
}

.close-btn {
  padding: 4px;
}

.panel-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.field-hint {
  margin-top: 4px;
  font-size: 12px;
  color: #909399;
}

.panel-actions {
  display: flex;
  gap: 8px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

.panel-actions .el-button {
  flex: 1;
}

.panel-art-form ::v-deep(.el-row > .el-col:last-child) {
  display: none;
}

.panel-art-form ::v-deep(.el-form-item__content) {
  max-width: 100%;
}

.panel-art-form ::v-deep(section) {
  padding: 0;
}
</style>
