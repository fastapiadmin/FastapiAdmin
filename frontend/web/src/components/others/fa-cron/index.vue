<template>
  <div class="cron-selector">
    <ElTabs v-model="activeTab" type="border-card">
      <ElTabPane name="秒" label="秒">
        <ElRadioGroup v-model="fields.second.mode">
          <ElRadio value="every">每秒 允许的通配符[,-*/]</ElRadio>
          <ElRadio value="range">
            <div class="flex items-center">
              <span class="mr-2">周期从</span>
              <ElInput v-model="fields.second.rangeStart" class="w-15! mr-2" />
              <span class="mr-2">到</span>
              <ElInput v-model="fields.second.rangeEnd" class="w-15! mr-2" />
              <span>秒</span>
            </div>
          </ElRadio>
          <ElRadio value="step">
            <div class="flex items-center">
              <span class="mr-2">从</span>
              <ElInput v-model="fields.second.stepFrom" class="w-15! mr-2" />
              <span class="mr-2">秒开始，每</span>
              <ElInput v-model="fields.second.stepInterval" class="w-15! mr-2" />
              <span>秒执行一次</span>
            </div>
          </ElRadio>
          <ElRadio value="specify">
            <div class="flex items-center">
              <span class="mr-2">指定</span>
              <ElCheckboxGroup
                v-model="fields.second.specified"
                :disabled="fields.second.mode !== 'specify'"
              >
                <ElCheckbox v-for="v in secondOptions" :key="v" :label="v" :value="v" />
              </ElCheckboxGroup>
            </div>
          </ElRadio>
        </ElRadioGroup>
      </ElTabPane>

      <ElTabPane name="分钟" label="分钟">
        <ElRadioGroup v-model="fields.minute.mode">
          <ElRadio value="every">每分钟 允许的通配符[,-*/]</ElRadio>
          <ElRadio value="range">
            <div class="flex items-center">
              <span class="mr-2">周期从</span>
              <ElInput v-model="fields.minute.rangeStart" class="w-15! mr-2" />
              <span class="mr-2">到</span>
              <ElInput v-model="fields.minute.rangeEnd" class="w-15! mr-2" />
              <span>分钟</span>
            </div>
          </ElRadio>
          <ElRadio value="step">
            <div class="flex items-center">
              <span class="mr-2">从</span>
              <ElInput v-model="fields.minute.stepFrom" class="w-15! mr-2" />
              <span class="mr-2">分钟开始，每</span>
              <ElInput v-model="fields.minute.stepInterval" class="w-15! mr-2" />
              <span>分钟执行一次</span>
            </div>
          </ElRadio>
          <ElRadio value="specify">
            <div class="flex items-center">
              <span class="mr-2">指定</span>
              <ElCheckboxGroup
                v-model="fields.minute.specified"
                :disabled="fields.minute.mode !== 'specify'"
              >
                <ElCheckbox v-for="v in minuteOptions" :key="v" :label="v" :value="v" />
              </ElCheckboxGroup>
            </div>
          </ElRadio>
        </ElRadioGroup>
      </ElTabPane>

      <ElTabPane name="小时" label="小时">
        <ElRadioGroup v-model="fields.hour.mode">
          <ElRadio value="every">每小时 允许的通配符[,-*/]</ElRadio>
          <ElRadio value="range">
            <div class="flex items-center">
              <span class="mr-2">周期从</span>
              <ElInput v-model="fields.hour.rangeStart" class="w-15! mr-2" />
              <span class="mr-2">到</span>
              <ElInput v-model="fields.hour.rangeEnd" class="w-15! mr-2" />
              <span>小时</span>
            </div>
          </ElRadio>
          <ElRadio value="step">
            <div class="flex items-center">
              <span class="mr-2">从</span>
              <ElInput v-model="fields.hour.stepFrom" class="w-15! mr-2" />
              <span class="mr-2">小时开始，每</span>
              <ElInput v-model="fields.hour.stepInterval" class="w-15! mr-2" />
              <span>小时执行一次</span>
            </div>
          </ElRadio>
          <ElRadio value="specify">
            <div class="flex items-center">
              <span class="mr-2">指定</span>
              <ElCheckboxGroup
                v-model="fields.hour.specified"
                :disabled="fields.hour.mode !== 'specify'"
              >
                <ElCheckbox v-for="v in hourOptions" :key="v" :label="v" :value="v" />
              </ElCheckboxGroup>
            </div>
          </ElRadio>
        </ElRadioGroup>
      </ElTabPane>

      <ElTabPane name="日" label="日">
        <ElRadioGroup v-model="fields.day.mode">
          <ElRadio value="every">每日 允许的通配符[,-*/]</ElRadio>
          <ElRadio value="any">不指定</ElRadio>
          <ElRadio value="range">
            <div class="flex items-center">
              <span class="mr-2">周期从</span>
              <ElInput v-model="fields.day.rangeStart" class="w-15! mr-2" />
              <span class="mr-2">到</span>
              <ElInput v-model="fields.day.rangeEnd" class="w-15! mr-2" />
              <span>日</span>
            </div>
          </ElRadio>
          <ElRadio value="step">
            <div class="flex items-center">
              <span class="mr-2">从</span>
              <ElInput v-model="fields.day.stepFrom" class="w-15! mr-2" />
              <span class="mr-2">日开始，每</span>
              <ElInput v-model="fields.day.stepInterval" class="w-15! mr-2" />
              <span>日执行一次</span>
            </div>
          </ElRadio>
          <ElRadio value="lastWeekday">
            <div class="flex items-center">
              <span class="mr-2">每月</span>
              <ElInput v-model="fields.day.extra" class="w-15! mr-2" />
              <span>号最近的那个工作日</span>
            </div>
          </ElRadio>
          <ElRadio value="last">本月最后一天</ElRadio>
          <ElRadio value="specify">
            <div class="flex items-center">
              <span class="mr-2">指定</span>
              <ElCheckboxGroup
                v-model="fields.day.specified"
                :disabled="fields.day.mode !== 'specify'"
              >
                <ElCheckbox v-for="v in dayOptions" :key="v" :label="v" :value="v" />
              </ElCheckboxGroup>
            </div>
          </ElRadio>
        </ElRadioGroup>
      </ElTabPane>

      <ElTabPane name="月" label="月">
        <ElRadioGroup v-model="fields.month.mode">
          <ElRadio value="every">每月 允许的通配符[,-*/]</ElRadio>
          <ElRadio value="any">不指定</ElRadio>
          <ElRadio value="range">
            <div class="flex items-center">
              <span class="mr-2">周期从</span>
              <ElInput v-model="fields.month.rangeStart" class="w-15! mr-2" />
              <span class="mr-2">到</span>
              <ElInput v-model="fields.month.rangeEnd" class="w-15! mr-2" />
              <span>月</span>
            </div>
          </ElRadio>
          <ElRadio value="step">
            <div class="flex items-center">
              <span class="mr-2">从</span>
              <ElInput v-model="fields.month.stepFrom" class="w-15! mr-2" />
              <span class="mr-2">月开始，每</span>
              <ElInput v-model="fields.month.stepInterval" class="w-15! mr-2" />
              <span>月执行一次</span>
            </div>
          </ElRadio>
          <ElRadio value="specify">
            <div class="flex items-center">
              <span class="mr-2">指定</span>
              <ElCheckboxGroup
                v-model="fields.month.specified"
                :disabled="fields.month.mode !== 'specify'"
              >
                <ElCheckbox v-for="v in monthOptions" :key="v" :label="v" :value="v" />
              </ElCheckboxGroup>
            </div>
          </ElRadio>
        </ElRadioGroup>
      </ElTabPane>

      <ElTabPane name="周" label="周">
        <ElRadioGroup v-model="fields.week.mode">
          <ElRadio value="every">每周 允许的通配符[,-*/]</ElRadio>
          <ElRadio value="any">不指定</ElRadio>
          <ElRadio value="range">
            <div class="flex items-center">
              <span class="mr-2">周期从星期</span>
              <ElInput v-model="fields.week.rangeStart" class="w-15! mr-2" />
              <span class="mr-2">到星期</span>
              <ElInput v-model="fields.week.rangeEnd" class="w-15! mr-2" />
            </div>
          </ElRadio>
          <ElRadio value="nthWeek">
            <div class="flex items-center">
              <span class="mr-2">第</span>
              <ElInput v-model="fields.week.rangeStart" class="w-15! mr-2" />
              <span class="mr-2">周的星期</span>
              <ElInput v-model="fields.week.rangeEnd" class="w-15! mr-2" />
            </div>
          </ElRadio>
          <ElRadio value="lastWeek">
            <div class="flex items-center">
              <span class="mr-2">本月最后一个星期</span>
              <ElInput v-model="fields.week.extra" class="w-15! mr-2" />
            </div>
          </ElRadio>
          <ElRadio value="specify">
            <div class="flex items-center">
              <span class="mr-2">指定</span>
              <ElCheckboxGroup
                v-model="fields.week.specified"
                :disabled="fields.week.mode !== 'specify'"
              >
                <ElCheckbox v-for="v in weekOptions" :key="v" :label="v" :value="v" />
              </ElCheckboxGroup>
            </div>
          </ElRadio>
        </ElRadioGroup>
      </ElTabPane>
    </ElTabs>

    <div class="cron-preview">
      <div class="flex items-center gap-2">
        <span class="text-xs text-(--el-text-color-secondary)">Cron 表达式：</span>
        <code class="text-sm font-mono">{{ cron }}</code>
      </div>
      <div class="flex items-center gap-2">
        <span class="text-xs text-(--el-text-color-secondary)">说明：</span>
        <span class="text-sm text-(--el-color-primary)">{{ cronDesc }}</span>
      </div>
      <div class="flex items-center gap-2">
        <span class="text-xs text-(--el-text-color-secondary)">下次执行：</span>
        <span class="text-sm">{{ nextRun || "—" }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, ref, watch } from "vue";
