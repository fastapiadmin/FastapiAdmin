<!-- 仪表盘首页：快捷入口 + 收藏夹 + 数据概览卡片 -->
<template>
  <div class="dashboard-container">
    <!-- github 角标 -->
    <FaGithubCorner class="github-corner" />

    <ElCard shadow="hover">
      <div class="flex flex-wrap items-center gap-y-3">
        <!-- 左侧问候语区域 -->
        <div class="flex min-w-0 flex-1 items-center">
          <div class="size-20 shrink-0 rounded-full bg-g-100 flex items-center justify-center">
            <ElAvatar
              v-if="userStore.basicInfo.avatar"
              size="large"
              :src="userStore.basicInfo.avatar"
              class="workplace-hero__avatar"
            />
            <ElIcon v-else :size="40" class="text-g-600">
              <UserFilled />
            </ElIcon>
          </div>
          <div>
            <div class="workplace-hero__greeting">
              {{ timefix }}{{ currentUser.name }}，{{ welcome }}
            </div>
            <ElText class="workplace-hero__meta">
              <p class="text-sm text-g-600">
                {{ currentUser.username }} · {{ currentUser.dept_name }} ·
                {{ currentUser.description }} · 今日天气晴朗，气温在15℃至25℃之间，东南风。
              </p>
            </ElText>
          </div>
        </div>

        <!-- 右侧图标区域 - PC端 -->
        <div class="hidden shrink-0 sm:block">
          <div class="flex items-center space-x-6">
            <!-- 文档 -->
            <div class="flex flex-col items-center">
              <div class="flex items-center text-sm font-bold text-[#4080ff]">
                <ElIcon class="mr-0.5"><Document /></ElIcon>
                文档
              </div>
              <div class="mt-3 whitespace-nowrap">
                <ElLink
                  href="https://blog.csdn.net/weixin_46768253/article/details/149569141?spm=1001.2014.3001.5502"
                  target="_blank"
                >
                  <FaSvgIcon :icon="resolveIconForFaSvgIcon('csdn')" class="text-lg" />
                </ElLink>
              </div>
            </div>
            <!-- 仓库 -->
            <div class="flex flex-col items-center">
              <div class="flex items-center text-sm font-bold text-[#ff9a2e]">
                <ElIcon class="mr-0.5">
                  <Folder />
                </ElIcon>
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

        <!-- 移动端图标区域 -->
        <div class="w-full sm:hidden">
          <div class="flex justify-end space-x-4 overflow-x-auto">
            <!-- 仓库图标 -->
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

    <!-- 数据统计 -->
    <ElRow :gutter="16" class="mt-4">
      <!-- 在线用户数量 -->
      <ElCol :span="8" :xs="24" class="mb-3 sm:mb-0">
        <ElCard shadow="hover" class="h-full flex flex-col">
          <template #header>
            <div class="flex items-center justify-between">
              <span class="text-g-600">在线用户</span>
              <ElTag type="danger" size="small">实时</ElTag>
            </div>
          </template>

          <div class="flex items-center justify-between mt-2 flex-1">
            <div class="flex items-center">
              <span class="text-lg transition-all duration-300 hover:scale-110">9999</span>
              <span v-if="true" class="ml-2 text-xs text-success">
                <ElIcon>
                  <Connection />
                </ElIcon>
                已连接
              </span>
              <span v-else class="ml-2 text-xs text-danger">
                <ElIcon>
                  <Failed />
                </ElIcon>
                未连接
              </span>
            </div>
            <FaSvgIcon
              :icon="resolveIconForFaSvgIcon('people')"
              class="size-8 animate-[pulse_2s_infinite]"
            />
          </div>

          <div class="flex items-center justify-between mt-2 text-sm text-g-600">
            <span>更新时间</span>
            <span>2025-07-12 00:00:00</span>
          </div>
        </ElCard>
      </ElCol>

      <!-- 访客数(UV) -->
      <ElCol :span="8" :xs="24" class="mb-3 sm:mb-0">
        <ElSkeleton :loading="visitStatsLoading" :rows="5" animated>
          <template #template>
            <ElCard>
              <template #header>
                <div>
                  <ElSkeletonItem variant="h3" style="width: 40%" />
                  <ElSkeletonItem variant="rect" style="float: right; width: 1em; height: 1em" />
                </div>
              </template>

              <div class="flex items-center justify-between">
                <ElSkeletonItem variant="text" style="width: 30%" />
                <ElSkeletonItem variant="circle" style="width: 2em; height: 2em" />
              </div>
              <div class="mt-5 flex items-center justify-between">
                <ElSkeletonItem variant="text" style="width: 50%" />
                <ElSkeletonItem variant="text" style="width: 1em" />
              </div>
            </ElCard>
          </template>
          <template v-if="!visitStatsLoading">
            <ElCard shadow="hover" class="h-full flex flex-col">
              <template #header>
                <div class="flex items-center justify-between">
                  <span class="text-g-600">访客数(UV)</span>
                  <ElTag type="success" size="small">日</ElTag>
                </div>
              </template>

              <div class="flex items-center justify-between mt-2 flex-1">
                <div class="flex items-center">
                  <span class="text-lg">{{ Math.round(transitionUvCount) }}</span>
                  <span
                    :class="[
                      'text-xs',
                      'ml-2',
                      computeGrowthRateClass(visitStatsData.uvGrowthRate),
                    ]"
                  >
                    <ElIcon>
                      <Top v-if="visitStatsData.uvGrowthRate > 0" />
                      <Bottom v-else-if="visitStatsData.uvGrowthRate < 0" />
                    </ElIcon>
                    {{ formatGrowthRate(visitStatsData.uvGrowthRate) }}
                  </span>
                </div>
                <FaSvgIcon :icon="resolveIconForFaSvgIcon('visitor')" class="size-8" />
              </div>

              <div class="flex items-center justify-between mt-2 text-sm text-g-600">
                <span>总访客数</span>
                <span>{{ Math.round(transitionTotalUvCount) }}</span>
              </div>
            </ElCard>
          </template>
        </ElSkeleton>
      </ElCol>

      <!-- 浏览量(PV) -->
      <ElCol :span="8" :xs="24">
        <ElSkeleton :loading="visitStatsLoading" :rows="5" animated>
          <template #template>
            <ElCard>
              <template #header>
                <div>
                  <ElSkeletonItem variant="h3" style="width: 40%" />
                  <ElSkeletonItem variant="rect" style="float: right; width: 1em; height: 1em" />
                </div>
              </template>

              <div class="flex items-center justify-between">
                <ElSkeletonItem variant="text" style="width: 30%" />
                <ElSkeletonItem variant="circle" style="width: 2em; height: 2em" />
              </div>
              <div class="mt-5 flex items-center justify-between">
                <ElSkeletonItem variant="text" style="width: 50%" />
                <ElSkeletonItem variant="text" style="width: 1em" />
              </div>
            </ElCard>
          </template>
          <template v-if="!visitStatsLoading">
            <ElCard shadow="hover" class="h-full flex flex-col">
              <template #header>
                <div class="flex items-center justify-between">
                  <span class="text-g-600">浏览量(PV)</span>
                  <ElTag type="primary" size="small">日</ElTag>
                </div>
              </template>

              <div class="flex items-center justify-between mt-2 flex-1">
                <div class="flex items-center">
                  <span class="text-lg">{{ Math.round(transitionPvCount) }}</span>
                  <span
                    :class="[
                      'text-xs',
                      'ml-2',
                      computeGrowthRateClass(visitStatsData.pvGrowthRate),
                    ]"
                  >
                    <ElIcon>
                      <Top v-if="visitStatsData.pvGrowthRate > 0" />
                      <Bottom v-else-if="visitStatsData.pvGrowthRate < 0" />
                    </ElIcon>
                    {{ formatGrowthRate(visitStatsData.pvGrowthRate) }}
                  </span>
                </div>
                <FaSvgIcon :icon="resolveIconForFaSvgIcon('browser')" class="size-8" />
              </div>

              <div class="flex items-center justify-between mt-2 text-sm text-g-600">
                <span>总浏览量</span>
                <span>{{ Math.round(transitionTotalPvCount) }}</span>
              </div>
            </ElCard>
          </template>
        </ElSkeleton>
      </ElCol>
    </ElRow>

    <ElRow :gutter="16" class="mt-4">
      <!-- 访问趋势统计图 -->
      <ElCol :xs="24" :span="8">
        <ElCard>
          <template #header>
            <div class="flex items-center justify-between">
              <span>访问趋势</span>
              <ElRadioGroup v-model="visitTrendDateRange" size="small">
                <ElRadioButton :value="7">近7天</ElRadioButton>
                <ElRadioButton :value="30">近30天</ElRadioButton>
              </ElRadioGroup>
            </div>
          </template>
          <ECharts :options="visitTrendChartOptions" height="calc(100vh - 550px)" />
        </ElCard>
      </ElCol>
      <!-- 最新动态 -->
      <ElCol :xs="24" :span="8">
        <ElCard>
          <template #header>
            <div class="flex items-center justify-between">
              <span class="header-title">最新动态</span>
              <ElLink
                type="primary"
                underline="never"
                href="https://gitee.com/fastapiadmin/FastapiAdmin/releases"
                target="_blank"
              >
                完整记录
                <ElIcon class="link-icon">
                  <TopRight />
                </ElIcon>
              </ElLink>
            </div>
          </template>

          <ElScrollbar height="calc(100vh - 550px)">
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
                      <ElIcon class="link-icon">
                        <TopRight />
                      </ElIcon>
                    </ElLink>
                  </div>
                </div>
              </ElTimelineItem>
            </ElTimeline>
          </ElScrollbar>
        </ElCard>
      </ElCol>

      <ElCol :xs="24" :span="8">
        <ElCard>
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
          <div style="height: calc(100vh - 550px)">
            <template v-if="quickLinks.length > 0">
              <div>
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
                      :style="{
                        backgroundColor: getQuickLinkColor(getQuickLinkStableIndex(item)),
                      }"
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
            </template>
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
          </div>
        </ElCard>
      </ElCol>
    </ElRow>
  </div>

  <div class="ecommerce mt-4">
    <ElRow :gutter="20">
      <ElCol :sm="24" :md="24" :lg="16">
        <Banner />
      </ElCol>
      <ElCol :sm="12" :md="12" :lg="4">
        <TotalOrderVolume />
      </ElCol>
      <ElCol :sm="12" :md="12" :lg="4">
        <TotalProducts />
      </ElCol>
    </ElRow>

    <ElRow :gutter="20">
      <ElCol :sm="12" :md="12" :lg="8">
        <SalesTrend />
      </ElCol>
      <ElCol :sm="12" :md="12" :lg="8">
        <SalesClassification />
      </ElCol>
      <ElCol :sm="24" :md="24" :lg="8">
        <ElRow :gutter="20">
          <ElCol :sm="24" :md="12" :lg="12">
            <ProductSales />
          </ElCol>
          <ElCol :sm="24" :md="12" :lg="12">
            <SalesGrowth />
          </ElCol>
          <ElCol :span="24" class="no-margin-bottom">
            <CartConversionRate />
          </ElCol>
        </ElRow>
      </ElCol>
    </ElRow>

    <ElRow :gutter="20">
      <ElCol :sm="24" :md="12" :lg="8">
        <HotCommodity />
      </ElCol>
      <ElCol :sm="24" :md="12" :lg="8">
        <AnnualSales />
      </ElCol>
      <ElCol :sm="24" :md="24" :lg="8">
        <TransactionList />
      </ElCol>
    </ElRow>

    <ElRow :gutter="20">
      <ElCol :md="24" :lg="8">
        <RecentTransaction />
      </ElCol>
      <ElCol :md="24" :lg="16" class="no-margin-bottom">
        <HotProductsList />
      </ElCol>
    </ElRow>
  </div>

  <div class="workplace-page">
    <!-- 横幅组件演示（原 widgets/banners，后续可调整） -->
    <div class="mt-4 workplace-banners-showcase">
      <h2 class="workplace-banners-showcase__title">基础 & 自定义按钮+背景色</h2>
      <ElRow :gutter="20">
        <ElCol :xs="24" :sm="12" :md="12" class="mb-5">
          <FaBasicBanner
            title="数据中心运行状态"
            subtitle="系统访问量同比增长 23%，所有服务运行稳定，数据监控正常。"
          />
        </ElCol>
        <ElCol :xs="24" :sm="12" :md="12" class="mb-5">
          <FaBasicBanner
            title="欢迎使用 Art Design Pro"
            subtitle="基于 Vue 3 + TypeScript + Element Plus 构建的现代化管理系统。"
            titleColor="#333"
            subtitleColor="#666"
            boxStyle="!bg-[#D4F1F7]"
            :buttonConfig="{
              show: true,
              text: '开始探索',
              color: 'var(--fa-success)',
              textColor: '#fff',
              radius: '6px',
            }"
            @buttonClick="handleBannerDemoClick"
          />
        </ElCol>
      </ElRow>

      <h2 class="workplace-banners-showcase__title">自定义图片 & 使用 slot 自定义内容</h2>

      <ElRow :gutter="20">
        <ElCol :xs="24" :sm="12" :md="12" class="mb-5">
          <FaBasicBanner
            title="探索星空计划"
            subtitle="加入我们的天文观测活动，发现宇宙的奥秘"
            boxStyle="!bg-[#FF8AAB]"
            :buttonConfig="{
              show: true,
              text: '立即参与',
              color: '#FF5A89',
              textColor: '#fff',
            }"
            :imageConfig="{
              src: bannerIcon3,
            }"
          />
        </ElCol>
        <ElCol :xs="24" :sm="12" :md="12" class="mb-5">
          <FaBasicBanner
            boxStyle="!bg-[#70B1FF]"
            :imageConfig="{
              src: bannerIcon5,
            }"
          >
            <template #title>
              <h3 class="workplace-banners-showcase__slot-heading">智能组件系统</h3>
            </template>

            <template #subtitle>
              <div class="workplace-banners-showcase__slot-sub">
                <p class="workplace-banners-showcase__slot-sub-p">
                  灵活配置，强大扩展，支持自定义插槽内容
                </p>
              </div>
            </template>

            <template #button>
              <div class="workplace-banners-showcase__slot-btn-wrap">
                <ElButton type="primary" color="#04A1FF">查看文档</ElButton>
              </div>
            </template>
          </FaBasicBanner>
        </ElCol>
      </ElRow>

      <h2 class="workplace-banners-showcase__title">抽象配置方案（Preset 模式）</h2>
      <ElRow :gutter="20">
        <ElCol :xs="24" :sm="12" :md="12" class="mb-5">
          <FaBasicBanner v-bind="presetBanners.marketing" />
        </ElCol>
        <ElCol :xs="24" :sm="12" :md="12" class="mb-5">
          <FaBasicBanner v-bind="presetBanners.info" />
        </ElCol>
      </ElRow>

      <h2 class="workplace-banners-showcase__title">卡片横幅</h2>
      <ElRow :gutter="20">
        <ElCol :xs="24" :sm="12" :md="12" :lg="6" class="mb-5">
          <FaCardBanner
            title="系统运行正常"
            description="所有核心服务运行稳定，响应时间在正常范围内。"
          />
        </ElCol>
        <ElCol :xs="24" :sm="12" :md="12" :lg="6" class="mb-5">
          <FaCardBanner
            :image="bannerIcon2"
            title="重要消息通知"
            description="您有 3 条待处理的重要消息，请及时查看。"
            :button="{
              show: true,
              text: '查看详情',
              color: 'var(--fa-warning)',
              textColor: '#fff',
            }"
          />
        </ElCol>
        <ElCol :xs="24" :sm="12" :md="12" :lg="6" class="mb-5">
          <FaCardBanner
            :image="bannerIcon3"
            title="数据分析报告"
            description="本周业务数据分析报告已完成，请查看关键指标。"
            :button="{
              show: true,
              text: '下载报告',
              color: 'var(--fa-error)',
              textColor: '#fff',
            }"
          />
        </ElCol>
        <ElCol :xs="24" :sm="12" :md="12" :lg="6" class="mb-5">
          <FaCardBanner
            :image="bannerIcon4"
            title="版本更新提醒"
            description="Art Design Pro v2.1.0 已发布，包含性能优化和新功能。"
            :button="{
              show: true,
              text: '立即更新',
              color: 'var(--theme-color)',
              textColor: '#fff',
            }"
            :cancelButton="{
              show: true,
              text: '稍后提醒',
              color: '#eee',
              textColor: '#333',
            }"
            @click="handleBannerDemoConfirm"
            @cancel="handleBannerDemoCancel"
          />
        </ElCol>
      </ElRow>
    </div>

    <!-- 日程日历（系统日志 / 消息区后期再调整） -->
    <div class="mt-4 workplace-ops-stack">
      <ElRow :gutter="16" class="workplace-ops-row">
        <ElCol :xs="24" class="workplace-ops-col workplace-ops-col--calendar">
          <ElCard
            shadow="hover"
            class="workplace-calendar-card workplace-surface workplace-ops-card"
          >
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
            <div class="workplace-ops-card__body workplace-ops-card__body--calendar">
              <Calendar />
            </div>
          </ElCard>
        </ElCol>
      </ElRow>
    </div>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "Home",
  inheritAttrs: false,
});

