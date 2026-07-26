# 自动化用例平台 (EcoFlow Auto Platform)

面向 EcoFlow APP 的可视化自动化测试管理平台。

核心链路：**设备发现 → 用例执行（Appium 真机）→ 结果存储 → 报告展示**。

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端框架 | React 18 + TypeScript 5 + Vite 5 |
| UI 组件库 | Ant Design 5 + @ant-design/icons |
| 路由 | React Router v6（createBrowserRouter + 懒加载） |
| 状态管理 | TanStack Query v5（服务端状态）+ React Context（认证状态） |
| HTTP 客户端 | Axios（JWT 拦截器） |
| 后端框架 | Flask 3 + Flask-SQLAlchemy + Flask-JWT-Extended + Flask-Migrate + Flask-CORS |
| 数据库 | PostgreSQL 16（原生 UUID 类型） |
| 序列化 | marshmallow |
| 定时任务 | APScheduler（心跳检测 + 队列消费） |
| 测试执行 | Appium（Android UIAutomator2 / iOS XCUITest） |
| 密码哈希 | bcrypt |
| 生产部署 | Gunicorn（wsgi.py） |

## 项目结构

```
ecoapp_autoPlatform/
├── frontend/                       # React + Vite + TypeScript
│   ├── src/
│   │   ├── api/                    # axios 实例 + 各模块请求函数
│   │   ├── components/             # 通用 UI 组件
│   │   ├── pages/                  # 页面组件（每个页面一个目录）
│   │   ├── hooks/                  # React Query 封装
│   │   ├── context/                # AuthContext（认证状态）
│   │   ├── types/                  # TypeScript 类型定义
│   │   ├── styles/                 # 全局样式
│   │   ├── App.tsx                 # 路由配置 + ErrorBoundary
│   │   └── main.tsx                # 入口（QueryClient + Auth + ConfigProvider）
│   ├── vite.config.ts              # @/ alias, proxy /api → :5001
│   ├── tsconfig.json
│   └── package.json
├── backend/                        # Flask 后端
│   ├── app/
│   │   ├── __init__.py             # create_app() 工厂
│   │   ├── config.py               # 三环境配置（开发/测试/生产）
│   │   ├── extensions.py           # db, jwt, migrate 扩展
│   │   ├── errors.py               # 统一错误处理
│   │   ├── logging_config.py       # 请求/响应日志
│   │   ├── scheduler.py            # APScheduler 定时任务
│   │   ├── models/                 # 6 个 SQLAlchemy 模型
│   │   ├── routes/                 # 6 个 Blueprint 路由
│   │   ├── services/               # 业务逻辑层
│   │   ├── executor/               # Appium 执行引擎
│   │   └── utils/                  # 工具函数
│   ├── migrations/                 # Flask-Migrate / Alembic
│   ├── scripts/                    # seed.py（种子数据）+ init.sql
│   ├── tests/                      # pytest 测试
│   ├── .env.example
│   ├── requirements.txt
│   ├── run.py                      # 开发入口
│   └── wsgi.py                     # 生产入口（Gunicorn）
├── .venv/                          # 共享 Python 虚拟环境
├── README.md
├── CLAUDE.md
└── .gitignore
```

## 快速开始

### 环境要求

- **Node.js** 18+
- **Python** 3.11+
- **PostgreSQL** 16+
- Appium Server 2.x（设备执行时需要）
- ADB（Android 设备发现）/ libimobiledevice（iOS 设备发现）

### 1. 克隆项目

```bash
git clone <repo-url>
cd ecoapp_autoPlatform
```

### 2. 后端

```bash
# 创建共享虚拟环境（项目根目录）
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 安装依赖
pip install -r backend/requirements.txt

# 配置环境变量
cp backend/.env.example backend/.env   # 编辑 .env 修改数据库连接等配置

# 创建数据库
createdb -U postgres auto_project

# 执行数据库迁移
cd backend
flask db upgrade

# 插入种子数据（默认管理员: admin / admin123）
python scripts/seed.py

# 启动开发服务器 (http://127.0.0.1:5001)
python run.py
```

### 3. 前端

