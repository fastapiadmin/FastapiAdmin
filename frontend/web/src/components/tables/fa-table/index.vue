<!--
  FaTable：ElTable 透传 + 分页 + 列渲染约定。
  - 属性 / 事件 / 插槽与 EP 文档一致；样式可由 tableStore 与 props 覆盖。
  - 暴露 `elTableRef`、`scrollToTop`；formatter 列见 TableFormatterOutlet 注释。
-->
<template>
  <div class="fa-table" :class="{ 'is-empty': isEmpty, 'no-pagination': !showPagination }">
    <div class="fa-table__main">
      <!-- 初始加载骨架屏：仅在 loading 且无数据时显示 -->
      <div v-if="loading && isEmpty" class="fa-table-skeleton">
        <ElSkeleton animated>
          <template #template>
            <div class="fa-table-skeleton__header">
              <ElSkeletonItem variant="rect" class="sk-c-1" />
              <ElSkeletonItem variant="rect" class="sk-c-2" />
              <ElSkeletonItem variant="rect" class="sk-c-3" />
              <ElSkeletonItem variant="rect" class="sk-c-4" />
              <ElSkeletonItem variant="rect" class="sk-c-5" />
              <ElSkeletonItem variant="rect" class="sk-c-6" />
            </div>
            <div v-for="i in 8" :key="i" class="fa-table-skeleton__row">
              <ElSkeletonItem variant="text" class="sk-c-1" />
              <ElSkeletonItem variant="text" class="sk-c-2" />
              <ElSkeletonItem variant="text" class="sk-c-3" />
              <ElSkeletonItem variant="text" class="sk-c-4" />
              <ElSkeletonItem variant="text" class="sk-c-5" />
              <ElSkeletonItem variant="text" class="sk-c-6" />
            </div>
          </template>
        </ElSkeleton>
      </div>
      <!-- 加载失败：保留页面骨架，提供明确原因与重试入口 -->
      <div v-else-if="error && isEmpty" class="fa-table__error" role="alert">
        <FaEmptyState
          icon="ri:error-warning-line"
          :title="$t('common.loadFailed')"
          :description="error.message"
        >
          <ElButton type="primary" plain @click="emit('retry')">
            {{ $t("common.retry") }}
          </ElButton>
        </FaEmptyState>
      </div>
      <!-- 通用移动端卡片：由列配置自动渲染 -->
      <div v-else-if="mobileCardsActive" class="fa-table__mobile-cards pb-12">
        <div v-if="data && data.length" class="flex items-center gap-2 px-1">
          <ElCheckbox
            :model-value="mobileAllSelected"
            :indeterminate="mobilePartiallySelected"
            @change="toggleMobileAll"
          >
            {{ $t("common.selectAll") }}
          </ElCheckbox>
        </div>
        <div v-if="!(data && data.length)" class="py-10 text-center text-sm text-g-500">
          {{ $t("common.noData") }}
        </div>
        <div
          v-for="(row, rowIndex) in data ?? []"
          :key="rowIndex"
          class="p-4 rounded-lg bg-(--default-box-color) border border-(--default-border)"
        >
          <div class="flex items-start justify-between gap-2">
            <ElCheckbox
              class="mt-0.5 shrink-0"
              :model-value="isMobileRowSelected(row)"
              @change="toggleMobileRow(row)"
            />
            <div class="min-w-0 flex-1 text-sm font-medium truncate">
              <component :is="() => mobileCell(mobileTitleColumn as ColumnOption, row)" />
            </div>
            <div v-if="mobileOperationColumn" class="mobile-card-actions mt-0! shrink-0">
              <component :is="() => mobileCell(mobileOperationColumn as ColumnOption, row)" />
            </div>
          </div>
          <div class="grid grid-cols-2 gap-x-3 gap-y-1.5 mt-3 text-xs text-g-600">
            <div
              v-for="col in mobileFieldColumns"
              :key="col.prop"
              class="min-w-0"
              :class="{
                'col-span-2': [
                  'created_time',
                  'updated_time',
                  'login_time',
                  'request_path',
                  'description',
                ].includes(col.prop ?? ''),
              }"
            >
              <span class="text-g-500">{{ col.label }}：</span>
              <component :is="() => mobileCell(col, row)" />
            </div>
          </div>
        </div>
      </div>
      <!-- 数据表格 -->
      <template v-else>
        <VueDraggable
          class="fa-table__drag-wrap"
          target="tbody"
          v-model="dragModel"
          :animation="150"
          :disabled="rowDragDisabled"
          @end="onRowDragEnd"
          ><ElTable
            ref="elTableRef"
            :key="tableKey"
            v-loading="!!loading"
            :expand-row-keys="
              props.rowKey && !hasExplicitTableProp('treeProps')
                ? expandRowKeys.map(String)
                : undefined
            "
            @expand-change="!hasExplicitTableProp('treeProps') ? onExpandChange : undefined"
            @selection-change="(val: any[]) => emit('selection-change', val)"
            v-bind="mergedTableProps"
          >
            <template v-for="col in displayColumns" :key="col.prop || col.type">
              <ElTableColumn v-if="col.type === 'globalIndex'" v-bind="{ ...col }">
                <template #default="{ $index }">
                  <span>{{ getGlobalIndex($index) }}</span>
                </template>
              </ElTableColumn>
              <ElTableColumn v-else-if="col.type === 'expand'" v-bind="cleanColumnProps(col)">
                <template #default="{ row: expandRow }">
                  <component :is="col.formatter ? col.formatter(expandRow) : null" />
                </template>
              </ElTableColumn>
              <ElTableColumn v-else v-bind="cleanBodyColumnProps(col)">
                <template #header="headerScope">
                  <component
                    v-if="col.useHeaderSlot && col.prop"
                    :is="() => renderColumnHeader(headerScope, col)"
                  />
                </template>
                <template #filter-icon="{ filterOpened }">
                  <Filter class="fa-filter-icon" :class="{ 'is-opened': filterOpened }" />
                </template>
                <template #default="slotScope">
                  <component
                    v-if="col.useSlot && col.prop && shouldRenderSlotScope(slotScope)"
                    :is="() => renderCellSlot(slotScope, col)"
                  />
                  <TableFormatterOutlet
                    v-else-if="col.formatter && !col.useSlot && shouldRenderSlotScope(slotScope)"
                    :column="col"
                    :record="slotScope.row"
                  />
                </template>
              </ElTableColumn>
            </template>
            <slot v-if="$slots.default" />
            <template #empty>
              <div v-if="loading"></div>
              <slot v-else name="empty">
                <FaEmptyState
                  icon="ri:inbox-line"
                  :title="emptyText || $t('common.noData')"
                  compact
                />
              </slot>
            </template>
          </ElTable>
        </VueDraggable>
      </template>
    </div>

    <div
      class="pagination"
      v-if="showPagination"
      :class="mergedPaginationOptions?.align"
      ref="paginationRef"
    >
      <FaPagination
        :page="pagination!.current"
        :limit="pagination!.size"
        :total="pagination!.total"
        :page-sizes="mergedPaginationOptions.pageSizes"
        :layout="mergedPaginationOptions.layout"
        :background="mergedPaginationOptions.background ?? true"
        :disabled="!!loading"
        :hidden="paginationHidden"
        :pager-count="mergedPaginationOptions.pagerCount"
        :size="mergedPaginationOptions.size"
        @pagination="handlePaginationEvent"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  ref,
  computed,
  nextTick,
  watch,
  getCurrentInstance,
  useAttrs,
  useSlots,
  isVNode,
  h,
  defineComponent,
  onMounted,
  onBeforeUnmount,
  type PropType,
} from "vue";
import { useI18n } from "vue-i18n";
import { translateColumnLabels } from "@utils/table/columnLabelI18n";
import type { ElTable, TableInstance, TableProps } from "element-plus";
import { useRoute } from "vue-router";
import { storeToRefs } from "pinia";

