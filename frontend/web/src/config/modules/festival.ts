/**
 * 节日庆祝配置
 *
 * 配置系统的节日烟花效果和祝福文本。
 * 支持单日节日和跨日期节日，可自定义烟花播放次数与连发间隔。
 * 同一天命中多条时，**日期区间更短**的一条优先生效（例如区间更短的节日条会盖住全年的「系统公告」）。
 *
 * ## 配置说明
 *
 * - name: 节日名称
 * - date: 节日开始日期（格式：YYYY-MM-DD）
 * - endDate: 节日结束日期（可选，用于跨日期节日）
 * - image: 礼花/烟花图片（需预先 import；空字符串表示默认几何粒子）
 * - scrollText: 滚动显示的祝福文本
 * - count: 烟花播放次数（可选，默认为 3 次）
 * - fireworkInterval: 两次发射间隔毫秒（可选，默认 1000；调小更密集，如雪花连续感）
 * - skipFireworks: 为 true 时不放烟花，仅显示 scrollText（适合长期顶栏公告）
 * - scrollText 可使用占位符 {{version}}、{{introduceUrl}}（构建时替换为版本号与演示链接）
 *
 * ## 礼花图与快捷键补充
 *
 * - `image` 为红包碎屑 hb、雪花 sd、礼花筒 yd 等时，须在下方 import，勿手写路径字符串。
 * - 全局快捷键：**Ctrl + Shift + P**（Windows / Linux）或 **⌘ + Shift + P**（macOS）立即触发一发礼花；
 *   若当天命中某条「带礼花」的节日配置则使用该配置的 `image`，否则为几何礼花。
 * - 实现：`src/layouts/art-fireworks-effect/index.vue`（键盘）、`src/hooks/core/useCeremony.ts`（自动连发）。
 *
 * ## 自动公历节日
 *
 * `src/config/modules/festival.builtin.ts` 会按**当前年份**生成元旦、劳动节、国庆、圣诞等公历节日及礼花效果；
 * 与下方 `festivalConfigList` **合并**后参与匹配：日期区间**更短**的优先；区间长度相同时 **本文件中的手动项优先于内置**。
 * 春节、中秋等农历日期请在本文件用手动 `date` / `endDate` 配置覆盖。
 *
 * ## 非节日常驻与周末
 *
 * 常驻条目标记 `isResidentBanner: true`（全年区间 + `skipFireworks` 典型）。展示优先级为：
 * **节日（内置+手动）→ 周末提示 → 常驻**：周六/周日若无其它节日命中，显示周末文案；工作日无节日则回落到常驻。
 *
 * ## 注意事项
 *
 * - 图片需要预先导入并在配置中引用；新增素材放在 `src/assets/images/ceremony/`，全局画布会预加载
 *   `festivalConfigList` 中所有非空 `image`。
 * - 跨日期节日会在整个日期范围内生效。
 * - 每个用户每个自然日「自动礼花」流程只会完整播放一次（由 setting store 按自然日记录）。
 *
 * @module config/modules/festival
 * @author FastapiAdmin Team
 */

import { FestivalConfig } from "@/types/config";

export const festivalConfigList: FestivalConfig[] = [
  /**
   * 非节日常驻：全年顶栏公告（匹配优先级最低，见文件头「优先级」说明）
   */
  {
    name: "系统公告",
    date: "2026-01-01",
    endDate: "2026-12-31",
    image: "",
    skipFireworks: true,
    isResidentBanner: true,
    count: 3,
    scrollText:
      '🎉 {{version}}版本正式上线！能力全面提升，配套完整交付方案，助力高效开发与商业落地。 <a href="{{introduceUrl}}" target="_blank" rel="noopener noreferrer">👉 立即体验演示</a>',
  },

  /**
   * 以下为历史示例片段（默认注释），需要时可取消注释并酌情调整日期 / import：
   *
   * 五月短区间示例：含当前日期则会出现节日滚动条；烟花需当日首次进入且未在同日标记已播。
   * 上线前请改成真实活动日期与文案。
   */
  // {
  //   name: "五月温馨提示",
  //   date: "2026-05-04",
  //   endDate: "2026-05-05",
  //   image: yd,
  //   count: 3,
  //   scrollText:
  //     "🎉 五月快乐！FastAPI Admin 祝您工作顺利、迭代顺利。本月请关注备份与安全策略，遇到问题可先查看文档或联系运维。",
  // },

  /** 单日示例（圣诞节）：需取消注释并确保已 import 雪花图 */
  // {
  //   name: "圣诞节",
  //   date: "2026-12-25",
  //   image: sd,
  //   count: 3,
  //   scrollText:
  //     "Merry Christmas！祝您圣诞快乐，愿节日的欢乐与祝福如雪花般纷至沓来！",
  // },

  /** 版本公告类跨日期示例（仅文案参考，可按需改写 scrollText） */
  // {
  //   name: "v3.0 测试阶段",
  //   date: "2026-11-03",
  //   endDate: "2026-11-09",
  //   image: "",
  //   count: 3,
  //   scrollText:
  //     "🚀 系统 v3.0 测试阶段正式开启！测试周期内请关注文档更新与反馈渠道，正式发布敬请期待～",
  // },
];

export { buildBuiltinSolarFestivals } from "./festival.builtin";
