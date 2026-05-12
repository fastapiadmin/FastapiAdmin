<!-- 招生咨询会 - 报名管理 -->
<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="80px">
        <el-form-item label="咨询会ID" prop="consultation_id">
          <el-input-number v-model="searchForm.consultation_id" :min="1" style="width: 120px" />
        </el-form-item>
        <el-form-item label="高校ID" prop="university_id">
          <el-input-number v-model="searchForm.university_id" :min="1" style="width: 120px" />
        </el-form-item>
        <el-form-item label="高校名称" prop="university_name">
          <el-input
            v-model="searchForm.university_name"
            placeholder="请输入高校名称"
            clearable
            style="width: 150px"
          />
        </el-form-item>
        <el-form-item label="联系人" prop="contact_person">
          <el-input
            v-model="searchForm.contact_person"
            placeholder="请输入联系人"
            clearable
            style="width: 120px"
          />
        </el-form-item>
        <el-form-item label="报名状态" prop="registration_status">
          <el-select
            v-model="searchForm.registration_status"
            placeholder="请选择状态"
            clearable
            style="width: 120px"
          >
            <el-option label="待审核" value="pending" />
            <el-option label="已通过" value="approved" />
            <el-option label="已拒绝" value="rejected" />
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
          <span class="title">报名记录列表</span>
          <div class="operations">
            <el-button
              v-permission="['module_consultation:registration:create']"
              type="primary"
              @click="handleCreate"
            >
              <i-ep-plus />
              新增
            </el-button>
            <el-button
              v-permission="['module_consultation:registration:one_click_register']"
              type="success"
              :disabled="!selectedIds.length"
              @click="handleOneClickRegister"
            >
              <i-ep-position />
              一键报名
            </el-button>
            <el-button
              v-permission="['module_consultation:registration:forward_to_team']"
              type="warning"
              :disabled="!selectedIds.length"
              @click="handleForwardToTeam"
            >
              <i-ep-promotion />
              转发招生组
            </el-button>
            <el-button
              v-permission="['module_consultation:registration:delete']"
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
        <el-table-column prop="consultation_id" label="咨询会ID" width="100" />
        <el-table-column prop="university_id" label="高校ID" width="100" />
        <el-table-column
          prop="university_name"
          label="高校名称"
          min-width="150"
          show-overflow-tooltip
        />
        <el-table-column prop="contact_person" label="联系人" width="100" />
        <el-table-column prop="contact_phone" label="联系电话" width="130" />
        <el-table-column prop="booth_number" label="展位号" width="100" />
        <el-table-column prop="booth_size" label="展位大小" width="100" />
        <el-table-column prop="registration_status" label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.registration_status)">
              {{ getStatusLabel(row.registration_status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_registered" label="已报名" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_registered ? 'success' : 'info'" size="small">
              {{ row.is_registered ? "是" : "否" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="registration_email"
          label="报名邮箱"
          width="180"
          show-overflow-tooltip
        />
        <el-table-column prop="registration_time" label="报名时间" width="160" />
        <el-table-column label="操作" width="260" fixed="right">
          <template #default="{ row }">
            <el-button
              v-permission="['module_consultation:registration:detail']"
              link
              type="primary"
              @click="handleView(row)"
            >
              详情
            </el-button>
            <el-button
              v-if="row.registration_status === 'pending'"
              v-permission="['module_consultation:registration:approve']"
              link
              type="success"
              @click="handleApprove(row)"
            >
              通过
            </el-button>
            <el-button
              v-if="row.registration_status === 'pending'"
              v-permission="['module_consultation:registration:approve']"
              link
              type="danger"
              @click="handleReject(row)"
            >
              拒绝
            </el-button>
            <el-button
              v-permission="['module_consultation:registration:one_click_register']"
              link
              type="success"
              :disabled="row.is_registered"
              @click="handleOneClickRegisterSingle(row)"
            >
              一键报名
            </el-button>
            <el-button
              v-permission="['module_consultation:registration:forward_to_team']"
              link
              type="warning"
              @click="handleForwardToTeamSingle(row)"
            >
              转发
            </el-button>
            <el-button
              v-permission="['module_consultation:registration:delete']"
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
    <el-dialog v-model="detailDialog.visible" title="报名详情" width="600px">
      <el-descriptions v-if="detailDialog.data" :column="2" border>
        <el-descriptions-item label="咨询会ID">
          {{ detailDialog.data.consultation_id }}
        </el-descriptions-item>
        <el-descriptions-item label="高校ID">
          {{ detailDialog.data.university_id }}
        </el-descriptions-item>
        <el-descriptions-item label="高校名称" :span="2">
          {{ detailDialog.data.university_name }}
        </el-descriptions-item>
        <el-descriptions-item label="联系人">
          {{ detailDialog.data.contact_person }}
        </el-descriptions-item>
        <el-descriptions-item label="联系电话">
          {{ detailDialog.data.contact_phone }}
        </el-descriptions-item>
        <el-descriptions-item label="联系邮箱">
          {{ detailDialog.data.contact_email }}
        </el-descriptions-item>
        <el-descriptions-item label="展位号">
          {{ detailDialog.data.booth_number || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="展位大小">
          {{ detailDialog.data.booth_size || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="报名状态">
          <el-tag :type="getStatusType(detailDialog.data.registration_status)">
            {{ getStatusLabel(detailDialog.data.registration_status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="报名时间">
          {{ detailDialog.data.registration_time || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="审核时间">
          {{ detailDialog.data.approval_time || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="审核意见" :span="2">
          {{ detailDialog.data.approval_comment || "-" }}
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 新增/编辑弹窗 -->
    <el-dialog
      v-model="formDialog.visible"
      :title="formDialog.type === 'create' ? '新增报名' : '编辑报名'"
      width="550px"
    >
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="咨询会" prop="consultation_id">
          <el-select
            v-model="form.consultation_id"
            placeholder="请选择咨询会"
            filterable
            clearable
            style="width: 100%"
          >
            <el-option
              v-for="item in consultationOptions"
              :key="item.id"
              :label="`${item.title} (${item.start_date}${item.city ? ' - ' + item.city : ''})`"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="高校" prop="university_id">
          <el-select
            v-model="form.university_id"
            placeholder="请选择高校"
            filterable
            clearable
            style="width: 100%"
            @change="handleUniversityChange"
          >
            <el-option
              v-for="item in universityOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="高校名称" prop="university_name">
          <el-input v-model="form.university_name" placeholder="请输入高校名称" readonly />
        </el-form-item>
        <el-form-item label="联系人" prop="contact_person">
          <el-input v-model="form.contact_person" placeholder="请输入联系人" />
        </el-form-item>
        <el-form-item label="联系电话" prop="contact_phone">
          <el-input v-model="form.contact_phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="联系邮箱" prop="contact_email">
          <el-input v-model="form.contact_email" :min="1" placeholder="请输入联系邮箱" />
        </el-form-item>
        <el-form-item label="展位号" prop="booth_number">
          <el-input v-model="form.booth_number" placeholder="请输入展位号" />
        </el-form-item>
        <el-form-item label="展位大小" prop="booth_size">
          <el-input v-model="form.booth_size" placeholder="请输入展位大小" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="formDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 审核弹窗 -->
    <el-dialog v-model="approveDialog.visible" title="审核通过" width="500px">
      <el-form ref="approveFormRef" :model="approveForm" label-width="100px">
        <el-form-item label="展位号" prop="booth_number">
          <el-input v-model="approveForm.booth_number" placeholder="请输入展位号" />
        </el-form-item>
        <el-form-item label="展位大小" prop="booth_size">
          <el-input v-model="approveForm.booth_size" placeholder="请输入展位大小" />
        </el-form-item>
        <el-form-item label="审核意见" prop="comment">
          <el-input
            v-model="approveForm.comment"
            type="textarea"
            :rows="3"
            placeholder="请输入审核意见"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="approveDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleApproveSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 拒绝弹窗 -->
    <el-dialog v-model="rejectDialog.visible" title="审核拒绝" width="500px">
      <el-form ref="rejectFormRef" :model="rejectForm" label-width="100px">
        <el-form-item label="拒绝原因" prop="comment">
          <el-input
            v-model="rejectForm.comment"
            type="textarea"
            :rows="3"
            placeholder="请输入拒绝原因"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="rejectDialog.visible = false">取消</el-button>
        <el-button type="danger" @click="handleRejectSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 一键报名结果弹窗 -->
    <el-dialog v-model="oneClickResultDialog.visible" title="一键报名" width="500px">
      <el-result
        :icon="oneClickResultDialog.success ? 'success' : 'error'"
        :title="oneClickResultDialog.success ? '报名成功' : '报名失败'"
        :sub-title="oneClickResultDialog.message"
      />
      <template #footer>
        <el-button type="primary" @click="oneClickResultDialog.visible = false">确定</el-button>
      </template>
    </el-dialog>

    <!-- 转发至招生组弹窗 -->
    <el-dialog v-model="forwardDialog.visible" title="转发至招生组" width="500px">
      <el-form ref="forwardFormRef" :model="forwardForm" label-width="100px">
        <el-form-item label="组长ID" prop="team_leader_id">
          <el-input-number
            v-model="forwardForm.team_leader_id"
            :min="1"
            placeholder="请输入组长ID"
            style="width: 200px"
          />
        </el-form-item>
        <el-form-item label="成员IDs" prop="assignee_ids">
          <el-select
            v-model="forwardForm.assignee_ids"
            multiple
            placeholder="请选择成员"
            style="width: 300px"
          >
            <el-option label="成员1" :value="1" />
            <el-option label="成员2" :value="2" />
            <el-option label="成员3" :value="3" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="forwardDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleForwardSubmit">确定转发</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";
import RegistrationAPI from "@/api/module_consultation/registration";
import ConsultationInfoAPI from "@/api/module_consultation/consultation";
import UniversityAPI from "@/api/module_consultation/university";
import type { RegistrationItem, RegistrationQuery } from "@/api/module_consultation/registration";
import type { ConsultationOption } from "@/api/module_consultation/consultation";
import type { UniversityOption } from "@/api/module_consultation/university";

const searchForm = reactive<RegistrationQuery>({
  consultation_id: undefined,
  university_id: undefined,
  university_name: undefined,
  contact_person: undefined,
  contact_phone: undefined,
  registration_status: undefined,
});

const loading = ref(false);
const tableData = ref<RegistrationItem[]>([]);
const selectedIds = ref<number[]>([]);
const pagination = reactive({ page: 1, pageSize: 10, total: 0 });

// 下拉选项数据
const consultationOptions = ref<ConsultationOption[]>([]);
const universityOptions = ref<UniversityOption[]>([]);

const formDialog = reactive({
  visible: false,
  type: "create" as "create" | "edit",
  data: undefined as RegistrationItem | undefined,
});
const detailDialog = reactive({ visible: false, data: undefined as RegistrationItem | undefined });
const approveDialog = reactive({ visible: false, id: 0 as number });
const rejectDialog = reactive({ visible: false, id: 0 as number });
const oneClickResultDialog = reactive({ visible: false, success: false, message: "" });
const forwardDialog = reactive({ visible: false, id: 0 as number });
const forwardForm = reactive({
  team_leader_id: undefined as number | undefined,
  assignee_ids: [] as number[],
});

const formRef = ref<FormInstance>();
const approveFormRef = ref<FormInstance>();
const rejectFormRef = ref<FormInstance>();
const forwardFormRef = ref<FormInstance>();

const form = reactive<any>({
  consultation_id: undefined,
  university_id: undefined,
  university_name: "",
  contact_person: "",
  contact_phone: "",
  contact_email: "",
  booth_number: "",
  booth_size: "",
});

const approveForm = reactive({ booth_number: "", booth_size: "", comment: "" });
const rejectForm = reactive({ comment: "" });

const formRules: FormRules = {
  consultation_id: [{ required: true, message: "请输入咨询会ID", trigger: "blur" }],
  university_id: [{ required: true, message: "请输入高校ID", trigger: "blur" }],
  contact_email: [{ required: true, message: "请输入联系邮箱", trigger: "blur" }],
};

const fetchList = async () => {
  loading.value = true;
  try {
    const params = { page_no: pagination.page, page_size: pagination.pageSize, ...searchForm };
    const res = await RegistrationAPI.getList(params);
    if (res.data?.data) {
      tableData.value = res.data.data.items || [];
      pagination.total = res.data.data.total || 0;
    }
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  pagination.page = 1;
  fetchList();
};
const handleReset = () => {
  Object.assign(searchForm, {
    consultation_id: undefined,
    university_id: undefined,
    university_name: undefined,
    contact_person: undefined,
    contact_phone: undefined,
    registration_status: undefined,
  });
  handleSearch();
};
const handleSelectionChange = (selection: RegistrationItem[]) => {
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

const getStatusType = (status: string): "info" | "success" | "danger" | "warning" => {
  if (status === "pending") return "info";
  if (status === "approved") return "success";
  if (status === "rejected") return "danger";
  return "info";
};
const getStatusLabel = (status: string) => {
  if (status === "pending") return "待审核";
  if (status === "approved") return "已通过";
  if (status === "rejected") return "已拒绝";
  return status;
};

const handleCreate = async () => {
  formDialog.type = "create";
  Object.assign(form, {
    consultation_id: undefined,
    university_id: undefined,
    university_name: "",
    contact_person: "",
    contact_phone: "",
    contact_email: "",
    booth_number: "",
    booth_size: "",
  });
  // 加载下拉选项
  await loadOptions();
  formDialog.visible = true;
};

// 加载下拉选项
const loadOptions = async () => {
  try {
    // 加载已审核咨询会列表
    const consultationRes = await ConsultationInfoAPI.getApprovedOptions();
    if (consultationRes.data?.data) {
      consultationOptions.value = consultationRes.data.data;
    }
    // 加载高校列表
    const universityRes = await UniversityAPI.getOptions();
    if (universityRes.data?.data) {
      universityOptions.value = universityRes.data.data;
    }
  } catch (error) {
    console.error("加载下拉选项失败:", error);
  }
};

// 高校选择变化处理
const handleUniversityChange = (universityId: number) => {
  const selected = universityOptions.value.find((item) => item.id === universityId);
  if (selected) {
    form.university_name = selected.name;
  } else {
    form.university_name = "";
  }
};

const handleView = (row: RegistrationItem) => {
  detailDialog.data = row;
  detailDialog.visible = true;
};

const handleSubmit = async () => {
  if (!formRef.value) return;
  await formRef.value.validate(async (valid) => {
    if (valid) {
      if (formDialog.type === "create") {
        await RegistrationAPI.create(form);
        ElMessage.success("创建成功");
      } else {
        await RegistrationAPI.update(formDialog.data!.id!, form);
        ElMessage.success("更新成功");
      }
      formDialog.visible = false;
      fetchList();
    }
  });
};

const handleApprove = (row: RegistrationItem) => {
  approveDialog.id = row.id!;
  Object.assign(approveForm, {
    booth_number: row.booth_number || "",
    booth_size: row.booth_size || "",
    comment: "",
  });
  approveDialog.visible = true;
};

const handleApproveSubmit = async () => {
  await RegistrationAPI.approve(approveDialog.id, approveForm);
  ElMessage.success("审核通过");
  approveDialog.visible = false;
  fetchList();
};

const handleReject = (row: RegistrationItem) => {
  rejectDialog.id = row.id!;
  Object.assign(rejectForm, { comment: "" });
  rejectDialog.visible = true;
};

const handleRejectSubmit = async () => {
  await RegistrationAPI.reject(rejectDialog.id, rejectForm);
  ElMessage.success("审核拒绝");
  rejectDialog.visible = false;
  fetchList();
};

const handleDelete = (row: RegistrationItem) => {
  ElMessageBox.confirm(`确定要删除这条报名记录吗？`, "删除确认", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await RegistrationAPI.delete(row.id!);
      ElMessage.success("删除成功");
      fetchList();
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
      await RegistrationAPI.batchDelete(selectedIds.value);
      ElMessage.success("批量删除成功");
      fetchList();
    })
    .catch(() => {});
};

// 一键报名 - 批量
const handleOneClickRegister = () => {
  if (!selectedIds.value.length) {
    ElMessage.warning("请选择要一键报名的记录");
    return;
  }
  if (selectedIds.value.length > 1) {
    ElMessage.warning("一键报名只能选择一条记录");
    return;
  }
  handleOneClickRegisterSingle(tableData.value.find((item) => item.id === selectedIds.value[0])!);
};

// 一键报名 - 单条
const handleOneClickRegisterSingle = async (row: RegistrationItem) => {
  try {
    ElMessageBox.confirm(`确定要对「${row.university_name}」进行一键报名吗？`, "一键报名确认", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "info",
    })
      .then(async () => {
        const res = await RegistrationAPI.oneClickRegister(row.id!);
        if (res.data?.success !== false) {
          oneClickResultDialog.success = true;
          oneClickResultDialog.message = `已成功向${row.university_name}发送报名回执邮件`;
          oneClickResultDialog.visible = true;
          fetchList();
        } else {
          oneClickResultDialog.success = false;
          oneClickResultDialog.message = res.data?.msg || "报名失败";
          oneClickResultDialog.visible = true;
        }
      })
      .catch(() => {});
  } catch (error: any) {
    oneClickResultDialog.success = false;
    oneClickResultDialog.message = error?.message || "一键报名失败";
    oneClickResultDialog.visible = true;
  }
};

// 转发至招生组 - 批量
const handleForwardToTeam = () => {
  if (!selectedIds.value.length) {
    ElMessage.warning("请选择要转发的记录");
    return;
  }
  if (selectedIds.value.length > 1) {
    ElMessage.warning("转发只能选择一条记录");
    return;
  }
  handleForwardToTeamSingle(tableData.value.find((item) => item.id === selectedIds.value[0])!);
};

// 转发至招生组 - 单条
const handleForwardToTeamSingle = (row: RegistrationItem) => {
  forwardDialog.id = row.id!;
  forwardForm.team_leader_id = undefined;
  forwardForm.assignee_ids = [];
  forwardDialog.visible = true;
};

// 转发提交
const handleForwardSubmit = async () => {
  try {
    await RegistrationAPI.forwardToTeam(forwardDialog.id, {
      team_leader_id: forwardForm.team_leader_id,
      assignee_ids: forwardForm.assignee_ids,
    });
    ElMessage.success("转发成功");
    forwardDialog.visible = false;
    fetchList();
  } catch {
    ElMessage.error("转发失败");
  }
};

onMounted(() => {
  fetchList();
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
</style>