import { useUserStore } from "@stores/index";
import MenuRouteIcon from "@/components/others/fa-menu-routeIcon/index.vue";
import Calendar from "@/components/others/fa-calendar/index.vue";
import { greetings } from "@utils/common";
import { ref, onMounted, onUnmounted, computed } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import {
  Delete,
  UserFilled,
  Close,
  Star,
  QuestionFilled,
  Bottom,
  Connection,
  Document,
  Failed,
  Folder,
  Top,
  TopRight,
} from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { quickStartManager, QUICK_LINK_MAX, type QuickLink } from "@utils/common";
import bannerIcon2 from "@imgs/3d/icon2.webp";
import bannerIcon3 from "@imgs/3d/icon3.webp";
import bannerIcon4 from "@imgs/3d/icon4.webp";
import bannerIcon5 from "@imgs/3d/icon7.webp";
import { dayjs } from "element-plus";
import { formatGrowthRate } from "@utils";
import { useTransition } from "@vueuse/core";
import FaSvgIcon from "@/components/base/fa-svg-icon/index.vue";
import { resolveIconForFaSvgIcon } from "@utils/menuIcon/remix";
import Banner from "./modules/banner.vue";
import TotalOrderVolume from "./modules/total-order-volume.vue";
import TotalProducts from "./modules/total-products.vue";
import SalesTrend from "./modules/sales-trend.vue";
import SalesClassification from "./modules/sales-classification.vue";
import TransactionList from "./modules/transaction-list.vue";
import HotCommodity from "./modules/hot-commodity.vue";
import RecentTransaction from "./modules/recent-transaction.vue";
import AnnualSales from "./modules/annual-sales.vue";
import ProductSales from "./modules/product-sales.vue";
import SalesGrowth from "./modules/sales-growth.vue";
import CartConversionRate from "./modules/cart-conversion-rate.vue";
import HotProductsList from "./modules/hot-products-list.vue";

