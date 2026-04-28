import App from './App.vue';
import { createApp } from 'vue';
import setupPlugins from '@/plugins';
import { createTerminal } from 'vue-web-terminal';
import '@styles/core/tailwind.css'; // tailwind
import '@styles/index.scss'; // 样式
import '@utils/sys/console.ts'; // 控制台输出内容
import { setupErrorHandle } from './utils/sys/error-handle';

// 暗黑主题样式
import 'element-plus/theme-chalk/dark/css-vars.css';
import 'element-plus/dist/index.css';
// 暗黑模式自定义变量
import '@/styles/dark/css-vars.css';

// 过渡动画
import 'animate.css';

import { useConfigStore } from '@/store';

const app = createApp(App);
// 注册插件（包含路由、store、指令、国际化等）
app.use(setupPlugins);
// 注册终端组件
app.use(createTerminal());

// 封装设置 title 和 favicon 的函数
const setTitleAndFavicon = async () => {
  try {
    const configStore = useConfigStore();
    // 强制从服务器获取最新配置
    await configStore.getConfig(true);

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
      const loadingLogo = document.querySelector('.loading-container-logo');
      if (loadingLogo instanceof HTMLImageElement) {
        loadingLogo.src = webLogo;
      }
    }
  } catch (error) {
    console.error('获取配置数据失败:', error);
  }
};

document.addEventListener('touchstart', function () {}, { passive: false });

// 错误处理
setupErrorHandle(app);

app.mount('#app');

// 在应用挂载后执行设置逻辑
setTitleAndFavicon();
