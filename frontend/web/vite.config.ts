import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";
import autoprefixer from "autoprefixer";
import path from "node:path";
import { fileURLToPath } from "url";
import vueDevTools from "vite-plugin-vue-devtools";
import viteCompression from "vite-plugin-compression";
import Components from "unplugin-vue-components/vite";
import AutoImport from "unplugin-auto-import/vite";
import ElementPlus from "unplugin-element-plus/vite";
import { ElementPlusResolver } from "unplugin-vue-components/resolvers";
import tailwindcss from "@tailwindcss/vite";
import vitePluginStart from "./build/vitePluginStart";
import Icons from "unplugin-icons/vite";
import IconsResolver from "unplugin-icons/resolver";
import { name, version, engines, dependencies, devDependencies } from "./package.json";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const __APP_INFO__ = {
  pkg: { name, version, engines, dependencies, devDependencies },
  buildTimestamp: Date.now(),
};

export default ({ mode }: { mode: string }) => {
  const root = process.cwd();
  const env = loadEnv(mode, root);
  const isProduction = mode === "prod";

  return defineConfig({
    define: {
      __APP_INFO__: JSON.stringify(__APP_INFO__),
    },
    base: env.VITE_BASE_URL,
    server: {
      host: true,
      port: Number(env.VITE_PORT),
      open: true,
      proxy: {
        [env.VITE_APP_BASE_API]: {
          target: env.VITE_API_BASE_URL,
          secure: false,
          changeOrigin: true,
          // rewrite: (path: string) => path.replace(new RegExp("^" + env.VITE_APP_BASE_API), ""),
        },
      },
    },
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url)),
        "@views": resolvePath("src/views"),
        "@imgs": resolvePath("src/assets/images"),
        "@icons": resolvePath("src/assets/images/svg"),
        "@utils": resolvePath("src/utils"),
        "@stores": resolvePath("src/store"),
        "@plugins": resolvePath("src/plugins"),
        "@styles": resolvePath("src/styles"),
        "@api": resolvePath("src/api"),
        "@fa_imgs": resolvePath("src/assets/fa_imgs"),
      },
    },
    build: {
      target: "es2024",
      outDir: "dist",
      chunkSizeWarningLimit: 4000, // 消除打包大小超过4000kb警告,
      minify: isProduction ? "terser" : false, // 只在生产环境启用压缩
      terserOptions: isProduction
        ? {
            compress: {
              keep_infinity: true, // 防止 Infinity 被压缩成 1/0，这可能会导致 Chrome 上的性能问题
              drop_console: true, // 生产环境去除 console.log, console.warn, console.error 等
              drop_debugger: true, // 生产环境去除 debugger
              pure_funcs: ["console.log", "console.info"], // 移除指定的函数调用
            },
            format: {
              comments: true, // 删除注释
            },
          }
        : {},
      rollupOptions: {
        onwarn(warning, warn) {
          // @vueuse/core 14.x 的 /* #__PURE__ */ 注释位置 Rollup 无法解析，
          // Rollup 会自动移除这些注释（见构建日志 "The comment will be removed to avoid issues"）
          if (warning.message?.includes("@vueuse/core") && warning.message?.includes("#__PURE__")) {
            return;
          }
          warn(warning);
        },
        output: {
          manualChunks(id) {
            if (!id.includes("node_modules")) return;
            // 针对大型库进行单独拆分
            if (id.includes("echarts") || id.includes("zrender")) return "echarts";
            if (id.includes("element-plus")) return "element-plus";
            if (id.includes("@wangeditor")) return "wangeditor";
            if (id.includes("codemirror")) return "codemirror";
            if (id.includes("exceljs")) return "exceljs";
            if (id.includes("@vue-flow") || id.includes("dagre")) return "vue-flow";
            if (id.includes("highlight.js") || id.includes("highlightjs")) return "highlight";
            if (id.includes("xgplayer")) return "xgplayer";
            if (id.includes("markdown-it")) return "markdown";
            if (id.includes("@iconify-json")) return "iconify-icons";
            if (id.includes("xlsx")) return "xlsx";
            if (id.includes("crypto-js")) return "crypto";
            if (id.includes("dayjs")) return "dayjs";
            if (
              id.includes("vue/") ||
              id.includes("vue-router") ||
              id.includes("pinia") ||
              id.includes("vue-i18n") ||
              id.includes("@vueuse")
            )
              return "vue-vendor";

            const module = id
              .toString()
              .replace(/^.*[/\\]node_modules[/\\]\.pnpm[/\\][^/\\]+[/\\]node_modules[/\\]/, "")
              .split("node_modules/")
              .pop()
              ?.split("/")[0];
            if (
              !module ||
              [
                "birpc",
                "hookable",
                "tslib",
                "copy-anything",
                "danmu.js",
                "lodash-unified",
                "perfect-debounce",
              ].includes(module)
            )
              return;
            return module;
          },
          // 用于从入口点创建的块的打包输出格式[name]表示文件名,[hash]表示该文件内容hash值
          entryFileNames: "js/[name].[hash].js",
          // 用于命名代码拆分时创建的共享块的输出命名
          chunkFileNames: "js/[name].[hash].js",
          // 用于输出静态资源的命名，[ext]表示文件扩展名
          assetFileNames: (assetInfo: any) => {
            const info = assetInfo.name.split(".");
            let extType = info[info.length - 1];
            if (/\.(mp4|webm|ogg|mp3|wav|flac|aac)(\?.*)?$/i.test(assetInfo.name)) {
              extType = "media";
            } else if (/\.(png|jpe?g|gif|svg)(\?.*)?$/.test(assetInfo.name)) {
              extType = "img";
            } else if (/\.(woff2?|eot|ttf|otf)(\?.*)?$/i.test(assetInfo.name)) {
              extType = "fonts";
            }
            return `${extType}/[name].[hash].[ext]`;
          },
        },
      },
      dynamicImportVarsOptions: {
        warnOnError: true,
        exclude: [],
        include: ["src/views/**/*.vue"],
      },
    },
    plugins: [
      vue(),
      vitePluginStart(),
      tailwindcss(),
      // API 自动导入
      AutoImport({
        imports: [
          "vue",
          "vue-router",
          "pinia",
          "@vueuse/core",
          "vue-i18n",
          {
            axios: [["default", "axios"]],
          },
          {
            "element-plus/es": [
              "ElScrollbar",
              "ElInput",
              "ElMessageBox",
              "ElNotification",
              "ElMessage",
              "ElSwitch",
              "ElAvatar",
              "ElButton",
            ],
          },
        ],
        dirs: ["./src/hooks/core"],
        dts: "src/types/auto-imports.d.ts",
        resolvers: [
          ElementPlusResolver(), // 自动导入 Element Plus 组件
          IconsResolver({}),
        ], // 自动导入 Element Plus 图标
        eslintrc: {
          enabled: true,
          filepath: "./.eslintrc-auto-import.json",
          globalsPropValue: true,
        },
        vueTemplate: true,
      }),
      // 组件自动导入
      Components({
        dirs: ["src/components", "src/layouts", "src/**/components"],
        dts: "src/types/components.d.ts",
        resolvers: [
          ElementPlusResolver(), // 自动导入 Element Plus 组件
          IconsResolver(), // 自动导入 Element Plus 图标
        ],
      }),
      Icons({
        // 自动安装图标库
        autoInstall: true,
      }),
      ElementPlus({
        // useSource: false 使用预编译 CSS，减少构建时间和样式按需加载时的依赖优化触发
        useSource: false,
      }),
      // 生产环境：gzip 压缩（兼容性好）
      ...(isProduction
        ? [
            viteCompression({
              verbose: false,
              algorithm: "gzip",
              ext: ".gz",
              threshold: 10240,
              deleteOriginFile: false,
            }),
            // 生产环境：brotli 压缩（压缩率更高，现代浏览器支持）
            viteCompression({
              verbose: false,
              algorithm: "brotliCompress",
              ext: ".br",
              threshold: 10240,
              deleteOriginFile: false,
            }),
          ]
        : []),
      /** 仅开发启用：避免生产包体积膨胀与运行期 DevTools 开销 */
      ...(isProduction ? [] : [vueDevTools()]),
    ],
    optimizeDeps: {
      include: [
        "@vue-flow/core",
        "@vue-flow/background",
        "@vue-flow/controls",
        "@vue-flow/minimap",
        "vue",
        "vue-router",
        "element-plus",
        "pinia",
        "axios",
        "@vueuse/core",
        "vue-json-pretty",
        "vue-web-terminal",
        "vue-draggable-plus",
        "element-plus",
        "@element-plus/icons-vue",
        "element-plus/es",
        "element-plus/es/locale/lang/en",
        "element-plus/es/locale/lang/zh-cn",
        "element-plus/es/components/alert/style/index",
        "element-plus/es/components/avatar/style/index",
        "element-plus/es/components/backtop/style/index",
        "element-plus/es/components/badge/style/index",
        "element-plus/es/components/base/style/index",
        "element-plus/es/components/breadcrumb-item/style/index",
        "element-plus/es/components/breadcrumb/style/index",
        "element-plus/es/components/button/style/index",
        "element-plus/es/components/calendar/style/index",
        "element-plus/es/components/card/style/index",
        "element-plus/es/components/cascader/style/index",
        "element-plus/es/components/checkbox-group/style/index",
        "element-plus/es/components/checkbox/style/index",
        "element-plus/es/components/col/style/index",
        "element-plus/es/components/color-picker/style/index",
        "element-plus/es/components/config-provider/style/index",
        "element-plus/es/components/date-picker/style/index",
        "element-plus/es/components/descriptions-item/style/index",
        "element-plus/es/components/descriptions/style/index",
        "element-plus/es/components/dialog/style/index",
        "element-plus/es/components/divider/style/index",
        "element-plus/es/components/drawer/style/index",
        "element-plus/es/components/dropdown-item/style/index",
        "element-plus/es/components/dropdown-menu/style/index",
        "element-plus/es/components/dropdown/style/index",
        "element-plus/es/components/empty/style/index",
        "element-plus/es/components/form-item/style/index",
        "element-plus/es/components/form/style/index",
        "element-plus/es/components/icon/style/index",
        "element-plus/es/components/image-viewer/style/index",
        "element-plus/es/components/image/style/index",
        "element-plus/es/components/input-number/style/index",
        "element-plus/es/components/input-tag/style/index",
        "element-plus/es/components/input/style/index",
        "element-plus/es/components/link/style/index",
        "element-plus/es/components/loading/style/index",
        "element-plus/es/components/menu-item/style/index",
        "element-plus/es/components/menu/style/index",
        "element-plus/es/components/message-box/style/index",
        "element-plus/es/components/message/style/index",
        "element-plus/es/components/notification/style/index",
        "element-plus/es/components/option/style/index",
        "element-plus/es/components/pagination/style/index",
        "element-plus/es/components/popover/style/index",
        "element-plus/es/components/progress/style/index",
        "element-plus/es/components/radio-button/style/index",
        "element-plus/es/components/radio-group/style/index",
        "element-plus/es/components/radio/style/index",
        "element-plus/es/components/row/style/index",
        "element-plus/es/components/scrollbar/style/index",
        "element-plus/es/components/select/style/index",
        "element-plus/es/components/skeleton-item/style/index",
        "element-plus/es/components/skeleton/style/index",
        "element-plus/es/components/step/style/index",
        "element-plus/es/components/steps/style/index",
        "element-plus/es/components/sub-menu/style/index",
        "element-plus/es/components/switch/style/index",
        "element-plus/es/components/tab-pane/style/index",
        "element-plus/es/components/table-column/style/index",
        "element-plus/es/components/table/style/index",
        "element-plus/es/components/tabs/style/index",
        "element-plus/es/components/tag/style/index",
        "element-plus/es/components/text/style/index",
        "element-plus/es/components/time-picker/style/index",
        "element-plus/es/components/time-select/style/index",
        "element-plus/es/components/timeline-item/style/index",
        "element-plus/es/components/timeline/style/index",
        "element-plus/es/components/tooltip/style/index",
        "element-plus/es/components/tree-select/style/index",
        "element-plus/es/components/tree/style/index",
        "element-plus/es/components/upload/style/index",
        "element-plus/es/components/watermark/style/index",
        "element-plus/es/components/tour/style/index",
        "element-plus/es/components/tour-step/style/index",
        "element-plus/es/components/popconfirm/style/index",
        "element-plus/es/components/container/style/index",
        "element-plus/es/components/main/style/index",
        "element-plus/es/components/aside/style/index",
        "element-plus/es/components/footer/style/index",
        "element-plus/es/components/header/style/index",
        "element-plus/es/components/slider/style/index",
        "element-plus/es/components/button-group/style/index",
        "element-plus/es/components/result/style/index",
        "element-plus/es/components/checkbox-button/style/index",
        "element-plus/es/components/space/style/index",
        "codemirror",
        "codemirror-editor-vue3",
        "@wangeditor-next/editor",
        "@wangeditor-next/editor-for-vue",
        "exceljs",
        "nprogress",
        "qs",
        "xgplayer",
        "@iconify/iconify",
        "@iconify/vue",
        "qrcode.vue",
        "xlsx",
        "highlight.js",
        "dagre",
        "dompurify",
        "markdown-it",
        "crypto-js",
        "file-saver",
        "mitt",
        "ohash",
        "pinia-plugin-persistedstate",
        "echarts",
      ],
    },
    css: {
      preprocessorOptions: {
        // 定义全局 SCSS 变量
        scss: {
          additionalData: `
            // 业务工具 mixin 注入（供 src 内 SCSS 文件直接使用，无需手动引入）。
            @use "@styles/core/mixin.scss" as *;
          `,
        },
      },
      postcss: {
        plugins: [
          autoprefixer(),
          {
            postcssPlugin: "internal:charset-removal",
            AtRule: {
              charset: (atRule: any) => {
                if (atRule.name === "charset") {
                  atRule.remove();
                }
              },
            },
          },
        ],
      },
    },
  });
};

function resolvePath(paths: string) {
  return path.resolve(__dirname, paths);
}
