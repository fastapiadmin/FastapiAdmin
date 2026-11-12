<!-- SSH 运维：左侧主机导航 + 右侧终端/批量执行/命令片段工作区 -->
<template>
  <div class="fa-full-height">
    <FaWorkbench :side-width="280">
      <template #side>
        <!-- 左：主机列表 -->
        <ElCard
          shadow="hover"
          class="fa-card flex h-full w-full flex-col"
          body-class="flex min-h-0 flex-1 flex-col p-0"
        >
          <div class="flex h-full min-h-0 flex-col">
            <div class="fa-panel-header justify-between">
              <span class="fa-panel-title">{{ $t("common.sshHost") }}</span>
              <ElButton
                v-hasPerm="['module_ops:ssh:create']"
                type="primary"
                size="small"
                :loading="createLoading"
                @click="handleAdd"
              >
                <ElIcon class="mr-1"><FaSvgIcon icon="ri:add-line" /></ElIcon>新增
              </ElButton>
            </div>

            <div class="px-2 pb-2">
              <ElInput
                v-model="hostKeyword"
                size="small"
                :placeholder="$t('common.searchHost')"
                clearable
                :aria-label="$t('common.searchHost')"
              >
                <template #prefix>
                  <ElIcon><FaSvgIcon icon="ri:search-line" /></ElIcon>
                </template>
              </ElInput>
            </div>

            <ElScrollbar class="min-h-0 flex-1 px-2">
              <div
                v-for="host in filteredHosts"
                :key="host.id"
                class="fa-list-item"
                :class="{ 'is-active': host.id === activeHostId }"
                @click="selectHost(host)"
                @dblclick="openTerminalFor(host)"
              >
                <span
                  class="fa-status-dot"
                  :style="{
                    background:
                      host.status === 0 ? 'var(--el-color-success)' : 'var(--el-color-info)',
                  }"
                />
                <div class="min-w-0 flex-1">
                  <div class="fa-list-item__title">{{ host.name }}</div>
                  <div class="fa-list-item__meta">
                    {{ host.username }}@{{ host.host }}:{{ host.port }}
                  </div>
                </div>
                <ElDropdown
                  trigger="click"
                  @command="(cmd) => handleHostCommand(String(cmd), host)"
                  @click.stop
                >
                  <FaIconButton
                    icon="ri:more-2-fill"
                    class="fa-list-item__action size-7!"
                    :aria-label="$t('common.more')"
                  />
                  <template #dropdown>
                    <ElDropdownMenu>
                      <ElDropdownItem command="terminal">{{
                        $t("common.openTerminal")
                      }}</ElDropdownItem>
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
                v-if="!filteredHosts.length"
                icon="ri:server-line"
                :title="$t('common.noHost')"
                :description="$t('common.noHostDesc')"
                compact
              />
            </ElScrollbar>

            <div class="fa-hint px-3 py-2">{{ $t("common.doubleClickHint") }}</div>
          </div>
        </ElCard>
      </template>

      <!-- 右：工作区 -->
      <ElCard
        shadow="hover"
        class="fa-card flex min-w-0 flex-1 flex-col"
        body-class="flex min-h-0 flex-1 flex-col p-0"
      >
        <div class="flex h-full min-h-0 flex-col">
          <ElTabs v-model="activeTab" class="fa-tabs-fill">
            <!-- 终端 -->
            <ElTabPane :label="$t('common.terminal')" name="terminal">
              <div class="flex h-full min-h-0 flex-col gap-2 p-3">
                <div class="flex flex-wrap items-center gap-2">
                  <ElTag v-if="terminalSession" size="small" type="success">
                    {{ terminalSession.host_name }}
                  </ElTag>
                  <span class="fa-hint">
                    {{
                      terminalSession
                        ? `会话 ${terminalSession.session_id.slice(0, 8)}`
                        : $t("common.noSession")
                    }}
                  </span>
                  <div class="ml-auto flex flex-wrap items-center gap-2">
                    <ElInput
                      v-model="logPath"
                      size="small"
                      :placeholder="$t('common.logPath')"
                      :aria-label="$t('common.logPath')"
                      class="w-[250px]"
                      clearable
                    />
                    <ElButton
                      v-hasPerm="['module_ops:ssh:terminal']"
                      size="small"
                      :disabled="!terminalHostId || !logPath"
                      :loading="terminalOpening"
                      @click="openLogTail"
                    >
                      日志跟踪
                    </ElButton>
                    <ElButton
                      v-if="!terminalSessionId"
                      v-hasPerm="['module_ops:ssh:terminal']"
                      type="primary"
                      size="small"
                      :disabled="!terminalHostId"
                      :loading="terminalOpening"
                      @click="openTerminal"
                    >
                      打开终端
                    </ElButton>
                    <template v-else>
                      <ElButton size="small" @click="clearTerminalOutput">{{
                        $t("common.clearScreen")
                      }}</ElButton>
                      <ElButton size="small" :loading="terminalOpening" @click="reconnectTerminal"
                        >重连</ElButton
                      >
                      <ElButton size="small" @click="sendCtrlC">Ctrl+C</ElButton>
                      <ElButton size="small" @click="closeTerminal">{{
                        $t("common.closeAction")
                      }}</ElButton>
                    </template>
                  </div>
                </div>

                <pre ref="terminalRef" class="fa-terminal min-h-0 flex-1 overflow-auto">{{
                  terminalOutput || $t("common.noOutputHint")
                }}</pre>

                <div class="flex items-center gap-2">
                  <ElInput
                    v-model="terminalInput"
                    :disabled="!terminalSessionId"
                    :placeholder="$t('common.cmdPlaceholder')"
                    @keydown="onTerminalInputKeydown"
                    :aria-label="$t('common.cmdPlaceholder')"
                  />
                  <ElButton
                    type="primary"
                    :disabled="!terminalSessionId"
                    @click="sendTerminalInput"
                  >
                    {{ $t("common.send") }}
                  </ElButton>
                </div>
              </div>
            </ElTabPane>

            <!-- 批量执行 -->
            <ElTabPane :label="$t('common.batchExec')" name="batch">
              <div class="flex h-full min-h-0 flex-col gap-2 p-3">
                <div class="flex flex-wrap items-center gap-2">
                  <ElSelect
                    v-model="batchHostIds"
                    multiple
                    collapse-tags
                    collapse-tags-tooltip
                    filterable
                    placeholder="选择目标主机（最多 50）"
                    class="w-[340px]"
                  >
                    <ElOption
                      v-for="host in hosts"
                      :key="host.id"
                      :label="host.name"
                      :value="host.id"
                    />
                  </ElSelect>
                  <ElButton :disabled="!enabledHostIds.length" @click="selectAllEnabled">
                    全选启用（{{ enabledHostIds.length }}）
                  </ElButton>
                  <ElButton
                    v-hasPerm="['module_ops:ssh:exec']"
                    type="primary"
                    :loading="batchRunning"
                    :disabled="!batchHostIds.length"
                    @click="runBatch"
                  >
                    执行
                  </ElButton>
                  <span class="fa-hint">命令原样交给远端 shell；执行会写入审计日志</span>
                </div>

                <ElInput
                  v-model="batchCommand"
                  type="textarea"
                  :rows="4"
                  class="fa-mono-textarea"
                  placeholder="例如：uptime && df -h（可从「命令片段」填入）"
                  aria-label="例如：uptime && df -h（可从「命令片段」填入）"
                />

                <ElScrollbar class="min-h-0 flex-1">
                  <div v-for="item in batchResults" :key="item.host_id" class="fa-block-card">
                    <div class="flex items-center gap-2">
                      <span
                        class="fa-status-dot"
                        :style="{
                          background: item.ok
                            ? 'var(--el-color-success)'
                            : 'var(--el-color-danger)',
                        }"
                      />
                      <span class="font-medium">{{ item.host_name }}</span>
                      <ElTag size="small" :type="item.ok ? 'success' : 'danger'">
                        {{ item.exit_status ?? "-" }}
                      </ElTag>
                      <span class="fa-hint ml-auto">{{ item.elapsed_ms }} ms</span>
                      <ElButton link size="small" @click="toggleResult(item.host_id)">
                        {{ expandedResults.has(item.host_id) ? "收起" : "查看输出" }}
                      </ElButton>
                    </div>
                    <pre v-if="expandedResults.has(item.host_id)" class="fa-block-card__output">{{
                      item.stdout || item.stderr || item.error
                    }}</pre>
                  </div>
                  <FaEmptyState
                    v-if="!batchResults.length"
                    icon="ri:terminal-box-line"
                    title="暂无执行结果"
                    description="选择主机并执行命令后在此显示结果"
                    compact
                  />
                </ElScrollbar>
              </div>
            </ElTabPane>

            <!-- 命令片段 -->
            <ElTabPane :label="$t('common.snippets')" name="snippet">
              <div class="flex h-full min-h-0 flex-col p-3">
                <div class="mb-2 flex items-center justify-between">
                  <span class="fa-panel-title">{{ $t("common.commonCommands") }}</span>
                  <ElButton
                    v-hasPerm="['module_ops:snippet:create']"
                    type="primary"
                    size="small"
                    @click="handleSnippetAdd"
                  >
                    新增片段
                  </ElButton>
                </div>
                <div class="mb-2">
                  <ElInput
                    v-model="snippetKeyword"
                    size="small"
                    placeholder="搜索片段名称 / 命令"
                    clearable
                    aria-label="搜索片段名称 / 命令"
                  />
                </div>
                <ElScrollbar class="min-h-0 flex-1">
                  <div v-for="item in filteredSnippets" :key="item.id" class="fa-block-card">
                    <div class="flex items-center gap-2">
                      <span class="font-medium">{{ item.name }}</span>
                      <span class="ml-auto flex items-center gap-1">
                        <ElButton
                          v-hasPerm="['module_ops:ssh:exec']"
                          link
                          type="primary"
                          @click="applySnippet(item)"
                        >
                          填入批量执行
                        </ElButton>
                        <ElButton
                          v-hasPerm="['module_ops:snippet:update']"
                          link
                          @click="handleSnippetEdit(item)"
                        >
                          编辑
                        </ElButton>
                        <ElButton link type="danger" @click="deleteSnippet(item)">删除</ElButton>
                      </span>
                    </div>
                    <pre class="mt-1 rounded bg-(--el-fill-color-light) p-2 text-xs">{{
                      item.command
                    }}</pre>
                    <div v-if="item.description" class="fa-hint mt-1">
                      {{ item.description }}
                    </div>
                  </div>
                  <FaEmptyState
                    v-if="!snippets.length"
                    icon="ri:command-line"
                    title="暂无命令片段"
                    description="保存常用命令，批量执行更高效"
                    compact
                  />
                </ElScrollbar>
              </div>
            </ElTabPane>
          </ElTabs>
        </div>
      </ElCard>
    </FaWorkbench>

    <!-- 主机新增/修改 -->
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

    <!-- 片段新增/修改 -->
    <FaDialog
      v-model="snippetDialogVisible.visible"
      :title="snippetDialogVisible.title"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      :form-mode="snippetDialogVisible.type"
      :confirm-loading="snippetSubmitLoading"
      @cancel="handleSnippetClose"
      @confirm="handleSnippetSubmit"
      size="sm"
    >
      <FaForm
        :key="snippetFormRenderKey"
        ref="snippetFormRef"
        v-model="snippetFormData"
        :items="snippetFormItems"
        :rules="snippetRules"
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
import SshAPI, {
  type BatchExecResult,
  type SshHost,
  type SshHostForm,
  type SshSnippet,
  type TerminalSession,
} from "@/api/module_ops/ssh";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import FaForm from "@/components/forms/fa-form/index.vue";
import { ElMessage } from "element-plus";

