<!-- 插件市场：卡片展示 + 搜索筛选 -->
<template>
  <div class="fa-full-height">
    <FaSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="pluginSearchItems"
      :is-expand="false"
      :show-expand="true"
      :show-reset="true"
      :show-search="true"
      :disabled-search="false"
      :default-expanded="false"
      @search="handleSearchBarSearch"
      @reset="onResetSearch"
    />

    <ElCard
      shadow="hover"
      class="fa-table-card"
      :style="{ 'margin-top': showSearchBar ? '12px' : '0' }"
    >
      <FaTableHeader
        v-model:columns="columnChecks"
        v-model:showSearchBar="showSearchBar"
        :loading="loading"
        layout="search,refresh"
        @refresh="fetchData"
      >
        <template #left>
          <ElButton
            v-if="hasAuth('module_platform:plugin:create')"
            type="primary"
            @click="handleOpenDialog('create')"
          >
            <ElIcon><Plus /></ElIcon>
            新增插件
          </ElButton>
        </template>
      </FaTableHeader>

      <!-- 加载 -->
      <ElSkeleton v-if="loading && !data.length" :rows="4" animated style="margin-top: 16px">
        <template #template>
          <div
            style="
              display: grid;
              grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
              gap: 16px;
            "
          >
            <div v-for="i in 6" :key="i" style="height: 260px">
              <ElSkeletonItem
                variant="rect"
                style="width: 100%; height: 100%; border-radius: var(--custom-radius)"
              />
            </div>
          </div>
        </template>
      </ElSkeleton>

      <!-- 卡片网格 -->
      <ElScrollbar v-else-if="data.length" class="plugin-scroll">
        <div class="plugin-grid">
          <div
            v-for="item in data"
            :key="item.id"
            class="plugin-card fa-card"
            :class="{ 'is-installed': item.installed }"
          >
            <!-- 头部：图标 + 名称 + 状态徽章 -->
            <div class="card-header">
              <span class="card-icon" :class="categoryIconBg(item.category)">
                <FaSvgIcon :icon="item.icon || 'ri:plug-2-line'" />
              </span>
              <div class="card-title-group">
                <span class="card-title">{{ item.name }}</span>
                <span class="card-badge" :class="item.status === 0 ? 'badge-on' : 'badge-off'">
                  {{ item.status === 0 ? "启用" : "停用" }}
                </span>
              </div>
            </div>

            <!-- 描述 -->
            <p class="card-desc">{{ item.description || "暂无描述" }}</p>

            <!-- 标签行 -->
            <div class="card-tags">
              <ElTag size="small" effect="plain" :type="categoryTagType(item.category)">
                {{ categoryLabel(item.category) }}
              </ElTag>
              <span class="tag-version">v{{ item.version || "1.0.0" }}</span>
              <ElTag v-if="item.price === 0" size="small" effect="plain" type="success">免费</ElTag>
              <ElTag v-else size="small" effect="plain" type="warning">
                ¥{{ ((item.price ?? 0) / 100).toFixed(2) }}
              </ElTag>
            </div>

            <!-- 底部 -->
            <div class="card-footer">
              <span class="footer-author">
                <FaSvgIcon icon="ri:user-3-line" />{{ item.author || "—" }}
              </span>
              <div class="footer-actions">
                <ElButton
                  size="small"
                  link
                  type="primary"
                  @click="handleOpenDialog('detail', item.id!)"
                >
                  详情
                </ElButton>
                <ElButton
                  v-if="hasAuth('module_platform:plugin:install') && !item.installed"
                  size="small"
                  type="primary"
                  @click="doInstall(item)"
                >
                  安装
                </ElButton>
                <ElDropdown v-if="showMore(item)" trigger="click">
                  <ElButton size="small" link type="primary" class="more-btn">
                    <ElIcon><MoreFilled /></ElIcon>
                  </ElButton>
                  <template #dropdown>
                    <ElDropdownMenu>
                      <ElDropdownItem
                        v-if="hasAuth('module_platform:plugin:update')"
                        @click="handleOpenDialog('update', item.id!)"
                      >
                        <ElIcon><Edit /></ElIcon>编辑
                      </ElDropdownItem>
                      <ElDropdownItem
                        v-if="hasAuth('module_platform:plugin:install') && item.installed"
                        @click="doToggle(item)"
                      >
                        <ElIcon>
                          <FaSvgIcon
                            :icon="
                              item.status === 0 ? 'ri:forbid-2-line' : 'ri:checkbox-circle-line'
                            "
                          />
                        </ElIcon>
                        {{ item.status === 0 ? "禁用" : "启用" }}
                      </ElDropdownItem>
                      <ElDropdownItem
                        v-if="hasAuth('module_platform:plugin:install') && item.installed"
                        @click="doUninstall(item)"
                        divided
                      >
                        <ElIcon><Delete /></ElIcon>卸载
                      </ElDropdownItem>
                      <ElDropdownItem
                        v-if="hasAuth('module_platform:plugin:delete')"
                        divided
                        @click="deletePluginRow(item.id!)"
                      >
                        <ElIcon><Delete /></ElIcon>删除
                      </ElDropdownItem>
                    </ElDropdownMenu>
                  </template>
                </ElDropdown>
              </div>
            </div>
          </div>
        </div>
      </ElScrollbar>

      <ElEmpty v-else-if="!loading" description="暂无插件" style="margin-top: 40px" />

      <!-- 分页 -->
      <div v-if="total > 0" class="plugin-pagination">
        <FaPagination
          :page="pageNo"
          :limit="pageSize"
          :total="total"
          :page-sizes="[12, 24, 48]"
          :disabled="loading"
          @pagination="onPaginationChange"
        />
      </div>
    </ElCard>

    <!-- ─── 对话框 ─── -->
    <FaDialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      width="720px"
      dialog-class="crud-embed-dialog"
      modal-class="crud-embed-dialog"
      :form-mode="dialogVisible.type"
      :confirm-loading="submitLoading"
      @cancel="handleCloseDialog"
      @confirm="dialogVisible.type === 'detail' ? handleCloseDialog() : handleSubmit()"
    >
      <template v-if="dialogVisible.type === 'detail'">
        <FaDescriptions
          :column="2"
          :data="detailFormData"
          :items="pluginDetailItems"
          max-height="75vh"
        >
          <template #status>
            <ElTag :type="detailFormData.status === 0 ? 'success' : 'danger'">
              {{ detailFormData.status === 0 ? "启用" : "停用" }}
            </ElTag>
          </template>
          <template #price>
            {{
              detailFormData.price === 0
                ? "免费"
                : "¥" + ((detailFormData.price ?? 0) / 100).toFixed(2)
            }}
          </template>
        </FaDescriptions>
      </template>
      <template v-else>
        <FaForm
          scrollbar
          max-height="75vh"
          :key="pluginFormRenderKey"
          ref="dataFormRef"
          v-model="formData"
          :items="pluginDialogFormItems"
          :rules="rules"
          label-suffix=":"
          :label-width="100"
          label-position="right"
          :span="24"
          :gutter="16"
          :show-reset="false"
          :show-submit="false"
          class="crud-dialog-art-form"
        >
          <template #status>
            <ElRadioGroup v-model="formData.status">
              <ElRadio :value="0">启用</ElRadio>
              <ElRadio :value="1">停用</ElRadio>
            </ElRadioGroup>
          </template>
        </FaForm>
      </template>
    </FaDialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useCrudDialog } from "@/hooks/core/useCrudDialog";
