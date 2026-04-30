/*
 * @Author: weisheng
 * @Date: 2023-05-20 10:00:00
 * @LastEditTime: 2025-05-21 15:46:14
 * @LastEditors: weisheng
 * @Description: Mock数据生成工具
 * @FilePath: /lsym-cx-mini/src/api/mock/utils/generators.ts
 */

// 模拟数据生成工具函数
export const generateMockData = {
  // 生成随机ID
  id: (): number => Math.floor(Math.random() * 10000),

  // 生成随机名称
  name: (prefix = '名称'): string => `${prefix}_${Math.floor(Math.random() * 1000)}`,

  // 生成随机代码
  code: (prefix = 'CODE'): string => `${prefix}_${Math.floor(Math.random() * 1000)}`,

  // 生成随机日期
  // 可以传入天数偏移，负数表示过去的日期，正数表示未来的日期
  date: (dayOffset = 0): string => {
    const date = new Date()
    if (dayOffset !== 0) {
      date.setDate(date.getDate() + dayOffset)
    }
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
  },

  // 生成随机时间
  // 可以传入天数偏移，负数表示过去的日期，正数表示未来的日期
  datetime: (dayOffset = 0): string => {
    const date = new Date()
    if (dayOffset !== 0) {
      date.setDate(date.getDate() + dayOffset)
    }
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}:${String(date.getSeconds()).padStart(2, '0')}`
  },

  // 生成随机布尔值
  boolean: (): boolean => Math.random() > 0.5,

  // 生成随机数字
  number: (min = 0, max = 100): number => Math.floor(Math.random() * (max - min)) + min,

  // 生成随机数组
  array: <T>(generator: (index: number) => T, length = 10): T[] => {
    const result: T[] = []
    for (let i = 0; i < length; i++) {
      result.push(generator(i))
    }
    return result
  },

  // 生成基础响应对象
  baseResponse: <T>(data: T = null as unknown as T, code = 2000, msg = '操作成功') => ({
    code,
    data,
    msg,
  }),

  // 生成列表响应对象
  listResponse: <T>(data: T[] = [], total = data.length, more = false, code = 2000, msg = '操作成功') => ({
    code,
    data,
    total,
    more,
    msg,
  }),

  // 生成GCN对象
  gcn: (_index?: number) => ({
    gid: generateMockData.id(),
    code: generateMockData.code('ORG'),
    name: generateMockData.name('组织'),
  }),

  // 生成员工对象
  faEmp: (index: number) => ({
    gid: generateMockData.id(),
    code: generateMockData.code('EMP'),
    name: generateMockData.name('员工'),
    org: generateMockData.gcn(index),
  }),

  // 生成车销业务员对象
  vehSaleEmp: (index: number) => ({
    gid: generateMockData.id(),
    code: generateMockData.code('VSE'),
    name: generateMockData.name('车销业务员'),
    faEmp: generateMockData.faEmp(index),
    org: generateMockData.gcn(index),
    wms: generateMockData.gcn(index),
  }),

  // 生成权限对象
  permission: (index: number) => ({
    module: `module_${index}`,
    moduleName: `模块${index}`,
    roleId: `role_${index}`,
    state: 1,
  }),

  // 生成代码名称对象
  codeName: (index: number, prefix = '线路') => ({
    code: generateMockData.code(`LINE_${index}`),
    name: `${prefix}${index}`,
  }),

  // 生成用户对象
  user: (roleCode = '01') => ({
    permissions: generateMockData.array(generateMockData.permission, 5),
    sortLines: generateMockData.array(generateMockData.codeName, 3),
    token: `mock_token_${Date.now()}`,
    roleCode, // 添加roleCode字段：01-车销业务员，02-仓管
    vehSaleEmp: generateMockData.vehSaleEmp(0),
  }),

  // 生成商品对象
  goods: (index: number) => ({
    gid: generateMockData.id(),
    code: generateMockData.code('GOODS'),
    name: generateMockData.name('商品'),
    gdCode: generateMockData.code('GDCODE'),
    spec: `规格${index}`,
    munit: '个',
    price: generateMockData.number(1, 1000) / 100,
    qpc: generateMockData.number(1, 10),
    qpcStr: `${generateMockData.number(1, 10)}个/箱`,
    qty: generateMockData.number(1, 100),
    qtyStr: `${generateMockData.number(1, 100)}个`,
    busInvQty: generateMockData.number(1, 100),
    advUseSignQty: generateMockData.number(1, 100),
    version: 1,
  }),
  // 单据状态，可选值为：0 | 100 | 1300 | 300 | 110 | 1310
  stat: (): number => {
    const stats = [100, 1300, 300, 110, 1310]
    return stats[generateMockData.number(0, stats.length - 1)]
  },
}
