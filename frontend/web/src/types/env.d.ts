// https://cn.vitejs.dev/guide/env-and-mode

/// <reference types="vite/client" />
/// <reference types="element-plus/global" />

// TypeScript 类型提示都为 string： https://github.com/vitejs/vite/issues/6930
interface ImportMetaEnv {
  /** 环境 */
  VITE_APP_ENV: string;

  /** 项目名称 */
  VITE_APP_TITLE: string;

  /** 网络请求公用地址 */
  VITE_API_BASE_URL: string;

  /** 代理前缀 */
  VITE_APP_BASE_API: string;

  /** 应用端口 */
  VITE_APP_PORT: number;

  /** 超时时间 */
  VITE_TIMEOUT: number;

  /** ws 端点 */
  VITE_APP_WS_ENDPOINT: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

/**
 * 平台的名称、版本、运行所需的`node`版本、依赖、构建时间的类型提示
 */
declare const __APP_INFO__: {
  pkg: {
    name: string;
    version: string;
    engines: {
      node: string;
    };
    dependencies: Record<string, string>;
    devDependencies: Record<string, string>;
  };
  buildTimestamp: number;
};
