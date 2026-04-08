<template>
  <div class="app-container">
    <PageSearch
      ref="searchRef"
      :search-config="searchConfig"
      @query-click="handleQueryClick"
      @reset-click="handleResetClick"
    />

    <PageContent ref="contentRef" :content-config="contentConfig">
      <template #toolbar="{ toolbarRight, onToolbar, removeIds, cols }">
        <CrudToolbarLeft :remove-ids="removeIds">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_generator:gencode:create']"
                type="primary"
                icon="Plus"
                @click="createTableVisible = true"
              >
                创建
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_generator:gencode:import']"
                type="success"
                icon="Upload"
                @click="handleImportClick"
              >
                导入
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_generator:gencode:delete']"
                type="danger"
                icon="Delete"
                :disabled="removeIds.length === 0"
                @click="handleDelete()"
              >
                批量删除
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_generator:gencode:operate']"
                type="warning"
                icon="Download"
                :disabled="removeIds.length === 0"
                @click="handleGenTable('0')"
              >
                批量生成
              </el-button>
            </el-col>
          </el-row>
        </CrudToolbarLeft>
        <div class="data-table__toolbar--right">
          <CrudToolbarRight :buttons="toolbarRight" :cols="cols" :on-toolbar="onToolbar" />
        </div>
      </template>

      <template #table="{ data, loading: tableLoading, tableRef, onSelectionChange, pagination }">
        <div class="data-table__content">
          <el-table
            :ref="tableRef as any"
            v-loading="tableLoading"
            row-key="id"
            :data="data"
            height="100%"
            border
            stripe
            @selection-change="
              (s) => {
                handleTableSelectionChange(s as GenTableSchema[]);
                onSelectionChange(s);
              }
            "
          >
            <template #empty>
              <el-empty :image-size="80" description="暂无数据" />
            </template>
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'selection')?.show"
              type="selection"
              align="center"
              width="55"
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'index')?.show"
              label="序号"
              type="index"
              min-width="30"
              align="center"
              fixed
            >
              <template #default="scope">
                <span>
                  {{ (pagination.currentPage - 1) * pagination.pageSize + scope.$index + 1 }}
                </span>
              </template>
            </el-table-column>
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'table_name')?.show"
              label="表名称"
              prop="table_name"
              :show-overflow-tooltip="true"
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'table_comment')?.show"
              label="表描述"
              prop="table_comment"
              :show-overflow-tooltip="true"
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'class_name')?.show"
              label="实体"
              prop="class_name"
              :show-overflow-tooltip="true"
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'created_time')?.show"
              label="创建时间"
              prop="created_time"
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'updated_time')?.show"
              label="更新时间"
              prop="updated_time"
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'operation')?.show"
              label="操作"
              align="center"
              min-width="120"
              class-name="small-padding fixed-width"
            >
              <template #default="scope">
                <el-button
                  v-hasPerm="['module_generator:gencode:update']"
                  link
                  type="primary"
                  :icon="MagicStick"
                  @click="handlePreviewTable(scope.row)"
                >
                  代码生成
                </el-button>
                <el-button
                  v-hasPerm="['module_generator:gencode:delete']"
                  link
                  type="danger"
                  icon="Delete"
                  @click="handleDelete(scope.row)"
                >
                  删除
                </el-button>
                <el-button
                  v-hasPerm="['module_generator:db:sync']"
                  link
                  type="success"
                  icon="Refresh"
                  @click="handleSynchDb(scope.row)"
                >
                  同步
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </template>
    </PageContent>

    <CreateTableDialog
      v-model="createTableVisible"
      :loading="loading"
      :link-from-gen="createTableLinkFromGen"
      @submit="handleCreateTableSubmit"
    />

    <ImportDbTableDialog
      ref="importDbDialogRef"
      v-model="importVisible"
      v-model:query="importQueryFormData"
      :data="dbTableList"
      :total="importTotal"
      :confirm-loading="importLoading"
      @query="handleImportQuery"
      @reset="handleImportReset"
      @confirm="handleImportTable"
      @fetch="getDbList"
      @selection-change="handleImportTableSelectionChange"
    />

    <GenCodeDrawer
      v-model="editVisible"
      v-model:preview-scope="previewScope"
      v-model:preview-types="previewTypes"
      v-model:code="code"
      :info="info"
      :rules="rules"
      :active-step="activeStep"
      :menu-options="menuOptions"
      :dict-options="dictOptions"
      :loading="loading"
      :next-step-loading="nextStepLoading"
      :preview-loading="previewLoading"
      :preview-type-options="previewTypeOptions"
      :filtered-tree-data="filteredTreeData"
      :cm-options="cmOptions"
      :bulk-set="bulkSet"
      @close="handleClose"
      @prev-step="prevStep"
      @next-step="nextStep"
      @gen-download="handleGenTable('0', info)"
      @gen-write="handleGenTable('1', info)"
      @clear-master-sub="clearMasterSub"
      @master-sub-blur="onMasterSubFieldBlur"
      @file-click="handleFileTreeNodeClick"
      @copy-code="handleCopyCode"
    />
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "GenCode",
  inheritAttrs: false,
});

