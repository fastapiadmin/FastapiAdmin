<template>
  <section id="repositories" class="repos" aria-labelledby="repos-title">
    <div class="repos-inner">
      <header class="repos-header">
        <p class="repos-eyebrow">{{ copy.eyebrow }}</p>
        <h2 id="repos-title" class="repos-title">{{ copy.title }}</h2>
        <p class="repos-subtitle">{{ copy.subtitle }}</p>
      </header>

      <div class="repos-grid">
        <a
          v-for="repo in repos"
          :key="repo.key"
          :href="repo.href"
          target="_blank"
          rel="noopener noreferrer"
          class="repo-card"
          :aria-label="`${repo.platform}: ${repo.name} — ${copy.starCta}`"
        >
          <div class="repo-head">
            <span class="repo-icon" aria-hidden="true">
              <svg v-if="repo.key === 'github'" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0C5.373 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12Z" />
              </svg>
              <svg v-else-if="repo.key === 'gitee'" viewBox="0 0 24 24" fill="currentColor">
                <path d="M11.984 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.016 0Zm6.09 5.333c.328 0 .593.266.593.593v1.482a.594.594 0 0 1-.593.593H9.777c-.982 0-1.778.796-1.778 1.778v5.63c0 .327.266.592.593.592h1.482c.327 0 .593-.265.593-.592v-4.445h6.667c.327 0 .593.265.593.593v1.482a.594.594 0 0 1-.593.593h-4.445v1.63c0 1.963-1.595 3.557-3.56 3.557H6.67a.594.594 0 0 1-.593-.593V9.778c0-2.456 1.995-4.445 4.445-4.445h5.552Z" />
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
                <circle cx="12" cy="12" r="1.8" fill="currentColor" stroke="none" />
                <ellipse cx="12" cy="12" rx="10" ry="4.3" />
                <ellipse cx="12" cy="12" rx="10" ry="4.3" transform="rotate(60 12 12)" />
                <ellipse cx="12" cy="12" rx="10" ry="4.3" transform="rotate(120 12 12)" />
              </svg>
            </span>
            <span class="repo-platform">{{ repo.platform }}</span>
            <span class="repo-arrow" aria-hidden="true">↗</span>
          </div>

          <p class="repo-name">{{ repo.name }}</p>
          <p class="repo-desc">{{ repo.desc }}</p>

          <div class="repo-foot">
            <img
              class="repo-badge"
              :src="repo.badge"
              :alt="`${repo.platform} ${copy.starAlt}`"
              height="22"
              loading="lazy"
              decoding="async"
              referrerpolicy="no-referrer"
            />
            <span class="repo-cta">{{ copy.starCta }}</span>
          </div>
        </a>
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
      eyebrow: 'COMMUNITY',
      title: 'Open source, three homes',
      subtitle: 'If FastapiAdmin helps you, a star on any platform keeps the project moving.',
      starCta: 'Star this repo',
      starAlt: 'star count',
      githubDesc: 'Primary repository. Issues, pull requests and releases live here.',
      giteeDesc: 'Fast access from mainland China, with a familiar workflow.',
      atomgitDesc: 'AtomGit mirror and community entry for the domestic ecosystem.',
    }
  : {
      eyebrow: '开源社区',
      title: '三个仓库，随你顺手',
      subtitle: '如果 FastapiAdmin 帮到了你，欢迎在任一平台点一个 Star，让项目被更多人看见。',
      starCta: '去点 Star',
      starAlt: 'Star 数',
      githubDesc: '主仓库，Issue、PR 与 Release 都在这里。',
      giteeDesc: '国内访问更快，适合国内开发者日常协作。',
      atomgitDesc: 'AtomGit 镜像与国内开源社区入口。',
    })

const repos = computed(() => [
  {
    key: 'github',
    platform: 'GitHub',
    name: 'fastapiadmin/FastapiAdmin',
    href: 'https://github.com/fastapiadmin/FastapiAdmin',
    badge: 'https://img.shields.io/github/stars/fastapiadmin/FastapiAdmin?style=flat-square&label=Stars&color=4F6BFF',
    desc: copy.value.githubDesc,
  },
  {
    key: 'gitee',
    platform: 'Gitee',
    name: 'fastapiadmin/FastapiAdmin',
    href: 'https://gitee.com/fastapiadmin/FastapiAdmin',
    badge: 'https://gitee.com/fastapiadmin/FastapiAdmin/badge/star.svg?theme=dark',
    desc: copy.value.giteeDesc,
  },
  {
    key: 'atomgit',
    platform: 'AtomGit',
    name: 'fastapiadmin/FastapiAdmin',
    href: 'https://atomgit.com/fastapiadmin/FastapiAdmin',
    badge: 'https://atomgit.com/fastapiadmin/FastapiAdmin/star/badge.svg',
    desc: copy.value.atomgitDesc,
  },
])
</script>

