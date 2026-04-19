<!-- 招生宣传活动 - 人员管理 -->
<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="80px">
        <el-form-item label="人员姓名" prop="personnel_name">
          <el-input v-model="searchForm.personnel_name" placeholder="请输入人员姓名" clearable style="width: 150px" />
        </el-form-item>
        <el-form-item label="人员编号" prop="personnel_code">
          <el-input v-model="searchForm.personnel_code" placeholder="请输入人员编号" clearable style="width: 140px" />
        </el-form-item>
        <el-form-item label="人员类型" prop="personnel_type">
          <el-select v-model="searchForm.personnel_type" placeholder="请选择类型" clearable style="width: 140px">
            <el-option label="招聘" value="recruit" />
            <el-option label="邀请" value="invite" />
            <el-option label="手动添加" value="manual" />
          </el-select>
        </el-form-item>
        <el-form-item label="招生组ID" prop="team_id">
          <el-input-number v-model="searchForm.team_id" :min="1" style="width: 120px" />
        </el-form-item>
        <el-form-item label="状态" prop="personnel_status">
          <el-select v-model="searchForm.personnel_status" placeholder="请选择状态" clearable style="width: 120px">
            <el-option label="在岗" value="active" />
            <el-option label="离岗" value="inactive" />
            <el-option label="待审核" value="pending" />
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
          <span class="title">人员列表</span>
          <div class="operations">
            <el-button v-permission="['module_promotion:personnel:create']" type="primary" @click="handleCreate"><i-ep-plus /> 新增</el-button>
            <el-button v-permission="['module_promotion:personnel:delete']" type="danger" :disabled="!selectedIds.length" @click="handleBatchDelete"><i-ep-delete /> 批量删除</el-button>
          </div>
        </div>
      </template>

      <el-table v-loading="loading" :data="tableData" stripe border @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="personnel_no" label="人员编号" width="150" />
        <el-table-column prop="personnel_name" label="姓名" min-width="100" show-overflow-tooltip>
          <template #default="{ row }">
            <el-link type="primary" @click="handleView(row)">{{ row.personnel_name || '-' }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="personnel_code" label="编号" width="120" />
        <el-table-column prop="personnel_type" label="类型" width="100">
          <template #default="{ row }">
            <el-tag>{{ getTypeLabel(row.personnel_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="team_name" label="所属团队" width="120" />
        <el-table-column prop="phone" label="联系电话" width="130" />
        <el-table-column prop="email" label="邮箱" width="180" show-overflow-tooltip />
        <el-table-column prop="join_date" label="加入日期" width="110" />
        <el-table-column prop="personnel_status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.personnel_status)">{{ getStatusLabel(row.personnel_status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-permission="['module_promotion:personnel:detail']" link type="primary" @click="handleView(row)">详情</el-button>
            <el-button v-permission="['module_promotion:personnel:update']" link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button v-permission="['module_promotion:personnel:delete']" link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination v-model:current-page="pagination.page" v-model:page-size="pagination.pageSize" :total="pagination.total" :page-sizes="[10, 20, 50, 100]" layout="total, sizes, prev, pager, next, jumper" @size-change="handleSizeChange" @current-change="handlePageChange" />
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailDialog.visible" title="人员详情" width="600px">
      <el-descriptions :column="2" border v-if="detailDialog.data">
        <el-descriptions-item label="人员编号">{{ detailDialog.data.personnel_no }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(detailDialog.data.personnel_status)">{{ getStatusLabel(detailDialog.data.personnel_status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="姓名" :span="2">{{ detailDialog.data.personnel_name }}</el-descriptions-item>
        <el-descriptions-item label="人员编号">{{ detailDialog.data.personnel_code || '-' }}</el-descriptions-item>
        <el-descriptions-item label="人员类型">
          <el-tag>{{ getTypeLabel(detailDialog.data.personnel_type) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="所属团队">{{ detailDialog.data.team_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="身份证号">{{ detailDialog.data.id_card || '-' }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ detailDialog.data.phone || '-' }}</el-descriptions-item>
        <el-descriptions-item label="邮箱" :span="2">{{ detailDialog.data.email || '-' }}</el-descriptions-item>
        <el-descriptions-item label="加入日期">{{ detailDialog.data.join_date || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ detailDialog.data.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ detailDialog.data.created_time }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ detailDialog.data.updated_time }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="formDialog.visible" :title="formDialog.type === 'create' ? '新增人员' : '编辑人员'" width="550px">
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="姓名" prop="personnel_name">
          <el-input v-model="form.personnel_name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="人员编号" prop="personnel_code">
          <el-input v-model="form.personnel_code" placeholder="请输入人员编号" />
        </el-form-item>
        <el-form-item label="人员类型" prop="personnel_type">
          <el-select v-model="form.personnel_type" placeholder="请选择人员类型" style="width: 100%">
            <el-option label="招聘" value="recruit" />
            <el-option label="邀请" value="invite" />
            <el-option label="手动添加" value="manual" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属团队" prop="team_id">
          <el-input-number v-model="form.team_id" :min="0" placeholder="团队ID" style="width: 100%" />
        </el-form-item>
        <el-form-item label="身份证号" prop="id_card">
          <el-input v-model="form.id_card" placeholder="请输入身份证号" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="加入日期" prop="join_date">
          <el-date-picker v-model="form.join_date" type="date" placeholder="选择加入日期" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="状态" prop="personnel_status">
          <el-radio-group v-model="form.personnel_status">
            <el-radio value="active">在岗</el-radio>
            <el-radio value="inactive">离岗</el-radio>
            <el-radio value="pending">待审核</el-radio>
          </el-radio-group>
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
import PersonnelAPI from "@/api/module_promotion/personnel";
import type { PersonnelItem, PersonnelForm, PersonnelQuery } from "@/api/module_promotion/personnel";

const loading = ref(false);
const tableData = ref<PersonnelItem[]>([]);
const selectedIds = ref<number[]>([]);

const searchFormRef = ref<FormInstance>();
const searchForm = reactive<PersonnelQuery>({
  personnel_name: "",
  personnel_code: "",
  personnel_type: "",
  team_id: undefined,
  team_name: "",
  personnel_status: "",
});

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

const detailDialog = reactive({
  visible: false,
  data: null as PersonnelItem | null,
});

const formDialog = reactive({
  visible: false,
  type: "create" as "create" | "edit",
  id: null as number | null,
});

const formRef = ref<FormInstance>();
const form = reactive<PersonnelForm>({
  personnel_name: "",
  personnel_code: "",
  personnel_type: "manual",
  team_id: undefined,
  team_name: "",
  id_card: "",
  phone: "",
  email: "",
  join_date: "",
  personnel_status: "active",
  remark: "",
});

const formRules: FormRules = {
  personnel_name: [{ required: true, message: "请输入姓名", trigger: "blur" }],
  personnel_type: [{ required: true, message: "请选择人员类型", trigger: "change" }],
};

function getTypeLabel(type: string): string {
  const map: Record<string, string> = {
    recruit: "招聘",
    invite: "邀请",
    manual: "手动添加",
  };
  return map[type] || type;
}

function getStatusLabel(status: string): string {
  const map: Record<string, string> = {
    active: "在岗",
    inactive: "离岗",
    invited: "已邀请",
    pending: "待审核",
  };
  return map[status] || status;
}

function getStatusType(status: string): string {
  const map: Record<string, string> = {
    active: "success",
    inactive: "info",
    pending: "warning",
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
    const res = await PersonnelAPI.getList(params);
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

function handleSelectionChange(selection: PersonnelItem[]) {
  selectedIds.value = selection.map((item) => item.id);
}

function handleCreate() {
  formDialog.type = "create";
  formDialog.id = null;
  Object.assign(form, {
    personnel_name: "",
    personnel_code: "",
    personnel_type: "manual",
    team_id: undefined,
    team_name: "",
    id_card: "",
    phone: "",
    email: "",
    join_date: "",
    personnel_status: "active",
    remark: "",
  });
  formDialog.visible = true;
}

function handleEdit(row: PersonnelItem) {
  formDialog.type = "edit";
  formDialog.id = row.id;
  Object.assign(form, row);
  formDialog.visible = true;
}

async function handleView(row: PersonnelItem) {
  try {
    const res = await PersonnelAPI.getDetail(row.id);
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
      const res = await PersonnelAPI.create(form);
      if (res.data.code === 0) {
        ElMessage.success("创建成功");
        formDialog.visible = false;
        fetchData();
      } else {
        ElMessage.error(res.data.msg || "创建失败");
      }
    } else {
      const res = await PersonnelAPI.update(formDialog.id!, form);
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

async function handleDelete(row: PersonnelItem) {
  try {
    await ElMessageBox.confirm("确定要删除该人员吗？", "提示", {
      type: "warning",
    });
    const res = await PersonnelAPI.delete(row.id);
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
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 个人员吗？`, "提示", {
      type: "warning",
    });
    const res = await PersonnelAPI.batchDelete(selectedIds.value);
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