<template>
  <div class="crud-export-modal-host">
    <!-- 导出弹窗 -->
    <FaDialog
      v-model="exportsModalVisible"
      title="导出数据"
      width="600px"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      @close="handleCloseExportsModal"
    >
      <!-- 滚动 -->
      <ElScrollbar max-height="60vh">
        <!-- 表单 -->
        <ElForm
          ref="exportsFormRef"
          style="padding-right: var(--el-dialog-padding-primary)"
          :model="exportsFormData"
          :rules="exportsFormRules"
        >
          <ElFormItem label="文件名" prop="filename">
            <ElInput v-model="exportsFormData.filename" placeholder="请输入文件名" clearable />
          </ElFormItem>
          <ElFormItem label="工作表名" prop="sheetname">
            <ElInput v-model="exportsFormData.sheetname" placeholder="请输入工作表名" clearable />
          </ElFormItem>
          <ElFormItem label="数据源" prop="origin">
            <ElSelect v-model="exportsFormData.origin">
              <ElOption
                label="当前数据 (当前页的数据)"
                :value="ExportsOriginEnum.CURRENT"
                :disabled="!pageData?.length"
              />
              <ElOption
                label="选中数据 (所有选中的数据)"
                :value="ExportsOriginEnum.SELECTED"
                :disabled="!selectionData?.length"
              />
              <ElOption
                label="全量数据 (所有分页的数据)"
                :value="ExportsOriginEnum.REMOTE"
                :disabled="!remoteExportEnabled"
              />
            </ElSelect>
          </ElFormItem>
          <ElFormItem label="字段" prop="fields">
            <ElCheckboxGroup v-model="exportsFormData.fields">
              <template v-for="col in cols" :key="col.prop">
                <ElCheckbox v-if="col.prop" :value="col.prop" :label="col.label" />
              </template>
            </ElCheckboxGroup>
          </ElFormItem>
        </ElForm>
      </ElScrollbar>
      <!-- 弹窗底部操作按钮 -->
      <template #footer>
        <div style="padding-right: var(--el-dialog-padding-primary)">
          <ElButton type="primary" @click="handleExportsSubmit">确 定</ElButton>
          <ElButton @click="handleCloseExportsModal">取 消</ElButton>
        </div>
      </template>
    </FaDialog>
  </div>
</template>

<script lang="ts" setup>
import FaDialog from "@/components/modal/fa-dialog/index.vue";
import ExcelJS from "exceljs";
import type { IContentConfig, IObject } from "@/components/modal/types";
import { useThrottleFn } from "@vueuse/core";
import { type FormInstance, type FormRules, ElMessage } from "element-plus";
import { nextTick, ref, reactive, computed } from "vue";

defineOptions({ name: "FaExportDialog", inheritAttrs: false });

function saveBlobDownload(blob: Blob, rawName: string) {
  const name = /\.xlsx?$/i.test(rawName) ? rawName : `${rawName}.xlsx`;
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  URL.revokeObjectURL(url);
}

/**
 * 导出模态框组件属性定义
 */
interface FaExportDialogProps {
  /** 内容配置 */
  contentConfig: Pick<
    IContentConfig,
    "permPrefix" | "cols" | "exportsAction" | "exportsBlobAction"
  >;
  /** 查询参数 */
  queryParams?: IObject;
  /** 页面数据 */
  pageData?: IObject[];
  /** 选中数据 */
  selectionData?: IObject[];
}

// 定义接收的属性
const props = defineProps<FaExportDialogProps>();

const remoteExportEnabled = computed(
  () => !!(props.contentConfig.exportsAction || props.contentConfig.exportsBlobAction)
);

// 定义模型值（控制弹窗显示/隐藏）
const exportsModalVisible = defineModel<boolean>("modelValue", {
  required: true,
  default: false,
});

/**
 * 导出数据源枚举
 */
enum ExportsOriginEnum {
  /** 当前数据 */
  CURRENT = "current",
  /** 选中数据 */
  SELECTED = "selected",
  /** 远程数据 */
  REMOTE = "remote",
}

