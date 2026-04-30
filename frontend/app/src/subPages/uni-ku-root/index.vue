<script setup lang="ts">
definePage({
  name: 'root',
  style: {
    navigationBarTitleText: 'uni-ku/root',
  },
})

const show = ref<boolean>(false)
</script>

<template>
  <page-meta :page-style="`overflow:${show ? 'hidden' : 'visible'};`" />
  <view class="min-h-200vh">
    <demo-block title="锁定滚动" transparent>
      <wd-cell-group border>
        <wd-cell title="锁定滚动" is-link @click="show = !show" />
      </wd-cell-group>
    </demo-block>

    <wd-popup
      v-model="show"
      lock-scroll
      position="bottom"
      closable
      :safe-area-inset-bottom="true"
      custom-style="height: 200px;"
      @close="show = false"
    />
  </view>
</template>
