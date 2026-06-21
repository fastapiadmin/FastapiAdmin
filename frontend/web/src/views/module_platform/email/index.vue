<!-- 邮件管理：Fa 布局 + useTable，3Tab 各自独立数据 -->
<template>
  <div class="fa-full-height">
    <ElTabs v-model="activeTab" @tab-change="onTabChange">
      <!-- Tab 1: SMTP 配置 -->
      <ElTabPane label="SMTP 配置" name="config">
        <FaSearchBar
          v-show="configShowSearchBar"
          v-model="configSearchForm"
          :items="configSearchItems"
          :is-expand="false"
          :show-expand="true"
          :show-reset="true"
          :show-search="true"
          :disabled-search="false"
          :default-expanded="false"
          :button-left-limit="0"
          @search="handleConfigSearch"
          @reset="onConfigResetSearch"
        />

        <ElCard
          shadow="hover"
          class="fa-table-card"
          :style="{ 'margin-top': configShowSearchBar ? '12px' : '0' }"
        >
          <FaTableHeader
            v-model:columns="configColumnChecks"
            v-model:showSearchBar="configShowSearchBar"
            :loading="configLoading"
            @refresh="refreshConfig"
          >
            <template #left>
              <FaTableHeaderLeft
                :remove-ids="configSelectedIds"
                :perm-create="['module_platform:email:update']"
                :perm-delete="['module_platform:email:update']"
                :delete-loading="configBatchDeleting"
                :create-loading="configCreateLoading"
                @add="handleConfigAdd"
                @delete="handleConfigBatchDelete"
              />
            </template>
          </FaTableHeader>

          <FaTable
            ref="configTableRef"
            :loading="configLoading"
            :data="configData"
            :columns="configColumns"
            :pagination="configPagination"
            @selection-change="onConfigSelectionChange"
            @pagination:size-change="handleConfigSizeChange"
            @pagination:current-change="handleConfigCurrentChange"
          />
        </ElCard>
      </ElTabPane>

      <!-- Tab 2: 邮件模板 -->
      <ElTabPane label="邮件模板" name="template">
        <FaSearchBar
          v-show="templateShowSearchBar"
          v-model="templateSearchForm"
          :items="templateSearchItems"
          :is-expand="false"
          :show-expand="true"
          :show-reset="true"
          :show-search="true"
          :disabled-search="false"
          :default-expanded="false"
          :button-left-limit="0"
          @search="handleTemplateSearch"
          @reset="onTemplateResetSearch"
        />

        <ElCard
          shadow="hover"
          class="fa-table-card"
          :style="{ 'margin-top': templateShowSearchBar ? '12px' : '0' }"
        >
          <FaTableHeader
            v-model:columns="templateColumnChecks"
            v-model:showSearchBar="templateShowSearchBar"
            :loading="templateLoading"
            @refresh="refreshTemplate"
          >
            <template #left>
              <FaTableHeaderLeft
                :remove-ids="templateSelectedIds"
                :perm-create="['module_platform:email:update']"
                :perm-delete="['module_platform:email:update']"
                :delete-loading="templateBatchDeleting"
                :create-loading="templateCreateLoading"
                @add="handleTemplateAdd"
                @delete="handleTemplateBatchDelete"
              />
            </template>
          </FaTableHeader>

          <FaTable
            ref="templateTableRef"
            :loading="templateLoading"
            :data="templateData"
            :columns="templateColumns"
            :pagination="templatePagination"
            @selection-change="onTemplateSelectionChange"
            @pagination:size-change="handleTemplateSizeChange"
            @pagination:current-change="handleTemplateCurrentChange"
          />
        </ElCard>
      </ElTabPane>

      <!-- Tab 3: 发送日志 -->
      <ElTabPane label="发送日志" name="log">
        <FaSearchBar
          v-show="logShowSearchBar"
          v-model="logSearchForm"
          :items="logSearchItems"
          :is-expand="false"
          :show-expand="true"
          :show-reset="true"
          :show-search="true"
          :disabled-search="false"
          :default-expanded="false"
          :button-left-limit="0"
          @search="handleLogSearch"
          @reset="onLogResetSearch"
        />

        <ElCard
          shadow="hover"
          class="fa-table-card"
          :style="{ 'margin-top': logShowSearchBar ? '12px' : '0' }"
        >
          <FaTableHeader
            v-model:columns="logColumnChecks"
            v-model:showSearchBar="logShowSearchBar"
            :loading="logLoading"
            @refresh="refreshLog"
          />

          <FaTable
            :loading="logLoading"
            :data="logData"
            :columns="logColumns"
            :pagination="logPagination"
            @pagination:size-change="handleLogSizeChange"
            @pagination:current-change="handleLogCurrentChange"
          />
        </ElCard>
      </ElTabPane>
    </ElTabs>

    <!-- SMTP 配置弹窗 -->
    <FaDialog
      v-model="configDialogVisible.visible"
      :title="configDialogVisible.title"
      width="640px"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      :form-mode="configDialogVisible.type"
      :confirm-loading="configSubmitting"
      @cancel="handleCloseConfigDialog"
      @confirm="handleSubmitConfig"
    >
      <FaForm
        :key="configFormRenderKey"
        scrollbar
        max-height="70vh"
        ref="configFormRef"
        v-model="configFormData"
        :items="configDialogFormItems"
        :rules="configFormRules"
        label-suffix=":"
        :label-width="110"
        label-position="right"
        :span="24"
        :gutter="16"
        :show-reset="false"
        :show-submit="false"
        class="crud-dialog-art-form"
      >
        <template #smtp_password_help>
          <span class="text-g-400" style="font-size: 12px">留空不修改原密码</span>
        </template>
      </FaForm>
    </FaDialog>

    <!-- 邮件模板弹窗 -->
    <FaDialog
      v-model="templateDialogVisible.visible"
      :title="templateDialogVisible.title"
      width="680px"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      :form-mode="templateDialogVisible.type"
      :confirm-loading="templateSubmitting"
      @cancel="handleCloseTemplateDialog"
      @confirm="handleSubmitTemplate"
    >
      <FaForm
        :key="templateFormRenderKey"
        scrollbar
        max-height="70vh"
        ref="templateFormRef"
        v-model="templateFormData"
        :items="templateDialogFormItems"
        :rules="templateFormRules"
        label-suffix=":"
        :label-width="110"
        label-position="right"
        :span="24"
        :gutter="16"
        :show-reset="false"
        :show-submit="false"
        class="crud-dialog-art-form"
      />
    </FaDialog>

    <!-- 发送测试邮件弹窗 -->
    <FaDialog
      v-model="sendVisible"
      title="发送测试邮件"
      width="520px"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      :confirm-loading="sendSubmitting"
      @cancel="handleCloseSendDialog"
      @confirm="handleSubmitSend"
    >
      <FaForm
        ref="sendFormRef"
        v-model="sendFormData"
        :items="sendDialogFormItems"
        :rules="sendFormRules"
        label-suffix=":"
        :label-width="110"
        label-position="right"
        :span="24"
        :gutter="16"
        :show-reset="false"
        :show-submit="false"
        class="crud-dialog-art-form"
      />
    </FaDialog>

    <!-- 测试连接弹窗 -->
    <FaDialog
      v-model="testVisible"
      title="测试 SMTP 连接"
      width="420px"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      :confirm-loading="testSubmitting"
      @cancel="handleCloseTestDialog"
      @confirm="handleSubmitTest"
    >
      <FaForm
        ref="testFormRef"
        v-model="testFormData"
        :items="testDialogFormItems"
        :rules="testFormRules"
        label-suffix=":"
        :label-width="110"
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

