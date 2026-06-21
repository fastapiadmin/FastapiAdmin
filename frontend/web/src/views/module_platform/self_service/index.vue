<template>
  <div class="fa-full-height">
    <ElTabs v-model="activeTab" @tab-change="onTabChange">
      <!-- ─── 工作台 ─── -->
      <ElTabPane label="工作台" name="workspace">
        <ElScrollbar
          v-if="workspace"
          class="workspace-scroll"
          :view-style="{ paddingRight: '4px' }"
        >
          <!-- 欢迎横幅 -->
          <FaBasicBanner
            class="workspace-banner"
            :title="`${workspace.tenant.name}（${workspace.tenant.code}）`"
            :subtitle="
              workspace.package
                ? `${workspace.package.name} · ${workspace.package.period === 'year' ? '年付' : '月付'} · 剩余 ${workspace.tenant.days_remaining} 天 · ${workspace.tenant.status_label}`
                : `暂无套餐 · 剩余 ${workspace.tenant.days_remaining} 天 · ${workspace.tenant.status_label}`
            "
            boxStyle="bg-theme/5!"
            titleColor="var(--fa-gray-900)"
            subtitleColor="var(--fa-gray-500)"
            :decoration="false"
          />

          <!-- 统计卡片行 -->
          <ElRow :gutter="16" class="workspace-section">
            <ElCol :xs="24" :sm="12" :md="6">
              <FaStatsCard
                icon="ri:user-line"
                iconStyle="bg-theme"
                boxStyle="bg-theme/10!"
                title="用户"
                :description="`上限 ${workspace.quota.max_users || '—'}`"
                :count="workspace.quota.current_users"
                textColor="var(--theme-color)"
                :showArrow="false"
              />
            </ElCol>
            <ElCol :xs="24" :sm="12" :md="6">
              <FaStatsCard
                icon="ri:shield-user-line"
                iconStyle="bg-success"
                boxStyle="bg-success/10!"
                title="角色"
                :description="`上限 ${workspace.quota.max_roles || '—'}`"
                :count="workspace.quota.current_roles"
                textColor="var(--el-color-success)"
                :showArrow="false"
              />
            </ElCol>
            <ElCol :xs="24" :sm="12" :md="6">
              <FaStatsCard
                icon="ri:organization-chart"
                iconStyle="bg-info"
                boxStyle="bg-info/10!"
                title="部门"
                :description="`上限 ${workspace.quota.max_depts || '—'}`"
                :count="workspace.quota.current_depts"
                textColor="var(--el-color-info)"
                :showArrow="false"
              />
            </ElCol>
            <ElCol :xs="24" :sm="12" :md="6">
              <FaStatsCard
                icon="ri:money-cny-box-line"
                iconStyle="bg-warning"
                boxStyle="bg-warning/10!"
                title="套餐价格"
                :description="
                  workspace.package
                    ? `${workspace.package.period === 'year' ? '年付' : '月付'}`
                    : '—'
                "
                :count="workspace.package ? +(workspace.package.price / 100).toFixed(0) : 0"
                separator=","
                textColor="var(--el-color-warning)"
                :showArrow="false"
              />
            </ElCol>
          </ElRow>

          <!-- 配额使用进度 -->
          <ElRow :gutter="16" class="workspace-section">
            <ElCol :xs="24" :sm="8" :md="8">
              <FaProgressCard
                :percentage="workspace.quota.usage_percent.users"
                title="用户用量"
                color="var(--theme-color)"
                icon="ri:user-line"
                iconStyle="bg-theme/12 text-theme"
              />
            </ElCol>
            <ElCol :xs="24" :sm="8" :md="8">
              <FaProgressCard
                :percentage="workspace.quota.usage_percent.roles"
                title="角色用量"
                color="#67c23a"
                icon="ri:shield-user-line"
                iconStyle="bg-success/12 text-success"
              />
            </ElCol>
            <ElCol :xs="24" :sm="8" :md="8">
              <FaProgressCard
                :percentage="workspace.quota.usage_percent.depts"
                title="部门用量"
                color="#409EFF"
                icon="ri:organization-chart"
                iconStyle="bg-info/12 text-info"
              />
            </ElCol>
          </ElRow>

          <!-- 近期订单时间轴 -->
          <ElRow :gutter="16" class="workspace-section">
            <ElCol :span="24">
              <FaTimelineListCard
                :list="recentOrderTimeline"
                title="近期订单"
                :subtitle="`共 ${recentOrderTimeline.length} 条记录`"
                :maxCount="5"
              />
            </ElCol>
          </ElRow>
        </ElScrollbar>
        <div v-else-if="workspaceLoading" class="workspace-loading">
          <ElSkeleton :rows="10" animated />
        </div>
      </ElTabPane>

      <!-- ─── 选购套餐 ─── -->
      <ElTabPane label="选购套餐" name="packages">
        <div v-if="!packagesLoading && packages.length" class="package-grid">
          <div
            v-for="pkg in packages"
            :key="pkg.id"
            class="package-card"
            :class="{ 'package-card--current': pkg.is_current }"
          >
            <div class="package-card__header">
              <h3>{{ pkg.name }}</h3>
              <ElTag v-if="pkg.is_current" type="warning" size="small">当前套餐</ElTag>
            </div>
            <div class="package-card__price">
              <span class="price-value">¥{{ (pkg.price / 100).toFixed(2) }}</span>
              <span class="price-period">/{{ pkg.period === "year" ? "年" : "月" }}</span>
            </div>
            <div class="package-card__specs">
              <div class="spec-item">
                <span class="spec-label">最大用户数</span>
                <span class="spec-value">{{ pkg.max_users || "无限" }}</span>
              </div>
              <div class="spec-item">
                <span class="spec-label">最大角色数</span>
                <span class="spec-value">{{ pkg.max_roles || "无限" }}</span>
              </div>
              <div class="spec-item">
                <span class="spec-label">最大部门数</span>
                <span class="spec-value">{{ pkg.max_depts || "无限" }}</span>
              </div>
              <div class="spec-item" v-if="pkg.trial_days > 0">
                <span class="spec-label">试用天数</span>
                <span class="spec-value">{{ pkg.trial_days }} 天</span>
              </div>
            </div>
            <div class="package-card__actions">
              <ElButton
                v-for="action in pkg.available_actions"
                :key="action"
                :type="action === 'upgrade' ? 'primary' : 'default'"
                @click="handleAction(action, pkg)"
              >
                {{ actionLabel(action) }}
              </ElButton>
            </div>
          </div>
        </div>
        <ElEmpty v-else-if="!packagesLoading" description="暂无可用套餐" />
        <ElSkeleton v-else :rows="6" animated />
      </ElTabPane>

      <!-- ─── 我的订单 ─── -->
      <ElTabPane label="我的订单" name="orders">
        <ElCard shadow="hover" class="fa-table-card">
          <FaTableHeader
            v-model:columns="orderColumnChecks"
            :loading="orderLoading"
            @refresh="getOrderData"
          />

          <FaTable
            ref="orderTableRef"
            :loading="orderLoading"
            :data="orderData"
            :columns="orderColumns"
            :pagination="orderPagination"
            @pagination:size-change="handleOrderSizeChange"
            @pagination:current-change="handleOrderCurrentChange"
          />
        </ElCard>
      </ElTabPane>
    </ElTabs>

    <!-- ─── 套餐操作确认弹窗 ─── -->
    <FaDialog v-model="actionDialogVisible" :title="actionDialogTitle" width="560px">
      <div v-if="preview">
        <FaDescriptions
          :column="2"
          border
          size="small"
          :data="preview"
          :items="previewDescriptionItems"
        >
          <template #target_package>
            <ElTag type="primary" size="small">{{ preview.target_package }}</ElTag>
          </template>
          <template #action>
            <ElTag :type="actionTypeTag(preview.action)" size="small">{{
              actionLabel(preview.action)
            }}</ElTag>
          </template>
          <template #amount>
            <span class="price">¥{{ (preview.amount / 100).toFixed(2) }}</span>
            / {{ preview.period === "year" ? "年" : "月" }}
          </template>
        </FaDescriptions>

        <div v-if="preview.gained_menus?.length" class="menu-change">
          <h4 class="menu-change__title gain">新增菜单</h4>
          <ElTag
            v-for="m in preview.gained_menus"
            :key="m.id"
            type="success"
            size="small"
            style="margin: 2px"
          >
            {{ m.name }}
          </ElTag>
        </div>
        <div v-if="preview.lost_menus?.length" class="menu-change">
          <h4 class="menu-change__title loss">失去菜单</h4>
          <ElTag
            v-for="m in preview.lost_menus"
            :key="m.id"
            type="danger"
            size="small"
            style="margin: 2px"
          >
            {{ m.name }}
          </ElTag>
        </div>
        <div v-if="preview.affected_roles?.length" style="margin-top: 12px">
          <span class="text-warning">影响角色：</span>
          <span
            v-for="r in preview.affected_roles"
            :key="r"
            style="margin-left: 4px; color: #e6a23c"
            >{{ r }}</span
          >
        </div>
        <div v-if="preview.affected_users > 0" style="margin-top: 8px">
          <span class="text-warning">影响用户数：{{ preview.affected_users }} 人</span>
        </div>
      </div>

      <template #footer>
        <ElButton @click="actionDialogVisible = false">取消</ElButton>
        <ElButton type="primary" :loading="actionSubmitting" @click="confirmAction"
          >确认下单</ElButton
        >
      </template>
    </FaDialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import type { TabPaneName } from "element-plus";
