<template>
  <el-form
    ref="formRef"
    :model="crontabValueObj"
    label-width="auto"
    label-suffix=":"
    :inline="true"
    class="interval-tab-form"
  >
    <el-form-item label="秒" prop="second" class="form-item">
      <el-select v-model="crontabValueObj.second" placeholder="秒" clearable>
        <el-option label="每秒" value="*">*</el-option>
        <el-option
          v-for="second in seconds"
          :key="second"
          :label="second"
          :value="second.toString()"
        >
          {{ second }}
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="分" prop="min" class="form-item">
      <el-select v-model="crontabValueObj.min" placeholder="分" clearable>
        <el-option label="每分" value="*">*</el-option>
        <el-option v-for="min in minutes" :key="min" :label="min" :value="min.toString()">
          {{ min }}
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="时" prop="hour" class="form-item">
      <el-select v-model="crontabValueObj.hour" placeholder="时" clearable>
        <el-option label="每时" value="*">*</el-option>
        <el-option v-for="hour in hours" :key="hour" :label="hour" :value="hour.toString()">
          {{ hour }}
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="天" prop="day" class="form-item">
      <el-select v-model="crontabValueObj.day" placeholder="天" clearable>
        <el-option label="每天" value="*">*</el-option>
        <el-option v-for="day in days" :key="day" :label="day" :value="day">{{ day }}</el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="周" prop="week" class="form-item">
      <el-select v-model="crontabValueObj.week" placeholder="周" clearable>
        <el-option label="每周" value="*">*</el-option>
        <el-option
          v-for="week in weekOptions"
          :key="week.value"
          :label="week.label"
          :value="week.value"
        >
          {{ week.label }}
        </el-option>
      </el-select>
    </el-form-item>

    <div class="form-actions">
      <el-button @click="emit('cancel')">取消</el-button>
      <el-button type="primary" @click="handleConfirm">确认</el-button>
    </div>
  </el-form>
</template>

<script lang="ts" setup>
// 定义接口，增强类型安全
interface CrontabValue {
  second: string;
  min: string;
  hour: string;
  day: string;
  week: string;
}

interface WeekOption {
  value: string;
  label: string;
}

// 定义props
const props = defineProps<{
  cronValue?: string;
}>();

// 定义emits
const emit = defineEmits<{
  (e: "confirm", value: string): void;
  (e: "cancel"): void;
}>();

const formRef = ref();

// 响应式数据
const crontabValueObj = ref<CrontabValue>({
  second: "*",
  min: "*",
  hour: "*",
  day: "*",
  week: "*",
});

// 常量定义，避免魔法数字
const MAX_SECONDS = 60;
const MAX_MINUTES = 60;
const MAX_HOURS = 24;
const MAX_DAYS = 31;

// 生成选择器选项
const seconds = ref(Array.from({ length: MAX_SECONDS }, (_, i) => i));
const minutes = ref(Array.from({ length: MAX_MINUTES }, (_, i) => i));
const hours = ref(Array.from({ length: MAX_HOURS }, (_, i) => i));
const days = ref(Array.from({ length: MAX_DAYS }, (_, i) => i + 1));
const weekOptions: WeekOption[] = [
  { value: "1", label: "周一" },
  { value: "2", label: "周二" },
  { value: "3", label: "周三" },
  { value: "4", label: "周四" },
  { value: "5", label: "周五" },
  { value: "6", label: "周六" },
  { value: "7", label: "周日" },
];

// 初始化时设置cron值
onMounted(() => {
  if (props.cronValue) {
    setCron(props.cronValue);
  }
});

// 处理确认
const handleConfirm = () => {
  // 简单验证
  const obj = crontabValueObj.value;
  if (!obj.second || !obj.min || !obj.hour || !obj.day || !obj.week) {
    ElMessage.warning("请完善所有时间选项");
    return;
  }

  const cronStr = `${obj.second} ${obj.min} ${obj.hour} ${obj.day} ${obj.week}`;
  emit("confirm", cronStr);
};

// 设置cron表达式的值
const setCron = (cronStr: string) => {
  if (!cronStr) return;
  const parts = cronStr.split(" ");
  if (parts.length !== 5) {
    ElMessage.warning("无效的cron表达式格式");
    return;
  }

  const [second, min, hour, day, week] = parts;
  crontabValueObj.value = {
    second: second || "*",
    min: min || "*",
    hour: hour || "*",
    day: day || "*",
    week: week || "*",
  };
};

// 暴露方法给父组件
defineExpose({ setCron });
</script>

<style lang="scss" scoped>
.interval-tab-form {
  flex-wrap: wrap;
  gap: 16px 8px;
  width: 100%;
}

.form-item {
  width: calc(20% - 8px);
  min-width: 120px;
}

.form-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  width: 100%;
  margin-top: 16px;
}

// 响应式调整
@media (max-width: 768px) {
  .form-item {
    width: calc(33.33% - 8px);
  }
}

@media (max-width: 480px) {
  .form-item {
    width: calc(50% - 8px);
  }
}
</style>
