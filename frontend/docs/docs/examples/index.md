---
outline: "deep"
title: 代码示例和使用案例
---
# 代码示例和使用案例

## 📝代码示例

### 1. 后端代码示例

#### 1.1 创建新的API模块

```python
# 1. 创建模型文件
# app/api/v1/models/demo/example_model.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.base_model import Base

class Example(Base):
    __tablename__ = "example"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# 2. 创建Schema文件
# app/api/v1/schemas/demo/example_schema.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ExampleBase(BaseModel):
    name: str
    description: Optional[str] = None

class ExampleCreate(ExampleBase):
    pass

class ExampleUpdate(ExampleBase):
    name: Optional[str] = None

class ExampleResponse(ExampleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 3. 创建查询参数文件
# app/api/v1/params/demo/example_param.py
from app.core.base_params import BaseParams
from typing import Optional

class ExampleParams(BaseParams):
    name: Optional[str] = None
    description: Optional[str] = None

# 4. 创建CRUD文件
# app/api/v1/cruds/demo/example_crud.py
from sqlalchemy.orm import Session
from app.api.v1.models.demo.example_model import Example
from app.api.v1.schemas.demo.example_schema import ExampleCreate, ExampleUpdate

class ExampleCrud:
    @staticmethod
    def get_by_id(db: Session, id: int):
        return db.query(Example).filter(Example.id == id).first()
    
    @staticmethod
    def get_list(db: Session, skip: int = 0, limit: int = 100, **filters):
        query = db.query(Example)
        
        # 应用过滤条件
        for key, value in filters.items():
            if value:
                query = query.filter(getattr(Example, key).like(f"%{value}%"))
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, example: ExampleCreate):
        db_example = Example(**example.model_dump())
        db.add(db_example)
        db.commit()
        db.refresh(db_example)
        return db_example
    
    @staticmethod
    def update(db: Session, db_example: Example, example: ExampleUpdate):
        update_data = example.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_example, key, value)
        db.commit()
        db.refresh(db_example)
        return db_example
    
    @staticmethod
    def delete(db: Session, id: int):
        db_example = db.query(Example).filter(Example.id == id).first()
        if db_example:
            db.delete(db_example)
            db.commit()
            return True
        return False

# 5. 创建服务文件
# app/api/v1/services/demo/example_service.py
from sqlalchemy.orm import Session
from app.api.v1.cruds.demo.example_crud import ExampleCrud
from app.api.v1.schemas.demo.example_schema import ExampleCreate, ExampleUpdate
from app.api.v1.params.demo.example_param import ExampleParams

class ExampleService:
    @staticmethod
    def get_example(db: Session, id: int):
        return ExampleCrud.get_by_id(db, id)
    
    @staticmethod
    def get_example_list(db: Session, params: ExampleParams):
        return ExampleCrud.get_list(
            db, 
            skip=params.skip, 
            limit=params.limit,
            name=params.name,
            description=params.description
        )
    
    @staticmethod
    def create_example(db: Session, example: ExampleCreate):
        return ExampleCrud.create(db, example)
    
    @staticmethod
    def update_example(db: Session, id: int, example: ExampleUpdate):
        db_example = ExampleCrud.get_by_id(db, id)
        if not db_example:
            return None
        return ExampleCrud.update(db, db_example, example)
    
    @staticmethod
    def delete_example(db: Session, id: int):
        return ExampleCrud.delete(db, id)

# 6. 创建控制器文件
# app/api/v1/controllers/demo/example_controller.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.schemas.demo.example_schema import ExampleCreate, ExampleUpdate, ExampleResponse
from app.api.v1.params.demo.example_param import ExampleParams
from app.api.v1.services.demo.example_service import ExampleService

router = APIRouter(prefix="/example", tags=["example"])

@router.get("", response_model=list[ExampleResponse])
def get_example_list(
    params: ExampleParams = Depends(),
    db: Session = Depends(get_db)
):
    examples = ExampleService.get_example_list(db, params)
    return examples

@router.get("/{id}", response_model=ExampleResponse)
def get_example(
    id: int,
    db: Session = Depends(get_db)
):
    example = ExampleService.get_example(db, id)
    if not example:
        raise HTTPException(status_code=404, detail="Example not found")
    return example

@router.post("", response_model=ExampleResponse)
def create_example(
    example: ExampleCreate,
    db: Session = Depends(get_db)
):
    return ExampleService.create_example(db, example)

@router.put("/{id}", response_model=ExampleResponse)
def update_example(
    id: int,
    example: ExampleUpdate,
    db: Session = Depends(get_db)
):
    updated_example = ExampleService.update_example(db, id, example)
    if not updated_example:
        raise HTTPException(status_code=404, detail="Example not found")
    return updated_example

@router.delete("/{id}")
def delete_example(
    id: int,
    db: Session = Depends(get_db)
):
    success = ExampleService.delete_example(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Example not found")
    return {"message": "Example deleted successfully"}

# 7. 注册路由
# app/api/v1/urls/demo/example_url.py
from fastapi import APIRouter
from app.api.v1.controllers.demo.example_controller import router as example_router

router = APIRouter()
router.include_router(example_router)

# 8. 添加到主路由
# plugin/init_app.py
from fastapi import FastAPI
from app.api.v1.urls.demo.example_url import router as example_router

def init_router(app: FastAPI):
    # 其他路由...
    app.include_router(example_router, prefix="/api/v1")

# 9. 添加到数据库迁移
# app/alembic/env.py
from app.api.v1.models.demo.example_model import Example
# 在 target_metadata 中添加 Example
```

