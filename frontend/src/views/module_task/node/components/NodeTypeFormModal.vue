<template>
  <el-dialog
    v-model="dialogVisible"
    :title="isEdit ? '编辑节点类型' : '创建节点类型'"
    :close-on-click-modal="false"
  >
    <el-form :model="formData" label-width="120px">
      <el-form-item label="节点编码" required>
        <el-input v-model="formData.code" placeholder="请输入节点编码" />
      </el-form-item>
      <el-form-item label="节点名称" required>
        <el-input v-model="formData.name" placeholder="请输入节点名称" />
      </el-form-item>
      <el-form-item label="节点分类">
        <el-select v-model="formData.category" placeholder="请选择节点分类" style="width: 100%">
          <el-option label="触发器" value="trigger" />
          <el-option label="动作" value="action" />
          <el-option label="条件" value="condition" />
          <el-option label="控制" value="control" />
          <el-option label="集成" value="integration" />
          <el-option label="自定义" value="custom" />
        </el-select>
      </el-form-item>
      <el-form-item label="配置Schema">
        <el-input
          v-model="configSchemaJson"
          type="textarea"
          :rows="5"
          placeholder="请输入配置Schema(JSON格式)"
        />
      </el-form-item>
      <el-form-item label="节点描述">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="3"
          placeholder="请输入节点描述"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="handleCancel">取消</el-button>
      <el-button type="primary" :loading="loading" @click="handleOk">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, watch, computed } from "vue";
import { ElMessage } from "element-plus";
import NodeAPI, { type NodeType, type NodeTypeForm } from "@/api/module_task/node";

const props = defineProps({
  visible: {
    type: Boolean,
    default: false,
  },
  nodeType: {
    type: Object as () => NodeType | undefined,
    default: undefined,
  },
});

const emit = defineEmits(["update:visible", "refresh"]);

const loading = ref(false);
const configSchemaJson = ref("{}");
const formData = reactive<Partial<NodeTypeForm>>({
  code: "",
  name: "",
  category: "action",
  description: "",
  config_schema: {},
});

const isEdit = computed(() => !!props.nodeType?.id);

const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit("update:visible", val),
});

watch(
  () => props.nodeType,
  (newNodeType) => {
    if (newNodeType) {
      Object.assign(formData, {
        code: newNodeType.code,
        name: newNodeType.name,
        category: newNodeType.category,
        description: newNodeType.description,
      });
      configSchemaJson.value = JSON.stringify(newNodeType.config_schema || {}, null, 2);
    } else {
      Object.assign(formData, {
        code: "",
        name: "",
        category: "action",
        description: "",
      });
      configSchemaJson.value = "{}";
    }
  },
  { immediate: true }
);

const handleOk = async () => {
  if (!formData.code || !formData.name) {
    ElMessage.error("请填写必填项");
    return;
  }

  try {
    formData.config_schema = JSON.parse(configSchemaJson.value);
  } catch {
    ElMessage.error("配置Schema格式错误，请输入有效的JSON");
    return;
  }

  loading.value = true;
  try {
    if (isEdit.value) {
      await NodeAPI.updateNodeType(props.nodeType!.id!, formData as NodeTypeForm);
    } else {
      await NodeAPI.createNodeType(formData as NodeTypeForm);
    }
    emit("refresh");
    handleCancel();
  } catch {
    ElMessage.error(isEdit.value ? "更新失败" : "创建失败");
  } finally {
    loading.value = false;
  }
};

const handleCancel = () => {
  emit("update:visible", false);
};
</script>

<style scoped lang="scss">
.icon-selector {
  display: flex;
  gap: 12px;
  align-items: center;
}

.color-selector {
  display: flex;
  gap: 12px;
  align-items: center;

  .color-presets {
    display: flex;
    gap: 8px;

    .color-preset {
      width: 24px;
      height: 24px;
      cursor: pointer;
      border: 2px solid transparent;
      border-radius: 4px;
      transition: all 0.3s;

      &:hover {
        border-color: #409eff;
        transform: scale(1.1);
      }
    }
  }
}

.icon-picker {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 12px;
  max-height: 400px;
  overflow-y: auto;

  .icon-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16px;
    cursor: pointer;
    border: 2px solid #dcdfe6;
    border-radius: 8px;
    transition: all 0.3s;

    &:hover {
      background-color: #ecf5ff;
      border-color: #409eff;
    }

    &.active {
      background-color: #ecf5ff;
      border-color: #409eff;
      box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
    }

    span {
      margin-top: 8px;
      font-size: 12px;
      color: #606266;
    }
  }
}
</style>
