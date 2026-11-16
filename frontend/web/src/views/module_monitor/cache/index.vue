<template>
  <div class="fa-full-height">
    <ElTabs v-model="activeTab" class="fa-tabs-fill">
      <!-- 监控信息 Tab -->
      <ElTabPane label="监控信息" name="0">
        <div class="cache-monitor">
          <section class="monitor-head">
            <div class="monitor-head__status">
              <span class="monitor-dot" :class="redisOnline ? 'is-success' : 'is-danger'" />
              <div class="min-w-0">
                <div class="monitor-head__title">
                  <span>Redis 运行状态</span>
                  <FaStatusTag
                    :label="redisOnline ? '运行中' : '不可用'"
                    :type="redisOnline ? 'success' : 'danger'"
                  />
                </div>
                <p class="monitor-head__desc">
                  {{ cache.info?.redis_mode === "standalone" ? "单机模式" : "集群模式" }}
                  · 端口 {{ cache.info?.tcp_port || "-" }} ·
                  {{ cache.info?.redis_version || "版本未知" }}
                </p>
                <p class="monitor-head__node">
                  已连接 {{ cache.info?.connected_clients || 0 }} 个客户端
                  <span class="monitor-sep">/</span>
                  网络 {{ cache.info?.instantaneous_input_kbps || 0 }} /
                  {{ cache.info?.instantaneous_output_kbps || 0 }} kbps
                </p>
              </div>
            </div>
            <div class="monitor-head__actions">
              <span class="monitor-updated">更新于 {{ updatedAt }}</span>
              <label class="monitor-auto">
                <ElSwitch v-model="autoRefresh" size="small" />
                <span>30 秒自动刷新</span>
              </label>
              <ElButton :icon="Refresh" :loading="refreshing" @click="getInfo()">刷新</ElButton>
            </div>
          </section>

          <ElAlert
            v-if="infoError"
            :title="`监控数据刷新失败：${infoError}`"
            type="error"
            show-icon
            :closable="false"
          />

          <section class="monitor-kpis">
            <div v-for="kpi in cacheKpis" :key="kpi.key" class="monitor-kpi">
              <div class="monitor-kpi__head">
                <span class="monitor-kpi__icon"><FaSvgIcon :icon="kpi.icon" /></span>
                <span>{{ kpi.label }}</span>
              </div>
              <div class="monitor-kpi__value">
                {{ kpi.value }}<small v-if="kpi.suffix">{{ kpi.suffix }}</small>
              </div>
              <div class="monitor-kpi__foot">
                <span>{{ kpi.detail }}</span>
                <span class="truncate">{{ kpi.note }}</span>
              </div>
            </div>
          </section>

          <div class="cache-grid">
            <ElCard shadow="never" class="monitor-panel cache-chart-card">
              <template #header>
                <div class="monitor-panel__head">
                  <div class="monitor-panel__title">
                    <FaSvgIcon icon="ri:bar-chart-2-line" />
                    <span>命令统计</span>
                  </div>
                  <span class="monitor-panel__hint">Top 8 + 其他</span>
                </div>
              </template>
              <div ref="commandstats" class="cache-chart" />
              <FaEmptyState
                v-if="!cache.command_stats?.length"
                class="cache-chart__empty"
                icon="ri:bar-chart-2-line"
                title="暂无命令统计"
                compact
              />
            </ElCard>

            <ElCard shadow="never" class="monitor-panel cache-memory-card">
              <template #header>
                <div class="monitor-panel__head">
                  <div class="monitor-panel__title">
                    <FaSvgIcon icon="ri:pie-chart-2-line" />
                    <span>内存与连接</span>
                  </div>
                  <FaStatusTag
                    v-if="maxMemoryBytes > 0"
                    :label="memoryLevelText"
                    :type="memoryLevel"
                    size="small"
                  />
                </div>
              </template>
              <div class="cache-memory">
                <div class="cache-memory__main">
                  <span>已用内存</span>
                  <strong>{{ cache.info?.used_memory_human || "-" }}</strong>
                  <small>上限 {{ maxmemoryLabel }}</small>
                </div>
                <ElProgress
                  v-if="maxMemoryBytes > 0"
                  :percentage="memoryPercent"
                  :status="memoryProgressStatus"
                  :stroke-width="8"
                  :show-text="false"
                />
                <p v-else class="cache-memory__hint">
                  未设置 maxmemory，Redis 会按需使用内存；可结合宿主机内存关注增长趋势。
                </p>
                <div class="cache-memory__facts">
                  <div>
                    <span>客户端</span><strong>{{ cache.info?.connected_clients || 0 }}</strong>
                  </div>
                  <div>
                    <span>Key 总数</span><strong>{{ cache.db_size || 0 }}</strong>
                  </div>
                  <div>
                    <span>网络入</span
                    ><strong>{{ cache.info?.instantaneous_input_kbps || 0 }} kbps</strong>
                  </div>
                  <div>
                    <span>网络出</span
                    ><strong>{{ cache.info?.instantaneous_output_kbps || 0 }} kbps</strong>
                  </div>
                </div>
              </div>
            </ElCard>
          </div>

          <ElCard shadow="never" class="monitor-panel cache-instance-card">
            <template #header>
              <div class="monitor-panel__head">
                <div class="monitor-panel__title">
                  <FaSvgIcon icon="ri:database-2-line" />
                  <span>实例概览</span>
                </div>
                <div class="cache-health">
                  <span :class="aofEnabled ? 'is-ok' : 'is-off'">
                    <i />AOF {{ aofEnabled ? "开启" : "关闭" }}
                  </span>
                  <span :class="rdbHealthy ? 'is-ok' : 'is-danger'">
                    <i />RDB
                    {{ rdbHealthy ? "正常" : cache.info?.rdb_last_bgsave_status || "未知" }}
                  </span>
                </div>
              </div>
            </template>
            <div class="cache-instance">
              <div v-for="item in instanceItems" :key="item.label" class="cache-instance__item">
                <span>{{ item.label }}</span>
                <strong :title="item.value">{{ item.value }}</strong>
              </div>
            </div>
          </ElCard>
        </div>
      </ElTabPane>

      <!-- 缓存管理 Tab：日常只保留业务缓存，键空间作为高级工具抽屉 -->
      <ElTabPane label="缓存管理" name="1">
        <div class="cache-manage">
          <div class="cache-manage__bar">
            <div class="cache-manage__intro">
              <div class="cache-manage__title">
                <FaSvgIcon icon="ri:database-2-line" />
                <span>业务缓存</span>
              </div>
              <p class="cache-manage__desc">
                按缓存对象查看键名与内容；需要按逻辑库、模式查找任意原始键时，再打开键空间。
              </p>
            </div>
            <ElButton
              v-hasPerm="['module_monitor:cache:query']"
              plain
              aria-label="打开键空间浏览"
              @click="openKeyspace"
            >
              <FaSvgIcon icon="ri:key-2-line" class="mr-1" />
              键空间
            </ElButton>
          </div>
          <div class="cache-manage__body grid grid-cols-1 xl:grid-cols-3 xl:grid-rows-1 gap-4">
            <!-- 缓存列表 -->
            <ElCard
              v-loading="loading"
              shadow="hover"
              class="fa-card flex flex-col min-h-100 xl:min-h-0"
              body-class="flex flex-col flex-1 min-h-0 overflow-hidden"
            >
              <template #header>
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <FaSvgIcon icon="ri:list-unordered" class="text-lg" />
                    <span class="font-medium">缓存列表</span>
                    <ElTag size="small" type="info" effect="plain">{{ cacheNames.length }}</ElTag>
                  </div>
                  <ElButton
                    v-hasPerm="['module_monitor:cache:query']"
                    type="primary"
                    link
                    :icon="RefreshRight"
                    @click="getCacheNameList"
                  />
                </div>
              </template>
              <ElScrollbar v-if="cacheNames.length" class="flex-1 min-h-0">
                <div class="cache-list" role="listbox" aria-label="缓存列表">
                  <div
                    v-for="item in cacheNames"
                    :key="item.cache_name"
                    class="cache-list__item"
                    :class="{ 'is-active': nowCacheName === item.cache_name }"
                    role="option"
                    :aria-selected="nowCacheName === item.cache_name"
                    tabindex="0"
                    @click="getCacheKeyList(item)"
                    @keydown.enter.self.prevent="getCacheKeyList(item)"
                    @keydown.space.self.prevent="getCacheKeyList(item)"
                  >
                    <span class="cache-list__main">
                      <span class="cache-list__name" :title="item.cache_name">
                        {{ item.cache_name }}
                      </span>
                      <span class="cache-list__remark" :title="item.remark || '—'">
                        {{ item.remark || "—" }}
                      </span>
                    </span>
                    <ElPopconfirm
                      :title="`确认删除缓存 ${item.cache_name} 吗？`"
                      placement="left"
                      @confirm="handleClearCacheName(item)"
                    >
                      <template #reference>
                        <ElButton
                          v-hasPerm="['module_monitor:cache:delete']"
                          class="cache-list__delete"
                          type="danger"
                          size="small"
                          link
                          :icon="Delete"
                          :aria-label="`删除缓存 ${item.cache_name}`"
                          @click.stop
                        />
                      </template>
                    </ElPopconfirm>
                  </div>
                </div>
              </ElScrollbar>
              <div v-else class="cache-list-empty">
                <FaEmptyState icon="ri:inbox-line" :title="$t('common.noData')" compact />
              </div>
            </ElCard>

            <!-- 键名列表 -->
            <ElCard
              v-loading="subLoading"
              shadow="hover"
              class="fa-card flex flex-col min-h-100 xl:min-h-0"
              body-class="flex flex-col flex-1 min-h-0 overflow-hidden"
            >
              <template #header>
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <FaSvgIcon icon="ri:key-2-line" class="text-lg" />
                    <span class="font-medium">键名列表</span>
                    <ElTag
                      v-if="nowCacheName"
                      size="small"
                      type="info"
                      effect="plain"
                      class="cache-scope-tag"
                    >
                      {{ nowCacheName }}
                    </ElTag>
                  </div>
                  <ElButton
                    v-hasPerm="['module_monitor:cache:query']"
                    type="primary"
                    link
                    :icon="RefreshRight"
                    @click="getCacheKeyList()"
                  />
                </div>
              </template>
              <ElScrollbar v-if="cacheKeys.length" class="flex-1 min-h-0">
                <div class="cache-list" role="listbox" aria-label="键名列表">
                  <div
                    v-for="key in cacheKeys"
                    :key="key"
                    class="cache-list__item"
                    :class="{ 'is-active': cacheForm.cache_key === key }"
                    role="option"
                    :aria-selected="cacheForm.cache_key === key"
                    tabindex="0"
                    @click="handleCacheValue(key)"
                    @keydown.enter.self.prevent="handleCacheValue(key)"
                    @keydown.space.self.prevent="handleCacheValue(key)"
                  >
                    <span class="cache-list__name" :title="key">{{ key }}</span>
                    <ElPopconfirm
                      :title="`确认删除键 ${key} 吗？`"
                      placement="left"
                      @confirm="handleClearCacheKey(key)"
                    >
                      <template #reference>
                        <ElButton
                          v-hasPerm="['module_monitor:cache:delete']"
                          class="cache-list__delete"
                          type="danger"
                          size="small"
                          link
                          :icon="Delete"
                          :aria-label="`删除键 ${key}`"
                          @click.stop
                        />
                      </template>
                    </ElPopconfirm>
                  </div>
                </div>
              </ElScrollbar>
              <div v-else class="cache-list-empty">
                <FaEmptyState
                  icon="ri:inbox-line"
                  :title="nowCacheName ? $t('common.noData') : '请选择左侧缓存'"
                  compact
                />
              </div>
            </ElCard>

            <!-- 缓存内容 -->
            <ElCard
              v-loading="loading"
              shadow="hover"
              class="fa-card flex flex-col min-h-100 xl:min-h-0"
              body-class="flex flex-col flex-1 min-h-0 overflow-hidden"
            >
              <template #header>
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <FaSvgIcon icon="ri:file-text-line" class="text-lg" />
                    <span class="font-medium">缓存内容</span>
                  </div>
                  <ElButton
                    v-hasPerm="['module_monitor:cache:delete']"
                    type="danger"
                    link
                    :icon="Delete"
                    @click="handleClearCacheAll"
                  >
                    清理全部
                  </ElButton>
                </div>
              </template>
              <div v-if="cacheForm.cache_key" class="cache-value-panel">
                <div class="cache-value-context">
                  <span class="cache-value-context__label">缓存</span>
                  <span class="cache-value-context__value" :title="cacheForm.cache_name">
                    {{ cacheForm.cache_name }}
                  </span>
                  <span class="cache-value-context__sep">/</span>
                  <span class="cache-value-context__key" :title="cacheForm.cache_key">
                    {{ cacheForm.cache_key }}
                  </span>
                </div>
                <div class="cache-value-toolbar">
                  <div class="flex min-w-0 items-center gap-2">
                    <span class="cache-format-tag" :class="`is-${cacheValueFormat.kind}`">
                      {{ cacheValueFormat.label }}
                    </span>
                    <span class="cache-value-size">
                      {{ cacheValueSize }} · {{ cacheValueLines }} 行
                    </span>
                  </div>
                  <div class="flex items-center gap-1">
                    <ElButton link size="small" :icon="DocumentCopy" @click="copyCacheValue">
                      复制
                    </ElButton>
                    <ElButton
                      v-if="cacheValueFormat.kind === 'text'"
                      link
                      size="small"
                      @click="cacheValueWrap = !cacheValueWrap"
                    >
                      {{ cacheValueWrap ? "不换行" : "自动换行" }}
                    </ElButton>
                  </div>
                </div>
                <div class="cache-value-body" :class="{ 'is-wrapped': cacheValueWrap }">
                  <VueJsonPretty
                    v-if="cacheValueFormat.kind === 'json'"
                    :data="cacheValueNormalized.parsed"
                    :show-line="true"
                    :show-icon="true"
                    :show-double-quotes="false"
                    :show-length="true"
                    :deep="3"
                  />
                  <pre v-else>{{ cacheForm.cache_value }}</pre>
                </div>
              </div>
              <FaEmptyState v-else icon="ri:file-text-line" title="选择键名查看缓存内容" compact />
            </ElCard>
          </div>

          <ElDrawer
            v-model="keyspaceVisible"
            title="键空间浏览"
            size="80%"
            class="keyspace-drawer"
            destroy-on-close
          >
            <div class="keyspace-workspace">
              <ElCard
                shadow="hover"
                class="fa-card flex flex-col h-full min-h-0"
                body-class="flex flex-col flex-1 min-h-0 overflow-hidden"
              >
                <div class="flex flex-wrap items-center gap-2">
                  <span class="text-[13px] text-(--el-text-color-secondary)">逻辑库</span>
                  <ElSelect v-model="redisDb" style="width: 160px" @change="scanRedisKeys(true)">
                    <ElOption
                      v-for="item in redisDatabases"
                      :key="item.db"
                      :label="`db${item.db}（${item.keys} 键）`"
                      :value="item.db"
                    />
                  </ElSelect>
                  <ElInput
                    v-model="redisPattern"
                    placeholder="键模式，如 fastapiadmin:*"
                    style="width: 260px"
                    clearable
                    @keyup.enter="scanRedisKeys(true)"
                    aria-label="键模式，如 fastapiadmin:*"
                  />
                  <ElButton type="primary" :loading="redisLoading" @click="scanRedisKeys(true)"
                    >扫描</ElButton
                  >
                  <ElButton :disabled="!redisCursor" @click="scanRedisKeys(false)"
                    >加载更多</ElButton
                  >
                  <span class="text-xs text-(--el-text-color-secondary)">
                    只读浏览 · 敏感键自动脱敏 · 已加载 {{ redisKeys.length }} 个键
                  </span>
                </div>
                <ElTable
                  v-loading="redisLoading"
                  :data="redisKeys"
                  class="mt-3 flex-1 min-h-0"
                  height="100%"
                  @row-click="openRedisValue"
                >
                  <template #empty>
                    <FaEmptyState
                      icon="ri:inbox-line"
                      title="没有扫描到键（可换逻辑库或模式再试）"
                      compact
                    />
                  </template>
                  <ElTableColumn prop="key" label="键名" min-width="320" show-overflow-tooltip />
                  <ElTableColumn prop="type" label="类型" width="110" />
                  <ElTableColumn label="TTL" width="120">
                    <template #default="{ row }">
                      {{ row.ttl === -1 ? "永不过期" : row.ttl === -2 ? "不存在" : `${row.ttl}s` }}
                    </template>
                  </ElTableColumn>
                  <ElTableColumn label="操作" width="90" align="center" fixed="right">
                    <template #default="{ row }">
                      <ElButton link type="primary" @click.stop="openRedisValue(row)"
                        >查看</ElButton
                      >
                    </template>
                  </ElTableColumn>
                </ElTable>
              </ElCard>

              <ElDialog
                v-model="redisValueVisible"
                :title="`键详情：${redisValue?.key ?? ''}`"
                width="760px"
              >
                <ElDescriptions :column="3" border size="small">
                  <ElDescriptionsItem label="类型">{{
                    redisValue?.type ?? "-"
                  }}</ElDescriptionsItem>
                  <ElDescriptionsItem label="TTL">
                    {{
                      redisValue?.ttl === -1
                        ? "永不过期"
                        : redisValue?.ttl === -2
                          ? "不存在"
                          : `${redisValue?.ttl ?? "-"}s`
                    }}
                  </ElDescriptionsItem>
                  <ElDescriptionsItem label="大小">
                    {{ redisValue?.size == null ? "-" : `${redisValue.size} B` }}
                  </ElDescriptionsItem>
                </ElDescriptions>
                <ElAlert
                  v-if="redisValue?.masked"
                  class="mt-3"
                  type="warning"
                  :closable="false"
                  title="该键命中敏感模式，值已脱敏"
                />
                <ElAlert
                  v-else-if="redisValue?.truncated"
                  class="mt-3"
                  type="info"
                  :closable="false"
                  title="值过大，仅展示前一部分"
                />
                <div class="keyspace-value">
                  <div class="cache-value-toolbar">
                    <div class="flex min-w-0 items-center gap-2">
                      <span class="cache-format-tag" :class="`is-${redisValueNormalized.kind}`">
                        {{
                          redisValueNormalized.kind === "json"
                            ? "JSON"
                            : redisValueNormalized.kind === "text"
                              ? "TEXT"
                              : "EMPTY"
                        }}
                      </span>
                      <span class="cache-value-size">
                        {{ formatByteSize(redisValueNormalized.pretty) }} ·
                        {{
                          redisValueNormalized.pretty
                            ? redisValueNormalized.pretty.split("\n").length
                            : 0
                        }}
                        行
                      </span>
                    </div>
                    <ElButton link size="small" :icon="DocumentCopy" @click="copyRedisValue">
                      复制
                    </ElButton>
                  </div>
                  <div class="cache-value-body">
                    <VueJsonPretty
                      v-if="redisValueNormalized.kind === 'json'"
                      :data="redisValueNormalized.parsed"
                      :show-line="true"
                      :show-icon="true"
                      :show-double-quotes="false"
                      :show-length="true"
                      :deep="3"
                    />
                    <pre v-else>{{ redisValueNormalized.pretty }}</pre>
                  </div>
                </div>
              </ElDialog>
            </div>
          </ElDrawer>
        </div>
      </ElTabPane>
    </ElTabs>
  </div>