import { useRouter } from "vue-router";
import { useTable } from "@/hooks/core/useTable";
import FaStatsCard from "@/components/cards/fa-stats-card/index.vue";
import FaProgressCard from "@/components/cards/fa-progress-card/index.vue";
import FaTimelineListCard from "@/components/cards/fa-timeline-list-card/index.vue";
import FaBasicBanner from "@/components/banners/fa-basic-banner/index.vue";
import SelfServiceAPI from "@/api/module_platform/self_service";
import type {
  AvailablePackage,
  PackageChangePreview,
  SelfServiceOrderItem,
  WorkspaceData,
} from "@/api/module_platform/self_service";
import { resolveStatusColumns } from "@utils";
import type { DescriptionsItem } from "@/components/others/fa-descriptions/index.vue";

defineOptions({ name: "SelfService" });

const router = useRouter();
const activeTab = ref("workspace");

// ─── 工作台 ───
const workspace = ref<WorkspaceData | null>(null);
const workspaceLoading = ref(false);

const recentOrderTimeline = computed(() => {
  if (!workspace.value?.recent_orders?.length) return [];
  return workspace.value.recent_orders.map((o) => {
    const statusMap: Record<number, { label: string; color: string }> = {
      0: { label: "待支付", color: "rgb(230, 162, 60)" },
      1: { label: "已支付", color: "rgb(103, 194, 58)" },
      2: { label: "已取消", color: "rgb(144, 147, 153)" },
      3: { label: "已退款", color: "rgb(245, 108, 108)" },
    };
    const s = statusMap[o.status] || { label: "未知", color: "rgb(144, 147, 153)" };
    return {
      time: o.created_at || "—",
      status: s.color,
      content: `${o.order_no} - ¥${((o.amount || 0) / 100).toFixed(2)}`,
      code: s.label,
    };
  });
});

