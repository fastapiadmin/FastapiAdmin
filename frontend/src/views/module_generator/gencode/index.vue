<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form
        ref="queryRef"
        :model="queryFormData"
        :inline="true"
        label-suffix=":"
        @submit.prevent="handleQuery"
      >
        <el-form-item label="表名称" prop="table_name">
          <el-input
            v-model="queryFormData.table_name"
            placeholder="请输入表名称"
            clearable
            style="width: 200px"
            @keyup.enter="handleQuery"
          />
        </el-form-item>
        <el-form-item label="表描述" prop="table_comment">
          <el-input
            v-model="queryFormData.table_comment"
            placeholder="请输入表描述"
            clearable
            style="width: 200px"
            @keyup.enter="handleQuery"
          />
        </el-form-item>
        <el-form-item class="search-buttons">
          <el-button
            v-hasPerm="['module_generator:gencode:query']"
            type="primary"
            icon="search"
            native-type="submit"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_generator:gencode:query']"
            icon="refresh"
            @click="handleRefresh"
          >
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 内容区域 -->
    <el-card class="data-table">
      <template #header>
        <div class="card-header">
          <span>
            <el-tooltip content="生成代码">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            生成代码
          </span>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--left">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_generator:gencode:create']"
                type="primary"
                plain
                icon="Plus"
                @click="createTableVisible = true"
              >
                创建
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_generator:gencode:import']"
                type="success"
                plain
                icon="Upload"
                @click="handleImportClick"
              >
                导入
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_generator:gencode:delete']"
                type="danger"
                plain
                icon="Delete"
                :disabled="ids.length === 0"
                @click="handleDelete()"
              >
                批量删除
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_generator:gencode:code']"
                type="warning"
                plain
                icon="Download"
                :disabled="!canGenerate"
                @click="handleGenTable('0')"
              >
                批量生成
              </el-button>
            </el-col>
          </el-row>
        </div>
        <div class="data-table__toolbar--right">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-tooltip content="刷新">
                <el-button
                  v-hasPerm="['module_generator:gencode:query']"
                  type="primary"
                  icon="refresh"
                  circle
                  @click="handleRefresh"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-popover placement="bottom" trigger="click">
                <template #reference>
                  <el-button type="danger" icon="operation" circle></el-button>
                </template>
                <el-scrollbar max-height="350px">
                  <template v-for="column in tableColumns" :key="column.prop">
                    <el-checkbox v-if="column.prop" v-model="column.show" :label="column.label" />
                  </template>
                </el-scrollbar>
              </el-popover>
            </el-col>
          </el-row>
        </div>
      </div>

      <el-table
        ref="dataTableRef"
        v-loading="loading"
        :data="tableList"
        highlight-current-row
        class="data-table__content"
        :height="450"
        border
        stripe
        @selection-change="handleTableSelectionChange"
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'selection')?.show"
          type="selection"
          align="center"
          width="55"
        ></el-table-column>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'index')?.show"
          label="序号"
          type="index"
          min-width="30"
          align="center"
          fixed
        >
          <template #default="scope">
            <span>
              {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'table_name')?.show"
          label="表名称"
          prop="table_name"
          :show-overflow-tooltip="true"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'table_comment')?.show"
          label="表描述"
          prop="table_comment"
          :show-overflow-tooltip="true"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'class_name')?.show"
          label="实体"
          prop="class_name"
          :show-overflow-tooltip="true"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'created_time')?.show"
          label="创建时间"
          prop="created_time"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'updated_time')?.show"
          label="更新时间"
          prop="updated_time"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'operation')?.show"
          label="操作"
          align="center"
          min-width="120"
          class-name="small-padding fixed-width"
        >
          <template #default="scope">
            <el-button
              v-hasPerm="['module_generator:gencode:update']"
              link
              type="primary"
              :icon="MagicStick"
              @click="handlePreviewTable(scope.row)"
            >
              代码生成
            </el-button>
            <el-button
              v-hasPerm="['module_generator:gencode:delete']"
              link
              type="danger"
              icon="Delete"
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
            <el-button
              v-hasPerm="['module_generator:db:sync']"
              link
              type="success"
              icon="Refresh"
              @click="handleSynchDb(scope.row)"
            >
              同步
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

    <!-- 创建表 -->
    <el-dialog v-model="createTableVisible" title="创建表" append-to-body>
      <span>创建表语句(支持多个建表sql语句)：</span>
      <el-button type="warning" size="small" class="ml-1 mb-1" @click="loadExampleMysql">
        加载MySQL示例
      </el-button>
      <el-button type="primary" size="small" class="ml-1 mb-1" @click="loadExamplePostgres">
        加载Postgres示例
      </el-button>
      <el-scrollbar max-height="72vh">
        <div class="absolute z-36 right-5 top-2">
          <el-link type="primary" @click="handleCopyCode">
            <el-icon>
              <CopyDocument />
            </el-icon>
            复制代码
          </el-link>
        </div>

        <Codemirror
          ref="sqlRef"
          v-model:value="createContent"
          :options="sqlOptions"
          border
          :height="'300px'"
          width="100%"
        />
      </el-scrollbar>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" :loading="loading" @click="handleCreateTable(createContent)">
            确 定
          </el-button>
          <el-button @click="handleCreateTableCancel()">取 消</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 导入表 -->
    <el-dialog v-model="importVisible" title="导入表" width="800px" top="5vh" append-to-body>
      <el-form ref="queryRef" :model="importQueryFormData" :inline="true">
        <el-form-item label="表名称" prop="table_name">
          <el-input
            v-model="importQueryFormData.table_name"
            placeholder="请输入表名称"
            clearable
            style="width: 180px"
            @keyup.enter="handleImportQuery"
          />
        </el-form-item>
        <el-form-item label="表描述" prop="table_comment">
          <el-input
            v-model="importQueryFormData.table_comment"
            placeholder="请输入表描述"
            clearable
            style="width: 180px"
            @keyup.enter="handleImportQuery"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            v-hasPerm="['module_generator:dblist:query']"
            type="primary"
            icon="Search"
            @click="handleImportQuery"
          >
            搜索
          </el-button>
          <el-button
            v-hasPerm="['module_generator:dblist:query']"
            icon="Refresh"
            @click="handleImportReset"
          >
            重置
          </el-button>
        </el-form-item>
      </el-form>
      <el-row>
        <el-table
          ref="table"
          :data="dbTableList"
          height="300px"
          border
          @row-click="clickRow"
          @selection-change="handleImportTableSelectionChange"
        >
          <template #empty>
            <el-empty :image-size="80" description="暂无数据" />
          </template>
          <el-table-column type="selection" width="55"></el-table-column>
          <el-table-column label="序号" type="index" min-width="30" align="center" fixed>
            <template #default="scope">
              <span>
                {{
                  (importQueryFormData.page_no - 1) * importQueryFormData.page_size +
                  scope.$index +
                  1
                }}
              </span>
            </template>
          </el-table-column>
          <el-table-column
            prop="database_name"
            label="数据库名称"
            :show-overflow-tooltip="true"
          ></el-table-column>
          <el-table-column
            prop="table_name"
            label="表名称"
            :show-overflow-tooltip="true"
          ></el-table-column>
          <el-table-column
            prop="table_comment"
            label="表描述"
            :show-overflow-tooltip="true"
          ></el-table-column>
          <el-table-column prop="table_type" label="表类型"></el-table-column>
        </el-table>
        <pagination
          v-model:page="importQueryFormData.page_no"
          v-model:limit="importQueryFormData.page_size"
          :total="importTotal"
          @pagination="getDbList"
        />
      </el-row>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" :loading="importLoading" @click="handleImportTable">
            确 定
          </el-button>
          <el-button @click="importVisible = false">取 消</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 代码生成抽屉 -->
    <el-drawer
      v-model="editVisible"
      :title="'【代码生成】' + info.table_name"
      size="85%"
      @close="handleClose"
    >
      <el-steps :active="activeStep" finish-status="success" simple>
        <el-step title="基础配置" />
        <el-step title="字段配置" />
        <el-step title="预览代码" />
      </el-steps>

      <div class="mt-5">
        <!-- 第一步：基础配置 -->
        <el-form
          v-show="activeStep == 0"
          ref="basicInfo"
          :model="info"
          :rules="rules"
          label-width="150px"
        >
          <el-row>
            <el-col :span="12">
              <el-form-item label="表名称" prop="table_name">
                <el-input v-model="info.table_name" placeholder="请输入表名称" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="表描述" prop="table_comment">
                <el-input v-model="info.table_comment" placeholder="请输入表描述" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="实体类名称" prop="class_name">
                <el-input v-model="info.class_name" placeholder="请输入" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item prop="package_name">
                <template #label>
                  包名
                  <el-tooltip content="生成在哪个python模块下，例如 module_gencode" placement="top">
                    <el-icon><QuestionFilled /></el-icon>
                  </el-tooltip>
                </template>
                <el-input v-model="info.package_name" disabled>
                  <template #prepend>默认不允许修改</template>
                  <template #append>目的为简化生成代码</template>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item prop="module_name">
                <template #label>
                  模块名
                  <el-tooltip content="可理解为子系统名，例如 system" placement="top">
                    <el-icon><QuestionFilled /></el-icon>
                  </el-tooltip>
                </template>
                <el-input v-model="info.module_name" disabled>
                  <template #prepend>默认不允许修改</template>
                  <template #append>目的为简化生成代码</template>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item prop="business_name">
                <template #label>
                  业务名
                  <el-tooltip content="可理解为功能英文名，例如 user" placement="top">
                    <el-icon><QuestionFilled /></el-icon>
                  </el-tooltip>
                </template>
                <el-input v-model="info.business_name" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item prop="function_name">
                <template #label>
                  功能名
                  <el-tooltip content="用作类描述，例如 用户" placement="top">
                    <el-icon><QuestionFilled /></el-icon>
                  </el-tooltip>
                </template>
                <el-input v-model="info.function_name" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item>
                <template #label>
                  上级菜单
                  <el-tooltip content="分配到指定菜单下，例如 系统管理" placement="top">
                    <el-icon><QuestionFilled /></el-icon>
                  </el-tooltip>
                </template>
                <el-tree-select
                  v-model="info.parent_menu_id"
                  :data="menuOptions"
                  placeholder="请选择系统菜单, 不选择默认分配到模块管理（id:7）"
                  check-strictly
                  filterable
                  :render-after-expand="false"
                />
              </el-form-item>
            </el-col>
            <el-col :span="24">
              <el-form-item label="备注" prop="description">
                <el-input v-model="info.description" type="textarea" :rows="3"></el-input>
              </el-form-item>
            </el-col>

            <el-divider>生成文件路径</el-divider>

            <el-col :span="24">
              <el-descriptions :column="2" border>
                <el-descriptions-item :label="info.function_name + '功能，后端控制层'">
                  backend/app/api/v1/{{ info.module_name }}/{{ info.business_name }}/controller.py
                </el-descriptions-item>
                <el-descriptions-item :label="info.function_name + '功能，后端业务层'">
                  backend/app/api/v1/{{ info.module_name }}/{{ info.business_name }}/service.py
                </el-descriptions-item>
                <el-descriptions-item :label="info.function_name + '功能，后端数据层'">
                  backend/app/api/v1/{{ info.module_name }}/{{ info.business_name }}/crud.py
                </el-descriptions-item>
                <el-descriptions-item :label="info.function_name + '功能，后端实体层'">
                  backend/app/api/v1/{{ info.module_name }}/{{ info.business_name }}/model.py
                </el-descriptions-item>
                <el-descriptions-item :label="info.function_name + '功能，后端访问层'">
                  backend/app/api/v1/{{ info.module_name }}/{{ info.business_name }}/param.py
                </el-descriptions-item>
                <el-descriptions-item :label="info.function_name + '功能，后端序列化层'">
                  backend/app/api/v1/{{ info.module_name }}/{{ info.business_name }}/schema.py
                </el-descriptions-item>
                <el-descriptions-item :label="info.function_name + '功能，数据库业务菜单'">
                  backend/sql/menu/{{ info.module_name }}.{{ info.business_name }}.sql
                </el-descriptions-item>
                <el-descriptions-item :label="info.function_name + '功能，前端接口层'">
                  frontend/src/api/{{ info.module_name }}/{{ info.business_name }}.ts
                </el-descriptions-item>
                <el-descriptions-item :label="info.function_name + '功能，前端视图层'">
                  frontend/src/views/{{ info.module_name }}/{{ info.business_name }}/index.vue
                </el-descriptions-item>
              </el-descriptions>
            </el-col>
          </el-row>
        </el-form>

        <!-- 第二步：字段配置 -->
        <div v-show="activeStep == 1" class="elTableCustom">
          <div class="mb-2 flex items-center gap-2">
            <el-tag size="small" type="info">批量设置</el-tag>
            <el-space size="small">
              <el-dropdown>
                <el-button size="small" type="primary" plain>查询</el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="bulkSet('is_query', '1')">全选</el-dropdown-item>
                    <el-dropdown-item @click="bulkSet('is_query', '0')">全不选</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
              <el-dropdown>
                <el-button size="small" type="success" plain>列表</el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="bulkSet('is_list', '1')">全选</el-dropdown-item>
                    <el-dropdown-item @click="bulkSet('is_list', '0')">全不选</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
              <el-dropdown>
                <el-button size="small" type="warning" plain>新增</el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="bulkSet('is_insert', '1')">全选</el-dropdown-item>
                    <el-dropdown-item @click="bulkSet('is_insert', '0')">全不选</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
              <el-dropdown>
                <el-button size="small" type="danger" plain>编辑</el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="bulkSet('is_edit', '1')">全选</el-dropdown-item>
                    <el-dropdown-item @click="bulkSet('is_edit', '0')">全不选</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </el-space>
          </div>
          <el-table
            ref="dragTable"
            v-loading="loading"
            :data="info.columns"
            row-key="id"
            max-height="680"
            highlight--currentrow
            class="data-table__content"
            border
            stripe
          >
            <template #empty>
              <el-empty :image-size="80" description="暂无数据" />
            </template>
            <el-table-column label="序号" type="index" min-width="7%" fixed />
            <el-table-column
              label="列名"
              prop="column_name"
              min-width="10%"
              :show-overflow-tooltip="true"
            />
            <el-table-column
              label="类型"
              prop="column_type"
              min-width="10%"
              :show-overflow-tooltip="true"
            />
            <el-table-column
              label="长度"
              prop="column_length"
              min-width="8%"
              :show-overflow-tooltip="true"
            >
              <template #default="scope">
                <el-input v-model="scope.row.column_length" :disabled="scope.row.is_pk === '1'" />
              </template>
            </el-table-column>
            <el-table-column label="注释" min-width="10%">
              <template #default="scope">
                <el-input v-model="scope.row.column_comment"></el-input>
              </template>
            </el-table-column>
            <el-table-column label="后端类型" min-width="12%">
              <template #default="scope">
                <el-select v-model="scope.row.python_type">
                  <el-option label="str" value="str" />
                  <el-option label="int" value="int" />
                  <el-option label="float" value="float" />
                  <el-option label="Decimal" value="Decimal" />
                  <el-option label="date" value="date" />
                  <el-option label="time" value="time" />
                  <el-option label="datetime" value="datetime" />
                  <el-option label="bytes" value="bytes" />
                  <el-option label="dict" value="dict" />
                  <el-option label="list" value="list" />
                </el-select>
              </template>
            </el-table-column>
            <el-table-column label="后端属性" min-width="12%">
              <template #default="scope">
                <el-input v-model="scope.row.python_field"></el-input>
              </template>
            </el-table-column>
            <el-table-column label="新增" min-width="10%">
              <template #default="scope">
                <el-checkbox
                  v-model="scope.row.is_insert"
                  true-value="1"
                  false-value="0"
                ></el-checkbox>
              </template>
            </el-table-column>
            <el-table-column label="编辑" min-width="10%">
              <template #default="scope">
                <el-checkbox
                  v-model="scope.row.is_edit"
                  true-value="1"
                  false-value="0"
                ></el-checkbox>
              </template>
            </el-table-column>
            <el-table-column label="列表" min-width="10%">
              <template #default="scope">
                <el-checkbox
                  v-model="scope.row.is_list"
                  true-value="1"
                  false-value="0"
                ></el-checkbox>
              </template>
            </el-table-column>
            <el-table-column label="查询" min-width="10%">
              <template #default="scope">
                <el-checkbox
                  v-model="scope.row.is_query"
                  true-value="1"
                  false-value="0"
                ></el-checkbox>
              </template>
            </el-table-column>
            <el-table-column label="查询方式" min-width="12%">
              <template #default="scope">
                <el-select v-model="scope.row.query_type">
                  <el-option label="=" value="EQ" />
                  <el-option label="!=" value="NE" />
                  <el-option label=">" value="GT" />
                  <el-option label=">=" value="GTE" />
                  <el-option label="<" value="LT" />
                  <el-option label="<=" value="LTE" />
                  <el-option label="LIKE" value="LIKE" />
                  <el-option label="BETWEEN" value="BETWEEN" />
                </el-select>
              </template>
            </el-table-column>
            <el-table-column
              label="默认值"
              prop="column_default"
              min-width="10%"
              :show-overflow-tooltip="true"
            >
              <template #default="scope">
                <el-input v-model="scope.row.column_default" :disabled="scope.row.is_pk === '1'" />
              </template>
            </el-table-column>
            <el-table-column label="自增" min-width="10%">
              <template #default="scope">
                <el-checkbox v-model="scope.row.is_increment" true-value="1" false-value="0" />
              </template>
            </el-table-column>
            <el-table-column label="允许空" min-width="10%">
              <template #default="scope">
                <el-checkbox
                  v-model="scope.row.is_nullable"
                  true-value="0"
                  false-value="1"
                ></el-checkbox>
              </template>
            </el-table-column>
            <el-table-column label="唯一" min-width="10%">
              <template #default="scope">
                <el-checkbox
                  v-model="scope.row.is_unique"
                  true-value="1"
                  false-value="0"
                ></el-checkbox>
              </template>
            </el-table-column>
            <el-table-column label="主键" min-width="10%">
              <template #default="scope">
                <el-checkbox v-model="scope.row.is_pk" true-value="1" false-value="0"></el-checkbox>
              </template>
            </el-table-column>
            <el-table-column label="表单类型" min-width="12%">
              <template #default="scope">
                <el-select v-model="scope.row.html_type">
                  <el-option label="文本框" value="input" />
                  <el-option label="文本域" value="textarea" />
                  <el-option label="下拉框" value="select" />
                  <el-option label="单选框" value="radio" />
                  <el-option label="复选框" value="checkbox" />
                  <el-option label="日期控件" value="datetime" />
                  <el-option label="图片上传" value="imageUpload" />
                  <el-option label="文件上传" value="fileUpload" />
                  <el-option label="富文本控件" value="editor" />
                </el-select>
              </template>
            </el-table-column>
            <el-table-column label="字典类型" min-width="12%" fixed="right">
              <template #default="scope">
                <el-select v-model="scope.row.dict_type" clearable filterable placeholder="请选择">
                  <el-option
                    v-for="dict in dictOptions"
                    :key="dict.dict_type"
                    :label="dict.dict_name"
                    :value="dict.dict_type || ''"
                  >
                    <span style="float: left">{{ dict.dict_name }}</span>
                    <span style="float: right; font-size: 13px; color: #8492a6">
                      {{ dict.dict_type }}
                    </span>
                  </el-option>
                </el-select>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 第三步：预览代码 -->
        <el-row v-show="activeStep == 2">
          <el-col :span="24" class="mb-2">
            <div class="flex-y-center gap-3">
              <span class="text-sm color-#909399">预览范围</span>
              <el-radio-group v-model="previewScope" size="small">
                <el-radio-button value="all">全部</el-radio-button>
                <el-radio-button value="frontend">前端</el-radio-button>
                <el-radio-button value="backend">后端</el-radio-button>
                <el-radio-button value="sql">数据库</el-radio-button>
              </el-radio-group>
              <span class="ml-3 text-sm color-#909399">类型</span>
              <el-checkbox-group v-model="previewTypes" size="small">
                <el-checkbox-button v-for="t in previewTypeOptions" :key="t" :value="t">
                  {{ t }}
                </el-checkbox-button>
              </el-checkbox-group>
            </div>
          </el-col>
          <el-col :span="6">
            <el-scrollbar max-height="72vh">
              <el-tree
                :data="filteredTreeData"
                default-expand-all
                highlight-current
                @node-click="handleFileTreeNodeClick"
              >
                <template #default="{ data }">
                  <div :class="`i-svg:${getFileTreeNodeIcon(data.label)}`" />
                  <span class="ml-1">{{ data.label }}</span>
                </template>
              </el-tree>
            </el-scrollbar>
          </el-col>
          <el-col :span="18">
            <el-scrollbar max-height="72vh">
              <div class="absolute z-36 right-5 top-2">
                <el-link type="primary" @click="handleCopyCode">
                  <el-icon>
                    <CopyDocument />
                  </el-icon>
                  复制代码
                </el-link>
              </div>

              <Codemirror
                ref="cmRef"
                v-model:value="code"
                :options="cmOptions"
                border
                :readonly="true"
                height="100%"
                width="100%"
              />
            </el-scrollbar>
          </el-col>
        </el-row>
      </div>

      <template #footer>
        <!-- 公共按钮：关闭 -->
        <el-button :icon="Close" @click="close">关闭</el-button>
        <el-button v-if="activeStep != 0" type="success" :icon="Back" @click="prevStep">
          上一步
        </el-button>
        <el-button
          v-if="activeStep != 2"
          v-hasPerm="['module_generator:gencode:update']"
          type="warning"
          :icon="Edit"
          :loading="loading"
          @click="submitForm"
        >
          保存配置
        </el-button>
        <el-button v-if="activeStep != 2" type="primary" @click="nextStep">
          下一步
          <el-icon class="el-icon--right"><Right /></el-icon>
        </el-button>
        <el-button
          v-if="activeStep === 2"
          type="warning"
          :icon="Download"
          :loading="loading"
          @click="handleGenTable('0', info)"
        >
          下载代码
        </el-button>
        <el-button
          v-if="activeStep === 2"
          type="primary"
          :icon="FolderOpened"
          :loading="loading"
          @click="handleGenTable('1', info)"
        >
          写入本地
        </el-button>
      </template>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "GenCode",
  inheritAttrs: false,
});