</template>

<script lang="ts" setup>
import { ElMessageBox } from "element-plus";
import { Refresh, RefreshRight, Delete, DocumentCopy } from "@element-plus/icons-vue";
import CacheAPI, {
  type CacheInfo,
  type CacheForm,
  type CacheMonitor,
  type RedisDatabase,
  type RedisInfo,
  type RedisKeyMeta,
  type RedisValue,
} from "@/api/module_monitor/cache";
import { echarts } from "@/plugins/echarts";
import VueJsonPretty from "vue-json-pretty";
import "vue-json-pretty/lib/styles.css";

// 与菜单 route_name 一致：KeepAlive 的 include/exclude 按组件 name 匹配
defineOptions({ name: "MonitorCache" });

const activeTab = ref("0");
const keyspaceVisible = ref(false);

const cacheNames = ref<CacheInfo[]>([]);
const cacheKeys = ref<string[]>([]);
const loading = ref(true);
const subLoading = ref(false);
const nowCacheName = ref("");

// ─── Redis 键空间浏览（只读）────────────────────────────────────────
const redisDatabases = ref<RedisDatabase[]>([]);
const redisDb = ref(0);
const redisPattern = ref("*");
const redisKeys = ref<RedisKeyMeta[]>([]);
const redisCursor = ref(0);
const redisLoading = ref(false);
const redisValueVisible = ref(false);
const redisValue = ref<RedisValue | null>(null);
const redisValueNormalized = computed(() => normalizeCacheValue(redisValue.value?.value));

