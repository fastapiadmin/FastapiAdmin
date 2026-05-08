<template>
  <div v-if="width > 1000">
    <SectionTitle :title="$t('setting.menuType.title')" />
    <div class="setting-box-wrap">
      <div
        class="setting-item"
        v-for="(item, index) in configOptions.menuLayoutList"
        :key="item.value"
        @click="switchMenuLayouts(item.value)"
      >
        <div class="box" :class="{ 'is-active': item.value === menuType, 'mt-16': index > 2 }">
          <img :src="item.img" />
        </div>
        <p class="name">{{ $t(`setting.menuType.list[${index}]`) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import SectionTitle from "./SectionTitle.vue";
import { useSettingsStore } from "@stores/modules/setting.store";
import { useSettingsConfig } from "../composables/useSettingsConfig";
import { useSettingsState } from "../composables/useSettingsState";

const { width } = useWindowSize();
const settingStore = useSettingsStore();
const { menuType } = storeToRefs(settingStore);
const { configOptions } = useSettingsConfig();
const { switchMenuLayouts } = useSettingsState();
</script>
