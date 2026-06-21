/**
 * useLoading — 按钮/操作的 loading 状态管理
 *
 * 用法 1：包装异步函数
 * ```ts
 * const { withLoading, isLoading } = useLoading();
 *
 * async function handleDelete(id: number) {
 *   await SomeAPI.delete(id);
 *   ElMessage.success("删除成功");
 * }
 *
 * const deleteBtn = withLoading("delete", handleDelete);
 *
 * // template:
 * // <ElButton :loading="isLoading('delete')" @click="deleteBtn">删除</ElButton>
 * ```
 *
 * 用法 2：手动控制（更灵活）
 * ```ts
 * const { loading, run } = useLoading("submit");
 *
 * async function handleSubmit() {
 *   await run(async () => {
 *     await SomeAPI.save(data);
 *   });
 * }
 *
 * // <ElButton :loading="loading" @click="handleSubmit">保存</ElButton>
 * ```
 *
 * 用法 3：单 ref 模式（最简）
 * ```ts
 * const { loading, withLoading } = useLoading();
 *
 * const handleDelete = withLoading(async (id: number) => {
 *   await SomeAPI.delete(id);
 * });
 *
 * // <ElButton :loading="loading" @click="handleDelete(1)">删除</ElButton>
 * ```
 */
import { computed, ref, type ComputedRef, type Ref } from "vue";

export interface UseLoadingReturn {
  /** 任意 key 是否在 loading（key-less 模式下表示唯一 loading） */
  loading: ComputedRef<boolean>;
  /** 当前 loading map（多 key 模式） */
  loadingMap: Readonly<Ref<Record<string, boolean>>>;
  /** 判断指定 key 是否 loading */
  isLoading: (key: string) => boolean;
  /** 包装异步函数（key-less 模式） */
  withLoading: <T extends (...args: any[]) => Promise<any>>(fn: T) => T;
  /** 包装异步函数并绑定 key（多 key 模式） */
  withKeyLoading: <T extends (...args: any[]) => Promise<any>>(key: string, fn: T) => T;
  /** 手动 run（多 key 模式） */
  run: <T>(key: string, fn: () => Promise<T>) => Promise<T>;
  /** 重置所有 loading（通常不需要） */
  reset: () => void;
}

/**
 * 创建 loading 状态管理。
 *
 * @param defaultKey 多 key 模式时的默认 key；不传则单 ref 模式
 */
export function useLoading(defaultKey?: string): UseLoadingReturn {
  const loadingMap = ref<Record<string, boolean>>({});

  function setLoading(key: string, val: boolean): void {
    loadingMap.value = { ...loadingMap.value, [key]: val };
  }

  function isLoading(key: string): boolean {
    return !!loadingMap.value[key];
  }

  /**
   * key-less 模式：直接返回 loading computed（任一 key loading 则 true）
   *  - defaultKey 模式：loading 跟踪该 key
   *  - 单一 ref：直接取 map[defaultKey]
   */
  const loading = computed(() => {
    if (defaultKey) {
      return !!loadingMap.value[defaultKey];
    }
    return Object.values(loadingMap.value).some(Boolean);
  });

  /**
   * 包装异步函数（key-less 模式：自动用 defaultKey 或全状态）
   */
  function withLoading<T extends (...args: any[]) => Promise<any>>(fn: T): T {
    const key = defaultKey ?? "__default__";
    return (async (...args: Parameters<T>) => {
      setLoading(key, true);
      try {
        return await fn(...args);
      } finally {
        setLoading(key, false);
      }
    }) as T;
  }

  /**
   * 包装异步函数 + 显式 key
   */
  function withKeyLoading<T extends (...args: any[]) => Promise<any>>(
    key: string,
    fn: T,
  ): T {
    return (async (...args: Parameters<T>) => {
      setLoading(key, true);
      try {
        return await fn(...args);
      } finally {
        setLoading(key, false);
      }
    }) as T;
  }

  /**
   * 手动 run 模式：调用方控制 key
   */
  async function run<T>(key: string, fn: () => Promise<T>): Promise<T> {
    setLoading(key, true);
    try {
      return await fn();
    } finally {
      setLoading(key, false);
    }
  }

  function reset(): void {
    loadingMap.value = {};
  }

  return {
    loading,
    loadingMap,
    isLoading,
    withLoading,
    withKeyLoading,
    run,
    reset,
  };
}