async function loadRedisDatabases() {
  const res = await CacheAPI.getRedisDatabases();
  redisDatabases.value = res.data.data || [];
  if (
    redisDatabases.value.length &&
    !redisDatabases.value.some((item) => item.db === redisDb.value)
  ) {
    redisDb.value = redisDatabases.value[0]!.db;
  }
}

async function scanRedisKeys(reset: boolean) {
  if (reset) {
    redisKeys.value = [];
    redisCursor.value = 0;
  }
  redisLoading.value = true;
  try {
    const res = await CacheAPI.scanRedisKeys({
      db: redisDb.value,
      pattern: redisPattern.value || "*",
      cursor: reset ? 0 : redisCursor.value,
      count: 100,
    });
    const page = res.data.data;
    const incoming = page?.keys || [];
    redisKeys.value = reset ? incoming : [...redisKeys.value, ...incoming];
    redisCursor.value = page?.cursor ?? 0;
  } finally {
    redisLoading.value = false;
  }
}

async function openRedisValue(row: unknown) {
  const target = row as RedisKeyMeta;
  const res = await CacheAPI.getRedisValue({ db: redisDb.value, key: target.key });
  redisValue.value = res.data.data ?? null;
  redisValueVisible.value = true;
}

async function ensureKeyspaceLoaded() {
  await loadRedisDatabases();
  await scanRedisKeys(true);
}