async function loadWorkspace() {
  workspaceLoading.value = true;
  try {
    const { data: res } = await SelfServiceAPI.getWorkspace();
    workspace.value = (res?.data as WorkspaceData) || null;
  } catch {
    // ignore
  } finally {
    workspaceLoading.value = false;
  }
}

// ─── 套餐 ───
const packages = ref<AvailablePackage[]>([]);
const packagesLoading = ref(false);

// ─── 订单表格 ───
const {
  columns: orderColumns,
  columnChecks: orderColumnChecks,
  data: orderData,
  loading: orderLoading,
  pagination: orderPagination,
  getData: getOrderData,
  handleSizeChange: handleOrderSizeChange,
  handleCurrentChange: handleOrderCurrentChange,
} = useTable({
  core: {
    apiFn: SelfServiceAPI.listMyOrders,
    apiParams: {
      page_no: 1,
      page_size: 20,
    },
    columnsFactory: resolveStatusColumns<SelfServiceOrderItem>(() => [
      { prop: "order_no", label: "订单号", minWidth: 200, showOverflowTooltip: true },
      { prop: "package_name", label: "套餐", width: 120 },
      {
        prop: "order_type",
        label: "类型",
        width: 100,
        status: {
          new: { type: "info", text: "新购" },
          renew: { type: "info", text: "续费" },
          upgrade: { type: "info", text: "升级" },
          downgrade: { type: "info", text: "降级" },
        },
      },
      {
        prop: "amount",
        label: "金额",
        width: 120,
        formatter: (row: SelfServiceOrderItem) => `¥${(row.amount / 100).toFixed(2)}`,
      },
      {
        prop: "status",
        label: "状态",
        width: 100,
        status: {
          0: { type: "warning", text: "待支付" },
          1: { type: "success", text: "已支付" },
          2: { type: "info", text: "已取消" },
          3: { type: "danger", text: "已退款" },
        },
      },
      {
        prop: "pay_method",
        label: "支付方式",
        width: 100,
        formatter: (row: SelfServiceOrderItem) => row.pay_method || "—",
      },
      { prop: "pay_time", label: "支付时间", width: 160, showOverflowTooltip: true },
      { prop: "created_at", label: "创建时间", width: 160, showOverflowTooltip: true },
    ]),
  },
});

// ─── 操作弹窗 ───
const actionDialogVisible = ref(false);
const actionSubmitting = ref(false);
const actionLoading = ref(false);
const preview = ref<PackageChangePreview | null>(null);
const currentAction = ref("");
const currentPackage = ref<AvailablePackage | null>(null);
const actionDialogTitle = ref("确认操作");

const previewDescriptionItems: DescriptionsItem[] = [
  { label: "当前套餐", prop: "current_package" },
  { label: "目标套餐", prop: "target_package", slot: "target_package" },
  { label: "操作类型", prop: "action", slot: "action" },
  { label: "应付金额", prop: "amount", slot: "amount" },
];

