<template>
  <div @click="openSearchModal">
    <!-- <div class="i-svg:search" /> -->
    <div class="command-palette-trigger" role="button" tabindex="0" aria-label="打开搜索面板">
      <div class="command-palette-trigger__left">
        <div class="i-svg:search" />
        <span class="command-palette-trigger__text">搜索菜单</span>
      </div>
      <kbd class="command-palette-trigger__kbd">Ctrl K</kbd>
    </div>
    <el-dialog
      v-model="isModalVisible"
      width="30%"
      :append-to-body="true"
      :show-close="false"
      @close="closeSearchModal"
    >
      <template #header>
        <el-input
          ref="searchInputRef"
          v-model="searchKeyword"
          size="large"
          placeholder="输入菜单名称关键字搜索"
          clearable
          @keyup.enter="selectActiveResult"
          @input="updateSearchResults"
          @keydown.up.prevent="navigateResults('up')"
          @keydown.down.prevent="navigateResults('down')"
          @keydown.esc="closeSearchModal"
        >
          <template #prepend>
            <el-button icon="Search" />
          </template>
        </el-input>
      </template>

      <div class="search-result">
        <!-- 搜索历史 -->
        <template v-if="searchKeyword === '' && searchHistory.length > 0">
          <div class="search-history">
            <div class="search-history__title">
              搜索历史
              <el-button
                type="primary"
                text
                size="small"
                class="search-history__clear"
                @click="clearHistory"
              >
                <el-icon><Delete /></el-icon>
              </el-button>
            </div>
            <ul class="search-history__list">
              <li
                v-for="(item, index) in searchHistory"
                :key="index"
                class="search-history__item"
                @click="navigateToRoute(item)"
              >
                <div class="search-history__icon">
                  <el-icon><Clock /></el-icon>
                </div>
                <span class="search-history__name">{{ item.title }}</span>
                <div class="search-history__action">
                  <el-icon @click.stop="removeHistoryItem(index)"><Close /></el-icon>
                </div>
              </li>
            </ul>
          </div>
        </template>

        <!-- 搜索结果 -->
        <template v-else>
          <ul v-if="displayResults.length > 0">
            <li
              v-for="(item, index) in displayResults"
              :key="item.path"
              :class="[
                'search-result__item',
                {
                  'search-result__item--active': index === activeIndex,
                },
              ]"
              @click="navigateToRoute(item)"
            >
              <el-icon v-if="item.icon && item.icon.startsWith('el-icon')">
                <component :is="item.icon.replace('el-icon-', '')" />
              </el-icon>
              <div v-else-if="item.icon" :class="`i-svg:${item.icon}`" />
              <div v-else class="i-svg:menu" />
              <span class="ml-2">{{ item.title }}</span>
            </li>
          </ul>
        </template>

        <!-- 无搜索历史显示 -->
        <div v-if="searchKeyword === '' && searchHistory.length === 0" class="no-history">
          <p class="no-history__text">没有搜索历史</p>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <div class="ctrl-k-hint">
            <span class="ctrl-k-text">Ctrl+K 快速打开</span>
          </div>
          <div class="shortcuts-group">
            <div class="key-box">
              <div class="key-btn">选择</div>
            </div>
            <div class="arrow-box">
              <div class="arrow-up-down">
                <div class="key-btn">
                  <div class="i-svg:up" />
                </div>
                <div class="key-btn ml-1">
                  <div class="i-svg:down" />
                </div>
              </div>
              <span class="key-text">切换</span>
            </div>
            <div class="key-box">
              <div class="key-btn esc-btn">ESC</div>
              <span class="key-text">关闭</span>
            </div>
          </div>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import router from "@/router";
import { usePermissionStore } from "@/store";
import { isExternal } from "@/utils";
import { RouteRecordRaw, LocationQueryRaw } from "vue-router";
import { Clock, Close, Delete } from "@element-plus/icons-vue";

const HISTORY_KEY = "menu_search_history";
const MAX_HISTORY = 5;

const permissionStore = usePermissionStore();
const isModalVisible = ref(false);
const searchKeyword = ref("");
const searchInputRef = ref();
const excludedRoutes = ref(["/redirect", "/login", "/401", "/404", "/500", "/:pathMatch(.*)*"]);
const menuItems = ref<SearchItem[]>([]);
const searchResults = ref<SearchItem[]>([]);
const activeIndex = ref(-1);
const searchHistory = ref<SearchItem[]>([]);

