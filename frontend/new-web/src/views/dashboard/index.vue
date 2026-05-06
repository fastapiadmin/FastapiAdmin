<template>
  <div class="workplace-page">
    <!-- 顶栏放入 gutter 行，与下方栅格列边缘对齐 -->
    <ElRow :gutter="16">
      <ElCol :span="24">
        <ElCard shadow="hover" class="workplace-hero-card workplace-surface">
          <div class="workplace-hero">
            <div class="flex flex-wrap items-center gap-4 min-w-0 flex-1">
              <div class="flex items-center md:mb-0">
                <div class="workplace-hero__avatar-wrap">
                  <ElAvatar
                    v-if="currentUser.avatar"
                    size="large"
                    :src="currentUser.avatar"
                    class="workplace-hero__avatar"
                  />
                  <ElIcon v-else :size="40" class="text-secondary workplace-hero__avatar-fallback">
                    <UserFilled />
                  </ElIcon>
                </div>
                <div>
                  <div class="workplace-hero__greeting">
                    {{ timefix }}{{ currentUser.name }}，{{ welcome }}
                  </div>
                  <ElText class="workplace-hero__meta">
                    {{ currentUser.username }} · {{ currentUser.dept_name }} ·
                    {{ currentUser.description }}
                  </ElText>
                </div>
              </div>
            </div>
            <div class="workplace-hero__actions">
              <div class="workplace-hero__login">
                <div class="workplace-hero__login-label">最近登录</div>
                <div class="workplace-hero__login-time">{{ currentUser.last_login }}</div>
              </div>
            </div>
          </div>
        </ElCard>
      </ElCol>
    </ElRow>

    <ElRow :gutter="16" class="mt-4 workplace-module-row">
      <ElCol :xs="24" :lg="16">
        <ElCard class="workplace-modules-card workplace-surface" shadow="hover">
          <template #header>
            <div>
              <span class="workplace-panel-title">模块入口</span>
              <p class="workplace-section-sub workplace-section-sub--inline">
                按业务域进入；灰色表示暂无该域权限（完整列表见左侧导航）
              </p>
            </div>
          </template>
          <div class="workplace-module-grid">
            <div
              v-for="mod in moduleGroupEntries"
              :key="mod.key"
              class="workplace-module-card"
              :class="{ 'is-disabled': !mod.entryPath }"
              role="button"
              :tabindex="mod.entryPath ? 0 : -1"
              @click="goModuleEntry(mod.entryPath)"
              @keydown.enter.prevent="goModuleEntry(mod.entryPath)"
              @keydown.space.prevent="goModuleEntry(mod.entryPath)"
            >
              <div class="workplace-module-card__icon">
                <ElIcon :size="26">
                  <component :is="moduleGroupIcons[mod.key as keyof typeof moduleGroupIcons]" />
                </ElIcon>
              </div>
              <div class="workplace-module-card__body">
                <span class="workplace-module-card__name">{{ mod.title }}</span>
                <span class="workplace-module-card__desc">{{ mod.subtitle }}</span>
                <span v-if="mod.entryPath" class="workplace-module-card__hint">
                  将进入：{{ mod.entryLabel || "—" }}
                </span>
                <span v-else class="workplace-module-card__hint workplace-module-card__hint--muted">
                  暂无该域权限
                </span>
              </div>
              <ElIcon class="workplace-module-card__arrow" :size="16">
                <Right />
              </ElIcon>
            </div>
          </div>
        </ElCard>
      </ElCol>
      <ElCol :xs="24" :lg="8" class="workplace-bookmarks-col">
        <ElCard class="workplace-bookmarks-card workplace-surface" shadow="hover">
          <template #header>
            <div class="workplace-bookmarks-card__header">
              <div>
                <span class="workplace-panel-title workplace-bookmarks-card__title-line">
                  <ElIcon class="workplace-bookmarks-card__star" :size="18"><Star /></ElIcon>
                  我的收藏
                  <ElTag
                    v-if="quickLinks.length > 0"
                    type="info"
                    size="small"
                    effect="plain"
                    round
                    class="workplace-bookmarks-card__count"
                  >
                    {{ quickLinks.length }}/{{ QUICK_LINK_MAX }}
                  </ElTag>
                </span>
                <p class="workplace-section-sub workplace-section-sub--inline">
                  最多 {{ QUICK_LINK_MAX }} 个 · 标签栏星标添加 · 仅本机
                </p>
              </div>
              <div class="workplace-bookmarks-card__header-actions">
                <ElTooltip content="在顶部标签栏左侧星标上点击，可加入或取消收藏" placement="top">
                  <ElIcon class="workplace-module-bookmarks__help" :size="15">
                    <QuestionFilled />
                  </ElIcon>
                </ElTooltip>
                <ElButton size="small" type="danger" plain @click="clearBookmarks()">
                  <ElIcon><Delete /></ElIcon>
                  {{ t("common.clear") }}
                </ElButton>
              </div>
            </div>
          </template>
          <div class="workplace-module-bookmarks">
            <template v-if="quickLinks.length > 0">
              <div class="workplace-quick-list workplace-quick-list--hub">
                <ElTooltip
                  v-for="(item, index) in quickLinks"
                  :key="item.id || `${item.href}-${index}`"
                  placement="top"
                  :show-after="400"
                  :content="item.title"
                >
                  <div
                    class="workplace-quick-row workplace-quick-row--compact workplace-quick-row--chip"
                    role="button"
                    tabindex="0"
                    @click="handleQuickLinkClick(item)"
                    @keydown.enter.prevent="handleQuickLinkClick(item)"
                    @keydown.space.prevent="handleQuickLinkClick(item)"
                  >
                    <span
                      class="workplace-quick-row__accent"
                      :style="{
                        backgroundColor: getQuickLinkColor(getQuickLinkStableIndex(item)),
                      }"
                    />
                    <div
                      class="workplace-quick-row__icon"
                      :style="{ color: getQuickLinkColor(getQuickLinkStableIndex(item)) }"
                    >
                      <MenuRouteIcon :icon="item.icon || 'menu'" />
                    </div>
                    <div class="workplace-quick-row__text">
                      <span class="workplace-quick-row__title">{{ item.title }}</span>
                    </div>
                    <div class="workplace-quick-row__actions">
                      <button
                        type="button"
                        class="workplace-quick-row__remove"
                        :disabled="!item.id && !item.href"
                        :title="item.id || item.href ? '移除收藏' : '无法移除（缺少路径）'"
                        :aria-label="`移除收藏 ${item.title}`"
                        @click.stop="handleDeleteLink(item)"
                      >
                        <ElIcon><Close /></ElIcon>
                      </button>
                    </div>
                  </div>
                </ElTooltip>
              </div>
            </template>
            <ElEmpty v-else :image-size="48" class="workplace-module-bookmarks__empty">
              <template #description>
                <p class="workplace-quick-empty__title">暂无收藏</p>
                <p class="workplace-quick-empty__hint">
                  在顶部
                  <strong>标签栏</strong>
                  左侧星标点击添加
                </p>
              </template>
            </ElEmpty>
          </div>
        </ElCard>
      </ElCol>
    </ElRow>

    <!-- 日程日历 + 系统日志 + 消息（大屏三列，日历限宽；小屏纵向堆叠） -->
    <div class="mt-4 workplace-ops-stack">
      <ElRow :gutter="16" class="workplace-ops-row">
        <ElCol :xs="24" :lg="7" class="workplace-ops-col workplace-ops-col--calendar">
          <ElCard
            shadow="hover"
            class="workplace-calendar-card workplace-surface workplace-ops-card"
          >
            <template #header>
              <div class="workplace-section-card__head">
                <div>
                  <span class="workplace-panel-title">日程日历</span>
                  <p class="workplace-section-sub workplace-section-sub--inline">
                    点击日期添加或编辑（本地演示）
                  </p>
                </div>
              </div>
            </template>
            <div class="workplace-ops-card__body workplace-ops-card__body--calendar">
              <HomeCalendar />
            </div>
          </ElCard>
        </ElCol>

        <ElCol :xs="24" :lg="10" class="workplace-ops-col">
          <ElCard
            shadow="hover"
            class="workplace-section-card workplace-surface workplace-ops-card"
          >
            <template #header>
              <div class="workplace-section-card__head">
                <div>
                  <span class="workplace-panel-title">系统日志</span>
                  <p class="workplace-section-sub workplace-section-sub--inline">
                    已加载 {{ systemLogs.length }} 条 · 默认 10 条
                  </p>
                </div>
                <div class="workplace-section-card__actions">
                  <ElButton
                    v-if="systemLogs.length > 10"
                    type="primary"
                    link
                    @click="logsExpanded = !logsExpanded"
                  >
                    {{ logsExpanded ? "收起" : "展开全部" }}
                  </ElButton>
                  <ElButton type="primary" link @click="goToLog()">日志管理</ElButton>
                </div>
              </div>
            </template>
            <div
              v-loading="logsLoading"
              class="workplace-ops-card__body workplace-ops-card__body--logs"
            >
              <ElEmpty
                v-if="!logsLoading && systemLogs.length === 0"
                :image-size="72"
                description="暂无日志"
              />
              <div v-else class="workplace-logs-scroll">
                <ElTable
                  :data="displayedLogs"
                  class="workplace-logs-table"
                  size="small"
                  :max-height="logsExpanded ? 360 : 220"
                >
                  <ElTableColumn label="类型" width="72" align="center">
                    <template #default="{ row }">
                      <ElTag :type="row.type === 1 ? 'success' : 'primary'" size="small">
                        {{ row.type === 1 ? "登录" : "操作" }}
                      </ElTag>
                    </template>
                  </ElTableColumn>
                  <ElTableColumn
                    label="路径"
                    prop="request_path"
                    min-width="120"
                    show-overflow-tooltip
                  />
                  <ElTableColumn label="方法" width="72" align="center">
                    <template #default="{ row }">
                      <ElTag :type="getMethodType(row.request_method)" size="small">
                        {{ row.request_method || "—" }}
                      </ElTag>
                    </template>
                  </ElTableColumn>
                  <ElTableColumn label="状态" width="64" align="center">
                    <template #default="{ row }">
                      <ElTag :type="getStatusCodeType(row.response_code)" size="small">
                        {{ row.response_code ?? "—" }}
                      </ElTag>
                    </template>
                  </ElTableColumn>
                  <ElTableColumn
                    label="IP"
                    prop="request_ip"
                    min-width="100"
                    show-overflow-tooltip
                  />
                  <ElTableColumn
                    label="时间"
                    prop="created_time"
                    min-width="136"
                    show-overflow-tooltip
                  />
                </ElTable>
              </div>
            </div>
          </ElCard>
        </ElCol>

        <ElCol :xs="24" :lg="7" class="workplace-ops-col">
          <ElCard
            shadow="hover"
            class="workplace-section-card workplace-surface workplace-ops-card"
          >
            <template #header>
              <div class="workplace-section-card__head">
                <div>
                  <span class="workplace-panel-title">最新消息</span>
                  <p class="workplace-section-sub workplace-section-sub--inline">
                    公告与通知 · 最近 5 条
                  </p>
                </div>
                <ElButton type="primary" link @click="goToNotice()">公告管理</ElButton>
              </div>
            </template>
            <div class="workplace-ops-card__body workplace-ops-card__body--notices">
              <ElEmpty v-if="noticeList.length === 0" :image-size="80" description="暂无数据" />
              <ElTimeline v-else class="workplace-notice-timeline">
                <ElTimelineItem
                  v-for="(item, index) in noticePreviewList"
                  :key="item.id"
                  :type="index === 0 ? 'primary' : 'info'"
                >
                  <div class="workplace-notice-card">
                    <div class="workplace-notice-card__head">
                      <div class="workplace-notice-card__titles">
                        <span class="workplace-notice-card__title">
                          {{ item.notice_title }}
                        </span>
                        <ElTag size="small" :type="getNoticeTypeColor(item.notice_type)">
                          {{ getNoticeTypeText(item.notice_type) }}
                        </ElTag>
                      </div>
                      <span class="workplace-notice-card__time">
                        {{ formatTime(item.created_time) }}
                      </span>
                    </div>
                    <div class="workplace-notice-card__content">
                      {{ item.notice_content }}
                    </div>
                    <div class="workplace-notice-card__foot">
                      <span class="workplace-notice-card__author">
                        {{ item.created_by?.name }} 发布
                      </span>
                      <ElTooltip placement="top" :content="item.description || item.notice_content">
                        <ElButton target="_blank" type="primary" link @click="goToNotice()">
                          详情↗
                        </ElButton>
                      </ElTooltip>
                    </div>
                  </div>
                </ElTimelineItem>
              </ElTimeline>
            </div>
          </ElCard>
        </ElCol>
      </ElRow>
    </div>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "Home",
  inheritAttrs: false,
});