#### 1.2 使用依赖注入

```python
# app/core/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.models.system.user_model import User
from app.core.security import ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# 使用示例
from fastapi import APIRouter, Depends
from app.api.v1.schemas.system.user_schema import UserResponse
from app.core.dependencies import get_current_active_user
from app.api.v1.models.system.user_model import User

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    return current_user
```

### 2. 前端代码示例

#### 2.1 创建新的页面

```vue
<!-- src/views/demo/example/index.vue -->
<template>
  <div class="example-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>示例管理</span>
          <el-button type="primary" @click="handleAdd">添加</el-button>
        </div>
      </template>
      
      <!-- 搜索表单 -->
      <el-form :inline="true" :model="searchForm" class="mb-4">
        <el-form-item label="名称">
          <el-input v-model="searchForm.name" placeholder="请输入名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="searchForm.description" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 数据表格 -->
      <el-table v-loading="loading" :data="exampleList" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 添加/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle">
      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" placeholder="请输入描述" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { exampleApi } from '@/api/demo/example';
import type { Example } from '@/api/demo/example';

// 搜索表单
const searchForm = reactive({
  name: '',
  description: ''
});

// 分页
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
});

// 数据
const exampleList = ref<Example[]>([]);
const loading = ref(false);

// 对话框
const dialogVisible = ref(false);
const dialogTitle = ref('添加示例');
const form = reactive({
  id: 0,
  name: '',
  description: ''
});
const formRef = ref();

// 验证规则
const rules = {
  name: [{ required: true, message: '请输入名称', trigger: 'blur' }]
};

// 加载数据
const loadData = async () => {
  loading.value = true;
  try {
    const res = await exampleApi.getList({
      page: pagination.currentPage,
      page_size: pagination.pageSize,
      ...searchForm
    });
    exampleList.value = res.data.items;
    pagination.total = res.data.total;
  } catch (error) {
    console.error('Failed to load examples:', error);
  } finally {
    loading.value = false;
  }
};

// 搜索
const handleSearch = () => {
  pagination.currentPage = 1;
  loadData();
};

// 重置
const resetForm = () => {
  searchForm.name = '';
  searchForm.description = '';
  pagination.currentPage = 1;
  loadData();
};

// 分页变化
const handleSizeChange = (size: number) => {
  pagination.pageSize = size;
  loadData();
};

const handleCurrentChange = (current: number) => {
  pagination.currentPage = current;
  loadData();
};

// 添加
const handleAdd = () => {
  dialogTitle.value = '添加示例';
  form.id = 0;
  form.name = '';
  form.description = '';
  dialogVisible.value = true;
};

// 编辑
const handleEdit = (row: Example) => {
  dialogTitle.value = '编辑示例';
  form.id = row.id;
  form.name = row.name;
  form.description = row.description;
  dialogVisible.value = true;
};

// 删除
const handleDelete = async (id: number) => {
  try {
    await exampleApi.delete(id);
    loadData();
  } catch (error) {
    console.error('Failed to delete example:', error);
  }
};

// 提交
const handleSubmit = async () => {
  if (!formRef.value) return;
  
  try {
    await formRef.value.validate();
    
    if (form.id) {
      // 编辑
      await exampleApi.update(form.id, form);
    } else {
      // 添加
      await exampleApi.create(form);
    }
    
    dialogVisible.value = false;
    loadData();
  } catch (error) {
    console.error('Failed to submit form:', error);
  }
};

// 初始化
onMounted(() => {
  loadData();
});
</script>

<style scoped>
.example-container {
  padding: 20px;
}

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

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}
</style>
```