import { useCrudForm } from "@/hooks/core/useCrudForm";
import { confirmDelete } from "@/hooks/core/useConfirm";
import PluginAPI, { type PluginForm, type PluginTable } from "@/api/module_platform/plugin";
import { useAuth } from "@/hooks/core/useAuth";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import {
  ElTag,
  ElMessage,
  ElButton,
  ElIcon,
  ElDropdown,
  ElDropdownMenu,
  ElDropdownItem,
} from "element-plus";
import { Plus, Edit, Delete, MoreFilled } from "@element-plus/icons-vue";

defineOptions({
  name: "PluginMarketplace",
  inheritAttrs: false,
});

const { hasAuth } = useAuth();

// ─── 搜索表单 ───
const searchForm = ref<{ name?: string; category?: string; status?: number }>({
  name: "",
  category: "",
  status: undefined,
});
const showSearchBar = ref(true);

const categoryOptions = ref([
  { label: "工具", value: "tool" },
  { label: "AI", value: "ai" },
  { label: "监控", value: "monitor" },
  { label: "业务", value: "business" },
]);

const statusOptions = ref([
  { label: "启用", value: 0 },
  { label: "停用", value: 1 },
]);

const pluginSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "插件名称",
    key: "name",
    type: "input",
    placeholder: "请输入插件名称",
    clearable: true,
    span: 6,
  },
  {
    label: "分类",
    key: "category",
    type: "select",
    props: { placeholder: "请选择分类", options: categoryOptions.value, clearable: true },
    span: 6,
  },
  {
    label: "状态",
    key: "status",
    type: "select",
    props: { placeholder: "请选择状态", options: statusOptions.value, clearable: true },
    span: 6,
  },
]);

