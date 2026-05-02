<!-- 我的应用管理 -->
<template>
  <div class="app-container">
    <PageSearch
      ref="searchRef"
      :search-config="searchConfig"
      @query-click="handleQueryClick"
      @reset-click="handleResetClick"
    />

    <PageContent ref="contentRef" class="flex-1 min-h-0" :content-config="contentConfig">
      <template #header>
        <div class="card-header">
          <span class="market-title">应用市场</span>
          <el-button
            v-hasPerm="['module_application:portal:create']"
            type="primary"
            icon="plus"
            @click="handleCreateApp"
          >
            创建应用
          </el-button>
        </div>
      </template>

      <template #table="{ data, loading }">
        <div v-loading="loading" class="app-grid-container">
          <div v-if="!loading && data.length === 0" class="app-grid-empty">
            <el-empty :image-size="88" description="暂无应用" />
          </div>
          <div v-else class="grid-wrapper">
            <div
              v-for="app in data"
              :key="app.id"
              class="app-grid-item"
              @click="app.status && app.id && openAppInternal()"
            >
              <el-card shadow="never" class="app-card" :class="{ 'card-disabled': !app.status }">
                <template #header>
                  <div class="app-info-header">
                    <el-avatar :size="40" :src="app.icon_url">
                      <el-icon size="20"><Monitor /></el-icon>
                    </el-avatar>
                    <h3 class="app-name" :title="app.name">{{ app.name }}</h3>
                    <el-tag
                      :type="app.status ? 'success' : 'info'"
                      size="small"
                      effect="plain"
                      class="app-status"
                    >
                      {{ app.status ? "启用" : "停用" }}
                    </el-tag>
                  </div>
                </template>

                <template #default>
                  <p v-if="app.description" class="app-description">{{ app.description }}</p>
                </template>

                <template #footer>
                  <div class="card-footer-row">
                    <div class="card-meta">
                      {{ app.created_by?.name || "—" }} · {{ formatTime(app.created_time) }}
                    </div>
                    <div class="card-actions" @click.stop>
                      <el-button
                        v-hasPerm="['module_application:portal:update']"
                        type="primary"
                        link
                        icon="Edit"
                        @click="handleAppAction('edit', app)"
                      />
                      <el-button
                        v-hasPerm="['module_application:portal:delete']"
                        type="danger"
                        link
                        icon="Delete"
                        @click="handleAppAction('delete', app)"
                      />
                    </div>
                  </div>
                </template>
              </el-card>
            </div>
          </div>
        </div>
      </template>
    </PageContent>

    <!-- 应用创建/编辑抽屉 -->
    <EnhancedDrawer
      v-model="dialogVisible"
      :title="dialogTitle"
      :size="drawerSize"
      direction="rtl"
      @close="handleCloseDialog"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="100px"
        label-position="right"
      >
        <el-form-item label="应用名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入应用名称" />
        </el-form-item>

        <el-form-item label="访问地址" prop="access_url">
          <el-input v-model="formData.access_url" placeholder="请输入访问地址" />
        </el-form-item>

        <el-form-item label="图标地址" prop="icon_url">
          <el-input v-model="formData.icon_url" placeholder="请输入图标地址" />
        </el-form-item>

        <el-form-item label="应用状态" prop="status">
          <el-radio-group v-model="formData.status">
            <el-radio value="0">启用</el-radio>
            <el-radio value="1">停用</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="应用描述" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="4"
            placeholder="请输入应用描述"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleCloseDialog">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </div>
      </template>
    </EnhancedDrawer>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "PortalApplication",
  inheritAttrs: false,
});

import { useAppStore } from "@/store/modules/app.store";
import { DeviceEnum } from "@/enums/settings/device.enum";
import { Monitor } from "@element-plus/icons-vue";
import ApplicationAPI, {
  type ApplicationForm,
  type ApplicationInfo,
  type ApplicationPageQuery,
} from "@/api/module_application/portal";
import { formatToDateTime } from "@/utils/dateUtil";
import PageSearch from "@/components/CURD/PageSearch.vue";
import PageContent from "@/components/CURD/PageContent.vue";
import EnhancedDrawer from "@/components/CURD/EnhancedDrawer.vue";
import UserTableSelect from "@/views/module_system/user/components/UserTableSelect.vue";
import type { IContentConfig, ISearchConfig } from "@/components/CURD/types";
import { useCrudList } from "@/components/CURD/useCrudList";
import { computed, markRaw, nextTick, reactive, ref } from "vue";

