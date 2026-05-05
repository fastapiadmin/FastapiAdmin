---
outline: "deep"
title: Development Guidelines
---
# Development Guidelines

## 📚 Guidelines Overview

To ensure project code consistency, readability, and maintainability, the FastapiAdmin project has established the following development guidelines. All developers participating in the project should follow these guidelines.

## 🎨 Frontend Development Guidelines

### 1. Code Style

#### 1.1 TypeScript Guidelines

- Use TypeScript strict mode (`"strict": true`)
- Add type annotations for all variables, functions, and interfaces
- Avoid using `any` type unless the type is truly indeterminable
- Use interfaces to define object types, not type aliases
- Use enums to define constant sets
- Use `type` to define union types and intersection types
- Use `as const` assertions to ensure type safety
- Use `readonly` modifiers to protect immutable data
- Use `unknown` type to handle data of uncertain types

#### 1.2 Vue Guidelines

- Use Composition API
- Use `<script setup lang="ts">` syntax
- Use PascalCase for component naming
- Use camelCase for variable and function naming
- Use UPPER_SNAKE_CASE for constant naming
- Use `ref()` to define reactive variables
- Use `computed()` to define computed properties
- Use `watch()` or `watchEffect()` to monitor changes
- Use `onMounted()`, `onUnmounted()` and other lifecycle hooks
- Use `defineProps()` to define component props with types
- Use `defineEmits()` to define component events with types
- Use `defineExpose()` to define exposed component properties and methods

#### 1.3 CSS Guidelines

- Use UnoCSS atomic CSS
- Avoid using inline styles
- Use BEM naming convention (if not using UnoCSS)
- Use kebab-case for class names
- Avoid using ID selectors
- Use CSS variables for theme management
- Avoid using `!important` modifier
- Use flexbox layout to ensure cross-platform consistency
- Use CSS Grid layout appropriately
- Optimize CSS selector priority

### 2. Component Development Best Practices

- **Single Responsibility Principle**: Each component should be responsible for only one function
- **Props Design**:
  - Use `required` and `default` to clearly specify props requirements
  - Add validation for complex props
  - Use `withDefaults()` to set default values for props
- **Events Design**:
  - Use kebab-case for event naming
  - Event parameter types should be clear
  - Avoid passing too many parameters in events
- **Slots Design**:
  - Use named slots to improve readability
  - Add default content for slots
  - Use scoped slots to pass data
- **Styles Design**:
  - Use `scoped` styles to avoid conflicts
  - Use `:deep()` selectors appropriately
  - Avoid using global styles in components

### 3. State Management Best Practices

- **Modular Design**: Split stores by functional modules
- **State Definition**:
  - Use `interface` to define state types
  - Initialize all states
  - Avoid using overly nested state structures
- **Actions Design**:
  - Handle asynchronous operations
  - Use try/catch to catch errors
  - Use transactions when committing multiple mutations
- **Getters Design**:
  - Cache calculation results
  - Avoid modifying state in getters
  - Use parameterized getters appropriately

### 4. API Call Best Practices

- **Modular Management**: Organize API interfaces by functional modules
- **Request Encapsulation**:
  - Unified handling of request headers
  - Unified error handling
  - Unified loading state handling
- **Response Handling**:
  - Type definitions for response data structures
  - Unified handling of response status codes
  - Appropriate handling of empty data and edge cases
- **Request Optimization**:
  - Use debounce and throttle
  - Cache results of frequent requests
  - Use concurrent requests appropriately

### 5. Performance Optimization Recommendations

- **Code Splitting**: Use route lazy loading and component lazy loading
- **Resource Optimization**:
  - Compress images and static resources
  - Use WebP format images
  - Use CDN appropriately
- **Rendering Optimization**:
  - Use `v-memo` to cache calculation results
  - Use `v-if` and `v-show` appropriately
  - Avoid using complex expressions in templates
- **Network Optimization**:
  - Use HTTP/2 or HTTP/3
  - Enable Gzip or Brotli compression
  - Set caching strategies appropriately

### 6. Testing Best Practices

