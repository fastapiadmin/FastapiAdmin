/**
 * NProgress 进度条配置模块
 *
 * 配置并导出 NProgress 进度条实例，用于页面加载时显示顶部进度条
 *
 * ## 配置说明
 *
 * | 配置项 | 类型 | 默认值 | 说明 |
 * |--------|------|--------|------|
 * | easing | string | 'ease' | 动画缓动方式 |
 * | speed | number | 500 | 进度条递增速度（毫秒） |
 * | showSpinner | boolean | false | 是否显示旋转加载图标 |
 * | trickleSpeed | number | 200 | 自动递增间隔（毫秒） |
 * | minimum | number | 0.3 | 初始化时的最小百分比（0-1） |
 *
 * @module utils/nprogress
 */

import NProgress from "nprogress";
import "nprogress/nprogress.css";

/**
 * 配置 NProgress 进度条
 *
 * 自定义进度条的动画效果和行为
 */
NProgress.configure({
  /** 动画缓动方式 */
  easing: "ease",
  /** 进度条递增速度（毫秒） */
  speed: 500,
  /** 是否显示旋转加载图标 */
  showSpinner: false,
  /** 自动递增间隔（毫秒） */
  trickleSpeed: 200,
  /** 初始化时的最小百分比 */
  minimum: 0.3,
});

/**
 * NProgress 实例导出
 *
 * @example
 * ```typescript
 * import NProgress from '@/utils/nprogress';
 *
 * // 路由跳转开始时显示进度条
 * NProgress.start();
 *
 * // 路由跳转完成时隐藏进度条
 * NProgress.done();
 * ```
 */
export default NProgress;
