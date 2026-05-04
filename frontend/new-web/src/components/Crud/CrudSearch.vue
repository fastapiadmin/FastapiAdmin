<template>
  <div>
    <!-- 与 examples/forms/search-bar 一致：ArtSearchBar 自带 art-card-xs；与表格区间距由全局 .data-table margin-top 控制 -->
    <div v-if="isArtVariant" v-bind="searchConfig.cardAttrs">
      <ArtSearchBar
        ref="artSearchBarRef"
        v-model="queryParams"
        :items="artSearchItems"
        :span="artSearchSpan"
        :gutter="artSearchGutter"
        :isExpand="artSearchIsExpandComputed"
        :defaultExpanded="searchConfig.searchDefaultExpanded ?? false"
        :showExpand="artSearchShowExpandComputed"
        :labelWidth="artLabelWidth"
        :labelPosition="artLabelPosition"
        :buttonLeftLimit="searchConfig.artSearchButtonLeftLimit"
        :showReset="artShowReset"
        :showSearch="artShowSearch"
        :disabledSearch="searchConfig.artSearchDisabledSearch ?? false"
        :sanitizeOutput="searchConfig.artSearchSanitizeOutput"
        :rules="mergedArtFormRules"
        @search="handleArtSearch"
        @reset="handleArtReset"
      >
        <template v-for="name in artSlotNames" :key="name" #[name]="slotProps">
          <slot :name="name" v-bind="slotProps || {}" />
        </template>
      </ArtSearchBar>

      <div v-if="searchConfig.customButtons?.length" class="flex flex-wrap items-center gap-2 mt-3">
        <template v-for="button in searchConfig.customButtons" :key="button.key">
          <el-button
            v-if="!button.perm || hasPermission(button.perm)"
            v-bind="button.attrs"
            @click="handleCustomButtonClick(button)"
          >
            {{ button.text }}
          </el-button>
        </template>
      </div>
    </div>

    <el-card v-else v-bind="cardAttrs">
      <!-- 搜索表单区域 -->
      <el-form
        :key="'page-search-expand-' + isExpand"
        ref="queryFormRef"
        label-suffix=":"
        v-bind="formAttrs"
        :model="queryParams"
        :class="isGrid"
        @submit.prevent="handleQuery"
      >
        <template v-for="(item, index) in formItems" :key="item.prop">
          <el-form-item
            v-show="isExpand ? true : index < showNumber"
            :label="item?.label"
            :prop="item.prop"
          >
            <!-- Label -->
            <template #label>
              <span class="flex-y-center">
                {{ item?.label || "" }}
                <el-tooltip v-if="item?.tips" v-bind="getTooltipProps(item.tips)">
                  <QuestionFilled class="w-4 h-4 mx-1" />
                </el-tooltip>
                <span v-if="searchConfig.colon" class="ml-0.5">:</span>
              </span>
            </template>

            <ElCascader
              v-if="item.type === 'cascader'"
              v-model="queryParams[item.prop]"
              v-bind="{ style: { width: '100%' }, ...item.attrs }"
              v-on="item.events || {}"
            />
            <component
              :is="getCustomComponent(item.type) || componentMap.get(item.type)"
              v-else
              v-model="queryParams[item.prop]"
              v-bind="{ style: { width: '100%' }, ...item.attrs }"
              v-on="item.events || {}"
            >
              <template v-if="item.type === 'select'">
                <template v-for="opt in item.options" :key="opt.value">
                  <el-option :label="opt.label" :value="opt.value" />
                </template>
              </template>
              <!-- 自定义组件的插槽支持 -->
              <template v-if="getCustomComponent(item.type) && item.slotName">
                <template v-for="slot in Object.keys($slots)" :key="slot">
                  <slot :name="slot"></slot>
                </template>
              </template>
            </component>
          </el-form-item>
        </template>

        <el-form-item :class="{ 'col-[auto/-1] justify-self-end': searchConfig?.grid === 'right' }">
          <!-- 自定义按钮组 -->
          <template v-if="searchConfig?.customButtons && searchConfig.customButtons.length > 0">
            <template v-for="button in searchConfig.customButtons" :key="button.key">
              <el-button
                v-if="!button.perm || hasPermission(button.perm)"
                v-bind="button.attrs"
                @click="handleCustomButtonClick(button)"
              >
                {{ button.text }}
              </el-button>
            </template>
          </template>

          <!-- 默认搜索/重置按钮 -->
          <template v-else>
            <!-- 搜索按钮 -->
            <el-button
              v-if="
                !searchConfig?.showSearchButton ||
                hasPermission(searchConfig.searchButtonPerm || [])
              "
              icon="search"
              type="primary"
              @click="handleQuery"
            >
              搜索
            </el-button>
            <!-- 重置按钮 -->
            <el-button
              v-if="
                !searchConfig?.showResetButton || hasPermission(searchConfig.resetButtonPerm || [])
              "
              icon="refresh"
              @click="handleReset"
            >
              重置
            </el-button>
          </template>

          <!-- 展开/收起 -->
          <template v-if="isExpandable && formItems.length > showNumber">
            <el-link class="ml-3" type="primary" underline="never" @click="isExpand = !isExpand">
              {{ isExpand ? "收起" : "展开" }}
              <component :is="isExpand ? ArrowUp : ArrowDown" class="w-4 h-4 ml-2" />
            </el-link>
          </template>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import type { IObject, IForm, ISearchConfig, ISearchComponent } from "./types";