- **Test Layering**: Unit tests, integration tests, end-to-end tests
- **Test Coverage**:
  - 100% coverage for core functionality
  - 80%+ coverage for complex logic
  - 50%+ coverage for simple functionality
- **Testing Tools**:
  - Use Vitest for unit testing
  - Use Playwright for end-to-end testing
  - Use Vue Test Utils for component testing

### 7. Code Review Points

- **Type Safety**: Check if TypeScript type definitions are correct
- **Code Quality**: Check if code is concise and clear
- **Performance Issues**: Check for performance bottlenecks
- **Security Issues**: Check for security vulnerabilities
- **Guideline Compliance**: Check if project development guidelines are followed

## 🐍 Backend Development Guidelines

### 1. Code Style

#### 1.1 Python Guidelines

- Follow PEP 8 code style
- Use 4 spaces for indentation
- Line length should not exceed 100 characters
- Leave two blank lines between functions and classes
- Leave one blank line between methods
- Group import statements by standard library, third-party library, and local library

#### 1.2 FastAPI Guidelines

- Use FastAPI decorators to define routes
- Use Pydantic models to define request and response data
- Use dependency injection for authentication and authorization
- Use path parameters and query parameters
- Use HTTPException for error handling
- Use Depends to inject dependencies

### 2. Directory Structure

```
backend/app/
├── api/             # API interfaces
├── common/          # Common code
├── config/          # Configuration management
├── core/            # Core functionality
├── plugin/          # Plugin system
├── scripts/         # Script tools
└── utils/           # Utility functions
```

### 3. Plugin Development Guidelines

- Plugin directories should start with `module_`
- Plugins should include files such as `controller.py`, `model.py`, `schema.py`, `service.py`, `crud.py`
- Controllers should use `APIRouter` to define routes
- Route prefixes should correspond to module names (module_xxx -> /xxx)
- Controllers should use `OperationLogRoute` to record operation logs
- Interfaces should use `AuthPermission` for permission control

### 4. Database Guidelines

- Use SQLAlchemy 2.0 ORM
- Use Alembic for database migrations
- Model classes should inherit from `Base`
- Model classes should define `__tablename__` attribute
- Field naming should use snake_case
- Table names should use snake_case plural form
- Foreign keys should be defined using `ForeignKey`
- Relationships should be defined using `relationship`

### 5. Authentication and Authorization Guidelines

- Use JWT for authentication
- Use RBAC model for permission management
- Interfaces should add permission control decorators
- Permission string format: `module:controller:action`
- Permissions should be configured in role management

### 6. Error Handling Guidelines

- Use `HTTPException` for HTTP errors
- Use custom exception handling for global errors
- Error responses should have a unified format
- Errors should be logged

### 7. Logging Guidelines

- Use Python standard library `logging` module
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Logs should include time, level, module, message, and other information
- Key operations should be logged
- Errors should be logged with detailed information

## 📦 FastApp Mobile Development Guidelines

### 1. Code Style

- Follow frontend development guidelines
- Use TypeScript strict mode
- Use Vue 3 Composition API
- Use `<script setup lang="ts">` syntax
- Use PascalCase for component naming
- Use camelCase for variable and function naming

### 2. Directory Structure

```
FastApp/src/
├── api/             # API interfaces
├── components/      # Components
├── composables/     # Composable functions
├── constants/       # Constant definitions
├── enums/           # Enum definitions
├── layouts/         # Layout components
├── pages/           # Page files
├── router/          # Router configuration
├── static/          # Static resources
├── store/           # State management
├── styles/          # Style files
├── types/           # TypeScript type definitions
├── utils/           # Utility functions
├── App.vue          # Application root component
└── main.ts          # Application entry file
```

### 3. Page Development Guidelines

- Page components should be placed in the `pages` directory
- Page directories should use kebab-case
- Page components should include `index.vue` file
- Page components can include auxiliary files such as `data.ts`, `types.ts`
- Page components should use lifecycle hooks such as `onLoad()`, `onShow()`
- Page navigation should use APIs such as `uni.navigateTo()`, `uni.switchTab()`

### 4. API Call Guidelines

