---
title: Sponsor FastApiAdmin
sidebar: false
aside: false
---

<style>
/* Global styles - increase page width */
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

const benefits = [
  { icon: '🌐', title: 'Website Operations', desc: 'Cover domain and server costs' },
  { icon: '🛠️', title: 'Development Tools', desc: 'Purchase professional dev tools' },
  { icon: '💬', title: 'Tech Support', desc: 'Provide better technical support' },
  { icon: '⚡', title: 'Continuous Dev', desc: 'Invest more energy in development' },
  { icon: '✨', title: 'Code Optimization', desc: 'Continuously optimize code quality' },
  { icon: '🚀', title: 'Feature R&D', desc: 'Develop more practical features' }
]

const honorarySponsors = [
  { name: '晨曦微光', avatar: '', amount: '$73.35', date: '2026-04' },
  { name: 'Alex_Chen', avatar: '', amount: '$44.01', date: '2026-04' },
  { name: '一叶知秋', avatar: '', amount: '$29.34', date: '2026-03' },
  { name: 'coding小王子', avatar: '', amount: '$73.35', date: '2026-03' },
  { name: 'Mr.Zhang', avatar: '', amount: '$14.67', date: '2026-03' },
  { name: '墨染青衣', avatar: '', amount: '$29.34', date: '2026-02' },
  { name: 'sky_walker', avatar: '', amount: '$44.01', date: '2026-02' },
  { name: '浅笑_安然', avatar: '', amount: '$22.01', date: '2026-02' },
  { name: 'Jason.Liu', avatar: '', amount: '$29.34', date: '2026-01' },
  { name: '梦里花落', avatar: '', amount: '$14.67', date: '2026-01' },
  { name: 'Leo_李', avatar: '', amount: '$73.35', date: '2026-01' },
  { name: '岁月静好', avatar: '', amount: '$29.34', date: '2025-12' },
  { name: 'code_monkey', avatar: '', amount: '$22.01', date: '2025-12' },
  { name: '北城以北', avatar: '', amount: '$44.01', date: '2025-11' },
  { name: 'Emma.Wang', avatar: '', amount: '$14.67', date: '2025-11' },
  { name: '烟雨_江南', avatar: '', amount: '$29.34', date: '2025-11' },
  { name: 'tech_lover88', avatar: '', amount: '$22.01', date: '2025-10' },
  { name: '清风徐来', avatar: '', amount: '$44.01', date: '2025-10' },
  { name: 'David.Zhou', avatar: '', amount: '$29.34', date: '2025-10' },
  { name: 'python小白', avatar: '', amount: '$14.67', date: '2025-09' }
]

const tiers = [
  {
    name: 'Exclusive Sponsor',
    icon: '👑',
    level: 'exclusive',
    price: 'Contact via WeChat/month',
    color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    benefits: [
      'Exclusive Logo on homepage above the fold',
      'First carousel position on demo site',
      'Exclusive Logo at top of left sidebar on all pages',
      'Exclusive product launch via all groups + official account (monthly)'
    ],
    requirements: 'Brand name + Official link + Logo (340px*160px) + Slogan'
  },
  {
    name: 'Platinum Sponsor',
    icon: '💎',
    level: 'platinum',
    price: 'Contact via WeChat/month',
    color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    benefits: [
      'Prominent Logo on homepage',
      'Prominent Logo on demo site homepage',
      'Prominent Logo at top of left sidebar',
      'Product promotion via all groups (monthly)'
    ],
    requirements: 'Brand name + Official link + Logo (340px*160px)'
  },
  {
    name: 'Gold Sponsor',
    icon: '🥇',
    level: 'gold',
    price: 'Contact via WeChat/month',
    color: 'linear-gradient(135deg, #f6d365 0%, #fda085 100%)',
    benefits: [
      'Large Logo on homepage',
      'Large Logo in right sidebar on all pages',
      'Product promotion via latest 3 groups (monthly)'
    ],
    requirements: 'Brand name + Official link + Logo (220px*70px)'
  },
  {
    name: 'Silver Sponsor',
    icon: '🥈',
    level: 'silver',
    price: 'Contact via WeChat/month',
    color: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    benefits: [
      'Small Logo in right sidebar on all pages'
    ],
    requirements: 'Brand name + Official link + Logo (110px*60px)'
  }
]