import { useUserStore } from "@/store/index";
import MenuRouteIcon from "@/components/MenuRouteIcon/index.vue";
import HomeCalendar from "./components/HomeCalendar.vue";
import { greetings } from "@/utils/common";
import NoticeAPI, { NoticeTable } from "@/api/module_system/notice";
import LogAPI, { type LogTable } from "@/api/module_system/log";
import type { MenuTable } from "@/api/module_system/menu";
import { ref, onMounted, onUnmounted, computed } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import {
  Delete,
  UserFilled,
  Close,
  Setting,
  Monitor,
  Timer,
  ChatDotRound,
  Cpu,
  Reading,
  Right,
  Star,
  QuestionFilled,
} from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { quickStartManager, QUICK_LINK_MAX, type QuickLink } from "@/utils/common";

/**
 * 工作台「模块总览」与 src/views 下目录对应：
 * module_system / module_monitor / module_task / module_ai / module_application / module_generator / module_example / module_common
 */
interface MenuLeaf {
  title: string;
  path: string;
  icon?: string;
  component_path?: string;
  order?: number;
}

interface WorkplaceModuleGroup {
  key: string;
  title: string;
  subtitle: string;
  /** 与菜单 component_path 片段匹配（含 views 相对路径） */
  matchHints: string[];
}

