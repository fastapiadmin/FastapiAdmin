<template>
  <FaDialog
    v-model="visible"
    title="创建数据表"
    width="min(800px, 94vw)"
    append-to-body
    dialog-class="create-table-dialog"
    @opened="onDialogOpened"
  >
    <ElAlert type="info" :closable="false" show-icon class="mb-3 !items-start">
      <template #title>
        <span class="text-sm leading-relaxed">
          <template v-if="editMode === 'visual'">
            选好数据库与单表/主子表，填好表名后点右下角「创建表」即可。
          </template>
          <template v-else>自带示例一键插入；会写 DDL 的可直接粘贴，支持多条语句。</template>
        </span>
      </template>
    </ElAlert>

    <div class="create-table-toolbar mb-3 flex flex-wrap items-center gap-2">
      <span class="text-sm text-[var(--el-text-color-regular)] shrink-0">方式</span>
      <ElRadioGroup v-model="editMode" size="small">
        <ElRadioButton value="visual">表结构（推荐）</ElRadioButton>
        <ElRadioButton value="sql">写 SQL</ElRadioButton>
      </ElRadioGroup>
    </div>

    <div v-show="editMode === 'sql'" class="sql-pane">
      <div class="mb-2 flex flex-wrap items-center gap-2">
        <ElDropdown trigger="click" @command="onSqlPresetCommand">
          <ElButton type="primary" size="small">
            插入示例模板
            <ElIcon class="el-icon--right"><ArrowDown /></ElIcon>
          </ElButton>
          <template #dropdown>
            <ElDropdownMenu>
              <ElDropdownItem command="single-mysql">单表 · MySQL</ElDropdownItem>
              <ElDropdownItem command="single-postgres">单表 · PostgreSQL</ElDropdownItem>
              <ElDropdownItem command="master-mysql" divided>主子表 · MySQL</ElDropdownItem>
              <ElDropdownItem command="master-postgres">主子表 · PostgreSQL</ElDropdownItem>
            </ElDropdownMenu>
          </template>
        </ElDropdown>
        <span class="text-xs text-[var(--el-text-color-secondary)]">从模板开始比自己写更省事</span>
      </div>
      <ElScrollbar max-height="min(52vh, 420px)" class="sql-editor-scroll">
        <div class="absolute z-36 right-5 top-2">
          <ElLink type="primary" @click="copySql">
            <ElIcon><CopyDocument /></ElIcon>
            复制
          </ElLink>
        </div>
        <Codemirror
          ref="sqlRef"
          v-model:value="sqlText"
          :options="sqlOptions"
          border
          height="360px"
          width="100%"
        />
      </ElScrollbar>
    </div>

    <div v-show="editMode === 'visual'" class="visual-pane">
      <ElScrollbar max-height="min(58vh, 520px)" class="visual-pane-scroll">
        <div class="visual-structure max-w-3xl">
          <ElDescriptions :column="1" border size="small" class="visual-desc">
            <template #title>
              <span class="text-sm font-medium text-[var(--el-text-color-primary)]">选项</span>
            </template>
            <ElDescriptionsItem label="数据库" label-class-name="visual-desc-label">
              <ElRadioGroup v-model="visual.dialect" size="small">
                <ElRadioButton value="mysql">MySQL</ElRadioButton>
                <ElRadioButton value="postgres">PostgreSQL</ElRadioButton>
              </ElRadioGroup>
            </ElDescriptionsItem>
            <ElDescriptionsItem label="表类型" label-class-name="visual-desc-label">
              <ElRadioGroup v-model="templateKind" size="small">
                <ElRadioButton value="single">只要一张表</ElRadioButton>
                <ElRadioButton value="masterSub">主表 + 子表明细</ElRadioButton>
              </ElRadioGroup>
            </ElDescriptionsItem>
          </ElDescriptions>

          <ElDescriptions :column="1" border size="small" class="visual-desc mt-3">
            <template #title>
              <span class="text-sm font-medium text-[var(--el-text-color-primary)]">主表</span>
            </template>
            <ElDescriptionsItem label-class-name="visual-desc-label">
              <template #label>
                <span class="text-[var(--el-color-danger)]">*</span>
                表名
              </template>
              <ElInput
                v-model="visual.mainTableName"
                placeholder="英文表名，如 gen_demo_order"
                clearable
              />
            </ElDescriptionsItem>
            <ElDescriptionsItem label="说明" label-class-name="visual-desc-label">
              <ElInput v-model="visual.mainComment" placeholder="中文说明，可选" clearable />
            </ElDescriptionsItem>
          </ElDescriptions>

          <ElDescriptions
            v-if="visual.subEnabled"
            :column="1"
            border
            size="small"
            class="visual-desc mt-3"
          >
            <template #title>
              <span class="text-sm font-medium text-[var(--el-text-color-primary)]">子表</span>
            </template>
            <ElDescriptionsItem label-class-name="visual-desc-label">
              <template #label>
                <span class="text-[var(--el-color-danger)]">*</span>
                表名
              </template>
              <ElInput
                v-model="visual.subTableName"
                placeholder="如 gen_demo_order_item"
                clearable
              />
            </ElDescriptionsItem>
            <ElDescriptionsItem label="说明" label-class-name="visual-desc-label">
              <ElInput v-model="visual.subComment" placeholder="中文说明，可选" clearable />
            </ElDescriptionsItem>
            <ElDescriptionsItem label="外键列" label-class-name="visual-desc-label">
              <ElInput
                v-model="visual.fkColumn"
                placeholder="子表里指向主表的那列，如 order_id"
                clearable
              />
            </ElDescriptionsItem>
            <ElDescriptionsItem label="对应主表列" label-class-name="visual-desc-label">
              <ElInput v-model="visual.fkRefColumn" placeholder="一般是 id" clearable />
            </ElDescriptionsItem>
          </ElDescriptions>

          <div class="mt-3">
            <ElLink type="primary" :underline="false" @click="syncVisualToSql">
              需要手写调整？生成 SQL 并切到「写 SQL」
            </ElLink>
          </div>
        </div>
        <p class="mb-1 mt-2 text-xs text-[var(--el-text-color-secondary)]">
          将要执行的 SQL（随上面表格自动更新）
        </p>
        <ElInput
          v-model="visualPreviewSql"
          type="textarea"
          :rows="6"
          readonly
          class="font-mono text-xs visual-sql-preview"
          placeholder="填写表名后会自动生成"
        />
      </ElScrollbar>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <ElButton type="primary" :loading="loading" @click="handleConfirm">创建表</ElButton>
        <ElButton @click="handleCancel">取消</ElButton>
      </div>
    </template>
  </FaDialog>
