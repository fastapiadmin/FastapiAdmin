---
outline: "deep"
title: Miniprogram Development Guide
---
# Miniprogram Development Guide

## 📋Project Overview

FastApp is the mobile application component of FastapiAdmin, based on **Uni App + Vue3 + TypeScript + Wot Design Uni**, supporting multi-platform deployment including WeChat Mini Program, Alipay Mini Program, Web H5, iOS, and Android.

### Core Features

- **Cross-platform Development**: Write once, run on multiple platforms
- **Modern Technology Stack**: Vue3 Composition API, TypeScript
- **Rich UI Components**: Based on Wot Design Uni, optimized for mobile
- **Unified Login**: Support for multiple login methods
- **Personal Center**: User information management, avatar upload
- **Workbench**: Quick access to commonly used functions
- **Message Push**: Real-time message notification
- **API Integration**: Seamless integration with FastapiAdmin backend
- **Responsive Design**: Adaptive layout for different screen sizes
- **Performance Optimization**: Code splitting, lazy loading, etc.

## 🛠️Technology Stack

| Category | Technology | Version | Description |
|---------|------------|---------|-------------|
| **Framework** | Uni App | 3.0.0 | Cross-platform application framework |
| **Language** | Vue | 3.3.4 | Frontend framework |
| **Language** | TypeScript | 5.1.6 | Static type checking |
| **UI Library** | Wot Design Uni | 1.9.1 | Mobile UI component library |
| **HTTP Client** | Uni.request | - | Network request API |
| **State Management** | Pinia | 2.1.6 | Lightweight state management |
| **Routing** | Uni Router | - | Page navigation |
| **Storage** | Uni Storage | - | Local storage API |
| **Build Tool** | Vite | 4.5.0 | Next generation frontend tooling |

## 📁Project Structure

```
FastApp/
├── public/              # Static assets
├── src/
│   ├── api/             # API request modules
│   ├── assets/          # Static resources (images, styles, etc.)
│   ├── components/      # Common components
│   ├── composables/     # Custom composables
│   ├── config/          # Configuration files
│   ├── pages/           # Page components
│   │   ├── index/        # Home page
│   │   ├── login/        # Login page
│   │   ├── mine/         # Personal center
│   │   └── workbench/    # Workbench
│   ├── services/        # Business logic services
│   ├── stores/          # Pinia stores
│   ├── styles/          # Global styles
│   ├── types/           # TypeScript types
│   ├── utils/           # Utility functions
│   ├── App.vue          # Root component
│   ├── main.ts          # Entry file
│   ├── manifest.json     # Uni App configuration
│   └── pages.json        # Page configuration
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

3. **Install HBuilderX** (recommended for Uni App development)

   Download from [HBuilderX Official Website](https://www.dcloud.io/hbuilderx.html)

### Project Setup

1. **Clone the repository**

   ```sh
   git clone https://github.com/fastapiadmin/FastApp.git
   cd FastApp
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
   # Start H5 development server
   pnpm run dev:h5

   # Start WeChat Mini Program development server
   pnpm run dev:mp-weixin

   # Start Alipay Mini Program development server
   pnpm run dev:mp-alipay
   ```

   - H5: `http://localhost:5174`
   - WeChat Mini Program: Use WeChat Developer Tools to open `dist/dev/mp-weixin`
   - Alipay Mini Program: Use Alipay Developer Tools to open `dist/dev/mp-alipay`

### Build for Production

```sh
# Build H5 version
pnpm run build:h5

# Build WeChat Mini Program version
pnpm run build:mp-weixin

# Build Alipay Mini Program version
pnpm run build:mp-alipay

# Build all platforms
pnpm run build:all
```

## 📝Development Process

### 1. Creating a New Page

1. **Add page configuration** in `pages.json`

   ```json
   // pages.json
   {
     "pages": [
       {
         "path": "pages/index/index",
         "style": {
           "navigationBarTitleText": "Home"
         }
       },
       // Add new page here
       {
         "path": "pages/example/index",
         "style": {
           "navigationBarTitleText": "Example"
         }
       }
     ]
   }
   ```