const timefix = greetings();
const userStore = useUserStore();
const { t } = useI18n();
const router = useRouter();

const welcome = "祝你开心每一天！";

interface VersionItem {
  id: string;
  title: string; // 版本标题（如：v2.4.0）
  date: string; // 发布时间
  content: string; // 版本描述
  link: string; // 详情链接
  tag?: string; // 版本标签（可选）
}

// 当前通知公告列表
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

// 访客统计数据加载状态
const visitStatsLoading = ref(true);
// 访客统计数据
const visitStatsData = ref({
  todayUvCount: 0,
  uvGrowthRate: 0,
  totalUvCount: 0,
  todayPvCount: 0,
  pvGrowthRate: 0,
  totalPvCount: 0,
});

// 数字过渡动画
const transitionUvCount = useTransition(
  computed(() => visitStatsData.value.todayUvCount),
  {
    duration: 1000,
    transition: [0.25, 0.1, 0.25, 1.0], // CSS cubic-bezier
  }
);

const transitionTotalUvCount = useTransition(
  computed(() => visitStatsData.value.totalUvCount),
  {
    duration: 1200,
    transition: [0.25, 0.1, 0.25, 1.0],
  }
);

const transitionPvCount = useTransition(
  computed(() => visitStatsData.value.todayPvCount),
  {
    duration: 1000,
    transition: [0.25, 0.1, 0.25, 1.0],
  }
);

