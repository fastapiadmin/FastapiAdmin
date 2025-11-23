# Sass多租户平台数据隔离与权限设计方案

## 1. 整体架构设计

### 1.1 核心数据隔离模型

我们采用了基于租户的多层级数据隔离架构：

- **租户层(tenant)**: 最高级别的数据隔离，所有业务数据都关联到特定租户
- **客户层(customer)**: 租户内的次级隔离，用于分离不同客户的数据
- **部门层(dept)**: 租户内部的组织结构，用于实现基于部门的数据权限
- **用户层(user)**: 最终的数据访问主体，通过角色定义其权限范围

### 1.2 实体关系图

```
Tenant (租户)
  ├── 1:N ── User (用户)
  ├── 1:N ── Dept (部门)
  └── 1:N ── Customer (客户)

Customer
  └── 1:N ── User (客户用户)

User
  ├── N:M ── Role (角色)
  └── N:1 ── Dept (部门)

Role
  ├── N:M ── Menu (功能菜单)
  └── N:M ── Dept (自定义数据权限)

Dept
  └── 树状结构 ── Dept (子部门)
```

## 2. 数据隔离实现

### 2.1 租户级隔离

- 所有业务表通过`tenant_id`字段关联到租户
- 系统租户(tenant_id=1)管理所有其他租户
- 普通租户只能访问自己的数据
- 实现方式：查询时自动添加`tenant_id`过滤条件

### 2.2 客户级隔离

- 客户属于特定租户(tenant_id)
- 客户用户通过`customer_id`关联到客户
- 客户用户只能访问其所属客户的数据
- 实现方式：为客户用户的数据查询添加`customer_id`过滤条件

### 2.3 用户类型定义

- **系统用户** (user_type=0): 属于系统租户(tenant_id=1)，无客户关联
- **租户用户** (user_type=1): 属于特定租户(tenant_id>1)，无客户关联
- **租户客户用户** (user_type=3): 属于特定租户下的特定客户(tenant_id>1, customer_id>1)

## 3. 数据权限实现

### 3.1 角色数据权限范围

通过`role`表的`data_scope`字段实现五种数据权限：

1. **仅本人数据权限** (data_scope='1')
   - 只能查看自己创建的数据
   - 实现：添加`created_id = current_user.id`过滤条件

2. **本部门数据权限** (data_scope='2')
   - 只能查看同部门的数据
   - 实现：通过查询部门内所有用户，然后过滤`created_id IN (部门用户ID列表)`

3. **本部门及以下数据权限** (data_scope='3')
   - 可以查看本部门及所有子部门的数据
   - 实现：递归获取所有子部门ID，然后通过部门ID列表过滤或通过部门用户ID列表过滤

4. **全部数据权限** (data_scope='4')
   - 可以查看租户内所有数据
   - 实现：只添加`tenant_id`过滤条件，不添加额外权限过滤

5. **自定义数据权限** (data_scope='5')
   - 通过`role_dept_relation`表定义可访问的部门列表
   - 实现：获取角色关联的所有部门ID，然后通过部门ID列表过滤或部门用户ID列表过滤

### 3.2 数据权限统一实现

我们创建了统一的数据权限混入类`DataPermissionMixin`，为所有业务模型提供权限过滤功能：

```python
class DataPermissionMixin:
    # 获取带有数据权限过滤的查询对象
    @classmethod
    def get_data_permission_query(cls, db, user_id, tenant_id=None, customer_id=None):
        # 实现权限过滤逻辑
        pass
    
    # 检查用户是否有权限访问特定记录
    @classmethod
    def has_permission_to_access(cls, db, user_id, record_id):
        # 实现单条记录权限检查
        pass
```

所有需要数据权限控制的业务模型只需继承此混入类，即可获得权限过滤功能。

### 3.3 部门层级结构实现

- 部门通过`parent_id`实现无限层级嵌套的树形结构
- 使用递归查询获取部门的所有子部门
- 为提升性能，考虑在后续版本中添加`tree_path`字段存储层级路径

### 3.3 权限过滤实现建议

在数据访问层实现统一的权限过滤机制：

