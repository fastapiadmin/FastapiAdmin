import { defineConfig } from 'vitepress'

/** 中文指南侧边栏(src/guide/ 下实际存在的文档) */
const zhGuideSidebar = [
  {
    text: '快速开始',
    items: [
      { text: '项目概述', link: '/guide/overview' },
      { text: '为什么选择 FastapiAdmin？', link: '/guide/why' },
      { text: '快速开始', link: '/guide/start' },
    ],
  },
  {
    text: '开发指南',
    items: [
      { text: '前端开发指南', link: '/guide/frontend' },
      { text: '后端开发指南', link: '/guide/backend' },
      { text: '移动端开发指南', link: '/guide/miniprogram' },
      { text: '开发规范', link: '/guide/guidelines' },
    ],
  },
  {
    text: '部署与发布',
    items: [
      { text: '部署指南', link: '/guide/deployment' },
      { text: '更新日志', link: '/guide/changelog' },
    ],
  },
]

/** 英文指南侧边栏(src/en/guide/ 下实际存在的文档) */
const enGuideSidebar = [
  {
    text: 'Getting Started',
    items: [
      { text: 'Project Overview', link: '/en/guide/overview' },
      { text: 'Why FastapiAdmin?', link: '/en/guide/why' },
      { text: 'Quick Start', link: '/en/guide/start' },
    ],
  },
  {
    text: 'Development',
    items: [
      { text: 'Frontend Development Guide', link: '/en/guide/frontend' },
      { text: 'Backend Development Guide', link: '/en/guide/backend' },
      { text: 'Miniprogram Development Guide', link: '/en/guide/miniprogram' },
      { text: 'Development Guidelines', link: '/en/guide/guidelines' },
    ],
  },
  {
    text: 'Deployment & Releases',
    items: [
      { text: 'Deployment Guide', link: '/en/guide/deployment' },
      { text: 'Changelog', link: '/en/guide/changelog' },
    ],
  },
]