import "codemirror/mode/javascript/javascript.js";
import "codemirror/mode/sql/sql.js";
import "codemirror/theme/dracula.css";
import { ref, reactive, computed, onActivated, onMounted, watch } from "vue";
import { useClipboard } from "@vueuse/core";
import { useRoute } from "vue-router";
import Codemirror from "codemirror-editor-vue3";
import type { EditorConfiguration } from "codemirror";
import type { CmComponentRef } from "codemirror-editor-vue3";
import { ElMessage, ElMessageBox, type FormInstance, type TableInstance } from "element-plus";
import {
  QuestionFilled,
  MagicStick,
  CopyDocument,
  Close,
  Right,
  FolderOpened,
  Back,
  Download,
  Edit,
} from "@element-plus/icons-vue";
import GencodeAPI, {
  type GenTableSchema,
  type DBTableSchema,
  type GenTablePageQuery,
} from "@/api/module_generator/gencode";
import MenuAPI, { MenuTable } from "@/api/module_system/menu";
import DictAPI, { DictTable } from "@/api/module_system/dict";
import { formatTree } from "@/utils/common";
import { MenuTypeEnum } from "@/enums";
import { useSettingsStore } from "@/store";
import { ThemeMode } from "@/enums/settings/theme.enum";

// 表格列配置接口
interface TableColumn {
  prop: string;
  label: string;
  show: boolean;
  minWidth?: string;
  formatter?: (row: any, column: any) => any;
}

