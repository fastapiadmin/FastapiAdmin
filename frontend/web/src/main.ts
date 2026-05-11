import App from "./App.vue";
import { createApp } from "vue";
import "@styles/core/tailwind.css";
import "@styles/index.scss";
import "element-plus/theme-chalk/dark/css-vars.css";
import "animate.css";

import { initPlugins } from "@/plugins";
import { useConfigStore } from "./store/modules/config.store";

document.addEventListener("touchstart", function () {}, { passive: false });

const app = createApp(App);
initPlugins(app);
app.mount("#app");

/** 挂载后拉取站点标题 / favicon（依赖 Pinia 与接口） */
const setTitleAndFavicon = async () => {
  try {
    const configStore = useConfigStore();
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

void setTitleAndFavicon();