import { ref, reactive, computed, onActivated, watch, nextTick, unref, provide } from "vue";
import { useClipboard } from "@vueuse/core";
import { useRoute } from "vue-router";
import type { EditorConfiguration } from "codemirror";
import type { CmComponentRef } from "codemirror-editor-vue3";
import { ElMessage, ElMessageBox, type FormInstance } from "element-plus";
import { MagicStick } from "@element-plus/icons-vue";
import GencodeAPI, {
  type GenTableSchema,
  type DBTableSchema,
  type GenTablePageQuery,
} from "@/api/module_generator/gencode";
import MenuAPI, { MenuTable } from "@/api/module_system/menu";
import DictAPI, { DictTable } from "@/api/module_system/dict";
import { MenuTypeEnum } from "@/enums";
import { useSettingsStore } from "@/store";
import { ThemeMode } from "@/enums/settings/theme.enum";
import CrudToolbarLeft from "@/components/CURD/CrudToolbarLeft.vue";
import CrudToolbarRight from "@/components/CURD/CrudToolbarRight.vue";
import PageSearch from "@/components/CURD/PageSearch.vue";
import PageContent from "@/components/CURD/PageContent.vue";
import CreateTableDialog, { type CreateTableSubmitMeta } from "./components/CreateTableDialog.vue";
import GenCodeDrawer from "./components/GenCodeDrawer.vue";
import ImportDbTableDialog from "./components/ImportDbTableDialog.vue";
import { GENCODE_BASIC_FORM_KEY, GENCODE_CM_KEY } from "./gencodeInjectionKeys";
import type { TreeNode } from "./types";
import { useCrudList } from "@/components/CURD/useCrudList";
import type { IContentConfig, ISearchConfig } from "@/components/CURD/types";

// 表格列配置接口
interface TableColumn {
  prop: string;
  label: string;
  show: boolean;
  minWidth?: string;
  formatter?: (row: any, column: any) => any;
}

// 文件数据接口
interface FileData {
  path: string;
  file_name: string;
  content: string;
  full_path: string;
}

const { searchRef, contentRef, handleQueryClick, handleResetClick, refreshList } = useCrudList();

// 组件引用（与子组件 inject 同步，供校验 / CodeMirror 主题）
const cmRef = ref<CmComponentRef>();
const basicInfo = ref<FormInstance>();
const importDbDialogRef = ref<InstanceType<typeof ImportDbTableDialog>>();

provide(GENCODE_BASIC_FORM_KEY, basicInfo);
provide(GENCODE_CM_KEY, cmRef);

// 状态管理
const loading = ref(false);
const nextStepLoading = ref(false);
const uniqueId = ref("");
const editVisible = ref(false);
const activeStep = ref(0);

// UI状态
const createTableVisible = ref(false);
const importVisible = ref(false);

// 表单和列表数据
const dbTableList = ref<DBTableSchema[]>([]);
const ids = ref<number[]>([]);
const tableNames = ref<string[]>([]);

// 导入弹窗专用状态
const importLoading = ref(false);
const importTotal = ref<number>(0);
const importQueryFormData = ref<GenTablePageQuery>({
  page_no: 1,
  page_size: 10,
  table_name: undefined,
  table_comment: undefined,
});

// 下拉选项数据
const dictOptions = ref<DictTable[]>([]);
const menuOptions = ref<OptionType[]>([]);

// 表格数据
type TableItem = {
  table_name: string;
  table_comment: string;
};
const tables = ref<TableItem[]>([]);

// 导入按钮点击事件
async function handleImportClick() {
  importVisible.value = true;
  await getDbList();
}

// 预览相关数据
const preview = reactive({
  open: false,
  title: "代码预览",
  data: {},
  active_name: "controller.py",
});

/** 预览接口加载中（第三步） */
const previewLoading = ref(false);

const previewScope = ref<"all" | "frontend" | "backend">("all");
const previewTypeOptions = ["ts", "vue", "python"];
const previewTypes = ref<string[]>([...previewTypeOptions]);
const code = ref<string>("");
const treeData = ref<TreeNode[]>([]);

const searchConfig = reactive<ISearchConfig>({
  permPrefix: "module_generator:gencode",
  colon: true,
  isExpandable: false,
  showNumber: 3,
  form: { labelWidth: "auto" },
  searchButtonPerm: "module_generator:gencode:query",
  resetButtonPerm: "module_generator:gencode:query",
  formItems: [
    {
      prop: "table_name",
      label: "表名称",
      type: "input",
      attrs: { placeholder: "请输入表名称", clearable: true, style: { width: "200px" } },
    },
    {
      prop: "table_comment",
      label: "表描述",
      type: "input",
      attrs: { placeholder: "请输入表描述", clearable: true, style: { width: "200px" } },
    },
  ],
});

const contentCols = reactive<TableColumn[]>([
  { prop: "selection", label: "选择框", show: true },
  { prop: "index", label: "序号", show: true },
  { prop: "table_name", label: "表名称", show: true },
  { prop: "table_comment", label: "表描述", show: true },
  { prop: "class_name", label: "实体", show: true },
  { prop: "created_time", label: "创建时间", show: true },
  { prop: "updated_time", label: "更新时间", show: true },
  { prop: "operation", label: "操作", show: true },
]);

