<!-- 菜单管理：Art + 树形表格；操作列最多 3 个外露，其余「更多」 -->
<template>
  <div class="fa-full-height">
    <FaSearchBar
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

    <ElCard
      shadow="hover"
      class="fa-table-card"
      :style="{ 'margin-top': showSearchBar ? '12px' : '0' }"
    >
      <FaTableHeader
        v-model:columns="columnChecks"
        v-model:showSearchBar="showSearchBar"
        :loading="loading"
        @refresh="loadMenuData"
      >
        <template #left>
          <div class="inline-flex flex-wrap items-center gap-2">
            <FaTableHeaderLeft
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
      </FaTableHeader>

      <FaTable
        ref="tableRef"
        row-key="id"
        :loading="loading"
        :columns="columns"
        :data="tableData"
        :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
        :default-expand-all="false"
        @selection-change="onTableSelectionChange"
        @row-click="handleRowClick"
      />
    </ElCard>

    <FaDrawer
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      :size="drawerSize"
      :form-mode="dialogVisible.type"
      :confirm-loading="submitLoading"
      @cancel="handleCloseDialog"
      @confirm="dialogVisible.type === 'detail' ? handleCloseDialog() : handleSubmit()"
    >
      <!-- 详情 -->
      <template v-if="dialogVisible.type === 'detail'">
        <FaDescriptions
          :column="4"
          :data="detailFormData"
          :items="menuDetailItems"
          :scrollbar="false"
        >
          <template #type="{ row }">
            <ElTag v-if="row?.type === MenuTypeEnum.CATALOG" type="warning">目录</ElTag>
            <ElTag v-if="row?.type === MenuTypeEnum.MENU" type="success">菜单</ElTag>
            <ElTag v-if="row?.type === MenuTypeEnum.BUTTON" type="danger">按钮</ElTag>
            <ElTag v-if="row?.type === MenuTypeEnum.EXTLINK" type="info">外链</ElTag>
          </template>
          <template #client="{ row }">
            <ElTag v-if="row?.client === MenuClientEnum.PC" type="primary">PC</ElTag>
            <ElTag v-else-if="row?.client === MenuClientEnum.APP" type="success">APP</ElTag>
            <ElTag v-else type="info">{{ row?.client || "—" }}</ElTag>
          </template>
          <template #icon="{ row }">
            <template v-if="row?.icon">
              <FaMenuRouteIcon :icon="row?.icon as string" :style="'vertical-align: -0.15em'" />
            </template>
          </template>
        </FaDescriptions>
      </template>

      <!-- 新增、编辑表单 -->
      <template v-else>
        <FaForm
          :key="menuFormRenderKey"
          ref="dataFormRef"
          v-model="formData"
          :items="menuDialogFormItems"
          :rules="rules"
          label-suffix=":"
          :label-width="'auto'"
          label-position="right"
          :span="24"
          :gutter="16"
          :show-reset="false"
          :show-submit="false"
          class="crud-dialog-art-form"
        >
          <!-- 父级菜单(条件显示) -->
          <template v-if="formData.type !== MenuTypeEnum.CATALOG" #parent_id>
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
          </template>

          <!-- 菜单类型(动态枚举按钮组) -->
          <template #type>
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
          </template>

          <!-- 终端(禁用态+提示) -->
          <template #client>
            <ElRadioGroup v-model="formData.client" :disabled="createParentLocked">
              <ElRadio :value="MenuClientEnum.PC">PC 桌面</ElRadio>
              <ElRadio :value="MenuClientEnum.APP">APP 移动</ElRadio>
            </ElRadioGroup>
            <ElText v-if="createParentLocked" type="info" size="small" class="block mt-1">
              子级终端与父菜单一致
            </ElText>
          </template>

          <!-- 外链地址(条件显示) -->
          <template v-if="formData.type == MenuTypeEnum.EXTLINK" #extlink_path>
            <ElInput v-model="formData.route_path" placeholder="请输入外链完整路径" />
          </template>

          <!-- 路由名称(Tooltip标签) -->
          <template v-if="formData.type !== MenuTypeEnum.BUTTON" #route_name>
            <ElInput v-model="formData.route_name" placeholder="请输入路由名称" />
          </template>

          <!-- 路由路径(Tooltip标签) -->
          <template
            v-if="formData.type == MenuTypeEnum.CATALOG || formData.type == MenuTypeEnum.MENU"
            #route_path
          >
            <ElInput v-model="formData.route_path" placeholder="请输入路由路径,如：/system" />
          </template>

          <!-- 组件路径(Tooltip+prepend/append) -->
          <template v-if="formData.type == MenuTypeEnum.MENU" #component_path>
            <ElInput
              v-model="formData.component_path"
              placeholder="请输入组件路径，如system/user/index"
              :style="'width: 95%'"
            >
              <template #prepend>src/views/</template>
              <template #append>.vue</template>
            </ElInput>
          </template>

          <!-- 路由参数(动态键值编辑器) -->
          <template v-if="formData.type == MenuTypeEnum.MENU" #params>
            <template
              v-if="
                !formData.params || (Array.isArray(formData.params) && formData.params.length === 0)
              "
            >
              <ElButton type="success" plain @click="formData.params = [{ key: '', value: '' }]">
                添加路由参数
              </ElButton>
            </template>
            <template v-else>
              <div v-for="(item, index) in formData.params" :key="index">
                <ElInput v-model="item.key" placeholder="参数名" :style="'width: 100px'" />
                <span class="mx-1">=</span>
                <ElInput v-model="item.value" placeholder="参数值" :style="'width: 100px'" />
                <ElIcon
                  v-if="formData.params.indexOf(item) === formData.params.length - 1"
                  class="ml-2 cursor-pointer color-[var(--el-color-success)]"
                  :style="'vertical-align: -0.15em'"
                  @click="formData.params.push({ key: '', value: '' })"
                >
                  <CirclePlusFilled />
                </ElIcon>
                <ElIcon
                  class="ml-2 cursor-pointer color-[var(--el-color-danger)]"
                  :style="'vertical-align: -0.15em'"
                  @click="formData.params.splice(formData.params.indexOf(item), 1)"
                >
                  <DeleteFilled />
                </ElIcon>
              </div>
            </template>
          </template>
          <!-- 是否隐藏(Tooltip标签) -->
          <template v-if="formData.type !== MenuTypeEnum.BUTTON" #hidden>
            <ElRadioGroup v-model="formData.hidden">
              <ElRadio :value="true">是</ElRadio>
              <ElRadio :value="false">否</ElRadio>
            </ElRadioGroup>
          </template>

          <!-- 始终显示(Tooltip标签) -->
          <template
            v-if="formData.type === MenuTypeEnum.CATALOG || formData.type === MenuTypeEnum.MENU"
            #always_show
          >
            <ElRadioGroup v-model="formData.always_show">
              <ElRadio :value="true">是</ElRadio>
              <ElRadio :value="false">否</ElRadio>
            </ElRadioGroup>
          </template>

          <!-- 缓存页面(v-if) -->
          <template v-if="formData.type === MenuTypeEnum.MENU" #keep_alive>
            <ElRadioGroup v-model="formData.keep_alive">
              <ElRadio :value="true">开启</ElRadio>
              <ElRadio :value="false">关闭</ElRadio>
            </ElRadioGroup>
          </template>

          <!-- 权限标识(v-if) -->
          <template
            v-if="formData.type == MenuTypeEnum.BUTTON || formData.type === MenuTypeEnum.MENU"
            #permission
          >
            <ElInput v-model="formData.permission" placeholder="请输入权限标识，如sys:user:add" />
          </template>

          <!-- 图标(v-if) -->
          <template v-if="formData.type !== MenuTypeEnum.BUTTON" #icon>
            <FaIconSelect v-model="formData.icon" />
          </template>

          <!-- 重定向(v-if, 动态placeholder) -->
          <template
            v-if="formData.type == MenuTypeEnum.CATALOG || formData.type === MenuTypeEnum.MENU"
            #redirect
          >
            <ElInput
              v-model="formData.redirect"
              :placeholder="
                formData.type === MenuTypeEnum.CATALOG
                  ? '目录必填，一般为默认子路由 path，如 /system/user'
                  : '可选，请输入重定向路由'
              "
            />
          </template>

          <!-- 常驻标签栏(v-if) -->
          <template v-if="formData.type != MenuTypeEnum.BUTTON" #affix>
            <ElRadioGroup v-model="formData.affix">
              <ElRadio :value="true">是</ElRadio>
              <ElRadio :value="false">否</ElRadio>
            </ElRadioGroup>
          </template>
        </FaForm>
      </template>
    </FaDrawer>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "SysMenu",
  inheritAttrs: false,
});

