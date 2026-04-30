---
outline: "deep"
title: API 文档说明
---
# API 文档说明

## 📚API 文档概述

FastapiAdmin 项目提供了完善的 API 文档，便于开发者了解和使用系统提供的接口。本文档将详细介绍如何使用和调用这些 API。

## 🔧后端 API 文档

### 1. 访问方式

后端 API 文档基于 FastAPI 自动生成，支持 Swagger 和 Redoc 两种格式：

- **Swagger UI**：<http://localhost:8001/api/v1/docs>（本地开发环境）
- **Redoc**：<http://localhost:8001/api/v1/redoc>（本地开发环境）
- **在线演示**：<https://service.fastapiadmin.com/api/v1/docs>（生产环境）

### 2. 使用方法

#### 2.1 认证登录

1. 打开 Swagger UI 文档页面
2. 点击页面右上角的 "Authorize" 按钮
3. 在弹出的对话框中输入用户名和密码
4. 点击 "Authorize" 按钮完成认证
5. 认证成功后，所有 API 调用都会自动携带认证信息

#### 2.2 接口测试

1. 在 Swagger UI 中找到需要测试的接口
2. 点击接口名称展开详细信息
3. 点击 "Try it out" 按钮
4. 填写必要的参数
5. 点击 "Execute" 按钮执行请求
6. 查看响应结果

### 3. API 接口分类

后端 API 接口主要分为以下几类：

- **系统管理**：用户、角色、菜单、部门、岗位等管理接口
- **监控管理**：在线用户、服务器监控、缓存监控等接口
- **任务管理**：定时任务管理接口
- **日志管理**：操作日志查询接口
- **开发工具**：代码生成、表单构建等接口

## 📱前端 API 调用

### 1. 前端 API 封装

前端项目使用 TypeScript 封装了 API 调用，主要位于 `frontend/src/api` 目录下，按模块分类组织：

```
frontend/src/api/
├── module_example/    # 示例模块
│   └── demo.ts
├── module_monitor/    # 监控模块
│   ├── cache.ts
│   ├── online.ts
│   └── server.ts
└── module_system/     # 系统模块
    ├── auth.ts
    ├── dept.ts
    ├── dict.ts
    ├── log.ts
    ├── menu.ts
    ├── notice.ts
    ├── params.ts
    ├── role.ts
    └── user.ts
```

### 2. API 调用示例

#### 2.1 导入 API 模块

```typescript
import { authApi } from '@/api/module_system/auth';
import { userApi } from '@/api/module_system/user';
```

#### 2.2 调用登录接口

```typescript
import { authApi } from '@/api/module_system/auth';
import { useUserStore } from '@/store/modules/user.store';

const userStore = useUserStore();

const login = async (username: string, password: string) => {
  try {
    const res = await authApi.login({
      username,
      password
    });
    
    // 保存 token
    userStore.setToken(res.data.token);
    
    // 获取用户信息
    await userStore.getUserInfo();
    
    // 跳转到首页
    router.push('/');
  } catch (error) {
    console.error('登录失败：', error);
  }
};
```

#### 2.3 调用用户管理接口

```typescript
import { userApi } from '@/api/module_system/user';

// 获取用户列表
const getUserList = async () => {
  try {
    const res = await userApi.getList({
      page: 1,
      pageSize: 10,
      username: 'admin'
    });
    console.log('用户列表：', res.data);
  } catch (error) {
    console.error('获取用户列表失败：', error);
  }
};

// 获取用户详情
const getUserDetail = async (userId: number) => {
  try {
    const res = await userApi.getDetail(userId);
    console.log('用户详情：', res.data);
  } catch (error) {
    console.error('获取用户详情失败：', error);
  }
};

// 创建用户
const createUser = async (userData: any) => {
  try {
    const res = await userApi.create(userData);
    console.log('创建用户成功：', res.data);
  } catch (error) {
    console.error('创建用户失败：', error);
  }
};

// 更新用户
const updateUser = async (userId: number, userData: any) => {
  try {
    const res = await userApi.update(userId, userData);
    console.log('更新用户成功：', res.data);
  } catch (error) {
    console.error('更新用户失败：', error);
  }
};

// 删除用户
const deleteUser = async (userId: number) => {
  try {
    const res = await userApi.delete(userId);
    console.log('删除用户成功：', res.data);
  } catch (error) {
    console.error('删除用户失败：', error);
  }
};
```

## 📱FastApp 移动端 API 调用

### 1. 移动端 API 封装

FastApp 移动端项目同样封装了 API 调用，主要位于 `src/api` 目录下：

```
FastApp/src/api/
├── auth.ts       # 认证相关接口
├── file.ts       # 文件相关接口
└── user.ts       # 用户相关接口
```

### 2. API 调用示例

#### 2.1 导入 API 模块

```typescript
import { authApi } from '@/api/auth';
import { userApi } from '@/api/user';
```

#### 2.2 调用登录接口

```typescript
import { authApi } from '@/api/auth';
import { useUserStore } from '@/store/modules/user.store';

const userStore = useUserStore();

const login = async (username: string, password: string) => {
  try {
    const res = await authApi.login({
      username,
      password
    });
    
    // 保存 token
    userStore.setToken(res.data.token);
    
    // 获取用户信息
    await userStore.getUserInfo();
    
    // 跳转到首页
    uni.switchTab({ url: '/pages/index/index' });
  } catch (error) {
    console.error('登录失败：', error);
  }
};
```