interface SearchItem {
  title: string;
  path: string;
  name?: string;
  icon?: string;
  redirect?: string;
  params?: LocationQueryRaw;
}

// 从本地存储加载搜索历史
function loadSearchHistory() {
  const historyStr = localStorage.getItem(HISTORY_KEY);
  if (historyStr) {
    try {
      searchHistory.value = JSON.parse(historyStr);
    } catch {
      searchHistory.value = [];
    }
  }
}

// 保存搜索历史到本地存储
function saveSearchHistory() {
  localStorage.setItem(HISTORY_KEY, JSON.stringify(searchHistory.value));
}

// 添加项目到搜索历史
function addToHistory(item: SearchItem) {
  // 检查是否已存在
  const index = searchHistory.value.findIndex((i) => i.path === item.path);

  // 如果存在则移除
  if (index !== -1) {
    searchHistory.value.splice(index, 1);
  }

  // 添加到历史开头
  searchHistory.value.unshift(item);

  // 限制历史记录数量
  if (searchHistory.value.length > MAX_HISTORY) {
    searchHistory.value = searchHistory.value.slice(0, MAX_HISTORY);
  }

  // 保存到本地存储
  saveSearchHistory();
}

// 移除历史记录项
function removeHistoryItem(index: number) {
  searchHistory.value.splice(index, 1);
  saveSearchHistory();
}

// 清空历史记录
function clearHistory() {
  searchHistory.value = [];
  localStorage.removeItem(HISTORY_KEY);
}

// 注册全局快捷键
function handleKeyDown(e: KeyboardEvent) {
  // 判断是否为Ctrl+K组合键
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
    e.preventDefault(); // 阻止默认行为
    openSearchModal();
  }
}

// 添加键盘事件监听
onMounted(() => {
  loadRoutes(permissionStore.routes);
  loadSearchHistory();
  document.addEventListener("keydown", handleKeyDown);
});

// 移除键盘事件监听
onBeforeUnmount(() => {
  document.removeEventListener("keydown", handleKeyDown);
});

// 打开搜索模态框
function openSearchModal() {
  searchKeyword.value = "";
  activeIndex.value = -1;
  isModalVisible.value = true;
  setTimeout(() => {
    searchInputRef.value.focus();
  }, 100);
}

// 关闭搜索模态框
function closeSearchModal() {
  isModalVisible.value = false;
}

// 更新搜索结果
function updateSearchResults() {
  activeIndex.value = -1;
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase();
    searchResults.value = menuItems.value.filter((item) =>
      item.title.toLowerCase().includes(keyword)
    );
  } else {
    searchResults.value = [];
  }
}

// 显示搜索结果
const displayResults = computed(() => searchResults.value);

// 执行搜索
function selectActiveResult() {
  if (displayResults.value.length > 0 && activeIndex.value >= 0) {
    navigateToRoute(displayResults.value[activeIndex.value]);
  }
}

// 导航搜索结果
function navigateResults(direction: string) {
  if (displayResults.value.length === 0) return;

  if (direction === "up") {
    activeIndex.value =
      activeIndex.value <= 0 ? displayResults.value.length - 1 : activeIndex.value - 1;
  } else if (direction === "down") {
    activeIndex.value =
      activeIndex.value >= displayResults.value.length - 1 ? 0 : activeIndex.value + 1;
  }
}

// 跳转到
function navigateToRoute(item: SearchItem) {
  closeSearchModal();
  // 添加到历史记录
  addToHistory(item);

  if (isExternal(item.path)) {
    window.open(item.path, "_blank");
  } else {
    router.push({ path: item.path, query: item.params });
  }
}

function loadRoutes(routes: RouteRecordRaw[], parentPath = "") {
  routes.forEach((route) => {
    // 计算完整路径
    const path = route.path.startsWith("/")
      ? route.path
      : `${parentPath}${parentPath.endsWith("/") ? "" : "/"}${route.path}`;

    // 检查是否需要排除
    if (excludedRoutes.value.includes(route.path) || isExternal(route.path) || route.meta?.hidden)
      return;

    // 处理有子路由的情况
    if (route.children) {
      // 如果父路由本身有title，也添加到menuItems中
      if (route.meta?.title) {
        const title = route.meta.title === "dashboard" ? "首页" : route.meta.title;
        menuItems.value.push({
          title,
          path,
          name: typeof route.name === "string" ? route.name : undefined,
          icon: route.meta.icon,
          redirect: typeof route.redirect === "string" ? route.redirect : undefined,
          params: route.meta.params
            ? JSON.parse(JSON.stringify(toRaw(route.meta.params)))
            : undefined,
        });
      }
      // 递归处理子路由
      loadRoutes(route.children, path);
    }
    // 处理没有子路由但有title的情况
    else if (route.meta?.title) {
      const title = route.meta.title === "dashboard" ? "首页" : route.meta.title;
      menuItems.value.push({
        title,
        path,
        name: typeof route.name === "string" ? route.name : undefined,
        icon: route.meta.icon,
        redirect: typeof route.redirect === "string" ? route.redirect : undefined,
        params: route.meta.params
          ? JSON.parse(JSON.stringify(toRaw(route.meta.params)))
          : undefined,
      });
    }
  });
}
</script>

