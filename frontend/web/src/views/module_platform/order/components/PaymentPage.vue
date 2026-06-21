<template>
  <div class="payment-page">
    <div v-if="loading" class="payment-loading">
      <ElSkeleton :rows="6" animated />
    </div>

    <div v-else-if="paid" class="payment-success">
      <div class="success-icon">✅</div>
      <h2>支付成功</h2>
      <p>订单 {{ orderNo }} 已完成支付</p>
      <p class="amount">¥{{ (amount / 100).toFixed(2) }}</p>
      <ElButton type="primary" @click="goOrders">查看订单</ElButton>
    </div>

    <div v-else-if="error" class="payment-error">
      <h2>订单异常</h2>
      <p>{{ error }}</p>
      <ElButton @click="goOrders">返回</ElButton>
    </div>

    <div v-else class="payment-content">
      <div class="order-info">
        <h2>订单支付</h2>
        <div class="info-row">
          <span class="label">订单号</span>
          <span class="value">{{ orderNo }}</span>
        </div>
        <div class="info-row">
          <span class="label">金额</span>
          <span class="value price">¥{{ (amount / 100).toFixed(2) }}</span>
        </div>
      </div>

      <div class="pay-methods">
        <h3>选择支付方式</h3>
        <div class="method-list">
          <div
            class="method-item"
            :class="{ active: selectedMethod === 'alipay' }"
            @click="selectedMethod = 'alipay'"
          >
            <span class="method-icon">💳</span>
            <span>支付宝</span>
          </div>
          <div
            class="method-item"
            :class="{ active: selectedMethod === 'wxpay' }"
            @click="selectedMethod = 'wxpay'"
          >
            <span class="method-icon">💚</span>
            <span>微信支付</span>
          </div>
        </div>
      </div>

      <div v-if="qrCodeUrl || payUrl" class="pay-result">
        <div v-if="qrCodeUrl" class="qr-section">
          <p class="hint">请使用{{ methodLabel }}扫码支付</p>
          <img :src="qrCodeUrl" class="qr-code" alt="支付二维码" />
        </div>
        <div v-else-if="payUrl" class="redirect-section">
          <p class="hint">即将跳转{{ methodLabel }}支付...</p>
          <ElButton type="primary" @click="openPayUrl">立即支付</ElButton>
        </div>
        <div class="poll-status">
          <ElTag :type="polling ? 'warning' : 'info'">
            {{ polling ? "等待支付中..." : "未发起支付" }}
          </ElTag>
        </div>
      </div>

      <div class="actions" v-if="!paying">
        <ElButton type="primary" size="large" @click="startPay" :loading="paying">
          立即支付
        </ElButton>
        <ElButton size="large" @click="goOrders">稍后支付</ElButton>
      </div>

      <div class="actions" v-if="payUrl && !paying">
        <ElButton type="success" size="large" @click="mockPaySuccess"> 模拟支付成功 </ElButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import OrderAPI from "@/api/module_platform/order";

defineOptions({ name: "PaymentPage" });

const route = useRoute();
const router = useRouter();

const orderId = computed(() => {
  const n = Number(route.params.orderId);
  return Number.isNaN(n) ? 0 : n;
});

// 订单号无效时直接重定向
if (orderId.value === 0) {
  router.replace("/module_platform/order");
}
const loading = ref(true);
const paid = ref(false);
const paying = ref(false);
const polling = ref(false);
const error = ref("");
const orderNo = ref("");
const amount = ref(0);
const qrCodeUrl = ref("");
const payUrl = ref("");
const selectedMethod = ref("alipay");
let pollTimer: ReturnType<typeof setInterval> | null = null;

const methodLabel = computed(() => (selectedMethod.value === "alipay" ? "支付宝" : "微信"));

async function loadOrderStatus() {
  try {
    const res = await OrderAPI.queryPaymentStatus(orderId.value);
    const data = res.data?.data;
    if (data?.paid) {
      paid.value = true;
      orderNo.value = data.order_no || "";
      amount.value = data.amount || 0;
      stopPolling();
    }
  } catch {
    // ignore
  }
}

