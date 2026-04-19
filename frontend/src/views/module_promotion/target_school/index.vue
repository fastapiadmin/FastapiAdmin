<!-- 招生宣传活动 - 目标学校管理 -->
<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="80px">
        <el-form-item label="学校名称" prop="school_name">
          <el-input v-model="searchForm.school_name" placeholder="请输入学校名称" clearable style="width: 180px" />
        </el-form-item>
        <el-form-item label="学校编码" prop="school_code">
          <el-input v-model="searchForm.school_code" placeholder="请输入学校编码" clearable style="width: 140px" />
        </el-form-item>
        <el-form-item label="学校级别" prop="school_level">
          <el-select v-model="searchForm.school_level" placeholder="请选择级别" clearable style="width: 140px">
            <el-option label="高中" value="high_school" />
            <el-option label="初中" value="middle_school" />
            <el-option label="完全中学" value="complete_school" />
            <el-option label="九年一贯制" value="nine_year" />
          </el-select>
        </el-form-item>
        <el-form-item label="省份" prop="province">
          <el-input v-model="searchForm.province" placeholder="请输入省份" clearable style="width: 120px" />
        </el-form-item>
        <el-form-item label="城市" prop="city">
          <el-input v-model="searchForm.city" placeholder="请输入城市" clearable style="width: 120px" />
        </el-form-item>
        <el-form-item label="跟进状态" prop="follow_status">
          <el-select v-model="searchForm.follow_status" placeholder="请选择状态" clearable style="width: 140px">
            <el-option label="新增" value="new" />
            <el-option label="已联系" value="contacted" />
            <el-option label="已拜访" value="visited" />
            <el-option label="已签约" value="signed" />
            <el-option label="已放弃" value="abandoned" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch"><i-ep-search /> 搜索</el-button>
          <el-button @click="handleReset"><i-ep-refresh /> 重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">目标学校列表</span>
          <div class="operations">
            <el-button v-permission="['module_promotion:target_school:create']" type="primary" @click="handleCreate"><i-ep-plus /> 新增</el-button>
            <el-button v-permission="['module_promotion:target_school:delete']" type="danger" :disabled="!selectedIds.length" @click="handleBatchDelete"><i-ep-delete /> 批量删除</el-button>
          </div>
        </div>
      </template>

      <el-table v-loading="loading" :data="tableData" stripe border @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="school_no" label="学校编号" width="150" />
        <el-table-column prop="school_name" label="学校名称" min-width="180" show-overflow-tooltip>
          <template #default="{ row }">
            <el-link type="primary" @click="handleView(row)">{{ row.school_name || '-' }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="school_code" label="学校编码" width="120" />
        <el-table-column prop="school_level" label="学校级别" width="100">
          <template #default="{ row }">
            <el-tag>{{ getLevelLabel(row.school_level) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="province" label="省份" width="100" />
        <el-table-column prop="city" label="城市" width="100" />
        <el-table-column prop="contact_person" label="联系人" width="100" />
        <el-table-column prop="contact_phone" label="联系电话" width="130" />
        <el-table-column prop="follow_status" label="跟进状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.follow_status)">{{ getStatusLabel(row.follow_status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-permission="['module_promotion:target_school:detail']" link type="primary" @click="handleView(row)">详情</el-button>
            <el-button v-permission="['module_promotion:target_school:update']" link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button v-permission="['module_promotion:target_school:delete']" link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination v-model:current-page="pagination.page" v-model:page-size="pagination.pageSize" :total="pagination.total" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" @size-change="handleSizeChange" @current-change="handlePageChange" />
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailDialog.visible" title="目标学校详情" width="650px">
      <el-descriptions :column="2" border v-if="detailDialog.data">
        <el-descriptions-item label="学校编号">{{ detailDialog.data.school_no }}</el-descriptions-item>
        <el-descriptions-item label="学校级别">
          <el-tag>{{ getLevelLabel(detailDialog.data.school_level) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="学校名称" :span="2">{{ detailDialog.data.school_name }}</el-descriptions-item>
        <el-descriptions-item label="学校编码">{{ detailDialog.data.school_code || '-' }}</el-descriptions-item>
        <el-descriptions-item label="跟进状态">
          <el-tag :type="getStatusType(detailDialog.data.follow_status)">{{ getStatusLabel(detailDialog.data.follow_status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="省份">{{ detailDialog.data.province || '-' }}</el-descriptions-item>
        <el-descriptions-item label="城市">{{ detailDialog.data.city || '-' }}</el-descriptions-item>
        <el-descriptions-item label="区县">{{ detailDialog.data.district || '-' }}</el-descriptions-item>
        <el-descriptions-item label="详细地址" :span="2">{{ detailDialog.data.address || '-' }}</el-descriptions-item>
        <el-descriptions-item label="联系人">{{ detailDialog.data.contact_person || '-' }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ detailDialog.data.contact_phone || '-' }}</el-descriptions-item>
        <el-descriptions-item label="优先级别">{{ detailDialog.data.priority_level || '-' }}</el-descriptions-item>
        <el-descriptions-item label="学生数量">{{ detailDialog.data.student_count || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ detailDialog.data.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ detailDialog.data.created_time }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ detailDialog.data.updated_time }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="formDialog.visible" :title="formDialog.type === 'create' ? '新增目标学校' : '编辑目标学校'" width="600px">
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="学校名称" prop="school_name">
          <el-input v-model="form.school_name" placeholder="请输入学校名称" />
        </el-form-item>
        <el-form-item label="学校编码" prop="school_code">
          <el-input v-model="form.school_code" placeholder="请输入学校编码" />
        </el-form-item>
        <el-form-item label="学校级别" prop="school_level">
          <el-select v-model="form.school_level" placeholder="请选择学校级别" style="width: 100%">
            <el-option label="高中" value="high_school" />
            <el-option label="初中" value="middle_school" />
            <el-option label="完全中学" value="complete_school" />
            <el-option label="九年一贯制" value="nine_year" />
          </el-select>
        </el-form-item>
        <el-form-item label="省份" prop="province">
          <el-input v-model="form.province" placeholder="请输入省份" />
        </el-form-item>
        <el-form-item label="城市" prop="city">
          <el-input v-model="form.city" placeholder="请输入城市" />
        </el-form-item>
        <el-form-item label="区县" prop="district">
          <el-input v-model="form.district" placeholder="请输入区县" />
        </el-form-item>
        <el-form-item label="详细地址" prop="address">
          <el-input v-model="form.address" placeholder="请输入详细地址" />
        </el-form-item>
        <el-form-item label="联系人" prop="contact_person">
          <el-input v-model="form.contact_person" placeholder="请输入联系人" />
        </el-form-item>
        <el-form-item label="联系电话" prop="contact_phone">
          <el-input v-model="form.contact_phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="跟进状态" prop="follow_status">
          <el-select v-model="form.follow_status" placeholder="请选择跟进状态" style="width: 100%">
            <el-option label="新增" value="new" />
            <el-option label="已联系" value="contacted" />
            <el-option label="已拜访" value="visited" />
            <el-option label="已签约" value="signed" />
            <el-option label="已放弃" value="abandoned" />
          </el-select>
        </el-form-item>
        <el-form-item label="优先级别" prop="priority_level">
          <el-input-number v-model="form.priority_level" :min="1" :max="5" style="width: 100%" />
        </el-form-item>
        <el-form-item label="学生数量" prop="student_count">
          <el-input-number v-model="form.student_count" :min="0" style="width: 100%" />
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="form.remark" type="textarea" :rows="3" placeholder="请输入备注" />
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
import TargetSchoolAPI from "@/api/module_promotion/target_school";
import type { TargetSchoolItem, TargetSchoolForm, TargetSchoolQuery } from "@/api/module_promotion/target_school";

const loading = ref(false);
const tableData = ref<TargetSchoolItem[]>([]);
const selectedIds = ref<number[]>([]);

const searchFormRef = ref<FormInstance>();
const searchForm = reactive<TargetSchoolQuery>({
  school_name: "",
  school_code: "",
  school_level: "",
  province: "",
  city: "",
  follow_status: "",
});

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

const detailDialog = reactive({
  visible: false,
  data: null as TargetSchoolItem | null,
});

const formDialog = reactive({
  visible: false,
  type: "create" as "create" | "edit",
  id: null as number | null,
});

const formRef = ref<FormInstance>();
const form = reactive<TargetSchoolForm>({
  school_name: "",
  school_code: "",
  school_level: "high_school",
  province: "",
  city: "",
  district: "",
  address: "",
  contact_person: "",
  contact_phone: "",
  follow_status: "new",
  priority_level: 3,
  student_count: 0,
  remark: "",
});

const formRules: FormRules = {
  school_name: [{ required: true, message: "请输入学校名称", trigger: "blur" }],
  school_level: [{ required: true, message: "请选择学校级别", trigger: "change" }],
};

function getLevelLabel(level: string): string {
  const map: Record<string, string> = {
    high_school: "高中",
    middle_school: "初中",
    complete_school: "完全中学",
    nine_year: "九年一贯制",
  };
  return map[level] || level;
}

function getStatusLabel(status: string): string {
  const map: Record<string, string> = {
    new: "新增",
    contacted: "已联系",
    visited: "已拜访",
    signed: "已签约",
    abandoned: "已放弃",
  };
  return map[status] || status;
}

function getStatusType(status: string): string {
  const map: Record<string, string> = {
    new: "info",
    contacted: "warning",
    visited: "success",
    signed: "success",
    abandoned: "info",
  };
  return map[status] || "info";
}

async function fetchData() {
  loading.value = true;
  try {
    const params = {
      ...searchForm,
      page: pagination.page,
      pageSize: pagination.pageSize,
    };
    const res = await TargetSchoolAPI.getList(params);
    if (res.data.code === 0) {
      tableData.value = res.data.data.items || [];
      pagination.total = res.data.data.total || 0;
    } else {
      ElMessage.error(res.data.msg || "获取数据失败");
    }
  } finally {
    loading.value = false;
  }
}

function handleSearch() {
  pagination.page = 1;
  fetchData();
}

function handleReset() {
  searchFormRef.value?.resetFields();
  handleSearch();
}

function handleSizeChange() {
  pagination.page = 1;
  fetchData();
}

function handlePageChange() {
  fetchData();
}

function handleSelectionChange(selection: TargetSchoolItem[]) {
  selectedIds.value = selection.map((item) => item.id);
}

function handleCreate() {
  formDialog.type = "create";
  formDialog.id = null;
  Object.assign(form, {
    school_name: "",
    school_code: "",
    school_level: "high_school",
    province: "",
    city: "",
    district: "",
    address: "",
    contact_person: "",
    contact_phone: "",
    follow_status: "new",
    priority_level: 3,
    student_count: 0,
    remark: "",
  });
  formDialog.visible = true;
}

function handleEdit(row: TargetSchoolItem) {
  formDialog.type = "edit";
  formDialog.id = row.id;
  Object.assign(form, row);
  formDialog.visible = true;
}

async function handleView(row: TargetSchoolItem) {
  try {
    const res = await TargetSchoolAPI.getDetail(row.id);
    if (res.data.code === 0) {
      detailDialog.data = res.data.data;
      detailDialog.visible = true;
    } else {
      ElMessage.error(res.data.msg || "获取详情失败");
    }
  } catch {
    ElMessage.error("获取详情失败");
  }
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false);
  if (!valid) return;

  try {
    if (formDialog.type === "create") {
      const res = await TargetSchoolAPI.create(form);
      if (res.data.code === 0) {
        ElMessage.success("创建成功");
        formDialog.visible = false;
        fetchData();
      } else {
        ElMessage.error(res.data.msg || "创建失败");
      }
    } else {
      const res = await TargetSchoolAPI.update(formDialog.id!, form);
      if (res.data.code === 0) {
        ElMessage.success("更新成功");
        formDialog.visible = false;
        fetchData();
      } else {
        ElMessage.error(res.data.msg || "更新失败");
      }
    }
  } catch {
    ElMessage.error("操作失败");
  }
}

async function handleDelete(row: TargetSchoolItem) {
  try {
    await ElMessageBox.confirm("确定要删除该目标学校吗？", "提示", {
      type: "warning",
    });
    const res = await TargetSchoolAPI.delete(row.id);
    if (res.data.code === 0) {
      ElMessage.success("删除成功");
      fetchData();
    } else {
      ElMessage.error(res.data.msg || "删除失败");
    }
  } catch {
    // 用户取消
  }
}

async function handleBatchDelete() {
  if (!selectedIds.value.length) return;
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 个目标学校吗？`, "提示", {
      type: "warning",
    });
    const res = await TargetSchoolAPI.batchDelete(selectedIds.value);
    if (res.data.code === 0) {
      ElMessage.success("批量删除成功");
      selectedIds.value = [];
      fetchData();
    } else {
      ElMessage.error(res.data.msg || "批量删除失败");
    }
  } catch {
    // 用户取消
  }
}

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
.card-header .title {
  font-weight: 600;
}
.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}
</style>