---
title: Who is Using
sidebar: false
aside: false
---

<style>
/* 全局样式 - 增加页面宽度 */
.VPDoc.has-sidebar .content-container,
.VPDoc.has-aside .content-container {
  max-width: 1200px !important;
}

.VPDoc .container {
  max-width: 1200px !important;
}

.VPDoc .content {
  max-width: 1200px !important;
}
</style>

<script setup>
import { ref } from 'vue'

const featuredUsers = [
  {
    name: 'Shenzhen Changhong Technology Co., Ltd.',
    location: 'Shenzhen · Pingshan',
    website: 'https://cn.sz-changhong.com/',
    websiteEn: 'https://www.sz-changhong.com/',
    registrant: 'Yang Xiangxiang',
    registrantUrl: 'https://gitee.com/xiao-lei',
    date: '2026-04-19',
    description: 'Enterprise management system built on FastapiAdmin'
  },
  {
    name: 'Beijing Yunxin XX Software Technology Co., Ltd.',
    location: 'Shaanxi · Xi\'an',
    registrant: 'Li Hao',
    registrantUrl: 'https://gitee.com/aiyun_lh',
    date: '2026-04-19',
    description: 'Unit manufacturing execution system built on FastapiAdmin'
  }
]

const stats = [
  { label: 'Registered Users', value: '2+', icon: '👥' },
  { label: 'Technical Support', value: 'Priority', icon: '🚀' },
  { label: 'License', value: 'Free', icon: '💎' }
]
</script>

<style scoped>
.hero-section {
  text-align: center;
  padding: 3rem 1rem;
  background: linear-gradient(120deg, #bd34fe 30%, #41d1ff);
  border-radius: 16px;
  color: white;
  margin-bottom: 3rem;
  box-shadow: 0 10px 40px rgba(189, 52, 254, 0.3);
}

.hero-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.hero-subtitle {
  font-size: 1.1rem;
  opacity: 0.95;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 0.8rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  display: inline-block;
}

.btn-primary {
  background: white;
  color: #667eea;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid white;
  backdrop-filter: blur(10px);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
  border-color: rgba(102, 126, 234, 0.4);
}

.stat-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #bd34fe;
  margin-bottom: 0.8rem;
}

.stat-label {
  font-size: 0.9rem;
  color: var(--vp-c-text-2);
  font-weight: 500;
}

.section-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 2rem;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.user-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 2rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.user-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(120deg, #bd34fe 30%, #41d1ff);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.user-card:hover::before {
  transform: scaleX(1);
}

.user-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2);
  border-color: rgba(102, 126, 234, 0.3);
}

.user-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.user-logo {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  flex-shrink: 0;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(120deg, #bd34fe 30%, #41d1ff);
  color: white;
  font-weight: 700;
  font-size: 1.4rem;
}

.user-logo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-name {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--vp-c-text-1);
  flex: 1;
  margin: 0;
}

.user-description {
  color: var(--vp-c-text-2);
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.user-info {
  line-height: 2;
  font-size: 0.9rem;
}

.user-info strong {
  color: var(--vp-c-text-1);
}

.user-info a {
  color: #667eea;
  text-decoration: none;
  transition: color 0.3s ease;
}

.user-info a:hover {
  color: #764ba2;
  text-decoration: underline;
}

.cta-section {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border: 2px dashed rgba(102, 126, 234, 0.3);
  border-radius: 16px;
  padding: 3rem;
  text-align: center;
  margin-top: 3rem;
}

.cta-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: var(--vp-c-text-1);
}

.cta-text {
  color: var(--vp-c-text-2);
  margin-bottom: 2rem;
  line-height: 1.8;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.view-all-link {
  display: inline-block;
  margin: 2rem auto;
  padding: 1rem 3rem;
  background: linear-gradient(120deg, #bd34fe 30%, #41d1ff);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(189, 52, 254, 0.3);
}

.view-all-link:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 25px rgba(189, 52, 254, 0.5);
  color: white;
}

/* 增加内容宽度 */
.vp-doc {
  max-width: 1200px !important;
}

.vp-doc .content-container {
  max-width: 100% !important;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .users-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>

<div class="hero-section">
  <h1 class="hero-title">🚀 Who is Using FastapiAdmin</h1>
  <p class="hero-subtitle">
    Thank you to every developer and enterprise who has chosen FastapiAdmin<br>
    After registration, you will receive <strong>priority technical support</strong>, and our maintenance team will respond to your issues promptly
  </p>
  <div class="hero-buttons">
    <a href="https://gitee.com/fastapiadmin/FastapiAdmin/issues/IJ9NKA" target="_blank" class="btn btn-primary">📝 Register Now (Gitee)</a>
    <a href="https://github.com/fastapiadmin/FastapiAdmin/issues/362" target="_blank" class="btn btn-primary">📝 Register Now (GitHub)</a>
    <a href="/en/users/all" class="btn btn-secondary">🔍 Browse All Users</a>
  </div>
</div>

<div class="stats-grid">
  <div v-for="stat in stats" :key="stat.label" class="stat-card">
    <div class="stat-icon">{{ stat.icon }}</div>
    <div class="stat-value">{{ stat.value }}</div>
    <div class="stat-label">{{ stat.label }}</div>
  </div>
</div>

<h2 class="section-title">✨ Featured Users</h2>

<div class="users-grid">
  <div v-for="user in featuredUsers" :key="user.name" class="user-card">
    <div class="user-header">
      <div class="user-logo">
        <img v-if="user.logo" :src="user.logo" :alt="user.name">
        <span v-else>{{ user.name.charAt(0) }}</span>
      </div>
      <h3 class="user-name">{{ user.name }}</h3>
    </div>
    <p class="user-description">{{ user.description }}</p>
    <div class="user-info">
      � <strong>Location</strong>: {{ user.location }}<br>
      <span v-if="user.website">🌐 <strong>Chinese Website</strong>: <a :href="user.website" target="_blank">{{ user.website }}</a><br></span>
      <span v-if="user.websiteEn">🌐 <strong>English Website</strong>: <a :href="user.websiteEn" target="_blank">{{ user.websiteEn }}</a><br></span>
      � <strong>Registrant</strong>: <a :href="user.registrantUrl" target="_blank">{{ user.registrant }}</a><br>
      📅 <strong>Date</strong>: {{ user.date }}
    </div>
  </div>
</div>

<div style="text-align: center;">
  <a href="/en/users/all" class="view-all-link">View All Users →</a>
</div>

<div class="cta-section">
  <h2 class="cta-title">💡 Build Your Business with FastapiAdmin</h2>
  <p class="cta-text">
    Registration is completely free. FastapiAdmin is open source and free. We solemnly promise not to charge any fees at any stage, and your information will not be used for commercial profit or other non-public purposes.
  </p>
  <a href="https://gitee.com/fastapiadmin/FastapiAdmin/issues/IJ9NKA" target="_blank" class="btn btn-primary">Register Now</a>
</div>
