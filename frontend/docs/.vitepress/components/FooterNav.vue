<template>
  <footer class="footer-nav" :aria-label="t.footerLabel" :data-mode="mode">
    <div class="fn-content">
      <div class="fn-section fn-brand">
        <div class="fn-section-title">FastApiAdmin</div>
        <p v-if="mode === 'full'" class="fn-section-desc">
          {{ description }}
        </p>
        <div class="fn-social">
          <a href="https://github.com/fastapiadmin/FastapiAdmin" target="_blank" rel="noreferrer" class="fn-social-link" :title="t.github">
            <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
          </a>
          <a href="https://gitee.com/fastapiadmin/FastapiAdmin" target="_blank" rel="noreferrer" class="fn-social-link" :title="t.gitee">
            <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M11.984 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.016 0zm6.09 5.333c.328 0 .593.266.593.593v1.482a.594.594 0 0 1-.593.593H9.777c-.982 0-1.778.796-1.778 1.778v5.63c0 .327.266.592.593.592h1.482c.327 0 .593-.265.593-.592v-4.445h6.667c.327 0 .593.265.593.593v1.482a.594.594 0 0 1-.593.593h-4.445v1.63c0 1.963-1.595 3.557-3.56 3.557H6.67a.594.594 0 0 1-.593-.593V9.778c0-2.456 1.995-4.445 4.445-4.445h5.552z"/></svg>
          </a>
          <a href="https://atomgit.com/fastapiadmin/FastapiAdmin" target="_blank" rel="noreferrer" class="fn-social-link" :title="t.atomgit">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">
              <circle cx="12" cy="12" r="1.8" fill="currentColor" stroke="none" />
              <ellipse cx="12" cy="12" rx="10" ry="4.3" />
              <ellipse cx="12" cy="12" rx="10" ry="4.3" transform="rotate(60 12 12)" />
              <ellipse cx="12" cy="12" rx="10" ry="4.3" transform="rotate(120 12 12)" />
            </svg>
          </a>
        </div>
      </div>

      <nav
        v-if="mode === 'full'"
        v-for="col in linkColumns"
        :key="col.title"
        class="fn-section"
        :aria-label="col.title"
      >
        <div class="fn-section-title">{{ col.title }}</div>
        <ul class="fn-link-list">
          <li v-for="link in col.links" :key="link.name">
            <a
              :href="link.href"
              :target="link.href.startsWith('http') ? '_blank' : undefined"
              rel="noopener noreferrer"
              class="fn-link"
            >{{ link.name }}</a>
          </li>
        </ul>
      </nav>
    </div>

    <div v-if="mode === 'full'" class="fn-separator" aria-hidden="true"></div>

    <div class="fn-bottom">
      <div class="fn-bottom-left">
        <span>Copyright © 2025-{{ currentYear }} service.fastapiadmin.com</span>
        <span>
          <a href="https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE" target="_blank" rel="noreferrer" class="fn-link">MIT License</a>
        </span>
        <template v-if="!isEn">
          <span class="fn-bottom-sep" aria-hidden="true">|</span>
          <span>陕ICP备2025069493号-1</span>
        </template>
      </div>
      <span>
        <!-- ✅ R5 P1-13:Footer 改 SaaS 化 — 删"Made with ❤ by Team"小作坊感 -->
        <template v-if="!isEn">本站基于 VitePress 构建 · MIT 协议开源</template>
        <template v-else>Built with VitePress · Open source under MIT License</template>
      </span>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useData } from 'vitepress'

type FooterMode = 'full' | 'minimal'

withDefaults(defineProps<{ mode?: FooterMode }>(), { mode: 'full' })

const currentYear = new Date().getFullYear()
const { lang } = useData()
const isEn = computed(() => lang.value === 'en')

interface LinkItem { name: string; href: string }
interface LinkColumn { title: string; links: LinkItem[] }

const zhColumns: LinkColumn[] = [
  {
    title: '快速开始',
    links: [
      { name: '为什么选择我们？', href: '/guide/why' },
      { name: '项目概述', href: '/guide/overview' },
      { name: '快速开始', href: '/guide/start' },
      { name: '前端开发', href: '/guide/frontend' },
      { name: '后端开发', href: '/guide/backend' },
    ],
  },
  {
    title: '生态系统',
    links: [
      { name: '移动端开发', href: '/guide/miniprogram' },
      { name: 'API 文档', href: '/guide/api-docs' },
      { name: '操作手册', href: '/guide/operation' },
      { name: '示例', href: '/guide/examples' },
      { name: '更新日志', href: '/guide/changelog' },
    ],
  },
  {
    title: '更多',
    links: [
      { name: '开发规范', href: '/guide/guidelines' },
      { name: '部署指南', href: '/guide/deployment' },
      { name: '二开教程', href: '/guide/custom-development' },
      { name: '关于我们', href: '/about/about' },
    ],
  },
]

