---
outline: "deep"
title: Frontend Development Guide
---
# Frontend Development Guide

## 📋Project Overview

The frontend part of FastapiAdmin is based on **Vue3 + TypeScript + ElementPlus + Vite**, providing a modern, efficient, and type-safe development experience.

### Core Features

- **Modern Technology Stack**: Vue3 Composition API, TypeScript, Vite
- **Rich UI Components**: Based on ElementPlus, with custom components
- **Responsive Design**: Adaptive layout for different screen sizes
- **State Management**: Using Pinia for lightweight state management
- **API Integration**: Axios for HTTP requests, unified error handling
- **Route Management**: Vue Router for page navigation
- **Theming Support**: Customizable theme, support for light/dark mode
- **Internationalization**: Support for multi-language switching

## 🛠️Technology Stack

| Category | Technology | Version | Description |
|---------|------------|---------|-------------|
| **Framework** | Vue | 3.3.4 | Frontend framework |
| **Language** | TypeScript | 5.1.6 | Static type checking |
| **Build Tool** | Vite | 4.5.0 | Next generation frontend tooling |
| **UI Library** | ElementPlus | 2.3.12 | UI component library |
| **State Management** | Pinia | 2.1.6 | Lightweight state management |
| **Routing** | Vue Router | 4.2.5 | Page navigation |
| **HTTP Client** | Axios | 1.6.2 | HTTP requests |
| **CSS Preprocessor** | SCSS | 1.69.5 | CSS extension language |
| **Code Quality** | ESLint | 8.49.0 | Code linter |
| **Code Format** | Prettier | 3.0.3 | Code formatter |

## 📁Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── api/             # API request modules
│   ├── assets/          # Static resources (images, styles, etc.)
│   ├── components/      # Common components
│   ├── directives/      # Custom directives
│   ├── hooks/           # Custom hooks
│   ├── layouts/         # Page layouts
│   ├── locales/         # Internationalization files
│   ├── router/          # Route configuration
│   ├── stores/          # Pinia stores
│   ├── styles/          # Global styles
│   ├── types/           # TypeScript types
│   ├── utils/           # Utility functions
│   ├── views/           # Page components
│   ├── App.vue          # Root component
│   └── main.ts          # Entry file
├── .env.development     # Development environment variables
├── .env.production      # Production environment variables
├── eslint.config.js     # ESLint configuration
├── index.html           # HTML template
├── package.json         # Project dependencies
├── tsconfig.json        # TypeScript configuration
├── tsconfig.node.json   # TypeScript configuration for Node.js
└── vite.config.ts       # Vite configuration
```

## 🚀Getting Started

### Environment Setup

1. **Install Node.js**

   ```sh
   # Using nvm (recommended)
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
   nvm install 20
   nvm use 20

   # Or using package manager
   # macOS
   brew install node@20

   # Ubuntu/Debian
   sudo apt update
   sudo apt install nodejs npm
   ```

2. **Install pnpm**

   ```sh
   npm install -g pnpm
   ```

### Project Setup

1. **Clone the repository**

   ```sh
   git clone https://github.com/fastapiadmin/FastapiAdmin.git
   cd FastapiAdmin/frontend
   ```

2. **Install dependencies**

   ```sh
   pnpm install
   ```

3. **Configure environment variables**

   ```sh
   cp .env.development.example .env.development
   # Edit .env.development file
   ```

4. **Start development server**

   ```sh
   pnpm run dev
   ```

   The frontend will be available at `http://localhost:5173`

### Build for production

```sh
pnpm run build
```

The built files will be in the `dist` directory

## 📝Development Process

### 1. Creating a New Page

1. **Create page component** in `src/views/` directory
2. **Register route** in `src/router/` directory
3. **Add menu** configuration (if needed)
4. **Implement page logic** and UI

### 2. API Calls

#### Base Setup

API requests are managed in the `src/api/` directory, using Axios with unified configuration.

#### Example API Call

```typescript
// src/api/user.ts
import request from './request'

export interface User {
  id: number
  username: string
  name: string
  email: string
  phone: string
  status: number
}

export interface UserListParams {
  page: number
  page_size: number
  username?: string
  name?: string
}

export const userApi = {
  // Get user list
  getUserList(params: UserListParams) {
    return request({
      url: '/api/v1/users',
      method: 'get',
      params
    })
  },

  // Get user detail
  getUserDetail(id: number) {
    return request({
      url: `/api/v1/users/${id}`,
      method: 'get'
    })
  },

  // Create user
  createUser(data: Partial<User>) {
    return request({
      url: '/api/v1/users',
      method: 'post',
      data
    })
  },

  // Update user
  updateUser(id: number, data: Partial<User>) {
    return request({
      url: `/api/v1/users/${id}`,
      method: 'put',
      data
    })
  },

  // Delete user
  deleteUser(id: number) {
    return request({
      url: `/api/v1/users/${id}`,
      method: 'delete'
    })
  }
}
```

