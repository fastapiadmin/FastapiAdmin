<template>
  <section id="quickstart" class="quickstart">
    <div class="quickstart__inner">
      <div class="quickstart__copy">
        <p class="quickstart__eyebrow">{{ copy.eyebrow }}</p>
        <h2 class="quickstart__title">{{ copy.title }}</h2>
        <p class="quickstart__lead">{{ copy.lead }}</p>

        <div class="quickstart__steps">
          <div v-for="step in copy.steps" :key="step.index" class="quickstart__step">
            <span class="quickstart__step-index">{{ step.index }}</span>
            <span>{{ step.label }}</span>
          </div>
        </div>

        <div class="quickstart__actions">
          <a class="quickstart__btn quickstart__btn--primary" :href="isEn ? '/en/guide/start' : '/guide/start'">
            {{ copy.primary }}
            <span aria-hidden="true">→</span>
          </a>
          <a class="quickstart__btn quickstart__btn--ghost" :href="isEn ? '/en/guide/deploy' : '/guide/deploy'">
            {{ copy.secondary }}
          </a>
        </div>
      </div>

      <div class="quickstart__terminal">
        <div class="quickstart__terminal-bar">
          <span class="quickstart__dots" aria-hidden="true"><i></i><i></i><i></i></span>
          <span class="quickstart__terminal-label">bash</span>
          <button class="quickstart__copy" type="button" :aria-label="copy.copyLabel" @click="copyCommand">
            {{ copied ? copy.copied : copy.copy }}
          </button>
        </div>
        <pre class="quickstart__code" aria-label="Quick start commands"><code><span class="quickstart__prompt">$</span> git clone https://github.com/fastapiadmin/FastapiAdmin.git
<span class="quickstart__prompt">$</span> cd FastapiAdmin
<span class="quickstart__prompt">$</span> docker compose up -d</code></pre>
        <div class="quickstart__status">
          <span><i></i> API</span>
          <span><i></i> Web</span>
          <span><i></i> MySQL</span>
          <span><i></i> Redis</span>
          <span class="quickstart__status-time">~ 2 min</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useData } from 'vitepress'

const { lang } = useData()
const isEn = computed(() => lang.value === 'en')
const copied = ref(false)

const copy = computed(() => isEn.value
  ? {
      eyebrow: 'QUICK START',
      title: 'From clone to running in three commands.',
      lead: 'No hidden setup scripts. Bring the API, web app, database and cache up together, then start building the product.',
      steps: [
        { index: '01', label: 'Clone the repo' },
        { index: '02', label: 'Start the stack' },
        { index: '03', label: 'Open the dashboard' },
      ],
      primary: 'Five-minute setup',
      secondary: 'Deployment guide',
      copy: 'Copy',
      copied: 'Copied',
      copyLabel: 'Copy quick start commands',
    }
  : {
      eyebrow: 'QUICK START',
      title: '从 clone 到跑起来，只要三条命令。',
      lead: '没有隐藏的初始化脚本。API、Web、数据库与缓存一起启动，把时间花在业务上，而不是环境上。',
      steps: [
        { index: '01', label: '克隆仓库' },
        { index: '02', label: '启动全栈' },
        { index: '03', label: '打开后台' },
      ],
      primary: '5 分钟开始',
      secondary: '部署指南',
      copy: '复制',
      copied: '已复制',
      copyLabel: '复制快速开始命令',
    })

const commandText = 'git clone https://github.com/fastapiadmin/FastapiAdmin.git\ncd FastapiAdmin\ndocker compose up -d'

async function copyCommand() {
  try {
    await navigator.clipboard.writeText(commandText)
    copied.value = true
    window.setTimeout(() => { copied.value = false }, 1800)
  } catch {
    copied.value = false
  }
}
</script>

<style scoped>
.quickstart {
  position: relative;
  scroll-margin-top: calc(var(--vp-nav-height) + 1rem);
  padding: 3rem 1.5rem 4rem;
}

.quickstart__inner {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
  gap: 2rem;
  align-items: center;
  max-width: 1152px;
  margin: 0 auto;
  padding: 2.5rem;
  overflow: hidden;
  background:
    radial-gradient(circle at 84% 8%, rgba(109, 91, 255, 0.4), transparent 38%),
    radial-gradient(circle at 8% 92%, rgba(79, 107, 255, 0.28), transparent 34%),
    #111528;
  border: 1px solid rgba(140, 155, 255, 0.22);
  border-radius: 22px;
  box-shadow: 0 30px 70px rgba(14, 18, 40, 0.22);
}

