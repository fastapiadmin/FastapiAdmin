<!-- 审核对话框 -->
<template>
  <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px" destroy-on-close>
    <el-form :model="formData" label-width="100px">
      <el-divider content-position="left">咨询会信息</el-divider>
      <el-descriptions :column="1" border>
        <el-descriptions-item label="标题">{{ data?.title }}</el-descriptions-item>
        <el-descriptions-item label="主办方">{{ data?.organizer }}</el-descriptions-item>
        <el-descriptions-item label="开始日期">{{ data?.start_date }}</el-descriptions-item>
        <el-descriptions-item label="城市">{{ data?.city || "-" }}</el-descriptions-item>
      </el-descriptions>

      <el-divider content-position="left" style="margin-top: 20px">审核意见</el-divider>
      <el-form-item v-if="type === 'reject'" label="拒绝理由">
        <el-input
          v-model="formData.review_comment"
          type="textarea"
          :rows="4"
          placeholder="请输入拒绝理由"
        />
      </el-form-item>
      <el-form-item v-else label="审核意见">
        <el-input
          v-model="formData.review_comment"
          type="textarea"
          :rows="4"
          placeholder="请输入审核意见（选填）"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button
          :type="type === 'approve' ? 'success' : 'danger'"
          :loading="submitLoading"
          @click="handleSubmit"
        >
          {{ type === "approve" ? "通过" : "拒绝" }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from "vue";
import { ElMessage } from "element-plus";
import ConsultationInfoAPI from "@/api/module_consultation/consultation";
import type { ConsultationInfoItem } from "@/api/module_consultation/consultation";

interface Props {
  visible: boolean;
  type: "approve" | "reject";
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

const dialogTitle = computed(() => {
  return props.type === "approve" ? "审核通过" : "审核拒绝";
});

const data = computed(() => props.data);
const submitLoading = ref(false);

const formData = reactive({
  review_comment: "",
});

const handleSubmit = async () => {
  if (props.type === "reject" && !formData.review_comment.trim()) {
    ElMessage.warning("请输入拒绝理由");
    return;
  }

  submitLoading.value = true;
  try {
    if (props.type === "approve") {
      await ConsultationInfoAPI.approve(props.data!.id!, formData.review_comment);
      ElMessage.success("审核通过");
    } else {
      await ConsultationInfoAPI.reject(props.data!.id!, formData.review_comment);
      ElMessage.success("审核拒绝");
    }
    emit("success");
    dialogVisible.value = false;
    formData.review_comment = "";
  } finally {
    submitLoading.value = false;
  }
};
</script>

<style lang="scss" scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
