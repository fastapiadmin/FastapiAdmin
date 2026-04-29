<template>
  <div class="app-container">
    <PageSearch
      ref="searchRef"
      :search-config="searchConfig"
      @query-click="handleQueryClick"
      @reset-click="handleResetClick"
    />

    <PageContent ref="contentRef" :content-config="contentConfig">
      <template #header>
        <div class="card-header">
          <span>
            <el-tooltip content="资源文件管理系统: 点击路径可以快速返回上级目录">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            文件列表(当前路径)：
          </span>
          <div class="breadcrumb-container">
            <span class="breadcrumb-label"></span>
            <el-breadcrumb separator="/">
              <el-breadcrumb-item
                v-for="(item, index) in breadcrumbList"
                :key="index"
                :class="{ 'is-link': index < breadcrumbList.length - 1 }"
                @click="handleBreadcrumbClick(item)"
              >
                {{ item.name }}
              </el-breadcrumb-item>
            </el-breadcrumb>
          </div>
        </div>
      </template>

      <template #toolbar="{ toolbarRight, onToolbar, removeIds, cols }">
        <CrudToolbarLeft :remove-ids="removeIds">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_monitor:resource:upload']"
                type="success"
                icon="plus"
                @click="handleUpload"
              >
                上传文件
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_monitor:resource:create_dir']"
                type="primary"
                icon="folder-add"
                @click="handleCreateDir"
              >
                新建文件夹
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_monitor:resource:delete']"
                type="danger"
                icon="delete"
                :disabled="removeIds.length === 0"
                @click="handleBatchDelete"
              >
                批量删除
              </el-button>
            </el-col>
          </el-row>
        </CrudToolbarLeft>
        <div class="data-table__toolbar--right flex flex-wrap items-center gap-3">
          <el-checkbox
            v-model="showHiddenFiles"
            v-hasPerm="['module_monitor:resource:query']"
            @change="onShowHiddenChange"
          >
            显示隐藏文件
          </el-checkbox>
          <CrudToolbarRight :buttons="toolbarRight" :cols="cols" :on-toolbar="onToolbar" />
        </div>
      </template>

      <template #table="{ data, loading: tableLoading, tableRef, onSelectionChange, pagination }">
        <div class="data-table__content">
          <el-table
            :ref="tableRef as any"
            v-loading="tableLoading"
            row-key="file_url"
            :data="data"
            height="100%"
            border
            stripe
            @selection-change="
              (s) => {
                handleSelectionChange(s as ResourceItem[]);
                onSelectionChange(s);
              }
            "
          >
            <template #empty>
              <el-empty :image-size="80" description="暂无数据" />
            </template>
            <el-table-column type="selection" min-width="40" align="center" />
            <el-table-column type="index" fixed label="序号" min-width="50">
              <template #default="scope">
                {{ (pagination.currentPage - 1) * pagination.pageSize + scope.$index + 1 }}
              </template>
            </el-table-column>
            <el-table-column label="名称" prop="name" min-width="200">
              <template #default="{ row }">
                <div class="file-name">
                  <el-icon class="file-icon">
                    <Folder v-if="row.is_dir" />
                    <Document v-else />
                  </el-icon>
                  <span class="file-name-clickable" @click="handleFileNameClick(row)">
                    {{ row.name }}
                  </span>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="大小" prop="size" min-width="120" align="center">
              <template #default="{ row }">
                <span v-if="!row.is_dir">{{ formatFileSize(row.size) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="修改时间" prop="modified_time" min-width="180" sortable />
            <el-table-column
              fixed="right"
              label="操作"
              align="center"
              min-width="200"
              class-name="search-buttons"
            >
              <template #default="{ row }">
                <el-button
                  v-if="!row.is_dir"
                  v-hasPerm="['module_monitor:resource:download']"
                  type="success"
                  size="small"
                  link
                  icon="download"
                  @click="handleDownload(row)"
                >
                  下载
                </el-button>
                <el-button
                  v-hasPerm="['module_monitor:resource:rename']"
                  type="primary"
                  size="small"
                  link
                  icon="edit"
                  @click="handleRename(row)"
                >
                  重命名
                </el-button>
                <el-button
                  v-hasPerm="['module_monitor:resource:delete']"
                  type="danger"
                  size="small"
                  link
                  icon="delete"
                  @click="handleDelete(row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </template>
    </PageContent>

    <!-- 上传对话框 -->
    <EnhancedDialog
      v-model="uploadDialogVisible"
      title="上传文件"
      width="500px"
      @close="handleUploadClose"
    >
      <el-upload
        ref="uploadRef"
        :auto-upload="false"
        :multiple="true"
        :file-list="uploadFileList"
        drag
        @change="handleUploadChange"
      >
        <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
        <div class="el-upload__text">
          将文件拖到此处，或
          <em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip" style="color: red">
            不支持多文件上传，单个文件不超过100MB，多文件上传，取最后一个文件上传
          </div>
        </template>
      </el-upload>
      <template #footer>
        <el-button @click="uploadDialogVisible = false">取消</el-button>
        <el-button
          v-hasPerm="['module_monitor:resource:upload']"
          type="primary"
          :loading="uploading"
          @click="handleUploadConfirm"
        >
          确定上传
        </el-button>
      </template>
    </EnhancedDialog>

    <!-- 新建文件夹对话框 -->
    <EnhancedDialog v-model="createDirDialogVisible" title="新建文件夹" width="400px">
      <el-form :model="createDirForm" label-width="80px">
        <el-form-item label="文件夹名" required>
          <el-input
            v-model="createDirForm.dir_name"
            placeholder="请输入文件夹名称"
            @keyup.enter="handleCreateDirConfirm"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createDirDialogVisible = false">取消</el-button>
        <el-button
          v-hasPerm="['module_monitor:resource:create_dir']"
          type="primary"
          @click="handleCreateDirConfirm"
        >
          确定
        </el-button>
      </template>
    </EnhancedDialog>

    <!-- 重命名对话框 -->
    <EnhancedDialog v-model="renameDialogVisible" title="重命名" width="400px">
      <el-form :model="renameForm" label-width="80px">
        <el-form-item label="新名称" required>
          <el-input
            v-model="renameForm.new_name"
            placeholder="请输入新名称"
            @keyup.enter="handleRenameConfirm"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="renameDialogVisible = false">取消</el-button>
        <el-button
          v-hasPerm="['module_monitor:resource:rename']"
          type="primary"
          @click="handleRenameConfirm"
        >
          确定
        </el-button>
      </template>
    </EnhancedDialog>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "ResourceMonitor",
  inheritAttrs: false,
});

