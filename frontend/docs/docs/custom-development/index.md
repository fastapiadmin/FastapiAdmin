# FastAPI Admin 二次开发手册

## 1. 项目概述

FastAPI Admin 是一个基于 FastAPI 框架开发的后台管理系统，具有完善的权限控制系统和模块化架构。本手册将指导您如何进行二次开发，特别是创建数据、实现权限控制和支持分页查询功能。

## 2. 核心架构

### 2.1 目录结构

```
backend/
├── app/
│   ├── api/                    # API 路由层
│   │   └── v1/                 # API 版本
│   │       └── module_xxx/     # 业务模块
│   │           ├── model.py    # 数据模型
│   │           ├── schema.py   # 请求/响应模型
│   │           ├── crud.py     # 数据操作层
│   │           ├── service.py  # 业务逻辑层
│   │           └── controller.py # API 控制器
│   ├── core/                   # 核心功能
│   │   ├── base_model.py       # 基础数据模型
│   │   ├── base_crud.py        # 基础数据操作
│   │   ├── permission.py       # 权限控制
│   │   └── ...
│   └── ...
└── ...
```

### 2.2 技术栈

- **Web框架**: FastAPI
- **ORM**: SQLAlchemy 2.0
- **数据库**: 支持 PostgreSQL/MySQL/SQLite
- **权限控制**: RBAC (基于角色的访问控制)
- **文档**: Swagger UI/ReDoc

## 3. 创建数据模型

### 3.1 基础模型继承

所有数据模型都应继承自 `ModelMixin` 和 `UserMixin`，这两个类提供了基础字段和权限支持：

```python
# app/api/v1/module_xxx/model.py
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class XXXModel(ModelMixin, UserMixin):
    """
    XXX模块数据模型
    """
    __tablename__: str = 'xxx_table_name'
    __table_args__: dict[str, str] = ({'comment': 'XXX表'})
    __loader_options__: list[str] = ["created_by", "updated_by"]  # 预加载关系

    # 自定义字段
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment='名称')
    value: Mapped[int] = mapped_column(Integer, default=0, comment='数值')
    # 更多字段...
```

### 3.2 模型字段说明

- `ModelMixin` 提供：`id`, `uuid`, `status`, `description`, `created_time`, `updated_time`
- `UserMixin` 提供：`created_id`, `updated_id`, `created_by`, `updated_by`

## 4. 实现权限控制

### 4.1 权限系统概述

系统实现了基于角色的数据权限控制，支持五种数据权限范围：

1. **仅本人数据 (1)**: 只能查看自己创建的数据
2. **本部门数据 (2)**: 只能查看同部门的数据
3. **本部门及以下 (3)**: 可以查看本部门及所有子部门的数据
4. **全部数据 (4)**: 可以查看所有数据
5. **自定义数据 (5)**: 通过角色关联的部门列表定义可访问的部门

### 4.2 权限自动应用

通过继承 `CRUDBase` 类，权限控制会自动应用到所有数据操作中：

```python
# app/api/v1/module_xxx/crud.py
from app.core.base_crud import CRUDBase
from app.api.v1.module_system.auth.schema import AuthSchema
from .model import XXXModel
from .schema import XXXCreateSchema, XXXUpdateSchema


class XXXCRUD(CRUDBase[XXXModel, XXXCreateSchema, XXXUpdateSchema]):
    """XXX数据操作层"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化"""
        self.auth = auth
        super().__init__(model=XXXModel, auth=auth)
```

### 4.3 权限检查流程

权限检查在 `permission.py` 中的 `__permission_condition` 方法实现：

1. 检查是否为超级管理员
2. 获取用户所有角色的数据权限范围
3. 合并权限范围（取最宽松权限）
4. 构造查询条件
5. 应用到所有查询中

## 5. 支持分页查询

### 5.1 分页实现

系统提供了两种分页实现方式：

#### 5.1.1 使用 base_crud 中的 page 方法

```python
# 在 service.py 中
from app.api.v1.module_system.auth.schema import AuthSchema
from .schema import XXXCreateSchema, XXXUpdateSchema, XXXOutSchema
from .crud import XXXCRUD

async def page_service(cls, auth: AuthSchema, offset: int, limit: int, search: dict) -> dict:
    """分页查询"""
    crud = XXXCRUD(auth)
    return await crud.page(
        offset=offset, 
        limit=limit, 
        order_by=[{'id': 'asc'}], 
        search=search, 
        out_schema=XXXOutSchema
    )
```

