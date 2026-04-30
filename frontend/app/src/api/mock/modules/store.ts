/*
 * @Author: weisheng
 * @Date: 2025-06-15 14:30:00
 * @LastEditTime: 2025-06-15 14:30:00
 * @LastEditors: weisheng
 * @Description: Pet Store - Store相关接口的mock数据
 * @FilePath: /wot-starter/src/api/mock/modules/store.ts
 */
import { defineMock } from '@alova/mock'
import { generateMockData } from '../utils/generators'

// 订单状态枚举
const ORDER_STATUS = ['placed', 'approved', 'delivered'] as const
type OrderStatus = typeof ORDER_STATUS[number]

// 生成订单对象
function generateOrder(id?: number, status?: OrderStatus) {
  const orderId = id || generateMockData.number(1, 10000)

  return {
    id: orderId,
    petId: generateMockData.number(1, 1000),
    quantity: generateMockData.number(1, 10),
    shipDate: generateMockData.datetime(generateMockData.number(1, 30)), // 1-30天后发货
    status: status || ORDER_STATUS[generateMockData.number(0, ORDER_STATUS.length - 1)],
    complete: generateMockData.boolean(),
  }
}

export default defineMock({
  // 获取库存
  '[GET]/store/inventory': () => {
    console.log('[Mock] GET /store/inventory')

    // 生成随机库存数据
    const inventory: Record<string, number> = {}

    // 为不同状态生成库存数量
    ORDER_STATUS.forEach((status) => {
      inventory[status] = generateMockData.number(0, 100)
    })

    // 添加一些额外的状态
    inventory.pending = generateMockData.number(0, 50)
    inventory.sold = generateMockData.number(0, 200)
    inventory.available = generateMockData.number(10, 300)

    return inventory
  },

  // 下单购买宠物
  '[POST]/store/order': ({ data }) => {
    console.log('[Mock] POST /store/order', data)

    // 验证必填字段
    if (!data.petId) {
      return {
        status: 400,
        body: {
          code: 400,
          message: 'Pet ID is required',
        },
      }
    }

    if (!data.quantity || data.quantity <= 0) {
      return {
        status: 400,
        body: {
          code: 400,
          message: 'Quantity must be greater than 0',
        },
      }
    }

    // 创建新订单
    const newOrder = {
      id: generateMockData.number(10001, 20000),
      petId: data.petId,
      quantity: data.quantity,
      shipDate: data.shipDate || generateMockData.datetime(generateMockData.number(1, 7)), // 默认7天内发货
      status: 'placed' as OrderStatus,
      complete: false,
    }

    return newOrder
  },

  // 根据ID获取订单
  '[GET]/store/order/{orderId}': ({ params }) => {
    console.log(`[Mock] GET /store/order/${params.orderId}`)

    const orderId = Number.parseInt(params.orderId)

    if (Number.isNaN(orderId)) {
      return {
        status: 400,
        body: {
          code: 400,
          message: 'Invalid order ID',
        },
      }
    }

    // 模拟订单不存在的情况
    if (orderId === 404) {
      return {
        status: 404,
        body: {
          code: 404,
          message: 'Order not found',
        },
      }
    }

    // 模拟无效订单ID的情况（订单ID必须在1-10之间）
    if (orderId < 1 || orderId > 10) {
      return {
        status: 400,
        body: {
          code: 400,
          message: 'Invalid ID supplied',
        },
      }
    }

    return generateOrder(orderId)
  },

  // 删除订单
  '[DELETE]/store/order/{orderId}': ({ params }) => {
    console.log(`[Mock] DELETE /store/order/${params.orderId}`)

    const orderId = Number.parseInt(params.orderId)

    if (Number.isNaN(orderId)) {
      return {
        status: 400,
        body: {
          code: 400,
          message: 'Invalid order ID',
        },
      }
    }

    // 模拟订单不存在的情况
    if (orderId === 404) {
      return {
        status: 404,
        body: {
          code: 404,
          message: 'Order not found',
        },
      }
    }

    // 模拟无效订单ID的情况
    if (orderId < 1) {
      return {
        status: 400,
        body: {
          code: 400,
          message: 'Invalid ID supplied',
        },
      }
    }

    return {
      code: 200,
      message: `Order ${orderId} deleted successfully`,
    }
  },
}, true)
