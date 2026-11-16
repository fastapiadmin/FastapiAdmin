<template>
  <div v-loading="loading" class="monitor-page">
    <ElAlert
      v-if="error"
      type="error"
      show-icon
      :closable="false"
      :title="$t('common.loadFailed')"
      class="mb-0"
    >
      <div class="flex flex-wrap items-center gap-3">
        <span>{{ error }}</span>
        <ElButton link type="primary" @click="fetchServerInfo()">
          {{ $t("common.retry") }}
        </ElButton>
      </div>
    </ElAlert>

    <section class="monitor-head">
      <div class="monitor-head__status">
        <span class="monitor-dot" :class="`is-${health.type}`" />
        <div class="min-w-0">
          <div class="monitor-head__title">
            <span>服务器运行状态</span>
            <FaStatusTag :label="health.label" :type="health.type" />
          </div>
          <p class="monitor-head__desc">{{ health.desc }}</p>
          <p class="monitor-head__node">
            {{ server.sys?.computer_name || "当前节点" }}
            <span class="monitor-sep">/</span>
            {{ server.sys?.os_name || "未知系统" }}
            <span class="monitor-sep">/</span>
            {{ server.sys?.computer_ip || "-" }}
          </p>
        </div>
      </div>
      <div class="monitor-head__actions">
        <span class="monitor-updated">更新于 {{ updatedAt }}</span>
        <label class="monitor-auto">
          <ElSwitch v-model="autoRefresh" size="small" />
          <span>30 秒自动刷新</span>
        </label>
        <ElButton :icon="Refresh" :loading="refreshing" @click="fetchServerInfo()">刷新</ElButton>
      </div>
    </section>

    <section class="monitor-kpis">
      <div v-for="kpi in kpis" :key="kpi.key" class="monitor-kpi" :class="`is-${kpi.level}`">
        <div class="monitor-kpi__head">
          <span class="monitor-kpi__icon"><FaSvgIcon :icon="kpi.icon" /></span>
          <span>{{ kpi.label }}</span>
          <span class="monitor-kpi__state">{{ levelText(kpi.level) }}</span>
        </div>
        <div class="monitor-kpi__value">
          {{ kpi.value }}<small>{{ kpi.suffix }}</small>
        </div>
        <ElProgress
          :percentage="kpi.percent"
          :status="kpi.progressStatus"
          :stroke-width="6"
          :show-text="false"
        />
        <div class="monitor-kpi__foot">
          <span>{{ kpi.detail }}</span>
          <span class="truncate">{{ kpi.note }}</span>
        </div>
      </div>
    </section>

    <ElRow :gutter="16" class="monitor-row">
      <ElCol :xs="24" :lg="12">
        <ElCard shadow="never" class="monitor-panel">
          <template #header>
            <div class="monitor-panel__head">
              <div class="monitor-panel__title">
                <FaSvgIcon icon="ri:cpu-line" />
                <span>CPU 使用情况</span>
              </div>
              <FaStatusTag :label="levelText(cpuLevel)" :type="cpuLevel" size="small" />
            </div>
          </template>
          <div class="resource-body">
            <ElProgress
              type="circle"
              :percentage="cpuUsage"
              :width="128"
              :stroke-width="10"
              :status="progressStatus(cpuLevel)"
            >
              <div class="resource-ring__value">{{ cpuUsage.toFixed(1) }}<small>%</small></div>
              <div class="resource-ring__label">使用率</div>
            </ElProgress>
            <div class="resource-metrics">
              <div v-for="item in cpuMetrics" :key="item.label" class="resource-metric">
                <span>{{ item.label }}</span>
                <strong>{{ item.value }}</strong>
              </div>
            </div>
          </div>
          <div class="monitor-legend">
            <span><i class="ok" />正常 &lt;60%</span>
            <span><i class="warn" />警告 60–80%</span>
            <span><i class="danger" />危险 &gt;80%</span>
          </div>
        </ElCard>
      </ElCol>

      <ElCol :xs="24" :lg="12">
        <ElCard shadow="never" class="monitor-panel">
          <template #header>
            <div class="monitor-panel__head">
              <div class="monitor-panel__title">
                <FaSvgIcon icon="ri:ram-line" />
                <span>内存使用情况</span>
              </div>
              <FaStatusTag :label="levelText(memLevel)" :type="memLevel" size="small" />
            </div>
          </template>
          <div class="resource-body">
            <ElProgress
              type="circle"
              :percentage="memUsage"
              :width="128"
              :stroke-width="10"
              :status="progressStatus(memLevel)"
            >
              <div class="resource-ring__value">{{ memUsage.toFixed(1) }}<small>%</small></div>
              <div class="resource-ring__label">使用率</div>
            </ElProgress>
            <div class="resource-metrics">
              <div v-for="item in memMetrics" :key="item.label" class="resource-metric">
                <span>{{ item.label }}</span>
                <strong>{{ item.value }}</strong>
              </div>
            </div>
          </div>
          <div class="monitor-legend">
            <span><i class="ok" />正常 &lt;60%</span>
            <span><i class="warn" />警告 60–80%</span>
            <span><i class="danger" />危险 &gt;80%</span>
          </div>
        </ElCard>
      </ElCol>
    </ElRow>

    <ElCard shadow="never" class="monitor-panel">
      <template #header>
        <div class="monitor-panel__head">
          <div class="monitor-panel__title">
            <FaSvgIcon icon="ri:hard-drive-2-line" />
            <span>磁盘使用情况</span>
            <span class="monitor-panel__sub">
              {{ sortedDisks.length }} 个挂载点 · 最高 {{ diskUsage.toFixed(1) }}%
            </span>
          </div>
          <span class="monitor-panel__hint">按使用率从高到低</span>
        </div>
      </template>
      <ElTable :data="sortedDisks" class="monitor-disk-table">
        <template #empty>
          <FaEmptyState icon="ri:inbox-line" :title="$t('common.noData')" compact />
        </template>
        <ElTableColumn label="盘符路径" prop="dir_name" min-width="220" show-overflow-tooltip />
        <ElTableColumn label="文件系统" prop="sys_type_name" width="110" align="center" />
        <ElTableColumn label="使用率" min-width="220">
          <template #default="{ row }">
            <div class="disk-usage">
              <ElProgress
                class="flex-1"
                :percentage="Number(row.usage) || 0"
                :status="progressStatus(levelOf(Number(row.usage) || 0))"
                :stroke-width="8"
                :show-text="false"
              />
              <span class="disk-usage__value">{{ (Number(row.usage) || 0).toFixed(1) }}%</span>
              <FaStatusTag
                :label="levelText(levelOf(Number(row.usage) || 0))"
                :type="levelOf(Number(row.usage) || 0)"
                size="small"
              />
            </div>
          </template>
        </ElTableColumn>
        <ElTableColumn label="已用 / 总量" width="170" align="right">
          <template #default="{ row }">
            <span class="fa-tnum">{{ row.used }} / {{ row.total }}</span>
          </template>
        </ElTableColumn>
        <ElTableColumn label="可用" prop="free" width="100" align="right" />
      </ElTable>
    </ElCard>

    <ElRow :gutter="16" class="monitor-row">
      <ElCol :xs="24" :lg="12">
        <ElCard shadow="never" class="monitor-panel monitor-panel--muted">
          <template #header>
            <div class="monitor-panel__title">
              <FaSvgIcon icon="ri:server-line" />
              <span>节点信息</span>
            </div>
          </template>
          <div class="info-grid">
            <div v-for="item in nodeInfo" :key="item.label" class="info-item">
              <span>{{ item.label }}</span>
              <strong :title="item.value">{{ item.value }}</strong>
            </div>
          </div>
        </ElCard>
      </ElCol>
      <ElCol :xs="24" :lg="12">
        <ElCard shadow="never" class="monitor-panel monitor-panel--muted">
          <template #header>
            <div class="monitor-panel__title">
              <FaSvgIcon icon="ri:code-s-slash-line" />
              <span>Python 运行环境</span>
            </div>
          </template>
          <div class="info-grid">
            <div
              v-for="item in pythonInfo"
              :key="item.label"
              class="info-item"
              :class="{ 'is-wide': item.wide }"
            >
              <span>{{ item.label }}</span>
              <strong :title="item.value">{{ item.value }}</strong>
            </div>
          </div>
        </ElCard>
      </ElCol>
    </ElRow>
  </div>
