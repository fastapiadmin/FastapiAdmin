---
outline: "deep"
title: Backend Development Guide
---
# Backend Development Guide

## 📋Project Overview

The backend part of FastapiAdmin is based on **Python + FastAPI + SQLAlchemy + Redis + MySQL**, providing a high-performance, scalable, and maintainable backend system.

### Core Features

- **Asynchronous Framework**: Based on FastAPI, supporting asynchronous processing for high concurrency
- **Automatic API Documentation**: Swagger UI and ReDoc automatically generated
- **Type Hints**: Full TypeScript support with Pydantic models
- **ORM Integration**: SQLAlchemy for database operations
- **Cache Support**: Redis integration for performance optimization
- **Authentication**: JWT OAuth2 authentication mechanism
- **Permission Control**: RBAC-based fine-grained permission management
- **Database Migration**: Alembic for database schema management
- **Configuration Management**: Environment-based configuration system
- **Logging**: Comprehensive logging system

## 🛠️Technology Stack

| Category | Technology | Version | Description |
|---------|------------|---------|-------------|
| **Language** | Python | >=3.10 | Programming language |
| **Framework** | FastAPI | 0.109.0 | Asynchronous web framework |
| **ORM** | SQLAlchemy | 2.0.23 | Object Relational Mapper |
| **Cache** | Redis | 4.5.4 | In-memory data store |
| **Database** | MySQL | 8.0+ | Relational database |
| **Authentication** | PyJWT | 2.6.0 | JWT token generation and verification |
| **Validation** | Pydantic | 2.5.0 | Data validation and settings management |
| **Migration** | Alembic | 1.12.1 | Database schema migration |
| **CORS** | FastAPI CORS | - | Cross-Origin Resource Sharing |
| **Dependency Injection** | FastAPI DI | - | Dependency injection system |

## 📁Project Structure

```
backend/
├── app/
│   ├── api/             # API routes and controllers
│   │   └── v1/          # API version 1
│   │       ├── controllers/  # Request handlers
│   │       ├── cruds/        # Data access layer
│   │       ├── models/       # Database models
│   │       ├── params/       # Request parameters
│   │       ├── schemas/      # Response schemas
│   │       └── urls/         # Route definitions
│   ├── core/            # Core functionality
│   │   ├── config.py     # Configuration management
│   │   ├── database.py   # Database connection
│   │   ├── security.py   # Security utilities
│   │   └── utils.py      # Common utilities
│   ├── middleware/      # Middleware
│   │   ├── cors.py       # CORS middleware
│   │   ├── jwt.py        # JWT middleware
│   │   └── logger.py     # Logging middleware
│   ├── plugins/         # Plugins and extensions
│   │   ├── init_app.py   # Application initialization
│   │   └── redis.py      # Redis plugin
│   ├── scripts/         # Scripts
│   │   ├── data/         # Initialization data
│   │   ├── alembic/      # Database migrations
│   │   ├── initialize.py # System initialization
│   │   └── main.py       # Main script
│   └── services/         # Business logic services
├── env/                 # Environment configuration files
│   ├── .env.dev         # Development environment
│   └── .env.prod        # Production environment
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── setup.py             # Package setup
└── README.md            # Backend documentation
```

## 🚀Getting Started

### Environment Setup

1. **Install Python**

   ```sh
   # macOS
   brew install python@3.10

   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3.10 python3.10-venv python3.10-dev

   # CentOS/RHEL
   sudo dnf install python3.10 python3.10-venv python3.10-devel
   ```

2. **Install MySQL and Redis**

   ```sh
   # macOS
   brew install mysql redis
   brew services start mysql redis

   # Ubuntu/Debian
   sudo apt update
   sudo apt install mysql-server redis-server
   sudo systemctl start mysql redis
   ```

### Project Setup

1. **Clone the repository**

   ```sh
   git clone https://github.com/fastapiadmin/FastapiAdmin.git
   cd FastapiAdmin/backend
   ```

