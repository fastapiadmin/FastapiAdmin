<template>
  <ElScrollbar v-if="scrollbar" :max-height="maxHeight" :view-style="{ overflowX: 'hidden' }">
    <FaDescriptionsContent v-bind="contentProps">
      <template v-for="(_, name) in $slots" :key="name" #[name]="slotProps">
        <slot :name="name" v-bind="slotProps" />
      </template>
    </FaDescriptionsContent>
  </ElScrollbar>
  <FaDescriptionsContent v-else v-bind="contentProps">
    <template v-for="(_, name) in $slots" :key="name" #[name]="slotProps">
      <slot :name="name" v-bind="slotProps" />
    </template>
  </FaDescriptionsContent>
</template>

<script lang="ts">
import { h, defineComponent, type PropType, type VNode } from "vue";
import { ElDescriptions, ElDescriptionsItem, ElTag } from "element-plus";

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

const TAG_TYPES: Set<string> = new Set(["primary", "success", "warning", "danger", "info"]);

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

const FaDescriptionsContent = defineComponent({
  name: "FaDescriptionsContent",
  props: {
    bindings: {
      type: Object as PropType<Record<string, unknown>>,
      required: true,
    },
    nsClass: { type: String, default: "" },
    items: {
      type: Array as PropType<DescriptionsItem[]>,
      default: () => [],
    },
    data: {
      type: Object as PropType<Record<string, unknown> | null>,
      default: null,
    },
    span: { type: Number, default: 2 },
  },
  setup(props, { slots }) {
    return () => {
      const slotObj: Record<string, () => VNode[]> = {};

      // Title slot
      const titleSlot = slots.title;
      if (titleSlot) {
        slotObj.title = () => titleSlot();
      }

      // default slot 存在时具名 slot 不会生效（因为父组件完全接管了渲染内容）
      const defaultSlot = slots.default;
      if (defaultSlot) {
        slotObj.default = () => defaultSlot();
      } else {
        const itemNodes: VNode[] = (props.items || []).map((item) => {
          const value = props.data ? getNestedValue(props.data, item.prop) : undefined;

          const itemChildren: (VNode | string)[] = [];

          if (item.slot) {
            const dynamicSlot = slots[item.slot];
            if (dynamicSlot) {
              itemChildren.push(...dynamicSlot({ item, value, row: props.data }));
            }
          } else if (item.tag != null) {
            const tag: boolean | TagConfig = item.tag;
            itemChildren.push(
              h(
                ElTag,
                { type: resolveTagType(value, tag) },
                { default: () => resolveTagText(value, tag) }
              )
            );
          } else {
            const propSlot = slots[item.prop];
            if (propSlot) {
              itemChildren.push(...propSlot({ item, value, row: props.data }));
            } else {
              itemChildren.push(String(value ?? ""));
            }
          }

          return h(
            ElDescriptionsItem,
            {
              label: item.label,
              span: item.span || props.span,
              "label-class-name": item.labelClassName,
              class: item.className,
            },
            { default: () => itemChildren }
          );
        });

        slotObj.default = () => itemNodes;
      }

      return h(ElDescriptions, { ...props.bindings, class: props.nsClass }, slotObj);
    };
  },
});
</script>

<script setup lang="ts">
import { computed, useAttrs } from "vue";
import { useNamespace } from "element-plus/es/hooks/use-namespace/index";

defineOptions({ name: "FaDescriptions" });

defineSlots<{
  default(props: object): any;
  title(props: object): any;
  [slotName: string]: (props: {
    item: DescriptionsItem;
    value: unknown;
    row: Record<string, unknown> | null;
  }) => any;
}>();

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
  size: undefined,
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
  if (props.size !== undefined) bind.size = props.size;
  if (props.labelWidth !== undefined) bind.labelWidth = props.labelWidth;
  return bind;
});

const contentProps = computed(() => ({
  bindings: bindings.value,
  nsClass: ns.b(),
  items: props.items,
  data: props.data,
  span: props.span,
}));
</script>

<style scoped>
:deep(.fa-descriptions) {
  width: 100%;
}
</style>