// https://vitepress.dev/reference/site-config
export default defineConfig({
  base: '/',
  title: 'FastapiAdmin',
  description: '基于 FastAPI + Vue3 + TypeScript 构建的企业级中后台解决方案,AI 驱动的全栈开发平台。',
  srcDir: 'src',
  outDir: 'dist',
  lang: 'zh-CN',
  lastUpdated: true,
  cleanUrls: true,
  metaChunk: true,
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/logo.svg?v=3' }],
    ['link', { rel: 'shortcut icon', href: '/favicon.ico?v=3' }],
  ],
  themeConfig: {
    search: {
      provider: 'local',
      options: {
        locales: {
          root: {
            translations: {
              button: { buttonText: '搜索文档', buttonAriaLabel: '搜索文档' },
              modal: {
                footer: {
                  selectText: '选择',
                  navigateText: '切换',
                  closeText: '关闭',
                },
              },
            },
          },
          en: {
            translations: {
              button: { buttonText: 'Search Documentation', buttonAriaLabel: 'Search Documentation' },
              modal: {
                footer: {
                  selectText: 'Select',
                  navigateText: 'Navigate',
                  closeText: 'Close',
                },
              },
            },
          },
        },
      },
    },
  },

  locales: {
    root: {
      label: '简体中文',
      lang: 'zh-CN',
      link: '/',
      themeConfig: {
        logo: '/logo.svg',
        nav: [
          { text: '首页', link: '/' },
          { text: '产品能力', link: '/#features' },
          {
            text: '快速开始',
            items: [
              { text: '项目概述', link: '/guide/overview' },
              { text: '为什么选择 FastapiAdmin？', link: '/guide/why' },
              { text: '快速开始', link: '/guide/start' },
            ],
          },
          {
            text: '开发指南',
            items: [
              { text: '前端开发指南', link: '/guide/frontend' },
              { text: '后端开发指南', link: '/guide/backend' },
              { text: '移动端开发指南', link: '/guide/miniprogram' },
              { text: '开发规范', link: '/guide/guidelines' },
            ],
          },
          {
            text: '部署与发布',
            items: [
              { text: '部署指南', link: '/guide/deployment' },
              { text: '更新日志', link: '/guide/changelog' },
            ],
          },
          { text: '更新日志', link: '/guide/changelog', activeMatch: '^/guide/changelog' },
          { text: '关于', link: '/about/about', activeMatch: '^/about/' },
        ],
        sidebar: {
          '/guide/': zhGuideSidebar,
        },
        socialLinks: [
          { icon: 'github', link: 'https://github.com/fastapiadmin/FastapiAdmin' },
          { icon: 'gitee', link: 'https://gitee.com/fastapiadmin/FastapiAdmin'},
          { icon: { svg: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="1.8" fill="currentColor" stroke="none"/><ellipse cx="12" cy="12" rx="10" ry="4.3"/><ellipse cx="12" cy="12" rx="10" ry="4.3" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4.3" transform="rotate(120 12 12)"/></svg>' }, link: 'https://atomgit.com/fastapiadmin/FastapiAdmin', ariaLabel: 'AtomGit' },
        ],
        outline: {
            level: [2, 3],
            label: "页面导航",
        },
        lastUpdated: {
            text: "最后更新于",
            formatOptions: {
                dateStyle: "short",
                timeStyle: "short",
            },
        },
        langMenuLabel: "多语言",
        returnToTopLabel: "回到顶部",
        sidebarMenuLabel: "菜单",
        darkModeSwitchLabel: "主题",
        lightModeSwitchTitle: "切换到浅色模式",
        darkModeSwitchTitle: "切换到深色模式",
      },
    },
    en: {
      label: 'English',
      lang: 'en',
      link: '/en/',
      themeConfig: {
        logo: '/logo.svg',
        nav: [
          { text: 'Home', link: '/en/' },
          { text: 'Capabilities', link: '/en/#features' },
          {
            text: 'Quick Start',
            items: [
              { text: 'Project Overview', link: '/en/guide/overview' },
              { text: 'Why FastapiAdmin?', link: '/en/guide/why' },
              { text: 'Quick Start', link: '/en/guide/start' },
            ],
          },
          {
            text: 'Development',
            items: [
              { text: 'Frontend Development Guide', link: '/en/guide/frontend' },
              { text: 'Backend Development Guide', link: '/en/guide/backend' },
              { text: 'Miniprogram Development Guide', link: '/en/guide/miniprogram' },
              { text: 'Development Guidelines', link: '/en/guide/guidelines' },
            ],
          },
          {
            text: 'Deployment & Releases',
            items: [
              { text: 'Deployment Guide', link: '/en/guide/deployment' },
              { text: 'Changelog', link: '/en/guide/changelog' },
            ],
          },
          { text: 'Changelog', link: '/en/guide/changelog', activeMatch: '^/en/guide/changelog' },
          { text: 'About', link: '/en/about/about', activeMatch: '^/en/about/' },
        ],
        sidebar: {
          '/en/guide/': enGuideSidebar,
        },
        socialLinks: [
          { icon: 'github', link: 'https://github.com/fastapiadmin/FastapiAdmin' },
          { icon: 'gitee', link: 'https://gitee.com/fastapiadmin/FastapiAdmin' },
          { icon: { svg: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="1.8" fill="currentColor" stroke="none"/><ellipse cx="12" cy="12" rx="10" ry="4.3"/><ellipse cx="12" cy="12" rx="10" ry="4.3" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4.3" transform="rotate(120 12 12)"/></svg>' }, link: 'https://atomgit.com/fastapiadmin/FastapiAdmin', ariaLabel: 'AtomGit' },
        ],
        outline: {
          level: [2, 3],
          label: 'On This Page',
        },
        lastUpdated: {
          text: 'Last updated',
          formatOptions: {
            dateStyle: 'short',
            timeStyle: 'short',
          },
        },
        langMenuLabel: 'Languages',
        returnToTopLabel: 'Return to top',
        sidebarMenuLabel: 'Menu',
        darkModeSwitchLabel: 'Theme',
        lightModeSwitchTitle: 'Switch to light theme',
        darkModeSwitchTitle: 'Switch to dark theme',
      },
    },
  },
})