/** 按「业务域」划分，与前端 views 目录一致 */
const WORKPLACE_MODULE_GROUPS: WorkplaceModuleGroup[] = [
  {
    key: "system",
    title: "系统管理",
    subtitle: "用户、角色、菜单、部门、字典、岗位、参数、公告、日志等",
    matchHints: ["module_system/"],
  },
  {
    key: "monitor",
    title: "监控运维",
    subtitle: "服务监控、缓存、在线用户、资源占用等",
    matchHints: ["module_monitor/"],
  },
  {
    key: "task",
    title: "任务与流程",
    subtitle: "定时任务、执行节点、工作流等",
    matchHints: ["module_task/"],
  },
  {
    key: "ai",
    title: "AI 助手",
    subtitle: "对话、记忆管理等",
    matchHints: ["module_ai/"],
  },
  {
    key: "app",
    title: "应用与生成",
    subtitle: "应用管理、代码生成、示例演示等",
    matchHints: ["module_application/", "module_generator/", "module_example/"],
  },
  {
    key: "docs",
    title: "文档中心",
    subtitle: "Swagger / Redoc / 本地文档等",
    matchHints: ["module_common/"],
  },
];

function normalizePath(p: string) {
  return p.replace(/\\/g, "/");
}

/**
 * 在已授权的叶子菜单中，按 matchHints 顺序找到第一个可进入的路由
 */
