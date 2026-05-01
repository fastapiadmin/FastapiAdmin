# Examples

## Basic Usage

### Backend API Examples

#### User Authentication

```python
from fastapi import APIRouter, Depends, HTTPException
from fastapi_admin.models import User
from fastapi_admin.depends import get_current_user

router = APIRouter()

@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    return {"user": current_user}
```

#### CRUD Operations

```python
from fastapi import APIRouter, Depends, HTTPException
from fastapi_admin.models import Role
from fastapi_admin.depends import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_admin.database import get_db

router = APIRouter()

@router.get("/roles")
async def get_roles(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    roles = await db.query(Role).all()
    return {"roles": roles}
```

### Frontend Examples

#### Vue Component

```vue
<template>
  <div class="user-profile">
    <h2>{{ user.name }}</h2>
    <p>{{ user.email }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const user = ref({})

onMounted(async () => {
  const response = await fetch('/api/v1/profile')
  user.value = await response.json()
})
</script>
```

## Advanced Examples

### Custom Dashboard

```vue
<template>
  <div class="dashboard">
    <div class="stats">
      <div class="stat-card">
        <h3>Total Users</h3>
        <p>{{ userCount }}</p>
      </div>
      <div class="stat-card">
        <h3>Active Roles</h3>
        <p>{{ roleCount }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const userCount = ref(0)
const roleCount = ref(0)

onMounted(async () => {
  // Fetch statistics
  const response = await fetch('/api/v1/stats')
  const data = await response.json()
  userCount.value = data.userCount
  roleCount.value = data.roleCount
})
</script>
```

### Docker Compose

```yaml
version: '3'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: fastapiadmin

  redis:
    image: redis:7.0
```