defineOptions({
  name: "SshOps",
  inheritAttrs: false,
});

const activeTab = ref("terminal");
const hosts = ref<SshHost[]>([]);
const snippets = ref<SshSnippet[]>([]);
const hostKeyword = ref("");
const activeHostId = ref<number>();

const snippetKeyword = ref("");

const filteredSnippets = computed(() => {
  const keyword = snippetKeyword.value.trim().toLowerCase();
  if (!keyword) return snippets.value;
  return snippets.value.filter(
    (item) =>
      item.name.toLowerCase().includes(keyword) || item.command.toLowerCase().includes(keyword)
  );
});

const filteredHosts = computed(() => {
  const keyword = hostKeyword.value.trim().toLowerCase();
  if (!keyword) return hosts.value;
  return hosts.value.filter(
    (host) =>
      host.name.toLowerCase().includes(keyword) ||
      host.host.toLowerCase().includes(keyword) ||
      host.username.toLowerCase().includes(keyword)
  );
});

async function loadHosts() {
  const res = await SshAPI.listHosts();
  hosts.value = res.data.data || [];
}

async function loadSnippets() {
  const res = await SshAPI.listSnippets();
  snippets.value = res.data.data || [];
}

function selectHost(host: SshHost) {
  activeHostId.value = host.id;
  terminalHostId.value = host.id;
}

