<template>
  <div
    class="relative pt-12 px-20 max-md:pt-15! max-sm:px-5! max-md:px-8! bg-transparent border-none!"
  >
    <!-- Decorative background -->
    <div
      class="absolute top-0 left-1/2 -translate-x-1/2 pointer-events-none overflow-hidden w-[800px] h-[500px] -z-1"
    >
      <div
        class="absolute top-[-120px] left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full bg-gradient-to-b from-primary/8 to-transparent opacity-60"
      />
      <div
        class="absolute top-[-60px] left-1/2 -translate-x-1/2 w-[400px] h-[400px] rounded-full bg-gradient-to-b from-primary/5 to-transparent opacity-40"
      />
    </div>

    <!-- Header -->
    <div class="mb-10 text-center relative">
      <h1 class="mb-2 text-4xl font-medium max-sm:text-3xl">选择适合您的套餐</h1>
      <h2 class="mb-2.5 text-2xl font-normal text-g-600 max-sm:text-2xl">按需付费，灵活升级</h2>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="mt-10">
      <ElSkeleton :rows="6" animated />
    </div>

    <!-- Empty -->
    <ElEmpty v-else-if="!plans.length" description="暂无可用套餐">
      <ElButton type="primary" @click="loadPackages">重新加载</ElButton>
    </ElEmpty>

    <!-- Pricing Cards -->
    <TransitionGroup
      v-else
      name="card"
      tag="div"
      class="mt-10 max-md:mt-0 flex flex-wrap justify-center -mx-2.5"
    >
      <div
        v-for="(plan, idx) in plans"
        :key="plan.id"
        class="px-2.5 mb-5 w-full sm:w-1/2 lg:w-1/4"
        :style="{ '--card-delay': `${idx * 0.08}s` }"
      >
        <ElCard
          class="relative flex flex-col h-full pricing-card rounded-2xl!"
          :class="{
            'is-current': plan.isCurrent,
            'is-recommended': plan.isRecommended,
          }"
        >
          <!-- Recommended Ribbon -->
          <div v-if="plan.isRecommended" class="recommended-ribbon">推荐</div>

          <!-- Card Header -->
          <div class="mb-5">
            <h3 class="mb-2.5 text-xl font-medium flex items-center gap-2">
              <span>{{ plan.name }}</span>
              <ElTag v-if="plan.isCurrent" type="warning" size="small">当前套餐</ElTag>
            </h3>

            <p
              class="h-10 pb-5 mb-5 overflow-hidden text-sm text-g-600 text-ellipsis border-b border-g-300/80 line-clamp-2"
            >
              {{ plan.summary }}
            </p>

            <!-- Price -->
            <div
              class="mt-7.5 px-4 py-4 -mx-1 rounded-xl bg-gradient-to-r from-primary/6 to-transparent"
            >
              <div class="flex flex-wrap items-baseline gap-x-1">
                <span class="text-4xl font-bold tracking-tight">¥{{ plan.price }}</span>
                <span class="ml-1.5 text-sm text-g-500">/{{ plan.periodLabel }}</span>
                <span v-if="plan.monthlyPrice" class="ml-2 text-xs text-g-400 line-through">
                  ¥{{ plan.monthlyPrice }}/月
                </span>
              </div>
            </div>
          </div>

          <!-- Feature List -->
          <div class="grow mb-5">
            <div
              v-for="feat in plan.features"
              :key="feat.text"
              class="flex items-start mb-1.5 px-2 py-1.5 -mx-2 text-sm rounded-lg transition-colors duration-150 hover:bg-g-100/60"
              :class="feat.highlight ? 'font-semibold text-theme!' : ''"
            >
              <ElIcon
                class="mr-2.5 mt-0.5 shrink-0"
                :class="feat.highlight ? 'text-theme!' : 'text-g-400!'"
              >
                <Check />
              </ElIcon>
              <span>{{ feat.text }}</span>
            </div>
          </div>

          <!-- CTA -->
          <div class="mt-auto text-center">
            <ElButton v-if="plan.isCurrent" class="w-full h-10 rounded-lg!" disabled>
              当前套餐
            </ElButton>
            <ElButton
              v-else
              :type="plan.isRecommended ? 'primary' : 'default'"
              class="w-full h-10 rounded-lg!"
              :class="{ 'btn-primary-gradient': plan.isRecommended }"
              :loading="buyingId === plan.id"
              @click="buyPackage(plan)"
            >
              {{ plan.actionLabel }}
            </ElButton>
          </div>
        </ElCard>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { Check } from "@element-plus/icons-vue";
import SelfServiceAPI, { type AvailablePackage } from "@/api/module_platform/self_service";

defineOptions({ name: "DashboardPricing" });

const router = useRouter();
const packages = ref<AvailablePackage[]>([]);
const loading = ref(true);
const buyingId = ref<number | null>(null);

interface FeatureItem {
  text: string;
  highlight: boolean;
}

interface PlanDisplay {
  id: number;
  name: string;
  price: string;
  periodLabel: string;
  monthlyPrice: string | null;
  summary: string;
  features: FeatureItem[];
  isCurrent: boolean;
  isRecommended: boolean;
  actionLabel: string;
  availableActions: string[];
}