import { ArrowUp, ArrowDown, QuestionFilled } from "@element-plus/icons-vue";
import type { FormInstance, FormRules } from "element-plus";
import InputTag from "@/components/InputTag/index.vue";
import ArtSearchBar from "@/components/Core/forms/art-search-bar/index.vue";
import { createCrudSearchInitialParams, mapCrudSearchFormItemsToArt } from "./crudSearchFormToArt";
import { getCurrentInstance, nextTick, useSlots, watch } from "vue";
import {
  ElInput,
  ElSelect,
  ElCascader,
  ElInputNumber,
  ElDatePicker,
  ElTimePicker,
  ElTimeSelect,
  ElTreeSelect,
  ElInputTag,
  ElRadioGroup,
  ElCheckboxGroup,
  ElSwitch,
  ElRate,
  ElSlider,
} from "element-plus";

// 定义接收的属性
const props = defineProps<{ searchConfig: ISearchConfig }>();
// 自定义事件
const emit = defineEmits<{
  queryClick: [queryParams: IObject];
  resetClick: [queryParams: IObject];
  dateRangeChange: [prop: string, range: [Date, Date] | [string, string] | [null, null]];
  customButtonClick: [buttonKey: string, queryParams: IObject];
}>();

// 时间范围处理相关
const dateRangeRefs = ref<Record<string, any>>({});

// 组件映射表
const componentMap = new Map<ISearchComponent, any>([
  // @ts-ignore
  ["input", markRaw(ElInput)], // @ts-ignore
  ["select", markRaw(ElSelect)], // @ts-ignore
  ["cascader", markRaw(ElCascader)], // @ts-ignore
  ["input-number", markRaw(ElInputNumber)], // @ts-ignore
  ["date-picker", markRaw(ElDatePicker)], // @ts-ignore
  ["time-picker", markRaw(ElTimePicker)], // @ts-ignore
  ["time-select", markRaw(ElTimeSelect)], // @ts-ignore
  ["tree-select", markRaw(ElTreeSelect)], // @ts-ignore
  ["input-tag", markRaw(ElInputTag)], // @ts-ignore
  ["custom-tag", markRaw(InputTag)], // @ts-ignore
  ["radio", markRaw(ElRadioGroup)], // @ts-ignore
  ["checkbox", markRaw(ElCheckboxGroup)], // @ts-ignore
  ["switch", markRaw(ElSwitch)], // @ts-ignore
  ["rate", markRaw(ElRate)], // @ts-ignore
  ["slider", markRaw(ElSlider)], // @ts-ignore
]);

// 自定义组件映射（从 searchConfig 中获取）
const getCustomComponent = (componentName: string) => {
  return props.searchConfig?.customComponents?.[componentName] || null;
};

// 权限控制检查（供下方 computed 使用）
const hasPermission = (perm: string | string[]): boolean => {
  if (!perm || !props.searchConfig?.permPrefix) return true;
  return true;
};

// 存储表单实例
const queryFormRef = ref<FormInstance>();
const artSearchBarRef = ref<InstanceType<typeof ArtSearchBar>>();
const slots = useSlots();
const artSlotNames = computed(() => Object.keys(slots));

// 响应式的 formItems
const formItems = reactive(props.searchConfig?.formItems ?? []);

// 存储查询参数（先于子组件挂载赋值，保证 ArtSearchBar 初始快照与 legacy 一致）
const queryParams = reactive<IObject>(createCrudSearchInitialParams(formItems, getCustomComponent));

const isArtVariant = computed(() => props.searchConfig.searchVariant === "art");

/** 与 Art 示例一致：控件不宜铺满整列；`false` 表示不限制（见 types） */
const artFieldMaxWidthComputed = computed(() => {
  const w = props.searchConfig.artSearchFieldMaxWidth;
  if (w === false) return undefined;
  if (w !== undefined && w !== "") return w;
  return "min(100%, 280px)";
});

const artSearchItems = computed(() =>
  mapCrudSearchFormItemsToArt(formItems, {
    customComponents: props.searchConfig.customComponents,
    fieldMaxWidth: artFieldMaxWidthComputed.value,
  })
);

const artSearchSpan = computed(() => props.searchConfig.artSearchSpan ?? 6);
const artSearchGutter = computed(() => props.searchConfig.artSearchGutter ?? 12);

/** 与 types 注释一致：`isExpandable === false` 时等价于始终展开全部筛选项 */
const artSearchIsExpandComputed = computed(
  () => props.searchConfig.artSearchIsExpand ?? props.searchConfig.isExpandable === false
);

const artSearchShowExpandComputed = computed(
  () => props.searchConfig.artSearchShowExpand ?? props.searchConfig.isExpandable !== false
);