// ─── 标签函数 ───
function actionLabel(action: string): string {
  const map: Record<string, string> = {
    buy: "购买",
    renew: "续费",
    upgrade: "升级",
    downgrade: "降级",
  };
  return map[action] || action;
}

function actionTypeTag(
  action: string
): "primary" | "success" | "info" | "warning" | "danger" | undefined {
  const map: Record<string, "primary" | "success" | "info" | "warning" | "danger" | undefined> = {
    buy: "success",
    renew: undefined,
    upgrade: "primary",
    downgrade: "warning",
  };
  return map[action];
}

// ─── 加载 ───
async function loadPackages() {
  packagesLoading.value = true;
  try {
    const { data: res } = await SelfServiceAPI.getAvailablePackages();
    const payload = res?.data as unknown as { packages?: AvailablePackage[] } | undefined;
    packages.value = payload?.packages || [];
  } catch {
    // ignore
  } finally {
    packagesLoading.value = false;
  }
}

function onTabChange(tab: TabPaneName) {
  if (tab === "workspace") loadWorkspace();
  else if (tab === "packages") loadPackages();
  else if (tab === "orders") getOrderData();
}

// ─── 动作处理 ───
async function handleAction(action: string, pkg: AvailablePackage) {
  currentAction.value = action;
  currentPackage.value = pkg;
  actionDialogTitle.value = `${actionLabel(action)} - ${pkg.name}`;
  actionLoading.value = true;
  preview.value = null;
  actionDialogVisible.value = true;

  try {
    const { data: res } = await SelfServiceAPI.previewPackageChange(pkg.id);
    preview.value = (res?.data as PackageChangePreview) || null;
  } catch {
    actionDialogVisible.value = false;
  } finally {
    actionLoading.value = false;
  }
}

async function confirmAction() {
  if (!currentPackage.value) return;
  actionSubmitting.value = true;
  try {
    const { data: res } = await SelfServiceAPI.createOrder({
      package_id: currentPackage.value.id,
      order_type: currentAction.value as "buy" | "renew" | "upgrade" | "downgrade",
    });
    const orderData = res?.data as { order_id: number; amount?: number } | undefined;
    actionDialogVisible.value = false;
    if (orderData?.order_id && (orderData?.amount || 0) > 0) {
      router.push(`/payment/${orderData.order_id}`);
    } else {
      activeTab.value = "orders";
      getOrderData();
    }
  } catch {
    // ignore
  } finally {
    actionSubmitting.value = false;
  }
}

onMounted(() => {
  loadWorkspace();
});
</script>

<style scoped lang="scss">
.fa-full-height {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;

  :deep(.el-tabs) {
    display: flex;
    flex: 1;
    flex-direction: column;
    min-height: 0;

    .el-tabs__content {
      flex: 1;
      min-height: 0;
      overflow: visible;
    }

    .el-tab-pane {
      display: flex;
      flex-direction: column;
      height: 100%;
    }
  }
}

/* ─── 工作台 ─── */
.workspace-scroll {
  flex: 1;
  min-height: 0;
}

.workspace-banner {
  margin-bottom: 16px;
}

.workspace-section {
  margin-bottom: 16px;
}

.workspace-loading {
  padding: 20px 0;
}

/* ─── 套餐卡片 ─── */
.package-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.package-card {
  padding: 24px;
  background: var(--default-box-color);
  border: 1px solid var(--fa-card-border);
  border-radius: calc(var(--custom-radius) + 4px);
  transition: box-shadow 0.3s;

  &:hover {
    box-shadow: 0 4px 16px rgb(0 0 0 / 8%);
  }

  &--current {
    background: #fdf6ec;
    border-color: #e6a23c;
  }

  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;

    h3 {
      margin: 0;
      font-size: 18px;
      font-weight: 600;
    }
  }

  &__price {
    padding-bottom: 16px;
    margin-bottom: 20px;
    border-bottom: 1px solid #ebeef5;

    .price-value {
      font-size: 28px;
      font-weight: 700;
      color: #303133;
    }

    .price-period {
      font-size: 14px;
      color: #909399;
    }
  }

  &__specs {
    margin-bottom: 20px;
  }

  &__actions {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }
}

.spec-item {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  font-size: 14px;

  .spec-label {
    color: #909399;
  }

  .spec-value {
    font-weight: 500;
    color: #303133;
  }
}

/* ─── 弹窗 ─── */
.menu-change {
  margin-top: 12px;

  &__title {
    margin: 0 0 8px;
    font-size: 14px;

    &.gain {
      color: #67c23a;
    }

    &.loss {
      color: #f56c6c;
    }
  }
}

.price {
  font-size: 16px;
  font-weight: 700;
  color: #f56c6c;
}

.text-warning {
  font-size: 13px;
  color: #e6a23c;
}
</style>