function handleHostCommand(command: string, host: SshHost) {
  if (command === "terminal") {
    openTerminalFor(host);
  } else if (command === "test") {
    void SshAPI.testHost(host.id).then((res) => ElMessage.success(res.data?.msg || "连接成功"));
  } else if (command === "edit") {
    void handleOpenDialog("update", host.id);
  } else if (command === "delete") {
    void deleteHost(host);
  }
}

async function deleteHost(host: SshHost) {
  await confirmDelete(`确认删除主机「${host.name}」？`);
  await SshAPI.deleteHosts([host.id]);
  if (activeHostId.value === host.id) activeHostId.value = undefined;
  await loadHosts();
}

// ── 主机表单 ──────────────────────────────────────────────────────────
type SshHostFormModel = SshHostForm & { id?: number };

const { dialogVisible } = useCrudDialog();
const dataFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const formRenderKey = ref(0);

const initialFormData: SshHostFormModel = {
  id: undefined,
  name: "",
  host: "",
  port: 22,
  username: "root",
  auth_type: "password",
  password: "",
  private_key: "",
  passphrase: "",
  status: 0,
  description: "",
};
const formData = ref<SshHostFormModel>({ ...initialFormData });

const formItems = computed<FormItem[]>(() => {
  const isKey = formData.value.auth_type === "key";
  return [
    { label: "名称", key: "name", type: "input", span: 12, props: { placeholder: "唯一名称" } },
    { label: "地址", key: "host", type: "input", span: 12, props: { placeholder: "如 10.0.0.1" } },
    {
      label: "端口",
      key: "port",
      type: "number",
      span: 12,
      props: { controlsPosition: "right", min: 1, max: 65535, style: { width: "160px" } },
    },
    { label: "用户名", key: "username", type: "input", span: 12 },
    {
      label: "认证方式",
      key: "auth_type",
      type: "radiogroup",
      span: 12,
      props: {
        options: [
          { label: "密码", value: "password" },
          { label: "私钥", value: "key" },
        ],
      },
    },
    {
      label: "密码",
      key: "password",
      type: "input",
      span: 12,
      hidden: isKey,
      props: { type: "password", showPassword: true, placeholder: "修改时不填表示不变" },
    },
    {
      label: "私钥",
      key: "private_key",
      type: "input",
      span: 24,
      hidden: !isKey,
      props: { type: "textarea", rows: 6, placeholder: "-----BEGIN OPENSSH PRIVATE KEY-----" },
    },
    {
      label: "私钥口令",
      key: "passphrase",
      type: "input",
      span: 12,
      hidden: !isKey,
      props: { type: "password", showPassword: true, placeholder: "可选" },
    },
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
  ];
});