const transitionTotalPvCount = useTransition(
  computed(() => visitStatsData.value.totalPvCount),
  {
    duration: 1200,
    transition: [0.25, 0.1, 0.25, 1.0],
  }
);

// 访问趋势日期范围（单位：天）
const visitTrendDateRange = ref(7);
// 访问趋势图表配置
const visitTrendChartOptions = ref();

/**
 * 更新访问趋势图表的配置项
 *
 * @param data - 访问趋势数据
 */
const updateVisitTrendChartOptions = () => {
  visitTrendChartOptions.value = {
    tooltip: {
      trigger: "axis",
    },
    legend: {
      data: ["浏览量(PV)", "访客数(UV)"],
      bottom: 0,
    },
    grid: {
      left: "1%",
      right: "5%",
      bottom: "10%",
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: Array.from({ length: visitTrendDateRange.value }, (_, index) =>
        dayjs()
          .subtract(visitTrendDateRange.value - index - 1, "day")
          .format("YYYY-MM-DD")
      ),
    },
    yAxis: {
      type: "value",
      splitLine: {
        show: true,
        lineStyle: {
          type: "dashed",
        },
      },
    },
    series: [
      {
        name: "浏览量(PV)",
        type: "line",
        data: Array.from(
          { length: visitTrendDateRange.value },
          () => Math.floor(Math.random() * 500) + 100
        ),
        areaStyle: {
          color: "rgba(64, 158, 255, 0.1)",
        },
        smooth: true,
        itemStyle: {
          color: "#4080FF",
        },
        lineStyle: {
          color: "#4080FF",
        },
      },
      {
        name: "访客数(UV)",
        type: "line",
        data: Array.from(
          { length: visitTrendDateRange.value },
          () => Math.floor(Math.random() * 200) + 50
        ),
        areaStyle: {
          color: "rgba(103, 194, 58, 0.1)",
        },
        smooth: true,
        itemStyle: {
          color: "#67C23A",
        },
        lineStyle: {
          color: "#67C23A",
        },
      },
    ],
  };
};