### 3. State Management

Using Pinia for state management, create stores in the `src/stores/` directory.

#### Example Store

```typescript
// src/stores/user.ts
import { defineStore } from 'pinia'
import { userApi, User, UserListParams } from '@/api/user'

export const useUserStore = defineStore('user', {
  state: () => ({
    users: [] as User[],
    total: 0,
    loading: false,
    currentUser: null as User | null
  }),

  getters: {
    getUserById: (state) => (id: number) => {
      return state.users.find(user => user.id === id)
    }
  },

  actions: {
    async getUserList(params: UserListParams) {
      this.loading = true
      try {
        const response = await userApi.getUserList(params)
        this.users = response.data.items
        this.total = response.data.total
        return response
      } finally {
        this.loading = false
      }
    },

    async getUserDetail(id: number) {
      this.loading = true
      try {
        const response = await userApi.getUserDetail(id)
        this.currentUser = response.data
        return response
      } finally {
        this.loading = false
      }
    },

    async createUser(data: Partial<User>) {
      this.loading = true
      try {
        const response = await userApi.createUser(data)
        await this.getUserList({ page: 1, page_size: 10 })
        return response
      } finally {
        this.loading = false
      }
    }
  }
})
```

### 4. UI Components

#### Using ElementPlus Components

```vue
<template>
  <el-card shadow="hover" class="mb-4">
    <template #header>
      <div class="card-header">
        <span>User List</span>
        <el-button type="primary" @click="handleAdd">Add User</el-button>
      </div>
    </template>

    <el-table :data="userStore.users" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="Username" />
      <el-table-column prop="name" label="Name" />
      <el-table-column prop="email" label="Email" />
      <el-table-column prop="phone" label="Phone" />
      <el-table-column prop="status" label="Status" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.status === 1 ? 'success' : 'danger'">
            {{ scope.row.status === 1 ? 'Active' : 'Inactive' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="Action" width="180" fixed="right">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.row)">Edit</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row.id)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-container">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.page_size"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="userStore.total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const pagination = ref({
  page: 1,
  page_size: 10
})

onMounted(() => {
  getUserList()
})

const getUserList = async () => {
  await userStore.getUserList(pagination.value)
}

const handleSizeChange = (size: number) => {
  pagination.value.page_size = size
  getUserList()
}

const handleCurrentChange = (current: number) => {
  pagination.value.page = current
  getUserList()
}

const handleAdd = () => {
  // Add user logic
}

const handleEdit = (user: any) => {
  // Edit user logic
}

const handleDelete = (id: number) => {
  // Delete user logic
}
</script>

<style scoped lang="scss">
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
```

### 5. Custom Components

Create custom components in the `src/components/` directory for reuse across the application.

#### Example Custom Component

```vue
<!-- src/components/CustomDialog.vue -->
<template>
  <el-dialog
    v-model="dialogVisible"
    :title="title"
    :width="width"
    :before-close="beforeClose"
    :destroy-on-close="destroyOnClose"
    @close="handleClose"
  >
    <slot></slot>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleCancel">Cancel</el-button>
        <el-button type="primary" @click="handleConfirm">Confirm</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  width: {
    type: String,
    default: '500px'
  },
  destroyOnClose: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void
  (e: 'confirm'): void
  (e: 'cancel'): void
  (e: 'close'): void
}>()

const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

const handleConfirm = () => {
  emit('confirm')
  dialogVisible.value = false
}

const handleCancel = () => {
  emit('cancel')
  dialogVisible.value = false
}

const handleClose = () => {
  emit('close')
}

const beforeClose = (done: () => void) => {
  emit('close')
  done()
}
</script>

<style scoped lang="scss">
.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}
</style>
```

## 🔧Common Development Tasks

### 1. Adding a New Route

1. **Create page component** in `src/views/` directory
2. **Register route** in `src/router/index.ts`