import { useTableStore } from "@stores";
import { useCommon } from "@/hooks/core/useCommon";
import { useTableHeight } from "@/hooks/core/useTableHeight";
import { useWindowSize } from "@vueuse/core";
import { VueDraggable } from "vue-draggable-plus";
import { Filter } from "@element-plus/icons-vue";
import { MOBILE_BREAKPOINT } from "@utils/constants/definitions";
import type { ColumnOption } from "@/types/component";
import type { TableError } from "@utils/table";

defineOptions({ name: "FaTable" });

defineSlots<{
  default(props: object): any;
  [slotName: string]: (props: Record<string, any>) => any;
}>();

const { width } = useWindowSize();
const isMobile = computed(() => width.value < MOBILE_BREAKPOINT);
// H5 ↔ 桌面切换时强制重建 ElTable，使列宽 / formatter 重新计算
const tableKey = computed(() => (isMobile.value ? "mobile" : "desktop"));
const elTableRef = ref<TableInstance | null>(null);
const paginationRef = ref<HTMLElement>();
const tableHeaderRef = ref<HTMLElement>();
const tableStore = useTableStore();
const slots = useSlots();
const {
  isBorder,
  isZebra,
  tableSize,
  isFullScreen,
  isHeaderBackground,
  isRowDrag,
  highlightCurrentRow,
} = storeToRefs(tableStore);

/** 分页配置接口 */
interface FaPaginationConfig {
  /** 当前页码 */
  current: number;
  /** 每页显示条目个数 */
  size: number;
  /** 总条目数 */
  total: number;
}

