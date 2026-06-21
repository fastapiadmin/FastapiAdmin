<template>
  <div ref="containerRef" class="screen-container">
    <canvas ref="canvasRef" class="particle-canvas" />
    <div class="scan-line scan-1" />
    <div class="scan-line scan-2" />

    <ScreenHeader />

    <!-- 顶部核心指标卡 x6 -->
    <div class="stat-row">
      <div v-for="s in stats" :key="s.label" class="stat-card">
        <div class="stat-val" :class="'stat-' + s.color">{{ s.value }}</div>
        <div class="stat-label">{{ s.label }}</div>
        <div class="stat-sub">
          <span :class="s.up ? 'up' : 'down'">{{ s.up ? "▲" : "▼" }} {{ s.change }}</span>
          <span class="stat-vs">较昨日</span>
        </div>
      </div>
    </div>

    <!-- 主体布局 -->
    <div class="screen-grid">
      <!-- 左列 -->
      <ServiceLevel class="gp-r1 gp-c1-3" />
      <TargetReality class="gp-r2 gp-c1-3" />

      <!-- 中间左 -->
      <LiveMetrics class="gp-r1 gp-c3-5" />
      <FunnelChart class="gp-r2 gp-c3-5" />

      <!-- 中国地图 -->
      <div class="panel p1 map-panel gp-r1 gp-c5-9" style="grid-row: 1 / 3">
        <FaMapChart :dynamic="true" />
      </div>

      <!-- 中间右 -->
      <ChannelDonut class="gp-r1 gp-c9-11" />
      <UserProfile class="gp-r2 gp-c9-11" />

      <!-- 右列 -->
      <ProductBar class="gp-r1 gp-c11-13" />
      <RealtimeMessages class="gp-r2 gp-c11-13" />
    </div>

    <!-- 大卡片行 x6 统计图 -->
    <div class="card-row">
      <MiniRevenue />
      <MiniOrders />
      <MiniTraffic />
      <MiniRefund />
      <MiniInventory />
      <MiniRating />
    </div>

    <!-- 底部状态栏 -->
    <div class="bottom-bar">
      <div class="bb-item"><span class="bb-dot pulse" />系统运行正常</div>
      <div class="bb-item">数据更新时间：{{ updateTime }}</div>
      <div class="bb-ticker">
        <span class="ticker-track">
          <span v-for="t in tickerItems" :key="t" class="ticker-item">{{ t }}</span>
        </span>
      </div>
      <div class="bb-items-right">
        <div v-for="s in structItems" :key="s.label" class="bb-meta">
          <span class="bb-meta-dot" :class="'sr-' + s.cls" />
          {{ s.label }}: {{ s.value }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  defineAsyncComponent,
  onMounted,
  onUnmounted,
  provide,
  reactive,
  ref,
  shallowRef,
} from "vue";
import ScreenHeader from "./modules/ScreenHeader.vue";
import ServiceLevel from "./modules/ServiceLevel.vue";
import TargetReality from "./modules/TargetReality.vue";
import LiveMetrics from "./modules/LiveMetrics.vue";
import FunnelChart from "./modules/FunnelChart.vue";
import ChannelDonut from "./modules/ChannelDonut.vue";
import UserProfile from "./modules/UserProfile.vue";
import ProductBar from "./modules/ProductBar.vue";
import RealtimeMessages from "./modules/RealtimeMessages.vue";
import MiniRevenue from "./modules/MiniRevenue.vue";
import MiniOrders from "./modules/MiniOrders.vue";
import MiniTraffic from "./modules/MiniTraffic.vue";
import MiniRefund from "./modules/MiniRefund.vue";
import MiniInventory from "./modules/MiniInventory.vue";
import MiniRating from "./modules/MiniRating.vue";

defineOptions({ name: "DashboardScreen" });

const FaMapChart = defineAsyncComponent(() => import("@/components/charts/fa-map-chart/index.vue"));

