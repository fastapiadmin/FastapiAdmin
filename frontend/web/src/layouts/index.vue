<!-- 布局容器 -->
<template>
  <div class="app-layout">
    <aside id="app-sidebar">
      <ArtSidebarMenu />
    </aside>

    <main id="app-main">
      <div id="app-header">
        <ArtHeaderBar />
      </div>
      <div id="app-content">
        <ArtPageContent />
      </div>
    </main>

    <div id="app-global">
      <ArtGlobalComponent />
      <Guide v-if="guideVisible" v-model="guideVisible" @skip="onGuideFinished" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import Guide from "@/components/Guide/index.vue";
import { useAppStore } from "@stores/modules/app.store";
import { useSettingsStore } from "@stores/modules/setting.store";

defineOptions({ name: "AppLayout" });

const appStore = useAppStore();
const settingStore = useSettingsStore();

const guideVisible = computed({
  get: () => appStore.guideVisible,
  set: (v: boolean) => appStore.showGuide(v),
});

function onGuideFinished(): void {
  settingStore.updateSetting("showGuide", false);
}
</script>

<style lang="scss" scoped>
@use "./style";
</style>