// 文件树节点接口
interface TreeNode {
  label: string;
  content?: string;
  children?: TreeNode[];
}

// 文件数据接口
interface FileData {
  path: string;
  file_name: string;
  content: string;
}

// 组件引用
const queryRef = ref<FormInstance>();
const table = ref<TableInstance>();
const cmRef = ref<CmComponentRef>();
const sqlRef = ref<CmComponentRef>();
const basicInfo = ref<FormInstance>();
const dragTable = ref<TableInstance>();

// 状态管理
const loading = ref(false);
const total = ref<number>(0);
const uniqueId = ref("");
const editVisible = ref(false);
const activeStep = ref(2);

// UI状态
const createTableVisible = ref(false);
const importVisible = ref(false);

// 表单和列表数据
const createContent = ref("");
const dateRange = ref<[Date, Date] | []>([]);
const tableList = ref<GenTableSchema[]>([]);
const dbTableList = ref<DBTableSchema[]>([]);
const ids = ref<number[]>([]);
const tableNames = ref<string[]>([]);

// 导入弹窗专用状态
const importLoading = ref(false);
const importTotal = ref<number>(0);
const importQueryFormData = reactive<GenTablePageQuery>({
  page_no: 1,
  page_size: 10,
  table_name: undefined,
  table_comment: undefined,
});

