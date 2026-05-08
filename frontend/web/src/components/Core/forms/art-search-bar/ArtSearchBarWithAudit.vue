<!-- 在 ArtSearchBar 上追加「创建人 / 更新人 / 创建时间 / 更新时间」，并内置 UserTableSelect 插槽；业务页只传自己的 items 即可 -->
<template>
  <ArtSearchBar
    ref="innerRef"
    v-model="modelValue"
    v-bind="forwardedAttrs"
    :items="mergedItems"
    @search="(p) => emit('search', p)"
    @reset="emit('reset')"
  >
    <template v-for="(_, name) in $slots" :key="name" #[name]="scope">
      <slot :name="name" v-bind="scope || {}" />
    </template>
    <template v-if="!$slots.created_id" #created_id>
      <div class="w-full min-w-0">
        <UserTableSelect
          :model-value="modelValue?.created_id == null ? undefined : modelValue.created_id"
          @update:model-value="(v) => patchField('created_id', v)"
          @confirm-click="emitImmediateSearch"
          @clear-click="emitImmediateSearch"
        />
      </div>
    </template>
    <template v-if="!$slots.updated_id" #updated_id>
      <div class="w-full min-w-0">
        <UserTableSelect
          :model-value="modelValue?.updated_id == null ? undefined : modelValue.updated_id"
          @update:model-value="(v) => patchField('updated_id', v)"
          @confirm-click="emitImmediateSearch"
          @clear-click="emitImmediateSearch"
        />
      </div>
    </template>
  </ArtSearchBar>
</template>

<script setup lang="ts">
import { computed, ref, useAttrs } from "vue";
import ArtSearchBar from "./index.vue";
import type { SearchFormItem } from "./index.vue";
import {
  getAuditSearchFormItems,
  type GetAuditSearchFormItemsOptions,
} from "./auditSearchFormItems";
import UserTableSelect from "@views/module_system/user/components/UserTableSelect.vue";

defineOptions({ name: "ArtSearchBarWithAudit", inheritAttrs: false });

const props = withDefaults(
  defineProps<{
    /** 仅业务条件表单项，不含审计四字段 */
    items: SearchFormItem[];
    /** 为 false 时与原生 ArtSearchBar 一致，仅使用 `items` */
    includeAudit?: boolean;
    /** 传给 getAuditSearchFormItems 的选项 */
    auditItemOptions?: GetAuditSearchFormItemsOptions;
  }>(),
  { includeAudit: true }
);

const emit = defineEmits<{
  search: [Record<string, any>];
  reset: [];
}>();

const modelValue = defineModel<Record<string, any>>({ default: () => ({}) });
const attrs = useAttrs();

const innerRef = ref<InstanceType<typeof ArtSearchBar> | null>(null);

const forwardedAttrs = computed(() => attrs as Record<string, unknown>);

const auditItems = computed(() => getAuditSearchFormItems(props.auditItemOptions));

const mergedItems = computed(() => {
  if (!props.includeAudit) return props.items;
  return [...props.items, ...auditItems.value];
});

function patchField(key: "created_id" | "updated_id", val: number | undefined) {
  modelValue.value = { ...modelValue.value, [key]: val };
}

function emitImmediateSearch() {
  emit("search", { ...modelValue.value });
}

defineExpose({
  validate: (...args: any[]) => innerRef.value?.validate?.(...args),
  reset: () => innerRef.value?.reset?.(),
  getOutput: () => innerRef.value?.getOutput?.(),
  ref: computed(() => innerRef.value?.ref),
});
</script>
