<template>
  <div class="crud-export-modal-host">
    <!-- 导出弹窗 -->
    <EnhancedDialog
      v-model="exportsModalVisible"
      title="导出数据"
      width="600px"
      dialog-class="crud-embed-dialog"
      @close="handleCloseExportsModal"
    >
      <!-- 滚动 -->
      <el-scrollbar max-height="60vh">
        <!-- 表单 -->
        <el-form
          ref="exportsFormRef"
          style="padding-right: var(--el-dialog-padding-primary)"
          :model="exportsFormData"
          :rules="exportsFormRules"
        >
          <el-form-item label="文件名" prop="filename">
            <el-input v-model="exportsFormData.filename" placeholder="请输入文件名" clearable />
          </el-form-item>
          <el-form-item label="工作表名" prop="sheetname">
            <el-input v-model="exportsFormData.sheetname" placeholder="请输入工作表名" clearable />
          </el-form-item>
          <el-form-item label="数据源" prop="origin">
            <el-select v-model="exportsFormData.origin">
              <el-option
                label="当前数据 (当前页的数据)"
                :value="ExportsOriginEnum.CURRENT"
                :disabled="!pageData?.length"
              />
              <el-option
                label="选中数据 (所有选中的数据)"
                :value="ExportsOriginEnum.SELECTED"
                :disabled="!selectionData?.length"
              />
              <el-option
                label="全量数据 (所有分页的数据)"
                :value="ExportsOriginEnum.REMOTE"
                :disabled="!props.contentConfig.exportsAction"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="字段" prop="fields">
            <el-checkbox-group v-model="exportsFormData.fields">
              <template v-for="col in cols" :key="col.prop">
                <el-checkbox v-if="col.prop" :value="col.prop" :label="col.label" />
              </template>
            </el-checkbox-group>
          </el-form-item>
        </el-form>
      </el-scrollbar>
      <!-- 弹窗底部操作按钮 -->
      <template #footer>
        <div style="padding-right: var(--el-dialog-padding-primary)">
          <el-button type="primary" @click="handleExportsSubmit">确 定</el-button>
          <el-button @click="handleCloseExportsModal">取 消</el-button>
        </div>
      </template>
    </EnhancedDialog>
  </div>
</template>

<script lang="ts" setup>
import EnhancedDialog from "@/components/Core/overlays/EnhancedDialog.vue";
import ExcelJS from "exceljs";
import type { IContentConfig, IObject } from "./types";
import { useThrottleFn } from "@vueuse/core";
import { type FormInstance, type FormRules, ElMessage } from "element-plus";
import { nextTick, ref, reactive, computed } from "vue";

/**
 * 导出模态框组件属性定义
 */
interface CrudExportModalProps {
  /** 内容配置 */
  contentConfig: Pick<IContentConfig, "permPrefix" | "cols" | "exportsAction">;
  /** 查询参数 */
  queryParams?: IObject;
  /** 页面数据 */
  pageData?: IObject[];
  /** 选中数据 */
  selectionData?: IObject[];
}

// 定义接收的属性
const props = defineProps<CrudExportModalProps>();

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
function handleExports() {
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
      if (props.contentConfig.exportsAction) {
        const lastFormData = props.queryParams ?? {};
        props.contentConfig
          .exportsAction(lastFormData)
          .then((res) => {
            worksheet.addRows(res);
            workbook.xlsx
              .writeBuffer()
              .then((buffer) => {
                saveXlsx(buffer, filename as string);
              })
              .catch((error) => {
                console.error("导出远程数据失败:", error);
                ElMessage.error("导出远程数据失败");
              });
          })
          .catch((error) => {
            console.error("获取远程数据失败:", error);
            ElMessage.error("获取远程数据失败");
          });
      } else {
        ElMessage.error("未配置exportsAction");
      }
    } else if (exportsFormData.origin === ExportsOriginEnum.SELECTED) {
      const rows = props.selectionData ?? [];
      worksheet.addRows(rows);
      workbook.xlsx
        .writeBuffer()
        .then((buffer) => {
          saveXlsx(buffer, filename as string);
        })
        .catch((error) => {
          console.error("导出选中数据失败:", error);
          ElMessage.error("导出选中数据失败");
        });
    } else {
      const rows = props.pageData ?? [];
      worksheet.addRows(rows);
      workbook.xlsx
        .writeBuffer()
        .then((buffer) => {
          saveXlsx(buffer, filename as string);
        })
        .catch((error) => {
          console.error("导出当前数据失败:", error);
          ElMessage.error("导出当前数据失败");
        });
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
