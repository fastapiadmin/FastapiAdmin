import type { EChartsOption } from "@/plugins/echarts";

/** 图例位置类型 */
export type LegendPosition = "bottom" | "top" | "left" | "right";

export type SymbolType =
  | "circle"
  | "rect"
  | "roundRect"
  | "triangle"
  | "diamond"
  | "pin"
  | "arrow"
  | "none";

/** 图表主题配置 */
export interface ChartThemeConfig {
  chartHeight: string;
  fontSize: number;
  fontColor: string;
  themeColor: string;
  colors: string[];
}

/** 图表初始化选项 */
export interface UseChartOptions {
  initOptions?: EChartsOption;
  initDelay?: number;
  threshold?: number;
  autoTheme?: boolean;
}

/** 基础图表 Props 接口 */
export interface BaseChartProps {
  title?: string;
  height?: string;
  loading?: boolean;
  isEmpty?: boolean;
  colors?: string[];
}

/** 轴线显示控制接口 */
export interface AxisDisplayProps {
  showAxisLabel?: boolean;
  showAxisLine?: boolean;
  showSplitLine?: boolean;
}

/** 交互显示控制接口 */
export interface InteractionProps {
  showTooltip?: boolean;
  showLegend?: boolean;
  legendPosition?: LegendPosition;
}

/** 柱状图数据项接口 */
export interface BarDataItem {
  name: string;
  data: number[];
  barWidth?: string | number;
  stack?: string;
}

/** 柱状图 Props 接口 */
export interface BarChartProps extends BaseChartProps, AxisDisplayProps, InteractionProps {
  data: number[] | BarDataItem[];
  xAxisData?: string[];
  barWidth?: string | number;
  stack?: boolean;
  borderRadius?: number | number[];
}

/** 折线图数据项接口 */
export interface LineDataItem {
  name: string;
  data: number[];
  lineWidth?: number;
  showAreaColor?: boolean;
  areaStyle?: { startOpacity?: number; endOpacity?: number; custom?: any };
  smooth?: boolean;
  symbol?: SymbolType;
  symbolSize?: number;
}

/** 折线图 Props 接口 */
export interface LineChartProps extends BaseChartProps, AxisDisplayProps, InteractionProps {
  data: number[] | LineDataItem[];
  xAxisData?: string[];
  lineWidth?: number;
  showAreaColor?: boolean;
  smooth?: boolean;
  symbol?: SymbolType;
  symbolSize?: number;
  animationDelay?: number;
}

/** 雷达图数据项接口 */
export interface RadarDataItem {
  name: string;
  value: number[];
}

/** 雷达图 Props 接口 */
export interface RadarChartProps extends BaseChartProps, InteractionProps {
  indicator?: Array<{ name: string; max: number }>;
  data?: RadarDataItem[];
}

/** 饼图/环形图数据项接口 */
export interface PieDataItem {
  value: number;
  name: string;
}

/** 环形图 Props 接口 */
export interface RingChartProps extends BaseChartProps, InteractionProps {
  data: PieDataItem[];
  radius?: string[];
  borderRadius?: number;
  centerText?: string;
  showLabel?: boolean;
}

/** K线图数据项接口 */
export interface KLineDataItem {
  time: string;
  open: number;
  close: number;
  high: number;
  low: number;
}

/** K线图 Props 接口 */
export interface KLineChartProps extends BaseChartProps {
  data?: KLineDataItem[];
  showDataZoom?: boolean;
  dataZoomStart?: number;
  dataZoomEnd?: number;
}

/** 散点图数据项接口 */
export interface ScatterDataItem {
  value: number[];
}

/** 散点图 Props 接口 */
export interface ScatterChartProps extends BaseChartProps, AxisDisplayProps, InteractionProps {
  data?: ScatterDataItem[];
  symbolSize?: number;
}

/** 双柱对比图 Props 接口 */
export interface DualBarCompareChartProps extends BaseChartProps {
  topData: number[];
  bottomData: number[];
  xAxisData: string[];
  topColor?: string;
  bottomColor?: string;
  barWidth?: number;
}

/** 地图图表 Props 接口 */
export interface MapChartProps extends BaseChartProps {
  mapData?: any[];
  selectedRegion?: string;
  showLabels?: boolean;
  showScatter?: boolean;
}

/** 双向堆叠柱状图 Props 接口（人口金字塔样式） */
export interface BidirectionalBarChartProps
  extends BaseChartProps, AxisDisplayProps, InteractionProps {
  positiveData: number[];
  negativeData: number[];
  xAxisData?: string[];
  positiveName?: string;
  negativeName?: string;
  barWidth?: string | number;
  yAxisMin?: number;
  yAxisMax?: number;
  showDataLabel?: boolean;
  positiveBorderRadius?: number | number[];
  negativeBorderRadius?: number | number[];
}

/** 图表配置生成器函数类型 */
export type ChartOptionGenerator = () => EChartsOption;

/** 图表事件回调类型 */
export type ChartEventCallback = (params: any) => void;

/** 图表错误信息接口 */
export interface ChartError {
  code: string;
  message: string;
  details?: any;
}