const currentSponsors = {
  exclusive: [
    {
      name: 'CoderXSLee',
      logo: 'https://foruda.gitee.com/avatar/1725853866438762352/562111_coderxslee_1725853866.png!avatar200',
      website: 'https://www.gitee.com/coderxslee',
      description: '',
      amount: '$14.67'
    }
  ],
  platinum: [
    // {
    //   name: 'DevTools Pro',
    //   logo: '',
    //   website: 'https://www.devtools-pro.com',
    //   description: 'Professional development tools and services',
    //   amount: '$800'
    // },
    // {
    //   name: 'Tech Academy',
    //   logo: '',
    //   website: 'https://www.tech-academy.com',
    //   description: 'Online technical courses and training',
    //   amount: '$800'
    // }
  ],
  gold: [
    // {
    //   name: 'Cloud Plus',
    //   logo: '',
    //   website: 'https://www.cloud-plus.com',
    //   description: 'Enterprise cloud service solutions',
    //   amount: '$500'
    // },
    // {
    //   name: 'Code Light',
    //   logo: '',
    //   website: 'https://www.code-light.com',
    //   description: 'Developer community and tech blog',
    //   amount: '$500'
    // },
    // {
    //   name: 'Smart IDE',
    //   logo: '',
    //   website: 'https://www.smart-ide.com',
    //   description: 'Next-gen intelligent development environment',
    //   amount: '$500'
    // }
  ],
  silver: [
    // {
    //   name: 'Keyboard Master',
    //   logo: '',
    //   website: 'https://www.keyboard-master.com',
    //   description: 'Professional mechanical keyboard brand',
    //   amount: '$150'
    // },
    // {
    //   name: 'Monitor Pro',
    //   logo: '',
    //   website: 'https://www.monitor-pro.com',
    //   description: 'Monitors designed for programmers',
    //   amount: '$150'
    // },
    // {
    //   name: 'Coffee Coder',
    //   logo: '',
    //   website: 'https://www.coffee-coder.com',
    //   description: 'Premium coffee for programmers',
    //   amount: '$150'
    // },
    // {
    //   name: 'Tech Books',
    //   logo: '',
    //   website: 'https://www.tech-books.com',
    //   description: 'Technical books and e-book platform',
    //   amount: '$150'
    // }
  ]
}
</script>

<style scoped>
.hero-section {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(120deg, #bd34fe 30%, #41d1ff);
  border-radius: 16px;
  color: white;
  margin-bottom: 3rem;
  box-shadow: 0 10px 40px rgba(189, 52, 254, 0.3);
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
  animation: pulse 15s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 0.8; }
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  position: relative;
  z-index: 1;
}

.hero-subtitle {
  font-size: 1.2rem;
  opacity: 0.95;
  margin-bottom: 2rem;
  line-height: 1.8;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
  position: relative;
  z-index: 1;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  position: relative;
  z-index: 1;
}

.btn {
  padding: 1rem 2.5rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  display: inline-block;
  font-size: 1.1rem;
}

.btn-primary {
  background: white;
  color: #667eea;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid white;
  backdrop-filter: blur(10px);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-3px);
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  margin: 4rem 0 2rem;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.benefit-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
}

.benefit-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
  border-color: rgba(102, 126, 234, 0.4);
}

.benefit-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.benefit-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--vp-c-text-1);
  margin-bottom: 0.5rem;
}

.benefit-desc {
  font-size: 0.9rem;
  color: var(--vp-c-text-2);
}