```python
# 伪代码示例
def apply_data_scope(query, current_user):
    # 1. 首先应用租户过滤
    query = query.filter(Model.tenant_id == current_user.tenant_id)
    
    # 2. 如果是客户用户，应用客户过滤
    if current_user.user_type == 2 and current_user.customer_id:
        query = query.filter(Model.customer_id == current_user.customer_id)
    
    # 3. 获取用户的最大数据权限范围
    data_scope = get_max_data_scope(current_user.roles)
    
    # 4. 应用数据权限过滤
    if data_scope == '1':  # 仅本人
        query = query.filter(Model.created_id == current_user.id)
    elif data_scope == '2':  # 本部门
        query = query.filter(Model.dept_id == current_user.dept_id)
    elif data_scope == '3':  # 本部门及以下
        dept = get_dept_by_id(current_user.dept_id)
        query = query.filter(Model.tree_path.like(f"{dept.tree_path}%"))
    elif data_scope == '5':  # 自定义
        dept_ids = get_custom_dept_ids(current_user.roles)
        query = query.filter(Model.dept_id.in_(dept_ids))
    # data_scope == '4' 时不过滤
    
    return query
```

## 4. 已修正的模型设计

### 4.1 BaseModel修改

- 优化了基础模型设计，同时包含`tenant_id`和`customer_id`字段
- 所有表默认继承这两个字段，支持完整的租户-客户数据隔离
- 通过ORM外键关联确保数据完整性
- 添加了UUID支持和通用的`to_dict`方法，便于数据序列化

### 4.2 客户模型修改

- 移除了客户之间的自关联关系，避免循环依赖
- 客户表专注于存储客户基本信息
- 明确了客户属于特定租户

### 4.3 用户模型修改

- 定义了三种用户类型：系统用户(0)、租户用户(1)、租户客户用户(3)
- 客户用户通过`customer_id`关联到特定客户
- 优化了外键定义，使用字符串引用避免循环导入
- 为关键字段添加了索引，提升查询性能
- 明确了用户与租户、客户、部门的关系定义

### 4.4 角色模型修改

- 优化了`data_scope`字段，使用字符串类型以便于理解
- 明确了五种数据权限的实现方式
- 保留了角色与部门的多对多关系，支持自定义数据权限

### 4.5 部门模型修改

- 优化了部门层级结构设计
- 添加了`tree_path`字段，提高层级查询性能
- 明确了部门属于特定租户

### 4.6 租户模型修改

- 简化了租户模型，移除了重复字段和不必要的关联
- 明确了租户作为数据隔离基础的角色
- 添加了必要的租户属性（名称、编码、域名、过期时间等）

## 5. 数据访问最佳实践

### 5.1 统一的数据权限过滤

- 使用`DataPermissionMixin`为所有业务模型提供统一的权限过滤功能
- 在业务层直接调用`get_data_permission_query`方法获取已过滤的查询对象
- 为所有CRUD操作添加权限检查，确保数据安全

### 5.2 性能优化

- 为`tenant_id`, `customer_id`, `dept_id`等关键字段创建索引
- 使用SQLAlchemy的延迟加载和预加载优化关联查询
- 避免在大型数据集上进行复杂的权限计算，考虑使用缓存机制

### 5.3 安全建议

- 使用ORM的参数化查询，避免SQL注入风险
- 在API层进行权限校验，而不仅仅是在数据访问层
- 对敏感操作（如删除、修改）进行日志记录和审计
- 实现数据变更的操作日志，记录操作者和变更内容

## 6. 扩展建议

### 6.1 动态数据权限

- 实现基于字段级的数据权限控制
- 支持更细粒度的数据访问规则定义

### 6.2 多维度权限

- 考虑添加基于项目、产品线等其他维度的数据权限
- 实现权限组合机制，满足复杂业务场景

### 6.3 性能优化

- 对于大型租户，考虑分库分表策略
- 实现数据缓存机制，减轻数据库压力

---

本设计方案通过清晰的层级结构和权限定义，实现了Sass平台中复杂的数据隔离和权限管理需求。通过标准化的实现方式，可以有效确保数据安全和访问控制的正确性。