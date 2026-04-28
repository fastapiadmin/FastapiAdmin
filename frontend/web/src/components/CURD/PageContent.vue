<template>
  <el-card
    class="data-table flex-1 min-h-0"
    :shadow="config.cardShadow ?? 'never'"
    :class="contentConfig.cardClass"
    :body-style="cardBodyStyle"
  >
    <template v-if="slots.header" #header>
      <slot name="header" />
    </template>
    <!-- 表格工具栏：#toolbar 可完全自定义；默认左右分栏 -->
    <div
      v-if="
        config.showToolbar !== false &&
        (slots.toolbar || toolbarLeftBtn.length > 0 || toolbarRightBtn.length > 0)
      "
      class="data-table__toolbar"
    >
      <slot
        name="toolbar"
        :toolbar-left="toolbarLeftBtn"
        :toolbar-right="toolbarRightBtn"
        :on-toolbar="handleToolbar"
        :remove-ids="removeIds"
        :cols="cols"
      >
        <CrudToolbarLeft
          v-if="toolbarLeftBtn.length > 0"
          :remove-ids="removeIds"
          :config-buttons="toolbarLeftBtn"
          @toolbar="handleToolbar"
        />
        <div class="data-table__toolbar--right">
          <CrudToolbarRight :buttons="toolbarRightBtn" :cols="cols" :on-toolbar="handleToolbar" />
        </div>
      </slot>
    </div>

    <!-- 列表：默认内置 el-table；传入 #table 插槽可完全自定义（普通表 / 树表等） -->
    <div class="data-table__content">
      <slot
        name="table"
        :data="pageData"
        :loading="loading"
        :table-ref="tableRef"
        :on-selection-change="handleSelectionChange"
        :pagination="pagination"
      >
        <el-table
          ref="tableRef"
          v-loading="loading"
          v-bind="contentConfig.table"
          :data="pageData"
          :row-key="pk"
          class="flex-1"
          @selection-change="handleSelectionChange"
          @filter-change="handleFilterChange"
        >
          <template v-for="col in cols" :key="col.prop">
            <el-table-column v-if="col.show" v-bind="col">
              <template #default="scope">
                <!-- 显示图片 -->
                <template v-if="col.templet === 'image'">
                  <template v-if="col.prop">
                    <template v-if="Array.isArray(scope.row[col.prop])">
                      <template v-for="(item, index) in scope.row[col.prop]" :key="item">
                        <el-image
                          :src="item"
                          :preview-src-list="scope.row[col.prop]"
                          :initial-index="Number(index)"
                          :preview-teleported="true"
                          :style="`width: ${col.imageWidth ?? 40}px; height: ${col.imageHeight ?? 40}px`"
                        />
                      </template>
                    </template>
                    <template v-else>
                      <el-image
                        :src="scope.row[col.prop]"
                        :preview-src-list="[scope.row[col.prop]]"
                        :preview-teleported="true"
                        :style="`width: ${col.imageWidth ?? 40}px; height: ${col.imageHeight ?? 40}px`"
                      />
                    </template>
                  </template>
                </template>
                <!-- 根据行的selectList属性返回对应列表值 -->
                <template v-else-if="col.templet === 'list'">
                  <template v-if="col.prop">
                    {{ (col.selectList ?? {})[scope.row[col.prop]] }}
                  </template>
                </template>
                <!-- 格式化显示链接 -->
                <template v-else-if="col.templet === 'url'">
                  <template v-if="col.prop">
                    <el-link type="primary" :href="scope.row[col.prop]" target="_blank">
                      {{ scope.row[col.prop] }}
                    </el-link>
                  </template>
                </template>
                <!-- 生成开关组件 -->
                <template v-else-if="col.templet === 'switch'">
                  <template v-if="col.prop">
                    <!-- pageData.length>0: 解决el-switch组件会在表格初始化的时候触发一次change事件 -->
                    <el-switch
                      v-model="scope.row[col.prop]"
                      :active-value="col.activeValue ?? 1"
                      :inactive-value="col.inactiveValue ?? 0"
                      :inline-prompt="true"
                      :active-text="col.activeText ?? ''"
                      :inactive-text="col.inactiveText ?? ''"
                      :validate-event="false"
                      :disabled="col.disabled"
                      @change="
                        pageData.length > 0 &&
                        handleModify(col.prop, scope.row[col.prop], scope.row)
                      "
                    />
                  </template>
                </template>
                <!-- 生成输入框组件 -->
                <template v-else-if="col.templet === 'input'">
                  <template v-if="col.prop">
                    <el-input
                      v-model="scope.row[col.prop]"
                      :type="col.inputType ?? 'text'"
                      :disabled="col.disabled"
                      @blur="handleModify(col.prop, scope.row[col.prop], scope.row)"
                    />
                  </template>
                </template>
                <!-- 格式化为价格 -->
                <template v-else-if="col.templet === 'price'">
                  <template v-if="col.prop">
                    {{ `${col.priceFormat ?? '￥'}${scope.row[col.prop]}` }}
                  </template>
                </template>
                <!-- 格式化为百分比 -->
                <template v-else-if="col.templet === 'percent'">
                  <template v-if="col.prop">{{ scope.row[col.prop] }}%</template>
                </template>
                <!-- 显示图标 -->
                <template v-else-if="col.templet === 'icon'">
                  <template v-if="col.prop">
                    <template v-if="scope.row[col.prop].startsWith('el-icon-')">
                      <el-icon>
                        <component :is="scope.row[col.prop].replace('el-icon-', '')" />
                      </el-icon>
                    </template>
                    <template v-else>
                      <div class="i-svg:{{ scope.row[col.prop] }}" />
                    </template>
                  </template>
                </template>
                <!-- 格式化时间 -->
                <template v-else-if="col.templet === 'date'">
                  <template v-if="col.prop">
                    {{
                      scope.row[col.prop]
                        ? useDateFormat(
                            scope.row[col.prop],
                            col.dateFormat ?? 'YYYY-MM-DD HH:mm:ss'
                          ).value
                        : ''
                    }}
                  </template>
                </template>
                <!-- 列操作栏 -->
                <template v-else-if="col.templet === 'tool'">
                  <template v-for="(btn, index) in tableToolbarBtn" :key="index">
                    <el-button
                      v-if="btn.render === undefined || btn.render(scope.row)"
                      v-hasPerm="btn.perm ?? '*:*:*'"
                      v-bind="btn.attrs"
                      @click="
                        handleOperate({
                          name: btn.name,
                          row: scope.row,
                          column: scope.column,
                          $index: scope.$index,
                        })
                      "
                    >
                      {{ btn.text }}
                    </el-button>
                  </template>
                </template>
                <!-- 自定义 -->
                <template v-else-if="col.templet === 'custom'">
                  <slot :name="col.slotName ?? col.prop" :prop="col.prop" v-bind="scope" />
                </template>
              </template>
            </el-table-column>
          </template>
        </el-table>
      </slot>
    </div>

    <template v-if="showPagination" #footer>
      <el-scrollbar :class="['h-8!', { 'flex-x-end': contentConfig?.pagePosition === 'right' }]">
        <el-pagination
          v-bind="pagination"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </el-scrollbar>
    </template>

    <!-- 导出弹窗 -->
    <EnhancedDialog
      v-model="exportsModalVisible"
      title="导出数据"
      width="600px"
      dialog-class="curd-embed-dialog"
      modal-class="curd-embed-dialog"
      @close="handleCloseExportsModal"
    >
      <!-- 滚动 -->
      <el-scrollbar max-height="60vh">
        <!-- 表单 -->
        <el-form
          ref="exportsFormRef"
          style="padding-right: var(--el-dialog-padding-primary)"
          :model="exportsFormData"
          :rules="exportsFormRules"
        >
          <el-form-item label="文件名" prop="filename">
            <el-input v-model="exportsFormData.filename" clearable />
          </el-form-item>
          <el-form-item label="工作表名" prop="sheetname">
            <el-input v-model="exportsFormData.sheetname" clearable />
          </el-form-item>
          <el-form-item label="数据源" prop="origin">
            <el-select v-model="exportsFormData.origin">
              <el-option label="当前数据 (当前页的数据)" :value="ExportsOriginEnum.CURRENT" />
              <el-option
                label="选中数据 (所有选中的数据)"
                :value="ExportsOriginEnum.SELECTED"
                :disabled="selectionData.length <= 0"
              />
              <el-option
                label="全量数据 (所有分页的数据)"
                :value="ExportsOriginEnum.REMOTE"
                :disabled="contentConfig.exportsAction === undefined"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="字段" prop="fields">
            <el-checkbox-group v-model="exportsFormData.fields">
              <template v-for="col in cols" :key="col.prop">
                <el-checkbox v-if="col.prop" :value="col.prop" :label="col.label" />
              </template>
            </el-checkbox-group>
          </el-form-item>
        </el-form>
      </el-scrollbar>
      <!-- 弹窗底部操作按钮 -->
      <template #footer>
        <div style="padding-right: var(--el-dialog-padding-primary)">
          <el-button type="primary" @click="handleExportsSubmit">确 定</el-button>
          <el-button @click="handleCloseExportsModal">取 消</el-button>
        </div>
      </template>
    </EnhancedDialog>
    <!-- 导入弹窗 -->
    <EnhancedDialog
      v-model="importModalVisible"
      title="导入数据"
      width="600px"
      dialog-class="curd-embed-dialog"
      modal-class="curd-embed-dialog"
      @close="handleCloseImportModal"
    >
      <!-- 滚动 -->
      <el-scrollbar max-height="60vh">
        <!-- 表单 -->
        <el-form
          ref="importFormRef"
          style="padding-right: var(--el-dialog-padding-primary)"
          :model="importFormData"
          :rules="importFormRules"
        >
          <el-form-item label="文件名" prop="files">
            <el-upload
              ref="uploadRef"
              v-model:file-list="importFormData.files"
              class="w-full"
              accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
              :drag="true"
              :limit="1"
              :auto-upload="false"
              :on-exceed="handleFileExceed"
            >
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                <span>将文件拖到此处，或</span>
                <em>点击上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  *.xlsx / *.xls
                  <el-link
                    v-if="contentConfig.importTemplate"
                    type="primary"
                    icon="download"
                    underline="never"
                    @click="handleDownloadTemplate"
                  >
                    下载模板
                  </el-link>
                </div>
              </template>
            </el-upload>
          </el-form-item>
        </el-form>
      </el-scrollbar>
      <!-- 弹窗底部操作按钮 -->
      <template #footer>
        <div style="padding-right: var(--el-dialog-padding-primary)">
          <el-button
            type="primary"
            :disabled="importFormData.files.length === 0"
            @click="handleImportSubmit"
          >
            确 定
          </el-button>
          <el-button @click="handleCloseImportModal">取 消</el-button>
        </div>
      </template>
    </EnhancedDialog>
  </el-card>
