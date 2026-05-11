<!-- 登录区底部：灰色提示 + 主题链（注册 / 返回登录等） -->
<template>
  <div
    class="login-auth-link-row mt-6 flex flex-wrap items-center justify-center gap-1 text-sm leading-normal"
  >
    <span class="inline-flex items-center text-[var(--el-text-color-secondary)]">{{ hint }}</span>
    <ElLink
      type="primary"
      :underline="false"
      class="inline-flex items-center font-medium !leading-[inherit]"
      @click="$emit('link')"
    >
      {{ linkText }}
    </ElLink>
  </div>
</template>

<script setup lang="ts">
defineProps<{ hint: string; linkText: string }>();
defineEmits<{ link: [] }>();
</script>

<style scoped lang="scss">
.login-auth-link-row {
  ::v-deep(.el-link),
  ::v-deep(.el-link__inner) {
    line-height: inherit;
  }
}
</style>
