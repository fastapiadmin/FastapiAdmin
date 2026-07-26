<template>
  <div class="fa-card flex flex-col p-5 h-134 overflow-hidden">
    <div class="fa-card-header">
      <div class="title">
        <h4>新用户</h4>
        <p>
          这个月增长
          <span class="text-success">+20%</span>
        </p>
      </div>
      <ElRadioGroup v-model="radio2">
        <ElRadioButton value="本月" label="本月"></ElRadioButton>
        <ElRadioButton value="上月" label="上月"></ElRadioButton>
        <ElRadioButton value="今年" label="今年"></ElRadioButton>
      </ElRadioGroup>
    </div>
    <FaTable
      class="w-full"
      :data="tableData"
      size="large"
      :border="false"
      :stripe="false"
      :header-cell-style="{ background: 'transparent' }"
    >
      <template #default>
        <ElTableColumn type="index" label="序号" width="60" />
        <ElTableColumn label="头像" prop="avatar" width="140px">
          <template #default="scope">
            <div class="flex items-center">
              <img class="size-9 rounded-lg" :src="scope.row.avatar" alt="avatar" loading="eager" />
              <div class="flex flex-col ml-3">
                <div class="font-medium">{{ scope.row.username }}</div>
                <div class="text-xs text-slate-500">{{ scope.row.province }}</div>
              </div>
            </div>
          </template>
        </ElTableColumn>
        <ElTableColumn label="价格" prop="price">
          <template #default="scope">
            <span class="font-semibold">¥{{ scope.row.price.toLocaleString() }}</span>
          </template>
        </ElTableColumn>

        <ElTableColumn label="库存" prop="stock" width="90px">
          <template #default="scope">
            <div
              class="inline-block px-2 py-1 text-xs font-medium rounded"
              :class="getStockClass(scope.row.stock)"
            >
              {{ getStockStatus(scope.row.stock) }}
            </div>
          </template>
        </ElTableColumn>
        <ElTableColumn label="进度" width="180">
          <template #default="scope">
            <ElProgress
              :percentage="scope.row.pro"
              :color="scope.row.color"
              :stroke-width="4"
              :aria-label="`${scope.row.username}的完成进度: ${scope.row.pro}%`"
            />
          </template>
        </ElTableColumn>
      </template>
    </FaTable>
  </div>
</template>

<script setup lang="ts">
import avatar1 from "@imgs/avatar/avatar1.webp";
import avatar2 from "@imgs/avatar/avatar2.webp";
import avatar3 from "@imgs/avatar/avatar3.webp";
import avatar4 from "@imgs/avatar/avatar4.webp";
import avatar5 from "@imgs/avatar/avatar5.webp";
import avatar6 from "@imgs/avatar/avatar6.webp";
import FaTable from "@/components/tables/fa-table/index.vue";

interface UserTableItem {
  username: string;
  province: string;
  sex: 0 | 1;
  price: number;
  stock: number;
  sales: number;
  age: number;
  percentage: number;
  pro: number;
  color: string;
  avatar: string;
}

const ANIMATION_DELAY = 100;

const radio2 = ref("本月");

/**
 * 新用户表格数据
 * 包含用户基本信息和完成进度
 */
const tableData = reactive<UserTableItem[]>([
  {
    username: "中小鱼",
    province: "北京",
    sex: 0,
    price: 1299,
    stock: 89,
    sales: 652,
    age: 22,
    percentage: 60,
    pro: 0,
    color: "var(--fa-primary)",
    avatar: avatar1,
  },
  {
    username: "何小荷",
    province: "深圳",
    sex: 1,
    price: 299,
    stock: 12,
    sales: 238,
    age: 21,
    percentage: 20,
    pro: 0,
    color: "var(--fa-secondary)",
    avatar: avatar2,
  },
  {
    username: "誶誶淰",
    province: "上海",
    sex: 1,
    price: 99,
    stock: 0,
    sales: 126,
    age: 23,
    percentage: 60,
    pro: 0,
    color: "var(--fa-warning)",
    avatar: avatar3,
  },
  {
    username: "发呆草",
    province: "长沙",
    sex: 0,
    price: 399,
    stock: 45,
    sales: 321,
    age: 28,
    percentage: 50,
    pro: 0,
    color: "var(--fa-info)",
    avatar: avatar4,
  },
  {
    username: "甜筒",
    province: "浙江",
    sex: 1,
    price: 1599,
    stock: 78,
    sales: 489,
    age: 26,
    percentage: 70,
    pro: 0,
    color: "var(--fa-error)",
    avatar: avatar5,
  },
  {
    username: "冷月呆呆",
    province: "湖北",
    sex: 1,
    price: 1059,
    stock: 0,
    sales: 0,
    age: 25,
    percentage: 90,
    pro: 0,
    color: "var(--fa-success)",
    avatar: avatar6,
  },
  {
    username: "冷呆呆",
    province: "湖北",
    sex: 1,
    price: 1059,
    stock: 0,
    sales: 0,
    age: 25,
    percentage: 90,
    pro: 0,
    color: "var(--fa-success)",
    avatar: avatar6,
  },
  {
    username: "冷月呆呆",
    province: "湖北",
    sex: 1,
    price: 1059,
    stock: 0,
    sales: 0,
    age: 25,
    percentage: 90,
    pro: 0,
    color: "var(--fa-success)",
    avatar: avatar6,
  },
]);

const STOCK_THRESHOLD = {
  LOW: 20,
  MEDIUM: 50,
} as const;

/**
 * 根据库存数量获取状态文本
 */
const getStockStatus = (stock: number): string => {
  if (stock === 0) return "缺货";
  if (stock < STOCK_THRESHOLD.LOW) return "低库存";
  if (stock < STOCK_THRESHOLD.MEDIUM) return "适中";
  return "充足";
};

/**
 * 根据库存数量获取状态样式类名
 * @param stock 库存数量
 * @returns CSS 类名
 */
const getStockClass = (stock: number): string => {
  if (stock === 0) return "text-danger bg-danger/12";
  if (stock < STOCK_THRESHOLD.LOW) return "text-warning bg-warning/12";
  if (stock < STOCK_THRESHOLD.MEDIUM) return "text-info bg-info/12";
  return "text-success bg-success/12";
};

/**
 * 添加进度条动画效果
 * 延迟后将进度值从 0 更新到目标百分比，触发动画
 */
const addAnimation = (): void => {
  setTimeout(() => {
    tableData.forEach((item) => {
      item.pro = item.percentage;
    });
  }, ANIMATION_DELAY);
};

onMounted(() => {
  addAnimation();
});
</script>

<style lang="scss" scoped>
.fa-card {
  :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
    color: var(--el-color-primary) !important;
    background: transparent !important;
  }
}
</style>
