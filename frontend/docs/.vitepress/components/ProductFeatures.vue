<template>
  <section id="features" class="features">
    <div class="features__inner">
      <header class="features__head">
        <p class="features__eyebrow">{{ copy.eyebrow }}</p>
        <h2 class="features__title">{{ copy.title }}</h2>
        <p class="features__lead">{{ copy.lead }}</p>
        <a class="features__link" :href="isEn ? '/en/guide/start' : '/guide/start'">
          {{ copy.link }}
          <span aria-hidden="true">→</span>
        </a>
      </header>

      <div class="bento">
        <article
          v-for="card in cards"
          :key="card.key"
          class="bento-card"
          :class="`bento-card--${card.key}`"
        >
          <div class="bento-card__top">
            <span class="bento-card__icon" aria-hidden="true">
              <svg v-if="card.key === 'ai'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 3l1.7 5.1L19 10l-5.3 1.9L12 17l-1.7-5.1L5 10l5.3-1.9L12 3Z" />
                <path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8L19 15Z" />
              </svg>
              <svg v-else-if="card.key === 'api'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
                <path d="M8 9l-3 3 3 3M16 9l3 3-3 3M13.5 6l-3 12" />
              </svg>
              <svg v-else-if="card.key === 'full'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round">
                <path d="M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3Z" />
                <path d="M4 7.5l8 4.5 8-4.5M12 12v9" />
              </svg>
              <svg v-else-if="card.key === 'rbac'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round">
                <path d="M12 3l7 2.8v5.6c0 4.5-3 7.7-7 9.6-4-1.9-7-5.1-7-9.6V5.8L12 3Z" />
                <path d="M9 12l2 2 4-4" stroke-linecap="round" />
              </svg>
              <svg v-else-if="card.key === 'async'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 13h4l2.5-7 3.5 12 2.3-6H20" />
              </svg>
              <svg v-else-if="card.key === 'deploy'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round">
                <path d="M4 8.5L12 4l8 4.5v7L12 20l-8-4.5v-7Z" />
                <path d="M4 8.5l8 4.5 8-4.5M12 13v7" />
                <path d="M8 6.3l8 4.4" />
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round">
                <rect x="7" y="2.8" width="10" height="18.4" rx="2.2" />
                <path d="M10.5 5.5h3" stroke-linecap="round" />
                <path d="M8 18.5h8" />
              </svg>
            </span>
            <span class="bento-card__index">{{ card.index }}</span>
          </div>

          <h3>{{ card.title }}</h3>
          <p class="bento-card__desc">{{ card.desc }}</p>

          <div v-if="card.key === 'ai'" class="ai-demo" aria-hidden="true">
            <span class="ai-demo__table">sys_user</span>
            <span class="ai-demo__arrow">→</span>
            <span class="ai-demo__files">
              <span>UserController.ts</span>
              <span>UserService.py</span>
              <span>UserView.vue</span>
            </span>
          </div>

          <div v-else-if="card.key === 'api'" class="api-demo" aria-hidden="true">
            <strong>200<span>+</span></strong>
            <span class="api-demo__label">{{ isEn ? 'REST endpoints' : '个 REST 接口' }}</span>
            <div class="api-demo__lines"><i></i><i></i><i></i></div>
          </div>

          <div v-else-if="card.key === 'full'" class="stack-chips" aria-hidden="true">
            <span>FastAPI</span><span>Vue 3</span><span>UniApp</span>
          </div>

          <div v-else-if="card.key === 'rbac'" class="permission-tags" aria-hidden="true">
            <span>{{ isEn ? 'Menu' : '菜单' }}</span>
            <span>{{ isEn ? 'Action' : '按钮' }}</span>
            <span>{{ isEn ? 'Data' : '数据' }}</span>
          </div>

          <div v-else-if="card.key === 'async'" class="latency-demo" aria-hidden="true">
            <i v-for="n in 8" :key="n" :style="{ height: `${18 + (n * 7) % 26}px` }"></i>
            <span>async / await</span>
          </div>

          <div v-else-if="card.key === 'deploy'" class="deploy-demo" aria-hidden="true">
            <span class="deploy-demo__prompt">$</span>
            <code>docker compose up -d</code>
          </div>

          <div v-else class="platform-chips" aria-hidden="true">
            <span>H5</span><span>{{ isEn ? 'WeChat' : '微信' }}</span><span>{{ isEn ? 'Alipay' : '支付宝' }}</span><span>App</span>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useData } from 'vitepress'

