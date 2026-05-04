<!-- 401页面 -->
<template>
  <ArtException
    :data="{
      title: '401',
      desc: $t('exceptionPage.401'),
      btnText: $t('exceptionPage.gohome'),
      imgUrl,
    }"
  />
</template>

<script setup lang="ts">
import imgUrl from "@imgs/svg/401.svg";
defineOptions({ name: "401" });
</script>
