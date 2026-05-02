<!-- 引导页 -->
<template>
  <el-tour v-model="open" :show-close="false" @change="handleChange">
    <el-tour-step
      v-for="(step, index) in steps"
      :key="index"
      :target="step.target"
      :title="step.title"
      :description="step.description"
      :prev-button-props="{
        children: t('common.prevLabel'),
        onClick: handlePrevClick,
      }"
      :next-button-props="{
        children: nextBtnName(index),
        onClick: handleNextClick,
      }"
      :placement="step.placement"
    />
    <template #indicators>
      <el-button size="small" @click="handleSkip">{{ t("common.skipLabel") }}</el-button>
    </template>
  </el-tour>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useSettingsStore } from "@/store";

const settingStore = useSettingsStore();
const { t } = useI18n();

const props = defineProps({
  // 是否可见
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

interface TourStep {
  target: string;
  title: string;
  description: string;
  placement: "top" | "bottom" | "left" | "right";
}

const layout = settingStore.layout;

const menuTarget = (): string => {
  if (layout === "left") {
    return ".layout__sidebar";
  } else if (layout === "top") {
    return ".layout__header-left";
  } else {
    return ".layout__header-menu";
  }
};

// 内置引导步骤数据
const steps: TourStep[] = [
  {
    target: menuTarget(),
    title: t("common.menu"),
    description: t("common.menuDes"),
    placement: layout === "left" ? "right" : "bottom",
  },
  {
    target: ".navbar-actions",
    title: t("common.tool"),
    description: t("common.toolDes"),
    placement: "bottom",
  },
  {
    target: ".tags-container",
    title: t("common.tagsView"),
    description: t("common.tagsViewDes"),
    placement: "bottom",
  },
];

// 当前步数
const currentStep = ref(0);

// 动态设置下一步按钮名称
const nextBtnName = computed(() => (index: number) => {
  if (index === steps.length - 1) {
    return t("common.doneLabel");
  }
  return t("common.nextLabel");
});

// 步数切换时触发
function handleChange(step: number) {
  currentStep.value = step;
  emit("change", step);
}

// 点击跳过按钮时触发
function handleSkip() {
  open.value = false;
  emit("skip");
}

// 点击上一步按钮时触发
function handlePrevClick() {
  emit("prev");
}

// 点击下一步按钮时触发
function handleNextClick() {
  emit("next");
}
</script>

<style scoped>
/* 可根据需要添加自定义样式 */
.el-tour__content .el-tour-indicators {
  display: flex;
  justify-content: flex-end;
  margin-right: 5px;
}
</style>
