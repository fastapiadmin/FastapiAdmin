import vue from '@vitejs/plugin-vue';
import * as path from 'path';
import { fileURLToPath } from 'url';
import { type ConfigEnv, type UserConfig, loadEnv, defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';
import vueDevTools from 'vite-plugin-vue-devtools';
import viteCompression from 'vite-plugin-compression';
import Components from 'unplugin-vue-components/vite';
import AutoImport from 'unplugin-auto-import/vite';
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers';
import ElementPlus from 'unplugin-element-plus/vite';

import { name, version, engines, dependencies, devDependencies } from './package.json';

// 平台的名称、版本、运行所需的 node 版本、依赖、构建时间的类型提示
const __APP_INFO__ = {
  pkg: { name, version, engines, dependencies, devDependencies },
  buildTimestamp: Date.now(),
};

// Vite配置  https://cn.vitejs.dev/config
export default defineConfig(({ mode }: ConfigEnv): UserConfig => {
  const root = process.cwd();
  const env = loadEnv(mode, root);

  console.log(`🚀 API_URL = ${env.VITE_API_URL}`);
  console.log(`🚀 VERSION = ${env.VITE_VERSION}`);

  return {
    define: {
      __APP_INFO__: JSON.stringify(__APP_INFO__),
      __APP_VERSION__: JSON.stringify(__APP_INFO__.pkg.version),
    },
    base: env.VITE_BASE_URL,
    server: {
      host: true,
      port: Number(env.VITE_APP_PORT),
      open: true,
      proxy: {
        // 代理 /dev-api 的请求
        [env.VITE_APP_BASE_API]: {
          target: env.VITE_API_BASE_URL, // 代理目标地址：https://后端地址
          secure: false, // 请求是否https
          changeOrigin: true, // 是否跨域
          // rewrite: (path: string) => path.replace(new RegExp("^" + env.VITE_APP_BASE_API), ""),
        },
      },
    },
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
        '@views': path.resolve(__dirname, 'src/views'),
        '@imgs': path.resolve(__dirname, 'src/assets/images'),
        '@icons': path.resolve(__dirname, 'src/assets/icons'),
        '@utils': path.resolve(__dirname, 'src/utils'),
        '@stores': path.resolve(__dirname, 'src/store'),
        '@styles': path.resolve(__dirname, 'src/assets/styles'),
      },
    },
    build: {
      target: 'es2015',
      outDir: 'dist',
      chunkSizeWarningLimit: 4000, // 消除打包大小超过4000kb警告
      minify: 'terser',
      terserOptions: {
        compress: {
          keep_infinity: true, // 防止 Infinity 被压缩成 1/0，这可能会导致 Chrome 上的性能问题
          drop_console: true, // 生产环境去除 console.log, console.warn, console.error 等
          drop_debugger: true, // 生产环境去除 debugger
          pure_funcs: ['console.log', 'console.info'], // 移除指定的函数调用
        },
        format: {
          comments: false, // 删除注释
        },
      } as any,
      dynamicImportVarsOptions: {
        warnOnError: true,
        exclude: [],
        include: ['src/views/**/*.vue'],
      },
      rollupOptions: {
        output: {
          // manualChunks: {
          //   "vue-i18n": ["vue-i18n"],
          // },
          manualChunks(id) {
            if (id.includes('node_modules')) {
              // 针对大型库进行单独拆分
              if (id.includes('echarts')) {
                return 'echarts';
              }
              if (id.includes('element-plus')) {
                return 'element-plus';
              }
              if (id.includes('@wangeditor-next')) {
                return 'wangeditor';
              }
              if (id.includes('codemirror')) {
                return 'codemirror';
              }
              if (id.includes('exceljs')) {
                return 'exceljs';
              }

              // 其他模块保持当前拆分方式
              const parts = id.toString().split('node_modules/');
              if (parts.length > 1) {
                const module = parts[1].split('/')[0];
                if (['birpc', 'hookable'].includes(module)) return;
                return module;
              }
              return;
            }
          },
          // 用于从入口点创建的块的打包输出格式[name]表示文件名,[hash]表示该文件内容hash值
          entryFileNames: 'js/[name].[hash].js',
          // 用于命名代码拆分时创建的共享块的输出命名
          chunkFileNames: 'js/[name].[hash].js',
          // 用于输出静态资源的命名，[ext]表示文件扩展名
          assetFileNames: (assetInfo: any) => {
            const info = assetInfo.name.split('.');
            let extType = info.length > 1 ? info[info.length - 1] : 'unknown';
            // console.log('文件信息', assetInfo.name)
            if (/(\.mp4|webm|ogg|mp3|wav|flac|aac)(\?.*)?$/i.test(assetInfo.name)) {
              extType = 'media';
            } else if (/(\.png|jpe?g|gif|svg)(\?.*)?$/.test(assetInfo.name)) {
              extType = 'img';
            } else if (/(\.woff2?|eot|ttf|otf)(\?.*)?$/i.test(assetInfo.name)) {
              extType = 'fonts';
            }
            return `${extType}/[name].[hash].[ext]`;
          },
        },
      },
    },
    plugins: [
      vue(),
      tailwindcss(),
      // API 自动导入
      AutoImport({
        imports: ['vue', '@vueuse/core', 'pinia', 'vue-router', 'vue-i18n'],
        dts: 'src/types/import/auto-imports.d.ts',
        resolvers: [
          ElementPlusResolver({
            importStyle: 'sass',
            // 自动导入 Element Plus 组件和类型
            directives: true,
            version: '^2.11.2',
          }),
        ],
        vueTemplate: true,
        eslintrc: {
          enabled: true,
          filepath: './.auto-import.json',
          globalsPropValue: true,
        },
      }),
      // 组件自动导入
      Components({
        // 导入 Element Plus 组件
        resolvers: [ElementPlusResolver({ importStyle: 'sass' })],
        // 指定自定义组件位置(默认:src/components)
        dirs: ['src/components', 'src/**/components'],
        // 导入组件类型声明文件路径 (false:关闭自动生成)
        dts: 'src/types/import/components.d.ts',
      }),
      // 按需定制主题配置
      ElementPlus({
        useSource: true,
      }),
      // 压缩
      viteCompression({
        verbose: false, // 是否在控制台输出压缩结果
        disable: false, // 是否禁用
        algorithm: 'gzip', // 压缩算法
        ext: '.gz', // 压缩后的文件名后缀
        threshold: 10240, // 只有大小大于该值的资源会被处理 10240B = 10KB
        deleteOriginFile: false, // 压缩后是否删除原文件
      }),
      vueDevTools(),
    ],
    css: {
      preprocessorOptions: {
        // 定义全局 SCSS 变量
        scss: {
          additionalData: `
            @use "@/styles/variables.scss" as *;
            @use "@styles/core/mixin.scss" as *;
          `,
        },
      },
      postcss: {
        plugins: [
          {
            postcssPlugin: 'internal:charset-removal',
            AtRule: {
              charset: (atRule) => {
                if (atRule.name === 'charset') {
                  atRule.remove();
                }
              },
            },
          },
        ],
      },
    },
    // 依赖预构建：避免运行时重复请求与转换，提升首次加载速度
    optimizeDeps: {
      include: [
        'vue',
        'vue-router',
        'element-plus',
        'pinia',
        'axios',
        '@vueuse/core',
        '@wangeditor-next/editor-for-vue',
        'codemirror-editor-vue3',
        'default-passive-events',
        'exceljs',
        'path-to-regexp',
        'echarts/core',
        'echarts/renderers',
        'echarts/charts',
        'echarts/components',
        'vue-i18n',
        'nprogress',
        'qs',
        'path-browserify',
        '@element-plus/icons-vue',
        'element-plus/es',
        'element-plus/es/locale/lang/en',
        'element-plus/es/locale/lang/zh-cn',
        'element-plus/es/components/alert/style/index',
        'element-plus/es/components/avatar/style/index',
        'element-plus/es/components/backtop/style/index',
        'element-plus/es/components/badge/style/index',
        'element-plus/es/components/base/style/index',
        'element-plus/es/components/breadcrumb-item/style/index',
        'element-plus/es/components/breadcrumb/style/index',
        'element-plus/es/components/button/style/index',
        'element-plus/es/components/card/style/index',
        'element-plus/es/components/cascader/style/index',
        'element-plus/es/components/checkbox-group/style/index',
        'element-plus/es/components/checkbox/style/index',
        'element-plus/es/components/col/style/index',
        'element-plus/es/components/color-picker/style/index',
        'element-plus/es/components/config-provider/style/index',
        'element-plus/es/components/date-picker/style/index',
        'element-plus/es/components/descriptions-item/style/index',
        'element-plus/es/components/descriptions/style/index',
        'element-plus/es/components/dialog/style/index',
        'element-plus/es/components/divider/style/index',
        'element-plus/es/components/drawer/style/index',
        'element-plus/es/components/dropdown-item/style/index',
        'element-plus/es/components/dropdown-menu/style/index',
        'element-plus/es/components/dropdown/style/index',
        'element-plus/es/components/empty/style/index',
        'element-plus/es/components/form-item/style/index',
        'element-plus/es/components/form/style/index',
        'element-plus/es/components/icon/style/index',
        'element-plus/es/components/image-viewer/style/index',
        'element-plus/es/components/image/style/index',
        'element-plus/es/components/input-number/style/index',
        'element-plus/es/components/input-tag/style/index',
        'element-plus/es/components/input/style/index',
        'element-plus/es/components/link/style/index',
        'element-plus/es/components/loading/style/index',
        'element-plus/es/components/menu-item/style/index',
        'element-plus/es/components/menu/style/index',
        'element-plus/es/components/message-box/style/index',
        'element-plus/es/components/message/style/index',
        'element-plus/es/components/notification/style/index',
        'element-plus/es/components/option/style/index',
        'element-plus/es/components/pagination/style/index',
        'element-plus/es/components/popover/style/index',
        'element-plus/es/components/progress/style/index',
        'element-plus/es/components/radio-button/style/index',
        'element-plus/es/components/radio-group/style/index',
        'element-plus/es/components/radio/style/index',
        'element-plus/es/components/row/style/index',
        'element-plus/es/components/scrollbar/style/index',
        'element-plus/es/components/select/style/index',
        'element-plus/es/components/skeleton-item/style/index',
        'element-plus/es/components/skeleton/style/index',
        'element-plus/es/components/step/style/index',
        'element-plus/es/components/steps/style/index',
        'element-plus/es/components/sub-menu/style/index',
        'element-plus/es/components/switch/style/index',
        'element-plus/es/components/tab-pane/style/index',
        'element-plus/es/components/table-column/style/index',
        'element-plus/es/components/table/style/index',
        'element-plus/es/components/tabs/style/index',
        'element-plus/es/components/tag/style/index',
        'element-plus/es/components/text/style/index',
        'element-plus/es/components/time-picker/style/index',
        'element-plus/es/components/time-select/style/index',
        'element-plus/es/components/timeline-item/style/index',
        'element-plus/es/components/timeline/style/index',
        'element-plus/es/components/tooltip/style/index',
        'element-plus/es/components/tree-select/style/index',
        'element-plus/es/components/tree/style/index',
        'element-plus/es/components/upload/style/index',
        'element-plus/es/components/watermark/style/index',
        'element-plus/es/components/tour/style/index',
        'element-plus/es/components/tour-step/style/index',
        'element-plus/es/components/popconfirm/style/index',
        'element-plus/es/components/container/style/index',
        'element-plus/es/components/main/style/index',
        'element-plus/es/components/aside/style/index',
        'element-plus/es/components/footer/style/index',
        'element-plus/es/components/header/style/index',
        'element-plus/es/components/slider/style/index',
        'element-plus/es/components/button-group/style/index',
        'element-plus/es/components/result/style/index',
        'element-plus/es/components/checkbox-button/style/index',
        'element-plus/es/components/space/style/index',
        'xlsx',
        'xgplayer',
        'crypto-js',
        'file-saver',
        'vue-img-cutter',
      ],
    },
  };
});
