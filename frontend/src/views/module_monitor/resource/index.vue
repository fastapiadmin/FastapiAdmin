<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form
        ref="queryFormRef"
        :model="queryFormData"
        :inline="true"
        label-suffix=":"
        @submit.prevent="handleQuery"
      >
        <el-form-item prop="name" label="关键词">
          <el-input
            v-model="queryFormData.name"
            placeholder="请输入文件名或目录名"
            clearable
            style="width: 200px"
            @keyup.enter="handleQuery"
          />
        </el-form-item>
        <el-form-item class="search-buttons">
          <el-button
            v-hasPerm="['module_monitor:resource:query']"
            type="primary"
            icon="search"
            native-type="submit"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_monitor:resource:query']"
            icon="refresh"
            @click="handleResetQuery"
          >
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 内容区域 -->
    <el-card class="data-table">
      <template #header>
        <div class="card-header">
          <span>
            <el-tooltip content="资源文件管理系统: 点击路径可以快速返回上级目录">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            文件列表(当前路径)：
          </span>
          <!-- 资源路径 -->
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

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--left">
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
                :disabled="selectedItems.length === 0"
                @click="handleBatchDelete"
              >
                批量删除
              </el-button>
            </el-col>
          </el-row>
        </div>
        <div class="data-table__toolbar--right">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-checkbox
                v-model="showHiddenFiles"
                v-hasPerm="['module_monitor:resource:query']"
                @change="handleShowHiddenChange"
              >
                显示隐藏文件
              </el-checkbox>
            </el-col>
            <el-col :span="1.5">
              <el-button-group>
                <el-button
                  v-hasPerm="['module_monitor:resource:query']"
                  :type="viewMode === 'list' ? 'primary' : ''"
                  @click="viewMode = 'list'"
                >
                  <el-icon><List /></el-icon>
                </el-button>
                <el-button
                  v-hasPerm="['module_monitor:resource:query']"
                  :type="viewMode === 'grid' ? 'primary' : ''"
                  @click="viewMode = 'grid'"
                >
                  <el-icon><Grid /></el-icon>
                </el-button>
              </el-button-group>
            </el-col>
            <el-col :span="1.5">
              <el-tooltip content="刷新">
                <el-button
                  v-hasPerm="['module_monitor:resource:query']"
                  type="primary"
                  icon="refresh"
                  circle
                  @click="handleRefresh"
                />
              </el-tooltip>
            </el-col>
          </el-row>
        </div>
      </div>

      <!-- 表格区域 -->
      <el-table
        v-if="viewMode === 'list'"
        ref="dataTableRef"
        v-loading="loading"
        :data="fileList"
        row-key="file_url"
        class="data-table__content"
        height="450"
        max-height="450px"
        border
        stripe
        @selection-change="handleSelectionChange"
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column type="selection" min-width="40" align="center" />
        <el-table-column type="index" fixed label="序号" min-width="50">
          <template #default="scope">
            {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column label="名称" prop="name" min-width="200">
          <template #default="{ row }">
            <div class="file-name">
              <el-icon class="file-icon">
                <Folder v-if="row.is_dir" />
                <Document v-else />
              </el-icon>
              <span :class="{ 'file-name-clickable': true }" @click="handleFileNameClick(row)">
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
          class="search-buttons"
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

      <!-- 网格视图 -->
      <div v-else class="grid-view">
        <div
          v-for="item in fileList"
          :key="item.file_url"
          class="grid-item"
          @click="handleItemClick(item)"
        >
          <div class="item-icon">
            <el-icon v-if="item.is_dir" size="48">
              <Folder />
            </el-icon>
            <el-icon v-else size="48">
              <Document />
            </el-icon>
          </div>
          <div class="item-name">{{ item.name }}</div>
          <div v-if="!item.is_dir" class="item-size">
            {{ formatFileSize(item.size) }}
          </div>
        </div>
      </div>

      <!-- 分页区域 -->
      <template #footer>
        <Pagination
          v-model:total="total"
          v-model:page="pagination.page_no"
          v-model:limit="pagination.page_size"
          @pagination="handlePagination"
        />
      </template>
    </el-card>

    <!-- 上传对话框 -->
    <el-dialog
      v-model="uploadDialogVisible"
      title="上传文件"
      width="500px"
      :before-close="handleUploadClose"
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
    </el-dialog>

    <!-- 新建文件夹对话框 -->
    <el-dialog v-model="createDirDialogVisible" title="新建文件夹" width="400px">
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
    </el-dialog>

    <!-- 重命名对话框 -->
    <el-dialog v-model="renameDialogVisible" title="重命名" width="400px">
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
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "ResourceMonitor",
  inheritAttrs: false,
});