function resolveEntryPath(
  leaves: Pick<MenuLeaf, "path" | "component_path">[],
  hints: string[]
): string | undefined {
  for (const hint of hints) {
    const hit = leaves.find(
      (l) => l.component_path && normalizePath(l.component_path).includes(hint)
    );
    if (hit) return hit.path;
  }
  return undefined;
}

function resolveEntryTitle(leaves: MenuLeaf[], hints: string[]): string | undefined {
  for (const hint of hints) {
    const hit = leaves.find(
      (l) => l.component_path && normalizePath(l.component_path).includes(hint)
    );
    if (hit) return hit.title;
  }
  return undefined;
}

/** 叶子菜单扁平化（与侧栏同源），按菜单 order 排序 */
function flattenLeafMenusFromTree(menus: MenuTable[]): MenuLeaf[] {
  const seen = new Set<string>();
  const out: MenuLeaf[] = [];
  const walk = (items: MenuTable[]) => {
    for (const m of items) {
      if (m.hidden) continue;
      if (m.children?.length) {
        walk(m.children);
      } else if (m.title && m.route_path) {
        const raw = m.route_path.trim();
        const path = raw.startsWith("/") ? raw : `/${raw}`;
        if (seen.has(path)) continue;
        seen.add(path);
        out.push({
          title: m.title,
          path,
          icon: m.icon,
          component_path: m.component_path,
          order: m.order,
        });
      }
    }
  };
  walk(menus);
  out.sort((a, b) => (a.order ?? 0) - (b.order ?? 0));
  return out;
}

const userStore = useUserStore();
const timefix = greetings();
const { t } = useI18n();
const router = useRouter();

// 通知公告数据（需早于 noticePreviewList）
const noticeList = ref<NoticeTable[]>([]);

const systemLogs = ref<LogTable[]>([]);
const logsLoading = ref(false);
const logsExpanded = ref(false);
const displayedLogs = computed(() => {
  if (logsExpanded.value || systemLogs.value.length <= 10) return systemLogs.value;
  return systemLogs.value.slice(0, 10);
});

const moduleGroupIcons = {
  system: Setting,
  monitor: Monitor,
  task: Timer,
  ai: ChatDotRound,
  app: Cpu,
  docs: Reading,
};

/** 叶子菜单（与侧栏同源），用于模块域入口解析 */
const allMenuLeaves = computed(() => flattenLeafMenusFromTree(userStore.routeList));

const moduleGroupEntries = computed(() => {
  const leaves = allMenuLeaves.value;
  return WORKPLACE_MODULE_GROUPS.map((g) => ({
    ...g,
    entryPath: resolveEntryPath(leaves, g.matchHints),
    entryLabel: resolveEntryTitle(leaves, g.matchHints),
  }));
});

function goModuleEntry(path: string | undefined) {
  if (!path) {
    ElMessage.info("当前账号在该模块暂无可用入口，请联系管理员分配权限");
    return;
  }
  goMenuShortcut(path);
}

const noticePreviewList = computed(() => noticeList.value.slice(0, 5));

function goMenuShortcut(path: string) {
  if (!path) return;
  router.push(path).catch(() => {
    ElMessage.warning("无法打开该页面，请检查路由配置");
  });
}