<script setup lang="ts">
import { h } from "vue";
import { useAuth } from "@/hooks/core/useAuth";
import { useTable } from "@/hooks/core/useTable";
import { useTableSelection } from "@/hooks/core/useTableSelection";
import { useCrudDialog } from "@/hooks/core/useCrudDialog";
import { confirmDelete, confirmBatchDelete } from "@/hooks/core/useConfirm";
import { renderTableOperationCell, type TableOperationAction, resolveStatusColumns } from "@utils";
import EmailAPI, {
  type EmailConfigTable,
  type EmailConfigCreateForm,
  type EmailConfigUpdateForm,
  type EmailTemplateTable,
  type EmailTemplateCreateForm,
  type EmailTemplateUpdateForm,
  type EmailLogTable,
} from "@/api/module_platform/email";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import type FaForm from "@/components/forms/fa-form/index.vue";
import FaStatusTag from "@/components/others/fa-status-tag/index.vue";
import { ElMessage } from "element-plus";

defineOptions({ name: "Email" });

const { hasAuth } = useAuth();
const activeTab = ref("config");

// ══════════════════ SMTP 配置 Tab ════════════════════

type ConfigSearchForm = { name?: string };

const configSearchForm = ref<ConfigSearchForm>({ name: undefined });
const configShowSearchBar = ref(true);

const configSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "配置名称",
    key: "name",
    type: "input",
    placeholder: "请输入配置名称",
    clearable: true,
    span: 6,
  },
]);

const configTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const {
  selectedIds: configSelectedIds,
  batchDeleting: configBatchDeleting,
  onTableSelectionChange: onConfigSelectionChange,
} = useTableSelection<EmailConfigTable>();

const configCreateLoading = ref(false);

const {
  columns: configColumns,
  columnChecks: configColumnChecks,
  data: configData,
  loading: configLoading,
  pagination: configPagination,
  getData: getConfigData,
  replaceSearchParams: replaceConfigSearchParams,
  resetSearchParams: resetConfigSearchParams,
  handleSizeChange: handleConfigSizeChange,
  handleCurrentChange: handleConfigCurrentChange,
  refreshData: refreshConfig,
  refreshCreate: refreshConfigCreate,
  refreshUpdate: refreshConfigUpdate,
  refreshRemove: refreshConfigRemove,
} = useTable({
  core: {
    apiFn: EmailAPI.listConfig,
    apiParams: { page_no: 1, page_size: 10 },
    columnsFactory: resolveStatusColumns<EmailConfigTable>(() => [
      { type: "selection", width: 48, fixed: "left" },
      { type: "globalIndex", width: 56, label: "序号" },
      { prop: "name", label: "配置名称", minWidth: 140, showOverflowTooltip: true },
      { prop: "smtp_host", label: "SMTP 服务器", minWidth: 160, showOverflowTooltip: true },
      { prop: "smtp_port", label: "端口", width: 70 },
      { prop: "smtp_user", label: "用户名", minWidth: 140, showOverflowTooltip: true },
      { prop: "from_name", label: "发件人", width: 100, showOverflowTooltip: true },
      {
        prop: "use_tls",
        label: "SSL/TLS",
        width: 90,
        status: {
          true: { type: "success", text: "启用" },
          false: { type: "info", text: "禁用" },
        },
      },
      {
        prop: "is_default",
        label: "默认",
        width: 70,
        status: {
          true: { type: "warning", size: "small", text: "默认" },
          false: { type: "info", size: "small", text: "—" },
        },
      },
      {
        prop: "status",
        label: "状态",
        width: 70,
        status: {
          "0": { type: "success", size: "small", text: "正常" },
          "1": { type: "danger", size: "small", text: "禁用" },
        },
      },
      {
        prop: "operation",
        label: "操作",
        width: 240,
        fixed: "right",
        align: "right",
        formatter: (row: EmailConfigTable) => {
          const actions: TableOperationAction[] = [
            {
              key: "test",
              label: "测试",
              artType: "view" as const,
              perm: "module_platform:email:update",
              run: () => openTestDialog(row),
            },
            {
              key: "edit",
              label: "编辑",
              artType: "edit" as const,
              perm: "module_platform:email:update",
              run: () => openConfigDialog("update", row),
            },
            {
              key: "delete",
              label: "删除",
              artType: "delete" as const,
              perm: "module_platform:email:update",
              run: () => deleteConfigRow(row),
            },
          ];
          return renderTableOperationCell(actions.filter((a) => a.perm != null && hasAuth(a.perm)));
        },
      },
    ]),
  },
});

// ══════════════════ 邮件模板 Tab ════════════════════

type TemplateSearchForm = { name?: string; template_code?: string };

const templateSearchForm = ref<TemplateSearchForm>({ name: undefined, template_code: undefined });
const templateShowSearchBar = ref(true);

const templateSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "模板名称",
    key: "name",
    type: "input",
    placeholder: "请输入模板名称",
    clearable: true,
    span: 6,
  },
  {
    label: "模板编码",
    key: "template_code",
    type: "input",
    placeholder: "请输入模板编码",
    clearable: true,
    span: 6,
  },
]);