2. **Create virtual environment**

   ```sh
   python3 -m venv .venv
   
   # Activate virtual environment
   # macOS/Linux
   source .venv/bin/activate
   # Windows
   .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```sh
   cp env/.env.dev.example env/.env.dev
   # Edit env/.env.dev file
   ```

5. **Initialize database**

   ```sh
   # Generate migration files
   python main.py revision "Initial migration" --env=dev

   # Apply migration
   python main.py upgrade --env=dev

   # Initialize system data
   python main.py init
   ```

6. **Start development server**

   ```sh
   python main.py run --env=dev
   ```

   The backend API will be available at `http://localhost:8001`

   API documentation will be available at:
   - Swagger UI: `http://localhost:8001/api/v1/docs`
   - ReDoc: `http://localhost:8001/api/v1/redoc`

## 📝Development Process

### 1. Creating a New Model

1. **Create model class** in `app/api/v1/models/` directory

   ```python
   # app/api/v1/models/demo/example_model.py
   from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
   from sqlalchemy.orm import relationship
   from app.core.database import Base
   from datetime import datetime

   class Example(Base):
       __tablename__ = "example"

       id = Column(Integer, primary_key=True, index=True)
       name = Column(String(100), nullable=False, index=True)
       description = Column(String(500), nullable=True)
       created_at = Column(DateTime, default=datetime.utcnow)
       updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

       # Relationships
       # relationship("OtherModel", back_populates="example")
   ```

2. **Register model** in `app/scripts/alembic/env.py`

### 2. Creating CRUD Operations

1. **Create CRUD class** in `app/api/v1/cruds/` directory

   ```python
   # app/api/v1/cruds/demo/example_crud.py
   from sqlalchemy.orm import Session
   from app.api.v1.models.demo.example_model import Example
   from app.api.v1.schemas.demo.example_schema import ExampleCreate, ExampleUpdate

   class ExampleCRUD:
       @staticmethod
       def get_by_id(db: Session, example_id: int):
           return db.query(Example).filter(Example.id == example_id).first()

       @staticmethod
       def get_list(db: Session, skip: int = 0, limit: int = 100):
           return db.query(Example).offset(skip).limit(limit).all()

       @staticmethod
       def create(db: Session, example: ExampleCreate):
           db_example = Example(**example.dict())
           db.add(db_example)
           db.commit()
           db.refresh(db_example)
           return db_example

       @staticmethod
       def update(db: Session, example_id: int, example: ExampleUpdate):
           db_example = ExampleCRUD.get_by_id(db, example_id)
           if db_example:
               update_data = example.dict(exclude_unset=True)
               for field, value in update_data.items():
                   setattr(db_example, field, value)
               db.commit()
               db.refresh(db_example)
           return db_example

       @staticmethod
       def delete(db: Session, example_id: int):
           db_example = ExampleCRUD.get_by_id(db, example_id)
           if db_example:
               db.delete(db_example)
               db.commit()
           return db_example

   example_crud = ExampleCRUD()
   ```

### 3. Creating Schemas

1. **Create schema classes** in `app/api/v1/schemas/` directory

   ```python
   # app/api/v1/schemas/demo/example_schema.py
   from pydantic import BaseModel, Field
   from datetime import datetime
   from typing import Optional

   class ExampleBase(BaseModel):
       name: str = Field(..., min_length=1, max_length=100)
       description: Optional[str] = Field(None, max_length=500)

   class ExampleCreate(ExampleBase):
       pass

   class ExampleUpdate(BaseModel):
       name: Optional[str] = Field(None, min_length=1, max_length=100)
       description: Optional[str] = Field(None, max_length=500)

   class ExampleResponse(ExampleBase):
       id: int
       created_at: datetime
       updated_at: datetime

       class Config:
           from_attributes = True

   class ExampleListResponse(BaseModel):
       items: list[ExampleResponse]
       total: int
   ```

### 4. Creating Request Parameters

1. **Create parameter classes** in `app/api/v1/params/` directory

   ```python
   # app/api/v1/params/demo/example_param.py
   from pydantic import BaseModel, Field
   from typing import Optional

   class ExampleListParams(BaseModel):
       page: int = Field(1, ge=1)
       page_size: int = Field(10, ge=1, le=100)
       name: Optional[str] = Field(None, max_length=100)
   ```

### 5. Creating Controller

