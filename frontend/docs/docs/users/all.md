---
title: 所有用户
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
    name: '深圳昌红科技有限公司',
    location: '深圳 · 坪山',
    province: '广东',
    website: 'https://cn.sz-changhong.com/',
    websiteEn: 'https://www.sz-changhong.com/',
    logo: '',
    registrant: '杨向向',
    registrantUrl: 'https://gitee.com/xiao-lei',
    date: '2026-04-19',
    description: '基于 FastapiAdmin 构建的企业管理系统'
  },
  {
    name: '北京云信XX软件技术有限公司',
    location: '陕西 · 西安',
    province: '陕西',
    website: '',
    logo: '',
    registrant: '李浩',
    registrantUrl: 'https://gitee.com/aiyun_lh',
    date: '2026-04-19',
    description: '基于 FastapiAdmin 构建的单元制造执行系统'
  },
  {
    name: '上海智慧科技有限公司',
    location: '上海 · 浦东',
    province: '上海',
    website: 'https://www.sh-wisdom.com/',
    websiteEn: '',
    logo: '',
    registrant: '张伟',
    registrantUrl: 'https://gitee.com/zhangwei',
    date: '2026-04-18',
    description: '基于 FastapiAdmin 构建的智能物流管理平台'
  },
  {
    name: '杭州云端网络科技有限公司',
    location: '浙江 · 杭州',
    province: '浙江',
    website: 'https://www.hz-cloud.com/',
    websiteEn: 'https://en.hz-cloud.com/',
    logo: '',
    registrant: '王芳',
    registrantUrl: 'https://gitee.com/wangfang',
    date: '2026-04-17',
    description: '基于 FastapiAdmin 构建的云端数据分析系统'
  },
  {
    name: '成都蜀道科技有限公司',
    location: '四川 · 成都',
    province: '四川',
    website: '',
    websiteEn: '',
    logo: '',
    registrant: '刘强',
    registrantUrl: 'https://gitee.com/liuqiang',
    date: '2026-04-16',
    description: '基于 FastapiAdmin 构建的电商运营管理系统'
  },
  {
    name: '广州南方数据科技有限公司',
    location: '广东 · 广州',
    province: '广东',
    website: 'https://www.gz-data.com/',
    websiteEn: '',
    logo: '',
    registrant: '陈明',
    registrantUrl: 'https://gitee.com/chenming',
    date: '2026-04-15',
    description: '基于 FastapiAdmin 构建的大数据可视化平台'
  },
  {
    name: '南京紫金软件开发有限公司',
    location: '江苏 · 南京',
    province: '江苏',
    website: 'https://www.nj-zijin.com/',
    websiteEn: 'https://en.nj-zijin.com/',
    logo: '',
    registrant: '赵丽',
    registrantUrl: 'https://gitee.com/zhaoli',
    date: '2026-04-14',
    description: '基于 FastapiAdmin 构建的教育培训管理系统'
  },
  {
    name: '武汉长江信息技术有限公司',
    location: '湖北 · 武汉',
    province: '湖北',
    website: '',
    websiteEn: '',
    logo: '',
    registrant: '孙涛',
    registrantUrl: 'https://gitee.com/suntao',
    date: '2026-04-13',
    description: '基于 FastapiAdmin 构建的医疗健康管理平台'
  },
  {
    name: '天津滨海创新科技有限公司',
    location: '天津 · 滨海新区',
    province: '天津',
    website: 'https://www.tj-binhai.com/',
    websiteEn: '',
    logo: '',
    registrant: '周敏',
    registrantUrl: 'https://gitee.com/zhoumin',
    date: '2026-04-12',
    description: '基于 FastapiAdmin 构建的智能制造执行系统'
  },
  {
    name: '重庆山城软件有限公司',
    location: '重庆 · 渝北',
    province: '重庆',
    website: 'https://www.cq-mountain.com/',
    websiteEn: 'https://en.cq-mountain.com/',
    logo: '',
    registrant: '吴静',
    registrantUrl: 'https://gitee.com/wujing',
    date: '2026-04-11',
    description: '基于 FastapiAdmin 构建的供应链管理系统'
  }
])

