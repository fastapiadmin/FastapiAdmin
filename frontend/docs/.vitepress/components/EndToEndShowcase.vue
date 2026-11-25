<template>
  <section class="endtoend-section" :aria-label="t.label">
    <div class="endtoend-inner">
      <div class="endtoend-header">
        <span class="endtoend-eyebrow">{{ t.eyebrow }}</span>
        <h2 class="endtoend-title">{{ t.title }}</h2>
        <p class="endtoend-subtitle">{{ t.subtitle }}</p>
      </div>

      <div
        v-for="(step, i) in steps"
        :key="step.id"
        :id="step.anchor"
        class="endtoend-step"
        :class="[
          'endtoend-step--' + (i % 2 === 0 ? 'left' : 'right'),
          step.imageKind === 'mobile' ? 'endtoend-step--mobile' : '',
        ]"
      >
        <div class="endtoend-step-content">
          <span class="endtoend-step-num">{{ t.stepLabel }} {{ String(i + 1).padStart(2, '0') }}</span>
          <h3 class="endtoend-step-title">{{ step.title }}</h3>
          <p class="endtoend-step-desc">{{ step.desc }}</p>
          <ul class="endtoend-step-features">
            <li v-for="(f, j) in step.features" :key="j">
              <svg
                class="endtoend-step-check"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2.5"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
              >
                <path d="M20 6L9 17l-5-5" />
              </svg>
              <span>{{ f }}</span>
            </li>
          </ul>
        </div>

        <!-- 该阶段全部产品截图(点击放大,灯箱内可前后切换) -->
        <div class="endtoend-step-images" :class="{ 'is-multi': step.images.length > 1 }">
          <button
            v-for="(img, j) in step.images"
            :key="img.src"
            type="button"
            class="endtoend-step-image-wrap"
            @click="openLightbox(step, j)"
            :aria-label="(isEn ? 'View ' : '查看 ') + img.alt"
          >
            <img :src="img.src" :alt="img.alt" loading="lazy" decoding="async" />
          </button>
        </div>
      </div>

      <ImageLightbox
        :visible="lightboxVisible"
        :src="lightboxSrc"
        :alt="lightboxAlt"
        :current-index="lightboxIndex"
        :total="lightboxTotal"
        @close="lightboxVisible = false"
        @prev="lightboxPrev"
        @next="lightboxNext"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref, defineAsyncComponent } from 'vue'
import { useData } from 'vitepress'
// 灯箱异步加载 — 用户点击图片才弹出,不占首屏
const ImageLightbox = defineAsyncComponent(() => import('./ImageLightbox.vue'))

const { lang } = useData()
const isEn = computed(() => lang.value === 'en')

interface StepImage {
  src: string
  alt: string
}

interface Step {
  id: number
  /** 锚点 id(SectionNav 导航点) */
  anchor: string
  title: string
  desc: string
  features: string[]
  images: StepImage[]
  /** "mobile" = 移动端竖屏截图,等宽横排;其他桌面截图按内容比例展示 */
  imageKind?: 'mobile' | 'desktop'
}

const t = computed(() =>
  isEn.value
    ? {
        label: 'End-to-End Showcase',
        eyebrow: 'Full-Stack, End-to-End',
        title: 'One Stack, All Surfaces',
        subtitle:
          'Web management, AI code generation, FastAPI async backend and UniApp mobile — one codebase, one design system, shipped together.',
        stepLabel: 'Stage',
      }
    : {
        label: '全栈贯通',
        eyebrow: '全栈贯通',
        title: '一套代码,全端覆盖',
        subtitle:
          'Web 管理后台、AI 代码生成、FastAPI 异步后端与 UniApp 移动端，一套代码、一套设计系统、一起交付。',
        stepLabel: '阶段',
      }
)