// 下拉选项数据
const dictOptions = ref<DictTable[]>([]);
const menuOptions = ref<OptionType[]>([]);

// 表格数据
type TableItem = {
  table_name: string;
  table_comment: string;
};
const tables = ref<TableItem[]>([]);

// 导入按钮点击事件
async function handleImportClick() {
  importVisible.value = true;
  await getDbList();
}

// 预览相关数据
const preview = reactive({
  open: false,
  title: "代码预览",
  data: {},
  active_name: "controller.py",
});

const previewScope = ref<"all" | "frontend" | "backend" | "sql">("all");
const previewTypeOptions = ["ts", "vue", "python", "sql"];
const previewTypes = ref<string[]>([...previewTypeOptions]);
const code = ref<string>("");
const treeData = ref<TreeNode[]>([]);

// 分页查询参数
const queryFormData = reactive<GenTablePageQuery>({
  page_no: 1,
  page_size: 10,
  table_name: undefined,
  table_comment: undefined,
});

// 表格列配置
const tableColumns = ref<TableColumn[]>([
  { prop: "selection", label: "选择框", show: true },
  { prop: "index", label: "序号", show: true },
  { prop: "table_name", label: "表名称", show: true },
  { prop: "table_comment", label: "表描述", show: true },
  { prop: "class_name", label: "实体", show: true },
  { prop: "created_time", label: "创建时间", show: true },
  { prop: "updated_time", label: "更新时间", show: true },
  { prop: "operation", label: "操作", show: true },
]);

