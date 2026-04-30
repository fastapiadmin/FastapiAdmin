---
outline: "deep"
title: API Documentation
---
# API Documentation

## 📚 API Documentation Overview

The FastapiAdmin project provides comprehensive API documentation to help developers understand and use the system's interfaces. This document will detail how to use and call these APIs.

## 🔧 Backend API Documentation

### 1. Access Methods

The backend API documentation is automatically generated based on FastAPI, supporting both Swagger and Redoc formats:

- **Swagger UI**: <http://localhost:8001/api/v1/docs> (local development environment)
- **Redoc**: <http://localhost:8001/api/v1/redoc> (local development environment)
- **Online Demo**: <https://service.fastapiadmin.com/api/v1/docs> (production environment)

### 2. Usage Methods

#### 2.1 Authentication and Login

1. Open the Swagger UI documentation page
2. Click the "Authorize" button in the top right corner of the page
3. Enter your username and password in the dialog box that appears
4. Click the "Authorize" button to complete authentication
5. After successful authentication, all API calls will automatically carry authentication information

#### 2.2 API Testing

1. Find the API you want to test in Swagger UI
2. Click the API name to expand detailed information
3. Click the "Try it out" button
4. Fill in the necessary parameters
5. Click the "Execute" button to execute the request
6. View the response results

### 3. API Interface Classification

Backend API interfaces are mainly divided into the following categories:

- **System Management**: User, role, menu, department, position, and other management interfaces
- **Monitoring Management**: Online users, server monitoring, cache monitoring, and other interfaces
- **Task Management**: Scheduled task management interfaces
- **Log Management**: Operation log query interfaces
- **Development Tools**: Code generation, form building, and other interfaces

## 📱 Frontend API Calls

### 1. Frontend API Encapsulation

The frontend project uses TypeScript to encapsulate API calls, mainly located in the `frontend/src/api` directory, organized by module:

```
frontend/src/api/
├── module_example/    # Example module
│   └── demo.ts
├── module_monitor/    # Monitoring module
│   ├── cache.ts
│   ├── online.ts
│   └── server.ts
└── module_system/     # System module
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

### 2. API Call Examples

#### 2.1 Import API Modules

```typescript
import { authApi } from '@/api/module_system/auth';
import { userApi } from '@/api/module_system/user';
```

#### 2.2 Call Login API

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

    // Save token
    userStore.setToken(res.data.token);

    // Get user info
    await userStore.getUserInfo();

    // Navigate to home page
    router.push('/');
  } catch (error) {
    console.error('Login failed:', error);
  }
};
```

#### 2.3 Call User Management API

```typescript
import { userApi } from '@/api/module_system/user';

// Get user list
const getUserList = async () => {
  try {
    const res = await userApi.getList({
      page: 1,
      pageSize: 10,
      username: 'admin'
    });
    console.log('User list:', res.data);
  } catch (error) {
    console.error('Failed to get user list:', error);
  }
};

// Get user detail
const getUserDetail = async (userId: number) => {
  try {
    const res = await userApi.getDetail(userId);
    console.log('User detail:', res.data);
  } catch (error) {
    console.error('Failed to get user detail:', error);
  }
};

// Create user
const createUser = async (userData: any) => {
  try {
    const res = await userApi.create(userData);
    console.log('User created successfully:', res.data);
  } catch (error) {
    console.error('Failed to create user:', error);
  }
};

// Update user
const updateUser = async (userId: number, userData: any) => {
  try {
    const res = await userApi.update(userId, userData);
    console.log('User updated successfully:', res.data);
  } catch (error) {
    console.error('Failed to update user:', error);
  }
};

// Delete user
const deleteUser = async (userId: number) => {
  try {
    const res = await userApi.delete(userId);
    console.log('User deleted successfully:', res.data);
  } catch (error) {
    console.error('Failed to delete user:', error);
  }
};
```

## 📱 FastApp Mobile API Calls

### 1. Mobile API Encapsulation

The FastApp mobile project also encapsulates API calls, mainly located in the `src/api` directory:

```
FastApp/src/api/
├── auth.ts       # Authentication related interfaces
├── file.ts       # File related interfaces
└── user.ts       # User related interfaces
```

### 2. API Call Examples

#### 2.1 Import API Modules

```typescript
import { authApi } from '@/api/auth';
import { userApi } from '@/api/user';
```

#### 2.2 Call Login API

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

    // Save token
    userStore.setToken(res.data.token);

    // Get user info
    await userStore.getUserInfo();

    // Navigate to home page
    uni.switchTab({ url: '/pages/index/index' });
  } catch (error) {
    console.error('Login failed:', error);
  }
};
```

#### 2.3 Call User Info API

```typescript
import { userApi } from '@/api/user';

