<template>
  <div class="dashboard-container">
    <FaGithubCorner class="github-corner" />

    <!-- 问候 + 外链 -->
    <ElCard shadow="hover">
      <div class="flex flex-wrap items-center gap-y-3">
        <div class="flex min-w-0 flex-1 items-center">
          <div class="size-20 shrink-0 rounded-full bg-g-100 flex items-center justify-center">
            <ElAvatar
              v-if="userStore.basicInfo.avatar"
              size="large"
              :src="userStore.basicInfo.avatar"
              class="workplace-hero__avatar"
            />
            <ElIcon v-else :size="40" class="text-g-600"><UserFilled /></ElIcon>
          </div>
          <div>
            <div class="workplace-hero__greeting">
              {{ timefix }}{{ currentUser.name }}，{{ welcome }}
            </div>
            <ElText class="workplace-hero__meta">
              <p class="text-sm text-g-600">
                {{ currentUser.username }} · {{ currentUser.dept_name }} ·
                {{ currentUser.description }}
              </p>
            </ElText>
          </div>
        </div>
        <div class="hidden shrink-0 sm:block">
          <div class="flex items-center space-x-6">
            <div class="flex flex-col items-center">
              <div class="flex items-center text-sm font-bold text-[#4080ff]">
                <ElIcon class="mr-0.5"><Document /></ElIcon>
                文档
              </div>
              <div class="mt-3 whitespace-nowrap">
                <ElLink
                  href="https://blog.csdn.net/weixin_46768253/article/details/149569141"
                  target="_blank"
                >
                  <FaSvgIcon :icon="resolveIconForFaSvgIcon('csdn')" class="text-lg" />
                </ElLink>
              </div>
            </div>
            <div class="flex flex-col items-center">
              <div class="flex items-center text-sm font-bold text-[#ff9a2e]">
                <ElIcon class="mr-0.5"><Folder /></ElIcon>
                仓库
              </div>
              <div class="mt-3 whitespace-nowrap">
                <ElLink href="https://gitee.com/fastapiadmin/FastapiAdmin" target="_blank">
                  <FaSvgIcon
                    :icon="resolveIconForFaSvgIcon('gitee')"
                    class="text-lg text-[#F76560]"
                  />
                </ElLink>
                <ElDivider direction="vertical" />
                <ElLink href="https://github.com/fastapiadmin/FastapiAdmin" target="_blank">
                  <FaSvgIcon
                    :icon="resolveIconForFaSvgIcon('github')"
                    class="text-lg text-[#4080FF]"
                  />
                </ElLink>
                <ElDivider direction="vertical" />
                <ElLink href="https://gitcode.com/qq_36002987/FastapiAdmin" target="_blank">
                  <FaSvgIcon
                    :icon="resolveIconForFaSvgIcon('gitcode')"
                    class="text-lg text-[#FF9A2E]"
                  />
                </ElLink>
              </div>
            </div>
          </div>
        </div>
        <div class="w-full sm:hidden">
          <div class="flex justify-end space-x-4 overflow-x-auto">
            <ElLink href="https://gitee.com/fastapiadmin/FastapiAdmin" target="_blank">
              <FaSvgIcon :icon="resolveIconForFaSvgIcon('gitee')" class="text-lg text-[#F76560]" />
            </ElLink>
            <ElDivider direction="vertical" />
            <ElLink href="https://github.com/fastapiadmin/FastapiAdmin" target="_blank">
              <FaSvgIcon :icon="resolveIconForFaSvgIcon('github')" class="text-lg text-[#4080FF]" />
            </ElLink>
            <ElDivider direction="vertical" />
            <ElLink href="https://gitcode.com/qq_36002987/FastapiAdmin" target="_blank">
              <FaSvgIcon
                :icon="resolveIconForFaSvgIcon('gitcode')"
                class="text-lg text-[#FF9A2E]"
              />
            </ElLink>
          </div>
        </div>
      </div>
    </ElCard>

    <!-- CardList 概览统计（含在线用户/UV/PV/访问量等） -->
    <CardList />

    <!-- 日程日历 + 我的收藏 -->
    <ElRow :gutter="16">
      <ElCol :xs="24" :span="12" class="flex flex-col">
        <ElCard shadow="hover" class="workplace-surface workplace-ops-card flex flex-col h-full">
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
          <div class="workplace-ops-card__body">
            <Calendar />
          </div>
        </ElCard>
      </ElCol>
      <ElCol :xs="24" :span="12" class="flex flex-col">
        <ElCard shadow="hover" class="flex flex-col h-full">
          <template #header>
            <div class="workplace-bookmarks-card__header">
              <div>
                <span class="workplace-panel-title workplace-bookmarks-card__title-line">
                  <ElIcon class="workplace-bookmarks-card__star" :size="18"><Star /></ElIcon>
                  我的收藏
                  <p class="workplace-section-sub workplace-section-sub--inline">
                    最多 {{ QUICK_LINK_MAX }} 个 · 标签栏星标添加 · 仅本机
                  </p>
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
          <div v-if="quickLinks.length > 0">
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
                  :style="{ backgroundColor: getQuickLinkColor(getQuickLinkStableIndex(item)) }"
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
          <ElEmpty v-else :image-size="48">
            <template #description>
              <p class="workplace-quick-empty__title">暂无收藏</p>
              <p class="workplace-quick-empty__hint">
                在顶部
                <strong>标签栏</strong>
                左侧星标点击添加
              </p>
            </template>
          </ElEmpty>
        </ElCard>
      </ElCol>
    </ElRow>

    <!-- 最新动态 + 关于项目 -->
    <ElRow :gutter="16">
      <ElCol :span="12" class="flex flex-col">
        <ElCard shadow="hover" class="h-full flex flex-col">
          <template #header>
            <div class="flex items-center justify-between">
              <span class="font-medium">最新动态</span>
              <ElLink
                type="primary"
                underline="never"
                href="https://gitee.com/fastapiadmin/FastapiAdmin/releases"
                target="_blank"
              >
                完整记录
                <ElIcon class="link-icon"><TopRight /></ElIcon>
              </ElLink>
            </div>
          </template>
          <ElScrollbar height="300px">
            <ElTimeline class="p-2">
              <ElTimelineItem
                v-for="(item, index) in vesionList"
                :key="index"
                :timestamp="item.date"
                placement="top"
                :color="index === 0 ? '#67C23A' : '#909399'"
                :hollow="index !== 0"
              >
                <div class="version-item" :class="{ 'latest-item': index === 0 }">
                  <div class="flex items-center justify-between">
                    <ElText tag="strong">{{ item.title }}</ElText>
                    <ElTag v-if="item.tag" :type="index === 0 ? 'success' : 'info'" size="small">
                      {{ item.tag }}
                    </ElTag>
                  </div>
                  <ElText class="version-content">{{ item.content }}</ElText>
                  <div v-if="item.link">
                    <ElLink
                      :type="index === 0 ? 'primary' : 'info'"
                      :href="item.link"
                      target="_blank"
                      underline="never"
                    >
                      详情
                      <ElIcon class="link-icon"><TopRight /></ElIcon>
                    </ElLink>
                  </div>
                </div>
              </ElTimelineItem>
            </ElTimeline>
          </ElScrollbar>
        </ElCard>
      </ElCol>
      <ElCol :span="12" class="flex flex-col">
        <AboutProject />
      </ElCol>
    </ElRow>
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: "Home", inheritAttrs: false });

