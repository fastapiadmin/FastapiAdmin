<!-- SQL 控制台：左侧连接/库表导航 + 右侧编辑器与结果区（外部 MySQL/PostgreSQL） -->
<template>
  <div class="fa-full-height">
    <FaWorkbench :side-width="320">
      <template #side>
        <!-- 左：连接 + 库表 -->
        <FaSidePanel :title="$t('common.db.databaseConnections')" class="db-side-panel">
          <template #actions>
            <ElButton
              v-hasPerm="['module_ops:dbconsole:conn:create']"
              type="primary"
              size="small"
              :loading="createLoading"
              @click="handleAdd"
            >
              <ElIcon class="mr-1"><FaSvgIcon icon="ri:add-line" /></ElIcon
              >{{ $t("common.addNew") }}
            </ElButton>
          </template>

          <div class="px-1">
            <div
              v-for="item in connections"
              :key="item.id"
              class="fa-list-item"
              :class="{ 'is-active': item.id === currentId }"
              @click="selectConnection(item)"
            >
              <span
                class="fa-status-dot"
                :style="{
                  background:
                    item.status === 0 ? 'var(--el-color-success)' : 'var(--el-color-info)',
                }"
              />
              <div class="min-w-0 flex-1">
                <div class="fa-list-item__title">{{ item.name }}</div>
                <div class="fa-list-item__meta">
                  {{ item.db_type }} · {{ item.host }}:{{ item.port }}
                </div>
              </div>
              <ElDropdown
                trigger="click"
                @command="(cmd) => handleConnCommand(String(cmd), item)"
                @click.stop
              >
                <FaIconButton
                  icon="ri:more-2-fill"
                  class="fa-list-item__action size-7!"
                  :aria-label="$t('common.more')"
                />
                <template #dropdown>
                  <ElDropdownMenu>
                    <ElDropdownItem command="test">{{
                      $t("common.testConnection")
                    }}</ElDropdownItem>
                    <ElDropdownItem command="edit">{{ $t("common.edit") }}</ElDropdownItem>
                    <ElDropdownItem command="delete" divided>{{
                      $t("common.delete")
                    }}</ElDropdownItem>
                  </ElDropdownMenu>
                </template>
              </ElDropdown>
            </div>
            <FaEmptyState
              v-if="!connections.length"
              icon="ri:database-2-line"
              :title="$t('common.db.noConnection')"
              :description="$t('common.db.noConnectionDesc')"
              compact
            />
          </div>

          <div class="fa-panel-sep fa-hint">{{ $t("common.db.dbTables") }}</div>
          <div class="px-1 pb-2">
            <div v-if="!currentId" class="fa-hint p-2">
              {{ $t("common.db.selectConnectionFirst") }}
            </div>
            <template v-else>
              <div class="fa-hint db-section-label">{{ $t("common.db.schemaLabel") }}</div>
              <div v-for="db in databases" :key="`db-${db.name}`" class="db-tree-node">
                <div
                  class="fa-list-item fa-list-item--sm"
                  :class="{ 'is-active': db.name === currentDatabase }"
                  @click="pickDatabase(db.name)"
                >
                  <FaSvgIcon
                    icon="ri:arrow-right-s-line"
                    class="fa-list-item__icon db-chevron"
                    :class="{ 'is-open': db.name === currentDatabase }"
                  />
                  <FaSvgIcon icon="ri:database-2-line" class="fa-list-item__icon" />
                  <span class="fa-list-item__title" :title="db.name">{{ db.name }}</span>
                </div>

                <div v-if="db.name === currentDatabase" class="db-tables">
                  <div class="db-tables__title">
                    {{ $t("common.db.tablesLabel") }}
                    <span v-if="tables.length">（{{ tables.length }}）</span>
                  </div>
                  <div
                    v-for="table in tables"
                    :key="`t-${table.name}`"
                    class="fa-list-item fa-list-item--sm db-table-item"
                    @click="insertTable(table.name)"
                  >
                    <FaSvgIcon icon="ri:table-line" class="fa-list-item__icon" />
                    <span class="fa-list-item__title" :title="table.name">{{ table.name }}</span>
                  </div>
                  <div v-if="!tables.length" class="fa-hint db-table-empty">
                    {{ $t("common.db.noTablesHint") }}
                  </div>
                </div>
              </div>
              <div v-if="!databases.length" class="fa-hint p-2">
                {{ $t("common.db.noDatabaseHint") }}
              </div>
              <div v-if="!currentDatabase && databases.length" class="fa-hint db-insert-hint">
                {{ $t("common.db.selectDbHint") }}
              </div>
              <div v-else-if="currentDatabase" class="fa-hint db-insert-hint">
                {{ $t("common.db.insertTableHint") }}
              </div>
            </template>
          </div>
        </FaSidePanel>
      </template>

      <ElCard
        shadow="hover"
        class="fa-card flex min-w-0 flex-1 flex-col"
        body-class="flex min-h-0 flex-1 flex-col p-0"
      >
        <div class="flex h-full min-h-0 flex-col">
          <div class="fa-panel-header">
            <span class="fa-panel-title">{{ $t("common.db.sqlConsole") }}</span>
            <ElTag v-if="currentConnection" size="small" type="info">
              {{ currentConnection.name }}
            </ElTag>
            <span v-else class="fa-hint">{{ $t("common.db.noConnectionSelected") }}</span>
            <div class="ml-auto flex flex-wrap items-center justify-end gap-2">
              <span class="fa-hint">{{ $t("common.db.allowWrite") }}</span>
              <ElSwitch v-model="confirmed" size="small" />
              <ElDropdown trigger="click" :disabled="!history.length" @command="applyHistory">
                <ElButton :disabled="!history.length">
                  <ElIcon class="mr-1"><Clock /></ElIcon>历史
                </ElButton>
                <template #dropdown>
                  <ElDropdownMenu>
                    <ElDropdownItem v-for="(item, index) in history" :key="index" :command="item">
                      {{ item.length > 60 ? `${item.slice(0, 60)}…` : item }}
                    </ElDropdownItem>
                  </ElDropdownMenu>
                </template>
              </ElDropdown>
              <ElButton
                v-hasPerm="['module_ops:dbconsole:query:execute']"
                type="primary"
                :loading="running"
                :disabled="!currentId"
                @click="runQuery"
              >
                {{ $t("common.db.execute") }}
              </ElButton>
              <ElButton :disabled="!sql" @click="clearEditor">{{ $t("common.db.clear") }}</ElButton>
            </div>
          </div>

          <div class="px-3 pt-3">
            <ElInput
              v-model="sql"
              type="textarea"
              :aria-label="$t('common.db.sqlConsole')"
              :rows="8"
              resize="vertical"
              class="fa-mono-textarea"
              :placeholder="$t('common.db.sqlPlaceholder')"
              @keydown.ctrl.enter.prevent="runQuery"
            />
            <div class="fa-hint mt-1 text-right">{{ $t("common.db.ctrlEnter") }}</div>
          </div>

          <div class="flex min-h-0 flex-1 flex-col px-3 pb-3">
            <ElAlert
              v-if="queryError"
              type="error"
              :closable="false"
              class="mb-2"
              :title="queryError"
            />
            <template v-if="result">
              <div class="fa-hint mb-2 flex flex-wrap items-center gap-2">
                <ElTag size="small" :type="result.read_only ? 'info' : 'warning'">
                  {{
                    result.read_only
                      ? "$t('common.db.readOnlyQuery')"
                      : "$t('common.db.writeOperation')"
                  }}
                </ElTag>
                <span class="fa-hint">{{ result.rowcount }} 行 · {{ result.elapsed_ms }} ms</span>
                <ElTag v-if="result.masked_columns.length" size="small" type="warning">
                  {{ $t("common.db.masked") }}：{{ result.masked_columns.join("、") }}
                </ElTag>
                <ElTag v-if="result.truncated" size="small" type="info">{{
                  $t("common.db.truncatedRows")
                }}</ElTag>
                <ElButton class="ml-auto" size="small" @click="exportCsv">{{
                  $t("common.db.exportCsv")
                }}</ElButton>
              </div>
              <FaTable
                :data="resultRows"
                :columns="resultColumns"
                height="100%"
                border
                class="min-h-0 flex-1"
              />
            </template>
            <FaEmptyState icon="ri:inbox-line" :title="$t('common.db.noResult')" compact />
          </div>

          <div class="fa-panel-sep fa-hint flex items-center gap-2">
            <span>
              {{
                currentConnection
                  ? `${currentConnection.name} · ${currentConnection.db_type}`
                  : $t("common.db.noConnectionSelected")
              }}
            </span>
            <span v-if="currentDatabase">· {{ currentDatabase }}</span>
            <span v-if="lastRun" class="ml-auto">
              {{ $t("common.db.lastRun") }} {{ lastRun.rows }} · {{ lastRun.ms }} ms
            </span>
          </div>
        </div>
      </ElCard>
    </FaWorkbench>

    <FaDialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      :form-mode="dialogVisible.type"
      :confirm-loading="submitLoading"
      @cancel="handleCloseDialog"
      @confirm="handleSubmit"
      size="md"
    >
      <FaForm
        :key="formRenderKey"
        ref="dataFormRef"
        v-model="formData"
        :items="formItems"
        :rules="rules"
        label-suffix=":"
        :label-width="96"
        label-position="right"
        :span="24"
        :gutter="16"
        :show-reset="false"
        :show-submit="false"
        class="crud-dialog-art-form"
      />
    </FaDialog>
  </div>
