import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";
import { fileURLToPath } from "url";
import vueDevTools from "vite-plugin-vue-devtools";
import viteCompression from "vite-plugin-compression";
import Components from "unplugin-vue-components/vite";
import AutoImport from "unplugin-auto-import/vite";
import ElementPlus from "unplugin-element-plus/vite";
import { ElementPlusResolver } from "unplugin-vue-components/resolvers";
import tailwindcss from "@tailwindcss/vite";
import { name, version, engines, dependencies, devDependencies } from "./package.json";

const __APP_INFO__ = {
  pkg: { name, version, engines, dependencies, devDependencies },
  buildTimestamp: Date.now(),
};

export default ({ mode }: { mode: string }) => {
  const root = process.cwd();
  const env = loadEnv(mode, root);
  const isProduction = mode === "production";

  console.log(`🚀 VITE_API_BASE_URL = ${env.VITE_API_BASE_URL}`);
  console.log(`🚀 VERSION = ${env.VITE_VERSION}`);

  return defineConfig({
    define: {
      __APP_VERSION__: JSON.stringify(env.VITE_VERSION),
      __APP_INFO__: JSON.stringify(__APP_INFO__),
    },
    base: env.VITE_BASE_URL,
    server: {
      host: true,
      port: Number(env.VITE_PORT),
      open: true,
      proxy: {
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
        "@": fileURLToPath(new URL("./src", import.meta.url)),
        "@views": resolvePath("src/views"),
        "@imgs": resolvePath("src/assets/images"),
        "@icons": resolvePath("src/assets/icons"),
        "@utils": resolvePath("src/utils"),
        "@stores": resolvePath("src/store"),
        "@styles": resolvePath("src/assets/styles"),
      },
    },
    build: {
      target: "es2015",
      outDir: "dist",
      chunkSizeWarningLimit: 4000,
      minify: isProduction ? "terser" : false,
      terserOptions: isProduction
        ? {
            compress: {
              keep_infinity: true,
              drop_console: true,
              drop_debugger: true,
              pure_funcs: ["console.log", "console.info"],
            },
            format: {
              comments: true,
            },
          }
        : {},
      dynamicImportVarsOptions: {
        warnOnError: true,
        exclude: [],
        include: ["src/views/**/*.vue"],
      },
      rollupOptions: {
        output: {
          manualChunks(id) {
            if (id.includes("node_modules")) {
              if (id.includes("echarts")) {
                return "echarts";
              }
              if (id.includes("element-plus")) {
                return "element-plus";
              }
              if (id.includes("@wangeditor-next")) {
                return "wangeditor";
              }
              if (id.includes("codemirror")) {
                return "codemirror";
              }
              if (id.includes("exceljs")) {
                return "exceljs";
              }
              const module = id.toString().split("node_modules/")[1].split("/")[0];
              if (["birpc", "hookable"].includes(module)) return;
              return module;
            }
          },
          entryFileNames: "js/[name].[hash].js",
          chunkFileNames: "js/[name].[hash].js",
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
    },
    plugins: [
      vue(),
      tailwindcss(),
      AutoImport({
        imports: ["vue", "vue-router", "pinia", "@vueuse/core", "vue-i18n"],
        dts: "src/types/import/auto-imports.d.ts",
        resolvers: [ElementPlusResolver({ importStyle: "sass" })],
        eslintrc: {
          enabled: true,
          filepath: "./.auto-import.json",
          globalsPropValue: true,
        },
        vueTemplate: true,
      }),
      Components({
        dts: "src/types/import/components.d.ts",
        resolvers: [ElementPlusResolver({ importStyle: "sass" })],
        dirs: ["src/components", "src/**/components"],
      }),
      ElementPlus({
        useSource: true,
      }),
      viteCompression({
        verbose: false,
        disable: false,
        algorithm: "gzip",
        ext: ".gz",
        threshold: 10240,
        deleteOriginFile: false,
      }),
      vueDevTools(),
    ],
    optimizeDeps: {
      include: [
        "vue",
        "vue-router",
        "element-plus",
        "pinia",
        "axios",
        "@vueuse/core",
        "@wangeditor-next/editor-for-vue",
        "codemirror-editor-vue3",
        "exceljs",
        "path-to-regexp",
        "echarts/core",
        "echarts/renderers",
        "echarts/charts",
        "echarts/components",
        "vue-i18n",
        "nprogress",
        "qs",
        "path-browserify",
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
      ],
    },
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `@use "@/styles/variables.scss" as *;`,
        },
      },
      postcss: {
        plugins: [
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