import { ref, reactive } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { Folder, Document, UploadFilled, QuestionFilled } from "@element-plus/icons-vue";
import {
  ResourceAPI,
  type ResourceItem,
  type ResourcePageQuery,
} from "@/api/module_monitor/resource";
import CrudToolbarLeft from "@/components/CURD/CrudToolbarLeft.vue";
import CrudToolbarRight from "@/components/CURD/CrudToolbarRight.vue";
import PageSearch from "@/components/CURD/PageSearch.vue";
import PageContent from "@/components/CURD/PageContent.vue";
import EnhancedDialog from "@/components/CURD/EnhancedDialog.vue";
import { useCrudList } from "@/components/CURD/useCrudList";
import type { IContentConfig, ISearchConfig } from "@/components/CURD/types";

const { searchRef, contentRef, handleQueryClick, handleResetClick, refreshList } = useCrudList();

const selectedItems = ref<ResourceItem[]>([]);
const breadcrumbList = ref([{ name: "资源根目录", path: "/" }]);
const showHiddenFiles = ref(false);

const currentPath = ref("/");

const searchConfig = reactive<ISearchConfig>({
  permPrefix: "module_monitor:resource",
  colon: true,
  isExpandable: false,
  showNumber: 3,
  form: { labelWidth: "auto" },
  searchButtonPerm: "module_monitor:resource:query",
  resetButtonPerm: "module_monitor:resource:query",
  formItems: [
    {
      prop: "name",
      label: "关键词",
      type: "input",
      attrs: { placeholder: "请输入文件名或目录名", clearable: true, style: { width: "200px" } },
    },
  ],
});