.tip-box {
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.1) 0%, rgba(255, 152, 0, 0.1) 100%);
  border-left: 4px solid #ffc107;
  border-radius: 8px;
  padding: 1.5rem;
  margin: 2rem 0;
}

.tip-box strong {
  color: #f57c00;
}

.tiers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.2rem;
  margin-bottom: 3rem;
}

.tier-card {
  background: var(--vp-c-bg-soft);
  border: 2px solid var(--vp-c-divider);
  border-radius: 16px;
  padding: 0;
  transition: all 0.3s ease;
  overflow: hidden;
  position: relative;
}

.tier-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 50px rgba(102, 126, 234, 0.3);
}

/* Special effects for high-tier sponsors */
.tier-card:nth-child(1),
.tier-card:nth-child(2) {
  border-width: 3px;
}

.tier-card:nth-child(1) {
  border-color: rgba(102, 126, 234, 0.5);
  box-shadow: 0 8px 30px rgba(102, 126, 234, 0.15);
}

.tier-card:nth-child(2) {
  border-color: rgba(245, 87, 108, 0.5);
  box-shadow: 0 8px 30px rgba(245, 87, 108, 0.15);
}

.tier-card:nth-child(1):hover {
  box-shadow: 0 20px 50px rgba(102, 126, 234, 0.4);
  border-color: rgba(102, 126, 234, 0.8);
}

.tier-card:nth-child(2):hover {
  box-shadow: 0 20px 50px rgba(245, 87, 108, 0.4);
  border-color: rgba(245, 87, 108, 0.8);
}

.tier-header {
  padding: 1.5rem;
  color: white;
  text-align: center;
  position: relative;
  overflow: hidden;
}

/* Silver sponsor uses dark text */
.tier-card:nth-child(4) .tier-header {
  color: #2c3e50;
}

.tier-icon {
  font-size: 2.5rem;
  margin-bottom: 0.8rem;
  display: block;
}

.tier-name {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 0.6rem;
}

.tier-price {
  font-size: 0.9rem;
  opacity: 0.9;
}

.tier-body {
  padding: 1.5rem;
}

.tier-benefits {
  list-style: none;
  padding: 0;
  margin: 0 0 1.2rem 0;
}

.tier-benefits li {
  padding: 0.35rem 0;
  border-bottom: 1px solid var(--vp-c-divider);
  display: flex;
  align-items: flex-start;
  gap: 0.4rem;
  color: var(--vp-c-text-2);
  line-height: 1.3;
  font-size: 0.85rem;
}

.tier-benefits li:last-child {
  border-bottom: none;
}

.tier-benefits li::before {
  content: '✓';
  color: #10b981;
  font-weight: 700;
  flex-shrink: 0;
  font-size: 0.9rem;
}

.tier-requirements {
  background: rgba(102, 126, 234, 0.05);
  border-radius: 8px;
  padding: 0.8rem;
  font-size: 0.8rem;
  color: var(--vp-c-text-2);
  margin-bottom: 1.2rem;
  line-height: 1.4;
}

.tier-requirements strong {
  color: var(--vp-c-text-1);
  display: block;
  margin-bottom: 0.4rem;
  font-size: 0.85rem;
}

.tier-button {
  display: block;
  width: 100%;
  padding: 0.8rem;
  background: linear-gradient(120deg, #bd34fe 30%, #41d1ff);
  color: white;
  text-align: center;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.tier-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(189, 52, 254, 0.4);
  color: white;
}

.guidelines-section {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 2rem;
  margin: 3rem 0;
}

.guidelines-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--vp-c-text-1);
  margin-bottom: 1rem;
}

.guidelines-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.guidelines-list li {
  padding: 0.4rem 0;
  padding-left: 1.2rem;
  position: relative;
  color: var(--vp-c-text-2);
  line-height: 1.8;
}