<style scoped lang="scss">
.command-palette-trigger {
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: space-between;
  height: 32px;
  padding: 0 12px;
  user-select: none;
  background: var(--el-fill-color-light);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 999px;
}

.command-palette-trigger__left {
  display: flex;
  gap: 8px;
  align-items: center;
}

.command-palette-trigger__left :deep([class^="i-svg:"]) {
  color: var(--el-text-color-secondary) !important;
}

.command-palette-trigger__text {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  white-space: nowrap;
}

.command-palette-trigger__kbd {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 2px 8px;
  font-size: 12px;
  line-height: 1;
  color: var(--el-text-color-secondary);
  white-space: nowrap;
  background: var(--el-bg-color-overlay);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 8px;
}

.command-palette-trigger:focus-visible {
  outline: 2px solid var(--el-color-primary);
  outline-offset: 2px;
}

.command-palette-trigger:hover {
  border-color: var(--el-border-color);
}

.search-result {
  max-height: 400px;
  overflow-y: auto;

  ul {
    padding: 0;
    margin: 0;
    list-style: none;
  }

  &__item {
    display: flex;
    align-items: center;
    padding: 10px;
    text-align: left;
    cursor: pointer;

    &--active {
      color: var(--el-color-primary);
      background-color: var(--el-menu-hover-bg-color);
    }
  }
}

/* 搜索历史样式 */
.search-history {
  &__title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 12px;
    font-size: 12px;
    line-height: 34px;
    color: var(--el-text-color-secondary);
  }

  &__clear {
    padding: 2px;
    font-size: 12px;

    &:hover {
      color: var(--el-color-danger);
    }
  }

  &__list {
    padding: 0;
    margin: 0;
  }

  &__icon {
    display: flex;
    align-items: center;
    margin-right: 10px;
    font-size: 16px;
    color: var(--el-text-color-secondary);
  }

  &__name {
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 14px;
    color: var(--el-text-color-primary);
    white-space: nowrap;
  }

  &__action {
    padding: 4px;
    color: var(--el-text-color-secondary);
    border-radius: 4px;
    opacity: 0;
    transition: opacity 0.2s;

    &:hover {
      color: var(--el-color-danger);
      background-color: var(--el-fill-color);
    }
  }

  &__item {
    display: flex;
    align-items: center;
    height: 40px;
    padding: 0 12px;
    cursor: pointer;

    &:hover {
      background-color: var(--el-fill-color-light);

      .search-history__action {
        opacity: 1;
      }
    }
  }
}

/* 没有搜索历史时的样式 */
.no-history {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100px;

  &__text {
    font-size: 14px;
    color: var(--el-text-color-secondary);
  }
}

.dialog-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.shortcuts-group {
  display: flex;
  gap: 15px;
  align-items: center;
}

.key-box {
  display: flex;
  gap: 5px;
  align-items: center;
}

.arrow-box {
  display: flex;
  gap: 5px;
  align-items: center;
}

.arrow-up-down {
  display: flex;
  gap: 2px;
  align-items: center;
}

.key-btn {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 32px;
  height: 20px;
  padding: 0 4px;
  font-size: 12px;
  color: var(--el-text-color-regular);
  background-color: var(--el-fill-color-blank);
  border: 1px solid var(--el-border-color);
  border-radius: 3px;
  box-shadow: var(--el-box-shadow-light);
}

.esc-btn {
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
  font-size: 11px;
}

.key-text {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.ctrl-k-hint {
  display: flex;
  align-items: center;
}

.ctrl-k-text {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

// 适配Element Plus对话框
:deep(.el-dialog__footer) {
  box-sizing: border-box;
  padding-top: 10px;
  text-align: right;
}
</style>
