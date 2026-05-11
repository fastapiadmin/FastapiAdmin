module.exports = {
  // 继承推荐规范配置
  extends: [
    "stylelint-config-standard",
    "stylelint-config-recommended",
    "stylelint-config-recommended-scss",
    "stylelint-config-recommended-vue/scss",
    "stylelint-config-html/vue",
    "stylelint-config-recess-order",
  ],
  plugins: [
    "stylelint-prettier", // 统一代码风格，格式冲突时以 Prettier 规则为准
  ],
  // 指定不同文件对应的解析器
  overrides: [
    {
      files: ["**/*.{vue,html}"],
      customSyntax: "postcss-html",
    },
    {
      files: ["**/*.{css,scss}"],
      customSyntax: "postcss-scss",
    },
    // Markdown 预览样式由多段合并，存在有意重复的限定选择器
    {
      files: ["**/src/styles/core/md.scss"],
      rules: {
        "no-duplicate-selectors": null,
      },
    },
  ],
  // 自定义规则
  rules: {
    "prettier/prettier": true, // 强制执行 Prettier 格式化规则（需配合 .prettierrc 配置文件）
    "declaration-property-value-no-unknown": null, // 允许非常规数值格式 ,如 height: calc(100% - 50)
    // Tailwind CSS v4 使用 @reference 引入主题而不注入样式，需放行
    "scss/at-rule-no-unknown": [
      true,
      {
        // Tailwind CSS v4：@custom-variant、@theme、@utility、@layer 等
        ignoreAtRules: ["reference", "custom-variant", "theme", "utility", "layer"],
      },
    ],
    "import-notation": "string", // 指定导入CSS文件的方式("string"|"url")
    "selector-class-pattern": null, // 选择器类名命名规则
    "custom-property-pattern": null, // 自定义属性命名规则
    "keyframes-name-pattern": null, // 动画帧节点样式命名规则
    "no-descending-specificity": null, // 允许无降序特异性
    "no-empty-source": null, // 允许空样式
    "property-no-vendor-prefix": null, // 允许属性前缀
    // SCSS @if/@else 链与 Prettier 易冲突，关闭「at-rule 前空行」检查
    "at-rule-empty-line-before": null,
    // 允许 global 、export 、deep伪类
    "selector-pseudo-class-no-unknown": [
      true,
      {
        ignorePseudoClasses: ["global", "export", "deep"],
      },
    ],
    // 允许 Vue 3 的 ::deep 伪元素选择器
    "selector-pseudo-element-no-unknown": [
      true,
      {
        ignorePseudoElements: ["deep"],
      },
    ],
    // 允许未知属性
    "property-no-unknown": [
      true,
      {
        ignoreProperties: [],
      },
    ],
    // 允许未知规则
    "at-rule-no-unknown": null, // 禁用默认的未知 at-rule 检查,
  },
};
