<!-- 资源管理：Art + useTable -->
<template>
  <div class="art-full-height resource-monitor-page">
    <ArtSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="resourceSearchItems"
      :rules="searchBarRules"
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
      class="resource-monitor-card flex flex-col flex-1 min-h-0 art-table-card"
      :style="{ 'margin-top': showSearchBar ? '12px' : '0' }"
    >
      <div
        class="resource-breadcrumb mb-3 shrink-0 flex flex-wrap items-center gap-2 border-b border-g-200 pb-3"
      >
        <ElTooltip content="资源文件管理系统: 点击路径可以快速返回上级目录">
          <QuestionFilled class="mx-1 h-4 w-4" />
        </ElTooltip>
        <span class="text-sm">文件列表(当前路径)：</span>
        <div class="breadcrumb-container min-w-0 flex-1">
          <ElBreadcrumb separator="/">
            <ElBreadcrumbItem
              v-for="(item, index) in breadcrumbList"
              :key="index"
              :class="{ 'is-link': index < breadcrumbList.length - 1 }"
              @click="handleBreadcrumbClick(item)"
            >
              {{ item.name }}
            </ElBreadcrumbItem>
          </ElBreadcrumb>
        </div>
      </div>

      <ArtTableHeader
        class="resource-toolbar shrink-0"
        v-model:columns="columnChecks"
        v-model:showSearchBar="showSearchBar"
        :loading="loading"
        @refresh="refreshData"
      >
        <template #left>
          <ElSpace wrap>
            <ElButton
              v-hasPerm="['module_monitor:resource:upload']"
              type="success"
              plain
              :icon="Plus"
              @click="handleUpload"
            >
              上传文件
            </ElButton>
            <ElButton
              v-hasPerm="['module_monitor:resource:create_dir']"
              type="primary"
              plain
              :icon="FolderAdd"
              @click="handleCreateDir"
            >
              新建文件夹
            </ElButton>
            <ElButton
              v-hasPerm="['module_monitor:resource:delete']"
              type="danger"
              plain
              :icon="Delete"
              :disabled="selectedPaths.length === 0"
              :loading="batchDeleting"
              @click="handleBatchDelete"
            >
              批量删除
            </ElButton>
            <ElCheckbox
              v-model="showHiddenFiles"
              v-hasPerm="['module_monitor:resource:query']"
              @change="onShowHiddenChange"
            >
              显示隐藏文件
            </ElCheckbox>
          </ElSpace>
        </template>
      </ArtTableHeader>

      <!-- 面包屑与表头已占用高度：表格高度须在独立 flex 子项内计算，否则分页会被挤出卡片 -->
      <div class="resource-table-region min-h-0 flex flex-1 flex-col overflow-hidden pb-3">
        <ArtTable
          row-key="file_url"
          :show-table-header="false"
          :loading="loading"
          :data="data"
          :columns="columns"
          :pagination="pagination"
          @selection-change="onTableSelectionChange"
          @pagination:size-change="handleSizeChange"
          @pagination:current-change="handleCurrentChange"
        />
      </div>
    </ElCard>

    <ArtDialog
      v-model="uploadDialogVisible"
      title="上传文件"
      width="500px"
      @close="handleUploadClose"
    >
      <ElUpload
        ref="uploadRef"
        :auto-upload="false"
        :multiple="true"
        :file-list="uploadFileList"
        drag
        @change="handleUploadChange"
      >
        <ElIcon class="el-icon--upload"><UploadFilled /></ElIcon>
        <div class="el-upload__text">
          将文件拖到此处，或
          <em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip text-error">
            不支持多文件上传，单个文件不超过100MB，多文件上传，取最后一个文件上传
          </div>
        </template>
      </ElUpload>
      <template #footer>
        <ElButton @click="uploadDialogVisible = false">取消</ElButton>
        <ElButton
          v-hasPerm="['module_monitor:resource:upload']"
          type="primary"
          :loading="uploading"
          @click="handleUploadConfirm"
        >
          确定上传
        </ElButton>
      </template>
    </ArtDialog>

    <ArtDialog v-model="createDirDialogVisible" title="新建文件夹" width="400px">
      <ElForm :model="createDirForm" label-width="80px">
        <ElFormItem label="文件夹名" required>
          <ElInput
            v-model="createDirForm.dir_name"
            placeholder="请输入文件夹名称"
            @keyup.enter="handleCreateDirConfirm"
          />
        </ElFormItem>
      </ElForm>
      <template #footer>
        <ElButton @click="createDirDialogVisible = false">取消</ElButton>
        <ElButton
          v-hasPerm="['module_monitor:resource:create_dir']"
          type="primary"
          @click="handleCreateDirConfirm"
        >
          确定
        </ElButton>
      </template>
    </ArtDialog>

    <ArtDialog v-model="renameDialogVisible" title="重命名" width="400px">
      <ElForm :model="renameForm" label-width="80px">
        <ElFormItem label="新名称" required>
          <ElInput
            v-model="renameForm.new_name"
            placeholder="请输入新名称"
            @keyup.enter="handleRenameConfirm"
          />
        </ElFormItem>
      </ElForm>
      <template #footer>
        <ElButton @click="renameDialogVisible = false">取消</ElButton>
        <ElButton
          v-hasPerm="['module_monitor:resource:rename']"
          type="primary"
          @click="handleRenameConfirm"
        >
          确定
        </ElButton>
      </template>
    </ArtDialog>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "ResourceMonitor",
  inheritAttrs: false,
});

