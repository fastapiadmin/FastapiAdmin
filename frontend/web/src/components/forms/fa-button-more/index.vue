<!-- 更多按钮 -->
<template>
  <div>
    <ElDropdown v-if="visibleItems.length">
      <FaIconButton icon="ri:more-2-fill" class="size-8! bg-g-200 dark:bg-g-300/45 text-sm" />
      <template #dropdown>
        <ElDropdownMenu>
          <ElDropdownItem
            v-for="item in visibleItems"
            :key="item.key"
            :disabled="item.disabled"
            @click="handleClick(item)"
          >
            <div class="flex items-center gap-2" :style="{ color: item.color }">
              <FaSvgIcon v-if="item.icon" :icon="item.icon" />
              <span>{{ item.label }}</span>
            </div>
          </ElDropdownItem>
        </ElDropdownMenu>
      </template>
    </ElDropdown>
  </div>
</template>

<script setup lang="ts">
import { checkPerm } from "@/utils/checkPerm";
import type { ButtonMoreItem } from "./types";

defineOptions({ name: "FaButtonMore" });

interface Props {
  /** 下拉项列表 */
  list: ButtonMoreItem[];
}

const props = withDefaults(defineProps<Props>(), {});

const visibleItems = computed(() => props.list.filter((item) => checkPerm(item.auth)));

interface Emits {
  click: [item: ButtonMoreItem];
}

const emit = defineEmits<Emits>();

const handleClick = (item: ButtonMoreItem) => {
  emit("click", item);
};
</script>
