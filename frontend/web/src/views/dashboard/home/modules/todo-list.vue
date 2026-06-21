<template>
  <div class="fa-card p-5 h-134 overflow-hidden">
    <div class="fa-card-header">
      <div class="title">
        <h4>待办事项</h4>
        <p>
          待处理
          <span class="text-danger">3</span>
        </p>
      </div>
    </div>

    <ElScrollbar class="h-[calc(100%-40px)]">
      <div
        class="flex items-center justify-between h-17.5 border-b border-g-300 text-sm last:border-b-0"
        v-for="(item, index) in list"
        :key="index"
      >
        <div>
          <p class="text-sm">
            <span class="text-g-800 font-medium">{{ item.username }}</span>
            <span class="mx-2 text-g-600">{{ item.type }}</span>
            <span class="text-theme">{{ item.target }}</span>
          </p>
          <p class="text-g-500 mt-1">{{ item.date }}</p>
        </div>
        <ElCheckbox v-model="item.complate" />
      </div>
    </ElScrollbar>
  </div>
</template>

<script setup lang="ts">
interface TodoItem {
  username: string;
  date: string;
  complate: boolean;
  type: string;
  target: string;
}

/**
 * 待办事项列表
 * 记录每日工作任务及完成状态
 */
const list = reactive<TodoItem[]>([
  {
    username: "张无忌",
    date: "上午 09:30",
    complate: true,
    type: "查看",
    target: "查看今天工作内容",
  },
  {
    username: "赵敏",
    date: "上午 10:30",
    complate: true,
    type: "回复",
    target: "回复邮件",
  },
  {
    username: "小昭",
    date: "上午 11:00",
    complate: true,
    type: "工作",
    target: "工作汇报整理",
  },
  {
    username: "金毛狮王",
    date: "下午 02:00",
    complate: false,
    type: "会议",
    target: "产品需求会议",
  },
  {
    username: "金花婆婆",
    date: "下午 03:30",
    complate: false,
    type: "会议",
    target: "整理会议内容",
  },
  {
    username: "张三丰",
    date: "下午 06:30",
    complate: false,
    type: "计划",
    target: "明天工作计划",
  },
  {
    username: "王思聪",
    date: "下午 06:30",
    complate: false,
    type: "计划",
    target: "明天工作内容",
  },
  {
    username: "范小荷",
    date: "下午 06:30",
    complate: false,
    type: "计划",
    target: "一起去看电影",
  },
  {
    username: "张无忌",
    date: "下午 06:30",
    complate: false,
    type: "计划",
    target: "练习乾坤大挪移",
  },
]);
</script>
