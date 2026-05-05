<!-- 我的应用管理：Art + useTable（卡片网格） -->
<template>
  <div class="art-full-height portal-application-page flex flex-col min-h-0">
    <ArtSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="portalSearchItems"
      :rules="searchBarRules"
      :is-expand="false"
      :show-expand="true"
      :show-reset="true"
      :show-search="true"
      :disabled-search="false"
      :default-expanded="false"
      @search="handleSearchBarSearch"
      @reset="onResetSearch"
    >
      <template #created_id>
        <UserTableSelect
          :model-value="searchForm.created_id == null ? undefined : searchForm.created_id"
          @update:model-value="(v: number | undefined) => (searchForm.created_id = v)"
          @confirm-click="afterUserSelectSearch"
          @clear-click="afterUserSelectSearch"
        />
      </template>
      <template #updated_id>
        <UserTableSelect
          :model-value="searchForm.updated_id == null ? undefined : searchForm.updated_id"
          @update:model-value="(v: number | undefined) => (searchForm.updated_id = v)"
          @confirm-click="afterUserSelectSearch"
          @clear-click="afterUserSelectSearch"
        />
      </template>
    </ArtSearchBar>

    <ElCard
      class="flex flex-1 min-h-0 flex-col art-table-card"
      :style="{ 'margin-top': showSearchBar ? '12px' : '0' }"
    >
      <ArtTableHeader
        v-model:columns="columnChecks"
        v-model:showSearchBar="showSearchBar"
        layout="search,refresh"
        :loading="loading"
        @refresh="refreshData"
      >
        <template #left>
          <div class="flex flex-wrap items-center gap-3">
            <span class="market-title">应用市场</span>
            <ElButton
              v-hasPerm="['module_application:portal:create']"
              type="primary"
              :icon="Plus"
              @click="handleCreateApp"
            >
              创建应用
            </ElButton>
          </div>
        </template>
      </ArtTableHeader>

      <div v-loading="loading" class="app-grid-container min-h-0 flex-1 overflow-auto">
        <div v-if="!loading && data.length === 0" class="app-grid-empty">
          <ElEmpty :image-size="88" description="暂无应用" />
        </div>
        <div v-else class="grid-wrapper">
          <div
            v-for="app in data"
            :key="app.id"
            class="app-grid-item"
            @click="app.status && app.id && openAppInternal()"
          >
            <ElCard shadow="never" class="app-card" :class="{ 'card-disabled': !app.status }">
              <template #header>
                <div class="app-info-header">
                  <ElAvatar :size="40" :src="app.icon_url">
                    <ElIcon :size="20"><Monitor /></ElIcon>
                  </ElAvatar>
                  <h3 class="app-name" :title="app.name">{{ app.name }}</h3>
                  <ElTag
                    :type="app.status ? 'success' : 'info'"
                    size="small"
                    effect="plain"
                    class="app-status"
                  >
                    {{ app.status ? "启用" : "停用" }}
                  </ElTag>
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
                    <ElButton
                      v-hasPerm="['module_application:portal:update']"
                      type="primary"
                      link
                      :icon="Edit"
                      @click="handleAppAction('edit', app)"
                    />
                    <ElButton
                      v-hasPerm="['module_application:portal:delete']"
                      type="danger"
                      link
                      :icon="Delete"
                      @click="handleAppAction('delete', app)"
                    />
                  </div>
                </div>
              </template>
            </ElCard>
          </div>
        </div>
      </div>

      <div class="portal-pagination flex shrink-0 justify-end border-g-200 pt-3 mt-auto border-t">
        <ElPagination
          background
          :current-page="paginationBind.current"
          :page-size="paginationBind.size"
          :total="paginationBind.total"
          :page-sizes="[12, 24, 48]"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </ElCard>

    <ArtDrawer
      v-model="dialogVisible"
      :title="dialogTitle"
      :size="drawerSize"
      direction="rtl"
      @close="handleCloseDialog"
    >
      <ElForm
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="100px"
        label-position="right"
      >
        <ElFormItem label="应用名称" prop="name">
          <ElInput v-model="formData.name" placeholder="请输入应用名称" />
        </ElFormItem>

        <ElFormItem label="访问地址" prop="access_url">
          <ElInput v-model="formData.access_url" placeholder="请输入访问地址" />
        </ElFormItem>

        <ElFormItem label="图标地址" prop="icon_url">
          <ElInput v-model="formData.icon_url" placeholder="请输入图标地址" />
        </ElFormItem>

        <ElFormItem label="应用状态" prop="status">
          <ElRadioGroup v-model="formData.status">
            <ElRadio value="0">启用</ElRadio>
            <ElRadio value="1">停用</ElRadio>
          </ElRadioGroup>
        </ElFormItem>

        <ElFormItem label="应用描述" prop="description">
          <ElInput
            v-model="formData.description"
            type="textarea"
            :rows="4"
            placeholder="请输入应用描述"
            maxlength="200"
            show-word-limit
          />
        </ElFormItem>
      </ElForm>

      <template #footer>
        <div class="dialog-footer">
          <ElButton @click="handleCloseDialog">取消</ElButton>
          <ElButton type="primary" @click="handleSubmit">确定</ElButton>
        </div>
      </template>
    </ArtDrawer>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "PortalApplication",
  inheritAttrs: false,
});

