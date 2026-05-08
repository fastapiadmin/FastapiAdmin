<!-- 表格组件 -->
<!-- 支持：el-table 全部属性、事件、插槽，同官方文档写法 -->
<!-- 扩展功能：分页组件、渲染自定义列、loading、表格全局边框、斑马纹、表格尺寸、表头背景配置 -->
<!-- 获取 ref：默认暴露了 elTableRef 外部通过 ref.value.elTableRef 可以调用 el-table 方法 -->
<template>
  <div class="art-table" :class="{ 'is-empty': isEmpty }" :style="containerHeight">
    <VueDraggable
      target="tbody"
      v-model="dragModel"
      :animation="150"
      :disabled="rowDragDisabled"
      @end="onRowDragEnd"
    >
      <ElTable ref="elTableRef" v-loading="!!loading" v-bind="mergedTableProps">
        <template v-for="col in columns" :key="col.prop || col.type">
          <!-- 渲染全局序号列 -->
          <ElTableColumn v-if="col.type === 'globalIndex'" v-bind="{ ...col }">
            <template #default="{ $index }">
              <span>{{ getGlobalIndex($index) }}</span>
            </template>
          </ElTableColumn>

          <!-- 渲染展开行 -->
          <ElTableColumn v-else-if="col.type === 'expand'" v-bind="cleanColumnProps(col)">
            <template #default="{ row: expandRow }">
              <component :is="col.formatter ? col.formatter(expandRow) : null" />
            </template>
          </ElTableColumn>

          <!-- 渲染普通列：default 插槽须紧凑书写，避免空白文本抢占 formatter（见 renderColumnFormatter 注释） -->
          <ElTableColumn v-else v-bind="cleanBodyColumnProps(col)">
            <template v-if="col.useHeaderSlot && col.prop" #header="headerScope">
              <slot
                :name="col.headerSlotName || `${col.prop}-header`"
                v-bind="{ ...headerScope, prop: col.prop, label: col.label }"
              >
                {{ col.label }}
              </slot>
            </template>
            <!-- 整段单行：插槽内兄弟节点之间的空白文本会让 EP 误判单元格内容 -->
            <!-- eslint-disable-next-line vue/max-attributes-per-line, prettier/prettier -->
            <template #default="slotScope">
              <slot
                v-if="col.useSlot && col.prop && shouldRenderSlotScope(slotScope)"
                :name="col.slotName || col.prop"
                v-bind="{
                  ...slotScope,
                  prop: col.prop,
                  value: col.prop ? slotScope.row[col.prop] : undefined,
                }"
              />
              <TableFormatterOutlet
                v-else-if="col.formatter && !col.useSlot && shouldRenderSlotScope(slotScope)"
                :column="col"
                :record="slotScope.row"
              />
            </template>
          </ElTableColumn>
        </template>

        <template v-if="$slots.default" #default><slot /></template>

        <template #empty>
          <div v-if="loading"></div>
          <ElEmpty v-else :description="emptyText" :image-size="120" />
        </template>
      </ElTable>
    </VueDraggable>

    <div
      class="pagination custom-pagination"
      v-if="showPagination"
      :class="mergedPaginationOptions?.align"
      ref="paginationRef"
    >
      <Pagination
        v-if="pagination"
        :page="pagination.current"
        :limit="pagination.size"
        :total="pagination.total"
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
  watchEffect,
  getCurrentInstance,
  useAttrs,
  isVNode,
  h,
  defineComponent,
  type PropType,
} from "vue";
import type { ElTable, TableProps } from "element-plus";
import { storeToRefs } from "pinia";
import { ColumnOption } from "@/types";
import { useTableStore } from "@stores/modules/table.store";
import { useCommon } from "@/hooks/core/useCommon";
import { useTableHeight } from "@/hooks/core/useTableHeight";
import { useResizeObserver, useWindowSize } from "@vueuse/core";
import Pagination from "@/components/Pagination/index.vue";
import { VueDraggable } from "vue-draggable-plus";

defineOptions({ name: "ArtTable" });

const { width } = useWindowSize();
const elTableRef = ref<InstanceType<typeof ElTable> | null>(null);
const paginationRef = ref<HTMLElement>();
const tableHeaderRef = ref<HTMLElement>();
const tableStore = useTableStore();
const { isBorder, isZebra, tableSize, isFullScreen, isHeaderBackground, isRowDrag } =
  storeToRefs(tableStore);

