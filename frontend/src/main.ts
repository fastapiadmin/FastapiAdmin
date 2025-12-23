import { createApp } from "vue";
import App from "./App.vue";
import setupPlugins from "@/plugins";

// 暗黑主题样式
import "element-plus/theme-chalk/dark/css-vars.css";
import "element-plus/dist/index.css";
// 暗黑模式自定义变量
import "@/styles/dark/css-vars.css";
import "@/styles/index.scss";

import "uno.css";

// 过渡动画
import "animate.css";

import { useConfigStore } from "@/store";

const app = createApp(App);
// 注册插件
app.use(setupPlugins);
// 封装设置 title 和 favicon 的函数
const setTitleAndFavicon = async () => {
  try {
    const configStore = useConfigStore();
    await configStore.getConfig();

    const webTitle = configStore.configData.sys_web_title?.config_value;
    const webFavicon = configStore.configData.sys_web_favicon?.config_value;
    const webLogo = configStore.configData.sys_web_logo?.config_value;

    if (webTitle) {
      document.title = webTitle;
    }

    if (webFavicon) {
      const favicon = document.querySelector('link[rel="icon"]');
      if (favicon instanceof HTMLLinkElement) {
        favicon.href = webFavicon;
      }
    }

    if (webLogo) {
      const loadingLogo = document.querySelector(".loading-container-logo");
      if (loadingLogo instanceof HTMLImageElement) {
        loadingLogo.src = webLogo;
      }
    }
  } catch (error) {
    console.error("获取配置数据失败:", error);
  }
};

app.mount("#app");

// 在应用挂载后执行设置逻辑
setTitleAndFavicon();