.quickstart__copy {
  position: relative;
  z-index: 1;
}

.quickstart__eyebrow {
  margin: 0 0 0.75rem;
  color: #aab6ff;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.14em;
}

.quickstart__title {
  margin: 0;
  color: #fff;
  font-size: clamp(1.75rem, 3vw, 2.4rem);
  font-weight: 750;
  letter-spacing: -0.035em;
  line-height: 1.2;
  text-wrap: balance;
}

.quickstart__lead {
  max-width: 430px;
  margin: 0.9rem 0 0;
  color: rgba(235, 238, 255, 0.7);
  font-size: 0.9rem;
  line-height: 1.75;
}

.quickstart__steps {
  display: flex;
  flex-wrap: wrap;
  gap: 0.55rem;
  margin-top: 1.4rem;
}

.quickstart__step {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  color: rgba(235, 238, 255, 0.82);
  font-size: 0.76rem;
}

.quickstart__step-index {
  color: #8fa4ff;
  font-family: var(--vp-font-family-mono);
  font-size: 0.64rem;
}

.quickstart__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.65rem;
  margin-top: 1.6rem;
}

.quickstart__btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.62rem 1rem;
  border-radius: 8px;
  font-size: 0.84rem;
  font-weight: 650;
  text-decoration: none;
  transition: transform 0.2s ease, background 0.2s ease;
}

.quickstart__btn:hover {
  transform: translateY(-1px);
}

.quickstart__btn--primary {
  color: #14162b;
  background: #fff;
}

.quickstart__btn--ghost {
  color: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.quickstart__btn--ghost:hover {
  background: rgba(255, 255, 255, 0.08);
}

.quickstart__terminal {
  position: relative;
  z-index: 1;
  overflow: hidden;
  background: rgba(8, 10, 22, 0.72);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 12px;
  box-shadow: 0 22px 50px rgba(0, 0, 0, 0.28);
}

.quickstart__terminal-bar {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.6rem 0.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.quickstart__dots {
  display: inline-flex;
  gap: 4px;
}

.quickstart__dots i {
  width: 6px;
  height: 6px;
  background: rgba(255, 255, 255, 0.28);
  border-radius: 50%;
}

.quickstart__dots i:first-child { background: #ff6b6b; }
.quickstart__dots i:nth-child(2) { background: #ffc078; }
.quickstart__dots i:nth-child(3) { background: #37b24d; }

.quickstart__terminal-label {
  color: rgba(255, 255, 255, 0.42);
  font-family: var(--vp-font-family-mono);
  font-size: 0.66rem;
}

.quickstart__copy {
  margin-left: auto;
  padding: 0.2rem 0.5rem;
  color: rgba(255, 255, 255, 0.55);
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 5px;
  font-size: 0.66rem;
  cursor: pointer;
}

.quickstart__copy:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.12);
}

.quickstart__code {
  margin: 0;
  padding: 1rem 0.9rem;
  overflow-x: auto;
  color: #dfe4ff;
  font-family: var(--vp-font-family-mono);
  font-size: 0.73rem;
  line-height: 1.9;
}

.quickstart__prompt {
  color: #63e6be;
  user-select: none;
}

.quickstart__status {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  padding: 0.65rem 0.9rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.quickstart__status span {
  display: inline-flex;
  align-items: center;
  gap: 0.32rem;
  color: rgba(235, 238, 255, 0.52);
  font-size: 0.64rem;
}

.quickstart__status i {
  width: 5px;
  height: 5px;
  background: #37b24d;
  border-radius: 50%;
}

.quickstart__status-time {
  margin-left: auto;
}

@media (max-width: 860px) {
  .quickstart__inner {
    grid-template-columns: 1fr;
    gap: 1.5rem;
    padding: 1.75rem;
  }
}

@media (max-width: 639px) {
  .quickstart {
    padding: 2rem 1.15rem 3rem;
  }

  .quickstart__inner {
    padding: 1.35rem;
    border-radius: 16px;
  }

  .quickstart__lead {
    font-size: 0.86rem;
  }

  .quickstart__code {
    font-size: 0.66rem;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
  }

  .quickstart__status-time {
    margin-left: 0;
  }
}
</style>
