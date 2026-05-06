/**
 * useCeremony - 节日庆祝管理
 *
 * 提供节日烟花效果和祝福文本展示功能，为系统增添节日氛围。
 * 自动检测当前日期是否为节日，并在首次进入时播放烟花动画和显示祝福语。
 *
 * ## 主要功能
 *
 * 1. 节日检测 - 自动匹配当前日期与节日配置列表，支持单日和跨日期节日
 * 2. 烟花动画 - 播放节日烟花特效，支持自定义图片和触发次数
 * 3. 祝福文本 - 烟花结束后显示节日祝福文本
 * 4. 状态管理 - 记录烟花播放状态，避免重复播放
 * 5. 清理机制 - 提供清理方法，支持手动停止和重置
 *
 * ## 使用示例
 *
 * ```typescript
 * // 在配置文件中定义节日
 * // 单日节日
 * {
 *   date: '2024-12-25',
 *   name: '圣诞节',
 *   image: christmasImage,
 *   count: 3 // 可选，不设置则使用默认值 3 次
 *   scrollText: 'Merry Christmas!',
 * }
 *
 * // 跨日期节日
 * {
 *   date: '2025-11-07',
 *   endDate: '2025-11-10',
 *   name: 'v3.0 测试阶段',
 *   image: '',
 *   count: 5 // 自定义烟花播放次数
 *   scrollText: '系统 v3.0 测试阶段正式开启！',
 * }
 * ```
 *
 * @module useCeremony
 * @author FastapiAdmin Team
 */

import { useTimeoutFn, useIntervalFn, useDateFormat } from "@vueuse/core";
import { storeToRefs } from "pinia";
import { computed } from "vue";
import { useSettingsStore } from "@/store/modules/setting.store";
import { mittBus } from "@/utils/sys";
import { festivalConfigList } from "@/config/modules/festival";
import { formatToDate } from "@/utils/common";

/**
 * 节日庆祝配置常量
 */
const FESTIVAL_CONFIG = {
  /** 初始延迟（毫秒） */
  INITIAL_DELAY: 300,
  /** 烟花播放间隔（毫秒） */
  FIREWORK_INTERVAL: 1000,
  /** 文本显示延迟（毫秒） */
  TEXT_DELAY: 2000,
  /** 默认烟花播放次数 */
  DEFAULT_FIREWORKS_COUNT: 3,
} as const;

/**
 * 节日庆祝功能
 * 提供节日烟花效果和祝福文本展示
 */
export function useCeremony() {
  const settingStore = useSettingsStore();
  const { holidayFireworksLoaded, isShowFireworks } = storeToRefs(settingStore);

  let fireworksInterval: { pause: () => void } | null = null;

  /**
   * 检查日期是否在节日范围内
   * @param currentDate 当前日期
   * @param festivalDate 节日开始日期
   * @param festivalEndDate 节日结束日期（可选）
   */
  const isDateInRange = (
    currentDate: string,
    festivalDate: string,
    festivalEndDate?: string
  ): boolean => {
    if (!festivalEndDate) {
      // 单日节日
      return currentDate === festivalDate;
    }

    // 跨日期节日
    const current = new Date(currentDate);
    const start = new Date(festivalDate);
    const end = new Date(festivalEndDate);

    return current >= start && current <= end;
  };

  /** 区间越短越「具体」，重叠时优先展示（如五月条优先于全年公告） */
  const festivalRangeSpanDays = (item: (typeof festivalConfigList)[number]): number => {
    if (!item.endDate) return 1;
    const s = new Date(item.date).getTime();
    const e = new Date(item.endDate).getTime();
    return Math.max(1, Math.round((e - s) / 86400000) + 1);
  };

  /**
   * 获取当前日期对应的节日数据（同日多条命中时取区间最短的一条）
   */
  const currentFestivalData = computed(() => {
    const currentDate = useDateFormat(new Date(), "YYYY-MM-DD").value;
    const matches = festivalConfigList.filter((item) =>
      isDateInRange(currentDate, item.date, item.endDate)
    );
    if (!matches.length) return undefined;
    matches.sort((a, b) => festivalRangeSpanDays(a) - festivalRangeSpanDays(b));
    return matches[0];
  });

  /**
   * 标记「今日已完成烟花流程」，用于 store 按自然日防抖（与节日配置的 date 字段无关）
   */
  const updateFestivalDate = () => {
    settingStore.setFestivalDate(formatToDate(new Date()));
  };

  /**
   * 触发烟花效果
   */
  const triggerFirework = () => {
    mittBus.emit("triggerFireworks", currentFestivalData.value?.image);
  };

  /**
   * 完成烟花效果后显示文本
   */
  const showFestivalText = () => {
    settingStore.setholidayFireworksLoaded(true);

    useTimeoutFn(() => {
      settingStore.setShowFestivalText(true);
      updateFestivalDate();
    }, FESTIVAL_CONFIG.TEXT_DELAY);
  };

  /**
   * 启动烟花循环
   */
  const startFireworksLoop = () => {
    let playedCount = 0;
    // 使用节日配置的播放次数，如果没有则使用默认值
    const count = currentFestivalData.value?.count ?? FESTIVAL_CONFIG.DEFAULT_FIREWORKS_COUNT;

    const { pause } = useIntervalFn(() => {
      triggerFirework();
      playedCount++;

      if (playedCount >= count) {
        pause();
        showFestivalText();
      }
    }, FESTIVAL_CONFIG.FIREWORK_INTERVAL);

    fireworksInterval = { pause };
  };

  /**
   * 顶栏纯文案关闭（仅 skipFireworks）持久化 key
   */
  const festivalScrollDismissKey = (cur: (typeof festivalConfigList)[number]): string =>
    `festival_scroll_dismissed_${cur.date}_${cur.endDate ?? ""}`;

  /**
   * 开启节日庆祝：skipFireworks 时直接显示滚动条；否则走烟花再出字
   */
  const openFestival = () => {
    const cur = currentFestivalData.value;
    if (!cur) return;

    if (cur.skipFireworks) {
      if (
        typeof localStorage !== "undefined" &&
        localStorage.getItem(festivalScrollDismissKey(cur)) === "1"
      ) {
        return;
      }
      settingStore.setShowFestivalText(true);
      return;
    }

    if (!isShowFireworks.value) {
      return;
    }

    const { start } = useTimeoutFn(startFireworksLoop, FESTIVAL_CONFIG.INITIAL_DELAY);
    start();
  };

  /**
   * 清理烟花效果
   */
  const cleanup = () => {
    if (fireworksInterval) {
      fireworksInterval.pause();
      fireworksInterval = null;
    }
    settingStore.setShowFestivalText(false);
  };

  /** 关闭顶栏滚动：skipFireworks 时写入 localStorage，下次不再自动展开 */
  const closeFestivalScroll = () => {
    const cur = currentFestivalData.value;
    settingStore.setShowFestivalText(false);
    if (cur?.skipFireworks && typeof localStorage !== "undefined") {
      localStorage.setItem(festivalScrollDismissKey(cur), "1");
    }
  };

  return {
    openFestival,
    cleanup,
    holidayFireworksLoaded,
    currentFestivalData,
    isShowFireworks,
    festivalScrollDismissKey,
    closeFestivalScroll,
  };
}
