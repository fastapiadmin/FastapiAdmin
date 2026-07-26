<template>
  <div class="markdown-content" v-html="renderedContent"></div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import MarkdownIt from "markdown-it";
import hljs from "highlight.js/lib/core";
import javascript from "highlight.js/lib/languages/javascript";
import typescript from "highlight.js/lib/languages/typescript";
import python from "highlight.js/lib/languages/python";
import json from "highlight.js/lib/languages/json";
import html from "highlight.js/lib/languages/xml";
import css from "highlight.js/lib/languages/css";
import scss from "highlight.js/lib/languages/scss";
import sql from "highlight.js/lib/languages/sql";
import bash from "highlight.js/lib/languages/bash";
import yaml from "highlight.js/lib/languages/yaml";
import markdown from "highlight.js/lib/languages/markdown";
import DOMPurify from "dompurify";
import "highlight.js/styles/atom-one-light.css";

// 注册语言（按需导入，减少打包体积）
hljs.registerLanguage("javascript", javascript);
hljs.registerLanguage("typescript", typescript);
hljs.registerLanguage("python", python);
hljs.registerLanguage("json", json);
hljs.registerLanguage("html", html);
hljs.registerLanguage("xml", html);
hljs.registerLanguage("vue", html);
hljs.registerLanguage("css", css);
hljs.registerLanguage("scss", scss);
hljs.registerLanguage("sql", sql);
hljs.registerLanguage("bash", bash);
hljs.registerLanguage("yaml", yaml);
hljs.registerLanguage("markdown", markdown);

defineOptions({ name: "FaMarkdownRenderer" });

interface Props {
  /** Markdown 源文本 */
  content: string;
  /** 超过此长度则截断并追加 "..."（按字符数，不按渲染后长度） */
  maxLength?: number;
  /** 是否对渲染后的 HTML 做 XSS 消毒，默认 true（AI 场景默认开；可信后端 HTML 渲染时可关闭） */
  sanitize?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  maxLength: undefined,
  sanitize: true,
});

const md: MarkdownIt = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  breaks: true,
  highlight(str: string, lang: string): string {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return `<pre class="hljs"><code>${hljs.highlight(str, { language: lang, ignoreIllegals: true }).value}</code></pre>`;
      } catch {
        return `<pre class="hljs"><code>${md.utils.escapeHtml(str)}</code></pre>`;
      }
    }
    return `<pre class="hljs"><code>${md.utils.escapeHtml(str)}</code></pre>`;
  },
});

const defaultRender =
  md.renderer.rules.link_open ||
  function (tokens: any[], idx: number, options: any, env: any, self: any) {
    return self.renderToken(tokens, idx, options, env, self);
  };

md.renderer.rules.link_open = function (
  tokens: any[],
  idx: number,
  options: any,
  env: any,
  self: any
) {
  tokens[idx].attrPush(["target", "_blank"]);
  tokens[idx].attrPush(["rel", "noopener noreferrer"]);
  return defaultRender(tokens, idx, options, env, self);
};

const renderedContent = computed(() => {
  if (!props.content) return "";
  const source =
    props.maxLength && props.content.length > props.maxLength
      ? props.content.substring(0, props.maxLength) + "..."
      : props.content;
  const html = md.render(source);
  return props.sanitize ? DOMPurify.sanitize(html) : html;
});
</script>

<style lang="scss" scoped>
.markdown-content {
  font-size: 14px;
  line-height: 1.6;
  color: var(--el-text-color-primary);
  overflow-wrap: break-word;

  :deep(pre) {
    padding: 12px;
    margin: 12px 0;
    overflow-x: auto;
    background: var(--el-fill-color-light);
    border-radius: 6px;

    code {
      font-family: "Courier New", Courier, monospace;
      font-size: 13px;
    }
  }

  :deep(code) {
    padding: 2px 6px;
    font-family: "Courier New", Courier, monospace;
    font-size: 13px;
    background: var(--el-fill-color-light);
    border-radius: 3px;
  }

  :deep(p) {
    margin: 8px 0;
  }

  :deep(ul),
  :deep(ol) {
    padding-left: 24px;
    margin: 8px 0;
  }

  :deep(li) {
    margin: 4px 0;
  }

  :deep(a) {
    color: var(--el-color-primary);
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }

  :deep(blockquote) {
    padding: 8px 16px;
    margin: 12px 0;
    background: var(--el-fill-color-light);
    border-left: 4px solid var(--el-color-primary);
  }

  :deep(table) {
    width: 100%;
    margin: 12px 0;
    border-collapse: collapse;

    th,
    td {
      padding: 8px 12px;
      border: 1px solid var(--el-border-color-light);
    }

    th {
      font-weight: 600;
      background: var(--el-fill-color-light);
    }
  }
}
</style>