#### 2.2 API调用示例

```typescript
// src/api/demo/example.ts
import request from '@/utils/request';

export interface Example {
  id: number;
  name: string;
  description: string;
  created_at: string;
  updated_at: string;
}

export interface ExampleListResponse {
  items: Example[];
  total: number;
  page: number;
  page_size: number;
}

export const exampleApi = {
  // 获取示例列表
  getList: (params: any) => {
    return request<ExampleListResponse>({
      url: '/api/v1/example',
      method: 'GET',
      params
    });
  },
  
  // 获取单个示例
  getOne: (id: number) => {
    return request<Example>({
      url: `/api/v1/example/${id}`,
      method: 'GET'
    });
  },
  
  // 创建示例
  create: (data: any) => {
    return request<Example>({
      url: '/api/v1/example',
      method: 'POST',
      data
    });
  },
  
  // 更新示例
  update: (id: number, data: any) => {
    return request<Example>({
      url: `/api/v1/example/${id}`,
      method: 'PUT',
      data
    });
  },
  
  // 删除示例
  delete: (id: number) => {
    return request({
      url: `/api/v1/example/${id}`,
      method: 'DELETE'
    });
  }
};
```

### 3. 移动端代码示例

#### 3.1 页面示例

```vue
<!-- src/pages/example/index.vue -->
<template>
  <view class="page">
    <view class="header">
      <text class="title">示例页面</text>
    </view>
    
    <view class="content">
      <!-- 搜索框 -->
      <view class="search-bar">
        <input 
          v-model="searchKeyword" 
          type="text" 
          placeholder="请输入搜索关键词"
          class="search-input"
        />
        <button type="primary" @click="handleSearch" class="search-button">搜索</button>
      </view>
      
      <!-- 示例列表 -->
      <view class="example-list">
        <view 
          v-for="item in exampleList" 
          :key="item.id"
          class="example-item"
          @click="handleItemClick(item)"
        >
          <view class="item-title">{{ item.name }}</view>
          <view class="item-description">{{ item.description }}</view>
          <view class="item-time">{{ formatTime(item.created_at) }}</view>
        </view>
        
        <!-- 空状态 -->
        <view v-if="exampleList.length === 0" class="empty-state">
          <text>暂无数据</text>
        </view>
      </view>
      
      <!-- 加载更多 -->
      <view v-if="loading" class="loading">
        <text>加载中...</text>
      </view>
    </view>
    
    <!-- 底部按钮 -->
    <view class="footer">
      <button type="primary" @click="handleAdd" class="add-button">添加示例</button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { exampleApi } from '@/api/example';
import type { Example } from '@/api/example';

// 搜索关键词
const searchKeyword = ref('');

// 示例列表
const exampleList = ref<Example[]>([]);

// 加载状态
const loading = ref(false);

// 搜索
const handleSearch = async () => {
  loading.value = true;
  try {
    const res = await exampleApi.getList({
      keyword: searchKeyword.value
    });
    exampleList.value = res.data.items;
  } catch (error) {
    console.error('搜索失败:', error);
  } finally {
    loading.value = false;
  }
};

// 点击示例项
const handleItemClick = (item: Example) => {
  // 跳转到详情页
  uni.navigateTo({
    url: `/pages/example/detail?id=${item.id}`
  });
};

// 添加示例
const handleAdd = () => {
  // 跳转到添加页面
  uni.navigateTo({
    url: '/pages/example/add'
  });
};

// 格式化时间
const formatTime = (time: string) => {
  const date = new Date(time);
  return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
};

// 加载数据
const loadData = async () => {
  loading.value = true;
  try {
    const res = await exampleApi.getList({});
    exampleList.value = res.data.items;
  } catch (error) {
    console.error('加载数据失败:', error);
  } finally {
    loading.value = false;
  }
};

// 初始化
onMounted(() => {
  loadData();
});
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.header {
  background-color: #007aff;
  color: #fff;
  padding: 20rpx;
  text-align: center;
}

.title {
  font-size: 32rpx;
  font-weight: bold;
}

.content {
  padding: 20rpx;
}

.search-bar {
  display: flex;
  margin-bottom: 20rpx;
}

.search-input {
  flex: 1;
  border: 1rpx solid #ddd;
  border-radius: 8rpx;
  padding: 15rpx;
  margin-right: 10rpx;
  background-color: #fff;
}

.search-button {
  width: 120rpx;
}

.example-list {
  background-color: #fff;
  border-radius: 8rpx;
  overflow: hidden;
}

.example-item {
  padding: 20rpx;
  border-bottom: 1rpx solid #eee;
}

.example-item:last-child {
  border-bottom: none;
}

.item-title {
  font-size: 28rpx;
  font-weight: bold;
  margin-bottom: 10rpx;
}

.item-description {
  font-size: 24rpx;
  color: #666;
  margin-bottom: 10rpx;
}

.item-time {
  font-size: 20rpx;
  color: #999;
}

.empty-state {
  padding: 100rpx 0;
  text-align: center;
  color: #999;
}

.loading {
  padding: 20rpx 0;
  text-align: center;
  color: #666;
}

.footer {
  padding: 20rpx;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #f5f5f5;
  border-top: 1rpx solid #eee;
}

.add-button {
  width: 100%;
}
</style>
```