const settingsStore = useSettingsStore();

// 主题计算属性
const codeTheme = computed(() => (settingsStore.theme === ThemeMode.DARK ? "dracula" : "default"));

// 监听主题变化并更新CodeMirror实例
watch(codeTheme, (newTheme) => {
  // 更新SQL编辑器主题
  if (sqlRef.value && sqlRef.value.cminstance) {
    sqlRef.value.cminstance.setOption("theme", newTheme);
  }

  // 更新代码预览编辑器主题
  if (cmRef.value && cmRef.value.cminstance) {
    cmRef.value.cminstance.setOption("theme", newTheme);
  }
});

// CodeMirror配置
const cmOptions: EditorConfiguration = {
  mode: "text/javascript",
  lineNumbers: true,
  smartIndent: true,
  indentUnit: 2,
  tabSize: 2,
  readOnly: false,
  theme: codeTheme.value,
  lineWrapping: true,
  autofocus: false,
};

const sqlOptions: EditorConfiguration = {
  mode: "text/x-sql",
  lineNumbers: true,
  smartIndent: true,
  indentUnit: 2,
  tabSize: 2,
  readOnly: false,
  theme: codeTheme.value,
  lineWrapping: true,
  autofocus: false,
};

// 工具函数
const { copy } = useClipboard();

// ===== 计算属性 =====

// 过滤后的文件树数据
const filteredTreeData = computed<TreeNode[]>(() => {
  if (!treeData.value.length) return [];

  // 基于原树按 scope/types 过滤叶子节点
  const match = (label: string, parentPath: string[]): boolean => {
    // scope 过滤：根据路径初步判断
    if (previewScope.value !== "all") {
      // 根据后端返回的格式，检查路径或文件名特征
      const isPythonBackend =
        parentPath.some((part) => part === "backend" || part === "python") || label.includes(".py");
      const isVueFrontend =
        parentPath.some((part) => part === "frontend" || part === "vue") ||
        label.includes(".vue") ||
        label.includes(".ts");
      const isSqlDatabase = parentPath.some((part) => part === "sql") || label.includes(".sql");

      if (previewScope.value === "backend" && !isPythonBackend) return false;
      if (previewScope.value === "frontend" && !isVueFrontend) return false;
      if (previewScope.value === "sql" && !isSqlDatabase) return false;
    }

    // 类型过滤：根据文件内容特征判断类型
    if (label.endsWith(".py")) return previewTypes.value.includes("python");
    if (label.endsWith(".sql")) return previewTypes.value.includes("sql");
    if (label.endsWith(".vue")) return previewTypes.value.includes("vue");
    if (label.endsWith(".ts")) return previewTypes.value.includes("ts");

    return true;
  };

  const cloneFilter = (node: TreeNode, parents: string[] = []): TreeNode | null => {
    if (!node.children || node.children.length === 0) {
      return match(node.label, parents) ? { ...node } : null;
    }
    const nextParents = [...parents, node.label];
    const children = (node.children || [])
      .map((c) => cloneFilter(c, nextParents))
      .filter(Boolean) as TreeNode[];
    if (!children.length) return null;
    return { label: node.label, children };
  };

  const filtered = treeData.value.map((n) => cloneFilter(n)).filter(Boolean) as TreeNode[];
  return filtered;
});

// 按钮状态计算
const canGenerate = computed(() => ids.value.length > 0);

// ===== 功能函数 =====

