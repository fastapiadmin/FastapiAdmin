---
title: All Users
sidebar: false
aside: false
---

<style>
/* 全局样式 - 增加页面宽度到 1600px，以便在宽屏下显示 4 列公司卡片 */
.VPDoc.has-sidebar .content-container,
.VPDoc.has-aside .content-container {
  max-width: 1600px !important;
}

.VPDoc .container {
  max-width: 1600px !important;
}

.VPDoc .content {
  max-width: 1600px !important;
}
</style>

<script setup>
import { ref, computed } from 'vue'

const allUsers = ref([
  {
    name: 'Shenzhen Changhong Technology Co., Ltd.',
    location: 'Shenzhen · Pingshan',
    region: 'Guangdong',
    website: 'https://cn.sz-changhong.com/',
    websiteEn: 'https://www.sz-changhong.com/',
    logo: '',
    registrant: 'Yang Xiangxiang',
    registrantUrl: 'https://gitee.com/xiao-lei',
    date: '2026-04-19',
    description: 'Enterprise management system built on FastapiAdmin'
  },
  {
    name: 'Beijing Yunxin XX Software Technology Co., Ltd.',
    location: 'Shaanxi · Xi\'an',
    region: 'Shaanxi',
    website: '',
    logo: '',
    registrant: 'Li Hao',
    registrantUrl: 'https://gitee.com/aiyun_lh',
    date: '2026-04-19',
    description: 'Unit manufacturing execution system built on FastapiAdmin'
  },
  {
    name: 'Shanghai Wisdom Technology Co., Ltd.',
    location: 'Shanghai · Pudong',
    region: 'Shanghai',
    website: 'https://www.sh-wisdom.com/',
    websiteEn: '',
    logo: '',
    registrant: 'Zhang Wei',
    registrantUrl: 'https://gitee.com/zhangwei',
    date: '2026-04-18',
    description: 'Intelligent logistics management platform built on FastapiAdmin'
  },
  {
    name: 'Hangzhou Cloud Network Technology Co., Ltd.',
    location: 'Zhejiang · Hangzhou',
    region: 'Zhejiang',
    website: 'https://www.hz-cloud.com/',
    websiteEn: 'https://en.hz-cloud.com/',
    logo: '',
    registrant: 'Wang Fang',
    registrantUrl: 'https://gitee.com/wangfang',
    date: '2026-04-17',
    description: 'Cloud data analysis system built on FastapiAdmin'
  },
  {
    name: 'Chengdu Shudao Technology Co., Ltd.',
    location: 'Sichuan · Chengdu',
    region: 'Sichuan',
    website: '',
    websiteEn: '',
    logo: '',
    registrant: 'Liu Qiang',
    registrantUrl: 'https://gitee.com/liuqiang',
    date: '2026-04-16',
    description: 'E-commerce operation management system built on FastapiAdmin'
  },
  {
    name: 'Guangzhou Southern Data Technology Co., Ltd.',
    location: 'Guangdong · Guangzhou',
    region: 'Guangdong',
    website: 'https://www.gz-data.com/',
    websiteEn: '',
    logo: '',
    registrant: 'Chen Ming',
    registrantUrl: 'https://gitee.com/chenming',
    date: '2026-04-15',
    description: 'Big data visualization platform built on FastapiAdmin'
  },
  {
    name: 'Nanjing Zijin Software Development Co., Ltd.',
    location: 'Jiangsu · Nanjing',
    region: 'Jiangsu',
    website: 'https://www.nj-zijin.com/',
    websiteEn: 'https://en.nj-zijin.com/',
    logo: '',
    registrant: 'Zhao Li',
    registrantUrl: 'https://gitee.com/zhaoli',
    date: '2026-04-14',
    description: 'Education and training management system built on FastapiAdmin'
  },
  {
    name: 'Wuhan Yangtze River Information Technology Co., Ltd.',
    location: 'Hubei · Wuhan',
    region: 'Hubei',
    website: '',
    websiteEn: '',
    logo: '',
    registrant: 'Sun Tao',
    registrantUrl: 'https://gitee.com/suntao',
    date: '2026-04-13',
    description: 'Medical health management platform built on FastapiAdmin'
  },
  {
    name: 'Tianjin Binhai Innovation Technology Co., Ltd.',
    location: 'Tianjin · Binhai New Area',
    region: 'Tianjin',
    website: 'https://www.tj-binhai.com/',
    websiteEn: '',
    logo: '',
    registrant: 'Zhou Min',
    registrantUrl: 'https://gitee.com/zhoumin',
    date: '2026-04-12',
    description: 'Smart manufacturing execution system built on FastapiAdmin'
  },
  {
    name: 'Chongqing Mountain City Software Co., Ltd.',
    location: 'Chongqing · Yubei',
    region: 'Chongqing',
    website: 'https://www.cq-mountain.com/',
    websiteEn: 'https://en.cq-mountain.com/',
    logo: '',
    registrant: 'Wu Jing',
    registrantUrl: 'https://gitee.com/wujing',
    date: '2026-04-11',
    description: 'Supply chain management system built on FastapiAdmin'
  }
])

