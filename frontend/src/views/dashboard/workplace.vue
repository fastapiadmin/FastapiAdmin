<template>
  <div class="app-container workplace-page">
    <div>
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
                <el-icon v-else :size="40" class="text-secondary workplace-hero__avatar-fallback">
                  <UserFilled />
                </el-icon>
              </div>
              <div>
                <div class="workplace-hero__greeting">
                  {{ timefix }}{{ currentUser.name }}，{{ welcome }}
                </div>
                <el-text class="workplace-hero__meta">
                  {{ currentUser.username }} · {{ currentUser.dept_name }} ·
                  {{ currentUser.description }}
                </el-text>
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
                  <el-icon :size="26">
                    <component :is="moduleGroupIcons[mod.key as keyof typeof moduleGroupIcons]" />
                  </el-icon>
                </div>
                <div class="workplace-module-card__body">
                  <span class="workplace-module-card__name">{{ mod.title }}</span>
                  <span class="workplace-module-card__desc">{{ mod.subtitle }}</span>
                  <span v-if="mod.entryPath" class="workplace-module-card__hint">
                    将进入：{{ mod.entryLabel || "—" }}
                  </span>
                  <span
                    v-else
                    class="workplace-module-card__hint workplace-module-card__hint--muted"
                  >
                    暂无该域权限
                  </span>
                </div>
                <el-icon class="workplace-module-card__arrow" :size="16">
                  <Right />
                </el-icon>
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
                    <el-icon class="workplace-bookmarks-card__star" :size="18"><Star /></el-icon>
                    我的收藏
                    <el-tag
                      v-if="quickLinks.length > 0"
                      type="info"
                      size="small"
                      effect="plain"
                      round
                      class="workplace-bookmarks-card__count"
                    >
                      {{ quickLinks.length }}/{{ QUICK_LINK_MAX }}
                    </el-tag>
                  </span>
                  <p class="workplace-section-sub workplace-section-sub--inline">
                    最多 {{ QUICK_LINK_MAX }} 个 · 标签栏星标添加 · 仅本机
                  </p>
                </div>
                <div class="workplace-bookmarks-card__header-actions">
                  <el-tooltip
                    content="在顶部标签栏左侧星标上点击，可加入或取消收藏"
                    placement="top"
                  >
                    <el-icon class="workplace-module-bookmarks__help" :size="15">
                      <QuestionFilled />
                    </el-icon>
                  </el-tooltip>
                  <ElButton size="small" type="danger" plain @click="clearBookmarks()">
                    <el-icon><Delete /></el-icon>
                    {{ t("common.clear") }}
                  </ElButton>
                </div>
              </div>
            </template>
            <div class="workplace-module-bookmarks">
              <template v-if="quickLinks.length > 0">
                <div class="workplace-quick-list workplace-quick-list--hub">
                  <el-tooltip
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
                        <el-icon v-if="item.icon && item.icon.startsWith('el-icon')">
                          <component :is="item.icon.replace('el-icon-', '')" />
                        </el-icon>
                        <div v-else-if="item.icon" :class="`i-svg:${item.icon}`" />
                        <div v-else class="i-svg:menu" />
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
                          <el-icon><Close /></el-icon>
                        </button>
                      </div>
                    </div>
                  </el-tooltip>
                </div>
              </template>
              <el-empty v-else :image-size="48" class="workplace-module-bookmarks__empty">
                <template #description>
                  <p class="workplace-quick-empty__title">暂无收藏</p>
                  <p class="workplace-quick-empty__hint">
                    在顶部
                    <strong>标签栏</strong>
                    左侧星标点击添加
                  </p>
                </template>
              </el-empty>
            </div>
          </ElCard>
        </ElCol>
      </ElRow>
    </div>

    <!-- 运行快照/任务 与 日志/消息：独立纵向堆叠，避免 el-row 负边距与 flex 链导致块级重叠 -->
    <div class="mt-4 workplace-ops-stack">
      <ElRow :gutter="16" class="workplace-ops-row workplace-ops-row--pair">
        <ElCol :xs="24" :md="12" class="workplace-ops-col">
          <ElCard
            v-loading="statsLoading"
            shadow="hover"
            class="workplace-snapshot-card workplace-surface workplace-ops-card"
          >
            <template #header>
              <div class="workplace-snapshot-card__head">
                <div>
                  <span class="workplace-panel-title">运行快照</span>
                  <p class="workplace-section-sub workplace-section-sub--inline">
                    关键指标一览；可进菜单看全量
                  </p>
                </div>
              </div>
            </template>
            <div class="workplace-snapshot-grid">
              <div class="workplace-stat-tile">
                <div class="workplace-stat-tile__label">系统用户</div>
                <div class="workplace-stat-tile__value">
                  {{ fmtMetric(overviewSnapshot.userTotal) }}
                </div>
                <div class="workplace-stat-tile__hint">账号总数</div>
              </div>
              <div class="workplace-stat-tile">
                <div class="workplace-stat-tile__label">当前在线</div>
                <div class="workplace-stat-tile__value">
                  {{ fmtMetric(overviewSnapshot.onlineTotal) }}
                </div>
                <div class="workplace-stat-tile__hint">会话在线</div>
              </div>
              <div class="workplace-stat-tile">
                <div class="workplace-stat-tile__label">本机负载</div>
                <div class="workplace-stat-tile__value workplace-stat-tile__value--sm">
                  CPU {{ fmtPercent(overviewSnapshot.cpuUsed) }} · 内存
                  {{ fmtPercent(overviewSnapshot.memUsage) }}
                </div>
                <div class="workplace-stat-tile__hint">监控服务所在机器</div>
              </div>
              <div class="workplace-stat-tile">
                <div class="workplace-stat-tile__label">调度任务</div>
                <div class="workplace-stat-tile__value">
                  {{ fmtMetric(overviewSnapshot.jobCount) }}
                </div>
                <div class="workplace-stat-tile__hint">
                  {{ overviewSnapshot.schedulerStatus || "—" }}
                  <template v-if="overviewSnapshot.schedulerRunning">· 引擎运行中</template>
                </div>
              </div>
              <div class="workplace-stat-tile">
                <div class="workplace-stat-tile__label">AI 与应用</div>
                <div class="workplace-stat-tile__value workplace-stat-tile__value--sm">
                  会话 {{ fmtMetric(overviewSnapshot.chatSessions) }} · 应用
                  {{ fmtMetric(overviewSnapshot.appCount) }}
                </div>
                <div class="workplace-stat-tile__hint">对话列表与应用数量</div>
              </div>
            </div>
            <div v-if="statsUpdatedAt" class="workplace-snapshot-card__foot">
              <span class="workplace-snapshot-card__foot-dot" aria-hidden="true" />
              更新于 {{ formatSnapshotTime(statsUpdatedAt) }}
            </div>
          </ElCard>
        </ElCol>

        <ElCol :xs="24" :md="12" class="workplace-ops-col">
          <ElCard
            shadow="hover"
            class="workplace-section-card workplace-surface workplace-ops-card"
          >
            <template #header>
              <div class="workplace-section-card__head">
                <div>
                  <span class="workplace-panel-title">运行中的任务</span>
                  <p class="workplace-section-sub workplace-section-sub--inline">
                    调度器 · 最多 10 条
                  </p>
                </div>
                <ElButton type="primary" link @click="goToJob()">任务管理</ElButton>
              </div>
            </template>
            <div v-loading="jobsLoading" class="workplace-ops-card__body">
              <el-empty
                v-if="!jobsLoading && runningJobs.length === 0"
                :image-size="64"
                description="暂无运行中的任务"
              />
              <ul v-else class="workplace-running-list workplace-running-list--in-grid">
                <li v-for="job in runningJobs" :key="job.id" class="workplace-running-list__item">
                  <div class="workplace-running-list__main">
                    <span class="workplace-running-list__name">{{ job.name }}</span>
                    <el-tag type="success" size="small">运行中</el-tag>
                  </div>
                  <div class="workplace-running-list__meta">
                    <span v-if="job.next_run_time">下次：{{ job.next_run_time }}</span>
                    <span v-if="job.trigger" class="workplace-running-list__trigger">
                      {{ job.trigger }}
                    </span>
                  </div>
                </li>
              </ul>
            </div>
          </ElCard>
        </ElCol>
      </ElRow>

      <ElRow :gutter="16" class="workplace-ops-row workplace-ops-row--pair">
        <ElCol :xs="24" :md="12" class="workplace-ops-col">
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
              <el-empty
                v-if="!logsLoading && systemLogs.length === 0"
                :image-size="72"
                description="暂无日志"
              />
              <div v-else class="workplace-logs-scroll">
                <el-table
                  :data="displayedLogs"
                  class="workplace-logs-table"
                  size="small"
                  stripe
                  :max-height="logsExpanded ? 360 : 220"
                >
                  <el-table-column label="类型" width="72" align="center">
                    <template #default="{ row }">
                      <el-tag :type="row.type === 1 ? 'success' : 'primary'" size="small">
                        {{ row.type === 1 ? "登录" : "操作" }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column
                    label="路径"
                    prop="request_path"
                    min-width="120"
                    show-overflow-tooltip
                  />
                  <el-table-column label="方法" width="72" align="center">
                    <template #default="{ row }">
                      <el-tag :type="getMethodType(row.request_method)" size="small">
                        {{ row.request_method || "—" }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column label="状态" width="64" align="center">
                    <template #default="{ row }">
                      <el-tag :type="getStatusCodeType(row.response_code)" size="small">
                        {{ row.response_code ?? "—" }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column
                    label="IP"
                    prop="request_ip"
                    min-width="100"
                    show-overflow-tooltip
                  />
                  <el-table-column
                    label="时间"
                    prop="created_time"
                    min-width="136"
                    show-overflow-tooltip
                  />
                </el-table>
              </div>
            </div>
          </ElCard>
        </ElCol>

        <ElCol :xs="24" :md="12" class="workplace-ops-col">
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
              <el-empty v-if="noticeList.length === 0" :image-size="80" description="暂无数据" />
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
                        <el-tag size="small" :type="getNoticeTypeColor(item.notice_type)">
                          {{ getNoticeTypeText(item.notice_type) }}
                        </el-tag>
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
                      <el-tooltip
                        placement="top"
                        :content="item.description || item.notice_content"
                      >
                        <ElButton target="_blank" type="primary" link @click="goToNotice()">
                          详情↗
                        </ElButton>
                      </el-tooltip>
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
  name: "Workplace",
  inheritAttrs: false,
});

import { useUserStore } from "@/store/index";
import { greetings } from "@/utils/common";
import NoticeAPI, { NoticeTable } from "@/api/module_system/notice";
import LogAPI, { type LogTable } from "@/api/module_system/log";
import type { SchedulerJob } from "@/api/module_task/cronjob/job";
import ServerAPI, { type ServerInfo } from "@/api/module_monitor/server";
import OnlineAPI from "@/api/module_monitor/online";
import { UserAPI } from "@/api/module_system/user";
import JobAPI from "@/api/module_task/cronjob/job";
import { AiChatAPI } from "@/api/module_ai/chat";
import { ApplicationAPI } from "@/api/module_application/portal";
import {
  WORKPLACE_MODULE_GROUPS,
  flattenLeafMenusFromTree,
  resolveEntryPath,
  resolveEntryTitle,
} from "./workplace-catalog";
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
import { quickStartManager, QUICK_LINK_MAX, type QuickLink } from "@/utils/quickStartManager";

const userStore = useUserStore();
const timefix = greetings();
const { t } = useI18n();
const router = useRouter();

// 通知公告数据（需早于 noticePreviewList）
const noticeList = ref<NoticeTable[]>([]);

const systemLogs = ref<LogTable[]>([]);
const logsLoading = ref(false);
const logsExpanded = ref(false);
const runningJobs = ref<SchedulerJob[]>([]);
const jobsLoading = ref(false);

const displayedLogs = computed(() => {
  if (logsExpanded.value || systemLogs.value.length <= 10) return systemLogs.value;
  return systemLogs.value.slice(0, 10);
});

interface OverviewSnapshot {
  userTotal: number | null;
  onlineTotal: number | null;
  cpuUsed: number | null;
  memUsage: number | null;
  jobCount: number | null;
  schedulerStatus: string;
  schedulerRunning: boolean;
  chatSessions: number | null;
  appCount: number | null;
}

const overviewSnapshot = ref<OverviewSnapshot>({
  userTotal: null,
  onlineTotal: null,
  cpuUsed: null,
  memUsage: null,
  jobCount: null,
  schedulerStatus: "",
  schedulerRunning: false,
  chatSessions: null,
  appCount: null,
});

function fmtMetric(n: number | null | undefined) {
  if (n == null || !Number.isFinite(n)) return "—";
  return String(n);
}

function fmtPercent(n: number | null | undefined) {
  if (n == null || !Number.isFinite(n)) return "—";
  return `${Number(n).toFixed(1)}%`;
}

function formatSnapshotTime(ts: number) {
  return new Date(ts).toLocaleString();
}

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

function goToJob() {
  router.push({ name: "Job" }).catch(() => {
    ElMessage.warning("任务管理页跳转失败，请检查路由配置");
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

async function fetchRunningJobs() {
  jobsLoading.value = true;
  try {
    const res = await JobAPI.getSchedulerJobs();
    if (res.data.code === 0) {
      const jobs = res.data.data ?? [];
      runningJobs.value = jobs.filter((j) => j.status === "运行中").slice(0, 10);
    }
  } catch (e) {
    console.error("工作台加载调度任务失败:", e);
  } finally {
    jobsLoading.value = false;
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
  fetchWorkplaceStats();
  fetchSystemLogs();
  fetchRunningJobs();
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

const statsLoading = ref(false);
const statsUpdatedAt = ref<number | null>(null);

async function fetchWorkplaceStats() {
  statsLoading.value = true;
  try {
    const [userR, onlineR, serverR, jobR, chatR, appR] = await Promise.allSettled([
      UserAPI.listUser({ page_no: 1, page_size: 1 }),
      OnlineAPI.listOnline({ page_no: 1, page_size: 1 }),
      ServerAPI.getServer(),
      JobAPI.getSchedulerStatus(),
      AiChatAPI.getSessionList({ page_no: 1, page_size: 1 }),
      ApplicationAPI.listApp({ page_no: 1, page_size: 1 }),
    ]);

    const snap = overviewSnapshot.value;

    snap.userTotal =
      userR.status === "fulfilled" && userR.value.data.code === 0
        ? (userR.value.data.data?.total ?? null)
        : null;

    snap.onlineTotal =
      onlineR.status === "fulfilled" && onlineR.value.data.code === 0
        ? (onlineR.value.data.data?.total ?? null)
        : null;

    if (serverR.status === "fulfilled" && serverR.value.data.code === 0) {
      const info = serverR.value.data.data as ServerInfo;
      snap.cpuUsed = info.cpu?.used ?? null;
      snap.memUsage = info.mem?.usage ?? null;
    } else {
      snap.cpuUsed = null;
      snap.memUsage = null;
    }

    if (jobR.status === "fulfilled" && jobR.value.data.code === 0) {
      const d = jobR.value.data.data;
      snap.jobCount = d?.job_count ?? null;
      snap.schedulerStatus = d?.status ?? "";
      snap.schedulerRunning = !!d?.is_running;
    } else {
      snap.jobCount = null;
      snap.schedulerStatus = "";
      snap.schedulerRunning = false;
    }

    snap.chatSessions =
      chatR.status === "fulfilled" && chatR.value.data.code === 0
        ? (chatR.value.data.data?.total ?? null)
        : null;

    snap.appCount =
      appR.status === "fulfilled" && appR.value.data.code === 0
        ? (appR.value.data.data?.total ?? null)
        : null;

    statsUpdatedAt.value = Date.now();
  } catch (e) {
    console.error("工作台运行快照加载失败:", e);
  } finally {
    statsLoading.value = false;
  }
}
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
    background: linear-gradient(
      135deg,
      var(--el-fill-color-blank) 0%,
      var(--el-fill-color-light) 100%
    );
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

.workplace-empty-hint {
  margin-top: 8px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.workplace-logs-card {
  :deep(.el-card__body) {
    padding: 12px 14px 14px;
  }
}

.workplace-logs-table {
  width: 100%;
}

.workplace-running-card {
  :deep(.el-card__body) {
    padding: 10px 12px 12px;
  }
}

.workplace-running-list {
  padding: 0;
  margin: 0;
  list-style: none;
}

.workplace-running-list__item {
  padding: 12px 14px;
  margin-bottom: 8px;
  background: var(--el-fill-color-blank);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: var(--workplace-radius-sm);

  &:last-child {
    margin-bottom: 0;
  }
}

.workplace-running-list__main {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  justify-content: space-between;
}

.workplace-running-list__name {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 13px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  white-space: nowrap;
}

.workplace-running-list__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 10px;
  margin-top: 4px;
  font-size: 11px;
  line-height: 1.35;
  color: var(--el-text-color-secondary);
}

.workplace-running-list__trigger {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
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
  overflow-x: hidden;
  overflow-y: auto;
}

.workplace-logs-scroll {
  width: 100%;
  min-width: 0;
  overflow-x: auto;
}

.workplace-notice-timeline {
  padding-left: 2px;
}

.workplace-running-list--in-grid {
  max-height: min(400px, 52vh);
  padding-right: 2px;
  overflow-x: hidden;
  overflow-y: auto;
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

.workplace-snapshot-card {
  :deep(.el-card__body) {
    padding: 18px 20px 16px;
    background: var(--el-fill-color-blank);
  }
}

.workplace-snapshot-card__head {
  width: 100%;
}

.workplace-snapshot-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(168px, 1fr));
  gap: 14px;
}

.workplace-ops-row--pair .workplace-snapshot-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

@media (width <= 575px) {
  .workplace-ops-row--pair .workplace-snapshot-grid {
    grid-template-columns: 1fr;
  }
}

.workplace-stat-tile {
  position: relative;
  min-width: 0;
  padding: 16px 16px 14px;
  overflow: hidden;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: var(--workplace-radius-sm);
  box-shadow: 0 1px 2px rgb(0 0 0 / 4%);
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;

  &::before {
    position: absolute;
    top: 0;
    right: 0;
    left: 0;
    height: 3px;
    content: "";
    background: var(--el-color-primary);
    opacity: 0.9;
  }

  &:hover {
    border-color: var(--el-color-primary-light-7);
    box-shadow: 0 8px 24px rgb(0 0 0 / 7%);
  }

  &:nth-child(2)::before {
    background: var(--el-color-success);
  }

  &:nth-child(3)::before {
    background: var(--el-color-warning);
  }

  &:nth-child(4)::before {
    background: var(--el-color-info);
  }

  &:nth-child(5)::before {
    background: #722ed1;
  }
}

.workplace-stat-tile__label {
  margin-bottom: 8px;
  font-size: 12px;
  font-weight: 500;
  color: var(--el-text-color-secondary);
}

.workplace-stat-tile__value {
  font-size: 24px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  line-height: 1.15;
  color: var(--el-color-primary);
  letter-spacing: -0.02em;
}

.workplace-stat-tile__value--sm {
  font-size: 14px;
  font-weight: 600;
  line-height: 1.45;
  color: var(--el-text-color-primary);
  letter-spacing: 0;
  overflow-wrap: anywhere;
}

.workplace-stat-tile__hint {
  margin-top: 8px;
  font-size: 11px;
  line-height: 1.4;
  color: var(--el-text-color-placeholder);
}

.workplace-snapshot-card__foot {
  display: flex;
  gap: 8px;
  align-items: center;
  padding-top: 14px;
  margin-top: 16px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
  border-top: 1px dashed var(--el-border-color-lighter);
}

.workplace-snapshot-card__foot-dot {
  flex-shrink: 0;
  width: 6px;
  height: 6px;
  background: var(--el-color-success);
  border-radius: 50%;
  opacity: 0.85;
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