</template>

<script lang="ts" setup>
import { Clock } from "@element-plus/icons-vue";
import DbConsoleAPI, {
  type DbConnection,
  type DbConnectionForm,
  type DbObject,
  type DbQueryResult,
} from "@/api/module_ops/dbconsole/connection";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import FaForm from "@/components/forms/fa-form/index.vue";
import type { ColumnOption } from "@/types/component";
import { ElMessage } from "element-plus";

defineOptions({
  name: "DbConsole",
  inheritAttrs: false,
});

type DbConnectionFormModel = DbConnectionForm & { id?: number };

// ── 连接与库表 ────────────────────────────────────────────────────────
const connections = ref<DbConnection[]>([]);
const currentId = ref<number>();
const currentConnection = computed(() =>
  connections.value.find((item) => item.id === currentId.value)
);
const databases = ref<DbObject[]>([]);
const tables = ref<DbObject[]>([]);
const currentDatabase = ref<string>();

const sql = ref("select 1");
const confirmed = ref(false);
const running = ref(false);
const result = ref<DbQueryResult>();
const queryError = ref("");
const lastRun = ref<{ rows: number; ms: number }>();
const history = ref<string[]>([]);
const HISTORY_KEY = "dbconsole:history";

function loadHistory() {
  try {
    const raw = localStorage.getItem(HISTORY_KEY);
    history.value = raw ? (JSON.parse(raw) as string[]) : [];
  } catch {
    history.value = [];
  }
}