const containerRef = ref<HTMLDivElement>();
const canvasRef = ref<HTMLCanvasElement>();
const isFullscreen = ref(false);
const updateTime = ref("");
const tickerItems = ref([
  "交易引擎: 23%",
  "消息队列: 58%",
  "缓存命中: 94.1%",
  "网关吞吐: 128Mbps",
  "QPS: 3.2K",
  "P99 延迟: 12ms",
]);
const animFrame = shallowRef(0);
let statsTimer = 0;

const stats = reactive([
  { label: "总交易额", value: "¥128.6万", change: "12.5%", up: true, color: "cyan" as const },
  { label: "订单总量", value: "8,350", change: "8.2%", up: true, color: "purple" as const },
  { label: "活跃商户", value: "1,286", change: "3.1%", up: true, color: "green" as const },
  { label: "售后工单", value: "356", change: "5.7%", up: false, color: "warn" as const },
  { label: "平均客单价", value: "¥468", change: "2.3%", up: true, color: "teal" as const },
  { label: "支付转化率", value: "38.2%", change: "1.8%", up: true, color: "rose" as const },
]);

const structItems = reactive([
  { label: "交易节点", value: "128", cls: "cyan" },
  { label: "主数据库", value: "运行中", cls: "green" },
  { label: "缓存集群", value: "94.1%", cls: "purple" },
  { label: "带宽使用", value: "1.2G", cls: "warn" },
  { label: "存储容量", value: "2.4T", cls: "cyan" },
  { label: "工作节点", value: "32", cls: "green" },
  { label: "API 网关", value: "99.9%", cls: "purple" },
  { label: "日志服务", value: "运行中", cls: "cyan" },
]);

function fmt(n: number): string {
  return n >= 10000 ? (n / 10000).toFixed(1) + "万" : n.toLocaleString();
}
function randFloat(base: number, pct: number): number {
  return base * (1 + (Math.random() - 0.5) * pct * 2);
}
function randPct(): string {
  return (Math.random() * 15 - 3).toFixed(1) + "%";
}

function updateStats() {
  const t = randFloat(1286000, 0.05);
  const o = randFloat(8350, 0.04);
  const m = randFloat(1286, 0.03);
  const w = randFloat(356, 0.08);
  stats[0]!.value = "¥" + fmt(Math.round(t));
  stats[1]!.value = fmt(Math.round(o));
  stats[2]!.value = fmt(Math.round(m));
  stats[3]!.value = fmt(Math.round(w));
  stats[4]!.value = "¥" + Math.round(randFloat(468, 0.03));
  stats[5]!.value = randFloat(38.2, 0.06).toFixed(1) + "%";
  stats[0]!.change = randPct();
  stats[0]!.up = Math.random() > 0.3;
  stats[1]!.change = randPct();
  stats[1]!.up = Math.random() > 0.4;
  stats[2]!.change = randPct();
  stats[2]!.up = Math.random() > 0.5;
  stats[3]!.change = randPct();
  stats[3]!.up = Math.random() > 0.6;
  stats[4]!.change = randPct();
  stats[4]!.up = Math.random() > 0.3;
  stats[5]!.change = randPct();
  stats[5]!.up = Math.random() > 0.4;
}

async function toggleFullscreen() {
  try {
    if (document.fullscreenElement) {
      await document.exitFullscreen();
    } else {
      await containerRef.value?.requestFullscreen();
    }
  } catch {
    /* ignored */
  }
}

function onFullscreenChange() {
  isFullscreen.value = !!document.fullscreenElement;
}

// fullscreenchange 是 document 级别事件，必须在 onUnmounted 中清理，
// 否则 keep-alive / 重复进入会累积监听器
onMounted(() => {
  document.addEventListener("fullscreenchange", onFullscreenChange);
});

onUnmounted(() => {
  document.removeEventListener("fullscreenchange", onFullscreenChange);
});

provide("toggleFullscreen", toggleFullscreen);
provide("isFullscreen", isFullscreen);

/* ========== 粒子背景 ========== */
let ctx: CanvasRenderingContext2D | null = null;
interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  r: number;
}
let particles: Particle[] = [];

