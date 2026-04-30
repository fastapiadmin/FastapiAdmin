// Type definitions for vite-plugin-uni-pages
// This file provides type definitions for the uni-pages plugin

declare module '@uni-helper/vite-plugin-uni-pages' {
  import type { Plugin } from 'vite'

  export interface UniPagesOptions {
    /**
     * Subpackage directory
     * @default 'src/pages'
     */
    subPackages?: string[]

    /**
     * Global style file
     */
    globalStyle?: Record<string, any>

    /**
     * Tabbar configuration
     */
    tabBar?: Record<string, any>

    /**
     * Whether to merge pages.json
     * @default true
     */
    mergePages?: boolean

    /**
     * Whether to use uni-cloud-router
     * @default false
     */
    uniCloudRouter?: boolean
  }

  export default function UniPages(options?: UniPagesOptions): Plugin
}

// Augment Uni namespace for type-safe routing
declare global {
  namespace UniNamespace {
    interface NavigateToOptions {
      url: string
    }

    interface RedirectToOptions {
      url: string
    }

    interface SwitchTabOptions {
      url: string
    }

    interface ReLaunchOptions {
      url: string
    }
  }
}
