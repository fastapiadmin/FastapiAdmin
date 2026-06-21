module.exports = {
  extends: [
    "stylelint-config-standard",
    "stylelint-config-recommended-scss",
    "stylelint-config-recess-order",
  ],
  overrides: [
    {
      files: ["**/*.{vue,html}"],
      customSyntax: "postcss-html",
    },
    {
      files: ["**/*.{css,scss}"],
      customSyntax: "postcss-scss",
    },
  ],
  rules: {
    "import-notation": "string",
    "selector-class-pattern": null,
    "custom-property-pattern": null,
    "keyframes-name-pattern": null,
    "no-descending-specificity": null,
    "no-empty-source": null,
    "property-no-vendor-prefix": null,
    "at-rule-empty-line-before": null,
    // 允许 placeholder mixin 中必要的浏览器前缀（:-ms-input-placeholder、::-webkit-input-placeholder）
    "selector-no-vendor-prefix": [
      true,
      {
        ignoreSelectors: ["::-webkit-input-placeholder", ":-ms-input-placeholder"],
      },
    ],
    // 允许 Vue SFC :deep() / ::deep / :global() / :slotted() 伪选择器
    "selector-pseudo-class-no-unknown": [
      true,
      {
        ignorePseudoClasses: ["global", "export", "deep", "slotted"],
      },
    ],
    "selector-pseudo-element-no-unknown": [
      true,
      {
        ignorePseudoElements: ["deep"],
      },
    ],
    // 允许 SCSS + Tailwind CSS v4 专属 at-rules
    "at-rule-no-unknown": null,
    // 允许注释前无空行（section 分隔注释紧凑排版更清晰）
    "comment-empty-line-before": null,
    "scss/at-rule-no-unknown": [
      true,
      {
        ignoreAtRules: [
          "apply",
          "use",
          "mixin",
          "include",
          "extend",
          "each",
          "if",
          "else",
          "for",
          "while",
          "reference",
          "tailwind",
          "theme",
          "utility",
          "source",
          "custom-variant",
          "layer",
          "config",
          "plugin",
        ],
      },
    ],
  },
};
