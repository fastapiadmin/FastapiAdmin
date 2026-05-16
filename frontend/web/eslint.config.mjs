// ESLint 配置文件
import fs from "fs";
import path, { dirname } from "path";
import { fileURLToPath } from "url";

// 从 ESLint 插件中导入推荐配置
import pluginJs from "@eslint/js";
import pluginVue from "eslint-plugin-vue";
import globals from "globals";
import tseslint from "typescript-eslint";

// 使用 import.meta.url 获取当前模块的路径
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 读取 .auto-import.json 文件的内容，并将其解析为 JSON 对象
const autoImportConfig = JSON.parse(
  fs.readFileSync(path.resolve(__dirname, ".auto-import.json"), "utf-8")
);

export default [
  // 忽略文件（flat config 中 ignores 需在最前面）
  {
    ignores: [
      "**/node_modules/**",
      "**/dist/**",
      "public/**",
      ".vscode/**",
      "src/assets/**",
      "src/utils/console.ts",
      ".auto-import.json",
    ],
  },
  // 全局语言环境
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
  },
  // 基础推荐配置
  pluginJs.configs.recommended,
  ...tseslint.configs.recommended,
  ...pluginVue.configs["flat/essential"],
  // 项目自定义规则
  {
    files: ["**/*.{js,mjs,cjs,ts,tsx,vue}"],
    languageOptions: {
      globals: {
        ...autoImportConfig.globals,
        // TypeScript 全局命名空间（global.d.ts 中声明的类型）
        Api: "readonly",
        OptionType: "readonly",
        ApiResponse: "readonly",
        UploadFilePath: "readonly",
        // unplugin-vue-components 自动注册的组件引用
        FaSearchBar: "readonly",
        FaSearchBarWithAudit: "readonly",
        FaForm: "readonly",
      },
    },
    rules: {
      "no-var": "error",
      "no-multiple-empty-lines": ["warn", { max: 1 }],
      "no-unexpected-multiline": "error",
      "@typescript-eslint/no-explicit-any": "off",
      "vue/multi-word-component-names": "off",
      // Prettier 负责格式化，ESLint 只关注代码质量
    },
  },
  // Vue 文件：使用 TypeScript parser
  {
    files: ["**/*.vue"],
    languageOptions: {
      parserOptions: { parser: tseslint.parser },
    },
  },
  // .d.ts 声明文件：放宽规则
  {
    files: ["**/*.d.ts"],
    rules: {
      "@typescript-eslint/no-empty-object-type": "off",
    },
  },
];
