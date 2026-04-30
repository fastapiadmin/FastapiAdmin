/*
 * @Author: weisheng
 * @Date: 2025-04-17 16:21:36
 * @LastEditTime: 2025-06-15 22:48:04
 * @LastEditors: weisheng
 * @Description: Mock适配器配置 - 集成所有模块的mock数据
 * @FilePath: /wot-starter/src/api/mock/mockAdapter.ts
 * 记得注释
 */
import { uniappMockResponse, uniappRequestAdapter } from '@alova/adapter-uniapp'
import { createAlovaMockAdapter } from '@alova/mock'

// 导入所有mock模块
import commonMocks from './modules/common'
import petMocks from './modules/pet'
import storeMocks from './modules/store'
import userMocks from './modules/user'

// 合并所有mock定义
const allMocks = [
  commonMocks,
  petMocks,
  storeMocks,
  userMocks,
]

// 创建mock适配器
const mockAdapter = createAlovaMockAdapter(allMocks, {
  // 使用uniapp请求适配器处理非mock请求
  httpAdapter: uniappRequestAdapter,

  // 使用uniapp mock响应适配器
  onMockResponse: uniappMockResponse,

  // 根据环境变量启用/禁用mock
  enable: true,

  // 添加延迟以模拟网络延迟 (200-600ms)
  delay: Math.random() * 400 + 200,

  // 在开发环境下打印mock请求日志
  mockRequestLogger: import.meta.env.MODE === 'development',
  // 路径匹配模式 - 使用完整路径匹配
  matchMode: 'pathname',
})

export default mockAdapter