const artLabelWidth = computed(() => props.searchConfig.form?.labelWidth ?? "70px");
const artLabelPosition = computed(
  () => (props.searchConfig.form?.labelPosition ?? "right") as "left" | "right" | "top"
);

const artShowSearch = computed(
  () =>
    !props.searchConfig.showSearchButton || hasPermission(props.searchConfig.searchButtonPerm || [])
);

const artShowReset = computed(
  () =>
    !props.searchConfig.showResetButton || hasPermission(props.searchConfig.resetButtonPerm || [])
);

const mergedArtFormRules = computed<FormRules>(() => {
  const base = props.searchConfig.artSearchRules ?? {};
  const fromItems: FormRules = {};
  for (const item of formItems) {
    if (item.rules) {
      fromItems[item.prop] = item.rules;
    }
  }
  return { ...base, ...fromItems };
});

const handleArtSearch = () => {
  emit("queryClick", buildQueryPayload());
};

const handleArtReset = () => {
  emit("resetClick", buildQueryPayload());
};
// 是否可展开/收缩
const isExpandable = ref(props.searchConfig?.isExpandable ?? true);
// 是否已展开
const isExpand = ref(false);
// 表单项展示数量，若可展开，超出展示数量的表单项隐藏
const showNumber = computed(() =>
  isExpandable.value ? (props.searchConfig?.showNumber ?? 3) : formItems.length
);
// 卡片组件自定义属性（阴影、自定义边距样式等）
const cardAttrs = computed<IObject>(() => {
  return {
    /** 与 ArtSearchBar `art-card-xs`、examples/forms/search-bar 同一套卡片质感 */
    class: "search-container art-card-xs",
    shadow: "never",
    style: { marginBottom: "0" },
    ...props.searchConfig?.cardAttrs,
  };
});
// 表单组件自定义属性（label位置、宽度、对齐方式等）
const formAttrs = computed<IForm>(() => {
  const custom = props.searchConfig?.form ?? {};
  if (props.searchConfig?.grid) {
    return { ...custom, inline: false };
  }
  return { inline: true, ...custom };
});
/** 默认 flex（scoped）；grid 时见 .crud-page-search--grid */
const isGrid = computed(() =>
  props.searchConfig?.grid ? "crud-page-search--grid" : "crud-page-search--flex"
);

/** 展开/收起后：表单已随 :key 重建，再触发 resize 让日期范围等组件量宽 */
watch(isExpand, () => {
  nextTick(() => {
    window.dispatchEvent(new Event("resize"));
  });
});

// 获取tooltip提示框属性
const getTooltipProps = (tips: string | IObject) => {
  return typeof tips === "string" ? { content: tips } : tips;
};

/** 查询前对 input 做 trim；去掉空条件，避免 GET 出现 name=&created_id= 等导致后端 Optional[int] 解析失败 */
function buildQueryPayload() {
  const q = { ...queryParams };
  for (const item of formItems) {
    if (item.type === "input" && typeof q[item.prop] === "string") {
      q[item.prop] = q[item.prop].trim();
    }
  }
  const out: IObject = {};
  for (const key of Object.keys(q)) {
    const v = q[key];
    if (v === "" || v === null || v === undefined) continue;
    if (Array.isArray(v) && v.length === 0) continue;
    out[key] = v;
  }
  return out;
}

// 查询/重置操作
const handleQuery = () => emit("queryClick", buildQueryPayload());
const handleReset = () => {
  queryFormRef.value?.resetFields();
  // 重置所有时间范围组件
  Object.values(dateRangeRefs.value).forEach((ref) => {
    if (ref && typeof ref.reset === "function") {
      ref.reset();
    }
  });
  emit("resetClick", buildQueryPayload());
};

// 处理自定义按钮点击
const handleCustomButtonClick = (button: any) => {
  // 如果配置了自定义处理器，优先使用
  if (button.handler && typeof button.handler === "function") {
    button.handler(queryParams, getCurrentInstance());
  }
  // 触发自定义事件
  emit("customButtonClick", button.key, queryParams);
};

onMounted(() => {
  formItems.forEach((item) => {
    if (item?.initFn) {
      item.initFn(item);
    }
  });
});
// 暴露的属性和方法
defineExpose({
  // 获取分页数据（与「搜索」提交时一致，含 input trim）
  getQueryParams: () => buildQueryPayload(),
  /** art 形态下 ArtSearchBar 实例（校验、getOutput 等） */
  artSearchBarRef,
});
</script>

<style lang="scss" scoped>
:deep(.el-input-number .el-input__inner) {
  text-align: left;
}

.el-form-item {
  margin-right: 0;
  margin-bottom: 0;
}

/* 卡片参与 flex 布局链时允许高度随内容收回，避免展开后再收起仍「撑住」 */
.search-container :deep(.el-card__body) {
  min-height: 0;
}

/* 默认行内搜索：明确左起排布，避免展开宽表单项后 flex 残留 justify/end 对齐 */
.crud-page-search--flex {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  place-content: flex-start flex-start;
  align-items: center;
  width: 100%;
  min-height: 0;
}

.crud-page-search--grid {
  display: grid !important;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1rem;
  align-items: center;
  width: 100%;
}
</style>