.guidelines-list li::before {
  content: '•';
  position: absolute;
  left: 0;
  top: 0.4rem;
  color: #667eea;
  font-weight: 700;
  font-size: 1rem;
  line-height: 1.8;
}

.example-box {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1rem 0;
  font-family: monospace;
  font-size: 0.9rem;
  color: var(--vp-c-text-2);
  white-space: pre-line;
}

.sponsors-section {
  margin: 3rem 0;
}

.sponsor-tier {
  margin-bottom: 2rem;
}

.sponsor-tier-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--vp-c-text-1);
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.empty-sponsors {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border: 2px dashed rgba(102, 126, 234, 0.3);
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  color: var(--vp-c-text-2);
}

.sponsors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
}

.sponsor-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
  text-decoration: none;
  display: block;
}

.sponsor-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
  border-color: rgba(102, 126, 234, 0.4);
}

.sponsor-logo {
  width: 60px;
  height: 60px;
  margin: 0 auto 1rem;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(120deg, rgba(189, 52, 254, 0.5) 30%, rgba(65, 209, 255, 0.5));
  color: white;
  font-weight: 700;
  font-size: 1.8rem;
}

.sponsor-logo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.sponsor-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--vp-c-text-1);
  margin-bottom: 0.5rem;
}

.sponsor-desc {
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
  line-height: 1.4;
  margin-bottom: 0.8rem;
}

.sponsor-amount {
  font-size: 1rem;
  font-weight: 700;
  color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  display: inline-block;
}

.cta-section {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border: 2px dashed rgba(102, 126, 234, 0.3);
  border-radius: 16px;
  padding: 1.5rem 3rem 3rem 3rem;
  text-align: center;
  margin: 3rem 0;
  overflow: hidden;
}

.cta-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0 0 1.5rem 0;
  padding: 0 0 1.5rem 0;
  border-bottom: 1px solid var(--vp-c-divider);
  border-top: none;
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

.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.contact-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
}

.contact-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
  border-color: rgba(102, 126, 234, 0.4);
}

.contact-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.contact-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--vp-c-text-1);
  margin-bottom: 0.5rem;
}

.contact-link {
  color: #667eea;
  text-decoration: none;
  word-break: break-all;
  font-size: 0.9rem;
}

.contact-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

.honorary-sponsors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 1rem;
  margin-top: 2rem;
}

.honorary-sponsor-card {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  padding: 1.5rem 1rem;
  text-align: center;
  transition: all 0.3s ease;
}

.honorary-sponsor-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
  border-color: rgba(102, 126, 234, 0.4);
}

.honorary-avatar {
  width: 50px;
  height: 50px;
  margin: 0 auto 0.8rem;
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(120deg, rgba(189, 52, 254, 0.5) 30%, rgba(65, 209, 255, 0.5));
  color: white;
  font-weight: 700;
  font-size: 1.2rem;
}

.honorary-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.honorary-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin-bottom: 0.5rem;
}

.honorary-amount {
  font-size: 0.9rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 0.3rem;
}

.honorary-date {
  font-size: 0.75rem;
  color: var(--vp-c-text-2);
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .tiers-grid {
    grid-template-columns: 1fr;
  }
  
  .benefits-grid {
    grid-template-columns: 1fr;
  }
}
</style>

<div class="hero-section">
  <h1 class="hero-title">💖 Sponsor FastApiAdmin</h1>
  <p class="hero-subtitle">
    Thank you for considering supporting the FastApiAdmin open-source project!<br>
    FastApiAdmin is licensed under the MIT open-source license, allowing free commercial use.<br>
    Since the project's release, we have been committed to continuous iteration and optimization with great passion.
  </p>
  <div class="hero-buttons">
    <a href="#sponsorship-tiers" class="btn btn-primary">💎 View Tiers</a>
    <a href="https://service.fastapiadmin.com/en/about/#%F0%9F%8E%A8-about-us" target="_blank" class="btn btn-secondary">📞 Contact Us</a>
  </div>