import { CirclePlusFilled, DeleteFilled } from "@element-plus/icons-vue";
import { useAppStore, useUserStore } from "@stores";
import { DeviceEnum } from "@/enums/settings/device.enum";
import { useTableColumns } from "@/hooks/core/useTableColumns";
import MenuAPI, {
  type MenuForm,
  type MenuPageQuery,
  type MenuTable,
} from "@/api/module_system/menu";
import { MenuClientEnum, MenuTypeEnum } from "@/enums/system/menu.enum";
import { formatTree } from "@utils/common";
import { useAuth } from "@/hooks/core/useAuth";
import { renderTableOperationCell, type TableOperationAction } from "@utils";
import type { SearchFormItem } from "@/components/forms/fa-search-bar/index.vue";
import type { FormItem } from "@/components/forms/fa-form/index.vue";
import FaSearchBar from "@/components/forms/fa-search-bar/index.vue";
import FaForm from "@/components/forms/fa-form/index.vue";
import FaMenuRouteIcon from "@/components/others/fa-menu-routeIcon/index.vue";
import { ElTag, ElMessage, ElMessageBox } from "element-plus";

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

function buildMenuRowActions(
  row: MenuTable,
  ctx: {
    onAdd?: (r: MenuTable) => void;
    onDetail: (id: number) => void;
    onEdit: (id: number) => void;
    onDelete: (id: number) => void;
  }
): TableOperationAction[] {
  const actions: TableOperationAction[] = [];
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
  return actions.filter((a) => a.perm != null && hasAuth(a.perm));
}