const appStore = useAppStore();

const { searchRef, contentRef, handleQueryClick, handleResetClick, refreshList } = useCrudList();
const formRef = ref();
const dialogVisible = ref(false);
const dialogType = ref<"create" | "edit">("create");
const currentApp = ref<ApplicationInfo | null>(null);

function triggerUserSearch() {
  nextTick(() => refreshList());
}

const searchConfig = reactive<ISearchConfig>({
  permPrefix: "module_application:portal",
  colon: true,
  isExpandable: true,
  showNumber: 2,
  form: { labelWidth: "auto" },
  formItems: [
    {
      prop: "name",
      label: "应用名称",
      type: "input",
      attrs: { placeholder: "请输入应用名称", clearable: true },
    },
    {
      prop: "status",
      label: "状态",
      type: "select",
      options: [
        { label: "启用", value: true },
        { label: "停用", value: false },
      ],
      attrs: { placeholder: "请选择状态", clearable: true, style: { width: "170px" } },
    },
    {
      prop: "created_id",
      label: "创建人",
      type: "user-table-select",
      initialValue: null,
      events: {
        "confirm-click": triggerUserSearch,
        "clear-click": triggerUserSearch,
      },
    },
    {
      prop: "updated_id",
      label: "更新人",
      type: "user-table-select",
      initialValue: null,
      events: {
        "confirm-click": triggerUserSearch,
        "clear-click": triggerUserSearch,
      },
    },
  ],
  customComponents: {
    "user-table-select": markRaw(UserTableSelect),
  },
});

const contentConfig = reactive<IContentConfig<ApplicationPageQuery>>({
  permPrefix: "module_application:portal",
  cols: [],
  hideColumnFilter: true,
  showToolbar: false,
  cardShadow: "hover",
  toolbar: [],
  defaultToolbar: [],
  pagination: {
    pageSize: 12,
    pageSizes: [12, 24, 48],
  },
  request: { page_no: "page_no", page_size: "page_size" },
  indexAction: async (params) => {
    const res = await ApplicationAPI.listApp(params as ApplicationPageQuery);
    return {
      total: res.data.data.total,
      list: res.data.data.items,
    };
  },
});

// 表单数据
const formData = reactive<ApplicationForm>({
  name: "",
  access_url: "",
  icon_url: "",
  status: "0",
  description: "",
});

// 表单验证规则
const formRules = reactive({
  name: [
    { required: true, message: "请输入应用名称", trigger: "blur" },
    { min: 2, max: 30, message: "长度在 2 到 30 个字符", trigger: "blur" },
  ],
  access_url: [
    { required: true, message: "请输入访问地址", trigger: "blur" },
    { type: "url" as const, message: "请输入正确的URL格式", trigger: "blur" },
  ],
  icon_url: [
    { required: true, message: "请输入图标地址", trigger: "blur" },
    { type: "url" as const, message: "请输入正确的URL格式", trigger: "blur" },
  ],
  status: [{ required: true, message: "请选择应用状态", trigger: "change" }],
});

// 计算属性
const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "500px" : "90%"));
const dialogTitle = computed(() => (dialogType.value === "create" ? "创建应用" : "编辑应用"));

// 格式化时间
const formatTime = (time: string | undefined) => {
  if (!time) return "—";
  return formatToDateTime(time, "YYYY-MM-DD HH:mm:ss");
};

// 创建应用
function handleCreateApp() {
  dialogType.value = "create";
  resetForm();
  dialogVisible.value = true;
}

// 编辑应用
function handleEditApp(app: ApplicationInfo) {
  dialogType.value = "edit";
  currentApp.value = app;
  Object.assign(formData, app);
  dialogVisible.value = true;
}

