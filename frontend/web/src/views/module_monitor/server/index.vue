<template>
  <div class="app-container">
    <ElRow :gutter="16">
      <ElCol :span="12" class="mb-4">
        <ElCard :loading="loading" shadow="hover">
          <template #header>
            <div class="flex items-center gap-2">
              <ElIcon><Cpu /></ElIcon>
              <span class="flex items-center gap-2">CPU使用情况</span>
              <ElTooltip content="展示CPU核心数及使用率">
                <ElIcon><QuestionFilled /></ElIcon>
              </ElTooltip>
            </div>
          </template>
          <ElRow :gutter="16">
            <!-- CPU核心数卡片 -->
            <ElCol :span="12">
              <ElCard shadow="hover">
                <span>核心数</span>
                <ElTooltip :content="(server.cpu?.cpu_num || 0).toFixed(1)">
                  <div class="text-center mb-4">
                    <ElProgress
                      type="circle"
                      :percentage="100"
                      :format="() => `${server.cpu?.cpu_num || 0}`"
                    />
                  </div>
                </ElTooltip>
                <ElDescriptions :column="1" border>
                  <ElDescriptionsItem label="总核心数">
                    {{ server.cpu?.cpu_num || 0 }}
                  </ElDescriptionsItem>
                  <ElDescriptionsItem label="已用核心">
                    {{ Math.floor(((server.cpu?.used || 0) * server.cpu?.cpu_num) / 100) }}
                  </ElDescriptionsItem>
                  <ElDescriptionsItem label="空闲核心">
                    {{ Math.floor(((server.cpu?.free || 0) * server.cpu?.cpu_num) / 100) }}
                  </ElDescriptionsItem>
                </ElDescriptions>
              </ElCard>
            </ElCol>
            <!-- CPU使用率卡片 -->
            <ElCol :span="12">
              <ElCard shadow="hover" class="h-full">
                <span>使用率</span>
                <ElTooltip :content="(server.cpu?.used || 0).toFixed(1) + '%'">
                  <div class="text-center mb-4">
                    <ElProgress
                      type="circle"
                      :percentage="server.cpu?.used || 0"
                      :status="
                        server.cpu?.used > 80
                          ? 'exception'
                          : server.cpu?.used > 60
                            ? 'warning'
                            : 'success'
                      "
                    />
                  </div>
                </ElTooltip>
                <ElDescriptions :column="1" border>
                  <ElDescriptionsItem label="用户使用率">
                    {{ (server.cpu?.used || 0).toFixed(1) + "%" }}
                  </ElDescriptionsItem>
                  <ElDescriptionsItem label="系统使用率">
                    {{ (server.cpu?.sys || 0).toFixed(1) + "%" }}
                  </ElDescriptionsItem>
                  <ElDescriptionsItem label="当前空闲率">
                    {{ (server.cpu?.free || 0).toFixed(1) + "%" }}
                  </ElDescriptionsItem>
                </ElDescriptions>
              </ElCard>
            </ElCol>
          </ElRow>
        </ElCard>
      </ElCol>

      <ElCol :span="12" class="mb-4">
        <ElCard :loading="loading" shadow="hover">
          <template #header>
            <div class="flex items-center gap-2">
              <ElIcon><Memo /></ElIcon>
              <span>内存使用情况</span>
              <ElTooltip content="展示系统内存和Python程序内存使用情况">
                <ElIcon><QuestionFilled /></ElIcon>
              </ElTooltip>
            </div>
          </template>
          <ElRow :gutter="16">
            <!-- 系统内存卡片 -->
            <ElCol :span="12">
              <ElCard shadow="hover" class="h-full">
                <span>系统内存</span>
                <ElTooltip :content="(server.mem?.usage || 0).toFixed(1) + '%'">
                  <div class="text-center mb-4">
                    <ElProgress
                      type="circle"
                      :percentage="server.mem?.usage || 0"
                      :status="
                        server.mem?.usage > 80
                          ? 'exception'
                          : server.mem?.usage > 60
                            ? 'warning'
                            : 'success'
                      "
                    />
                  </div>
                </ElTooltip>
                <ElDescriptions :column="1" border>
                  <ElDescriptionsItem label="总内存">
                    {{ server.mem?.total }}
                  </ElDescriptionsItem>
                  <ElDescriptionsItem label="已用内存">
                    {{ server.mem?.used }}
                  </ElDescriptionsItem>
                  <ElDescriptionsItem label="空闲内存">
                    {{ server.mem?.free }}
                  </ElDescriptionsItem>
                </ElDescriptions>
              </ElCard>
            </ElCol>
            <!-- Python内存卡片 -->
            <ElCol :span="12">
              <ElCard shadow="hover" class="h-full">
                <span>Python内存</span>
                <ElTooltip :content="(server.py?.memory_usage || 0).toFixed(1) + '%'">
                  <div class="text-center mb-4">
                    <ElProgress
                      type="circle"
                      :percentage="server.py?.memory_usage || 0"
                      :status="
                        server.py?.memory_usage > 80
                          ? 'exception'
                          : server.py?.memory_usage > 60
                            ? 'warning'
                            : 'success'
                      "
                    />
                  </div>
                </ElTooltip>
                <ElDescriptions :column="1" border>
                  <ElDescriptionsItem label="总内存">
                    {{ server.py?.memory_total }}
                  </ElDescriptionsItem>
                  <ElDescriptionsItem label="已用内存">
                    {{ server.py?.memory_used }}
                  </ElDescriptionsItem>
                  <ElDescriptionsItem label="空闲内存">
                    {{ server.py?.memory_free }}
                  </ElDescriptionsItem>
                </ElDescriptions>
              </ElCard>
            </ElCol>
          </ElRow>
        </ElCard>
      </ElCol>

      <ElCol :span="24" class="mb-4">
        <ElCard :loading="loading">
          <template #header>
            <div class="flex items-center gap-2">
              <ElIcon><Monitor /></ElIcon>
              <span class="font-medium">服务器基本信息</span>
              <ElTooltip content="展示服务器基本配置信息">
                <ElIcon><QuestionFilled /></ElIcon>
              </ElTooltip>
            </div>
          </template>
          <ElDescriptions :column="2" border>
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
          </ElDescriptions>
        </ElCard>
      </ElCol>

      <ElCol :span="24" class="mb-4">
        <ElCard :loading="loading" class="shadow-sm">
          <template #header>
            <div class="flex items-center gap-2">
              <ElIcon><Dish /></ElIcon>
              <span class="font-medium">Python运行环境</span>
              <ElTooltip content="展示Python环境配置及运行状态">
                <ElIcon><QuestionFilled /></ElIcon>
              </ElTooltip>
            </div>
          </template>
          <ElDescriptions :column="3" border>
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
            <ElDescriptionsItem label="安装路径">
              {{ server.py?.home || "-" }}
            </ElDescriptionsItem>
            <ElDescriptionsItem label="项目路径">
              {{ server.sys?.user_dir || "-" }}
            </ElDescriptionsItem>
          </ElDescriptions>
        </ElCard>
      </ElCol>

      <ElCol :span="24">
        <ElCard :loading="loading">
          <template #header>
            <div class="flex items-center gap-2">
              <ElIcon>
                <Files />
              </ElIcon>
              <span class="font-medium">磁盘使用情况</span>
              <ElTooltip content="展示磁盘空间使用详情">
                <ElIcon><QuestionFilled /></ElIcon>
              </ElTooltip>
            </div>
          </template>
          <ElTable :data="server.disks">
            <template #empty>
              <ElEmpty :image-size="80" description="暂无数据" />
            </template>
            <ElTableColumn label="盘符路径" prop="dir_name" :show-overflow-tooltip="true" />
            <ElTableColumn label="文件系统" prop="sys_type_name" align="center" width="100" />
            <ElTableColumn label="盘符名称" prop="type_name" />
            <ElTableColumn prop="usage" label="使用率" align="center">
              <template #default="{ row }">
                <!-- 使用 element-plus 的 Progress 组件 -->
                <div>
                  <ElProgress
                    :percentage="Number(row.usage)"
                    :status="row.usage > 80 ? 'exception' : row.usage > 60 ? 'warning' : 'success'"
                    :text-inside="true"
                    :stroke-width="16"
                  />
                </div>
              </template>
            </ElTableColumn>
            <ElTableColumn label="总大小" prop="total" align="center" width="100" />
            <ElTableColumn label="可用大小" prop="free" align="center" width="100" />
            <ElTableColumn label="已用大小" prop="used" align="center" width="100" />
          </ElTable>
        </ElCard>
      </ElCol>
    </ElRow>
  </div>
</template>

<script lang="ts" setup>
import ServerAPI, { type ServerInfo } from "@/api/module_monitor/server";

const loading = ref(false);
const server = ref<ServerInfo>({
  cpu: {
    cpu_num: 0,
    used: 0,
    sys: 0,
    free: 0,
  },
  mem: {
    total: "",
    used: "",
    free: "",
    usage: 0,
  },
  sys: {
    computer_name: "",
    os_name: "",
    computer_ip: "",
    os_arch: "",
    user_dir: "",
  },
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

<style lang="scss" scoped></style>