async function startPay() {
  paying.value = true;
  try {
    const res = await OrderAPI.payOrder(orderId.value, { pay_method: selectedMethod.value });
    const data = res.data?.data;
    orderNo.value = data.order_no;
    amount.value = data.amount;
    qrCodeUrl.value = data.qr_code_url || "";
    payUrl.value = data.pay_url || "";
    startPolling();
  } catch (e: any) {
    ElMessage.error(e?.msg || "创建支付失败");
  } finally {
    paying.value = false;
  }
}

function openPayUrl() {
  if (payUrl.value) {
    window.open(payUrl.value, "_blank");
  }
}

async function mockPaySuccess() {
  try {
    await OrderAPI.mockPaymentCallback(orderId.value);
    ElMessage.success("支付成功（模拟）");
    paid.value = true;
    stopPolling();
  } catch (e: any) {
    ElMessage.error(e?.msg || "模拟支付失败");
  }
}

function startPolling() {
  polling.value = true;
  pollTimer = setInterval(async () => {
    try {
      const res = await OrderAPI.queryPaymentStatus(orderId.value);
      const data = res.data?.data;
      if (data?.paid) {
        paid.value = true;
        orderNo.value = data.order_no || orderNo.value;
        amount.value = data.amount || amount.value;
        stopPolling();
        ElMessage.success("支付成功");
      }
    } catch {
      // ignore
    }
  }, 2000);
}

function stopPolling() {
  polling.value = false;
  if (pollTimer) {
    clearInterval(pollTimer);
    pollTimer = null;
  }
}

function goOrders() {
  router.push("/self-service?tab=orders");
}

onMounted(async () => {
  loading.value = true;
  await loadOrderStatus();
  loading.value = false;
});

onUnmounted(() => {
  stopPolling();
});
</script>

<style scoped lang="scss">
.payment-page {
  max-width: 520px;
  padding: 24px;
  margin: 40px auto;
}

.payment-loading {
  padding: 40px;
}

.payment-content {
  .order-info {
    padding: 20px;
    margin-bottom: 24px;
    background: #f5f7fa;
    border-radius: 8px;

    h2 {
      margin: 0 0 16px;
      font-size: 20px;
    }
  }

  .info-row {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    font-size: 14px;

    .label {
      color: #909399;
    }

    .value.price {
      font-size: 18px;
      font-weight: 700;
      color: #f56c6c;
    }
  }
}

.pay-methods {
  margin-bottom: 24px;

  h3 {
    margin: 0 0 12px;
    font-size: 15px;
  }
}

.method-list {
  display: flex;
  gap: 12px;
}

.method-item {
  display: flex;
  flex: 1;
  gap: 8px;
  align-items: center;
  padding: 14px 16px;
  cursor: pointer;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  transition: all 0.2s;

  &:hover {
    border-color: #409eff;
  }

  &.active {
    background: #ecf5ff;
    border-color: #409eff;
  }

  .method-icon {
    font-size: 20px;
  }
}

.pay-result {
  margin-bottom: 24px;
  text-align: center;

  .hint {
    margin-bottom: 16px;
    font-size: 14px;
    color: #909399;
  }

  .qr-code {
    width: 200px;
    height: 200px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
  }

  .poll-status {
    margin-top: 12px;
  }
}

.actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 24px;
}

.payment-success {
  padding: 60px 20px;
  text-align: center;

  .success-icon {
    margin-bottom: 16px;
    font-size: 48px;
  }

  h2 {
    margin: 0 0 8px;
    font-size: 22px;
    color: #67c23a;
  }

  p {
    margin-bottom: 4px;
    color: #606266;
  }

  .amount {
    margin: 16px 0 24px;
    font-size: 24px;
    font-weight: 700;
    color: #303133;
  }
}

.payment-error {
  padding: 60px 20px;
  text-align: center;

  h2 {
    color: #f56c6c;
  }
}
</style>