const rules = computed(() => {
  const isCreate = dialogVisible.type === "create";
  const isKey = formData.value.auth_type === "key";
  return {
    name: [{ required: true, message: "请输入名称", trigger: "blur" }],
    host: [{ required: true, message: "请输入地址", trigger: "blur" }],
    username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
    password:
      isCreate && !isKey ? [{ required: true, message: "请输入密码", trigger: "blur" }] : [],
    private_key:
      isCreate && isKey ? [{ required: true, message: "请输入私钥", trigger: "blur" }] : [],
  };
});

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
  useCrudForm<SshHostFormModel>({
    formData,
    initialFormData,
    dialogVisible,
    dataFormRef,
    formRenderKey,
    detailApi: SshAPI.detailHost,
    createApi: SshAPI.createHost,
    updateApi: SshAPI.updateHost,
    titles: { create: "新增主机", update: "修改主机" },
    onUpdateSuccess: loadHosts,
    onCreateSuccess: loadHosts,
  });

// ── 片段表单 ──────────────────────────────────────────────────────────
type SshSnippetFormModel = {
  id?: number;
  name: string;
  command: string;
  description?: string | null;
};

const { dialogVisible: snippetDialogVisible } = useCrudDialog();
const snippetFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const snippetFormRenderKey = ref(0);