function pushHistory(text: string) {
  if (!text) return;
  history.value = [text, ...history.value.filter((item) => item !== text)].slice(0, 10);
  localStorage.setItem(HISTORY_KEY, JSON.stringify(history.value));
}

function applyHistory(text: string) {
  sql.value = text;
}

function extractErrorMessage(error: unknown): string {
  const err = error as { response?: { data?: { msg?: string } }; message?: string };
  return err?.response?.data?.msg || err?.message || "执行失败";
}

const resultColumns = computed<ColumnOption[]>(() =>
  (result.value?.columns ?? []).map((name, index) => ({
    prop: `c${index}`,
    label: name,
    minWidth: 140,
    showOverflowTooltip: true,
  }))
);

const resultRows = computed<Record<string, unknown>[]>(() =>
  (result.value?.rows ?? []).map((row) =>
    Object.fromEntries(row.map((value, index) => [`c${index}`, value]))
  )
);

async function loadConnections() {
  const res = await DbConsoleAPI.listConnections();
  connections.value = res.data.data || [];
  if (currentId.value && !connections.value.some((item) => item.id === currentId.value)) {
    currentId.value = undefined;
    databases.value = [];
    tables.value = [];
  }
}

async function selectConnection(row: DbConnection) {
  currentId.value = row.id;
  currentDatabase.value = undefined;
  tables.value = [];
  result.value = undefined;
  const res = await DbConsoleAPI.listDatabases(row.id);
  databases.value = res.data.data || [];
}

async function pickDatabase(name: string) {
  currentDatabase.value = name;
  if (!currentId.value) return;
  const res = await DbConsoleAPI.listTables(currentId.value, name);
  tables.value = res.data.data || [];
}

function insertTable(name: string) {
  sql.value = `select * from ${name} limit 100`;
}

function clearEditor() {
  sql.value = "";
}