const plans = computed<PlanDisplay[]>(() => {
  const raw = packages.value;
  if (!raw.length) return [];

  // Determine recommended: highest-tier non-current paid plan
  const sorted = [...raw].sort((a, b) => b.price - a.price);
  const recommendedId = sorted.find((p) => !p.is_current && p.price > 0)?.id ?? null;

  return raw.map((p) => enrichPlan(p, p.id === recommendedId));
});

function enrichPlan(p: AvailablePackage, isRecommended: boolean): PlanDisplay {
  const [action = "buy"] = p.available_actions;
  const periodLabel = p.period === "year" ? "年" : "月";
  const priceYuan = p.price / 100;

  // Monthly equivalent for yearly plans
  let monthlyPrice: string | null = null;
  if (p.period === "year") {
    const monthly = priceYuan / 12;
    monthlyPrice = monthly % 1 === 0 ? monthly.toFixed(0) : monthly.toFixed(2);
  }

  // Summary
  const summary = p.description
    ? p.description
    : p.trial_days > 0
      ? `免费试用 ${p.trial_days} 天`
      : `专业功能，按${periodLabel}订阅`;

  // Features
  const features: FeatureItem[] = [];
  if (p.max_users) features.push({ text: `最多 ${p.max_users} 个用户`, highlight: false });
  if (p.max_roles) features.push({ text: `最多 ${p.max_roles} 个角色`, highlight: false });
  if (p.max_depts) features.push({ text: `最多 ${p.max_depts} 个部门`, highlight: false });
  if (p.max_storage_mb)
    features.push({ text: `最多 ${p.max_storage_mb} MB 存储`, highlight: false });

  // Highlight the "full features" or trial line
  const lastFeature = p.trial_days > 0 ? `${p.trial_days} 天免费试用` : "完整功能";
  features.push({ text: lastFeature, highlight: p.trial_days === 0 && !p.is_current });

  // Price format
  const priceStr = p.price % 100 === 0 ? priceYuan.toFixed(0) : priceYuan.toFixed(2);

  // Action label
  let actionLabel: string;
  switch (action) {
    case "renew":
      actionLabel = "立即续费";
      break;
    case "upgrade":
      actionLabel = "升级套餐";
      break;
    case "downgrade":
      actionLabel = "降级套餐";
      break;
    default:
      actionLabel = p.trial_days > 0 ? "免费试用" : "立即购买";
  }

  return {
    id: p.id,
    name: p.name,
    price: priceStr,
    periodLabel,
    monthlyPrice,
    summary,
    features,
    isCurrent: p.is_current,
    isRecommended,
    actionLabel,
    availableActions: p.available_actions,
  };
}

async function loadPackages() {
  loading.value = true;
  try {
    const res = await SelfServiceAPI.getAvailablePackages();
    const data = res.data?.data;
    packages.value = data?.packages || [];
  } catch {
    ElMessage.error("加载套餐信息失败");
  } finally {
    loading.value = false;
  }
}

async function buyPackage(plan: PlanDisplay) {
  buyingId.value = plan.id;
  const [action = "buy"] = plan.availableActions;
  try {
    const res = await SelfServiceAPI.createOrder({
      package_id: plan.id,
      order_type: action as "buy" | "renew" | "upgrade" | "downgrade",
    });
    const data = res.data?.data;
    if (data?.amount > 0) {
      router.push(`/payment/${data.order_id}`);
    } else {
      router.push("/self-service?tab=orders");
    }
  } catch (e: any) {
    ElMessage.error(e?.msg || "下单失败");
  } finally {
    buyingId.value = null;
  }
}

onMounted(() => {
  loadPackages();
});
</script>

<style scoped lang="scss">
.pricing-card {
  transition:
    transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1),
    box-shadow 0.3s ease;

  &:hover {
    box-shadow: 0 16px 40px rgb(0 0 0 / 10%);
    transform: translateY(-6px);
  }

  &.is-current {
    background: linear-gradient(180deg, #fffaf0 0%, #fff 60%);
    border: 2px solid #e6a23c;
  }

  &.is-recommended {
    border: 2px solid var(--el-color-primary, #409eff);
    box-shadow: 0 4px 24px rgb(64 158 255 / 15%);

    &:hover {
      box-shadow: 0 16px 44px rgb(64 158 255 / 20%);
    }
  }

  // Override ElCard default padding
  :deep(.el-card__body) {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 28px 24px;
  }
}

/* Recommended ribbon */
.recommended-ribbon {
  position: absolute;
  top: 16px;
  right: -38px;
  z-index: 10;
  width: 124px;
  padding: 5px 0;
  font-size: 12px;
  font-weight: 600;
  color: #fff;
  text-align: center;
  letter-spacing: 1px;
  background: linear-gradient(135deg, var(--el-color-primary, #409eff), #79bbff);
  box-shadow: 0 2px 8px rgb(64 158 255 / 30%);
  transform: rotate(45deg);
}

/* Primary gradient button */
.btn-primary-gradient {
  color: #fff !important;
  background: linear-gradient(135deg, var(--el-color-primary, #409eff), #79bbff) !important;
  border: none !important;
  transition:
    opacity 0.2s,
    transform 0.2s;

  &:hover {
    opacity: 0.92;
    transform: scale(1.02);
  }

  &:active {
    transform: scale(0.98);
  }
}

/* Card entrance animation */
.card-enter-active {
  transition:
    opacity 0.45s ease,
    transform 0.45s ease;
  transition-delay: var(--card-delay, 0s);
}

.card-enter-from {
  opacity: 0;
  transform: translateY(24px);
}
</style>