const templateTableRef = ref<{ elTableRef?: { clearSelection: () => void } } | null>(null);
const {
  selectedIds: templateSelectedIds,
  batchDeleting: templateBatchDeleting,
  onTableSelectionChange: onTemplateSelectionChange,
} = useTableSelection<EmailTemplateTable>();

const templateCreateLoading = ref(false);

const {
  columns: templateColumns,
  columnChecks: templateColumnChecks,
  data: templateData,
  loading: templateLoading,
  pagination: templatePagination,
  getData: getTemplateData,
  replaceSearchParams: replaceTemplateSearchParams,
  resetSearchParams: resetTemplateSearchParams,
  handleSizeChange: handleTemplateSizeChange,
  handleCurrentChange: handleTemplateCurrentChange,
  refreshData: refreshTemplate,
  refreshCreate: refreshTemplateCreate,
  refreshUpdate: refreshTemplateUpdate,
  refreshRemove: refreshTemplateRemove,
} = useTable({
  core: {
    apiFn: EmailAPI.listTemplate,
    apiParams: { page_no: 1, page_size: 10 },
    columnsFactory: resolveStatusColumns<EmailTemplateTable>(() => [
      { type: "selection", width: 48, fixed: "left" },
      { type: "globalIndex", width: 56, label: "序号" },
      { prop: "name", label: "模板名称", minWidth: 140, showOverflowTooltip: true },
      {
        prop: "template_code",
        label: "模板编码",
        width: 140,
        formatter: (row: EmailTemplateTable) =>
          h(FaStatusTag, { type: "info", size: "small", label: row.template_code }),
      },
      { prop: "subject", label: "邮件主题", minWidth: 200, showOverflowTooltip: true },
      {
        prop: "status",
        label: "状态",
        width: 70,
        status: {
          "0": { type: "success", size: "small", text: "正常" },
          "1": { type: "danger", size: "small", text: "禁用" },
        },
      },
      { prop: "description", label: "备注", minWidth: 120, showOverflowTooltip: true },
      {
        prop: "operation",
        label: "操作",
        width: 160,
        fixed: "right",
        align: "right",
        formatter: (row: EmailTemplateTable) => {
          const actions: TableOperationAction[] = [
            {
              key: "edit",
              label: "编辑",
              artType: "edit" as const,
              perm: "module_platform:email:update",
              run: () => openTemplateDialog("update", row),
            },
            {
              key: "delete",
              label: "删除",
              artType: "delete" as const,
              perm: "module_platform:email:update",
              run: () => deleteTemplateRow(row),
            },
          ];
          return renderTableOperationCell(actions.filter((a) => a.perm != null && hasAuth(a.perm)));
        },
      },
    ]),
  },
});

// ══════════════════ 发送日志 Tab ════════════════════

type LogSearchForm = { to_email?: string; biz_type?: string; template_code?: string };

const logSearchForm = ref<LogSearchForm>({
  to_email: undefined,
  biz_type: undefined,
  template_code: undefined,
});
const logShowSearchBar = ref(true);

const logSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "收件人",
    key: "to_email",
    type: "input",
    placeholder: "请输入邮箱",
    clearable: true,
    span: 6,
  },
  {
    label: "模板编码",
    key: "template_code",
    type: "input",
    placeholder: "请输入模板编码",
    clearable: true,
    span: 6,
  },
]);