2. **Create page component** in `src/pages/` directory

   ```vue
   <!-- src/pages/example/index.vue -->
   <template>
     <view class="example-page">
       <wd-nav-bar title="Example Page" />
       <view class="content">
         <wd-button type="primary" @click="handleClick">Click Me</wd-button>
         <wd-text>{{ message }}</wd-text>
       </view>
     </view>
   </template>

   <script setup lang="ts">
   import { ref } from 'vue'
   
   const message = ref('Hello from Example Page')
   
   const handleClick = () => {
     message.value = 'Button clicked!'
   }
   </script>

   <style scoped>
   .example-page {
     min-height: 100vh;
     background-color: #f5f5f5;
   }
   
   .content {
     padding: 20px;
   }
   </style>
   ```

### 2. API Calls

#### Base Setup

API requests are managed in the `src/api/` directory, using Uni.request for network requests.

#### Example API Call

```typescript
// src/api/user.ts
import { request } from '@/utils/request'

export interface User {
  id: number
  username: string
  name: string
  email: string
  phone: string
  avatar: string
}

export interface LoginParams {
  username: string
  password: string
}

export interface LoginResponse {
  token: string
  user: User
}

export const userApi = {
  // Login
  login(params: LoginParams) {
    return request<LoginResponse>({
      url: '/api/v1/auth/login',
      method: 'post',
      data: params
    })
  },

  // Get user info
  getUserInfo() {
    return request<User>({
      url: '/api/v1/users/me',
      method: 'get'
    })
  },

  // Update user info
  updateUserInfo(data: Partial<User>) {
    return request<User>({
      url: '/api/v1/users/me',
      method: 'put',
      data: data
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
import { userApi, User, LoginParams } from '@/api/user'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null,
    token: '',
    loading: false,
    isLoggedIn: false
  }),

  getters: {
    getUser: (state) => state.user,
    getToken: (state) => state.token,
    getLoading: (state) => state.loading,
    getIsLoggedIn: (state) => state.isLoggedIn
  },

  actions: {
    async login(params: LoginParams) {
      this.loading = true
      try {
        const response = await userApi.login(params)
        this.token = response.token
        this.user = response.user
        this.isLoggedIn = true
        // Save token to local storage
        uni.setStorageSync('token', response.token)
        return response
      } finally {
        this.loading = false
      }
    },

    async getUserInfo() {
      this.loading = true
      try {
        const response = await userApi.getUserInfo()
        this.user = response
        return response
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.user = null
      this.token = ''
      this.isLoggedIn = false
      // Clear token from local storage
      uni.removeStorageSync('token')
    }
  }
})
```

### 4. UI Components

#### Using Wot Design Uni Components

```vue
<template>
  <view class="user-profile">
    <wd-nav-bar title="User Profile" />
    <view class="profile-content">
      <wd-avatar :src="user?.avatar || defaultAvatar" size="large" class="avatar" />
      <view class="user-info">
        <wd-text class="username">{{ user?.name || 'Unknown' }}</wd-text>
        <wd-text class="email">{{ user?.email || 'No email' }}</wd-text>
      </view>
      <wd-cell-group class="profile-items">
        <wd-cell title="Username" :value="user?.username" is-link @click="editUsername" />
        <wd-cell title="Phone" :value="user?.phone || 'Not set'" is-link @click="editPhone" />
        <wd-cell title="Password" value="******" is-link @click="changePassword" />
      </wd-cell-group>
      <wd-button type="danger" @click="logout" class="logout-btn">Logout</wd-button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const defaultAvatar = '/static/avatar-default.png'

const user = computed(() => userStore.user)

onMounted(() => {
  if (userStore.isLoggedIn) {
    userStore.getUserInfo()
  }
})

const editUsername = () => {
  // Edit username logic
}

const editPhone = () => {
  // Edit phone logic
}

const changePassword = () => {
  // Change password logic
}

const logout = () => {
  uni.showModal({
    title: 'Logout',
    content: 'Are you sure you want to logout?',
    success: (res) => {
      if (res.confirm) {
        userStore.logout()
        uni.navigateTo({ url: '/pages/login/index' })
      }
    }
  })
}
</script>

<style scoped>
.user-profile {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.profile-content {
  padding: 20px;
}

.avatar {
  display: block;
  margin: 0 auto 20px;
}

.user-info {
  text-align: center;
  margin-bottom: 30px;
}

.username {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 8px;
}

.email {
  font-size: 14px;
  color: #666;
}

.profile-items {
  margin-bottom: 30px;
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
}

.logout-btn {
  width: 100%;
}
</style>
```