// 快速链接数据
const quickLinks = ref<QuickLink[]>(quickStartManager.getQuickLinks());

// 格式化时间
const formatTime = (time: string | undefined) => {
  if (!time) return "";
  const date = new Date(time);
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  const minutes = Math.floor(diff / (1000 * 60));
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));

  if (minutes < 1) return "刚刚";
  if (minutes < 60) return `${minutes}分钟前`;
  if (hours < 24) return `${hours}小时前`;
  if (days < 7) return `${days}天前`;
  return date.toLocaleDateString();
};

// 跳转通知公告详情页
const goToNotice = () => {
  router.push({ name: "Notice" }).catch(() => {
    ElMessage.warning(`公告通知跳转失败，请检查路由配置`);
  });
};

function goToLog() {
  router.push({ name: "Log" }).catch(() => {
    ElMessage.warning("日志管理页跳转失败，请检查路由配置");
  });
}

function getStatusCodeType(code?: number): "success" | "warning" | "info" | "danger" {
  if (code === undefined) return "info";
  if (code >= 200 && code < 300) return "success";
  if (code >= 300 && code < 400) return "warning";
  return "danger";
}

function getMethodType(method?: string): "success" | "warning" | "info" | "danger" {
  if (method === undefined) return "info";
  if (method === "GET") return "info";
  if (method === "POST") return "success";
  if (method === "PUT" || method === "PATCH") return "warning";
  if (method === "DELETE") return "danger";
  return "info";
}

async function fetchSystemLogs() {
  logsLoading.value = true;
  try {
    const res = await LogAPI.listLog({ page_no: 1, page_size: 50 });
    if (res.data.code === 0) {
      systemLogs.value = res.data.data?.items ?? [];
    }
  } catch (e) {
    console.error("工作台加载系统日志失败:", e);
  } finally {
    logsLoading.value = false;
  }
}

// 获取通知类型文本和颜色
const getNoticeTypeText = (type: string | undefined) => {
  switch (type) {
    case "1":
      return "通知";
    case "2":
      return "公告";
    default:
      return "通知";
  }
};

// 获取通知类型对应的标签颜色
const getNoticeTypeColor = (type: string | undefined) => {
  switch (type) {
    case "1":
      return "primary";
    case "2":
      return "success";
    default:
      return "primary";
  }
};

// 获取通知公告列表
const listNotice = async () => {
  try {
    const response = await NoticeAPI.listNotice({
      page_no: 1,
      page_size: 5,
      status: "0", // 只获取启用的公告
    });
    if (response.data.code === 0) {
      noticeList.value = response.data.data.items;
    }
  } catch (error) {
    console.error("获取通知公告失败:", error);
  }
};

// 处理快速链接点击
const handleQuickLinkClick = (item: QuickLink) => {
  if (item.href) {
    router.push(item.href).catch(() => {
      ElMessage.warning(`路由 ${item.href} 不存在，请检查配置`);
    });
  } else {
    ElMessage.info(`${item.title} 功能待开发`);
  }
};

/** 与主题协调的固定色板，按索引循环，避免随机色闪烁 */
const QUICK_LINK_PALETTE = ["#4080ff", "#23c343", "#ff9a2e", "#f76560", "#a9aeb8", "#00b42a"];

function getQuickLinkColor(index: number) {
  return QUICK_LINK_PALETTE[index % QUICK_LINK_PALETTE.length];
}

/** 列表中颜色与顺序与「全部收藏」一致，筛选后仍稳定 */
function getQuickLinkStableIndex(item: QuickLink): number {
  const list = quickLinks.value;
  const i = list.findIndex((l) =>
    l.id != null && l.id !== "" ? l.id === item.id : l.href === item.href
  );
  return i >= 0 ? i : 0;
}

// 处理删除链接
const handleDeleteLink = (item: QuickLink) => {
  ElMessageBox.confirm(`确定要取消收藏"${item.title}"吗？`, "取消收藏确认", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      if (item.id) {
        quickStartManager.removeQuickLink(item.id);
      } else if (item.href) {
        quickStartManager.removeQuickLinkByHref(item.href);
      } else {
        ElMessage.warning("无法移除：缺少标识");
        return;
      }
      ElMessage.success(`已取消收藏：${item.title}`);
    })
    .catch(() => {
      // 用户取消删除
    });
};

const clearBookmarks = () => {
  ElMessageBox.confirm("确定要清空收藏吗？", "清空收藏确认", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      quickStartManager.clearQuickLinks();
      ElMessage.success("已清空收藏");
    })
    .catch(() => {});
};

// 监听快速链接变化
const updateQuickLinks = (links: QuickLink[]) => {
  quickLinks.value = links;
};