const contentConfig = reactive<IContentConfig<GenTablePageQuery>>({
  permPrefix: "module_generator:gencode",
  cols: contentCols as IContentConfig["cols"],
  hideColumnFilter: false,
  toolbar: [],
  defaultToolbar: ["refresh", "filter"],
  pagination: {
    pageSize: 10,
    pageSizes: [10, 20, 30, 50],
  },
  request: { page_no: "page_no", page_size: "page_size" },
  indexAction: async (params) => {
    const res = await GencodeAPI.listTable(params as GenTablePageQuery);
    return {
      total: res.data.data.total,
      list: res.data.data.items,
    };
  },
});

const settingsStore = useSettingsStore();

// 主题计算属性
const codeTheme = computed(() => (settingsStore.theme === ThemeMode.DARK ? "dracula" : "default"));

// 监听主题变化并更新CodeMirror实例
watch(codeTheme, (newTheme) => {
  if (cmRef.value && cmRef.value.cminstance) {
    cmRef.value.cminstance.setOption("theme", newTheme);
  }
});

// CodeMirror配置
const cmOptions: EditorConfiguration = {
  mode: "text/javascript",
  lineNumbers: true,
  smartIndent: true,
  indentUnit: 2,
  tabSize: 2,
  readOnly: false,
  theme: codeTheme.value,
  lineWrapping: true,
  autofocus: false,
};

// 工具函数
const { copy } = useClipboard();

// ===== 计算属性 =====

// 过滤后的文件树数据
const filteredTreeData = computed<TreeNode[]>(() => {
  if (!treeData.value.length) return [];

  // 基于原树按 scope/types 过滤叶子节点
  const match = (label: string, parentPath: string[]): boolean => {
    // scope 过滤：根据路径初步判断
    if (previewScope.value !== "all") {
      // 根据后端返回的格式，检查路径或文件名特征
      const isPythonBackend =
        parentPath.some((part) => part === "backend" || part === "python") || label.includes(".py");
      const isVueFrontend =
        parentPath.some((part) => part === "frontend" || part === "vue") ||
        label.includes(".vue") ||
        label.includes(".ts");

      if (previewScope.value === "backend" && !isPythonBackend) return false;
      if (previewScope.value === "frontend" && !isVueFrontend) return false;
    }

    // 类型过滤：根据文件内容特征判断类型
    if (label.endsWith(".py")) return previewTypes.value.includes("python");
    if (label.endsWith(".vue")) return previewTypes.value.includes("vue");
    if (label.endsWith(".ts")) return previewTypes.value.includes("ts");

    return true;
  };

  const cloneFilter = (node: TreeNode, parents: string[] = []): TreeNode | null => {
    if (!node.children || node.children.length === 0) {
      return match(node.label, parents) ? { ...node } : null;
    }
    const nextParents = [...parents, node.label];
    const children = (node.children || [])
      .map((c) => cloneFilter(c, nextParents))
      .filter(Boolean) as TreeNode[];
    if (!children.length) return null;
    return { label: node.label, children };
  };

  const filtered = treeData.value.map((n) => cloneFilter(n)).filter(Boolean) as TreeNode[];
  return filtered;
});

// ===== 功能函数 =====

/** 一键复制代码 */
const handleCopyCode = () => {
  const content = code.value;

  if (content) {
    copy(content);
    ElMessage.success("代码复制成功");
  } else {
    ElMessage.warning("没有可复制的代码");
  }
};

/** 文件树节点点击事件 */
function handleFileTreeNodeClick(data: TreeNode): void {
  if (data && (!data.children || data.children.length === 0)) {
    code.value = data.content || "";
    void nextTick(() => applyPreviewEditorMode(data.label));
  }
}

/** 递归构建树形结构 */
function buildTree(data: FileData[]): TreeNode {
  // 创建根节点
  const root: TreeNode = { label: "前后端代码", children: [] };

  data.forEach((item) => {
    // 将路径分成数组（确保使用正斜杠）
    const parts = item.path.split("/").filter((part) => part !== "");

    let currentNode = root;

    // 遍历路径部分，创建对应的文件夹节点
    parts.forEach((part) => {
      // 查找或创建当前部分的子节点
      let node = currentNode.children?.find((child) => child.label === part);
      if (!node) {
        node = { label: part, children: [] };
        currentNode.children?.push(node);
      }
      currentNode = node;
    });

    // 添加文件节点（保持原有目录树展示：文件节点仅显示文件名）
    currentNode.children?.push({
      label: item.file_name,
      full_path: item.full_path,
      content: item?.content,
    });
  });

  return root;
}

/** 深度优先取第一个文件节点 */
function findFirstLeafInTree(nodes: TreeNode[]): TreeNode | null {
  for (const node of nodes) {
    if (!node.children || node.children.length === 0) {
      return node;
    }
    const leaf = findFirstLeafInTree(node.children);
    if (leaf) return leaf;
  }
  return null;
}

