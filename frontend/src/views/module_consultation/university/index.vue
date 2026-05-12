<!-- 招生咨询会 - 高校信息管理 -->
<template>
  <div class="app-container">
    <el-card class="search-card" shadow="never">
      <el-form ref="searchFormRef" :model="searchForm" :inline="true" label-width="80px">
        <el-form-item label="高校名称" prop="name">
          <el-input
            v-model="searchForm.name"
            placeholder="请输入高校名称"
            clearable
            style="width: 180px"
          />
        </el-form-item>
        <el-form-item label="高校代码" prop="code">
          <el-input
            v-model="searchForm.code"
            placeholder="请输入高校代码"
            clearable
            style="width: 150px"
          />
        </el-form-item>
        <el-form-item label="省份" prop="province">
          <el-input
            v-model="searchForm.province"
            placeholder="请输入省份"
            clearable
            style="width: 120px"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select
            v-model="searchForm.status"
            placeholder="请选择状态"
            clearable
            style="width: 120px"
          >
            <el-option label="启用" value="active" />
            <el-option label="停用" value="inactive" />
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
          <span class="title">高校信息列表</span>
          <div class="operations">
            <el-button
              v-permission="['module_consultation:university:create']"
              type="primary"
              @click="handleCreate"
            >
              <i-ep-plus />
              新增
            </el-button>
            <el-button
              v-permission="['module_consultation:university:delete']"
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
        <el-table-column prop="name" label="高校名称" min-width="180" show-overflow-tooltip />
        <el-table-column prop="code" label="高校代码" width="120" />
        <el-table-column prop="abbreviation" label="简称" width="100" />
        <el-table-column prop="province" label="省份" width="100" />
        <el-table-column prop="city" label="城市" width="100" />
        <el-table-column prop="contact_person" label="联系人" width="100" />
        <el-table-column prop="contact_phone" label="联系电话" width="130" />
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'">
              {{ row.status === 'active' ? '启用' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_time" label="创建时间" width="160" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              v-permission="['module_consultation:university:detail']"
              link
              type="primary"
              @click="handleView(row)"
            >
              详情
            </el-button>
            <el-button
              v-permission="['module_consultation:university:update']"
              link
              type="primary"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              v-permission="['module_consultation:university:delete']"
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
    <el-dialog v-model="detailDialog.visible" title="高校详情" width="600px">
      <el-descriptions v-if="detailDialog.data" :column="2" border>
        <el-descriptions-item label="高校名称" :span="2">
          {{ detailDialog.data.name }}
        </el-descriptions-item>
        <el-descriptions-item label="高校代码">
          {{ detailDialog.data.code || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="简称">
          {{ detailDialog.data.abbreviation || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="省份">
          {{ detailDialog.data.province || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="城市">
          {{ detailDialog.data.city || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="详细地址" :span="2">
          {{ detailDialog.data.address || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="联系人">
          {{ detailDialog.data.contact_person || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="联系电话">
          {{ detailDialog.data.contact_phone || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="联系邮箱" :span="2">
          {{ detailDialog.data.contact_email || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="官网链接" :span="2">
          {{ detailDialog.data.website || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="detailDialog.data.status === 'active' ? 'success' : 'info'">
            {{ detailDialog.data.status === 'active' ? '启用' : '停用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">
          {{ detailDialog.data.created_time || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="高校简介" :span="2">
          {{ detailDialog.data.description || '-' }}
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 新增/编辑弹窗 -->
    <el-dialog
      v-model="formDialog.visible"
      :title="formDialog.type === 'create' ? '新增高校' : '编辑高校'"
      width="600px"
    >
      <el-form ref="formRef" :model="form" :rules="formRules" label-width="100px">
        <el-form-item label="高校名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入高校名称" />
        </el-form-item>
        <el-form-item label="高校代码" prop="code">
          <el-input v-model="form.code" placeholder="请输入高校代码" />
        </el-form-item>
        <el-form-item label="简称" prop="abbreviation">
          <el-input v-model="form.abbreviation" placeholder="请输入简称" />
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
        <el-form-item label="省份" prop="province">
          <el-input v-model="form.province" placeholder="请输入省份" />
        </el-form-item>
        <el-form-item label="城市" prop="city">
          <el-input v-model="form.city" placeholder="请输入城市" />
        </el-form-item>
        <el-form-item label="详细地址" prop="address">
          <el-input v-model="form.address" placeholder="请输入详细地址" />
        </el-form-item>
        <el-form-item label="官网链接" prop="website">
          <el-input v-model="form.website" placeholder="请输入官网链接" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio label="active">启用</el-radio>
            <el-radio label="inactive">停用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="高校简介" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入高校简介"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="formDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";
import UniversityAPI from "@/api/module_consultation/university";
import type { UniversityItem, UniversityForm, UniversityQuery } from "@/api/module_consultation/university";

const searchForm = reactive<UniversityQuery>({
  name: undefined,
  code: undefined,
  province: undefined,
  status: undefined,
});

const loading = ref(false);
const tableData = ref<UniversityItem[]>([]);
const selectedIds = ref<number[]>([]);
const pagination = reactive({ page: 1, pageSize: 10, total: 0 });

const formDialog = reactive({
  visible: false,
  type: "create" as "create" | "edit",
  id: undefined as number | undefined,
});

const form = reactive<UniversityForm>({
  name: "",
  code: "",
  abbreviation: "",
  contact_person: "",
  contact_phone: "",
  contact_email: "",
  province: "",
  city: "",
  address: "",
  description: "",
  website: "",
  status: "active",
});

const formRef = ref<FormInstance>();

const formRules: FormRules = {
  name: [{ required: true, message: "请输入高校名称", trigger: "blur" }],
};

const detailDialog = reactive({
  visible: false,
  data: null as UniversityItem | null,
});

const fetchList = async () => {
  loading.value = true;
  try {
    const res = await UniversityAPI.getList({
      page: pagination.page,
      pageSize: pagination.pageSize,
      ...searchForm,
    });
    if (res.data?.data) {
      const result = res.data.data;
      tableData.value = result.items || [];
      pagination.total = result.total || 0;
    }
  } catch (error) {
    console.error("获取高校列表失败:", error);
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
    name: undefined,
    code: undefined,
    province: undefined,
    status: undefined,
  });
  pagination.page = 1;
  fetchList();
};

const handleSelectionChange = (selection: UniversityItem[]) => {
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

const resetForm = () => {
  Object.assign(form, {
    name: "",
    code: "",
    abbreviation: "",
    contact_person: "",
    contact_phone: "",
    contact_email: "",
    province: "",
    city: "",
    address: "",
    description: "",
    website: "",
    status: "active",
  });
};

const handleCreate = () => {
  formDialog.type = "create";
  formDialog.id = undefined;
  resetForm();
  formDialog.visible = true;
};

const handleEdit = (row: UniversityItem) => {
  formDialog.type = "edit";
  formDialog.id = row.id;
  Object.assign(form, {
    name: row.name,
    code: row.code || "",
    abbreviation: row.abbreviation || "",
    contact_person: row.contact_person || "",
    contact_phone: row.contact_phone || "",
    contact_email: row.contact_email || "",
    province: row.province || "",
    city: row.city || "",
    address: row.address || "",
    description: row.description || "",
    website: row.website || "",
    status: row.status,
  });
  formDialog.visible = true;
};

const handleSubmit = async () => {
  if (!formRef.value) return;
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (formDialog.type === "create") {
          await UniversityAPI.create(form);
          ElMessage.success("创建成功");
        } else {
          await UniversityAPI.update(formDialog.id!, form);
          ElMessage.success("更新成功");
        }
        formDialog.visible = false;
        fetchList();
      } catch (error) {
        console.error("提交失败:", error);
      }
    }
  });
};

const handleView = async (row: UniversityItem) => {
  try {
    const res = await UniversityAPI.getDetail(row.id!);
    if (res.data?.data) {
      detailDialog.data = res.data.data;
      detailDialog.visible = true;
    }
  } catch (error) {
    console.error("获取详情失败:", error);
  }
};

const handleDelete = (row: UniversityItem) => {
  ElMessageBox.confirm(`确定删除高校 "${row.name}" 吗？`, "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        await UniversityAPI.delete(row.id!);
        ElMessage.success("删除成功");
        fetchList();
      } catch (error) {
        console.error("删除失败:", error);
      }
    })
    .catch(() => {});
};

const handleBatchDelete = () => {
  if (!selectedIds.value.length) return;
  ElMessageBox.confirm(`确定删除选中的 ${selectedIds.value.length} 条记录吗？`, "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        for (const id of selectedIds.value) {
          await UniversityAPI.delete(id);
        }
        ElMessage.success("批量删除成功");
        fetchList();
      } catch (error) {
        console.error("批量删除失败:", error);
      }
    })
    .catch(() => {});
};

onMounted(() => {
  fetchList();
});
</script>

<style scoped>
.search-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 16px;
  font-weight: bold;
}

.operations {
  display: flex;
  gap: 10px;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
