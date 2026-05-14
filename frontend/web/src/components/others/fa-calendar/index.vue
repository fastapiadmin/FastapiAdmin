<template>
  <div class="home-calendar">
    <ElCalendar v-model="currentDate">
      <template #date-cell="{ data }">
        <div
          class="home-calendar__cell relative flex h-full min-h-14 max-h-20 flex-col overflow-hidden p-0.5 c-p"
          :class="{ 'is-selected': data.isSelected }"
          @click="handleCellClick(data.day)"
        >
          <p class="absolute right-0.5 top-0.5 text-[11px] leading-none opacity-80">
            {{ formatDate(data.day) }}
          </p>
          <div class="mt-4 flex max-h-12 w-full flex-col gap-px overflow-y-auto pr-0.5">
            <div
              v-for="event in getEvents(data.day)"
              :key="`${event.date}-${event.content}`"
              @click.stop="handleEventClick(event)"
            >
              <div
                class="min-w-0 overflow-hidden text-ellipsis whitespace-nowrap rounded px-1 py-px text-[10px] leading-snug font-medium hover:opacity-80"
                :class="[event.bgClass, event.textClass]"
              >
                {{ event.content }}
              </div>
            </div>
          </div>
        </div>
      </template>
    </ElCalendar>

    <ElDialog v-model="dialogVisible" :title="dialogTitle" width="600px" @closed="resetForm">
      <ElForm :model="eventForm" label-width="80px">
        <ElFormItem label="活动标题" required>
          <ElInput v-model="eventForm.content" placeholder="请输入活动标题" />
        </ElFormItem>
        <ElFormItem label="事件颜色">
          <ElRadioGroup v-model="eventForm.type">
            <ElRadio v-for="et in eventTypes" :key="et.value" :value="et.value">
              {{ et.label }}
            </ElRadio>
          </ElRadioGroup>
        </ElFormItem>
        <ElFormItem label="开始日期" required>
          <ElDatePicker
            v-model="eventForm.date"
            :style="'width: 100%'"
            type="date"
            placeholder="选择日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </ElFormItem>
        <ElFormItem label="结束日期">
          <ElDatePicker
            v-model="eventForm.endDate"
            :style="'width: 100%'"
            type="date"
            placeholder="选择结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            :min-date="eventForm.date"
          />
        </ElFormItem>
      </ElForm>
      <template #footer>
        <span class="dialog-footer">
          <ElButton v-if="isEditing" type="danger" @click="handleDeleteEvent">删除</ElButton>
          <ElButton type="primary" @click="handleSaveEvent">
            {{ isEditing ? "更新" : "添加" }}
          </ElButton>
        </span>
      </template>
    </ElDialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { dayjs } from "element-plus";

defineOptions({ name: "FaCalendar" });

interface CalendarEvent {
  date: string;
  endDate?: string;
  content: string;
  type?: "primary" | "success" | "warning" | "danger";
  bgClass?: string;
  textClass?: string;
}

const eventTypes = [
  { label: "基本", value: "primary" },
  { label: "成功", value: "success" },
  { label: "警告", value: "warning" },
  { label: "危险", value: "danger" },
] as const;

const d = (dayOfMonth: number) => dayjs().date(dayOfMonth).format("YYYY-MM-DD");

const currentDate = ref(new Date());
const dialogVisible = ref(false);
const dialogTitle = ref("添加事件");
const editingEventIndex = ref<number>(-1);

const events = ref<CalendarEvent[]>([
  { date: d(3), content: "产品需求评审", type: "primary" },
  { date: d(5), endDate: d(7), content: "项目周报会议（跨日期）", type: "primary" },
  { date: d(10), content: "瑜伽课程", type: "success" },
  { date: d(15), content: "团队建设活动", type: "primary" },
  { date: d(20), content: "代码评审", type: "danger" },
  { date: d(20), content: "团队午餐", type: "primary" },
  { date: d(20), content: "项目进度汇报", type: "warning" },
  { date: d(Math.min(28, dayjs().daysInMonth())), content: "月度总结会", type: "warning" },
]);

const eventForm = ref<CalendarEvent>({
  date: "",
  endDate: "",
  content: "",
  type: "primary",
});

const isEditing = computed(() => editingEventIndex.value >= 0);

const formatDate = (date: string) => date.split("-")[2];

const getEventClasses = (type: CalendarEvent["type"] = "primary") => {
  const classMap = {
    primary: { bgClass: "bg-theme/12", textClass: "text-theme" },
    success: { bgClass: "bg-success/12", textClass: "text-success" },
    warning: { bgClass: "bg-warning/12", textClass: "text-warning" },
    danger: { bgClass: "bg-danger/12", textClass: "text-danger" },
  };
  return classMap[type];
};

const getEvents = (day: string) => {
  return events.value
    .filter((event) => {
      const eventDate = new Date(event.date);
      const cellDate = new Date(day);
      const endDate = event.endDate ? new Date(event.endDate) : new Date(event.date);
      return cellDate >= eventDate && cellDate <= endDate;
    })
    .map((event) => {
      const { bgClass, textClass } = getEventClasses(event.type);
      return { ...event, bgClass, textClass };
    });
};

const resetForm = () => {
  eventForm.value = {
    date: "",
    endDate: "",
    content: "",
    type: "primary",
  };
  editingEventIndex.value = -1;
};

const handleCellClick = (day: string) => {
  dialogTitle.value = "添加事件";
  eventForm.value = {
    date: day,
    content: "",
    type: "primary",
  };
  editingEventIndex.value = -1;
  dialogVisible.value = true;
};

const handleEventClick = (event: CalendarEvent) => {
  dialogTitle.value = "编辑事件";
  eventForm.value = { ...event };
  editingEventIndex.value = events.value.findIndex(
    (e) => e.date === event.date && e.content === event.content
  );
  dialogVisible.value = true;
};

const handleSaveEvent = () => {
  if (!eventForm.value.content || !eventForm.value.date) return;
  if (isEditing.value) {
    events.value[editingEventIndex.value] = { ...eventForm.value };
  } else {
    events.value.push({ ...eventForm.value });
  }
  dialogVisible.value = false;
  resetForm();
};

const handleDeleteEvent = () => {
  if (isEditing.value) {
    events.value.splice(editingEventIndex.value, 1);
    dialogVisible.value = false;
    resetForm();
  }
};
</script>

<style scoped>
.home-calendar {
  width: 100%;
  min-width: 0;
}

:deep(.el-calendar__header) {
  padding: 6px 4px;
  border-bottom: none;
}

:deep(.el-calendar__title) {
  font-size: 14px;
  font-weight: 600;
}

:deep(.el-calendar__header .el-button) {
  padding: 4px 8px;
}

:deep(.el-calendar__body) {
  padding: 2px 0 4px;
}

:deep(.el-calendar-table thead th) {
  padding: 4px 0;
  font-size: 11px;
  font-weight: 500;
}

:deep(.is-selected) {
  background-color: var(--el-color-warning-light-9) !important;
}

:deep(.el-calendar-day) {
  height: auto;
  min-height: 3rem;
  padding: 0;
}

:deep(.el-calendar-day:hover) {
  background-color: transparent !important;
}

:deep(.el-dialog__body) {
  padding-top: 20px;
}
</style>