<style scoped>
.repos {
  padding: 2.5rem 1.5rem 2rem;
  scroll-margin-top: calc(var(--vp-nav-height) + 1rem);
}

.repos-inner {
  max-width: 1100px;
  margin: 0 auto;
}

.repos-header {
  max-width: 640px;
  margin: 0 auto 2.5rem;
  text-align: center;
}

.repos-eyebrow {
  margin: 0 0 0.7rem;
  color: var(--vp-eyebrow-color);
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.repos-title {
  text-wrap: balance;
  word-break: keep-all;
  overflow-wrap: anywhere;
  margin: 0;
  color: var(--vp-home-text-1);
  font-size: var(--vp-section-title-size);
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.25;
}

.repos-subtitle {
  margin: 0.9rem auto 0;
  color: var(--vp-home-text-2);
  font-size: 0.95rem;
  line-height: 1.7;
}

.repos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.repo-card {
  position: relative;
  display: flex;
  flex-direction: column;
  min-height: 210px;
  padding: 1.35rem;
  overflow: hidden;
  color: inherit;
  text-decoration: none;
  background: var(--vp-home-card-bg);
  border: 1px solid var(--vp-home-card-border);
  border-radius: var(--vp-radius-lg);
  transition:
    transform 0.25s var(--vp-ease-standard),
    border-color 0.25s ease,
    background 0.25s ease,
    box-shadow 0.25s ease;
}

.repo-card::before {
  content: '';
  position: absolute;
  inset: 0 0 auto;
  height: 2px;
  background: var(--vp-brand-gradient);
  opacity: 0;
  transition: opacity 0.25s ease;
}

.repo-card:hover {
  transform: translateY(calc(-1 * var(--vp-hover-lift)));
  background: var(--vp-home-card-hover-bg);
  border-color: rgba(109, 91, 255, 0.35);
  box-shadow: 0 18px 40px rgba(79, 107, 255, 0.14);
}

.repo-card:hover::before {
  opacity: 1;
}

.repo-card:focus-visible {
  outline: var(--vp-focus-ring);
  outline-offset: var(--vp-focus-offset);
}

.repo-head {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.repo-icon {
  display: grid;
  flex: 0 0 auto;
  width: 36px;
  height: 36px;
  color: var(--vp-c-indigo);
  background: rgba(79, 107, 255, 0.1);
  border-radius: 10px;
  place-items: center;
}

.repo-icon svg {
  width: 19px;
  height: 19px;
}

.repo-platform {
  color: var(--vp-home-text-1);
  font-size: 0.95rem;
  font-weight: 700;
}

.repo-arrow {
  margin-left: auto;
  color: var(--vp-home-text-3);
  font-size: 1rem;
  transition: transform 0.25s ease, color 0.25s ease;
}

.repo-card:hover .repo-arrow {
  color: var(--vp-c-indigo);
  transform: translate(2px, -2px);
}

.repo-name {
  margin: 1rem 0 0;
  color: var(--vp-home-text-2);
  font-family: var(--vp-font-family-mono);
  font-size: 0.82rem;
  word-break: break-all;
}

.repo-desc {
  flex: 1;
  margin: 0.55rem 0 0;
  color: var(--vp-home-text-2);
  font-size: 0.88rem;
  line-height: 1.65;
}

.repo-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  margin-top: 1.15rem;
}

.repo-badge {
  display: block;
  width: auto;
  height: 22px;
}

.repo-cta {
  color: var(--vp-c-indigo);
  font-size: 0.8rem;
  font-weight: 600;
  white-space: nowrap;
}

.dark .repo-icon {
  background: rgba(143, 164, 255, 0.14);
}

@media (max-width: 768px) {
  .repos {
    padding: 3rem 1rem 1.5rem;
  }

  .repos-grid {
    grid-template-columns: 1fr;
  }

  .repo-card {
    min-height: 0;
  }
}
</style>
