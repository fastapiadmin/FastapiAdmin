<!-- Art 栈 CRUD 示例：组合 CrudLayout + useCrudArtTableDemo；业务页可效仿或改用 CrudSearch/CrudContent -->
<template>
  <CrudLayout root-class="pb-5">
    <template #search>
      <ArtSearchBar
        ref="searchBarRef"
        v-model="searchFormState"
        :items="searchItems"
        :rules="rules"
        :is-expand="false"
        :show-expand="true"
        :show-reset-button="true"
        :show-search-button="true"
        :disabled-search-button="false"
        @search="handleSearch"
        @reset="handleReset"
      />
    </template>

    <ElCard class="data-table flex min-h-0 flex-1 flex-col art-table-card" shadow="never">
      <template #header>
        <div class="flex-cb">
          <h4 class="m-0">用户数据表格</h4>
        </div>
      </template>

      <ArtTableHeader
        v-model:columns="columnChecks"
        :loading="loading"
        layout="refresh,size,fullscreen,columns,settings"
        full-class="art-table-card"
        @refresh="handleRefresh"
      >
        <template #left>
          <ElSpace wrap>
            <ElButton type="primary" @click="handleAdd" v-ripple>
              <ElIcon>
                <Plus />
              </ElIcon>
              新增用户
            </ElButton>

            <ArtExcelExport
              :data="data as any"
              :columns="exportColumns as any"
              filename="用户数据"
              :auto-index="true"
              button-text="导出"
              @export-success="handleExportSuccess"
            />
            <ArtExcelImport
              style="margin: 0 12px"
              @import-success="handleImportSuccess"
              @import-error="handleImportError"
            />

            <ElButton plain v-ripple @click="handleClearData">清空数据</ElButton>

            <ElButton :disabled="selectedRows.length === 0" v-ripple @click="handleBatchDelete">
              <ElIcon>
                <Delete />
              </ElIcon>
              批量删除 ({{ selectedRows.length }})
            </ElButton>

            <ElDropdown style="margin-left: 10px" @command="handleColumnCommand">
              <ElButton type="primary" plain>
                动态更新表格列
                <ElIcon class="el-icon--right">
                  <ArrowDown />
                </ElIcon>
              </ElButton>
              <template #dropdown>
                <ElDropdownMenu>
                  <ElDropdownItem command="addColumn">新增列（备注列）</ElDropdownItem>
                  <ElDropdownItem command="batchAddColumns">批量新增（备注、标签）</ElDropdownItem>
                  <ElDropdownItem command="toggleColumn">切换列（手机号）</ElDropdownItem>
                  <ElDropdownItem command="batchToggleColumns">
                    批量切换（性别、手机号）
                  </ElDropdownItem>
                  <ElDropdownItem command="removeColumn">删除列（状态列）</ElDropdownItem>
                  <ElDropdownItem command="batchRemoveColumns">
                    批量删除（状态、评分）
                  </ElDropdownItem>
                  <ElDropdownItem command="updateColumn">更新列（手机号）</ElDropdownItem>
                  <ElDropdownItem command="batchUpdateColumns">
                    批量更新（性别、手机号）
                  </ElDropdownItem>
                  <ElDropdownItem command="reorderColumns">
                    交换列位置（性别、手机号）
                  </ElDropdownItem>
                  <ElDropdownItem command="resetColumns" divided>重置所有列配置</ElDropdownItem>
                </ElDropdownMenu>
              </template>
            </ElDropdown>
          </ElSpace>
        </template>
      </ArtTableHeader>

      <ArtTable
        ref="tableRef"
        :loading="loading"
        :pagination="artPagination"
        :data="data as Record<string, any>[]"
        :columns="columns"
        :height="computedTableHeight"
        empty-height="360px"
        class="min-h-0 flex-1"
        @selection-change="handleSelectionChange"
        @row-click="handleRowClick"
        @header-click="handleHeaderClick"
        @sort-change="handleSortChange"
        @pagination:size-change="handleSizeChange"
        @pagination:current-change="handleCurrentChange"
      >
        <template #avatar="{ row }">
          <div class="flex gap-3 user-info">
            <ElAvatar :src="row.avatar" :size="40" />
            <div class="flex-1 min-w-0">
              <p class="m-0 overflow-hidden font-medium text-ellipsis whitespace-nowrap">
                {{ row.userName }}
              </p>
              <p
                class="m-0 mt-1 overflow-hidden text-xs text-g-700 text-ellipsis whitespace-nowrap"
              >
                {{ row.userEmail }}
              </p>
            </div>
          </div>
        </template>

        <template #avatar-header="{ column }">
          <div class="flex-c gap-1">
            <span>{{ column.label }}</span>
            <ElTooltip content="包含头像、姓名和邮箱" placement="top">
              <ElIcon>
                <QuestionFilled />
              </ElIcon>
            </ElTooltip>
          </div>
        </template>

        <template #status="{ row }">
          <ElTag :type="getUserStatusConfig(row.status).type" effect="light">
            {{ getUserStatusConfig(row.status).text }}
          </ElTag>
        </template>

        <template #score="{ row }">
          <ElRate v-model="row.score" disabled size="small" />
        </template>

        <template #operation="{ row }">
          <div class="flex">
            <ArtButtonTable type="view" :row="row" @click="handleView(row)" />
            <ArtButtonTable type="add" :row="row" @click="handleAdd()" />
            <ArtButtonTable type="edit" :row="row" @click="handleEdit(row)" />
            <ArtButtonTable type="delete" :row="row" @click="handleDelete(row)" />
          </div>
        </template>

        <template #userPhone-header="{ column }">
          <ElPopover placement="bottom" :width="200" trigger="hover">
            <template #reference>
              <div class="inline-block gap-1 text-theme c-p custom-header">
                <span>{{ column.label }}</span>
                <ElIcon>
                  <Search />
                </ElIcon>
              </div>
            </template>
            <ElInput
              v-model="phoneSearch"
              placeholder="搜索手机号"
              size="small"
              @input="handlePhoneSearch"
            >
              <template #prefix>
                <ElIcon>
                  <Search />
                </ElIcon>
              </template>
            </ElInput>
          </ElPopover>
        </template>
      </ArtTable>
    </ElCard>
  </CrudLayout>
</template>

<script setup lang="ts">
import { Plus, Delete, Search, QuestionFilled, ArrowDown } from "@element-plus/icons-vue";
import CrudLayout from "./CrudLayout.vue";
import { useCrudArtTableDemo } from "./useCrudArtTableDemo";

defineOptions({ name: "CrudArtTableDemo" });

const {
  searchBarRef,
  searchFormState,
  searchItems,
  rules,
  phoneSearch,
  selectedRows,
  tableRef,
  columnChecks,
  loading,
  data,
  artPagination,
  columns,
  computedTableHeight,
  exportColumns,
  getUserStatusConfig,
  handleSearch,
  handleReset,
  handlePhoneSearch,
  handleRefresh,
  handleSelectionChange,
  handleRowClick,
  handleHeaderClick,
  handleSortChange,
  handleSizeChange,
  handleCurrentChange,
  handleAdd,
  handleEdit,
  handleDelete,
  handleView,
  handleBatchDelete,
  handleExportSuccess,
  handleImportSuccess,
  handleImportError,
  handleClearData,
  handleColumnCommand,
} = useCrudArtTableDemo();
</script>

<style scoped>
.user-info .el-avatar {
  flex-shrink: 0;
  width: 40px !important;
  height: 40px !important;
}

.user-info .el-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.custom-header:hover {
  color: var(--el-color-primary-light-3);
}
</style>