// 删除应用
async function handleDeleteApp(app: ApplicationInfo) {
  try {
    await ElMessageBox.confirm("确认删除该应用？", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });

    await ApplicationAPI.deleteApp([app.id!]);
    await refreshList();
  } catch (error) {
    if (error !== "cancel") {
      console.error("删除应用失败:", error);
    }
  }
}

// 应用操作
async function handleAppAction(command: string, app: ApplicationInfo) {
  switch (command) {
    case "edit":
      handleEditApp(app);
      break;
    case "delete":
      await handleDeleteApp(app);
      break;
  }
}

// 内部打开应用
function openAppInternal() {
  ElMessage.warning("插件应用点击，业务场景暂时开放中。。。");
  return;
}

// 重置表单
function resetForm() {
  Object.assign(formData, {
    name: "",
    access_url: "",
    icon_url: "",
    status: "0",
    description: "",
  });
  formRef.value?.resetFields();
}

// 关闭弹窗
function handleCloseDialog() {
  dialogVisible.value = false;
  resetForm();
}

// 提交表单
async function handleSubmit() {
  try {
    await formRef.value?.validate();

    if (dialogType.value === "create") {
      await ApplicationAPI.createApp(formData);
    } else {
      await ApplicationAPI.updateApp(currentApp.value!.id!, formData);
    }

    dialogVisible.value = false;
    resetForm();
    await refreshList();
  } catch (error) {
    console.error("提交失败:", error);
  }
}
</script>

<style lang="scss" scoped>
/* 高度交给外层 flex：app-container + PageContent(flex-1 min-h-0)，勿再用 100vh 计算，否则会超出 app-main、底部 padding 不显 */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.market-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.app-grid-container {
  flex: 1;
  min-height: 200px;
}

.app-grid-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 220px;
}

.grid-wrapper {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.app-grid-item {
  min-width: 0;
}

.app-card {
  display: flex;
  flex: 1;
  flex-direction: column;
  height: 100%;
  min-height: 120px;
  cursor: pointer;
  transition: box-shadow 0.2s ease;

  &:hover:not(.card-disabled) {
    box-shadow: var(--el-box-shadow-light);
  }

  &.card-disabled {
    cursor: not-allowed;
    opacity: 0.55;
  }

  /* 仅保留底栏一条横线，避免与表头下边框重复成「双线」 */
  :deep(.el-card__header) {
    padding: 14px 14px 12px;
    border-bottom: none;
  }

  :deep(.el-card__body) {
    display: flex;
    flex: 1;
    flex-direction: column;
    justify-content: center;
    min-height: 0;
    padding: 12px 14px;
  }

  :deep(.el-card__footer) {
    padding: 10px 14px 14px;
    margin-top: auto;
  }
}

.app-info-header {
  display: flex;
  gap: 12px;
  align-items: center;
  min-width: 0;
}

.app-name {
  flex: 1;
  min-width: 0;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 15px;
  font-weight: 600;
  white-space: nowrap;
}

.app-status {
  flex-shrink: 0;
}

.card-footer-row {
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
  min-height: 28px;
}

.card-actions {
  display: inline-flex;
  flex-shrink: 0;
  gap: 0;
  align-items: center;
}

.app-description {
  display: -webkit-box;
  margin: 0;
  overflow: hidden;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  font-size: 13px;
  line-height: 1.55;
  color: var(--el-text-color-secondary);
  -webkit-box-orient: vertical;
}

.card-meta {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 12px;
  line-height: 1.4;
  color: var(--el-text-color-placeholder);
  white-space: nowrap;
}

@media (width <= 480px) {
  .grid-wrapper {
    grid-template-columns: 1fr;
  }

  .card-footer-row {
    flex-wrap: wrap;
    gap: 8px;
    min-height: 0;
  }

  .card-meta {
    flex: 1 1 100%;
    word-break: break-all;
    white-space: normal;
  }

  .card-actions {
    margin-left: auto;
  }
}
</style>
