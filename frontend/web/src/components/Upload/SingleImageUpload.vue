<!-- 单图上传组件 -->
<template>
  <div class="single-image-upload">
    <el-upload
      v-model:file-list="internalFileList"
      class="single-upload"
      list-type="picture-card"
      :show-file-list="false"
      :accept="props.accept"
      :before-upload="handleBeforeUpload"
      :http-request="handleUpload"
      :on-success="onSuccess"
      :on-error="onError"
      :on-remove="handleDelete"
      :disabled="props.disabled"
    >
      <template #default>
        <template v-if="internalFileList && internalFileList.length > 0 && internalFileList[0].url">
          <el-image
            :key="internalFileList[0].url"
            class="single-upload__image"
            :src="internalFileList[0].url"
            fit="cover"
            :preview-src-list="props.enablePreview ? [internalFileList[0].url] : []"
            :preview-teleported="true"
            @click.stop="handleImageClick"
          />
          <el-icon
            v-if="!props.disabled"
            class="single-upload__delete-btn"
            @click.stop="handleDelete"
          >
            <CircleCloseFilled />
          </el-icon>
        </template>
        <template v-else>
          <el-icon class="single-upload__add-btn">
            <Plus />
          </el-icon>
        </template>
      </template>
    </el-upload>
    <div v-if="props.showTip" class="el-upload__tip">
      {{ props.tipText || `支持 ${props.accept} 格式，文件大小不超过 ${props.maxFileSize}MB` }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { UploadRawFile, UploadRequestOptions, ElMessage, type UploadUserFile } from "element-plus";
import ParamsAPI from "@/api/module_system/params";

const props = defineProps({
  /**
   * 请求携带的额外参数
   */
  data: {
    type: Object,
    default: () => {
      return {};
    },
  },
  /**
   * 上传文件的参数名
   */
  name: {
    type: String,
    default: "file",
  },
  /**
   * 最大文件大小（单位：M）
   */
  maxFileSize: {
    type: Number,
    default: 10,
  },

  /**
   * 上传图片格式，默认支持所有图片(image/*)，指定格式示例：'.png,.jpg,.jpeg,.gif,.bmp'
   */
  accept: {
    type: String,
    default: "image/*",
  },

  /**
   * 自定义样式，用于设置组件的宽度和高度等其他样式
   */
  style: {
    type: Object,
    default: () => {
      return {
        width: "150px",
        height: "150px",
      };
    },
  },

  /**
   * 是否禁用
   */
  disabled: {
    type: Boolean,
    default: false,
  },

  /**
   * 是否显示提示信息
   */
  showTip: {
    type: Boolean,
    default: false,
  },

  /**
   * 提示文本
   */
  tipText: {
    type: String,
    default: "",
  },

  /**
   * 是否启用图片预览功能
   */
  enablePreview: {
    type: Boolean,
    default: true,
  },
});

// 接收字符串类型的modelValue，保持与现有代码的兼容性
const modelValue = defineModel<string>({
  default: "",
});

// 内部使用的文件列表
const internalFileList = ref<UploadUserFile[]>([]);

// 监听modelValue变化，同步到internalFileList
watch(
  () => modelValue.value,
  (newVal) => {
    if (newVal) {
      internalFileList.value = [
        {
          name: newVal.split("/").pop() || "image",
          url: newVal,
        },
      ];
    } else {
      internalFileList.value = [];
    }
  },
  { immediate: true }
);

// 监听internalFileList变化，同步到modelValue
watch(
  () => internalFileList.value,
  (newVal) => {
    if (newVal && newVal.length > 0 && newVal[0].url) {
      modelValue.value = newVal[0].url;
    } else {
      modelValue.value = "";
    }
  },
  { deep: true }
);

/**
 * 定义组件触发的事件
 */
const emit = defineEmits<{
  (e: "success", fileInfo: UploadFilePath): void;
  (e: "error", error: any): void;
  (e: "input", value: string): void;
  (e: "update:modelValue", value: string): void;
}>();

/**
 * 限制用户上传文件的格式和大小
 */
function handleBeforeUpload(file: UploadRawFile) {
  // 校验文件类型：虽然 accept 属性限制了用户在文件选择器中可选的文件类型，但仍需在上传时再次校验文件实际类型，确保符合 accept 的规则
  const acceptTypes = props.accept.split(",").map((type) => type.trim());

  // 检查文件格式是否符合 accept
  const isValidType = acceptTypes.some((type) => {
    if (type === "image/*") {
      // 如果是 image/*，检查 MIME 类型是否以 "image/" 开头
      return file.type.startsWith("image/");
    } else if (type.startsWith(".")) {
      // 如果是扩展名 (.png, .jpg)，检查文件名是否以指定扩展名结尾
      return file.name.toLowerCase().endsWith(type);
    } else {
      // 如果是具体的 MIME 类型 (image/png, image/jpeg)，检查是否完全匹配
      return file.type === type;
    }
  });

  if (!isValidType) {
    ElMessage.warning(`上传文件的格式不正确，仅支持：${props.accept}`);
    return false;
  }

  // 限制文件大小
  if (file.size > props.maxFileSize * 1024 * 1024) {
    ElMessage.warning(`上传图片不能大于 ${props.maxFileSize}MB`);
    return false;
  }
  return true;
}

/*
 * 上传图片
 */
async function handleUpload(options: UploadRequestOptions) {
  try {
    const file = options.file;
    const formData = new FormData();

    formData.append(props.name, file);

    // 处理附加参数
    for (const [key, value] of Object.entries(props.data)) {
      formData.append(key, String(value));
    }

    const response = await ParamsAPI.uploadFile(formData);

    if (response.data.code === 0 && response.data) {
      const fileInfo: UploadFilePath = response.data.data;
      // 调用成功回调
      onSuccess(fileInfo);
      return fileInfo;
    } else {
      const errorMsg = response.data.msg || "上传失败";
      ElMessage.error(errorMsg);
      throw new Error(errorMsg);
    }
  } catch (error) {
    onError(error instanceof Error ? error : new Error(String(error)));
    throw error;
  }
}

/**
 * 删除图片
 */
function handleDelete() {
  // 清空模型值并通知父组件
  internalFileList.value = [];
}

/**
 * 图片点击处理
 * 阻止事件冒泡到上传组件，避免触发上传
 */
function handleImageClick(event: Event) {
  // 阻止事件冒泡
  event.stopPropagation();

  // 如果启用了预览功能，则触发预览
  if (
    props.enablePreview &&
    internalFileList.value &&
    internalFileList.value.length > 0 &&
    internalFileList.value[0].url
  ) {
    // Element Plus的el-image组件会自动处理preview-src-list的预览功能
    // 这里只需要阻止冒泡即可
  }
}

/**
 * 上传成功回调
 *
 * @param fileInfo 上传成功后的文件信息
 */
const onSuccess = (fileInfo: UploadFilePath) => {
  // 更新绑定的值为文件URL
  const newFileList = [
    {
      name: fileInfo.file_name,
      url: fileInfo.file_url,
    },
  ];

  internalFileList.value = newFileList;

  // 触发事件
  emit("success", fileInfo);
  emit("input", fileInfo.file_url);
  emit("update:modelValue", fileInfo.file_url);
};

/**
 * 上传失败回调
 */
const onError = (error: any) => {
  console.error("图片上传失败:", error);
  ElMessage.error("图片上传失败，请重试");
  emit("error", error);
};
</script>

<style scoped lang="scss">
.single-image-upload {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.single-upload {
  &__image {
    cursor: pointer;
    border-radius: 6px;
  }

  &__delete-btn {
    position: absolute;
    top: 1px;
    right: 1px;
    display: none;
    font-size: 16px;
    color: var(--el-color-warning);
    cursor: pointer;
    background: var(--el-bg-color-overlay);
    border-radius: 100%;

    &:hover {
      color: var(--el-color-danger);
    }
  }

  &__add-btn {
    font-size: 28px;
    color: var(--el-text-color-placeholder);
  }
}

:deep(.el-upload--picture-card) {
  position: relative;
  width: v-bind("props.style.width ?? '150px'");
  height: v-bind("props.style.height ?? '150px'");

  &:hover {
    .single-upload__delete-btn {
      display: block;
    }
  }
}

.el-upload__tip {
  margin-top: 7px;
  font-size: 12px;
  color: var(--el-text-color-regular);
}
</style>
