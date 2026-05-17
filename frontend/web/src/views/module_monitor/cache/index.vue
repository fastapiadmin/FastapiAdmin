<template>
  <div class="fa-full-height">
    <ElTabs>
      <!-- 监控信息 Tab -->
      <ElTabPane label="监控信息">
        <div class="monitor-tab">
          <ElRow :gutter="16">
            <ElCol :span="24">
              <ElCard shadow="hover">
                <template #header>
                  <div class="flex items-center gap-2">
                    <FaSvgIcon icon="ri:database-2-line" class="text-lg" />
                    <span class="font-medium">Redis监控信息</span>
                  </div>
                </template>
                <FaDescriptions :column="6" :scrollbar="false">
                  <ElDescriptionsItem label="Redis版本">
                    {{ cache.info?.redis_version || "-" }}
                  </ElDescriptionsItem>
                  <ElDescriptionsItem label="运行模式">
                    {{ cache.info?.redis_mode === "standalone" ? "单机" : "集群" }}
                  </ElDescriptionsItem>
                  <ElDescriptionsItem label="端口">
                    {{ cache.info?.tcp_port || "-" }}
                  </ElDescriptionsItem>
                  <ElDescriptionsItem label="客户端数">
                    {{ cache.info?.connected_clients || 0 }}
                  </ElDescriptionsItem>
                  <ElDescriptionsItem label="运行时间(天)">
                    {{ cache.info?.uptime_in_days || 0 }}
                  </ElDescriptionsItem>
                  <ElDescriptionsItem label="使用内存">
                    {{ cache.info?.used_memory_human || "-" }}
                  </ElDescriptionsItem>
                  <ElDescriptionsItem label="使用CPU">
                    {{
                      cache.info?.used_cpu_user_children
                        ? parseFloat(cache.info.used_cpu_user_children).toFixed(2)
                        : "-"
                    }}
                  </ElDescriptionsItem>
                  <ElDescriptionsItem label="内存配置">
                    {{ cache.info?.maxmemory_human || "-" }}
                  </ElDescriptionsItem>
                  <ElDescriptionsItem label="AOF">
                    {{ cache.info?.aof_enabled === "0" ? "关闭" : "开启" }}
                  </ElDescriptionsItem>
                  <ElDescriptionsItem label="RDB状态">
                    {{ cache.info?.rdb_last_bgsave_status || "-" }}
                  </ElDescriptionsItem>
                  <ElDescriptionsItem label="Key数量">
                    {{ cache.db_size || 0 }}
                  </ElDescriptionsItem>
                  <ElDescriptionsItem label="网络IO">
                    {{ cache.info?.instantaneous_input_kbps || 0 }}kps/
                    {{ cache.info?.instantaneous_output_kbps || 0 }}kps
                  </ElDescriptionsItem>
                </FaDescriptions>
              </ElCard>
            </ElCol>
          </ElRow>

          <ElRow :gutter="16" class="flex-1 min-h-0">
            <ElCol :span="12" class="flex flex-col min-h-0">
              <ElCard shadow="hover" class="flex-1 flex flex-col chart-card">
                <template #header>
                  <div class="flex items-center gap-2">
                    <FaSvgIcon icon="ri:bar-chart-2-line" class="text-lg" />
                    <span class="font-medium">命令统计</span>
                  </div>
                </template>
                <div ref="commandstats" class="chart-container" />
              </ElCard>
            </ElCol>
            <ElCol :span="12" class="flex flex-col min-h-0">
              <ElCard shadow="hover" class="flex-1 flex flex-col chart-card">
                <template #header>
                  <div class="flex items-center gap-2">
                    <FaSvgIcon icon="ri:pie-chart-2-line" class="text-lg" />
                    <span class="font-medium">内存信息</span>
                  </div>
                </template>
                <div ref="usedmemory" class="chart-container" />
              </ElCard>
            </ElCol>
          </ElRow>
        </div>
      </ElTabPane>

      <!-- 缓存管理 Tab -->
      <ElTabPane label="缓存管理">
        <div class="cache-mgmt-tab">
          <ElRow :gutter="16" class="flex-1 min-h-0">
            <!-- 缓存列表 -->
            <ElCol :span="8" class="cache-mgmt-col">
              <ElCard :loading="loading" shadow="hover" class="cache-mgmt-card">
                <template #header>
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-2">
                      <FaSvgIcon icon="ri:list-unordered" class="text-lg" />
                      <span class="font-medium">缓存列表</span>
                    </div>
                    <ElButton
                      v-hasPerm="['module_monitor:cache:query']"
                      type="primary"
                      link
                      icon="RefreshRight"
                      @click="refreshCacheNames"
                    />
                  </div>
                </template>
                <div class="cache-table-wrap">
                  <ElTable :loading="loading" :data="cacheNames" row-key="cache_name">
                    <template #empty>
                      <ElEmpty :image-size="80" description="暂无数据" />
                    </template>
                    <ElTableColumn prop="cache_name" label="缓存名称" show-overflow-tooltip>
                      <template #default="{ row }">
                        <ElButton
                          v-hasPerm="['module_monitor:cache:query']"
                          type="primary"
                          link
                          @click="getCacheKeyList(row)"
                        >
                          {{ row.cache_name }}
                        </ElButton>
                      </template>
                    </ElTableColumn>
                    <ElTableColumn prop="remark" label="备注" show-overflow-tooltip />
                    <ElTableColumn label="操作" width="60" align="center">
                      <template #default="{ row }">
                        <ElPopconfirm
                          :title="`确认删除缓存 ${row.cache_name} 吗？`"
                          placement="top"
                          @confirm="handleClearCacheName(row)"
                        >
                          <template #reference>
                            <ElButton
                              v-hasPerm="['module_monitor:cache:delete']"
                              type="danger"
                              size="small"
                              link
                              icon="delete"
                            />
                          </template>
                        </ElPopconfirm>
                      </template>
                    </ElTableColumn>
                  </ElTable>
                </div>
              </ElCard>
            </ElCol>

            <!-- 键名列表 -->
            <ElCol :span="8" class="cache-mgmt-col">
              <ElCard :loading="loading" shadow="hover" class="cache-mgmt-card">
                <template #header>
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-2">
                      <FaSvgIcon icon="ri:key-2-line" class="text-lg" />
                      <span class="font-medium">键名列表</span>
                    </div>
                    <ElButton
                      v-hasPerm="['module_monitor:cache:query']"
                      type="primary"
                      link
                      icon="RefreshRight"
                      @click="refreshCacheKeys"
                    />
                  </div>
                </template>
                <div class="cache-table-wrap">
                  <ElTable
                    :loading="subLoading"
                    :data="cacheKeys.map((key) => ({ cacheKey: key }))"
                    row-key="cacheKey"
                  >
                    <template #empty>
                      <ElEmpty :image-size="80" description="暂无数据" />
                    </template>
                    <ElTableColumn prop="cacheKey" label="缓存键名" show-overflow-tooltip>
                      <template #default="{ row }">
                        <ElButton
                          v-hasPerm="['module_monitor:cache:detail']"
                          type="primary"
                          link
                          @click="handleCacheValue(row.cacheKey)"
                        >
                          {{ row.cacheKey }}
                        </ElButton>
                      </template>
                    </ElTableColumn>
                    <ElTableColumn label="操作" width="60" align="center">
                      <template #default="{ row }">
                        <ElPopconfirm
                          :title="`确认删除键 ${row.cacheKey} 吗？`"
                          placement="top"
                          @confirm="handleClearCacheKey(row.cacheKey)"
                        >
                          <template #reference>
                            <ElButton
                              v-hasPerm="['module_monitor:cache:delete']"
                              type="danger"
                              size="small"
                              link
                              icon="delete"
                            />
                          </template>
                        </ElPopconfirm>
                      </template>
                    </ElTableColumn>
                  </ElTable>
                </div>
              </ElCard>
            </ElCol>

            <!-- 缓存内容 -->
            <ElCol :span="8" class="cache-mgmt-col">
              <ElCard :loading="loading" shadow="hover" class="cache-mgmt-card">
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
                      icon="delete"
                      @click="handleClearCacheAll"
                    >
                      清理全部
                    </ElButton>
                  </div>
                </template>
                <div class="cache-form-wrap">
                  <ElForm :model="cacheForm" label-suffix=":" label-position="top">
                    <ElFormItem label="缓存名称">
                      <ElInput v-model="cacheForm.cache_name" readonly placeholder="缓存名称" />
                    </ElFormItem>
                    <ElFormItem label="缓存键名">
                      <ElInput v-model="cacheForm.cache_key" readonly placeholder="缓存键名" />
                    </ElFormItem>
                    <ElFormItem label="缓存内容" class="cache-value-item">
                      <ElInput
                        v-model="cacheForm.cache_value"
                        type="textarea"
                        readonly
                        placeholder="缓存内容"
                      />
                    </ElFormItem>
                  </ElForm>
                </div>
              </ElCard>
            </ElCol>
          </ElRow>
        </div>
      </ElTabPane>
    </ElTabs>
  </div>