function formatMenuOperationCell(row: MenuTable, ctx: Parameters<typeof buildMenuRowActions>[1]) {
  const actions = buildMenuRowActions(row, ctx);
  return renderTableOperationCell(actions, {
    wrapperClass: "inline-flex flex-wrap items-center justify-end gap-1 menu-table-actions",
  });
}

const menuClientTab = ref<"pc" | "app">("pc");
const searchForm = ref<MenuSearchForm>({
  name: undefined,
  status: undefined,
  created_time: undefined,
});
const showSearchBar = ref(true);
const searchBarRef = ref<InstanceType<typeof FaSearchBar> | null>(null);
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
      style: { width: "100%" },
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

const menuDetailItems: import("@/components/others/fa-descriptions/index.vue").DescriptionsItem[] =
  [
    { label: "编号", prop: "id" },
    { label: "菜单名称", prop: "name" },
    { label: "菜单类型", prop: "type", slot: "type" },
    { label: "终端", prop: "client", slot: "client" },
    { label: "图标", prop: "icon", slot: "icon" },
    { label: "权限标识", prop: "permission" },
    { label: "路由名称", prop: "route_name" },
    { label: "路由路径", prop: "route_path" },
    { label: "组件路径", prop: "component_path" },
    { label: "重定向", prop: "redirect" },
    { label: "父级编号", prop: "parent_id" },
    { label: "父级菜单", prop: "parent_name" },
    {
      label: "是否缓存",
      prop: "keep_alive",
      tag: {
        map: { true: { type: "success", text: "是" }, false: { type: "danger", text: "否" } },
      },
    },
    {
      label: "是否显示",
      prop: "hidden",
      tag: {
        map: { true: { type: "success", text: "是" }, false: { type: "danger", text: "否" } },
      },
    },
    {
      label: "是否显示根路由",
      prop: "always_show",
      tag: {
        map: { true: { type: "success", text: "是" }, false: { type: "danger", text: "否" } },
      },
    },
    { label: "菜单标题", prop: "title" },
    { label: "路由参数", prop: "params" },
    {
      label: "是否固定路由",
      prop: "affix",
      tag: {
        map: { true: { type: "success", text: "是" }, false: { type: "danger", text: "否" } },
      },
    },
    {
      label: "状态",
      prop: "status",
      tag: {
        map: { "0": { type: "success", text: "启用" }, "1": { type: "danger", text: "停用" } },
      },
    },
    { label: "排序", prop: "order" },
    { label: "创建时间", prop: "created_time" },
    { label: "更新时间", prop: "updated_time" },
    { label: "描述", prop: "description", span: 4 },
  ];

