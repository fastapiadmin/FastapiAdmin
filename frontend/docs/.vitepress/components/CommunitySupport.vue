<template>
  <section id="community" class="community" aria-labelledby="community-title">
    <div class="community-inner">
      <header class="community-header">
        <p class="community-eyebrow">{{ copy.eyebrow }}</p>
        <h2 id="community-title" class="community-title">{{ copy.title }}</h2>
        <p class="community-subtitle">{{ copy.subtitle }}</p>
      </header>

      <div class="community-grid">
        <article v-for="item in items" :key="item.key" class="community-card">
          <div class="community-card-head">
            <span class="community-icon" aria-hidden="true">
              <svg v-if="item.key === 'group'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">
                <path d="M21 11.5a8.4 8.4 0 0 1-8.5 8.3 9.5 9.5 0 0 1-3.8-.8L4 20l1.2-3.7A8 8 0 0 1 4 11.5 8.4 8.4 0 0 1 12.5 3 8.4 8.4 0 0 1 21 11.5Z" stroke-linejoin="round" />
                <path d="M8.5 11.5h.01M12 11.5h.01M15.5 11.5h.01" stroke-linecap="round" />
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">
                <path d="M12 20s-7-4.3-7-9.2A4.1 4.1 0 0 1 9.1 6 4.6 4.6 0 0 1 12 7.4 4.6 4.6 0 0 1 14.9 6A4.1 4.1 0 0 1 19 10.8C19 15.7 12 20 12 20Z" stroke-linejoin="round" />
              </svg>
            </span>
            <div class="community-card-copy">
              <h3>{{ item.title }}</h3>
              <p>{{ item.desc }}</p>
            </div>
          </div>

          <div class="community-body">
            <div class="qr-frame" :class="{ 'qr-frame--dark': item.dark, 'qr-frame--poster': item.poster }">
              <img
                :src="item.image"
                :alt="item.alt"
                :width="item.poster ? 828 : 200"
                :height="item.poster ? 1124 : 200"
                loading="lazy"
                decoding="async"
              />
            </div>
            <div class="qr-side">
              <p class="qr-hint">{{ item.hint }}</p>
              <p class="qr-note">{{ item.note }}</p>
            </div>
          </div>
        </article>
      </div>

      <p class="community-disclaimer">{{ copy.disclaimer }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useData, withBase } from 'vitepress'

const { lang } = useData()
const isEn = computed(() => lang.value === 'en')

const copy = computed(() => isEn.value
  ? {
      eyebrow: 'COMMUNITY & SUPPORT',
      title: 'Talk, learn, and build together',
      subtitle: 'Scan to join the community group, or buy the author a coffee if the project saves you time.',
      groupTitle: 'Community group',
      groupDesc: 'Scan to join the QQ group and talk with the author and other users.',
      groupHint: 'QQ group: 832624014',
      groupNote: 'The QR code opens the group directly. If it expires, search the group number in QQ.',
      groupAlt: 'FastapiAdmin community QQ group QR code',
      supportTitle: 'Buy me a coffee',
      supportDesc: 'If FastapiAdmin helps your work, a voluntary tip keeps the project moving.',
      supportHint: 'WeChat Pay · voluntary',
      supportNote: 'Scan with WeChat. Tips are voluntary and do not purchase support or features.',
      supportAlt: 'WeChat Pay QR code for voluntary support',
      disclaimer: 'Community chat and voluntary tips are separate from commercial support. Please do not tip if you need an invoice or a guaranteed response.',
    }
  : {
      eyebrow: '社区与支持',
      title: '一起交流，一起把项目做好',
      subtitle: '扫码加入社区群，或请作者喝杯咖啡；你的反馈和鼓励都会让项目走得更远。',
      groupTitle: '社区交流群',
      groupDesc: '扫码加入 QQ 群，和作者、其他使用者一起交流使用心得与二开经验。',
      groupHint: 'QQ 群号：832624014',
      groupNote: '二维码可直接加群；若二维码失效，可在 QQ 中搜索群号。',
      groupAlt: 'FastapiAdmin 社区 QQ 交流群二维码',
      supportTitle: '赞赏支持',
      supportDesc: '如果这个项目帮你节省了时间，欢迎自愿赞赏，支持后续维护和更新。',
      supportHint: '微信扫码 · 自愿赞赏',
      supportNote: '请使用微信扫码。赞赏完全自愿，不构成付费服务或功能承诺。',
      supportAlt: '微信赞赏收款二维码',
      disclaimer: '社区交流与自愿赞赏均不代表商业支持；如需发票或确定性的响应时间，请勿赞赏。',
    })