```typescript
// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/layouts/index.vue'

const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: {
          title: 'Dashboard',
          icon: 'House',
          affix: true
        }
      },
      // Add new route here
      {
        path: 'example',
        name: 'Example',
        component: () => import('@/views/example/index.vue'),
        meta: {
          title: 'Example Page',
          icon: 'Document'
        }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

### 2. Adding a New Menu Item

1. **Add route** as described above
2. **Set menu meta** in the route configuration
3. **The menu will be automatically generated** based on the route configuration

### 3. Theme Customization

#### Customizing ElementPlus Theme

1. **Create theme configuration** in `src/styles/theme.scss`

```scss
// src/styles/theme.scss
@forward 'element-plus/theme-chalk/src/common/var.scss' with (
  $colors: (
    'primary': (
      'base': #409EFF,
    ),
    'success': (
      'base': #67C23A,
    ),
    'warning': (
      'base': #E6A23C,
    ),
    'danger': (
      'base': #F56C6C,
    ),
    'info': (
      'base': #909399,
    ),
  )
);

// Import ElementPlus styles
@import 'element-plus/theme-chalk/src/index.scss';
```

2. **Import theme** in `src/main.ts`

```typescript
// src/main.ts
import '@/styles/theme.scss'
```

### 4. Internationalization

#### Adding New Language

1. **Create language files** in `src/locales/` directory
2. **Configure i18n** in `src/plugins/i18n.ts`

```typescript
// src/plugins/i18n.ts
import { createI18n } from 'vue-i18n'
import zh from '@/locales/zh-CN'
import en from '@/locales/en-US'

const messages = {
  'zh-CN': zh,
  'en-US': en
}

const i18n = createI18n({
  locale: localStorage.getItem('language') || 'zh-CN',
  fallbackLocale: 'zh-CN',
  messages
})

export default i18n
```

#### Using i18n in Components

```vue
<template>
  <div>
    <h1>{{ $t('hello') }}</h1>
    <el-button @click="switchLanguage">
      {{ $t('switchLanguage') }}
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

const switchLanguage = () => {
  locale.value = locale.value === 'zh-CN' ? 'en-US' : 'zh-CN'
  localStorage.setItem('language', locale.value)
}
</script>
```

## 📡API Calls

### 1. API Request Configuration

The API request configuration is centralized in `src/api/request.ts`, including base URL, interceptors, error handling, etc.

```typescript
// src/api/request.ts
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import router from '@/router'