const steps = computed<Step[]>(() =>
  isEn.value
    ? [
        {
          id: 1,
          anchor: 'end-to-end-web',
          title: 'Web Management',
          desc: 'A complete admin shell: dashboard, RBAC, CRUD, audit logs and 30+ business modules. Vue3 + TypeScript + Element Plus, no scaffolding.',
          features: [
            'Dashboard with live metrics',
            'Menu / button / data-level RBAC',
            'Audit logs + operation history',
          ],
          images: [
            { src: '/showcase/dashboard.webp', alt: 'FastApiAdmin Web Dashboard' },
            { src: '/showcase/ai.webp', alt: 'AI Assistant built into the admin console' },
          ],
        },
        {
          id: 2,
          anchor: 'end-to-end-gen',
          title: 'AI Code Generator',
          desc: 'Pick a database table → AI generates Controller / Service / Model / Vue pages. CRUD in seconds, not days.',
          features: [
            'Schema-aware code generation',
            'Pydantic + TypeScript types',
            'One-click export to repo',
          ],
          images: [
            { src: '/showcase/gencode.webp', alt: 'AI Code Generator Interface' },
          ],
        },
        {
          id: 3,
          anchor: 'end-to-end-api',
          title: 'FastAPI Async Backend',
          desc: 'Native async/await end-to-end. Pydantic auto-validation, SQLAlchemy 2.0, Redis caching, JWT + OAuth2.',
          features: [
            'Async/await all the way down',
            'Auto OpenAPI 3.1 docs',
            'JWT + OAuth2 + RBAC',
          ],
          images: [
            { src: '/showcase/login.webp', alt: 'Login with puzzle verification and API auth' },
          ],
        },
        {
          id: 4,
          anchor: 'end-to-end-app',
          title: 'UniApp Mobile',
          desc: 'One codebase, four targets. UniApp + Vue3 + Wot Design → H5, WeChat / Alipay mini programs and native App, with shared auth and dark mode.',
          features: [
            'Single codebase → 4 platforms',
            'Built-in mobile RBAC',
            'Real-time push notifications',
          ],
          imageKind: 'mobile',
          images: [
            { src: '/showcase/app_home.png', alt: 'FastApiAdmin Mobile Home' },
            { src: '/showcase/app_login.png', alt: 'FastApiAdmin Mobile Login' },
            { src: '/showcase/app_mine.png', alt: 'FastApiAdmin Mobile Profile' },
          ],
        },
      ]
    : [
        {
          id: 1,
          anchor: 'end-to-end-web',
          title: 'Web 管理后台',
          desc: '完整管理壳：仪表盘、RBAC、CRUD、审计日志与 30+ 业务模块。Vue3 + TypeScript + Element Plus，克隆即跑，零脚手架。',
          features: [
            '仪表盘 + 实时业务指标',
            '菜单 / 按钮 / 数据三级 RBAC',
            '操作日志 + 审计追踪',
          ],
          images: [
            { src: '/showcase/dashboard.webp', alt: 'FastApiAdmin Web 管理后台' },
            { src: '/showcase/ai.webp', alt: '内置 AI 智能助手' },
          ],
        },
        {
          id: 2,
          anchor: 'end-to-end-gen',
          title: 'AI 代码生成器',
          desc: '选表 → 自动生成 Controller / Service / Model / Vue 页面与类型定义，CRUD 从几天缩短到几秒。',
          features: [
            '数据库 schema 智能识别',
            'Pydantic + TypeScript 类型同步',
            '一键导出到代码仓库',
          ],
          images: [
            { src: '/showcase/gencode.webp', alt: 'AI 代码生成器界面' },
          ],
        },
        {
          id: 3,
          anchor: 'end-to-end-api',
          title: 'FastAPI 异步后端',
          desc: '原生 async/await 全链路。Pydantic 自动校验,SQLAlchemy 2.0,Redis 缓存,JWT + OAuth2 认证。',
          features: [
            '全异步 async/await',
            '自动生成 OpenAPI 3.1 文档',
            'JWT + OAuth2 + RBAC',
          ],
          images: [
            { src: '/showcase/login.webp', alt: '登录、拼图验证与 API 认证' },
          ],
        },
        {
          id: 4,
          anchor: 'end-to-end-app',
          title: 'UniApp 移动端',
          desc: '一套代码、4 个目标端。UniApp + Vue3 + Wot Design → H5 / 微信小程序 / 支付宝小程序 / 原生 App，登录、权限与暗色模式同源。',
          features: [
            '一套代码 4 个平台',
            '内置移动端 RBAC',
            '实时消息推送',
          ],
          imageKind: 'mobile',
          images: [
            { src: '/showcase/app_home.png', alt: 'FastApiAdmin 移动端首页' },
            { src: '/showcase/app_login.png', alt: 'FastApiAdmin 移动端登录' },
            { src: '/showcase/app_mine.png', alt: 'FastApiAdmin 个人中心' },
          ],
        },
      ]
)