- Follow frontend API call guidelines
- Use the encapsulated `request.ts` utility
- API interfaces should be classified by module
- API calls should handle error situations
- API calls should display loading state

### 5. Cross-Platform Adaptation Guidelines

- Use conditional compilation to handle platform differences
- Use `#ifdef`, `#ifndef`, `#endif` directives
- Platform-specific APIs should add conditional compilation
- Styles should consider differences between platforms
- Layouts should use flexbox to ensure cross-platform consistency

## 🎯 Git Commit Guidelines

### 1. Branch Management

- `master`: Main branch, used for releasing production versions
- `dev`: Development branch, used for integration development
- `feature/xxx`: Feature branch, used for developing new features
- `bugfix/xxx`: Fix branch, used for fixing bugs
- `hotfix/xxx`: Hotfix branch, used for emergency fixes in production environment

### 2. Commit Message Guidelines

Commit messages should follow the following format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### 2.1 Type

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test code changes
- `chore`: Build tool or dependency changes
- `revert`: Revert commit

#### 2.2 Scope

- Optional, used to specify the scope of changes
- For example: `api`, `component`, `page`, `store`, etc.

#### 2.3 Subject

- Brief commit message, not exceeding 50 characters
- Use imperative mood, starting with a verb
- First letter lowercase
- No period at the end

#### 2.4 Body

- Optional, detailed commit message
- Each line not exceeding 72 characters
- Explain why, not how

#### 2.5 Footer

- Optional, used to reference issues or bugs
- For example: `Closes #123`, `Fixes #456`

### 3. Commit Examples

```
feat(api): Add user login endpoint

- Implement user login functionality
- Add JWT authentication
- Handle login error cases

Closes #123
```

```
fix(frontend): Fix homepage carousel display issue

- Fix carousel height calculation error
- Optimize carousel transition animation

Fixes #456
```

```
docs: Update development documentation

- Add API documentation
- Improve deployment guide
```

### 4. Pull Request Guidelines

- Pull Requests should merge from feature branches to dev branch
- Pull Request titles should be clear and semantic
- Pull Request descriptions should detail the changes
- Pull Requests should include related issue links
- Pull Requests should pass all tests
- Pull Requests should be reviewed by at least one reviewer

## 🔧 Toolchain Guidelines

### 1. Frontend Toolchain

- Use Vite as build tool
- Use ESLint for code linting
- Use Prettier for code formatting
- Use Stylelint for style linting
- Use Husky for Git hook management
- Use Commitlint for commit message checking

### 2. Backend Toolchain

- Use Poetry or pip for dependency management
- Use Pylint or Flake8 for code linting
- Use Black for code formatting
- Use MyPy for type checking
- Use pytest for testing

## 💡 Development Process Guidelines

### 1. Requirements Analysis

- Clarify functional requirements
- Analyze business logic
- Determine technical solutions

### 2. Design Phase

- Design database table structure
- Design API interfaces
- Design frontend pages
- Design component structure

### 3. Development Phase

- Create branches
- Implement features
- Write tests
- Run tests

### 4. Testing Phase

- Unit tests
- Integration tests
- End-to-end tests
- Performance tests

### 5. Deployment Phase

- Build production version
- Deploy to test environment
- Perform regression testing
- Deploy to production environment

### 6. Maintenance Phase

- Monitor system running status
- Handle bugs and issues
- Perform performance optimization
- Perform feature iterations

## 📚 Reference Materials

- [TypeScript Official Documentation](https://www.typescriptlang.org/docs/)
- [Vue Official Documentation](https://vuejs.org/docs/)
- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Official Documentation](https://docs.sqlalchemy.org/)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [ESLint Official Documentation](https://eslint.org/docs/)
- [Prettier Official Documentation](https://prettier.io/docs/en/)

## 🤝 Contribution Guidelines

If you have any suggestions or improvements for the development guidelines, please submit an Issue or Pull Request. We will carefully consider every suggestion and continuously improve the development guidelines.

## 📄 License Agreement

This development guidelines document adopts the MIT License, consistent with the FastapiAdmin project.