// ─── 数据管理 ───
const data = ref<PluginTable[]>([]);
const loading = ref(false);
const pageNo = ref(1);
const pageSize = ref(12);
const total = ref(0);

async function fetchData() {
  loading.value = true;
  try {
    const res = await PluginAPI.list(
      { page_no: pageNo.value, page_size: pageSize.value, ...searchForm.value }
    );
    const result = res.data?.data;
    data.value = (result?.items as PluginTable[]) || [];
    total.value = result?.total || 0;
  } catch {
    // ignore
  } finally {
    loading.value = false;
  }
}

function onPaginationChange({ page, limit }: { page: number; limit: number }) {
  pageNo.value = page;
  pageSize.value = limit;
  fetchData();
}

const columnChecks = ref([]);

async function handleSearchBarSearch(params: Record<string, unknown>) {
  searchForm.value = {
    name: (params.name as string) ?? "",
    category: (params.category as string) ?? "",
    status: params.status !== undefined ? Number(params.status) : undefined,
  };
  pageNo.value = 1;
  await fetchData();
}

async function onResetSearch() {
  searchForm.value = { name: "", category: "", status: undefined };
  pageNo.value = 1;
  await fetchData();
}

// ─── 分类辅助函数 ───
function categoryLabel(cat?: string): string {
  const map: Record<string, string> = { tool: "工具", ai: "AI", monitor: "监控", business: "业务" };
  return (cat && map[cat]) || cat || "—";
}

function categoryIconBg(cat?: string): string {
  const map: Record<string, string> = {
    tool: "icon-bg-default",
    ai: "icon-bg-warning",
    monitor: "icon-bg-success",
    business: "icon-bg-info",
  };
  return (cat && map[cat]) || "icon-bg-default";
}

function categoryTagType(cat?: string): "success" | "warning" | "info" | "danger" | undefined {
  const map: Record<string, "success" | "warning" | "info" | "danger" | undefined> = {
    tool: "info",
    ai: "warning",
    monitor: "success",
    business: undefined,
  };
  return cat ? map[cat] : "info";
}

// ─── 显示更多按钮 ───
function showMore(row: PluginTable): boolean {
  return (
    hasAuth("module_platform:plugin:update") ||
    hasAuth("module_platform:plugin:delete") ||
    (hasAuth("module_platform:plugin:install") && !!row.installed)
  );
}

// ─── 操作 ───
async function deletePluginRow(id: number) {
  try {
    await confirmDelete("确认删除该插件?");
    await PluginAPI.delete([id]);
    await fetchData();
  } catch {
    // 用户取消
  }
}

async function doInstall(row: PluginTable) {
  if (!row.id) return;
  try {
    await PluginAPI.install(row.id);
    ElMessage.success("安装成功");
    row.installed = true;
  } catch {
    ElMessage.error("安装失败");
  }
}

