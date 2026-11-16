import { defineConfig } from "vitest/config";
import vue from "@vitejs/plugin-vue";
import AutoImport from "unplugin-auto-import/vite";
import path from "node:path";
import { name, version } from "./package.json";

export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      imports: ["vue", "vue-router", "pinia", "@vueuse/core", "vue-i18n"],
      dts: false,
      vueTemplate: true,
    }),
  ],
  // 与 vite.config.ts 一致：注入构建期常量，否则 import 到 utils/storage 等模块会报
  // 「__APP_INFO__ is not defined」。
  define: {
    __APP_INFO__: JSON.stringify({ pkg: { name, version } }),
  },
  // 与 vite.config.ts 的 resolve.alias 保持一致，
  // 否则单测里 import 到应用模块时会出现「Failed to resolve import」。
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
      "@views": path.resolve(__dirname, "src/views"),
      "@imgs": path.resolve(__dirname, "src/assets/images"),
      "@icons": path.resolve(__dirname, "src/assets/images/svg"),
      "@utils": path.resolve(__dirname, "src/utils"),
      "@stores": path.resolve(__dirname, "src/store"),
      "@plugins": path.resolve(__dirname, "src/plugins"),
      "@styles": path.resolve(__dirname, "src/styles"),
      "@api": path.resolve(__dirname, "src/api"),
      "@fa_imgs": path.resolve(__dirname, "src/assets/fa_imgs"),
    },
  },
  test: {
    globals: true,
    environment: "jsdom",
    include: ["src/**/*.{test,spec}.{ts,js}"],
  },
});