const { lang } = useData()
const isEn = computed(() => lang.value === 'en')

const copy = computed(() => isEn.value
  ? {
      eyebrow: 'PRODUCT CAPABILITIES',
      title: 'A delivery-ready stack,\nnot another admin template.',
      lead: 'From the data table to the deployed product: typed API, generated CRUD, permissions, mobile and one-command delivery — already wired together.',
      link: 'See the full capability map',
    }
  : {
      eyebrow: 'PRODUCT CAPABILITIES',
      title: '不是另一个后台模板，\n是能直接交付的全栈底座。',
      lead: '从一张数据表到真正上线的产品：类型安全的接口、自动生成的 CRUD、权限、移动端和一条命令的交付，已经接好。',
      link: '查看完整能力清单',
    })

const cards = computed(() => isEn.value
  ? [
      { key: 'ai', index: '01', title: 'AI Code Generator', desc: 'Pick a table. Get Controller, Service, Model, Vue pages and shared types — regular CRUD stops consuming engineering time.' },
      { key: 'api', index: '02', title: 'API-first by default', desc: 'Typed REST endpoints, Pydantic validation and OpenAPI 3.1 docs. The frontend consumes the same contract.' },
      { key: 'full', index: '03', title: 'Full-stack, one repo', desc: 'FastAPI backend, Vue 3 web and UniApp mobile live together, sharing the same brand tokens.' },
      { key: 'rbac', index: '04', title: 'Enterprise RBAC', desc: 'JWT + OAuth2, menu / button / data-level permissions and a full operation audit trail.' },
      { key: 'async', index: '05', title: 'Async end to end', desc: 'Native async/await, SQLAlchemy 2.0 and Redis caching keep the whole request path non-blocking.' },
      { key: 'deploy', index: '06', title: 'One-command deploy', desc: 'Docker Compose orchestrates API, web, Nginx and SSL. From clone to production without a deployment checklist.' },
      { key: 'mobile', index: '07', title: 'Web + mobile unified', desc: 'One codebase for H5, WeChat / Alipay mini programs and native App, with shared auth, permissions and dark mode.' },
    ]
  : [
      { key: 'ai', index: '01', title: 'AI 代码生成器', desc: '选一张表，生成 Controller、Service、Model、Vue 页面与共享类型。常规 CRUD 不再占用研发时间。' },
      { key: 'api', index: '02', title: '默认 API-first', desc: '类型安全的 REST 接口、Pydantic 自动校验、OpenAPI 3.1 文档，前端消费同一份契约。' },
      { key: 'full', index: '03', title: '全栈，一个仓库', desc: 'FastAPI 后端、Vue 3 Web 与 UniApp 移动端放在一起，共享同一套品牌 Token。' },
      { key: 'rbac', index: '04', title: '企业级 RBAC', desc: 'JWT + OAuth2，菜单、按钮、数据三级权限，操作日志全审计。' },
      { key: 'async', index: '05', title: '全链路异步', desc: '原生 async/await、SQLAlchemy 2.0 与 Redis 缓存，从接口到数据层保持非阻塞。' },
      { key: 'deploy', index: '06', title: '一条命令上线', desc: 'Docker Compose 编排 API、Web、Nginx 与 SSL，从 clone 到生产不用背部署清单。' },
      { key: 'mobile', index: '07', title: 'Web + 移动端一体', desc: '一套代码生成 H5、微信 / 支付宝小程序与 App，登录、权限与暗色模式同源。' },
    ])