/** 一键复制代码 */
const handleCopyCode = () => {
  if (code.value) {
    copy(code.value);
    ElMessage.success("代码复制成功");
  } else {
    ElMessage.warning("没有可复制的代码");
  }
};

/** 获取文件树节点图标 */
function getFileTreeNodeIcon(label: string): string {
  if (label.endsWith(".py")) return "python";
  if (label.endsWith(".sql")) return "sql";
  if (label.endsWith(".vue")) return "vue";
  if (label.endsWith(".ts")) return "typescript";
  return "file";
}

/** 文件树节点点击事件 */
function handleFileTreeNodeClick(data: TreeNode): void {
  if (data && (!data.children || data.children.length === 0)) {
    code.value = data.content || "";
  }
}

/** 递归构建树形结构 */
function buildTree(data: FileData[]): TreeNode {
  // 创建根节点
  const root: TreeNode = { label: "前后端代码", children: [] };

  data.forEach((item) => {
    // 将路径分成数组（确保使用正斜杠）
    const parts = item.path.split("/").filter((part) => part !== "");

    let currentNode = root;

    // 遍历路径部分，创建对应的文件夹节点
    parts.forEach((part) => {
      // 查找或创建当前部分的子节点
      let node = currentNode.children?.find((child) => child.label === part);
      if (!node) {
        node = { label: part, children: [] };
        currentNode.children?.push(node);
      }
      currentNode = node;
    });

    // 添加文件节点
    currentNode.children?.push({
      label: item.file_name,
      content: item?.content,
    });
  });

  return root;
}

/** 获取生成预览 */
async function handlePreview(row: GenTableSchema): Promise<void> {
  try {
    if (!row.id) {
      ElMessage.warning("无效的表ID");
      return;
    }

    const response = await GencodeAPI.previewTable(row.id!);
    preview.data = response.data.data;

    // 转换后端返回的数据为树形结构
    const filesData = Object.entries(response.data.data).map(([key, content]) => {
      // 解析文件路径
      const pathParts = key.split("/");
      let fileName = pathParts.pop() || "";
      const path = pathParts.join("/");

      // 移除文件名结尾的.j2后缀
      if (fileName.endsWith(".j2")) {
        fileName = fileName.substring(0, fileName.lastIndexOf(".j2"));
      }

      // 确保content是字符串类型
      const contentStr = typeof content === "string" ? content : JSON.stringify(content);

      return {
        path,
        file_name: fileName,
        content: contentStr,
      } as FileData;
    });

    // 构建树形数据
    const treeRoot = buildTree(filesData);
    treeData.value = [treeRoot];

    // 查找第一个叶子节点作为默认显示内容
    const findFirstLeafNode = (nodes: TreeNode[]): TreeNode | null => {
      for (const node of nodes) {
        if (!node.children || node.children.length === 0) {
          return node;
        }
        const leaf = findFirstLeafNode(node.children);
        if (leaf) return leaf;
      }
      return null;
    };

    const firstLeafNode = findFirstLeafNode(treeData.value);
    code.value = firstLeafNode?.content || "";

    preview.open = true;
    preview.active_name = "model.py";
  } catch (error) {
    console.error("预览代码失败:", error);
  }
}

/** 查询表集合 */
async function loadingData(): Promise<void> {
  loading.value = true;
  try {
    const response = await GencodeAPI.listTable(queryFormData);
    if (response?.data?.data) {
      tableList.value = response.data.data.items;
      total.value = response.data.data.total;
    }
  } catch (error) {
    console.error("获取表数据失败:", error);
  } finally {
    loading.value = false;
  }
}

/** 表格行内生成代码操作 */
async function handleGenTable(targetGenType: string, row?: GenTableSchema): Promise<void> {
  let tbNames: string | string[] = [];

  // 判断是单条还是批量操作
  if (row) {
    tbNames = [row.table_name || ""];
  } else if (tableNames.value.length > 0) {
    tbNames = tableNames.value;
  } else {
    ElMessage.error("请选择要生成的数据");
    return;
  }

  loading.value = true;
  try {
    if (targetGenType === "1") {
      if (!Array.isArray(tbNames) || tbNames.length !== 1 || !tbNames[0]) {
        ElMessage.error("自定义路径只能生成单表代码");
        loading.value = false;
        return;
      }

      await GencodeAPI.genCodeToPath(tbNames[0]);
      ElMessage.success("代码已生成到指定路径");
    } else {
      // ZIP压缩包下载
      const tableNamesArray = Array.isArray(tbNames) ? tbNames : [tbNames];
      const response = await GencodeAPI.batchGenCode(tableNamesArray);
      // 处理文件下载
      const blob = new Blob([response.data], { type: "application/zip" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "code.zip";
      link.click();
      URL.revokeObjectURL(url); // 释放URL对象
      ElMessage.success("代码生成成功，正在下载...");
    }
  } catch (error) {
    console.error("生成代码失败:", error);
  } finally {
    loading.value = false;
  }
}

/** 同步数据库操作 */
async function handleSynchDb(row: GenTableSchema): Promise<void> {
  const tableName = row.table_name || "";

  if (!tableName) {
    ElMessage.error("表名不能为空");
    return;
  }

  try {
    await ElMessageBox.confirm('确认要强制同步"' + tableName + '"表结构吗？', "确认操作", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });

    loading.value = true;
    await GencodeAPI.syncDb(tableName);
    loadingData(); // 同步成功后刷新列表
  } catch (error) {
    if (error !== "cancel") {
      console.error("同步表结构失败:", error);
    }
  } finally {
    loading.value = false;
  }
}

/** 重置按钮操作 */
async function handleRefresh() {
  dateRange.value = [];
  // 手动重置表单
  queryFormData.page_no = 1;
  queryFormData.page_size = 10;
  queryFormData.table_name = undefined;
  queryFormData.table_comment = undefined;
  await loadingData();
}

/** 多选框选中数据 - 主表格 */
function handleTableSelectionChange(selection: GenTableSchema[]): void {
  ids.value = selection.map((item) => item.id!);
  tableNames.value = selection.map((item) => item.table_name || "").filter(Boolean);
}

/** 多选框选中数据 - 导入表格 */
function handleImportTableSelectionChange(selection: DBTableSchema[]): void {
  tables.value = selection.map((item) => ({
    table_name: item.table_name || "",
    table_comment: item.table_comment || "",
  }));
}

// 修改菜单选项过滤逻辑，添加递归过滤函数
const filterMenuTypes = (nodes: MenuTable[]) => {
  return nodes
    .filter((node) => node.type === MenuTypeEnum.CATALOG || node.type === MenuTypeEnum.MENU)
    .map((node: any): any => ({
      ...node,
      children: node.children ? filterMenuTypes(node.children) : [],
    }));
};

/** 表格行内修改按钮操作 */
async function handlePreviewTable(row?: GenTableSchema): Promise<void> {
  const selectedTableId = row?.id || ids.value[0];
  if (selectedTableId) {
    // 设置编辑的表ID和名称
    info.table_name = row?.table_name || "";
    // 加载表详情数据
    await loadTableDetail(selectedTableId);
    editVisible.value = true;

    const menu_response = await MenuAPI.listMenu();
    menuOptions.value = formatTree(filterMenuTypes(menu_response.data.data));

    const dict_response = await DictAPI.listDictType({ page_no: 1, page_size: 100 });
    dictOptions.value = dict_response.data.data.items;
  } else {
    ElMessage.error("请选择要修改的数据");
  }
}

/** 删除按钮操作 */
async function handleDelete(row?: GenTableSchema): Promise<void> {
  const tableIds = row?.id ? [row.id] : ids.value;

  if (tableIds.length === 0) {
    ElMessage.error("请选择要删除的数据");
    return;
  }

  try {
    await ElMessageBox.confirm(`是否确认删除选中的${tableIds.length}条数据？`, "删除确认", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });

    loading.value = true;
    await GencodeAPI.deleteTable(tableIds);
    loadingData();
  } catch (error) {
    if (error !== "cancel") {
      console.error("删除表数据失败:", error);
    }
  } finally {
    loading.value = false;
  }
}

