<template>
  <ElCollapse class="gencode-help-collapse mb-4" accordion>
    <ElCollapseItem name="rules">
      <template #title>
        <span class="gencode-help-collapse__title">
          <ElIcon class="gencode-help-collapse__icon"><InfoFilled /></ElIcon>
          菜单、页面路由与接口路径对照（写入本地时）
        </span>
      </template>
      <ElTable :data="rows" border size="small" class="gencode-rules-table">
        <ElTableColumn prop="parent" label="上级目录" min-width="88" />
        <ElTableColumn prop="sidebar" label="侧栏结构（目录→菜单→按钮）" min-width="200" />
        <ElTableColumn prop="page" label="浏览器地址（页面路由）" min-width="160" />
        <ElTableColumn prop="api" label="前端请求的 HTTP 路径" min-width="160" />
      </ElTable>
      <p class="gencode-help-footnote">
        包名、模块名、业务名见下方表单（业务名对应 plugin 下功能目录，可与
        <code>module_example</code>
        中
        <code>demo</code>
        、
        <code>demo/demo01</code>
        、
        <code>gen_demo02</code>
        对照）。权限为
        <code>包名:模块名:操作</code>
        ，第三段是操作类型（如
        <code>query</code>
        、
        <code>create</code>
        ），与业务目录名无关。动态路由将
        <code>module_xxx</code>
        映射为接口前缀
        <code>/xxx</code>
        ，故页面 URL 与 API 前缀可以不同。仅「下载 ZIP」不会创建菜单。
      </p>
    </ElCollapseItem>
  </ElCollapse>
</template>

<script setup lang="ts">
import { InfoFilled } from "@element-plus/icons-vue";

defineOptions({ name: "GencodeHelpPanel" });

const rows = [
  {
    parent: "已选",
    sidebar: "上级目录 → 短包名目录 → 功能菜单 → 按钮",
    page: "/包名/业务名",
    api: "/短包名/业务名",
  },
  {
    parent: "未选",
    sidebar: "module_包名 → 功能菜单 → 按钮（与 plugin 目录一致）",
    page: "/module_包名/业务名",
    api: "/短包名/业务名",
  },
];
</script>

<style scoped lang="scss">
.gencode-help-collapse {
  overflow: hidden;
  border: 1px solid var(--el-border-color-lighter);
  border-radius: var(--el-border-radius-base);
}

.gencode-help-collapse ::v-deep(.el-collapse-item__header) {
  padding: 8px 12px;
  font-size: 13px;
  font-weight: 500;
  background: var(--el-fill-color-light);
}

.gencode-help-collapse ::v-deep(.el-collapse-item__wrap) {
  border-top: 1px solid var(--el-border-color-lighter);
}

.gencode-help-collapse ::v-deep(.el-collapse-item__content) {
  padding: 10px 12px 12px;
}

.gencode-help-collapse__title {
  display: inline-flex;
  gap: 6px;
  align-items: center;
}

.gencode-help-collapse__icon {
  flex-shrink: 0;
}

.gencode-rules-table ::v-deep(.el-table__cell) {
  font-size: 12px;
}

.gencode-help-footnote {
  margin: 10px 0 0;
  font-size: 12px;
  line-height: 1.55;
  color: var(--el-text-color-secondary);
}

.gencode-help-footnote code {
  padding: 0 4px;
  font-size: 11px;
  background: var(--el-fill-color);
  border-radius: 3px;
}
</style>