// Get user info
const getUserInfo = async () => {
  try {
    const res = await userApi.getUserInfo();
    console.log('User info:', res.data);
    return res.data;
  } catch (error) {
    console.error('Failed to get user info:', error);
    return null;
  }
};

// Update user info
const updateUserInfo = async (userData: any) => {
  try {
    const res = await userApi.updateUserInfo(userData);
    console.log('User info updated successfully:', res.data);
    return true;
  } catch (error) {
    console.error('Failed to update user info:', error);
    return false;
  }
};
```

## 🛠️ API Call Best Practices

### 1. Error Handling

When calling APIs, you should properly handle possible errors:

```typescript
try {
  const res = await apiCall();
  // Handle successful response
} catch (error: any) {
  // Handle errors
  if (error.response) {
    // Server returned error status code
    console.error('Server error:', error.response.data);
    uni.showToast({
      title: error.response.data.message || 'Server error',
      icon: 'none'
    });
  } else if (error.request) {
    // Request was sent but no response received
    console.error('Network error:', error.request);
    uni.showToast({
      title: 'Network error, please check your connection',
      icon: 'none'
    });
  } else {
    // Request configuration error
    console.error('Request error:', error.message);
    uni.showToast({
      title: 'Request error',
      icon: 'none'
    });
  }
}
```

### 2. Loading State

When calling APIs, you should display a loading state to improve user experience:

```typescript
const loading = ref(false);

const fetchData = async () => {
  loading.value = true;
  try {
    const res = await apiCall();
    // Process data
  } catch (error) {
    // Handle errors
  } finally {
    loading.value = false;
  }
};
```

### 3. Caching Strategy

For data that doesn't change frequently, you can use a caching strategy to reduce network requests:

```typescript
import { ref, onMounted } from 'vue';
import { userApi } from '@/api/user';
import { useStorage } from '@/utils/storage';

const userList = ref([]);
const loading = ref(false);
const storage = useStorage();

const fetchUserList = async () => {
  // Try to get from cache
  const cachedData = storage.get('userList');
  if (cachedData) {
    userList.value = cachedData;
    return;
  }

  loading.value = true;
  try {
    const res = await userApi.getList({ page: 1, pageSize: 100 });
    userList.value = res.data.items;
    // Cache data, valid for 5 minutes
    storage.set('userList', res.data.items, 5 * 60 * 1000);
  } catch (error) {
    console.error('Failed to get user list:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchUserList();
});
```

## 📝 API Design Standards

### 1. URL Standards

- API URLs use lowercase letters and underscores
- Resource paths use plural forms
- Version numbers are placed in the URL prefix (e.g., `/api/v1/`)

### 2. HTTP Methods

- `GET`: Retrieve resources
- `POST`: Create resources
- `PUT`: Update resources
- `DELETE`: Delete resources
- `PATCH`: Partially update resources

### 3. Response Format

All API responses use a unified format:

```json
{
  "code": 200,
  "message": "success",
  "data": {...}
}
```

- `code`: Status code, 200 indicates success, others indicate failure
- `message`: Response message, "success" when successful, error message when failed
- `data`: Response data, returning different data structures based on the interface

### 4. Paginated Response

Response format for paginated interfaces:

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

- `items`: Data list for the current page
- `total`: Total number of records
- `page`: Current page number
- `pageSize`: Page size
- `pages`: Total number of pages

## 💡 Common Issues and Solutions

### 1. Authentication Failed

**Issue**: API call returns 401 error
**Solution**: Check if you are logged in, if the login status has expired, and re-login to obtain new authentication information.

### 2. Insufficient Permissions

**Issue**: API call returns 403 error
**Solution**: Check if the current user has sufficient permissions to perform the operation, and contact the administrator to assign permissions.

### 3. Parameter Error

**Issue**: API call returns 422 error
**Solution**: Check if the request parameters are correct, if required parameters are missing, and if the parameter format meets the requirements.

### 4. Network Error

**Issue**: API call times out or cannot connect
**Solution**: Check if the network connection is normal, if the API address is correct, and if the server is running normally.

### 5. Server Error

**Issue**: API call returns 500 error
**Solution**: Check server logs, view the specific error cause, and contact backend developers to resolve.

## 📚 Reference Documentation

- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [Swagger UI Official Documentation](https://swagger.io/docs/open-source-tools/swagger-ui/)
- [Redoc Official Documentation](https://redocly.com/docs/redoc/)

Through the introduction of this document, you should now understand how to use and call the APIs of the FastapiAdmin project. If you encounter any issues during use, please refer to the common issues and solutions, or contact the project maintainers for help.
