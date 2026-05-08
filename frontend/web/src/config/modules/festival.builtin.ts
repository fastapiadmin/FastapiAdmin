/**
 * 内置公历节日（自动按年份生成日期）
 *
 * 与 `festival.ts` 中的手动配置合并后参与匹配：区间更短优先；区间长度相同时 **手动配置优先于内置**。
 * 农历春节/中秋等需农历库的可在 `festival.ts` 用手动区间覆盖。
 *
 * 含少量「动态公历」规则（感恩节、母亲节、父亲节等按星期推算）。
 * 缅怀类日期（九一八、国家公祭日等）使用 `skipFireworks: true`，仅顶栏文案、不放礼花。
 *
 * @module config/modules/festival.builtin
 */

import type { FestivalConfig } from "@/types/config";
import hb from "@imgs/ceremony/hb.png";
import sd from "@imgs/ceremony/sd.png";
import yd from "@imgs/ceremony/yd.png";

function pad2(n: number) {
  return String(n).padStart(2, "0");
}

function ymd(year: number, month: number, day: number): string {
  return `${year}-${pad2(month)}-${pad2(day)}`;
}

/** month 为 1～12 */
function nthWeekdayOfMonth(year: number, month: number, weekday: number, nth: number): number {
  const month0 = month - 1;
  let seen = 0;
  for (let d = 1; d <= 31; d++) {
    const dt = new Date(year, month0, d);
    if (dt.getMonth() !== month0) break;
    if (dt.getDay() === weekday) {
      seen++;
      if (seen === nth) return d;
    }
  }
  return 1;
}

/** 美国感恩节：11 月第四个星期四 */
function thanksgivingUsDay(year: number): number {
  let count = 0;
  for (let d = 1; d <= 30; d++) {
    if (new Date(year, 10, d).getDay() === 4) {
      count++;
      if (count === 4) return d;
    }
  }
  return 26;
}

/** 单条公历规则（同年同月，不做跨年区间；`endDay` 与 `day` 须同月） */
interface SolarRule {
  name: string;
  month: number;
  day: number;
  endDay?: number;
  image: string;
  count?: number;
  fireworkInterval?: number;
  scrollText: string;
  /** 为 true 时不放礼花，仅顶栏文案（适合缅怀、公祭日） */
  skipFireworks?: boolean;
}

