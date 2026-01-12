<!-- 字典数据 -->
<template>
  <el-drawer
    v-model="drawerVisible"
    :title="'【' + props.dictLabel + '】字典数据'"
    :size="drawerSize"
  >
    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form
        ref="queryFormRef"
        :model="queryFormData"
        :inline="true"
        label-suffix=":"
        @submit.prevent="handleQuery"
      >
        <el-form-item prop="dict_label" label="字典数据标签">
          <el-input v-model="queryFormData.dict_label" placeholder="请输入字典标签" clearable />
        </el-form-item>
        <el-form-item prop="status" label="状态">
          <el-select
            v-model="queryFormData.status"
            placeholder="请选择状态"
            style="width: 167.5px"
            clearable
          >
            <el-option value="0" label="启用" />
            <el-option value="1" label="停用" />
          </el-select>
        </el-form-item>
        <!-- 时间范围，收起状态下隐藏 -->
        <el-form-item v-if="isExpand" prop="start_time" label="创建时间">
          <DatePicker v-model="dateRange" @update:model-value="handleDateRangeChange" />
        </el-form-item>
        <!-- 查询、重置、展开/收起按钮 -->
        <el-form-item class="search-buttons">
          <el-button type="primary" icon="search" native-type="submit">查询</el-button>
          <el-button icon="refresh" @click="handleResetQuery">重置</el-button>
          <!-- 展开/收起 -->
          <template v-if="isExpandable">
            <el-link class="ml-3" type="primary" underline="never" @click="isExpand = !isExpand">
              {{ isExpand ? "收起" : "展开" }}
              <el-icon>
                <template v-if="isExpand">
                  <ArrowUp />
                </template>
                <template v-else>
                  <ArrowDown />
                </template>
              </el-icon>
            </el-link>
          </template>
        </el-form-item>
      </el-form>
    </div>

    <!-- 内容区域 -->
    <el-card class="data-table">
      <template #header>
        <div class="card-header">
          <span>
            <el-tooltip content="字典数据管理维护系统的字典数据。">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            字典数据列表
          </span>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--left">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_system:dict_data:create']"
                type="success"
                icon="plus"
                @click="handleOpenDialog('create')"
              >
                新增
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_system:dict_data:delete']"
                type="danger"
                icon="delete"
                :disabled="selectIds.length === 0"
                @click="handleDelete(selectIds)"
              >
                批量删除
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-dropdown v-hasPerm="['module_system:dict_data:patch']" trigger="click">
                <el-button type="default" :disabled="selectIds.length === 0" icon="ArrowDown">
                  更多
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item icon="Check" @click="handleMoreClick('0')">
                      批量启用
                    </el-dropdown-item>
                    <el-dropdown-item icon="CircleClose" @click="handleMoreClick('1')">
                      批量停用
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </el-col>
          </el-row>
        </div>
        <div class="data-table__toolbar--right">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-tooltip content="导出">
                <el-button
                  v-hasPerm="['module_system:dict_data:export']"
                  type="warning"
                  icon="download"
                  circle
                  @click="handleOpenExportsModal"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-tooltip content="刷新">
                <el-button type="default" icon="refresh" circle @click="handleRefresh" />
              </el-tooltip>
            </el-col>
          </el-row>
        </div>
      </div>

      <!-- 表格区域：系统配置列表 -->
      <el-table
        ref="dataTableRef"
        v-loading="loading"
        :data="pageTableData"
        highlight-current-row
        class="data-table__content"
        height="460"
        border
        stripe
        @selection-change="handleSelectionChange"
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column type="selection" min-width="55" align="center" />
        <el-table-column type="index" fixed label="序号" min-width="60">
          <template #default="scope">
            {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column label="标签" prop="dict_label" min-width="150" show-overflow-tooltip />
        <el-table-column label="状态" prop="status" min-width="100" show-overflow-tooltip>
          <template #default="scope">
            <el-tag :type="scope.row.status === '0' ? 'success' : 'danger'">
              {{ scope.row.status === "0" ? "启用" : "停用" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="类型" prop="dict_type" min-width="180" show-overflow-tooltip>
          <template #default="scope">
            <el-tag type="primary">{{ scope.row.dict_type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="值" prop="dict_value" min-width="100" show-overflow-tooltip />
        <el-table-column label="样式属性" prop="css_class" min-width="100" show-overflow-tooltip />
        <el-table-column
          label="列表类样式"
          prop="list_class"
          min-width="100"
          show-overflow-tooltip
        />
        <el-table-column label="排序" prop="dict_sort" min-width="60" />
        <el-table-column label="是否默认" prop="is_default" min-width="100">
          <template #default="scope">
            <el-tag v-if="scope.row.is_default" type="success">是</el-tag>
            <el-tag v-else type="danger">否</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="描述" prop="description" min-width="100" show-overflow-tooltip />
        <el-table-column label="创建时间" prop="created_time" min-width="200" sortable />
        <el-table-column label="更新时间" prop="updated_time" min-width="200" sortable />
        <el-table-column fixed="right" label="操作" align="center" min-width="200">
          <template #default="scope">
            <el-button
              v-hasPerm="['module_system:dict_data:detail']"
              type="info"
              size="small"
              link
              icon="document"
              @click="handleOpenDialog('detail', scope.row.id)"
            >
              详情
            </el-button>
            <el-button
              v-hasPerm="['module_system:dict_data:update']"
              type="primary"
              size="small"
              link
              icon="edit"
              @click="handleOpenDialog('update', scope.row.id)"
            >
              编辑
            </el-button>
            <el-button
              v-hasPerm="['module_system:dict_data:delete']"
              type="danger"
              size="small"
              link
              icon="delete"
              @click="handleDelete([scope.row.id])"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页区域 -->
      <template #footer>
        <pagination
          v-model:total="total"
          v-model:page="queryFormData.page_no"
          v-model:limit="queryFormData.page_size"
          @pagination="loadingData"
        />
      </template>
    </el-card>

    <!-- 弹窗区域 -->
    <el-dialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      @close="handleCloseDialog"
    >
      <!-- 详情 -->
      <template v-if="dialogVisible.type === 'detail'">
        <el-descriptions :column="4" border>
          <el-descriptions-item label="数据标签" :span="2">
            {{ detailFormData.dict_label }}
          </el-descriptions-item>
          <el-descriptions-item label="数据类型" :span="2">
            {{ detailFormData.dict_type }}
          </el-descriptions-item>
          <el-descriptions-item label="数据值" :span="2">
            {{ detailFormData.dict_value }}
          </el-descriptions-item>
          <el-descriptions-item label="样式属性" :span="2">
            {{ detailFormData.css_class }}
          </el-descriptions-item>
          <el-descriptions-item label="列表样式属性" :span="2">
            {{ detailFormData.list_class }}
          </el-descriptions-item>
          <el-descriptions-item label="是否默认" :span="2">
            <el-tag v-if="detailFormData.is_default" type="success">是</el-tag>
            <el-tag v-else type="danger">否</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态" :span="2">
            <el-tag v-if="detailFormData.status === '0'" type="success">启用</el-tag>
            <el-tag v-else type="danger">停用</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="排序" :span="2">
            {{ detailFormData.dict_sort }}
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">
            {{ detailFormData.description }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">
            {{ detailFormData.created_time }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间" :span="2">
            {{ detailFormData.updated_time }}
          </el-descriptions-item>
        </el-descriptions>
      </template>
      <!-- 新增、编辑表单 -->
      <template v-else>
        <el-form
          ref="dataFormRef"
          :model="formData"
          :rules="rules"
          label-suffix=":"
          label-width="auto"
          label-position="right"
        >
          <el-form-item label="数据类型" prop="dict_type">
            <el-input
              v-model="formData.dict_type"
              placeholder="请输入数据类型"
              :maxlength="50"
              :disabled="true"
            />
          </el-form-item>
          <el-form-item label="数据标签" prop="dict_label">
            <el-input v-model="formData.dict_label" placeholder="请输入数据标签" :maxlength="255" />
          </el-form-item>
          <el-form-item label="数据值" prop="dict_value">
            <el-input v-model="formData.dict_value" placeholder="请输入数据值" :maxlength="255" />
          </el-form-item>
          <el-form-item label="样式属性" prop="css_class">
            <el-select
              v-model="formData.css_class"
              placeholder="请选择常用颜色或输入自定义"
              clearable
              filterable
              allow-create
              default-first-option
            >
              <!-- Element Plus 常用主题色（十六进制） -->
              <el-option value="#409EFF" label="蓝色-Primary (#409EFF)" />
              <el-option value="#67C23A" label="绿色-Success (#67C23A)" />
              <el-option value="#E6A23C" label="橙色-Warning (#E6A23C)" />
              <el-option value="#F56C6C" label="红色-Danger (#F56C6C)" />
              <el-option value="#909399" label="灰色-Info (#909399)" />
              <!-- 文本常用颜色 -->
              <el-option value="#303133" label="深灰-文本主要 (#303133)" />
              <el-option value="#606266" label="灰色-文本常规 (#606266)" />
              <el-option value="#C0C4CC" label="浅灰-占位文本 (#C0C4CC)" />
              <!-- 基础色 -->
              <el-option value="#000000" label="黑色 (#000000)" />
              <el-option value="#FFFFFF" label="白色 (#FFFFFF)" />
            </el-select>
          </el-form-item>
          <el-form-item label="列表类样式" prop="list_class">
            <el-select v-model="formData.list_class" placeholder="请选择列表类样式" clearable>
              <el-option value="default" label="默认(default)" />
              <el-option value="primary" label="主要(primary)" />
              <el-option value="success" label="成功(success)" />
              <el-option value="warning" label="警告(warning)" />
              <el-option value="danger" label="危险(danger)" />
              <el-option value="info" label="信息(info)" />
            </el-select>
          </el-form-item>
          <el-form-item label="是否默认" prop="is_default">
            <el-radio-group v-model="formData.is_default">
              <el-radio :value="true">是</el-radio>
              <el-radio :value="false">否</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="排序" prop="dict_sort">
            <el-input-number v-model="formData.dict_sort" controls-position="right" :min="1" />
          </el-form-item>
          <el-form-item label="状态" prop="status">
            <el-switch
              v-model="formData.status"
              inline-prompt
              :active-value="'0'"
              :inactive-value="'1'"
            />
          </el-form-item>

          <el-form-item label="描述" prop="description">
            <el-input
              v-model="formData.description"
              :rows="4"
              :maxlength="100"
              show-word-limit
              type="textarea"
              placeholder="请输入描述"
            />
          </el-form-item>
        </el-form>
      </template>

      <template #footer>
        <div class="dialog-footer">
          <!-- 详情弹窗不需要确定按钮的提交逻辑 -->
          <el-button @click="handleCloseDialog">取消</el-button>
          <el-button v-if="dialogVisible.type !== 'detail'" type="primary" @click="handleSubmit">
            确定
          </el-button>
          <el-button v-else type="primary" @click="handleCloseDialog">确定</el-button>
        </div>
      </template>
    </el-dialog>
  </el-drawer>
  <ExportModal
    v-model="exportsDialogVisible"
    :content-config="curdContentConfig"
    :query-params="queryFormData"
    :page-data="pageTableData"
    :selection-data="selectionRows"
  />
</template>

<script setup lang="ts">
// 添加 props 来接收 dictType
const props = defineProps({
  dictType: {
    type: String,
    required: true,
  },
  dictLabel: {
    type: String,
    required: true,
  },
  dictTypeId: {
    type: Number,
    required: true,
  },
});

const drawerVisible = defineModel<boolean>();
import DictAPI, { DictDataTable, DictDataForm, DictDataPageQuery } from "@/api/module_system/dict";
import { useAppStore } from "@/store/modules/app.store";
import { DeviceEnum } from "@/enums/settings/device.enum";
import ExportModal from "@/components/CURD/ExportModal.vue";
import type { IContentConfig } from "@/components/CURD/types";
import { formatToDateTime } from "@/utils/dateUtil";

const appStore = useAppStore();
const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "80%" : "60%"));

const queryFormRef = ref();
const dataFormRef = ref();
const total = ref(0);
const selectIds = ref<number[]>([]);
const loading = ref(false);

const isExpand = ref(false);
const isExpandable = ref(true);

// 分页表单
const pageTableData = ref<DictDataTable[]>([]);

// 导出弹窗显示状态 & 选中行
const exportsDialogVisible = ref(false);
const selectionRows = ref<DictDataTable[]>([]);

// 详情表单
const detailFormData = ref<DictDataTable>({});

// 分页查询参数
const queryFormData = reactive<DictDataPageQuery>({
  page_no: 1,
  page_size: 10,
  dict_label: undefined,
  dict_type: props.dictType,
  status: undefined,
  created_time: undefined,
  updated_time: undefined,
});

// 编辑表单
const formData = reactive<DictDataForm>({
  id: undefined,
  dict_sort: 1,
  dict_label: "",
  dict_value: "",
  dict_type: "",
  css_class: "",
  list_class: undefined,
  is_default: false,
  status: "0",
  description: "",
  dict_type_id: undefined,
});

// 弹窗状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

// 表单验证规则
const rules = reactive({
  dict_label: [{ required: true, message: "请输入字典标签", trigger: "blur" }],
  dict_type: [{ required: true, message: "请输入字典类型", trigger: "blur" }],
  dict_value: [{ required: true, message: "请输入字典键值", trigger: "blur" }],
  status: [{ required: true, message: "请选择状态", trigger: "blur" }],
  dict_sort: [{ required: true, message: "请输入排序", trigger: "blur" }],
  // css_class: [{ required: true, message: "请输入样式类名", trigger: "blur" }],
  // list_class: [{ required: true, message: "请输入列表类名", trigger: "blur" }],
  is_default: [{ required: true, message: "请选择是否默认", trigger: "blur" }],
});

// 日期范围临时变量
const dateRange = ref<[Date, Date] | []>([]);

// 处理日期范围变化
function handleDateRangeChange(range: [Date, Date]) {
  dateRange.value = range;
  if (range && range.length === 2) {
    queryFormData.created_time = [formatToDateTime(range[0]), formatToDateTime(range[1])];
  } else {
    queryFormData.created_time = undefined;
  }
}

// 列表刷新
async function handleRefresh() {
  await loadingData();
}

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    // 在查询参数中添加 dictType
    const response = await DictAPI.listDictData(queryFormData);
    pageTableData.value = response.data.data.items;
    total.value = response.data.data.total;
  } catch (error: any) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

// 查询（重置页码后获取数据）
async function handleQuery() {
  queryFormData.page_no = 1;
  loadingData();
}

// 重置查询
async function handleResetQuery() {
  queryFormRef.value.resetFields();
  queryFormData.page_no = 1;
  // 额外清空日期范围与时间查询参数
  dateRange.value = [];
  queryFormData.created_time = undefined;
  loadingData();
}

// 定义初始表单数据常量
const initialFormData: DictDataForm = {
  id: undefined,
  dict_sort: 1,
  dict_label: "",
  dict_value: "",
  dict_type: "",
  css_class: "",
  list_class: undefined,
  is_default: false,
  status: "0",
  description: "",
  dict_type_id: props.dictTypeId,
};

// 重置表单
async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  // 完全重置 formData 为初始状态
  Object.assign(formData, initialFormData);
}

// 行复选框选中项变化
async function handleSelectionChange(selection: any) {
  selectIds.value = selection.map((item: any) => item.id);
  selectionRows.value = selection;
}

// 关闭弹窗
async function handleCloseDialog() {
  dialogVisible.visible = false;
  resetForm();
}

// 打开系统配置弹窗
async function handleOpenDialog(type: "create" | "update" | "detail", id?: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await DictAPI.detailDictData(id);
    if (type === "detail") {
      dialogVisible.title = "字典数据详情";
      Object.assign(detailFormData.value, response.data.data);
    } else if (type === "update") {
      dialogVisible.title = "修改字典数据";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增字典数据";
    // 重置为初始值并确保状态默认开启
    Object.assign(formData, initialFormData);
    formData.dict_type = props.dictType;
    formData.status = "0";
    formData.id = undefined;
  }
  dialogVisible.visible = true;
}

// 新增、编辑弹窗处理
async function handleSubmit() {
  // 表单校验
  dataFormRef.value.validate(async (valid: any) => {
    if (valid) {
      loading.value = true;
      // 根据弹窗传入的参数(deatil\create\update)判断走什么逻辑
      const id = formData.id;
      if (id) {
        try {
          await DictAPI.updateDictData(id, { id, ...formData });
          dialogVisible.visible = false;
          resetForm();
          handleResetQuery();
        } catch (error: any) {
          console.error(error);
        } finally {
          loading.value = false;
        }
      } else {
        try {
          await DictAPI.createDictData(formData);
          dialogVisible.visible = false;
          resetForm();
          handleResetQuery();
        } catch (error: any) {
          console.error(error);
        } finally {
          loading.value = false;
        }
      }
    }
  });
}

// 删除、批量删除
async function handleDelete(ids: number[]) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        loading.value = true;
        await DictAPI.deleteDictData(ids);
        handleResetQuery();
      } catch (error: any) {
        console.error(error);
      } finally {
        loading.value = false;
      }
    })
    .catch(() => {
      ElMessageBox.close();
    });
}

