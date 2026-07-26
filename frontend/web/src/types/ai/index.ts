/**
 * AI 操作处理器（简化版）
 * 可以是简单函数，也可以是配置对象
 */
export type AiActionHandler<T = any> =
  | ((args: T) => Promise<void> | void)
  | {
      execute: (args: T) => Promise<void> | void;
      needConfirm?: boolean;
      confirmMessage?: string | ((args: T) => string);
      successMessage?: string | ((args: T) => string);
      callBackendApi?: boolean;
    };

/**
 * AI 操作配置
 */
export interface UseAiActionOptions {
  actionHandlers?: Record<string, AiActionHandler>;
  onRefresh?: () => Promise<void> | void;
  onAutoSearch?: (keywords: string) => void;
  currentRoute?: string;
}