function exportCsv() {
  const current = result.value;
  if (!current || !current.columns.length) return;
  const escapeCell = (value: unknown) => {
    const text = value == null ? "" : String(value);
    return /[",\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
  };
  const header = current.columns.map(escapeCell).join(",");
  const body = current.rows.map((row) => row.map(escapeCell).join(",")).join("\n");
  const blob = new Blob([`\uFEFF${header}\n${body}`], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `query-result-${Date.now()}.csv`;
  link.click();
  URL.revokeObjectURL(url);
}

async function runQuery() {
  if (!currentId.value) {
    ElMessage.warning("请先选择一个连接");
    return;
  }
  if (!sql.value.trim()) {
    ElMessage.warning("请先输入 SQL");
    return;
  }
  running.value = true;
  queryError.value = "";
  try {
    const res = await DbConsoleAPI.runQuery(currentId.value, {
      sql: sql.value,
      confirmed: confirmed.value,
    });
    result.value = res.data.data;
    if (result.value) {
      lastRun.value = { rows: result.value.rowcount, ms: result.value.elapsed_ms };
    }
    pushHistory(sql.value.trim());
  } catch (error) {
    result.value = undefined;
    queryError.value = extractErrorMessage(error);
  } finally {
    running.value = false;
  }
}

function handleConnCommand(command: string, row: DbConnection) {
  if (command === "test") {
    void DbConsoleAPI.testConnection(row.id).then((res) =>
      ElMessage.success(res.data?.msg || "连接成功")
    );
  } else if (command === "edit") {
    void handleOpenDialog("update", row.id);
  } else if (command === "delete") {
    void deleteRow(row);
  }
}

async function deleteRow(row: DbConnection) {
  await confirmDelete(`确认删除连接「${row.name}」？`);
  await DbConsoleAPI.deleteConnections([row.id]);
  if (currentId.value === row.id) {
    currentId.value = undefined;
    databases.value = [];
    tables.value = [];
    result.value = undefined;
  }
  await loadConnections();
}

// ── 新增 / 修改 ───────────────────────────────────────────────────────
const { dialogVisible } = useCrudDialog();
const dataFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const formRenderKey = ref(0);

const initialFormData: DbConnectionFormModel = {
  id: undefined,
  name: "",
  db_type: "mysql",
  host: "",
  port: 3306,
  username: "",
  password: "",
  database: "",
  description: "",
  status: 0,
};
const formData = ref<DbConnectionFormModel>({ ...initialFormData });

const formItems = computed<FormItem[]>(() => [
  {
    label: "名称",
    key: "name",
    type: "input",
    span: 12,
    props: { placeholder: "唯一名称", maxlength: 64 },
  },
  {
    label: "类型",
    key: "db_type",
    type: "select",
    span: 12,
    props: {
      options: [
        { label: "MySQL", value: "mysql" },
        { label: "PostgreSQL", value: "postgres" },
      ],
    },
  },
  { label: "主机", key: "host", type: "input", span: 12, props: { placeholder: "如 127.0.0.1" } },
  {
    label: "端口",
    key: "port",
    type: "number",
    span: 12,
    props: { controlsPosition: "right", min: 1, max: 65535, style: { width: "160px" } },
  },
  { label: "用户名", key: "username", type: "input", span: 12 },
  {
    label: "密码",
    key: "password",
    type: "input",
    span: 12,
    props: { type: "password", showPassword: true, placeholder: "修改时不填表示不变" },
  },
  { label: "默认库", key: "database", type: "input", span: 12, props: { placeholder: "可空" } },
  {
    label: "状态",
    key: "status",
    type: "radiogroup",
    span: 12,
    props: {
      options: [
        { label: "启用", value: 0 },
        { label: "停用", value: 1 },
      ],
    },
  },
  { label: "备注", key: "description", type: "input", span: 24 },
]);

const rules = computed(() => ({
  name: [{ required: true, message: "请输入名称", trigger: "blur" }],
  db_type: [{ required: true, message: "请选择类型", trigger: "change" }],
  host: [{ required: true, message: "请输入主机", trigger: "blur" }],
  port: [{ required: true, message: "请输入端口", trigger: "blur" }],
  username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  password:
    dialogVisible.type === "create"
      ? [{ required: true, message: "请输入密码", trigger: "blur" }]
      : [],
}));

const createLoading = ref(false);

async function handleAdd() {
  createLoading.value = true;
  try {
    await handleOpenDialog("create");
  } finally {
    createLoading.value = false;
  }
}

const { submitLoading, handleCloseDialog, handleOpenDialog, handleSubmit } =
  useCrudForm<DbConnectionFormModel>({
    formData,
    initialFormData,
    dialogVisible,
    dataFormRef,
    formRenderKey,
    detailApi: DbConsoleAPI.detailConnection,
    createApi: DbConsoleAPI.createConnection,
    updateApi: DbConsoleAPI.updateConnection,
    titles: { create: "新增连接", update: "修改连接" },
    onUpdateSuccess: loadConnections,
    onCreateSuccess: loadConnections,
  });

onMounted(() => {
  loadHistory();
  void loadConnections();
});
</script>

<style lang="scss" scoped>
.db-side-panel {
  width: 100%;
  height: 100%;
}

.db-section-label {
  margin-left: 2px;
  white-space: nowrap;
}

.db-chevron {
  transition: transform 0.15s ease;
}

.db-chevron.is-open {
  transform: rotate(90deg);
}

.db-tables {
  margin: 2px 0 8px 26px;
  padding-left: 10px;
  border-left: 1px solid var(--el-border-color-lighter);
}

.db-tables__title {
  padding: 4px 0 2px;
  font-size: var(--fa-font-size-sm);
  color: var(--el-text-color-secondary);
  white-space: nowrap;
}

.db-table-item {
  padding-left: 8px;
}

.db-table-empty {
  padding: 4px 8px 6px;
}

.db-insert-hint {
  margin-top: 8px;
  padding-left: 2px;
}
</style>