const searchKeyword = ref('')
const activeRegion = ref('All')

const regions = computed(() => {
  const set = new Set(allUsers.value.map(u => u.region))
  return ['All', ...Array.from(set)]
})

const filteredUsers = computed(() => {
  return allUsers.value.filter(user => {
    const matchKeyword = !searchKeyword.value ||
      user.name.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
      user.location.toLowerCase().includes(searchKeyword.value.toLowerCase())
    const matchRegion = activeRegion.value === 'All' || user.region === activeRegion.value
    return matchKeyword && matchRegion
  })
})
</script>

<style scoped>
.page-header {
  text-align: center;
  padding: 3rem 1rem;
  background: linear-gradient(120deg, #bd34fe 30%, #41d1ff);
  border-radius: 16px;
  color: white;
  margin-bottom: 3rem;
  box-shadow: 0 10px 40px rgba(189, 52, 254, 0.3);
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.page-subtitle {
  font-size: 1.1rem;
  opacity: 0.95;
  margin-bottom: 1.5rem;
}

.stats-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.2);
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  backdrop-filter: blur(10px);
  margin: 0 0.5rem;
}

.register-btn {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.8rem 2rem;
  background: white;
  color: #667eea;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.register-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.search-section {
  margin-bottom: 2rem;
}

.search-input {
  width: 100%;
  padding: 1rem 1.5rem;
  font-size: 1rem;
  border: 2px solid var(--vp-c-divider);
  border-radius: 12px;
  background: var(--vp-c-bg-soft);
  transition: all 0.3s ease;
  outline: none;
}

.search-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.filter-section {
  margin-bottom: 3rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  justify-content: center;
}

.filter-tag {
  padding: 0.6rem 1.5rem;
  cursor: pointer;
  border-radius: 25px;
  border: 2px solid var(--vp-c-divider);
  background: var(--vp-c-bg-soft);
  transition: all 0.3s ease;
  font-weight: 500;
  position: relative;
}

.filter-tag:hover {
  transform: translateY(-2px);
  border-color: #bd34fe;
}

.filter-tag-active {
  background: linear-gradient(120deg, #bd34fe 30%, #41d1ff);
  color: white;
  border: none;
  box-shadow: 0 4px 15px rgba(189, 52, 254, 0.4);
  padding: calc(0.6rem + 2px) calc(1.5rem + 2px);
}

.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.user-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 1.2rem 1rem;
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
  gap: 0.8rem;
  margin-bottom: 0.6rem;
}

.user-logo {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  flex-shrink: 0;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(120deg, #bd34fe 30%, #41d1ff);
  color: white;
  font-weight: 700;
  font-size: 1.2rem;
}

.user-logo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-name {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--vp-c-text-1);
  line-height: 1.3;
  flex: 1;
  margin: 0;
}

.user-description {
  color: var(--vp-c-text-2);
  margin-bottom: 0.8rem;
  line-height: 1.4;
  font-style: italic;
  font-size: 0.85rem;
}

.user-info {
  line-height: 1.6;
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
}

.user-info strong {
  color: var(--vp-c-text-1);
}

.user-info a {
  color: #667eea;
  text-decoration: none;
  transition: color 0.3s ease;
  word-break: break-all;
}

