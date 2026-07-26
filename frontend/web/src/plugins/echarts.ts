/**
 * ECharts 插件配置
 *
 * 按需导入 ECharts 图表和组件，减小打包体积。
 * 只注册项目中实际使用的图表类型和组件。
 *
 * @module plugins/echarts
 * @author FastapiAdmin Team
 */

// ECharts 按需导入配置
import * as echarts from "echarts/core";

// 导入图表类型（按需引入，仅导入项目中实际使用的）
import {
  BarChart,
  LineChart,
  PieChart,
  ScatterChart,
  RadarChart,
  MapChart,
  CandlestickChart,
  GaugeChart,
} from "echarts/charts";

// 导入组件（按需引入，仅导入项目中实际使用的）
import {
  TooltipComponent,
  GridComponent,
  LegendComponent,
  DataZoomComponent,
  GeoComponent,
  TitleComponent,
} from "echarts/components";

// 导入渲染器
import { CanvasRenderer } from "echarts/renderers";

// 注册必要的组件（按需注册）
echarts.use([
  // 图表类型
  BarChart,
  LineChart,
  PieChart,
  ScatterChart,
  RadarChart,
  MapChart,
  CandlestickChart,
  GaugeChart,

  // 组件（仅保留实际使用的）
  TooltipComponent,
  GridComponent,
  LegendComponent,
  DataZoomComponent,
  GeoComponent,
  TitleComponent,

  // 渲染器
  CanvasRenderer,
]);

// 导出 echarts 实例和类型
export { echarts };
export type { EChartsOption, BarSeriesOption } from "echarts";

// 导出常用的图形工具
export const graphic = echarts.graphic;