const {
  columns: logColumns,
  columnChecks: logColumnChecks,
  data: logData,
  loading: logLoading,
  pagination: logPagination,
  getData: getLogData,
  replaceSearchParams: replaceLogSearchParams,
  resetSearchParams: resetLogSearchParams,
  handleSizeChange: handleLogSizeChange,
  handleCurrentChange: handleLogCurrentChange,
  refreshData: refreshLog,
} = useTable({
  core: {
    apiFn: EmailAPI.listLog,
    apiParams: { page_no: 1, page_size: 10 },
    columnsFactory: resolveStatusColumns<EmailLogTable>(() => [
      { type: "globalIndex", width: 56, label: "序号" },
      { prop: "to_email", label: "收件人", minWidth: 180, showOverflowTooltip: true },
      { prop: "subject", label: "主题", minWidth: 200, showOverflowTooltip: true },
      {
        prop: "template_code",
        label: "模板",
        width: 120,
        formatter: (row: EmailLogTable) =>
          row.template_code
            ? h(FaStatusTag, { type: "info", size: "small", label: row.template_code! })
            : h("span", { class: "text-g-400" }, () => "—"),
      },
      {
        prop: "biz_type",
        label: "业务类型",
        width: 110,
        formatter: (row: EmailLogTable) =>
          h(FaStatusTag, { size: "small", label: bizTypeLabel(row.biz_type) }),
      },
      {
        prop: "status",
        label: "发送状态",
        width: 90,
        status: {
          1: { type: "success", text: "成功" },
          0: { type: "danger", text: "失败" },
        },
      },
      { prop: "retry_count", label: "重试", width: 60 },
      {
        prop: "error_msg",
        label: "错误信息",
        minWidth: 160,
        showOverflowTooltip: true,
        formatter: (row: EmailLogTable) =>
          row.error_msg || h("span", { class: "text-g-400" }, () => "—"),
      },
      { prop: "created_time", label: "发送时间", width: 168, showOverflowTooltip: true },
    ]),
  },
});

// ══════════════════ SMTP 配置弹窗 ════════════════════

const { dialogVisible: configDialogVisible } = useCrudDialog();
const configFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const configSubmitting = ref(false);
const configFormRenderKey = ref(0);
const editingConfigId = ref<number | null>(null);

const configFormData = ref<EmailConfigCreateForm & { id?: number }>({
  name: "",
  smtp_host: "",
  smtp_port: 465,
  smtp_user: "",
  smtp_password: "",
  from_name: "FastapiAdmin",
  use_tls: true,
  is_default: false,
  timeout: 30,
  description: "",
});

const initialConfigForm: EmailConfigCreateForm & { id?: number } = {
  name: "",
  smtp_host: "",
  smtp_port: 465,
  smtp_user: "",
  smtp_password: "",
  from_name: "FastapiAdmin",
  use_tls: true,
  is_default: false,
  timeout: 30,
  description: "",
};

const configFormRules = {
  name: [{ required: true, message: "请输入配置名称", trigger: "blur" }],
  smtp_host: [{ required: true, message: "请输入 SMTP 服务器地址", trigger: "blur" }],
  smtp_port: [{ required: true, message: "请输入端口", trigger: "blur" }],
  smtp_user: [{ required: true, message: "请输入 SMTP 用户名", trigger: "blur" }],
};

const configDialogFormItems = computed<FormItem[]>(() => [
  {
    label: "配置名称",
    key: "name",
    type: "input",
    span: 24,
    props: { placeholder: "如：企业邮箱", maxlength: 100 },
  },
  {
    label: "SMTP 服务器",
    key: "smtp_host",
    type: "input",
    span: 24,
    props: { placeholder: "如：smtp.qq.com", maxlength: 255 },
  },
  { label: "SMTP 端口", key: "smtp_port", type: "number", span: 12, props: { min: 1, max: 65535 } },
  { label: "超时(秒)", key: "timeout", type: "number", span: 12, props: { min: 5, max: 120 } },
  {
    label: "用户名",
    key: "smtp_user",
    type: "input",
    span: 24,
    props: { placeholder: "SMTP 登录用户名", maxlength: 255 },
  },
  {
    label: "授权密码",
    key: "smtp_password",
    type: "input",
    span: 24,
    props: { type: "password", showPassword: true, placeholder: "SMTP 授权码", maxlength: 255 },
    extra: editingConfigId.value ? "留空不修改原密码" : undefined,
  },
  {
    label: "发件人名称",
    key: "from_name",
    type: "input",
    span: 24,
    props: { placeholder: "发件人显示名称", maxlength: 100 },
  },
  { label: "SSL/TLS", key: "use_tls", type: "switch", span: 12 },
  { label: "设为默认", key: "is_default", type: "switch", span: 12 },
  {
    label: "备注",
    key: "description",
    type: "textarea",
    span: 24,
    props: { rows: 2, maxlength: 255, placeholder: "可选" },
  },
]);

async function handleConfigAdd() {
  configCreateLoading.value = true;
  try {
    await openConfigDialog("create");
  } finally {
    configCreateLoading.value = false;
  }
}

