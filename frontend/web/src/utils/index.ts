/**
 * Check if an element has a class
 * @param {HTMLElement} ele
 * @param {string} cls
 * @returns {boolean}
 */
export function hasClass(ele: HTMLElement, cls: string) {
  return !!ele.className.match(new RegExp('(\\s|^)' + cls + '(\\s|$)'));
}

/**
 * Add class to element
 * @param {HTMLElement} ele
 * @param {string} cls
 */
export function addClass(ele: HTMLElement, cls: string) {
  if (!hasClass(ele, cls)) ele.className += ' ' + cls;
}

/**
 * Remove class from element
 * @param {HTMLElement} ele
 * @param {string} cls
 */
export function removeClass(ele: HTMLElement, cls: string) {
  if (hasClass(ele, cls)) {
    const reg = new RegExp('(\\s|^)' + cls + '(\\s|$)');
    ele.className = ele.className.replace(reg, ' ');
  }
}

/**
 * 判断是否是外部链接
 *
 * @param {string} path
 * @returns {Boolean}
 */
export function isExternal(path: string) {
  const isExternal = /^(https?:|http?:|mailto:|tel:)/.test(path);
  return isExternal;
}

/**
 * 格式化增长率，保留两位小数 ，并且去掉末尾的0  取绝对值
 *
 * @param growthRate
 * @returns
 */
export function formatGrowthRate(growthRate: number) {
  if (growthRate === 0) {
    return '-';
  }

  const formattedRate = Math.abs(growthRate * 100)
    .toFixed(2)
    .replace(/\.?0+$/, '');
  return formattedRate + '%';
}

//表单生成相关

export function isNumberStr(str: string): boolean {
  return /^[+-]?(0|([1-9]\d*))(\.\d+)?$/g.test(str);
}

export function titleCase(str: string): string {
  return str.replace(/([A-Z])/g, ' $1').replace(/^./, function (str) {
    return str.toUpperCase();
  });
}

export function makeMap(str: string, expectsLowerCase?: boolean) {
  const map = Object.create(null);
  const list = str.split(',');
  for (let i = 0; i < list.length; i++) {
    map[list[i]] = true;
  }
  return expectsLowerCase ? (val: string) => map[val.toLowerCase()] : (val: string) => map[val];
}

export const beautifierConf = {
  html: {
    indent_size: '2',
    indent_char: ' ',
    max_preserve_newlines: '-1',
    preserve_newlines: false,
    keep_array_indentation: false,
    break_chained_methods: false,
    indent_scripts: 'separate',
    brace_style: 'end-expand',
    space_before_conditional: true,
    unescape_strings: false,
    jslint_happy: false,
    end_with_newline: true,
    wrap_line_length: '110',
    indent_inner_html: true,
    comma_first: false,
    e4x: true,
    indent_empty_lines: true,
  },
  js: {
    indent_size: '2',
    indent_char: ' ',
    max_preserve_newlines: '-1',
    preserve_newlines: false,
    keep_array_indentation: false,
    break_chained_methods: false,
    indent_scripts: 'normal',
    brace_style: 'end-expand',
    space_before_conditional: true,
    unescape_strings: false,
    jslint_happy: true,
    end_with_newline: true,
    wrap_line_length: '110',
    indent_inner_html: true,
    comma_first: false,
    e4x: true,
    indent_empty_lines: true,
  },
};

/**
 * Utils 工具函数统一导出
 * 提供向后兼容性和便捷导入
 *
 * @module utils/index
 * @author Fastapi Admin Team
 */

// UI 相关
export * from './ui';

// 路由相关
export * from './router';

// 路由导航相关
export * from './navigation';

// 系统管理相关
export * from './sys';

// 常量定义相关
export * from './constants';

// 存储相关
export * from './storage';

// HTTP 相关
export * from './http';

// 表单相关
export * from './form';

// socket 相关
export * from './socket';
