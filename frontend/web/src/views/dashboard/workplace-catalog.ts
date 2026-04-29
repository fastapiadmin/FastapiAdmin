import type { MenuTable } from "@/api/module_system/menu";

/**
 * 工作台「模块总览」与 src/views 下目录对应：
 * module_system / module_monitor / module_task / module_ai / module_application / module_generator / module_example / module_common
 */
export interface MenuLeaf {
  title: string;
  path: string;
  icon?: string;
  component_path?: string;
  order?: number;
}

export interface WorkplaceModuleGroup {
  key: string;
  title: string;
  subtitle: string;
  /** 与菜单 component_path 片段匹配（含 views 相对路径） */
  matchHints: string[];
}

/** 按「业务域」划分，与前端 views 目录一致 */
export const WORKPLACE_MODULE_GROUPS: WorkplaceModuleGroup[] = [
  {
    key: "system",
    title: "系统管理",
    subtitle: "用户、角色、菜单、部门、字典、岗位、参数、公告、日志等",
    matchHints: ["module_system/"],
  },
  {
    key: "monitor",
    title: "监控运维",
    subtitle: "服务监控、缓存、在线用户、资源占用等",
    matchHints: ["module_monitor/"],
  },
  {
    key: "task",
    title: "任务与流程",
    subtitle: "定时任务、执行节点、工作流等",
    matchHints: ["module_task/"],
  },
  {
    key: "ai",
    title: "AI 助手",
    subtitle: "对话、记忆管理等",
    matchHints: ["module_ai/"],
  },
  {
    key: "app",
    title: "应用与生成",
    subtitle: "应用管理、代码生成、示例演示等",
    matchHints: ["module_application/", "module_generator/", "module_example/"],
  },
  {
    key: "docs",
    title: "文档中心",
    subtitle: "Swagger / Redoc / 本地文档等",
    matchHints: ["module_common/"],
  },
];

function normalizePath(p: string) {
  return p.replace(/\\/g, "/");
}

/**
 * 在已授权的叶子菜单中，按 matchHints 顺序找到第一个可进入的路由
 */
export function resolveEntryPath(
  leaves: Pick<MenuLeaf, "path" | "component_path">[],
  hints: string[]
): string | undefined {
  for (const hint of hints) {
    const hit = leaves.find(
      (l) => l.component_path && normalizePath(l.component_path).includes(hint)
    );
    if (hit) return hit.path;
  }
  return undefined;
}

export function resolveEntryTitle(leaves: MenuLeaf[], hints: string[]): string | undefined {
  for (const hint of hints) {
    const hit = leaves.find(
      (l) => l.component_path && normalizePath(l.component_path).includes(hint)
    );
    if (hit) return hit.title;
  }
  return undefined;
}

/** 叶子菜单扁平化（与侧栏同源），按菜单 order 排序 */
export function flattenLeafMenusFromTree(menus: MenuTable[]): MenuLeaf[] {
  const seen = new Set<string>();
  const out: MenuLeaf[] = [];
  const walk = (items: MenuTable[]) => {
    for (const m of items) {
      if (m.hidden) continue;
      if (m.children?.length) {
        walk(m.children);
      } else if (m.title && m.route_path) {
        const raw = m.route_path.trim();
        const path = raw.startsWith("/") ? raw : `/${raw}`;
        if (seen.has(path)) continue;
        seen.add(path);
        out.push({
          title: m.title,
          path,
          icon: m.icon,
          component_path: m.component_path,
          order: m.order,
        });
      }
    }
  };
  walk(menus);
  out.sort((a, b) => (a.order ?? 0) - (b.order ?? 0));
  return out;
}
