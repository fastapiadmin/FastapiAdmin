// https://cn.vitejs.dev/guide/env-and-mode

/// <reference types="vite/client" />
/// <reference types="element-plus/global" />

// TypeScript 类型提示都为 string： https://github.com/vitejs/vite/issues/6930
interface ImportMetaEnv {
  /** 环境标识 */
  VITE_APP_ENV: string;

  /** 项目名称 */
  VITE_APP_TITLE: string;

  /** API 请求基础路径 */
  VITE_API_URL: string;

  /** 开发环境代理目标地址 */
  VITE_API_BASE_URL: string;

  /** 代理前缀 */
  VITE_APP_BASE_API: string;

  /** 开发服务器端口 */
  VITE_PORT: number;

  /** 网络请求超时时间（毫秒） */
  VITE_API_TIMEOUT: number;

  /** WebSocket 端点 */
  VITE_APP_WS_ENDPOINT: string;

  /** 应用部署基础路径 */
  VITE_BASE_URL: string;

  /** 权限模式 */
  VITE_ACCESS_MODE: string;

  /** 跨域请求是否携带 Cookie */
  VITE_WITH_CREDENTIALS: string;

  /** 是否在控制台输出路由信息 */
  VITE_OPEN_ROUTE_INFO: string;

  /** 锁屏加密密钥 */
  VITE_LOCK_ENCRYPT_KEY: string;

  /** 是否删除控制台输出 */
  VITE_DROP_CONSOLE: string;

  /** 应用版本号 */
  VITE_VERSION: string;
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
