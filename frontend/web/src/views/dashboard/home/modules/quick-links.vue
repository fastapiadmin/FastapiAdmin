<template>
  <div class="fa-card p-5 pb-3 h-54 max-sm:h-54 flex flex-col">
    <div class="fa-card-header">
      <div class="title">
        <h4>
          快速链接
          <ElTooltip content="在顶部标签栏左侧星标上点击，可加入或取消收藏" placement="top">
            <ElIcon :size="14"><QuestionFilled /></ElIcon>
          </ElTooltip>
        </h4>
      </div>
    </div>
    <ElScrollbar class="flex-1 min-h-0">
      <div v-if="quickLinks.length" class="grid grid-cols-4 gap-2">
        <div
          v-for="(item, i) in quickLinks"
          :key="item.id || item.href"
          class="group relative flex flex-col items-center gap-1 py-2 px-1 rounded-lg cursor-pointer hover:bg-(--el-fill-color-lighter) transition-colors"
          @click="handleClick(item)"
        >
          <span
            class="flex items-center justify-center w-9 h-9 rounded text-white"
            :style="{ backgroundColor: PALETTE[i % PALETTE.length] }"
          >
            <FaMenuRouteIcon :icon="item.icon || 'menu'" :size="18" />
          </span>
          <span class="text-xs text-center leading-tight line-clamp-2 text-g-700">{{
            item.title
          }}</span>
          <button
            type="button"
            class="absolute -top-1 right-0 flex items-center justify-center w-4 h-4 rounded-full bg-(--el-bg-color) text-(--el-text-color-placeholder) opacity-0 group-hover:opacity-100 transition-opacity border-0 cursor-pointer hover:text-(--el-color-danger)! hover:bg-(--el-color-danger-light-9)!"
            :aria-label="`移除 ${item.title}`"
            @click.stop="handleRemove(item)"
          >
            <ElIcon :size="10"><Close /></ElIcon>
          </button>
        </div>
      </div>
      <ElEmpty v-else description="暂无链接" :image-size="50" />
    </ElScrollbar>
  </div>
</template>

<script setup lang="ts">
import { onScopeDispose, ref } from "vue";
import { useRouter } from "vue-router";
import { Close, QuestionFilled } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { quickStartManager, type QuickLink } from "@utils";

const router = useRouter();

const quickLinks = ref<QuickLink[]>(quickStartManager.getQuickLinks());
const sync = (links: QuickLink[]) => {
  quickLinks.value = links;
};
quickStartManager.addListener(sync);
onScopeDispose(() => quickStartManager.removeListener(sync));

const PALETTE = ["#4080ff", "#23c343", "#ff9a2e", "#f76560", "#a9aeb8", "#00b42a"];

const handleClick = (item: QuickLink) => {
  if (!item.href) return ElMessage.info(`${item.title} 功能待开发`);
  router.push(item.href).catch(() => ElMessage.warning(`路由 ${item.href} 不存在，请检查配置`));
};

const handleRemove = (item: QuickLink) => {
  if (item.id) quickStartManager.removeQuickLink(item.id);
  else if (item.href) quickStartManager.removeQuickLinkByHref(item.href);
};
</script>
