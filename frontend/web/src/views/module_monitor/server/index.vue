<template>
  <div class="app-container">
    <el-row :gutter="16">
      <el-col :span="12" class="mb-4">
        <el-card :loading="loading" shadow="hover">
          <template #header>
            <div class="flex items-center gap-2">
              <el-icon><Cpu /></el-icon>
              <span class="flex items-center gap-2">CPU使用情况</span>
              <el-tooltip content="展示CPU核心数及使用率">
                <el-icon><QuestionFilled /></el-icon>
              </el-tooltip>
            </div>
          </template>
          <el-row :gutter="16">
            <!-- CPU核心数卡片 -->
            <el-col :span="12">
              <el-card shadow="hover">
                <span>核心数</span>
                <el-tooltip :content="(server.cpu?.cpu_num || 0).toFixed(1)">
                  <div class="text-center mb-4">
                    <el-progress
                      type="circle"
                      :percentage="100"
                      :format="() => `${server.cpu?.cpu_num || 0}`"
                    />
                  </div>
                </el-tooltip>
                <el-descriptions :column="1" border>
                  <el-descriptions-item label="总核心数">
                    {{ server.cpu?.cpu_num || 0 }}
                  </el-descriptions-item>
                  <el-descriptions-item label="已用核心">
                    {{ Math.floor(((server.cpu?.used || 0) * server.cpu?.cpu_num) / 100) }}
                  </el-descriptions-item>
                  <el-descriptions-item label="空闲核心">
                    {{ Math.floor(((server.cpu?.free || 0) * server.cpu?.cpu_num) / 100) }}
                  </el-descriptions-item>
                </el-descriptions>
              </el-card>
            </el-col>
            <!-- CPU使用率卡片 -->
            <el-col :span="12">
              <el-card shadow="hover" class="h-full">
                <span>使用率</span>
                <el-tooltip :content="(server.cpu?.used || 0).toFixed(1) + '%'">
                  <div class="text-center mb-4">
                    <el-progress
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
                </el-tooltip>
                <el-descriptions :column="1" border>
                  <el-descriptions-item label="用户使用率">
                    {{ (server.cpu?.used || 0).toFixed(1) + '%' }}
                  </el-descriptions-item>
                  <el-descriptions-item label="系统使用率">
                    {{ (server.cpu?.sys || 0).toFixed(1) + '%' }}
                  </el-descriptions-item>
                  <el-descriptions-item label="当前空闲率">
                    {{ (server.cpu?.free || 0).toFixed(1) + '%' }}
                  </el-descriptions-item>
                </el-descriptions>
              </el-card>
            </el-col>
          </el-row>
        </el-card>
      </el-col>

      <el-col :span="12" class="mb-4">
        <el-card :loading="loading" shadow="hover">
          <template #header>
            <div class="flex items-center gap-2">
              <el-icon><Memo /></el-icon>
              <span>内存使用情况</span>
              <el-tooltip content="展示系统内存和Python程序内存使用情况">
                <el-icon><QuestionFilled /></el-icon>
              </el-tooltip>
            </div>
          </template>
          <el-row :gutter="16">
            <!-- 系统内存卡片 -->
            <el-col :span="12">
              <el-card shadow="hover" class="h-full">
                <span>系统内存</span>
                <el-tooltip :content="(server.mem?.usage || 0).toFixed(1) + '%'">
                  <div class="text-center mb-4">
                    <el-progress
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
                </el-tooltip>
                <el-descriptions :column="1" border>
                  <el-descriptions-item label="总内存">
                    {{ server.mem?.total }}
                  </el-descriptions-item>
                  <el-descriptions-item label="已用内存">
                    {{ server.mem?.used }}
                  </el-descriptions-item>
                  <el-descriptions-item label="空闲内存">
                    {{ server.mem?.free }}
                  </el-descriptions-item>
                </el-descriptions>
              </el-card>
            </el-col>
            <!-- Python内存卡片 -->
            <el-col :span="12">
              <el-card shadow="hover" class="h-full">
                <span>Python内存</span>
                <el-tooltip :content="(server.py?.memory_usage || 0).toFixed(1) + '%'">
                  <div class="text-center mb-4">
                    <el-progress
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
                </el-tooltip>
                <el-descriptions :column="1" border>
                  <el-descriptions-item label="总内存">
                    {{ server.py?.memory_total }}
                  </el-descriptions-item>
                  <el-descriptions-item label="已用内存">
                    {{ server.py?.memory_used }}
                  </el-descriptions-item>
                  <el-descriptions-item label="空闲内存">
                    {{ server.py?.memory_free }}
                  </el-descriptions-item>
                </el-descriptions>
              </el-card>
            </el-col>
          </el-row>
        </el-card>
      </el-col>

      <el-col :span="24" class="mb-4">
        <el-card :loading="loading">
          <template #header>
            <div class="flex items-center gap-2">
              <el-icon><Monitor /></el-icon>
              <span class="font-medium">服务器基本信息</span>
              <el-tooltip content="展示服务器基本配置信息">
                <el-icon><QuestionFilled /></el-icon>
              </el-tooltip>
            </div>
          </template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="服务器名称">
              {{ server.sys?.computer_name || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="操作系统">
              {{ server.sys?.os_name || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="服务器IP">
              {{ server.sys?.computer_ip || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="系统架构">
              {{ server.sys?.os_arch || '-' }}
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>

      <el-col :span="24" class="mb-4">
        <el-card :loading="loading" class="shadow-sm">
          <template #header>
            <div class="flex items-center gap-2">
              <el-icon><Dish /></el-icon>
              <span class="font-medium">Python运行环境</span>
              <el-tooltip content="展示Python环境配置及运行状态">
                <el-icon><QuestionFilled /></el-icon>
              </el-tooltip>
            </div>
          </template>
          <el-descriptions :column="3" border>
            <el-descriptions-item label="Python名称">
              {{ server.py?.name || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="Python版本">
              {{ server.py?.version || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="启动时间">
              {{ server.py?.start_time || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="运行时长">
              {{ server.py?.run_time || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="安装路径">
              {{ server.py?.home || '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="项目路径">
              {{ server.sys?.user_dir || '-' }}
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>

      <el-col :span="24">
        <el-card :loading="loading">
          <template #header>
            <div class="flex items-center gap-2">
              <el-icon>
                <Files />
              </el-icon>
              <span class="font-medium">磁盘使用情况</span>
              <el-tooltip content="展示磁盘空间使用详情">
                <el-icon><QuestionFilled /></el-icon>
              </el-tooltip>
            </div>
          </template>
          <el-table :data="server.disks" border stripe>
            <template #empty>
              <el-empty :image-size="80" description="暂无数据" />
            </template>
            <el-table-column label="盘符路径" prop="dir_name" :show-overflow-tooltip="true" />
            <el-table-column label="文件系统" prop="sys_type_name" align="center" width="100" />
            <el-table-column label="盘符名称" prop="type_name" />
            <el-table-column prop="usage" label="使用率" align="center">
              <template #default="{ row }">
                <!-- 使用 element-plus 的 Progress 组件 -->
                <div>
                  <el-progress
                    :percentage="Number(row.usage)"
                    :status="row.usage > 80 ? 'exception' : row.usage > 60 ? 'warning' : 'success'"
                    :text-inside="true"
                    :stroke-width="16"
                  />
                </div>
              </template>
            </el-table-column>
            <el-table-column label="总大小" prop="total" align="center" width="100" />
            <el-table-column label="可用大小" prop="free" align="center" width="100" />
            <el-table-column label="已用大小" prop="used" align="center" width="100" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts" setup>
  import ServerAPI, { type ServerInfo } from '@/api/module_monitor/server';

  const loading = ref(false);
  const server = ref<ServerInfo>({
    cpu: {
      cpu_num: 0,
      used: 0,
      sys: 0,
      free: 0,
    },
    mem: {
      total: '',
      used: '',
      free: '',
      usage: 0,
    },
    sys: {
      computer_name: '',
      os_name: '',
      computer_ip: '',
      os_arch: '',
      user_dir: '',
    },
    py: {
      name: '',
      version: '',
      start_time: '',
      run_time: '',
      home: '',
      memory_total: '',
      memory_used: '',
      memory_free: '',
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
      console.error('获取服务器信息失败:', error);
    } finally {
      loading.value = false;
    }
  }

  onMounted(() => {
    getList();
  });
</script>

<style lang="scss" scoped></style>