const openKeyspace = async () => {
  keyspaceVisible.value = true;
  await ensureKeyspaceLoaded();
};

const commandstats = ref<HTMLElement | null>(null);
const cache = ref<CacheMonitor>({
  info: {} as RedisInfo,
  command_stats: [],
  db_size: 0,
});
const updatedAt = ref("--:--:--");
const refreshing = ref(true);
const autoRefresh = ref(true);
const infoError = ref("");
let refreshTimer: number | undefined;
const REFRESH_INTERVAL = 30_000;

type Level = "success" | "warning" | "danger";
type ProgressStatus = "success" | "warning" | "exception";

const redisOnline = computed(() => Boolean(cache.value.info?.redis_version));
const aofEnabled = computed(() => String(cache.value.info?.aof_enabled ?? "1") !== "0");
const rdbHealthy = computed(
  () => String(cache.value.info?.rdb_last_bgsave_status ?? "").toLowerCase() === "ok"
);

const MEMORY_UNITS: Record<string, number> = {
  "": 1,
  k: 1024,
  m: 1024 ** 2,
  g: 1024 ** 3,
  t: 1024 ** 4,
  p: 1024 ** 5,
};

function parseMemorySize(value?: string): number {
  const match = String(value ?? "")
    .trim()
    .match(/^([\d.]+)\s*([kmgtp]?)b?$/i);
  if (!match) return 0;
  return (Number(match[1]) || 0) * (MEMORY_UNITS[match[2]!.toLowerCase()] || 1);
}

