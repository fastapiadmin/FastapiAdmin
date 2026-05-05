/**
 * 通用工具函数模块
 *
 * 提供项目中常用的通用工具函数，包括：
 * - 问候语生成
 * - 日期范围处理
 * - 树形结构转换
 * - 对象深拷贝
 * - 空值判断
 * - Blob 格式验证
 *
 * @module utils/common
 */

/**
 * 根据当前时间生成问候语
 *
 * 根据当前小时返回不同的问候语，支持中文问候和特殊时段的温馨提示
 *
 * @returns {string} 问候语字符串
 *
 * @example
 * ```typescript
 * const greeting = greetings();
 * console.log(greeting); // 输出："上午好！" 或其他时段的问候语
 * ```
 */
export function greetings(): string {
  const currentDate = new Date();
  const hours = currentDate.getHours();

  if (hours >= 6 && hours < 8) {
    return "晨起披衣出草堂，轩窗已自喜微凉🌅！";
  } else if (hours >= 8 && hours < 12) {
    return "上午好！";
  } else if (hours >= 12 && hours < 14) {
    return "中午好！";
  } else if (hours >= 14 && hours < 18) {
    return "下午好！";
  } else if (hours >= 18 && hours < 24) {
    return "晚上好！";
  } else {
    return "偷偷向银河要了一把碎星，只等你闭上眼睛撒入你的梦中，晚安🌛！";
  }
}

/**
 * 获取日期范围内的所有日期
 *
 * 根据起始日期和结束日期，生成期间所有日期的字符串数组
 * 支持跨月份和跨年度的日期范围
 *
 * @param {string | number | Date} startDate - 起始日期
 * @param {string | number | Date} endDate - 结束日期
 * @returns {string[]} 日期字符串数组，格式为 YYYY-MM-DD
 *
 * @example
 * ```typescript
 * const dates = getRangeDate('2024-01-30', '2024-02-02');
 * // 输出：['2024-01-30', '2024-01-31', '2024-02-01', '2024-02-02']
 * ```
 */
export function getRangeDate(
  startDate: string | number | Date,
  endDate: string | number | Date
): string[] {
  const targetArr: string[] = [];
  const start = new Date(startDate);
  const end = new Date(endDate);

  const startDateInfo = {
    year: start.getFullYear(),
    month: start.getMonth() + 1,
    day: start.getDate(),
  };

  const endDateInfo = {
    year: end.getFullYear(),
    month: end.getMonth() + 1,
    day: end.getDate(),
  };

  if (startDateInfo.year === endDateInfo.year) {
    if (startDateInfo.month !== endDateInfo.month) {
      // 同年不同月
      const startMax = new Date(startDateInfo.year, startDateInfo.month, 0).getDate();
      const endNum = startMax - startDateInfo.day + endDateInfo.day;

      for (let i = startDateInfo.day; i <= startDateInfo.day + endNum; i++) {
        if (i > startMax) {
          targetArr.push(
            `${endDateInfo.year}-${
              endDateInfo.month < 10 ? "0" + endDateInfo.month : endDateInfo.month
            }-${i - startMax < 10 ? "0" + (i - startMax) : i - startMax}`
          );
        } else {
          targetArr.push(
            `${startDateInfo.year}-${
              startDateInfo.month < 10 ? "0" + startDateInfo.month : startDateInfo.month
            }-${i < 10 ? "0" + i : i}`
          );
        }
      }
    } else {
      // 同年同月
      for (let i = startDateInfo.day; i <= endDateInfo.day; i++) {
        targetArr.push(
          `${startDateInfo.year}-${
            startDateInfo.month < 10 ? "0" + startDateInfo.month : startDateInfo.month
          }-${i < 10 ? "0" + i : i}`
        );
      }
    }
  } else {
    // 不同年
    const startMax = new Date(startDateInfo.year, startDateInfo.month, 0).getDate();
    const endNum = startMax - startDateInfo.day + endDateInfo.day;

    for (let i = startDateInfo.day; i <= startDateInfo.day + endNum; i++) {
      if (i > startMax) {
        targetArr.push(
          `${endDateInfo.year}-${
            endDateInfo.month < 10 ? "0" + endDateInfo.month : endDateInfo.month
          }-${i - startMax < 10 ? "0" + (i - startMax) : i - startMax}`
        );
      } else {
        targetArr.push(
          `${startDateInfo.year}-${
            startDateInfo.month < 10 ? "0" + startDateInfo.month : startDateInfo.month
          }-${i < 10 ? "0" + i : i}`
        );
      }
    }
  }

  return targetArr;
}