const initialSnippetForm: SshSnippetFormModel = {
  id: undefined,
  name: "",
  command: "",
  description: "",
};
const snippetFormData = ref<SshSnippetFormModel>({ ...initialSnippetForm });

const snippetFormItems = computed<FormItem[]>(() => [
  { label: "名称", key: "name", type: "input", span: 12 },
  {
    label: "命令",
    key: "command",
    type: "input",
    span: 12,
    props: { type: "textarea", rows: 4, placeholder: "如 df -h" },
  },
  { label: "备注", key: "description", type: "input", span: 24 },
]);

const snippetRules = computed(() => ({
  name: [{ required: true, message: "请输入名称", trigger: "blur" }],
  command: [{ required: true, message: "请输入命令", trigger: "blur" }],
}));

function handleSnippetAdd() {
  void handleSnippetOpen("create");
}

function handleSnippetEdit(snippet: SshSnippet) {
  void handleSnippetOpen("update", snippet.id);
}

function applySnippet(snippet: SshSnippet) {
  batchCommand.value = snippet.command;
  activeTab.value = "batch";
}

async function deleteSnippet(snippet: SshSnippet) {
  await confirmDelete(`确认删除片段「${snippet.name}」？`);
  await SshAPI.deleteSnippets([snippet.id]);
  await loadSnippets();
}

const {
  submitLoading: snippetSubmitLoading,
  handleCloseDialog: handleSnippetClose,
  handleOpenDialog: handleSnippetOpen,
  handleSubmit: handleSnippetSubmit,
} = useCrudForm<SshSnippetFormModel>({
  formData: snippetFormData,
  initialFormData: initialSnippetForm,
  dialogVisible: snippetDialogVisible,
  dataFormRef: snippetFormRef,
  formRenderKey: snippetFormRenderKey,
  detailApi: (snippetId: number) => {
    const row = snippets.value.find((item) => item.id === snippetId);
    return Promise.resolve({ data: { data: row as SshSnippetFormModel | undefined } });
  },
  createApi: SshAPI.createSnippet,
  updateApi: SshAPI.updateSnippet,
  titles: { create: "新增命令片段", update: "修改命令片段" },
  onUpdateSuccess: loadSnippets,
  onCreateSuccess: loadSnippets,
});

// ── 批量执行 ──────────────────────────────────────────────────────────
const batchHostIds = ref<number[]>([]);
const batchCommand = ref("");
const batchRunning = ref(false);
const batchResults = ref<BatchExecResult[]>([]);
const expandedResults = ref<Set<number>>(new Set());

const enabledHostIds = computed(() =>
  hosts.value.filter((host) => host.status === 0).map((host) => host.id)
);

function selectAllEnabled() {
  batchHostIds.value = [...enabledHostIds.value];
}

function toggleResult(hostId: number) {
  const next = new Set(expandedResults.value);
  if (next.has(hostId)) {
    next.delete(hostId);
  } else {
    next.add(hostId);
  }
  expandedResults.value = next;
}

async function runBatch() {
  if (!batchHostIds.value.length || !batchCommand.value.trim()) {
    ElMessage.warning("请选择主机并填写命令");
    return;
  }
  batchRunning.value = true;
  try {
    const res = await SshAPI.batchExec({
      host_ids: batchHostIds.value,
      command: batchCommand.value,
      timeout: 15,
    });
    const results = res.data.data || [];
    results.sort((a, b) => a.host_name.localeCompare(b.host_name));
    batchResults.value = results;
    expandedResults.value = new Set(results.filter((item) => !item.ok).map((item) => item.host_id));
    ElMessage.success("批量执行完成");
  } finally {
    batchRunning.value = false;
  }
}

