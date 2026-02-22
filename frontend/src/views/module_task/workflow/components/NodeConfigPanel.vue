<template>
  <div class="node-config-panel">
    <div class="panel-header">
      <span>节点配置</span>
      <ElButton type="text" class="close-btn" @click="handleClose">
        <ElIcon><Close /></ElIcon>
      </ElButton>
    </div>

    <div class="panel-content">
      <ElForm :model="formData" label-width="80px" size="small">
        <ElFormItem label="节点类型">
          <ElSelect v-model="formData.type" placeholder="请选择节点类型" @change="handleTypeChange">
            <ElOption
              v-for="type in nodeTypes"
              :key="type.id"
              :label="type.name"
              :value="type.code"
            />
          </ElSelect>
        </ElFormItem>

        <ElFormItem label="节点名称">
          <ElInput v-model="formData.label" placeholder="请输入节点名称" />
        </ElFormItem>

        <ElFormItem label="位置参数">
          <ElInput v-model="formData.args" placeholder="多个参数用逗号分隔，如: arg1, arg2, arg3" />
          <div class="field-hint">多个参数用逗号分隔</div>
        </ElFormItem>

        <ElFormItem label="关键字参数">
          <ElInput
            v-model="formData.kwargsStr"
            type="textarea"
            :rows="4"
            placeholder='JSON格式，如: {"key": "value", "count": 10}'
          />
          <div class="field-hint">JSON 格式的关键字参数</div>
        </ElFormItem>

        <ElFormItem label="描述">
          <ElInput
            v-model="formData.description"
            type="textarea"
            :rows="2"
            placeholder="请输入描述信息"
          />
        </ElFormItem>
      </ElForm>

      <div class="panel-actions">
        <ElButton type="primary" size="small" @click="handleSave">保存</ElButton>
        <ElButton type="danger" size="small" @click="handleDelete">删除节点</ElButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import {
  ElButton,
  ElForm,
  ElFormItem,
  ElInput,
  ElSelect,
  ElOption,
  ElMessage,
  ElIcon,
} from "element-plus";
import { Close } from "@element-plus/icons-vue";
import NodeAPI, { type NodeType } from "@/api/module_task/node";

const props = defineProps({
  node: {
    type: Object,
    default: () => ({}),
  },
});

const emit = defineEmits(["close", "save", "delete"]);

const nodeTypes = ref<NodeType[]>([]);

const formData = ref({
  type: props.node?.type || "",
  label: props.node?.data?.label || "",
  args: props.node?.data?.args || "",
  kwargsStr: props.node?.data?.kwargsStr || "{}",
  description: props.node?.data?.description || "",
});

const loadNodeTypes = async () => {
  try {
    const res = await NodeAPI.getNodeTypeOptions();
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

      formData.value = {
        type: newNode.type || "",
        label: newNode.data?.label || "",
        args: newNode.data?.args || "",
        kwargsStr,
        description: newNode.data?.description || "",
      };
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
</style>