</template>

<script setup lang="ts">
  import { useDateFormat, useThrottleFn } from '@vueuse/core';
  import {
    ElMessage,
    genFileId,
    type FormInstance,
    type FormRules,
    type UploadInstance,
    type UploadRawFile,
    type UploadUserFile,
    type TableInstance,
  } from 'element-plus';
  import ExcelJS from 'exceljs';
  import { reactive, ref, computed, nextTick, useSlots } from 'vue';
  import CrudToolbarLeft from './CrudToolbarLeft.vue';
  import CrudToolbarRight from './CrudToolbarRight.vue';
  import EnhancedDialog from './EnhancedDialog.vue';
  import type { IContentConfig, IObject, IOperateData } from './types';
  import type { IToolsButton } from './types';

  const slots = useSlots();

  const cardBodyStyle = {
    display: 'flex',
    flex: 1,
    flexDirection: 'column' as const,
    minHeight: 0,
    overflow: 'hidden',
    padding: '16px 20px',
  };

  // 定义接收的属性
  const props = defineProps<{ contentConfig: IContentConfig }>();
  // 定义自定义事件
  const emit = defineEmits<{
    addClick: [];
    exportClick: [];
    toolbarClick: [name: string];
    editClick: [row: IObject];
    filterChange: [data: IObject];
    operateClick: [data: IOperateData];
  }>();

  // 表格工具栏按钮配置
  const config = computed(() => props.contentConfig);
  const buttonConfig = reactive<Record<string, IObject>>({
    add: { text: '新增', attrs: { icon: 'plus', type: 'success' }, perm: 'create' },
    delete: { text: '删除', attrs: { icon: 'delete', type: 'danger' }, perm: 'delete' },
    patch: { text: '批量修改', attrs: { icon: 'edit', type: 'warning' }, perm: 'patch' },
    import: { text: '导入', attrs: { icon: 'upload', type: 'info' }, perm: 'import' },
    export: { text: '导出', attrs: { icon: 'download', type: 'warning' }, perm: 'export' },
    refresh: { text: '刷新', attrs: { icon: 'refresh', type: 'success' }, perm: '*:*:*' },
    filter: { text: '筛选列', attrs: { icon: 'operation', type: 'danger' }, perm: '*:*:*' },
    view: { text: '详情', attrs: { icon: 'view', type: 'primary' }, perm: 'detail' },
    edit: { text: '编辑', attrs: { icon: 'edit', type: 'primary' }, perm: 'update' },
  });

  // 主键
  const pk = props.contentConfig.pk ?? 'id';
  // 权限名称前缀
  const authPrefix = computed(() => props.contentConfig.permPrefix);

  // 获取按钮权限标识
  function getButtonPerm(action: string): string | null {
    // 如果action已经包含完整路径(包含冒号)，则直接使用
    if (action.includes(':')) {
      return action;
    }
    // 否则使用权限前缀组合
    return authPrefix.value ? `${authPrefix.value}:${action}` : null;
  }

  // 检查是否有权限
  // function hasButtonPerm(action: string): boolean {
  //   const perm = getButtonPerm(action);
  //   // 如果没有设置权限标识，则默认具有权限
  //   if (!perm) return true;
  //   return hasAuth(perm);
  // }

  // 创建工具栏按钮
  function createToolbar(toolbar: Array<string | IToolsButton>, attr = {}) {
    return toolbar.map((item) => {
      const isString = typeof item === 'string';
      const name = isString ? item : item?.name || '';
      const base = (isString ? buttonConfig[item] : buttonConfig[name]) as IObject | undefined;
      return {
        name,
        text: isString ? buttonConfig[item].text : (item?.text ?? base?.text),
        // 对象写法（如 { name: 'refresh', perm: 'refresh' }）需合并 buttonConfig 默认 attrs，否则无 icon/type
        attrs: {
          ...attr,
          ...(isString ? buttonConfig[item].attrs : { ...base?.attrs, ...item?.attrs }),
        },
        render: isString ? undefined : (item?.render ?? undefined),
        perm: isString
          ? getButtonPerm(buttonConfig[item].perm)
          : item?.perm
            ? getButtonPerm(item.perm as string)
            : '*:*:*',
      };
    });
  }

  // 左侧工具栏按钮
  const toolbarLeftBtn = computed(() => {
    if (!config.value.toolbar || config.value.toolbar.length === 0) return [];
    return createToolbar(config.value.toolbar, {});
  });

  const hideColumnFilter = computed(() => {
    if (config.value.hideColumnFilter === true) return true;
    if (config.value.hideColumnFilter === false) return false;
    return Boolean(slots.table);
  });

  // 右侧工具栏按钮
  const toolbarRightBtn = computed(() => {
    if (!config.value.defaultToolbar || config.value.defaultToolbar.length === 0) return [];
    const raw = createToolbar(config.value.defaultToolbar, { circle: true });
    if (hideColumnFilter.value) {
      return raw.filter((b) => b.name !== 'filter');
    }
    return raw;
  });

  // 表格操作工具栏（优先使用 templet 为 tool 的列，避免仅数据列时取错最后一列）
  const toolColumn = computed(
    () => config.value.cols.find((c) => c.templet === 'tool') ?? config.value.cols.at(-1)
  );
  const tableToolbar = computed(() => toolColumn.value?.operat ?? ['edit', 'delete']);
  const tableToolbarBtn = computed(() =>
    createToolbar(tableToolbar.value, { link: true, size: 'small' })
  );

  // 表格列
  const cols = ref(
    props.contentConfig.cols.map((col) => {
      if (col.initFn) {
        col.initFn(col);
      }
      if (col.show === undefined) {
        col.show = true;
      }
      if (
        col.prop !== undefined &&
        col.columnKey === undefined &&
        col['column-key'] === undefined
      ) {
        col.columnKey = col.prop;
      }
      if (
        col.type === 'selection' &&
        col.reserveSelection === undefined &&
        col['reserve-selection'] === undefined
      ) {
        // 配合表格row-key实现跨页多选
        col.reserveSelection = true;
      }
      return col;
    })
  );
  // 加载状态
  const loading = ref(false);
  // 列表数据
  const pageData = ref<IObject[]>([]);
  // 显示分页
  const showPagination = props.contentConfig.pagination !== false;
  // 分页配置
  const defaultPagination = {
    background: true,
    layout: 'total, sizes, prev, pager, next, jumper',
    pageSize: 20,
    pageSizes: [10, 20, 30, 50],
    total: 0,
    currentPage: 1,
  };
  const pagination = reactive(
    typeof props.contentConfig.pagination === 'object'
      ? { ...defaultPagination, ...props.contentConfig.pagination }
      : defaultPagination
  );
  // 分页相关的请求参数
  const request = props.contentConfig.request ?? {
    page_no: 1,
    page_size: 10,
  };

  const tableRef = ref<TableInstance>();

  // 行选中
  const selectionData = ref<IObject[]>([]);
  // 删除ID集合 用于批量删除
  const removeIds = ref<(number | string)[]>([]);
  function handleSelectionChange(selection: any[]) {
    selectionData.value = selection;
    removeIds.value = selection.map((item) => item[pk]);
  }

  // 获取行选中
  function getSelectionData() {
    return selectionData.value;
  }

  // 刷新
  function handleRefresh(isRestart = false) {
    fetchPageData(lastFormData, isRestart);
  }

  // 删除
  function handleDelete(id?: number | string) {
    let ids = '';
    if (id !== undefined && id !== null && id !== '') {
      ids = String(id);
    } else if (removeIds.value.length) {
      ids = removeIds.value.map(String).join(',');
    }
    if (!ids) {
      ElMessage.warning('请勾选删除项');
      return;
    }

    const dc = props.contentConfig.deleteConfirm;
    ElMessageBox.confirm(dc?.message ?? '确认删除?', dc?.title ?? '警告', {
      confirmButtonText: dc?.confirmButtonText ?? '确定',
      cancelButtonText: dc?.cancelButtonText ?? '取消',
      type: dc?.type ?? 'warning',
    })
      .then(function () {
        if (props.contentConfig.deleteAction) {
          props.contentConfig
            .deleteAction(ids)
            .then(() => {
              removeIds.value = [];
              //清空选中项
              tableRef.value?.clearSelection();
              handleRefresh(true);
            })
            .catch(() => {});
        } else {
          ElMessage.error('未配置deleteAction');
        }
      })
      .catch(() => {});
  }

  // 导出表单
  const fields: string[] = [];
  cols.value.forEach((item) => {
    if (item.prop !== undefined) {
      fields.push(item.prop);
    }
  });
  const enum ExportsOriginEnum {
    CURRENT = 'current',
    SELECTED = 'selected',
    REMOTE = 'remote',
  }
  const exportsModalVisible = ref(false);
  const exportsFormRef = ref<FormInstance>();
  const exportsFormData = reactive({
    filename: '',
    sheetname: '',
    fields,
    origin: ExportsOriginEnum.CURRENT,
  });
  const exportsFormRules: FormRules = {
    fields: [{ required: true, message: '请选择字段' }],
    origin: [{ required: true, message: '请选择数据源' }],
  };
  // 打开导出弹窗
  function handleOpenExportsModal() {
    exportsModalVisible.value = true;
  }
  // 导出确认
  const handleExportsSubmit = useThrottleFn(() => {
    exportsFormRef.value?.validate((valid: boolean) => {
      if (valid) {
        handleExports();
        handleCloseExportsModal();
      }
    });
  }, 3000);
  // 关闭导出弹窗
  function handleCloseExportsModal() {
    exportsModalVisible.value = false;
    exportsFormRef.value?.resetFields();
    nextTick(() => {
      exportsFormRef.value?.clearValidate();
    });
  }
  // 导出
  function handleExports() {
    const filename = exportsFormData.filename
      ? exportsFormData.filename
      : props.contentConfig.permPrefix || 'export';
    const sheetname = exportsFormData.sheetname ? exportsFormData.sheetname : 'sheet';
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet(sheetname);
    const columns: Partial<ExcelJS.Column>[] = [];
    cols.value.forEach((col) => {
      if (col.label && col.prop && exportsFormData.fields.includes(col.prop)) {
        columns.push({ header: col.label, key: col.prop });
      }
    });
    worksheet.columns = columns;
    if (exportsFormData.origin === ExportsOriginEnum.REMOTE) {
      if (props.contentConfig.exportsAction) {
        props.contentConfig.exportsAction(lastFormData).then((res) => {
          worksheet.addRows(res);
          workbook.xlsx
            .writeBuffer()
            .then((buffer) => {
              saveXlsx(buffer, filename as string);
            })
            .catch((error) => console.log(error));
        });
      } else {
        ElMessage.error('未配置exportsAction');
      }
    } else {
      worksheet.addRows(
        exportsFormData.origin === ExportsOriginEnum.SELECTED ? selectionData.value : pageData.value
      );
      workbook.xlsx
        .writeBuffer()
        .then((buffer) => {
          saveXlsx(buffer, filename as string);
        })
        .catch((error) => console.log(error));
    }
  }

  // 导入表单
  let isFileImport = false;
  const uploadRef = ref<UploadInstance>();
  const importModalVisible = ref(false);
  const importFormRef = ref<FormInstance>();
  const importFormData = reactive<{
    files: UploadUserFile[];
  }>({
    files: [],
  });
  const importFormRules: FormRules = {
    files: [{ required: true, message: '请选择文件' }],
  };
  // 打开导入弹窗
  function handleOpenImportModal(isFile: boolean = false) {
    importModalVisible.value = true;
    isFileImport = isFile;
  }
  // 覆盖前一个文件
  function handleFileExceed(files: File[]) {
    uploadRef.value!.clearFiles();
    const file = files[0] as UploadRawFile;
    file.uid = genFileId();
    uploadRef.value!.handleStart(file);
  }
  // 下载导入模板
  function handleDownloadTemplate() {
    const importTemplate = props.contentConfig.importTemplate;
    if (typeof importTemplate === 'string') {
      window.open(importTemplate);
    } else if (typeof importTemplate === 'function') {
      importTemplate().then((response) => {
        const fileData = response.data;
        const fileName = decodeURI(
          response.headers['content-disposition'].split(';')[1].split('=')[1]
        );
        saveXlsx(fileData, fileName);
      });
    } else {
      ElMessage.error('未配置importTemplate');
    }
  }
  // 导入确认
  const handleImportSubmit = useThrottleFn(() => {
    importFormRef.value?.validate((valid: boolean) => {
      if (valid) {
        if (isFileImport) {
          handleImport();
        } else {
          handleImports();
        }
      }
    });
  }, 3000);
  // 关闭导入弹窗
  function handleCloseImportModal() {
    importModalVisible.value = false;
    importFormRef.value?.resetFields();
    nextTick(() => {
      importFormRef.value?.clearValidate();
    });
  }
  // 文件导入
  function handleImport() {
    const importAction = props.contentConfig.importAction;
    if (importAction === undefined) {
      ElMessage.error('未配置importAction');
      return;
    }
    importAction(importFormData.files[0].raw as File).then(() => {
      ElMessage.success('导入数据成功');
      handleCloseImportModal();
      handleRefresh(true);
    });
  }
  // 导入
  function handleImports() {
    const importsAction = props.contentConfig.importsAction;
    if (importsAction === undefined) {
      ElMessage.error('未配置importsAction');
      return;
    }
    // 获取选择的文件
    const file = importFormData.files[0].raw as File;
    // 创建Workbook实例
    const workbook = new ExcelJS.Workbook();
    // 使用FileReader对象来读取文件内容
    const fileReader = new FileReader();
    // 二进制字符串的形式加载文件
    fileReader.readAsArrayBuffer(file);
    fileReader.onload = (ev) => {
      if (ev.target !== null && ev.target.result !== null) {
        const result = ev.target.result as ArrayBuffer;
        // 从 buffer中加载数据解析
        workbook.xlsx
          .load(result)
          .then((workbook) => {
            // 解析后的数据
            const data = [];
            // 获取第一个worksheet内容
            const worksheet = workbook.getWorksheet(1);
            if (worksheet) {
              // 获取第一行的标题
              const fields: any[] = [];
              worksheet.getRow(1).eachCell((cell) => {
                fields.push(cell.value);
              });
              // 遍历工作表的每一行（从第二行开始，因为第一行通常是标题行）
              for (let rowNumber = 2; rowNumber <= worksheet.rowCount; rowNumber++) {
                const rowData: IObject = {};
                const row = worksheet.getRow(rowNumber);
                // 遍历当前行的每个单元格
                row.eachCell((cell, colNumber) => {
                  // 获取标题对应的键，并将当前单元格的值存储到相应的属性名中
                  rowData[fields[colNumber - 1]] = cell.value;
                });
                // 将当前行的数据对象添加到数组中
                data.push(rowData);
              }
            }
            if (data.length === 0) {
              ElMessage.error('未解析到数据');
              return;
            }
            importsAction(data).then(() => {
              ElMessage.success('导入数据成功');
              handleCloseImportModal();
              handleRefresh(true);
            });
          })
          .catch((error) => console.log(error));
      } else {
        ElMessage.error('读取文件失败');
      }
    };
  }

  // 操作栏
  function handleToolbar(name: string) {
    switch (name) {
      case 'refresh':
        handleRefresh();
        break;
      case 'export':
        handleOpenExportsModal();
        break;
      case 'imports':
        handleOpenImportModal();
        break;
      case 'add':
        emit('addClick');
        break;
      case 'delete':
        handleDelete();
        break;
      case 'patch':
        emit('toolbarClick', name);
        break;
      case 'import':
        handleOpenImportModal(true);
        break;
      default:
        emit('toolbarClick', name);
        break;
    }
  }

  // 操作列
  function handleOperate(data: IOperateData) {
    switch (data.name) {
      case 'delete':
        if (props.contentConfig?.deleteAction) {
          handleDelete(data.row[pk]);
        } else {
          emit('operateClick', data);
        }
        break;
      default:
        emit('operateClick', data);
        break;
    }
  }

  // 属性修改
  function handleModify(field: string, value: boolean | string | number, row: Record<string, any>) {
    if (props.contentConfig.modifyAction) {
      props.contentConfig.modifyAction({
        [pk]: row[pk],
        field,
        value,
      });
    } else {
      ElMessage.error('未配置modifyAction');
    }
  }

  // 分页切换
  function handleSizeChange(value: number) {
    pagination.pageSize = value;
    handleRefresh();
  }
  function handleCurrentChange(value: number) {
    pagination.currentPage = value;
    handleRefresh();
  }

  // 远程数据筛选
  let filterParams: IObject = {};
  function handleFilterChange(newFilters: any) {
    const filters: IObject = {};
    for (const key in newFilters) {
      const col = cols.value.find((col) => {
        return col.columnKey === key || col['column-key'] === key;
      });
      if (col && col.filterJoin !== undefined) {
        filters[key] = newFilters[key].join(col.filterJoin);
      } else {
        filters[key] = newFilters[key];
      }
    }
    filterParams = { ...filterParams, ...filters };
    emit('filterChange', filterParams);
  }

  // 获取筛选条件
  function getFilterParams() {
    return filterParams;
  }

  // 获取分页数据
  let lastFormData = {};
  function getIndexActionErrorMessage(err: unknown): string {
    if (err && typeof err === 'object' && 'response' in err) {
      const d = (err as { response?: { data?: { msg?: string; message?: string } } }).response
        ?.data;
      if (d?.msg) return String(d.msg);
      if (d?.message) return String(d.message);
    }
    if (err instanceof Error && err.message) return err.message;
    return '数据加载失败';
  }

  function fetchPageData(formData: IObject = {}, isRestart = false) {
    loading.value = true;
    // 上一次搜索条件
    lastFormData = formData;
    // 重置页码
    if (isRestart) {
      pagination.currentPage = 1;
    }
    props.contentConfig
      .indexAction(
        showPagination
          ? {
              [request.page_no]: pagination.currentPage,
              [request.page_size]: pagination.pageSize,
              ...formData,
            }
          : formData
      )
      .then((data) => {
        if (showPagination) {
          if (props.contentConfig.parseData) {
            data = props.contentConfig.parseData(data);
          }
          pagination.total = data.total;
          pageData.value = data.list;
        } else {
          pageData.value = data;
        }
      })
      .catch((err: unknown) => {
        console.error(err);
        ElMessage.error(getIndexActionErrorMessage(err));
      })
      .finally(() => {
        loading.value = false;
      });
  }
  if (props.contentConfig.initialFetch !== false) {
    fetchPageData();
  }

  // 导出Excel
  function exportPageData(formData: IObject = {}) {
    if (props.contentConfig.exportAction) {
      props.contentConfig.exportAction(formData).then((response) => {
        const fileData = response.data;
        const fileName = decodeURI(
          response.headers['content-disposition'].split(';')[1].split('=')[1]
        );
        saveXlsx(fileData, fileName);
      });
    } else {
      ElMessage.error('未配置exportAction');
    }
  }

  // 浏览器保存文件
  function saveXlsx(fileData: any, fileName: string) {
    const fileType =
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8';

    const blob = new Blob([fileData], { type: fileType });
    const downloadUrl = window.URL.createObjectURL(blob);

    const downloadLink = document.createElement('a');
    downloadLink.href = downloadUrl;
    downloadLink.download = fileName;

    document.body.appendChild(downloadLink);
    downloadLink.click();

    document.body.removeChild(downloadLink);
    window.URL.revokeObjectURL(downloadUrl);
  }

  // 暴露的属性和方法
  defineExpose({
    fetchPageData,
    exportPageData,
    getFilterParams,
    getSelectionData,
    handleRefresh,
    handleToolbar,
    handleDelete,
    pageData,
    pagination,
    tableRef,
  });
</script>

<style lang="scss" scoped>
  :deep(.curd-embed-dialog) {
    padding-right: 0;
  }
</style>