### 5. Navigation

#### Page Navigation

```javascript
// Navigate to a new page
uni.navigateTo({
  url: '/pages/example/index'
})

// Redirect to a page (no back button)
uni.redirectTo({
  url: '/pages/login/index'
})

// Navigate to tab page
uni.switchTab({
  url: '/pages/index/index'
})

// Go back to previous page
uni.navigateBack({
  delta: 1
})
```

#### Passing Parameters

```javascript
// Pass parameters when navigating
uni.navigateTo({
  url: `/pages/example/index?id=1&name=test`
})

// Receive parameters on the target page
// In onLoad lifecycle hook
onLoad((options) => {
  console.log(options.id) // '1'
  console.log(options.name) // 'test'
})
```

## 📡API Calls

### 1. Network Request Configuration

The network request configuration is centralized in `src/utils/request.ts`, including base URL, interceptors, error handling, etc.

```typescript
// src/utils/request.ts
import type { UniRequestOptions, UniRequestSuccessResult } from '@/types/uni'

export interface RequestOptions extends UniRequestOptions {
  showLoading?: boolean
  loadingText?: string
}

export interface RequestResult<T = any> {
  code: number
  message: string
  data: T
}

export function request<T = any>(options: RequestOptions): Promise<T> {
  return new Promise((resolve, reject) => {
    const {
      url,
      method = 'GET',
      data,
      header = {},
      showLoading = true,
      loadingText = 'Loading...',
      ...restOptions
    } = options

    // Show loading
    if (showLoading) {
      uni.showLoading({
        title: loadingText,
        mask: true
      })
    }

    // Add base URL
    const baseURL = import.meta.env.VITE_API_BASE_URL
    const requestUrl = url.startsWith('http') ? url : `${baseURL}${url}`

    // Add token to header
    const token = uni.getStorageSync('token')
    if (token) {
      header['Authorization'] = `Bearer ${token}`
    }

    // Send request
    uni.request({
      url: requestUrl,
      method,
      data,
      header,
      ...restOptions,
      success: (res: UniRequestSuccessResult) => {
        // Hide loading
        if (showLoading) {
          uni.hideLoading()
        }

        // Handle response
        if (res.statusCode === 200) {
          const result = res.data as RequestResult<T>
          if (result.code === 200) {
            resolve(result.data)
          } else {
            // Handle business error
            uni.showToast({
              title: result.message || 'Request failed',
              icon: 'none'
            })
            reject(new Error(result.message || 'Request failed'))
          }
        } else if (res.statusCode === 401) {
          // Handle unauthorized
          uni.showToast({
            title: 'Please login again',
            icon: 'none'
          })
          uni.redirectTo({ url: '/pages/login/index' })
          reject(new Error('Unauthorized'))
        } else {
          // Handle other errors
          uni.showToast({
            title: `Error: ${res.statusCode}`,
            icon: 'none'
          })
          reject(new Error(`HTTP error ${res.statusCode}`))
        }
      },
      fail: (err) => {
        // Hide loading
        if (showLoading) {
          uni.hideLoading()
        }

        // Handle network error
        uni.showToast({
          title: 'Network error',
          icon: 'none'
        })
        reject(err)
      }
    })
  })
}
```

### 2. API Modules

Organize API requests into modules by functionality in the `src/api/` directory.

### 3. Mock Data (Development Only)

For development purposes, you can use mock data to simulate API responses.

