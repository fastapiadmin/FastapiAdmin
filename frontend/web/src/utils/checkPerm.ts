/**
 * 纯权限检查函数
 *
 * 检查当前登录用户是否拥有指定权限字符串。
 * 供 useAuth().hasAuth 和 renderTableOperationCell 内部共用，
 * 统一 is_superuser / ROLE_ROOT / 通配符 / prems 的核心检查逻辑。
 *
 * @param perm - 权限标识（如 "module_system:user:create"），空字符串或 undefined 视为有权限
 */
import { ROLE_ROOT } from "@/constants";
import { useUserStore } from "@stores";

export function checkPerm(perm?: string): boolean {
  if (!perm) return true;

  const userStore = useUserStore();
  if (!userStore.basicInfo) return false;
  if (userStore.basicInfo.is_superuser) return true;

  const roles = (userStore.basicInfo as Record<string, any>)?.roles as
    | { code?: string }[]
    | undefined;
  if (roles?.some((r) => r.code === ROLE_ROOT)) return true;
  if (userStore.prems.includes("*:*:*")) return true;
  if (userStore.prems.includes(perm)) return true;

  return false;
}