#### 5.1.2 使用 PaginationService

```python
# 在 controller.py 中
from fastapi import APIRouter, Depends
from app.common.request import PaginationService
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.api.v1.module_system.auth.schema import AuthSchema
from .service import XXXService
from .schema import XXXQueryParam

@XXXRouter.get("/list", summary="查询列表")
async def get_obj_list_controller(
    page: PaginationQueryParam = Depends(),
    search: XXXQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_xxx:query"]))
) -> JSONResponse:
    """查询列表"""
    result_dict_list = await XXXService.list_service(auth=auth, search=search, order_by=page.order_by)
    result_dict = await PaginationService.paginate(data_list=result_dict_list, page_no=page.page_no, page_size=page.page_size)
    return SuccessResponse(data=result_dict, msg="查询成功")
```

### 5.2 分页参数

分页查询支持以下参数：

- `page_no`: 页码（默认 1）
- `page_size`: 每页条数（默认 10）
- `order_by`: 排序字段（如 `[{"id": "asc"}, {"name": "desc"}]`）

### 5.3 分页响应格式

```json
{
  "code": 200,
  "data": {
    "page_no": 1,
    "page_size": 10,
    "total": 100,
    "has_next": true,
    "items": [
      {"id": 1, "name": "示例1", ...},
      // 更多数据...
    ]
  },
  "msg": "查询成功"
}
```

## 6. 完整开发流程示例

下面以创建一个 `Task` 任务模块为例，演示完整的开发流程。

### 6.1 创建数据模型

```python
# app/api/v1/module_xxx/task/model.py
from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class TaskModel(ModelMixin, UserMixin):
    """
    任务数据模型
    """
    __tablename__: str = 'task'
    __table_args__: dict[str, str] = ({'comment': '任务表'})
    __loader_options__: list[str] = ["created_by", "updated_by"]

    title: Mapped[str] = mapped_column(String(128), nullable=False, comment='任务标题')
    content: Mapped[str] = mapped_column(Text, nullable=True, comment='任务内容')
    priority: Mapped[int] = mapped_column(Integer, default=3, comment='优先级：1-高，2-中，3-低')
    status: Mapped[str] = mapped_column(String(10), default='0', comment='状态：0-待处理，1-进行中，2-已完成')
```

### 6.2 创建请求/响应模型

```python
# app/api/v1/module_xxx/task/schema.py
from pydantic import BaseModel, Field
from app.core.base_schema import BaseSchema, UserBySchema


class TaskCreateSchema(BaseModel):
    """任务创建模型"""
    title: str = Field(..., max_length=128, description='任务标题')
    content: str | None = Field(None, description='任务内容')
    priority: int = Field(3, ge=1, le=3, description='优先级')
    status: str = Field("0", description='状态')
    description: str | None = Field(None, description='描述')


class TaskUpdateSchema(TaskCreateSchema):
    """任务更新模型"""
    ...


class TaskOutSchema(TaskCreateSchema, BaseSchema, UserBySchema):
    """任务响应模型"""
    model_config = {
        "from_attributes": True
    }


class TaskQueryParam:
    """任务查询参数"""
    def __init__(
        self,
        title: str | None = None,
        priority: int | None = None,
        status: str | None = None,
        # 更多查询参数...
    ) -> None:
        self.title = ("like", title) if title else None
        self.priority = priority
        self.status = status
        # 更多查询参数处理...
```

### 6.3 创建数据操作层

```python
# app/api/v1/module_xxx/task/crud.py
from app.core.base_crud import CRUDBase
from app.api.v1.module_system.auth.schema import AuthSchema
from .model import TaskModel
from .schema import TaskCreateSchema, TaskUpdateSchema


class TaskCRUD(CRUDBase[TaskModel, TaskCreateSchema, TaskUpdateSchema]):
    """任务数据操作层"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化"""
        self.auth = auth
        super().__init__(model=TaskModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> TaskModel | None:
        """根据ID获取任务"""
        return await self.get(id=id)

    async def create_crud(self, data: TaskCreateSchema) -> TaskModel:
        """创建任务"""
        return await self.create(data=data)

    # 更多数据操作方法...
```

### 6.4 创建业务逻辑层