// Create axios instance
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
service.interceptors.request.use(
  (config) => {
    // Add token to request headers
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
service.interceptors.response.use(
  (response) => {
    const res = response.data

    // If the custom code is not 200, it's an error
    if (res.code !== 200) {
      ElMessage({
        message: res.message || 'Error',
        type: 'error',
        duration: 5 * 1000
      })

      // 401: Unauthorized, need to re-login
      if (res.code === 401) {
        ElMessageBox.confirm('You have been logged out, please log in again', 'Confirm logout', {
          confirmButtonText: 'Re-Login',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }).then(() => {
          localStorage.removeItem('token')
          localStorage.removeItem('userInfo')
          router.push('/login')
        })
      }

      return Promise.reject(new Error(res.message || 'Error'))
    } else {
      return response
    }
  },
  (error) => {
    console.error('Response error:', error)

    let message = 'Network error'
    if (error.response) {
      switch (error.response.status) {
        case 400:
          message = 'Bad request'
          break
        case 401:
          message = 'Unauthorized'
          localStorage.removeItem('token')
          router.push('/login')
          break
        case 403:
          message = 'Forbidden'
          break
        case 404:
          message = 'Not found'
          break
        case 500:
          message = 'Internal server error'
          break
        default:
          message = `Error: ${error.response.status}`
      }
    }

    ElMessage({
      message: message,
      type: 'error',
      duration: 5 * 1000
    })

    return Promise.reject(error)
  }
)

export default service
```

### 2. API Modules

Organize API requests into modules by functionality in the `src/api/` directory.

### 3. Mock Data (Development Only)

For development purposes, you can use mock data to simulate API responses.

```typescript
// src/api/mock.ts
import { MockMethod } from 'vite-plugin-mock'

export default [
  {
    url: '/api/v1/users',
    method: 'get',
    response: () => {
      return {
        code: 200,
        message: 'success',
        data: {
          items: [
            {
              id: 1,
              username: 'admin',
              name: 'Administrator',
              email: 'admin@example.com',
              phone: '13800138000',
              status: 1
            },
            {
              id: 2,
              username: 'demo',
              name: 'Demo User',
              email: 'demo@example.com',
              phone: '13800138001',
              status: 1
            }
          ],
          total: 2
        }
      }
    }
  }
] as MockMethod[]
```

## 🔒Authentication

### 1. Login Flow

1. **User enters credentials** in the login form
2. **Frontend sends login request** to backend API
3. **Backend returns JWT token** if credentials are valid
4. **Frontend stores token** in localStorage
5. **Frontend redirects** to dashboard page
6. **Subsequent requests** include token in Authorization header

### 2. Token Management

- **Storage**: Store token in localStorage for persistence
- **Expiry**: Check token expiry and refresh if needed
- **Logout**: Clear token and user information from localStorage
- **Route Guard**: Protect routes that require authentication

### 3. Route Guard

```typescript
// src/router/guard.ts
import router from './index'
import { ElMessage } from 'element-plus'

router.beforeEach((to, from, next) => {
  // Check if route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const token = localStorage.getItem('token')
    if (!token) {
      // No token, redirect to login
      ElMessage({
        message: 'Please login first',
        type: 'warning'
      })
      next({ path: '/login' })
    } else {
      // Token exists, proceed
      next()
    }
  } else {
    // Route doesn't require authentication, proceed
    next()
  }
})
```

## 📱Responsive Design

### 1. Breakpoints

Use ElementPlus breakpoints for responsive design:

| Breakpoint | Width | Description |
|-----------|-------|-------------|
| xs | < 768px | Extra small screen |
| sm | ≥ 768px | Small screen |
| md | ≥ 992px | Medium screen |
| lg | ≥ 1200px | Large screen |
| xl | ≥ 1920px | Extra large screen |

### 2. Media Queries

```scss
// src/styles/mixins.scss
@mixin respond-to($breakpoint) {
  @if $breakpoint == xs {
    @media (max-width: 767px) {
      @content;
    }
  } @else if $breakpoint == sm {
    @media (min-width: 768px) {
      @content;
    }
  } @else if $breakpoint == md {
    @media (min-width: 992px) {
      @content;
    }
  } @else if $breakpoint == lg {
    @media (min-width: 1200px) {
      @content;
    }
  } @else if $breakpoint == xl {
    @media (min-width: 1920px) {
      @content;
    }
  }
}

// Usage
.container {
  width: 100%;
  
  @include respond-to(sm) {
    width: 750px;
  }
  
  @include respond-to(md) {
    width: 970px;
  }
  
  @include respond-to(lg) {
    width: 1170px;
  }
}
```

### 3. Flexible Layout

Use Flexbox or Grid for flexible layouts:

```vue
<template>
  <div class="flex-container">
    <div class="flex-item">Item 1</div>
    <div class="flex-item">Item 2</div>
    <div class="flex-item">Item 3</div>
  </div>
</template>

<style scoped lang="scss">
.flex-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  
  @include respond-to(xs) {
    flex-direction: column;
  }
  
  @include respond-to(sm) {
    flex-direction: row;
  }
}

.flex-item {
  flex: 1;
  min-width: 200px;
  padding: 20px;
  background-color: #f0f0f0;
  border-radius: 8px;
}
</style>
```

## ⚡Performance Optimization

### 1. Code Splitting

Use dynamic import for code splitting to reduce initial bundle size:

```typescript
// src/router/index.ts
const routes = [
  {
    path: '/dashboard',
    component: () => import('@/views/dashboard/index.vue')
  },
  {
    path: '/users',
    component: () => import('@/views/users/index.vue')
  }
]
```

### 2. Lazy Loading

Lazy load images and components to improve page load speed:

```vue
<template>
  <img v-lazy="imageUrl" alt="Lazy loaded image">
  <el-image v-lazy :src="imageUrl" />
</template>

<script setup lang="ts">
const imageUrl = 'https://example.com/image.jpg'
</script>
```

### 3. Virtual Scrolling

Use virtual scrolling for large lists to improve performance:

```vue
<template>
  <el-table-v2
    :columns="columns"
    :data="data"
    :height="400"
  />
</template>

<script setup lang="ts">
const columns = [
  { key: 'id', title: 'ID', width: 80 },
  { key: 'name', title: 'Name', width: 180 },
  { key: 'email', title: 'Email', width: 200 }
]

const data = Array.from({ length: 10000 }, (_, i) => ({
  id: i + 1,
  name: `User ${i + 1}`,
  email: `user${i + 1}@example.com`
}))
</script>
```

### 4. Memoization

Use `computed` and `useMemo` for expensive calculations:

```vue
<script setup lang="ts">
import { computed, useMemo } from 'vue'

const expensiveValue = computed(() => {
  // Expensive calculation
  return heavyComputation()
})

