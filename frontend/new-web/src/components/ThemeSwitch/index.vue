<template>
  <ElDropdown trigger="click" @command="handleDarkChange">
    <ElIcon :size="20">
      <component :is="settingsStore.theme === ThemeMode.DARK ? Moon : Sunny" />
    </ElIcon>
    <template #dropdown>
      <ElDropdownMenu>
        <ElDropdownItem
          v-for="item in theneList"
          :key="item.value"
          :command="item.value"
          :disabled="settingsStore.theme === item.value"
        >
          <ElIcon>
            <component :is="item.component" />
          </ElIcon>
          {{ item.label }}
        </ElDropdownItem>
      </ElDropdownMenu>
    </template>
  </ElDropdown>
</template>
<script setup lang="ts">
import { useSettingsStore } from "@/store";
import { ThemeMode } from "@/enums";
import { Moon, Sunny, Monitor } from "@element-plus/icons-vue";

const { t } = useI18n();
const settingsStore = useSettingsStore();

const theneList = [
  { label: t("login.light"), value: ThemeMode.LIGHT, component: Sunny },
  { label: t("login.dark"), value: ThemeMode.DARK, component: Moon },
  { label: t("login.auto"), value: ThemeMode.AUTO, component: Monitor },
];

const handleDarkChange = (theme: ThemeMode) => {
  settingsStore.updateTheme(theme);
};
</script>