const maxMemoryBytes = computed(() => parseMemorySize(cache.value.info?.maxmemory_human));
const usedMemoryBytes = computed(() => parseMemorySize(cache.value.info?.used_memory_human));
const maxmemoryLabel = computed(() =>
  maxMemoryBytes.value > 0 ? cache.value.info?.maxmemory_human || "-" : "未设置"
);
const memoryPercent = computed(() =>
  maxMemoryBytes.value > 0
    ? Math.min(100, Math.round((usedMemoryBytes.value / maxMemoryBytes.value) * 1000) / 10)
    : 0
);
const memoryLevel = computed<Level>(() => {
  if (memoryPercent.value >= 80) return "danger";
  if (memoryPercent.value >= 60) return "warning";
  return "success";
});
const memoryLevelText = computed(() =>
  memoryLevel.value === "danger" ? "过高" : memoryLevel.value === "warning" ? "偏高" : "正常"
);
const memoryProgressStatus = computed<ProgressStatus>(() =>
  memoryLevel.value === "danger" ? "exception" : memoryLevel.value
);

const cacheKpis = computed(() => [
  {
    key: "keys",
    icon: "ri:key-2-line",
    label: "Key 总数",
    value: cache.value.db_size || 0,
    suffix: "",
    detail: "当前实例",
    note: "含过期键",
  },
  {
    key: "memory",
    icon: "ri:database-2-line",
    label: "已用内存",
    value: cache.value.info?.used_memory_human || "-",
    suffix: "",
    detail: `上限 ${maxmemoryLabel.value}`,
    note: maxMemoryBytes.value > 0 ? `使用率 ${memoryPercent.value}%` : "未限制",
  },
  {
    key: "clients",
    icon: "ri:links-line",
    label: "客户端连接",
    value: cache.value.info?.connected_clients || 0,
    suffix: "个",
    detail: "当前连接数",
    note: `运行 ${cache.value.info?.uptime_in_days || 0} 天`,
  },
  {
    key: "network",
    icon: "ri:exchange-line",
    label: "实时网络 I/O",
    value: Number(cache.value.info?.instantaneous_input_kbps || 0).toFixed(2),
    suffix: "kbps",
    detail: `出 ${Number(cache.value.info?.instantaneous_output_kbps || 0).toFixed(2)} kbps`,
    note: "instantaneous",
  },
]);

const instanceItems = computed(() => [
  { label: "Redis 版本", value: cache.value.info?.redis_version || "-" },
  {
    label: "运行模式",
    value: cache.value.info?.redis_mode === "standalone" ? "单机" : "集群",
  },
  { label: "监听端口", value: String(cache.value.info?.tcp_port || "-") },
  { label: "客户端连接", value: `${cache.value.info?.connected_clients || 0} 个` },
  { label: "运行天数", value: `${cache.value.info?.uptime_in_days || 0} 天` },
  {
    label: "内存上限",
    value: maxMemoryBytes.value > 0 ? cache.value.info?.maxmemory_human || "-" : "未设置",
  },
  { label: "AOF", value: aofEnabled.value ? "开启" : "关闭" },
  {
    label: "RDB 最近保存",
    value:
      cache.value.info?.rdb_last_bgsave_status?.toLowerCase() === "ok"
        ? "正常"
        : cache.value.info?.rdb_last_bgsave_status || "未知",
  },
]);
const cacheForm = ref<CacheForm>({
  cache_name: "",
  cache_key: "",
  cache_value: "",
});

type CacheValueKind = "json" | "text" | "empty";
type CacheJSONValue = string | number | boolean | unknown[] | Record<string, unknown> | null;
interface NormalizedCacheValue {
  kind: CacheValueKind;
  parsed: CacheJSONValue;
  pretty: string;
}

const cacheValueWrap = ref(true);

function normalizeCacheValue(value: unknown): NormalizedCacheValue {
  const raw =
    typeof value === "string"
      ? value
      : value === null || value === undefined
        ? ""
        : JSON.stringify(value, null, 2);
  const trimmed = raw.trim();
  if (!trimmed) return { kind: "empty", parsed: null, pretty: "" };
  try {
    const parsed: unknown = JSON.parse(trimmed);
    if (parsed && typeof parsed === "object") {
      return {
        kind: "json",
        parsed: parsed as CacheJSONValue,
        pretty: JSON.stringify(parsed, null, 2),
      };
    }
  } catch {
    // 非 JSON，按原始文本展示
  }
  return { kind: "text", parsed: null, pretty: raw };
}

