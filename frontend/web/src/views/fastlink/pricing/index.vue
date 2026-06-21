<template>
  <div class="pt-24 px-20 max-md:pt-15! max-sm:px-5! max-md:px-8! bg-transparent border-none!">
    <div class="mb-10 text-center">
      <h1 class="mb-2 text-4xl font-medium max-sm:text-3xl">选择适合您的套餐</h1>
      <h2 class="mb-2.5 text-2xl font-normal text-g-600 max-sm:text-2xl">按需付费，灵活升级</h2>
    </div>

    <div class="mt-10 max-md:mt-0">
      <ElSkeleton v-if="loading" :rows="6" animated />

      <ElEmpty v-else-if="!packages.length" description="暂无可用套餐" />

      <ElRow v-else :gutter="20" justify="center">
        <ElCol v-for="plan in packages" :key="plan.id" :xs="24" :sm="12" :md="6" class="mb-5">
          <ElCard
            class="flex flex-col h-full rounded-xl pricing-card"
            :class="{ 'current-card': plan.is_current }"
          >
            <div class="mb-5">
              <h3 class="mb-2.5 text-xl font-medium flex items-center gap-2">
                {{ plan.name }}
                <ElTag v-if="plan.is_current" type="warning" size="small">当前套餐</ElTag>
              </h3>
              <p
                class="h-10 pb-5 mb-5 overflow-hidden text-sm text-g-600 text-ellipsis border-b border-g-300/80 line-clamp-2"
              >
                {{ getPlanSummary(plan) }}
              </p>
              <div class="mt-7.5 flex flex-wrap items-baseline gap-x-1">
                <span class="text-3xl font-medium">¥{{ formatPrice(plan.price) }}</span>
                <span class="ml-2 text-sm text-g-600">/{{ getPeriodLabel(plan.period) }}</span>
              </div>
            </div>

            <div class="grow mb-5">
              <div
                v-for="feat in getFeatures(plan)"
                :key="feat"
                class="flex items-center mb-2.5 text-sm"
              >
                <ElIcon class="mr-2.5 text-theme!"><Check /></ElIcon>
                <span>{{ feat }}</span>
              </div>
            </div>

            <div class="mt-auto text-center">
              <ElButton v-if="plan.is_current" class="w-full h-10" disabled> 当前套餐 </ElButton>
              <ElButton
                v-else
                type="primary"
                class="w-full h-10"
                :loading="buyingId === plan.id"
                @click="buyPackage(plan)"
              >
                {{ getActionLabel(plan) }}
              </ElButton>
            </div>
          </ElCard>
        </ElCol>
      </ElRow>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { Check } from "@element-plus/icons-vue";
import SelfServiceAPI, { type AvailablePackage } from "@/api/module_platform/self_service";

defineOptions({ name: "DashboardPricing" });

const router = useRouter();
const packages = ref<AvailablePackage[]>([]);
const loading = ref(true);
const buyingId = ref<number | null>(null);

function formatPrice(price: number): string {
  const yuan = price / 100;
  return price % 100 === 0 ? yuan.toFixed(0) : yuan.toFixed(2);
}

function getPeriodLabel(period: string): string {
  return period === "year" ? "年" : "月";
}

function getPlanSummary(plan: AvailablePackage): string {
  if (plan.description) return plan.description;
  return plan.trial_days > 0
    ? `免费试用 ${plan.trial_days} 天`
    : `专业功能，按${getPeriodLabel(plan.period)}订阅`;
}

function getFeatures(plan: AvailablePackage): string[] {
  const features = [];
  if (plan.max_users) {
    features.push(`最多 ${plan.max_users} 个用户`);
  }
  if (plan.max_roles) {
    features.push(`最多 ${plan.max_roles} 个角色`);
  }
  if (plan.max_depts) {
    features.push(`最多 ${plan.max_depts} 个部门`);
  }
  if (plan.max_storage_mb) {
    features.push(`最多 ${plan.max_storage_mb} MB 存储`);
  }
  features.push(plan.trial_days > 0 ? `${plan.trial_days} 天免费试用` : "完整功能");
  return features;
}

function getActionLabel(plan: AvailablePackage): string {
  const [action] = plan.available_actions;
  switch (action) {
    case "renew":
      return "立即续费";
    case "upgrade":
      return "升级套餐";
    case "downgrade":
      return "降级套餐";
    case "buy":
    default:
      return plan.trial_days > 0 ? "免费试用" : "立即购买";
  }
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

async function buyPackage(pkg: AvailablePackage) {
  buyingId.value = pkg.id;
  const [action] = pkg.available_actions;
  try {
    const res = await SelfServiceAPI.createOrder({
      package_id: pkg.id,
      order_type: (action || "buy") as "buy" | "renew" | "upgrade" | "downgrade",
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
.current-card {
  border: 2px solid #e6a23c;
}

.pricing-card {
  &:not(.current-card) {
    transition:
      transform 0.2s ease,
      box-shadow 0.2s ease;

    &:hover {
      box-shadow: 0 8px 25px rgb(0 0 0 / 10%);
      transform: translateY(-4px);
    }
  }
}
</style>
