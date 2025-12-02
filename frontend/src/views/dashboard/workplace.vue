<template>
  <div class="app-container">
    <div>
      <ElCard shadow="hover">
        <div class="flex flex-wrap justify-between items-center">
          <div class="flex items-center md:mb-0">
            <ElAvatar size="large" :src="currentUser.avatar" class="mr-20px" />
            <div>
              <div class="text-20px font-bold">
                {{ timefix }}{{ currentUser.name }}，{{ welcome }}
              </div>
              <el-text>
                {{ currentUser.username }} | {{ currentUser.dept_name }} |
                {{ currentUser.description }}
              </el-text>
            </div>
          </div>
          <!-- 最近登录时间 -->
          <div class="statItem text-14px text-gray-600 text-right">
            <el-text>最近登录时间</el-text>
            <div class="mt-5px text-20px">{{ currentUser.last_login }}</div>
          </div>
        </div>
      </ElCard>
    </div>

    <div class="mt-4">
      <ElRow :gutter="16" justify="space-between">
        <!-- 左侧：进行中的项目 + 动态 -->
        <ElCol :xl="16" :lg="16" :md="24" :sm="24" :xs="24">
          <!-- 进行中的项目 -->
          <ElCard shadow="hover" title="进行中的项目">
            <template #header>
              <span class="font-bold">进行中的项目</span>
              <ElLink href="" type="primary" underline="never" style="float: right">
                全部项目
              </ElLink>
            </template>
            <el-empty v-if="projectNotice.length === 0" :image-size="80" description="暂无数据" />
            <ElRow v-else>
              <ElCol
                v-for="item in projectNotice"
                :key="`card-${item.id}`"
                :xl="8"
                :lg="8"
                :md="12"
                :sm="24"
                :xs="24"
              >
                <ElCard :key="item.id" shadow="hover">
                  <ElDescriptions :column="1">
                    <ElDescriptionsItem>
                      <div class="flex items-center">
                        <ElAvatar :src="item.avatar" size="small" class="mr-20px" />
                        <ElLink :href="item.href" underline="never">{{ item.title }}</ElLink>
                      </div>
                    </ElDescriptionsItem>

                    <ElDescriptionsItem>
                      <el-tooltip placement="top" :content="item.description">
                        <el-text line-clamp="1" class="truncate-text">
                          {{ item.description }}
                        </el-text>
                      </el-tooltip>
                    </ElDescriptionsItem>

                    <ElDescriptionsItem>
                      <div class="flex justify-between items-center">
                        <ElLink :href="item.memberLink" underline="never">
                          {{ item.member || "" }}
                        </ElLink>
                        <span>{{ item.updatedAt }}</span>
                      </div>
                    </ElDescriptionsItem>
                  </ElDescriptions>
                </ElCard>
              </ElCol>
            </ElRow>
          </ElCard>
          <!-- 通知公告 -->
          <ElCard shadow="hover" class="mt-4">
            <template #header>
              <div class="flex justify-between items-center">
                <span class="font-bold">通知公告</span>
                <ElButton type="primary" link @click="goToNotice()">更多</ElButton>
              </div>
            </template>
            <el-empty v-if="noticeList.length === 0" :image-size="80" description="暂无数据" />
            <ElTimeline>
              <ElTimelineItem
                v-for="(item, index) in noticeList"
                :key="item.id"
                :type="index === 0 ? 'primary' : 'info'"
              >
                <div
                  class="bg-[var(--el-fill-color-light)] rounded-lg p-4 border border-[var(--el-border-color)] hover:shadow-md transition-shadow"
                >
                  <div class="flex justify-between items-start mb-2">
                    <div class="flex items-center gap-2">
                      <span class="font-medium text-[var(--el-text-color-primary)]">
                        {{ item.notice_title }}
                      </span>
                      <el-tag size="small" :type="getNoticeTypeColor(item.notice_type)">
                        {{ getNoticeTypeText(item.notice_type) }}
                      </el-tag>
                    </div>
                    <span class="text-xs text-[var(--el-text-color-regular)]">
                      {{ formatTime(item.created_time) }}
                    </span>
                  </div>
                  <div class="text-sm text-[var(--el-text-color-regular)] mb-3 line-clamp-2">
                    {{ item.notice_content }}
                  </div>
                  <div class="flex justify-between items-center text-xs">
                    <span class="text-[var(--el-text-color-regular)]">
                      {{ item.created_by?.name }} 发布
                    </span>
                    <el-tooltip placement="top" :content="item.description || item.notice_content">
                      <ElButton target="_blank" type="primary" link @click="goToNotice()">
                        详情↗
                      </ElButton>
                    </el-tooltip>
                  </div>
                </div>
              </ElTimelineItem>
            </ElTimeline>
          </ElCard>

          <!-- 团队 -->
          <ElCard shadow="hover" class="mt-4">
            <template #header>
              <span class="font-bold">团队</span>
            </template>
            <el-empty v-if="projectNotice.length === 0" :image-size="80" description="暂无数据" />
            <ElRow v-else :gutter="16">
              <ElCol
                v-for="item in projectNotice"
                :key="`members-item-${item.id}`"
                :span="8"
                class="mb-3"
              >
                <ElLink
                  underline="never"
                  :href="item.href"
                  class="flex items-center hover:bg-[var(--el-fill-color-light)] p-2 rounded transition-colors"
                >
                  <ElAvatar :src="item.avatar" size="small" class="mr-2" />
                  <span class="text-sm truncate text-[var(--el-text-color-regular)]">
                    {{ item.member }}
                  </span>
                </ElLink>
              </ElCol>
            </ElRow>
          </ElCard>
        </ElCol>

        <!-- 右侧：快速开始 / 便捷导航 + XX 指数 -->
        <ElCol :xl="8" :lg="8" :md="12" :sm="12" :xs="24">
          <!-- 快速开始 / 便捷导航 -->
          <ElCard shadow="hover" class="mb-4">
            <template #header>
              <div class="flex justify-between items-center">
                <div class="flex items-center gap-2">
                  <el-tooltip
                    content="快速访问常用功能，标签右键收藏可添加快捷栏菜单。"
                    placement="top"
                  >
                    <el-icon class="cursor-help" size="16">
                      <QuestionFilled />
                    </el-icon>
                  </el-tooltip>
                  <span class="font-bold">快速开始 / 便捷导航</span>
                </div>
                <ElButton size="small" type="danger" plain @click="clearBookmarks()">
                  <el-icon>
                    <Delete />
                  </el-icon>
                  {{ t("common.clear") }}
                </ElButton>
              </div>
            </template>
            <ElRow v-if="quickLinks.length > 0" :gutter="8">
              <ElCol v-for="(item, index) in quickLinks" :key="index" :span="6" class="group mb-4">
                <ElButton
                  plain
                  type="default"
                  class="w-full relative"
                  @click="handleQuickLinkClick(item)"
                >
                  <el-icon
                    v-if="item.icon && item.icon.startsWith('el-icon')"
                    :color="getRandomColor()"
                  >
                    <component :is="item.icon.replace('el-icon-', '')" />
                  </el-icon>
                  <div
                    v-else-if="item.icon"
                    :class="`i-svg:${item.icon} mr-2`"
                    :style="{ color: getRandomColor() }"
                  />
                  <div v-else :class="`i-svg:menu mr-2`" :style="{ color: getRandomColor() }" />

                  <span>{{ item.title }}</span>
                  <el-icon
                    color="var(--el-color-danger)"
                    class="absolute top-0 right-0 opacity-0 group-hover:opacity-100"
                    @click.stop="handleDeleteLink(item)"
                  >
                    <CircleClose />
                  </el-icon>
                </ElButton>
              </ElCol>
            </ElRow>
            <el-empty v-else :image-size="80" description="暂无数据" />
          </ElCard>

          <!-- XX 指数 -->
          <ElCard class="mb-4 font-bold" header="XX 指数">
            <ECharts
              class="chart"
              :options="chartOptions"
              height="450px"
              autoresize
              :init-options="{ renderer: 'canvas' }"
            />
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

