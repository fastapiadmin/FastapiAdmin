<template>
  <ElScrollbar v-if="scrollbar" :max-height="maxHeight" :view-style="{ overflowX: 'hidden' }">
    <ElDescriptions v-bind="bindings" :class="ns.b()">
      <template v-if="$slots.title" #title>
        <slot name="title" />
      </template>
      <template v-if="!$slots.default">
        <ElDescriptionsItem
          v-for="item in items"
          :key="item.prop"
          :label="item.label"
          :span="item.span || span"
          :label-class-name="item.labelClassName"
          :class-name="item.className"
        >
          <!-- 带 slot 名称的项：通过具名插槽自定义 -->
          <slot
            v-if="item.slot"
            :name="item.slot"
            :item="item"
            :value="data ? getNestedValue(data, item.prop) : undefined"
            :row="data"
          />
          <!-- Tag 模式 -->
          <template v-else-if="item.tag">
            <ElTag
              v-if="item.tag === true && data && data[item.prop] !== undefined"
              :type="resolveTagType(getNestedValue(data, item.prop))"
            >
              {{ getNestedValue(data, item.prop) }}
            </ElTag>
            <ElTag
              v-else-if="typeof item.tag === 'object' && data"
              :type="resolveTagType(getNestedValue(data, item.prop), item.tag.type)"
            >
              {{ resolveTagText(getNestedValue(data, item.prop), item.tag) }}
            </ElTag>
          </template>
          <!-- 纯文本模式 -->
          <template v-else>
            <slot
              :name="item.prop"
              :item="item"
              :value="data ? getNestedValue(data, item.prop) : undefined"
              :row="data"
            >
              {{ data ? getNestedValue(data, item.prop) : "" }}
            </slot>
          </template>
        </ElDescriptionsItem>
      </template>
      <!-- 完全自定义模式 -->
      <template v-else>
        <slot />
      </template>
    </ElDescriptions>
  </ElScrollbar>
  <!-- 不使用滚动条时直接渲染 -->
  <ElDescriptions v-else v-bind="bindings" :class="ns.b()">
    <template v-if="$slots.title" #title>
      <slot name="title" />
    </template>
    <template v-if="!$slots.default">
      <ElDescriptionsItem
        v-for="item in items"
        :key="item.prop"
        :label="item.label"
        :span="item.span || span"
        :label-class-name="item.labelClassName"
        :class-name="item.className"
      >
        <slot
          v-if="item.slot"
          :name="item.slot"
          :item="item"
          :value="data ? getNestedValue(data, item.prop) : undefined"
          :row="data"
        />
        <template v-else-if="item.tag">
          <ElTag
            v-if="item.tag === true && data && data[item.prop] !== undefined"
            :type="resolveTagType(getNestedValue(data, item.prop))"
          >
            {{ getNestedValue(data, item.prop) }}
          </ElTag>
          <ElTag
            v-else-if="typeof item.tag === 'object' && data"
            :type="resolveTagType(getNestedValue(data, item.prop), item.tag.type)"
          >
            {{ resolveTagText(getNestedValue(data, item.prop), item.tag) }}
          </ElTag>
        </template>
        <template v-else>
          <slot
            :name="item.prop"
            :item="item"
            :value="data ? getNestedValue(data, item.prop) : undefined"
            :row="data"
          >
            {{ data ? getNestedValue(data, item.prop) : "" }}
          </slot>
        </template>
      </ElDescriptionsItem>
    </template>
    <template v-else>
      <slot />
    </template>
  </ElDescriptions>
</template>

<script setup lang="ts">
defineOptions({ name: "FaDescriptions" });

import { computed, useAttrs } from "vue";
import { useNamespace } from "element-plus";
// ── 组件类型定义（内联，避免跨文件引用导致 TS Server 延迟）──
/** ElTag 可接受的 type 值 */
export type TagType = "primary" | "success" | "warning" | "danger" | "info";