import cronParser from "cron-parser";
import dayjs from "dayjs";

interface FieldState {
  mode: string;
  rangeStart: string;
  rangeEnd: string;
  stepFrom: string;
  stepInterval: string;
  specified: string[];
  extra: string;
}

interface Fields {
  second: FieldState;
  minute: FieldState;
  hour: FieldState;
  day: FieldState;
  month: FieldState;
  week: FieldState;
}

const defaultField = (init: Partial<FieldState> = {}): FieldState => ({
  mode: "every",
  rangeStart: "0",
  rangeEnd: "0",
  stepFrom: "0",
  stepInterval: "1",
  specified: [],
  extra: "",
  ...init,
});

const fields = ref<Fields>({
  second: defaultField({ rangeStart: "0", rangeEnd: "59", stepFrom: "0" }),
  minute: defaultField({ rangeStart: "0", rangeEnd: "59", stepFrom: "0" }),
  hour: defaultField({ rangeStart: "0", rangeEnd: "23", stepFrom: "0" }),
  day: defaultField({ mode: "every", rangeStart: "1", rangeEnd: "31", stepFrom: "1" }),
  month: defaultField({ mode: "every", rangeStart: "1", rangeEnd: "12", stepFrom: "1" }),
  week: defaultField({ mode: "any", rangeStart: "1", rangeEnd: "7", stepFrom: "1" }),
});

