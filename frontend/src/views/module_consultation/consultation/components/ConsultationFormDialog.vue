<!-- 咨询会信息表单弹窗 -->
<template>
  <el-dialog
    v-model="dialogVisible"
    :title="dialogTitle"
    width="800px"
    destroy-on-close
    :close-on-click-modal="false"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="formRules"
      label-width="120px"
      class="consultation-form"
    >
      <el-divider content-position="left">基本信息</el-divider>
      
      <el-row :gutter="20">
        <el-col :span="24">
          <el-form-item label="咨询会标题" prop="title">
            <el-input v-model="formData.title" placeholder="请输入咨询会标题" maxlength="200" show-word-limit />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="24">
          <el-form-item label="咨询会描述" prop="description">
            <el-input
              v-model="formData.description"
              type="textarea"
              :rows="3"
              placeholder="请输入咨询会描述"
              maxlength="2000"
              show-word-limit
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-divider content-position="left">主办方信息</el-divider>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="主办方" prop="organizer">
            <el-input v-model="formData.organizer" placeholder="请输入主办方" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="主办方类型" prop="organizer_type">
            <el-select v-model="formData.organizer_type" placeholder="请选择" clearable style="width: 100%">
              <el-option label="教育部门" value="education_dept" />
              <el-option label="高校" value="university" />
              <el-option label="中学" value="high_school" />
              <el-option label="培训机构" value="training" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-divider content-position="left">时间地点</el-divider>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="开始日期" prop="start_date">
            <el-date-picker
              v-model="formData.start_date"
              type="date"
              placeholder="选择开始日期"
              value-format="YYYY-MM-DD"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="结束日期" prop="end_date">
            <el-date-picker
              v-model="formData.end_date"
              type="date"
              placeholder="选择结束日期"
              value-format="YYYY-MM-DD"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="开始时间" prop="start_time">
            <el-time-picker
              v-model="formData.start_time"
              placeholder="选择开始时间"
              value-format="HH:mm"
              format="HH:mm"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="结束时间" prop="end_time">
            <el-time-picker
              v-model="formData.end_time"
              placeholder="选择结束时间"
              value-format="HH:mm"
              format="HH:mm"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="省份" prop="province">
            <el-input v-model="formData.province" placeholder="请输入省份" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="城市" prop="city">
            <el-input v-model="formData.city" placeholder="请输入城市" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="区县" prop="district">
            <el-input v-model="formData.district" placeholder="请输入区县" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="24">
          <el-form-item label="详细地址" prop="address">
            <el-input v-model="formData.address" placeholder="请输入详细地址" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-divider content-position="left">其他信息</el-divider>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="预计参观人数" prop="estimated_visitors">
            <el-input-number
              v-model="formData.estimated_visitors"
              :min="0"
              :step="100"
              placeholder="请输入预计参观人数"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="展位费用" prop="booth_fee">
            <el-input-number
              v-model="formData.booth_fee"
              :min="0"
              :precision="2"
              :step="100"
              placeholder="请输入展位费用"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="信息来源" prop="source_type">
            <el-select v-model="formData.source_type" placeholder="请选择信息来源" style="width: 100%">
              <el-option label="全网抓取" value="crawler" />
              <el-option label="第三方上传" value="upload" />
              <el-option label="手动录入" value="manual" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="来源链接" prop="source_url">
            <el-input v-model="formData.source_url" placeholder="请输入来源链接" />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">
          确定
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from "vue";
import { ElMessage } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";
import ConsultationInfoAPI from "@/api/module_consultation/consultation";
import type { ConsultationInfoItem, ConsultationInfoForm } from "@/api/module_consultation/consultation";

// Props & Emits
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

// 弹窗显示控制
const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit("update:visible", val),
});

// 弹窗标题
const dialogTitle = computed(() => {
  return props.type === "create" ? "新增咨询会信息" : "编辑咨询会信息";
});

// 表单引用
const formRef = ref<FormInstance>();
const submitLoading = ref(false);

// 表单数据
const formData = reactive<ConsultationInfoForm>({
  title: "",
  description: "",
  organizer: "",
  organizer_type: undefined,
  start_date: "",
  end_date: undefined,
  start_time: undefined,
  end_time: undefined,
  province: undefined,
  city: undefined,
  district: undefined,
  address: undefined,
  participating_universities: undefined,
  estimated_visitors: undefined,
  booth_fee: undefined,
  source_type: "manual",
  source_url: undefined,
});

// 表单校验规则
const formRules: FormRules = {
  title: [
    { required: true, message: "请输入咨询会标题", trigger: "blur" },
    { min: 2, max: 200, message: "长度在 2 到 200 个字符", trigger: "blur" },
  ],
  organizer: [
    { required: true, message: "请输入主办方", trigger: "blur" },
    { min: 2, max: 200, message: "长度在 2 到 200 个字符", trigger: "blur" },
  ],
  start_date: [{ required: true, message: "请选择开始日期", trigger: "change" }],
};

// 监听数据变化
watch(
  () => props.data,
  (newData) => {
    if (newData) {
      Object.assign(formData, newData);
    } else {
      // 重置表单
      Object.assign(formData, {
        title: "",
        description: "",
        organizer: "",
        organizer_type: undefined,
        start_date: "",
        end_date: undefined,
        start_time: undefined,
        end_time: undefined,
        province: undefined,
        city: undefined,
        district: undefined,
        address: undefined,
        participating_universities: undefined,
        estimated_visitors: undefined,
        booth_fee: undefined,
        source_type: "manual",
        source_url: undefined,
      });
    }
  },
  { immediate: true, deep: true }
);

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return;

  const valid = await formRef.value.validate().catch(() => false);
  if (!valid) return;

  submitLoading.value = true;
  try {
    if (props.type === "create") {
      await ConsultationInfoAPI.create(formData);
      ElMessage.success("创建成功");
    } else {
      await ConsultationInfoAPI.update(props.data!.id!, formData);
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
  :deep(.el-divider__text) {
    font-size: 14px;
    font-weight: 600;
    color: var(--el-text-color-primary);
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
