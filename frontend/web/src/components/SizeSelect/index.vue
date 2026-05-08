<!-- 布局大小（触发器与顶栏 ArtIconButton 一致，避免与其它图标尺寸/悬停不一致） -->
<template>
  <ElTooltip :content="t('sizeSelect.tooltip')" effect="dark" placement="bottom">
    <ElDropdown trigger="click" @command="handleSizeChange">
      <span class="inline-flex outline-none leading-none">
        <ArtIconButton
          :icon="resolveIconForArtSvgIcon('size')"
          class="size-select-btn text-[19px]"
        />
      </span>
      <template #dropdown>
        <ElDropdownMenu>
          <ElDropdownItem
            v-for="item of sizeOptions"
            :key="item.value"
            :disabled="appStore.size == item.value"
            :command="item.value"
          >
            {{ item.label }}
          </ElDropdownItem>
        </ElDropdownMenu>
      </template>
    </ElDropdown>
  </ElTooltip>
</template>

<script setup lang="ts">
import ArtIconButton from "@/components/Core/widget/art-icon-button/index.vue";
import { ComponentSize } from "@/enums/settings/layout.enum";
import { useAppStore } from "@stores/modules/app.store";
import { resolveIconForArtSvgIcon } from "@utils/menuIcon/remix";
import { computed } from "vue";

const { t } = useI18n();
const sizeOptions = computed(() => {
  return [
    { label: t("sizeSelect.default"), value: ComponentSize.DEFAULT },
    { label: t("sizeSelect.large"), value: ComponentSize.LARGE },
    { label: t("sizeSelect.small"), value: ComponentSize.SMALL },
  ];
});

const appStore = useAppStore();
function handleSizeChange(size: string) {
  appStore.changeSize(size);
  ElMessage.success(t("sizeSelect.message.success"));
}
</script>
