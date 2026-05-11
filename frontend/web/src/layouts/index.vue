<!-- 布局容器 -->
<template>
  <div class="app-layout">
    <aside id="app-sidebar">
      <FaSidebarMenu />
    </aside>

    <main id="app-main">
      <div id="app-header">
        <FaHeaderBar />
      </div>
      <div id="app-content">
        <FaPageContent />
      </div>
    </main>

    <div id="app-global">
      <FaGlobalComponent />
      <Guide v-if="guideVisible" v-model="guideVisible" @skip="onGuideFinished" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import Guide from "@/components/others/fa-guide/index.vue";
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
