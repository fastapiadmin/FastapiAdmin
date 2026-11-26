<script lang="ts" setup>
import { useI18n } from 'vue-i18n'

const router = useRouter()

const route = useRoute()

const { t } = useI18n()

const { activeTabbar, getTabbarItemValue, setTabbarItemActive, tabbarList } = useTabbar()

const { enabled: watermarkEnabled, content: watermarkContent, color: watermarkColor } = useWatermark()

function handleTabbarChange({ value }: { value: string }) {
  setTabbarItemActive(value)
  router.pushTab({ name: value })
}

onMounted(() => {
  // #ifdef APP
  uni.hideTabBar()
  // #endif
  nextTick(() => {
    if (route.name && route.name !== activeTabbar.value.name) {
      setTabbarItemActive(route.name)
    }
  })
})
</script>

<script lang="ts">
export default {
  options: {
    addGlobalClass: true,
    virtualHost: true,
    styleIsolation: 'shared',
  },
}
</script>

<template>
  <slot />
  <wd-gap
    safe-area-bottom
    height="calc(var(--wot-tabbar-height, 50px) + env(safe-area-inset-bottom))"
    custom-class="tabbar-gap"
  />
  <wd-tabbar
    :model-value="activeTabbar.name" bordered safe-area-inset-bottom fixed
    custom-style="background: var(--wot-tabbar-bg, #FFFFFF);"
    @change="handleTabbarChange"
  >
    <wd-tabbar-item
      v-for="(item, index) in tabbarList" :key="index" :name="item.name"
      :value="getTabbarItemValue(item.name)" :title="t(item.titleKey)" :icon="item.icon"
    />
  </wd-tabbar>
  <wd-watermark
    v-if="watermarkEnabled"
    :content="watermarkContent"
    :color="watermarkColor"
    :width="130"
    :height="140"
    :opacity="0.08"
    layout="grid"
  />
</template>
