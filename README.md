# 自动化用例平台 (EcoFlow Auto Platform)

面向 EcoFlow APP 的可视化自动化测试管理平台。

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端框架 | React 18 + TypeScript 5 + Vite 5 |
| UI 组件库 | Ant Design 5 |
| 路由 | React Router v6 |
| 状态管理 | TanStack Query v5 + React Context |
| 后端框架 | Flask 3 |
| 数据库 | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0 + Flask-SQLAlchemy |
| 迁移 | Alembic / Flask-Migrate |
| 测试执行 | Appium (Android UIAutomator2 / iOS XCUITest) |
| 认证 | JWT (Flask-JWT-Extended) |

## 项目结构

```
ecoapp_autoPlatform/
├── frontend/          # React + Vite 前端
│   └── src/
│       ├── api/       # axios 封装 + 请求函数
│       ├── components/# 通用 UI 组件
│       ├── pages/     # 页面组件
│       ├── hooks/     # React Query hooks
│       ├── context/   # AuthContext
│       └── types/     # TypeScript 类型
├── backend/           # Flask 后端
│   └── app/
│       ├── models/    # SQLAlchemy ORM 模型
│       ├── routes/    # Blueprint 路由
│       ├── services/  # 业务逻辑层
│       ├── executor/  # Appium 执行引擎
│       └── utils/     # 工具函数
├── documents/         # 设计文档
└── impl/api/          # API 接口规范
```

## 快速开始

### 环境要求

- Node.js 18+
- Python 3.11+
- PostgreSQL 16+
- Appium Server 2.x（设备执行时需要）
- ADB（Android 设备发现）/ libimobiledevice（iOS 设备发现）

### 后端

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # 编辑数据库连接等配置
flask db upgrade           # 执行数据库迁移
python run.py              # 启动开发服务器 (http://localhost:5000)
```

### 前端

```bash
cd frontend
npm install
npm run dev                # 启动开发服务器 (http://localhost:5173)
```

### 测试

```bash
# 后端测试
cd backend && pytest

# 前端测试
cd frontend && npx vitest
```

## 核心功能

- **仪表盘**: 统计概览 + 趋势图
- **用例管理**: 树形分类 + 用例 CRUD + 内联编辑 + 脚本上传
- **执行面板**: 勾选用例 → 触发执行 → FIFO 队列 → 实时状态
- **设备管理**: 自动发现 (ADB/iOS) + 心跳维护
- **结果报告**: 日志查看 + 聚合统计 + 导出

## 设计文档

详见 `documents/` 目录和 `CLAUDE.md`。

<img width="1470" height="956" alt="image" src="https://github.com/user-attachments/assets/bb5ee0fb-3e65-4043-b50f-26e080b1e8f8" />

