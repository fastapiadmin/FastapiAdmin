/*
 * @Author: weisheng
 * @Date: 2025-06-15 14:25:00
 * @LastEditTime: 2025-06-26 21:59:38
 * @LastEditors: weisheng
 * @Description: Pet Store - Pet相关接口的mock数据
 * @FilePath: /wot-starter/src/api/mock/modules/pet.ts
 */
import { defineMock } from '@alova/mock'
import { generateMockData } from '../utils/generators'

// 宠物状态枚举
const PET_STATUS = ['available', 'pending', 'sold'] as const
type PetStatus = typeof PET_STATUS[number]

// 宠物类别
const PET_CATEGORIES = [
  { id: 1, name: 'Dogs' },
  { id: 2, name: 'Cats' },
  { id: 3, name: 'Birds' },
  { id: 4, name: 'Fish' },
  { id: 5, name: 'Reptiles' },
]

// 宠物标签
const PET_TAGS = [
  { id: 1, name: 'friendly' },
  { id: 2, name: 'playful' },
  { id: 3, name: 'calm' },
  { id: 4, name: 'energetic' },
  { id: 5, name: 'trained' },
  { id: 6, name: 'house-trained' },
]

// 生成宠物对象
function generatePet(id?: number, status?: PetStatus) {
  const petId = id || generateMockData.number(1, 10000)
  const category = PET_CATEGORIES[generateMockData.number(0, PET_CATEGORIES.length - 1)]
  const tags = generateMockData.array(() => PET_TAGS[generateMockData.number(0, PET_TAGS.length - 1)], generateMockData.number(1, 3))

  return {
    id: petId,
    category,
    name: generateMockData.name('Pet'),
    photoUrls: generateMockData.array(
      index => `https://example.com/pet/${petId}/photo${index + 1}.jpg`,
      generateMockData.number(1, 3),
    ),
    tags,
    status: status || PET_STATUS[generateMockData.number(0, PET_STATUS.length - 1)],
  }
}

export default defineMock({
  // 上传宠物图片
  '[POST]/pet/{petId}/uploadImage': ({ params, data }) => {
    console.log(`[Mock] POST /pet/${params.petId}/uploadImage`, data)

    return {
      code: 200,
      type: 'success',
      message: `Image uploaded successfully for pet ${params.petId}`,
      data: {
        petId: params.petId,
        imageUrl: `https://example.com/pet/${params.petId}/uploaded-${Date.now()}.jpg`,
      },
    }
  },

  // 添加新宠物
  '[POST]/pet': ({ data }) => {
    console.log('[Mock] POST /pet', data)

    const newPet = {
      ...data,
      id: generateMockData.number(10001, 20000),
    }

    return newPet
  },

  // 更新宠物信息
  '[PUT]/pet': ({ data }) => {
    console.log('[Mock] PUT /pet', data)

    if (!data.id) {
      return {
        status: 400,
        body: {
          code: 400,
          message: 'Pet ID is required',
        },
      }
    }

    return {
      ...data,
      updatedAt: generateMockData.datetime(),
    }
  },

  // 根据状态查找宠物
  '[GET]/pet/findByStatus': ({ query }) => {
    console.log('[Mock] GET /pet/findByStatus', query)

    const status = query.status as PetStatus
    const validStatuses = Array.isArray(status) ? status : [status]

    // 验证状态
    const invalidStatuses = validStatuses.filter(s => !PET_STATUS.includes(s as PetStatus))
    if (invalidStatuses.length > 0) {
      return {
        status: 400,
        body: {
          code: 400,
          message: `Invalid status value: ${invalidStatuses.join(', ')}`,
        },
      }
    }

    // 生成符合状态的宠物列表
    const pets = generateMockData.array(
      index => generatePet(undefined, validStatuses[index % validStatuses.length] as PetStatus),
      generateMockData.number(5, 15),
    )

    return pets
  },

  // 根据ID获取宠物
  '[GET]/pet/{petId}': ({ params }) => {
    console.log(`[Mock] GET /pet/${params.petId}`)

    const petId = Number.parseInt(params.petId)

    if (Number.isNaN(petId)) {
      return {
        status: 400,
        body: {
          code: 400,
          message: 'Invalid pet ID',
        },
      }
    }

    // 模拟宠物不存在的情况
    if (petId === 404) {
      return {
        status: 404,
        body: {
          code: 404,
          message: 'Pet not found',
        },
      }
    }

    return generatePet(petId)
  },

  // 使用表单数据更新宠物
  '[POST]/pet/{petId}': ({ params, data }) => {
    console.log(`[Mock] POST /pet/${params.petId}`, data)

    const petId = Number.parseInt(params.petId)

    if (Number.isNaN(petId)) {
      return {
        status: 400,
        body: {
          code: 400,
          message: 'Invalid pet ID',
        },
      }
    }

    // 模拟宠物不存在的情况
    if (petId === 404) {
      return {
        status: 404,
        body: {
          code: 404,
          message: 'Pet not found',
        },
      }
    }

    const updatedPet = {
      ...generatePet(petId),
      ...data,
      updatedAt: generateMockData.datetime(),
    }

    return updatedPet
  },

  // 删除宠物
  '[DELETE]/pet/{petId}': ({ params, headers }) => {
    console.log(`[Mock] DELETE /pet/${params.petId}`, headers)

    const petId = Number.parseInt(params.petId)

    if (Number.isNaN(petId)) {
      return {
        status: 400,
        body: {
          code: 400,
          message: 'Invalid pet ID',
        },
      }
    }

    // 检查API密钥
    if (!headers.api_key) {
      return {
        status: 401,
        body: {
          code: 401,
          message: 'API key is required',
        },
      }
    }

    // 模拟宠物不存在的情况
    if (petId === 404) {
      return {
        status: 404,
        body: {
          code: 404,
          message: 'Pet not found',
        },
      }
    }

    return {
      code: 200,
      message: `Pet ${petId} deleted successfully`,
    }
  },
}, true)
