import { defineConfig } from 'vitepress'

export default defineConfig({
    base: '/',
    srcDir: 'src',
    outDir: './dist',
    title: 'FastApiAdmin',
    description: '⚡️ 现代、开源、全栈融合的中后台快速开发平台',
    ignoreDeadLinks: [
        'http://localhost:8000/docs',
        'http://localhost:5173',
        'http://localhost:8001/api/v1/docs',
        'http://localhost:8001/api/v1/redoc'
    ],
    vite: {
        build: {
            chunkSizeWarningLimit: 1000,
            rollupOptions: {
                output: {
                    manualChunks(id) {
                        if (id.includes('node_modules')) {
                            if (id.includes('vue')) {
                                return 'vue-vendor'
                            }
                            if (id.includes('vitepress')) {
                                return 'vitepress-vendor'
                            }
                            return 'vendor'
                        }
                    }
                }
            }
        }
    },
    head: [
        ["link",{rel: "apple-touch-icon", sizes: "180x180", href: "/favicon.png"}],
        ["link",{rel: "icon",type: "image/png", sizes: "32x32", href: "/favicon.png"}],
        ["link",{rel: "icon",type: "image/png", sizes: "16x16", href: "/favicon.png"}],
        ["link",{rel: "shortcut icon", href: "/favicon.png"}],
        ["meta",{name: "description", content: "FastApiAdmin - 现代、开源、全栈融合的快速开发平台，基于 FastAPI + Vue3 + TypeScript 构建的企业级中后台解决方案"}],
        ["meta",{name: "keywords", content: "FastAPI, Vue3, TypeScript, 中后台, 快速开发, 企业级, 全栈, 开源"}],
        ["meta",{name: "author", content: "FastapiAdmin Team"}],
        ["meta",{property: "og:title", content: "FastApiAdmin - 现代、开源、全栈融合的快速开发平台"}],
        ["meta",{property: "og:description", content: "基于 FastAPI + Vue3 + TypeScript 构建的企业级中后台解决方案，支持多端开发"}],
        ["meta",{property: "og:image", content: "/logo.png"}],
        ["meta",{property: "og:url", content: "https://service.fastapiadmin.com"}],
        ["meta",{property: "og:type", content: "website"}],
        ["meta",{name: "twitter:card", content: "summary_large_image"}],
        ["meta",{name: "twitter:title", content: "FastApiAdmin - 现代、开源、全栈融合的快速开发平台"}],
        ["meta",{name: "twitter:description", content: "基于 FastAPI + Vue3 + TypeScript 构建的企业级中后台解决方案，支持多端开发"}],
        ["meta",{name: "twitter:image", content: "/logo.png"}],
        ["link",{rel: "canonical", href: "https://service.fastapiadmin.com"}]
    ],
    locales: {
        root: {
            label: '简体中文',
            lang: 'zh',
            link: '/',
            description: '现代、开源、全栈融合的中后台快速开发平台',
            themeConfig: {
                nav: [
                    { text: '首页', link: '/' },
                    {
                        text: '指南',
                        items: [
                            { text: '项目概述', link: '/guide/overview' },
                            { text: '快速开始', link: '/guide/start' },
                            { text: '为什么选择FastapiAdmin?', link: '/guide/why' },
                            { text: '前端开发', link: '/guide/frontend' },
                            { text: '后端开发', link: '/guide/backend' },
                            { text: '移动端开发', link: '/guide/miniprogram' },
                            { text: '开发规范', link: '/guide/guidelines' },
                            { text: '示例', link: '/guide/examples' },
                            { text: '自定义开发', link: '/guide/custom-development' },
                            { text: '部署指南', link: '/guide/deployment' },
                            { text: 'API文档说明', link: '/guide/api-docs' }
                        ]
                    },
                    {
                        text: '版本',
                        items: [
                            { text: 'master', link: 'https://github.com/fastapiadmin/FastapiAdmin', target: '_blank' },
                            { text: 'V2.0.0', link: 'https://github.com/fastapiadmin/FastapiAdmin/tree/v2.0.0', target: '_blank' },
                            { text: 'V1.0.0', link: 'https://github.com/fastapiadmin/FastapiAdmin/tree/v1.0.0', target: '_blank' }
                        ]
                    },
                    { text: '他们在使用', link: '/about/users' },
                    { text: '赞助', link: '/about/sponsor' },
                    { text: '贡献指南', link: '/about/contributing' },
                    { text: '关于我们', link: '/about/about' },
                ],
                sidebar: [
                    {
                        text: '指南',
                        collapsed: false,
                        items: [
                            { text: '项目概述', link: '/guide/overview' },
                            { text: '快速开始', link: '/guide/start' },
                            { text: '为什么选择FastapiAdmin?', link: '/guide/why' },
                            { text: '前端开发', link: '/guide/frontend' },
                            { text: '后端开发', link: '/guide/backend' },
                            { text: '移动端开发', link: '/guide/miniprogram' },
                            { text: '开发规范', link: '/guide/guidelines' },
                            { text: '示例', link: '/guide/examples' },
                            { text: '自定义开发', link: '/guide/custom-development' },
                            { text: '部署指南', link: '/guide/deployment' },
                            { text: 'API文档说明', link: '/guide/api-docs' }
                        ]
                    },
                    {
                        text: '关于',
                        items: [
                            { text: '他们在使用', link: '/about/users' },
                            { text: '所有用户', link: '/about/users-all' },
                            { text: '赞助', link: '/about/sponsor' },
                            { text: '贡献指南', link: '/about/contributing' },
                            { text: '关于我们', link: '/about/about' },
                        ]
                    }
                ],
                footer: {
                    message: '<a href="https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE" target="_blank">MIT License</a>',
                    copyright: 'Copyright © 2025-2026 service.fastapiadmin.com 版权所有 |隐私 |条款 陕ICP备2025069493号-1'
                },
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
                darkModeSwitchTitle: "切换到深色模式"
            }
        },
        en: {
            label: 'English',
            lang: 'en',
            link: '/en/',
            description: 'Modern, open-source, full-stack integrated backend rapid development platform',
            themeConfig: {
                nav: [
                    { text: 'Home', link: '/en/' },
                    {
                        text: 'Guide',
                        items: [
                            { text: 'Overview', link: '/en/guide/overview' },
                            { text: 'Quick Start', link: '/en/guide/start' },
                            { text: 'Why FastapiAdmin?', link: '/en/guide/why' },
                            { text: 'Frontend', link: '/en/guide/frontend' },
                            { text: 'Backend', link: '/en/guide/backend' },
                            { text: 'Mini Program', link: '/en/guide/miniprogram' },
                            { text: 'Guidelines', link: '/en/guide/guidelines' },
                            { text: 'Examples', link: '/en/guide/examples' },
                            { text: 'Custom Development', link: '/en/guide/custom-development' },
                            { text: 'Deployment', link: '/en/guide/deployment' },
                            { text: 'API Docs', link: '/en/guide/api-docs' }
                        ]
                    },
                    {
                        text: 'Versions',
                        items: [
                            { text: 'master', link: 'https://github.com/fastapiadmin/FastapiAdmin', target: '_blank' },
                            { text: 'V2.0.0', link: 'https://github.com/fastapiadmin/FastapiAdmin/tree/v2.0.0', target: '_blank' },
                            { text: 'V1.0.0', link: 'https://github.com/fastapiadmin/FastapiAdmin/tree/v1.0.0', target: '_blank' }
                        ]
                    },
                    { text: 'Who is Using', link: '/en/about/users' },
                    { text: 'Sponsor', link: '/en/about/sponsor' },
                    { text: 'Contributing Guide', link: '/en/about/contributing' },
                    { text: 'About Us', link: '/en/about/about' },
                ],
                sidebar: [
                    {
                        text: 'Guide',
                        collapsed: false,
                        items: [
                            { text: 'Overview', link: '/en/guide/overview' },
                            { text: 'Quick Start', link: '/en/guide/start' },
                            { text: 'Why FastapiAdmin?', link: '/en/guide/why' },
                            { text: 'Frontend', link: '/en/guide/frontend' },
                            { text: 'Backend', link: '/en/guide/backend' },
                            { text: 'Mini Program', link: '/en/guide/miniprogram' },
                            { text: 'Guidelines', link: '/en/guide/guidelines' },
                            { text: 'Examples', link: '/en/guide/examples' },
                            { text: 'Custom Development', link: '/en/guide/custom-development' },
                            { text: 'Deployment', link: '/en/guide/deployment' },
                            { text: 'API Docs', link: '/en/guide/api-docs' }
                        ]
                    },
                    {
                        text: 'About',
                        items: [
                            { text: 'Who is Using', link: '/en/about/users' },
                            { text: 'All Users', link: '/en/about/users-all' },
                            { text: 'Sponsor', link: '/en/about/sponsor' },
                            { text: 'Contributing Guide', link: '/en/about/contributing' },
                            { text: 'About Us', link: '/en/about/about' },
                        ]
                    }
                ],
                footer: {
                    message: '<a href="https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE" target="_blank">MIT License</a>',
                    copyright: 'Copyright © 2025-2026 service.fastapiadmin.com All Rights Reserved | Privacy | Terms ICP: Shaanxi 2025069493-1'
                },
                outline: {
                    level: [2, 3],
                    label: "On this page",
                },
                lastUpdated: {
                    text: "Last updated",
                    formatOptions: {
                        dateStyle: "short",
                        timeStyle: "short",
                    },
                },
                langMenuLabel: "Languages",
                returnToTopLabel: "Return to top",
                sidebarMenuLabel: "Menu",
                darkModeSwitchLabel: "Theme",
                lightModeSwitchTitle: "Switch to light mode",
                darkModeSwitchTitle: "Switch to dark mode"
            }
        },
    },
    lastUpdated: true,
    metaChunk: true,
    themeConfig: {
        logo: '/logo.png',
        socialLinks: [
            { icon: 'github', link: 'https://github.com/fastapiadmin/FastapiAdmin' },
            { icon: 'gitee', link: 'https://gitee.com/fastapiadmin/FastapiAdmin' },
            { icon: 'gitcode', link: 'https://gitcode.com/qq_36002987/FastapiAdmin' }
        ],
        search: {
            provider: 'local',
            options: {
                locales: {
                    root: {
                        translations: {
                            button: {
                                buttonText: '搜索文档',
                                buttonAriaLabel: '搜索文档'
                            },
                            modal: {
                                footer: {
                                    selectText: '选择',
                                    navigateText: '切换',
                                    closeText: '关闭',
                                },
                                noResultsText: '没有找到相关结果',
                                resetButtonTitle: '清除搜索词',
                                backButtonTitle: '返回',
                            },
                        },
                    },
                    en: {
                        translations: {
                            button: {
                                buttonText: 'Search',
                                buttonAriaLabel: 'Search documentation'
                            },
                            modal: {
                                footer: {
                                    selectText: 'Select',
                                    navigateText: 'Navigate',
                                    closeText: 'Close',
                                },
                                noResultsText: 'No results found',
                                resetButtonTitle: 'Clear search',
                                backButtonTitle: 'Back',
                            },
                        },
                    },
                },
                detailedView: true
            },
        }
    },
})