```typescript
// src/api/mock.ts
export const mockData = {
  user: {
    id: 1,
    username: 'demo',
    name: 'Demo User',
    email: 'demo@example.com',
    phone: '13800138000',
    avatar: '/static/avatar-default.png'
  },
  menu: [
    {
      id: 1,
      name: 'Dashboard',
      icon: 'home',
      url: '/pages/dashboard/index'
    },
    {
      id: 2,
      name: 'Tasks',
      icon: 'todo',
      url: '/pages/tasks/index'
    },
    {
      id: 3,
      name: 'Messages',
      icon: 'chat',
      url: '/pages/messages/index'
    }
  ]
}
```

## 🔒Authentication

### 1. Login Flow

1. **User enters credentials** in the login form
2. **App sends login request** to backend API
3. **Backend returns JWT token** if credentials are valid
4. **App stores token** in local storage
5. **App redirects** to home page
6. **Subsequent requests** include token in Authorization header

### 2. Token Management

- **Storage**: Store token in uni.setStorageSync for persistence
- **Expiry**: Check token expiry and refresh if needed
- **Logout**: Clear token and user information from storage
- **Auto Login**: Check for existing token on app launch

### 3. Login Page Example

```vue
<template>
  <view class="login-page">
    <view class="login-form">
      <view class="logo-container">
        <image src="/static/logo.png" class="logo" mode="aspectFit" />
        <text class="app-name">FastApp</text>
      </view>
      <wd-form @submit="handleSubmit">
        <wd-input
          v-model="form.username"
          placeholder="Username"
          clearable
          required
          class="form-item"
        />
        <wd-input
          v-model="form.password"
          placeholder="Password"
          password
          clearable
          required
          class="form-item"
        />
        <wd-button type="primary" form-type="submit" class="login-btn" :loading="loading">
          Login
        </wd-button>
      </wd-form>
      <view class="login-info">
        <text class="demo-account">Demo Account: demo / 123456</text>
        <text class="admin-account">Admin Account: admin / 123456</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const loading = ref(false)
const form = ref({
  username: '',
  password: ''
})

const handleSubmit = async () => {
  if (!form.value.username || !form.value.password) {
    uni.showToast({
      title: 'Please enter username and password',
      icon: 'none'
    })
    return
  }

  loading.value = true
  try {
    await userStore.login(form.value)
    uni.showToast({
      title: 'Login successful',
      icon: 'success'
    })
    uni.switchTab({ url: '/pages/index/index' })
  } catch (error) {
    console.error('Login failed:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background-color: #f5f5f5;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.login-form {
  width: 100%;
  max-width: 400px;
  background-color: #fff;
  border-radius: 12px;
  padding: 30px 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.logo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.logo {
  width: 80px;
  height: 80px;
  margin-bottom: 16px;
}

.app-name {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.form-item {
  margin-bottom: 20px;
}

.login-btn {
  width: 100%;
  margin-top: 10px;
}

.login-info {
  margin-top: 20px;
  font-size: 12px;
  color: #999;
  text-align: center;
}

.demo-account {
  display: block;
  margin-bottom: 8px;
}
</style>
```

## 📱UI Components

### 1. Common Components

#### Layout Components

- **wd-cell-group**: Group of cells
- **wd-cell**: List item with title and value
- **wd-grid**: Grid layout
- **wd-flex**: Flexible layout

#### Form Components

- **wd-input**: Text input
- **wd-button**: Button
- **wd-checkbox**: Checkbox
- **wd-radio**: Radio button
- **wd-picker**: Picker for date, time, etc.
- **wd-upload**: File upload

#### Feedback Components

- **wd-toast**: Toast message
- **wd-loading**: Loading indicator
- **wd-dialog**: Dialog box
- **wd-action-sheet**: Action sheet
- **wd-popup**: Popup layer

#### Navigation Components

- **wd-nav-bar**: Navigation bar
- **wd-tab-bar**: Tab bar
- **wd-steps**: Step indicator

### 2. Custom Components

Create custom components in the `src/components/` directory for reuse across the application.

#### Example Custom Component

