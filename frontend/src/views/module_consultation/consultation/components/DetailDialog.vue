<!-- 详情对话框（与 Excel/抓取字段一致） -->
<template>
  <el-dialog v-model="dialogVisible" title="咨询会信息详情" width="900px" destroy-on-close>
    <el-descriptions v-if="data" :column="2" border>
      <el-descriptions-item v-if="data.excel_serial_no" label="序号">
        {{ data.excel_serial_no }}
      </el-descriptions-item>
      <el-descriptions-item label="标题" :span="data.excel_serial_no ? 1 : 2">
        {{ data.title }}
      </el-descriptions-item>
      <el-descriptions-item label="省份">{{ data.province || "-" }}</el-descriptions-item>
      <el-descriptions-item label="指导单位">{{ data.guidance_unit || "-" }}</el-descriptions-item>
      <el-descriptions-item label="承办单位">{{ data.organizer }}</el-descriptions-item>
      <el-descriptions-item label="线路安排">{{ data.route_arrangement || "-" }}</el-descriptions-item>
      <el-descriptions-item label="是否参加">{{ data.is_participating || "-" }}</el-descriptions-item>
      <el-descriptions-item label="信息来源">
        <el-tag :type="getSourceTypeType(data.source_type)">
          {{ getSourceTypeLabel(data.source_type) }}
        </el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="时间原文" :span="2">
        {{ data.event_time_text || "-" }}
      </el-descriptions-item>
      <el-descriptions-item label="开始日期">{{ data.start_date }}</el-descriptions-item>
      <el-descriptions-item label="结束日期">{{ data.end_date || "-" }}</el-descriptions-item>
      <el-descriptions-item label="地点" :span="2">{{ data.address || "-" }}</el-descriptions-item>
      <el-descriptions-item label="人员" :span="2">{{ data.personnel || "-" }}</el-descriptions-item>
      <el-descriptions-item label="收费标准" :span="2">
        {{ data.fee_description || "-" }}
      </el-descriptions-item>
      <el-descriptions-item label="邮寄材料地址" :span="2">
        {{ data.mailing_address || "-" }}
      </el-descriptions-item>
      <el-descriptions-item label="联系人及电话" :span="2">
        {{ data.contact_info || "-" }}
      </el-descriptions-item>
      <el-descriptions-item label="汇款账户" :span="2">
        {{ data.remittance_account || "-" }}
      </el-descriptions-item>
      <el-descriptions-item label="回执情况">{{ data.receipt_status || "-" }}</el-descriptions-item>
      <el-descriptions-item label="材料已领取">
        {{ data.materials_received || "-" }}
      </el-descriptions-item>
      <el-descriptions-item label="材料" :span="2">{{ data.materials || "-" }}</el-descriptions-item>
      <el-descriptions-item label="是否需要回执" :span="2">
        {{ data.receipt_required_time || "-" }}
      </el-descriptions-item>
      <el-descriptions-item label="备注" :span="2">
        {{ data.remarks || data.description || "-" }}
      </el-descriptions-item>
      <el-descriptions-item label="状态">
        <el-tag :type="getStatusType(data.status)">
          {{ getStatusLabel(data.status) }}
        </el-tag>
      </el-descriptions-item>
      <el-descriptions-item
        v-if="data.compliance_score !== null && data.compliance_score !== undefined"
        label="合规评分"
      >
        <el-tag :type="getComplianceType(data.compliance_score)">
          {{ data.compliance_score }}分
        </el-tag>
      </el-descriptions-item>
      <el-descriptions-item v-if="data.compliance_level" label="合规等级">
        {{ data.compliance_level }}
      </el-descriptions-item>
      <el-descriptions-item label="创建时间" :span="2">
        {{ data.created_time }}
      </el-descriptions-item>
      <el-descriptions-item label="更新时间" :span="2">
        {{ data.updated_time }}
      </el-descriptions-item>
    </el-descriptions>

    <template #footer>
      <el-button @click="dialogVisible = false">关闭</el-button>
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

type TagType = "primary" | "success" | "warning" | "info" | "danger";

const getSourceTypeType = (type: string): TagType => {
  const map: Record<string, TagType> = {
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

const getStatusType = (status: string): TagType => {
  const map: Record<string, TagType> = {
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

const getComplianceType = (score: number): TagType => {
  if (score >= 8) return "success";
  if (score >= 6) return "warning";
  return "danger";
};
</script>
