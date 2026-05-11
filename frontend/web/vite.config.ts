import fs from "node:fs";
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

/**
 * 扫描 node_modules 下 Element Plus 全部组件的样式入口（与 unplugin 按需样式一致）。
 * 漏扫会在首次用到该组件时触发 dependency optimization 更新 → dev 整页刷新。
 */
function elementPlusComponentStyleIncludes(rootDir: string): string[] {
  const componentsDir = path.join(rootDir, "node_modules", "element-plus", "es", "components");
  try {
    return fs
      .readdirSync(componentsDir, { withFileTypes: true })
      .filter((e) => e.isDirectory())
      .filter((e) => fs.existsSync(path.join(componentsDir, e.name, "style", "index.mjs")))
      .map((e) => `element-plus/es/components/${e.name}/style/index`);
  } catch {
    return [];
  }
}

/**
 * 多在路由/异步组件里才加载的依赖；提前预构建可减少「点一下整页 reload」。
 * 不把 dependencies 全量打入 optimizeDeps，以免拖慢首次 dev 启动。
 */
const OPTIMIZE_DEPS_LAZY_CHUNKS = [
  "xgplayer",
  "@vue-flow/core",
  "@vue-flow/background",
  "@vue-flow/controls",
  "@vue-flow/minimap",
  "@wangeditor-next/editor",
  "codemirror",
  "vue-json-pretty",
  "vue-web-terminal",
  "vue3-cron-plus",
  "@iconify/vue",
  "vuedraggable",
  "vue-draggable-plus",
  "qrcode.vue",
  "xlsx",
  "markdown-it",
  "highlight.js",
  "dagre",
  "dompurify",
  "js-beautify",
  "markdown-it-highlightjs",
  "animate.css",
  "clipboard",
  "crypto-js",
  "file-saver",
  "mitt",
  "ohash",
  "pinia-plugin-persistedstate",
] as const;

function buildOptimizeDepsInclude(rootDir: string): string[] {
  const core = [
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
  ];

  return [
    ...new Set([
      ...core,
      ...OPTIMIZE_DEPS_LAZY_CHUNKS,
      ...elementPlusComponentStyleIncludes(rootDir),
    ]),
  ];
}

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
        "@icons": resolvePath("src/assets/images/svg"),
        "@utils": resolvePath("src/utils"),
        "@stores": resolvePath("src/store"),
        "@styles": resolvePath("src/styles"),
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
              if (id.includes("echarts")) return "echarts";
              if (id.includes("element-plus")) return "element-plus";
              if (id.includes("@wangeditor-next")) return "wangeditor";
              if (id.includes("codemirror")) return "codemirror";
              if (id.includes("exceljs")) return "exceljs";
              if (id.includes("@vue-flow")) return "vue-flow";
              if (id.includes("highlight.js") || id.includes("highlightjs")) return "highlight";
              if (id.includes("xgplayer")) return "xgplayer";
              if (id.includes("markdown-it")) return "markdown";
              const module = id.toString().split("node_modules/")[1].split("/")[0];
              if (["birpc", "hookable", "tslib", "copy-anything"].includes(module)) return;
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
        /** art-* 布局组件以 src/layouts 为唯一源码目录（与 src/layouts/index.vue 一致），避免与旧路径重复 */
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
      /** 仅开发启用：避免生产包体积膨胀与运行期 DevTools 开销 */
      ...(isProduction ? [] : [vueDevTools()]),
    ],
    optimizeDeps: {
      include: buildOptimizeDepsInclude(root),
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
