import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  // 路径别名
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@public': resolve(__dirname, 'src/public')
    }
  },
  
  // 构建优化
  build: {
    // 输出目录
    outDir: 'dist',
    
    // 关闭生成source map，提升构建速度和减少文件大小
    sourcemap: false,
    
    // 代码分割配置
    rollupOptions: {
      output: {
        // 代码分割策略
        manualChunks: {
          // 将第三方依赖打包成单独的chunk
          vendor: ['vue', 'vue-router', 'pinia'],
          // 将vitepress核心打包成单独的chunk
          vitepress: ['vitepress'],
          // 将工具库打包成单独的chunk
          utils: ['medium-zoom']
        },
        // 输出文件名格式
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
        assetFileNames: 'assets/[ext]/[name]-[hash].[ext]'
      }
    },
    
    // 压缩配置
    minify: 'terser',
    terserOptions: {
      compress: {
        // 移除console
        drop_console: true,
        // 移除debugger
        drop_debugger: true,
        // 移除未使用的变量
        unused: true,
        // 合并变量
        collapse_vars: true,
        // 内联函数
        inline: true
      },
      // 压缩命名
      mangle: {
        // 压缩变量名
        toplevel: true,
        // 压缩属性名
        properties: true
      }
    },
    
    // 缓存配置
    cacheDir: '.vite/cache',
    
    // 限制chunk大小
    chunkSizeWarningLimit: 2000,
    
    // 预加载策略
    preload: {
      include: {
        type: 'modulepreload',
        include: 'auto'
      }
    }
  },
  
  // 开发服务器配置
  server: {
    port: 5180,
    host: true,
    open: true,
    // 热更新配置
    hmr: {
      overlay: true,
      timeout: 3000
    },
    // 优化开发服务器性能
    fs: {
      strict: false
    }
  },
  
  // 插件配置
  plugins: [],
  
  // CSS配置
  css: {
    // 启用CSS模块
    modules: {
      localsConvention: 'camelCase'
    },
    // 预处理器配置
    preprocessorOptions: {
      scss: {
        additionalData: `@import "@/styles/variables.scss";`
      }
    },
    // 开发环境启用CSS源码映射
    devSourcemap: true
  },
  
  // 优化配置
  optimizeDeps: {
    // 强制预构建的依赖
    include: ['vue', 'vue-router', 'pinia', 'medium-zoom'],
    // 禁用依赖预构建
    disabled: false,
    // 缓存目录
    cacheDir: '.vite/deps',
    // 构建选项
    esbuildOptions: {
      target: 'esnext'
    }
  },
  
  // 环境变量配置
  envDir: '.env',
  envPrefix: 'VITE_'
})