import { h, ref, reactive, computed } from "vue";
import {
  ElMessage,
  ElMessageBox,
  ElIcon,
  ElSpace,
  ElTooltip,
  type UploadFile,
  type UploadFiles,
  type UploadUserFile,
} from "element-plus";
import {
  Delete,
  Document,
  Folder,
  FolderAdd,
  Plus,
  QuestionFilled,
  UploadFilled,
} from "@element-plus/icons-vue";
import { useTable } from "@/hooks/core/useTable";
import ArtTable from "@/components/Core/tables/art-table/index.vue";
import ArtTableHeader from "@/components/Core/tables/art-table-header/index.vue";
import ArtSearchBar from "@/components/Core/forms/art-search-bar/index.vue";
import type { SearchFormItem } from "@/components/Core/forms/art-search-bar/index.vue";
import ArtButtonTable from "@/components/Core/forms/art-button-table/index.vue";
import ArtDialog from "@/components/Core/modal/art-dialog/index.vue";
import { ResourceAPI, type ResourceItem } from "@/api/module_monitor/resource";
import type { ColumnOption } from "@/types/component";
import { useAuth } from "@/hooks/core/useAuth";

const { hasAuth } = useAuth();

type ResourceSearchForm = {
  name?: string;
};

function buildResourceReplaceParams(u: ResourceSearchForm): Record<string, unknown> {
  return {
    name: u.name,
  };
}

function fetchResourceTableList(params: Record<string, unknown>) {
  return ResourceAPI.listResource({
    page_no: 1,
    page_size: 10,
    ...params,
  });
}

const searchForm = ref<ResourceSearchForm>({
  name: undefined,
});

const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof ArtSearchBar> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const resourceSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "关键词",
    key: "name",
    type: "input",
    placeholder: "请输入文件名或目录名",
    clearable: true,
    span: 6,
  },
]);

const selectedRows = ref<ResourceItem[]>([]);
const selectedPaths = computed(() => selectedRows.value.map((r) => r.file_url));

function onTableSelectionChange(rows: ResourceItem[]) {
  selectedRows.value = rows;
}

const breadcrumbList = ref([{ name: "资源根目录", path: "/" }]);
const showHiddenFiles = ref(false);
const currentPath = ref("/");

const uploadDialogVisible = ref(false);
const createDirDialogVisible = ref(false);
const renameDialogVisible = ref(false);
const uploading = ref(false);
const batchDeleting = ref(false);

const uploadRef = ref();
const uploadFileList = ref<UploadUserFile[]>([]);

const createDirForm = reactive({
  dir_name: "",
});

const renameForm = reactive({
  new_name: "",
  old_path: "",
});