/**
 * 根据增长率计算对应的 CSS 类名
 *
 * @param growthRate - 增长率数值
 */
const computeGrowthRateClass = (growthRate?: number): string => {
  if (!growthRate) {
    return "text-[--el-color-info]";
  }
  if (growthRate > 0) {
    return "text-[--el-color-danger]";
  } else if (growthRate < 0) {
    return "text-[--el-color-success]";
  } else {
    return "text-[--el-color-info]";
  }
};

// 监听访问趋势日期范围的变化，重新获取趋势数据
watch(
  () => visitTrendDateRange.value,
  () => {
    updateVisitTrendChartOptions();
  },
  { immediate: true }
);

// 组件挂载后加载访客统计数据和通知公告数据
onMounted(() => {
  visitStatsLoading.value = false;
  visitStatsData.value = {
    todayUvCount: Math.floor(Math.random() * 200) + 50,
    uvGrowthRate: parseFloat((Math.random() * 20 - 10).toFixed(2)),
    totalUvCount: Math.floor(Math.random() * 5000) + 1000,
    todayPvCount: Math.floor(Math.random() * 500) + 100,
    pvGrowthRate: parseFloat((Math.random() * 20 - 10).toFixed(2)),
    totalPvCount: Math.floor(Math.random() * 20000) + 5000,
  };
  updateVisitTrendChartOptions();
});