```bash
cd frontend
npm install
npm run dev                         # 启动开发服务器 (http://localhost:5173)
```

Vite 开发服务器自动将 `/api` 请求代理到后端 `http://127.0.0.1:5001`。

### 4. 访问

打开浏览器访问 `http://localhost:5173`，使用默认管理员账号登录：
- 用户名：`admin`
- 密码：`admin123`

## 常用命令

### 后端

```bash
cd backend

# 运行测试
pytest                              # 全部测试
pytest tests/test_auth.py -v        # 指定测试文件
pytest -k test_login                # 按名称筛选

# 代码检查
ruff check app/                     # Python lint
ruff format app/                    # Python 格式化

# 数据库
flask db current                    # 查看当前迁移版本
psql -U postgres -d auto_project -c "\dt"  # 查看所有表
```

### 前端

```bash
cd frontend

# 运行测试
npm run test                        # vitest

# 代码检查
npm run lint                        # ESLint
npm run format                      # Prettier

# 构建
npm run build                       # tsc + vite build → dist/
```

## 环境配置

通过 `backend/.env` 中的 `FLASK_ENV` 切换运行环境：

| 环境 | 配置类 | 说明 |
|------|--------|------|
| development | DevelopmentConfig | 默认，DEBUG=True，PostgreSQL |
| testing | TestingConfig | pytest 使用，SQLite 内存数据库 |
| production | ProductionConfig | Gunicorn 部署，PostgreSQL |

## 数据库

### 核心表（6 张）

| 表名 | 说明 | 关键字段 |
|------|------|----------|
| users | 系统用户 | username（UNIQUE），bcrypt 密码 |
| categories | 分类树 | parent_id 自引用邻接表 |
| test_cases | 测试用例 | priority + platform 枚举，script_path |
| devices | 测试设备 | device_id（UNIQUE），心跳维护状态 |
| run_groups | 执行批次 | 一次提交 = 一个批次，批次内用例串行 |
| test_runs | 单用例执行 | 完整状态机（queued → running → passed/failed/error） |

### 状态机

- **设备**: `online` ↔ `busy` / `offline`（心跳超时 60s → offline）
- **test_runs**: `queued` → `running` → `passed` / `failed` / `error`（终态不可逆）
- **run_groups**: `queued` → `running` → `completed`（终态不可逆）

## 核心功能

| 模块 | 说明 |
|------|------|
| 仪表盘 | 统计概览 + 趋势卡片 |
| 用例管理 | 树形分类 + CRUD + 内联编辑 + 脚本上传 + 拖拽排序 |
| 执行面板 | 勾选用例 → 触发执行 → FIFO 队列 → 实时状态轮询 |
| 设备管理 | 自动发现（ADB/iOS）+ 心跳维护 + 在线状态 |
| 结果报告 | 日志查看器 + 聚合统计 |

## 实现状态

| 模块 | 状态 |
|------|------|
| 数据模型（6 表） | ✅ 完成 |
| 路由 + Service + API | ✅ 完成 |
| 前端所有页面 + 组件 | ✅ 完成 |
| 前端路由 + 认证守卫 | ✅ 完成 |
| 执行引擎（Executor） | ✅ 架构完成，待 Appium 真实联调 |
| Scheduler（心跳 + 队列消费） | ❌ Stub（TODO 待实现） |
| 后端测试 | ✅ test_auth, test_cases |
| 前端测试 | ⚠️ vitest 已配置，组件/页面级测试待补充 |
| 种子数据 | ✅ admin/admin123 + 3 个默认分类 |

## 运行截图

<img width="1470" height="956" alt="image" src="https://github.com/user-attachments/assets/bb5ee0fb-3e65-4043-b50f-26e080b1e8f8" />

## 生产部署

```bash
# 使用 Gunicorn 启动
cd backend
gunicorn wsgi:app -w 4 -b 0.0.0.0:5001

# 前端构建并部署静态文件
cd frontend
npm run build                      # 输出到 dist/
# 将 dist/ 部署到 Nginx 或 CDN
```

## 更多信息

- 项目详细说明和架构约定参见 `CLAUDE.md`
- API 接口规范参见 `impl/api/` 目录
- 设计文档参见 `documents/` 目录
