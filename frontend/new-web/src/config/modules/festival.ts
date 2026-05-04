/**
 * 节日庆祝配置
 *
 * 配置系统的节日烟花效果和祝福文本。
 * 支持单日节日和跨日期节日，可自定义烟花播放次数。
 *
 * ## 配置说明
 *
 * - name: 节日名称
 * - date: 节日开始日期（格式：YYYY-MM-DD）
 * - endDate: 节日结束日期（可选，用于跨日期节日）
 * - image: 烟花图片（需要预先导入）
 * - scrollText: 滚动显示的祝福文本
 * - count: 烟花播放次数（可选，默认为 3 次）
 * - skipFireworks: 为 true 时不放烟花，仅显示 scrollText（适合长期顶栏公告）
 * - scrollText 可使用占位符 {{version}}、{{introduceUrl}}（构建时替换为版本号与演示链接）
 *
 * ## 注意事项
 *
 * - 图片需要预先导入并在配置中引用
 * - 跨日期节日会在整个日期范围内生效
 * - 每个用户每天只会播放一次烟花效果
 *
 * @module config/modules/festival
 * @author FastapiAdmin Team
 */

import { FestivalConfig } from "@/types/config";

// 导入烟花图片（根据需要取消注释）
// import sd from "@imgs/ceremony/sd.png";
// import yd from "@imgs/ceremony/yd.png";

export const festivalConfigList: FestivalConfig[] = [
  /**
   * 全年默认顶栏公告（与多条日期重叠时，区间更短的配置优先，例如上面的五月条）
   */
  {
    name: "系统公告",
    date: "2026-01-01",
    endDate: "2026-12-31",
    image: "",
    skipFireworks: true,
    count: 3,
    scrollText:
      '🎉 {{version}}版本正式上线！能力全面提升，配套完整交付方案，助力高效开发与商业落地。 <a href="{{introduceUrl}}" target="_blank" rel="noopener noreferrer">👉 立即体验演示</a>',
  },
  /**
   * 五月示例（2026-05-01～05-31 生效，含当前日期则会出现节日滚动条；烟花需当日首次进入且未在同日标记已播）
   * 上线前请改成真实活动日期与文案；需要自定义烟花图时在配置里 import 并填入 image
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
  // 单日示例（圣诞节）：需取消注释并 import 图片
  // {
  //   name: 'v3.0 Sass 升级至 TailwindCSS',
  //   date: '2025-11-03',
  //   endDate: '2025-11-09',
  //   image: '',
  //   count: 3,
  //   scrollText:
  //     '🚀 系统 v3.0 测试阶段正式开启！测试周期为 11 月 3 日 - 11 月 16 日，通过 TailwindCSS 重构样式体系、统一 Iconify 图标方案，带来更高效现代的开发体验，正式发布敬请期待～'
  // }
  // 单日示例：圣诞节
  // {
  //   name: '圣诞节',
  //   date: '2024-12-25',
  //   image: sd,
  //   count: 3 // 可选，不设置则使用默认值 3 次
  //   scrollText: 'Merry Christmas！Art Design Pro 祝您圣诞快乐，愿节日的欢乐与祝福如雪花般纷至沓来！',
  // }
];