// ── 终端（POST 轮询）──────────────────────────────────────────────────
const terminalHostId = ref<number>();
const terminalOpening = ref(false);
const terminalSession = ref<TerminalSession>();
const terminalSessionId = computed(() => terminalSession.value?.session_id || "");
const terminalOutput = ref("");
const terminalInput = ref("");
const terminalRef = ref<HTMLElement>();
const logPath = ref("");
let pollTimer: number | undefined;

function b64encode(text: string): string {
  const bytes = new TextEncoder().encode(text);
  let binary = "";
  bytes.forEach((byte) => (binary += String.fromCharCode(byte)));
  return btoa(binary);
}

function b64decode(value: string): string {
  const binary = atob(value);
  const bytes = Uint8Array.from(binary, (char) => char.charCodeAt(0));
  return new TextDecoder().decode(bytes);
}

// 轻量终端缓冲：处理 ANSI 转义（颜色/光标）、回车覆盖、退格，避免原样显示控制字符
const MAX_TERM_LINES = 2000;
const termLines: string[] = [];
let termRow = 0;
let termCol = 0;

function resetTerminal() {
  termLines.length = 0;
  termRow = 0;
  termCol = 0;
  terminalOutput.value = "";
}

function scrollTerminal() {
  nextTick(() => {
    if (terminalRef.value) terminalRef.value.scrollTop = terminalRef.value.scrollHeight;
  });
}

function trimTerminal() {
  if (termLines.length <= MAX_TERM_LINES) return;
  const drop = termLines.length - MAX_TERM_LINES;
  termLines.splice(0, drop);
  termRow = Math.max(0, termRow - drop);
}

function processTerminalChunk(chunk: string) {
  // 用 RegExp 构造，避免 eslint no-control-regex（\x1b = ESC, \x07 = BEL）
  const esc = String.fromCharCode(0x1b);
  const bel = String.fromCharCode(0x07);
  const oscRe = new RegExp(`${esc}\\][^${bel}${esc}]*(?:${bel}|${esc}\\\\)`, "g");
  const csiRe = new RegExp(`${esc}\\[[0-9;?]*[a-zA-Z]`, "g");
  const charsetRe = new RegExp(`${esc}[()][A-Z0-9]`, "g");
  const text = chunk.replace(oscRe, "").replace(csiRe, "").replace(charsetRe, "");
  for (const ch of text) {
    if (ch === "\r") {
      termCol = 0;
    } else if (ch === "\n") {
      termRow += 1;
      if (termLines[termRow] === undefined) termLines[termRow] = "";
      termCol = 0;
    } else if (ch === "\b") {
      termCol = Math.max(0, termCol - 1);
      termLines[termRow] = (termLines[termRow] ?? "").slice(0, termCol);
    } else if (ch < " ") {
      continue;
    } else {
      const line = termLines[termRow] ?? "";
      const padded = line.padEnd(termCol, " ");
      termLines[termRow] = padded.slice(0, termCol) + ch + padded.slice(termCol + 1);
      termCol += 1;
    }
  }
  trimTerminal();
  terminalOutput.value = termLines.join("\n");
  scrollTerminal();
}

function appendSystemLine(text: string) {
  processTerminalChunk(`${text}\r\n`);
}

function startPolling() {
  stopPolling();
  pollTimer = window.setInterval(async () => {
    if (!terminalSessionId.value) return;
    try {
      const res = await SshAPI.pollTerminal(terminalSessionId.value, 1.2);
      const payload = res.data.data;
      if (payload?.data) processTerminalChunk(b64decode(payload.data));
      if (payload?.closed) {
        appendSystemLine("[会话已结束]");
        stopPolling();
      }
    } catch {
      stopPolling();
    }
  }, 700);
}

function stopPolling() {
  if (pollTimer !== undefined) {
    window.clearInterval(pollTimer);
    pollTimer = undefined;
  }
}

async function openTerminalFor(host: SshHost) {
  selectHost(host);
  activeTab.value = "terminal";
  await openTerminal();
}

