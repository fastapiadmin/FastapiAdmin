<!-- 在线用户 -->
<template>
  <div class="app-container">
    <CrudSearch
      ref="searchRef"
      :search-config="searchConfig"
      @query-click="handleQueryClick"
      @reset-click="handleResetClick"
    />

    <CrudContent ref="contentRef" :content-config="contentConfig">
      <!-- eslint-disable-next-line vue/no-unused-vars -- 与 demo 同源解构，本页无批删逻辑 -->
      <template #toolbar="{ toolbarRight, onToolbar, removeIds, cols }">
        <CrudToolbarLeft>
          <el-button
            v-hasPerm="['module_monitor:online:delete']"
            type="danger"
            icon="delete"
            @click="handleClear"
          >
            强退所有
          </el-button>
        </CrudToolbarLeft>
        <div class="data-table__toolbar--right">
          <CrudToolbarActions :buttons="toolbarRight" :cols="cols" :on-toolbar="onToolbar" />
        </div>
      </template>

      <template #table="{ data, loading, tableRef, onSelectionChange, pagination }">
        <div class="data-table__content">
          <el-table
            :ref="tableRef as any"
            v-loading="loading"
            :data="data"
            height="100%"
            border
            stripe
            @selection-change="onSelectionChange"
          >
            <template #empty>
              <el-empty :image-size="80" description="暂无数据" />
            </template>

            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'selection')?.show"
              type="selection"
              min-width="55"
              align="center"
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'index')?.show"
              type="index"
              fixed
              label="序号"
              min-width="60"
            >
              <template #default="scope">
                {{ (pagination.currentPage - 1) * pagination.pageSize + scope.$index + 1 }}
              </template>
            </el-table-column>
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'session_id')?.show"
              key="session_id"
              label="会话编号"
              prop="session_id"
              min-width="250"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'login_type')?.show"
              key="login_type"
              label="登录类型"
              prop="login_type"
              min-width="100"
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'ipaddr')?.show"
              key="ipaddr"
              label="IP地址"
              prop="ipaddr"
              min-width="150"
              show-overflow-tooltip
            >
              <template #default="scope">
                <el-text>{{ scope.row.ipaddr }}</el-text>
                <CopyButton
                  v-if="scope.row.ipaddr"
                  :text="scope.row.ipaddr"
                  :style="{ marginLeft: '2px' }"
                />
              </template>
            </el-table-column>
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'name')?.show"
              key="name"
              label="用户名"
              prop="name"
              min-width="80"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'user_name')?.show"
              key="user_name"
              label="账号"
              prop="user_name"
              min-width="80"
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'login_location')?.show"
              key="login_location"
              label="登录位置"
              prop="login_location"
              min-width="280"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'os')?.show"
              key="os"
              label="操作系统"
              prop="os"
              min-width="120"
              show-overflow-tooltip
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'login_time')?.show"
              key="login_time"
              label="登录时间"
              prop="login_time"
              min-width="180"
            />
            <el-table-column
              v-if="contentCols.find((col) => col.prop === 'operation')?.show"
              key="operation"
              fixed="right"
              label="操作"
              min-width="100"
            >
              <template #default="scope">
                <el-button
                  v-hasPerm="['module_monitor:online:delete']"
                  type="danger"
                  size="small"
                  link
                  icon="delete"
                  @click="handleSubmit(scope.row.session_id)"
                >
                  强退
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </template>
    </CrudContent>
  </div>
</template>

<script lang="ts" setup>
defineOptions({
  name: "OnlineUser",
  inheritAttrs: false,
});

import OnlineAPI, { type OnlineUserPageQuery } from "@/api/module_monitor/online";
import { reactive } from "vue";
import CrudToolbarLeft from "@/components/CURD/CrudToolbarLeft.vue";
import { CrudToolbarActions } from "@/components/Crud";
import CrudSearch from "@/components/CURD/CrudSearch.vue";
import CrudContent from "@/components/CURD/CrudContent.vue";
import { useCrudList } from "@/components/Crud/useCrudList";
import type { ISearchConfig, IContentConfig } from "@/components/Crud/types";

const { searchRef, contentRef, handleQueryClick, handleResetClick, refreshList } = useCrudList();

const searchConfig = reactive<ISearchConfig>({
  permPrefix: "module_monitor:online",
  colon: true,
  isExpandable: false,
  showNumber: 3,
  form: { labelWidth: "auto" },
  formItems: [
    {
      prop: "ipaddr",
      label: "IP地址",
      type: "input",
      attrs: { placeholder: "请输入IP地址", clearable: true },
    },
    {
      prop: "name",
      label: "用户名",
      type: "input",
      attrs: { placeholder: "请输入用户名", clearable: true },
    },
    {
      prop: "login_location",
      label: "登录位置",
      type: "input",
      attrs: { placeholder: "请输入登录位置", clearable: true },
    },
  ],
});

const contentCols = reactive<
  Array<{
    prop?: string;
    label?: string;
    show?: boolean;
  }>
>([
  { prop: "selection", label: "选择框", show: true },
  { prop: "index", label: "序号", show: true },
  { prop: "session_id", label: "会话编号", show: true },
  { prop: "login_type", label: "登录类型", show: true },
  { prop: "name", label: "登录名称", show: true },
  { prop: "user_name", label: "用户账号", show: true },
  { prop: "ipaddr", label: "主机", show: true },
  { prop: "login_location", label: "登录地点", show: true },
  { prop: "os", label: "操作系统", show: true },
  { prop: "login_time", label: "登录时间", show: true },
  { prop: "operation", label: "操作", show: true },
]);

const contentConfig = reactive<IContentConfig<OnlineUserPageQuery>>({
  permPrefix: "module_monitor:online",
  cols: contentCols as IContentConfig["cols"],
  hideColumnFilter: false,
  toolbar: [],
  defaultToolbar: ["refresh", "filter"],
  pagination: {
    pageSize: 10,
    pageSizes: [10, 20, 30, 50],
  },
  request: { page_no: "page_no", page_size: "page_size" },
  indexAction: async (params) => {
    const res = await OnlineAPI.listOnline(params as OnlineUserPageQuery);
    return {
      total: res.data.data.total,
      list: res.data.data.items,
    };
  },
});

async function handleSubmit(session_id: string) {
  ElMessageBox.confirm(`确认强制退出会话 ${session_id}?`, "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        await OnlineAPI.deleteOnline(session_id);
        refreshList();
      } catch (error: unknown) {
        console.error(error);
      }
    })
    .catch(() => {
      ElMessageBox.close();
    });
}

async function handleClear() {
  ElMessageBox.confirm("确认强制退出所有用户?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        await OnlineAPI.clearOnline();
        refreshList();
      } catch (error: unknown) {
        console.error(error);
      }
    })
    .catch(() => {
      ElMessageBox.close();
    });
}
</script>

<style lang="scss" scoped></style>
