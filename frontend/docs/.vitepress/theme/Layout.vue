<script setup lang="ts">
import { computed } from 'vue'
import { useData, useRoute } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import FooterNav from '../components/FooterNav.vue'
import OpenSourceRepos from '../components/OpenSourceRepos.vue'
import HeroShowcase from '../components/HeroShowcase.vue'

const { lang } = useData()
const route = useRoute()

/** 跳到主要内容 — 多语言 */
const skipText = computed(() => (lang.value === 'en' ? 'Skip to main content' : '跳到主要内容'))

/**
 * FooterNav 按页面类型差异化展示:
 * - 首页(/): 完整 full — 提供跳出 guide 的快速通道,符合营销页转化漏斗
 * - about: 精简 minimal — 保留品牌/社交/版权(认知价值),但去掉 3 列 nav(避免与 VPSidebar 重复)
 * - guide/* / changelog / 404 / 其它: 不渲染 — 左侧 VPSidebar + prev/next 已覆盖导航需求,
 *   再渲染会形成"双重底栏"感知,违背 R4 视觉评审"内容优先 / 减少重复"原则
 */
type FooterMode = 'full' | 'minimal'
const footerMode = computed<FooterMode | null>(() => {
  // VitePress route.path 实际带 .html 后缀(与 link 里的相对路径不同)
  // 兼容处理:用 endsWith + 根路径白名单
  const p = route.path
  if (p === '/' || p === '/en/' || p === '/en' || p === '/en/index.html') return 'full'
  if (p.endsWith('/about/about.html')) return 'minimal'
  return null
})
</script>

<template>
  <a href="#VPContent" class="skip-to-content">
    {{ skipText }}
  </a>
  <DefaultTheme.Layout>
    <template #home-hero-image>
      <HeroShowcase />
    </template>
    <template #home-hero-after>
      <OpenSourceRepos />
    </template>
    <template #layout-bottom>
      <FooterNav v-if="footerMode" :mode="footerMode" />
    </template>
  </DefaultTheme.Layout>
</template>

<style>
@view-transition {
  navigation: auto;
}

.skip-to-content {
  position: fixed;
  top: -100%;
  left: 1rem;
  z-index: 9999;
  padding: 0.6rem 1.2rem;
  background: linear-gradient(135deg, #5B6CF7, #8B5CF6);
  color: #fff;
  font-size: 0.85rem;
  font-weight: 600;
  border-radius: 8px;
  text-decoration: none;
  transition: top 0.2s ease;
}

.skip-to-content:focus,
.skip-to-content:focus-visible {
  top: 0.75rem;
  outline: 2px solid #fff;
  outline-offset: 2px;
}
</style>