function formatByteSize(raw: string): string {
  const bytes = new Blob([raw]).size;
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}

const cacheValueNormalized = computed(() => normalizeCacheValue(cacheForm.value.cache_value));
const cacheValueFormat = computed<{ kind: CacheValueKind; label: string }>(() => {
  const { kind } = cacheValueNormalized.value;
  return { kind, label: kind === "json" ? "JSON" : kind === "text" ? "TEXT" : "EMPTY" };
});
const cacheValueSize = computed(() => formatByteSize(cacheForm.value.cache_value || ""));
const cacheValueLines = computed(() => {
  const text = cacheValueNormalized.value.pretty;
  return text ? text.split("\n").length : 0;
});

const copyCacheValue = async () => {
  try {
    await navigator.clipboard.writeText(cacheForm.value.cache_value || "");
    ElMessage.success("缓存内容已复制");
  } catch {
    ElMessage.error("复制失败，请手动选择内容");
  }
};

const copyRedisValue = async () => {
  try {
    await navigator.clipboard.writeText(redisValueNormalized.value.pretty);
    ElMessage.success("键值已复制");
  } catch {
    ElMessage.error("复制失败，请手动选择内容");
  }
};

let commandstatsInstance: echarts.ECharts | null = null;

const resetCacheForm = () => {
  cacheKeys.value = [];
  cacheForm.value = { cache_name: "", cache_key: "", cache_value: "" };
};

const getCacheNameList = async () => {
  try {
    loading.value = true;
    const response = await CacheAPI.getCacheNames();
    cacheNames.value = response.data.data;
    resetCacheForm();
  } catch (error: unknown) {
    if (import.meta.env.DEV) console.error("获取缓存列表出错:", error);
  } finally {
    loading.value = false;
  }
};

const handleClearCacheName = async (row: CacheInfo) => {
  try {
    await CacheAPI.deleteCacheName(row.cache_name);
    getCacheNameList();
    ElMessage.success("缓存已清理");
  } catch (error: unknown) {
    if (import.meta.env.DEV) console.error("清理缓存名称出错:", error);
  }
};

const getCacheKeyList = async (row?: CacheInfo) => {
  try {
    const cacheName = row?.cache_name || nowCacheName.value;
    if (!cacheName) return;
    subLoading.value = true;
    const response = await CacheAPI.getCacheKeys(cacheName);
    cacheKeys.value = response.data.data;
    nowCacheName.value = cacheName;
    cacheForm.value = { cache_name: cacheName, cache_key: "", cache_value: "" };
  } catch (error: unknown) {
    if (import.meta.env.DEV) console.error("获取缓存键名列表出错:", error);
  } finally {
    subLoading.value = false;
  }
};

async function handleClearCacheKey(cacheKey: string) {
  try {
    await CacheAPI.deleteCacheKey(cacheKey);
    getCacheKeyList();
    ElMessage.success("缓存键已清理");
  } catch (error: unknown) {
    if (import.meta.env.DEV) console.error("清理缓存键名出错:", error);
    ElMessage.error("清理缓存键失败，请稍后重试");
  }
}

async function handleCacheValue(cacheKey: string) {
  try {
    loading.value = true;
    const response = await CacheAPI.getCacheValue(nowCacheName.value, cacheKey);
    const data = response.data.data;
    cacheForm.value = {
      ...data,
      cache_value:
        typeof data.cache_value === "string"
          ? data.cache_value
          : JSON.stringify(data.cache_value, null, 2),
    };
  } catch (error: unknown) {
    if (import.meta.env.DEV) console.error("获取缓存内容失败:", error);
    ElMessage.error("获取缓存内容失败，请稍后重试");
  } finally {
    loading.value = false;
  }
}

const handleClearCacheAll = async () => {
  try {
    await ElMessageBox.confirm("确定要清理全部缓存吗？", "危险！", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    await CacheAPI.deleteCacheAll();
    getCacheNameList();
    ElMessage.success("全部缓存已清理");
  } catch (error: unknown) {
    if (error !== "cancel") {
      if (import.meta.env.DEV) console.error("清理全部缓存失败:", error);
      ElMessage.error("清理全部缓存失败，请稍后重试");
    }
  }
};

const getInfo = async (silent = false) => {
  if (!silent) refreshing.value = true;
  infoError.value = "";
  try {
    const response = await CacheAPI.getCacheInfo();
    cache.value = response.data.data || { info: {}, command_stats: [], db_size: 0 };
    updatedAt.value = new Date().toLocaleTimeString("zh-CN", { hour12: false });
    await nextTick();
    void initCharts();
  } catch (error: unknown) {
    if (import.meta.env.DEV) console.error("获取缓存监控数据失败:", error);
    infoError.value = error instanceof Error ? error.message : "获取缓存监控数据失败";
    if (!silent) ElMessage.error("获取缓存监控数据失败");
  } finally {
    refreshing.value = false;
  }
};

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
    if (document.visibilityState === "visible" && activeTab.value === "0") {
      void getInfo(true);
    }
  }, REFRESH_INTERVAL);
}

/** 等待容器完成布局（路由过渡/首次渲染时 clientWidth/Height 可能为 0），避免 ECharts "Can't get DOM width or height" 警告 */
const waitForSize = (el: HTMLElement): Promise<void> =>
  new Promise((resolve) => {
    const check = () => {
      if (commandstats.value !== el || (el.clientWidth > 0 && el.clientHeight > 0)) {
        resolve();
        return;
      }
      requestAnimationFrame(check);
    };
    check();
  });