import { EChartsOption } from "echarts";
import { useUserStore } from "@/store/index";
import { greetings } from "@/utils/common";
import NoticeAPI, { NoticeTable } from "@/api/module_system/notice";
import { ref, onMounted, reactive } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { QuestionFilled, Delete, CircleClose } from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { quickStartManager, type QuickLink } from "@/utils/quickStartManager";

const userStore = useUserStore();
const timefix = greetings();
const { t } = useI18n();
const router = useRouter();

// 通知公告数据
const noticeList = ref<NoticeTable[]>([]);

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
      page_size: 10,
      status: '0', // 只获取启用的公告
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
    // 内部路由跳转
    router.push(item.href).catch(() => {
      ElMessage.warning(`路由 ${item.href} 不存在，请检查配置`);
    });
    ElMessage.success(`进入：${item.title}`);
  } else {
    ElMessage.info(`${item.title} 功能待开发`);
  }
};

const getRandomColor = () => {
  // 预定义几个亮且鲜艳的颜色
  const colors = [
    "#FF5733",
    "#33FF57",
    "#3357FF",
    "#FF33E6",
    "#FFFF33",
    "#33FFFF",
    "#FF3333",
    "#5733FF",
    "#33FFE6",
    "#E633FF",
  ];
  // 随机选择一个颜色返回
  const randomIndex = Math.floor(Math.random() * colors.length);
  return colors[randomIndex];
};
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
        ElMessage.success(`已取消收藏：${item.title}`);
      }
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