function formatFileSize(size?: number | null) {
  if (!size || size === null) return "—";
  const units = ["B", "KB", "MB", "GB", "TB"];
  let unitIndex = 0;
  let fileSize = size;

  while (fileSize >= 1024 && unitIndex < units.length - 1) {
    fileSize /= 1024;
    unitIndex++;
  }

  return `${fileSize.toFixed(1)} ${units[unitIndex]}`;
}

function updateBreadcrumb() {
  if (currentPath.value === "/") {
    breadcrumbList.value = [{ name: "资源根目录", path: "/" }];
    return;
  }

  const parts = currentPath.value.split("/").filter((part) => part !== "");

  breadcrumbList.value = [
    { name: "资源根目录", path: "/" },
    ...parts.map((part, index) => ({
      name: part,
      path: parts.slice(0, index + 1).join("/"),
    })),
  ];
}

function handleFilePreview(file: ResourceItem) {
  let previewUrl = file.file_url;

  if (previewUrl && !previewUrl.startsWith("http")) {
    previewUrl = `${window.location.origin}${previewUrl}`;
  }

  window.open(previewUrl, "_blank");
}

const {
  columns,
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
} = useTable({
  core: {
    apiFn: fetchResourceTableList,
    apiParams: {
      page_no: 1,
      page_size: 20,
    },
    columnsFactory: (): ColumnOption<ResourceItem>[] => [
      { type: "selection", width: 48, fixed: "left" },
      { type: "globalIndex", width: 56, label: "序号" },
      {
        prop: "name",
        label: "名称",
        minWidth: 200,
        formatter: (row: ResourceItem) =>
          h("div", { class: "file-name flex items-center gap-2" }, [
            h(ElIcon, { class: "file-icon" }, () => h(row.is_dir ? Folder : Document)),
            h(
              "span",
              {
                class:
                  "file-name-clickable cursor-pointer text-theme hover:text-theme/80 hover:underline",
                onClick: () => handleFileNameClick(row),
              },
              row.name
            ),
          ]),
      },
      {
        prop: "size",
        label: "大小",
        minWidth: 120,
        align: "center",
        formatter: (row: ResourceItem) => (row.is_dir ? "" : h("span", formatFileSize(row.size))),
      },
      {
        prop: "modified_time",
        label: "修改时间",
        minWidth: 180,
        sortable: true,
        showOverflowTooltip: true,
      },
      {
        prop: "operation",
        label: "操作",
        width: 220,
        fixed: "right",
        align: "center",
        formatter: (row: ResourceItem) =>
          h(
            ElSpace,
            { wrap: true, size: 4 },
            () =>
              [
                !row.is_dir && hasAuth("module_monitor:resource:download")
                  ? h(ElTooltip, { content: "下载", placement: "top" }, () =>
                      h("span", { class: "inline-flex" }, [
                        h(ArtButtonTable, {
                          type: "view",
                          icon: "ri:download-line",
                          onClick: () => void handleDownload(row),
                        }),
                      ])
                    )
                  : null,
                hasAuth("module_monitor:resource:rename")
                  ? h(ElTooltip, { content: "重命名", placement: "top" }, () =>
                      h("span", { class: "inline-flex" }, [
                        h(ArtButtonTable, {
                          type: "edit",
                          onClick: () => void handleRenameOpen(row),
                        }),
                      ])
                    )
                  : null,
                hasAuth("module_monitor:resource:delete")
                  ? h(ElTooltip, { content: "删除", placement: "top" }, () =>
                      h("span", { class: "inline-flex" }, [
                        h(ArtButtonTable, {
                          type: "delete",
                          onClick: () => void handleDelete(row),
                        }),
                      ])
                    )
                  : null,
              ].filter(Boolean) as ReturnType<typeof h>[]
          ),
      },
    ],
  },
});

function handleBreadcrumbClick(item: { path: string }) {
  currentPath.value = item.path;
  updateBreadcrumb();
  void getData();
}

function handleFileNameClick(row: ResourceItem) {
  if (row.is_dir) {
    if (currentPath.value === "/") {
      currentPath.value = row.name;
    } else {
      currentPath.value = `${currentPath.value}/${row.name}`;
    }
    updateBreadcrumb();
    void getData();
  } else {
    handleFilePreview(row);
  }
}