const initCharts = async () => {
  if (!commandstats.value) return;
  await waitForSize(commandstats.value);
  if (!commandstats.value) return; // 等待期间组件被卸载

  commandstatsInstance?.dispose();
  commandstatsInstance = echarts.init(commandstats.value, "macarons");

  // 命令种类多时只展示 Top 8 + 其他，避免标签重叠成一团
  const rawStats = cache.value.command_stats || [];
  const sortedStats = [...rawStats].sort((a, b) => Number(b.value) - Number(a.value));
  const topStats: Array<{ name: string; value: number }> = sortedStats
    .slice(0, 8)
    .map((item) => ({ name: item.name, value: Number(item.value) || 0 }));
  const restStats = sortedStats.slice(8);
  if (restStats.length > 0) {
    topStats.push({
      name: "其他",
      value: restStats.reduce((sum, item) => sum + Number(item.value || 0), 0),
    });
  }
  commandstatsInstance.setOption({
    tooltip: { trigger: "item", formatter: "{a} <br/>{b} : {c} ({d}%)" },
    legend: {
      type: "scroll",
      bottom: 0,
      itemWidth: 10,
      itemHeight: 10,
      textStyle: { fontSize: 11 },
    },
    series: [
      {
        name: "命令",
        type: "pie",
        radius: ["34%", "66%"],
        center: ["50%", "45%"],
        minAngle: 2,
        data: topStats,
        animationEasing: "cubicInOut",
        animationDuration: 800,
        label: { show: false },
        labelLine: { show: false },
      },
    ],
  });
};

const handleChartResize = () => {
  commandstatsInstance?.resize();
};

onMounted(() => {
  getCacheNameList();
  getInfo();
  startRefreshTimer();
  window.addEventListener("resize", handleChartResize);
});

watch(autoRefresh, startRefreshTimer);

watch(activeTab, (tab) => {
  if (tab === "0") {
    nextTick(() => void initCharts());
  }
});

onActivated(() => {
  startRefreshTimer();
  if (activeTab.value === "0") nextTick(() => void initCharts());
});

onDeactivated(stopRefreshTimer);

onUnmounted(() => {
  stopRefreshTimer();
  window.removeEventListener("resize", handleChartResize);
  commandstatsInstance?.dispose();
});
</script>

<style scoped lang="scss">
.cache-manage {
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: 100%;
  min-height: 0;
  min-width: 0;
  padding-right: 2px;
}

.cache-manage__bar {
  display: flex;
  flex: none;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 16px 20px;
  border: 1px solid var(--fa-border-subtle);
  border-radius: 12px;
  background: var(--fa-surface);
}

.cache-manage__intro {
  min-width: 0;
}

.cache-manage__title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: var(--fa-text-1);
}

.cache-manage__desc {
  margin: 4px 0 0;
  font-size: 13px;
  line-height: 1.5;
  color: var(--fa-text-3);
}

.cache-manage__body {
  flex: 1;
  min-width: 0;
  min-height: 0;
}

.cache-manage__body.grid {
  overflow-y: auto;
}