```python
# app/api/v1/module_xxx/task/service.py
from app.core.exceptions import CustomException
from app.api.v1.module_system.auth.schema import AuthSchema
from .schema import TaskCreateSchema, TaskUpdateSchema, TaskOutSchema, TaskQueryParam
from .crud import TaskCRUD


class TaskService:
    """任务业务逻辑层"""

    @classmethod
    async def create_service(cls, auth: AuthSchema, data: TaskCreateSchema) -> dict:
        """创建任务"""
        # 业务逻辑验证
        if len(data.title) < 2:
            raise CustomException(msg='任务标题至少2个字符')
        
        # 创建任务
        obj = await TaskCRUD(auth).create_crud(data=data)
        return TaskOutSchema.model_validate(obj).model_dump()

    @classmethod
    async def page_service(cls, auth: AuthSchema, offset: int, limit: int, search: dict) -> dict:
        """分页查询任务"""
        return await TaskCRUD(auth).page(
            offset=offset,
            limit=limit,
            order_by=[{'id': 'desc'}],
            search=search,
            out_schema=TaskOutSchema
        )

    # 更多业务逻辑方法...
```

### 6.5 创建API控制器

```python
# app/api/v1/module_xxx/task/controller.py
from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse

from app.common.response import SuccessResponse
from app.core.base_params import PaginationQueryParam
from app.core.dependencies import AuthPermission
from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.router_class import OperationLogRoute
from .service import TaskService
from .schema import TaskCreateSchema, TaskQueryParam


TaskRouter = APIRouter(route_class=OperationLogRoute, prefix="/task", tags=["任务管理"])


@TaskRouter.post("/create", summary="创建任务")
async def create_task_controller(
    data: TaskCreateSchema = Body(...),
    auth: AuthSchema = Depends(AuthPermission(["module_xxx:task:create"]))
) -> JSONResponse:
    """创建任务"""
    result = await TaskService.create_service(auth=auth, data=data)
    return SuccessResponse(data=result, msg="创建任务成功")


@TaskRouter.get("/page", summary="分页查询任务")
async def page_task_controller(
    page: PaginationQueryParam = Depends(),
    search: TaskQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_xxx:task:query"]))
) -> JSONResponse:
    """分页查询任务"""
    search_dict = {k: v for k, v in search.__dict__.items() if v is not None}
    result = await TaskService.page_service(
        auth=auth,
        offset=(page.page_no - 1) * page.page_size,
        limit=page.page_size,
        search=search_dict
    )
    return SuccessResponse(data=result, msg="查询任务成功")

# 更多API端点...
```

### 6.6 注册路由

确保在模块的 `__init__.py` 中导出路由：

```python
# app/api/v1/module_xxx/__init__.py
from .task.controller import TaskRouter

__all__ = ["TaskRouter"]
```

然后在应用的路由注册中包含该模块：

```python
# app/api/v1/__init__.py
from .module_xxx import TaskRouter

# 注册到总路由
```

## 7. 权限配置

### 7.1 角色数据权限

在角色管理中设置数据权限范围：

- 数据权限 = 1: 仅本人数据
- 数据权限 = 2: 本部门数据
- 数据权限 = 3: 本部门及以下数据
- 数据权限 = 4: 全部数据
- 数据权限 = 5: 自定义数据（通过角色-部门关联设置）

### 7.2 API权限

在菜单管理中配置API权限：

- 权限标识格式：`module_xxx:yyy:zzz`
  - `module_xxx`: 模块名称
  - `yyy`: 功能名称
  - `zzz`: 操作类型（create, update, delete, query, detail）

## 8. 开发注意事项

1. **数据模型继承**：所有业务模型必须继承 `ModelMixin` 和 `UserMixin`
2. **权限控制**：使用 `CRUDBase` 类自动应用权限过滤
3. **分页查询**：使用 `page` 方法获取分页数据
4. **预加载关系**：在模型中设置 `__loader_options__` 定义默认预加载关系
5. **异常处理**：使用 `CustomException` 抛出业务异常
6. **日志记录**：使用 `log.info()` 记录关键操作

## 9. 测试与部署

### 9.1 开发环境启动

```bash
python main.py run --env=dev
```

### 9.2 数据库迁移

```bash
# 生成迁移脚本
python main.py revision --env=dev

# 应用迁移
python main.py upgrade --env=dev
```

### 9.3 文档访问

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 10. 总结

本手册介绍了 FastAPI Admin 二次开发的核心流程，包括创建数据模型、实现权限控制和支持分页查询。通过遵循本手册的指导，您可以快速开发新的业务模块，并确保其与现有系统的兼容性和一致性。

如需更详细的开发文档，请参考代码注释和 Swagger UI 接口文档。