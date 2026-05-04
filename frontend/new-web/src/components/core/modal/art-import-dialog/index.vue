<template>
  <div class="crud-import-modal-host">
    <!-- 导入弹窗 -->
    <ArtDialog
      v-model="importModalVisible"
      :title="props.title"
      :width="props.width"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      @close="handleClose"
    >
      <!-- 滚动 -->
      <ElScrollbar :max-height="props.maxHeight">
        <!-- 表单 -->
        <ElForm
          ref="importFormRef"
          style="padding-right: var(--el-dialog-padding-primary)"
          :model="importFormData"
          :rules="importFormRules"
        >
          <ElFormItem prop="files">
            <ElUpload
              ref="uploadRef"
              v-model:file-list="importFormData.files"
              class="w-full"
              :accept="props.accept"
              :drag="true"
              :limit="props.limit"
              :auto-upload="false"
              :on-exceed="handleFileExceed"
            >
              <ElIcon class="el-icon--upload"><UploadFilled /></ElIcon>
              <div class="el-upload__text">
                {{ props.dropText || "将文件拖到此处，或" }}
                <em>{{ props.browseText || "点击上传" }}</em>
              </div>
              <template #tip>
                <div class="el-upload__tip flex flex-wrap gap-2">
                  <ElText v-if="props.note" type="warning" class="mx-1">{{ props.note }}</ElText>
                  <ElText v-if="props.fileTypeWarning" type="danger" class="mx-1">
                    {{ props.fileTypeWarning }}
                  </ElText>
                  <ElLink
                    v-if="props.showTemplateDownload"
                    v-hasPerm="[`${props.contentConfig.permPrefix}:download`]"
                    class="mx-1 inline-flex items-center gap-0.5"
                    type="primary"
                    underline="never"
                    @click="handleDownloadTemplate"
                  >
                    <ElIcon class="text-base"><Download /></ElIcon>
                    <span>{{ props.templateDownloadText || "下载模板" }}</span>
                  </ElLink>
                </div>
              </template>
            </ElUpload>
          </ElFormItem>
        </ElForm>
      </ElScrollbar>
      <template #footer>
        <div style="padding-right: var(--el-dialog-padding-primary)">
          <ElButton @click="handleClose">{{ props.cancelButtonText || "取 消" }}</ElButton>
          <ElButton
            type="primary"
            :disabled="importFormData.files.length === 0 || props.loading"
            :loading="props.loading"
            @click="handleUpload"
          >
            {{ props.confirmButtonText || "确 定" }}
          </ElButton>
        </div>
      </template>
    </ArtDialog>
  </div>
</template>

<script lang="ts" setup>
import { Download, UploadFilled } from "@element-plus/icons-vue";
import ArtDialog from "@/components/Core/modal/art-dialog/index.vue";
import { ElMessage, type UploadUserFile } from "element-plus";
import { ref, reactive } from "vue";
import type { IContentConfig, IObject } from "@/components/Core/modal/types";

defineOptions({ name: "ArtImportDialog", inheritAttrs: false });

/**
 * 导入模态框组件属性定义
 */
interface ArtImportDialogProps {
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
   * 当接口无 Content-Disposition 时使用的默认模板文件名
   */
  defaultTemplateFileName?: string;

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
const props = withDefaults(defineProps<ArtImportDialogProps>(), {
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
        const cd = response.headers?.["content-disposition"] as string | undefined;
        let fileName = props.defaultTemplateFileName || "template.xlsx";
        if (cd) {
          try {
            const part = cd.split(";").find((s) => s.trim().startsWith("filename"));
            if (part) {
              const raw = part.split("=")[1]?.replace(/^"|"$/g, "");
              if (raw) fileName = decodeURI(raw);
            }
          } catch {
            /* 使用 defaultTemplateFileName */
          }
        }
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