const searchKeyword = ref('')
const activeProvince = ref('全部')

const provinces = computed(() => {
  const set = new Set(allUsers.value.map(u => u.province))
  return ['全部', ...Array.from(set)]
})

const filteredUsers = computed(() => {
  return allUsers.value.filter(user => {
    const matchKeyword = !searchKeyword.value ||
      user.name.includes(searchKeyword.value) ||
      user.location.includes(searchKeyword.value)
    const matchProvince = activeProvince.value === '全部' || user.province === activeProvince.value
    return matchKeyword && matchProvince
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
  <h1 class="page-title">🚀 他们在使用 FastapiAdmin</h1>
  <p class="page-subtitle">
    感谢每一位选择 FastapiAdmin 的开发者和企业。登记后，您将获得<strong>优先技术支持</strong>，我们的维护团队将第一时间响应您的问题。
  </p>
  <div>
    <span class="stats-badge">👥 {{ allUsers.length }} 位登记用户</span>
    <span class="stats-badge">🚀 优先技术支持</span>
    <span class="stats-badge">💎 完全免费</span>
  </div>
  <a href="https://gitee.com/fastapiadmin/FastapiAdmin/issues/IJ9NKA" target="_blank" class="register-btn">📝 立即登记</a>
</div>

<div class="search-section">
  <input
    v-model="searchKeyword"
    placeholder="🔍 搜索公司/组织/项目名称..."
    class="search-input"
  />
</div>

<div class="filter-section">
  <span
    v-for="p in provinces"
    :key="p"
    @click="activeProvince = p"
    :class="['filter-tag', { 'filter-tag-active': activeProvince === p }]"
  >{{ p }}</span>
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
      📍 <strong>所在地区</strong>：{{ user.location }}<br>
      <template v-if="user.website">
        🌐 <strong>中文官网</strong>：<br>
        <a :href="user.website" target="_blank">{{ user.website }}</a><br>
      </template>
      <template v-if="user.websiteEn">
        🌐 <strong>英文官网</strong>：<br>
        <a :href="user.websiteEn" target="_blank">{{ user.websiteEn }}</a><br>
      </template>
      <span v-if="user.registrant">
        👤 <strong>登记人</strong>：
        <a v-if="user.registrantUrl" :href="user.registrantUrl" target="_blank">{{ user.registrant }}</a>
        <span v-else>{{ user.registrant }}</span>
        <br>
      </span>
      📅 <strong>登记时间</strong>：{{ user.date }}
    </div>
  </div>
</div>

<div v-else class="empty-state">
  <div class="empty-icon">
    {{ searchKeyword || activeProvince !== '全部' ? '🔍' : '🚀' }}
  </div>
  <h3 class="empty-title">
    {{ searchKeyword || activeProvince !== '全部' ? '未找到匹配的用户' : '期待您的加入' }}
  </h3>
  <p class="empty-text">
    {{ searchKeyword || activeProvince !== '全部' ? '尝试调整搜索关键词或地区筛选' : '成为第一个登记的用户，获得优先技术支持' }}
  </p>
  <a v-if="!searchKeyword && activeProvince === '全部'" href="https://gitee.com/fastapiadmin/FastapiAdmin/issues/IJ9NKA" target="_blank" class="register-btn">立即登记</a>
</div>

<div class="cta-section">
  <h2 class="cta-title">💡 基于 FastapiAdmin 开发你的业务</h2>
  <p class="cta-text">
    登记完全免费，FastapiAdmin 项目开源且免费。我们郑重承诺，不会在任何阶段向您收取任何形式的使用费用，您的信息也不会被用于商业盈利或其他非公开目的。
  </p>
  <a href="https://gitee.com/fastapiadmin/FastapiAdmin/issues/IJ9NKA" target="_blank" class="register-btn">立即登记</a>
</div>