const BUILTIN_SOLAR_RULES: SolarRule[] = [
  {
    name: "元旦",
    month: 1,
    day: 1,
    image: yd,
    count: 5,
    fireworkInterval: 900,
    scrollText: "🎊 元旦快乐！新的一年，愿交付顺利、迭代省心。",
  },
  {
    name: "中国人民警察节",
    month: 1,
    day: 10,
    image: yd,
    count: 3,
    scrollText: "👮 人民警察节，向守护平安的人们致敬。",
  },
  {
    name: "情人节",
    month: 2,
    day: 14,
    image: hb,
    count: 4,
    fireworkInterval: 1000,
    scrollText: "💗 情人节快乐，感谢与你并肩写代码、扛上线。",
  },
  {
    name: "妇女节",
    month: 3,
    day: 8,
    image: yd,
    count: 3,
    scrollText: "🌷 节日快乐，致敬每一位闪光的你。",
  },
  {
    name: "植树节",
    month: 3,
    day: 12,
    image: yd,
    count: 3,
    scrollText: "🌳 植树节，愿代码像小树一样扎根生长、枝繁叶茂。",
  },
  {
    name: "消费者权益日",
    month: 3,
    day: 15,
    image: yd,
    count: 3,
    scrollText: "🛡️ 诚信交付、透明沟通，做值得信赖的系统与服务。",
  },
  {
    name: "愚人节",
    month: 4,
    day: 1,
    image: yd,
    count: 3,
    scrollText: "😜 愚人节开心一下～线上变更请以发布单为准哦。",
  },
  {
    name: "清明节",
    month: 4,
    day: 4,
    endDay: 6,
    image: yd,
    count: 3,
    fireworkInterval: 1100,
    scrollText: "🌿 清明安康，春风遥寄思念；出行与发布请注意安全。",
  },
  {
    name: "世界地球日",
    month: 4,
    day: 22,
    image: yd,
    count: 3,
    scrollText: "🌍 地球日，绿色运维、节约资源，从每一次构建与发布做起。",
  },
  {
    name: "世界读书日",
    month: 4,
    day: 23,
    image: yd,
    count: 3,
    scrollText: "📖 读书日，文档与注释也是团队的财富～",
  },
  {
    name: "劳动节",
    month: 5,
    day: 1,
    endDay: 5,
    image: yd,
    count: 4,
    fireworkInterval: 1000,
    scrollText: "🛠️ 劳动节快乐！劳逸结合，迭代与健康都要照顾好。",
  },
  {
    name: "青年节",
    month: 5,
    day: 4,
    image: yd,
    count: 3,
    scrollText: "🎓 青年节快乐，保持好奇与折腾的勇气。",
  },
  {
    name: "护士节",
    month: 5,
    day: 12,
    image: yd,
    count: 3,
    scrollText: "💉 国际护士节，致敬白衣天使与每一位守护健康的人。",
  },
  {
    name: "儿童节",
    month: 6,
    day: 1,
    image: yd,
    count: 4,
    scrollText: "🎈 儿童节快乐，愿童心常在、Bug 少见。",
  },
  {
    name: "世界环境日",
    month: 6,
    day: 5,
    image: yd,
    count: 3,
    scrollText: "🌱 环境日，绿色机房、高效能耗，可持续迭代。",
  },
  {
    name: "建党节",
    month: 7,
    day: 1,
    image: hb,
    count: 4,
    fireworkInterval: 950,
    scrollText: "🎖️ 不忘初心，牢记使命，祝伟大的党生日快乐。",
  },
  {
    name: "建军节",
    month: 8,
    day: 1,
    image: hb,
    count: 4,
    scrollText: "⭐ 八一建军节，致敬人民子弟兵与默默守护的你们。",
  },
  {
    name: "全民健身日",
    month: 8,
    day: 8,
    image: yd,
    count: 3,
    scrollText: "🏃 全民健身日，久坐记得拉伸，健康才是最长迭代。",
  },
  {
    name: "中国人民抗日战争胜利纪念日",
    month: 9,
    day: 3,
    image: hb,
    count: 4,
    scrollText: "🇨🇳 铭记胜利，珍爱和平；吾辈当自强，系统当稳健。",
  },
  {
    name: "教师节",
    month: 9,
    day: 10,
    image: yd,
    count: 3,
    scrollText: "📚 教师节快乐，感谢传道授业与代码 Review～",
  },
  {
    name: "九一八事变纪念日",
    month: 9,
    day: 18,
    image: "",
    count: 3,
    skipFireworks: true,
    scrollText: "铭记历史、缅怀先烈。勿忘国耻，吾辈自强。（本日仅展示提示，不播放礼花）",
  },
  {
    name: "烈士纪念日",
    month: 9,
    day: 30,
    image: "",
    count: 3,
    skipFireworks: true,
    scrollText: "人民英雄永垂不朽。缅怀先烈，砥砺前行。（本日仅展示提示，不播放礼花）",
  },
  {
    name: "国庆节",
    month: 10,
    day: 1,
    endDay: 7,
    image: hb,
    count: 6,
    fireworkInterval: 850,
    scrollText: "🇨🇳 国庆快乐！祝祖国繁荣昌盛，祝你的系统稳如磐石。",
  },
  {
    name: "程序员节",
    month: 10,
    day: 24,
    image: yd,
    count: 5,
    fireworkInterval: 900,
    scrollText: "💻 1024 程序员节快乐！少 Bug、多睡眠，Git 永不冲突～",
  },
  {
    name: "万圣节",
    month: 10,
    day: 31,
    image: sd,
    count: 3,
    scrollText: "🎃 Halloween～夜间发布记得多留一道检查。",
  },
  {
    name: "双十一",
    month: 11,
    day: 11,
    image: hb,
    count: 4,
    scrollText: "🛒 双十一购物愉快～理性消费，库存与订单接口要顶住峰值哦。",
  },
  {
    name: "国家宪法日",
    month: 12,
    day: 4,
    image: yd,
    count: 3,
    scrollText: "📜 国家宪法日，法治同行，合规上线。",
  },
  {
    name: "国家公祭日",
    month: 12,
    day: 13,
    image: "",
    count: 3,
    skipFireworks: true,
    scrollText: "勿忘历史，祈愿和平。缅怀南京大屠杀遇难同胞。（本日仅展示提示，不播放礼花）",
  },
  {
    name: "平安夜",
    month: 12,
    day: 24,
    image: sd,
    count: 4,
    fireworkInterval: 950,
    scrollText: "🍎 平安夜安康，今晚值班的同学辛苦了。",
  },
  {
    name: "圣诞节",
    month: 12,
    day: 25,
    image: sd,
    count: 4,
    scrollText: "🎄 Merry Christmas！愿温暖与发布一样准时送达。",
  },
];

function buildDynamicSolarFestivals(year: number): FestivalConfig[] {
  const motherDay = nthWeekdayOfMonth(year, 5, 0, 2);
  const fatherDay = nthWeekdayOfMonth(year, 6, 0, 3);
  const thanksgiving = thanksgivingUsDay(year);

  const dynamics: SolarRule[] = [
    {
      name: "母亲节",
      month: 5,
      day: motherDay,
      image: hb,
      count: 3,
      scrollText: "💐 母亲节快乐，感谢每一份牵挂与支持。",
    },
    {
      name: "父亲节",
      month: 6,
      day: fatherDay,
      image: hb,
      count: 3,
      scrollText: "👔 父亲节快乐，沉默的爱与可靠的后端一样珍贵。",
    },
    {
      name: "感恩节",
      month: 11,
      day: thanksgiving,
      image: yd,
      count: 3,
      fireworkInterval: 1000,
      scrollText: "🦃 感恩节，感谢并肩的同事与用户信任。",
    },
  ];

  return dynamics.map((r) => {
    const date = ymd(year, r.month, r.day);
    const endDate = r.endDay !== undefined ? ymd(year, r.month, r.endDay) : undefined;
    return {
      name: r.name,
      date,
      endDate,
      image: r.image,
      scrollText: r.scrollText,
      count: r.count,
      fireworkInterval: r.fireworkInterval,
      skipFireworks: r.skipFireworks,
    };
  });
}

/**
 * 生成本年度内置公历节日配置（可直接与手动 `festivalConfigList` 合并）
 */
export function buildBuiltinSolarFestivals(year: number): FestivalConfig[] {
  const staticPart = BUILTIN_SOLAR_RULES.map((r) => {
    const date = ymd(year, r.month, r.day);
    const endDate = r.endDay !== undefined ? ymd(year, r.month, r.endDay) : undefined;
    return {
      name: r.name,
      date,
      endDate,
      image: r.image,
      scrollText: r.scrollText,
      count: r.count,
      fireworkInterval: r.fireworkInterval,
      skipFireworks: r.skipFireworks,
    };
  });
  return [...staticPart, ...buildDynamicSolarFestivals(year)];
}