const projectNotice = [
  {
    id: "xxx1",
    title: "Mysql",
    avatar: "https://labs.mysql.com/common/themes/sakila/favicon.ico",
    description: "最流行的关系型数据库",
    updatedAt: "几秒前",
    member: "科学搬砖组",
    href: "https://www.mysql.com/",
    memberLink: "",
  },
  {
    id: "xxx2",
    title: "Fastapi",
    avatar: "https://fastapi.tiangolo.com/img/favicon.png",
    description: "一个现代、快速(高性能)的 web 框架",
    updatedAt: "6 年前",
    member: "全组都是吴彦祖",
    href: "https://fastapi.tiangolo.com/zh/",
    memberLink: "",
  },
  {
    id: "xxx3",
    title: "Element-plus",
    avatar: "https://element-plus.org/images/element-plus-logo-small.svg",
    description: "面向设计师和开发者的组件库",
    updatedAt: "几秒前",
    member: "中二少女团",
    href: "https://element-plus.org/zh-CN/",
    memberLink: "",
  },
  {
    id: "xxx4",
    title: "Vue",
    avatar: "https://cn.vuejs.org/logo.svg",
    description: "渐进式 JavaScript 框架",
    updatedAt: "6 年前",
    member: "程序员日常",
    href: "https://cn.vuejs.org/",
    memberLink: "",
  },
  {
    id: "xxx5",
    title: "Vite",
    avatar: "https://vitejs.cn/vite3-cn/logo.svg",
    description: "Vite 下一代的前端工具链",
    updatedAt: "6 年前",
    member: "高逼格设计天团",
    href: "https://cn.vitejs.dev/",
    memberLink: "",
  },
  {
    id: "xxx6",
    title: "Python",
    avatar: "https://python.p2hp.com/static/favicon.ico",
    description: "一种解释型、面向对象类型编程语言",
    updatedAt: "6 年前",
    member: "骗你来学计算机",
    href: "",
    memberLink: "",
  },
];

const chartOptions = reactive<EChartsOption>({
  tooltip: { trigger: "item" },
  legend: { data: ["个人", "团队", "部门"] },
  radar: {
    shape: "circle",
    indicator: [
      { name: "引用", max: 10 },
      { name: "热度", max: 10 },
      { name: "贡献", max: 10 },
      { name: "产量", max: 10 },
      { name: "口碑", max: 10 },
    ],
  },
  series: [
    {
      name: "Budget vs spending",
      type: "radar",
      areaStyle: {},
      symbol: "none",
      emphasis: { focus: "self" },
      data: [
        { value: [10, 7, 5, 4, 8], name: "个人" },
        { value: [3, 1, 3, 6, 9], name: "团队" },
        { value: [4, 7, 5, 6, 1], name: "部门" },
      ],
    },
  ],
});
</script>

<style scoped>
/* 最小化自定义样式，主要使用UnoCSS和Element Plus内置样式 */
</style>
