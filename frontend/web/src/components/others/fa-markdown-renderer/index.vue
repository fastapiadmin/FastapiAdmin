<template>
  <div class="markdown-content" v-html="renderedContent"></div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import MarkdownIt from "markdown-it";
import markdownItHighlightjs from "markdown-it-highlightjs";
import hljs from "highlight.js";
import "highlight.js/styles/atom-one-light.css";

interface Props {
  content: string;
  maxLength?: number;
}

const props = withDefaults(defineProps<Props>(), {
  maxLength: undefined,
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
}).use(markdownItHighlightjs);

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
  const content =
    props.maxLength && props.content.length > props.maxLength
      ? props.content.substring(0, props.maxLength) + "..."
      : props.content;
  return md.render(content);
});
</script>

<style lang="scss" scoped>
.markdown-content {
  font-size: 14px;
  line-height: 1.6;
  color: var(--el-text-color-primary);
  word-wrap: break-word;

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