import { useUserStore } from "@stores/index";
import MenuRouteIcon from "@/components/others/fa-menu-routeIcon/index.vue";
import Calendar from "@/components/others/fa-calendar/index.vue";
import CardList from "../workplace/modules/card-list.vue";
import AboutProject from "../workplace/modules/about-project.vue";
import { greetings } from "@utils/common";
import { ref, onMounted, onUnmounted } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import {
  Delete,
  UserFilled,
  Close,
  Star,
  QuestionFilled,
  Document,
  Folder,
  TopRight,
} from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { quickStartManager, QUICK_LINK_MAX, type QuickLink } from "@utils/common";
import { dayjs } from "element-plus";
import FaSvgIcon from "@/components/base/fa-svg-icon/index.vue";
import { resolveIconForFaSvgIcon } from "@utils/menuIcon/remix";

const timefix = greetings();
const userStore = useUserStore();
const { t } = useI18n();
const router = useRouter();
const welcome = "祝你开心每一天！";

interface VersionItem {
  id: string;
  title: string;
  date: string;
  content: string;
  link: string;
  tag?: string;
}
const vesionList = ref<VersionItem[]>([
  {
    id: "1",
    title: "v3.2.1",
    date: dayjs().format("YYYY-MM-DD HH:mm:ss"),
    content: "优化性能，修复若干小bug。",
    link: "https://gitee.com/fastapiadmin/FastapiAdmin/releases",
    tag: "更新",
  },
  {
    id: "2",
    title: "v3.2.0",
    date: dayjs().subtract(1, "day").format("YYYY-MM-DD HH:mm:ss"),
    content: "新增用户行为分析功能。",
    link: "https://gitee.com/fastapiadmin/FastapiAdmin/releases",
    tag: "新功能",
  },
  {
    id: "3",
    title: "v3.1.0",
    date: dayjs().subtract(3, "day").format("YYYY-MM-DD HH:mm:ss"),
    content: "优化权限管理系统。",
    link: "https://gitee.com/fastapiadmin/FastapiAdmin/releases",
    tag: "优化",
  },
]);

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

