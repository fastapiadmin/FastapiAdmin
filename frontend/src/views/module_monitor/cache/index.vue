<template>
  <div class="app-container">
    <el-tabs type="border-card">
      <!-- 监控信息 Tab -->
      <el-tab-pane class="monitor" label="监控信息">
        <el-row :gutter="16">
          <!-- 基本信息 -->
          <el-col :span="24">
            <el-card shadow="hover">
              <template #header>
                <div class="flex items-center gap-2">
                  <el-icon>
                    <Monitor />
                  </el-icon>
                  <span>Redis监控信息</span>
                  <el-tooltip content="展示Redis监控信息详情">
                    <el-icon>
                      <QuestionFilled />
                    </el-icon>
                  </el-tooltip>
                </div>
              </template>
              <el-descriptions :column="12" border :direction="'vertical'">
                <el-descriptions-item label="Redis版本">
                  {{ cache.info?.redis_version || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="运行模式">
                  {{ cache.info?.redis_mode === "standalone" ? "单机" : "集群" }}
                </el-descriptions-item>
                <el-descriptions-item label="端口">
                  {{ cache.info?.tcp_port || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="客户端数">
                  {{ cache.info?.connected_clients || 0 }}
                </el-descriptions-item>
                <el-descriptions-item label="运行时间(天)">
                  {{ cache.info?.uptime_in_days || 0 }}
                </el-descriptions-item>
                <el-descriptions-item label="使用内存">
                  {{ cache.info?.used_memory_human || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="使用CPU">
                  {{
                    cache.info?.used_cpu_user_children
                      ? parseFloat(cache.info.used_cpu_user_children).toFixed(2)
                      : "-"
                  }}
                </el-descriptions-item>
                <el-descriptions-item label="内存配置">
                  {{ cache.info?.maxmemory_human || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="AOF是否开启">
                  {{ cache.info?.aof_enabled === "0" ? "否" : "是" }}
                </el-descriptions-item>
                <el-descriptions-item label="RDB是否成功">
                  {{ cache.info?.rdb_last_bgsave_status || "-" }}
                </el-descriptions-item>
                <el-descriptions-item label="Key数量">
                  {{ cache.db_size || 0 }}
                </el-descriptions-item>
                <el-descriptions-item label="网络入口/出口">
                  {{
                    `${cache.info?.instantaneous_input_kbps || 0}kps/${cache.info?.instantaneous_output_kbps || 0}kps`
                  }}
                </el-descriptions-item>
              </el-descriptions>
            </el-card>
          </el-col>

          <!-- 监控图表 -->
          <el-col :span="12" class="mt-4">
            <el-card shadow="hover">
              <template #header>
                <div class="flex items-center gap-2">
                  <el-icon>
                    <Stopwatch />
                  </el-icon>
                  <span class="title">命令统计</span>
                  <el-tooltip content="展示命令统计详情">
                    <el-icon>
                      <QuestionFilled />
                    </el-icon>
                  </el-tooltip>
                </div>
              </template>
              <div ref="commandstats" class="chart-container" />
            </el-card>
          </el-col>

          <el-col :span="12" class="mt-4">
            <el-card shadow="hover">
              <template #header>
                <div class="flex items-center gap-2">
                  <el-icon>
                    <Stopwatch />
                  </el-icon>
                  <span>内存信息</span>
                  <el-tooltip content="展示内存信息详情">
                    <el-icon>
                      <QuestionFilled />
                    </el-icon>
                  </el-tooltip>
                </div>
              </template>
              <div ref="usedmemory" class="chart-container" />
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>

      <!-- 缓存管理 Tab -->
      <el-tab-pane class="cache" label="缓存管理">
        <el-row :gutter="16">
          <!-- 缓存列表 -->
          <el-col :span="8">
            <el-card :loading="loading" shadow="hover">
              <template #header>
                <div class="flex justify-between items-center">
                  <div class="flex items-center gap-2">
                    <el-icon>
                      <Tickets />
                    </el-icon>
                    <span class="flex items-center gap-2">缓存列表</span>
                    <el-tooltip content="展示缓存列表详情">
                      <el-icon>
                        <QuestionFilled />
                      </el-icon>
                    </el-tooltip>
                  </div>
                  <div>
                    <el-button
                      v-hasPerm="['module_monitor:cache:query']"
                      type="primary"
                      link
                      icon="RefreshRight"
                      @click="refreshCacheNames"
                    />
                  </div>
                </div>
              </template>
              <el-table
                :loading="loading"
                :data="cacheNames"
                row-key="cache_name"
                height="calc(100vh - 280px)"
                max-height="calc(100vh - 280px)"
                border
              >
                <template #empty>
                  <el-empty :image-size="80" description="暂无数据" />
                </template>
                <el-table-column prop="cache_name" label="缓存名称" show-overflow-tooltip>
                  <template #default="{ row }">
                    <el-button
                      v-hasPerm="['module_monitor:cache:query']"
                      type="primary"
                      link
                      @click="getCacheKeyList(row)"
                    >
                      {{ row.cache_name }}
                    </el-button>
                  </template>
                </el-table-column>
                <el-table-column prop="remark" label="备注" show-overflow-tooltip />
                <el-table-column label="操作" width="60" align="center">
                  <template #default="{ row }">
                    <el-popconfirm
                      class="box-item"
                      :title="`确认删除缓存 ${row.cache_name} 吗？`"
                      placement="top"
                      @confirm="handleClearCacheName(row)"
                    >
                      <template #reference>
                        <el-button
                          v-hasPerm="['module_monitor:cache:delete']"
                          type="danger"
                          size="small"
                          link
                          icon="delete"
                        />
                      </template>
                    </el-popconfirm>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-col>

          <!-- 键名列表 -->
          <el-col :span="8">
            <el-card :loading="loading" shadow="hover">
              <template #header>
                <div class="flex justify-between items-center">
                  <div class="flex items-center gap-2">
                    <el-icon>
                      <Key />
                    </el-icon>
                    <span class="flex items-center gap-2">键名列表</span>
                    <el-tooltip content="展示键名列表详情">
                      <el-icon>
                        <QuestionFilled />
                      </el-icon>
                    </el-tooltip>
                  </div>
                  <div>
                    <el-button
                      v-hasPerm="['module_monitor:cache:query']"
                      type="primary"
                      link
                      icon="RefreshRight"
                      @click="refreshCacheKeys"
                    />
                  </div>
                </div>
              </template>
              <el-table
                :loading="subLoading"
                :data="cacheKeys.map((key) => ({ cacheKey: key }))"
                height="calc(100vh - 280px)"
                max-height="calc(100vh - 280px)"
                row-key="cacheKey"
                border
              >
                <template #empty>
                  <el-empty :image-size="80" description="暂无数据" />
                </template>
                <el-table-column prop="cacheKey" label="缓存键名" show-overflow-tooltip>
                  <template #default="{ row }">
                    <el-button
                      v-hasPerm="['module_monitor:cache:detail']"
                      type="primary"
                      link
                      @click="handleCacheValue(row.cacheKey)"
                    >
                      {{ row.cacheKey }}
                    </el-button>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="60" align="center">
                  <template #default="{ row }">
                    <el-popconfirm
                      class="box-item"
                      :title="`确认删除键 ${row.cacheKey} 吗？`"
                      placement="top"
                      @confirm="handleClearCacheKey(row.cacheKey)"
                    >
                      <template #reference>
                        <el-button
                          v-hasPerm="['module_monitor:cache:delete']"
                          type="danger"
                          size="small"
                          link
                          icon="delete"
                        />
                      </template>
                    </el-popconfirm>
                  </template>
                </el-table-column>
              </el-table>
            </el-card>
          </el-col>

          <!-- 缓存内容 -->
          <el-col :span="8">
            <el-card :loading="loading" shadow="hover">
              <template #header>
                <div class="flex justify-between items-center">
                  <div class="flex items-center gap-2">
                    <el-icon>
                      <Key />
                    </el-icon>
                    <span class="flex items-center gap-2">缓存内容</span>
                    <el-tooltip content="展示缓存内容详情">
                      <el-icon>
                        <QuestionFilled />
                      </el-icon>
                    </el-tooltip>
                  </div>
                  <div>
                    <el-button
                      v-hasPerm="['module_monitor:cache:delete']"
                      type="danger"
                      link
                      icon="delete"
                      @click="handleClearCacheAll"
                    >
                      清理全部
                    </el-button>
                  </div>
                </div>
              </template>
              <el-form :model="cacheForm" label-suffix=":" label-width="auto" label-position="top">
                <el-form-item label="缓存名称">
                  <el-input v-model="cacheForm.cache_name" readonly placeholder="缓存名称" />
                </el-form-item>
                <el-form-item label="缓存键名">
                  <el-input v-model="cacheForm.cache_key" readonly placeholder="缓存键名" />
                </el-form-item>
                <el-form-item label="缓存内容">
                  <el-input
                    v-model="cacheForm.cache_value"
                    type="textarea"
                    :rows="20"
                    readonly
                    placeholder="缓存内容"
                  />
                </el-form-item>
              </el-form>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script lang="ts" setup>
import CacheAPI, {
  type CacheInfo,
  type CacheForm,
  type CacheMonitor,
  type RedisInfo,
} from "@/api/module_monitor/cache";
import * as echarts from "echarts";

// 响应式状态定义
const cacheNames = ref<CacheInfo[]>([]);
const cacheKeys = ref<string[]>([]);
const loading = ref(true);
const subLoading = ref(false);
const nowCacheName = ref("");
const commandstats = ref<HTMLElement | null>(null);
const usedmemory = ref<HTMLElement | null>(null);
const cache = ref<CacheMonitor>({
  info: {} as RedisInfo,
  command_stats: [],
  db_size: 0,
});
const cacheForm = ref<CacheForm>({
  cache_name: "",
  cache_key: "",
  cache_value: "",
});

let commandstatsInstance: echarts.ECharts | null = null;
let usedmemoryInstance: echarts.ECharts | null = null;

const resetCacheForm = () => {
  cacheKeys.value = [];
  cacheForm.value = {
    cache_name: "",
    cache_key: "",
    cache_value: "",
  };
};

// 缓存名称相关方法
const getCacheNameList = async () => {
  try {
    loading.value = true;
    const response = await CacheAPI.getCacheNames();
    cacheNames.value = response.data.data;
    resetCacheForm();
  } catch (error) {
    console.error("获取缓存列表出错:", error);
  } finally {
    loading.value = false;
  }
};

// 刷新缓存列表
const refreshCacheNames = () => {
  getCacheNameList();
};

// 清理缓存名称
const handleClearCacheName = async (row: CacheInfo) => {
  try {
    await CacheAPI.deleteCacheName(row.cache_name);
    refreshCacheNames();
  } catch (error) {
    console.error("清理缓存名称出错:", error);
  }
};

// 缓存键名相关方法
const getCacheKeyList = async (row?: CacheInfo) => {
  try {
    const cacheName = row?.cache_name || nowCacheName.value;
    if (!cacheName) return;

    subLoading.value = true;
    const response = await CacheAPI.getCacheKeys(cacheName);
    cacheKeys.value = response.data.data;
    nowCacheName.value = cacheName;
    cacheForm.value = {
      cache_name: cacheName,
      cache_key: "",
      cache_value: "",
    };
  } catch (error) {
    console.error("获取缓存键名列表出错:", error);
  } finally {
    subLoading.value = false;
  }
};

// 刷新键名列表
const refreshCacheKeys = () => {
  getCacheKeyList();
};

// 清理缓存键名
async function handleClearCacheKey(cacheKey: string) {
  try {
    await CacheAPI.deleteCacheKey(cacheKey);
    getCacheKeyList();
  } catch (error) {
    console.error("清理缓存键名出错:", error);
  }
}

// 缓存内容相关方法
async function handleCacheValue(cacheKey: string) {
  try {
    loading.value = true;
    const response = await CacheAPI.getCacheValue(nowCacheName.value, cacheKey);
    cacheForm.value = response.data.data;
  } catch (error) {
    console.error("获取缓存内容失败:", error);
  } finally {
    loading.value = false;
  }
}

// 清理全部缓存
const handleClearCacheAll = async () => {
  ElMessageBox.confirm("确定要清理全部缓存吗？", "危险！", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      return await CacheAPI.deleteCacheAll();
    })
    .then(() => {
      getCacheNameList();
    })
    .catch((error) => {
      if (error !== "cancel") {
        console.error("清理全部缓存失败:", error);
      }
    });
};

// 监控数据获取
const getInfo = async () => {
  try {
    loading.value = true;
    const response = await CacheAPI.getCacheInfo();
    cache.value = response.data.data || {
      info: {},
      command_stats: [],
      dbSize: 0,
    };
    initCharts();
  } catch (error) {
    console.error("获取缓存监控数据失败:", error);
  } finally {
    loading.value = false;
  }
};

// 图表初始化
const initCharts = () => {
  if (!commandstats.value || !usedmemory.value) return;

  commandstatsInstance = echarts.init(commandstats.value, "macarons");
  usedmemoryInstance = echarts.init(usedmemory.value, "macarons");

  const commandStatsOption = {
    tooltip: {
      trigger: "item",
      formatter: "{a} <br/>{b} : {c} ({d}%)",
    },
    series: [
      {
        name: "命令",
        type: "pie",
        roseType: "radius",
        radius: [15, 95],
        center: ["50%", "38%"],
        data: cache.value.command_stats || [],
        animationEasing: "cubicInOut",
        animationDuration: 1000,
      },
    ],
  };

  const usedMemory = cache.value.info?.used_memory_human || "0";
  const usedMemoryOption = {
    tooltip: {
      formatter: `{b} <br/>{a} : ${usedMemory}`,
    },
    series: [
      {
        name: "峰值",
        type: "gauge",
        min: 0,
        max: 1000,
        detail: {
          formatter: usedMemory,
        },
        data: [
          {
            value: parseFloat(usedMemory) || 0,
            name: "内存消耗",
          },
        ],
      },
    ],
  };

  commandstatsInstance.setOption(commandStatsOption);
  usedmemoryInstance.setOption(usedMemoryOption);
};

// 生命周期钩子
onMounted(() => {
  getCacheNameList();
  getInfo();
});

onUnmounted(() => {
  commandstatsInstance?.dispose();
  usedmemoryInstance?.dispose();
});
</script>

<style scoped lang="scss">
.chart-container {
  height: calc(100vh - 480px);
}
</style>