</template>

<script lang="ts" setup>
import { Refresh } from "@element-plus/icons-vue";
import ServerAPI, { type ServerInfo } from "@/api/module_monitor/server";

// 与菜单 route_name 一致：KeepAlive 的 include/exclude 按组件 name 匹配
defineOptions({ name: "MonitorServer" });

type Level = "success" | "warning" | "danger";
type ProgressStatus = "success" | "warning" | "exception";

const WARN_THRESHOLD = 60;
const DANGER_THRESHOLD = 80;
const REFRESH_INTERVAL = 30_000;

const server = ref<ServerInfo>({
  cpu: { cpu_num: 0, used: 0, sys: 0, free: 0 },
  mem: { total: "", used: "", free: "", usage: 0 },
  sys: { computer_name: "", os_name: "", computer_ip: "", os_arch: "", user_dir: "" },
  py: {
    name: "",
    version: "",
    start_time: "",
    run_time: "",
    home: "",
    memory_total: "",
    memory_used: "",
    memory_free: "",
    memory_usage: 0,
  },
  disks: [],
});

const loading = ref(true);
const refreshing = ref(false);
const error = ref("");
const updatedAt = ref("--:--:--");
const autoRefresh = ref(true);
let refreshTimer: number | undefined;

const cpuUsage = computed(() => Number(server.value.cpu?.used) || 0);
const memUsage = computed(() => Number(server.value.mem?.usage) || 0);
const pythonUsage = computed(() => Number(server.value.py?.memory_usage) || 0);
const diskUsage = computed(() =>
  Math.max(0, ...(server.value.disks || []).map((disk) => Number(disk.usage) || 0))
);
const cpuLevel = computed(() => levelOf(cpuUsage.value));
const memLevel = computed(() => levelOf(memUsage.value));
const diskLevel = computed(() => levelOf(diskUsage.value));