async function openConfigDialog(type: "create" | "update", row?: EmailConfigTable) {
  configDialogVisible.type = type;
  editingConfigId.value = row?.id ?? null;
  if (type === "create") {
    configDialogVisible.title = "新增 SMTP 配置";
    configFormData.value = { ...initialConfigForm };
  } else if (row) {
    configDialogVisible.title = "编辑 SMTP 配置";
    const res = await EmailAPI.detailConfig(row.id!);
    Object.assign(configFormData.value, res.data.data);
    configFormData.value.smtp_password = "";
  }
  configFormRenderKey.value += 1;
  configDialogVisible.visible = true;
}

async function handleSubmitConfig() {
  const form: any = configFormRef.value;
  if (!form) return;
  const valid = await form.validate().catch(() => false);
  if (!valid) return;
  configSubmitting.value = true;
  try {
    const id = configFormData.value.id;
    if (id) {
      const body: EmailConfigUpdateForm = { ...configFormData.value };
      if (!body.smtp_password) delete body.smtp_password;
      await EmailAPI.updateConfig(id, body);
      await refreshConfigUpdate();
    } else {
      await EmailAPI.createConfig(configFormData.value);
      await refreshConfigCreate();
    }
    configDialogVisible.visible = false;
  } catch {
    /* ignore */
  } finally {
    configSubmitting.value = false;
  }
}

function handleCloseConfigDialog() {
  configDialogVisible.visible = false;
  configFormRef.value?.resetFields();
}

// ══════════════════ 邮件模板弹窗 ════════════════════

const { dialogVisible: templateDialogVisible } = useCrudDialog();
const templateFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const templateSubmitting = ref(false);
const templateFormRenderKey = ref(0);
const editingTemplateId = ref<number | null>(null);

const templateFormData = ref<EmailTemplateCreateForm & { id?: number }>({
  name: "",
  template_code: "",
  subject: "",
  body_html: "",
  body_text: "",
  variables: "",
  description: "",
});

const initialTemplateForm: EmailTemplateCreateForm & { id?: number } = {
  name: "",
  template_code: "",
  subject: "",
  body_html: "",
  body_text: "",
  variables: "",
  description: "",
};

const templateFormRules = {
  name: [{ required: true, message: "请输入模板名称", trigger: "blur" }],
  template_code: [{ required: true, message: "请输入模板编码", trigger: "blur" }],
  subject: [{ required: true, message: "请输入邮件主题", trigger: "blur" }],
  body_html: [{ required: true, message: "请输入 HTML 正文", trigger: "blur" }],
};

const templateDialogFormItems = computed<FormItem[]>(() => [
  {
    label: "模板名称",
    key: "name",
    type: "input",
    span: 24,
    props: { placeholder: "如：注册欢迎邮件", maxlength: 100 },
  },
  {
    label: "模板编码",
    key: "template_code",
    type: "input",
    span: 24,
    props: { placeholder: "如：register", maxlength: 100, disabled: !!editingTemplateId.value },
  },
  {
    label: "邮件主题",
    key: "subject",
    type: "input",
    span: 24,
    props: { placeholder: "支持 {{ variable }} 变量替换", maxlength: 255 },
  },
  {
    label: "HTML 正文",
    key: "body_html",
    type: "textarea",
    span: 24,
    props: { rows: 8, placeholder: "Jinja2 模板语法的 HTML 内容" },
  },
  {
    label: "纯文本版本",
    key: "body_text",
    type: "textarea",
    span: 24,
    props: { rows: 3, placeholder: "纯文本降级版本，可选" },
  },
  {
    label: "变量说明",
    key: "variables",
    type: "input",
    span: 24,
    props: { placeholder: 'JSON 格式，如 {"username":"用户名","link":"链接"}', maxlength: 500 },
  },
  {
    label: "备注",
    key: "description",
    type: "textarea",
    span: 24,
    props: { rows: 2, maxlength: 255, placeholder: "可选" },
  },
]);

async function handleTemplateAdd() {
  templateCreateLoading.value = true;
  try {
    await openTemplateDialog("create");
  } finally {
    templateCreateLoading.value = false;
  }
}

