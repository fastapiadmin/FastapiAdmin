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
          <slot
            v-if="item.slot"
            :name="item.slot"
            :item="item"
            :value="data ? getNestedValue(data, item.prop) : undefined"
            :row="data"
          />
          <ElTag
            v-else-if="item.tag != null"
            :type="resolveTagType(getNestedValue(data, item.prop), item.tag)"
          >
            {{ resolveTagText(getNestedValue(data, item.prop), item.tag) }}
          </ElTag>
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
  </ElScrollbar>
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
        <ElTag
          v-else-if="item.tag != null"
          :type="resolveTagType(getNestedValue(data, item.prop), item.tag)"
        >
          {{ resolveTagText(getNestedValue(data, item.prop), item.tag) }}
        </ElTag>
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

export type TagType = "primary" | "success" | "warning" | "danger" | "info";

export interface TagConfig {
  map?: Record<string, { type?: TagType; text?: string }>;
  type?: TagType;
}

export interface DescriptionsItem {
  label: string;
  prop: string;
  span?: number;
  tag?: boolean | TagConfig;
  slot?: string;
  labelClassName?: string;
  className?: string;
}

const attrs = useAttrs();
const ns = useNamespace("descriptions");

interface Props {
  column?: number;
  border?: boolean;
  size?: "default" | "small";
  labelWidth?: string;
  items?: DescriptionsItem[];
  data?: Record<string, unknown> | null;
  span?: number;
  scrollbar?: boolean;
  maxHeight?: string;
}

const props = withDefaults(defineProps<Props>(), {
  column: 4,
  border: true,
  size: "default",
  labelWidth: undefined,
  items: () => [],
  data: null,
  span: 2,
  scrollbar: true,
  maxHeight: "70vh",
});

const bindings = computed(() => {
  const bind: Record<string, unknown> = {
    column: props.column,
    border: props.border,
    ...attrs,
  };
  if (props.size !== "default") bind.size = props.size;
  if (props.labelWidth !== undefined) bind.labelWidth = props.labelWidth;
  return bind;
});

function getNestedValue(obj: Record<string, unknown> | null, path: string): unknown {
  if (!obj) return undefined;
  return path.split(".").reduce((acc, key) => {
    if (acc && typeof acc === "object" && key in acc) {
      return (acc as Record<string, unknown>)[key];
    }
    return undefined;
  }, obj as unknown);
}

function resolveTagType(value: unknown, tag: boolean | TagConfig): TagType {
  if (typeof tag === "boolean") {
    return tag ? "success" : "danger";
  }
  if (tag.map) {
    const raw = value == null ? "" : String(value);
    if (raw in tag.map) {
      const t = tag.map[raw]!.type;
      if (t && TAG_TYPES.has(t)) return t;
    }
  }
  if (tag.type && TAG_TYPES.has(tag.type)) return tag.type;
  return "info";
}

const TAG_TYPES: Set<string> = new Set(["primary", "success", "warning", "danger", "info"]);

function resolveTagText(value: unknown, tag: boolean | TagConfig): string {
  const raw = value == null ? "" : String(value);
  if (typeof tag === "boolean") {
    return raw;
  }
  if (tag.map && raw in tag.map) {
    return tag.map[raw]!.text ?? raw;
  }
  return raw;
}
</script>

<style scoped>
:deep(.fa-descriptions) {
  width: 100%;
}
</style>