async function doUninstall(row: PluginTable) {
  if (!row.id) return;
  try {
    await PluginAPI.uninstall(row.id);
    ElMessage.success("卸载成功");
    row.installed = false;
  } catch {
    ElMessage.error("卸载失败");
  }
}

async function doToggle(row: PluginTable) {
  if (!row.id) return;
  try {
    await PluginAPI.toggle(row.id);
    ElMessage.success(row.status === 0 ? "已禁用" : "已启用");
    row.status = row.status === 0 ? 1 : 0;
  } catch {
    ElMessage.error("操作失败");
  }
}

// ─── 对话框 ───
const { dialogVisible } = useCrudDialog();
const detailFormData = ref<PluginTable>({} as PluginTable);

const pluginDetailItems = [
  { label: "插件名称", prop: "name" },
  { label: "插件编码", prop: "code" },
  { label: "版本", prop: "version" },
  { label: "分类", prop: "category" },
  { label: "作者", prop: "author" },
  { label: "状态", prop: "status", slot: "status" },
  { label: "价格", prop: "price", slot: "price" },
  { label: "排序", prop: "sort" },
  { label: "菜单路径", prop: "menu_path" },
  { label: "权限前缀", prop: "permission_prefix" },
  { label: "依赖插件", prop: "dependencies" },
  { label: "描述", prop: "description", span: 4 },
];

const formData = ref<PluginForm>({
  name: undefined,
  code: undefined,
  category: "tool",
  version: "1.0.0",
  status: 0,
  price: 0,
  sort: 0,
  description: undefined,
  author: undefined,
  icon: undefined,
  menu_path: undefined,
  permission_prefix: undefined,
  dependencies: undefined,
});

const initialFormData: PluginForm = { ...formData.value };
const pluginFormRenderKey = ref(0);
const dataFormRef = ref<any>(null);

const rules = {
  name: [{ required: true, message: "请输入插件名称", trigger: "blur" }],
  code: [{ required: true, message: "请输入插件编码", trigger: "blur" }],
  category: [{ required: true, message: "请选择分类", trigger: "change" }],
};

const pluginDialogFormItems: FormItem[] = [
  {
    label: "插件名称",
    key: "name",
    type: "input",
    span: 12,
    props: { placeholder: "请输入插件名称", clearable: true },
  },
  {
    label: "插件编码",
    key: "code",
    type: "input",
    span: 12,
    props: { placeholder: "请输入插件编码", clearable: true },
  },
  {
    label: "分类",
    key: "category",
    type: "select",
    span: 12,
    props: { options: categoryOptions.value, placeholder: "请选择分类", clearable: true },
  },
  {
    label: "版本",
    key: "version",
    type: "input",
    span: 12,
    props: { placeholder: "版本号", clearable: true },
  },
  {
    label: "作者",
    key: "author",
    type: "input",
    span: 12,
    props: { placeholder: "请输入作者", clearable: true },
  },
  {
    label: "图标",
    key: "icon",
    type: "input",
    span: 12,
    props: { placeholder: "iconify 图标名", clearable: true },
  },
  {
    label: "价格(分)",
    key: "price",
    type: "input-number",
    span: 12,
    props: { min: 0, placeholder: "0=免费" },
  },
  { label: "排序", key: "sort", type: "input-number", span: 12, props: { min: 0 } },
  {
    label: "菜单路径",
    key: "menu_path",
    type: "input",
    span: 12,
    props: { placeholder: "安装后的菜单路径", clearable: true },
  },
  {
    label: "权限前缀",
    key: "permission_prefix",
    type: "input",
    span: 12,
    props: { placeholder: "权限前缀", clearable: true },
  },
  {
    label: "依赖插件",
    key: "dependencies",
    type: "textarea",
    span: 24,
    props: { placeholder: "依赖插件编码(JSON数组)", rows: 2 },
  },
  {
    label: "描述",
    key: "description",
    type: "textarea",
    span: 24,
    props: { placeholder: "请输入描述", rows: 3 },
  },
];