/* Lightbox — 在触发阶段(step)的截图组内循环切换 */
const lightboxVisible = ref(false)
const lightboxIndex = ref(0)
const lightboxImages = ref<StepImage[]>([])

const lightboxSrc = computed(() => lightboxImages.value[lightboxIndex.value]?.src ?? '')
const lightboxAlt = computed(() => lightboxImages.value[lightboxIndex.value]?.alt ?? '')
const lightboxTotal = computed(() => lightboxImages.value.length)

const openLightbox = (step: Step, index: number) => {
  lightboxImages.value = step.images
  lightboxIndex.value = index
  lightboxVisible.value = true
}

const lightboxPrev = () => {
  const total = lightboxTotal.value
  if (!total) return
  lightboxIndex.value = (lightboxIndex.value - 1 + total) % total
}

const lightboxNext = () => {
  const total = lightboxTotal.value
  if (!total) return
  lightboxIndex.value = (lightboxIndex.value + 1) % total
}
</script>

<style scoped>
/* ============================================================================
 * EndToEndShowcase — Linear 风格 S 型 alternate 布局
 * 4 段(偶数:内容在左,图在右;奇数:图在左,内容在右)
 * 每段配齐该阶段全部产品截图,每个阶段对应一个锚点(SectionNav)
 * 移动端 (≤960px) 全部堆叠成 vertical flow
 * ============================================================================ */

.endtoend-section {
  position: relative;
  z-index: 20;
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--vp-section-padding);
  overflow: hidden;
}

.endtoend-header {
  text-align: center;
  margin-bottom: 5rem;
}

.endtoend-eyebrow {
  display: block;
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--vp-eyebrow-color);
  margin-bottom: 0.6rem;
}

.endtoend-title {
  text-wrap: balance;
  word-break: keep-all;
  overflow-wrap: anywhere;
  font-size: var(--vp-section-title-size);
  font-weight: 800;
  background: var(--vp-brand-gradient);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin-bottom: 0.8rem;
  line-height: 1.3;
}

.endtoend-subtitle {
  font-size: 1.05rem;
  color: var(--vp-home-text-2);
  max-width: 640px;
  margin: 0 auto;
  line-height: 1.6;
}

/* ── Step alternate layout ── */
.endtoend-step {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  margin-bottom: 6rem;
  /* 锚点滚动时避开 VitePress sticky nav */
  scroll-margin-top: 96px;
}

.endtoend-step:last-child {
  margin-bottom: 0;
}

/* 奇数段(i=1,3) — images 在左,content 在右 */
.endtoend-step--right .endtoend-step-images {
  order: 1;
}
.endtoend-step--right .endtoend-step-content {
  order: 2;
}

/* ── Content side ── */
.endtoend-step-num {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--vp-brand-accent);
  background: rgba(109, 91, 255, 0.12);
  padding: 0.35rem 0.75rem;
  border-radius: 9999px;
  margin-bottom: 1rem;
  border: 1px solid rgba(109, 91, 255, 0.25);
}

.endtoend-step-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--vp-home-text-1);
  margin-bottom: 0.8rem;
  line-height: 1.3;
}

.endtoend-step-desc {
  font-size: 1rem;
  color: var(--vp-home-text-2);
  line-height: 1.7;
  margin-bottom: 1.5rem;
}