.cache-scope-tag {
  max-width: 160px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cache-list {
  padding: 2px 0;
}

.cache-list__item {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
  padding: 10px 14px;
  cursor: pointer;
  border-bottom: 1px solid var(--fa-border-subtle);
  outline: none;
  transition:
    background-color 0.16s ease,
    box-shadow 0.16s ease;
}

.cache-list__item:last-child {
  border-bottom: none;
}

.cache-list__item:hover,
.cache-list__item:focus-visible {
  background: var(--el-fill-color-light);
}

.cache-list__item:focus-visible {
  box-shadow: inset 0 0 0 1px var(--el-color-primary);
}

.cache-list__item.is-active {
  background: var(--el-color-primary-light-9);
  box-shadow: inset 2px 0 0 var(--el-color-primary);
}

.cache-list__main {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
}

/* 键名列表没有名称+备注容器，让名称占满剩余宽度，删除图标自然落到行尾 */
.cache-list__item > .cache-list__name {
  flex: 1;
  min-width: 0;
}

.cache-list__name {
  overflow: hidden;
  color: var(--fa-text-1);
  font-size: 13px;
  font-weight: 500;
  line-height: 1.4;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cache-list__item.is-active .cache-list__name {
  color: var(--el-color-primary);
}

.cache-list__remark {
  overflow: hidden;
  color: var(--fa-text-3);
  font-size: 12px;
  line-height: 1.4;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cache-list__delete {
  flex: none;
  opacity: 0.45;
  transition: opacity 0.16s ease;
}

.cache-list__item:hover .cache-list__delete,
.cache-list__item:focus-within .cache-list__delete {
  opacity: 1;
}

.cache-list-empty {
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: center;
  min-height: 0;
}

.cache-value-panel {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 10px;
  min-height: 0;
}

.cache-value-context {
  display: flex;
  align-items: center;
  gap: 6px;
  min-width: 0;
  padding: 8px 10px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
  background: var(--el-fill-color-lighter);
  border-radius: 8px;
}

.cache-value-context__label,
.cache-value-context__sep {
  flex: none;
  color: var(--el-text-color-placeholder);
}

.cache-value-context__value,
.cache-value-context__key {
  min-width: 0;
  overflow: hidden;
  font-family: var(--fa-font-mono);
  color: var(--el-text-color-regular);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cache-value-context__value {
  max-width: 45%;
}

.cache-value-context__key {
  flex: 1;
}

.cache-value-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.cache-format-tag {
  display: inline-flex;
  align-items: center;
  height: 20px;
  padding: 0 6px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.04em;
  border-radius: 4px;
}

.cache-format-tag.is-json {
  color: var(--el-color-primary);
  background: var(--el-color-primary-light-9);
}

.cache-format-tag.is-text,
.cache-format-tag.is-empty {
  color: var(--el-text-color-secondary);
  background: var(--el-fill-color-light);
}

.cache-value-size {
  overflow: hidden;
  font-size: 12px;
  color: var(--el-text-color-secondary);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cache-value-body {
  flex: 1;
  min-height: 0;
  padding: 12px 14px;
  overflow: auto;
  background: var(--el-fill-color-blank);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 8px;
}

.cache-value-body pre {
  margin: 0;
  font-family: var(--fa-font-mono);
  font-size: 12px;
  line-height: 1.65;
  color: var(--el-text-color-regular);
  white-space: pre;
}

.cache-value-body.is-wrapped pre {
  white-space: pre-wrap;
  word-break: break-word;
}

.cache-value-body :deep(.vjs-tree) {
  font-family: var(--fa-font-mono);
  font-size: 12px;
  line-height: 1.65;
}

.cache-value-body :deep(.vjs-tree__content) {
  font-family: var(--fa-font-mono);
}

.keyspace-drawer :deep(.el-drawer__body) {
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.keyspace-workspace {
  display: flex;
  flex: 1;
  min-height: 0;
}

.keyspace-workspace > .el-card {
  flex: 1;
  min-height: 0;
}

.keyspace-value {
  display: flex;
  flex-direction: column;
  gap: 10px;
  height: min(52vh, 460px);
  margin-top: 12px;
}

.keyspace-workspace > .el-card {
  flex: 1;
  min-height: 0;
}

@media (min-width: 1280px) {
  .cache-manage__body.grid {
    overflow: hidden;
  }
}

.cache-monitor {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 0;
  min-height: 0;
  height: 100%;
  overflow-y: auto;
  padding-right: 2px;
}

.cache-monitor > * {
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

.monitor-kpi__value {
  font-size: 30px;
  font-weight: 600;
  line-height: 1;
  color: var(--fa-text-1);
  font-variant-numeric: tabular-nums;
}

.monitor-kpi__value small {
  margin-left: 3px;
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

.cache-grid {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(0, 1fr);
  gap: 16px;
  align-items: stretch;
}

.monitor-panel {
  border-radius: 12px;
  border-color: var(--fa-border-subtle);
  background: var(--fa-surface);
}

.monitor-panel :deep(.el-card__header) {
  padding: 14px 20px;
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

.monitor-panel__hint {
  font-size: 12px;
  font-weight: 400;
  color: var(--fa-text-3);
}

.cache-chart-card :deep(.el-card__body) {
  position: relative;
  height: 340px;
  padding: 8px 12px 12px;
}

.cache-chart {
  width: 100%;
  height: 100%;
}

.cache-chart__empty {
  position: absolute;
  inset: 8px 12px 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cache-memory-card :deep(.el-card__body) {
  height: 340px;
  padding: 18px 20px;
}

.cache-memory {
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: 100%;
}

.cache-memory__main {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.cache-memory__main span {
  font-size: 12px;
  color: var(--fa-text-3);
}

.cache-memory__main strong {
  font-size: 34px;
  font-weight: 600;
  line-height: 1.1;
  color: var(--fa-text-1);
  font-variant-numeric: tabular-nums;
}

.cache-memory__main small {
  font-size: 12px;
  color: var(--fa-text-3);
}

.cache-memory__hint {
  padding: 10px 12px;
  border-radius: 8px;
  background: var(--fa-surface-2);
  font-size: 12px;
  line-height: 1.6;
  color: var(--fa-text-3);
}

.cache-memory__facts {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
  margin-top: auto;
}

.cache-memory__facts > div {
  padding: 10px 12px;
  border-radius: 8px;
  background: var(--fa-surface-2);
  min-width: 0;
}

.cache-memory__facts span {
  display: block;
  font-size: 12px;
  color: var(--fa-text-3);
}

.cache-memory__facts strong {
  display: block;
  margin-top: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 14px;
  color: var(--fa-text-1);
  font-variant-numeric: tabular-nums;
}

.cache-health {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.cache-health span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 9px;
  border-radius: 999px;
  font-size: 12px;
  color: var(--fa-text-2);
  background: var(--fa-surface-2);
}

.cache-health i {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--el-color-success);
}

.cache-health .is-off {
  color: var(--fa-text-3);
}

.cache-health .is-off i {
  background: var(--fa-text-3);
}

.cache-health .is-danger {
  color: var(--el-color-danger);
}

.cache-health .is-danger i {
  background: var(--el-color-danger);
}

.cache-instance {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.cache-instance__item {
  padding: 12px 14px;
  border-radius: 8px;
  background: var(--fa-surface-2);
  min-width: 0;
}

.cache-instance__item span {
  display: block;
  font-size: 12px;
  color: var(--fa-text-3);
}

.cache-instance__item strong {
  display: block;
  margin-top: 5px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 14px;
  font-weight: 600;
  color: var(--fa-text-1);
}

@media (max-width: 1200px) {
  .cache-grid {
    grid-template-columns: minmax(0, 1fr);
  }
}

@media (max-width: 1100px) {
  .monitor-kpis {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .cache-instance {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .monitor-kpis,
  .cache-instance {
    grid-template-columns: minmax(0, 1fr);
  }

  .monitor-head {
    padding: 16px;
  }

  .cache-chart-card :deep(.el-card__body),
  .cache-memory-card :deep(.el-card__body) {
    height: 320px;
  }
}
</style>
