<template>
  <div class="hero-showcase hero-showcase--dark">
    <div class="hero-showcase__halo" aria-hidden="true"></div>

    <div class="hero-showcase__frame">
      <div class="hero-showcase__chrome">
        <span class="hero-showcase__dots" aria-hidden="true">
          <i></i><i></i><i></i>
        </span>
        <span class="hero-showcase__url">service.fastapiadmin.com/web</span>
        <span class="hero-showcase__live"><i></i>{{ isEn ? 'LIVE' : '实时' }}</span>
      </div>
      <div class="hero-showcase__screen">
        <img
          :src="withBase('/showcase/dashboard-dark.webp')"
          :alt="isEn ? 'FastapiAdmin dashboard in dark mode' : 'FastapiAdmin 深色模式后台仪表盘'"
          width="1440"
          height="900"
          loading="eager"
          decoding="async"
        />
        <span class="hero-showcase__shine" aria-hidden="true"></span>
      </div>
    </div>

    <div class="hero-showcase__chip hero-showcase__chip--api">
      <strong>200+</strong>
      <span>REST API</span>
    </div>
    <div class="hero-showcase__chip hero-showcase__chip--ai">
      <strong>AI</strong>
      <span>{{ isEn ? 'CRUD in seconds' : '选表即出 CRUD' }}</span>
    </div>
    <div class="hero-showcase__chip hero-showcase__chip--rbac">
      <strong>RBAC</strong>
      <span>{{ isEn ? '3-level access' : '菜单 / 按钮 / 数据' }}</span>
    </div>

    <p class="hero-showcase__caption">
      {{ isEn ? 'Real dashboard · dark mode · Vue 3 + TypeScript' : '真实后台截图 · 深色模式 · Vue 3 + TypeScript' }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useData, withBase } from 'vitepress'

const { lang } = useData()
const isEn = computed(() => lang.value === 'en')
</script>

<style scoped>
.hero-showcase {
  position: relative;
  width: 100%;
  max-width: 560px;
  margin-left: auto;
  padding: 18px 0 30px;
}

.hero-showcase__halo {
  position: absolute;
  inset: 8% 2% 12% 8%;
  background:
    radial-gradient(circle at 70% 30%, rgba(109, 91, 255, 0.32), transparent 58%),
    radial-gradient(circle at 25% 75%, rgba(79, 107, 255, 0.22), transparent 55%);
  filter: blur(38px);
  pointer-events: none;
}

.hero-showcase__frame {
  position: relative;
  overflow: hidden;
  background: var(--vp-home-card-bg);
  border: 1px solid var(--vp-home-card-border);
  border-radius: 16px;
  box-shadow:
    0 30px 80px rgba(20, 28, 60, 0.18),
    0 2px 10px rgba(20, 28, 60, 0.06);
  transform: perspective(1400px) rotateY(-3deg) rotateX(1.5deg);
  transform-origin: 50% 40%;
  transition: transform 0.45s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.45s ease;
}

.hero-showcase__frame:hover {
  transform: perspective(1400px) rotateY(0deg) rotateX(0deg) translateY(-4px);
  box-shadow:
    0 36px 90px rgba(20, 28, 60, 0.22),
    0 2px 10px rgba(20, 28, 60, 0.06);
}

.hero-showcase__chrome {
  display: flex;
  align-items: center;
  gap: 10px;
  height: 38px;
  padding: 0 12px;
  background: var(--vp-home-card-bg);
  border-bottom: 1px solid var(--vp-home-card-border);
}

.hero-showcase__dots {
  display: inline-flex;
  gap: 5px;
}

.hero-showcase__dots i {
  width: 7px;
  height: 7px;
  background: var(--vp-c-text-3);
  border-radius: 50%;
  opacity: 0.45;
}

.hero-showcase__dots i:first-child {
  background: #ff6b6b;
  opacity: 0.85;
}

.hero-showcase__dots i:nth-child(2) {
  background: #ffc078;
  opacity: 0.85;
}

.hero-showcase__dots i:nth-child(3) {
  background: #37b24d;
  opacity: 0.85;
}