/** 分页器配置选项接口 */
interface PaginationOptions {
  /** 每页显示个数选择器的选项列表 */
  pageSizes?: number[];
  /** 分页器的对齐方式 */
  align?: "left" | "center" | "right";
  /** 分页器的布局 */
  layout?: string;
  /** 是否显示分页器背景 */
  background?: boolean;
  /** 只有一页时是否隐藏分页器 */
  hideOnSinglePage?: boolean;
  /** 分页器的大小 */
  size?: "small" | "default" | "large";
  /** 分页器的页码数量 */
  pagerCount?: number;
}

/** FaTable 组件的 Props 接口 */
interface Props extends TableProps<Record<string, any>> {
  /** 加载状态 */
  loading?: boolean;
  /** 列表请求错误；有值时展示可重试错误态 */
  error?: TableError | null;
  /** 列渲染配置 */
  columns?: ColumnOption[];
  /** 窄屏使用通用卡片列表（生成页/普通表格页可开启） */
  mobileCards?: boolean;
  /** 分页状态 */
  pagination?: FaPaginationConfig;
  /** 分页配置 */
  paginationOptions?: PaginationOptions;
  /** 空数据表格高度 */
  emptyHeight?: string;
  /** 空数据时显示的文本 */
  emptyText?: string;
  /** 是否开启 FaTableHeader，解决表格高度自适应问题 */
  showTableHeader?: boolean;
  /** 为 true 时关闭行拖拽（忽略工具栏「行拖拽」开关） */
  disableRowDrag?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  columns: () => [],
  mobileCards: false,
  fit: true,
  showHeader: true,
  stripe: undefined,
  border: undefined,
  size: undefined,
  emptyHeight: "100%",
  emptyText: "",
  showTableHeader: true,
  disableRowDrag: false,
});
const instance = getCurrentInstance();
const attrs = useAttrs();
const route = useRoute();

// ── 树形表格展开状态记忆 ──
/** localStorage 存储 key */
const expandStorageKey = computed(() => `table-expand-${route.path}`);

/** 当前展开的行 key 集合 */
const expandRowKeys = ref<(string | number)[]>([]);

/** 保存展开状态到 localStorage */
function saveExpandState(keys: (string | number)[]) {
  try {
    localStorage.setItem(expandStorageKey.value, JSON.stringify(keys));
  } catch {
    // 静默忽略
  }
}