// 菜单新增/编辑表单 —— 简单字段走 items，条件渲染/Tooltip标签/复杂控件走插槽
const menuDialogFormItems: FormItem[] = [
  { key: "parent_id", label: "父级菜单", type: "input" /* #parent_id 插槽 */ },
  { key: "name", label: "菜单名称", type: "input", props: { placeholder: "请输入菜单名称" } },
  { key: "title", label: "菜单标题", type: "input", props: { placeholder: "请输入菜单标题" } },
  { key: "type", label: "菜单类型", type: "input" /* #type 插槽 */ },
  { key: "client", label: "终端", type: "input" /* #client 插槽 */ },
  { key: "extlink_path", label: "外链地址", type: "input" /* #extlink_path 插槽 */ },
  { key: "route_name", label: "路由名称", type: "input" /* #route_name 插槽 */ },
  { key: "route_path", label: "路由路径", type: "input" /* #route_path 插槽 */ },
  { key: "component_path", label: "组件路径", type: "input" /* #component_path 插槽 */ },
  { key: "params", label: "路由参数", type: "input" /* #params 插槽 */ },
  { key: "hidden", label: "是否隐藏", type: "input" /* #hidden 插槽 */ },
  { key: "always_show", label: "始终显示", type: "input" /* #always_show 插槽 */ },
  { key: "keep_alive", label: "缓存页面", type: "input" /* #keep_alive 插槽 */ },
  { key: "order", label: "排序", type: "number", props: { controlsPosition: "right", min: 1 } },
  { key: "permission", label: "权限标识", type: "input" /* #permission 插槽 */ },
  { key: "icon", label: "图标", type: "input" /* #icon 插槽 */ },
  { key: "redirect", label: "重定向", type: "input" /* #redirect 插槽 */ },
  { key: "affix", label: "常驻标签栏", type: "input" /* #affix 插槽 */ },
  {
    key: "status",
    label: "状态",
    type: "radiogroup",
    props: {
      options: [
        { label: "启用", value: "0" },
        { label: "禁用", value: "1" },
      ],
    },
  },
  {
    key: "description",
    label: "描述",
    type: "input",
    props: {
      type: "textarea",
      rows: 4,
      maxlength: 100,
      showWordLimit: true,
      placeholder: "请输入描述",
    },
  },
];

const formData = ref<MenuForm>({
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

async function deleteMenuRow(id: number) {
  try {
    await ElMessageBox.confirm("确认删除该项数据?", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });

    await MenuAPI.deleteMenu([id]);
    await userStore.getUserInfo();
    ElMessage.success("删除成功");
    selectedRows.value = [];
    await loadMenuData();
  } catch {
    // 用户取消
  }
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
        ? h(FaMenuRouteIcon, { icon: row.icon, style: { verticalAlign: "-0.15em" } })
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
    width: 220,
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
        if (formData.value.type === MenuTypeEnum.CATALOG) {
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

const dataFormRef = ref<InstanceType<typeof FaForm> | null>(null);
const menuFormRenderKey = ref(0);

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
  const pid = formData.value.parent_id;
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
      Object.assign(formData.value, response.data.data);
    }
  } else {
    dialogVisible.title = "新增菜单";
    formData.value = { ...initialFormData };
    menuFormRenderKey.value += 1;
    if (parentRow?.id != null) {
      formData.value.parent_id = parentRow.id;
      formData.value.client = (parentRow.client as MenuClientEnum) || menuClientTab.value;
      if (parentRow.type === MenuTypeEnum.MENU) {
        createParentLocked.value = true;
        formData.value.type = MenuTypeEnum.BUTTON;
      } else if (parentRow.type === MenuTypeEnum.CATALOG) {
        formData.value.type = MenuTypeEnum.MENU;
      }
    } else {
      formData.value.client = menuClientTab.value;
    }
  }
  dialogVisible.visible = true;
}

function handleMenuTypeChange() {
  if (formData.value.type === MenuTypeEnum.MENU) {
    formData.value.component_path = "";
  }
  nextTick(() => {
    dataFormRef.value?.clearValidate("redirect");
    if (formData.value.type === MenuTypeEnum.CATALOG) {
      dataFormRef.value?.validateField("redirect")?.catch(() => {});
    }
  });
}

async function handleSubmit() {
  const allowed = allowedMenuTypeValues.value;
  if (!allowed.length) return;
  const t = formData.value.type as MenuTypeEnum;
  if (!allowed.includes(t)) {
    formData.value.type = allowed[0] as MenuForm["type"];
  }
  dataFormRef.value?.validate(async (valid: boolean) => {
    if (!valid) return;
    submitLoading.value = true;
    const id = formData.value.id;
    try {
      if (id) {
        await MenuAPI.updateMenu(id, { id, ...formData.value });
      } else {
        await MenuAPI.createMenu(formData.value);
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

async function handleBatchDelete() {
  const ids = selectedIds.value;
  if (ids.length === 0) return;
  try {
    await ElMessageBox.confirm(`确定删除选中的 ${ids.length} 条数据吗？`, "批量删除", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    batchDeleting.value = true;
    await MenuAPI.deleteMenu(ids);
    await userStore.getUserInfo();
    ElMessage.success("删除成功");
    selectedRows.value = [];
    await loadMenuData();
  } catch {
    // 用户取消
  } finally {
    batchDeleting.value = false;
  }
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
  });
  try {
    await ElMessageBox.confirm("确认启用或停用该项数据?", "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
    await MenuAPI.batchMenu({ ids, status });
    await loadMenuData();
  } catch {
    // 用户取消
  }
}

onMounted(() => {
  void loadMenuData();
});
</script>

<style scoped lang="scss">
:deep(.menu-table-actions .inline-flex) {
  vertical-align: middle;
}
</style>
