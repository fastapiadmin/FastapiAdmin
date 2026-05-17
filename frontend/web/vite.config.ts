import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";
import fs from "node:fs";
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
import { name, version, engines, dependencies, devDependencies } from "./package.json";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

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
    const dirs = fs
      .readdirSync(componentsDir, { withFileTypes: true })
      .filter((e) => e.isDirectory());
    const result: string[] = [];
    for (const d of dirs) {
      const styleDir = path.join(componentsDir, d.name, "style");
      if (fs.existsSync(path.join(styleDir, "index.mjs"))) {
        result.push(`element-plus/es/components/${d.name}/style/index`);
      }
      if (fs.existsSync(path.join(styleDir, "css.mjs"))) {
        result.push(`element-plus/es/components/${d.name}/style/css`);
      }
    }
    return result;
  } catch {
    return [];
  }
}

export default ({ mode }: { mode: string }) => {
  const root = process.cwd();
  const env = loadEnv(mode, root);
  const isProduction = mode === "production";

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
        "@views/*": resolvePath("src/views/*"),
        "@imgs": resolvePath("src/assets/images"),
        "@icons": resolvePath("src/assets/images/svg"),
        "@utils": resolvePath("src/utils"),
        "@stores": resolvePath("src/store"),
        "@plugins": resolvePath("src/plugins"),
        "@styles": resolvePath("src/styles"),
      },
    },
    build: {
      target: "es2024",
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
      rollupOptions: {
        output: {
          manualChunks(id) {
            if (!id.includes("node_modules")) return;
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
            if (id.includes("js-beautify")) return "beautify";
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
      /** 自动按需导入 API */
      AutoImport({
        imports: ["vue", "vue-router", "pinia", "@vueuse/core", "vue-i18n"],
        dts: "src/types/import/auto-imports.d.ts",
        resolvers: [ElementPlusResolver()],
        eslintrc: {
          enabled: true,
          filepath: "./.auto-import.json",
          globalsPropValue: true,
        },
        vueTemplate: true,
      }),
      Components({
        dts: "src/types/import/components.d.ts",
        resolvers: [ElementPlusResolver()],
      }),
      ElementPlus({
        useSource: true,
      }),
      viteCompression({
        verbose: false, // 是否在控制台输出压缩结果
        disable: false, // 是否禁用
        algorithm: "gzip", // 压缩算法
        ext: ".gz", // 压缩后的文件名后缀
        threshold: 10240, // 只有大小大于该值的资源会被处理 10240B = 10KB
        deleteOriginFile: false, // 压缩后是否删除原文件
      }),
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
        "vue-i18n",
        "vue-json-pretty",
        "vue-web-terminal",
        "vue3-cron-plus",
        "vuedraggable",
        "vue-draggable-plus",
        "element-plus",
        "@element-plus/icons-vue",
        "element-plus/es",
        "element-plus/es/locale/lang/en",
        "element-plus/es/locale/lang/zh-cn",
        "pinia",
        "axios",
        "@vueuse/core",
        "codemirror",
        "codemirror-editor-vue3",
        "@wangeditor-next/editor",
        "@wangeditor-next/editor-for-vue",
        "exceljs",
        "echarts/core",
        "echarts/renderers",
        "echarts/charts",
        "echarts/components",
        "nprogress",
        "qs",
        "path-to-regexp",
        "path-browserify",
        "xgplayer",
        "@iconify/vue",
        "qrcode.vue",
        "xlsx",
        "highlight.js",
        "dagre",
        "dompurify",
        "js-beautify",
        "markdown-it",
        "markdown-it-highlightjs",
        "clipboard",
        "crypto-js",
        "file-saver",
        "mitt",
        "ohash",
        "pinia-plugin-persistedstate",
        ...elementPlusComponentStyleIncludes(root),
      ],
    },
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `
            @use "@styles/core/el-light.scss" as *; 
            @use "@styles/core/mixin.scss" as *;
          `,
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