/** 横幅演示（原 widgets/banners） */
function handleBannerDemoClick() {
  console.log("banner clicked");
}

function handleBannerDemoConfirm() {
  console.log("confirm clicked");
}

function handleBannerDemoCancel() {
  console.log("cancel clicked");
}

const presetBanners = {
  marketing: {
    title: "限时优惠活动",
    subtitle: "精选商品 48 小时闪购，最高享受 7 折优惠，数量有限！",
    titleColor: "var(--fa-gray-900)",
    subtitleColor: "var(--fa-gray-900)",
    boxStyle: "!bg-success/15",
    meteorConfig: { enabled: true, count: 15 },
    buttonConfig: {
      show: true,
      text: "立即抢购",
      color: "var(--fa-success)",
      textColor: "#fff",
    },
  },
  info: {
    title: "服务到期提醒",
    subtitle: "您的高级服务将在 7 天后到期，请及时续费以继续享受完整功能。",
    titleColor: "var(--fa-gray-900)",
    subtitleColor: "var(--fa-gray-900)",
    boxStyle: "!bg-theme/15",
    meteorConfig: { enabled: true, count: 15 },
    buttonConfig: {
      show: true,
      text: "立即续费",
      color: "var(--fa-secondary)",
      textColor: "#fff",
    },
  },
} as const;