function levelOf(value: number): Level {
  if (value >= DANGER_THRESHOLD) return "danger";
  if (value >= WARN_THRESHOLD) return "warning";
  return "success";
}

function levelText(level: Level): string {
  return level === "danger" ? "过高" : level === "warning" ? "偏高" : "正常";
}

function progressStatus(level: Level): ProgressStatus {
  return level === "danger" ? "exception" : level;
}

const health = computed<{ type: Level; label: string; desc: string }>(() => {
  const max = Math.max(cpuUsage.value, memUsage.value, diskUsage.value);
  if (max >= DANGER_THRESHOLD) {
    return { type: "danger", label: "资源紧张", desc: "存在使用率超过 80% 的核心资源，请及时处理" };
  }
  if (max >= WARN_THRESHOLD) {
    return { type: "warning", label: "需关注", desc: "部分资源已进入预警区间，建议持续观察" };
  }
  return { type: "success", label: "运行正常", desc: "CPU、内存与磁盘均处于安全水位" };
});

const kpis = computed(() => [
  {
    key: "cpu",
    icon: "ri:cpu-line",
    label: "CPU 使用率",
    value: cpuUsage.value.toFixed(1),
    suffix: "%",
    percent: cpuUsage.value,
    level: cpuLevel.value,
    progressStatus: progressStatus(cpuLevel.value),
    detail: `${server.value.cpu?.cpu_num || 0} 个逻辑核心`,
    note: `系统 ${(Number(server.value.cpu?.sys) || 0).toFixed(1)}%`,
  },
  {
    key: "memory",
    icon: "ri:ram-line",
    label: "内存使用率",
    value: memUsage.value.toFixed(1),
    suffix: "%",
    percent: memUsage.value,
    level: memLevel.value,
    progressStatus: progressStatus(memLevel.value),
    detail: `${server.value.mem?.used || "-"} / ${server.value.mem?.total || "-"}`,
    note: `空闲 ${server.value.mem?.free || "-"}`,
  },
  {
    key: "disk",
    icon: "ri:hard-drive-2-line",
    label: "磁盘最高占用",
    value: diskUsage.value.toFixed(1),
    suffix: "%",
    percent: diskUsage.value,
    level: diskLevel.value,
    progressStatus: progressStatus(diskLevel.value),
    detail: `${server.value.disks?.length || 0} 个挂载点`,
    note: `最高 ${diskUsage.value.toFixed(1)}%`,
  },
  {
    key: "python",
    icon: "ri:code-s-slash-line",
    label: "Python 进程内存",
    value: pythonUsage.value.toFixed(1),
    suffix: "%",
    percent: pythonUsage.value,
    level: levelOf(pythonUsage.value),
    progressStatus: progressStatus(levelOf(pythonUsage.value)),
    detail: server.value.py?.memory_used || "-",
    note: `总量 ${server.value.py?.memory_total || "-"}`,
  },
]);

const cpuMetrics = computed(() => [
  { label: "逻辑核心", value: `${server.value.cpu?.cpu_num || 0} 核` },
  { label: "用户态", value: `${(Number(server.value.cpu?.used) || 0).toFixed(1)}%` },
  { label: "系统态", value: `${(Number(server.value.cpu?.sys) || 0).toFixed(1)}%` },
  { label: "空闲", value: `${(Number(server.value.cpu?.free) || 0).toFixed(1)}%` },
]);