const memoizedValue = useMemo(() => {
  // Memoized calculation
  return anotherHeavyComputation()
}, [dependencies])
</script>
```

## 📦Build and Deployment

### 1. Build Process

```sh
# Development build
pnpm run build:dev

# Production build
pnpm run build

# Build with analysis
pnpm run build:analyze
```

### 2. Build Optimization

Configure Vite for optimal build output:

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  build: {
    target: 'es2015',
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    },
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia'],
          element: ['element-plus'],
          axios: ['axios']
        }
      }
    }
  }
})
```

### 3. Deployment

#### Docker Deployment

```dockerfile
# Dockerfile
FROM nginx:alpine

COPY dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### Nginx Configuration

```nginx
# nginx.conf
server {
  listen 80;
  server_name localhost;

  location / {
    root /usr/share/nginx/html;
    index index.html index.htm;
    try_files $uri $uri/ /index.html;
  }

  location /api/ {
    proxy_pass http://backend:8001;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  }
}
```

## 🐛Common Issues and Solutions

### 1. TypeScript Errors

**Issue**: TypeScript compilation errors
**Solution**: Check type definitions, add proper types, use type assertions if needed

### 2. API Request Failures

**Issue**: API requests returning 401 Unauthorized
**Solution**: Check if token is valid, ensure token is included in request headers

**Issue**: API requests returning 403 Forbidden
**Solution**: Check user permissions, ensure user has access to requested resource

### 3. CORS Issues

**Issue**: Cross-Origin Resource Sharing errors
**Solution**: Configure CORS on backend, ensure frontend API base URL is correct

### 4. Build Failures

**Issue**: Build process fails with error
**Solution**: Check for TypeScript errors, ensure all dependencies are installed, check Vite configuration

### 5. Performance Issues

**Issue**: Page load time is slow
**Solution**: Implement code splitting, lazy loading, virtual scrolling, optimize images

**Issue**: Component rendering is slow
**Solution**: Use computed properties, memoization, avoid unnecessary re-renders

### 6. Styling Issues

**Issue**: Styles not applying correctly
**Solution**: Check CSS selectors, use scoped styles, avoid CSS conflicts

**Issue**: Responsive design not working
**Solution**: Check media queries, ensure proper breakpoints, test on different devices

## 📚Best Practices

### 1. Coding Standards

- **File Naming**: Use kebab-case for files, PascalCase for components
- **Variable Naming**: Use camelCase for variables, PascalCase for components
- **Function Naming**: Use camelCase for functions, PascalCase for classes
- **Constant Naming**: Use UPPER_SNAKE_CASE for constants
- **Indentation**: Use 2 spaces for indentation
- **Line Length**: Keep lines under 120 characters
- **Comments**: Add comments for complex logic

### 2. Component Design

- **Single Responsibility**: Each component should have a single responsibility
- **Props Validation**: Validate props with TypeScript or prop types
- **Event Naming**: Use kebab-case for event names
- **Slot Naming**: Use kebab-case for slot names
- **Reusability**: Design components for reuse across the application

### 3. State Management

- **Store Structure**: Organize stores by feature or domain
- **Mutations**: Keep mutations simple and synchronous
- **Actions**: Use actions for asynchronous operations
- **Getters**: Use getters for derived state
- **Modules**: Split large stores into modules

### 4. API Design

- **Endpoint Naming**: Use RESTful API naming conventions
- **Error Handling**: Unified error handling for API requests
- **Request Interceptors**: Add common logic (e.g., authentication) to request interceptors
- **Response Interceptors**: Add common logic (e.g., error handling) to response interceptors
- **Caching**: Implement caching for frequently used data

### 5. Security

- **Input Validation**: Validate all user input
- **XSS Protection**: Use Vue's built-in XSS protection
- **CSRF Protection**: Implement CSRF protection for forms
- **Token Security**: Securely store and transmit tokens
- **Sensitive Data**: Avoid storing sensitive data in frontend

## 🎉Conclusion

The frontend part of FastapiAdmin provides a modern, efficient, and type-safe development experience based on Vue3, TypeScript, and ElementPlus. By following the guidelines in this document, you can build high-quality, maintainable frontend applications that integrate seamlessly with the FastapiAdmin backend.

For more detailed information about Vue3, TypeScript, or ElementPlus, please refer to their official documentation:

- [Vue3 Documentation](https://vuejs.org/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [ElementPlus Documentation](https://element-plus.org/)
- [Vite Documentation](https://vitejs.dev/)