// 组件挂载时获取数据和添加监听器
onMounted(() => {
  listNotice();
  fetchSystemLogs();
  quickStartManager.addListener(updateQuickLinks);
});

// 组件卸载时移除监听器
onUnmounted(() => {
  quickStartManager.removeListener(updateQuickLinks);
});

const welcome = "祝你开心每一天！";

const currentUser = {
  avatar:
    userStore.basicInfo.avatar ||
    "https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png",
  name: userStore.basicInfo.name || "吴彦祖",
  username: userStore.basicInfo.username || "账号信息",
  description: userStore.basicInfo.description || "用户说明",
  dept_name: userStore.basicInfo.dept_name || "软件专业部",
  last_login: userStore.basicInfo.last_login || "2023-01-01 00:00:00",
};
</script>

<style scoped lang="scss">
.workplace-section-sub {
  margin: 4px 0 0;
  font-size: 12px;
  font-weight: normal;
  line-height: 1.45;
  color: var(--el-text-color-secondary);
}

.workplace-section-sub--inline {
  margin: 2px 0 0;
}

.workplace-page {
  --workplace-radius: 12px;
  --workplace-radius-sm: 10px;

  display: flex;
  flex-direction: column;
  min-width: 0;
}

/* 与上方模块区隔离，两行 ops 之间固定间距，避免与下方栅格视觉「叠在一起」 */
.workplace-ops-stack {
  display: flex;
  flex-shrink: 0;
  flex-direction: column;
  gap: 16px;
  width: 100%;
}

.workplace-surface {
  overflow: hidden;
  border: 1px solid var(--el-border-color-lighter);
  border-radius: var(--workplace-radius);

  :deep(.el-card__header) {
    border-bottom-color: var(--el-border-color-extra-light);
  }
}

.workplace-calendar-card {
  :deep(.el-card__body) {
    padding: 8px 10px 10px;
  }
}

/* 与日志/消息同排时限高；列变窄后不再占满屏宽 */
.workplace-ops-col--calendar {
  max-width: 100%;
}

.workplace-ops-card__body--calendar {
  max-height: min(300px, 36vh);
  overflow: auto;
}

.workplace-panel-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  letter-spacing: 0.02em;
}

/* —— 顶栏 —— */
.workplace-hero-card {
  :deep(.el-card__body) {
    padding: 20px 22px;
  }
}

.workplace-hero__avatar-wrap {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  margin-right: 18px;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 50%;
  box-shadow: 0 2px 8px rgb(0 0 0 / 5%);
}

.workplace-hero__avatar {
  border: 2px solid var(--el-bg-color);
}

.workplace-hero__avatar-fallback {
  opacity: 0.55;
}

.workplace-hero__greeting {
  margin-bottom: 6px;
  font-size: 20px;
  font-weight: 700;
  line-height: 1.3;
  color: var(--el-text-color-primary);
}

.workplace-hero__meta {
  font-size: 13px;
  line-height: 1.5;
  color: var(--el-text-color-secondary);
}

.workplace-hero__login {
  min-width: 168px;
  padding: 12px 16px;
  text-align: right;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: var(--workplace-radius-sm);
  box-shadow: 0 1px 3px rgb(0 0 0 / 4%);
}

