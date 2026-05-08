<!-- 节日 / 公告顶栏：文案来自 festival 配置（占位符 {{version}}、{{introduceUrl}}） -->
<template>
  <div
    class="overflow-hidden transition-[height] duration-300 ease-in-out"
    :style="{ height: showFestivalStrip ? '48px' : '0' }"
  >
    <ArtTextScroll
      v-if="showFestivalStrip"
      class="!mb-3"
      type="primary"
      :text="festivalScrollDisplayHtml"
      height="40px"
      :speed="55"
      :always-scroll="true"
      show-close
      @close="closeFestivalScroll"
    />
  </div>
</template>

<script setup lang="ts">
import { useSettingsStore } from "@stores/modules/setting.store";
import { useCeremony } from "@/hooks/core/useCeremony";
import { WEB_LINKS } from "@utils/constants";

defineOptions({ name: "ArtFestivalTextScroll" });

const settingStore = useSettingsStore();
const { showFestivalText } = storeToRefs(settingStore);
const { currentFestivalData, closeFestivalScroll } = useCeremony();

function versionLabel(): string {
  const v = String(import.meta.env.VITE_VERSION ?? "").trim();
  if (!v) return "";
  return v.startsWith("v") ? v : `v${v}`;
}

const festivalScrollDisplayHtml = computed(() => {
  const raw = currentFestivalData.value?.scrollText ?? "";
  const ver = versionLabel() || "v0.0.0";
  return raw.replace(/\{\{version\}\}/g, ver).replace(/\{\{introduceUrl\}\}/g, WEB_LINKS.INTRODUCE);
});

const showFestivalStrip = computed(
  () =>
    showFestivalText.value &&
    !!currentFestivalData.value?.scrollText &&
    currentFestivalData.value.scrollText !== ""
);
</script>