/** 从 localStorage 恢复展开状态 */
function restoreExpandState(): (string | number)[] {
  try {
    const raw = localStorage.getItem(expandStorageKey.value);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

// 数据刷新后尝试恢复展开状态
watch(
  () => props.data,
  (newData) => {
    if (!newData?.length) {
      expandRowKeys.value = [];
      return;
    }
    const savedKeys = restoreExpandState();
    if (savedKeys.length > 0) {
      expandRowKeys.value = savedKeys;
    }
  },
  { immediate: true }
);

/** 仅当调用方显式传入对应 prop 时视为「固定」，否则交由表格 store */
const hasExplicitTableProp = (propName: string): boolean => {
  try {
    const rawProps = (instance?.vnode.props || {}) as Record<string, unknown>;
    const kebabName = propName.replace(/[A-Z]/g, (match) => `-${match.toLowerCase()}`);
    return propName in rawProps || kebabName in rawProps;
  } catch {
    return false;
  }
};

const LAYOUT = {
  MOBILE: "prev, pager, next, sizes, jumper, total",
  IPAD: "prev, pager, next, jumper, total",
  DESKTOP: "total, prev, pager, next, sizes, jumper",
};

const layout = computed(() => {
  if (width.value < MOBILE_BREAKPOINT) {
    return LAYOUT.MOBILE;
  } else if (width.value < 1024) {
    return LAYOUT.IPAD;
  } else {
    return LAYOUT.DESKTOP;
  }
});

// 默认分页常量
const DEFAULT_PAGINATION_OPTIONS: PaginationOptions = {
  pageSizes: [10, 20, 30, 50, 100],
  align: "center",
  background: true,
  layout: layout.value,
  hideOnSinglePage: false,
  size: undefined,
  pagerCount: width.value > 1200 ? 7 : 5,
};

// 合并分页配置
const mergedPaginationOptions = computed(() => ({
  ...DEFAULT_PAGINATION_OPTIONS,
  ...props.paginationOptions,
}));

/** 对齐 ElPagination hide-on-single-page，交给封装组件的 hidden */
const paginationHidden = computed(() => {
  const p = props.pagination;
  const opts = mergedPaginationOptions.value;
  if (!p || !opts.hideOnSinglePage) return false;
  const size = p.size || 10;
  const total = p.total ?? 0;
  if (total <= 0) return false;
  return Math.ceil(total / size) <= 1;
});

// 边框 (优先级：props > store)
const border = computed(() => props.border ?? isBorder.value);
// 斑马纹
const stripe = computed(() => props.stripe ?? isZebra.value);
// 表格尺寸
const size = computed(() => props.size ?? tableSize.value);
const { t: translate } = useI18n();
const displayColumns = computed(() => translateColumnLabels(props.columns ?? [], translate));
const mobileCardsActive = computed(() => props.mobileCards && width.value < 1025);

function getRowValue(row: Record<string, unknown>, path: string): unknown {
  return path.split(".").reduce<unknown>((acc, key) => {
    if (acc && typeof acc === "object") return (acc as Record<string, unknown>)[key];
    return undefined;
  }, row);
}

function mobileCell(col: ColumnOption, row: Record<string, unknown>) {
  const slot = col.prop ? slots[col.prop] : undefined;
  if (slot) {
    const rendered = slot({ row });
    return Array.isArray(rendered) ? h("span", rendered) : rendered;
  }
  if (col.formatter) {
    const out = col.formatter(row);
    return isVNode(out) ? out : h("span", String(out ?? "—"));
  }
  const value = col.prop ? getRowValue(row, col.prop) : "";
  return h("span", value === null || value === undefined || value === "" ? "—" : String(value));
}

const mobileTitleColumn = computed(
  () =>
    displayColumns.value.find((col) =>
      ["name", "title", "username", "notice_title", "request_path", "version"].includes(
        col.prop ?? ""
      )
    ) ?? displayColumns.value.find((col) => col.prop && col.prop !== "operation")
);

const mobileFieldColumns = computed(() =>
  displayColumns.value
    .filter(
      (col) =>
        col.prop &&
        col.prop !== "operation" &&
        col.prop !== mobileTitleColumn.value?.prop &&
        col.type !== "selection" &&
        col.type !== "globalIndex" &&
        col.type !== "expand"
    )
    .slice(0, 8)
);

const mobileOperationColumn = computed(() =>
  displayColumns.value.find((col) => col.prop === "operation")
);

const mobileSelectedRows = ref<Record<string, unknown>[]>([]);

const mobileAllSelected = computed(() => {
  const rows = props.data ?? [];
  return rows.length > 0 && mobileSelectedRows.value.length === rows.length;
});

const mobilePartiallySelected = computed(() => {
  const count = mobileSelectedRows.value.length;
  return count > 0 && count < (props.data?.length ?? 0);
});

function isMobileRowSelected(row: Record<string, unknown>): boolean {
  return mobileSelectedRows.value.includes(row);
}

function emitMobileSelection(): void {
  emit("selection-change", [...mobileSelectedRows.value]);
}

function toggleMobileRow(row: Record<string, unknown>): void {
  const index = mobileSelectedRows.value.indexOf(row);
  if (index >= 0) mobileSelectedRows.value.splice(index, 1);
  else mobileSelectedRows.value.push(row);
  emitMobileSelection();
}

function toggleMobileAll(checked: boolean | string | number): void {
  mobileSelectedRows.value = checked ? [...(props.data ?? [])] : [];
  emitMobileSelection();
}

watch(
  () => props.data,
  () => {
    mobileSelectedRows.value = [];
    if (mobileCardsActive.value) emitMobileSelection();
  }
);
// 数据是否为空
const isEmpty = computed(() => props.data?.length === 0);

const paginationHeight = ref(0);
const tableHeaderHeight = ref(0);

// 使用 useResizeObserver 监听分页器高度变化
useResizeObserver(paginationRef, (entries) => {
  const entry = entries[0];
  if (entry) {
    // 使用 requestAnimationFrame 避免 ResizeObserver loop 警告
    requestAnimationFrame(() => {
      paginationHeight.value = entry.contentRect.height;
    });
  }
});

// 使用 useResizeObserver 监听表格头部高度变化
useResizeObserver(tableHeaderRef, (entries) => {
  const entry = entries[0];
  if (entry) {
    // 使用 requestAnimationFrame 避免 ResizeObserver loop 警告
    requestAnimationFrame(() => {
      tableHeaderHeight.value = entry.contentRect.height;
    });
  }
});

// 分页器与表格之间的间距常量（计算属性，响应 showTableHeader 变化）
const PAGINATION_SPACING = computed(() => (props.showTableHeader ? 6 : 15));

// 使用表格高度计算 Hook（返回含分页、表头偏移的精确高度）
useTableHeight({
  showTableHeader: computed(() => props.showTableHeader),
  paginationHeight,
  tableHeaderHeight,
  paginationSpacing: PAGINATION_SPACING,
});

// 表格高度逻辑
const height = computed(() => {
  // 全屏模式下占满全屏
  if (isFullScreen.value) return "100%";
  // 空数据且非加载状态时固定高度
  if (isEmpty.value && !props.loading) return props.emptyHeight;
  // 使用传入的高度
  if (props.height) return props.height;
  // flex 布局下 .fa-table__main 已扣除分页空间，ElTable 用 100% 填满即可
  return "100%";
});

// 表头背景颜色样式
const headerCellStyle = computed(() => ({
  background: isHeaderBackground.value
    ? "var(--el-fill-color-lighter)"
    : "var(--default-box-color)",
  ...(props.headerCellStyle || {}), // 合并用户传入的样式
}));

const mergedTableProps = computed(() => {
  const { expandRowKeys: _ignored, ...restProps } = props;
  void _ignored;
  return {
    ...attrs,
    ...restProps,
    height: height.value,
    stripe: stripe.value,
    border: border.value,
    size: size.value,
    headerCellStyle: headerCellStyle.value,
    highlightCurrentRow: highlightCurrentRow.value,
    // Element Plus 默认值为 true，未显式传入时不应被 FaTable 覆盖成 false。
    selectOnIndeterminate: hasExplicitTableProp("selectOnIndeterminate")
      ? props.selectOnIndeterminate
      : undefined,
  };
});

interface Emits {
  (e: "selection-change", val: any[]): void;
  (e: "pagination:size-change", val: number): void;
  (e: "pagination:current-change", val: number): void;
  (e: "update:data", val: Record<string, unknown>[]): void;
  (e: "row-order-change", val: Record<string, unknown>[]): void;
  (e: "retry"): void;
}

const emit = defineEmits<Emits>();

/** 无 data 时用固定空数组，避免 v-model 每次拿到新 [] */
const emptyDataStub = ref<Record<string, unknown>[]>([]);

const dragModel = computed({
  get() {
    const d = props.data;
    if (Array.isArray(d)) return d;
    return emptyDataStub.value;
  },
  set(val) {
    emit("update:data", val);
  },
});

const rowDragActive = computed(() => !props.disableRowDrag && isRowDrag.value);

const rowDragDisabled = computed(() => !rowDragActive.value || !!props.loading);

const onRowDragEnd = () => {
  const d = props.data;
  if (Array.isArray(d)) {
    emit("row-order-change", d as Record<string, unknown>[]);
  }
};

/** 树形表格行展开/收起变化时记录状态 */
const onExpandChange = (row: Record<string, unknown>, expandedRows: Record<string, unknown>[]) => {
  const rowKey = (row as Record<string, unknown>)[props.rowKey as string];
  if (rowKey === undefined || rowKey === null) return;

  const currentKeys = [...expandRowKeys.value];
  const isExpanded = expandedRows.some(
    (r) => (r as Record<string, unknown>)[props.rowKey as string] === rowKey
  );

  if (isExpanded) {
    if (!currentKeys.includes(rowKey as string | number)) {
      currentKeys.push(rowKey as string | number);
    }
  } else {
    const idx = currentKeys.indexOf(rowKey as string | number);
    if (idx > -1) {
      currentKeys.splice(idx, 1);
    }
  }

  expandRowKeys.value = currentKeys;
  saveExpandState(currentKeys);
};

// 是否显示分页器
const showPagination = computed(() => !!props.pagination);

// 无分页树形表：最后一条“可见”行不画底边；隐藏行可能排在最后，不能只靠 :last-child
let lastRowObserver: MutationObserver | null = null;
let lastRowFrame = 0;
const markLastVisibleRow = () => {
  const table = elTableRef.value?.$el as HTMLElement | undefined;
  if (!table || showPagination.value) return;
  const rows = table.querySelectorAll<HTMLElement>(".el-table__body tr");
  let lastVisible: HTMLElement | undefined;
  rows.forEach((row) => {
    row.classList.remove("fa-table-last-visible-row");
    if (row.getClientRects().length > 0) lastVisible = row;
  });
  lastVisible?.classList.add("fa-table-last-visible-row");
};
const scheduleMarkLastRow = () => {
  cancelAnimationFrame(lastRowFrame);
  lastRowFrame = requestAnimationFrame(markLastVisibleRow);
};
onMounted(() => {
  nextTick(() => {
    const table = elTableRef.value?.$el as HTMLElement | undefined;
    if (!table) return;
    lastRowObserver = new MutationObserver(scheduleMarkLastRow);
    lastRowObserver.observe(table, {
      subtree: true,
      childList: true,
      attributes: true,
      attributeFilter: ["style"],
    });
    scheduleMarkLastRow();
  });
});
onBeforeUnmount(() => {
  lastRowObserver?.disconnect();
  lastRowObserver = null;
  cancelAnimationFrame(lastRowFrame);
});
watch(
  () => [props.data, props.loading, props.pagination?.current, props.pagination?.size],
  () => nextTick(scheduleMarkLastRow),
  { deep: false }
);

// Element Plus 在部分场景会先用 $index = -1 进行预渲染。
// 这对普通展示无影响，但会让 ElForm 错误注册出 lineList.-1.xxx 这类字段。
const shouldRenderSlotScope = (slotScope: { $index?: number }) => {
  return slotScope.$index === undefined || slotScope.$index >= 0;
};

/** Vue 3.5：useSlots() 直接调用 slot 渲染函数，模板中零 <slot> 元素 */
function renderColumnHeader(headerScope: Record<string, unknown>, col: Record<string, unknown>) {
  const slotName = (col.headerSlotName || `${col.prop}-header`) as string;
  return slots[slotName]?.({ ...headerScope, prop: col.prop, label: col.label }) ?? col.label;
}

function renderCellSlot(slotScope: Record<string, unknown>, col: Record<string, unknown>) {
  const slotName = (col.slotName || col.prop) as string;
  const row = slotScope.row as Record<string, unknown> | undefined;
  return (
    slots[slotName]?.({
      ...slotScope,
      prop: col.prop,
      value: col.prop ? row?.[col.prop as string] : undefined,
    }) ?? null
  );
}

/**
 * ElTableColumn 若存在 default 插槽且插槽产物含任意非 Comment 的 vnode（含空白文本节点），
 * 将不会执行 formatter（见 element-plus render-helper setColumnRenders）。
 * FaTable 中 ElTableColumn 与子节点之间的换行/缩进可能被编译进默认插槽，导致 formatter（如操作列里的按钮）永远不渲染。
 * 对声明了 formatter 且未使用 useSlot 的列，在此显式渲染 formatter 返回值。
 */
const renderColumnFormatter = (col: ColumnOption, row: Record<string, unknown>) => {
  if (!col.formatter) return null;
  const result = col.formatter(row as never);
  if (isVNode(result)) return result;
  if (result === null || result === undefined) return null;
  return h("span", String(result));
};

/**
 * 在 render 里调用 formatter(row) 生成 VNode；勿把 VNode 当 props 传入（克隆后会失效）。
 * 与 renderColumnFormatter 同文件定义，保证闭包一致。
 */
const TableFormatterOutlet = defineComponent({
  name: "TableFormatterOutlet",
  props: {
    column: { type: Object as PropType<ColumnOption>, required: true },
    /** 避免 prop 名 row 与插槽解构冲突 */
    record: { type: Object as PropType<Record<string, unknown>>, required: true },
  },
  setup(props) {
    return () => renderColumnFormatter(props.column, props.record);
  },
});

// 清理列属性，移除插槽相关的自定义属性，确保它们不会被 ElTableColumn 错误解释
const cleanColumnProps = (col: ColumnOption) => {
  const columnProps = { ...col };
  // 删除自定义的插槽控制属性
  delete columnProps.useHeaderSlot;
  delete columnProps.headerSlotName;
  delete columnProps.useSlot;
  delete columnProps.slotName;
  return columnProps;
};

/** 创建人 / 更新人列识别：通过 prop 或 label 匹配 */
const PERSON_FILTER_RE = /(?:create|update)(?:d)?_(?:by|user|name|id)|creator|updater/i;
const isPersonFilterColumn = (col: ColumnOption): boolean => {
  // 已显式配置筛选则跳过自动逻辑
  if (col.filters || col.filterMethod) return false;
  const prop = col.prop || "";
  const label = col.label || "";
  return PERSON_FILTER_RE.test(prop) || /创建人|更新人|创建者|更新者/.test(label);
};

/** 将创建人/更新人列 prop 归一化为名称取值路径：
 *  created_id → created_by.name；created_by / created_by.name 等保持不变 */
const getPersonNamePath = (prop: string): string => prop.replace(/_id(?:\..*)?$/i, "_by.name");

/** 解析嵌套路径取值（如 created_by.name），与 ElTable 单元格取值规则一致 */
const getPathValue = (row: Record<string, any>, path: string): unknown => {
  let value: unknown = row;
  for (const key of path.split(".")) {
    if (value == null) return undefined;
    value = (value as Record<string, unknown>)[key];
  }
  return value;
};

/** 单元格值规范化为筛选文本：对象时优先取 name（created_by/updated_by 为对象） */
const toFilterText = (v: unknown): string => {
  if (v && typeof v === "object" && "name" in v) {
    return String((v as { name: unknown }).name ?? "");
  }
  return String(v);
};

/** 从当前表格数据中提取某列的去重值作为筛选选项 */
const getColumnFilterOptions = (col: ColumnOption): { text: string; value: string }[] => {
  if (!col.prop) return [];
  const seen = new Set<string>();
  const options: { text: string; value: string }[] = [];
  const path = getPersonNamePath(col.prop);
  for (const row of props.data || []) {
    const v = getPathValue(row as Record<string, any>, path);
    if (v === null || v === undefined || v === "") continue;
    const text = toFilterText(v);
    if (!text) continue;
    if (!seen.has(text)) {
      seen.add(text);
      options.push({ text, value: text });
    }
  }
  return options;
};

/** 普通列：单元格已由插槽内 TableFormatterOutlet 渲染，勿再把 formatter 传给 ElTableColumn，避免与 EP 内置 renderCell 混用 */
const cleanBodyColumnProps = (col: ColumnOption) => {
  const columnProps = cleanColumnProps(col);
  delete columnProps.formatter;
  // H5 端：操作列只显示「更多」按钮，宽度收窄到 80；响应式跟随窗口变化
  const isOpCol = col.prop === "operation" || col.label === "操作";
  if (isOpCol && isMobile.value) {
    columnProps.width = 80;
  }
  // 数字类列默认右对齐（金额/数量/大小/比率等），可用 align 显式覆盖
  const NUMERIC_PROP_RE =
    /(price|amount|total|count|qty|quantity|size|score|rate|usage|percent|salary|balance|cost|fee|weight|duration|cpu|memory|disk)/i;
  const NUMERIC_LABEL_RE =
    /(金额|价格|数量|总数|次数|大小|占比|比率|百分比|容量|时长|内存|磁盘|使用率|得分|费用|余额)/;
  if (
    columnProps.align === undefined &&
    !isOpCol &&
    (NUMERIC_PROP_RE.test(String(col.prop || "")) || NUMERIC_LABEL_RE.test(String(col.label || "")))
  ) {
    columnProps.align = "right";
  }
  // 普通文本列默认省略 + 悬停显示完整内容（状态/格式化/操作列除外）
  if (
    columnProps.showOverflowTooltip === undefined &&
    !isOpCol &&
    !col.formatter &&
    !col.status &&
    !col.type
  ) {
    columnProps.showOverflowTooltip = true;
  }
  // 创建人 / 更新人列：自动生成表头筛选选项，无需调用方手写 filters
  if (isPersonFilterColumn(col)) {
    columnProps.filters = getColumnFilterOptions(col);
    columnProps.filterMethod = (value: any, row: any) =>
      toFilterText(
        getPathValue(row as Record<string, any>, getPersonNamePath(col.prop as string))
      ) === String(value);
  }
  return columnProps;
};

const { scrollToTop: scrollPageToTop } = useCommon();

// 滚动表格内容到顶部，并可以联动页面滚动到顶部
const scrollToTop = () => {
  nextTick(() => {
    elTableRef.value?.setScrollTop(0); // 滚动 ElTable 内部滚动条到顶部
    scrollPageToTop(); // 调用公共 composable 滚动页面到顶部
  });
};

/** 对接封装分页 @pagination，保持对外仍为 size-change / current-change 事件 */
const handlePaginationEvent = (payload: { page: number; limit: number }) => {
  const p = props.pagination;
  if (!p) return;
  if (payload.limit !== p.size) {
    emit("pagination:size-change", payload.limit);
    return;
  }
  if (payload.page !== p.current) {
    emit("pagination:current-change", payload.page);
    scrollToTop();
  }
};

// 全局序号
const getGlobalIndex = (index: number) => {
  if (!props.pagination) return index + 1;
  const { current, size } = props.pagination;
  return (current - 1) * size + index + 1;
};

// 查找并绑定表格头部元素 - 使用 VueUse 优化
const findTableHeader = () => {
  if (!props.showTableHeader) {
    tableHeaderRef.value = undefined;
    return;
  }

  const tableHeader = document.getElementById("fa-table-header");
  if (tableHeader) {
    tableHeaderRef.value = tableHeader;
  } else {
    // 如果找不到表格头部，设置为 undefined，useElementSize 会返回 0
    tableHeaderRef.value = undefined;
  }
};

watch(
  () => props.showTableHeader,
  (shouldShow) => {
    if (shouldShow) {
      nextTick(() => {
        findTableHeader();
      });
    } else {
      tableHeaderRef.value = undefined;
    }
  },
  { immediate: true }
);

defineExpose({
  scrollToTop,
  elTableRef,
});
</script>

<style lang="scss" scoped>
.fa-table {
  position: relative;
  /* 无分页时不需要“表格 → 分页”的分隔线；覆盖普通/固定列/树形表最后一行 */
  &.no-pagination {
    :deep(.el-table__body tr:last-child > td),
    :deep(.el-table__body tr:last-child > th),
    :deep(.el-table__row:last-child > td) {
      border-bottom: 0 !important;
      box-shadow: none !important;
    }

    :deep(.el-table__inner-wrapper::before),
    :deep(.el-table__inner-wrapper::after),
    :deep(.el-table__body-wrapper::after) {
      content: none !important;
    }

    /* 树形表/折叠行会在可见行后保留隐藏行，:last-child 不一定是最后可见行 */
    :deep(.fa-table-last-visible-row > td) {
      border-bottom: 0 !important;
      box-shadow: none !important;
    }
  }

  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;

  .fa-table__main {
    flex: 1;
    min-height: 0;
    padding-top: 10px;

    /* VueDraggable 透传高度，确保 ElTable height: 100% 能正确解析 */
    > * {
      height: 100%;
    }
  }

  /* ── 表格骨架屏 ── */
  .fa-table-skeleton {
    padding: 12px 0;

    .fa-table-skeleton__header {
      display: grid;
      grid-template-columns: 56px 1fr 1fr 120px 1fr 100px;
      gap: 4px;
      padding: 10px 16px;
      margin-bottom: 4px;
      border-bottom: 1px solid var(--el-border-color-lighter);

      .el-skeleton__item {
        height: 22px;
      }
    }

    .fa-table-skeleton__row {
      display: grid;
      grid-template-columns: 56px 1fr 1fr 120px 1fr 100px;
      gap: 4px;
      align-items: center;
      padding: 12px 16px;
    }

    /* 每行 6 列宽度的别名 */
    .sk-c-1 {
      grid-column: 1;
    }

    .sk-c-2 {
      grid-column: 2;
    }

    .sk-c-3 {
      grid-column: 3;
    }

    .sk-c-4 {
      grid-column: 4;
    }

    .sk-c-5 {
      grid-column: 5;
    }

    .sk-c-6 {
      grid-column: 6;
    }
  }

  .el-table {
    height: 100%;
  }

  :deep(.el-loading-mask) {
    z-index: 100;
    background-color: var(--default-box-color) !important;
  }

  /* Loading 过渡动画 - 消失时淡出 */
  .loading-fade-leave-active {
    transition: opacity 0.3s ease-out;
  }

  .loading-fade-leave-to {
    opacity: 0;
  }

  /* 空状态垂直居中 + 优化间距 */
  &.is-empty {
    :deep(.el-table__body-wrapper) {
      display: flex;
      align-items: center;
      justify-content: center;
    }

    :deep(.el-table__empty-block) {
      min-height: 180px;
    }

    :deep(.el-empty) {
      .el-empty__image {
        width: var(--fa-empty-size, 60px);
      }

      .el-empty__description {
        margin-top: 8px;

        p {
          font-size: 13px;
          color: var(--fa-gray-500);
        }
      }
    }
  }

  /* 表格行悬停行高亮（强化） */
  :deep(.el-table__body tr.el-table__row) {
    transition: background-color 0.2s ease;

    &:hover > td.el-table__cell {
      background-color: var(--fa-hover-color) !important;
    }

    &.current-row > td.el-table__cell {
      background-color: color-mix(in srgb, var(--el-color-primary) 8%, transparent) !important;
    }
  }

  /* 斑马纹优化 */
  :deep(.el-table--striped .el-table__body tr.el-table__row--striped) {
    td.el-table__cell {
      background-color: var(--fa-gray-100);
    }

    &:hover td.el-table__cell {
      background-color: var(--fa-hover-color) !important;
    }
  }

  /* 分页按钮样式已统一由 FaPagination 组件处理 */
  .pagination {
    display: flex;
    flex-shrink: 0;
    padding-top: 13px;

    /* 分页对齐方式 */
    &.left {
      justify-content: flex-start;
    }

    &.center {
      justify-content: center;
    }

    &.right {
      justify-content: flex-end;
    }
  }

  /* 表头筛选图标：替换 EP 默认箭头为漏斗，悬停/展开/已筛选时高亮为主题色 */
  :deep(.el-table__column-filter-trigger .fa-filter-icon) {
    color: var(--el-text-color-placeholder);
    transition: color 0.2s ease;
  }

  :deep(.el-table__column-filter-trigger:hover .fa-filter-icon),
  :deep(.el-table__column-filter-trigger .fa-filter-icon.is-opened),
  :deep(.cell.highlight .fa-filter-icon) {
    color: var(--theme-color);
  }
}

.fa-table__error {
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: center;
  min-height: 240px;
  padding: 32px 16px;
}

.fa-table__mobile-cards {
  height: 100%;
  overflow-y: auto;
}

@media (width >= 800px) and (width <= 1200px) {
  .fa-table__mobile-cards {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    align-content: start;
    gap: 16px;
  }

  .fa-table__mobile-cards > .py-10 {
    grid-column: 1 / -1;
  }
}
</style>
