<!-- 招生咨询会 - 报名管理 -->
<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="80px">
        <el-form-item label="咨询会ID" prop="consultation_id">
          <el-input v-model="searchForm.consultation_id" placeholder="请输入咨询会ID" clearable style="width: 150px" />
        </el-form-item>
        <el-form-item label="高校名称" prop="university_name">
          <el-input v-model="searchForm.university_name" placeholder="请输入高校名称" clearable style="width: 150px" />
        </el-form-item>
        <el-form-item label="联系人" prop="contact_person">
          <el-input v-model="searchForm.contact_person" placeholder="请输入联系人" clearable style="width: 150px" />
        </el-form-item>
        <el-form-item label="联系电话" prop="contact_phone">
          <el-input v-model="searchForm.contact_phone" placeholder="请输入联系电话" clearable style="width: 150px" />
        </el-form-item>
        <el-form-item label="报名状态" prop="registration_status">
          <el-select v-model="searchForm.registration_status" placeholder="请选择状态" clearable style="width: 150px">
            <el-option label="待审核" value="pending" />
            <el-option label="已通过" value="approved" />
            <el-option label="已拒绝" value="rejected" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <i-ep-search /> 搜索
          </el-button>
          <el-button @click="handleReset">
            <i-ep-refresh /> 重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">报名记录列表</span>
          <div class="operations">
            <el-button v-permission="['module_consultation:registration:create']" type="primary" @click="handleCreate">
              <i-ep-plus /> 新增
            </el-button>
            <el-button v-permission="['module_consultation:registration:delete']" type="danger" :disabled="!selectedIds.length" @click="handleBatchDelete">
              <i-ep-delete /> 批量删除
            </el-button>
          </div>
        </div>
      </template>

      <el-table v-loading="loading" :data="tableData" stripe border @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="consultation_id" label="咨询会ID" width="100" />
        <el-table-column prop="university_name" label="高校名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="contact_person" label="联系人" width="100" />
        <el-table-column prop="contact_phone" label="联系电话" width="130" />
        <el-table-column prop="booth_size" label="展位大小" width="100" />
        <el-table-column prop="booth_fee" label="展位费用" width="100" align="center">
          <template #default="{ row }">
            {{ row.booth_fee !== null ? `¥${row.booth_fee}` : '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="registration_status" label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.registration_status)">
              {{ getStatusLabel(row.registration_status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_paid" label="已支付" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_paid ? 'success' : 'info'">{{ row.is_paid ? '是' : '否' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="registration_time" label="报名时间" width="160" />
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button v-permission="['module_consultation:registration:detail']" link type="primary" @click="handleView(row)">详情</el-button>
            <el-button v-if="row.registration_status === 'pending'" v-permission="['module_consultation:registration:approve']" link type="success" @click="handleApprove(row)">通过</el-button>
            <el-button v-if="row.registration_status === 'pending'" v-permission="['module_consultation:registration:approve']" link type="danger" @click="handleReject(row)">拒绝</el-button>
            <el-button v-if="row.registration_status === 'approved' && !row.is_paid" v-permission="['module_consultation:registration:update']" link type="warning" @click="handleConfirmPayment(row)">确认支付</el-button>
            <el-button v-permission="['module_consultation:registration:delete']" link type="danger" @click="handleDelete(row)">删除</el-button>
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
      <el-descriptions :column="2" border>
        <el-descriptions-item label="咨询会ID">{{ detailDialog.data?.consultation_id }}</el-descriptions-item>
        <el-descriptions-item label="高校名称">{{ detailDialog.data?.university_name }}</el-descriptions-item>
        <el-descriptions-item label="联系人">{{ detailDialog.data?.contact_person }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ detailDialog.data?.contact_phone }}</el-descriptions-item>
        <el-descriptions-item label="联系邮箱">{{ detailDialog.data?.contact_email }}</el-descriptions-item>
        <el-descriptions-item label="展位大小">{{ detailDialog.data?.booth_size }}</el-descriptions-item>
        <el-descriptions-item label="展位费用">{{ detailDialog.data?.booth_fee }}</el-descriptions-item>
        <el-descriptions-item label="展位号">{{ detailDialog.data?.booth_number }}</el-descriptions-item>
        <el-descriptions-item label="报名状态">
          <el-tag :type="getStatusType(detailDialog.data?.registration_status)">
            {{ getStatusLabel(detailDialog.data?.registration_status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="是否支付">
          <el-tag :type="detailDialog.data?.is_paid ? 'success' : 'info'">{{ detailDialog.data?.is_paid ? '是' : '否' }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="报名时间">{{ detailDialog.data?.registration_time }}</el-descriptions-item>
        <el-descriptions-item label="审核时间">{{ detailDialog.data?.approval_time }}</el-descriptions-item>
        <el-descriptions-item label="审核意见" :span="2">{{ detailDialog.data?.approval_comment }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ detailDialog.data?.remarks }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="formDialog.visible" :title="formDialog.type === 'create' ? '新增报名' : '编辑报名'" width="600px">
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="咨询会ID" prop="consultation_id">
          <el-input-number v-model="form.consultation_id" :min="1" style="width: 200px" />
        </el-form-item>
        <el-form-item label="高校ID" prop="university_id">
          <el-input-number v-model="form.university_id" :min="1" style="width: 200px" />
        </el-form-item>
        <el-form-item label="高校名称" prop="university_name">
          <el-input v-model="form.university_name" placeholder="请输入高校名称" />
        </el-form-item>
        <el-form-item label="联系人" prop="contact_person">
          <el-input v-model="form.contact_person" placeholder="请输入联系人" />
        </el-form-item>
        <el-form-item label="联系电话" prop="contact_phone">
          <el-input v-model="form.contact_phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="联系邮箱" prop="contact_email">
          <el-input v-model="form.contact_email" placeholder="请输入联系邮箱" />
        </el-form-item>
        <el-form-item label="展位大小" prop="booth_size">
          <el-input v-model="form.booth_size" placeholder="请输入展位大小，如：3x3" />
        </el-form-item>
        <el-form-item label="备注" prop="remarks">
          <el-input v-model="form.remarks" type="textarea" :rows="3" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="formDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 审核通过弹窗 -->
    <el-dialog v-model="approveDialog.visible" title="审核通过" width="500px">
      <el-form ref="approveFormRef" :model="approveForm" label-width="100px">
        <el-form-item label="展位号" prop="booth_number">
          <el-input v-model="approveForm.booth_number" placeholder="请输入展位号" />
        </el-form-item>
        <el-form-item label="展位大小" prop="booth_size">
          <el-input v-model="approveForm.booth_size" placeholder="请输入展位大小" />
        </el-form-item>
        <el-form-item label="展位费用" prop="booth_fee">
          <el-input-number v-model="approveForm.booth_fee" :min="0" :precision="2" style="width: 200px" />
        </el-form-item>
        <el-form-item label="审核意见" prop="comment">
          <el-input v-model="approveForm.comment" type="textarea" :rows="3" placeholder="请输入审核意见" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="approveDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleApproveSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 审核拒绝弹窗 -->
    <el-dialog v-model="rejectDialog.visible" title="审核拒绝" width="500px">
      <el-form ref="rejectFormRef" :model="rejectForm" :rules="rejectRules" label-width="100px">
        <el-form-item label="拒绝原因" prop="comment">
          <el-input v-model="rejectForm.comment" type="textarea" :rows="4" placeholder="请输入拒绝原因" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="rejectDialog.visible = false">取消</el-button>
        <el-button type="danger" @click="handleRejectSubmit">确定拒绝</el-button>
      </template>
    </el-dialog>

    <!-- 确认支付弹窗 -->
    <el-dialog v-model="paymentDialog.visible" title="确认支付" width="500px">
      <el-form ref="paymentFormRef" :model="paymentForm" :rules="paymentRules" label-width="100px">
        <el-form-item label="支付时间" prop="payment_time">
          <el-date-picker v-model="paymentForm.payment_time" type="datetime" placeholder="选择支付时间" value-format="YYYY-MM-DD HH:mm:ss" style="width: 200px" />
        </el-form-item>
        <el-form-item label="备注" prop="comment">
          <el-input v-model="paymentForm.comment" type="textarea" :rows="3" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="paymentDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handlePaymentSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";
import RegistrationAPI from "@/api/module_consultation/registration";
import type { RegistrationItem, RegistrationQuery } from "@/api/module_consultation/registration";

const searchForm = reactive<RegistrationQuery>({
  consultation_id: undefined,
  university_name: undefined,
  contact_person: undefined,
  contact_phone: undefined,
  registration_status: undefined,
});

const loading = ref(false);
const tableData = ref<RegistrationItem[]>([]);
const selectedIds = ref<number[]>([]);

const pagination = reactive({ page: 1, pageSize: 10, total: 0 });

const formDialog = reactive({ visible: false, type: "create" as "create" | "edit", data: undefined as RegistrationItem | undefined });
const detailDialog = reactive({ visible: false, data: undefined as RegistrationItem | undefined });
const approveDialog = reactive({ visible: false, data: undefined as RegistrationItem | undefined });
const rejectDialog = reactive({ visible: false, data: undefined as RegistrationItem | undefined });
const paymentDialog = reactive({ visible: false, data: undefined as RegistrationItem | undefined });

const formRef = ref<FormInstance>();
const approveFormRef = ref<FormInstance>();
const rejectFormRef = ref<FormInstance>();
const paymentFormRef = ref<FormInstance>();

const form = reactive<any>({
  consultation_id: undefined,
  university_id: undefined,
  university_name: "",
  contact_person: "",
  contact_phone: "",
  contact_email: "",
  booth_size: "",
  remarks: "",
});

const formRules: FormRules = {
  consultation_id: [{ required: true, message: "请输入咨询会ID", trigger: "blur" }],
  university_id: [{ required: true, message: "请输入高校ID", trigger: "blur" }],
};

const approveForm = reactive({ booth_number: "", booth_size: "", booth_fee: undefined as number | undefined, comment: "" });
const rejectForm = reactive({ comment: "" });
const rejectRules: FormRules = { comment: [{ required: true, message: "请输入拒绝原因", trigger: "blur" }] };
const paymentForm = reactive({ payment_time: "", comment: "" });
const paymentRules: FormRules = { payment_time: [{ required: true, message: "请选择支付时间", trigger: "change" }] };

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

const handleSearch = () => { pagination.page = 1; fetchList(); };
const handleReset = () => { Object.assign(searchForm, { consultation_id: undefined, university_name: undefined, contact_person: undefined, contact_phone: undefined, registration_status: undefined }); handleSearch(); };
const handleSelectionChange = (selection: RegistrationItem[]) => { selectedIds.value = selection.map(item => item.id!); };
const handleSizeChange = (size: number) => { pagination.pageSize = size; fetchList(); };
const handlePageChange = (page: number) => { pagination.page = page; fetchList(); };

const getStatusType = (status: string) => ({ pending: "warning", approved: "success", rejected: "danger", cancelled: "info" }[status] || "info");
const getStatusLabel = (status: string) => ({ pending: "待审核", approved: "已通过", rejected: "已拒绝", cancelled: "已取消" }[status] || status);

const handleCreate = () => { formDialog.type = "create"; Object.assign(form, { consultation_id: undefined, university_id: undefined, university_name: "", contact_person: "", contact_phone: "", contact_email: "", booth_size: "", remarks: "" }); formDialog.visible = true; };
const handleView = (row: RegistrationItem) => { detailDialog.data = row; detailDialog.visible = true; };
const handleEdit = (row: RegistrationItem) => { formDialog.type = "edit"; formDialog.data = row; Object.assign(form, row); formDialog.visible = true; };

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

const handleDelete = (row: RegistrationItem) => {
  ElMessageBox.confirm(`确定要删除这条报名记录吗？`, "删除确认", { confirmButtonText: "确定", cancelButtonText: "取消", type: "warning" })
    .then(async () => { await RegistrationAPI.delete(row.id!); ElMessage.success("删除成功"); fetchList(); }).catch(() => {});
};

const handleBatchDelete = () => {
  if (!selectedIds.value.length) { ElMessage.warning("请选择要删除的记录"); return; }
  ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 条记录吗？`, "批量删除确认", { confirmButtonText: "确定", cancelButtonText: "取消", type: "warning" })
    .then(async () => { await RegistrationAPI.batchDelete(selectedIds.value); ElMessage.success("批量删除成功"); fetchList(); }).catch(() => {});
};

const handleApprove = (row: RegistrationItem) => { approveDialog.data = row; Object.assign(approveForm, { booth_number: "", booth_size: row.booth_size || "", booth_fee: row.booth_fee, comment: "" }); approveDialog.visible = true; };

const handleApproveSubmit = async () => {
  if (!approveFormRef.value) return;
  await approveFormRef.value.validate(async (valid) => {
    if (valid) {
      await RegistrationAPI.approve(approveDialog.data!.id!, approveForm);
      ElMessage.success("审核通过");
      approveDialog.visible = false;
      fetchList();
    }
  });
};

const handleReject = (row: RegistrationItem) => { rejectDialog.data = row; Object.assign(rejectForm, { comment: "" }); rejectDialog.visible = true; };

const handleRejectSubmit = async () => {
  if (!rejectFormRef.value) return;
  await rejectFormRef.value.validate(async (valid) => {
    if (valid) {
      await RegistrationAPI.reject(rejectDialog.data!.id!, rejectForm.comment);
      ElMessage.success("已拒绝");
      rejectDialog.visible = false;
      fetchList();
    }
  });
};

const handleConfirmPayment = (row: RegistrationItem) => { paymentDialog.data = row; Object.assign(paymentForm, { payment_time: "", comment: "" }); paymentDialog.visible = true; };

const handlePaymentSubmit = async () => {
  if (!paymentFormRef.value) return;
  await paymentFormRef.value.validate(async (valid) => {
    if (valid) {
      await RegistrationAPI.confirmPayment(paymentDialog.data!.id!, paymentForm.payment_time, paymentForm.comment);
      ElMessage.success("确认成功");
      paymentDialog.visible = false;
      fetchList();
    }
  });
};

onMounted(() => { fetchList(); });
</script>

<style lang="scss" scoped>
.search-card { margin-bottom: 16px; }
.table-card {
  .card-header { display: flex; justify-content: space-between; align-items: center; .title { font-size: 16px; font-weight: 600; } .operations { display: flex; gap: 8px; } }
}
.pagination-container { display: flex; justify-content: flex-end; padding-top: 16px; }
</style>