## 🚀使用案例

### 1. 企业内部管理系统

#### 1.1 需求分析

- **用户管理**：员工信息管理、角色权限管理
- **部门管理**：部门结构管理、人员调动
- **考勤管理**：打卡记录、请假审批
- **审批流程**：请假、报销、加班等审批
- **数据统计**：员工数据、考勤数据统计分析

#### 1.2 技术实现

- **后端**：使用 FastapiAdmin 提供的用户、角色、权限等模块，扩展考勤和审批模块
- **前端**：使用 ElementPlus 构建管理界面，实现数据表格、表单、流程等组件
- **移动端**：使用 FastApp 实现员工打卡、审批查看等功能

#### 1.3 部署方案

- **生产环境**：使用 Docker Compose 部署，包含后端、前端、MySQL、Redis、Nginx
- **监控**：使用 Prometheus + Grafana 监控系统状态
- **备份**：定期备份数据库和配置文件

### 2. 电商后台管理系统

#### 2.1 需求分析

- **商品管理**：商品分类、商品信息、库存管理
- **订单管理**：订单处理、物流跟踪、退款管理
- **用户管理**：客户信息、会员等级、积分管理
- **营销管理**：优惠券、活动管理、数据分析
- **统计报表**：销售数据、用户数据、商品数据统计

#### 2.2 技术实现

- **后端**：基于 FastapiAdmin 扩展商品、订单、营销等模块
- **前端**：使用 ElementPlus 构建管理界面，实现商品列表、订单处理等功能
- **移动端**：使用 FastApp 实现商家查看订单、管理商品等功能

#### 2.3 部署方案

- **生产环境**：使用云服务器部署，采用负载均衡架构
- **数据库**：使用主从复制提高可靠性
- **缓存**：使用 Redis 缓存热点数据，提高响应速度
- **CDN**：使用 CDN 加速静态文件传输

### 3. 内容管理系统

#### 3.1 需求分析

- **内容管理**：文章、图片、视频等内容管理
- **分类管理**：内容分类、标签管理
- **用户管理**：作者、编辑、审核员等角色管理
- **审核流程**：内容发布审核流程
- **统计分析**：内容阅读量、用户活跃度等统计

#### 3.2 技术实现

- **后端**：基于 FastapiAdmin 扩展内容、分类等模块
- **前端**：使用 ElementPlus 构建管理界面，实现富文本编辑器、媒体库等功能
- **移动端**：使用 FastApp 实现作者查看文章状态、编辑文章等功能

#### 3.3 部署方案

- **生产环境**：使用容器化部署，便于横向扩展
- **存储**：使用对象存储服务存储媒体文件
- **搜索**：集成 Elasticsearch 实现全文搜索
- **监控**：使用 ELK Stack 收集和分析日志

## 🔧最佳实践

### 1. 代码规范

#### 1.1 后端代码规范