const exportsFormRef = ref<FormInstance>();
const exportsFormData = reactive({
  filename: "",
  sheetname: "",
  fields: [] as string[],
  origin: ExportsOriginEnum.CURRENT,
});
const exportsFormRules: FormRules = {
  fields: [{ required: true, message: "请选择字段" }],
  origin: [{ required: true, message: "请选择数据源" }],
};

// 表格列
const cols = computed(() =>
  props.contentConfig.cols.map((col) => {
    if (col.initFn) {
      col.initFn(col);
    }
    if (col.show === undefined) {
      col.show = true;
    }
    if (col.prop !== undefined && col.columnKey === undefined && col["column-key"] === undefined) {
      col.columnKey = col.prop;
    }
    if (
      col.type === "selection" &&
      col.reserveSelection === undefined &&
      col["reserve-selection"] === undefined
    ) {
      // 配合表格row-key实现跨页多选
      col.reserveSelection = true;
    }
    return col;
  })
);

// 初始化字段
const initFields = () => {
  const fields: string[] = [];
  cols.value.forEach((item) => {
    if (item.prop !== undefined) {
      fields.push(item.prop);
    }
  });
  exportsFormData.fields = fields;
};

// 初始化
initFields();

// 关闭导出弹窗
function handleCloseExportsModal() {
  exportsModalVisible.value = false;
  exportsFormRef.value?.resetFields();
  nextTick(() => {
    exportsFormRef.value?.clearValidate();
  });
}

// 导出
async function handleExports() {
  try {
    const filename = exportsFormData.filename
      ? exportsFormData.filename
      : props.contentConfig.permPrefix || "export";
    const sheetname = exportsFormData.sheetname ? exportsFormData.sheetname : "sheet";
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet(sheetname);
    const columns: Partial<ExcelJS.Column>[] = [];
    cols.value.forEach((col) => {
      if (col.label && col.prop && exportsFormData.fields.includes(col.prop)) {
        columns.push({ header: col.label, key: col.prop });
      }
    });
    worksheet.columns = columns;

    if (exportsFormData.origin === ExportsOriginEnum.REMOTE) {
      const lastFormData = props.queryParams ?? {};
      if (props.contentConfig.exportsBlobAction) {
        const blob = await props.contentConfig.exportsBlobAction(lastFormData);
        saveBlobDownload(blob, filename as string);
        ElMessage.success("导出成功");
        return;
      }
      if (props.contentConfig.exportsAction) {
        const res = await props.contentConfig.exportsAction(lastFormData);
        worksheet.addRows(res);
        const buffer = await workbook.xlsx.writeBuffer();
        saveXlsx(buffer, filename as string);
      } else {
        ElMessage.error("未配置 exportsAction 或 exportsBlobAction");
      }
    } else if (exportsFormData.origin === ExportsOriginEnum.SELECTED) {
      const rows = props.selectionData ?? [];
      worksheet.addRows(rows);
      const buffer = await workbook.xlsx.writeBuffer();
      saveXlsx(buffer, filename as string);
    } else {
      const rows = props.pageData ?? [];
      worksheet.addRows(rows);
      const buffer = await workbook.xlsx.writeBuffer();
      saveXlsx(buffer, filename as string);
    }
  } catch (error) {
    console.error("导出失败:", error);
    ElMessage.error("导出失败");
  }
}

// 导出确认
const handleExportsSubmit = useThrottleFn(() => {
  exportsFormRef.value?.validate((valid: boolean) => {
    if (valid) {
      handleExports();
      handleCloseExportsModal();
    }
  });
}, 3000);

// 浏览器保存文件
function saveXlsx(fileData: any, fileName: string) {
  try {
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
  } catch (error) {
    console.error("保存文件失败:", error);
    ElMessage.error("保存文件失败");
  }
}

// 提供给父组件的方法
defineExpose({
  handleCloseExportsModal,
});
</script>