</template>

<script setup lang="ts">
import "codemirror/mode/sql/sql.js";
import "codemirror/theme/dracula.css";
import { ref, watch, nextTick, computed } from "vue";
import Codemirror from "codemirror-editor-vue3";
import type { EditorConfiguration } from "codemirror";
import type { CmComponentRef } from "codemirror-editor-vue3";
import { ElMessage } from "element-plus";
import { ArrowDown, CopyDocument } from "@element-plus/icons-vue";
import { useClipboard } from "@vueuse/core";
import FaDialog from "@/components/modal/fa-dialog/index.vue";
import { useSettingsStore } from "@stores";
import { ThemeMode } from "@/enums/settings/theme.enum";
import { buildSqlFromVisual } from "../utils/buildCreateTableSql";
import type { SqlDialect, VisualBuildState } from "../utils/buildCreateTableSql";
import {
  applySubColumns,
  mergeGenTableLinkIntoVisual,
  visualPresetMasterSub,
  visualPresetSingle,
  type GenTableCreateLink,
} from "../utils/createTableVisualPresets";
import {
  getExampleFromPresetMasterSub,
  getExampleFromPresetSingle,
} from "../utils/createTableSqlExamples";

defineOptions({ name: "CreateTableDialog" });

const visible = defineModel<boolean>({ default: false });

export interface CreateTableSubmitMeta {
  fromVisual: boolean;
  visualSnapshot?: VisualBuildState;
}

const props = withDefaults(
  defineProps<{
    loading?: boolean;
    /** 代码生成抽屉第三步打开时传入，用于预填「表结构」主/子表名 */
    linkFromGen?: GenTableCreateLink | null;
  }>(),
  { loading: false, linkFromGen: null }
);

const emit = defineEmits<{
  submit: [sql: string, meta?: CreateTableSubmitMeta];
}>();

const { copy } = useClipboard();
const settingsStore = useSettingsStore();

const editMode = ref<"sql" | "visual">("visual");
const sqlText = ref("");
const sqlRef = ref<CmComponentRef>();
const visual = ref<VisualBuildState>(visualPresetSingle("mysql"));
const visualPreviewSql = ref("");

/** 单表 / 主子表：与「模板按钮」等价，用语义化文案降低理解成本 */
const templateKind = computed({
  get: (): "single" | "masterSub" => (visual.value.subEnabled ? "masterSub" : "single"),
  set: (v: string) => {
    if (v === "single" || v === "masterSub") applyVisualPreset(v);
  },
});

const codeTheme = ref(settingsStore.theme === ThemeMode.DARK ? "dracula" : "default");

const sqlOptions: EditorConfiguration = {
  mode: "text/x-sql",
  lineNumbers: true,
  smartIndent: true,
  indentUnit: 2,
  tabSize: 2,
  readOnly: false,
  theme: codeTheme.value,
  lineWrapping: true,
  autofocus: false,
};

watch(
  () => settingsStore.theme,
  (t) => {
    const newTheme = t === ThemeMode.DARK ? "dracula" : "default";
    codeTheme.value = newTheme;
    sqlOptions.theme = newTheme;
    if (sqlRef.value?.cminstance) {
      sqlRef.value.cminstance.setOption("theme", newTheme);
    }
  }
);

function onDialogOpened() {
  dialectWatchSkip = true;
  editMode.value = "visual";
  sqlText.value = "";
  visual.value = visualPresetSingle("mysql");
  visualPreviewSql.value = "";
  void nextTick(() => {
    dialectWatchSkip = false;
    applyLinkFromGenIfAny();
  });
}

