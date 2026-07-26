<!-- 通知组件 -->
<template>
  <div
    class="fa-notification-panel fa-card-sm shadow-xl! flex flex-col"
    :style="{
      transform: show ? 'scaleY(1)' : 'scaleY(0.9)',
      opacity: show ? 1 : 0,
    }"
    v-show="visible"
    @click.stop
  >
    <div class="flex-cb px-3.5 mt-3.5 shrink-0">
      <span class="text-base font-medium text-g-800">{{ $t("notice.title") }}</span>
    </div>

    <ElScrollbar class="flex-1 min-h-0 overflow-y-scroll scrollbar-thin">
      <ul>
        <li
          v-for="(item, index) in noticeList"
          :key="item.title + item.time"
          class="box-border flex-c px-3.5 py-3.5 c-p last:border-b-0 hover:bg-g-200/60"
          @click="handleMarkAsRead(index)"
        >
          <div
            class="size-9 leading-9 text-center rounded-lg flex-cc"
            :class="item.type === 2 ? 'bg-warning/12 text-warning' : 'bg-theme/12 text-theme'"
          >
            <FaSvgIcon class="text-lg bg-transparent!" :icon="getNoticeIcon(item.type)" />
          </div>
          <div class="w-[calc(100%-45px)] ml-3.5">
            <h4 class="text-sm font-normal leading-5.5 text-g-900">{{ item.title }}</h4>
            <p class="mt-1.5 text-xs text-g-500">{{ item.time }}</p>
          </div>
          <div v-if="!item.read" class="ml-2 size-2 rounded-full bg-danger shrink-0"></div>
        </li>
      </ul>

      <!-- 空状态 -->
      <div
        v-show="noticeList.length === 0"
        class="h-full text-g-500 text-center bg-transparent! flex flex-col items-center justify-center mt-12"
      >
        <FaSvgIcon icon="system-uicons:inbox" class="text-5xl" />
        <p class="mt-3.5 text-xs bg-transparent!">{{ $t("notice.empty") }}</p>
      </div>
    </ElScrollbar>

    <div class="box-border w-full px-3.5 pt-2 pb-3.5 shrink-0">
      <ElButton class="w-full" @click="handleViewAll" v-ripple>
        {{ $t("notice.viewAll") }}
      </ElButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import { useRouter } from "vue-router";

import NoticeAPI from "@/api/module_system/notice";

defineOptions({ name: "FaNotification" });

const router = useRouter();

interface NoticeItem {
  title: string;
  time: string;
  read: boolean;
  type: number;
}

interface Props {
  value: boolean;
}

const props = withDefaults(defineProps<Props>(), {});

interface Emits {
  "update:value": [value: boolean];
}

const emit = defineEmits<Emits>();

const show = ref(false);
const visible = ref(false);
const noticeList = ref<NoticeItem[]>([]);
const loading = ref(false);

const getNoticeIcon = (type: number) =>
  type === 2 ? "ri:megaphone-line" : "ri:notification-3-line";

const fetchNotices = async () => {
  loading.value = true;
  try {
    const res = await NoticeAPI.listNoticeAvailable();
    const items = res.data?.data ?? [];
    noticeList.value = items.map((n) => ({
      title: n.notice_title ?? "",
      time: n.created_time ?? "",
      read: false,
      type: Number(n.notice_type) || 1,
    }));
  } catch {
    noticeList.value = [];
  } finally {
    loading.value = false;
  }
};

onMounted(() => fetchNotices());
watch(visible, (v) => {
  if (v) fetchNotices();
});

const handleViewAll = () => {
  router.push("/system/notice");
  emit("update:value", false);
};

const handleMarkAsRead = (index: number) => {
  const item = noticeList.value[index];
  if (item && !item.read) {
    item.read = true;
    // 本地标记已读；全局计数由 noticeStore 管理
  }
};

const showNotice = (open: boolean) => {
  if (open) {
    visible.value = true;
    setTimeout(() => {
      show.value = true;
    }, 5);
  } else {
    show.value = false;
    setTimeout(() => {
      visible.value = false;
    }, 350);
  }
};

watch(
  () => props.value,
  (newValue) => {
    showNotice(newValue);
  }
);
</script>

<style scoped>
@reference '@styles/tailwind.css';

.fa-notification-panel {
  @apply absolute 
  top-14.5
  right-5 
  w-90 
  h-125
  overflow-hidden 
  transition-all 
  duration-300
  origin-top 
  will-change-[top,left] 
  max-[640px]:top-16.25
  max-[640px]:right-0
  max-[640px]:w-full 
  max-[640px]:h-[80vh];
}

.fa-notification-panel.fa-notification-panel {
  border-radius: calc(var(--custom-radius) + 2px) !important;
}

.scrollbar-thin::-webkit-scrollbar {
  width: 5px !important;
}

.dark .scrollbar-thin::-webkit-scrollbar-track {
  background-color: var(--default-box-color);
}

.dark .scrollbar-thin::-webkit-scrollbar-thumb {
  background-color: var(--fa-scrollbar-thumb-dark) !important;
}
</style>
