<!-- 菜单管理 -->
<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div class="search-container">
      <el-form
        ref="queryFormRef"
        :model="queryFormData"
        :inline="true"
        label-suffix=":"
        @submit.prevent="handleQuery"
      >
        <el-form-item prop="name" label="菜单名称">
          <el-input v-model="queryFormData.name" placeholder="请输入菜单名称" clearable />
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
          <el-button
            v-hasPerm="['module_system:menu:query']"
            type="primary"
            icon="search"
            native-type="submit"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_system:menu:query']"
            icon="refresh"
            @click="handleResetQuery"
          >
            重置
          </el-button>
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
            <el-tooltip content="菜单管理系统的菜单和权限。">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
            菜单列表
          </span>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--left">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_system:menu:create']"
                type="success"
                icon="plus"
                @click="handleOpenDialog('create')"
              >
                新增
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_system:menu:delete']"
                type="danger"
                icon="delete"
                :disabled="selectIds.length === 0"
                @click="handleDelete(selectIds)"
              >
                批量删除
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-dropdown v-hasPerm="['module_system:menu:patch']" trigger="click">
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
              <el-tooltip content="刷新">
                <el-button
                  v-hasPerm="['module_system:menu:query']"
                  type="primary"
                  icon="refresh"
                  circle
                  @click="handleRefresh"
                />
              </el-tooltip>
            </el-col>
          </el-row>
        </div>
      </div>

      <!-- 表格区域 -->
      <el-table
        ref="dataTableRef"
        v-loading="loading"
        row-key="id"
        :data="pageTableData"
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
        class="data-table__content"
        :height="540"
        border
        stripe
        @selection-change="handleSelectionChange"
        @row-click="handleRowClick"
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column type="selection" min-width="55" align="center" />
        <el-table-column type="index" fixed label="序号" min-width="60" />
        <el-table-column label="菜单名称" prop="name" min-width="240" />
        <el-table-column label="图标" prop="icon" min-width="80" align="center">
          <template #default="scope">
            <template v-if="scope.row.icon && scope.row.icon.startsWith('el-icon')">
              <el-icon style="vertical-align: -0.15em">
                <component :is="scope.row.icon.replace('el-icon-', '')" />
              </el-icon>
            </template>
            <template v-else-if="scope.row.icon">
              <div :class="`i-svg:${scope.row.icon}`" />
            </template>
          </template>
        </el-table-column>
        <el-table-column label="状态" prop="status" min-width="80" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.status === '0' ? 'success' : 'danger'">
              {{ scope.row.status ? "启用" : "停用" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="类型" prop="type" min-width="80" align="center">
          <template #default="scope">
            <el-tag v-if="scope.row.type === MenuTypeEnum.CATALOG" type="warning">目录</el-tag>
            <el-tag v-if="scope.row.type === MenuTypeEnum.MENU" type="success">菜单</el-tag>
            <el-tag v-if="scope.row.type === MenuTypeEnum.BUTTON" type="danger">按钮</el-tag>
            <el-tag v-if="scope.row.type === MenuTypeEnum.EXTLINK" type="info">外链</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="排序" prop="order" min-width="80" />
        <el-table-column label="重定向" prop="redirect" min-width="200" />
        <el-table-column label="是否缓存" prop="keep_alive" min-width="100">
          <template #default="scope">
            <el-tag :type="scope.row.keep_alive ? 'success' : 'danger'">
              {{ scope.row.keep_alive ? "是" : "否" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="是否隐藏" prop="hidden" min-width="100">
          <template #default="scope">
            <el-tag :type="scope.row.hidden ? 'success' : 'danger'">
              {{ scope.row.hidden ? "是" : "否" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="显示根路由" prop="always_show" min-width="120">
          <template #default="scope">
            <el-tag :type="scope.row.always_show ? 'success' : 'danger'">
              {{ scope.row.always_show ? "是" : "否" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="固定路由" prop="affix" min-width="100">
          <template #default="scope">
            <el-tag :type="scope.row.affix ? 'success' : 'danger'">
              {{ scope.row.affix ? "是" : "否" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="菜单标题" prop="title" min-width="200" />
        <el-table-column label="权限标识" prop="permission" min-width="220" />
        <el-table-column label="路由名称" prop="route_name" min-width="200" />
        <el-table-column label="路由路径" prop="route_path" min-width="200" />
        <el-table-column label="组件路径" prop="component_path" min-width="200" />
        <el-table-column label="路由参数" prop="params" min-width="100" />
        <el-table-column label="描述" prop="description" min-width="200" />
        <el-table-column label="创建时间" prop="created_time" min-width="200" sortable />
        <el-table-column label="更新时间" prop="updated_time" min-width="200" sortable />

        <el-table-column fixed="right" label="操作" align="center" min-width="260">
          <template #default="scope">
            <el-button
              v-if="scope.row.type == MenuTypeEnum.CATALOG || scope.row.type == MenuTypeEnum.MENU"
              v-hasPerm="['module_system:menu:create']"
              type="success"
              link
              size="small"
              icon="plus"
              @click.stop="handleOpenDialog('create', undefined, scope.row.id)"
            >
              新增
            </el-button>
            <el-button
              v-hasPerm="['module_system:menu:query']"
              type="info"
              size="small"
              link
              icon="document"
              @click="handleOpenDialog('detail', scope.row.id)"
            >
              详情
            </el-button>
            <el-button
              v-hasPerm="['module_system:menu:update']"
              type="primary"
              size="small"
              link
              icon="edit"
              @click="handleOpenDialog('update', scope.row.id)"
            >
              编辑
            </el-button>
            <el-button
              v-hasPerm="['module_system:menu:delete']"
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
    </el-card>

    <!-- 弹窗区域 -->
    <el-drawer
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      :size="drawerSize"
      @close="handleCloseDialog"
    >
      <!-- 详情 -->
      <template v-if="dialogVisible.type === 'detail'">
        <el-descriptions :column="4" border>
          <el-descriptions-item label="编号" :span="2">
            {{ detailFormData.id }}
          </el-descriptions-item>
          <el-descriptions-item label="菜单名称" :span="2">
            {{ detailFormData.name }}
          </el-descriptions-item>
          <el-descriptions-item label="菜单类型" :span="2">
            <el-tag v-if="detailFormData.type === MenuTypeEnum.CATALOG" type="warning">目录</el-tag>
            <el-tag v-if="detailFormData.type === MenuTypeEnum.MENU" type="success">菜单</el-tag>
            <el-tag v-if="detailFormData.type === MenuTypeEnum.BUTTON" type="danger">按钮</el-tag>
            <el-tag v-if="detailFormData.type === MenuTypeEnum.EXTLINK" type="info">外链</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="图标" :span="2">
            <template #default>
              <template v-if="detailFormData.icon && detailFormData.icon.startsWith('el-icon')">
                <el-icon style="vertical-align: -0.15em">
                  <component :is="detailFormData.icon.replace('el-icon-', '')" />
                </el-icon>
              </template>
              <template v-else-if="detailFormData.icon">
                <div :class="`i-svg:${detailFormData.icon}`" />
              </template>
            </template>
          </el-descriptions-item>
          <el-descriptions-item label="排序" :span="2">
            {{ detailFormData.order }}
          </el-descriptions-item>
          <el-descriptions-item label="权限标识" :span="2">
            {{ detailFormData.permission }}
          </el-descriptions-item>
          <el-descriptions-item label="路由名称" :span="2">
            {{ detailFormData.route_name }}
          </el-descriptions-item>
          <el-descriptions-item label="路由路径" :span="2">
            {{ detailFormData.route_path }}
          </el-descriptions-item>
          <el-descriptions-item label="组件路径" :span="2">
            {{ detailFormData.component_path }}
          </el-descriptions-item>
          <el-descriptions-item label="重定向" :span="2">
            {{ detailFormData.redirect }}
          </el-descriptions-item>
          <el-descriptions-item label="父级编号" :span="2">
            {{ detailFormData.parent_id }}
          </el-descriptions-item>
          <el-descriptions-item label="父级菜单" :span="2">
            {{ detailFormData.parent_name }}
          </el-descriptions-item>
          <el-descriptions-item label="是否缓存" :span="2">
            <el-tag :type="detailFormData.keep_alive ? 'success' : 'danger'">
              {{ detailFormData.keep_alive ? "是" : "否" }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="是否显示" :span="2">
            <el-tag :type="detailFormData.hidden ? 'success' : 'danger'">
              {{ detailFormData.hidden ? "是" : "否" }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="是否显示根路由" :span="2">
            <el-tag :type="detailFormData.always_show ? 'success' : 'danger'">
              {{ detailFormData.always_show ? "是" : "否" }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="菜单标题" :span="2">
            {{ detailFormData.title }}
          </el-descriptions-item>
          <el-descriptions-item label="路由参数" :span="2">
            {{ detailFormData.params }}
          </el-descriptions-item>
          <el-descriptions-item label="是否固定路由" :span="2">
            <el-tag :type="detailFormData.affix ? 'success' : 'danger'">
              {{ detailFormData.affix ? "是" : "否" }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态" :span="2">
            <el-tag :type="detailFormData.status ? 'success' : 'danger'">
              {{ detailFormData.status ? "启用" : "停用" }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="排序" :span="2">
            {{ detailFormData.order }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">
            {{ detailFormData.created_time }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间" :span="2">
            {{ detailFormData.updated_time }}
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="4">
            {{ detailFormData.description }}
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
          <el-form-item
            v-if="formData.type !== MenuTypeEnum.CATALOG"
            label="父级菜单"
            prop="parent_id"
            if
          >
            <el-tree-select
              v-model="formData.parent_id"
              placeholder="选择上级菜单"
              :data="menuOptions"
              filterable
              check-strictly
              :render-after-expand="false"
            />
          </el-form-item>

          <el-form-item label="菜单名称" prop="name">
            <el-input v-model="formData.name" placeholder="请输入菜单名称" />
          </el-form-item>

          <el-form-item label="菜单标题" prop="title">
            <el-input v-model="formData.title" placeholder="请输入菜单标题" />
          </el-form-item>

          <el-form-item label="菜单类型" prop="type">
            <el-radio-group v-model="formData.type" @change="handleMenuTypeChange">
              <el-radio :value="MenuTypeEnum.CATALOG">目录</el-radio>
              <el-radio :value="MenuTypeEnum.MENU">菜单</el-radio>
              <el-radio :value="MenuTypeEnum.BUTTON">按钮</el-radio>
              <el-radio :value="MenuTypeEnum.EXTLINK">外链</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item v-if="formData.type == MenuTypeEnum.EXTLINK" label="外链地址" prop="path">
            <el-input v-model="formData.route_path" placeholder="请输入外链完整路径" />
          </el-form-item>

          <el-form-item v-if="formData.type !== MenuTypeEnum.BUTTON" prop="route_name">
            <template #label>
              <div class="flex-y-center">
                路由名称
                <el-tooltip placement="bottom" effect="light">
                  <template #content>
                    如果需要开启缓存，需保证页面 defineOptions 中的 name 与此处一致，建议使用驼峰。
                  </template>
                  <el-icon class="ml-1 cursor-pointer">
                    <QuestionFilled />
                  </el-icon>
                </el-tooltip>
              </div>
            </template>
            <el-input v-model="formData.route_name" placeholder="请输入路由名称" />
          </el-form-item>

          <el-form-item
            v-if="formData.type == MenuTypeEnum.CATALOG || formData.type == MenuTypeEnum.MENU"
            prop="route_path"
          >
            <template #label>
              <div class="flex-y-center">
                路由路径
                <el-tooltip placement="bottom" effect="light">
                  <template #content>
                    定义应用中不同页面对应的 URL 路径，目录需以 /
                    开头，菜单项不用。例如：系统管理目录 /system，系统管理下的用户管理菜单 user。
                  </template>
                  <el-icon class="ml-1 cursor-pointer">
                    <QuestionFilled />
                  </el-icon>
                </el-tooltip>
              </div>
            </template>
            <el-input v-model="formData.route_path" placeholder="请输入路由路径,如：/system" />
          </el-form-item>

          <el-form-item v-if="formData.type == MenuTypeEnum.MENU" prop="component">
            <template #label>
              <div class="flex-y-center">
                组件路径
                <el-tooltip placement="bottom" effect="light">
                  <template #content>
                    组件页面完整路径，相对于 src/views/，如 system/user/index，缺省后缀 .vue
                  </template>
                  <el-icon class="ml-1 cursor-pointer">
                    <QuestionFilled />
                  </el-icon>
                </el-tooltip>
              </div>
            </template>

            <el-input
              v-model="formData.component_path"
              placeholder="请输入组件路径，如system/user/index"
              style="width: 95%"
            >
              <template v-if="formData.type == MenuTypeEnum.MENU" #prepend>src/views/</template>
              <template v-if="formData.type == MenuTypeEnum.MENU" #append>.vue</template>
            </el-input>
          </el-form-item>

          <el-form-item v-if="formData.type == MenuTypeEnum.MENU">
            <template #label>
              <div class="flex-y-center">
                路由参数
                <el-tooltip placement="bottom" effect="light">
                  <template #content>
                    组件页面使用 `useRoute().query.参数名` 获取路由参数值。
                  </template>
                  <el-icon class="ml-1 cursor-pointer">
                    <QuestionFilled />
                  </el-icon>
                </el-tooltip>
              </div>
            </template>

            <div
              v-if="
                !formData.params || (Array.isArray(formData.params) && formData.params.length === 0)
              "
            >
              <el-button type="success" plain @click="formData.params = [{ key: '', value: '' }]">
                添加路由参数
              </el-button>
            </div>

            <div v-else>
              <div v-for="(item, index) in formData.params" :key="index">
                <el-input v-model="item.key" placeholder="参数名" style="width: 100px" />

                <span class="mx-1">=</span>

                <el-input v-model="item.value" placeholder="参数值" style="width: 100px" />

                <el-icon
                  v-if="formData.params.indexOf(item) === formData.params.length - 1"
                  class="ml-2 cursor-pointer color-[var(--el-color-success)]"
                  style="vertical-align: -0.15em"
                  @click="formData.params.push({ key: '', value: '' })"
                >
                  <CirclePlusFilled />
                </el-icon>
                <el-icon
                  class="ml-2 cursor-pointer color-[var(--el-color-danger)]"
                  style="vertical-align: -0.15em"
                  @click="formData.params.splice(formData.params.indexOf(item), 1)"
                >
                  <DeleteFilled />
                </el-icon>
              </div>
            </div>
          </el-form-item>

          <el-form-item v-if="formData.type !== MenuTypeEnum.BUTTON">
            <template #label>
              <div class="flex-y-center">
                是否隐藏
                <el-tooltip placement="bottom" effect="light">
                  <template #content>
                    选择"是", 菜单中隐藏
                    <br />
                    选择"否"，菜单中显示。
                    <br />
                  </template>
                  <el-icon class="ml-1 cursor-pointer">
                    <QuestionFilled />
                  </el-icon>
                </el-tooltip>
              </div>
            </template>

            <el-radio-group v-model="formData.hidden">
              <el-radio :value="true">是</el-radio>
              <el-radio :value="false">否</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item
            v-if="formData.type === MenuTypeEnum.CATALOG || formData.type === MenuTypeEnum.MENU"
          >
            <template #label>
              <div class="flex-y-center">
                始终显示
                <el-tooltip placement="bottom" effect="light">
                  <template #content>
                    选择"是"，即使目录或菜单下只有一个子节点，也会显示父节点。
                    <br />
                    选择"否"，如果目录或菜单下只有一个子节点，则只显示该子节点，隐藏父节点。
                    <br />
                    如果是叶子节点，请选择"否"。
                  </template>
                  <el-icon class="ml-1 cursor-pointer">
                    <QuestionFilled />
                  </el-icon>
                </el-tooltip>
              </div>
            </template>

            <el-radio-group v-model="formData.always_show">
              <el-radio :value="true">是</el-radio>
              <el-radio :value="false">否</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item v-if="formData.type === MenuTypeEnum.MENU" label="缓存页面">
            <el-radio-group v-model="formData.keep_alive">
              <el-radio :value="true">开启</el-radio>
              <el-radio :value="false">关闭</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="排序" prop="order">
            <el-input-number v-model="formData.order" controls-position="right" :min="1" />
          </el-form-item>

          <!-- 权限标识 -->
          <el-form-item
            v-if="formData.type == MenuTypeEnum.BUTTON || formData.type === MenuTypeEnum.MENU"
            label="权限标识"
            prop="perm"
          >
            <el-input v-model="formData.permission" placeholder="请输入权限标识，如sys:user:add" />
          </el-form-item>

          <el-form-item v-if="formData.type !== MenuTypeEnum.BUTTON" label="图标" prop="icon">
            <!-- 图标选择器 -->
            <icon-select v-model="formData.icon" />
          </el-form-item>

          <el-form-item
            v-if="formData.type == MenuTypeEnum.CATALOG || formData.type === MenuTypeEnum.MENU"
            label="重定向"
            prop="redirect"
          >
            <el-input v-model="formData.redirect" placeholder="请输入重定向路由" />
          </el-form-item>

          <el-form-item v-if="formData.type != MenuTypeEnum.BUTTON" label="常驻标签栏" prop="affix">
            <el-radio-group v-model="formData.affix">
              <el-radio :value="true">是</el-radio>
              <el-radio :value="false">否</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="状态" prop="status">
            <el-radio-group v-model="formData.status">
              <el-radio value="0">启用</el-radio>
              <el-radio value="1">禁用</el-radio>
            </el-radio-group>
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
          <el-button v-if="dialogVisible.type !== 'detail'" type="primary" @click="handleSubmit">
            确定
          </el-button>
          <el-button v-else type="primary" @click="handleCloseDialog">确定</el-button>
          <el-button @click="handleCloseDialog">取消</el-button>
        </div>
      </template>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "SysMenu",
  inheritAttrs: false,
});

import { useAppStore } from "@/store/modules/app.store";
import { useUserStore } from "@/store/modules/user.store";
import { DeviceEnum } from "@/enums/settings/device.enum";

import MenuAPI, { MenuPageQuery, MenuForm, MenuTable } from "@/api/module_system/menu";
import { MenuTypeEnum } from "@/enums/system/menu.enum";
import { formatTree } from "@/utils/common";
import { formatToDateTime } from "@/utils/dateUtil";

const appStore = useAppStore();
const userStore = useUserStore();

const queryFormRef = ref();
const dataFormRef = ref();
const selectIds = ref<number[]>([]);
const loading = ref(false);

const isExpand = ref(false);
const isExpandable = ref(true);

// 分页表单
const pageTableData = ref<MenuTable[]>([]);

// 详情表单
const detailFormData = ref<MenuTable>({});

// 分页查询参数
const queryFormData = reactive<MenuPageQuery>({
  name: undefined,
  status: undefined,
  created_time: undefined,
});

// 编辑表单
const formData = reactive<MenuForm>({
  id: undefined,
  name: undefined,
  type: MenuTypeEnum.CATALOG,
  icon: undefined,
  order: 999,
  permission: "",
  route_name: "",
  route_path: "",
  component_path: undefined,
  redirect: undefined,
  parent_id: undefined,
  keep_alive: false,
  hidden: false,
  always_show: false,
  title: "",
  params: undefined,
  affix: false,
  status: '0',
  description: undefined,
});

// 弹窗状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "600px" : "90%"));

// 顶级菜单下拉选项
const menuOptions = ref<OptionType[]>([]);

// 表单验证规则
const rules = reactive({
  name: [
    { required: true, message: "请输入菜单名称", trigger: "blur" },
    { min: 2, max: 50, message: "长度 2 到 50 个字符", trigger: "blur" },
  ],
  parent_id: [{ required: true, message: "请选择父级菜单", trigger: "blur" }],
  type: [{ required: true, message: "请选择菜单类型", trigger: "blur" }],
  order: [{ required: true, message: "请输入排序", trigger: "blur" }],
  permission: [{ required: true, message: "请输入权限标识", trigger: "blur" }],
  route_name: [{ required: true, message: "请输入路由名称", trigger: "blur" }],
  route_path: [
    { required: true, message: "请输入路由路径", trigger: "blur" },
    {
      validator: (rule: any, value: string, callback: any) => {
        if (value && !value.startsWith("/")) {
          callback(new Error("目录和菜单路由必须以/开头"));
        } else {
          callback();
        }
      },
      trigger: "blur",
    },
  ],
  component_path: [{ required: true, message: "请输入组件路径", trigger: "blur" }],
  title: [
    { required: true, message: "请输入菜单标题", trigger: "blur" },
    { min: 2, max: 50, message: "长度 2 到 50 个字符", trigger: "blur" },
  ],
  keep_alive: [{ required: true, message: "请选择是否缓存", trigger: "change" }],
  hidden: [{ required: true, message: "请选择是否隐藏", trigger: "change" }],
  always_show: [{ required: true, message: "请选择始终显示", trigger: "change" }],
  status: [{ required: true, message: "请选择状态", trigger: "change" }],
});

// 选择表格的行菜单ID
const selectedMenuId = ref<number | undefined>();

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
  loading.value = true;
  try {
    const response = await MenuAPI.listMenu(queryFormData);
    pageTableData.value = response.data.data;
  } catch (error: any) {
    console.error(error);
  } finally {
    loading.value = false;
  }
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

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    const response = await MenuAPI.listMenu(queryFormData);
    pageTableData.value = response.data.data;
    // 加载菜单选项，只显示目录、菜单
    menuOptions.value = formatTree(filterMenuTypes(response.data.data));
  } catch (error: any) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

// 查询（重置页码后获取数据）
async function handleQuery() {
  loadingData();
}

// 重置查询
async function handleResetQuery() {
  queryFormRef.value.resetFields();
  // 额外清空日期范围与时间查询参数
  dateRange.value = [];
  queryFormData.created_time = undefined;
  handleQuery();
}

// 定义初始表单数据常量
const initialFormData: MenuForm = {
  id: undefined,
  name: undefined,
  type: MenuTypeEnum.MENU,
  icon: undefined,
  order: 1,
  permission: "",
  route_name: "",
  route_path: "",
  component_path: "",
  redirect: "",
  parent_id: undefined,
  keep_alive: false,
  hidden: false,
  always_show: false,
  title: "",
  params: [] as { key: string; value: string }[],
  affix: false,
  status: '0',
  description: undefined,
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
}

// 行点击事件
async function handleRowClick(row: MenuTable) {
  selectedMenuId.value = row.id;
}

// 关闭弹窗
async function handleCloseDialog() {
  dialogVisible.visible = false;
  resetForm();
}

//打开弹窗
async function handleOpenDialog(
  type: "create" | "update" | "detail",
  id?: number,
  parentId?: number
) {
  dialogVisible.type = type;
  if (id) {
    const response = await MenuAPI.detailMenu(id);
    if (type === "detail") {
      dialogVisible.title = "菜单详情";
      Object.assign(detailFormData.value, response.data.data);
    } else if (type === "update") {
      dialogVisible.title = "修改菜单";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增菜单";
    formData.id = undefined;
    // 设置父级部门
    if (parentId) {
      formData.parent_id = parentId;
    }
  }
  dialogVisible.visible = true;
}

// 菜单类型切换
function handleMenuTypeChange() {
  // 如果菜单类型改变
  if (formData.type !== formData.type) {
    if (formData.type === MenuTypeEnum.MENU) {
      // 目录切换到菜单时，清空组件路径
      formData.component_path = "";
    }
  }
}

// 提交表单
async function handleSubmit() {
  // 表单校验
  dataFormRef.value.validate(async (valid: any) => {
    if (valid) {
      loading.value = true;
      // 根据弹窗传入的参数(deatil\create\update)判断走什么逻辑
      const id = formData.id;
      try {
        if (id) {
          await MenuAPI.updateMenu(id, formData);
        } else {
          await MenuAPI.createMenu(formData);
        }
        await userStore.getUserInfo();
        dialogVisible.visible = false;
        resetForm();
        handleResetQuery();
      } catch (error: any) {
        console.error(error);
      } finally {
        loading.value = false;
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
        await MenuAPI.deleteMenu(ids);
        await userStore.getUserInfo();
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

// 批量启用/停用
async function handleMoreClick(status: string) {
  ElMessageBox.confirm(`确认${status === "0" ? "启用" : "停用"}该项数据?`, "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        loading.value = true;
        await MenuAPI.batchMenu({ ids: selectIds.value, status });
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

onMounted(() => {
  handleQuery();
});
</script>