.hero-showcase__url {
  flex: 1;
  overflow: hidden;
  color: var(--vp-c-text-3);
  font-family: var(--vp-font-family-mono);
  font-size: 10px;
  line-height: 1;
  text-align: center;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.hero-showcase__live {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: var(--vp-c-text-3);
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.08em;
}

.hero-showcase__live i {
  width: 5px;
  height: 5px;
  background: #37b24d;
  border-radius: 50%;
  box-shadow: 0 0 0 3px rgba(55, 178, 77, 0.16);
}

.hero-showcase__screen {
  position: relative;
  overflow: hidden;
  aspect-ratio: 1440 / 900;
  background: #fff;
}

.hero-showcase__screen img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top left;
}

.hero-showcase__shine {
  position: absolute;
  inset: 0;
  background: linear-gradient(115deg, transparent 42%, rgba(255, 255, 255, 0.16) 50%, transparent 58%);
  opacity: 0.5;
  pointer-events: none;
}

.hero-showcase__chip {
  position: absolute;
  display: flex;
  flex-direction: column;
  gap: 1px;
  padding: 9px 13px;
  background: var(--vp-home-card-bg);
  background: color-mix(in srgb, var(--vp-home-card-bg) 88%, transparent);
  border: 1px solid var(--vp-home-card-border);
  border-radius: 10px;
  box-shadow: 0 12px 30px rgba(20, 28, 60, 0.12);
  backdrop-filter: blur(12px);
  pointer-events: none;
}

.hero-showcase__chip strong {
  color: var(--vp-c-text-1);
  font-size: 15px;
  font-weight: 800;
  letter-spacing: -0.01em;
  line-height: 1.1;
}

.hero-showcase__chip span {
  color: var(--vp-c-text-3);
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 0.02em;
  white-space: nowrap;
}

.hero-showcase__chip--api {
  top: 22%;
  left: -26px;
}

.hero-showcase__chip--ai {
  top: 55%;
  right: -22px;
}

.hero-showcase__chip--rbac {
  bottom: 16%;
  left: -12px;
}

.hero-showcase__caption {
  margin: 16px 0 0;
  color: var(--vp-c-text-3);
  font-size: 11px;
  text-align: right;
}

@media (max-width: 959px) {
  .hero-showcase {
    max-width: 480px;
    margin: 0 auto;
    padding-bottom: 10px;
  }

  .hero-showcase__frame {
    transform: none;
  }

  .hero-showcase__chip {
    display: none;
  }

  .hero-showcase__caption {
    text-align: center;
  }
}

@media (max-width: 639px) {
  .hero-showcase {
    padding-top: 4px;
  }

  .hero-showcase__chrome {
    height: 32px;
  }

  .hero-showcase__url {
    font-size: 9px;
  }

  .hero-showcase__caption {
    margin-top: 10px;
    font-size: 10px;
  }
}

.hero-showcase--dark .hero-showcase__frame {
  background: #0b0f17;
  border-color: rgba(255, 255, 255, 0.12);
  box-shadow:
    0 30px 80px rgba(3, 8, 24, 0.55),
    0 2px 10px rgba(3, 8, 24, 0.3);
}

.hero-showcase--dark .hero-showcase__chrome {
  background: #0d121c;
  border-bottom-color: rgba(255, 255, 255, 0.1);
}

.hero-showcase--dark .hero-showcase__url {
  color: rgba(255, 255, 255, 0.55);
}

.hero-showcase--dark .hero-showcase__live {
  color: #4ade80;
}

.hero-showcase--dark .hero-showcase__screen {
  background: #0b0f17;
}

.hero-showcase--dark .hero-showcase__caption {
  color: var(--vp-c-text-3);
}

.hero-showcase--dark .hero-showcase__shine {
  opacity: 0.08;
  background: linear-gradient(115deg, transparent 42%, rgba(255, 255, 255, 0.08) 50%, transparent 58%);
}

.hero-showcase--dark .hero-showcase__chip {
  background: rgba(10, 14, 24, 0.86);
  border-color: rgba(255, 255, 255, 0.14);
  box-shadow: 0 14px 34px rgba(3, 8, 24, 0.45);
}

.hero-showcase--dark .hero-showcase__chip strong {
  color: #ffffff;
}

.hero-showcase--dark .hero-showcase__chip span {
  color: rgba(255, 255, 255, 0.62);
}
</style>