async function openTemplateDialog(type: "create" | "update", row?: EmailTemplateTable) {
  templateDialogVisible.type = type;
  editingTemplateId.value = row?.id ?? null;
  if (type === "create") {
    templateDialogVisible.title = "新增邮件模板";
    templateFormData.value = { ...initialTemplateForm };
  } else if (row) {
    templateDialogVisible.title = "编辑邮件模板";
    const res = await EmailAPI.detailTemplate(row.id!);
    Object.assign(templateFormData.value, res.data.data);
  }
  templateFormRenderKey.value += 1;
  templateDialogVisible.visible = true;
}

async function handleSubmitTemplate() {
  const form: any = templateFormRef.value;
  if (!form) return;
  const valid = await form.validate().catch(() => false);
  if (!valid) return;
  templateSubmitting.value = true;
  try {
    const id = templateFormData.value.id;
    if (id) {
      await EmailAPI.updateTemplate(id, templateFormData.value as EmailTemplateUpdateForm);
      await refreshTemplateUpdate();
    } else {
      await EmailAPI.createTemplate(templateFormData.value);
      await refreshTemplateCreate();
    }
    templateDialogVisible.visible = false;
  } catch {
    /* ignore */
  } finally {
    templateSubmitting.value = false;
  }
}

function handleCloseTemplateDialog() {
  templateDialogVisible.visible = false;
  templateFormRef.value?.resetFields();
}

// ══════════════════ 发送测试邮件弹窗 ════════════════════

const sendVisible = ref(false);
const sendSubmitting = ref(false);
const sendFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const sendFormData = ref({ to_email: "", to_name: "", template_code: "", biz_type: "test" });

const sendFormRules = {
  to_email: [
    { required: true, message: "请输入收件人邮箱", trigger: "blur" },
    { type: "email", message: "邮箱格式不正确", trigger: "blur" },
  ],
  template_code: [{ required: true, message: "请选择模板", trigger: "change" }],
};

const sendDialogFormItems = computed<FormItem[]>(() => [
  {
    label: "收件人邮箱",
    key: "to_email",
    type: "input",
    span: 24,
    props: { placeholder: "test@example.com" },
  },
  {
    label: "收件人姓名",
    key: "to_name",
    type: "input",
    span: 24,
    props: { placeholder: "可选", maxlength: 100 },
  },
  {
    label: "模板编码",
    key: "template_code",
    type: "select",
    span: 24,
    props: {
      placeholder: "请选择邮件模板",
      options:
        templateData.value?.map((t: EmailTemplateTable) => ({
          label: `${t.name} (${t.template_code})`,
          value: t.template_code,
        })) ?? [],
    },
  },
  {
    label: "业务类型",
    key: "biz_type",
    type: "input",
    span: 24,
    props: { placeholder: "如：test", maxlength: 50 },
  },
]);

async function handleSubmitSend() {
  const form: any = sendFormRef.value;
  if (!form) return;
  const valid = await form.validate().catch(() => false);
  if (!valid) return;
  sendSubmitting.value = true;
  try {
    await EmailAPI.sendEmail(sendFormData.value);
    ElMessage.success("发送成功");
    sendVisible.value = false;
  } catch {
    /* ignore */
  } finally {
    sendSubmitting.value = false;
  }
}

function handleCloseSendDialog() {
  sendVisible.value = false;
}

// ══════════════════ 测试连接弹窗 ════════════════════

const testVisible = ref(false);
const testSubmitting = ref(false);
const testFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const testFormData = ref({ config_id: 0, to_email: "", config_name: "" });
const testFormRules = {
  to_email: [
    { required: true, message: "请输入测试收件人邮箱", trigger: "blur" },
    { type: "email", message: "邮箱格式不正确", trigger: "blur" },
  ],
};

const testDialogFormItems = computed<FormItem[]>(() => [
  { label: "SMTP 配置", key: "config_name", type: "input", span: 24, props: { disabled: true } },
  {
    label: "测试收件人",
    key: "to_email",
    type: "input",
    span: 24,
    props: { placeholder: "输入接收测试邮件的邮箱" },
  },
]);

function openTestDialog(row: EmailConfigTable) {
  testFormData.value = { config_id: row.id ?? 0, to_email: "", config_name: row.name };
  testVisible.value = true;
}