const activeTab = ref("秒");

const props = defineProps<{ modelValue?: string }>();
const emit = defineEmits<{
  "update:modelValue": [value: string];
}>();

const pad = (n: number) => n.toString().padStart(2, "0");
const rangeOptions = (count: number, start = 0) =>
  Array.from({ length: count }, (_, i) => pad(start + i));
const secondOptions = rangeOptions(60);
const minuteOptions = rangeOptions(60);
const hourOptions = rangeOptions(24);
const dayOptions = rangeOptions(31, 1);
const monthOptions = rangeOptions(12, 1);
const weekOptions = rangeOptions(7, 1);

function toSegment(field: FieldState): string {
  switch (field.mode) {
    case "every":
      return "*";
    case "any":
      return "?";
    case "range":
      return `${field.rangeStart}-${field.rangeEnd}`;
    case "step":
      return `${field.stepFrom}/${field.stepInterval}`;
    case "specify":
      return (
        field.specified
          .map((v) => parseInt(v))
          .sort((a, b) => a - b)
          .join(",") || "*"
      );
    case "last":
      return "L";
    case "lastWeekday":
      return `${field.extra}W`;
    case "lastWeek":
      return `${field.extra}L`;
    case "nthWeek":
      return `${field.rangeStart}#${field.rangeEnd}`;
    default:
      return "*";
  }
}