```vue
<!-- src/components/CustomCard.vue -->
<template>
  <view class="custom-card" :class="{ 'card-border': border }">
    <view class="card-header" v-if="title">
      <wd-text class="card-title">{{ title }}</wd-text>
      <slot name="header"></slot>
    </view>
    <view class="card-content">
      <slot></slot>
    </view>
    <view class="card-footer" v-if="footer">
      <slot name="footer"></slot>
    </view>
  </view>
</template>

<script setup lang="ts">
defineProps({
  title: {
    type: String,
    default: ''
  },
  border: {
    type: Boolean,
    default: true
  },
  footer: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.custom-card {
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 16px;
}

.card-border {
  border: 1px solid #e5e5e5;
}

.card-header {
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.card-content {
  padding: 16px;
}

.card-footer {
  padding: 16px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: flex-end;
}
</style>
```

## 🔧Multi-platform Adaptation

### 1. Platform-specific Code

Use conditional compilation to write platform-specific code:

```vue
<template>
  <view class="platform-demo">
    <!-- Platform-specific UI -->
    <view v-if="isWeChat">
      <text>WeChat Mini Program</text>
    </view>
    <view v-else-if="isAlipay">
      <text>Alipay Mini Program</text>
    </view>
    <view v-else-if="isH5">
      <text>Web H5</text>
    </view>
    <view v-else>
      <text>Other Platforms</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const isWeChat = computed(() => {
  return uni.getSystemInfoSync().platform === 'devtools' || 
         uni.getSystemInfoSync().platform === 'ios' || 
         uni.getSystemInfoSync().platform === 'android'
})

const isAlipay = computed(() => {
  // Check if running in Alipay Mini Program
  return typeof my !== 'undefined'
})

const isH5 = computed(() => {
  return uni.getSystemInfoSync().platform === 'h5'
})
</script>
```

### 2. Platform-specific Styles

```css
/* Common styles */
.common-style {
  font-size: 16px;
  color: #333;
}

/* H5-specific styles */
@media screen and (min-width: 750px) {
  .h5-specific {
    padding: 20px;
  }
}

/* Mini Program-specific styles */
/* WeChat Mini Program */
/* #ifdef MP-WEIXIN */
.mp-weixin-specific {
  background-color: #f7f7f7;
}
/* #endif */

/* Alipay Mini Program */
/* #ifdef MP-ALIPAY */
.mp-alipay-specific {
  background-color: #f5f5f5;
}
/* #endif */
```

### 3. Platform-specific APIs

```javascript
// Use platform-specific APIs
if (uni.canIUse('getLocation')) {
  uni.getLocation({
    type: 'wgs84',
    success: (res) => {
      console.log('Latitude:', res.latitude)
      console.log('Longitude:', res.longitude)
    }
  })
} else {
  // API not supported
  uni.showToast({
    title: 'Location API not supported',
    icon: 'none'
  })
}
```

## ⚡Performance Optimization

### 1. Code Splitting

- **Lazy Loading**: Lazy load pages and components
- **Dynamic Import**: Use dynamic import for large modules
- **Tree Shaking**: Remove unused code during build

### 2. Rendering Optimization

- **Reduce Re-renders**: Use computed properties and memoization
- **Virtual Scrolling**: Use virtual scrolling for long lists
- **Avoid Inline Styles**: Use class-based styles instead of inline styles
- **Optimize Images**: Use appropriate image formats and sizes

### 3. Network Optimization

- **API Caching**: Cache frequently used API responses
- **Request Batching**: Combine multiple requests when possible
- **Compression**: Enable GZIP compression for API responses
- **CDN**: Use CDN for static assets

### 4. Storage Optimization

- **Local Storage**: Use uni.setStorageSync for small amounts of data
- **IndexedDB**: Use for larger datasets
- **Cleanup**: Remove unused data from storage
- **Encryption**: Encrypt sensitive data before storing

### 5. Startup Optimization

- **Splash Screen**: Use splash screen for better user experience
- **Preloading**: Preload essential resources during splash screen
- **Minimize Bundle Size**: Optimize build output
- **Code Splitting**: Load only essential code on startup

## 📦Packaging and Deployment

### 1. WeChat Mini Program

