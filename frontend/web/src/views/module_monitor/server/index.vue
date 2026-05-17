<template>
  <div class="server-container">
    <ElRow :gutter="16" class="server-row">
      <!-- CPU 使用情况 -->
      <ElCol :span="12" class="server-col">
        <ElCard :loading="loading" shadow="hover" class="server-card">
          <template #header>
            <div class="flex items-center gap-2">
              <FaSvgIcon icon="ri:cpu-line" class="text-lg" />
              <span class="font-medium">CPU使用情况</span>
            </div>
          </template>
          <div class="flex-c flex-col gap-4">
            <div class="flex-c gap-6">
              <ElProgress
                type="circle"
                :percentage="server.cpu?.used || 0"
                :status="
                  (server.cpu?.used || 0) > 80
                    ? 'exception'
                    : (server.cpu?.used || 0) > 60
                      ? 'warning'
                      : 'success'
                "
              >
                <span class="text-sm">{{ (server.cpu?.used || 0).toFixed(1) }}%</span>
              </ElProgress>
              <FaDescriptions :column="2" size="small" :scrollbar="false">
                <ElDescriptionsItem label="核心数">
                  {{ server.cpu?.cpu_num || 0 }}
                </ElDescriptionsItem>
                <ElDescriptionsItem label="已用核心">
                  {{ Math.floor(((server.cpu?.used || 0) * (server.cpu?.cpu_num || 0)) / 100) }}
                </ElDescriptionsItem>
                <ElDescriptionsItem label="用户使用率">
                  {{ (server.cpu?.used || 0).toFixed(1) }}%
                </ElDescriptionsItem>
                <ElDescriptionsItem label="系统使用率">
                  {{ (server.cpu?.sys || 0).toFixed(1) }}%
                </ElDescriptionsItem>
              </FaDescriptions>
            </div>
          </div>
        </ElCard>
      </ElCol>

      <!-- 内存使用情况 -->
      <ElCol :span="12" class="server-col">
        <ElCard :loading="loading" shadow="hover" class="server-card">
          <template #header>
            <div class="flex items-center gap-2">
              <FaSvgIcon icon="ri:memory-line" class="text-lg" />
              <span class="font-medium">内存使用情况</span>
            </div>
          </template>
          <div class="flex-c flex-col gap-4">
            <div class="flex-c gap-6">
              <ElProgress
                type="circle"
                :percentage="server.mem?.usage || 0"
                :status="
                  (server.mem?.usage || 0) > 80
                    ? 'exception'
                    : (server.mem?.usage || 0) > 60
                      ? 'warning'
                      : 'success'
                "
              >
                <span class="text-sm">{{ (server.mem?.usage || 0).toFixed(1) }}%</span>
              </ElProgress>
              <FaDescriptions :column="2" size="small" :scrollbar="false">
                <ElDescriptionsItem label="总内存">
                  {{ server.mem?.total }}
                </ElDescriptionsItem>
                <ElDescriptionsItem label="已用内存">
                  {{ server.mem?.used }}
                </ElDescriptionsItem>
                <ElDescriptionsItem label="空闲内存">
                  {{ server.mem?.free }}
                </ElDescriptionsItem>
                <ElDescriptionsItem label="Python内存">
                  {{ server.py?.memory_usage ? server.py.memory_usage.toFixed(1) + "%" : "-" }}
                </ElDescriptionsItem>
              </FaDescriptions>
            </div>
          </div>
        </ElCard>
      </ElCol>
    </ElRow>

    <ElRow :gutter="16" class="server-row">
      <!-- 服务器基本信息 -->
      <ElCol :span="12" class="server-col">
        <ElCard :loading="loading" shadow="hover" class="server-card">
          <template #header>
            <div class="flex items-center gap-2">
              <FaSvgIcon icon="ri:server-line" class="text-lg" />
              <span class="font-medium">服务器基本信息</span>
            </div>
          </template>
          <FaDescriptions :column="2" size="small" :scrollbar="false">
            <ElDescriptionsItem label="服务器名称">
              {{ server.sys?.computer_name || "-" }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="操作系统">
              {{ server.sys?.os_name || "-" }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="服务器IP">
              {{ server.sys?.computer_ip || "-" }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="系统架构">
              {{ server.sys?.os_arch || "-" }}
            </ElDescriptionsItem>
          </FaDescriptions>
        </ElCard>
      </ElCol>

      <!-- Python运行环境 -->
      <ElCol :span="12" class="server-col">
        <ElCard :loading="loading" shadow="hover" class="server-card">
          <template #header>
            <div class="flex items-center gap-2">
              <FaSvgIcon icon="ri:code-s-slash-line" class="text-lg" />
              <span class="font-medium">Python运行环境</span>
            </div>
          </template>
          <FaDescriptions :column="2" size="small" :scrollbar="false">
            <ElDescriptionsItem label="Python名称">
              {{ server.py?.name || "-" }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="Python版本">
              {{ server.py?.version || "-" }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="启动时间">
              {{ server.py?.start_time || "-" }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="运行时长">
              {{ server.py?.run_time || "-" }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="安装路径" :span="2">
              {{ server.py?.home || "-" }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="项目路径" :span="2">
              {{ server.sys?.user_dir || "-" }}
            </ElDescriptionsItem>
          </FaDescriptions>
        </ElCard>
      </ElCol>
    </ElRow>

    <!-- 磁盘使用情况 -->
    <ElRow :gutter="16" class="server-row">
      <ElCol :span="24" class="server-col">
        <ElCard :loading="loading" shadow="hover" class="server-card">
          <template #header>
            <div class="flex items-center gap-2">
              <FaSvgIcon icon="ri:hard-drive-2-line" class="text-lg" />
              <span class="font-medium">磁盘使用情况</span>
            </div>
          </template>
          <ElTable :data="server.disks" stripe>
            <template #empty>
              <ElEmpty :image-size="80" description="暂无数据" />
            </template>
            <ElTableColumn label="盘符路径" prop="dir_name" show-overflow-tooltip />
            <ElTableColumn label="文件系统" prop="sys_type_name" align="center" width="100" />
            <ElTableColumn label="盘符名称" prop="type_name" show-overflow-tooltip />
            <ElTableColumn label="使用率" align="center" width="200">
              <template #default="{ row }">
                <ElProgress
                  :percentage="Number(row.usage)"
                  :status="row.usage > 80 ? 'exception' : row.usage > 60 ? 'warning' : 'success'"
                  :stroke-width="16"
                  text-inside
                />
              </template>
            </ElTableColumn>
            <ElTableColumn label="总大小" prop="total" align="center" width="100" />
            <ElTableColumn label="已用" prop="used" align="center" width="100" />
            <ElTableColumn label="可用" prop="free" align="center" width="100" />
          </ElTable>
        </ElCard>
      </ElCol>
    </ElRow>
  </div>
</template>

<script lang="ts" setup>
import FaDescriptions from "@/components/others/fa-descriptions/index.vue";
import ServerAPI, { type ServerInfo } from "@/api/module_monitor/server";

defineOptions({ name: "ServerMonitor" });

const loading = ref(false);
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

async function getList() {
  loading.value = true;
  try {
    const response = await ServerAPI.getServer();
    server.value = response.data.data;
  } catch (error) {
    console.error("获取服务器信息失败:", error);
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  getList();
});
</script>

<style scoped lang="scss">
// 与 dashboard 首页一致：自定义圆角 + 边框色
:deep(.el-card) {
  --el-card-border-radius: calc(var(--custom-radius) + 2px);

  border: 1px solid var(--fa-card-border);
}

.server-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.server-row {
  .server-col {
    display: flex;
    flex-direction: column;
    min-height: 0;

    .server-card {
      display: flex;
      flex: 1;
      flex-direction: column;

      :deep(.el-card__body) {
        flex: 1;
      }
    }
  }
}
</style>