const cron = computed(() => {
  const f = fields.value;
  return `${toSegment(f.second)} ${toSegment(f.minute)} ${toSegment(f.hour)} ${toSegment(f.day)} ${toSegment(f.month)} ${toSegment(f.week)}`;
});

const cronDesc = computed(() => {
  const { second, minute, hour, day, month, week } = fields.value;
  const W = ["", "周日", "周一", "周二", "周三", "周四", "周五", "周六"];

  // 层级: 年 -> 月 -> 日/周 -> 时 -> 分 -> 秒
  const parts: string[] = [];
  parts.push("每年");

  // 月
  if (month.mode === "specify" && month.specified.length)
    parts.push(`${month.specified.join("、")}月`);
  else parts.push("每月");

  // 日/周
  if (day.mode === "specify") parts.push(`${day.specified.join("、")}号`);
  else if (day.mode === "last") parts.push("最后一天");
  else if (day.mode === "lastWeekday") parts.push(`${day.extra}号最近工作日`);
  else if (week.mode === "specify") parts.push(week.specified.map((v) => W[+v] || v).join("、"));
  else if (week.mode === "range")
    parts.push(`${W[+week.rangeStart] || ""}至${W[+week.rangeEnd] || ""}`);
  else if (week.mode === "lastWeek") parts.push(`最后一个${W[+week.extra] || ""}`);
  else if (week.mode === "every") parts.push(day.mode === "any" ? "每周" : "每天");
  else parts.push("每天");

  // 时
  if (hour.mode === "every") parts.push("每时");
  else if (hour.mode === "step") parts.push(`每${hour.stepInterval}时`);
  else if (hour.mode === "specify" && hour.specified.length === 1)
    parts.push(`${hour.specified[0]}时`);

  // 分
  if (minute.mode === "every") parts.push("每分");
  else if (minute.mode === "step") parts.push(`每${minute.stepInterval}分`);
  else if (minute.mode === "specify" && minute.specified.length === 1)
    parts.push(`${minute.specified[0]}分`);

  // 秒
  if (second.mode === "every") parts.push("每秒");
  else if (second.mode === "step") parts.push(`每${second.stepInterval}秒`);
  else if (second.mode === "specify" && second.specified.length === 1)
    parts.push(`${second.specified[0]}秒`);

  return parts.join(" ");
});

let skipParse = false;
watch(cron, (val) => {
  skipParse = true;
  emit("update:modelValue", val);
  nextTick(() => {
    skipParse = false;
  });
});