.user-info a:hover {
  color: #764ba2;
  text-decoration: underline;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  border: 2px dashed var(--vp-c-divider);
  border-radius: 16px;
  background: var(--vp-c-bg-soft);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: var(--vp-c-text-1);
}

.empty-text {
  color: var(--vp-c-text-2);
  margin-bottom: 2rem;
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
}

/* 增加内容宽度 */
:deep(.VPDoc) {
  max-width: 1600px !important; 
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }
  
  .users-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-badge {
    display: block;
    margin: 0.5rem 0;
  }
}
</style>

<div class="page-header">
  <h1 class="page-title">🚀 Who is Using FastapiAdmin</h1>
  <p class="page-subtitle">
    Thank you to every developer and enterprise who has chosen FastapiAdmin. After registration, you will receive <strong>priority technical support</strong>, and our maintenance team will respond to your issues promptly.
  </p>
  <div>
    <span class="stats-badge">👥 {{ allUsers.length }} Registered Users</span>
    <span class="stats-badge">🚀 Priority Support</span>
    <span class="stats-badge">💎 Completely Free</span>
  </div>
  <a href="https://gitee.com/fastapiadmin/FastapiAdmin/issues/IJ9NKA" target="_blank" class="register-btn">📝 Register Now</a>
</div>

<div class="search-section">
  <input
    v-model="searchKeyword"
    placeholder="🔍 Search by company / organization / project name..."
    class="search-input"
  />
</div>

<div class="filter-section">
  <span
    v-for="r in regions"
    :key="r"
    @click="activeRegion = r"
    :class="['filter-tag', { 'filter-tag-active': activeRegion === r }]"
  >{{ r }}</span>
</div>

<div v-if="filteredUsers.length > 0" class="users-grid">
  <div v-for="user in filteredUsers" :key="user.name" class="user-card">
    <div class="user-header">
      <div class="user-logo">
        <img v-if="user.logo" :src="user.logo" :alt="user.name">
        <span v-else>{{ user.name.charAt(0) }}</span>
      </div>
      <h3 class="user-name">{{ user.name }}</h3>
    </div>
    <p v-if="user.description" class="user-description">{{ user.description }}</p>
    <div class="user-info">
      📍 <strong>Location</strong>: {{ user.location }}<br>
      <template v-if="user.website">
        🌐 <strong>Chinese Website</strong>:<br>
        <a :href="user.website" target="_blank">{{ user.website }}</a><br>
      </template>
      <template v-if="user.websiteEn">
        🌐 <strong>English Website</strong>:<br>
        <a :href="user.websiteEn" target="_blank">{{ user.websiteEn }}</a><br>
      </template>
      <span v-if="user.registrant">
        👤 <strong>Registrant</strong>:
        <a v-if="user.registrantUrl" :href="user.registrantUrl" target="_blank">{{ user.registrant }}</a>
        <span v-else>{{ user.registrant }}</span>
        <br>
      </span>
      📅 <strong>Date</strong>: {{ user.date }}
    </div>
  </div>
</div>

<div v-else class="empty-state">
  <div class="empty-icon">
    {{ searchKeyword || activeRegion !== 'All' ? '🔍' : '🚀' }}
  </div>
  <h3 class="empty-title">
    {{ searchKeyword || activeRegion !== 'All' ? 'No matching users found' : 'Waiting for You' }}
  </h3>
  <p class="empty-text">
    {{ searchKeyword || activeRegion !== 'All' ? 'Try adjusting your search or region filter' : 'Be the first registered user and get priority technical support' }}
  </p>
  <a v-if="!searchKeyword && activeRegion === 'All'" href="https://gitee.com/fastapiadmin/FastapiAdmin/issues/IJ9NKA" target="_blank" class="register-btn">Register Now</a>
</div>

<div class="cta-section">
  <h2 class="cta-title">💡 Build Your Business with FastapiAdmin</h2>
  <p class="cta-text">
    Registration is completely free. FastapiAdmin is open source and free. We solemnly promise not to charge any fees at any stage, and your information will not be used for commercial profit or other non-public purposes.
  </p>
  <a href="https://gitee.com/fastapiadmin/FastapiAdmin/issues/IJ9NKA" target="_blank" class="register-btn">Register Now</a>
</div>