function initParticles() {
  const c = canvasRef.value;
  if (!c) return;
  ctx = c.getContext("2d");
  resizeCanvas();
  spawnParticles();
  tick();
}

function resizeCanvas() {
  const c = canvasRef.value;
  if (!c || !containerRef.value) return;
  c.width = containerRef.value.clientWidth;
  c.height = containerRef.value.clientHeight;
}

function spawnParticles() {
  const c = canvasRef.value;
  if (!c) return;
  const count = Math.floor((c.width * c.height) / 18000);
  particles = Array.from({ length: count }, () => ({
    x: Math.random() * c.width,
    y: Math.random() * c.height,
    vx: (Math.random() - 0.5) * 0.4,
    vy: (Math.random() - 0.5) * 0.4,
    r: Math.random() * 1.5 + 0.5,
  }));
}

function tick() {
  if (!ctx || !canvasRef.value) return;
  const c = canvasRef.value;
  const w = c.width;
  const h = c.height;
  ctx.clearRect(0, 0, w, h);

  for (const p of particles) {
    p.x += p.vx;
    p.y += p.vy;
    if (p.x < 0) p.x = w;
    if (p.x > w) p.x = 0;
    if (p.y < 0) p.y = h;
    if (p.y > h) p.y = 0;
  }

  for (let i = 0; i < particles.length; i++) {
    const a = particles[i]!;
    ctx.beginPath();
    ctx.arc(a.x, a.y, a.r, 0, Math.PI * 2);
    ctx.fillStyle = "rgba(0,212,255,0.25)";
    ctx.fill();

    for (let j = i + 1; j < particles.length; j++) {
      const b = particles[j]!;
      const dx = a.x - b.x;
      const dy = a.y - b.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 120) {
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.strokeStyle = `rgba(0,212,255,${0.06 * (1 - dist / 120)})`;
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }
    }
  }

  animFrame.value = requestAnimationFrame(tick);
}

onMounted(() => {
  const timeTick = () => {
    updateTime.value = new Date().toLocaleTimeString("zh-CN", { hour12: false });
  };
  timeTick();
  window.setInterval(timeTick, 1000);
  initParticles();
  statsTimer = window.setInterval(updateStats, 3000);
  updateStats();
  window.addEventListener("resize", () => {
    resizeCanvas();
    spawnParticles();
  });
});

onUnmounted(() => {
  cancelAnimationFrame(animFrame.value);
  clearInterval(statsTimer);
  document.removeEventListener("fullscreenchange", onFullscreenChange);
  if (document.fullscreenElement) {
    document.exitFullscreen().catch(() => {});
  }
});
</script>

<style scoped>
.screen-container {
  --bg: #060b24;
  --accent: #00d4ff;
  --text: #b8c6e0;
  --border: rgb(0 180 255 / 12%);

  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  font-family: "PingFang SC", "Microsoft YaHei", monospace;
  color: var(--text);
  background: var(--bg);
}

