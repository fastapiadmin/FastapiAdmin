<!-- 图标选择器 -->
<template>
  <div ref="iconSelectRef" :style="{ width: props.width }">
    <ElPopover :visible="popoverVisible" :width="props.width" placement="bottom-end">
      <template #reference>
        <div @click="popoverVisible = !popoverVisible">
          <slot>
            <ElInput v-model="selectedIcon" readonly placeholder="点击选择图标" class="reference">
              <template #prepend>
                <!-- EP（含 el-icon- 前缀或与 icons-vue 同名的裸值） / Iconify / 自定义 SVG 文件名 -->
                <ElIcon v-if="elementIconComp">
                  <component :is="elementIconComp" />
                </ElIcon>
                <FaSvgIcon v-else-if="selectedIcon" :icon="resolveIconForFaSvgIcon(selectedIcon)" />
              </template>
              <template #suffix>
                <!-- 清空按钮 -->
                <ElIcon
                  v-if="selectedIcon"
                  :style="{ marginRight: '8px' }"
                  @click.stop="clearSelectedIcon"
                >
                  <CircleClose />
                </ElIcon>

                <ElIcon
                  :style="{
                    transform: popoverVisible ? 'rotate(180deg)' : 'rotate(0)',
                    transition: 'transform .5s',
                  }"
                >
                  <ArrowDown @click.stop="togglePopover" />
                </ElIcon>
              </template>
            </ElInput>
          </slot>
        </div>
      </template>

      <!-- 图标选择弹窗 -->
      <div ref="popoverContentRef">
        <ElInput v-model="filterText" placeholder="搜索图标" clearable @input="filterIcons" />
        <ElTabs v-model="activeTab" @tab-click="handleTabClick">
          <ElTabPane label="SVG 图标" name="svg">
            <ElScrollbar height="300px">
              <ul class="flex flex-wrap">
                <li
                  v-for="icon in filteredSvgIcons"
                  :key="'svg-' + icon"
                  class="p-2 m-1 cursor-pointer border border-(--el-border-color) rounded transition-all duration-300 hover:border-(--el-color-primary) hover:scale-120"
                  @click="selectIcon(icon)"
                >
                  <ElTooltip :content="icon" placement="bottom" effect="light">
                    <FaSvgIcon :icon="resolveIconForFaSvgIcon(icon)" />
                  </ElTooltip>
                </li>
              </ul>
            </ElScrollbar>
          </ElTabPane>
          <ElTabPane label="Element 图标" name="element">
            <ElScrollbar height="300px">
              <ul class="flex flex-wrap">
                <li
                  v-for="icon in filteredElementIcons"
                  :key="icon"
                  class="flex-cc p-2 m-1 cursor-pointer border border-(--el-border-color) rounded transition-all duration-300 hover:border-(--el-color-primary) hover:scale-120"
                  @click="selectIcon(icon)"
                >
                  <ElIcon>
                    <component :is="elementPlusIconsVue[icon]" />
                  </ElIcon>
                </li>
              </ul>
            </ElScrollbar>
          </ElTabPane>
        </ElTabs>
      </div>
    </ElPopover>
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: "FaIconSelect" });
import { CircleClose, ArrowDown } from "@element-plus/icons-vue";
import {
  listLocalIconBasenames,
  isIconifyStoredIcon,
  resolveElementPlusIconComponent,
  resolveIconForFaSvgIcon,
} from "@utils";

interface Props {
  modelValue?: string;
  width?: string | number;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: "",
  width: 500,
});

interface Emits {
  "update:modelValue": [value: string];
}

const emit = defineEmits<Emits>();

const iconSelectRef = ref();
const popoverContentRef = ref();
const popoverVisible = ref(false);
const activeTab = ref("svg");

const svgIcons = ref<string[]>([]);
const elementIcons = ref<string[]>([]);
const elementPlusIconsVue = ref<Record<string, any>>({});

// 异步加载 Element Plus 图标，避免影响首屏
async function loadElementIcons() {
  if (elementIcons.value.length > 0) return;
  const icons = await import("@element-plus/icons-vue");
  elementPlusIconsVue.value = icons;
  elementIcons.value = Object.keys(icons);
}
const selectedIcon = defineModel<string | undefined>("modelValue", {
  default: "",
});

const filterText = ref("");
const filteredSvgIcons = ref<string[]>([]);
const filteredElementIcons = ref<string[]>(elementIcons.value);

const elementIconComp = computed(() => resolveElementPlusIconComponent(selectedIcon.value));

function loadIcons() {
  svgIcons.value = listLocalIconBasenames();
  filteredSvgIcons.value = svgIcons.value;
}

async function handleTabClick(tabPane: any) {
  activeTab.value = tabPane.props.name;
  if (tabPane.props.name === "element") {
    await loadElementIcons();
  }
  filterIcons();
}

function filterIcons() {
  if (activeTab.value === "svg") {
    filteredSvgIcons.value = filterText.value
      ? svgIcons.value.filter((icon) => icon.toLowerCase().includes(filterText.value.toLowerCase()))
      : svgIcons.value;
  } else {
    filteredElementIcons.value = filterText.value
      ? elementIcons.value.filter((icon) =>
          icon.toLowerCase().includes(filterText.value.toLowerCase())
        )
      : elementIcons.value;
  }
}

function selectIcon(icon: string) {
  const iconName = activeTab.value === "element" ? "el-icon-" + icon : icon;
  emit("update:modelValue", iconName);
  popoverVisible.value = false;
}

function togglePopover() {
  popoverVisible.value = !popoverVisible.value;
}

onClickOutside(iconSelectRef, () => (popoverVisible.value = false), {
  ignore: [popoverContentRef],
});

/**
 * 清空已选图标
 */
function clearSelectedIcon() {
  selectedIcon.value = "";
}

onMounted(async () => {
  loadIcons();
  if (selectedIcon.value) {
    const raw = selectedIcon.value.trim();
    const epKey = raw.replace(/^el-icon-/i, "");
    if (raw.startsWith("el-icon-")) {
      await loadElementIcons();
      if (elementIcons.value.includes(epKey)) {
        activeTab.value = "element";
      } else {
        activeTab.value = "svg";
      }
    } else if (isIconifyStoredIcon(raw)) {
      activeTab.value = "svg";
    } else {
      activeTab.value = "svg";
    }
  }
});
</script>
