<!-- 菜单管理：Art + 树形表格（对齐 system/menu 模版） -->
<template>
  <div class="art-full-height">
    <ArtSearchBar
      v-show="showSearchBar"
      ref="searchBarRef"
      v-model="searchForm"
      :items="menuSearchItems"
      :rules="searchBarRules"
      :is-expand="false"
      :show-expand="true"
      :show-reset="true"
      :show-search="true"
      :disabled-search="false"
      :default-expanded="false"
      @search="handleSearchBarSearch"
      @reset="onResetSearch"
    />

    <ElTabs
      v-model="menuClientTab"
      class="menu-client-tabs px-1 mb-2"
      @tab-change="handleMenuClientTabChange"
    >
      <ElTabPane label="PC 桌面菜单管理" name="pc" />
      <ElTabPane label="APP 移动端菜单管理" name="app" />
    </ElTabs>

    <ElCard class="art-table-card" :style="{ 'margin-top': showSearchBar ? '12px' : '0' }">
      <ArtTableHeader
        v-model:columns="columnChecks"
        v-model:showSearchBar="showSearchBar"
        :loading="loading"
        :show-zebra="false"
        @refresh="loadMenuData"
      >
        <template #left>
          <div class="inline-flex flex-wrap items-center gap-2">
            <ArtTableHeaderLeft
              :remove-ids="selectedIds"
              :perm-create="['module_system:menu:create']"
              :perm-delete="['module_system:menu:delete']"
              :perm-patch="['module_system:menu:patch']"
              :delete-loading="batchDeleting"
              @add="handleOpenDialog('create')"
              @delete="handleBatchDelete"
              @more="handleMoreClick"
            />
            <ElButton @click="toggleExpand">{{ isExpanded ? "收起" : "展开" }}</ElButton>
          </div>
        </template>
      </ArtTableHeader>

      <ArtTable
        ref="tableRef"
        row-key="id"
        :loading="loading"
        :columns="columns"
        :data="tableData"
        :stripe="false"
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
        :default-expand-all="false"
        @selection-change="onTableSelectionChange"
        @row-click="handleRowClick"
      />
    </ElCard>

    <ArtDrawer
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      :size="drawerSize"
      @close="handleCloseDialog"
    >
      <!-- 详情 -->
      <template v-if="dialogVisible.type === 'detail'">
        <ElDescriptions :column="4" border>
          <ElDescriptionsItem label="编号" :span="2">
            {{ detailFormData.id }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="菜单名称" :span="2">
            {{ detailFormData.name }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="菜单类型" :span="2">
            <ElTag v-if="detailFormData.type === MenuTypeEnum.CATALOG" type="warning">目录</ElTag>
            <ElTag v-if="detailFormData.type === MenuTypeEnum.MENU" type="success">菜单</ElTag>
            <ElTag v-if="detailFormData.type === MenuTypeEnum.BUTTON" type="danger">按钮</ElTag>
            <ElTag v-if="detailFormData.type === MenuTypeEnum.EXTLINK" type="info">外链</ElTag>
          </ElDescriptionsItem>
          <ElDescriptionsItem label="终端" :span="2">
            <ElTag v-if="detailFormData.client === MenuClientEnum.PC" type="primary">PC</ElTag>
            <ElTag v-else-if="detailFormData.client === MenuClientEnum.APP" type="success">
              APP
            </ElTag>
            <ElTag v-else type="info">{{ detailFormData.client || "—" }}</ElTag>
          </ElDescriptionsItem>
          <ElDescriptionsItem label="图标" :span="2">
            <template #default>
              <template v-if="detailFormData.icon">
                <MenuRouteIcon :icon="detailFormData.icon" style="vertical-align: -0.15em" />
              </template>
            </template>
          </ElDescriptionsItem>
          <ElDescriptionsItem label="排序" :span="2">
            {{ detailFormData.order }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="权限标识" :span="2">
            {{ detailFormData.permission }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="路由名称" :span="2">
            {{ detailFormData.route_name }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="路由路径" :span="2">
            {{ detailFormData.route_path }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="组件路径" :span="2">
            {{ detailFormData.component_path }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="重定向" :span="2">
            {{ detailFormData.redirect }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="父级编号" :span="2">
            {{ detailFormData.parent_id }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="父级菜单" :span="2">
            {{ detailFormData.parent_name }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="是否缓存" :span="2">
            <ElTag :type="detailFormData.keep_alive ? 'success' : 'danger'">
              {{ detailFormData.keep_alive ? "是" : "否" }}
            </ElTag>
          </ElDescriptionsItem>
          <ElDescriptionsItem label="是否显示" :span="2">
            <ElTag :type="detailFormData.hidden ? 'success' : 'danger'">
              {{ detailFormData.hidden ? "是" : "否" }}
            </ElTag>
          </ElDescriptionsItem>
          <ElDescriptionsItem label="是否显示根路由" :span="2">
            <ElTag :type="detailFormData.always_show ? 'success' : 'danger'">
              {{ detailFormData.always_show ? "是" : "否" }}
            </ElTag>
          </ElDescriptionsItem>
          <ElDescriptionsItem label="菜单标题" :span="2">
            {{ detailFormData.title }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="路由参数" :span="2">
            {{ detailFormData.params }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="是否固定路由" :span="2">
            <ElTag :type="detailFormData.affix ? 'success' : 'danger'">
              {{ detailFormData.affix ? "是" : "否" }}
            </ElTag>
          </ElDescriptionsItem>
          <ElDescriptionsItem label="状态" :span="2">
            <ElTag :type="detailFormData.status === '0' ? 'success' : 'danger'">
              {{ detailFormData.status === "0" ? "启用" : "停用" }}
            </ElTag>
          </ElDescriptionsItem>
          <ElDescriptionsItem label="排序" :span="2">
            {{ detailFormData.order }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="创建时间" :span="2">
            {{ detailFormData.created_time }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="更新时间" :span="2">
            {{ detailFormData.updated_time }}
          </ElDescriptionsItem>
          <ElDescriptionsItem label="描述" :span="4">
            {{ detailFormData.description }}
          </ElDescriptionsItem>
        </ElDescriptions>
      </template>

      <!-- 新增、编辑表单 -->
      <template v-else>
        <ElForm
          ref="dataFormRef"
          :model="formData"
          :rules="rules"
          label-suffix=":"
          label-width="auto"
          label-position="right"
        >
          <ElFormItem
            v-if="formData.type !== MenuTypeEnum.CATALOG"
            label="父级菜单"
            prop="parent_id"
          >
            <ElTreeSelect
              v-model="formData.parent_id"
              placeholder="选择上级菜单"
              :data="menuOptions"
              filterable
              check-strictly
              :render-after-expand="false"
              :disabled="createParentLocked"
            />
            <ElText v-if="createParentLocked" type="info" size="small" class="block mt-1">
              在菜单下仅可新增按钮，父级已固定
            </ElText>
          </ElFormItem>

          <ElFormItem label="菜单名称" prop="name">
            <ElInput v-model="formData.name" placeholder="请输入菜单名称" />
          </ElFormItem>

          <ElFormItem label="菜单标题" prop="title">
            <ElInput v-model="formData.title" placeholder="请输入菜单标题" />
          </ElFormItem>

          <ElFormItem label="菜单类型" prop="type">
            <ElRadioGroup v-model="formData.type" @change="handleMenuTypeChange">
              <ElRadio
                v-if="allowedMenuTypeValues.includes(MenuTypeEnum.CATALOG)"
                :value="MenuTypeEnum.CATALOG"
              >
                目录
              </ElRadio>
              <ElRadio
                v-if="allowedMenuTypeValues.includes(MenuTypeEnum.MENU)"
                :value="MenuTypeEnum.MENU"
              >
                菜单
              </ElRadio>
              <ElRadio
                v-if="allowedMenuTypeValues.includes(MenuTypeEnum.BUTTON)"
                :value="MenuTypeEnum.BUTTON"
              >
                按钮
              </ElRadio>
              <ElRadio
                v-if="allowedMenuTypeValues.includes(MenuTypeEnum.EXTLINK)"
                :value="MenuTypeEnum.EXTLINK"
              >
                外链
              </ElRadio>
            </ElRadioGroup>
          </ElFormItem>

          <ElFormItem label="终端" prop="client">
            <ElRadioGroup v-model="formData.client" :disabled="createParentLocked">
              <ElRadio :value="MenuClientEnum.PC">PC 桌面</ElRadio>
              <ElRadio :value="MenuClientEnum.APP">APP 移动</ElRadio>
            </ElRadioGroup>
            <ElText v-if="createParentLocked" type="info" size="small" class="block mt-1">
              子级终端与父菜单一致
            </ElText>
          </ElFormItem>

          <ElFormItem v-if="formData.type == MenuTypeEnum.EXTLINK" label="外链地址" prop="path">
            <ElInput v-model="formData.route_path" placeholder="请输入外链完整路径" />
          </ElFormItem>

          <ElFormItem v-if="formData.type !== MenuTypeEnum.BUTTON" prop="route_name">
            <template #label>
              <div class="flex-y-center">
                路由名称
                <ElTooltip placement="bottom" effect="light">
                  <template #content>
                    如果需要开启缓存，需保证页面 defineOptions 中的 name 与此处一致，建议使用驼峰。
                  </template>
                  <ElIcon class="ml-1 cursor-pointer">
                    <QuestionFilled />
                  </ElIcon>
                </ElTooltip>
              </div>
            </template>
            <ElInput v-model="formData.route_name" placeholder="请输入路由名称" />
          </ElFormItem>

          <ElFormItem
            v-if="formData.type == MenuTypeEnum.CATALOG || formData.type == MenuTypeEnum.MENU"
            prop="route_path"
          >
            <template #label>
              <div class="flex-y-center">
                路由路径
                <ElTooltip placement="bottom" effect="light">
                  <template #content>
                    定义应用中不同页面对应的 URL 路径，目录需以 /
                    开头，菜单项不用。例如：系统管理目录 /system，系统管理下的用户管理菜单 user。
                  </template>
                  <ElIcon class="ml-1 cursor-pointer">
                    <QuestionFilled />
                  </ElIcon>
                </ElTooltip>
              </div>
            </template>
            <ElInput v-model="formData.route_path" placeholder="请输入路由路径,如：/system" />
          </ElFormItem>

          <ElFormItem v-if="formData.type == MenuTypeEnum.MENU" prop="component">
            <template #label>
              <div class="flex-y-center">
                组件路径
                <ElTooltip placement="bottom" effect="light">
                  <template #content>
                    组件页面完整路径，相对于 src/views/，如 system/user/index，缺省后缀 .vue
                  </template>
                  <ElIcon class="ml-1 cursor-pointer">
                    <QuestionFilled />
                  </ElIcon>
                </ElTooltip>
              </div>
            </template>

            <ElInput
              v-model="formData.component_path"
              placeholder="请输入组件路径，如system/user/index"
              style="width: 95%"
            >
              <template v-if="formData.type == MenuTypeEnum.MENU" #prepend>src/views/</template>
              <template v-if="formData.type == MenuTypeEnum.MENU" #append>.vue</template>
            </ElInput>
          </ElFormItem>

          <ElFormItem v-if="formData.type == MenuTypeEnum.MENU">
            <template #label>
              <div class="flex-y-center">
                路由参数
                <ElTooltip placement="bottom" effect="light">
                  <template #content>
                    组件页面使用 `useRoute().query.参数名` 获取路由参数值。
                  </template>
                  <ElIcon class="ml-1 cursor-pointer">
                    <QuestionFilled />
                  </ElIcon>
                </ElTooltip>
              </div>
            </template>

            <div
              v-if="
                !formData.params || (Array.isArray(formData.params) && formData.params.length === 0)
              "
            >
              <ElButton type="success" plain @click="formData.params = [{ key: '', value: '' }]">
                添加路由参数
              </ElButton>
            </div>

            <div v-else>
              <div v-for="(item, index) in formData.params" :key="index">
                <ElInput v-model="item.key" placeholder="参数名" style="width: 100px" />

                <span class="mx-1">=</span>

                <ElInput v-model="item.value" placeholder="参数值" style="width: 100px" />

                <ElIcon
                  v-if="formData.params.indexOf(item) === formData.params.length - 1"
                  class="ml-2 cursor-pointer color-[var(--el-color-success)]"
                  style="vertical-align: -0.15em"
                  @click="formData.params.push({ key: '', value: '' })"
                >
                  <CirclePlusFilled />
                </ElIcon>
                <ElIcon
                  class="ml-2 cursor-pointer color-[var(--el-color-danger)]"
                  style="vertical-align: -0.15em"
                  @click="formData.params.splice(formData.params.indexOf(item), 1)"
                >
                  <DeleteFilled />
                </ElIcon>
              </div>
            </div>
          </ElFormItem>

          <ElFormItem v-if="formData.type !== MenuTypeEnum.BUTTON">
            <template #label>
              <div class="flex-y-center">
                是否隐藏
                <ElTooltip placement="bottom" effect="light">
                  <template #content>
                    选择"是", 菜单中隐藏
                    <br />
                    选择"否"，菜单中显示。
                    <br />
                  </template>
                  <ElIcon class="ml-1 cursor-pointer">
                    <QuestionFilled />
                  </ElIcon>
                </ElTooltip>
              </div>
            </template>

            <ElRadioGroup v-model="formData.hidden">
              <ElRadio :value="true">是</ElRadio>
              <ElRadio :value="false">否</ElRadio>
            </ElRadioGroup>
          </ElFormItem>

          <ElFormItem
            v-if="formData.type === MenuTypeEnum.CATALOG || formData.type === MenuTypeEnum.MENU"
          >
            <template #label>
              <div class="flex-y-center">
                始终显示
                <ElTooltip placement="bottom" effect="light">
                  <template #content>
                    选择"是"，即使目录或菜单下只有一个子节点，也会显示父节点。
                    <br />
                    选择"否"，如果目录或菜单下只有一个子节点，则只显示该子节点，隐藏父节点。
                    <br />
                    如果是叶子节点，请选择"否"。
                  </template>
                  <ElIcon class="ml-1 cursor-pointer">
                    <QuestionFilled />
                  </ElIcon>
                </ElTooltip>
              </div>
            </template>

            <ElRadioGroup v-model="formData.always_show">
              <ElRadio :value="true">是</ElRadio>
              <ElRadio :value="false">否</ElRadio>
            </ElRadioGroup>
          </ElFormItem>

          <ElFormItem v-if="formData.type === MenuTypeEnum.MENU" label="缓存页面">
            <ElRadioGroup v-model="formData.keep_alive">
              <ElRadio :value="true">开启</ElRadio>
              <ElRadio :value="false">关闭</ElRadio>
            </ElRadioGroup>
          </ElFormItem>

          <ElFormItem label="排序" prop="order">
            <ElInputNumber v-model="formData.order" controls-position="right" :min="1" />
          </ElFormItem>

          <!-- 权限标识 -->
          <ElFormItem
            v-if="formData.type == MenuTypeEnum.BUTTON || formData.type === MenuTypeEnum.MENU"
            label="权限标识"
            prop="perm"
          >
            <ElInput v-model="formData.permission" placeholder="请输入权限标识，如sys:user:add" />
          </ElFormItem>

          <ElFormItem v-if="formData.type !== MenuTypeEnum.BUTTON" label="图标" prop="icon">
            <!-- 图标选择器 -->
            <icon-select v-model="formData.icon" />
          </ElFormItem>

          <ElFormItem
            v-if="formData.type == MenuTypeEnum.CATALOG || formData.type === MenuTypeEnum.MENU"
            label="重定向"
            prop="redirect"
            :required="formData.type === MenuTypeEnum.CATALOG"
          >
            <ElInput
              v-model="formData.redirect"
              :placeholder="
                formData.type === MenuTypeEnum.CATALOG
                  ? '目录必填，一般为默认子路由 path，如 /system/user'
                  : '可选，请输入重定向路由'
              "
            />
          </ElFormItem>

          <ElFormItem v-if="formData.type != MenuTypeEnum.BUTTON" label="常驻标签栏" prop="affix">
            <ElRadioGroup v-model="formData.affix">
              <ElRadio :value="true">是</ElRadio>
              <ElRadio :value="false">否</ElRadio>
            </ElRadioGroup>
          </ElFormItem>

          <ElFormItem label="状态" prop="status">
            <ElRadioGroup v-model="formData.status">
              <ElRadio value="0">启用</ElRadio>
              <ElRadio value="1">禁用</ElRadio>
            </ElRadioGroup>
          </ElFormItem>

          <ElFormItem label="描述" prop="description">
            <ElInput
              v-model="formData.description"
              :rows="4"
              :maxlength="100"
              show-word-limit
              type="textarea"
              placeholder="请输入描述"
            />
          </ElFormItem>
        </ElForm>
      </template>

      <template #footer>
        <div class="dialog-footer">
          <!-- 详情弹窗不需要确定按钮的提交逻辑 -->
          <ElButton
            v-if="dialogVisible.type !== 'detail'"
            type="primary"
            :loading="submitLoading"
            @click="handleSubmit"
          >
            确定
          </ElButton>
          <ElButton v-else type="primary" @click="handleCloseDialog">确定</ElButton>
          <ElButton @click="handleCloseDialog">取消</ElButton>
        </div>
      </template>
    </ArtDrawer>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "SysMenu",
  inheritAttrs: false,
});

import { h, ref, reactive, computed, nextTick, onMounted } from "vue";
import { CirclePlusFilled, DeleteFilled, QuestionFilled } from "@element-plus/icons-vue";
import { useAppStore } from "@/store/modules/app.store";
import { useUserStore } from "@/store/modules/user.store";
import { DeviceEnum } from "@/enums/settings/device.enum";
import { useTableColumns } from "@/hooks/core/useTableColumns";
import MenuAPI, {
  type MenuForm,
  type MenuPageQuery,
  type MenuTable,
} from "@/api/module_system/menu";
import { MenuClientEnum, MenuTypeEnum } from "@/enums/system/menu.enum";
import { formatTree } from "@/utils/common";
import MenuRouteIcon from "@/components/MenuRouteIcon/index.vue";
import ArtTable from "@/components/Core/tables/art-table/index.vue";
import ArtTableHeader from "@/components/Core/tables/art-table-header/index.vue";
import ArtTableHeaderLeft from "@/components/Core/tables/art-table-header-left/index.vue";
import ArtButtonTable from "@/components/Core/forms/art-button-table/index.vue";
import ArtSearchBar from "@/components/Core/forms/art-search-bar/index.vue";
import type { SearchFormItem } from "@/components/Core/forms/art-search-bar/index.vue";
import ArtDrawer from "@/components/Core/modal/art-drawer/index.vue";
import {
  ElMessage,
  ElMessageBox,
  ElTag,
  ElTooltip,
  ElDropdown,
  ElDropdownMenu,
  ElDropdownItem,
} from "element-plus";
import { useAuth } from "@/hooks/core/useAuth";

const MAX_INLINE_ROW_ACTIONS = 3;
const { hasAuth } = useAuth();
const appStore = useAppStore();
const userStore = useUserStore();

type MenuSearchForm = {
  name?: string;
  status?: string;
  created_time?: string[];
};

function buildMenuListQuery(p: MenuSearchForm): MenuPageQuery {
  return {
    name: p.name,
    status: p.status,
    created_time:
      Array.isArray(p.created_time) && p.created_time.length === 2 ? p.created_time : undefined,
  };
}

function menuTypeTag(row: MenuTable) {
  const t = row.type;
  if (t === MenuTypeEnum.CATALOG) return h(ElTag, { type: "warning" }, () => "目录");
  if (t === MenuTypeEnum.MENU) return h(ElTag, { type: "success" }, () => "菜单");
  if (t === MenuTypeEnum.BUTTON) return h(ElTag, { type: "danger" }, () => "按钮");
  if (t === MenuTypeEnum.EXTLINK) return h(ElTag, { type: "info" }, () => "外链");
  return h("span", "—");
}

function menuClientTag(row: MenuTable) {
  if (row.client === MenuClientEnum.PC) return h(ElTag, { type: "primary" }, () => "PC");
  if (row.client === MenuClientEnum.APP) return h(ElTag, { type: "success" }, () => "APP");
  return h(ElTag, { type: "info" }, () => String(row.client ?? "—"));
}

function ynTag(v: boolean | undefined, yes = "是", no = "否") {
  return h(ElTag, { type: v ? "success" : "danger" }, () => (v ? yes : no));
}

type RowAction = {
  key: string;
  label: string;
  artType: "add" | "edit" | "delete" | "view" | "more";
  icon?: string;
  perm: string;
  disabled?: boolean;
  run: () => void;
};

function buildMenuRowActions(
  row: MenuTable,
  ctx: {
    onAdd?: (r: MenuTable) => void;
    onDetail: (id: number) => void;
    onEdit: (id: number) => void;
    onDelete: (id: number) => void;
  }
): RowAction[] {
  const actions: RowAction[] = [];
  if (ctx.onAdd && (row.type === MenuTypeEnum.CATALOG || row.type === MenuTypeEnum.MENU)) {
    actions.push({
      key: "add",
      label: "新增",
      artType: "add",
      perm: "module_system:menu:create",
      run: () => ctx.onAdd!(row),
    });
  }
  actions.push(
    {
      key: "detail",
      label: "详情",
      artType: "view",
      perm: "module_system:menu:detail",
      run: () => ctx.onDetail(row.id!),
    },
    {
      key: "edit",
      label: "编辑",
      artType: "edit",
      perm: "module_system:menu:update",
      run: () => ctx.onEdit(row.id!),
    },
    {
      key: "delete",
      label: "删除",
      artType: "delete",
      perm: "module_system:menu:delete",
      run: () => ctx.onDelete(row.id!),
    }
  );
  return actions.filter((a) => hasAuth(a.perm));
}

function formatMenuOperationCell(row: MenuTable, ctx: Parameters<typeof buildMenuRowActions>[1]) {
  const actions = buildMenuRowActions(row, ctx);
  if (actions.length === 0) {
    return h("span", { class: "text-g-400" }, "—");
  }
  const inline = actions.slice(0, MAX_INLINE_ROW_ACTIONS);
  const overflow = actions.slice(MAX_INLINE_ROW_ACTIONS);

  const inlineNodes = inline.map((a) =>
    h(ElTooltip, { content: a.label, placement: "top" }, () =>
      h("span", { class: "inline-flex" }, [
        h(ArtButtonTable, {
          type: a.artType,
          icon: a.icon,
          onClick: a.run,
        }),
      ])
    )
  );

  if (overflow.length === 0) {
    return h(
      "div",
      { class: "inline-flex flex-wrap items-center justify-end gap-1 menu-table-actions" },
      inlineNodes
    );
  }

  const dropdown = h(
    ElDropdown,
    { trigger: "click" },
    {
      default: () =>
        h(ElTooltip, { content: "更多", placement: "top" }, () =>
          h("span", { class: "inline-flex align-middle" }, [
            h(ArtButtonTable, {
              type: "more",
              onClick: () => {},
            }),
          ])
        ),
      dropdown: () =>
        h(
          ElDropdownMenu,
          null,
          overflow.map((a) =>
            h(
              ElDropdownItem,
              {
                key: a.key,
                disabled: a.disabled,
                onClick: () => a.run(),
              },
              () => a.label
            )
          )
        ),
    }
  );

  return h(
    "div",
    { class: "inline-flex flex-wrap items-center justify-end gap-1 menu-table-actions" },
    [...inlineNodes, dropdown]
  );
}

const menuClientTab = ref<"pc" | "app">("pc");
const searchForm = ref<MenuSearchForm>({
  name: undefined,
  status: undefined,
  created_time: undefined,
});
const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof ArtSearchBar> | null>(null);
const searchBarRules: Record<string, unknown> = {};

const statusOptions = ref([
  { label: "启用", value: "0" },
  { label: "停用", value: "1" },
]);

const menuSearchItems = computed<SearchFormItem[]>(() => [
  {
    label: "菜单名称",
    key: "name",
    type: "input",
    placeholder: "请输入菜单名称",
    clearable: true,
    span: 6,
  },
  {
    label: "状态",
    key: "status",
    type: "select",
    props: {
      placeholder: "请选择状态",
      options: statusOptions.value,
      clearable: true,
    },
    span: 6,
  },
  {
    label: "创建时间",
    key: "created_time",
    type: "datetimerange",
    span: 6,
    props: {
      type: "datetimerange",
      rangeSeparator: "至",
      startPlaceholder: "开始日期",
      endPlaceholder: "结束日期",
      format: "YYYY-MM-DD HH:mm:ss",
      valueFormat: "YYYY-MM-DD HH:mm:ss",
      style: { width: "340px" },
    },
  },
]);

const tableRef = ref<{
  elTableRef?: { toggleRowExpansion: (row: MenuTable, expanded?: boolean) => void };
} | null>(null);
const tableData = ref<MenuTable[]>([]);
const loading = ref(false);
const isExpanded = ref(false);
const selectedRows = ref<MenuTable[]>([]);
const selectedIds = computed(() =>
  selectedRows.value.map((r) => r.id).filter((id): id is number => id != null && !Number.isNaN(id))
);
const batchDeleting = ref(false);
const submitLoading = ref(false);

const menuOptions = ref<OptionType[]>([]);
const fullMenuTree = ref<MenuTable[]>([]);
const createParentLocked = ref(false);

const detailFormData = ref<MenuTable>({});

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
  status: "0",
  description: undefined,
  client: MenuClientEnum.PC,
});

const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail",
});

const drawerSize = computed(() => (appStore.device === DeviceEnum.DESKTOP ? "600px" : "90%"));

function typesAllowedUnderParent(parentType: MenuTypeEnum): MenuTypeEnum[] {
  switch (parentType) {
    case MenuTypeEnum.CATALOG:
      return [MenuTypeEnum.CATALOG, MenuTypeEnum.MENU, MenuTypeEnum.EXTLINK];
    case MenuTypeEnum.MENU:
      return [MenuTypeEnum.BUTTON];
    case MenuTypeEnum.BUTTON:
    case MenuTypeEnum.EXTLINK:
      return [];
    default:
      return [MenuTypeEnum.CATALOG, MenuTypeEnum.MENU, MenuTypeEnum.EXTLINK];
  }
}

function findMenuNodeById(
  id: number | undefined,
  nodes: MenuTable[] = fullMenuTree.value
): MenuTable | null {
  if (id == null) return null;
  for (const n of nodes) {
    if (n.id === id) return n;
    if (n.children?.length) {
      const f = findMenuNodeById(id, n.children);
      if (f) return f;
    }
  }
  return null;
}

function filterMenuTypes(nodes: MenuTable[]): MenuTable[] {
  return nodes
    .filter((node) => node.type === MenuTypeEnum.CATALOG || node.type === MenuTypeEnum.MENU)
    .map((node: MenuTable & { children?: MenuTable[] }) => ({
      ...node,
      children: node.children ? filterMenuTypes(node.children) : [],
    }));
}

async function loadMenuData() {
  loading.value = true;
  try {
    const res = await MenuAPI.listMenu({
      ...buildMenuListQuery(searchForm.value),
      menu_client: menuClientTab.value,
    });
    const tree = res.data.data || [];
    fullMenuTree.value = tree;
    tableData.value = tree;
    menuOptions.value = formatTree(filterMenuTypes(tree));
  } catch (e: unknown) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}

function handleMenuClientTabChange(name: string | number) {
  menuClientTab.value = name === "app" ? "app" : "pc";
  void loadMenuData();
}

async function handleSearchBarSearch(params: MenuSearchForm) {
  await searchBarRef.value?.validate?.();
  searchForm.value = { ...params };
  await loadMenuData();
}

function onResetSearch() {
  searchForm.value = {
    name: undefined,
    status: undefined,
    created_time: undefined,
  };
  void loadMenuData();
}

function onTableSelectionChange(rows: MenuTable[]) {
  selectedRows.value = rows;
}

function toggleExpand() {
  isExpanded.value = !isExpanded.value;
  nextTick(() => {
    const el = tableRef.value?.elTableRef;
    if (!el || !tableData.value.length) return;
    const walk = (rows: MenuTable[]) => {
      rows.forEach((row) => {
        if (row.children?.length) {
          el.toggleRowExpansion(row, isExpanded.value);
          walk(row.children);
        }
      });
    };
    walk(tableData.value);
  });
}

function deleteMenuRow(id: number) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      await MenuAPI.deleteMenu([id]);
      await userStore.getUserInfo();
      ElMessage.success("删除成功");
      selectedRows.value = [];
      await loadMenuData();
    })
    .catch(() => {});
}

const opCtx = {
  onAdd: (r: MenuTable) => void handleOpenDialog("create", undefined, r),
  onDetail: (id: number) => void handleOpenDialog("detail", id),
  onEdit: (id: number) => void handleOpenDialog("update", id),
  onDelete: deleteMenuRow,
};

const { columnChecks, columns } = useTableColumns<MenuTable>(() => [
  { type: "selection", width: 48, fixed: "left" },
  { type: "index", label: "序号", width: 60, fixed: "left" },
  { prop: "name", label: "菜单名称", minWidth: 200, showOverflowTooltip: true },
  {
    prop: "icon",
    label: "图标",
    width: 72,
    align: "center",
    formatter: (row: MenuTable) =>
      row.icon
        ? h(MenuRouteIcon, { icon: row.icon, style: { verticalAlign: "-0.15em" } })
        : h("span", { class: "text-g-400" }, "—"),
  },
  {
    prop: "status",
    label: "状态",
    width: 88,
    formatter: (row: MenuTable) =>
      h(ElTag, { type: row.status === "0" ? "success" : "danger" }, () =>
        row.status === "0" ? "启用" : "停用"
      ),
  },
  { prop: "type", label: "类型", width: 88, align: "center", formatter: menuTypeTag },
  { prop: "client", label: "终端", width: 88, align: "center", formatter: menuClientTag },
  { prop: "order", label: "排序", width: 80 },
  { prop: "route_name", label: "路由名称", minWidth: 100, showOverflowTooltip: true },
  { prop: "route_path", label: "路由路径", minWidth: 140, showOverflowTooltip: true },
  { prop: "permission", label: "权限标识", minWidth: 160, showOverflowTooltip: true },
  { prop: "component_path", label: "组件路径", minWidth: 140, showOverflowTooltip: true },
  { prop: "redirect", label: "重定向", minWidth: 100, showOverflowTooltip: true },
  {
    prop: "keep_alive",
    label: "是否缓存",
    width: 96,
    formatter: (row: MenuTable) => ynTag(row.keep_alive),
  },
  {
    prop: "hidden",
    label: "是否隐藏",
    width: 96,
    formatter: (row: MenuTable) => ynTag(row.hidden),
  },
  {
    prop: "always_show",
    label: "显示根路由",
    width: 108,
    formatter: (row: MenuTable) => ynTag(row.always_show),
  },
  {
    prop: "affix",
    label: "固定路由",
    width: 96,
    formatter: (row: MenuTable) => ynTag(row.affix),
  },
  { prop: "title", label: "菜单标题", minWidth: 100, showOverflowTooltip: true },
  {
    prop: "params",
    label: "路由参数",
    minWidth: 100,
    formatter: (row: MenuTable) =>
      row.params == null
        ? "—"
        : typeof row.params === "object"
          ? JSON.stringify(row.params)
          : String(row.params),
  },
  { prop: "description", label: "描述", minWidth: 140, showOverflowTooltip: true },
  { prop: "created_time", label: "创建时间", width: 168, showOverflowTooltip: true },
  { prop: "updated_time", label: "更新时间", width: 168, showOverflowTooltip: true },
  {
    prop: "operation",
    label: "操作",
    width: 260,
    fixed: "right",
    align: "right",
    formatter: (row: MenuTable) => formatMenuOperationCell(row, opCtx),
  },
]);

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
      validator: (rule: unknown, value: string, callback: (e?: Error) => void) => {
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
  client: [{ required: true, message: "请选择终端", trigger: "change" }],
  redirect: [
    {
      validator: (_rule: unknown, value: string | undefined, callback: (e?: Error) => void) => {
        if (formData.type === MenuTypeEnum.CATALOG) {
          if (value === undefined || value === null || String(value).trim() === "") {
            callback(new Error("目录类型必须填写重定向地址"));
            return;
          }
        }
        callback();
      },
      trigger: "blur",
    },
  ],
});

const selectedMenuId = ref<number | undefined>();

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
  status: "0",
  description: undefined,
  client: MenuClientEnum.PC,
};

const dataFormRef = ref();

async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  Object.assign(formData, initialFormData);
}

async function handleRowClick(row: MenuTable) {
  selectedMenuId.value = row.id;
}

const allowedMenuTypeValues = computed(() => {
  const pid = formData.parent_id;
  const parentNode = findMenuNodeById(pid);
  if (!parentNode?.type) {
    return [MenuTypeEnum.CATALOG, MenuTypeEnum.MENU, MenuTypeEnum.EXTLINK];
  }
  return typesAllowedUnderParent(parentNode.type as MenuTypeEnum);
});

async function handleCloseDialog() {
  dialogVisible.visible = false;
  createParentLocked.value = false;
  await resetForm();
}

async function handleOpenDialog(
  type: "create" | "update" | "detail",
  id?: number,
  parentRow?: MenuTable
) {
  dialogVisible.type = type;
  createParentLocked.value = false;
  if (id) {
    const response = await MenuAPI.detailMenu(id);
    if (type === "detail") {
      dialogVisible.title = "菜单详情";
      Object.assign(detailFormData.value, response.data.data ?? {});
    } else if (type === "update") {
      dialogVisible.title = "修改菜单";
      Object.assign(formData, response.data.data);
    }
  } else {
    dialogVisible.title = "新增菜单";
    Object.assign(formData, initialFormData);
    if (parentRow?.id != null) {
      formData.parent_id = parentRow.id;
      formData.client = (parentRow.client as MenuClientEnum) || menuClientTab.value;
      if (parentRow.type === MenuTypeEnum.MENU) {
        createParentLocked.value = true;
        formData.type = MenuTypeEnum.BUTTON;
      } else if (parentRow.type === MenuTypeEnum.CATALOG) {
        formData.type = MenuTypeEnum.MENU;
      }
    } else {
      formData.client = menuClientTab.value;
    }
  }
  dialogVisible.visible = true;
}

function handleMenuTypeChange() {
  if (formData.type === MenuTypeEnum.MENU) {
    formData.component_path = "";
  }
  nextTick(() => {
    dataFormRef.value?.clearValidate("redirect");
    if (formData.type === MenuTypeEnum.CATALOG) {
      dataFormRef.value?.validateField("redirect").catch(() => {});
    }
  });
}

async function handleSubmit() {
  const allowed = allowedMenuTypeValues.value;
  if (!allowed.length) return;
  const t = formData.type as MenuTypeEnum;
  if (!allowed.includes(t)) {
    formData.type = allowed[0] as MenuForm["type"];
  }
  dataFormRef.value?.validate(async (valid: boolean) => {
    if (!valid) return;
    submitLoading.value = true;
    const id = formData.id;
    try {
      if (id) {
        await MenuAPI.updateMenu(id, { id, ...formData });
      } else {
        await MenuAPI.createMenu(formData);
      }
      dialogVisible.visible = false;
      await resetForm();
      await loadMenuData();
      await userStore.getUserInfo();
    } catch (error: unknown) {
      console.error(error);
    } finally {
      submitLoading.value = false;
    }
  });
}

function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  ElMessageBox.confirm(`确定删除选中的 ${ids.length} 条数据吗？`, "批量删除", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        batchDeleting.value = true;
        await MenuAPI.deleteMenu(ids);
        await userStore.getUserInfo();
        ElMessage.success("删除成功");
        selectedRows.value = [];
        await loadMenuData();
      } finally {
        batchDeleting.value = false;
      }
    })
    .catch(() => {});
}

async function handleMoreClick(status: string) {
  const ids = selectedIds.value;
  if (!ids.length) {
    ElMessage.warning("请先选择要操作的数据");
    return;
  }
  ElMessageBox.confirm(`确认${status === "0" ? "启用" : "停用"}该项数据?`, "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        await MenuAPI.batchMenu({ ids, status });
        await loadMenuData();
      } catch (error: unknown) {
        console.error(error);
      }
    })
    .catch(() => {});
}

onMounted(() => {
  void loadMenuData();
});
</script>

<style scoped lang="scss">
.art-full-height {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.art-table-card {
  flex: 1;
}

:deep(.menu-table-actions .inline-flex) {
  vertical-align: middle;
}
</style>
