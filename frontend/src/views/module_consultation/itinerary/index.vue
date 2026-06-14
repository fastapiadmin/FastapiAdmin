<!-- 招生咨询会 - 行程方案管理 -->
<template>
  <div class="app-container">
    <!-- 搜索卡片 -->
    <el-card class="search-card" shadow="never">
      <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="80px">
        <el-form-item label="咨询会" prop="consultation_id">
          <el-select
            v-model="searchForm.consultation_id"
            placeholder="请选择咨询会"
            clearable
            filterable
            style="width: 220px"
          >
            <el-option
              v-for="item in consultationOptions"
              :key="item.id"
              :label="item.title"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="招生组" prop="team_id">
          <el-select
            v-model="searchForm.team_id"
            placeholder="请选择招生组"
            clearable
            filterable
            style="width: 200px"
          >
            <el-option
              v-for="item in teamOptions"
              :key="item.id"
              :label="item.team_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="方案名称" prop="itinerary_name">
          <el-input
            v-model="searchForm.itinerary_name"
            placeholder="请输入方案名称"
            clearable
            style="width: 180px"
          />
        </el-form-item>
        <el-form-item label="状态" prop="itinerary_status">
          <el-select
            v-model="searchForm.itinerary_status"
            placeholder="请选择状态"
            clearable
            style="width: 120px"
          >
            <el-option label="草稿" value="draft" />
            <el-option label="已确认" value="confirmed" />
            <el-option label="执行中" value="executed" />
            <el-option label="已完成" value="completed" />
            <el-option label="已归档" value="archived" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <i-ep-search />
            搜索
          </el-button>
          <el-button @click="handleReset">
            <i-ep-refresh />
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 视图切换 -->
    <el-card class="table-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">行程方案列表</span>
          <div class="operations">
            <el-radio-group v-model="viewMode" size="small" style="margin-right: 12px">
              <el-radio-button value="list">列表</el-radio-button>
              <el-radio-button value="kanban">看板</el-radio-button>
              <el-radio-button value="calendar">日历</el-radio-button>
            </el-radio-group>
            <el-button
              v-permission="['module_consultation:itinerary:create']"
              type="primary"
              @click="handleCreate"
            >
              <i-ep-plus />
              新增
            </el-button>
            <el-button
              v-permission="['module_consultation:itinerary:delete']"
              type="danger"
              :disabled="!selectedIds.length"
              @click="handleBatchDelete"
            >
              <i-ep-delete />
              批量删除
            </el-button>
          </div>
        </div>
      </template>

      <!-- 列表视图 -->
      <el-table
        v-if="viewMode === 'list'"
        v-loading="loading"
        :data="tableData"
        stripe
        border
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="consultation_id" label="咨询会" width="180" show-overflow-tooltip>
          <template #default="{ row }">
            {{ getConsultationName(row.consultation_id) }}
          </template>
        </el-table-column>
        <el-table-column prop="team_id" label="招生组" width="150" show-overflow-tooltip>
          <template #default="{ row }">
            {{ getTeamName(row.team_id) }}
          </template>
        </el-table-column>
        <el-table-column
          prop="itinerary_name"
          label="方案名称"
          min-width="150"
          show-overflow-tooltip
        >
          <template #default="{ row }">
            <el-link type="primary" @click="handleView(row)">
              {{ row.itinerary_name || "-" }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column prop="start_date" label="开始日期" width="110" />
        <el-table-column prop="end_date" label="结束日期" width="110" />
        <el-table-column prop="departure_city" label="出发城市" width="100" />
        <el-table-column prop="destination_city" label="目的城市" width="100" />
        <el-table-column prop="board_column" label="看板列" width="100">
          <template #default="{ row }">
            <el-tag :type="getBoardColumnType(row.board_column)">
              {{ getBoardColumnLabel(row.board_column) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="itinerary_status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.itinerary_status)">
              {{ getStatusLabel(row.itinerary_status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_synced" label="已同步" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_synced ? 'success' : 'info'" size="small">
              {{ row.is_synced ? "是" : "否" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              v-permission="['module_consultation:itinerary:detail']"
              link
              type="primary"
              @click="handleView(row)"
            >
              详情
            </el-button>
            <el-button
              v-permission="['module_consultation:itinerary:update']"
              link
              type="primary"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              v-permission="['module_consultation:itinerary:move_task']"
              link
              type="warning"
              @click="handleMoveTask(row)"
            >
              移动
            </el-button>
            <el-button
              v-permission="['module_consultation:itinerary:delete']"
              link
              type="danger"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 看板视图 -->
      <div v-else-if="viewMode === 'kanban'" v-loading="kanbanLoading" class="kanban-board">
        <div v-for="column in kanbanColumns" :key="column.key" class="kanban-column">
          <div class="kanban-column-header">
            <span class="kanban-column-title">{{ column.label }}</span>
            <el-badge :value="kanbanData[column.key]?.length || 0" :type="column.type" />
          </div>
          <div class="kanban-column-body" @dragover.prevent @drop="handleDrop(column.key, $event)">
            <div
              v-for="item in kanbanData[column.key]"
              :key="item.id"
              class="kanban-card"
              draggable="true"
              @dragstart="handleDragStart(item, $event)"
            >
              <div class="kanban-card-title">{{ item.itinerary_name || `行程-${item.id}` }}</div>
              <div class="kanban-card-info">
                <span>
                  <i-ep-location />
                  {{ item.destination_city || "-" }}
                </span>
                <span>
                  <i-ep-calendar />
                  {{ item.start_date }}
                </span>
              </div>
              <div class="kanban-card-tags">
                <el-tag v-if="item.auto_generated" type="warning" size="small">自动生成</el-tag>
                <el-tag :type="getStatusType(item.itinerary_status)" size="small">
                  {{ getStatusLabel(item.itinerary_status) }}
                </el-tag>
              </div>
              <div class="kanban-card-actions">
                <el-button link type="primary" size="small" @click="handleView(item)">
                  详情
                </el-button>
                <el-button link type="warning" size="small" @click="handleMoveTask(item)">
                  移动
                </el-button>
              </div>
            </div>
            <div v-if="!kanbanData[column.key]?.length" class="kanban-empty">暂无可拖拽任务</div>
          </div>
        </div>
      </div>

      <!-- 日历视图 -->
      <div v-else-if="viewMode === 'calendar'" v-loading="calendarLoading" class="calendar-board">
        <div class="calendar-header">
          <el-button size="small" @click="prevMonth">
            <i-ep-arrow-left />
            上月
          </el-button>
          <span class="calendar-title">{{ currentMonth }}</span>
          <el-button size="small" @click="nextMonth">
            下月
            <i-ep-arrow-right />
          </el-button>
        </div>
        <div class="calendar-grid">
          <div class="calendar-weekday">
            <span v-for="day in weekDays" :key="day">{{ day }}</span>
          </div>
          <div class="calendar-days">
            <div
              v-for="(day, index) in calendarDays"
              :key="index"
              class="calendar-day"
              :class="{ 'other-month': !day.isCurrentMonth, today: day.isToday }"
            >
              <span class="day-number">{{ day.date }}</span>
              <div class="day-items">
                <div
                  v-for="item in day.items"
                  :key="item.id"
                  class="calendar-item"
                  @click="handleView(item)"
                >
                  <span class="calendar-item-title">
                    {{ item.itinerary_name || `行程-${item.id}` }}
                  </span>
                  <span class="calendar-item-city">{{ item.destination_city }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="viewMode === 'list'" class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailDialog.visible" title="行程方案详情" width="600px">
      <el-descriptions v-if="detailDialog.data" :column="2" border>
        <el-descriptions-item label="咨询会">
          {{ getConsultationName(detailDialog.data.consultation_id) }}
        </el-descriptions-item>
        <el-descriptions-item label="招生组">
          {{ getTeamName(detailDialog.data.team_id) }}
        </el-descriptions-item>
        <el-descriptions-item label="方案名称" :span="2">
          {{ detailDialog.data.itinerary_name || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="开始日期">
          {{ detailDialog.data.start_date }}
        </el-descriptions-item>
        <el-descriptions-item label="结束日期">
          {{ detailDialog.data.end_date || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="出发城市">
          {{ detailDialog.data.departure_city || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="目的城市">
          {{ detailDialog.data.destination_city || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="交通方式">
          {{ detailDialog.data.transportation || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="车次/航班">
          {{ detailDialog.data.transportation_no || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="出发时间">
          {{ detailDialog.data.departure_time || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="到达时间">
          {{ detailDialog.data.arrival_time || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="酒店名称" :span="2">
          {{ detailDialog.data.hotel_name || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="酒店地址" :span="2">
          {{ detailDialog.data.hotel_address || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="入住日期">
          {{ detailDialog.data.check_in_date || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="退房日期">
          {{ detailDialog.data.check_out_date || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="房间号">
          {{ detailDialog.data.room_number || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="看板列">
          <el-tag :type="getBoardColumnType(detailDialog.data.board_column)">
            {{ getBoardColumnLabel(detailDialog.data.board_column) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="任务类型">
          <el-tag v-if="detailDialog.data.auto_generated" type="warning">自动生成</el-tag>
          <span v-else>手动</span>
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(detailDialog.data.itinerary_status)">
            {{ getStatusLabel(detailDialog.data.itinerary_status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="已同步">
          <el-tag :type="detailDialog.data.is_synced ? 'success' : 'info'">
            {{ detailDialog.data.is_synced ? "是" : "否" }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 新增/编辑弹窗 -->
    <el-dialog
      v-model="formDialog.visible"
      :title="formDialog.type === 'create' ? '新增行程方案' : '编辑行程方案'"
      width="550px"
    >
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="咨询会" prop="consultation_id">
          <el-select
            v-model="form.consultation_id"
            placeholder="请选择咨询会"
            clearable
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="item in consultationOptions"
              :key="item.id"
              :label="item.title"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="招生组" prop="team_id">
          <el-select
            v-model="form.team_id"
            placeholder="请选择招生组"
            clearable
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="item in teamOptions"
              :key="item.id"
              :label="item.team_name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="方案名称" prop="itinerary_name">
          <el-input v-model="form.itinerary_name" placeholder="请输入方案名称" />
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker
            v-model="form.start_date"
            type="date"
            placeholder="选择开始日期"
            value-format="YYYY-MM-DD"
            style="width: 200px"
          />
        </el-form-item>
        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker
            v-model="form.end_date"
            type="date"
            placeholder="选择结束日期"
            value-format="YYYY-MM-DD"
            style="width: 200px"
          />
        </el-form-item>
        <el-form-item label="出发城市" prop="departure_city">
          <el-input v-model="form.departure_city" placeholder="请输入出发城市" />
        </el-form-item>
        <el-form-item label="目的城市" prop="destination_city">
          <el-input v-model="form.destination_city" placeholder="请输入目的城市" />
        </el-form-item>
        <el-form-item label="交通方式" prop="transportation">
          <el-input v-model="form.transportation" placeholder="请输入交通方式" />
        </el-form-item>
        <el-form-item label="车次/航班" prop="transportation_no">
          <el-input v-model="form.transportation_no" placeholder="请输入车次/航班" />
        </el-form-item>
        <el-form-item label="出发时间" prop="departure_time">
          <el-date-picker
            v-model="form.departure_time"
            type="datetime"
            placeholder="选择出发时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 200px"
          />
        </el-form-item>
        <el-form-item label="到达时间" prop="arrival_time">
          <el-date-picker
            v-model="form.arrival_time"
            type="datetime"
            placeholder="选择到达时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 200px"
          />
        </el-form-item>
        <el-form-item label="酒店名称" prop="hotel_name">
          <el-input v-model="form.hotel_name" placeholder="请输入酒店名称" />
        </el-form-item>
        <el-form-item label="酒店地址" prop="hotel_address">
          <el-input v-model="form.hotel_address" placeholder="请输入酒店地址" />
        </el-form-item>
        <el-form-item label="入住日期" prop="check_in_date">
          <el-date-picker
            v-model="form.check_in_date"
            type="date"
            placeholder="选择入住日期"
            value-format="YYYY-MM-DD"
            style="width: 200px"
          />
        </el-form-item>
        <el-form-item label="退房日期" prop="check_out_date">
          <el-date-picker
            v-model="form.check_out_date"
            type="date"
            placeholder="选择退房日期"
            value-format="YYYY-MM-DD"
            style="width: 200px"
          />
        </el-form-item>
        <el-form-item label="房间号" prop="room_number">
          <el-input v-model="form.room_number" placeholder="请输入房间号" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="formDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 移动任务弹窗 -->
    <el-dialog v-model="moveDialog.visible" title="移动任务" width="400px">
      <el-form label-width="80px">
        <el-form-item label="当前列">
          <el-tag :type="getBoardColumnType(moveDialog.data?.board_column)">
            {{ getBoardColumnLabel(moveDialog.data?.board_column) }}
          </el-tag>
        </el-form-item>
        <el-form-item label="移动到">
          <el-select
            v-model="moveDialog.targetColumn"
            placeholder="请选择目标列"
            style="width: 200px"
          >
            <el-option
              v-for="col in kanbanColumns"
              :key="col.key"
              :label="col.label"
              :value="col.key"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="moveDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleMoveSubmit">确定移动</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted, computed } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";
import ItineraryAPI, {
  type ItineraryItem,
  type ItineraryQuery,
} from "@/api/module_consultation/itinerary";
import ConsultationInfoAPI, {
  type ConsultationOption,
} from "@/api/module_consultation/consultation";
import TeamAPI, { type TeamItem } from "@/api/module_promotion/team";

// 下拉选项
const consultationOptions = ref<ConsultationOption[]>([]);
const teamOptions = ref<TeamItem[]>([]);

const loadOptions = async () => {
  try {
    const consultRes = await ConsultationInfoAPI.getApprovedOptions();
    if (consultRes.data?.data) {
      consultationOptions.value = consultRes.data.data;
    }
  } catch {
    // ignore
  }
  try {
    const teamRes = await TeamAPI.getList({} as any);
    if (teamRes.data?.data?.items) {
      teamOptions.value = teamRes.data.data.items;
    } else if (teamRes.data?.data) {
      teamOptions.value = Array.isArray(teamRes.data.data) ? teamRes.data.data : [];
    }
  } catch {
    // ignore
  }
};

const getConsultationName = (id: number | undefined) => {
  if (!id) return "-";
  const item = consultationOptions.value.find((c) => c.id === id);
  return item?.title || String(id);
};

const getTeamName = (id: number | undefined) => {
  if (!id) return "-";
  const item = teamOptions.value.find((t) => t.id === id);
  return item?.team_name || String(id);
};

const searchForm = reactive<ItineraryQuery>({
  consultation_id: undefined,
  team_id: undefined,
  itinerary_name: undefined,
  itinerary_status: undefined,
});
const loading = ref(false);
const tableData = ref<ItineraryItem[]>([]);
const selectedIds = ref<number[]>([]);
const pagination = reactive({ page: 1, pageSize: 10, total: 0 });

// 视图模式
const viewMode = ref<"list" | "kanban" | "calendar">("list");

// 看板相关
const kanbanLoading = ref(false);
const kanbanData = ref<{ todo: ItineraryItem[]; doing: ItineraryItem[]; done: ItineraryItem[] }>({
  todo: [],
  doing: [],
  done: [],
});
const kanbanColumns = [
  { key: "todo", label: "待办", type: "info" },
  { key: "doing", label: "进行中", type: "warning" },
  { key: "done", label: "已完成", type: "success" },
];
const draggedItem = ref<ItineraryItem | null>(null);

// 日历相关
const calendarLoading = ref(false);
const currentDate = ref(new Date());
const weekDays = ["日", "一", "二", "三", "四", "五", "六"];

const currentMonth = computed(() => {
  const year = currentDate.value.getFullYear();
  const month = currentDate.value.getMonth() + 1;
  return `${year}年${month}月`;
});

interface CalendarDay {
  date: number;
  isCurrentMonth: boolean;
  isToday: boolean;
  items: ItineraryItem[];
}

const calendarDays = computed<CalendarDay[]>(() => {
  const year = currentDate.value.getFullYear();
  const month = currentDate.value.getMonth();
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const startWeekDay = firstDay.getDay();
  const endWeekDay = lastDay.getDay();
  const days: CalendarDay[] = [];
  const today = new Date();

  // 上月部分
  for (let i = startWeekDay - 1; i >= 0; i--) {
    const d = new Date(year, month, -i);
    days.push({ date: d.getDate(), isCurrentMonth: false, isToday: false, items: [] });
  }

  // 当月部分
  for (let i = 1; i <= lastDay.getDate(); i++) {
    const d = new Date(year, month, i);
    const dateStr = `${year}-${String(month + 1).padStart(2, "0")}-${String(i).padStart(2, "0")}`;
    const isToday = d.toDateString() === today.toDateString();
    const items = kanbanData.value.todo
      .concat(kanbanData.value.doing)
      .concat(kanbanData.value.done)
      .filter((item) => item.start_date === dateStr);
    days.push({ date: i, isCurrentMonth: true, isToday, items });
  }

  // 下月部分
  for (let i = 1; i < 7 - endWeekDay; i++) {
    days.push({ date: i, isCurrentMonth: false, isToday: false, items: [] });
  }

  return days;
});

// 弹窗状态
const formDialog = reactive({
  visible: false,
  type: "create" as "create" | "edit",
  data: undefined as ItineraryItem | undefined,
});
const detailDialog = reactive({ visible: false, data: undefined as ItineraryItem | undefined });
const moveDialog = reactive({
  visible: false,
  data: undefined as ItineraryItem | undefined,
  targetColumn: "",
});
const formRef = ref<FormInstance>();

const form = reactive<any>({
  consultation_id: undefined,
  team_id: undefined,
  itinerary_name: "",
  start_date: "",
  end_date: "",
  departure_city: "",
  destination_city: "",
  transportation: "",
  departure_time: "",
  arrival_time: "",
  transportation_no: "",
  hotel_name: "",
  hotel_address: "",
  check_in_date: "",
  check_out_date: "",
  room_number: "",
});

const formRules: FormRules = {
  consultation_id: [{ required: true, message: "请输入咨询会ID", trigger: "blur" }],
  start_date: [{ required: true, message: "请选择开始日期", trigger: "change" }],
};

// 获取列表
const fetchList = async () => {
  loading.value = true;
  try {
    const params = { page_no: pagination.page, page_size: pagination.pageSize, ...searchForm };
    const res = await ItineraryAPI.getList(params);
    if (res.data?.data) {
      tableData.value = res.data.data.items || [];
      pagination.total = res.data.data.total || 0;
    }
  } finally {
    loading.value = false;
  }
};

// 获取看板数据
const fetchKanbanData = async () => {
  kanbanLoading.value = true;
  try {
    const res = await ItineraryAPI.getKanbanBoard();
    if (res.data?.data) {
      kanbanData.value = res.data.data;
    }
  } finally {
    kanbanLoading.value = false;
  }
};

// 日历操作
const prevMonth = () => {
  currentDate.value = new Date(
    currentDate.value.getFullYear(),
    currentDate.value.getMonth() - 1,
    1
  );
};
const nextMonth = () => {
  currentDate.value = new Date(
    currentDate.value.getFullYear(),
    currentDate.value.getMonth() + 1,
    1
  );
};

// 监听视图模式变化
const handleViewModeChange = () => {
  if (viewMode.value === "kanban" || viewMode.value === "calendar") {
    fetchKanbanData();
  }
};

// 看板拖拽
const handleDragStart = (item: ItineraryItem, event: DragEvent) => {
  draggedItem.value = item;
  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = "move";
  }
};
const handleDrop = async (column: string, event: DragEvent) => {
  event.preventDefault();
  if (!draggedItem.value) return;
  try {
    await ItineraryAPI.moveTask(draggedItem.value.id!, { board_column: column });
    ElMessage.success("任务移动成功");
    await fetchKanbanData();
  } catch {
    ElMessage.error("移动失败");
  }
  draggedItem.value = null;
};

// 操作处理
const handleSearch = () => {
  pagination.page = 1;
  fetchList();
};
const handleReset = () => {
  Object.assign(searchForm, {
    consultation_id: undefined,
    team_id: undefined,
    itinerary_name: undefined,
    itinerary_status: undefined,
  });
  handleSearch();
};
const handleSelectionChange = (selection: ItineraryItem[]) => {
  selectedIds.value = selection.map((item) => item.id!);
};
const handleSizeChange = (size: number) => {
  pagination.pageSize = size;
  fetchList();
};
const handlePageChange = (page: number) => {
  pagination.page = page;
  fetchList();
};

const getStatusType = (status: string) => {
  if (status === "draft") return "info";
  if (status === "confirmed") return "success";
  if (status === "executed") return "warning";
  if (status === "completed") return "success";
  return "";
};
const getStatusLabel = (status: string) => {
  if (status === "draft") return "草稿";
  if (status === "confirmed") return "已确认";
  if (status === "executed") return "执行中";
  if (status === "completed") return "已完成";
  if (status === "archived") return "已归档";
  return status;
};
const getBoardColumnType = (column?: string) => {
  if (column === "todo") return "info";
  if (column === "doing") return "warning";
  if (column === "done") return "success";
  return "info";
};
const getBoardColumnLabel = (column?: string) => {
  if (column === "todo") return "待办";
  if (column === "doing") return "进行中";
  if (column === "done") return "已完成";
  return "待办";
};

const handleCreate = () => {
  formDialog.type = "create";
  Object.assign(form, {
    consultation_id: undefined,
    team_id: undefined,
    itinerary_name: "",
    start_date: "",
    end_date: "",
    departure_city: "",
    destination_city: "",
    transportation: "",
    departure_time: "",
    arrival_time: "",
    transportation_no: "",
    hotel_name: "",
    hotel_address: "",
    check_in_date: "",
    check_out_date: "",
    room_number: "",
  });
  formDialog.visible = true;
};

const handleView = (row: ItineraryItem) => {
  detailDialog.data = row;
  detailDialog.visible = true;
};
const handleEdit = (row: ItineraryItem) => {
  formDialog.type = "edit";
  formDialog.data = row;
  Object.assign(form, row);
  formDialog.visible = true;
};

const handleMoveTask = (row: ItineraryItem) => {
  moveDialog.data = row;
  moveDialog.targetColumn = "";
  moveDialog.visible = true;
};
const handleMoveSubmit = async () => {
  if (!moveDialog.targetColumn) {
    ElMessage.warning("请选择目标列");
    return;
  }
  try {
    await ItineraryAPI.moveTask(moveDialog.data!.id!, { board_column: moveDialog.targetColumn });
    ElMessage.success("任务移动成功");
    moveDialog.visible = false;
    if (viewMode.value !== "list") await fetchKanbanData();
    else await fetchList();
  } catch {
    ElMessage.error("移动失败");
  }
};

const handleSubmit = async () => {
  if (!formRef.value) return;
  await formRef.value.validate(async (valid) => {
    if (valid) {
      if (formDialog.type === "create") {
        await ItineraryAPI.create(form);
        ElMessage.success("创建成功");
      } else {
        await ItineraryAPI.update(formDialog.data!.id!, form);
        ElMessage.success("更新成功");
      }
      formDialog.visible = false;
      if (viewMode.value !== "list") await fetchKanbanData();
      else await fetchList();
    }
  });
};

const handleDelete = (row: ItineraryItem) => {
  ElMessageBox.confirm(`确定要删除这条行程方案吗？`, "删除确认", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await ItineraryAPI.delete(row.id!);
      ElMessage.success("删除成功");
      if (viewMode.value !== "list") await fetchKanbanData();
      else await fetchList();
    })
    .catch(() => {});
};

const handleBatchDelete = () => {
  if (!selectedIds.value.length) {
    ElMessage.warning("请选择要删除的记录");
    return;
  }
  ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 条记录吗？`, "批量删除确认", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await ItineraryAPI.batchDelete(selectedIds.value);
      ElMessage.success("批量删除成功");
      fetchList();
    })
    .catch(() => {});
};

// 监听视图模式
onMounted(() => {
  loadOptions();
  fetchList();
  watch(() => viewMode.value, handleViewModeChange);
});
</script>

<style lang="scss" scoped>
.search-card {
  margin-bottom: 16px;
}
.table-card {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    .title {
      font-size: 16px;
      font-weight: 600;
    }
    .operations {
      display: flex;
      gap: 8px;
    }
  }
}
.pagination-container {
  display: flex;
  justify-content: flex-end;
  padding-top: 16px;
}

// 看板样式
.kanban-board {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding: 8px 0;
}
.kanban-column {
  flex: 1;
  min-width: 280px;
  max-width: 350px;
  background: #f5f7fa;
  border-radius: 8px;
  padding: 12px;
}
.kanban-column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 2px solid #e4e7ed;
}
.kanban-column-title {
  font-weight: 600;
  font-size: 15px;
  color: #303133;
}
.kanban-column-body {
  min-height: 400px;
}
.kanban-card {
  background: #fff;
  border-radius: 6px;
  padding: 12px;
  margin-bottom: 8px;
  cursor: grab;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.2s;
}
.kanban-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}
.kanban-card-title {
  font-weight: 600;
  font-size: 14px;
  color: #303133;
  margin-bottom: 8px;
}
.kanban-card-info {
  font-size: 12px;
  color: #909399;
  display: flex;
  gap: 12px;
  margin-bottom: 8px;
}
.kanban-card-tags {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}
.kanban-card-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}
.kanban-empty {
  text-align: center;
  color: #c0c4cc;
  padding: 40px 0;
}

// 日历样式
.calendar-board {
  padding: 8px 0;
}
.calendar-header {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}
.calendar-title {
  font-weight: 600;
  font-size: 16px;
}
.calendar-grid {
  border: 1px solid #ebeef5;
  border-radius: 4px;
}
.calendar-weekday {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}
.calendar-weekday span {
  text-align: center;
  padding: 8px;
  font-weight: 600;
  color: #606266;
}
.calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
}
.calendar-day {
  min-height: 100px;
  border-right: 1px solid #ebeef5;
  border-bottom: 1px solid #ebeef5;
  padding: 4px;
}
.calendar-day:nth-child(7n) {
  border-right: none;
}
.calendar-day.other-month {
  background: #fafafa;
}
.calendar-day.other-month .day-number {
  color: #c0c4cc;
}
.calendar-day.today {
  background: #ecf5ff;
}
.calendar-day.today .day-number {
  color: #409eff;
  font-weight: 600;
}
.day-number {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 4px;
}
.day-items {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.calendar-item {
  background: #409eff;
  color: #fff;
  border-radius: 2px;
  padding: 2px 4px;
  font-size: 12px;
  cursor: pointer;
}
.calendar-item:hover {
  background: #66b1ff;
}
.calendar-item-title {
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.calendar-item-city {
  display: block;
  font-size: 10px;
  opacity: 0.8;
}
</style>
