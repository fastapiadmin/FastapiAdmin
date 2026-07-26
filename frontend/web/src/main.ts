// ---------------------------------------------------------------------------
// 样式（顺序：EP 基础 → tailwind → 项目全局覆写）
// 必须将 EP 预编译 CSS 放在 index.scss 之前，确保 :root 声明被后加载的覆盖。
// ---------------------------------------------------------------------------
import "element-plus/theme-chalk/base.css";
import "@styles/tailwind.css";
import "@styles/index.scss";

// ---------------------------------------------------------------------------
// 应用初始化
// ---------------------------------------------------------------------------
import App from "./App.vue";
import { createApp } from "vue";
import { printConsoleBanner } from "@utils";
import { initPlugins } from "@/plugins";

/**
 * iOS Safari 中 touch 事件默认是 passive 的，导致 `:active` CSS 伪类不生效。
 * 注册一个空的 `touchstart` 监听（非 passive）来激活 `:active` 响应。
 */
document.addEventListener("touchstart", function () {}, { passive: false });

/** 启动顺序：
 *  1. printConsoleBanner  —— 控制台欢迎信息（无依赖）
 *  2. initPlugins         —— 注册所有 Vue 插件（Pinia → Router → 指令 → 国际化 → Element Plus）
 *  3. mount               —— 挂载根组件
 *  挂载后 App.vue 的 onMounted 中初始化站点标题/favicon（需等 Pinia store 就绪）
 */
(async () => {
  const app = createApp(App);
  printConsoleBanner();
  await initPlugins(app);
  app.mount("#app");
})();
