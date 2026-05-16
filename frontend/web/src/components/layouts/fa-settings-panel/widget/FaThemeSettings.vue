<template>
  <FaSectionTitle :title="$t('setting.theme.title')" />
  <div class="setting-box-wrap">
    <div
      class="setting-item"
      v-for="(item, index) in configOptions.themeList"
      :key="item.theme"
      @click="switchThemeStyles(item.theme)"
    >
      <div class="box" :class="{ 'is-active': item.theme === systemThemeMode }">
        <img :src="item.img" loading="eager" />
      </div>
      <p class="name">{{ $t(`setting.theme.list[${index}]`) }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSettingsStore } from "@stores";
import { useSettingsConfig } from "../composables/useSettingsConfig";
import { useTheme } from "@/hooks/core/useTheme";

const settingStore = useSettingsStore();
const { systemThemeMode } = storeToRefs(settingStore);
const { configOptions } = useSettingsConfig();
const { switchThemeStyles } = useTheme();
</script>
