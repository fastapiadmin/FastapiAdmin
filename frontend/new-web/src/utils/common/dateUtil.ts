/**
 * 日期工具函数模块
 *
 * 提供日期格式化和实时时间获取功能，基于 dayjs 库封装
 *
 * ## 主要功能
 *
 * - 日期时间格式化
 * - 日期格式化
 * - 时间格式化
 * - 实时时间响应式获取
 *
 * @module utils/dateUtil
 */

import { reactive, toRefs } from "vue";
import { tryOnMounted, tryOnUnmounted } from "@vueuse/core";
import dayjs from "dayjs";

/** 默认日期时间格式 */
const DATE_TIME_FORMAT = "YYYY-MM-DD HH:mm:ss";

/** 默认日期格式 */
const DATE_FORMAT = "YYYY-MM-DD";

/**
 * 格式化日期时间
 *
 * 将日期对象转换为指定格式的字符串
 *
 * @param {dayjs.ConfigType} [date] - 日期对象，可以是字符串、数字或 Date 对象
 * @param {string} [format=DATE_TIME_FORMAT] - 格式化字符串，默认为 'YYYY-MM-DD HH:mm:ss'
 * @returns {string} 格式化后的日期时间字符串
 *
 * @example
 * ```typescript
 * formatToDateTime(new Date()); // "2024-01-15 10:30:45"
 * formatToDateTime('2024-01-15', 'YYYY/MM/DD'); // "2024/01/15"
 * ```
 */
export function formatToDateTime(
  date?: dayjs.ConfigType,
  format: string = DATE_TIME_FORMAT
): string {
  return dayjs(date).format(format);
}

/**
 * 格式化日期
 *
 * 将日期对象转换为仅包含日期部分的字符串
 *
 * @param {dayjs.ConfigType} [date] - 日期对象，可以是字符串、数字或 Date 对象
 * @param {string} [format=DATE_FORMAT] - 格式化字符串，默认为 'YYYY-MM-DD'
 * @returns {string} 格式化后的日期字符串
 *
 * @example
 * ```typescript
 * formatToDate(new Date()); // "2024-01-15"
 * formatToDate('2024-01-15', 'YYYY年MM月DD日'); // "2024年01月15日"
 * ```
 */
export function formatToDate(date?: dayjs.ConfigType, format: string = DATE_FORMAT): string {
  return dayjs(date).format(format);
}

/**
 * 格式化时间
 *
 * 将日期对象转换为仅包含时间部分的字符串
 *
 * @param {dayjs.ConfigType} [time] - 时间对象，可以是字符串、数字或 Date 对象
 * @param {string} [format='HH:mm:ss'] - 格式化字符串，默认为 'HH:mm:ss'
 * @returns {string} 格式化后的时间字符串
 *
 * @example
 * ```typescript
 * formatToTime(new Date()); // "10:30:45"
 * formatToTime('2024-01-15 10:30:45', 'HH:mm'); // "10:30"
 * ```
 */
export function formatToTime(time?: dayjs.ConfigType, format: string = "HH:mm:ss"): string {
  return dayjs(time).format(format);
}

/**
 * 响应式实时时间 Hook
 *
 * 获取实时更新的时间信息，每秒自动更新
 *
 * @param {boolean} [immediate=true] - 是否在组件挂载时立即开始更新
 * @returns {object} 包含时间信息的响应式对象和控制方法
 *
 * @example
 * ```typescript
 * const { year, month, day, hour, minute, second, week, start, stop } = useNow();
 * console.log(year.value); // 当前年份
 * console.log(week.value); // 当前星期
 * ```
 */
export const useNow = (immediate: boolean = true) => {
  let timer: ReturnType<typeof setInterval>;

  /** 时间状态对象 */
  const state = reactive({
    year: 0,
    month: 0,
    week: "",
    day: 0,
    hour: "",
    minute: "",
    second: 0,
    meridiem: "",
  });

  /**
   * 更新时间状态
   */
  const update = () => {
    const now = dayjs();

    const h = now.format("HH");
    const m = now.format("mm");
    const s = now.get("s");

    state.year = now.get("y");
    state.month = now.get("M") + 1;
    state.week = "星期" + ["日", "一", "二", "三", "四", "五", "六"][now.day()];
    state.day = now.get("date");
    state.hour = h;
    state.minute = m;
    state.second = s;
    state.meridiem = now.format("A");
  };

  /**
   * 开始更新时间
   */
  function start(): void {
    update();
    clearInterval(timer);
    timer = setInterval(() => update(), 1000);
  }

  /**
   * 停止更新时间
   */
  function stop(): void {
    clearInterval(timer);
  }

  // 组件挂载时自动开始
  tryOnMounted(() => {
    if (immediate) {
      start();
    }
  });

  // 组件卸载时自动停止
  tryOnUnmounted(() => {
    stop();
  });

  return {
    ...toRefs(state),
    start,
    stop,
  };
};