/** Tag 渲染配置 */
export interface TagConfig {
  /**
   * Tag 映射表：key 为数据值，value 为 { type: ElTag类型, text: 显示文本 }
   * 例：{ '0': { type: 'success', text: '启用' }, '1': { type: 'danger', text: '停用' } }
   */
  map?: Record<string, { type?: TagType; text?: string }>;
  /** 默认 type，当 map 未匹配到时使用 */
  type?: TagType;
}

/** 单个描述项配置 */
export interface DescriptionsItem {
  /** 标签文本 */
  label: string;
  /** 对应 data 中的属性名，支持 'a.b.c' 嵌套路径 */
  prop: string;
  /** 列跨度，不传则使用组件级 span 默认值 */
  span?: number;
  /**
   * 渲染模式:
   * - 不设置：纯文本
   * - true：作为 ElTag 渲染，文本为 data[prop]
   * - TagConfig 对象：通过 map 映射类型和文本
   */
  tag?: boolean | TagConfig;
  /** 自定义插槽名称，设置后该 item 将通过具名插槽渲染 */
  slot?: string;
  /** 传递给 el-descriptions-item 的 label-class-name */
  labelClassName?: string;
  /** 传递给 el-descriptions-item 的 class-name */
  className?: string;
}

const attrs = useAttrs();
const ns = useNamespace("descriptions");

const props = withDefaults(
  defineProps<{
    /** 每行显示的描述项数量，默认 4 */
    column?: number;
    /** 是否展示边框，默认 true */
    border?: boolean;
    /** 列表尺寸，默认 'default' */
    size?: "default" | "small";
    /** 标签宽度 */
    labelWidth?: string;
    /** 描述项配置列表 */
    items?: DescriptionsItem[];
    /** 数据对象，items 模式下自动取 data[item.prop] 渲染 */
    data?: Record<string, unknown> | null;
    /** 默认 span，当 item 未指定 span 时生效，默认 2 */
    span?: number;
    /** 是否需要内置 ElScrollbar 包裹，默认 true */
    scrollbar?: boolean;
    /** ElScrollbar 最大高度，默认 '70vh' */
    maxHeight?: string;
  }>(),
  {
    column: 4,
    border: true,
    size: "default",
    labelWidth: undefined,
    items: () => [],
    data: null,
    span: 2,
    scrollbar: true,
    maxHeight: "70vh",
  }
);

// 传递给 ElDescriptions 的绑定属性
const bindings = computed(() => {
  const bind: Record<string, unknown> = {
    column: props.column,
    border: props.border,
    ...attrs, // 透传 class、style 等属性
  };
  if (props.size !== "default") bind.size = props.size;
  if (props.labelWidth !== undefined) bind.labelWidth = props.labelWidth;
  return bind;
});

/** 获取嵌套属性值，支持 'a.b.c' 路径 */
function getNestedValue(obj: Record<string, unknown> | null, path: string): unknown {
  if (!obj) return undefined;
  return path.split(".").reduce((acc, key) => {
    if (acc && typeof acc === "object" && key in acc) {
      return (acc as Record<string, unknown>)[key];
    }
    return undefined;
  }, obj as unknown);
}

/** 解析 ElTag 的 type 属性，确保返回 ElTag 可接受的有效类型值 */
function resolveTagType(_value: unknown, fallback?: string): TagType {
  // 优先级 1: fallback 本身就是合法 TagType → 直接使用
  if (fallback && isValidTagType(fallback)) return fallback;
  // 优先级 2: 无有效 fallback 时，用 'info' 作为兜底
  return "info";
}

const TAG_TYPES: Set<string> = new Set(["primary", "success", "warning", "danger", "info"]);
function isValidTagType(v: string): v is TagType {
  return TAG_TYPES.has(v);
}

/** 解析 ElTag 显示的文本，支持 tagMap 映射 */
function resolveTagText(value: unknown, tag: TagConfig): string {
  const raw = value == null ? "" : String(value);
  if (tag.map && raw in tag.map) {
    return tag.map[raw].text ?? raw;
  }
  return raw;
}
</script>

<style scoped>
/*
 * fa-descriptions 在 ElScrollbar 内部包裹时，
 * 需要占满宽度，避免 ElDescriptions 边框被截断。
 */
:deep(.fa-descriptions) {
  width: 100%;
}
</style>
