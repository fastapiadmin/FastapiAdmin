<!-- 详情对话框 -->
<template>
  <el-dialog v-model="dialogVisible" title="咨询会信息详情" width="700px" destroy-on-close>
    <el-descriptions v-if="data" :column="2" border>
      <el-descriptions-item label="标题" :span="2">{{ data.title }}</el-descriptions-item>
      <el-descriptions-item label="描述" :span="2">
        {{ data.description || "-" }}
      </el-descriptions-item>
      <el-descriptions-item label="主办方">{{ data.organizer }}</el-descriptions-item>
      <el-descriptions-item label="主办方类型">
        {{ getOrganizerTypeLabel(data.organizer_type) }}
      </el-descriptions-item>
      <el-descriptions-item label="开始日期">{{ data.start_date }}</el-descriptions-item>
      <el-descriptions-item label="结束日期">{{ data.end_date || "-" }}</el-descriptions-item>
      <el-descriptions-item label="开始时间">{{ data.start_time || "-" }}</el-descriptions-item>
      <el-descriptions-item label="结束时间">{{ data.end_time || "-" }}</el-descriptions-item>
      <el-descriptions-item label="省份">{{ data.province || "-" }}</el-descriptions-item>
      <el-descriptions-item label="城市">{{ data.city || "-" }}</el-descriptions-item>
      <el-descriptions-item label="区县">{{ data.district || "-" }}</el-descriptions-item>
      <el-descriptions-item label="详细地址" :span="2">
        {{ data.address || "-" }}
      </el-descriptions-item>
      <el-descriptions-item label="参与高校数量">{{ data.university_count }}</el-descriptions-item>
      <el-descriptions-item label="预计参观人数">
        {{ data.estimated_visitors || "-" }}
      </el-descriptions-item>
      <el-descriptions-item label="展位费用">
        {{ data.booth_fee ? "¥" + data.booth_fee : "-" }}
      </el-descriptions-item>
      <el-descriptions-item label="信息来源">
        <el-tag :type="getSourceTypeType(data.source_type)">
          {{ getSourceTypeLabel(data.source_type) }}
        </el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="状态">
        <el-tag :type="getStatusType(data.status)">
          {{ getStatusLabel(data.status) }}
        </el-tag>
      </el-descriptions-item>
      <el-descriptions-item v-if="data.compliance_score !== null" label="合规评分">
        <el-tag :type="getComplianceType(data.compliance_score)">
          {{ data.compliance_score }}分
        </el-tag>
      </el-descriptions-item>
      <el-descriptions-item v-if="data.compliance_level" label="合规等级">
        {{ getComplianceLevelLabel(data.compliance_level) }}
      </el-descriptions-item>
      <el-descriptions-item label="是否归档">
        {{ data.is_archived ? "是" : "否" }}
      </el-descriptions-item>
      <el-descriptions-item v-if="data.is_archived" label="归档时间">
        {{ data.archived_time }}
      </el-descriptions-item>
      <el-descriptions-item label="创建时间" :span="2">
        {{ data.created_time }}
      </el-descriptions-item>
      <el-descriptions-item label="更新时间" :span="2">
        {{ data.updated_time }}
      </el-descriptions-item>
    </el-descriptions>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">关闭</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { ConsultationInfoItem } from "@/api/module_consultation/consultation";

interface Props {
  visible: boolean;
  data?: ConsultationInfoItem;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: "update:visible", value: boolean): void;
}>();

const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit("update:visible", val),
});

const data = computed(() => props.data);

// 辅助函数
const getOrganizerTypeLabel = (type?: string) => {
  const map: Record<string, string> = {
    education_dept: "教育部门",
    university: "高校",
    high_school: "中学",
    training: "培训机构",
    other: "其他",
  };
  return type ? map[type] : "-";
};

const getSourceTypeType = (type: string) => {
  const map: Record<string, string> = {
    crawler: "primary",
    upload: "success",
    manual: "warning",
  };
  return map[type] || "info";
};

const getSourceTypeLabel = (type: string) => {
  const map: Record<string, string> = {
    crawler: "全网抓取",
    upload: "第三方上传",
    manual: "手动录入",
  };
  return map[type] || type;
};

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    pending: "warning",
    approved: "success",
    rejected: "danger",
    expired: "info",
  };
  return map[status] || "info";
};

const getStatusLabel = (status: string) => {
  const map: Record<string, string> = {
    pending: "待审核",
    approved: "已审核",
    rejected: "已拒绝",
    expired: "已过期",
  };
  return map[status] || status;
};

const getComplianceType = (score: number) => {
  if (score >= 80) return "success";
  if (score >= 60) return "warning";
  return "danger";
};

const getComplianceLevelLabel = (level: string) => {
  const map: Record<string, string> = {
    low: "低风险",
    medium: "中风险",
    high: "高风险",
  };
  return map[level] || level;
};
</script>

<style lang="scss" scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>