.endtoend-step-features {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.endtoend-step-features li {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.92rem;
  color: var(--vp-home-text-2);
  line-height: 1.5;
}

.endtoend-step-check {
  flex-shrink: 0;
  width: 1.1rem;
  height: 1.1rem;
  color: var(--vp-status-shipped, #10b981);
}

/* ── Images side ── */
.endtoend-step-images {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  align-items: stretch;
}

/* 单图:占满整列 */
.endtoend-step-images:not(.is-multi) {
  grid-template-columns: 1fr;
}

.endtoend-step-image-wrap {
  position: relative;
  display: block;
  width: 100%;
  padding: 0;
  border: 1px solid var(--vp-home-card-border);
  border-radius: var(--vp-radius-xl);
  overflow: hidden;
  background: var(--vp-home-card-bg);
  cursor: pointer;
  text-align: left;
  box-shadow:
    0 24px 60px rgba(79, 107, 255, 0.18),
    0 8px 20px rgba(0, 0, 0, 0.08);
  transition:
    transform 0.5s var(--vp-ease-emphasis, cubic-bezier(0.34, 1.56, 0.64, 1)),
    box-shadow 0.5s ease;
}

/* 边框渐变描边(Layered gradient border) */
.endtoend-step-image-wrap::before {
  content: '';
  position: absolute;
  inset: -1px;
  border-radius: var(--vp-radius-xl);
  padding: 1px;
  background: linear-gradient(135deg, rgba(109, 91, 255, 0.4), transparent 50%, rgba(79, 107, 255, 0.3));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.endtoend-step-image-wrap:focus-visible {
  outline: 2px solid var(--vp-brand-accent);
  outline-offset: 2px;
}

.endtoend-step-image-wrap:hover {
  transform: translateY(-4px);
  box-shadow:
    0 32px 80px rgba(79, 107, 255, 0.28),
    0 12px 30px rgba(0, 0, 0, 0.12);
}

.endtoend-step-images img {
  display: block;
  width: 100%;
  aspect-ratio: 16 / 10;
  object-fit: cover;
}

/* 移动端阶段:竖屏截图等宽横排(真机比例,不裁切) */
.endtoend-step--mobile .endtoend-step-images {
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
}

.endtoend-step--mobile .endtoend-step-images img {
  aspect-ratio: auto;
  height: auto;
  object-fit: contain;
}

/* 标题下的 brand 渐变强调线 */
.endtoend-header .endtoend-title {
  position: relative;
}

.endtoend-header .endtoend-title::after {
  content: '';
  display: block;
  width: 60px;
  height: 3px;
  margin: 0.8rem auto 0;
  background: var(--vp-brand-gradient);
  border-radius: 2px;
  opacity: 0.65;
  transition: width 0.4s var(--vp-ease-emphasis, cubic-bezier(0.34, 1.56, 0.64, 1));
}

.endtoend-header:hover .endtoend-title::after {
  width: 80px;
}

@media (max-width: 960px) {
  .endtoend-section {
    padding: var(--vp-section-padding-mobile);
  }

  .endtoend-step {
    grid-template-columns: 1fr;
    gap: 2rem;
    margin-bottom: 4rem;
  }

  /* 移动端:图片置顶,内容置底 */
  .endtoend-step--right .endtoend-step-images,
  .endtoend-step--left .endtoend-step-images {
    order: 1;
  }
  .endtoend-step--right .endtoend-step-content,
  .endtoend-step--left .endtoend-step-content {
    order: 2;
  }

  /* 桌面截图在小屏堆叠,手机截图仍横排 */
  .endtoend-step-images {
    grid-template-columns: 1fr;
  }
  .endtoend-step--mobile .endtoend-step-images {
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
  }

  .endtoend-step-title {
    font-size: 1.4rem;
  }

  .endtoend-header {
    margin-bottom: 3rem;
  }
}

@media (max-width: 640px) {
  .endtoend-step--mobile .endtoend-step-images {
    gap: 0.375rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .endtoend-step-image-wrap {
    transition: none;
  }
}
</style>