const quickLinks = ref<QuickLink[]>(quickStartManager.getQuickLinks());
const handleQuickLinkClick = (item: QuickLink) => {
  if (item.href) {
    router.push(item.href).catch(() => {
      ElMessage.warning(`路由 ${item.href} 不存在，请检查配置`);
    });
  } else {
    ElMessage.info(`${item.title} 功能待开发`);
  }
};
const QUICK_LINK_PALETTE = ["#4080ff", "#23c343", "#ff9a2e", "#f76560", "#a9aeb8", "#00b42a"];
const getQuickLinkColor = (index: number) => QUICK_LINK_PALETTE[index % QUICK_LINK_PALETTE.length];
const getQuickLinkStableIndex = (item: QuickLink): number => {
  const i = quickLinks.value.findIndex((l) =>
    l.id != null && l.id !== "" ? l.id === item.id : l.href === item.href
  );
  return i >= 0 ? i : 0;
};
const handleDeleteLink = async (item: QuickLink) => {
  try {
    await ElMessageBox.confirm(`确定要取消收藏"${item.title}"吗？`, "取消收藏确认", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    if (item.id) quickStartManager.removeQuickLink(item.id);
    else if (item.href) quickStartManager.removeQuickLinkByHref(item.href);
    else {
      ElMessage.warning("无法移除：缺少标识");
      return;
    }
    ElMessage.success(`已取消收藏：${item.title}`);
  } catch {
    /* 用户取消 */
  }
};
const clearBookmarks = async () => {
  try {
    await ElMessageBox.confirm("确定要清空收藏吗？", "清空收藏确认", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    quickStartManager.clearQuickLinks();
    ElMessage.success("已清空收藏");
  } catch {
    /* 用户取消 */
  }
};
const updateQuickLinks = (links: QuickLink[]) => {
  quickLinks.value = links;
};
onMounted(() => {
  quickStartManager.addListener(updateQuickLinks);
});
onUnmounted(() => {
  quickStartManager.removeListener(updateQuickLinks);
});
</script>

<style scoped lang="scss">
:deep(.el-card) {
  --el-card-border-radius: calc(var(--custom-radius) + 2px);

  border: 1px solid var(--fa-card-border);
}

.dashboard-container {
  position: relative;
  display: flex;
  flex-direction: column;

  > * {
    margin-bottom: 16px;
  }

  > :last-child {
    margin-bottom: 0;
  }

  &::after {
    display: block;
    flex-shrink: 0;
    height: 16px;
    content: "";
  }
}

.github-corner {
  position: absolute;
  top: 0;
  right: 0;
  z-index: 1;
  border: 0;
}

.version-item {
  padding: 10px 12px;
  background: var(--el-fill-color-lighter);
  border-radius: 8px;
  transition: all 0.2s;

  &.latest-item {
    background: var(--el-color-primary-light-9);
    border: 1px solid var(--el-color-primary-light-5);
  }

  &:hover {
    transform: translateX(5px);
  }

  .version-content {
    display: block;
    margin-top: 6px;
    margin-bottom: 8px;
    font-size: 13px;
    line-height: 1.4;
    color: var(--el-text-color-secondary);
  }
}

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

.workplace-surface {
  overflow: hidden;
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 12px;

  :deep(.el-card__header) {
    border-bottom-color: var(--el-border-color-extra-light);
  }
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

.workplace-hero__avatar {
  border: 2px solid var(--el-bg-color);
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

.workplace-module-bookmarks__help {
  flex-shrink: 0;
  color: var(--el-text-color-secondary);
  cursor: help;
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

.workplace-section-card__head {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: flex-start;
  justify-content: space-between;
  width: 100%;
}
</style>
