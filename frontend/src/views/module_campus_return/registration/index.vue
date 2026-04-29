<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="90px">
        <el-form-item label="学生姓名" prop="student_name">
          <el-input v-model="searchForm.student_name" placeholder="请输入学生姓名" clearable style="width: 150px" />
        </el-form-item>
        <el-form-item label="批次" prop="batch_id">
          <el-input-number v-model="searchForm.batch_id" :min="0" placeholder="批次ID" style="width: 120px" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 140px">
            <el-option label="草稿" value="draft" />
            <el-option label="待审核" value="pending" />
            <el-option label="已通过" value="approved" />
            <el-option label="已拒绝" value="rejected" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch"><i-ep-search />搜索</el-button>
          <el-button @click="handleReset"><i-ep-refresh />重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">报名列表</span>
          <div class="operations">
            <el-button v-permission="['module_campus_return:registration:create']" type="primary" @click="handleCreate">
              <i-ep-plus />新增
            </el-button>
          </div>
        </div>
      </template>

      <el-table v-loading="loading" :data="tableData" stripe border>
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="student_name" label="学生姓名" width="100" />
        <el-table-column prop="student_number" label="学号" width="120" />
        <el-table-column prop="phone" label="联系电话" width="120" />
        <el-table-column prop="high_school_name" label="目标高中" min-width="150" show-overflow-tooltip />
        <el-table-column prop="batch_id" label="批次ID" width="80" align="center" />
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="review_comment" label="审核意见" min-width="120" show-overflow-tooltip />
        <el-table-column prop="created_time" label="创建时间" width="160" />
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button v-permission="['module_campus_return:registration:query']" link type="primary" @click="handleView(row)">
              详情
            </el-button>
            <el-button v-permission="['module_campus_return:registration:update']" link type="primary" @click="handleEdit(row)" :disabled="row.status !== 'draft' && row.status !== 'rejected'">
              编辑
            </el-button>
            <el-button v-permission="['module_campus_return:registration:approve']" link type="success" :disabled="row.status !== 'pending'" @click="handleApprove(row)">
              审批
            </el-button>
            <el-button v-permission="['module_campus_return:registration:delete']" link type="danger" @click="handleDelete(row)">
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

    <el-dialog v-model="detailDialog.visible" title="报名详情" width="650px">
      <el-descriptions v-if="detailDialog.data" :column="2" border>
        <el-descriptions-item label="学生姓名">{{ detailDialog.data.student_name }}</el-descriptions-item>
        <el-descriptions-item label="学号">{{ detailDialog.data.student_number || "-" }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ detailDialog.data.phone || "-" }}</el-descriptions-item>
        <el-descriptions-item label="电子邮箱">{{ detailDialog.data.email || "-" }}</el-descriptions-item>
        <el-descriptions-item label="目标高中">{{ detailDialog.data.high_school_name || "-" }}</el-descriptions-item>
        <el-descriptions-item label="批次ID">{{ detailDialog.data.batch_id }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(detailDialog.data.status)">{{ getStatusLabel(detailDialog.data.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="审核意见" :span="2">{{ detailDialog.data.review_comment || "-" }}</el-descriptions-item>
        <el-descriptions-item label="报名动机" :span="2">{{ detailDialog.data.motivation || "-" }}</el-descriptions-item>
        <el-descriptions-item label="相关经历" :span="2">{{ detailDialog.data.experience || "-" }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ detailDialog.data.created_time }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <el-dialog v-model="formDialog.visible" :title="formDialog.type === 'create' ? '新增报名' : '编辑报名'" width="600px">
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="批次ID" prop="batch_id">
          <el-input-number v-model="form.batch_id" :min="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="学生姓名" prop="student_name">
          <el-input v-model="form.student_name" placeholder="请输入学生姓名" />
        </el-form-item>
        <el-form-item label="学号" prop="student_number">
          <el-input v-model="form.student_number" placeholder="请输入学号" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="电子邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入电子邮箱" />
        </el-form-item>
        <el-form-item label="目标高中" prop="high_school_name">
          <el-input v-model="form.high_school_name" placeholder="请输入目标高中名称" />
        </el-form-item>
        <el-form-item label="报名动机" prop="motivation">
          <el-input v-model="form.motivation" type="textarea" :rows="3" placeholder="请输入报名动机" />
        </el-form-item>
        <el-form-item label="相关经历" prop="experience">
          <el-input v-model="form.experience" type="textarea" :rows="3" placeholder="请输入相关经历" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="formDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="approveDialog.visible" title="报名审批" width="500px">
      <el-form ref="approveFormRef" :model="approveForm" label-width="80px">
        <el-form-item label="审批结果">
          <el-radio-group v-model="approveForm.approved">
            <el-radio :value="true">通过</el-radio>
            <el-radio :value="false">拒绝</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="审批意见">
          <el-input v-model="approveForm.comment" type="textarea" :rows="3" placeholder="请输入审批意见" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="approveDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleApproveSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import type { FormInstance } from "element-plus";
import { ElMessage, ElMessageBox } from "element-plus";
import { RegistrationAPI, type RegistrationItem, type RegistrationForm, type RegistrationQuery } from "@/api/module_campus_return/registration";

const loading = ref(false);
const tableData = ref<RegistrationItem[]>([]);
const searchFormRef = ref<FormInstance>();
const formRef = ref<FormInstance>();
const approveFormRef = ref<FormInstance>();

const searchForm = reactive<RegistrationQuery>({
  student_name: "",
  batch_id: undefined,
  status: "",
});

const pagination = reactive({ page: 1, pageSize: 10, total: 0 });

const detailDialog = reactive<{ visible: boolean; data: RegistrationItem | null }>({ visible: false, data: null });

const formDialog = reactive<{ visible: boolean; type: "create" | "edit"; id?: number }>({ visible: false, type: "create" });

const form = reactive<RegistrationForm>({
  batch_id: 0,
  student_name: "",
  student_number: "",
  phone: "",
  email: "",
  high_school_name: "",
  motivation: "",
  experience: "",
});

const approveForm = reactive({ approved: true, comment: "", id: 0 });

const formRules = {
  batch_id: [{ required: true, message: "请输入批次ID", trigger: "blur" }],
  student_name: [{ required: true, message: "请输入学生姓名", trigger: "blur" }],
};

const getStatusType = (status: string) => {
  const map: Record<string, string> = { draft: "info", pending: "warning", approved: "success", rejected: "danger" };
  return map[status] || "info";
};

const getStatusLabel = (status: string) => {
  const map: Record<string, string> = { draft: "草稿", pending: "待审核", approved: "已通过", rejected: "已拒绝" };
  return map[status] || status;
};

const fetchData = async () => {
  loading.value = true;
  try {
    const res = await RegistrationAPI.list({ ...searchForm, page: pagination.page, pageSize: pagination.pageSize });
    tableData.value = res.list || [];
    pagination.total = res.total || 0;
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => { pagination.page = 1; fetchData(); };
const handleReset = () => { searchFormRef.value?.resetFields(); handleSearch(); };
const handleSizeChange = () => { pagination.page = 1; fetchData(); };
const handlePageChange = () => { fetchData(); };

const handleCreate = () => {
  formDialog.type = "create";
  Object.assign(form, { batch_id: 0, student_name: "", student_number: "", phone: "", email: "", high_school_name: "", motivation: "", experience: "" });
  formDialog.visible = true;
};

const handleEdit = async (row: RegistrationItem) => {
  formDialog.type = "edit";
  formDialog.id = row.id;
  const res = await RegistrationAPI.getById(row.id!);
  Object.assign(form, res);
  formDialog.visible = true;
};

const handleView = async (row: RegistrationItem) => {
  const res = await RegistrationAPI.getById(row.id!);
  detailDialog.data = res;
  detailDialog.visible = true;
};

const handleSubmit = async () => {
  if (!formRef.value) return;
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (formDialog.type === "create") {
          await RegistrationAPI.create(form);
          ElMessage.success("创建成功");
        } else {
          await RegistrationAPI.update(formDialog.id!, form);
          ElMessage.success("更新成功");
        }
        formDialog.visible = false;
        fetchData();
      } catch { ElMessage.error("操作失败"); }
    }
  });
};

const handleApprove = (row: RegistrationItem) => {
  approveForm.id = row.id!;
  approveForm.approved = true;
  approveForm.comment = "";
  approveDialog.visible = true;
};

const handleApproveSubmit = async () => {
  try {
    if (approveForm.approved) {
      await RegistrationAPI.approve(approveForm.id, approveForm.comment);
      ElMessage.success("审批通过");
    } else {
      await RegistrationAPI.reject(approveForm.id, approveForm.comment);
      ElMessage.success("已拒绝");
    }
    approveDialog.visible = false;
    fetchData();
  } catch { ElMessage.error("操作失败"); }
};

const handleDelete = async (row: RegistrationItem) => {
  await ElMessageBox.confirm("确定删除该报名记录吗？", "提示", { type: "warning" });
  await RegistrationAPI.delete(row.id!);
  ElMessage.success("删除成功");
  fetchData();
};

const approveDialog = reactive({ visible: false });

onMounted(() => { fetchData(); });
</script>

<style scoped>
.search-card { margin-bottom: 16px; }
.table-card { margin-bottom: 16px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.title { font-weight: 600; }
.pagination-container { margin-top: 16px; display: flex; justify-content: flex-end; }
</style>