// ---- 解析 cron 表达式 → 回填 fields ----
function parseSegment(seg: string, field: FieldState): void {
  if (seg === "*") {
    field.mode = "every";
  } else if (seg === "?") {
    field.mode = "any";
  } else if (seg === "L") {
    field.mode = "last";
  } else if (seg.includes("W")) {
    field.mode = "lastWeekday";
    field.extra = seg.replace("W", "");
  } else if (seg.includes("L")) {
    field.mode = "lastWeek";
    field.extra = seg.replace("L", "");
  } else if (seg.includes("#")) {
    field.mode = "nthWeek";
    const [a, b] = seg.split("#");
    field.rangeStart = a!;
    field.rangeEnd = b!;
  } else if (seg.includes("-")) {
    field.mode = "range";
    const [a, b] = seg.split("-");
    field.rangeStart = a!;
    field.rangeEnd = b!;
  } else if (seg.includes("/")) {
    field.mode = "step";
    const [a, b] = seg.split("/");
    field.stepFrom = a!;
    field.stepInterval = b!;
  } else if (seg.includes(",")) {
    field.mode = "specify";
    field.specified = seg.split(",").map((v) => pad(parseInt(v)));
  } else if (/^\d+$/.test(seg)) {
    field.mode = "specify";
    field.specified = [pad(parseInt(seg))];
  }
}

function applyCron(expr: string) {
  const parts = expr.trim().split(/\s+/);
  if (parts.length < 6) return;
  const keys: (keyof Fields)[] = ["second", "minute", "hour", "day", "month", "week"];
  keys.forEach((key, i) => {
    parseSegment(parts[i]!, fields.value[key]);
  });
  // 自动定位到第一个非默认的 tab
  const idx = parts.findIndex((p) => p !== "*" && p !== "?");
  const tabMap = ["秒", "分钟", "小时", "日", "月", "周"];
  activeTab.value = idx >= 0 ? tabMap[idx]! : "秒";
}

watch(
  () => props.modelValue,
  (val) => {
    if (skipParse) return;
    if (val) applyCron(val);
  },
  { immediate: true }
);

// ---- 下一次执行时间 ----
const nextRun = ref("");

function calcNextRun(expr: string) {
  if (!expr?.trim()) {
    nextRun.value = "";
    return;
  }
  try {
    const parser = (cronParser as any).default ?? cronParser;
    const interval = parser.parse(expr, {
      currentDate: new Date(),
    });
    nextRun.value = dayjs(interval.next().toDate()).format("YYYY-MM-DD HH:mm:ss");
  } catch {
    nextRun.value = "无效表达式";
  }
}

watch(cron, (val) => calcNextRun(val), { immediate: true });

const clear = () => {
  fields.value = {
    second: defaultField({ rangeStart: "0", rangeEnd: "59", stepFrom: "0" }),
    minute: defaultField({ rangeStart: "0", rangeEnd: "59", stepFrom: "0" }),
    hour: defaultField({ rangeStart: "0", rangeEnd: "23", stepFrom: "0" }),
    day: defaultField({ mode: "every", rangeStart: "1", rangeEnd: "31", stepFrom: "1" }),
    month: defaultField({ mode: "every", rangeStart: "1", rangeEnd: "12", stepFrom: "1" }),
    week: defaultField({ mode: "any", rangeStart: "1", rangeEnd: "7", stepFrom: "1" }),
  };
  activeTab.value = "秒";
};

defineExpose({ clear });
</script>

<style lang="scss" scoped>
.cron-selector {
  padding: 12px;

  :deep(.el-tabs__content) {
    padding: 8px;
  }

  :deep(.el-radio-group) {
    .el-radio {
      width: 100%;
      height: auto;
      min-height: 28px;
      margin-bottom: 6px;
    }
  }

  :deep(.el-checkbox-group) {
    display: flex;
    flex-wrap: wrap;

    .el-checkbox {
      height: auto;
      margin-right: 6px;
      margin-bottom: 6px;
    }
  }
}

.cron-preview {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 10px;
  margin-top: 12px;
  background-color: var(--el-fill-color);
  border-radius: 4px;
}
</style>