/** 第三步已填主表/子表时：切到表结构模式并带入名称，减少重复输入 */
function applyLinkFromGenIfAny() {
  const link = props.linkFromGen;
  if (!link) return;
  const touched =
    (link.table_name || "").trim() ||
    (link.table_comment || "").trim() ||
    ((link.sub_table_name || "").trim() && (link.sub_table_fk_name || "").trim());
  if (!touched) return;
  visual.value = mergeGenTableLinkIntoVisual(link, visual.value.dialect);
  editMode.value = "visual";
  visualPreviewSql.value = buildSqlFromVisual(applySubColumns(visual.value));
  ElMessage.info({
    message: "已带入代码生成里的表名，检查无误后点「创建表」即可",
    duration: 2800,
  });
}

watch(
  visual,
  () => {
    if (editMode.value !== "visual" || !visible.value) return;
    visualPreviewSql.value = buildSqlFromVisual(applySubColumns(visual.value));
  },
  { deep: true }
);

watch(editMode, (m) => {
  if (m === "sql") {
    sqlText.value = buildSqlFromVisual(applySubColumns(visual.value));
    void nextTick(() => sqlRef.value?.cminstance?.refresh());
  } else {
    visualPreviewSql.value = buildSqlFromVisual(applySubColumns(visual.value));
  }
});

let dialectWatchSkip = false;
watch(
  () => visual.value.dialect,
  (_d, prev) => {
    if (dialectWatchSkip) return;
    if (prev === undefined) return;
    const d = visual.value.dialect;
    visual.value = visual.value.subEnabled
      ? applySubColumns(visualPresetMasterSub(d))
      : visualPresetSingle(d);
  }
);

function applyVisualPreset(kind: "single" | "masterSub") {
  const d = visual.value.dialect;
  visual.value =
    kind === "single" ? visualPresetSingle(d) : applySubColumns(visualPresetMasterSub(d));
}

function syncVisualToSql() {
  if (!validateVisual()) return;
  sqlText.value = buildSqlFromVisual(applySubColumns(visual.value));
  editMode.value = "sql";
  void nextTick(() => {
    sqlRef.value?.cminstance?.refresh();
  });
  ElMessage.success("已切换到「写 SQL」，可继续改");
}

function onSqlPresetCommand(cmd: string) {
  switch (cmd) {
    case "single-mysql":
      loadPresetSql("single", "mysql");
      break;
    case "single-postgres":
      loadPresetSql("single", "postgres");
      break;
    case "master-mysql":
      loadPresetSql("masterSub", "mysql");
      break;
    case "master-postgres":
      loadPresetSql("masterSub", "postgres");
      break;
    default:
      break;
  }
}

/** 表结构模式提交前校验，避免无效请求 */
function validateVisual(): boolean {
  const v = applySubColumns(visual.value);
  if (!(v.mainTableName || "").trim()) {
    ElMessage.warning("请填写主表表名");
    return false;
  }
  if (v.subEnabled) {
    if (!(v.subTableName || "").trim()) {
      ElMessage.warning("请填写子表表名");
      return false;
    }
    if (!(v.fkColumn || "").trim()) {
      ElMessage.warning("请填写子表上的外键列名");
      return false;
    }
    if (!(v.fkRefColumn || "").trim()) {
      ElMessage.warning("请填写主表上被引用的列名（一般为 id）");
      return false;
    }
  }
  return true;
}

function loadPresetSql(kind: "single" | "masterSub", dialect: SqlDialect) {
  sqlText.value =
    kind === "single"
      ? getExampleFromPresetSingle(dialect)
      : getExampleFromPresetMasterSub(dialect);
}

function copySql() {
  if (!sqlText.value) {
    ElMessage.warning("没有可复制的内容");
    return;
  }
  copy(sqlText.value);
  ElMessage.success("已复制");
}

function handleConfirm() {
  if (editMode.value === "visual" && !validateVisual()) return;
  const sql =
    editMode.value === "sql"
      ? sqlText.value.trim()
      : buildSqlFromVisual(applySubColumns(visual.value)).trim();
  if (!sql) {
    ElMessage.error("请填写表名或 SQL");
    return;
  }
  if (editMode.value === "visual") {
    emit("submit", sql, {
      fromVisual: true,
      visualSnapshot: applySubColumns(visual.value),
    });
  } else {
    emit("submit", sql);
  }
}

function handleCancel() {
  visible.value = false;
}
</script>

<style scoped lang="scss">
.sql-pane {
  position: relative;
}

.visual-pane :deep(.el-textarea__inner) {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

.visual-sql-preview {
  margin-top: 10px;
}

/* 表结构：描述列表表格化，标签列对齐、内容区可伸缩 */
.visual-structure {
  .visual-desc {
    :deep(.el-descriptions__label) {
      width: 108px;
      vertical-align: middle;
    }

    :deep(.el-descriptions__cell) {
      vertical-align: middle;
    }

    :deep(.el-descriptions__content) {
      min-width: 0;
    }

    :deep(.el-descriptions__title) {
      margin-bottom: 8px;
    }
  }
}
</style>