import { ref, reactive, onMounted, computed } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import {
  List,
  Grid,
  Folder,
  Document,
  UploadFilled,
  QuestionFilled,
} from "@element-plus/icons-vue";
import {
  ResourceAPI,
  type ResourceItem,
  type ResourcePageQuery,
} from "@/api/module_monitor/resource";

// 分页表单
const fileList = ref<ResourceItem[]>([]);

// 响应式数据
const loading = ref(false);
const selectedItems = ref<ResourceItem[]>([]);
const breadcrumbList = ref([{ name: "资源根目录", path: "/" }]);
const showHiddenFiles = ref(false);
const viewMode = ref<"list" | "grid">("list");
const total = ref(0);
const isSearchMode = ref(false); // 用于标记是否处于搜索模式
const queryFormRef = ref();

// 路径相关数据
const currentPath = ref("/"); // 当前路径的响应式变量

// 分页查询参数
const pagination = reactive({
  page_no: 1,
  page_size: 10,
});

// 搜索表单数据
const queryFormData = reactive<ResourcePageQuery>({
  name: undefined,
  page_no: 1,
  page_size: 10,
});

// 对话框状态
const uploadDialogVisible = ref(false);
const createDirDialogVisible = ref(false);
const renameDialogVisible = ref(false);
const uploading = ref(false);

// 上传相关
const uploadRef = ref();
const uploadFileList = ref<any[]>([]);

// 表单数据
const createDirForm = reactive({
  dir_name: "",
});

const renameForm = reactive({
  new_name: "",
  old_path: "",
});

// 计算属性
const currentQuery = computed(() => {
  // 构建查询参数
  const query: any = {
    include_hidden: showHiddenFiles.value,
    page_no: pagination.page_no,
    page_size: pagination.page_size,
  };

  // 如果当前路径不是根路径，则添加路径参数
  if (currentPath.value && currentPath.value !== "/") {
    // 对于文件夹导航，直接传递文件夹名称
    query.path = currentPath.value;
  }

  // 添加搜索关键词
  if (queryFormData.name) {
    query.name = queryFormData.name;
  }

  return query;
});

// 加载文件列表
async function loadFileList() {
  loading.value = true;
  try {
    const response = await ResourceAPI.listResource(currentQuery.value);

    // 正确处理后端返回的分页数据结构
    const pageResult = response.data?.data;

    if (pageResult && Array.isArray(pageResult.items)) {
      fileList.value = pageResult.items;
      total.value = pageResult.total;
      if (pageResult.page_no !== undefined) {
        pagination.page_no = pageResult.page_no;
      }
      if (pageResult.page_size !== undefined) {
        pagination.page_size = pageResult.page_size;
      }
    } else {
      fileList.value = [];
      total.value = 0;
    }
  } catch (error) {
    console.error("Load file list error:", error);
    fileList.value = [];
    total.value = 0;
  } finally {
    loading.value = false;
  }
}

// 面包屑点击处理
function handleBreadcrumbClick(item: any) {
  // 更新当前路径为点击的面包屑项路径
  currentPath.value = item.path;
  updateBreadcrumb();
  loadFileList();
}

// 更新面包屑路径
function updateBreadcrumb() {
  // 对于根路径，直接显示根目录
  if (currentPath.value === "/") {
    breadcrumbList.value = [{ name: "资源根目录", path: "/" }];
    return;
  }

  // 对于嵌套路径，需要分解并构建面包屑
  const parts = currentPath.value.split("/").filter((part) => part !== "");

  breadcrumbList.value = [
    { name: "资源根目录", path: "/" },
    ...parts.map((part, index) => ({
      name: part,
      path: parts.slice(0, index + 1).join("/"),
    })),
  ];
}

// 文件名点击处理
function handleFileNameClick(row: ResourceItem) {
  if (row.is_dir) {
    // 如果当前在根路径，则直接使用文件夹名称
    // 如果当前已在某个文件夹中，则拼接路径
    if (currentPath.value === "/") {
      currentPath.value = row.name;
    } else {
      currentPath.value = currentPath.value + "/" + row.name;
    }
    updateBreadcrumb();
    loadFileList();
  } else {
    // 文件预览，使用后端返回的完整URL
    handleFilePreview(row);
  }
}

// 网格视图项目点击处理
function handleItemClick(item: ResourceItem) {
  if (item.is_dir) {
    // 如果当前在根路径，则直接使用文件夹名称
    // 如果当前已在某个文件夹中，则拼接路径
    if (currentPath.value === "/") {
      currentPath.value = item.name;
    } else {
      currentPath.value = currentPath.value + "/" + item.name;
    }
    updateBreadcrumb();
    loadFileList();
  } else {
    // 文件预览，使用后端返回的完整URL
    handleFilePreview(item);
  }
}