</script>

<style scoped>
.features {
  position: relative;
  scroll-margin-top: calc(var(--vp-nav-height) + 1rem);
  padding: 4.5rem 1.5rem 2rem;
}

.features__inner {
  max-width: 1152px;
  margin: 0 auto;
}

.features__head {
  max-width: 720px;
  margin-bottom: 2.25rem;
}

.features__eyebrow {
  margin: 0 0 0.8rem;
  color: var(--vp-eyebrow-color);
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.features__title {
  margin: 0;
  color: var(--vp-home-text-1);
  font-size: clamp(1.85rem, 3.6vw, 2.65rem);
  font-weight: 750;
  letter-spacing: -0.04em;
  line-height: 1.16;
  white-space: pre-line;
  text-wrap: balance;
}

.features__lead {
  max-width: 620px;
  margin: 1rem 0 0;
  color: var(--vp-home-text-2);
  font-size: 0.98rem;
  line-height: 1.75;
}

.features__link {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  margin-top: 1.1rem;
  color: var(--vp-c-indigo);
  font-size: 0.88rem;
  font-weight: 650;
  text-decoration: none;
}

.features__link span {
  transition: transform 0.2s ease;
}

.features__link:hover span {
  transform: translateX(3px);
}

.bento {
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  gap: 1rem;
}

.bento-card {
  position: relative;
  display: flex;
  flex-direction: column;
  grid-column: span 4;
  min-height: 208px;
  padding: 1.35rem;
  overflow: hidden;
  background: var(--vp-home-card-bg);
  border: 1px solid var(--vp-home-card-border);
  border-radius: var(--vp-radius-lg);
  transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
}

.bento-card:hover {
  transform: translateY(-3px);
  border-color: rgba(79, 107, 255, 0.34);
  box-shadow: 0 18px 44px rgba(20, 28, 60, 0.08);
}

.bento-card--ai { grid-column: span 7; }
.bento-card--api { grid-column: span 5; }
.bento-card--deploy { grid-column: span 5; }
.bento-card--mobile { grid-column: span 7; }

.bento-card--ai {
  background:
    radial-gradient(circle at 88% 12%, rgba(109, 91, 255, 0.18), transparent 48%),
    var(--vp-home-card-bg);
}

.bento-card__top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 1.05rem;
}

.bento-card__icon {
  display: grid;
  width: 38px;
  height: 38px;
  color: var(--vp-c-indigo);
  background: rgba(79, 107, 255, 0.1);
  border-radius: 11px;
  place-items: center;
}

.bento-card__icon svg {
  width: 19px;
  height: 19px;
}

.bento-card__index {
  color: var(--vp-c-text-3);
  font-family: var(--vp-font-family-mono);
  font-size: 0.68rem;
  letter-spacing: 0.06em;
  opacity: 0.65;
}

.bento-card h3 {
  margin: 0;
  color: var(--vp-home-text-1);
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  line-height: 1.35;
}

.bento-card__desc {
  margin: 0.45rem 0 0;
  color: var(--vp-home-text-2);
  font-size: 0.86rem;
  line-height: 1.7;
}

.ai-demo {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-top: auto;
  padding-top: 1.4rem;
  font-family: var(--vp-font-family-mono);
  font-size: 0.7rem;
}

.ai-demo__table,
.ai-demo__files span {
  padding: 0.38rem 0.55rem;
  background: rgba(79, 107, 255, 0.08);
  border: 1px solid rgba(79, 107, 255, 0.16);
  border-radius: 6px;
  color: var(--vp-c-indigo);
  white-space: nowrap;
}

.ai-demo__arrow {
  color: var(--vp-c-text-3);
}