/** 分页配置接口 */
interface PaginationConfig {
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

/** ArtTable 组件的 Props 接口 */
interface ArtTableProps extends TableProps<Record<string, any>> {
  /** 加载状态 */
  loading?: boolean;
  /** 列渲染配置 */
  columns?: ColumnOption[];
  /** 分页状态 */
  pagination?: PaginationConfig;
  /** 分页配置 */
  paginationOptions?: PaginationOptions;
  /** 空数据表格高度 */
  emptyHeight?: string;
  /** 空数据时显示的文本 */
  emptyText?: string;
  /** 是否开启 ArtTableHeader，解决表格高度自适应问题 */
  showTableHeader?: boolean;
  /** 为 true 时关闭行拖拽（忽略工具栏「行拖拽」开关） */
  disableRowDrag?: boolean;
}

const props = withDefaults(defineProps<ArtTableProps>(), {
  columns: () => [],
  fit: true,
  showHeader: true,
  stripe: undefined,
  border: undefined,
  size: undefined,
  emptyHeight: "100%",
  emptyText: "暂无数据",
  showTableHeader: true,
  disableRowDrag: false,
});
const instance = getCurrentInstance();
const attrs = useAttrs();

/** 仅当调用方显式传入对应 prop 时视为「固定」，否则交由表格 store */
const hasExplicitTableProp = (propName: string): boolean => {
  const rawProps = (instance?.vnode.props || {}) as Record<string, unknown>;
  const kebabName = propName.replace(/[A-Z]/g, (match) => `-${match.toLowerCase()}`);
  return propName in rawProps || kebabName in rawProps;
};

const LAYOUT = {
  MOBILE: "prev, pager, next, sizes, jumper, total",
  IPAD: "prev, pager, next, jumper, total",
  DESKTOP: "total, prev, pager, next, sizes, jumper",
};

const layout = computed(() => {
  if (width.value < 768) {
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
  size: "default",
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

// 使用表格高度计算 Hook
const { containerHeight } = useTableHeight({
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
  // 默认占满容器高度
  return "100%";
});

// 表头背景颜色样式
const headerCellStyle = computed(() => ({
  background: isHeaderBackground.value
    ? "var(--el-fill-color-lighter)"
    : "var(--default-box-color)",
  ...(props.headerCellStyle || {}), // 合并用户传入的样式
}));

const mergedTableProps = computed(() => ({
  ...attrs,
  ...props,
  height: height.value,
  stripe: stripe.value,
  border: border.value,
  size: size.value,
  headerCellStyle: headerCellStyle.value,
  // Element Plus 默认值为 true，未显式传入时不应被 ArtTable 覆盖成 false。
  selectOnIndeterminate: hasExplicitTableProp("selectOnIndeterminate")
    ? props.selectOnIndeterminate
    : undefined,
}));

const emit = defineEmits<{
  (e: "pagination:size-change", val: number): void;
  (e: "pagination:current-change", val: number): void;
  (e: "update:data", val: Record<string, unknown>[]): void;
  (e: "row-order-change", val: Record<string, unknown>[]): void;
}>();

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

// 是否显示分页器
const showPagination = computed(() => props.pagination && !isEmpty.value);

// Element Plus 在部分场景会先用 $index = -1 进行预渲染。
// 这对普通展示无影响，但会让 ElForm 错误注册出 lineList.-1.xxx 这类字段。
const shouldRenderSlotScope = (slotScope: { $index?: number }) => {
  return slotScope.$index === undefined || slotScope.$index >= 0;
};

/**
 * ElTableColumn 若存在 default 插槽且插槽产物含任意非 Comment 的 vnode（含空白文本节点），
 * 将不会执行 formatter（见 element-plus render-helper setColumnRenders）。
 * ArtTable 中 ElTableColumn 与子节点之间的换行/缩进可能被编译进默认插槽，导致 formatter（如操作列里的按钮）永远不渲染。
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

/** 普通列：单元格已由插槽内 TableFormatterOutlet 渲染，勿再把 formatter 传给 ElTableColumn，避免与 EP 内置 renderCell 混用 */
const cleanBodyColumnProps = (col: ColumnOption) => {
  const columnProps = cleanColumnProps(col);
  delete columnProps.formatter;
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

  const tableHeader = document.getElementById("art-table-header");
  if (tableHeader) {
    tableHeaderRef.value = tableHeader;
  } else {
    // 如果找不到表格头部，设置为 undefined，useElementSize 会返回 0
    tableHeaderRef.value = undefined;
  }
};

watchEffect(
  () => {
    // 访问响应式数据以建立依赖追踪
    void props.data?.length; // 追踪数据变化
    const shouldShow = props.showTableHeader;

    // 只有在需要显示表格头部时才查找
    if (shouldShow) {
      nextTick(() => {
        findTableHeader();
      });
    } else {
      // 不显示时清空引用
      tableHeaderRef.value = undefined;
    }
  },
  { flush: "post" }
);

defineExpose({
  scrollToTop,
  elTableRef,
});
</script>

<style lang="scss" scoped>
@use "./style";
</style>