</div>

<h2 class="section-title">🎯 Your Support Will Help Us</h2>

<div class="benefits-grid">
  <div v-for="benefit in benefits" :key="benefit.title" class="benefit-card">
    <div class="benefit-icon">{{ benefit.icon }}</div>
    <div class="benefit-title">{{ benefit.title }}</div>
    <div class="benefit-desc">{{ benefit.desc }}</div>
  </div>
</div>

<h2 id="sponsorship-tiers" class="section-title">💎 Sponsorship Tiers and Benefits</h2>

<div class="tip-box">
  <strong>💡 Note:</strong> The conversion effectiveness of sponsorship displays may be affected by various factors such as market environment and audience characteristics. We cannot guarantee specific conversion results.
</div>

<div class="tiers-grid">
  <div v-for="tier in tiers" :key="tier.level" class="tier-card">
    <div class="tier-header" :style="{ background: tier.color }">
      <span class="tier-icon">{{ tier.icon }}</span>
      <div class="tier-name">{{ tier.name }}</div>
      <div class="tier-price">{{ tier.price }}</div>
    </div>
    <div class="tier-body">
      <ul class="tier-benefits">
        <li v-for="(benefit, index) in tier.benefits" :key="index">{{ benefit }}</li>
      </ul>
      <div class="tier-requirements">
        <strong>Required Materials:</strong>
        {{ tier.requirements }}
      </div>
      <a href="#contact-us" class="tier-button">Sponsor Now</a>
    </div>
  </div>
</div>

<div class="guidelines-section">
  <div class="guidelines-title">📋 Content Guidelines</div>
  <ul class="guidelines-list">
    <li>We recommend promoting products or services related to developers, such as low-code platforms, technical courses, development tools, cloud services, personal blogs, and physical products like keyboards, monitors, headphones, etc.</li>
    <li>Products with low relevance to the developer community should be considered carefully.</li>
    <li>We refuse to promote products that violate laws and regulations, involve gray industries, as well as IP proxies, internet access tools, etc.</li>
    <li>To avoid excessive disturbance to group members, promotions in communication groups should not exceed twice per day, with excess portions deferred to the next day.</li>
  </ul>
  
  <div class="guidelines-title" style="margin-top: 2rem;">📢 Group Message Example</div>
  <div class="example-box">Thank you xxx for the special sponsorship of the FastApiAdmin open-source project! Here is their product information for those interested:
【Product Name】
【Official Link】https://xxx.com</div>
</div>

<h2 class="section-title">🌟 Current Sponsors</h2>