.ai-demo__files {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
}

.ai-demo__files span:nth-child(2) {
  background: rgba(18, 184, 134, 0.09);
  border-color: rgba(18, 184, 134, 0.18);
  color: #0b6b4f;
}

.dark .ai-demo__files span:nth-child(2) {
  color: #63e6be;
}

.ai-demo__files span:nth-child(3) {
  background: rgba(245, 127, 0, 0.09);
  border-color: rgba(245, 127, 0, 0.18);
  color: #8a4b00;
}

.dark .ai-demo__files span:nth-child(3) {
  color: #ffc078;
}

.api-demo {
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 0.55rem;
  margin-top: auto;
  padding-top: 1.2rem;
}

.api-demo strong {
  color: var(--vp-c-indigo);
  font-size: 2.35rem;
  font-weight: 800;
  letter-spacing: -0.05em;
  line-height: 1;
}

.api-demo strong span {
  font-size: 1.4rem;
}

.api-demo__label {
  color: var(--vp-c-text-3);
  font-size: 0.76rem;
}

.api-demo__lines {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: 62px;
  margin-left: auto;
}

.api-demo__lines i {
  height: 3px;
  background: linear-gradient(90deg, rgba(79, 107, 255, 0.5), rgba(109, 91, 255, 0.08));
  border-radius: 2px;
}

.api-demo__lines i:nth-child(2) { width: 78%; }
.api-demo__lines i:nth-child(3) { width: 52%; }

.stack-chips,
.permission-tags,
.platform-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-top: auto;
  padding-top: 1.25rem;
}

.stack-chips span,
.permission-tags span,
.platform-chips span {
  padding: 0.32rem 0.55rem;
  color: var(--vp-c-text-2);
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-home-card-border);
  border-radius: 6px;
  font-family: var(--vp-font-family-mono);
  font-size: 0.68rem;
  line-height: 1.2;
}

.permission-tags span {
  color: var(--vp-c-indigo);
  background: rgba(79, 107, 255, 0.07);
  border-color: rgba(79, 107, 255, 0.14);
  font-family: inherit;
}

.platform-chips span {
  color: var(--vp-home-text-1);
  font-family: inherit;
  font-weight: 600;
}

.latency-demo {
  display: flex;
  align-items: flex-end;
  gap: 4px;
  height: 50px;
  margin-top: auto;
  padding-top: 1.1rem;
}

.latency-demo i {
  width: 6px;
  background: linear-gradient(180deg, rgba(79, 107, 255, 0.75), rgba(109, 91, 255, 0.2));
  border-radius: 2px;
}

.latency-demo span {
  margin-left: 0.4rem;
  color: var(--vp-c-text-3);
  font-family: var(--vp-font-family-mono);
  font-size: 0.66rem;
}

.deploy-demo {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  margin-top: auto;
  padding: 0.7rem 0.8rem;
  background: #14161b;
  border-radius: 8px;
  color: #d7dbff;
  font-family: var(--vp-font-family-mono);
  font-size: 0.72rem;
}

.deploy-demo__prompt {
  color: #63e6be;
}

@media (max-width: 960px) {
  .bento-card {
    grid-column: span 6;
  }

  .bento-card--ai,
  .bento-card--api,
  .bento-card--mobile {
    grid-column: span 12;
  }
}

@media (max-width: 639px) {
  .features {
    padding: 3rem 1.15rem 1.5rem;
  }

  .features__head {
    margin-bottom: 1.5rem;
  }

  .bento {
    grid-template-columns: 1fr;
  }

  .bento-card,
  .bento-card--ai,
  .bento-card--api,
  .bento-card--deploy,
  .bento-card--mobile {
    grid-column: auto;
    min-height: 0;
  }

  .features__title {
    font-size: 1.6rem;
    line-height: 1.22;
  }

  .bento-card__desc {
    font-size: 0.84rem;
  }
}
</style>
