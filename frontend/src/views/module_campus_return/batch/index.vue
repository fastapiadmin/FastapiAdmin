<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="90px">
        <el-form-item label="批次名称" prop="batch_name">
          <el-input v-model="searchForm.batch_name" placeholder="请输入批次名称" clearable style="width: 180px" />
        </el-form-item>
        <el-form-item label="年度" prop="year">
          <el-input-number v-model="searchForm.year" :min="2020" :max="2099" style="width: 120px" />
        </el-form-item>
        <el-form-item label="学期" prop="semester">
          <el-select v-model="searchForm.semester" placeholder="请选择" clearable style="width: 140px">
            <el-option label="上学期" value="上学期" />
            <el-option label="下学期" value="下学期" />
            <el-option label="暑假" value="暑假" />
            <el-option label="寒假" value="寒假" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 140px">
            <el-option label="草稿" value="draft" />
            <el-option label="招募中" value="recruiting" />
            <el-option label="审核中" value="reviewing" />
            <el-option label="已确认" value="confirmed" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <i-ep-search />搜索
          </el-button>
          <el-button @click="handleReset">
            <i-ep-refresh />重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">批次列表</span>
          <div class="operations">
            <el-button v-permission="['module_campus_return:batch:create']" type="primary" @click="handleCreate">
              <i-ep-plus />新增
            </el-button>
          </div>
        </div>
      </template>

      <el-table v-loading="loading" :data="tableData" stripe border>
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="batch_name" label="批次名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="year" label="年度" width="80" align="center" />
        <el-table-column prop="semester" label="学期" width="80" align="center" />
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="recruitment_start" label="招募开始" width="110" />
        <el-table-column prop="recruitment_end" label="招募结束" width="110" />
        <el-table-column prop="activity_start" label="活动开始" width="110" />
        <el-table-column prop="activity_end" label="活动结束" width="110" />
        <el-table-column prop="max_teams" label="最大团队数" width="100" align="center" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-permission="['module_campus_return:batch:query']" link type="primary" @click="handleView(row)">
              详情
            </el-button>
            <el-button v-permission="['module_campus_return:batch:update']" link type="primary" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button v-permission="['module_campus_return:batch:delete']" link type="danger" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
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

    <el-dialog v-model="detailDialog.visible" title="批次详情" width="700px">
      <el-descriptions v-if="detailDialog.data" :column="2" border>
        <el-descriptions-item label="批次名称" :span="2">{{ detailDialog.data.batch_name }}</el-descriptions-item>
        <el-descriptions-item label="年度">{{ detailDialog.data.year }}</el-descriptions-item>
        <el-descriptions-item label="学期">{{ detailDialog.data.semester }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(detailDialog.data.status)">{{ getStatusLabel(detailDialog.data.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="审核方式">{{ getReviewTypeLabel(detailDialog.data.review_type) }}</el-descriptions-item>
        <el-descriptions-item label="招募开始日期">{{ detailDialog.data.recruitment_start || "-" }}</el-descriptions-item>
        <el-descriptions-item label="招募结束日期">{{ detailDialog.data.recruitment_end || "-" }}</el-descriptions-item>
        <el-descriptions-item label="活动开始日期">{{ detailDialog.data.activity_start || "-" }}</el-descriptions-item>
        <el-descriptions-item label="活动结束日期">{{ detailDialog.data.activity_end || "-" }}</el-descriptions-item>
        <el-descriptions-item label="最大团队数">{{ detailDialog.data.max_teams }}</el-descriptions-item>
        <el-descriptions-item label="团队人数">{{ detailDialog.data.min_team_members }}-{{ detailDialog.data.max_team_members }}</el-descriptions-item>
        <el-descriptions-item label="需要培训">{{ detailDialog.data.require_training ? "是" : "否" }}</el-descriptions-item>
        <el-descriptions-item label="需要考试">{{ detailDialog.data.require_exam ? "是" : "否" }}</el-descriptions-item>
        <el-descriptions-item label="需要保险">{{ detailDialog.data.require_insurance ? "是" : "否" }}</el-descriptions-item>
        <el-descriptions-item label="需要打卡">{{ detailDialog.data.require_checkin ? "是" : "否" }}</el-descriptions-item>
        <el-descriptions-item label="最少打卡次数">{{ detailDialog.data.min_checkin_count }}</el-descriptions-item>
        <el-descriptions-item label="考试及格分">{{ detailDialog.data.exam_pass_score }}</el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">{{ detailDialog.data.description || "-" }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <el-dialog v-model="formDialog.visible" :title="formDialog.type === 'create' ? '新增批次' : '编辑批次'" width="700px">
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="120px">
        <el-form-item label="批次名称" prop="batch_name">
          <el-input v-model="form.batch_name" placeholder="请输入批次名称" />
        </el-form-item>
        <el-form-item label="年度" prop="year">
          <el-input-number v-model="form.year" :min="2020" :max="2099" style="width: 100%" />
        </el-form-item>
        <el-form-item label="学期" prop="semester">
          <el-select v-model="form.semester" placeholder="请选择学期" style="width: 100%">
            <el-option label="上学期" value="上学期" />
            <el-option label="下学期" value="下学期" />
            <el-option label="暑假" value="暑假" />
            <el-option label="寒假" value="寒假" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择状态" style="width: 100%">
            <el-option label="草稿" value="draft" />
            <el-option label="招募中" value="recruiting" />
            <el-option label="审核中" value="reviewing" />
            <el-option label="已确认" value="confirmed" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item label="审核方式" prop="review_type">
          <el-select v-model="form.review_type" placeholder="请选择" style="width: 100%">
            <el-option label="手动审核" value="manual" />
            <el-option label="自动审核" value="auto" />
            <el-option label="混合审核" value="mixed" />
          </el-select>
        </el-form-item>
        <el-form-item label="招募时间">
          <el-col :span="11">
            <el-form-item prop="recruitment_start">
              <el-date-picker v-model="form.recruitment_start" type="date" placeholder="开始日期" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="2" style="text-align: center">-</el-col>
          <el-col :span="11">
            <el-form-item prop="recruitment_end">
              <el-date-picker v-model="form.recruitment_end" type="date" placeholder="结束日期" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-form-item>
        <el-form-item label="活动日期">
          <el-col :span="11">
            <el-form-item prop="activity_start">
              <el-date-picker v-model="form.activity_start" type="date" placeholder="开始日期" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="2" style="text-align: center">-</el-col>
          <el-col :span="11">
            <el-form-item prop="activity_end">
              <el-date-picker v-model="form.activity_end" type="date" placeholder="结束日期" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-form-item>
        <el-form-item label="团队配置">
          <el-col :span="8">
            <el-form-item prop="max_teams">
              <span style="color: #666">最大团队数:</span>
              <el-input-number v-model="form.max_teams" :min="1" style="width: 80px; margin-left: 5px" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item prop="min_team_members">
              <span style="color: #666">最少人数:</span>
              <el-input-number v-model="form.min_team_members" :min="1" style="width: 80px; margin-left: 5px" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item prop="max_team_members">
              <span style="color: #666">最多人数:</span>
              <el-input-number v-model="form.max_team_members" :min="1" style="width: 80px; margin-left: 5px" />
            </el-form-item>
          </el-col>
        </el-form-item>
        <el-form-item label="要求配置">
          <el-checkbox v-model="form.require_training">需要培训</el-checkbox>
          <el-checkbox v-model="form.require_exam">需要考试</el-checkbox>
          <el-checkbox v-model="form.require_insurance">需要保险</el-checkbox>
          <el-checkbox v-model="form.require_checkin">需要打卡</el-checkbox>
        </el-form-item>
        <el-form-item v-if="form.require_exam" label="考试及格分数" prop="exam_pass_score">
          <el-input-number v-model="form.exam_pass_score" :min="0" :max="100" />
        </el-form-item>
        <el-form-item v-if="form.require_checkin" label="最少打卡次数" prop="min_checkin_count">
          <el-input-number v-model="form.min_checkin_count" :min="1" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="formDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import type { FormInstance, FormRules } from "element-plus";
import { ElMessage, ElMessageBox } from "element-plus";
import { BatchAPI, type BatchItem, type BatchForm, type BatchQuery } from "@/api/module_campus_return/batch";

const loading = ref(false);
const tableData = ref<BatchItem[]>([]);
const searchFormRef = ref<FormInstance>();
const formRef = ref<FormInstance>();

const searchForm = reactive<BatchQuery>({
  batch_name: "",
  year: undefined,
  semester: "",
  status: "",
});

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

const detailDialog = reactive<{ visible: boolean; data: BatchItem | null }>({
  visible: false,
  data: null,
});

const formDialog = reactive<{ visible: boolean; type: "create" | "edit"; id?: number }>({
  visible: false,
  type: "create",
});

const form = reactive<BatchForm & {
  recruitment_start?: string;
  recruitment_end?: string;
  activity_start?: string;
  activity_end?: string;
  require_training: boolean;
  require_exam: boolean;
  require_insurance: boolean;
  require_checkin: boolean;
}>({
  batch_name: "",
  year: new Date().getFullYear(),
  semester: "",
  status: "draft",
  review_type: "manual",
  max_teams: 100,
  min_team_members: 1,
  max_team_members: 10,
  require_training: true,
  require_exam: true,
  require_insurance: true,
  require_checkin: true,
  exam_pass_score: 60,
  min_checkin_count: 3,
});

const formRules: FormRules = {
  batch_name: [{ required: true, message: "请输入批次名称", trigger: "blur" }],
  year: [{ required: true, message: "请选择年度", trigger: "change" }],
  semester: [{ required: true, message: "请选择学期", trigger: "change" }],
};

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    draft: "info",
    recruiting: "success",
    reviewing: "warning",
    confirmed: "success",
    in_progress: "primary",
    completed: "info",
    cancelled: "danger",
  };
  return map[status] || "info";
};