<div class="sponsors-section">
  <div class="sponsor-tier">
    <div class="sponsor-tier-title">👑 Exclusive Sponsor</div>
    <div v-if="currentSponsors.exclusive.length === 0" class="empty-sponsors">Currently vacant, looking forward to your participation</div>
    <div v-else class="sponsors-grid">
      <a v-for="sponsor in currentSponsors.exclusive" :key="sponsor.name" :href="sponsor.website" target="_blank" class="sponsor-card">
        <div class="sponsor-logo">
          <img v-if="sponsor.logo" :src="sponsor.logo" :alt="sponsor.name">
          <span v-else>{{ sponsor.name.charAt(0) }}</span>
        </div>
        <div class="sponsor-name">{{ sponsor.name }}</div>
        <div class="sponsor-desc">{{ sponsor.description }}</div>
        <div class="sponsor-amount">{{ sponsor.amount }}/month</div>
      </a>
    </div>
  </div>
  
  <div class="sponsor-tier">
    <div class="sponsor-tier-title">💎 Platinum Sponsor</div>
    <div v-if="currentSponsors.platinum.length === 0" class="empty-sponsors">Currently vacant, looking forward to your participation</div>
    <div v-else class="sponsors-grid">
      <a v-for="sponsor in currentSponsors.platinum" :key="sponsor.name" :href="sponsor.website" target="_blank" class="sponsor-card">
        <div class="sponsor-logo">
          <img v-if="sponsor.logo" :src="sponsor.logo" :alt="sponsor.name">
          <span v-else>{{ sponsor.name.charAt(0) }}</span>
        </div>
        <div class="sponsor-name">{{ sponsor.name }}</div>
        <div class="sponsor-desc">{{ sponsor.description }}</div>
        <div class="sponsor-amount">{{ sponsor.amount }}/month</div>
      </a>
    </div>
  </div>
  
  <div class="sponsor-tier">
    <div class="sponsor-tier-title">🥇 Gold Sponsor</div>
    <div v-if="currentSponsors.gold.length === 0" class="empty-sponsors">Currently vacant, looking forward to your participation</div>
    <div v-else class="sponsors-grid">
      <a v-for="sponsor in currentSponsors.gold" :key="sponsor.name" :href="sponsor.website" target="_blank" class="sponsor-card">
        <div class="sponsor-logo">
          <img v-if="sponsor.logo" :src="sponsor.logo" :alt="sponsor.name">
          <span v-else>{{ sponsor.name.charAt(0) }}</span>
        </div>
        <div class="sponsor-name">{{ sponsor.name }}</div>
        <div class="sponsor-desc">{{ sponsor.description }}</div>
        <div class="sponsor-amount">{{ sponsor.amount }}/month</div>
      </a>
    </div>
  </div>
  
  <div class="sponsor-tier">
    <div class="sponsor-tier-title">🥈 Silver Sponsor</div>
    <div v-if="currentSponsors.silver.length === 0" class="empty-sponsors">Currently vacant, looking forward to your participation</div>
    <div v-else class="sponsors-grid">
      <a v-for="sponsor in currentSponsors.silver" :key="sponsor.name" :href="sponsor.website" target="_blank" class="sponsor-card">
        <div class="sponsor-logo">
          <img v-if="sponsor.logo" :src="sponsor.logo" :alt="sponsor.name">
          <span v-else>{{ sponsor.name.charAt(0) }}</span>
        </div>
        <div class="sponsor-name">{{ sponsor.name }}</div>
        <div class="sponsor-desc">{{ sponsor.description }}</div>
        <div class="sponsor-amount">{{ sponsor.amount }}/month</div>
      </a>
    </div>
  </div>
</div>

<div class="cta-section">
  <h2 class="cta-title">☕ Honorary Sponsorship</h2>
  <p class="cta-text">
    You can sponsor through the appreciation codes of maintenance team members on the <a href="/en/about/" style="color: #667eea; text-decoration: none;">About Us</a> page.<br>
    Buy a cup of coffee for the FastApiAdmin maintenance team members!
  </p>
  
  <div class="honorary-sponsors-grid">
    <div v-for="sponsor in honorarySponsors" :key="sponsor.name + sponsor.date" class="honorary-sponsor-card">
      <div class="honorary-avatar">
        <img v-if="sponsor.avatar" :src="sponsor.avatar" :alt="sponsor.name">
        <span v-else>{{ sponsor.name.charAt(0) }}</span>
      </div>
      <div class="honorary-name">{{ sponsor.name }}</div>
      <div class="honorary-amount">{{ sponsor.amount }}</div>
      <div class="honorary-date">{{ sponsor.date }}</div>
    </div>
  </div>
</div>

<div class="cta-section" style="margin-top: 3rem;">
  <h2 class="cta-title">🎉 Looking Forward to Working with You</h2>
  <p class="cta-text">
    If you are interested in sponsoring the FastApiAdmin project or want to learn more,<br>
    please feel free to contact us through the above methods. We will be happy to serve you!
  </p>
  <a href="https://service.fastapiadmin.com/en/about/#%F0%9F%8E%A8-about-us" target="_blank" class="btn btn-primary">Contact Us Now</a>
</div>