.particle-canvas {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

.scan-line {
  position: absolute;
  left: 0;
  z-index: 1;
  width: 100%;
  height: 1px;
  pointer-events: none;
  opacity: 0.08;
  will-change: transform;
}

.scan-1 {
  top: 0;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
  animation: scanDown 6s linear infinite;
}

.scan-2 {
  top: 100%;
  background: linear-gradient(90deg, transparent, #7c3aed, transparent);
  animation: scanDown 6s linear 3s infinite;
}
@keyframes scanDown {
  0% {
    transform: translateY(0);
  }

  100% {
    transform: translateY(-100vh);
  }
}

/* ===== 背景网格 ===== */
.screen-container::after {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  content: "";
  background-image:
    linear-gradient(rgb(0 212 255 / 3%) 1px, transparent 1px),
    linear-gradient(90deg, rgb(0 212 255 / 3%) 1px, transparent 1px);
  background-size: 60px 60px;
}

/* ===== 顶部指标卡 ===== */
.stat-row {
  position: relative;
  z-index: 2;
  display: flex;
  flex-shrink: 0;
  gap: 16px;
  padding: 0 16px 16px;
}

.stat-card {
  position: relative;
  display: flex;
  flex: 1;
  flex-direction: column;
  justify-content: center;
  padding: 18px 24px;
  overflow: hidden;
  background: linear-gradient(135deg, rgb(0 20 60 / 60%) 0%, rgb(0 10 40 / 50%) 100%);
  border: 1px solid var(--border);
  border-radius: 10px;
}

.stat-card::before {
  position: absolute;
  top: -1px;
  right: 14px;
  left: 14px;
  height: 1px;
  content: "";
  background: linear-gradient(90deg, transparent, rgb(0 212 255 / 40%), transparent);
}

.stat-card::after {
  position: absolute;
  top: 4px;
  left: 4px;
  width: 8px;
  height: 8px;
  content: "";
  border-top: 1px solid rgb(0 212 255 / 50%);
  border-left: 1px solid rgb(0 212 255 / 50%);
}

.stat-val {
  margin-bottom: 6px;
  font-size: 28px;
  font-weight: 800;
  line-height: 1;
}

.stat-cyan {
  color: #00d4ff;
}

.stat-purple {
  color: #7c3aed;
}

.stat-green {
  color: #10b981;
}

.stat-warn {
  color: #f59e0b;
}

.stat-teal {
  color: #14b8a6;
}

.stat-rose {
  color: #f43f5e;
}

.stat-label {
  margin-bottom: 6px;
  font-size: 11px;
  opacity: 0.4;
}

.stat-sub {
  display: flex;
  gap: 6px;
  align-items: center;
  font-size: 10px;
}

.stat-sub .up {
  color: #10b981;
}

.stat-sub .down {
  color: #f59e0b;
}

.stat-vs {
  opacity: 0.3;
}

/* ===== Grid 主体 ===== */
.screen-grid {
  position: relative;
  z-index: 2;
  display: grid;
  flex: 1;
  grid-template-rows: repeat(2, 1fr);
  grid-template-columns: repeat(12, 1fr);
  gap: 16px;
  min-height: 0;
  padding: 0 16px 16px;
}

.gp-r1 {
  grid-row: 1;
}

.gp-r2 {
  grid-row: 2;
}

.gp-c1-3 {
  grid-column: 1 / 3;
}

.gp-c1-4 {
  grid-column: 1 / 4;
}

.gp-c3-5 {
  grid-column: 3 / 5;
}

.gp-c4-10 {
  grid-column: 4 / 10;
}

.gp-c5-9 {
  grid-column: 5 / 9;
}

.gp-c9-11 {
  grid-column: 9 / 11;
}

.gp-c10-13 {
  grid-column: 10 / 13;
}

.gp-c11-13 {
  grid-column: 11 / 13;
}

/* ===== 共享面板 ===== */
:deep(.panel) {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 18px 16px;
  overflow: hidden;
  background: linear-gradient(180deg, rgb(0 30 80 / 55%) 0%, rgb(6 11 36 / 70%) 100%);
  border: 1px solid var(--border);
  border-radius: 14px;
}

:deep(.panel)::before {
  position: absolute;
  top: 0;
  right: 20px;
  left: 20px;
  z-index: 1;
  height: 1px;
  pointer-events: none;
  content: "";
  background: linear-gradient(90deg, transparent, rgb(0 212 255 / 30%), transparent);
}

:deep(.panel)::after {
  position: absolute;
  inset: -1px;
  z-index: 0;
  pointer-events: none;
  content: "";
  background:
    linear-gradient(to right, rgb(0 212 255 / 30%) 1px, transparent 1px) 0 0 / 12px 1px no-repeat,
    linear-gradient(to bottom, rgb(0 212 255 / 30%) 1px, transparent 1px) 0 0 / 1px 12px no-repeat,
    linear-gradient(to left, rgb(0 212 255 / 30%) 1px, transparent 1px) 100% 0 / 12px 1px no-repeat,
    linear-gradient(to bottom, rgb(0 212 255 / 30%) 1px, transparent 1px) 100% 0 / 1px 12px
      no-repeat,
    linear-gradient(to right, rgb(0 212 255 / 30%) 1px, transparent 1px) 0 100% / 12px 1px no-repeat,
    linear-gradient(to top, rgb(0 212 255 / 30%) 1px, transparent 1px) 0 100% / 1px 12px no-repeat,
    linear-gradient(to left, rgb(0 212 255 / 30%) 1px, transparent 1px) 100% 100% / 12px 1px
      no-repeat,
    linear-gradient(to top, rgb(0 212 255 / 30%) 1px, transparent 1px) 100% 100% / 1px 12px
      no-repeat;
  border-radius: 14px;
}

:deep(.map-panel) {
  padding: 0;
  overflow: hidden;
}

:deep(.map-panel)::after {
  background: none;
}

:deep(.map-panel > div) {
  height: 100% !important;
  padding: 12px;
}

:deep(#china-map) {
  border-radius: 12px;
}

:deep(.panel-hd) {
  display: flex;
  flex-shrink: 0;
  gap: 8px;
  align-items: center;
  padding-bottom: 12px;
  margin-bottom: 10px;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 1px;
  border-bottom: 1px solid rgb(0 212 255 / 8%);
}

:deep(.dot) {
  display: inline-block;
  flex-shrink: 0;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  box-shadow: 0 0 6px currentcolor;
}

:deep(.dot.accent) {
  color: var(--accent);
  background: var(--accent);
}

:deep(.dot.green) {
  color: #10b981;
  background: #10b981;
}

:deep(.dot.warn) {
  color: #f59e0b;
  background: #f59e0b;
}

:deep(.dot.purple) {
  color: #7c3aed;
  background: #7c3aed;
}

/* ===== 大卡片行 x6 ===== */
.card-row {
  position: relative;
  z-index: 2;
  display: flex;
  flex-shrink: 0;
  gap: 16px;
  height: 180px;
  padding: 0 16px 16px;
}

.card-row > * {
  flex: 1;
}

/* ===== 底部状态栏 ===== */
.bottom-bar {
  position: relative;
  z-index: 2;
  display: flex;
  flex-shrink: 0;
  gap: 24px;
  align-items: center;
  padding: 10px 24px;
  margin: 0 16px 16px;
  font-size: 11px;
  background: linear-gradient(90deg, rgb(0 20 60 / 50%) 0%, rgb(0 20 60 / 30%) 100%);
  border: 1px solid rgb(0 180 255 / 10%);
  border-radius: 8px;
  opacity: 0.7;
}

.bb-item {
  display: flex;
  flex-shrink: 0;
  gap: 6px;
  align-items: center;
}

.bb-dot {
  width: 6px;
  height: 6px;
  background: #10b981;
  border-radius: 50%;
  box-shadow: 0 0 6px #10b981;
}

.bb-ticker {
  flex: 1;
  overflow: hidden;
  mask-image: linear-gradient(90deg, transparent, #000 10%, #000 90%, transparent);
}

.ticker-track {
  display: flex;
  gap: 32px;
  white-space: nowrap;
  animation: tickerScroll 20s linear infinite;
}

.ticker-item {
  flex-shrink: 0;
}
@keyframes tickerScroll {
  0% {
    transform: translateX(0);
  }

  100% {
    transform: translateX(-100%);
  }
}

.bb-items-right {
  display: flex;
  flex-shrink: 0;
  gap: 14px;
  align-items: center;
}

.bb-meta {
  display: flex;
  gap: 4px;
  align-items: center;
  font-size: 10px;
  opacity: 0.6;
}

.bb-meta-dot {
  flex-shrink: 0;
  width: 5px;
  height: 5px;
  border-radius: 50%;
}

.sr-cyan {
  background: #00d4ff;
  box-shadow: 0 0 5px #00d4ff;
}

.sr-green {
  background: #10b981;
  box-shadow: 0 0 5px #10b981;
}

.sr-purple {
  background: #7c3aed;
  box-shadow: 0 0 5px #7c3aed;
}

.sr-warn {
  background: #f59e0b;
  box-shadow: 0 0 5px #f59e0b;
}
</style>