const { submitLoading, handleCloseDialog, handleOpenDialog, handleSubmit } =
  useCrudForm<PluginForm>({
    formData,
    initialFormData,
    dialogVisible,
    dataFormRef,
    formRenderKey: pluginFormRenderKey,
    detailApi: PluginAPI.detail as unknown as (
      id: number
    ) => Promise<{ data: { data?: PluginForm } }>,
    createApi: PluginAPI.create,
    updateApi: PluginAPI.update,
    titles: { create: "新增插件", update: "编辑插件", detail: "插件详情" },
    detailFormData,
    onCreateSuccess: async () => {
      await fetchData();
    },
    onUpdateSuccess: async () => {
      await fetchData();
    },
    onSubmitSuccess: async () => {
      await fetchData();
    },
  });

onMounted(() => {
  fetchData();
});
</script>

<style scoped lang="scss">
.fa-full-height {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
}

.plugin-scroll {
  flex: 1;
  min-height: 0;
  margin-top: 16px;
}

.plugin-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
}

.plugin-card {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0;
  padding: 20px;
  overflow: hidden;
  transition:
    box-shadow 0.3s,
    transform 0.25s;

  &:hover {
    box-shadow: 0 8px 24px rgb(0 0 0 / 8%);
    transform: translateY(-3px);
  }

  &.is-installed {
    border-color: var(--el-color-success-light-5);
  }

  .card-header {
    display: flex;
    gap: 12px;
    align-items: center;
    margin-bottom: 12px;
  }

  .card-icon {
    display: flex;
    flex-shrink: 0;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    font-size: 20px;
    border-radius: 10px;

    &.icon-bg-default {
      color: var(--el-text-color-secondary);
      background: var(--el-fill-color);
    }

    &.icon-bg-warning {
      color: var(--el-color-warning);
      background: var(--el-color-warning-light-9);
    }

    &.icon-bg-success {
      color: var(--el-color-success);
      background: var(--el-color-success-light-9);
    }

    &.icon-bg-info {
      color: var(--el-color-info);
      background: var(--el-color-info-light-9);
    }
  }

  .card-title-group {
    display: flex;
    flex: 1;
    gap: 8px;
    align-items: center;
    min-width: 0;
  }

  .card-title {
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 15px;
    font-weight: 600;
    color: var(--el-text-color-primary);
    white-space: nowrap;
  }

  .card-badge {
    display: inline-flex;
    flex-shrink: 0;
    align-items: center;
    padding: 1px 8px;
    font-size: 11px;
    font-weight: 500;
    line-height: 1.6;
    border-radius: 10px;

    &.badge-on {
      color: var(--el-color-success);
      background: var(--el-color-success-light-9);
    }

    &.badge-off {
      color: var(--el-color-danger);
      background: var(--el-color-danger-light-9);
    }
  }

  .card-desc {
    display: -webkit-box;
    min-height: calc(13px * 1.6 * 2);
    margin: 0 0 12px;
    overflow: hidden;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    font-size: 13px;
    line-height: 1.6;
    color: var(--el-text-color-secondary);
    -webkit-box-orient: vertical;
  }

  .card-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
    margin-bottom: 14px;
  }

  .tag-version {
    font-size: 12px;
    color: var(--el-text-color-placeholder);
  }

  .card-footer {
    display: flex;
    gap: 8px;
    align-items: center;
    justify-content: space-between;
    padding-top: 12px;
    margin-top: auto;
    border-top: 1px solid var(--el-border-color-lighter);
  }

  .footer-author {
    display: inline-flex;
    flex-shrink: 0;
    gap: 4px;
    align-items: center;
    font-size: 12px;
    color: var(--el-text-color-secondary);
  }

  .footer-actions {
    display: flex;
    flex-shrink: 0;
    gap: 4px;
    align-items: center;
  }

  .more-btn {
    padding: 2px 4px;
    font-size: 16px;
  }
}

.plugin-pagination {
  padding-top: 16px;
}
</style>