- **命名规范**：使用 snake_case 命名变量和函数，使用 PascalCase 命名类
- **代码风格**：遵循 PEP 8 代码风格指南
- **类型注解**：使用类型注解提高代码可读性和可维护性
- **错误处理**：使用 try-except 捕获异常，返回统一的错误格式
- **日志记录**：使用结构化日志，记录关键操作和错误信息

#### 1.2 前端代码规范

- **命名规范**：使用 camelCase 命名变量和函数，使用 PascalCase 命名组件
- **代码风格**：遵循 ESLint 和 Prettier 配置
- **类型注解**：使用 TypeScript 类型注解
- **组件设计**：遵循单一职责原则，组件拆分合理
- **状态管理**：使用 Pinia 管理全局状态，合理使用组件状态

### 2. 性能优化

#### 2.1 后端优化

- **数据库优化**：使用索引、优化查询语句、合理使用缓存
- **API 优化**：使用分页、限流、缓存等技术
- **代码优化**：减少不必要的计算和IO操作
- **并发优化**：合理使用异步编程，提高并发处理能力

#### 2.2 前端优化

- **资源优化**：使用代码分割、懒加载、压缩等技术
- **渲染优化**：减少 DOM 操作，使用虚拟列表，合理使用缓存
- **网络优化**：使用 HTTP/2、HTTPS、CDN 等技术
- **状态管理优化**：合理使用全局状态，避免不必要的重渲染

### 3. 安全最佳实践

#### 3.1 后端安全

- **认证授权**：使用 JWT 认证，实现细粒度的权限控制
- **输入验证**：使用 Pydantic 进行数据验证，防止注入攻击
- **密码安全**：使用 bcrypt 等算法加密存储密码
- **CORS 配置**：合理配置 CORS 策略，防止跨站请求伪造
- **敏感信息保护**：避免在日志中记录敏感信息，使用环境变量存储配置

#### 3.2 前端安全

- **XSS 防护**：使用 Vue 的自动转义功能，避免直接操作 DOM
- **CSRF 防护**：使用 token 验证，防止跨站请求伪造
- **敏感信息保护**：不在前端存储敏感信息，使用 HTTPS 传输数据
- **依赖安全**：定期更新依赖包，避免使用有安全漏洞的依赖

## 📚参考资源

- **FastAPI 官方文档**：[https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **Vue 3 官方文档**：[https://v3.vuejs.org/](https://v3.vuejs.org/)
- **ElementPlus 官方文档**：[https://element-plus.org/](https://element-plus.org/)
- **Uni App 官方文档**：[https://uniapp.dcloud.io/](https://uniapp.dcloud.io/)
- **TypeScript 官方文档**：[https://www.typescriptlang.org/](https://www.typescriptlang.org/)
- **Docker 官方文档**：[https://docs.docker.com/](https://docs.docker.com/)
- **Nginx 官方文档**：[https://nginx.org/en/docs/](https://nginx.org/en/docs/)

## 🤝常见问题

### 1. 如何快速创建新的 API 模块？

**解决方案**：
- 使用 FastapiAdmin 提供的代码生成工具
- 参考示例代码，按照标准流程创建模型、Schema、CRUD、服务、控制器等文件
- 注册路由并添加到数据库迁移

### 2. 如何处理跨域问题？

**解决方案**：
- 在后端配置 CORS 中间件
- 在前端使用代理服务器
- 使用 JSONP 或 WebSocket 等技术

### 3. 如何优化数据库查询性能？

**解决方案**：
- 添加合适的索引
- 优化查询语句，避免全表扫描
- 使用分页查询，限制返回数据量
- 合理使用缓存，减少数据库查询次数

### 4. 如何实现文件上传功能？

**解决方案**：
- 使用 FastAPI 的 File 上传功能
- 配置文件存储路径和权限
- 实现文件上传、下载、删除等 API
- 前端使用 FormData 上传文件

### 5. 如何实现定时任务？

**解决方案**：
- 使用 APScheduler 库实现定时任务
- 配置任务调度器，设置任务执行时间和频率
- 实现任务函数，处理具体业务逻辑
- 监控任务执行状态和结果

## 📄许可协议

FastapiAdmin 项目采用 MIT 许可协议，详见 [LICENSE](https://github.com/fastapiadmin/FastapiAdmin/blob/master/LICENSE) 文件。
