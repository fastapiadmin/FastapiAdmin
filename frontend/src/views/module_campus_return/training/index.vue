<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="批次ID">
          <el-input-number v-model="searchForm.batch_id" :min="0" style="width: 120px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData"><i-ep-search />搜索</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">培训课程列表</span>
          <el-button v-permission="['module_campus_return:training:create']" type="primary" @click="showForm = true">
            <i-ep-plus />创建课程
          </el-button>
        </div>
      </template>

      <el-table v-loading="loading" :data="tableData" stripe border>
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="course_name" label="课程名称" min-width="180" />
        <el-table-column prop="duration" label="时长(分钟)" width="100" align="center" />
        <el-table-column prop="is_required" label="必修" width="80" align="center">
          <template #default="{ row }">{{ row.is_required ? "是" : "否" }}</template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="80" align="center">
          <template #default="{ row }"><el-tag :type="row.is_active ? 'success' : 'info'">{{ row.is_active ? '启用' : '禁用' }}</el-tag></template>
        </el-table-column>
        <el-table-column prop="created_time" label="创建时间" width="160" />
      </el-table>
    </el-card>

    <el-dialog v-model="showForm" title="创建课程" width="550px">
      <el-form ref="formRef" :model="form" label-width="100px">
        <el-form-item label="批次ID" prop="batch_id"><el-input-number v-model="form.batch_id" :min="1" style="width: 100%" /></el-form-item>
        <el-form-item label="课程名称" prop="course_name"><el-input v-model="form.course_name" placeholder="请输入" /></el-form-item>
        <el-form-item label="课程描述"><el-input v-model="form.description" type="textarea" :rows="3" /></el-form-item>
        <el-form-item label="视频URL"><el-input v-model="form.video_url" placeholder="请输入视频链接" /></el-form-item>
        <el-form-item label="时长(分钟)"><el-input-number v-model="form.duration" :min="0" style="width: 100%" /></el-form-item>
        <el-form-item label="是否必修"><el-switch v-model="form.is_required" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showForm = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
import { ElMessage } from "element-plus";
import { TrainingAPI, type TrainingCourseItem, type TrainingCourseForm } from "@/api/module_campus_return/training";

const loading = ref(false);
const tableData = ref<TrainingCourseItem[]>([]);
const showForm = ref(false);
const formRef = ref();
const searchForm = reactive({ batch_id: undefined as number | undefined });
const form = reactive<TrainingCourseForm & { is_required: boolean }>({ batch_id: 0, course_name: "", description: "", video_url: "", duration: 0, is_required: true });

const fetchData = async () => {
  loading.value = true;
  try { tableData.value = await TrainingAPI.listCourses(searchForm.batch_id) || []; }
  finally { loading.value = false; }
};

const handleSubmit = async () => {
  await TrainingAPI.createCourse(form);
  ElMessage.success("创建成功");
  showForm.value = false;
  fetchData();
};

onMounted(() => { fetchData(); });
</script>

<style scoped>
.search-card { margin-bottom: 16px; }
.table-card { margin-bottom: 16px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.title { font-weight: 600; }
</style>
