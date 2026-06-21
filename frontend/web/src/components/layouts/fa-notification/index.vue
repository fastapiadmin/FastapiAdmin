<!-- 通知组件 -->
<template>
  <div
    class="absolute top-14.5 right-5 w-90 h-125 overflow-hidden transition-all duration-300 origin-top will-change-[top,left] max-[640px]:top-[65px] max-[640px]:right-0 max-[640px]:w-full max-[640px]:h-[80vh] fa-card-sm shadow-xl!"
    :style="{
      transform: show ? 'scaleY(1)' : 'scaleY(0.9)',
      opacity: show ? 1 : 0,
    }"
    v-show="visible"
    @click.stop
  >
    <div class="flex items-center justify-between px-3.5 mt-3.5">
      <span class="text-base font-medium text-g-800">{{ $t("notice.title") }}</span>
      <span
        class="text-xs text-g-800 px-1.5 py-1 cursor-pointer select-none rounded hover:bg-g-200"
      >
        {{ $t("notice.btnRead") }}
      </span>
    </div>

    <ul class="box-border flex items-end w-full h-12.5 px-3.5 border-b border-(--default-border)">
      <li
        v-for="(item, index) in barList"
        :key="index"
        class="h-12 leading-12 mr-5 overflow-hidden text-[13px] text-g-700 cursor-pointer select-none"
        :class="{ 'bar-active': barActiveIndex === index }"
        @click="changeBar(index)"
      >
        {{ item.name }} ({{ item.num }})
      </li>
    </ul>

    <div class="w-full h-[calc(100%-95px)]">
      <ElScrollbar class="h-[calc(100%-60px)]">
        <!-- 通知 -->
        <ul v-show="barActiveIndex === 0">
          <li
            v-for="(item, index) in noticeList"
            :key="index"
            class="box-border flex items-center px-3.5 py-3.5 cursor-pointer last:border-b-0 hover:bg-g-200/60"
          >
            <div
              class="size-9 leading-9 text-center rounded-lg flex items-center justify-center"
              :class="[getNoticeStyle(item.type).iconClass]"
            >
              <FaSvgIcon class="text-lg bg-transparent!" :icon="getNoticeStyle(item.type).icon" />
            </div>
            <div class="w-[calc(100%-45px)] ml-3.5">
              <h4 class="text-sm font-normal leading-5.5 text-g-900">{{ item.title }}</h4>
              <p class="mt-1.5 text-xs text-g-500">{{ item.time }}</p>
            </div>
          </li>
        </ul>

        <!-- 消息 -->
        <ul v-show="barActiveIndex === 1">
          <li
            v-for="(item, index) in msgList"
            :key="index"
            class="box-border flex items-center px-3.5 py-3.5 cursor-pointer last:border-b-0 hover:bg-g-200/60"
          >
            <div
              class="size-9 leading-9 text-center rounded-lg flex items-center justify-center bg-info/12 text-info"
            >
              <FaSvgIcon class="text-lg bg-transparent!" icon="ri:message-3-line" />
            </div>
            <div class="w-[calc(100%-45px)] ml-3.5">
              <h4 class="text-sm font-normal leading-5.5 text-g-900">{{ item.title }}</h4>
              <p class="mt-1.5 text-xs text-g-500">{{ item.time }}</p>
            </div>
          </li>
        </ul>

        <!-- 待办 -->
        <ul v-show="barActiveIndex === 2">
          <li
            v-for="(item, index) in pendingList"
            :key="index"
            class="box-border px-5 py-3.5 last:border-b-0"
          >
            <h4>{{ item.title }}</h4>
            <p class="text-xs text-g-500">{{ item.time }}</p>
          </li>
        </ul>

        <!-- 空状态 -->
        <div
          v-show="currentTabIsEmpty"
          class="relative top-25 h-full text-g-500 text-center bg-transparent!"
        >
          <FaSvgIcon icon="system-uicons:inbox" class="text-5xl" />
          <p class="mt-3.5 text-xs bg-transparent!">
            {{ $t("notice.text[0]") }}{{ barList[barActiveIndex]?.name }}
          </p>
        </div>
      </ElScrollbar>

      <div class="relative box-border w-full px-3.5">
        <ElButton class="w-full mt-3" @click="handleViewAll" v-ripple>
          {{ $t("notice.viewAll") }}
        </ElButton>
      </div>
    </div>

    <div class="h-25"></div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted, type Ref, type ComputedRef } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";

import NoticeAPI, {
  type NoticeTable,
  type NotificationPanelMessage,
} from "@/api/module_system/notice";

defineOptions({ name: "FaNotification" });

interface NoticeItem {
  /** 标题 */
  title: string;
  /** 时间 */
  time: string;
  /** 类型 */
  type: NoticeType;
}

interface MessageItem {
  /** 标题 */
  title: string;
  /** 时间 */
  time: string;
  /** 内容 */
  content?: string;
}

interface PendingItem {
  /** 标题 */
  title: string;
  /** 时间 */
  time: string;
}

interface BarItem {
  /** 名称 */
  name: ComputedRef<string>;
  /** 数量 */
  num: number;
}

interface NoticeStyle {
  /** 图标 */
  icon: string;
  /** icon 样式 */
  iconClass: string;
}

type NoticeType = "email" | "message" | "collection" | "user" | "notice";

const { t } = useI18n();

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
const barActiveIndex = ref(0);