.workplace-hero__login-label {
  margin-bottom: 4px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.workplace-hero__login-time {
  font-size: 17px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  color: var(--el-text-color-primary);
}

.workplace-logs-table {
  width: 100%;
}

/* ========== 模块入口 / 收藏：各为独立卡片（同行等高） ========== */
.workplace-module-row {
  align-items: stretch;
}

.workplace-module-row > .el-col {
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.workplace-modules-card,
.workplace-bookmarks-card {
  display: flex;
  flex: 1;
  flex-direction: column;
  width: 100%;
  min-height: 0;
}

.workplace-modules-card {
  :deep(.el-card__body) {
    display: flex;
    flex: 1;
    flex-direction: column;
    min-height: 0;
    padding: 16px 18px 18px;
  }
}

.workplace-bookmarks-col {
  @media (width <= 991px) {
    margin-top: 16px;
  }
}

.workplace-bookmarks-card {
  :deep(.el-card__body) {
    display: flex;
    flex: 1;
    flex-direction: column;
    min-height: 0;
    padding: 12px 16px 16px;
  }
}

.workplace-bookmarks-card__header {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 12px;
  align-items: flex-start;
  justify-content: space-between;
}

.workplace-bookmarks-card__title-line {
  display: inline-flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.workplace-bookmarks-card__star {
  flex-shrink: 0;
  color: var(--el-color-warning);
}

.workplace-bookmarks-card__count {
  height: 22px;
  font-variant-numeric: tabular-nums;
}

.workplace-bookmarks-card__header-actions {
  display: flex;
  flex-shrink: 0;
  gap: 8px;
  align-items: center;
}

.workplace-module-bookmarks {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
}

.workplace-module-bookmarks__help {
  flex-shrink: 0;
  color: var(--el-text-color-secondary);
  cursor: help;
}

.workplace-module-bookmarks__empty {
  padding: 12px 0;
}

.workplace-module-grid {
  display: grid;
  flex: 1;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  align-content: start;
  min-height: 0;
}

@media (width >= 1400px) {
  .workplace-modules-card .workplace-module-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (width <= 520px) {
  .workplace-modules-card .workplace-module-grid {
    grid-template-columns: 1fr;
  }
}

.workplace-section-card {
  :deep(.el-card__body) {
    padding: 12px 18px 18px;
  }
}

.workplace-section-card__head {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: flex-start;
  justify-content: space-between;
  width: 100%;
}

.workplace-section-card__actions {
  display: flex;
  flex-shrink: 0;
  flex-wrap: wrap;
  gap: 4px;
  align-items: center;
}

/* 运行快照+任务、日志+消息：每行两列并排 */
.workplace-ops-row {
  row-gap: 16px;
  align-items: stretch;
  width: 100%;
}

.workplace-ops-col {
  display: flex;
  min-width: 0;
}

.workplace-ops-card {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-width: 0;

  :deep(.el-card__body) {
    display: flex;
    flex: 1;
    flex-direction: column;
    min-height: 0;
  }
}

.workplace-ops-card__body {
  flex: 1;
  min-height: 0;
}

.workplace-ops-card__body--logs {
  min-width: 0;
}

.workplace-ops-card__body--notices {
  max-height: min(520px, 62vh);
  padding-right: 2px;
  overflow: hidden auto;
}

.workplace-logs-scroll {
  width: 100%;
  min-width: 0;
  overflow-x: auto;
}

.workplace-notice-timeline {
  padding-left: 2px;
}

.workplace-module-card {
  position: relative;
  display: flex;
  gap: 12px;
  align-items: flex-start;
  min-height: 108px;
  padding: 14px 36px 14px 14px;
  cursor: pointer;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: var(--workplace-radius-sm);
  transition:
    border-color 0.2s,
    box-shadow 0.2s,
    background 0.2s,
    transform 0.15s ease;

  &:focus-visible {
    outline: none;
    box-shadow: 0 0 0 2px var(--el-color-primary-light-7);
  }

  &:not(.is-disabled):hover {
    background: var(--el-bg-color);
    border-color: var(--el-color-primary-light-5);
    box-shadow: 0 6px 20px rgb(0 0 0 / 6%);
    transform: translateY(-1px);
  }

  &.is-disabled {
    cursor: not-allowed;
    opacity: 0.72;
  }
}

.workplace-module-card__icon {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  color: var(--el-color-primary);
  background: var(--el-color-primary-light-9);
  border-radius: 12px;
}

.workplace-module-card.is-disabled .workplace-module-card__icon {
  color: var(--el-text-color-disabled);
  background: var(--el-fill-color-light);
}

.workplace-module-card__body {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}

.workplace-module-card__name {
  font-size: 15px;
  font-weight: 600;
  line-height: 1.3;
  color: var(--el-text-color-primary);
}

.workplace-module-card__desc {
  font-size: 12px;
  line-height: 1.45;
  color: var(--el-text-color-secondary);
}

.workplace-module-card__hint {
  font-size: 11px;
  line-height: 1.35;
  color: var(--el-color-primary);
}

.workplace-module-card__hint--muted {
  color: var(--el-text-color-placeholder);
}

.workplace-module-card__arrow {
  position: absolute;
  top: 50%;
  right: 12px;
  color: var(--el-text-color-placeholder);
  transform: translateY(-50%);
}

.workplace-module-card:not(.is-disabled):hover .workplace-module-card__arrow {
  color: var(--el-color-primary);
}

.workplace-notice-card {
  padding: 14px 16px;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: var(--workplace-radius-sm);
  box-shadow: 0 1px 3px rgb(0 0 0 / 4%);
  transition:
    border-color 0.2s,
    box-shadow 0.2s;

  &:hover {
    border-color: var(--el-color-primary-light-7);
    box-shadow: 0 4px 14px rgb(0 0 0 / 6%);
  }
}

.workplace-notice-card__head {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 10px;
}

.workplace-notice-card__titles {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  min-width: 0;
}

.workplace-notice-card__title {
  font-size: 15px;
  font-weight: 600;
  line-height: 1.35;
  color: var(--el-text-color-primary);
}

.workplace-notice-card__time {
  flex-shrink: 0;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.workplace-notice-card__content {
  display: -webkit-box;
  margin-bottom: 12px;
  overflow: hidden;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  font-size: 13px;
  line-height: 1.55;
  color: var(--el-text-color-regular);
  -webkit-box-orient: vertical;
}

.workplace-notice-card__foot {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
}

.workplace-notice-card__author {
  color: var(--el-text-color-secondary);
}

/* ========== 顶栏问候 ========== */
.workplace-hero {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: flex-start;
  justify-content: space-between;
}

.workplace-hero__actions {
  display: flex;
  flex-shrink: 0;
  flex-wrap: wrap;
  gap: 16px 20px;
  align-items: flex-start;
  justify-content: flex-end;
}

.workplace-quick-empty__title {
  margin: 0 0 8px;
  font-size: 14px;
  color: var(--el-text-color-regular);
}

.workplace-quick-empty__hint {
  margin: 0;
  font-size: 13px;
  line-height: 1.55;
  color: var(--el-text-color-secondary);
}

.workplace-quick-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* 3 列 × 最多 5 排固定高度（15 格）；窄屏 2 列时 15 个占 8 排 */
.workplace-quick-list--hub {
  --hub-row-h: 38px;
  --hub-gap: 8px;

  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  grid-auto-rows: var(--hub-row-h);
  gap: var(--hub-gap);
  align-content: start;

  /* 正好 5 排所占高度：5 行 + 4 道行间距 */
  min-height: calc(5 * var(--hub-row-h) + 4 * var(--hub-gap));
}

@media (width <= 520px) {
  .workplace-quick-list--hub {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    min-height: calc(8 * var(--hub-row-h) + 7 * var(--hub-gap));
  }
}

.workplace-quick-row--compact {
  min-height: 44px;
  padding: 6px 8px 6px 4px;
}

.workplace-quick-row {
  position: relative;
  display: flex;
  gap: 10px;
  align-items: center;
  min-height: 56px;
  padding: 8px 10px 8px 6px;
  cursor: pointer;
  outline: none;
  background: var(--el-fill-color-blank);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: var(--el-border-radius-base);
  transition:
    border-color 0.2s,
    box-shadow 0.2s,
    background 0.2s;

  &:hover {
    background: var(--el-bg-color);
    border-color: var(--el-color-primary-light-5);
    box-shadow: var(--el-box-shadow-light);
  }

  &:focus-visible {
    border-color: var(--el-color-primary);
    box-shadow: 0 0 0 2px var(--el-color-primary-light-7);
  }
}

.workplace-quick-row__accent {
  flex-shrink: 0;
  align-self: stretch;
  width: 3px;
  min-height: 36px;
  border-radius: 2px;
}

.workplace-quick-row__icon {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  font-size: 22px;
  line-height: 1;
  background: var(--el-color-primary-light-9);
  border-radius: 10px;
}

.workplace-quick-row__text {
  flex: 1;
  min-width: 0;
}

.workplace-quick-row__title {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 13px;
  font-weight: 600;
  line-height: 1.35;
  color: var(--el-text-color-primary);
  white-space: nowrap;
}

.workplace-quick-row__actions {
  display: flex;
  flex-shrink: 0;
  gap: 2px;
  align-items: center;
}

.workplace-quick-row__remove {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  padding: 0;
  color: var(--el-text-color-secondary);
  cursor: pointer;
  background: transparent;
  border: 1px solid transparent;
  border-radius: 8px;
  transition:
    color 0.2s,
    background 0.2s,
    border-color 0.2s,
    opacity 0.2s;

  .workplace-quick-row--chip & {
    width: 26px;
    height: 26px;
  }

  &:disabled {
    cursor: not-allowed;
    opacity: 0.35;
  }

  &:hover:not(:disabled) {
    color: var(--el-color-danger);
    background: var(--el-color-danger-light-9);
    border-color: var(--el-color-danger-light-7);
  }
}

.workplace-quick-row--chip {
  min-width: 0;

  .workplace-quick-row__icon {
    width: 34px;
    height: 34px;
    font-size: 18px;
  }

  .workplace-quick-row__accent {
    min-height: 30px;
  }
}

/* 与 --hub-row-h 对齐，保证每排高度一致 */
.workplace-quick-list--hub .workplace-quick-row--compact {
  box-sizing: border-box;
  gap: 4px;
  height: 100%;
  min-height: 0;
  padding: 4px 4px 4px 2px;
}

.workplace-quick-list--hub .workplace-quick-row--chip .workplace-quick-row__icon {
  width: 26px;
  height: 26px;
  font-size: 14px;
}

.workplace-quick-list--hub .workplace-quick-row--chip .workplace-quick-row__accent {
  min-height: 24px;
}

.workplace-quick-list--hub .workplace-quick-row__title {
  font-size: 12px;
}
</style>