async function handleSubmitTest() {
  const form: any = testFormRef.value;
  if (!form) return;
  const valid = await form.validate().catch(() => false);
  if (!valid) return;
  testSubmitting.value = true;
  try {
    await EmailAPI.testConfig({
      config_id: testFormData.value.config_id,
      to_email: testFormData.value.to_email,
    });
    ElMessage.success("测试邮件已发送");
    testVisible.value = false;
  } catch {
    /* ignore */
  } finally {
    testSubmitting.value = false;
  }
}

function handleCloseTestDialog() {
  testVisible.value = false;
}

// ══════════════════ 删除操作 ════════════════════

async function deleteConfigRow(row: EmailConfigTable) {
  if (!row.id) return;
  try {
    await confirmDelete(`确定删除配置「${row.name}」？`);
    await EmailAPI.deleteConfig([row.id]);
    configTableRef.value?.elTableRef?.clearSelection();
    await refreshConfigRemove();
  } catch {
    /* 取消 */
  }
}
async function handleConfigBatchDelete() {
  if (configSelectedIds.value.length === 0) return;
  try {
    await confirmBatchDelete(configSelectedIds.value.length);
    configBatchDeleting.value = true;
    await EmailAPI.deleteConfig(configSelectedIds.value);
    configTableRef.value?.elTableRef?.clearSelection();
    await refreshConfigRemove();
  } catch {
    /* 取消 */
  } finally {
    configBatchDeleting.value = false;
  }
}

async function deleteTemplateRow(row: EmailTemplateTable) {
  if (!row.id) return;
  try {
    await confirmDelete(`确定删除模板「${row.name}」？`);
    await EmailAPI.deleteTemplate([row.id]);
    templateTableRef.value?.elTableRef?.clearSelection();
    await refreshTemplateRemove();
  } catch {
    /* 取消 */
  }
}
async function handleTemplateBatchDelete() {
  if (templateSelectedIds.value.length === 0) return;
  try {
    await confirmBatchDelete(templateSelectedIds.value.length);
    templateBatchDeleting.value = true;
    await EmailAPI.deleteTemplate(templateSelectedIds.value);
    templateTableRef.value?.elTableRef?.clearSelection();
    await refreshTemplateRemove();
  } catch {
    /* 取消 */
  } finally {
    templateBatchDeleting.value = false;
  }
}

// ══════════════════ 搜索逻辑 ════════════════════

async function handleConfigSearch(p: ConfigSearchForm) {
  replaceConfigSearchParams({ name: p.name || undefined } as unknown as ConfigSearchForm);
  getConfigData();
}
function onConfigResetSearch() {
  configSearchForm.value = { name: undefined };
  void resetConfigSearchParams();
}

async function handleTemplateSearch(p: TemplateSearchForm) {
  replaceTemplateSearchParams({
    name: p.name || undefined,
    template_code: p.template_code || undefined,
  } as unknown as TemplateSearchForm);
  getTemplateData();
}
function onTemplateResetSearch() {
  templateSearchForm.value = { name: undefined, template_code: undefined };
  void resetTemplateSearchParams();
}

async function handleLogSearch(p: LogSearchForm) {
  replaceLogSearchParams({
    to_email: p.to_email || undefined,
    template_code: p.template_code || undefined,
  } as unknown as LogSearchForm);
  getLogData();
}
function onLogResetSearch() {
  logSearchForm.value = { to_email: undefined, template_code: undefined };
  void resetLogSearchParams();
}

// ══════════════════ Tab 切换 ════════════════════

function onTabChange(tab: string | number) {
  if (tab === "config") getConfigData();
  else if (tab === "template") getTemplateData();
  else if (tab === "log") getLogData();
}

// ══════════════════ 工具函数 ════════════════════

function bizTypeLabel(type: string): string {
  const map: Record<string, string> = {
    register: "注册",
    reset_password: "重置密码",
    invite: "邀请",
    expiry_warning: "到期提醒",
    ticket_reply: "工单回复",
    package_change: "套餐变更",
    invoice_issued: "发票开具",
    other: "其他",
    test: "测试",
  };
  return map[type] || type;
}
</script>

<style scoped lang="scss">
:deep(.el-tabs) {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
}

:deep(.el-tabs__content) {
  flex: 1;
  min-height: 0;
  overflow: visible;
}

:deep(.el-tab-pane) {
  display: flex;
  flex-direction: column;
  height: 100%;
}
</style>
