import App from "./App.vue";
import { createApp } from "vue";
import { initStore } from "./store"; // Store
import { initRouter } from "./router"; // Router
import language from "./locales"; // 国际化
import "@styles/core/tailwind.css"; // tailwind
import "@styles/index.scss"; // 样式
import "@utils/sys/console.ts"; // 控制台输出内容
import { initGlobDirectives } from "./directives";
import { setupErrorHandle } from "./utils/sys/error-handle";

// 暗黑主题样式
import "element-plus/theme-chalk/dark/css-vars.css";

// 过渡动画
import "animate.css";

// 引入 vue-web-terminal
import { createTerminal } from "vue-web-terminal";

document.addEventListener("touchstart", function () {}, { passive: false });

const app = createApp(App);
initStore(app);
initRouter(app);
initGlobDirectives(app);
setupErrorHandle(app);

// 注册终端组件
app.use(createTerminal());

app.use(language);
app.mount("#app");

// 封装设置 title 和 favicon 的函数
import { useConfigStore } from "./store/modules/config.store";

const setTitleAndFavicon = async () => {
  try {
    const configStore = useConfigStore();
    // 强制从服务器获取最新配置
    await configStore.getConfig(true);

    const webTitle = configStore.configData.sys_web_title?.config_value;
    const webFavicon = configStore.configData.sys_web_favicon?.config_value;

    if (webTitle) {
      document.title = webTitle;
    }

    if (webFavicon) {
      document.querySelectorAll('link[rel="icon"], link[rel="shortcut icon"]').forEach((node) => {
        if (node instanceof HTMLLinkElement) {
          node.href = webFavicon;
        }
      });
    }
  } catch (error) {
    console.error("获取配置数据失败:", error);
  }
};

// 在应用挂载后执行设置逻辑
setTitleAndFavicon();
