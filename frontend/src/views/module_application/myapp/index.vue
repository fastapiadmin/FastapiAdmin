<!-- 我的应用管理 -->
<template>
  <div class="app-container">
    <!-- 顶部搜索和操作区域 -->
    <div class="search-container">
      <el-form
        ref="queryFormRef"
        :model="queryFormData"
        :inline="true"
        label-suffix=":"
        @submit.prevent="handleQuery"
      >
        <el-form-item prop="name" label="应用名称">
          <el-input v-model="queryFormData.name" placeholder="请输入应用名称" clearable />
        </el-form-item>
        <el-form-item prop="status" label="状态">
          <el-select
            v-model="queryFormData.status"
            placeholder="请选择状态"
            clearable
            style="width: 170px"
          >
            <el-option label="启用" :value="true" />
            <el-option label="停用" :value="false" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="isExpand" prop="creator" label="创建人">
          <UserTableSelect
            v-model="queryFormData.creator"
            @confirm-click="handleConfirm"
            @clear-click="handleQuery"
          />
        </el-form-item>
        <el-form-item class="search-buttons">
          <el-button
            v-hasPerm="['module_module_application:myapp:query']"
            type="primary"
            icon="search"
            native-type="submit"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_application:myapp:query']"
            icon="refresh"
            @click="handleResetQuery"
          >
            重置
          </el-button>
          <!-- 展开/收起 -->
          <template v-if="isExpandable">
            <el-link class="ml-3" type="primary" underline="never" @click="isExpand = !isExpand">
              {{ isExpand ? "收起" : "展开" }}
              <el-icon>
                <template v-if="isExpand">
                  <ArrowUp />
                </template>
                <template v-else>
                  <ArrowDown />
                </template>
              </el-icon>
            </el-link>
          </template>
        </el-form-item>
      </el-form>
    </div>

    <!-- 应用卡片展示区域 -->
    <el-card shadow="hover" class="app-grid-card">
      <template #header>
        <div class="card-header">
          <span>
            <el-tooltip content="点击卡片，打开应用">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            应用市场
          </span>
          <el-button
            v-hasPerm="['module_application:myapp:create']"
            type="primary"
            icon="plus"
            @click="handleCreateApp"
          >
            创建应用
          </el-button>
        </div>
      </template>

      <!-- 应用网格 - 优化布局 -->
      <div v-loading="loading" class="app-grid-container">
        <div class="grid-wrapper">
          <div
            v-for="app in applicationList"
            :key="app.id"
            class="app-grid-item"
            @mouseenter="app.id && (hoveredCard = app.id)"
            @mouseleave="hoveredCard = null"
            @click="app.status && app.id && openAppInternal(app)"
          >
            <el-card shadow="hover" class="app-card" :class="{ 'card-disabled': !app.status }">
              <!-- 卡片头部 -->
              <template #header>
                <div class="app-info-header">
                  <el-avatar :size="42" :src="app.icon_url" class="app-avatar">
                    <el-icon size="20"><Monitor /></el-icon>
                  </el-avatar>
                  <div class="app-title-wrap">
                    <h3 class="app-name" :title="app.name">{{ app.name }}</h3>
                    <el-tag
                      :type="app.status ? 'success' : 'info'"
                      size="small"
                      effect="plain"
                      class="status-tag"
                    >
                      {{ app.status ? "启用" : "停用" }}
                    </el-tag>
                  </div>

                  <!-- 操作按钮 -->
                  <div v-if="hoveredCard === app.id" class="card-actions" @click.stop>
                    <el-button
                      v-hasPerm="['module_application:myapp:update']"
                      type="primary"
                      link
                      icon="Edit"
                      @click="handleAppAction('edit', app)"
                    ></el-button>
                    <el-button
                      v-hasPerm="['module_application:myapp:delete']"
                      type="danger"
                      link
                      icon="Delete"
                      @click="handleAppAction('delete', app)"
                    ></el-button>
                  </div>
                </div>
              </template>

              <!-- 卡片内容 -->
              <template #default>
                <div class="app-content">
                  <p class="app-description" :title="app.description">
                    {{ app.description || "暂无描述" }}
                  </p>
                </div>
              </template>

              <!-- 卡片底部 -->
              <template #footer>
                <div class="card-footer">
                  <div class="footer-item">
                    <el-icon size="14" class="footer-icon"><User /></el-icon>
                    <span class="footer-text">{{ app.created_by?.name || "未知" }}</span>
                  </div>
                  <div class="footer-item">
                    <el-icon size="14" class="footer-icon"><Clock /></el-icon>
                    <span class="footer-text">{{ formatTime(app.created_time) }}</span>
                  </div>
                </div>
              </template>
            </el-card>
          </div>
        </div>
      </div>
      <!-- 空状态 -->
      <div v-if="applicationList.length === 0 && !loading">
        <el-empty :image-size="80" description="暂无数据" />
      </div>

      <!-- 分页区域 -->
      <template #footer>
        <!-- 使用卡片 footer 样式右对齐，无需额外容器 -->
        <pagination
          v-model:total="total"
          v-model:page="queryFormData.page_no"
          v-model:limit="queryFormData.page_size"
          :page-sizes="[12, 24, 48]"
          @pagination="loadApplicationList"
        />
      </template>
    </el-card>

    <!-- 应用创建/编辑弹窗 -->
    <el-drawer
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
            <el-radio :value="true">启用</el-radio>
            <el-radio :value="false">停用</el-radio>
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
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "MyApplication",
  inheritAttrs: false,
});