// 打开导出弹窗
function handleOpenExportsModal() {
  exportsDialogVisible.value = true;
}

// 批量启用/停用
async function handleMoreClick(status: string) {
  if (selectIds.value.length) {
    ElMessageBox.confirm(`确认${status === "0" ? "启用" : "停用"}该项数据?`, "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    })
      .then(async () => {
        try {
          loading.value = true;
          await DictAPI.batchDictData({ ids: selectIds.value, status });
          handleResetQuery();
        } catch (error: any) {
          console.error(error);
        } finally {
          loading.value = false;
        }
      })
      .catch(() => {
        ElMessageBox.close();
      });
  }
}

// 导出字段
const exportColumns = [
  { prop: "dict_label", label: "数据标签" },
  { prop: "dict_type", label: "数据类型" },
  { prop: "dict_value", label: "数据值" },
  { prop: "css_class", label: "样式属性" },
  { prop: "list_class", label: "列表类样式" },
  { prop: "dict_sort", label: "排序" },
  { prop: "is_default", label: "是否默认" },
  { prop: "status", label: "状态" },
  { prop: "description", label: "描述" },
  { prop: "created_time", label: "创建时间" },
  { prop: "updated_time", label: "更新时间" },
];

// 导出配置（用于导出弹窗）
const curdContentConfig = {
  permPrefix: "module_system:dict_data",
  cols: exportColumns as any,
  exportsAction: async (params: any) => {
    const query: any = { ...params };
    query.page_no = 1;
    query.page_size = 1000;
    const all: any[] = [];
    while (true) {
      const res = await DictAPI.listDictData(query);
      const items = res.data?.data?.items || [];
      const total = res.data?.data?.total || 0;
      all.push(...items);
      if (all.length >= total || items.length === 0) break;
      query.page_no += 1;
    }
    return all;
  },
} as unknown as IContentConfig;

onMounted(() => {
  loadingData();
});
</script>

<style lang="scss" scoped></style>