/** 加载SQL示例 */
function loadExampleMysql(): void {
  const exampleSql = `-- MySQL SQL案例
  CREATE TABLE \`gen_demo01\` (
    \`name\` varchar(64) DEFAULT NULL COMMENT '名称',
    \`id\` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
    \`uuid\` varchar(64) NOT NULL COMMENT 'UUID全局唯一标识',
    \`status\` varchar(10) NOT NULL COMMENT '是否启用(0:启用 1:禁用)',
    \`description\` text COMMENT '备注/描述',
    \`created_time\` datetime NOT NULL COMMENT '创建时间',
    \`updated_time\` datetime NOT NULL COMMENT '更新时间',
    \`created_id\` int DEFAULT NULL COMMENT '创建人ID',
    \`updated_id\` int DEFAULT NULL COMMENT '更新人ID',
    PRIMARY KEY (\`id\`),
    UNIQUE KEY \`uuid\` (\`uuid\`),
    KEY \`ix_gen_demo01_created_id\` (\`created_id\`),
    KEY \`ix_gen_demo01_updated_id\` (\`updated_id\`),
    CONSTRAINT \`gen_demo01_ibfk_1\` FOREIGN KEY (\`created_id\`) REFERENCES \`sys_user\` (\`id\`) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT \`gen_demo01_ibfk_2\` FOREIGN KEY (\`updated_id\`) REFERENCES \`sys_user\` (\`id\`) ON DELETE SET NULL ON UPDATE CASCADE
  ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='示例表'`;
  createContent.value = exampleSql;
}

function loadExamplePostgres(): void {
  const exampleSql = `-- Psstgres SQL案例
  CREATE TABLE gen_demo01(
    id SERIAL NOT NULL,
    uuid varchar(64) NOT NULL,
    name varchar(64),
    status varchar(10) NOT NULL,
    description text,
    created_time timestamp without time zone NOT NULL,
    updated_time timestamp without time zone NOT NULL,
    created_id integer,
    updated_id integer,
    PRIMARY KEY(id),
    CONSTRAINT gen_demo01_created_id_fkey FOREIGN key(created_id) REFERENCES sys_user(id),
    CONSTRAINT gen_demo01_updated_id_fkey FOREIGN key(updated_id) REFERENCES sys_user(id)
  );
  CREATE UNIQUE INDEX en_demo01_uuid_key ON public.gen_demo01 USING btree (uuid);
  CREATE INDEX ix_gen_demo01_created_id ON public.gen_demo01 USING btree (created_id);
  CREATE INDEX ix_gen_demo01_updated_id ON public.gen_demo01 USING btree (updated_id);
  COMMENT ON TABLE gen_demo01 IS '示例表';
  COMMENT ON COLUMN gen_demo01.name IS '名称';
  COMMENT ON COLUMN gen_demo01.id IS '主键ID';
  COMMENT ON COLUMN gen_demo01.uuid IS 'UUID全局唯一标识';
  COMMENT ON COLUMN gen_demo01.status IS '是否启用(0:启用 1:禁用)';
  COMMENT ON COLUMN gen_demo01.description IS '备注/描述';
  COMMENT ON COLUMN gen_demo01.created_time IS '创建时间';
  COMMENT ON COLUMN gen_demo01.updated_time IS '更新时间';
  COMMENT ON COLUMN gen_demo01.created_id IS '创建人ID';
  COMMENT ON COLUMN gen_demo01.updated_id IS '更新人ID';`;
  createContent.value = exampleSql;
}

/** 创建表操作 */
async function handleCreateTable(sql: string): Promise<void> {
  if (!sql || sql.trim() === "") {
    ElMessage.error("请输入创建表SQL语句");
    return;
  }

  loading.value = true;
  try {
    await GencodeAPI.createTable(sql);
    createTableVisible.value = false;
    createContent.value = "";
    loadingData();
  } catch (error) {
    console.error("创建表数据失败:", error);
  } finally {
    loading.value = false;
  }
}

/** 取消创建表操作 */
function handleCreateTableCancel(): void {
  createTableVisible.value = false;
  createContent.value = "";
}