/** 按文件名切换预览区语法高亮 */
function applyPreviewEditorMode(fileLabel: string) {
  const inst = cmRef.value?.cminstance;
  if (!inst) return;
  let mode = "text/javascript";
  if (fileLabel.endsWith(".py")) mode = "text/x-python";
  else if (fileLabel.endsWith(".vue")) mode = "text/html";
  else if (fileLabel.endsWith(".ts")) mode = "text/typescript";
  inst.setOption("mode", mode);
}

/** 获取生成预览 */
async function handlePreview(row: GenTableSchema): Promise<void> {
  if (!row.id) {
    ElMessage.warning("无效的表ID");
    return;
  }

  previewLoading.value = true;
  try {
    const response = await GencodeAPI.previewTable(row.id!);
    const raw = response.data?.data;
    if (!raw || typeof raw !== "object" || Object.keys(raw).length === 0) {
      ElMessage.warning("预览内容为空，请先保存配置并检查字段与主子表设置");
      treeData.value = [];
      code.value = "";
      preview.data = {};
      return;
    }

    preview.data = raw;

    const filesData = Object.entries(raw).map(([key, content]) => {
      const pathParts = key.split("/");
      let fileName = pathParts.pop() || "";
      const path = pathParts.join("/");

      if (fileName.endsWith(".j2")) {
        fileName = fileName.substring(0, fileName.lastIndexOf(".j2"));
      }

      const contentStr = typeof content === "string" ? content : JSON.stringify(content);

      return {
        path,
        file_name: fileName,
        content: contentStr,
        full_path: key,
      } as FileData;
    });

    const treeRoot = buildTree(filesData);
    // 预览树仅展示生成文件树（不额外展示“上级目录：xxx”）
    treeData.value = [treeRoot];

    await nextTick();
    let firstLeaf: TreeNode | null = null;
    for (const r of filteredTreeData.value) {
      firstLeaf = findFirstLeafInTree([r]);
      if (firstLeaf) break;
    }
    if (!firstLeaf) {
      firstLeaf = findFirstLeafInTree(treeData.value);
    }

    code.value = firstLeaf?.content || "";
    await nextTick();
    if (firstLeaf?.label) {
      applyPreviewEditorMode(firstLeaf.label);
    }

    preview.open = true;
    preview.active_name = "model.py";
  } catch (error) {
    console.error("预览代码失败:", error);
  } finally {
    previewLoading.value = false;
  }
}