const memMetrics = computed(() => [
  { label: "总内存", value: server.value.mem?.total || "-" },
  { label: "已用内存", value: server.value.mem?.used || "-" },
  { label: "空闲内存", value: server.value.mem?.free || "-" },
  { label: "Python 进程", value: server.value.py?.memory_used || "-" },
]);

const sortedDisks = computed(() =>
  [...(server.value.disks || [])].sort((a, b) => (Number(b.usage) || 0) - (Number(a.usage) || 0))
);

const nodeInfo = computed(() => [
  { label: "服务器名称", value: server.value.sys?.computer_name || "-" },
  { label: "操作系统", value: server.value.sys?.os_name || "-" },
  { label: "服务器 IP", value: server.value.sys?.computer_ip || "-" },
  { label: "系统架构", value: server.value.sys?.os_arch || "-" },
]);

const pythonInfo = computed(() => [
  { label: "Python 名称", value: server.value.py?.name || "-" },
  { label: "Python 版本", value: server.value.py?.version || "-" },
  { label: "启动时间", value: server.value.py?.start_time || "-" },
  { label: "运行时长", value: server.value.py?.run_time || "-" },
  { label: "安装路径", value: server.value.py?.home || "-", wide: true },
  { label: "项目路径", value: server.value.sys?.user_dir || "-", wide: true },
]);

async function fetchServerInfo(silent = false) {
  if (!silent) {
    if (server.value.sys?.computer_name) refreshing.value = true;
    else loading.value = true;
  }
  error.value = "";
  try {
    const res = await ServerAPI.getServer();
    if (res.data?.data) {
      server.value = res.data.data;
      updatedAt.value = new Date().toLocaleTimeString("zh-CN", { hour12: false });
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : "服务器信息加载失败";
  } finally {
    loading.value = false;
    refreshing.value = false;
  }
}

function stopRefreshTimer() {
  if (refreshTimer) {
    clearInterval(refreshTimer);
    refreshTimer = undefined;
  }
}

function startRefreshTimer() {
  stopRefreshTimer();
  if (!autoRefresh.value) return;
  refreshTimer = window.setInterval(() => {
    if (document.visibilityState === "visible") void fetchServerInfo(true);
  }, REFRESH_INTERVAL);
}

watch(autoRefresh, startRefreshTimer);

onMounted(() => {
  void fetchServerInfo();
  startRefreshTimer();
});

onActivated(startRefreshTimer);
onDeactivated(stopRefreshTimer);
onUnmounted(stopRefreshTimer);
</script>

<style scoped>
.monitor-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 0;
  min-height: 0;
  overflow-y: auto;
  /* ElRow 的负 gutter 会让内容比容器宽 8px；这里只允许纵向滚动，避免出现横向滚动条 */
  overflow-x: clip;
}

.monitor-page > * {
  flex-shrink: 0;
}

.monitor-head {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 18px 20px;
  border: 1px solid var(--fa-border-subtle);
  border-radius: 12px;
  background:
    radial-gradient(
      circle at 0% 0%,
      color-mix(in srgb, var(--el-color-primary) 10%, transparent),
      transparent 42%
    ),
    var(--fa-surface);
}

.monitor-head__status {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  min-width: 0;
}

.monitor-dot {
  width: 10px;
  height: 10px;
  margin-top: 8px;
  border-radius: 50%;
  flex: none;
  box-shadow: 0 0 0 4px color-mix(in srgb, currentColor 14%, transparent);
}

.monitor-dot.is-success {
  color: var(--el-color-success);
  background: var(--el-color-success);
}

.monitor-dot.is-warning {
  color: var(--el-color-warning);
  background: var(--el-color-warning);
}

.monitor-dot.is-danger {
  color: var(--el-color-danger);
  background: var(--el-color-danger);
}

.monitor-head__title {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  font-size: 18px;
  font-weight: 600;
  color: var(--fa-text-1);
}

.monitor-head__desc {
  margin-top: 6px;
  font-size: 13px;
  color: var(--fa-text-2);
}

.monitor-head__node {
  margin-top: 4px;
  font-size: 12px;
  color: var(--fa-text-3);
}

.monitor-sep {
  padding: 0 4px;
  opacity: 0.5;
}

.monitor-head__actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 14px;
}

.monitor-updated,
.monitor-auto {
  font-size: 12px;
  color: var(--fa-text-3);
}