1. **Create controller class** in `app/api/v1/controllers/` directory

   ```python
   # app/api/v1/controllers/demo/example_controller.py
   from fastapi import APIRouter, Depends, HTTPException, Query
   from sqlalchemy.orm import Session
   from app.core.database import get_db
   from app.api.v1.cruds.demo.example_crud import example_crud
   from app.api.v1.schemas.demo.example_schema import ExampleCreate, ExampleUpdate, ExampleResponse, ExampleListResponse
   from app.api.v1.params.demo.example_param import ExampleListParams

   router = APIRouter(prefix="/examples", tags=["examples"])

   @router.get("", response_model=ExampleListResponse)
def get_examples(
    params: ExampleListParams = Depends(),
    db: Session = Depends(get_db)
):
    skip = (params.page - 1) * params.page_size
    examples = example_crud.get_list(db, skip=skip, limit=params.page_size)
    total = db.query(example_crud.model).count()
    return ExampleListResponse(items=examples, total=total)

   @router.get("/{example_id}", response_model=ExampleResponse)
def get_example(
    example_id: int,
    db: Session = Depends(get_db)
):
    example = example_crud.get_by_id(db, example_id)
    if not example:
        raise HTTPException(status_code=404, detail="Example not found")
    return example

   @router.post("", response_model=ExampleResponse, status_code=201)
def create_example(
    example: ExampleCreate,
    db: Session = Depends(get_db)
):
    return example_crud.create(db, example)

   @router.put("/{example_id}", response_model=ExampleResponse)
def update_example(
    example_id: int,
    example: ExampleUpdate,
    db: Session = Depends(get_db)
):
    updated_example = example_crud.update(db, example_id, example)
    if not updated_example:
        raise HTTPException(status_code=404, detail="Example not found")
    return updated_example

   @router.delete("/{example_id}", status_code=204)
def delete_example(
    example_id: int,
    db: Session = Depends(get_db)
):
    deleted_example = example_crud.delete(db, example_id)
    if not deleted_example:
        raise HTTPException(status_code=404, detail="Example not found")
    return None
   ```

### 6. Registering Routes

1. **Create route file** in `app/api/v1/urls/` directory

   ```python
   # app/api/v1/urls/demo/example_url.py
   from fastapi import APIRouter
   from app.api.v1.controllers.demo.example_controller import router as example_router

   router = APIRouter()
   router.include_router(example_router)
   ```

2. **Register route** in `app/plugins/init_app.py`

   ```python
   # app/plugins/init_app.py
   from fastapi import FastAPI
   from app.api.v1.urls.demo.example_url import router as example_router

   def init_routes(app: FastAPI):
       # ... existing routes
       app.include_router(example_router, prefix="/api/v1")
   ```

### 7. Database Migration

1. **Generate migration file**

   ```sh
   python main.py revision "Add example table" --env=dev
   ```

2. **Apply migration**

   ```sh
   python main.py upgrade --env=dev
   ```

## 🔧Common Development Tasks

### 1. Adding a New API Endpoint

1. **Create model** (if needed)
2. **Create CRUD operations** (if needed)
3. **Create schemas** for request and response
4. **Create controller** with endpoint logic
5. **Register route** in URL configuration
6. **Add to migration** (if database changes)
7. **Test endpoint** using Swagger UI

### 2. Authentication and Authorization

#### JWT Authentication

```python
# app/core/security.py
from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)
```

#### Dependency Injection for Authentication

```python
# app/api/v1/controllers/user_controller.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_token
from app.api.v1.models.user_model import User
from app.api.v1.cruds.user_crud import user_crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = verify_token(token, credentials_exception)
    user = user_crud.get_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

### 3. Permission Control

#### RBAC Model

FastapiAdmin uses Role-Based Access Control (RBAC) for permission management:

1. **Roles**: Define roles with specific permissions
2. **Permissions**: Define what actions can be performed
3. **Users**: Assign roles to users
4. **Resources**: Define protected resources (endpoints, data)

#### Permission Checker

```python
# app/core/security.py
def check_permission(current_user: User, required_permission: str) -> bool:
    """Check if user has required permission"""
    # Check if user is admin
    if current_user.is_admin:
        return True
    
    # Check user roles and permissions
    for role in current_user.roles:
        for permission in role.permissions:
            if permission.code == required_permission:
                return True
    
    return False

