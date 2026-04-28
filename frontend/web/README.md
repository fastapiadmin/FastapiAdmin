# frontend

## 项目结构

```sh
FastapiAdmin/frontend
├─ docs                 # 项目文档工程
├─ public               # 静态资源文件
│  └─ docs              # 帮助文档模块
├─ src                  # 源代码
│  ├─ api               # 接口文件
│  ├─ assets            # 静态资源文件
│  ├─ components        # 组件模块
│  ├─ constants         # 常量模块
│  ├─ lang              # 语言模块
│  ├─ layouts           # 布局模块
│  ├─ plugins           # 插件模块
│  ├─ router            # 路由模块
│  ├─ store             # 状态管理模块
│  ├─ styles            # 样式模块
│  ├─ types             # 类型模块
│  ├─ utils             # 工具模块
│  ├─ view              # 视图模块
│  ├─ App.vue           # 根组件
│  ├─ main.js           # 入口文件
│  └─ settings.js       # 全局样式文件
├─ .env.development     # 项目开发环境配置
├─ .env.production      # 项目生产环境配置
├─ index.html           # 模板文件
├─ package.json         # 项目依赖文件
├─ tsconfig.json        # ts配置文件
├─ uno.config.json      # uno配置文件
├─ vite.config.js       # vite服务配置文件
└─ README.md            # 项目说明文档

```

## 快速开始

```sh
# 进入前端工程目录
cd frontend/web
# 安装依赖
pnpm install
# 启动前端服务
pnpm run dev
# 构建前端, 生成 `frontend/dist` 目录
pnpm run build
# 运行命令，查看未用到的依赖
depcheck
```

### 4. 开发模式启动

#### 方式：一键启动（推荐）

```bash
# 直接启动Electron开发模式（自动启动后端）
cd frontend/web
npm run electron:dev
```

## 📦 生产环境打包

### 完整打包流程

```bash
# 1. 打包后端为独立可执行文件
cd backend
uv run pyinstaller --onefile --name fastapi-backend main.py

# 2. 复制后端可执行文件到前端资源目录
# 注意：PyInstaller会根据平台自动添加后缀（.exe on Windows, no suffix on macOS/Linux）
cp dist/fastapi-backend* ../frontend/web/resources/

# 3. 构建前端
cd ../frontend/web
npm run build

# 4. 打包Electron应用
# electron-builder配置位于package.json的build字段中
npm run electron:build
```

### 输出文件
- **Windows**：
  - 安装包：`frontend/release/MyElectronApp Setup 1.0.0.exe`
  - 便携版：`frontend/release/win-unpacked/MyElectronApp.exe`
- **macOS**：
  - 安装包：`frontend/release/MyElectronApp-1.0.0-arm64-mac.zip`（或类似名称）
  - 应用程序：`frontend/release/mac-arm64/MyElectronApp.app`
- **Linux**：
  - AppImage：`frontend/release/MyElectronApp-1.0.0-arm64.AppImage`（或类似名称）