.monitor-auto {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.monitor-kpis {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.monitor-kpi {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 16px;
  border: 1px solid var(--fa-border-subtle);
  border-radius: 12px;
  background: var(--fa-surface);
  min-width: 0;
}

.monitor-kpi__head {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--fa-text-2);
}

.monitor-kpi__icon {
  display: inline-flex;
  color: var(--el-color-primary);
  font-size: 16px;
}

.monitor-kpi__state {
  margin-left: auto;
  font-size: 12px;
  color: var(--fa-text-3);
}

.monitor-kpi.is-warning .monitor-kpi__state {
  color: var(--el-color-warning);
}

.monitor-kpi.is-danger .monitor-kpi__state {
  color: var(--el-color-danger);
}

.monitor-kpi__value {
  font-size: 30px;
  font-weight: 600;
  line-height: 1;
  color: var(--fa-text-1);
  font-variant-numeric: tabular-nums;
}

.monitor-kpi__value small {
  margin-left: 2px;
  font-size: 14px;
  font-weight: 500;
  color: var(--fa-text-3);
}

.monitor-kpi__foot {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  font-size: 12px;
  color: var(--fa-text-3);
  min-width: 0;
}

.monitor-row {
  margin-bottom: 0;
  row-gap: 16px;
}

.monitor-panel {
  border-radius: 12px;
  border-color: var(--fa-border-subtle);
  background: var(--fa-surface);
}

.monitor-panel + .monitor-panel {
  margin-top: 0;
}

.monitor-row .el-col {
  display: flex;
  margin-bottom: 0;
}

.monitor-row .el-col > .monitor-panel {
  display: flex;
  flex: 1;
  flex-direction: column;
  width: 100%;
  height: 100%;
}

.monitor-row .el-col > .monitor-panel :deep(.el-card__body) {
  flex: 1;
}

.monitor-panel__head {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.monitor-panel__title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 600;
  color: var(--fa-text-1);
}

.monitor-panel__title :deep(svg),
.monitor-panel__title .fa-svg-icon {
  color: var(--el-color-primary);
}

.monitor-panel__sub,
.monitor-panel__hint {
  font-size: 12px;
  font-weight: 400;
  color: var(--fa-text-3);
}

.monitor-panel__sub {
  margin-left: 4px;
}

.resource-body {
  display: flex;
  align-items: center;
  gap: 24px;
}

.resource-metrics {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
  flex: 1;
  min-width: 0;
}

.resource-metric {
  padding: 10px 12px;
  border-radius: 8px;
  background: var(--fa-surface-2);
  min-width: 0;
}

.resource-metric span {
  display: block;
  font-size: 12px;
  color: var(--fa-text-3);
}

.resource-metric strong {
  display: block;
  margin-top: 4px;
  font-size: 14px;
  font-weight: 600;
  color: var(--fa-text-1);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.resource-ring__value {
  font-size: 26px;
  font-weight: 600;
  line-height: 1.1;
  color: var(--fa-text-1);
  font-variant-numeric: tabular-nums;
}

.resource-ring__value small {
  font-size: 12px;
  margin-left: 1px;
  color: var(--fa-text-3);
}

.resource-ring__label {
  margin-top: 2px;
  font-size: 12px;
  color: var(--fa-text-3);
}

.monitor-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px dashed var(--fa-border-subtle);
  font-size: 12px;
  color: var(--fa-text-3);
}

.monitor-legend span {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.monitor-legend i {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.monitor-legend .ok {
  background: var(--el-color-success);
}

.monitor-legend .warn {
  background: var(--el-color-warning);
}

.monitor-legend .danger {
  background: var(--el-color-danger);
}

.disk-usage {
  display: flex;
  align-items: center;
  gap: 10px;
}

.disk-usage__value {
  width: 48px;
  text-align: right;
  font-size: 12px;
  color: var(--fa-text-2);
  font-variant-numeric: tabular-nums;
}

.monitor-panel--muted {
  background: color-mix(in srgb, var(--fa-surface-2) 62%, var(--fa-surface));
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px 20px;
}

.info-item {
  min-width: 0;
}

.info-item span {
  display: block;
  font-size: 12px;
  color: var(--fa-text-3);
}

.info-item strong {
  display: block;
  margin-top: 3px;
  font-size: 13px;
  font-weight: 500;
  color: var(--fa-text-1);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.info-item.is-wide {
  grid-column: 1 / -1;
}

@media (max-width: 1400px) {
  .monitor-kpis {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 992px) {
  .resource-body {
    flex-direction: column;
    align-items: stretch;
  }

  .resource-metrics {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .monitor-head {
    align-items: flex-start;
  }

  .monitor-kpis,
  .resource-metrics,
  .info-grid {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }

  .monitor-head__actions {
    width: 100%;
    justify-content: space-between;
  }

  .monitor-head__title {
    font-size: 16px;
  }

  .monitor-kpi__value {
    font-size: 26px;
  }
}
</style>