// 快速链接数据
const quickLinks = ref<QuickLink[]>(quickStartManager.getQuickLinks());

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
const handleDeleteLink = async (item: QuickLink) => {
  try {
    await ElMessageBox.confirm(`确定要取消收藏"${item.title}"吗？`, "取消收藏确认", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    if (item.id) {
      quickStartManager.removeQuickLink(item.id);
    } else if (item.href) {
      quickStartManager.removeQuickLinkByHref(item.href);
    } else {
      ElMessage.warning("无法移除：缺少标识");
      return;
    }
    ElMessage.success(`已取消收藏：${item.title}`);
  } catch {
    // 用户取消
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
    // 用户取消
  }
};

// 监听快速链接变化
const updateQuickLinks = (links: QuickLink[]) => {
  quickLinks.value = links;
};

// 组件挂载时获取数据和添加监听器
onMounted(() => {
  quickStartManager.addListener(updateQuickLinks);
});

// 组件卸载时移除监听器
onUnmounted(() => {
  quickStartManager.removeListener(updateQuickLinks);
});

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
</script>

<style scoped lang="scss">
.dashboard-container {
  position: relative;

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

.workplace-calendar-card {
  :deep(.el-card__body) {
    padding: 8px 10px 10px;
  }
}

.workplace-ops-col--calendar {
  max-width: 100%;
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

/* —— 顶栏 —— */
.workplace-hero-card {
  :deep(.el-card__body) {
    padding: 20px 22px;
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

/* 首页横幅组件演示区 */
.workplace-banners-showcase {
  padding: 16px;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-lighter);
  border-radius: var(--el-border-radius-base);
}

.workplace-banners-showcase__title {
  margin: 20px 0 16px;
  font-size: 1.25rem;
  font-weight: 500;
  color: var(--el-text-color-primary);

  &:first-child {
    margin-top: 0;
  }
}

.workplace-banners-showcase__slot-heading {
  margin: 0;
  font-size: 1.6rem;
  color: #fff !important;
}

.workplace-banners-showcase__slot-sub {
  margin-top: 12px;
}

.workplace-banners-showcase__slot-sub-p {
  position: relative;
  z-index: 10;
  margin: 0;
  font-style: italic;
}

.workplace-banners-showcase__slot-btn-wrap {
  margin-top: 12px;
}
</style>
