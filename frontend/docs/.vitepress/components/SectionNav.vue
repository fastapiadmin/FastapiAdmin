<template>
  <nav v-if="visible" class="section-nav" :aria-label="navLabel">
    <button
      v-for="section in sections"
      :key="section.id"
      class="section-nav-dot"
      :class="{ active: activeSection === section.id }"
      @click="scrollTo(section.id)"
      :title="section.label"
      :aria-label="(isEn ? 'Jump to ' : '跳转到') + section.label"
      :aria-current="activeSection === section.id ? 'location' : undefined"
    >
      <span class="section-nav-dot-inner" aria-hidden="true"></span>
      <span class="section-nav-label">{{ section.label }}</span>
    </button>
  </nav>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useData } from 'vitepress'

interface Section {
  id: string
  label: string
}

const { lang } = useData()
const isEn = computed(() => lang.value === 'en')
const navLabel = computed(() => isEn.value ? 'Page sections' : '页面章节')

const sections = computed<Section[]>(() => isEn.value
    ? [
        { id: 'repositories', label: 'Repositories' },
        { id: 'features', label: 'Capabilities' },
        { id: 'end-to-end-web', label: 'Web Admin' },
        { id: 'end-to-end-gen', label: 'AI Generator' },
        { id: 'end-to-end-api', label: 'FastAPI Backend' },
        { id: 'end-to-end-app', label: 'Mobile' },
        { id: 'quickstart', label: 'Quick Start' },
        { id: 'community', label: 'Community' },
      ]
    : [
        { id: 'repositories', label: '开源仓库' },
        { id: 'features', label: '产品能力' },
        { id: 'end-to-end-web', label: 'Web 管理' },
        { id: 'end-to-end-gen', label: 'AI 生成' },
        { id: 'end-to-end-api', label: 'FastAPI 后端' },
        { id: 'end-to-end-app', label: '移动端' },
        { id: 'quickstart', label: '快速开始' },
        { id: 'community', label: '社区与支持' },
      ]
)

const activeSection = ref('')
const visible = ref(false)
let observer: IntersectionObserver | null = null
let scrollHandler: (() => void) | null = null

const scrollTo = (id: string) => {
  const el = document.getElementById(id)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

onMounted(() => {
  // Only show on homepage
  if (typeof window === 'undefined' || window.location.pathname.includes('/guide/') || window.location.pathname.includes('/about/')) return

  // 首屏不显示：滚过 Hero 后再出现，避免移动端底部导航压住首屏内容
  const updateVisibility = () => {
    const threshold = window.innerWidth <= 768 ? 480 : 240
    const community = document.getElementById('community')
    // 社区/赞赏区已是页尾，不再需要章节导航，同时避免遮住二维码卡片
    const nearEnd = community
      ? community.getBoundingClientRect().top < window.innerHeight - 40
      : false
    visible.value = window.scrollY > threshold && !nearEnd
  }
  updateVisibility()
  scrollHandler = updateVisibility
  window.addEventListener('scroll', updateVisibility, { passive: true })
  window.addEventListener('resize', updateVisibility)

  observer = new IntersectionObserver(
    (entries) => {
      // Find the most visible section
      let maxRatio = 0
      let mostVisible = ''

      for (const entry of entries) {
        if (entry.isIntersecting && entry.intersectionRatio > maxRatio) {
          maxRatio = entry.intersectionRatio
          mostVisible = entry.target.id
        }
      }

      if (mostVisible) {
        activeSection.value = mostVisible
      }
    },
    {
      threshold: [0, 0.1, 0.2, 0.3, 0.4, 0.5],
      rootMargin: '-80px 0px -40% 0px',
    }
  )

  // Observe all section elements
  setTimeout(() => {
    for (const section of sections.value) {
      const el = document.getElementById(section.id)
      if (el) observer?.observe(el)
    }
  }, 200)

})

onUnmounted(() => {
  if (observer) observer.disconnect()
  if (scrollHandler) {
    window.removeEventListener('scroll', scrollHandler)
    window.removeEventListener('resize', scrollHandler)
  }
})
</script>

<style scoped>
.section-nav {
  position: fixed;
  right: 1.5rem;
  top: 50%;
  transform: translateY(-50%);
  z-index: var(--vp-z-index-sticky-cta);  /* 70 — 与 sticky-cta 同级,语义分层清晰 */
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  padding: 0.75rem 0.5rem;
  background: var(--vp-home-card-bg);
  border: 1px solid var(--vp-home-card-border);
  border-radius: 9999px;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  transition: background 0.3s, border-color 0.3s;
}

.dark .section-nav {
  background: rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 255, 255, 0.06);
}

.section-nav-dot {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  /* WCAG 2.5.5 44x44 触屏目标 */
  min-width: 2.4rem;
  min-height: 2.4rem;
  padding: 0;
  border: none;
  background: none;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.section-nav-dot:hover {
  transform: scale(1.15);
}

.section-nav-dot:focus-visible {
  outline: 2px solid var(--vp-brand-accent);
  outline-offset: 2px;
  border-radius: 50%;
}

.section-nav-dot-inner {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(128, 128, 128, 0.35);
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), background 0.3s, border-color 0.3s, box-shadow 0.4s;
}

.section-nav-dot.active .section-nav-dot-inner {
  width: 10px;
  height: 10px;
  background: var(--vp-brand-gradient);
  box-shadow: 0 0 12px rgba(109, 91, 255, 0.6);
}

.section-nav-label {
  position: absolute;
  right: calc(100% + 0.75rem);
  white-space: nowrap;
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--vp-home-text-1);
  background: var(--vp-home-card-bg);
  border: 1px solid var(--vp-home-card-border);
  padding: 0.25rem 0.6rem;
  border-radius: var(--vp-radius-sm);
  backdrop-filter: blur(8px);
  opacity: 0;
  pointer-events: none;
  transition: transform 0.25s, background 0.2s, border-color 0.2s, opacity 0.2s;
  transform: translateX(8px);
}

.section-nav-dot:hover .section-nav-label {
  opacity: 1;
  transform: translateX(0);
}

/* ========================================================================
 * Mobile — 横向 tab bar 替代方案(原 display: none,触屏用户失去导航)
 * 设计:贴底悬浮、横向滚动、active 用品牌渐变
 * ======================================================================== */
@media (max-width: 768px) {
  .section-nav {
    position: fixed;
    top: auto;
    bottom: 0.75rem;
    left: 0.75rem;
    right: 0.75rem;
    transform: none;
    flex-direction: row;
    gap: 0.25rem;
    padding: 0.4rem 0.5rem;
    border-radius: var(--vp-radius-md);
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }

  .section-nav::-webkit-scrollbar {
    display: none;
  }

  .section-nav-dot {
    flex: 0 0 auto;
    min-width: 3.5rem;
    min-height: 2.75rem;  /* 44px WCAG 2.5.5 AAA */
    padding: 0 0.5rem;
    border-radius: var(--vp-radius-sm);
    transition: background 0.2s, transform 0.2s;
  }

  .section-nav-dot:hover {
    transform: none;
  }

  .section-nav-dot.active {
    background: rgba(109, 91, 255, 0.18);
  }

  .section-nav-dot-inner {
    display: none;
  }

  .section-nav-label {
    position: static;
    opacity: 1;
    transform: none;
    background: none;
    border: none;
    padding: 0;
    backdrop-filter: none;
    font-size: 0.78rem;
    color: var(--vp-home-text-2);
    pointer-events: auto;
  }

  .section-nav-dot.active .section-nav-label {
    color: var(--vp-home-text-1);
    font-weight: 700;
  }
}
</style>