import { useAppStore } from "@/store/modules/app.store";
import { useTagsViewStore } from "@/store";
import { useRouter } from "vue-router";
import { DeviceEnum } from "@/enums/settings/device.enum";
import { Monitor, User, Clock } from "@element-plus/icons-vue";
import ApplicationAPI, {
  type ApplicationForm,
  type ApplicationInfo,
  type ApplicationPageQuery,
} from "@/api/module_application/myapp";
import { formatToDateTime } from "@/utils/dateUtil";

const appStore = useAppStore();
const tagsViewStore = useTagsViewStore();
const router = useRouter();

// 响应式数据
const queryFormRef = ref();
const formRef = ref();
const loading = ref(false);
const total = ref(0);
const dialogVisible = ref(false);
const dialogType = ref<"create" | "edit">("create");
const currentApp = ref<ApplicationInfo | null>(null);
const isExpand = ref(false);
const isExpandable = ref(true);
const hoveredCard = ref<number | null>(null);

// 分页查询参数
const queryFormData = reactive<ApplicationPageQuery>({
  page_no: 1,
  page_size: 12,
  name: undefined,
  status: undefined,
  creator: undefined,
});

// 应用列表数据
const applicationList = ref<ApplicationInfo[]>([]);

// 表单数据
const formData = reactive<ApplicationForm>({
  name: "",
  access_url: "",
  icon_url: "",
  status: true,
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
  if (!time) return "未知";
  return formatToDateTime(time, "YYYY-MM-DD HH:mm:ss");
};

// 加载应用列表
async function loadApplicationList() {
  loading.value = true;
  try {
    const response = await ApplicationAPI.listApp(queryFormData);
    applicationList.value = response.data.data.items;
    total.value = response.data.data.total;
  } catch (error) {
    console.error("加载应用列表失败:", error);
  } finally {
    loading.value = false;
  }
}

// 查询
async function handleQuery() {
  queryFormData.page_no = 1;
  await loadApplicationList();
}

// 选择创建人后触发查询
function handleConfirm() {
  handleQuery();
}

// 重置查询
async function handleResetQuery() {
  queryFormRef.value?.resetFields();
  queryFormData.page_no = 1;
  await loadApplicationList();
}

// 创建应用
function handleCreateApp() {
  console.log("handleCreateApp");
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
    await loadApplicationList();
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
function openAppInternal(app: ApplicationInfo) {
  if (!app.status || !app.id) {
    if (!app.status) {
      ElMessage.warning("应用已停用，无法打开");
    } else {
      ElMessage.warning("应用ID不存在，无法打开");
    }
    return;
  }

  if (!app.access_url) {
    ElMessage.warning("应用访问地址不存在");
    return;
  }

  // 创建一个动态路由路径
  const appPath = `/internal-app/${app.id}`;
  const appName = `InternalApp${app.id}`;
  const appTitle = app.name || "未命名应用";

  // 先导航到路由，这样可以动态设置路由的meta信息
  router
    .push({
      path: appPath,
      query: { url: app.access_url, appId: app.id.toString(), appName: appTitle },
    })
    .then(() => {
      // 导航完成后，手动添加或更新标签视图
      nextTick(() => {
        // 查找是否已存在该标签
        const existingTag = tagsViewStore.visitedViews.find((tag) => tag.path === appPath);

        if (existingTag) {
          // 如果存在，更新标题
          tagsViewStore.updateVisitedView({
            ...existingTag,
            title: appTitle,
          });
        } else {
          // 如果不存在，添加新标签
          tagsViewStore.addView({
            name: appName,
            title: appTitle,
            path: appPath,
            fullPath:
              appPath +
              `?url=${encodeURIComponent(app.access_url || "")}&appId=${app.id}&appName=${encodeURIComponent(appTitle)}`,
            icon: "Monitor",
            affix: false,
            keepAlive: false,
            query: { url: app.access_url, appId: app?.id?.toString(), appName: appTitle },
          });
        }
      });
    });
}

// 重置表单
function resetForm() {
  Object.assign(formData, {
    name: "",
    access_url: "",
    icon_url: "",
    status: true,
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
    await loadApplicationList();
  } catch (error) {
    console.error("提交失败:", error);
  }
}

// 初始化
onMounted(() => {
  loadApplicationList();
});
</script>

<style lang="scss" scoped>
.app-grid-card {
  position: relative;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 200px);

  :deep(.el-card__footer) {
    display: flex;
    justify-content: flex-end;
    margin-top: auto;
  }
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

// 网格容器
.app-grid-container {
  flex: 1;
  padding: 2px 0;
}

.grid-wrapper {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
  padding: 0 2px;

  @media (max-width: 768px) {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 14px;
  }

  @media (max-width: 480px) {
    grid-template-columns: 1fr;
    gap: 12px;
  }
}

// 卡片项
.app-grid-item {
  height: fit-content;
}

// 卡片样式
.app-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
  cursor: pointer;
  background: linear-gradient(145deg, var(--el-bg-color) 0%, var(--el-bg-color-page) 100%);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

  &:hover {
    border-color: var(--el-color-primary);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
    transform: translateY(-2px);
  }

  &:active {
    transform: translateY(0);
  }

  &.card-disabled {
    cursor: not-allowed;
    opacity: 0.6;

    &:hover {
      border-color: var(--el-border-color-lighter);
      box-shadow: none;
      transform: none;
    }
  }

  :deep(.el-card__header) {
    padding: 16px 18px 14px;
    background: linear-gradient(
      90deg,
      rgba(var(--el-color-primary-rgb), 0.02) 0%,
      transparent 100%
    );
    border-bottom: 1px solid var(--el-border-color-lighter);
  }

  :deep(.el-card__body) {
    display: flex;
    flex: 1;
    flex-direction: column;
    padding: 18px;
  }

  :deep(.el-card__footer) {
    padding: 12px 18px 16px;
    background: rgba(var(--el-fill-color-light-rgb), 0.3);
    border-top: 1px solid var(--el-border-color-lighter);
  }
}

// 头部信息
.app-info-header {
  position: relative;
  display: flex;
  gap: 12px;
  align-items: flex-start;
  min-width: 0;
}

.app-avatar {
  flex-shrink: 0;
  background: var(--el-fill-color-light);
  border: 2px solid var(--el-border-color-lighter);
  transition: all 0.3s ease;

  .app-card:hover & {
    background: rgba(var(--el-color-primary-rgb), 0.1);
    border-color: var(--el-color-primary);
  }
}

.app-title-wrap {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 8px;
  min-width: 0;
}

.app-name {
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 16px;
  font-weight: 600;
  line-height: 1.4;
  color: var(--el-text-color-primary);
  white-space: nowrap;
}

.status-tag {
  align-self: flex-start;
  padding: 2px 10px;
  font-size: 12px;
  font-weight: 500;
  border-radius: 12px;
}

// 悬停操作按钮
.card-actions {
  position: absolute;
  top: 50%;
  right: -10px;
  z-index: 10;
  padding: 8px;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(8px);
  transform: translateY(-50%);

  .el-button {
    padding: 4px 8px;
    margin: 0 2px;

    &:first-child {
      margin-left: 0;
    }

    &:last-child {
      margin-right: 0;
    }
  }
}

// 内容区域
.app-content {
  display: flex;
  flex: 1;
  flex-direction: column;
  justify-content: center;
}

.app-description {
  display: -webkit-box;
  min-height: 2.8em;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  font-size: 14px;
  line-height: 1.6;
  color: var(--el-text-color-regular);
  -webkit-box-orient: vertical;
}

// 底部信息
.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 0 4px;
}

.footer-item {
  display: flex;
  flex-shrink: 0;
  gap: 6px;
  align-items: center;
  min-width: 0;
}

.footer-icon {
  color: var(--el-text-color-secondary);
}

.footer-text {
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 13px;
  color: var(--el-text-color-secondary);
  white-space: nowrap;
}

// 响应式调整
@media (max-width: 768px) {
  .app-name {
    font-size: 15px;
  }

  .app-description {
    font-size: 13px;
  }

  .card-actions {
    position: static;
    align-self: flex-end;
    margin-top: 8px;
    transform: none;

    .el-button {
      padding: 3px 6px;
      font-size: 12px;
    }
  }
}

@media (max-width: 480px) {
  .app-card {
    :deep(.el-card__header) {
      padding: 14px 16px;
    }

    :deep(.el-card__body) {
      padding: 16px;
    }

    :deep(.el-card__footer) {
      padding: 10px 16px 12px;
    }
  }

  .app-name {
    font-size: 14px;
  }
}
</style>
