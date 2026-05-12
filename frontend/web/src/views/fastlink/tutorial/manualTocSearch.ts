/**
 * 功能验收手册 — 侧栏「筛选目录」扩展词
 * 含与 sys_menu 对齐前的俗称、简称，避免改名后搜不到。
 */

/** 模块级补充检索词 */
export const MANUAL_MODULE_SEARCH_ALIASES: Readonly<Record<string, readonly string[]>> = {
  "mod-system": ["平台管理", "系统管理", "用户", "权限"],
  "mod-monitor": ["监控"],
  "mod-task": ["任务", "调度", "工作流", "cron"],
  "mod-ai": ["AI", "智能", "会话", "记忆"],
  "mod-generator": ["代码生成", "生成器"],
  "mod-app": ["应用", "门户", "插件"],
  "mod-example": ["示例", "案例", "demo"],
  "mod-dashboard": ["仪表盘", "首页", "工作台", "教程"],
  "mod-layout": ["布局", "顶栏", "侧栏", "主题", "锁屏"],
  "mod-exception": ["错误页", "404", "403"],
  "mod-swagger": ["接口", "API", "文档", "swagger", "redoc"],
};

/** 页面级补充检索词（anchor 与 MANUAL_TOC 一致） */
export const MANUAL_PAGE_SEARCH_ALIASES: Readonly<Record<string, readonly string[]>> = {
  "page-resource": ["资源监控", "文件", "上传"],
  "page-cronjob": ["定时任务", "调度器", "job", "cron"],
  "page-cronnode": ["任务节点", "节点"],
  "page-workflow": ["工作流", "流程", "编排"],
  "page-nodetype": ["节点类型", "编排"],
  "page-ai-chat": ["AI 聊天", "聊天", "chat"],
  "page-ai-fachat": ["FA 聊天", "fachat"],
  "page-ai-memory": ["记忆管理", "memory"],
  "page-portal": ["应用门户", "portal"],
  "page-demo": ["示例一", "demo"],
  "page-demo01": ["示例二", "demo01", "三级"],
  "page-swagger": ["Swagger", "swagger"],
  "page-redoc": ["Redoc", "redoc"],
  "page-ljdoc": ["LJDoc", "ljdoc", "LangJin"],
  "page-db-article": ["文章", "article"],
  "page-db-tutorial": ["操作手册", "手册", "教程"],
  "page-login": ["登录", "auth"],
  "page-changelog": ["日志", "版本", "release"],
  "page-home": ["home", "入口"],
  "page-profile": ["个人中心", "profile", "账号"],
};

function includesLoose(text: string, q: string): boolean {
  return text.toLowerCase().includes(q.toLowerCase());
}

/** 模块是否在筛选下保留（标题、别名或任一子页命中） */
export function manualModuleMatchesQuery(modTitle: string, modAnchor: string, q: string): boolean {
  if (includesLoose(modTitle, q)) return true;
  const ma = MANUAL_MODULE_SEARCH_ALIASES[modAnchor];
  if (ma?.some((a) => includesLoose(a, q))) return true;
  return false;
}

/** 子页是否在筛选下保留 */
export function manualPageMatchesQuery(pageTitle: string, pageAnchor: string, q: string): boolean {
  if (includesLoose(pageTitle, q)) return true;
  const pa = MANUAL_PAGE_SEARCH_ALIASES[pageAnchor];
  if (pa?.some((a) => includesLoose(a, q))) return true;
  return false;
}