/**
 * 将扁平列表转换为树形结构
 *
 * 通过 parent_id 字段将扁平数组转换为嵌套的树形结构
 * 保留原始数据的所有字段
 *
 * @param {any[]} list - 扁平列表数据，每个项必须包含 id 和 parent_id 字段
 * @returns {any[]} 树形结构数组
 *
 * @example
 * ```typescript
 * const list = [
 *   { id: 1, name: '节点1', parent_id: null },
 *   { id: 2, name: '节点2', parent_id: 1 },
 * ];
 * const tree = listToTree(list);
 * // 输出：[{ id: 1, name: '节点1', parent_id: null, children: [{ id: 2, name: '节点2', parent_id: 1 }] }]
 * ```
 */
export function listToTree(list: any[]): any[] {
  const map: { [key: string | number]: any } = {};

  // 创建映射表，保留每个节点的 parent_id 等原始字段
  list.forEach((item) => {
    map[item.id] = { ...item };
  });

  const tree: any[] = [];

  list.forEach((item) => {
    const parentId = item.parent_id;

    if (parentId && map[parentId]) {
      // 将当前节点加入其父节点的 children 数组中
      if (!map[parentId].children) {
        map[parentId].children = [];
      }
      map[parentId].children.push(map[item.id]);
    } else if (parentId === null || parentId === undefined) {
      // 根节点
      tree.push(map[item.id]);
    }
  });

  return tree;
}

/**
 * 格式化树形结构为级联选择器格式
 *
 * 将树形数据转换为适合 Element Plus Cascader 组件使用的格式
 * 包含 value、label、disabled 和 children 字段
 *
 * @param {any[]} nodes - 树形结构数据
 * @returns {any[]} 格式化后的树形结构
 *
 * @example
 * ```typescript
 * const nodes = [{ id: 1, name: '部门1', status: true, children: [...] }];
 * const formatted = formatTree(nodes);
 * // 输出：[{ value: 1, label: '部门1', disabled: false, children: [...] }]
 * ```
 */
export function formatTree(nodes: any[]): any[] {
  return nodes.map((node) => {
    const formattedNode: any = {
      value: node.id,
      label: node.name,
      disabled: node.status === false || String(node.status) === "false",
    };

    if (node.children && node.children.length > 0) {
      formattedNode.children = formatTree(node.children);
    }

    return formattedNode;
  });
}

/**
 * 深拷贝对象
 *
 * 使用 JSON 序列化和反序列化实现对象的深拷贝
 * 注意：此方法不支持函数、Symbol、循环引用等特殊类型
 *
 * @param {any} obj - 需要拷贝的对象
 * @returns {any} 拷贝后的新对象
 *
 * @example
 * ```typescript
 * const original = { a: 1, b: { c: 2 } };
 * const copy = cloneDeep(original);
 * copy.b.c = 3; // 不影响原对象
 * ```
 */
export function cloneDeep(obj: any): any {
  return JSON.parse(JSON.stringify(obj));
}

/**
 * 判断字符串是否为空
 *
 * 检查字符串是否为 undefined、null 或空字符串
 *
 * @param {string | null | undefined} obj - 需要检查的字符串
 * @returns {boolean} 是否为空
 *
 * @example
 * ```typescript
 * isEmpty('');      // true
 * isEmpty(null);    // true
 * isEmpty(undefined); // true
 * isEmpty('hello'); // false
 * ```
 */
export function isEmpty(obj: string | null | undefined): boolean {
  return obj === undefined || obj === null || obj === "";
}

/**
 * 验证数据是否为 Blob 格式
 *
 * 通过检查 Content-Type 是否为 application/json 来判断
 *
 * @param {Blob} data - 需要验证的数据
 * @returns {boolean} 是否为 Blob 格式
 *
 * @example
 * ```typescript
 * const blob = new Blob(['test'], { type: 'text/plain' });
 * blobValidate(blob); // true
 * ```
 */
export function blobValidate(data: Blob): boolean {
  return data.type !== "application/json";
}
