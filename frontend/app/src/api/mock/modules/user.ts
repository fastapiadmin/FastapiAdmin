/*
 * @Author: weisheng
 * @Date: 2025-06-15 14:35:00
 * @LastEditTime: 2025-06-27 09:43:25
 * @LastEditors: weisheng
 * @Description: Pet Store - User相关接口的mock数据
 * @FilePath: /wot-starter/src/api/mock/modules/user.ts
 */
import { defineMock } from '@alova/mock'
import { generateMockData } from '../utils/generators'

// 用户状态枚举
const USER_STATUS = [0, 1, 2] // 0: 离线, 1: 在线, 2: 忙碌
type UserStatus = typeof USER_STATUS[number]

// 生成用户对象
function generateUser(username?: string, status?: UserStatus) {
  const baseUsername = username || generateMockData.name('user').toLowerCase()

  return {
    id: generateMockData.number(1, 10000),
    username: baseUsername,
    firstName: generateMockData.name('First'),
    lastName: generateMockData.name('Last'),
    email: `${baseUsername}@example.com`,
    password: 'password123', // 在实际应用中不应该返回密码
    phone: `1${generateMockData.number(1000000000, 9999999999)}`,
    userStatus: CommonUtil.isDef(status) ? status : USER_STATUS[generateMockData.number(0, USER_STATUS.length - 1)],
  }
}

// 模拟用户数据库
const mockUsers = generateMockData.array(index => generateUser(`user${index + 1}`), 10)

export default defineMock({
  // 批量创建用户（数组输入）
  '[POST]/user/createWithArray': ({ data }) => {
    console.log('[Mock] POST /user/createWithArray', data)

    if (!Array.isArray(data)) {
      return {
        status: 400,
        body: {
          code: 400,
          message: 'Input should be an array of users',
        },
      }
    }

    // 验证每个用户对象
    for (const user of data) {
      if (!user.username) {
        return {
          status: 400,
          body: {
            code: 400,
            message: 'Username is required for all users',
          },
        }
      }
    }

    return {
      code: 200,
      message: `Successfully created ${data.length} users`,
    }
  },

  // 批量创建用户（列表输入）
  '[POST]/user/createWithList': ({ data }) => {
    console.log('[Mock] POST /user/createWithList', data)

    if (!Array.isArray(data)) {
      return {
        status: 400,
        body: {
          code: 400,
          message: 'Input should be a list of users',
        },
      }
    }

    // 验证每个用户对象
    for (const user of data) {
      if (!user.username) {
        return {
          status: 400,
          body: {
            code: 400,
            message: 'Username is required for all users',
          },
        }
      }
    }

    return {
      code: 200,
      message: `Successfully created ${data.length} users from list`,
    }
  },

  // 用户登录
  '[GET]/user/login': ({ query }) => {
    console.log('[Mock] GET /user/login', query)

    const { username, password } = query

    if (!username || !password) {
      return {
        status: 400,
        body: {
          code: 400,
          message: 'Username and password are required',
        },
      }
    }

    // 模拟登录验证
    if (username === 'admin' && password === 'admin') {
      return {
        code: 200,
        message: 'logged in user session',
        token: `mock_token_${Date.now()}`,
        expiresIn: 3600, // 1小时
        user: generateUser('admin', 1),
      }
    }

    // 模拟用户名密码错误
    if (username === 'invalid' || password === 'invalid') {
      return {
        status: 400,
        body: {
          code: 400,
          message: 'Invalid username/password supplied',
        },
      }
    }

    // 默认成功登录
    return {
      code: 200,
      message: 'logged in user session',
      token: `mock_token_${Date.now()}`,
      expiresIn: 3600,
      user: generateUser(username as string, 1),
    }
  },

  // 用户登出
  '[GET]/user/logout': () => {
    console.log('[Mock] GET /user/logout')

    return {
      code: 200,
      message: 'ok',
    }
  },

  // 根据用户名获取用户
  '[GET]/user/{username}': ({ params }) => {
    console.log(`[Mock] GET /user/${params.username}`)

    const username = params.username

    if (!username) {
      return {
        status: 400,
        body: {
          code: 400,
          message: 'Username is required',
        },
      }
    }

    // 模拟用户不存在的情况
    if (username === 'notfound') {
      return {
        status: 404,
        body: {
          code: 404,
          message: 'User not found',
        },
      }
    }

    // 从模拟数据库中查找用户
    const existingUser = mockUsers.find(user => user.username === username)
    if (existingUser) {
      return existingUser
    }

    // 生成新用户
    return generateUser(username)
  },

  // 更新用户信息
  '[PUT]/user/{username}': ({ params, data }) => {
    console.log(`[Mock] PUT /user/${params.username}`, data)

    const username = params.username

    if (!username) {
      return {
        status: 400,
        body: {
          code: 400,
          message: 'Username is required',
        },
      }
    }

    // 模拟用户不存在的情况
    if (username === 'notfound') {
      return {
        status: 404,
        body: {
          code: 404,
          message: 'User not found',
        },
      }
    }

    // 更新用户信息
    const updatedUser = {
      ...generateUser(username),
      ...data,
      username, // 确保用户名不被修改
      updatedAt: generateMockData.datetime(),
    }

    return updatedUser
  },

  // 删除用户
  '[DELETE]/user/{username}': ({ params }) => {
    console.log(`[Mock] DELETE /user/${params.username}`)

    const username = params.username

    if (!username) {
      return {
        status: 400,
        body: {
          code: 400,
          message: 'Username is required',
        },
      }
    }

    // 模拟用户不存在的情况
    if (username === 'notfound') {
      return {
        status: 404,
        body: {
          code: 404,
          message: 'User not found',
        },
      }
    }

    return {
      code: 200,
      message: `User ${username} deleted successfully`,
    }
  },

  // 创建用户
  '[POST]/user': ({ data }) => {
    console.log('[Mock] POST /user', data)

    if (!data.username) {
      return {
        status: 400,
        body: {
          code: 400,
          message: 'Username is required',
        },
      }
    }

    // 检查用户名是否已存在
    const existingUser = mockUsers.find(user => user.username === data.username)
    if (existingUser) {
      return {
        status: 409,
        body: {
          code: 409,
          message: 'Username already exists',
        },
      }
    }

    // 创建新用户
    const newUser = {
      ...generateUser(),
      ...data,
      id: generateMockData.number(20001, 30000),
      createdAt: generateMockData.datetime(),
    }

    return newUser
  },
}, true)
