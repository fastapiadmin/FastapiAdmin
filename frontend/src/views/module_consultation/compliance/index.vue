<!-- 招生咨询会 - 合规诊断管理 -->
<template>
  <div class="app-container">
    <el-tabs v-model="activeTab" type="border-card">
      <!-- 诊断记录 -->
      <el-tab-pane label="诊断记录" name="diagnosis">
        <el-card class="search-card" shadow="never">
          <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="90px">
            <el-form-item label="咨询会ID" prop="consultation_id">
              <el-input-number v-model="searchForm.consultation_id" :min="1" style="width: 150px" />
            </el-form-item>
            <el-form-item label="合规等级" prop="compliance_level">
              <el-select
                v-model="searchForm.compliance_level"
                placeholder="请选择"
                clearable
                style="width: 120px"
              >
                <el-option label="高" value="high" />
                <el-option label="中" value="medium" />
                <el-option label="低" value="low" />
              </el-select>
            </el-form-item>
            <el-form-item label="高风险" prop="is_high_risk">
              <el-select
                v-model="searchForm.is_high_risk"
                placeholder="请选择"
                clearable
                style="width: 100px"
              >
                <el-option label="是" :value="true" />
                <el-option label="否" :value="false" />
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
              <span class="title">诊断记录列表</span>
              <div class="operations">
                <el-button
                  v-permission="['module_consultation:compliance:create']"
                  type="primary"
                  @click="handleCreateDiagnosis"
                >
                  <i-ep-plus />
                  新增诊断
                </el-button>
                <el-button
                  v-permission="['module_consultation:compliance:delete']"
                  type="danger"
                  :disabled="!selectedIds.length"
                  @click="handleBatchDeleteDiagnosis"
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
            <el-table-column prop="compliance_score" label="合规评分" width="100" align="center">
              <template #default="{ row }">
                <el-tag :type="getScoreType(row.compliance_score)">
                  {{ row.compliance_score }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="compliance_level" label="合规等级" width="100">
              <template #default="{ row }">
                <el-tag :type="getLevelType(row.compliance_level)">
                  {{ getLevelLabel(row.compliance_level) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="is_high_risk" label="高风险" width="80">
              <template #default="{ row }">
                <el-tag v-if="row.is_high_risk" type="danger" size="small">是</el-tag>
                <span v-else>-</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="risk_factors"
              label="风险因素"
              min-width="150"
              show-overflow-tooltip
            >
              <template #default="{ row }">
                {{ row.risk_factors?.join(", ") || "-" }}
              </template>
            </el-table-column>
            <el-table-column prop="is_latest" label="最新" width="70">
              <template #default="{ row }">
                <el-tag v-if="row.is_latest" type="success" size="small">最新</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="diagnosis_time" label="诊断时间" width="160" />
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button
                  v-permission="['module_consultation:compliance:detail']"
                  link
                  type="primary"
                  @click="handleViewDiagnosis(row)"
                >
                  详情
                </el-button>
                <el-button
                  v-permission="['module_consultation:compliance:delete']"
                  link
                  type="danger"
                  @click="handleDeleteDiagnosis(row)"
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
      </el-tab-pane>

      <!-- 合规规则 -->
      <el-tab-pane label="合规规则" name="rule">
        <el-card class="search-card" shadow="never">
          <el-form
            ref="ruleSearchFormRef"
            :model="ruleSearchForm"
            :inline="true"
            label-width="80px"
          >
            <el-form-item label="规则名称" prop="name">
              <el-input
                v-model="ruleSearchForm.name"
                placeholder="请输入规则名称"
                clearable
                style="width: 200px"
              />
            </el-form-item>
            <el-form-item label="风险等级" prop="risk_level">
              <el-select
                v-model="ruleSearchForm.risk_level"
                placeholder="请选择"
                clearable
                style="width: 100px"
              >
                <el-option label="高" value="high" />
                <el-option label="中" value="medium" />
                <el-option label="低" value="low" />
              </el-select>
            </el-form-item>
            <el-form-item label="是否启用" prop="is_active">
              <el-select
                v-model="ruleSearchForm.is_active"
                placeholder="请选择"
                clearable
                style="width: 100px"
              >
                <el-option label="是" :value="true" />
                <el-option label="否" :value="false" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleRuleSearch">
                <i-ep-search />
                搜索
              </el-button>
              <el-button @click="handleRuleReset">
                <i-ep-refresh />
                重置
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <el-card class="table-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span class="title">合规规则列表</span>
              <div class="operations">
                <el-button
                  v-permission="['module_consultation:compliance:create']"
                  type="primary"
                  @click="handleCreateRule"
                >
                  <i-ep-plus />
                  新增规则
                </el-button>
                <el-button
                  v-permission="['module_consultation:compliance:delete']"
                  type="danger"
                  :disabled="!ruleSelectedIds.length"
                  @click="handleBatchDeleteRule"
                >
                  <i-ep-delete />
                  批量删除
                </el-button>
              </div>
            </div>
          </template>

          <el-table
            v-loading="ruleLoading"
            :data="ruleTableData"
            stripe
            border
            @selection-change="handleRuleSelectionChange"
          >
            <el-table-column type="selection" width="55" align="center" />
            <el-table-column type="index" label="序号" width="60" align="center" />
            <el-table-column prop="name" label="规则名称" min-width="150" show-overflow-tooltip />
            <el-table-column prop="rule_type" label="规则类型" width="120" />
            <el-table-column
              prop="description"
              label="描述"
              min-width="150"
              show-overflow-tooltip
            />
            <el-table-column prop="risk_level" label="风险等级" width="100">
              <template #default="{ row }">
                <el-tag :type="getRiskType(row.risk_level)">
                  {{ getLevelLabel(row.risk_level) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="rule_weight" label="权重" width="70" align="center" />
            <el-table-column prop="order" label="排序" width="70" align="center" />
            <el-table-column prop="is_active" label="启用" width="70" align="center">
              <template #default="{ row }">
                <el-tag :type="row.is_active ? 'success' : 'info'" size="small">
                  {{ row.is_active ? "是" : "否" }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button
                  v-permission="['module_consultation:compliance:detail']"
                  link
                  type="primary"
                  @click="handleViewRule(row)"
                >
                  详情
                </el-button>
                <el-button
                  v-permission="['module_consultation:compliance:update']"
                  link
                  type="primary"
                  @click="handleEditRule(row)"
                >
                  编辑
                </el-button>
                <el-button
                  v-permission="['module_consultation:compliance:update']"
                  link
                  type="warning"
                  @click="handleToggleRule(row)"
                >
                  {{ row.is_active ? "禁用" : "启用" }}
                </el-button>
                <el-button
                  v-permission="['module_consultation:compliance:delete']"
                  link
                  type="danger"
                  @click="handleDeleteRule(row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <div class="pagination-container">
            <el-pagination
              v-model:current-page="rulePagination.page"
              v-model:page-size="rulePagination.pageSize"
              :total="rulePagination.total"
              :page-sizes="[10, 20, 50, 100]"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleRuleSizeChange"
              @current-change="handleRulePageChange"
            />
          </div>
        </el-card>
      </el-tab-pane>
    </el-tabs>

    <!-- 诊断详情弹窗 -->
    <el-dialog v-model="diagnosisDetailDialog.visible" title="诊断详情" width="600px">
      <el-descriptions v-if="diagnosisDetailDialog.data" :column="2" border>
        <el-descriptions-item label="咨询会ID">
          {{ diagnosisDetailDialog.data.consultation_id }}
        </el-descriptions-item>
        <el-descriptions-item label="合规评分">
          <el-tag :type="getScoreType(diagnosisDetailDialog.data.compliance_score)">
            {{ diagnosisDetailDialog.data.compliance_score }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="合规等级">
          <el-tag :type="getLevelType(diagnosisDetailDialog.data.compliance_level)">
            {{ getLevelLabel(diagnosisDetailDialog.data.compliance_level) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="高风险">
          <el-tag v-if="diagnosisDetailDialog.data.is_high_risk" type="danger">是</el-tag>
          <span v-else>否</span>
        </el-descriptions-item>
        <el-descriptions-item label="诊断时间" :span="2">
          {{ diagnosisDetailDialog.data.diagnosis_time }}
        </el-descriptions-item>
        <el-descriptions-item label="风险因素" :span="2">
          {{ diagnosisDetailDialog.data.risk_factors?.join(", ") || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="改进建议" :span="2">
          {{ diagnosisDetailDialog.data.improvement_suggestions?.join(", ") || "-" }}
        </el-descriptions-item>
        <el-descriptions-item label="风险警告" :span="2">
          {{ diagnosisDetailDialog.data.risk_warning || "-" }}
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 新增/编辑诊断弹窗 -->
    <el-dialog
      v-model="diagnosisFormDialog.visible"
      :title="diagnosisFormDialog.type === 'create' ? '新增诊断' : '编辑诊断'"
      width="500px"
    >
      <el-form
        ref="diagnosisFormRef"
        :model="diagnosisForm"
        :rules="diagnosisRules"
        label-width="100px"
      >
        <el-form-item label="咨询会ID" prop="consultation_id">
          <el-input-number v-model="diagnosisForm.consultation_id" :min="1" style="width: 200px" />
        </el-form-item>
        <el-form-item label="合规评分" prop="compliance_score">
          <el-input-number
            v-model="diagnosisForm.compliance_score"
            :min="0"
            :max="100"
            style="width: 200px"
          />
        </el-form-item>
        <el-form-item label="合规等级" prop="compliance_level">
          <el-select
            v-model="diagnosisForm.compliance_level"
            placeholder="请选择"
            style="width: 200px"
          >
            <el-option label="高" value="high" />
            <el-option label="中" value="medium" />
            <el-option label="低" value="low" />
          </el-select>
        </el-form-item>
        <el-form-item label="高风险" prop="is_high_risk">
          <el-switch v-model="diagnosisForm.is_high_risk" />
        </el-form-item>
        <el-form-item label="风险警告" prop="risk_warning">
          <el-input
            v-model="diagnosisForm.risk_warning"
            type="textarea"
            :rows="2"
            placeholder="请输入风险警告"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="diagnosisFormDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleDiagnosisSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 规则详情弹窗 -->
    <el-dialog v-model="ruleDetailDialog.visible" title="规则详情" width="600px">
      <el-descriptions v-if="ruleDetailDialog.data" :column="2" border>
        <el-descriptions-item label="规则名称" :span="2">
          {{ ruleDetailDialog.data.name }}
        </el-descriptions-item>
        <el-descriptions-item label="规则类型">
          {{ ruleDetailDialog.data.rule_type }}
        </el-descriptions-item>
        <el-descriptions-item label="风险等级">
          <el-tag :type="getRiskType(ruleDetailDialog.data.risk_level)">
            {{ getLevelLabel(ruleDetailDialog.data.risk_level) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="权重">
          {{ ruleDetailDialog.data.rule_weight }}
        </el-descriptions-item>
        <el-descriptions-item label="排序">{{ ruleDetailDialog.data.order }}</el-descriptions-item>
        <el-descriptions-item label="启用">
          <el-tag :type="ruleDetailDialog.data.is_active ? 'success' : 'info'">
            {{ ruleDetailDialog.data.is_active ? "是" : "否" }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">
          {{ ruleDetailDialog.data.description || "-" }}
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 新增/编辑规则弹窗 -->
    <el-dialog
      v-model="ruleFormDialog.visible"
      :title="ruleFormDialog.type === 'create' ? '新增规则' : '编辑规则'"
      width="500px"
    >
      <el-form ref="ruleFormRef" :model="ruleForm" :rules="ruleFormRules" label-width="100px">
        <el-form-item label="规则名称" prop="name">
          <el-input v-model="ruleForm.name" placeholder="请输入规则名称" />
        </el-form-item>
        <el-form-item label="规则类型" prop="rule_type">
          <el-input v-model="ruleForm.rule_type" placeholder="请输入规则类型" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="ruleForm.description"
            type="textarea"
            :rows="2"
            placeholder="请输入描述"
          />
        </el-form-item>
        <el-form-item label="风险等级" prop="risk_level">
          <el-select v-model="ruleForm.risk_level" placeholder="请选择" style="width: 200px">
            <el-option label="高" value="high" />
            <el-option label="中" value="medium" />
            <el-option label="低" value="low" />
          </el-select>
        </el-form-item>
        <el-form-item label="权重" prop="rule_weight">
          <el-input-number
            v-model="ruleForm.rule_weight"
            :min="1"
            :max="100"
            style="width: 200px"
          />
        </el-form-item>
        <el-form-item label="排序" prop="order">
          <el-input-number v-model="ruleForm.order" :min="0" style="width: 200px" />
        </el-form-item>
        <el-form-item label="启用" prop="is_active">
          <el-switch v-model="ruleForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="ruleFormDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleRuleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";
import ComplianceAPI from "@/api/module_consultation/compliance";
import type {
  DiagnosisItem,
  DiagnosisQuery,
  RuleItem,
  RuleQuery,
} from "@/api/module_consultation/compliance";

const activeTab = ref("diagnosis");

// 诊断相关
const searchForm = reactive<DiagnosisQuery>({
  consultation_id: undefined,
  compliance_level: undefined,
  is_high_risk: undefined,
});
const loading = ref(false);
const tableData = ref<DiagnosisItem[]>([]);
const selectedIds = ref<number[]>([]);
const pagination = reactive({ page: 1, pageSize: 10, total: 0 });

const diagnosisDetailDialog = reactive({
  visible: false,
  data: undefined as DiagnosisItem | undefined,
});
const diagnosisFormDialog = reactive({
  visible: false,
  type: "create" as "create" | "edit",
  data: undefined as DiagnosisItem | undefined,
});
const diagnosisFormRef = ref<FormInstance>();

const diagnosisForm = reactive<any>({
  consultation_id: undefined,
  compliance_score: 0,
  compliance_level: "",
  is_high_risk: false,
  risk_warning: "",
});
const diagnosisRules: FormRules = {
  consultation_id: [{ required: true, message: "请输入咨询会ID", trigger: "blur" }],
  compliance_score: [{ required: true, message: "请输入合规评分", trigger: "blur" }],
  compliance_level: [{ required: true, message: "请选择合规等级", trigger: "change" }],
};

const fetchDiagnosisList = async () => {
  loading.value = true;
  try {
    const params = { page_no: pagination.page, page_size: pagination.pageSize, ...searchForm };
    const res = await ComplianceAPI.getDiagnosisList(params);
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
  fetchDiagnosisList();
};
const handleReset = () => {
  Object.assign(searchForm, {
    consultation_id: undefined,
    compliance_level: undefined,
    is_high_risk: undefined,
  });
  handleSearch();
};
const handleSelectionChange = (selection: DiagnosisItem[]) => {
  selectedIds.value = selection.map((item) => item.id!);
};
const handleSizeChange = (size: number) => {
  pagination.pageSize = size;
  fetchDiagnosisList();
};
const handlePageChange = (page: number) => {
  pagination.page = page;
  fetchDiagnosisList();
};

const handleViewDiagnosis = (row: DiagnosisItem) => {
  diagnosisDetailDialog.data = row;
  diagnosisDetailDialog.visible = true;
};
const handleDeleteDiagnosis = (row: DiagnosisItem) => {
  ElMessageBox.confirm(`确定要删除这条诊断记录吗？`, "删除确认", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await ComplianceAPI.deleteDiagnosis(row.id!);
      ElMessage.success("删除成功");
      fetchDiagnosisList();
    })
    .catch(() => {});
};
const handleBatchDeleteDiagnosis = () => {
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
      await ComplianceAPI.batchDeleteDiagnosis(selectedIds.value);
      ElMessage.success("批量删除成功");
      fetchDiagnosisList();
    })
    .catch(() => {});
};
const handleCreateDiagnosis = () => {
  diagnosisFormDialog.type = "create";
  Object.assign(diagnosisForm, {
    consultation_id: undefined,
    compliance_score: 0,
    compliance_level: "",
    is_high_risk: false,
    risk_warning: "",
  });
  diagnosisFormDialog.visible = true;
};
const handleDiagnosisSubmit = async () => {
  if (!diagnosisFormRef.value) return;
  await diagnosisFormRef.value.validate(async (valid) => {
    if (valid) {
      if (diagnosisFormDialog.type === "create") {
        await ComplianceAPI.createDiagnosis(diagnosisForm);
        ElMessage.success("创建成功");
      } else {
        await ComplianceAPI.updateDiagnosis(diagnosisFormDialog.data!.id!, diagnosisForm);
        ElMessage.success("更新成功");
      }
      diagnosisFormDialog.visible = false;
      fetchDiagnosisList();
    }
  });
};

// 规则相关
const ruleSearchForm = reactive<RuleQuery>({
  name: undefined,
  risk_level: undefined,
  is_active: undefined,
});
const ruleLoading = ref(false);
const ruleTableData = ref<RuleItem[]>([]);
const ruleSelectedIds = ref<number[]>([]);
const rulePagination = reactive({ page: 1, pageSize: 10, total: 0 });

const ruleDetailDialog = reactive({ visible: false, data: undefined as RuleItem | undefined });
const ruleFormDialog = reactive({
  visible: false,
  type: "create" as "create" | "edit",
  data: undefined as RuleItem | undefined,
});
const ruleFormRef = ref<FormInstance>();

const ruleForm = reactive<any>({
  name: "",
  rule_type: "",
  description: "",
  risk_level: "",
  rule_weight: 10,
  order: 0,
  is_active: true,
});
const ruleFormRules: FormRules = {
  name: [{ required: true, message: "请输入规则名称", trigger: "blur" }],
  rule_type: [{ required: true, message: "请输入规则类型", trigger: "blur" }],
  risk_level: [{ required: true, message: "请选择风险等级", trigger: "change" }],
};

const fetchRuleList = async () => {
  ruleLoading.value = true;
  try {
    const params = {
      page_no: rulePagination.page,
      page_size: rulePagination.pageSize,
      ...ruleSearchForm,
    };
    const res = await ComplianceAPI.getRuleList(params);
    if (res.data?.data) {
      ruleTableData.value = res.data.data.items || [];
      rulePagination.total = res.data.data.total || 0;
    }
  } finally {
    ruleLoading.value = false;
  }
};

const handleRuleSearch = () => {
  rulePagination.page = 1;
  fetchRuleList();
};
const handleRuleReset = () => {
  Object.assign(ruleSearchForm, { name: undefined, risk_level: undefined, is_active: undefined });
  handleRuleSearch();
};
const handleRuleSelectionChange = (selection: RuleItem[]) => {
  ruleSelectedIds.value = selection.map((item) => item.id!);
};
const handleRuleSizeChange = (size: number) => {
  rulePagination.pageSize = size;
  fetchRuleList();
};
const handleRulePageChange = (page: number) => {
  rulePagination.page = page;
  fetchRuleList();
};

const handleViewRule = (row: RuleItem) => {
  ruleDetailDialog.data = row;
  ruleDetailDialog.visible = true;
};
const handleEditRule = (row: RuleItem) => {
  ruleFormDialog.type = "edit";
  ruleFormDialog.data = row;
  Object.assign(ruleForm, row);
  ruleFormDialog.visible = true;
};
const handleToggleRule = (row: RuleItem) => {
  ElMessageBox.confirm(
    `确定要${row.is_active ? "禁用" : "启用"}规则 "${row.name}" 吗？`,
    "切换状态",
    { confirmButtonText: "确定", cancelButtonText: "取消", type: "info" }
  )
    .then(async () => {
      await ComplianceAPI.toggleRuleStatus(row.id!);
      ElMessage.success("操作成功");
      fetchRuleList();
    })
    .catch(() => {});
};
const handleDeleteRule = (row: RuleItem) => {
  ElMessageBox.confirm(`确定要删除规则 "${row.name}" 吗？`, "删除确认", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await ComplianceAPI.deleteRule(row.id!);
      ElMessage.success("删除成功");
      fetchRuleList();
    })
    .catch(() => {});
};
const handleBatchDeleteRule = () => {
  if (!ruleSelectedIds.value.length) {
    ElMessage.warning("请选择要删除的记录");
    return;
  }
  ElMessageBox.confirm(
    `确定要删除选中的 ${ruleSelectedIds.value.length} 条记录吗？`,
    "批量删除确认",
    { confirmButtonText: "确定", cancelButtonText: "取消", type: "warning" }
  )
    .then(async () => {
      await ComplianceAPI.batchDeleteRule(ruleSelectedIds.value);
      ElMessage.success("批量删除成功");
      fetchRuleList();
    })
    .catch(() => {});
};
const handleCreateRule = () => {
  ruleFormDialog.type = "create";
  Object.assign(ruleForm, {
    name: "",
    rule_type: "",
    description: "",
    risk_level: "",
    rule_weight: 10,
    order: 0,
    is_active: true,
  });
  ruleFormDialog.visible = true;
};
const handleRuleSubmit = async () => {
  if (!ruleFormRef.value) return;
  await ruleFormRef.value.validate(async (valid) => {
    if (valid) {
      if (ruleFormDialog.type === "create") {
        await ComplianceAPI.createRule(ruleForm);
        ElMessage.success("创建成功");
      } else {
        await ComplianceAPI.updateRule(ruleFormDialog.data!.id!, ruleForm);
        ElMessage.success("更新成功");
      }
      ruleFormDialog.visible = false;
      fetchRuleList();
    }
  });
};

// 工具函数
const getScoreType = (score: number) => {
  if (score >= 80) return "success";
  if (score >= 60) return "warning";
  return "danger";
};
const getLevelType = (level: string) => {
  if (level === "high") return "danger";
  if (level === "medium") return "warning";
  return "success";
};
const getRiskType = (level: string) => {
  if (level === "high") return "danger";
  if (level === "medium") return "warning";
  return "success";
};
const getLevelLabel = (level: string) => ({ high: "高", medium: "中", low: "低" })[level] || level;

onMounted(() => {
  fetchDiagnosisList();
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
