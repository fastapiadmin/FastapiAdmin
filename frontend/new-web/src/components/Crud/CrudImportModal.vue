<template>
  <div class="crud-import-modal-host">
    <!-- 导入弹窗 -->
    <EnhancedDialog
      v-model="importModalVisible"
      :title="props.title"
      :width="props.width"
      dialog-class="crud-embed-dialog"
      @close="handleClose"
    >
      <!-- 滚动 -->
      <el-scrollbar :max-height="props.maxHeight">
        <!-- 表单 -->
        <el-form
          ref="importFormRef"
          style="padding-right: var(--el-dialog-padding-primary)"
          :model="importFormData"
          :rules="importFormRules"
        >
          <el-form-item prop="files">
            <el-upload
              ref="uploadRef"
              v-model:file-list="importFormData.files"
              class="w-full"
              :accept="props.accept"
              :drag="true"
              :limit="props.limit"
              :auto-upload="false"
              :on-exceed="handleFileExceed"
            >
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                {{ props.dropText || "将文件拖到此处，或" }}
                <em>{{ props.browseText || "点击上传" }}</em>
              </div>
              <template #tip>
                <div class="el-upload__tip flex flex-wrap gap-2">
                  <el-text v-if="props.note" type="warning" class="mx-1">{{ props.note }}</el-text>
                  <el-text v-if="props.fileTypeWarning" type="danger" class="mx-1">
                    {{ props.fileTypeWarning }}
                  </el-text>
                  <el-link
                    v-if="props.showTemplateDownload"
                    v-hasPerm="[`${props.contentConfig.permPrefix}:download`]"
                    class="mx-1"
                    type="primary"
                    icon="download"
                    underline="never"
                    @click="handleDownloadTemplate"
                  >
                    {{ props.templateDownloadText || "下载模板" }}
                  </el-link>
                </div>
              </template>
            </el-upload>
          </el-form-item>
        </el-form>
      </el-scrollbar>
      <template #footer>
        <div style="padding-right: var(--el-dialog-padding-primary)">
          <el-button @click="handleClose">{{ props.cancelButtonText || "取 消" }}</el-button>
          <el-button
            type="primary"
            :disabled="importFormData.files.length === 0 || props.loading"
            :loading="props.loading"
            @click="handleUpload"
          >
            {{ props.confirmButtonText || "确 定" }}
          </el-button>
        </div>
      </template>
    </EnhancedDialog>
  </div>
</template>

<script lang="ts" setup>
import EnhancedDialog from "@/components/Core/overlays/EnhancedDialog.vue";
import { ElMessage, type UploadUserFile } from "element-plus";
import { ref, reactive } from "vue";
import type { IContentConfig, IObject } from "./types";

/**
 * 导入模态框组件属性定义
 */
interface CrudImportModalProps {
  /**
   * 弹窗标题
   */
  title?: string;

  /**
   * 弹窗宽度
   */
  width?: string;

  /**
   * 最大高度
   */
  maxHeight?: string;

  /**
   * 接受的文件类型
   */
  accept?: string;

  /**
   * 文件数量限制
   */
  limit?: number;

  /**
   * 是否显示下载模板按钮
   */
  showTemplateDownload?: boolean;

  /**
   * 拖放提示文本
   */
  dropText?: string;

  /**
   * 浏览按钮文本
   */
  browseText?: string;

  /**
   * 模板下载按钮文本
   */
  templateDownloadText?: string;

  /**
   * 取消按钮文本
   */
  cancelButtonText?: string;

  /**
   * 确认按钮文本
   */
  confirmButtonText?: string;

  /**
   * 注意事项文本
   */
  note?: string;

  /**
   * 文件类型警告文本
   */
  fileTypeWarning?: string;

  /**
   * 上传文件的参数名
   */
  uploadFileName?: string;

  /**
   * 上传请求的额外参数
   */
  uploadData?: IObject;

  /**
   * 导入配置
   */
  contentConfig: IContentConfig;

  /**
   * 上传loading状态
   */
  loading?: boolean;
}

// 定义props
const props = withDefaults(defineProps<CrudImportModalProps>(), {
  title: "导入数据",
  width: "600px",
  maxHeight: "60vh",
  accept:
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel",
  limit: 1,
  showTemplateDownload: true,
  note: "注意事项：",
  fileTypeWarning: "格式为*.xlsx / *.xls，文件不超过 5MB",
  uploadFileName: "file",
  uploadData: () => ({}),
});

// 定义模型值（控制弹窗显示/隐藏）
const importModalVisible = defineModel<boolean>("modelValue", {
  required: true,
  default: false,
});

// 定义事件
const emit = defineEmits<{
  /** 导入成功事件 */
  "import-success": [data: any];
  /** 导入失败事件 */
  "import-fail": [error: any];
  /** 关闭事件 */
  close: [];
  /** 下载模板事件 */
  "download-template": [];
  /** 上传事件 */
  upload: [formData: FormData, file: File];
}>();

// 引用
const importFormRef = ref(null);
const uploadRef = ref(null);

// 表单数据
const importFormData = reactive<{
  files: UploadUserFile[];
}>({
  files: [],
});

// 表单规则
const importFormRules = {
  files: [{ required: true, message: "文件不能为空", trigger: "blur" }],
};

// 文件超出个数限制
const handleFileExceed = () => {
  ElMessage.warning(`只能上传${props.limit}个文件`);
};

// 浏览器保存文件
function saveXlsx(fileData: any, fileName: string) {
  const fileType =
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8";

  const blob = new Blob([fileData], { type: fileType });
  const downloadUrl = window.URL.createObjectURL(blob);

  const downloadLink = document.createElement("a");
  downloadLink.href = downloadUrl;
  downloadLink.download = fileName;

  document.body.appendChild(downloadLink);
  downloadLink.click();

  document.body.removeChild(downloadLink);
  window.URL.revokeObjectURL(downloadUrl);
}

// 下载导入模板
function handleDownloadTemplate() {
  try {
    const importTemplate = props.contentConfig.importTemplate;
    if (typeof importTemplate === "string") {
      window.open(importTemplate);
    } else if (typeof importTemplate === "function") {
      importTemplate().then((response) => {
        const fileData = response.data;
        const fileName = decodeURI(
          response.headers["content-disposition"].split(";")[1].split("=")[1]
        );
        saveXlsx(fileData, fileName);
      });
    } else {
      ElMessage.error("未配置importTemplate");
    }
  } catch (error) {
    console.error("下载模板失败:", error);
    ElMessage.error("下载模板失败");
  }
}

// 上传文件 - 由父组件实现具体逻辑
const handleUpload = async () => {
  if (!importFormData.files.length) {
    ElMessage.warning("请选择文件");
    return;
  }

  try {
    const file = importFormData.files[0].raw as File;
    const formData = new FormData();
    formData.append(props.uploadFileName, file);

    Object.keys(props.uploadData).forEach((key) => {
      formData.append(key, props.uploadData[key]);
    });

    emit("upload", formData, file);
  } catch (error: any) {
    console.error("上传失败:", error);
    ElMessage.error("上传失败：" + error.message || error);
    emit("import-fail", error);
  }
};

// 关闭弹窗
const handleClose = () => {
  importFormData.files.length = 0;
  importModalVisible.value = false;
  emit("close");
};

// 提供给父组件的方法
defineExpose({
  handleClose,
});
</script>
