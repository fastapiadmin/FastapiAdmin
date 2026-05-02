/**
 * AI 相关类型定义模块
 *
 * 提供 AI 助手相关的类型定义
 *
 * ## 主要功能
 *
 * - AI 操作处理器类型
 * - AI 操作配置类型
 * - AI 命令执行相关类型
 *
 * ## 使用场景
 *
 * - AI 助手功能开发
 * - AI 操作处理逻辑
 * - AI 命令执行流程
 *
 * @module types/ai/index
 * @author FastapiAdmin Team
 */

/**
 * AI 操作处理器（简化版）
 *
 * 可以是简单函数，也可以是配置对象
 */
export type AiActionHandler<T = any> =
  | ((args: T) => Promise<void> | void)
  | {
      /** 执行函数 */
      execute: (args: T) => Promise<void> | void;
      /** 是否需要确认（默认 true） */
      needConfirm?: boolean;
      /** 确认消息（支持函数或字符串） */
      confirmMessage?: string | ((args: T) => string);
      /** 成功消息（支持函数或字符串） */
      successMessage?: string | ((args: T) => string);
      /** 是否调用后端 API（默认 false，如果为 true 则自动调用 executeCommand） */
      callBackendApi?: boolean;
    };

/**
 * AI 操作配置
 */
export interface UseAiActionOptions {
  /** 操作映射表：函数名 -> 处理器 */
  actionHandlers?: Record<string, AiActionHandler>;
  /** 数据刷新函数（操作完成后调用） */
  onRefresh?: () => Promise<void> | void;
  /** 自动搜索处理函数 */
  onAutoSearch?: (keywords: string) => void;
  /** 当前路由路径（用于执行命令时传递） */
  currentRoute?: string;
}
