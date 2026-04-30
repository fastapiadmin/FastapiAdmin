<script setup lang="ts">
onLaunch((options) => {
  console.log('App.vue onLaunch', options)
})

onShow((options) => {
  console.log('App.vue onShow', options)
})

onHide(() => {
  console.log('App Hide')
})
</script>

<style lang="scss">
.page-wraper {
  min-height: calc(100vh - var(--window-top));
  box-sizing: border-box;
  background: #f9f9f9;
}

.wot-theme-dark.page-wraper {
  background: #222;
}
</style>