const enColumns: LinkColumn[] = [
  {
    title: 'Get Started',
    links: [
      { name: 'Why FastApiAdmin?', href: '/en/guide/why' },
      { name: 'Overview', href: '/en/guide/overview' },
      { name: 'Quick Start', href: '/en/guide/start' },
      { name: 'Frontend', href: '/en/guide/frontend' },
      { name: 'Backend', href: '/en/guide/backend' },
    ],
  },
  {
    title: 'Ecosystem',
    links: [
      { name: 'Mobile Development', href: '/en/guide/miniprogram' },
      { name: 'API Docs', href: '/en/guide/api-docs' },
      { name: 'User Manual', href: '/en/guide/operation' },
      { name: 'Examples', href: '/en/guide/examples' },
      { name: 'Changelog', href: '/en/guide/changelog' },
    ],
  },
  {
    title: 'More',
    links: [
      { name: 'Guidelines', href: '/en/guide/guidelines' },
      { name: 'Deployment', href: '/en/guide/deployment' },
      { name: 'Custom Dev', href: '/en/guide/custom-development' },
      { name: 'About', href: '/en/about/about' },
    ],
  },
]

const description = computed(() =>
  isEn.value
    ? 'Enterprise-grade admin platform built with FastAPI + Vue3 + TypeScript. AI-powered full-stack development that fits your team’s workflow.'
    : '基于 FastAPI + Vue3 + TypeScript 构建的企业级中后台解决方案，AI 驱动的全栈开发平台。'
)

const t = computed(() => isEn.value
    ? {
        footerLabel: 'Site footer',
        github: 'GitHub',
        gitee: 'Gitee',
        atomgit: 'AtomGit',
      }
    : {
        footerLabel: '网站页脚',
        github: 'GitHub',
        gitee: '码云',
        atomgit: 'AtomGit',
      }
)

const linkColumns = computed(() => isEn.value ? enColumns : zhColumns)
</script>

<style scoped>
.footer-nav {
  position: relative;
  z-index: 20;
  padding: 3rem 1.5rem 1.5rem;
}

/* minimal 模式:about 页面专用 — 居中签名式布局,只展示 brand + social + 版权 */
.footer-nav[data-mode="minimal"] {
  padding: 2.5rem 1.5rem 1.5rem;
}

.footer-nav[data-mode="minimal"] .fn-content {
  justify-content: center;
  max-width: 520px;
  text-align: center;
  margin: 0 auto;
}

.footer-nav[data-mode="minimal"] .fn-brand {
  flex: 0 1 auto;
  min-width: 0;
  max-width: none;
  align-items: center;
}

.footer-nav[data-mode="minimal"] .fn-section-title,
.footer-nav[data-mode="minimal"] .fn-section-desc {
  text-align: center;
}

.footer-nav[data-mode="minimal"] .fn-social {
  justify-content: center;
}

.fn-content {
  display: flex;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  gap: 2rem;
  flex-wrap: wrap;
}

.fn-section {
  min-width: 140px;
  display: flex;
  flex-direction: column;
}

.fn-brand {
  flex: 1;
  min-width: 260px;
  max-width: 360px;
}

.fn-section-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--vp-home-text-1);
  margin-bottom: 1rem;
}

.fn-section-desc {
  font-size: 0.85rem;
  color: var(--vp-home-text-2);
  line-height: 1.65;
  margin-bottom: 1rem;
}

.fn-social {
  display: flex;
  gap: 0.75rem;
}

.fn-social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.75rem;  /* 44px WCAG 2.5.5 AAA */
  height: 2.75rem;
  border-radius: var(--vp-radius-sm);
  color: var(--vp-home-text-2);
  background: var(--vp-home-card-bg);
  border: 1px solid var(--vp-home-card-border);
  transition: transform 0.25s, background 0.2s, border-color 0.2s;
}

.fn-social-link:focus-visible {
  outline: var(--vp-focus-ring);
  outline-offset: var(--vp-focus-offset);
}

.fn-social-link svg {
  width: 1rem;
  height: 1rem;
}

.fn-social-link:hover {
  color: var(--vp-home-text-1);
  border-color: rgba(109, 91, 255, 0.35);
  background: var(--vp-home-card-hover-bg);
}

.fn-link-list {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}

.fn-link {
  color: var(--vp-home-text-2);
  font-size: 0.85rem;
  text-decoration: none;
  transition: color 0.2s ease;
}

.fn-link:hover {
  color: var(--vp-home-text-1);
}

.fn-heart {
  display: inline-block;
  width: 0.95em;
  height: 0.95em;
  vertical-align: -0.12em;
  color: #6D5BFF;
  margin: 0 0.15em;
}

.fn-separator {
  max-width: 1200px;
  margin: 2.5rem auto 1.5rem;
  border-top: 1px solid var(--vp-home-card-border);
}

.fn-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  color: var(--vp-home-text-3);
  font-size: 0.8rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.fn-bottom-left {
  display: flex;
  gap: 0.5rem;
}

.fn-bottom-sep {
  color: var(--vp-home-card-border);
}

@media (max-width: 768px) {
  .fn-content {
    flex-direction: column;
    gap: 2rem;
  }
  .fn-bottom {
    flex-direction: column;
    text-align: center;
  }
  .fn-bottom-left {
    flex-direction: column;
    gap: 0.3rem;
  }
}
</style>