1. **Build** the WeChat Mini Program version
2. **Open** the `dist/build/mp-weixin` directory in WeChat Developer Tools
3. **Test** the mini program in developer tools
4. **Submit** for review in WeChat Mini Program backend
5. **Publish** after approval

### 2. Alipay Mini Program

1. **Build** the Alipay Mini Program version
2. **Open** the `dist/build/mp-alipay` directory in Alipay Developer Tools
3. **Test** the mini program in developer tools
4. **Submit** for review in Alipay Mini Program backend
5. **Publish** after approval

### 3. H5 Deployment

1. **Build** the H5 version
2. **Deploy** the `dist/build/h5` directory to a web server
3. **Configure** Nginx or Apache for static file serving
4. **Enable** HTTPS for better security

### 4. Mobile App (iOS/Android)

1. **Build** the app version using HBuilderX
2. **Configure** app information in manifest.json
3. **Generate** iOS/Android app packages
4. **Submit** to App Store and Google Play

## 🐛Common Issues and Solutions

### 1. Platform Compatibility Issues

**Issue**: Code works on H5 but not on mini programs
**Solution**: Check for platform-specific APIs, use conditional compilation, test on target platforms

### 2. Network Request Issues

**Issue**: API requests fail with CORS errors
**Solution**: Configure CORS on backend, use proxy during development

**Issue**: Request timeout errors
**Solution**: Increase timeout, check network connection, optimize API response time

### 3. UI Display Issues

**Issue**: Layout looks different on different devices
**Solution**: Use responsive design, test on multiple devices, use flexbox for layouts

**Issue**: Components not rendering correctly
**Solution**: Check component usage, ensure proper props, update UI library version

### 4. Performance Issues

**Issue**: App is slow to launch
**Solution**: Optimize startup process, reduce initial bundle size, use code splitting

**Issue**: Scroll lag on long lists
**Solution**: Use virtual scrolling, optimize list items, reduce DOM nodes

### 5. Storage Issues

**Issue**: Storage quota exceeded
**Solution**: Clean up unused data, use appropriate storage mechanism, monitor storage usage

### 6. Authentication Issues

**Issue**: Token expired
**Solution**: Implement token refresh mechanism, prompt user to re-login

**Issue**: Auto login not working
**Solution**: Check token storage, verify token validity on startup

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
- **Props Validation**: Validate props with TypeScript
- **Event Naming**: Use kebab-case for event names
- **Slot Naming**: Use kebab-case for slot names
- **Reusability**: Design components for reuse across the application

### 3. State Management

- **Store Structure**: Organize stores by feature or domain
- **Actions**: Use actions for asynchronous operations
- **Getters**: Use getters for derived state
- **Modules**: Split large stores into modules
- **Persistence**: Persist essential state to local storage

### 4. API Design

- **Endpoint Naming**: Use RESTful API naming conventions
- **Error Handling**: Unified error handling for API requests
- **Request Interceptors**: Add common logic (e.g., authentication) to request interceptors
- **Response Interceptors**: Add common logic (e.g., error handling) to response interceptors
- **Caching**: Implement caching for frequently used data

### 5. Security

- **Input Validation**: Validate all user input
- **Token Security**: Securely store and transmit tokens
- **HTTPS**: Use HTTPS for all communications
- **Data Protection**: Encrypt sensitive data
- **Rate Limiting**: Implement rate limiting to prevent abuse

## 🎉Conclusion

FastApp provides a comprehensive mobile application solution for FastapiAdmin, leveraging the power of Uni App to achieve cross-platform deployment. By following the guidelines in this document, you can develop high-quality, performant, and maintainable mobile applications that seamlessly integrate with the FastapiAdmin backend.

For more detailed information about Uni App, Vue3, or Wot Design Uni, please refer to their official documentation:

- [Uni App Documentation](https://uniapp.dcloud.io/)
- [Vue3 Documentation](https://vuejs.org/)
- [Wot Design Uni Documentation](https://wot-design-uni.github.io/)
- [TypeScript Documentation](https://www.typescriptlang.org/)