async function handleSearchBarSearch(params: ResourceSearchForm) {
  await searchBarRef.value?.validate?.();
  replaceSearchParams(buildResourceReplaceParams(params));
  getData();
}

async function onResetSearch() {
  searchForm.value = { name: undefined };
  await resetSearchParams();
}

function onShowHiddenChange() {
  getData();
}

function handleUpload() {
  uploadDialogVisible.value = true;
  uploadFileList.value = [];
}

function handleUploadChange(_file: UploadFile, fileList: UploadFiles) {
  uploadFileList.value = fileList as UploadUserFile[];
}

async function handleUploadConfirm() {
  if (uploadFileList.value.length === 0) {
    ElMessage.warning("请选择要上传的文件");
    return;
  }

  try {
    uploading.value = true;
    const formData = new FormData();
    uploadFileList.value.forEach((file) => {
      const raw = file.raw;
      if (raw) formData.append("file", raw);
    });

    const targetPath = currentPath.value === "/" ? "" : currentPath.value;
    formData.append("target_path", targetPath);

    await ResourceAPI.uploadFile(formData);
    uploadDialogVisible.value = false;
    await refreshData();
  } catch (error) {
    console.error("Upload error:", error);
  } finally {
    uploading.value = false;
  }
}

function handleUploadClose() {
  uploadDialogVisible.value = false;
  uploadFileList.value = [];
}

function handleCreateDir() {
  createDirForm.dir_name = "";
  createDirDialogVisible.value = true;
}

async function handleCreateDirConfirm() {
  if (!createDirForm.dir_name.trim()) {
    ElMessage.warning("请输入文件夹名称");
    return;
  }

  try {
    const parentPath = currentPath.value === "/" ? "" : currentPath.value;
    await ResourceAPI.createDirectory({
      parent_path: parentPath,
      dir_name: createDirForm.dir_name.trim(),
    });
    createDirDialogVisible.value = false;
    await refreshData();
  } catch (error) {
    console.error("Create directory error:", error);
  }
}

function handleRenameOpen(item: ResourceItem) {
  renameForm.old_path = item.file_url;
  renameForm.new_name = item.name;
  renameDialogVisible.value = true;
}

async function handleRenameConfirm() {
  if (!renameForm.new_name.trim()) {
    ElMessage.warning("请输入新名称");
    return;
  }

  try {
    await ResourceAPI.renameResource({
      old_path: renameForm.old_path,
      new_name: renameForm.new_name.trim(),
    });
    renameDialogVisible.value = false;
    await refreshData();
  } catch (error) {
    console.error("Rename error:", error);
  }
}

async function handleDownload(item: ResourceItem) {
  try {
    const response = await ResourceAPI.downloadFile(item.file_url);
    const blob = response.data;
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = item.name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Download error:", error);
  }
}

async function handleDelete(item: ResourceItem) {
  try {
    await ElMessageBox.confirm(`确定要删除 ${item.name} 吗？`, "确认删除", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });

    await ResourceAPI.deleteResource([item.file_url]);
    selectedRows.value = [];
    await refreshData();
  } catch (error) {
    if (error !== "cancel") {
      console.error("Delete error:", error);
    }
  }
}

async function handleBatchDelete() {
  if (selectedRows.value.length === 0) {
    ElMessage.warning("请选择要删除的文件");
    return;
  }

  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedRows.value.length} 个文件吗？`,
      "确认删除",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }
    );

    batchDeleting.value = true;
    const paths = selectedRows.value.map((item) => item.file_url);
    await ResourceAPI.deleteResource(paths);
    selectedRows.value = [];
    await refreshData();
  } catch (error) {
    if (error !== "cancel") {
      console.error("Batch delete error:", error);
    }
  } finally {
    batchDeleting.value = false;
  }
}
</script>

<style lang="scss" scoped>
.resource-monitor-page :deep(.resource-monitor-card.el-card > .el-card__body) {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
}

:deep(.el-breadcrumb__item) {
  &.is-link {
    color: var(--el-color-primary);
    cursor: pointer;

    &:hover {
      color: var(--el-color-primary-light-3);
    }
  }
}
</style>