function measureTerminal(): { cols: number; rows: number } {
  const element = terminalRef.value;
  const width = element?.clientWidth ?? 800;
  const height = element?.clientHeight ?? 420;
  // 12px 等宽字体约 7.2px/字符、约 18.6px/行，预留滚动条与内边距
  return {
    cols: Math.max(40, Math.floor((width - 24) / 7.2)),
    rows: Math.max(10, Math.floor((height - 24) / 18.6)),
  };
}

let resizeTimer: number | undefined;
function onWindowResize() {
  if (!terminalSessionId.value) return;
  if (resizeTimer !== undefined) window.clearTimeout(resizeTimer);
  resizeTimer = window.setTimeout(() => {
    if (!terminalSessionId.value) return;
    const size = measureTerminal();
    void SshAPI.resizeTerminal(terminalSessionId.value, size.cols, size.rows).catch(
      () => undefined
    );
  }, 300);
}

async function reconnectTerminal() {
  await closeTerminal();
  await openTerminal();
}

async function openTerminal() {
  if (!terminalHostId.value) return;
  terminalOpening.value = true;
  try {
    const size = measureTerminal();
    const res = await SshAPI.openTerminal({
      host_id: terminalHostId.value,
      cols: size.cols,
      rows: size.rows,
    });
    terminalSession.value = res.data.data;
    resetTerminal();
    appendSystemLine(`[已连接 ${terminalSession.value?.host_name}]`);
    startPolling();
  } finally {
    terminalOpening.value = false;
  }
}

async function openLogTail() {
  if (!terminalHostId.value || !logPath.value.trim()) return;
  terminalOpening.value = true;
  try {
    const res = await SshAPI.openLog({
      host_id: terminalHostId.value,
      path: logPath.value.trim(),
      lines: 200,
    });
    terminalSession.value = res.data.data;
    resetTerminal();
    appendSystemLine(`[日志跟踪 ${logPath.value}]`);
    startPolling();
  } finally {
    terminalOpening.value = false;
  }
}

const inputHistory: string[] = [];
let inputHistoryIndex = -1;

async function sendTerminalInput() {
  if (!terminalSessionId.value) return;
  const text = terminalInput.value;
  terminalInput.value = "";
  if (text.trim()) {
    inputHistory.push(text);
    inputHistoryIndex = inputHistory.length;
  }
  await SshAPI.inputTerminal(terminalSessionId.value, b64encode(`${text}\r`));
}

function onTerminalInputKeydown(event: Event | KeyboardEvent) {
  const key = (event as KeyboardEvent).key;
  if (key === "Enter") {
    event.preventDefault();
    void sendTerminalInput();
    return;
  }
  if (key === "ArrowUp") {
    event.preventDefault();
    if (inputHistoryIndex > 0) {
      inputHistoryIndex -= 1;
      terminalInput.value = inputHistory[inputHistoryIndex] ?? "";
    }
    return;
  }
  if (key === "ArrowDown") {
    event.preventDefault();
    if (inputHistoryIndex < inputHistory.length - 1) {
      inputHistoryIndex += 1;
      terminalInput.value = inputHistory[inputHistoryIndex] ?? "";
    } else {
      inputHistoryIndex = inputHistory.length;
      terminalInput.value = "";
    }
  }
}

async function sendCtrlC() {
  if (!terminalSessionId.value) return;
  await SshAPI.inputTerminal(terminalSessionId.value, b64encode("\x03"));
}

function clearTerminalOutput() {
  terminalOutput.value = "";
}

async function closeTerminal() {
  const sessionId = terminalSessionId.value;
  stopPolling();
  terminalSession.value = undefined;
  if (sessionId) {
    await SshAPI.closeTerminal(sessionId).catch(() => undefined);
  }
  appendSystemLine("[已关闭]");
}

onMounted(async () => {
  await loadHosts();
  await loadSnippets();
  window.addEventListener("resize", onWindowResize);
});

onBeforeUnmount(() => {
  stopPolling();
  window.removeEventListener("resize", onWindowResize);
  if (resizeTimer !== undefined) window.clearTimeout(resizeTimer);
});
</script>