const contentConfig = reactive<IContentConfig<ResourcePageQuery>>({
  permPrefix: "module_monitor:resource",
  cols: [],
  hideColumnFilter: true,
  toolbar: [],
  defaultToolbar: ["refresh"],
  pk: "file_url",
  pagination: {
    pageSize: 10,
    pageSizes: [10, 20, 30, 50],
  },
  request: { page_no: "page_no", page_size: "page_size" },
  indexAction: async (params) => {
    const merged: ResourcePageQuery = {
      ...(params as ResourcePageQuery),
      include_hidden: showHiddenFiles.value,
    };
    if (currentPath.value && currentPath.value !== "/") {
      merged.path = currentPath.value;
    }
    const res = await ResourceAPI.listResource(merged);
    return {
      total: res.data.data.total,
      list: res.data.data.items,
    };
  },
});

const uploadDialogVisible = ref(false);
const createDirDialogVisible = ref(false);
const renameDialogVisible = ref(false);
const uploading = ref(false);

const uploadRef = ref();
const uploadFileList = ref<any[]>([]);

const createDirForm = reactive({
  dir_name: "",
});

const renameForm = reactive({
  new_name: "",
  old_path: "",
});

function handleBreadcrumbClick(item: { path: string }) {
  currentPath.value = item.path;
  updateBreadcrumb();
  refreshList();
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

function handleFileNameClick(row: ResourceItem) {
  if (row.is_dir) {
    if (currentPath.value === "/") {
      currentPath.value = row.name;
    } else {
      currentPath.value = currentPath.value + "/" + row.name;
    }
    updateBreadcrumb();
    refreshList();
  } else {
    handleFilePreview(row);
  }
}

function handleFilePreview(file: ResourceItem) {
  let previewUrl = file.file_url;

  if (previewUrl && !previewUrl.startsWith("http")) {
    previewUrl = `${window.location.origin}${previewUrl}`;
  }

  window.open(previewUrl, "_blank");
}

function handleSelectionChange(selection: ResourceItem[]) {
  selectedItems.value = selection;
}

function handleUpload() {
  uploadDialogVisible.value = true;
  uploadFileList.value = [];
}

function handleUploadChange(_file: unknown, fileList: unknown[]) {
  uploadFileList.value = fileList as any[];
}

async function handleUploadConfirm() {
  if (uploadFileList.value.length === 0) {
    ElMessage.warning("请选择要上传的文件");
    return;
  }

  try {
    uploading.value = true;
    const formData = new FormData();
    uploadFileList.value.forEach((file: { raw?: Blob }) => {
      const raw = file.raw;
      if (raw) formData.append("file", raw);
    });

    const targetPath = currentPath.value === "/" ? "" : currentPath.value;
    formData.append("target_path", targetPath);

    await ResourceAPI.uploadFile(formData);
    uploadDialogVisible.value = false;
    refreshList();
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
    refreshList();
  } catch (error) {
    console.error("Create directory error:", error);
  }
}

function onShowHiddenChange() {
  refreshList();
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

function handleRename(item: ResourceItem) {
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
    refreshList();
  } catch (error) {
    console.error("Rename error:", error);
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
    refreshList();
  } catch (error) {
    if (error !== "cancel") {
      console.error("Delete error:", error);
    }
  }
}

async function handleBatchDelete() {
  if (selectedItems.value.length === 0) {
    ElMessage.warning("请选择要删除的文件");
    return;
  }

  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedItems.value.length} 个文件吗？`,
      "确认删除",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }
    );

    const paths = selectedItems.value.map((item) => item.file_url);

    await ResourceAPI.deleteResource(paths);
    refreshList();
  } catch (error) {
    if (error !== "cancel") {
      console.error("Batch delete error:", error);
    }
  }
}

function formatFileSize(size?: number | null) {
  if (!size || size === null) return "-";
  const units = ["B", "KB", "MB", "GB", "TB"];
  let unitIndex = 0;
  let fileSize = size;

  while (fileSize >= 1024 && unitIndex < units.length - 1) {
    fileSize /= 1024;
    unitIndex++;
  }

  return `${fileSize.toFixed(1)} ${units[unitIndex]}`;
}
</script>

<style lang="scss" scoped>
.card-header {
  display: flex;
  align-items: center;
}

.data-table__content {
  .file-name {
    display: flex;
    gap: 8px;
    align-items: center;

    .file-name-clickable {
      color: var(--el-color-primary);
      cursor: pointer;

      &:hover {
        color: var(--el-color-primary-light-3);
        text-decoration: underline;
      }
    }
  }
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