// 文件预览
function handleFilePreview(file: ResourceItem) {
  // 直接使用file_url字段进行预览
  let previewUrl = file.file_url;

  // 如果是相对路径，构建完整URL
  if (previewUrl && !previewUrl.startsWith("http")) {
    previewUrl = `${window.location.origin}${previewUrl}`;
  }

  // 所有文件类型统一直接打开预览
  window.open(previewUrl, "_blank");
}

// 选择项变化处理
function handleSelectionChange(selection: ResourceItem[]) {
  selectedItems.value = selection;
}

// 打开上传对话框
function handleUpload() {
  uploadDialogVisible.value = true;
  uploadFileList.value = [];
}

// 上传文件变化处理
function handleUploadChange(file: any, fileList: any[]) {
  uploadFileList.value = fileList;
}

// 确认上传文件
async function handleUploadConfirm() {
  if (uploadFileList.value.length === 0) {
    ElMessage.warning("请选择要上传的文件");
    return;
  }

  try {
    uploading.value = true;
    const formData = new FormData();
    uploadFileList.value.forEach((file: any) => {
      formData.append("file", file.raw);
    });

    // 在根目录时传递空字符串作为target_path，与后端relative_path格式保持一致
    const targetPath = currentPath.value === "/" ? "" : currentPath.value;
    formData.append("target_path", targetPath);

    await ResourceAPI.uploadFile(formData);
    uploadDialogVisible.value = false;
    loadFileList();
  } catch (error) {
    console.error("Upload error:", error);
  } finally {
    uploading.value = false;
  }
}

// 关闭上传对话框
function handleUploadClose() {
  uploadDialogVisible.value = false;
  uploadFileList.value = [];
}

// 打开新建目录对话框
function handleCreateDir() {
  createDirForm.dir_name = "";
  createDirDialogVisible.value = true;
}

// 确认创建目录
async function handleCreateDirConfirm() {
  if (!createDirForm.dir_name.trim()) {
    ElMessage.warning("请输入文件夹名称");
    return;
  }

  try {
    // 在根目录时传递空字符串作为parent_path，与后端relative_path格式保持一致
    const parentPath = currentPath.value === "/" ? "" : currentPath.value;
    await ResourceAPI.createDirectory({
      parent_path: parentPath,
      dir_name: createDirForm.dir_name.trim(),
    });
    createDirDialogVisible.value = false;
    loadFileList();
  } catch (error) {
    console.error("Create directory error:", error);
  }
}

// 列表刷新
async function handleRefresh() {
  await loadFileList();
}

// 查询（重置页码后获取数据）
async function handleQuery() {
  queryFormData.page_no = 1;
  await loadFileList();
}

// 重置查询
async function handleResetQuery() {
  queryFormRef.value.resetFields();
  queryFormData.page_no = 1;
  isSearchMode.value = false; // 退出搜索模式
  await loadFileList();
}

// 显示隐藏文件切换
function handleShowHiddenChange() {
  loadFileList();
}

// 文件下载
async function handleDownload(item: ResourceItem) {
  try {
    // 使用file_url字段
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

// 打开重命名对话框
function handleRename(item: ResourceItem) {
  // 使用file_url字段
  renameForm.old_path = item.file_url;
  renameForm.new_name = item.name;
  renameDialogVisible.value = true;
}

// 确认重命名
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
    loadFileList();
  } catch (error) {
    console.error("Rename error:", error);
  }
}

// 文件删除
async function handleDelete(item: ResourceItem) {
  try {
    await ElMessageBox.confirm(`确定要删除 ${item.name} 吗？`, "确认删除", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });

    // 使用file_url字段
    await ResourceAPI.deleteResource([item.file_url]);
    loadFileList();
  } catch (error) {
    if (error !== "cancel") {
      console.error("Delete error:", error);
    }
  }
}

// 分页处理
function handlePagination(params: { page: number; limit: number }) {
  pagination.page_no = params.page;
  pagination.page_size = params.limit;
  loadFileList();
}

// 批量删除
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

    // 使用file_url字段
    const paths = selectedItems.value.map((item) => item.file_url);

    await ResourceAPI.deleteResource(paths);
    loadFileList();
  } catch (error) {
    if (error !== "cancel") {
      console.error("Batch delete error:", error);
    }
  }
}

// 格式化文件大小
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

// 生命周期
onMounted(() => {
  loadFileList();
});
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

.grid-view {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 20px;
  height: calc(100vh - 200px);

  .grid-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    // 使用系统主题颜色
    border-radius: 8px;
    transition: all 0.3s;

    .item-name {
      margin-bottom: 5px;
      font-size: 14px;
      text-align: center;
      word-break: break-all;
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