#### 2.3 调用用户信息接口

```typescript
import { userApi } from '@/api/user';

// 获取用户信息
const getUserInfo = async () => {
  try {
    const res = await userApi.getUserInfo();
    console.log('用户信息：', res.data);
    return res.data;
  } catch (error) {
    console.error('获取用户信息失败：', error);
    return null;
  }
};

// 更新用户信息
const updateUserInfo = async (userData: any) => {
  try {
    const res = await userApi.updateUserInfo(userData);
    console.log('更新用户信息成功：', res.data);
    return true;
  } catch (error) {
    console.error('更新用户信息失败：', error);
    return false;
  }
};
```

## 🛠️API 调用最佳实践

### 1. 错误处理

在调用 API 时，应该合理处理可能出现的错误：

```typescript
try {
  const res = await apiCall();
  // 处理成功响应
} catch (error: any) {
  // 处理错误
  if (error.response) {
    // 服务器返回错误状态码
    console.error('服务器错误：', error.response.data);
    uni.showToast({
      title: error.response.data.message || '服务器错误',
      icon: 'none'
    });
  } else if (error.request) {
    // 请求已发送但没有收到响应
    console.error('网络错误：', error.request);
    uni.showToast({
      title: '网络错误，请检查网络连接',
      icon: 'none'
    });
  } else {
    // 请求配置出错
    console.error('请求错误：', error.message);
    uni.showToast({
      title: '请求错误',
      icon: 'none'
    });
  }
}
```

### 2. 加载状态

在调用 API 时，应该显示加载状态，提升用户体验：

```typescript
const loading = ref(false);

const fetchData = async () => {
  loading.value = true;
  try {
    const res = await apiCall();
    // 处理数据
  } catch (error) {
    // 处理错误
  } finally {
    loading.value = false;
  }
};
```

### 3. 缓存策略

对于不常变化的数据，可以使用缓存策略，减少网络请求：

```typescript
import { ref, onMounted } from 'vue';
import { userApi } from '@/api/user';
import { useStorage } from '@/utils/storage';

const userList = ref([]);
const loading = ref(false);
const storage = useStorage();

const fetchUserList = async () => {
  // 尝试从缓存获取
  const cachedData = storage.get('userList');
  if (cachedData) {
    userList.value = cachedData;
    return;
  }

  loading.value = true;
  try {
    const res = await userApi.getList({ page: 1, pageSize: 100 });
    userList.value = res.data.items;
    // 缓存数据，有效期 5 分钟
    storage.set('userList', res.data.items, 5 * 60 * 1000);
  } catch (error) {
    console.error('获取用户列表失败：', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchUserList();
});
```

## 📝API 设计规范

### 1. URL 规范

- 接口 URL 使用小写字母和下划线
- 资源路径使用复数形式
- 版本号放在 URL 前缀（如 `/api/v1/`）

### 2. HTTP 方法

- `GET`：获取资源
- `POST`：创建资源
- `PUT`：更新资源
- `DELETE`：删除资源
- `PATCH`：部分更新资源

### 3. 响应格式

所有 API 响应采用统一的格式：

```json
{
  "code": 200,
  "message": "success",
  "data": {...}
}
```

- `code`：状态码，200 表示成功，其他表示失败
- `message`：响应消息，成功时为 "success"，失败时为错误信息
- `data`：响应数据，根据接口不同返回不同的数据结构

### 4. 分页响应

分页接口的响应格式：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [...],
    "total": 100,
    "page": 1,
    "pageSize": 10,
    "pages": 10
  }
}
```

- `items`：当前页的数据列表
- `total`：总记录数
- `page`：当前页码
- `pageSize`：每页大小
- `pages`：总页数

## 💡常见问题及解决方案

### 1. 认证失败

**问题**：API 调用返回 401 错误
**解决方案**：检查是否已登录，登录状态是否过期，重新登录获取新的认证信息。

### 2. 权限不足

**问题**：API 调用返回 403 错误
**解决方案**：检查当前用户是否有足够的权限执行该操作，联系管理员分配权限。

### 3. 参数错误

**问题**：API 调用返回 422 错误
**解决方案**：检查请求参数是否正确，是否缺少必要参数，参数格式是否符合要求。

### 4. 网络错误

**问题**：API 调用超时或无法连接
**解决方案**：检查网络连接是否正常，API 地址是否正确，服务器是否正常运行。

### 5. 服务器错误

**问题**：API 调用返回 500 错误
**解决方案**：检查服务器日志，查看具体错误原因，联系后端开发人员解决。

## 📚参考文档

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Swagger UI 官方文档](https://swagger.io/docs/open-source-tools/swagger-ui/)
- [Redoc 官方文档](https://redocly.com/docs/redoc/)

通过本文档的介绍，相信您已经了解了如何使用和调用 FastapiAdmin 项目的 API。如果您在使用过程中遇到任何问题，请参考常见问题及解决方案，或联系项目维护人员获取帮助。