const useNotificationData = () => {
  const panelLoading = ref(false);
  const noticeList = ref<NoticeItem[]>([]);
  const msgList = ref<MessageItem[]>([]);
  const pendingList = ref<PendingItem[]>([]);

  const fetchPanel = async () => {
    panelLoading.value = true;
    try {
      const res = await NoticeAPI.getNotificationPanel();
      const data = (res.data as any)?.data ?? res.data ?? {};

      // 通知
      const notices: any[] = data.notices || [];
      noticeList.value = notices.map((n: NoticeTable) => ({
        title: n.notice_title || "",
        time: n.created_time || "",
        type: "notice" as NoticeType,
      }));

      // 消息
      const messages: NotificationPanelMessage[] = data.messages || [];
      msgList.value = messages.map((m) => ({
        title: m.title || "",
        time: m.time || "",
        content: m.content || "",
      }));

      // 待办
      const pendings: NotificationPanelMessage[] = data.pendings || [];
      pendingList.value = pendings.map((p) => ({
        title: p.title || "",
        time: p.time || "",
      }));
    } catch {
      noticeList.value = [];
      msgList.value = [];
      pendingList.value = [];
    } finally {
      panelLoading.value = false;
    }
  };

  onMounted(() => fetchPanel());
  watch(visible, (v) => {
    if (v) fetchPanel();
  });

  // 标签栏数据
  const barList = computed<BarItem[]>(() => [
    {
      name: computed(() => t("notice.bar[0]")),
      num: noticeList.value.length,
    },
    {
      name: computed(() => t("notice.bar[1]")),
      num: msgList.value.length,
    },
    {
      name: computed(() => t("notice.bar[2]")),
      num: pendingList.value.length,
    },
  ]);

  return {
    noticeList,
    msgList,
    pendingList,
    barList,
  };
};

// 样式管理
const useNotificationStyles = () => {
  const noticeStyleMap: Record<NoticeType, NoticeStyle> = {
    email: {
      icon: "ri:mail-line",
      iconClass: "bg-warning/12 text-warning",
    },
    message: {
      icon: "ri:volume-down-line",
      iconClass: "bg-success/12 text-success",
    },
    collection: {
      icon: "ri:hefa-3-line",
      iconClass: "bg-danger/12 text-danger",
    },
    user: {
      icon: "ri:volume-down-line",
      iconClass: "bg-info/12 text-info",
    },
    notice: {
      icon: "ri:notification-3-line",
      iconClass: "bg-theme/12 text-theme",
    },
  };

  const getNoticeStyle = (type: NoticeType): NoticeStyle => {
    const defaultStyle: NoticeStyle = {
      icon: "ri:arrow-right-circle-line",
      iconClass: "bg-theme/12 text-theme",
    };

    return noticeStyleMap[type] || defaultStyle;
  };

  return {
    getNoticeStyle,
  };
};

// 动画管理
const useNotificationAnimation = () => {
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

  return {
    showNotice,
  };
};

// 标签页管理
const useTabManagement = (
  noticeList: Ref<NoticeItem[]>,
  msgList: Ref<MessageItem[]>,
  pendingList: Ref<PendingItem[]>,
  businessHandlers: {
    handleNoticeAll: () => void;
    handleMsgAll: () => void;
    handlePendingAll: () => void;
  }
) => {
  const changeBar = (index: number) => {
    barActiveIndex.value = index;
  };

  // 检查当前标签页是否为空
  const currentTabIsEmpty = computed(() => {
    const tabDataMap = [noticeList.value, msgList.value, pendingList.value];

    const currentData = tabDataMap[barActiveIndex.value];
    return currentData && currentData.length === 0;
  });

  const handleViewAll = () => {
    // 查看全部处理器映射
    const viewAllHandlers: Record<number, () => void> = {
      0: businessHandlers.handleNoticeAll,
      1: businessHandlers.handleMsgAll,
      2: businessHandlers.handlePendingAll,
    };

    const handler = viewAllHandlers[barActiveIndex.value];
    handler?.();

    // 关闭通知面板
    emit("update:value", false);
  };

  return {
    changeBar,
    currentTabIsEmpty,
    handleViewAll,
  };
};

// 业务逻辑处理
const useBusinessLogic = () => {
  const handleNoticeAll = () => {
    // 跳转到公告管理页面
    const router = useRouter();
    router.push("/module_system/notice");
  };

  const handleMsgAll = () => {
    console.info("[TODO] 查看全部消息");
  };

  const handlePendingAll = () => {
    console.info("[TODO] 查看全部待办");
  };

  return {
    handleNoticeAll,
    handleMsgAll,
    handlePendingAll,
  };
};

// 组合所有逻辑
const { noticeList, msgList, pendingList, barList } = useNotificationData();
const { getNoticeStyle } = useNotificationStyles();
const { showNotice } = useNotificationAnimation();
const { handleNoticeAll, handleMsgAll, handlePendingAll } = useBusinessLogic();
const { changeBar, currentTabIsEmpty, handleViewAll } = useTabManagement(
  noticeList,
  msgList,
  pendingList,
  { handleNoticeAll, handleMsgAll, handlePendingAll }
);

// 监听属性变化
watch(
  () => props.value,
  (newValue) => {
    showNotice(newValue);
  }
);
</script>

<style scoped>
.bar-active {
  color: var(--theme-color) !important;
  border-bottom: 2px solid var(--theme-color);
}
</style>
