<!-- 顶部快速入口面板 -->
<template>
  <ElPopover
    ref="popoverRef"
    :width="700"
    :offset="0"
    :show-arrow="false"
    trigger="hover"
    placement="bottom-start"
    popper-class="fast-enter-popover"
    :popper-style="{
      border: '1px solid var(--default-border)',
      borderRadius: 'calc(var(--custom-radius) / 2 + 4px)',
    }"
  >
    <template #reference>
      <div class="flex-c gap-2">
        <slot />
      </div>
    </template>

    <div class="grid grid-cols-[2fr_0.8fr]">
      <div>
        <div class="grid grid-cols-2 gap-1.5">
          <!-- 应用列表 -->
          <div
            v-for="application in enabledApplications"
            :key="application.name"
            class="mr-3 c-p flex-c gap-3 rounded-lg p-2 hover:bg-g-200/70 dark:hover:bg-g-200/90 hover:[&_.app-icon]:bg-transparent!"
            @click="handleApplicationClick(application)"
          >
            <div class="app-icon size-12 flex-cc rounded-lg bg-g-200/80 dark:bg-g-300/30">
              <FaSvgIcon
                class="text-xl"
                :icon="application.icon"
                :style="{ color: application.iconColor }"
              />
            </div>
            <div>
              <h3 class="m-0 text-sm font-medium text-g-800">{{ application.name }}</h3>
              <p class="mt-1 text-xs text-g-600">{{ application.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="border-l-d pl-6 pt-2">
        <h3 class="mb-2.5 text-base font-medium text-g-800">快速链接</h3>
        <ul>
          <li
            v-for="quickLink in enabledQuickLinks"
            :key="quickLink.name"
            class="c-p py-2 hover:[&_span]:text-theme"
            @click="handleQuickLinkClick(quickLink)"
          >
            <span class="text-g-600 no-underline">{{ quickLink.name }}</span>
          </li>
        </ul>
      </div>
    </div>
  </ElPopover>

  <!-- 礼花效果介绍弹窗（放在 Popover 外，避免被 Popover 销毁） -->
  <ElDialog
    v-model="fireworksDialogVisible"
    title="礼花效果"
    width="480px"
    :close-on-click-modal="true"
  >
    <div class="px-2">
      <div class="mb-5 flex items-start gap-4">
        <div class="flex-cc size-14 rounded-xl bg-linear-to-br from-purple-400 to-indigo-500">
          <FaSvgIcon icon="ri:loader-line" class="text-2xl text-white" />
        </div>
        <div class="flex-1">
          <h4 class="m-0 text-base font-semibold">节日礼花动画</h4>
          <p class="mt-1 text-sm text-g-500 leading-relaxed">
            根据当前节日自动匹配对应素材的全屏 Canvas 烟花效果，支持多种粒子形状和绚丽色彩。
          </p>
        </div>
      </div>

      <ElDivider />

      <div class="space-y-3">
        <div class="flex items-center gap-3">
          <ElTag type="primary" class="rounded-md! border-0! shrink-0">快捷键</ElTag>
          <span class="text-sm text-g-600">
            <ElTag size="small" class="mr-1!">Ctrl</ElTag>
            +
            <ElTag size="small" class="mx-1!">Shift</ElTag>
            +
            <ElTag size="small" class="ml-1!">P</ElTag>
            <span class="mx-2 text-g-400">/</span>
            <ElTag size="small" class="mr-1!">⌘</ElTag>
            +
            <ElTag size="small" class="mx-1!">Shift</ElTag>
            +
            <ElTag size="small" class="ml-1!">P</ElTag>
          </span>
        </div>
        <div class="flex items-center gap-3">
          <ElTag type="success" class="rounded-md! border-0! shrink-0">节日素材</ElTag>
          <span class="text-sm text-g-600">
            礼花素材与当前节日配置一致，自动匹配春节、元宵、中秋等传统节日主题
          </span>
        </div>
        <div class="flex items-center gap-3">
          <ElTag type="warning" class="rounded-md! border-0! shrink-0">触发方式</ElTag>
          <span class="text-sm text-g-600">
            页面加载时自动检测节日并连发，也可通过快捷键手动触发一次
          </span>
        </div>
      </div>
    </div>
  </ElDialog>
</template>

<script setup lang="ts">
import { useFastEnter } from "@/hooks/core/useFastEnter";
import type { FastEnterApplication, FastEnterQuickLink } from "@/types/config";

defineOptions({ name: "FaFastEnter" });

const router = useRouter();
const popoverRef = ref();
const fireworksDialogVisible = ref(false);

// 使用快速入口配置
const { enabledApplications, enabledQuickLinks } = useFastEnter();

/**
 * 处理导航跳转
 * @param routeName 路由名称
 * @param link 外部链接
 */
const handleNavigate = (
  routeName?: string,
  link?: string,
  routeQuery?: Record<string, string>
): void => {
  const targetPath = routeName || link;

  if (!targetPath) {
    console.warn("导航配置无效：缺少路由名称或链接");
    return;
  }

  if (targetPath.startsWith("http")) {
    window.open(targetPath, "_blank");
  } else {
    router.push({ name: targetPath, query: routeQuery ?? {} });
  }

  popoverRef.value?.hide();
};

/**
 * 处理应用项点击
 * @param application 应用配置对象
 */
const handleApplicationClick = (application: FastEnterApplication): void => {
  if (application.isDialog) {
    popoverRef.value?.hide();
    fireworksDialogVisible.value = true;
    return;
  }
  handleNavigate(application.routeName, application.link, application.routeQuery);
};

/**
 * 处理快速链接点击
 * @param quickLink 快速链接配置对象
 */
const handleQuickLinkClick = (quickLink: FastEnterQuickLink): void => {
  if (quickLink.isDialog) {
    popoverRef.value?.hide();
    fireworksDialogVisible.value = true;
    return;
  }
  handleNavigate(quickLink.routeName, quickLink.link, quickLink.routeQuery);
};
</script>
