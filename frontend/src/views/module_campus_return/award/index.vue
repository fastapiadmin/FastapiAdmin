<template>
  <div class="app-container">
    <el-card shadow="never">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="奖项类别" name="category">
          <el-form :inline="true" style="margin-bottom: 16px">
            <el-form-item label="批次ID"><el-input-number v-model="categorySearch.batch_id" :min="0" style="width: 120px" /></el-form-item>
            <el-form-item><el-button type="primary" @click="fetchCategories"><i-ep-search />搜索</el-button></el-form-item>
          </el-form>
          <el-table v-loading="categoryLoading" :data="categoryData" stripe border>
            <el-table-column type="index" label="序号" width="60" align="center" />
            <el-table-column prop="category_name" label="奖项名称" min-width="150" />
            <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
            <el-table-column prop="quota" label="名额" width="80" align="center" />
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="表彰提名" name="nomination">
          <el-form :inline="true" style="margin-bottom: 16px">
            <el-form-item label="批次ID"><el-input-number v-model="nominationSearch.batch_id" :min="0" style="width: 120px" /></el-form-item>
            <el-form-item label="状态">
              <el-select v-model="nominationSearch.status" placeholder="请选择" clearable style="width: 140px">
                <el-option label="待审核" value="pending" />
                <el-option label="审核中" value="reviewing" />
                <el-option label="已通过" value="approved" />
                <el-option label="已拒绝" value="rejected" />
                <el-option label="已获奖" value="won" />
              </el-select>
            </el-form-item>
            <el-form-item><el-button type="primary" @click="fetchNominations"><i-ep-search />搜索</el-button></el-form-item>
          </el-form>
          <el-table v-loading="nominationLoading" :data="nominationData" stripe border>
            <el-table-column type="index" label="序号" width="60" align="center" />
            <el-table-column prop="user_name" label="被提名姓名" width="100" />
            <el-table-column prop="nomination_reason" label="提名理由" min-width="200" show-overflow-tooltip />
            <el-table-column prop="status" label="状态" width="100" align="center">
              <template #default="{ row }"><el-tag :type="getStatusType(row.status)">{{ getStatusLabel(row.status) }}</el-tag></template>
            </el-table-column>
            <el-table-column prop="rank" label="名次" width="80" align="center">
              <template #default="{ row }">{{ row.rank || "-" }}</template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { AwardAPI, type AwardCategoryItem, type AwardNominationItem } from "@/api/module_campus_return/award";

const activeTab = ref("category");
const categoryLoading = ref(false);
const nominationLoading = ref(false);
const categoryData = ref<AwardCategoryItem[]>([]);
const nominationData = ref<AwardNominationItem[]>([]);
const categorySearch = reactive({ batch_id: undefined as number | undefined });
const nominationSearch = reactive({ batch_id: undefined as number | undefined, status: "" });

const getStatusType = (status: string) => ({ pending: "warning", reviewing: "primary", approved: "success", rejected: "danger", won: "warning" }[status] || "info");
const getStatusLabel = (status: string) => ({ pending: "待审核", reviewing: "审核中", approved: "已通过", rejected: "已拒绝", won: "已获奖" }[status] || status);

const fetchCategories = async () => {
  categoryLoading.value = true;
  try { categoryData.value = await AwardAPI.listCategories(categorySearch.batch_id) || []; }
  finally { categoryLoading.value = false; }
};

const fetchNominations = async () => {
  nominationLoading.value = true;
  try { nominationData.value = await AwardAPI.listNominations(nominationSearch) || []; }
  finally { nominationLoading.value = false; }
};

onMounted(() => { fetchCategories(); fetchNominations(); });
</script>

<style scoped>
</style>
