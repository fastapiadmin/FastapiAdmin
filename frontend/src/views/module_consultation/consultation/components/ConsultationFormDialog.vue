<!-- 咨询会信息表单（与详情/Excel 字段一致） -->
<template>
  <el-dialog
    v-model="dialogVisible"
    :title="dialogTitle"
    width="900px"
    destroy-on-close
    :close-on-click-modal="false"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="formRules"
      label-width="130px"
      class="consultation-form"
    >
      <el-divider content-position="left">基本信息</el-divider>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="序号" prop="excel_serial_no">
            <el-input v-model="formData.excel_serial_no" placeholder="Excel序号" clearable />
          </el-form-item>
        </el-col>
        <el-col :span="16">
          <el-form-item label="标题" prop="title">
            <el-input
              v-model="formData.title"
              placeholder="留空将按省份-线路-承办单位自动生成"
              maxlength="200"
              show-word-limit
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="省份" prop="province">
            <el-input v-model="formData.province" placeholder="省份" clearable />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="指导单位" prop="guidance_unit">
            <el-input v-model="formData.guidance_unit" placeholder="指导单位" clearable />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="承办单位" prop="organizer">
            <el-input v-model="formData.organizer" placeholder="承办单位" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="线路安排" prop="route_arrangement">
            <el-input v-model="formData.route_arrangement" placeholder="线路安排" clearable />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="是否参加" prop="is_participating">
            <el-input v-model="formData.is_participating" placeholder="是否参加" clearable />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="信息来源" prop="source_type">
            <el-select v-model="formData.source_type" style="width: 100%">
              <el-option label="全网抓取" value="crawler" />
              <el-option label="第三方上传" value="upload" />
              <el-option label="手动录入" value="manual" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-divider content-position="left">时间地点</el-divider>
      <el-row :gutter="20">
        <el-col :span="24">
          <el-form-item label="时间原文" prop="event_time_text">
            <el-input
              v-model="formData.event_time_text"
              type="textarea"
              :rows="3"
              placeholder="如：6月25-28日，或多场次说明"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="开始日期" prop="start_date">
            <el-date-picker
              v-model="formData.start_date"
              type="date"
              placeholder="开始日期"
              value-format="YYYY-MM-DD"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="结束日期" prop="end_date">
            <el-date-picker
              v-model="formData.end_date"
              type="date"
              placeholder="结束日期"
              value-format="YYYY-MM-DD"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="24">
          <el-form-item label="地点" prop="address">
            <el-input
              v-model="formData.address"
              type="textarea"
              :rows="2"
              placeholder="地点/详细地址"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-divider content-position="left">联系与费用</el-divider>
      <el-row :gutter="20">
        <el-col :span="24">
          <el-form-item label="人员" prop="personnel">
            <el-input v-model="formData.personnel" type="textarea" :rows="2" placeholder="人员" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="24">
          <el-form-item label="收费标准" prop="fee_description">
            <el-input
              v-model="formData.fee_description"
              type="textarea"
              :rows="3"
              placeholder="收费标准说明"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="24">
          <el-form-item label="邮寄材料地址" prop="mailing_address">
            <el-input
              v-model="formData.mailing_address"
              type="textarea"
              :rows="2"
              placeholder="邮寄材料地址"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="24">
          <el-form-item label="联系人及电话" prop="contact_info">
            <el-input v-model="formData.contact_info" placeholder="联系人及电话" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="24">
          <el-form-item label="汇款账户" prop="remittance_account">
            <el-input
              v-model="formData.remittance_account"
              type="textarea"
              :rows="3"
              placeholder="汇款账户信息"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-divider content-position="left">回执与材料</el-divider>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="回执情况" prop="receipt_status">
            <el-input v-model="formData.receipt_status" placeholder="回执情况" clearable />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="材料已领取" prop="materials_received">
            <el-input v-model="formData.materials_received" placeholder="材料已领取" clearable />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="24">
          <el-form-item label="材料" prop="materials">
            <el-input v-model="formData.materials" type="textarea" :rows="2" placeholder="材料" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="24">
          <el-form-item label="是否需要回执" prop="receipt_required_time">
            <el-input
              v-model="formData.receipt_required_time"
              placeholder="是否需要回执（具体时间）"
              clearable
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="24">
          <el-form-item label="备注" prop="remarks">
            <el-input v-model="formData.remarks" type="textarea" :rows="3" placeholder="备注" />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">确定</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from "vue";
import { ElMessage } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";
import ConsultationInfoAPI from "@/api/module_consultation/consultation";
import type {
  ConsultationInfoItem,
  ConsultationInfoForm,
} from "@/api/module_consultation/consultation";

interface Props {
  visible: boolean;
  type: "create" | "edit";
  data?: ConsultationInfoItem;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: "update:visible", value: boolean): void;
  (e: "success"): void;
}>();

const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit("update:visible", val),
});

const dialogTitle = computed(() =>
  props.type === "create" ? "新增咨询会信息" : "编辑咨询会信息"
);

const formRef = ref<FormInstance>();
const submitLoading = ref(false);

const defaultForm = (): ConsultationInfoForm => ({
  title: "",
  organizer: "",
  start_date: "",
  source_type: "manual",
  excel_serial_no: undefined,
  guidance_unit: undefined,
  route_arrangement: undefined,
  is_participating: undefined,
  event_time_text: undefined,
  end_date: undefined,
  address: undefined,
  personnel: undefined,
  fee_description: undefined,
  mailing_address: undefined,
  contact_info: undefined,
  remittance_account: undefined,
  receipt_status: undefined,
  materials: undefined,
  materials_received: undefined,
  remarks: undefined,
  receipt_required_time: undefined,
  province: undefined,
});

const formData = reactive<ConsultationInfoForm>(defaultForm());

const formRules: FormRules = {
  organizer: [
    { required: true, message: "请输入承办单位", trigger: "blur" },
    { min: 2, max: 200, message: "长度在 2 到 200 个字符", trigger: "blur" },
  ],
  start_date: [{ required: true, message: "请选择开始日期", trigger: "change" }],
};

const buildTitle = () => {
  const parts = [formData.province, formData.route_arrangement, formData.organizer].filter(
    (p) => p && String(p).trim()
  );
  return (parts.length ? parts.join("-") : formData.organizer).slice(0, 200);
};

const resetForm = () => {
  Object.assign(formData, defaultForm());
};

watch(
  () => props.data,
  (newData) => {
    if (newData) {
      Object.assign(formData, defaultForm(), newData);
    } else {
      resetForm();
    }
  },
  { immediate: true }
);

const handleSubmit = async () => {
  if (!formRef.value) return;
  const valid = await formRef.value.validate().catch(() => false);
  if (!valid) return;

  if (!formData.title?.trim()) {
    formData.title = buildTitle();
  }
  if (!formData.title?.trim() || formData.title.length < 2) {
    ElMessage.warning("请填写标题或完善省份、线路、承办单位以自动生成标题");
    return;
  }

  submitLoading.value = true;
  try {
    const payload = { ...formData };
    if (props.type === "create") {
      await ConsultationInfoAPI.create(payload);
      ElMessage.success("创建成功");
    } else {
      await ConsultationInfoAPI.update(props.data!.id!, payload);
      ElMessage.success("更新成功");
    }
    emit("success");
    dialogVisible.value = false;
  } finally {
    submitLoading.value = false;
  }
};
</script>

<style lang="scss" scoped>
.consultation-form {
  max-height: 65vh;
  overflow-y: auto;
  padding-right: 8px;

  :deep(.el-divider__text) {
    font-size: 14px;
    font-weight: 600;
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
