<!-- 语言切换 -->
<template>
  <ElDropdown trigger="click" @command="handleLanguageChange">
    <div class="navbar-lang-trigger flex-cc">
      <ArtSvgIcon :icon="resolveIconForArtSvgIcon('language')" :class="size" />
    </div>
    <template #dropdown>
      <ElDropdownMenu>
        <ElDropdownItem
          v-for="item in langOptions"
          :key="item.value"
          :disabled="appStore.language === item.value"
          :command="item.value"
        >
          {{ item.label }}
        </ElDropdownItem>
      </ElDropdownMenu>
    </template>
  </ElDropdown>
</template>

<script setup lang="ts">
import ArtSvgIcon from "@/components/Core/base/art-svg-icon/index.vue";
import { useAppStore } from "@stores/modules/app.store";
import { LanguageEnum } from "@/enums/settings/locale.enum";
import { resolveIconForArtSvgIcon } from "@utils/menuIcon/remix";

defineProps({
  size: {
    type: String,
    required: false,
  },
});

const langOptions = [
  { label: "中文", value: LanguageEnum.ZH_CN },
  { label: "English", value: LanguageEnum.EN },
];

const appStore = useAppStore();
const { locale, t } = useI18n();

/**
 * 处理语言切换
 *
 * @param lang  语言（zh-cn、en）
 */
function handleLanguageChange(lang: string) {
  locale.value = lang;
  appStore.changeLanguage(lang);

  ElMessage.success(t("langSelect.message.success"));
}
</script>
