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

        <ElFormItem v-if="nodeConfigSchema && nodeConfigSchema.length > 0" label="节点配置">
          <div v-for="(field, index) in nodeConfigSchema" :key="index" class="config-field">
            <ElFormItem :label="field.label">
              <ElInput
                v-if="field.type === 'text' || field.type === 'textarea'"
                v-model="formData.config[field.key]"
                :type="field.type"
                :rows="field.rows || 2"
                :placeholder="field.placeholder || `请输入${field.label}`"
              />
              <ElSelect
                v-else-if="field.type === 'select'"
                v-model="formData.config[field.key]"
                :placeholder="field.placeholder || `请选择${field.label}`"
              >
                <ElOption
                  v-for="option in field.options"
                  :key="option.value"
                  :label="option.label"
                  :value="option.value"
                />
              </ElSelect>
              <ElInputNumber
                v-else-if="field.type === 'number'"
                v-model="formData.config[field.key]"
                :min="field.min"
                :max="field.max"
              />
              <ElSwitch v-else-if="field.type === 'boolean'" v-model="formData.config[field.key]" />
            </ElFormItem>
          </div>
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
  ElInputNumber,
  ElSwitch,
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
const selectedTemplate = ref<number>();
const nodeConfigSchema = ref<any[]>([]);

const formData = ref({
  type: props.node?.type || "",
  label: props.node?.data?.label || "",
  config: props.node?.data?.config || {},
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
  if (nodeType && nodeType.config_schema) {
    nodeConfigSchema.value = nodeType.config_schema.fields || [];
  } else {
    nodeConfigSchema.value = [];
  }

  selectedTemplate.value = undefined;
  formData.value.config = {};
};

watch(
  () => props.node,
  (newNode) => {
    if (newNode) {
      formData.value = {
        type: newNode.type || "",
        label: newNode.data?.label || "",
        config: newNode.data?.config || {},
        description: newNode.data?.description || "",
      };

      if (newNode.type) {
        handleTypeChange(newNode.type);
      }
    }
  },
  { deep: true }
);

function handleClose() {
  emit("close");
}

function handleSave() {
  emit("save", formData.value);
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

.config-field {
  margin-bottom: 8px;
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
