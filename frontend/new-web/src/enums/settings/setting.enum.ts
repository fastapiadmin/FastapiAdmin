/**
 * 页面切换动画枚举
 */
export const enum PageSwitchingAnimationEnum {
  /**
   * 无动画
   */
  NONE = "none",
  /**
   * 淡入淡出
   */
  FADE = "fade",
  /**
   * 平滑切换
   */
  FADE_SLIDE = "fade-slide",
  /**
   * 缩放切换
   */
  FADE_SCALE = "fade-scale",
  /**
   * 左右滑动
   */
  SLIDE_LEFT_RIGHT = "slide-left-right",
  /**
   * 缩放进出
   */
  ZOOM_IN_OUT = "zoom-in-out",
  /**
   * 上下滑动
   */
  SLIDE_UP_DOWN = "slide-up-down",
  /**
   * 弹性效果
   */
  BOUNCE = "bounce",
}
export const PageSwitchingAnimationOptions: Record<string, OptionType> = {
  none: { value: "none", label: "无动画" },
  fade: { value: "fade", label: "淡入淡出" },
  "fade-slide": { value: "fade-slide", label: "平滑切换" },
  "fade-scale": { value: "fade-scale", label: "缩放切换" },
  "slide-left-right": { value: "slide-left-right", label: "左右滑动" },
  "zoom-in-out": { value: "zoom-in-out", label: "缩放进出" },
  "slide-up-down": { value: "slide-up-down", label: "上下滑动" },
  bounce: { value: "bounce", label: "弹性效果" },
};
