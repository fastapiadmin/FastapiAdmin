<script lang="ts" setup>
const { toastOptions, currentPage } = storeToRefs(useGlobalToast())

const { close: closeGlobalToast } = useGlobalToast()

const toast = useToast('globalToast')
const currentPath = getCurrentPath()

// #ifdef MP-ALIPAY
const hackAlipayVisible = ref(false)

nextTick(() => {
  hackAlipayVisible.value = true
})
// #endif

watch(() => toastOptions.value, (newVal) => {
  if (newVal && newVal.show) {
    if (currentPage.value === currentPath) {
      toast.show(toastOptions.value)
    }
  }
  else {
    toast.close()
  }
})
</script>

<script lang="ts">
export default {
  options: {
    virtualHost: true,
    addGlobalClass: true,
    styleIsolation: 'shared',
  },
}
</script>

<template>
  <!-- #ifdef MP-ALIPAY -->
  <wd-toast v-if="hackAlipayVisible" selector="globalToast" :closed="closeGlobalToast" />
  <!-- #endif -->
  <!-- #ifndef MP-ALIPAY -->
  <wd-toast selector="globalToast" :closed="closeGlobalToast" />
  <!-- #endif -->
</template>