import { computed, nextTick, reactive, ref } from "vue";
import { Delete, Edit, Monitor, Plus } from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { useAppStore } from "@/store/modules/app.store";
import { DeviceEnum } from "@/enums/settings/device.enum";
import ApplicationAPI, {
  type ApplicationForm,
  type ApplicationInfo,
} from "@/api/module_application/portal";
import { formatToDateTime } from "@/utils/common/dateUtil";
import { useTable } from "@/hooks/core/useTable";
import ArtTableHeader from "@/components/Core/tables/art-table-header/index.vue";
import ArtSearchBar from "@/components/Core/forms/art-search-bar/index.vue";
import type { SearchFormItem } from "@/components/Core/forms/art-search-bar/index.vue";
import ArtDrawer from "@/components/Core/modal/art-drawer/index.vue";
import UserTableSelect from "@/views/module_system/user/components/UserTableSelect.vue";
import type { ColumnOption } from "@/types/component";

const appStore = useAppStore();

type PortalSearchForm = {
  name?: string;
  status?: string;
  created_id?: number;
  updated_id?: number;
};

function buildPortalReplaceParams(u: PortalSearchForm): Record<string, unknown> {
  return {
    name: u.name,
    status: u.status,
    created_id: u.created_id,
    updated_id: u.updated_id,
  };
}

const searchForm = ref<PortalSearchForm>({
  name: undefined,
  status: undefined,
  created_id: undefined,
  updated_id: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof ArtSearchBar> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const statusOptions = ref([
  { label: "启用", value: "0" },
  { label: "停用", value: "1" },
]);

const portalSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "应用名称",
    key: "name",
    type: "input",
    placeholder: "请输入应用名称",
    clearable: true,
    span: 6,
  },
  {
    label: "状态",
    key: "status",
    type: "select",
    props: {
      placeholder: "请选择状态",
      options: statusOptions.value,
      clearable: true,
    },
    span: 6,
  },
  {
    label: "创建人",
    key: "created_id",
    type: "input",
    span: 6,
  },
  {
    label: "更新人",
    key: "updated_id",
    type: "input",
    span: 6,
  },
]);

const formRef = ref();
const dialogVisible = ref(false);
const dialogType = ref<"create" | "edit">("create");
const currentApp = ref<ApplicationInfo | null>(null);

const {
  columnChecks,
  data,
  loading,
  pagination,
  getData,
  replaceSearchParams,
  resetSearchParams,
  handleSizeChange,
  handleCurrentChange,
  refreshData,
  refreshCreate,
  refreshUpdate,
} = useTable({
  core: {
    apiFn: ApplicationAPI.listApp,
    apiParams: {
      page_no: 1,
      page_size: 10,
    },
    columnsFactory: (): ColumnOption<ApplicationInfo>[] => [],
  },
});

const paginationBind = computed(() => {
  const p = pagination as unknown as {
    current?: number;
    size?: number;
    total?: number;
    page_no?: number;
    page_size?: number;
  };
  return {
    current: p.current ?? p.page_no ?? 1,
    size: p.size ?? p.page_size ?? 12,
    total: p.total ?? 0,
  };
});

const formData = reactive<ApplicationForm>({
  name: "",
  access_url: "",
  icon_url: "",
  status: "0",
  description: "",
});

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

const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "500px" : "90%"));
const dialogTitle = computed(() => (dialogType.value === "create" ? "创建应用" : "编辑应用"));

const formatTime = (time: string | undefined) => {
  if (!time) return "—";
  return formatToDateTime(time, "YYYY-MM-DD HH:mm:ss");
};

async function handleSearchBarSearch(params: PortalSearchForm) {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildPortalReplaceParams(params));
  getData();
}

async function applyPortalSearchFromForm() {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildPortalReplaceParams(searchForm.value));
  getData();
}

async function afterUserSelectSearch() {
  await nextTick();
  await applyPortalSearchFromForm();
}

async function onResetSearch() {
  searchForm.value = {
    name: undefined,
    status: undefined,
    created_id: undefined,
    updated_id: undefined,
  };
  await resetSearchParams();
}

function handleCreateApp() {
  dialogType.value = "create";
  resetForm();
  dialogVisible.value = true;
}

function handleEditApp(app: ApplicationInfo) {
  dialogType.value = "edit";
  currentApp.value = app;
  Object.assign(formData, app);
  dialogVisible.value = true;
}

async function handleDeleteApp(app: ApplicationInfo) {
  try {
    await ElMessageBox.confirm("确认删除该应用？", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });

    await ApplicationAPI.deleteApp([app.id!]);
    await refreshData();
  } catch (error) {
    if (error !== "cancel") {
      console.error("删除应用失败:", error);
    }
  }
}

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

function openAppInternal() {
  ElMessage.warning("插件应用点击，业务场景暂时开放中。。。");
}

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

function handleCloseDialog() {
  dialogVisible.value = false;
  resetForm();
}

async function handleSubmit() {
  try {
    await formRef.value?.validate();

    if (dialogType.value === "create") {
      await ApplicationAPI.createApp(formData);
      await refreshCreate();
    } else {
      await ApplicationAPI.updateApp(currentApp.value!.id!, formData);
      await refreshUpdate();
    }

    dialogVisible.value = false;
    resetForm();
  } catch (error) {
    console.error("提交失败:", error);
  }
}
</script>

<style lang="scss" scoped>
.market-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.app-grid-container {
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