# Usage in controller
@router.get("/protected")
def protected_route(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not check_permission(current_user, "protected_resource:read"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return {"message": "Access granted"}
```

### 4. Configuration Management

#### Environment Variables

FastapiAdmin uses environment variables for configuration management:

```python
# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "FastapiAdmin"
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    DATABASE_URL: str
    
    # Redis settings
    REDIS_URL: str
    
    # Security settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

#### Environment Files

Environment variables are stored in `.env` files for different environments:

```
# env/.env.dev
# Database
DATABASE_URL="mysql+aiomysql://admin:123456@localhost:3306/fastapiadmin_dev"

# Redis
REDIS_URL="redis://localhost:6379/0"

# Security
SECRET_KEY="your-secret-key-here"
```

### 5. Logging

#### Logger Configuration

```python
# app/core/logger.py
import logging
import sys
from logging.handlers import RotatingFileHandler
from app.core.config import settings

# Create logger
logger = logging.getLogger(settings.PROJECT_NAME)
logger.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Create file handler
file_handler = RotatingFileHandler(
    "app.log", maxBytes=10485760, backupCount=5
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

export logger
```

#### Usage

```python
from app.core.logger import logger

logger.info("Application started")
logger.error("An error occurred")
logger.debug("Debug information")
```

## 📡API Design

### 1. RESTful API Principles

FastapiAdmin follows RESTful API design principles:

- **Resource Naming**: Use nouns for endpoints (e.g., `/users`, `/products`)
- **HTTP Methods**: Use appropriate HTTP methods for operations:
  - `GET`: Retrieve resources
  - `POST`: Create resources
  - `PUT`: Update resources
  - `DELETE`: Delete resources
- **Status Codes**: Use standard HTTP status codes:
  - `200 OK`: Successful GET, PUT
  - `201 Created`: Successful POST
  - `204 No Content`: Successful DELETE
  - `400 Bad Request`: Invalid request
  - `401 Unauthorized`: Authentication required
  - `403 Forbidden`: Insufficient permissions
  - `404 Not Found`: Resource not found
  - `500 Internal Server Error`: Server error

### 2. API Response Format

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "name": "Example",
    "description": "This is an example"
  }
}
```

### 3. Pagination

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "name": "Item 1"
      },
      {
        "id": 2,
        "name": "Item 2"
      }
    ],
    "total": 100,
    "page": 1,
    "page_size": 10
  }
}
```

## 🔒Security Best Practices

### 1. Input Validation

- **Use Pydantic**: Validate all input data with Pydantic models
- **Type Hints**: Use Python type hints for type safety
- **Parameter Constraints**: Set constraints on parameters (min/max length, regex patterns)
- **Sanitization**: Sanitize user input to prevent injection attacks

### 2. Authentication

- **JWT Tokens**: Use secure JWT tokens with proper expiration
- **Password Hashing**: Use bcrypt for password hashing
- **Token Rotation**: Implement token rotation for enhanced security
- **Multi-factor Authentication**: Support MFA for sensitive operations

### 3. Authorization

- **RBAC**: Use Role-Based Access Control for granular permissions
- **Least Privilege**: Assign minimum required permissions to users
- **Permission Checks**: Verify permissions for every protected resource
- **Audit Logs**: Log permission changes and access attempts

### 4. Data Protection

- **Encryption**: Encrypt sensitive data at rest and in transit
- **HTTPS**: Use HTTPS for all communications
- **CORS**: Configure CORS properly to restrict cross-origin requests
- **CSRF Protection**: Implement CSRF protection for forms

### 5. Rate Limiting

- **API Rate Limits**: Limit requests per user/IP to prevent abuse
- **Brute Force Protection**: Implement delays for failed login attempts
- **Throttling**: Throttle sensitive operations (password resets, etc.)

## 📦Deployment

### 1. Docker Deployment

#### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["python", "main.py", "run", "--env=prod"]
```

#### Docker Compose

```yaml
# docker-compose.yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8001:8001"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=mysql+aiomysql://admin:123456@db:3306/fastapiadmin
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=your-secret-key-here

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - MYSQL_DATABASE=fastapiadmin
      - MYSQL_USER=admin
      - MYSQL_PASSWORD=123456
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:7.0
    volumes:
      - redis_data:/data

volumes:
  mysql_data:
  redis_data:
```

### 2. Manual Deployment

1. **Prepare server** with Python, MySQL, and Redis installed
2. **Upload code** to server
3. **Install dependencies** in virtual environment
4. **Configure environment variables** for production
5. **Set up Nginx** as reverse proxy
6. **Use Gunicorn** with Uvicorn workers
7. **Set up systemd service** for automatic startup

### 3. Cloud Deployment

FastapiAdmin can be deployed to various cloud platforms:

- **AWS**: EC2 + RDS + ElastiCache
- **Azure**: App Service + Azure Database for MySQL + Azure Cache for Redis
- **GCP**: Compute Engine + Cloud SQL + Memorystore
- **Aliyun**: ECS + RDS + Redis
- **Tencent Cloud**: CVM + TDSQL + Redis

## 🐛Common Issues and Solutions

### 1. Database Connection Issues

**Issue**: Database connection fails
**Solution**: Check database credentials, ensure database service is running, verify network connectivity

### 2. Redis Connection Issues

**Issue**: Redis connection fails
**Solution**: Check Redis URL, ensure Redis service is running, verify network connectivity

### 3. CORS Errors

**Issue**: Cross-Origin Resource Sharing errors
**Solution**: Configure CORS properly in backend settings, ensure frontend URL is allowed

### 4. JWT Token Issues

**Issue**: Token validation fails
**Solution**: Check SECRET_KEY consistency, verify token format, ensure token hasn't expired

### 5. Permission Denied Errors

**Issue**: 403 Forbidden errors
**Solution**: Check user permissions, ensure role assignments are correct, verify permission strings

### 6. Database Migration Errors

**Issue**: Migration fails with SQL errors
**Solution**: Check migration files, ensure models are correctly defined, verify database schema

### 7. Performance Issues

**Issue**: API response times are slow
**Solution**: Use Redis caching, optimize database queries, implement pagination, consider async operations

## 📚Best Practices

### 1. Coding Standards

- **PEP 8**: Follow PEP 8 Python coding standards
- **Type Hints**: Use type hints for better code clarity and type checking
- **Docstrings**: Add docstrings for functions, classes, and modules
- **Modularity**: Keep code modular and reusable
- **Error Handling**: Implement proper error handling and logging

### 2. Database Best Practices

- **Indexing**: Add indexes for frequently queried columns
- **Query Optimization**: Use efficient queries, avoid N+1 queries
- **Transaction Management**: Use transactions for atomic operations
- **Connection Pooling**: Use connection pooling for better performance
- **Backup**: Implement regular database backups

### 3. Security Best Practices

- **Input Validation**: Validate all user input
- **Password Hashing**: Never store plain text passwords
- **HTTPS**: Use HTTPS for all communications
- **Rate Limiting**: Implement rate limiting to prevent abuse
- **Audit Logs**: Log security-related events

### 4. Performance Best Practices

- **Caching**: Use Redis for caching frequently accessed data
- **Async Operations**: Use async/await for I/O operations
- **Pagination**: Implement pagination for large datasets
- **Compression**: Use gzip compression for API responses
- **Load Balancing**: Use load balancing for high-traffic applications

### 5. Deployment Best Practices

- **Environment Separation**: Use separate environments for development, testing, and production
- **Configuration Management**: Use environment variables for configuration
- **Automated Deployment**: Implement CI/CD pipelines
- **Monitoring**: Set up monitoring and alerting
- **Rollback Plan**: Have a rollback plan for failed deployments

## 🎉Conclusion

The backend part of FastapiAdmin provides a robust, secure, and high-performance foundation for building enterprise-level applications. By following the guidelines in this document, you can develop maintainable, scalable backend systems that meet the needs of modern applications.

For more detailed information about FastAPI, SQLAlchemy, or other technologies used in FastapiAdmin, please refer to their official documentation:

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Redis Python Documentation](https://redis-py.readthedocs.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)