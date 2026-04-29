import { reactive, toRefs } from "vue";
import { tryOnMounted, tryOnUnmounted } from "@vueuse/core";
import dayjs from "dayjs";

const DATE_TIME_FORMAT = "YYYY-MM-DD HH:mm:ss";
const DATE_FORMAT = "YYYY-MM-DD";

export function formatToDateTime(date?: dayjs.ConfigType, format = DATE_TIME_FORMAT): string {
  return dayjs(date).format(format);
}

export function formatToDate(date?: dayjs.ConfigType, format = DATE_FORMAT): string {
  return dayjs(date).format(format);
}

export function formatToTime(time?: dayjs.ConfigType, format = "HH:mm:ss"): string {
  return dayjs(time).format(format);
}

export const useNow = (immediate = true) => {
  let timer: ReturnType<typeof setInterval>;

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

  function start() {
    update();
    clearInterval(timer);
    timer = setInterval(() => update(), 1000);
  }

  function stop() {
    clearInterval(timer);
  }

  tryOnMounted(() => {
    if (immediate) {
      start();
    }
  });

  tryOnUnmounted(() => {
    stop();
  });

  return {
    ...toRefs(state),
    start,
    stop,
  };
};
