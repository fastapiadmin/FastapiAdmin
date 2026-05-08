import { ref, watch } from "vue";

/** 左侧插画背景与右侧登录区的分栏比例 */
export type LoginPanelAlign = "left" | "center" | "right";

const STORAGE_KEY = "login-panel-align";

function readInitial(): LoginPanelAlign {
  try {
    const v = localStorage.getItem(STORAGE_KEY);
    if (v === "left" || v === "center" || v === "right") return v;
  } catch {
    /* ignore */
  }
  /** 默认：插画在左、表单在右 */
  return "right";
}

/**
 * 登录页布局（本地持久化）
 * - left/right：交换插画与表单列左右位置（列宽约 65%/35%）
 * - center：隐藏插画，全宽背景 + 440px 卡片在顶栏与页脚之间居中悬浮
 */
export function useLoginPanelAlign() {
  const panelAlign = ref<LoginPanelAlign>(readInitial());

  watch(panelAlign, (v) => {
    try {
      localStorage.setItem(STORAGE_KEY, v);
    } catch {
      /* ignore */
    }
  });

  return { panelAlign };
}
