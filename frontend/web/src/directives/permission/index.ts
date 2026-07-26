import type { Directive, DirectiveBinding } from "vue";
import { useAuth } from "@/hooks/core/useAuth";

/**
 * 按钮权限指令
 *
 * 统一的权限入口，内部委托 useAuth().hasAuth 进行权限判断。
 * 支持 v-hasPerm="'sys:user:add'" 或 v-hasPerm="['sys:user:add', 'sys:user:edit']"。
 */
export const hasPerm: Directive = {
  mounted(el: HTMLElement, binding: DirectiveBinding) {
    const perms = binding.value;

    if (!perms || (typeof perms !== "string" && !Array.isArray(perms))) {
      throw new Error(
        "需要提供权限标识！例如：v-hasPerm=\"'sys:user:add'\" 或 v-hasPerm=\"['sys:user:add', 'sys:user:edit']\""
      );
    }

    const { hasAuth } = useAuth();
    if (!hasAuth(perms) && el.parentNode) {
      el.parentNode.removeChild(el);
    }
  },
};
