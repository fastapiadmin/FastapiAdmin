<!-- 招生宣传活动 - 团队管理 -->
<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="80px">
        <el-form-item label="团队名称" prop="team_name">
          <el-input
            v-model="searchForm.team_name"
            placeholder="请输入团队名称"
            clearable
            style="width: 180px"
          />
        </el-form-item>
        <el-form-item label="团队编码" prop="team_code">
          <el-input
            v-model="searchForm.team_code"
            placeholder="请输入团队编码"
            clearable
            style="width: 150px"
          />
        </el-form-item>
        <el-form-item label="团队级别" prop="team_level">
          <el-select
            v-model="searchForm.team_level"
            placeholder="请选择级别"
            clearable
            style="width: 140px"
          >
            <el-option label="总部" value="headquarters" />
            <el-option label="大区" value="region" />
            <el-option label="省区" value="province" />
            <el-option label="市区" value="city" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="team_status">
          <el-select
            v-model="searchForm.team_status"
            placeholder="请选择状态"
            clearable
            style="width: 120px"
          >
            <el-option label="在用" value="active" />
            <el-option label="停用" value="inactive" />
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

    <el-card class="table-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">团队列表</span>
          <div class="operations">
            <el-button
              v-permission="['module_promotion:team:create']"
              type="primary"
              @click="handleCreate"
            >
              <i-ep-plus />
              新增
            </el-button>
            <el-button
              v-permission="['module_promotion:team:delete']"
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

      <el-table
        v-loading="loading"
        :data="tableData"
        stripe
        border
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="team_no" label="团队编号" width="150" />
        <el-table-column prop="team_name" label="团队名称" min-width="150" show-overflow-tooltip>
          <template #default="{ row }">
            <el-link type="primary" @click="handleView(row)">{{ row.team_name || "-" }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="team_code" label="团队编码" width="120" />
        <el-table-column prop="team_level" label="团队级别" width="100">
          <template #default="{ row }">
            <el-tag>{{ getLevelLabel(row.team_level) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="parent_name" label="上级团队" width="120" />
        <el-table-column prop="leader_name" label="负责人" width="100" />
        <el-table-column prop="member_count" label="成员数量" width="100" />
        <el-table-column prop="team_status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.team_status === 'active' ? 'success' : 'info'">
              {{ row.team_status === "active" ? "在用" : "停用" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button
              v-permission="['module_promotion:team:detail']"
              link
              type="primary"
              @click="handleView(row)"
            >
              详情
            </el-button>
            <el-button
              v-permission="['module_promotion:team:update']"
              link
              type="primary"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              v-permission="['module_promotion:team:delete']"
              link
              type="danger"
              @click="handleDelete(row)"
            >
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

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailDialog.visible" title="团队详情" width="600px">
      <el-descriptions v-if="detailDialog.data" :column="2" border>
        <el-descriptions-item label="团队编号">
          {{ detailDialog.data.team_no }}
        </el-descriptions-item>
        <el-descriptions-item label="团队状态">
          <el-tag :type="detailDialog.data.team_status === 'active' ? 'success' : 'info'">
            {{ detailDialog.data.team_status === "active" ? "在用" : "停用" }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="团队名称" :span="2">
          {{ detailDialog.data.team_name }}
        </el-descriptions-item>
        <el-descriptions-item label="团队编码">
          {{ detailDialog.data.team_code || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="团队级别">
          <el-tag>{{ getLevelLabel(detailDialog.data.team_level) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="上级团队">
          {{ detailDialog.data.parent_name || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="负责人">
          {{ detailDialog.data.leader_name || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="联系电话">
          {{ detailDialog.data.leader_phone || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="成员数量">
          {{ detailDialog.data.member_count || 0 }}
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">
          {{ detailDialog.data.remark || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">
          {{ detailDialog.data.created_time }}
        </el-descriptions-item>
        <el-descriptions-item label="更新时间">
          {{ detailDialog.data.updated_time }}
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 新增/编辑弹窗 -->
    <el-dialog
      v-model="formDialog.visible"
      :title="formDialog.type === 'create' ? '新增团队' : '编辑团队'"
      width="550px"
    >
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="团队名称" prop="team_name">
          <el-input v-model="form.team_name" placeholder="请输入团队名称" />
        </el-form-item>
        <el-form-item label="团队编码" prop="team_code">
          <el-input v-model="form.team_code" placeholder="请输入团队编码" />
        </el-form-item>
        <el-form-item label="团队级别" prop="team_level">
          <el-select v-model="form.team_level" placeholder="请选择团队级别" style="width: 100%">
            <el-option label="总部" value="headquarters" />
            <el-option label="大区" value="region" />
            <el-option label="省区" value="province" />
            <el-option label="市区" value="city" />
          </el-select>
        </el-form-item>
        <el-form-item label="上级团队" prop="parent_id">
          <el-input-number
            v-model="form.parent_id"
            :min="0"
            placeholder="上级团队ID"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="负责人" prop="leader_name">
          <el-input v-model="form.leader_name" placeholder="请输入负责人姓名" />
        </el-form-item>
        <el-form-item label="联系电话" prop="leader_phone">
          <el-input v-model="form.leader_phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="成员数量" prop="member_count">
          <el-input-number v-model="form.member_count" :min="0" style="width: 100%" />
        </el-form-item>
        <el-form-item label="状态" prop="team_status">
          <el-radio-group v-model="form.team_status">
            <el-radio value="active">在用</el-radio>
            <el-radio value="inactive">停用</el-radio>
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
import TeamAPI from "@/api/module_promotion/team";
import type { TeamItem, TeamForm, TeamQuery } from "@/api/module_promotion/team";

const loading = ref(false);
const tableData = ref<TeamItem[]>([]);
const selectedIds = ref<number[]>([]);

const searchFormRef = ref<FormInstance>();
const searchForm = reactive<TeamQuery>({
  team_name: "",
  team_code: "",
  team_level: "",
  team_status: "",
});

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

const detailDialog = reactive({
  visible: false,
  data: null as TeamItem | null,
});

const formDialog = reactive({
  visible: false,
  type: "create" as "create" | "edit",
  id: null as number | null,
});

const formRef = ref<FormInstance>();
const form = reactive<TeamForm>({
  team_name: "",
  team_code: "",
  team_level: "city",
  parent_id: undefined,
  parent_name: "",
  leader_name: "",
  leader_phone: "",
  member_count: undefined,
  team_status: "active",
  remark: "",
});

const formRules: FormRules = {
  team_name: [{ required: true, message: "请输入团队名称", trigger: "blur" }],
  team_level: [{ required: true, message: "请选择团队级别", trigger: "change" }],
};

function getLevelLabel(level: string): string {
  const map: Record<string, string> = {
    headquarters: "总部",
    region: "大区",
    province: "省区",
    city: "市区",
  };
  return map[level] || level;
}

async function fetchData() {
  loading.value = true;
  try {
    const params = {
      ...searchForm,
      page: pagination.page,
      pageSize: pagination.pageSize,
    };
    const res = await TeamAPI.getList(params);
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

function handleSelectionChange(selection: TeamItem[]) {
  selectedIds.value = selection.map((item) => item.id);
}

function handleCreate() {
  formDialog.type = "create";
  formDialog.id = null;
  Object.assign(form, {
    team_name: "",
    team_code: "",
    team_level: "city",
    parent_id: undefined,
    parent_name: "",
    leader_name: "",
    leader_phone: "",
    member_count: undefined,
    team_status: "active",
    remark: "",
  });
  formDialog.visible = true;
}

function handleEdit(row: TeamItem) {
  formDialog.type = "edit";
  formDialog.id = row.id;
  Object.assign(form, row);
  formDialog.visible = true;
}

async function handleView(row: TeamItem) {
  try {
    const res = await TeamAPI.getDetail(row.id);
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
      const res = await TeamAPI.create(form);
      if (res.data.code === 0) {
        ElMessage.success("创建成功");
        formDialog.visible = false;
        fetchData();
      } else {
        ElMessage.error(res.data.msg || "创建失败");
      }
    } else {
      const res = await TeamAPI.update(formDialog.id!, form);
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

async function handleDelete(row: TeamItem) {
  try {
    await ElMessageBox.confirm("确定要删除该团队吗？", "提示", {
      type: "warning",
    });
    const res = await TeamAPI.delete(row.id);
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
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 个团队吗？`, "提示", {
      type: "warning",
    });
    const res = await TeamAPI.batchDelete(selectedIds.value);
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
