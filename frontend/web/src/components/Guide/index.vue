<!-- 新手引导：目标用函数延迟解析并带回退节点，避免找不到节点时浮层居中变成「纯弹窗」 -->
<template>
  <ElTour
    v-model="open"
    :show-close="false"
    :mask="true"
    :z-index="3100"
    append-to="body"
    @change="handleChange"
    @finish="handleTourFinish"
    @close="handleTourClose"
  >
    <ElTourStep
      :target="targetMenu"
      :title="t('common.menu')"
      :description="t('common.menuDes')"
      :placement="placementMenu"
      :prev-button-props="{
        children: t('common.prevLabel'),
        onClick: handlePrevClick,
      }"
      :next-button-props="{
        children: t('common.nextLabel'),
        onClick: handleNextClick,
      }"
    />
    <ElTourStep
      :target="targetToolbar"
      :title="t('common.tool')"
      :description="t('common.toolDes')"
      placement="bottom"
      :prev-button-props="{
        children: t('common.prevLabel'),
        onClick: handlePrevClick,
      }"
      :next-button-props="{
        children: t('common.nextLabel'),
        onClick: handleNextClick,
      }"
    />
    <ElTourStep
      :target="targetTags"
      :title="t('common.tagsView')"
      :description="t('common.tagsViewDes')"
      placement="bottom"
      :prev-button-props="{
        children: t('common.prevLabel'),
        onClick: handlePrevClick,
      }"
      :next-button-props="{
        children: lastStepNextLabel,
        onClick: handleNextClick,
      }"
    />
    <template #indicators>
      <ElButton size="small" @click="handleSkip">{{ t("common.skipLabel") }}</ElButton>
    </template>
  </ElTour>
</template>

<script setup lang="ts">
import { computed, type PropType } from "vue";
import { useSettingsStore } from "@stores";
import { MenuTypeEnum } from "@/enums/appEnum";

const settingStore = useSettingsStore();
const { t } = useI18n();

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  teleport: {
    type: [String, Object] as PropType<string | HTMLElement | null>,
    default: "body",
  },
});

const emit = defineEmits(["update:modelValue", "change", "prev", "next", "skip"]);

const open = computed({
  get: () => props.modelValue,
  set: (val) => emit("update:modelValue", val),
});

function hasUsefulRect(el: HTMLElement): boolean {
  const r = el.getBoundingClientRect();
  return r.width > 4 && r.height > 4;
}

function firstPresent(selectors: string[]): HTMLElement | null {
  for (const sel of selectors) {
    const el = document.querySelector(sel);
    if (el instanceof HTMLElement && hasUsefulRect(el)) {
      return el;
    }
  }
  return null;
}

/** 菜单高亮：按菜单类型优先，其次回退到侧栏 / 顶栏菜单 / 主内容区 */
function resolveMenuEl(): HTMLElement | null {
  const mt = settingStore.menuType as MenuTypeEnum;
  let order: string[] = [];
  switch (mt) {
    case MenuTypeEnum.TOP:
      order = ["#app-menu-top", "#app-menu-top-left", "#app-sidebar", "#app-main"];
      break;
    case MenuTypeEnum.TOP_LEFT:
      order = ["#app-menu-top-left", "#app-menu-top", "#app-sidebar", "#app-main"];
      break;
    case MenuTypeEnum.DUAL_MENU:
    case MenuTypeEnum.LEFT:
    default:
      order = ["#app-sidebar", "#app-menu-top", "#app-menu-top-left", "#app-main"];
      break;
  }
  return firstPresent(order) ?? (document.querySelector("#app-main") as HTMLElement | null);
}

function resolveToolbarEl(): HTMLElement | null {
  return (
    firstPresent(["#app-header-toolbar", "#app-header"]) ??
    (document.querySelector("#app-main") as HTMLElement | null)
  );
}

/** 标签栏关闭时可落到内容区，保证仍有镂空指引 */
function resolveTagsEl(): HTMLElement | null {
  return (
    firstPresent([".worktab-tags-shell", "#app-header", "#app-content"]) ??
    (document.querySelector("#app-main") as HTMLElement | null)
  );
}

/** Element Plus Tour：target 支持函数，在打开时解析 DOM，避免初始渲染阶段节点未就绪 */
function targetMenu(): HTMLElement | null {
  return resolveMenuEl();
}
function targetToolbar(): HTMLElement | null {
  return resolveToolbarEl();
}
function targetTags(): HTMLElement | null {
  return resolveTagsEl();
}

const placementMenu = computed((): "top" | "bottom" | "left" | "right" => {
  const mt = settingStore.menuType as MenuTypeEnum;
  return mt === MenuTypeEnum.LEFT || mt === MenuTypeEnum.DUAL_MENU ? "right" : "bottom";
});

const lastStepNextLabel = computed(() => t("common.doneLabel"));

function handleChange(step: number) {
  emit("change", step);
}

function handleSkip() {
  open.value = false;
  emit("skip");
}

function handleTourFinish() {
  open.value = false;
  emit("skip");
}

function handleTourClose() {
  emit("skip");
}

function handlePrevClick() {
  emit("prev");
}

function handleNextClick() {
  emit("next");
}
</script>

<style scoped>
.el-tour__content .el-tour-indicators {
  display: flex;
  justify-content: flex-end;
  margin-right: 5px;
}
</style>