const items = computed(() => [
  {
    key: 'group',
    title: copy.value.groupTitle,
    desc: copy.value.groupDesc,
    hint: copy.value.groupHint,
    note: copy.value.groupNote,
    alt: copy.value.groupAlt,
    image: withBase('/community/community-group-crop.png'),
    dark: true,
    poster: false,
  },
  {
    key: 'support',
    title: copy.value.supportTitle,
    desc: copy.value.supportDesc,
    hint: copy.value.supportHint,
    note: copy.value.supportNote,
    alt: copy.value.supportAlt,
    image: withBase('/community/wechat-pay.jpg'),
    dark: false,
    poster: true,
  },
])
</script>

<style scoped>
.community {
  padding: 3rem 1.5rem 4.5rem;
  scroll-margin-top: calc(var(--vp-nav-height) + 1rem);
}

.community-inner {
  max-width: 1000px;
  margin: 0 auto;
}

.community-header {
  max-width: 640px;
  margin: 0 auto 2.25rem;
  text-align: center;
}

.community-eyebrow {
  margin: 0 0 0.7rem;
  color: var(--vp-eyebrow-color);
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.community-title {
  margin: 0;
  text-wrap: balance;
  word-break: keep-all;
  overflow-wrap: anywhere;
  color: var(--vp-home-text-1);
  font-size: var(--vp-section-title-size);
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.25;
}

.community-subtitle {
  margin: 0.9rem auto 0;
  color: var(--vp-home-text-2);
  font-size: 0.95rem;
  line-height: 1.7;
}

.community-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.25rem;
}

.community-card {
  display: flex;
  flex-direction: column;
  padding: 1.25rem;
  background: var(--vp-home-card-bg);
  border: 1px solid var(--vp-home-card-border);
  border-radius: var(--vp-radius-lg);
}

.community-card-head {
  display: flex;
  gap: 0.8rem;
  align-items: flex-start;
}

.community-icon {
  display: grid;
  flex: 0 0 auto;
  width: 38px;
  height: 38px;
  color: var(--vp-c-indigo);
  background: rgba(79, 107, 255, 0.1);
  border-radius: 11px;
  place-items: center;
}

.community-icon svg {
  width: 20px;
  height: 20px;
}

.community-card-copy h3 {
  margin: 0;
  color: var(--vp-home-text-1);
  font-size: 1rem;
  font-weight: 700;
  line-height: 1.4;
}

.community-card-copy p {
  margin: 0.35rem 0 0;
  color: var(--vp-home-text-2);
  font-size: 0.86rem;
  line-height: 1.65;
}

.community-body {
  display: grid;
  grid-template-columns: 170px minmax(0, 1fr);
  gap: 1rem;
  align-items: center;
  margin-top: 1.1rem;
}

.qr-frame {
  display: grid;
  width: 170px;
  aspect-ratio: 1;
  padding: 7px;
  overflow: hidden;
  background: #fff;
  border: 1px solid var(--vp-home-card-border);
  border-radius: 14px;
  place-items: center;
}

.qr-frame--dark {
  background: #14161b;
}

.qr-frame--poster {
  width: 170px;
  aspect-ratio: 828 / 1124;
}

.qr-frame img {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 7px;
  object-fit: contain;
}

.qr-side {
  min-width: 0;
}

.qr-hint {
  margin: 0;
  color: var(--vp-home-text-1);
  font-size: 0.86rem;
  font-weight: 700;
  line-height: 1.5;
}

.qr-note {
  margin: 0.5rem 0 0;
  color: var(--vp-home-text-3);
  font-size: 0.78rem;
  line-height: 1.6;
}

.community-disclaimer {
  max-width: 760px;
  margin: 1.5rem auto 0;
  color: var(--vp-home-text-3);
  font-size: 0.76rem;
  line-height: 1.6;
  text-align: center;
}

@media (max-width: 760px) {
  .community {
    padding: 2.5rem 1.25rem 3.5rem;
  }

  .community-grid {
    grid-template-columns: 1fr;
  }

  .community-body {
    grid-template-columns: 140px minmax(0, 1fr);
  }

  .qr-frame {
    width: 140px;
  }

  .qr-frame--poster {
    width: 150px;
  }
}

@media (max-width: 420px) {
  .community-body {
    grid-template-columns: 1fr;
  }

  .qr-frame {
    width: 170px;
    margin: 0 auto;
  }

  .qr-frame--poster {
    width: 170px;
  }
}
</style>