/** 导入表操作 */
async function handleImportTable(): Promise<void> {
  if (tables.value.length === 0) {
    ElMessage.error("请选择要导入的表");
    return;
  }

  importLoading.value = true;
  try {
    // 提取表名数组
    const tableNames = tables.value.map((table) => table.table_name || "");
    await GencodeAPI.importTable(tableNames);
    importVisible.value = false;
    loadingData(); // 导入成功后刷新已导入的表列表
  } catch (error) {
    console.error("导入表失败:", error);
  } finally {
    importLoading.value = false;
  }
}

/** 单击选择行 */
function clickRow(row: DBTableSchema): void {
  table.value?.toggleRowSelection(row);
}

/** 查询数据库表数据 */
async function getDbList(): Promise<void> {
  importLoading.value = true;
  try {
    const res = await GencodeAPI.listDbTable(importQueryFormData);
    if (res.data && res.data.data) {
      dbTableList.value = res.data.data.items;
      importTotal.value = res.data.data.total;
    }
  } catch (error) {
    console.error("获取数据库表列表失败:", error);
  } finally {
    importLoading.value = false;
  }
}

/** 导入弹窗搜索按钮操作 */
async function handleImportQuery(): Promise<void> {
  importQueryFormData.page_no = 1;
  await getDbList();
}

/** 导入弹窗重置按钮操作 */
async function handleImportReset(): Promise<void> {
  if (queryRef.value) {
    queryRef.value.resetFields();
  }
  await handleImportQuery();
}

/** 搜索按钮操作 */
async function handleQuery(): Promise<void> {
  queryFormData.page_no = 1;
  await loadingData();
}

// 路由和导航
const route = useRoute();

// ===== 生命周期和初始化 =====

/** 页面激活时执行 */
onActivated(async () => {
  const time = route.query.t;
  if (time != null && String(time) !== uniqueId.value) {
    uniqueId.value = String(time);
    queryFormData.page_no = Number(route.query.page_no || 1);
    dateRange.value = [];
    await loadingData();
  }
});

// 表单数据
const info = reactive<GenTableSchema>({
  id: undefined,
  table_name: "",
  table_comment: "",
  sub_table_name: "",
  sub_table_fk_name: "",
  class_name: "",
  package_name: "",
  module_name: "",
  business_name: "",
  function_name: "",
  description: "",
  parent_menu_id: undefined,
  pk_column: undefined,
  sub_table: undefined,
  columns: [],
  sub: false,
});

// 校验规则
const rules = {
  table_name: [{ required: true, message: "表名称不能为空", trigger: "blur" }],
  class_name: [{ required: true, message: "实体名称不能为空", trigger: "blur" }],
  package_name: [{ required: true, message: "生成包路径不能为空", trigger: "blur" }],
  module_name: [{ required: true, message: "生成模块名不能为空", trigger: "blur" }],
  business_name: [{ required: true, message: "生成业务名不能为空", trigger: "blur" }],
  function_name: [{ required: true, message: "生成功能名不能为空", trigger: "blur" }],
  parent_menu_id: [{ required: true, message: "所属菜单不能为空", trigger: "change" }],
};

// ===== 工具函数
/** 提交表单 - 保存配置 */
async function submitForm() {
  // 检查是否有表ID
  if (!info.id) {
    ElMessage.error("无效的表ID");
    return;
  }

  try {
    loading.value = true;

    // 检查字段列表
    if (!info.columns || info.columns.length === 0) {
      ElMessage.error("请配置字段信息");
      return;
    }

    // 提交表单数据，确保columns是必需的
    const tableData = {
      ...info,
      columns: info.columns || [], // 确保columns存在
    };

    const response = await GencodeAPI.updateTable(tableData as GenTableSchema, info.id || 0);

    if (response?.data?.code === 200) {
      ElMessage.success((response?.data as any)?.message || "保存成功");
      return true;
    }
  } catch (error) {
    console.error("保存表单失败:", error);
  } finally {
    loading.value = false;
  }
}

// 下一步
async function nextStep(): Promise<void> {
  if (activeStep.value < 3) {
    activeStep.value++;

    // 当从字段配置进入预览步骤时，自动加载预览数据
    if (activeStep.value === 2 && info.id) {
      await handlePreview({ id: info.id, table_name: info.table_name } as GenTableSchema);
    }
  }
}

// 上一步
function prevStep(): void {
  if (activeStep.value > 0) {
    activeStep.value--;
  }
}

// 批量设置字段属性
function bulkSet(field: string | string[], value: any): void {
  if (!info.columns || !Array.isArray(info.columns)) return;

  const fieldsToUpdate = Array.isArray(field) ? field : [field];

  info.columns.forEach((column) => {
    if (column && typeof column === "object") {
      fieldsToUpdate.forEach((f) => {
        (column as any)[f] = value;
      });
    }
  });
}

function close(): void {
  editVisible.value = false;
  activeStep.value = 0; // 重置步骤

  // 清除表单验证状态
  setTimeout(() => {
    basicInfo.value?.resetFields();
  }, 300);
}

/** 处理抽屉关闭事件 */
function handleClose(): void {
  close();
}

/** 加载表详情 */
async function loadTableDetail(id: number | string) {
  try {
    loading.value = true;
    const response = await GencodeAPI.detailTable(Number(id));

    if (response?.data?.data) {
      const data = response.data.data;

      // 填充表单数据
      Object.assign(info, { ...data });

      // 处理列数据
      if (data && data.columns && Array.isArray(data.columns)) {
        // 深拷贝确保数据独立性
        info.columns = JSON.parse(JSON.stringify(data.columns));
        // 设置列的选中状态
        info.columns.forEach((item: any) => {
          item.select = true;
        });
      }

      // 重置当前步骤为第一步
      activeStep.value = 0;
    }
  } catch (error) {
    console.error("获取表详情失败:", error);
  } finally {
    loading.value = false;
  }
}

// ===== 生命周期函数

/** 组件挂载时 */
onMounted(() => {
  // 初始化数据加载
  loadingData();
});
</script>

<style lang="scss" scoped></style>
