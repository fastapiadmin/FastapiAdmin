<template>
  <div class="fa-card p-3 pb-1 h-55 max-sm:h-55 flex flex-col relative overflow-hidden">
    <div class="fa-card-header">
      <div class="title">
        <h4>
          快速链接
          <ElTooltip content="在顶部标签栏左侧星标上点击，可加入或取消收藏" placement="top">
            <ElIcon :size="14"><QuestionFilled /></ElIcon>
          </ElTooltip>
        </h4>
      </div>
      <ElTooltip
        v-if="quickLinks.length > 8"
        :content="`共 ${quickLinks.length} 个收藏，首页展示前 8 个`"
        placement="top"
      >
        <span class="quick-links__overflow">{{ quickLinks.length - 8 }} 个未展示</span>
      </ElTooltip>
    </div>
    <div v-if="visibleQuickLinks.length" class="quick-links-grid">
      <div
        v-for="(item, i) in visibleQuickLinks"
        :key="item.id || item.href"
        class="quick-link group relative flex flex-col items-center py-1 px-1 rounded-lg"
      >
        <button
          type="button"
          class="quick-link__open flex w-full flex-col items-center gap-1"
          @click="handleClick(item)"
        >
          <span
            class="flex items-center justify-center w-8 h-8 rounded text-white"
            :style="{ backgroundColor: PALETTE[i % PALETTE.length] }"
          >
            <FaMenuRouteIcon :icon="item.icon || 'menu'" :size="16" />
          </span>
          <span class="text-[11px] text-center leading-[1.15] line-clamp-2 text-g-700">{{
            item.title
          }}</span>
        </button>
        <ElPopconfirm
          :title="`移除“${item.title}”快捷链接？`"
          width="210"
          confirm-button-text="移除"
          cancel-button-text="取消"
          confirm-button-type="danger"
          :hide-after="0"
          @confirm="handleRemove(item)"
        >
          <template #reference>
            <button
              type="button"
              class="quick-link__delete absolute -top-2 -right-2 z-[1] flex items-center justify-center rounded-full border cursor-pointer opacity-0 group-hover:opacity-100 group-focus-within:opacity-100 focus-visible:opacity-100"
              :aria-label="`移除 ${item.title}`"
              @click.stop
            >
              <ElIcon :size="12"><FaSvgIcon icon="ri:close-line" /></ElIcon>
            </button>
          </template>
        </ElPopconfirm>
      </div>
    </div>
    <div
      v-if="!quickLinks.length"
      class="flex flex-1 items-center justify-center px-4 text-xs text-center text-(--el-text-color-placeholder)"
    >
      点击顶部标签左侧 ☆ 收藏常用页面
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onScopeDispose, ref } from "vue";
import { useRouter } from "vue-router";
import { QuestionFilled } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { quickStartManager, type QuickLink } from "@utils";

const router = useRouter();

const quickLinks = ref<QuickLink[]>(quickStartManager.getQuickLinks());
const visibleQuickLinks = computed(() => quickLinks.value.slice(0, 8));
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
  ElMessage.success("已移除快捷链接");
};
</script>

<style scoped>
.quick-links-grid {
  display: grid;
  flex: 1;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  grid-template-rows: repeat(2, minmax(0, 1fr));
  gap: 8px;
  min-height: 0;
  place-items: center;
}

.quick-links__overflow {
  align-self: flex-start;
  padding: 1px 6px;
  border-radius: 999px;
  font-size: 10px;
  line-height: 16px;
  color: var(--fa-text-3);
  background: var(--fa-surface-2);
}

.quick-link {
  width: min(100%, 80px);
  aspect-ratio: 1;
  justify-content: center;
  border: 1px solid transparent;
  transition:
    background-color 0.16s ease,
    border-color 0.16s ease;
}

.quick-link:hover,
.quick-link:focus-within {
  background-color: var(--fa-surface-2);
  background-color: color-mix(in srgb, var(--el-color-primary) 7%, var(--fa-surface));
  border-color: color-mix(in srgb, var(--el-color-primary) 18%, var(--fa-border-subtle));
}

.quick-link__open {
  border: 0;
  background: transparent;
  color: inherit;
  cursor: pointer;
}

.quick-link__open:focus-visible {
  outline: 2px solid var(--el-color-primary-light-5);
  outline-offset: 2px;
  border-radius: 6px;
}

.quick-link__delete {
  width: 24px;
  height: 24px;
  color: var(--el-text-color-placeholder);
  background: var(--fa-surface);
  border-color: var(--fa-border-subtle);
  box-shadow: 0 1px 3px rgb(0 0 0 / 12%);
  transition:
    color 0.16s ease,
    background-color 0.16s ease,
    border-color 0.16s ease,
    opacity 0.16s ease;
}

.quick-link__delete:hover,
.quick-link__delete:focus-visible {
  color: var(--el-color-danger);
  background: var(--el-color-danger-light-9);
  border-color: var(--el-color-danger-light-7);
}
</style>