/** 表格行内生成代码操作 */
async function handleGenTable(targetGenType: string, row?: GenTableSchema): Promise<void> {
  let tbNames: string | string[] = [];

  // 判断是单条还是批量操作
  if (row) {
    tbNames = [row.table_name || ""];
  } else if (tableNames.value.length > 0) {
    tbNames = tableNames.value;
  } else {
    ElMessage.error("请选择要生成的数据");
    return;
  }

  loading.value = true;
  try {
    if (targetGenType === "1") {
      if (!Array.isArray(tbNames) || tbNames.length !== 1 || !tbNames[0]) {
        ElMessage.error("自定义路径只能生成单表代码");
        loading.value = false;
        return;
      }
      if (row?.id) await confirmWritePaths(row.id);
      await GencodeAPI.genCodeToPath(tbNames[0]);
      ElMessage.success("已写入项目目录并创建菜单（若尚未存在）");
    } else {
      // ZIP压缩包下载
      const tableNamesArray = Array.isArray(tbNames) ? tbNames : [tbNames];
      const response = await GencodeAPI.batchGenCode(tableNamesArray);
      const raw = response.data as Blob;
      if (raw.size < 100 && raw.type.includes("json")) {
        const text = await raw.text();
        try {
          const json = JSON.parse(text) as { msg?: string };
          ElMessage.error(json.msg || "批量生成失败");
          return;
        } catch {
          /* 非 JSON 小文件仍尝试下载 */
        }
      }
      const blob = new Blob([raw], { type: "application/zip" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "code.zip";
      link.click();
      URL.revokeObjectURL(url);
      ElMessage.success("已开始下载 code.zip");
    }
  } catch (error) {
    console.error("生成代码失败:", error);
  } finally {
    loading.value = false;
  }
}

function escapeHtml(s: string) {
  return s
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

async function confirmWritePaths(tableId: number) {
  // 先保存当前抽屉配置，否则 preview 仍基于旧配置，回显会不准确
  await GencodeAPI.updateTable(info as GenTableSchema, tableId);
  const previewRes = await GencodeAPI.previewTable(tableId);
  const raw = previewRes.data?.data as Record<string, unknown> | undefined;
  const keys = raw && typeof raw === "object" ? Object.keys(raw) : [];
  const shown = keys.slice(0, 80);
  const more =
    keys.length > shown.length
      ? `<div style="margin-top:10px;padding:8px 12px;border-radius:6px;background:var(--el-fill-color-light);font-size:12px;color:var(--el-text-color-secondary);text-align:center">还有 <b style="color:var(--el-text-color-primary)">${keys.length - shown.length}</b> 个文件未列出</div>`
      : "";
  const listRows = shown
    .map((p, i) => {
      const bg = i % 2 === 0 ? "var(--el-fill-color-blank)" : "var(--el-fill-color-light)";
      return `<div class="gencode-write-path-row" style="padding:9px 14px;font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-size:12px;line-height:1.45;white-space:nowrap;color:var(--el-text-color-primary);background:${bg};border-bottom:1px solid var(--el-border-color-lighter)">${escapeHtml(p)}</div>`;
    })
    .join("");
  const listHtml = shown.length
    ? `<div class="gencode-write-path-list-wrap">${listRows}</div>${more}`
    : `<div style="padding:16px;border-radius:8px;background:var(--el-fill-color-light);color:var(--el-text-color-secondary);font-size:13px;text-align:center">未获取到预览路径，仍将继续写入。</div>`;
  const tipHtml = `<div style="margin-top:12px;padding-top:10px;border-top:1px solid var(--el-border-color-lighter);font-size:12px;line-height:1.5;color:var(--el-text-color-secondary)">与「代码预览」同源；路径为相对项目根的落盘位置。</div>`;
  await ElMessageBox.confirm(
    `<div class="gencode-write-confirm-body" style="font-family:var(--el-font-family);line-height:1.5;color:var(--el-text-color-primary)">
      <div style="margin-bottom:12px">
        <div style="font-size:15px;font-weight:600;letter-spacing:0.02em">将写入以下文件</div>
        <div style="margin-top:4px;font-size:12px;color:var(--el-text-color-secondary)">共 ${keys.length} 项 · 相对项目根目录</div>
      </div>
      ${listHtml}
      ${shown.length ? tipHtml : ""}
    </div>`,
    "写入本地确认",
    {
      confirmButtonText: "确认写入",
      cancelButtonText: "取消",
      type: "warning",
      dangerouslyUseHTMLString: true,
      customClass: "gencode-write-confirm-box",
    }
  );
}

/** 同步数据库操作 */
async function handleSynchDb(row: GenTableSchema): Promise<void> {
  const tableName = row.table_name || "";

  if (!tableName) {
    ElMessage.error("表名不能为空");
    return;
  }

  const renderSummary = (p: any) => {
    const added = p.added?.length ?? 0;
    const removed = p.removed?.length ?? 0;
    const changed = p.changed?.length ?? 0;
    const unchanged = p.unchanged ?? 0;
    return { added, removed, changed, unchanged };
  };

  const renderHtml = (title: string, p: any) => {
    const s = renderSummary(p);
    const list = (xs: string[]) => (xs?.length ? xs.slice(0, 20).join(", ") : "无");
    return `
      <div style="line-height:1.6">
        <div style="font-weight:600;margin-bottom:6px">${title}</div>
        <div>新增：<b>${s.added}</b>；删除：<b>${s.removed}</b>；变更：<b>${s.changed}</b>；未变：${s.unchanged}</div>
        <div style="margin-top:6px">新增列：${list(p.added || [])}</div>
        <div>删除列：${list(p.removed || [])}</div>
        <div>变更列：${list((p.changed || []).map((c: any) => c.column_name))}</div>
        <div style="margin-top:8px;color:var(--el-text-color-secondary)">提示：同步会尽量保留你已配置的 dict/html/query 等生成项，仅以数据库结构为准更新元信息。</div>
      </div>
    `;
  };

  try {
    loading.value = true;
    const previewRes = await GencodeAPI.syncDbPreview(tableName);
    const preview = previewRes.data?.data as any;
    const mainHtml = renderHtml(`主表：${tableName}`, preview);
    const subHtml =
      preview?.sub_table_name && preview?.sub
        ? renderHtml(`子表：${preview.sub_table_name}`, preview.sub)
        : "";

    await ElMessageBox.confirm(`${mainHtml}${subHtml}`, "同步差异预览", {
      confirmButtonText: "确认同步",
      cancelButtonText: "取消",
      type: "warning",
      dangerouslyUseHTMLString: true,
    });

    await GencodeAPI.syncDb(tableName);
    ElMessage.success("表结构已同步到代码生成配置");
    refreshList();
  } catch (error) {
    if (error !== "cancel") console.error("同步表结构失败:", error);
  } finally {
    loading.value = false;
  }
}

/** 多选框选中数据 - 主表格 */
function handleTableSelectionChange(selection: GenTableSchema[]): void {
  ids.value = selection.map((item) => item.id!);
  tableNames.value = selection.map((item) => item.table_name || "").filter(Boolean);
}

type ImportTableSelectionRow = { table_name: string; table_comment: string };

/** 多选框选中数据 - 导入表格 */
function handleImportTableSelectionChange(rows: ImportTableSelectionRow[]): void {
  tables.value = rows;
}

/** 代码生成「上级菜单」仅展示目录节点，便于挂到目录下生成新菜单（不选菜单/按钮作为父级） */
const filterMenuTypes = (nodes: MenuTable[]) => {
  return nodes
    .filter((node) => node.type === MenuTypeEnum.CATALOG)
    .map((node: any): any => ({
      ...node,
      children: node.children ? filterMenuTypes(node.children) : [],
    }));
};

/** 代码生成专用：保留 route_path，便于实时推断分系统 module_xxx */
function formatMenuTreeWithMeta(nodes: any[]): any[] {
  return nodes.map((node) => {
    const formattedNode: any = {
      value: node.id,
      label: node.name,
      disabled: node.status === false || String(node.status) === "false",
      route_path: node.route_path,
    };
    if (node.children && node.children.length > 0) {
      formattedNode.children = formatMenuTreeWithMeta(node.children);
    }
    return formattedNode;
  });
}

/** 表格行内「代码生成」：先打开抽屉再拉数据，避免接口慢时误以为点不动 */
async function handlePreviewTable(row?: GenTableSchema): Promise<void> {
  const selectedTableId = row?.id ?? ids.value[0];
  if (selectedTableId === undefined || selectedTableId === null) {
    ElMessage.error("请选择要修改的数据");
    return;
  }

  // 先用“列表行数据”把基础信息回显出来（接口慢时不至于看到空表单/旧数据闪烁）
  Object.assign(info, {
    id: row?.id ?? selectedTableId,
    table_name: row?.table_name || info.table_name || "",
    table_comment: row?.table_comment ?? info.table_comment ?? "",
    class_name: row?.class_name ?? info.class_name ?? "",
    package_name: row?.package_name ?? info.package_name ?? "",
    module_name: row?.module_name ?? info.module_name ?? "",
    business_name: row?.business_name ?? info.business_name ?? "",
    function_name: row?.function_name ?? info.function_name ?? "",
    description: row?.description ?? info.description ?? "",
    parent_menu_id: row?.parent_menu_id ?? info.parent_menu_id ?? undefined,
    sub_table_name: row?.sub_table_name ?? info.sub_table_name ?? "",
    sub_table_fk_name: row?.sub_table_fk_name ?? info.sub_table_fk_name ?? "",
  } as Partial<GenTableSchema>);
  // 字段列表以 detail 接口为准，避免上一张表的 columns 残留
  info.columns = [];
  activeStep.value = 0;
  editVisible.value = true;

  try {
    await loadTableDetail(selectedTableId);
  } catch (e) {
    console.error("获取表详情失败:", e);
    ElMessage.error("获取表详情失败，请稍后重试");
    // 保持抽屉打开，便于重试或关闭；勿因接口失败整抽屉被关掉像「点不动」
    return;
  }

  try {
    const [menu_response, dict_response] = await Promise.all([
      MenuAPI.listMenu(),
      DictAPI.listDictType({ page_no: 1, page_size: 100 }),
    ]);
    // 使用代码生成专用格式化：保留 route_path 供「分系统」实时回显
    menuOptions.value = formatMenuTreeWithMeta(filterMenuTypes(menu_response.data.data));
    dictOptions.value = dict_response.data.data.items;
  } catch (e) {
    console.error("菜单或字典加载失败:", e);
    ElMessage.warning("菜单或字典选项加载失败，部分下拉可能为空");
  }
}

/** 删除按钮操作 */
async function handleDelete(row?: GenTableSchema): Promise<void> {
  const tableIds = row?.id ? [row.id] : ids.value;

  if (tableIds.length === 0) {
    ElMessage.error("请选择要删除的数据");
    return;
  }

  try {
    await ElMessageBox.confirm(`是否确认删除选中的${tableIds.length}条数据？`, "删除确认", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });

    await GencodeAPI.deleteTable(tableIds);
    refreshList();
  } catch (error) {
    if (error !== "cancel") {
      console.error("删除表数据失败:", error);
    }
  }
}

/** 创建表（由 CreateTableDialog 提交 SQL；表结构模式成功后可回写第三步主子表配置） */
async function handleCreateTableSubmit(sql: string, meta?: CreateTableSubmitMeta): Promise<void> {
  if (!sql || sql.trim() === "") {
    ElMessage.error("请输入创建表SQL语句");
    return;
  }

  loading.value = true;
  try {
    await GencodeAPI.createTable(sql);
    createTableVisible.value = false;
    if (editVisible.value && activeStep.value === 2 && meta?.fromVisual && meta.visualSnapshot) {
      const v = meta.visualSnapshot;
      info.table_name = (v.mainTableName || "").trim();
      const mc = (v.mainComment || "").trim();
      if (mc) info.table_comment = mc;
      if (v.subEnabled) {
        info.sub_table_name = (v.subTableName || "").trim();
        info.sub_table_fk_name = (v.fkColumn || "").trim();
      } else {
        info.sub_table_name = "";
        info.sub_table_fk_name = "";
      }
      info.master_sub_hint = undefined;
      void nextTick(() => {
        basicInfo.value?.clearValidate?.(["table_name", "sub_table_name", "sub_table_fk_name"]);
      });
    }
    refreshList();
    importVisible.value = true;
    await getDbList();
  } catch (error) {
    console.error("创建表数据失败:", error);
  } finally {
    loading.value = false;
  }
}

/** 导入表操作 */
async function handleImportTable(): Promise<void> {
  if (tables.value.length === 0) {
    ElMessage.error("请选择要导入的表");
    return;
  }

  importLoading.value = true;
  try {
    // 提取表名数组
    const tableNames = tables.value.map((table) => table.table_name || "");
    await GencodeAPI.importTable(tableNames);
    importVisible.value = false;
    refreshList();
    // 导入成功后自动打开代码生成抽屉
    if (tables.value.length === 1) {
      await nextTick();
      const list = (unref(contentRef.value?.pageData) ?? []) as GenTableSchema[];
      const importedTable = list.find((t) => t.table_name === tables.value[0].table_name);
      if (importedTable) {
        await handlePreviewTable(importedTable);
      }
    } else {
      // 导入了多个表，刷新列表
      ElMessage.success(`成功导入 ${tables.value.length} 个表`);
    }
  } catch (error) {
    console.error("导入表失败:", error);
  } finally {
    importLoading.value = false;
  }
}

/** 查询数据库表数据 */
async function getDbList(): Promise<void> {
  importLoading.value = true;
  try {
    const res = await GencodeAPI.listDbTable(importQueryFormData.value);
    if (res.data && res.data.data) {
      dbTableList.value = res.data.data.items;
      importTotal.value = res.data.data.total;
    }
  } catch (error) {
    console.error("获取数据库表列表失败:", error);
  } finally {
    importLoading.value = false;
  }
}

/** 导入弹窗搜索按钮操作 */
async function handleImportQuery(): Promise<void> {
  importQueryFormData.value.page_no = 1;
  await getDbList();
}

/** 导入弹窗重置按钮操作 */
async function handleImportReset(): Promise<void> {
  importDbDialogRef.value?.resetQueryForm();
  await handleImportQuery();
}

// 路由和导航
const route = useRoute();

// ===== 生命周期和初始化 =====

/** 页面激活时执行 */
onActivated(async () => {
  const time = route.query.t;
  if (time != null && String(time) !== uniqueId.value) {
    uniqueId.value = String(time);
    const pageNo = Number(route.query.page_no || 1);
    await nextTick();
    if (contentRef.value) {
      contentRef.value.pagination.currentPage = pageNo;
      const q = searchRef.value?.getQueryParams() ?? {};
      const f = contentRef.value.getFilterParams?.() ?? {};
      contentRef.value.fetchPageData({ ...q, ...f }, false);
    }
  }
});

// 表单数据（后端返回字段可能含 null，这里做更宽松的承载，避免 TS 因类型收窄报错）
const info = reactive<
  GenTableSchema & {
    sub_table_name?: string | null;
    sub_table_fk_name?: string | null;
  }
>({
  id: undefined,
  table_name: "",
  table_comment: "",
  sub_table_name: "",
  sub_table_fk_name: "",
  class_name: "",
  package_name: "",
  module_name: "",
  business_name: "",
  function_name: "",
  description: "",
  parent_menu_id: undefined,
  pk_column: undefined,
  sub_table: undefined,
  columns: [],
  sub: false,
  master_sub_hint: undefined,
});

/** 代码生成抽屉第三步打开时，创建表弹窗从当前表单预填主/子表名（表结构模式） */
const createTableLinkFromGen = computed(() => {
  if (!editVisible.value || activeStep.value !== 2) return null;
  return {
    table_name: info.table_name,
    table_comment: info.table_comment,
    sub_table_name: info.sub_table_name ?? undefined,
    sub_table_fk_name: info.sub_table_fk_name ?? undefined,
  };
});

/** 主子表两项同填或同空，且子表名不得与主表相同 */
function validateMasterSubPair(_rule: unknown, _value: unknown, callback: (e?: Error) => void) {
  const sn = (info.sub_table_name || "").trim();
  const fk = (info.sub_table_fk_name || "").trim();
  if (Boolean(sn) !== Boolean(fk)) {
    callback(new Error("子表表名与外键列须同时填写或同时留空"));
    return;
  }
  if (sn && fk && sn === (info.table_name || "").trim()) {
    callback(new Error("子表表名不能与主表表名相同"));
    return;
  }
  callback();
}

function onMasterSubFieldBlur() {
  void nextTick(() => {
    basicInfo.value?.validateField("sub_table_name").catch(() => {});
    basicInfo.value?.validateField("sub_table_fk_name").catch(() => {});
  });
}

function clearMasterSub() {
  info.sub_table_name = "";
  info.sub_table_fk_name = "";
  info.master_sub_hint = undefined;
  info.sub = false;
  info.sub_table = undefined;
  void nextTick(() => {
    basicInfo.value?.clearValidate(["sub_table_name", "sub_table_fk_name"]);
  });
}

/** module_example 风格下业务名可空；模块名示例见 demo、gen_demo02 */
function validateBusinessName(_rule: unknown, value: unknown, callback: (e?: Error) => void) {
  const pkg = (info.package_name || "").trim();
  const mod = (info.module_name || "").trim();
  const isExampleStyle = pkg.startsWith("module_") && Boolean(mod) && !mod.startsWith("module_");
  if (isExampleStyle) {
    callback();
    return;
  }
  if (value == null || !String(value).trim()) {
    callback(new Error("业务名不能为空"));
    return;
  }
  callback();
}

// 校验规则
const rules = {
  table_name: [{ required: true, message: "表名称不能为空", trigger: "blur" }],
  class_name: [{ required: true, message: "实体名称不能为空", trigger: "blur" }],
  package_name: [{ required: true, message: "生成包路径不能为空", trigger: "blur" }],
  module_name: [{ required: true, message: "生成模块名不能为空", trigger: "blur" }],
  business_name: [{ validator: validateBusinessName, trigger: "blur" }],
  function_name: [{ required: true, message: "生成功能名不能为空", trigger: "blur" }],
  /** 与后端一致：可选；不选时写入本地会按包名自动建目录菜单 */
  sub_table_name: [{ validator: validateMasterSubPair, trigger: "blur" }],
  sub_table_fk_name: [{ validator: validateMasterSubPair, trigger: "blur" }],
};

// ===== 工具函数
/** 提交表单 - 保存配置（从基础配置进入字段配置时允许尚无列，便于先保存主表信息） */
async function submitForm(options?: { requireColumns?: boolean }) {
  const requireColumns = options?.requireColumns !== false;

  // 检查是否有表ID
  if (!info.id) {
    ElMessage.error("无效的表ID");
    return;
  }

  try {
    loading.value = true;

    if (requireColumns && (!info.columns || info.columns.length === 0)) {
      ElMessage.error("请配置字段信息");
      return;
    }

    // 提交表单数据，确保columns是必需的，并且parent_menu_id总是被包含
    const tableData = {
      ...info,
      parent_menu_id: info.parent_menu_id ?? null, // 将undefined转换为null，确保属性被传输
      columns: info.columns || [], // 确保columns存在
    };
    delete (tableData as Record<string, unknown>).sub_table;
    delete (tableData as Record<string, unknown>).sub;
    delete (tableData as Record<string, unknown>).pk_column;
    delete (tableData as Record<string, unknown>).master_sub_hint;

    const savedColumns = info.columns;
    const res = await GencodeAPI.updateTable(tableData as GenTableSchema, info.id || 0);
    if (res.data?.data) {
      Object.assign(info, res.data.data as GenTableSchema);
      if (savedColumns && savedColumns.length > 0) {
        info.columns = savedColumns;
      }
    }
    return true;
  } catch (error) {
    console.error("保存表单失败:", error);
  } finally {
    loading.value = false;
  }
}

// 下一步
async function nextStep(): Promise<void> {
  if (activeStep.value < 3) {
    nextStepLoading.value = true;
    try {
      // 在进入下一步前先保存当前配置
      if (activeStep.value === 0) {
        // 第一步：基础配置
        const basicInfoValid = await basicInfo.value?.validate().catch(() => false);
        if (!basicInfoValid) return;
      } else if (activeStep.value === 1) {
        // 第二步：字段配置
        if (!info.columns || info.columns.length === 0) {
          ElMessage.error("请配置字段信息");
          return;
        }
      }

      // 保存配置：从第 1 步离开时要求已配置列；从第 0 步进入字段配置时允许仅保存基础信息
      const saved = await submitForm({ requireColumns: activeStep.value !== 0 });
      if (!saved) return;

      activeStep.value++;

      // 当从字段配置进入预览步骤时，自动加载预览数据
      if (activeStep.value === 2 && info.id) {
        await handlePreview({ id: info.id, table_name: info.table_name } as GenTableSchema);
      }
    } finally {
      nextStepLoading.value = false;
    }
  }
}

// 上一步
function prevStep(): void {
  if (activeStep.value > 0) {
    activeStep.value--;
  }
}

// 批量设置字段属性
function bulkSet(field: string | string[], value: any): void {
  if (!info.columns || !Array.isArray(info.columns)) return;

  const fieldsToUpdate = Array.isArray(field) ? field : [field];

  info.columns.forEach((column) => {
    if (column && typeof column === "object") {
      fieldsToUpdate.forEach((f) => {
        (column as any)[f] = value;
      });
    }
  });
}

function close(): void {
  editVisible.value = false;
  activeStep.value = 0; // 重置步骤

  // 清除表单验证状态
  setTimeout(() => {
    basicInfo.value?.resetFields();
  }, 300);
}

/** 处理抽屉关闭事件 */
function handleClose(): void {
  close();
}

/** 加载表详情 */
async function loadTableDetail(id: number | string) {
  try {
    loading.value = true;
    const response = await GencodeAPI.detailTable(Number(id));

    if (response?.data?.data) {
      const data = response.data.data;

      // 填充表单数据
      Object.assign(info, { ...data });

      // 处理列数据
      if (data && data.columns && Array.isArray(data.columns)) {
        // 深拷贝确保数据独立性
        info.columns = JSON.parse(JSON.stringify(data.columns));
        // 设置列的选中状态
        (info.columns ?? []).forEach((item: any) => {
          item.select = true;
        });
      }

      // 重置当前步骤为第一步
      activeStep.value = 0;
    }
  } catch (error) {
    console.error("获取表详情失败:", error);
    throw error;
  } finally {
    loading.value = false;
  }
}
</script>
