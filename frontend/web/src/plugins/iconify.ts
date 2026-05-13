/**
 * 本地注册 Iconify 图标集，实现离线显示（不再从 CDN 加载）
 */
import { addCollection } from "@iconify/vue";
import ri from "@iconify-json/ri/icons.json";
import svgSpinners from "@iconify-json/svg-spinners/icons.json";
import lineMd from "@iconify-json/line-md/icons.json";

export function initIconify(): void {
  addCollection(ri);
  addCollection(svgSpinners);
  addCollection(lineMd);
}