</template>

<script lang="ts" setup>
import FaDescriptions from "@/components/others/fa-descriptions/index.vue";
import { ElMessageBox } from "element-plus";
import CacheAPI, {
  type CacheInfo,
  type CacheForm,
  type CacheMonitor,
  type RedisInfo,
} from "@/api/module_monitor/cache";
import * as echarts from "echarts";

defineOptions({ name: "CacheMonitor" });

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
  cacheForm.value = { cache_name: "", cache_key: "", cache_value: "" };
};

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

const refreshCacheNames = () => {
  getCacheNameList();
};

const handleClearCacheName = async (row: CacheInfo) => {
  try {
    await CacheAPI.deleteCacheName(row.cache_name);
    refreshCacheNames();
  } catch (error) {
    console.error("清理缓存名称出错:", error);
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
  } catch (error) {
    console.error("获取缓存键名列表出错:", error);
  } finally {
    subLoading.value = false;
  }
};

const refreshCacheKeys = () => {
  getCacheKeyList();
};

async function handleClearCacheKey(cacheKey: string) {
  try {
    await CacheAPI.deleteCacheKey(cacheKey);
    getCacheKeyList();
  } catch (error) {
    console.error("清理缓存键名出错:", error);
  }
}

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

const handleClearCacheAll = async () => {
  try {
    await ElMessageBox.confirm("确定要清理全部缓存吗？", "危险！", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    await CacheAPI.deleteCacheAll();
    getCacheNameList();
  } catch (error: unknown) {
    if (error !== "cancel") {
      console.error("清理全部缓存失败:", error);
    }
  }
};

const getInfo = async () => {
  try {
    loading.value = true;
    const response = await CacheAPI.getCacheInfo();
    cache.value = response.data.data || { info: {}, command_stats: [], dbSize: 0 };
    initCharts();
  } catch (error) {
    console.error("获取缓存监控数据失败:", error);
  } finally {
    loading.value = false;
  }
};

const initCharts = () => {
  if (!commandstats.value || !usedmemory.value) return;

  commandstatsInstance = echarts.init(commandstats.value, "macarons");
  usedmemoryInstance = echarts.init(usedmemory.value, "macarons");

  commandstatsInstance.setOption({
    tooltip: { trigger: "item", formatter: "{a} <br/>{b} : {c} ({d}%)" },
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
  });

  const usedMemory = cache.value.info?.used_memory_human || "0";
  usedmemoryInstance.setOption({
    tooltip: { formatter: `{b} <br/>{a} : ${usedMemory}` },
    series: [
      {
        name: "峰值",
        type: "gauge",
        min: 0,
        max: 1000,
        detail: { formatter: usedMemory },
        data: [{ value: parseFloat(usedMemory) || 0, name: "内存消耗" }],
      },
    ],
  });

  void nextTick(() => {
    commandstatsInstance?.resize();
    usedmemoryInstance?.resize();
  });
};

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
// 与 dashboard 首页一致：自定义圆角 + 边框色
:deep(.el-card) {
  --el-card-border-radius: calc(var(--custom-radius) + 2px);

  border: 1px solid var(--fa-card-border);
}

.fa-full-height {
  :deep(.el-tabs) {
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;

    > .el-tabs__content {
      display: flex;
      flex: 1;
      flex-direction: column;
      min-height: 0;

      > .el-tab-pane {
        display: flex;
        flex: 1;
        flex-direction: column;
        min-height: 0;
        overflow: hidden;
      }
    }
  }
}

.monitor-tab {
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: 100%;
  min-height: 0;
}

.chart-card {
  :deep(.el-card__body) {
    display: flex;
    flex: 1;
    flex-direction: column;
    min-height: 0;
  }
}

.chart-container {
  flex: 1;
  min-height: 200px;
}

// === 缓存管理三栏 ===
.cache-mgmt-tab {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
}

.cache-mgmt-col {
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.cache-mgmt-card {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;

  :deep(.el-card__body) {
    display: flex;
    flex: 1;
    flex-direction: column;
    min-height: 0;

    > .cache-table-wrap,
    > .cache-form-wrap {
      flex: 1;
      min-height: 0;
    }
  }
}

.cache-table-wrap {
  position: relative;
  overflow: hidden;

  :deep(.el-table) {
    position: absolute;
    inset: 0;
    height: auto;

    .el-table__inner-wrapper {
      display: flex;
      flex-direction: column;
      height: 100%;
    }

    .el-table__header-wrapper {
      flex-shrink: 0;
    }

    .el-table__body-wrapper {
      flex: 1;
      overflow-y: auto;
    }
  }
}

.cache-form-wrap {
  display: flex;
  flex-direction: column;

  .el-form {
    display: flex;
    flex: 1;
    flex-direction: column;
    min-height: 0;
  }
}

.cache-value-item {
  flex: 1;
  min-height: 0;
  max-height: 60%;

  :deep(.el-form-item__content) {
    height: 100%;

    .el-textarea {
      height: 100%;

      textarea {
        height: 100% !important;
        resize: none;
      }
    }
  }
}
</style>