const getStatusLabel = (status: string) => {
  const map: Record<string, string> = {
    draft: "草稿",
    recruiting: "招募中",
    reviewing: "审核中",
    confirmed: "已确认",
    in_progress: "进行中",
    completed: "已完成",
    cancelled: "已取消",
  };
  return map[status] || status;
};

const getReviewTypeLabel = (type: string) => {
  const map: Record<string, string> = { manual: "手动审核", auto: "自动审核", mixed: "混合审核" };
  return map[type] || type;
};

const fetchData = async () => {
  loading.value = true;
  try {
    const res = await BatchAPI.list({ ...searchForm, page: pagination.page, pageSize: pagination.pageSize });
    tableData.value = res.list;
    pagination.total = res.total;
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  pagination.page = 1;
  fetchData();
};

const handleReset = () => {
  searchFormRef.value?.resetFields();
  handleSearch();
};

const handleSizeChange = () => {
  pagination.page = 1;
  fetchData();
};

const handlePageChange = () => {
  fetchData();
};

const handleCreate = () => {
  formDialog.type = "create";
  formDialog.id = undefined;
  Object.assign(form, {
    batch_name: "",
    year: new Date().getFullYear(),
    semester: "",
    status: "draft",
    review_type: "manual",
    max_teams: 100,
    min_team_members: 1,
    max_team_members: 10,
    require_training: true,
    require_exam: true,
    require_insurance: true,
    require_checkin: true,
    exam_pass_score: 60,
    min_checkin_count: 3,
  });
  formDialog.visible = true;
};

const handleEdit = async (row: BatchItem) => {
  formDialog.type = "edit";
  formDialog.id = row.id;
  const res = await BatchAPI.getById(row.id!);
  Object.assign(form, res);
  formDialog.visible = true;
};

const handleView = async (row: BatchItem) => {
  const res = await BatchAPI.getById(row.id!);
  detailDialog.data = res;
  detailDialog.visible = true;
};

const handleSubmit = async () => {
  if (!formRef.value) return;
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (formDialog.type === "create") {
          await BatchAPI.create(form);
          ElMessage.success("创建成功");
        } else {
          await BatchAPI.update(formDialog.id!, form);
          ElMessage.success("更新成功");
        }
        formDialog.visible = false;
        fetchData();
      } catch {
        ElMessage.error("操作失败");
      }
    }
  });
};

const handleDelete = async (row: BatchItem) => {
  await ElMessageBox.confirm("确定删除该批次吗？", "提示", { type: "warning" });
  await BatchAPI.delete(row.id!);
  ElMessage.success("删除成功");
  fetchData();
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.search-card {
  margin-bottom: 16px;
}
.table-card {
  margin-bottom: 16px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.title {
  font-weight: 600;
}
.pagination-container {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>
