/**
 * 通用工具函数模块
 *
 * 提供 DOM 操作、字符串处理、数字格式化等通用工具函数
 *
 * @module utils/common/helper
 */

/**
 * 判断 DOM 元素是否包含指定的 CSS 类名
 *
 * @param {HTMLElement} ele - 目标 DOM 元素
 * @param {string} cls - 要检查的类名
 * @returns {boolean} 是否包含该类名
 *
 * @example
 * ```typescript
 * const element = document.getElementById('myDiv');
 * const hasClass = hasClass(element, 'active');
 * ```
 */
export function hasClass(ele: HTMLElement, cls: string): boolean {
  return !!ele.className.match(new RegExp("(\\s|^)" + cls + "(\\s|$)"));
}

/**
 * 为 DOM 元素添加 CSS 类名
 *
 * 如果元素已包含该类名，则不会重复添加
 *
 * @param {HTMLElement} ele - 目标 DOM 元素
 * @param {string} cls - 要添加的类名
 *
 * @example
 * ```typescript
 * const element = document.getElementById('myDiv');
 * addClass(element, 'active');
 * ```
 */
export function addClass(ele: HTMLElement, cls: string): void {
  if (!hasClass(ele, cls)) {
    ele.className += " " + cls;
  }
}

/**
 * 从 DOM 元素移除 CSS 类名
 *
 * @param {HTMLElement} ele - 目标 DOM 元素
 * @param {string} cls - 要移除的类名
 *
 * @example
 * ```typescript
 * const element = document.getElementById('myDiv');
 * removeClass(element, 'active');
 * ```
 */
export function removeClass(ele: HTMLElement, cls: string): void {
  if (hasClass(ele, cls)) {
    const reg = new RegExp("(\\s|^)" + cls + "(\\s|$)");
    ele.className = ele.className.replace(reg, " ");
  }
}

/**
 * 判断是否是外部链接
 *
 * 通过检查 URL 是否以 http://、https://、mailto: 或 tel: 开头来判断
 *
 * @param {string} path - 要检查的路径或 URL
 * @returns {boolean} 是否为外部链接
 *
 * @example
 * ```typescript
 * isExternal('https://example.com'); // true
 * isExternal('/dashboard'); // false
 * isExternal('mailto:info@example.com'); // true
 * ```
 */
export function isExternal(path: string): boolean {
  return /^(https?:|http?:|mailto:|tel:)/.test(path);
}

/**
 * 格式化增长率
 *
 * 将增长率转换为百分比格式，保留两位小数并去掉末尾的零，取绝对值
 *
 * @param {number} growthRate - 增长率（小数形式）
 * @returns {string} 格式化后的增长率字符串
 *
 * @example
 * ```typescript
 * formatGrowthRate(0.1234); // '12.34%'
 * formatGrowthRate(-0.05); // '5%'
 * formatGrowthRate(0); // '-'
 * ```
 */
export function formatGrowthRate(growthRate: number): string {
  if (growthRate === 0) {
    return "-";
  }

  const formattedRate = Math.abs(growthRate * 100)
    .toFixed(2)
    .replace(/\.?0+$/, "");
  return formattedRate + "%";
}

/**
 * 判断字符串是否为有效数字格式
 *
 * 支持整数、小数、正负号
 *
 * @param {string} str - 要检查的字符串
 * @returns {boolean} 是否为有效数字格式
 *
 * @example
 * ```typescript
 * isNumberStr('123'); // true
 * isNumberStr('-123.45'); // true
 * isNumberStr('abc'); // false
 * ```
 */
export function isNumberStr(str: string): boolean {
  return /^[+-]?(0|([1-9]\d*))(\.\d+)?$/g.test(str);
}

/**
 * 将字符串转换为标题格式
 *
 * 在每个大写字母前添加空格，并将首字母转为大写
 *
 * @param {string} str - 要转换的字符串
 * @returns {string} 标题格式的字符串
 *
 * @example
 * ```typescript
 * titleCase('helloWorld'); // 'Hello World'
 * titleCase('myNameIsJohn'); // 'My Name Is John'
 * ```
 */
export function titleCase(str: string): string {
  return str.replace(/([A-Z])/g, " $1").replace(/^./, (s) => s.toUpperCase());
}

/**
 * 创建一个映射函数
 *
 * 将逗号分隔的字符串转换为一个查找函数，用于快速判断值是否在列表中
 *
 * @param {string} str - 逗号分隔的字符串列表
 * @param {boolean} [expectsLowerCase] - 是否将输入值转为小写后再比较
 * @returns {(val: string) => boolean} 映射函数
 *
 * @example
 * ```typescript
 * const isEventTag = makeMap('click,focus,blur');
 * isEventTag('click'); // true
 * isEventTag('mouseover'); // false
 * ```
 */
export function makeMap(str: string, expectsLowerCase?: boolean): (val: string) => boolean {
  const map: Record<string, boolean> = Object.create(null);
  const list = str.split(",");
  for (let i = 0; i < list.length; i++) {
    map[list[i]] = true;
  }
  return expectsLowerCase
    ? (val: string) => Boolean(map[val.toLowerCase()])
    : (val: string) => Boolean(map[val]);
}

/**
 * 代码美化器配置
 *
 * 包含 HTML 和 JavaScript 代码的格式化配置
 *
 * @example
 * ```typescript
 * import { beautifierConf } from '@/utils/common/helper';
 * // 使用 beautifierConf.html 或 beautifierConf.js 配置代码格式化
 * ```
 */
export const beautifierConf = {
  /** HTML 代码美化配置 */
  html: {
    indent_size: "2",
    indent_char: " ",
    max_preserve_newlines: "-1",
    preserve_newlines: false,
    keep_array_indentation: false,
    break_chained_methods: false,
    indent_scripts: "separate",
    brace_style: "end-expand",
    space_before_conditional: true,
    unescape_strings: false,
    jslint_happy: false,
    end_with_newline: true,
    wrap_line_length: "110",
    indent_inner_html: true,
    comma_first: false,
    e4x: true,
    indent_empty_lines: true,
  },
  /** JavaScript 代码美化配置 */
  js: {
    indent_size: "2",
    indent_char: " ",
    max_preserve_newlines: "-1",
    preserve_newlines: false,
    keep_array_indentation: false,
    break_chained_methods: false,
    indent_scripts: "normal",
    brace_style: "end-expand",
    space_before_conditional: true,
    unescape_strings: false,
    jslint_happy: true,
    end_with_newline: true,
    wrap_line_length: "110",
    indent_inner_html: true,
    comma_first: false,
    e4x: true,
    indent_empty_lines: true,
  },
};
