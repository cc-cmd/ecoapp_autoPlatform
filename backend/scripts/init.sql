-- ============================================================
-- 自动化用例平台 — 数据库初始化脚本
-- 版本：v1.0
-- 日期：2026-07-26
-- 数据库：PostgreSQL 16+
-- 执行方式：psql -U postgres -d auto_project -f init.sql
--
-- 注意：此文件对应 Alembic 初始迁移 0001_initial_schema.py。
--       两者保持同步，schema 变更时需同时更新。
--       推荐使用 Alembic 迁移（flask db upgrade），此文件作为备用手动初始化方案。
-- ============================================================

-- 1. 启用扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- 2. 创建枚举类型
CREATE TYPE priority_enum        AS ENUM ('P0', 'P1', 'P2', 'P3');
CREATE TYPE platform_enum        AS ENUM ('android', 'ios');
CREATE TYPE device_status_enum   AS ENUM ('online', 'busy', 'offline');
CREATE TYPE run_group_status_enum AS ENUM ('queued', 'running', 'completed');
CREATE TYPE run_status_enum      AS ENUM ('queued', 'running', 'passed', 'failed', 'error');

-- 3. users
CREATE TABLE users (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username      VARCHAR(64)  NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    created_at    TIMESTAMP    NOT NULL DEFAULT NOW()
);
CREATE UNIQUE INDEX idx_users_username ON users (username);

-- 4. categories
CREATE TABLE categories (
    id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name       VARCHAR(128) NOT NULL,
    parent_id  UUID REFERENCES categories(id) ON DELETE SET NULL,
    sort_order INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX idx_categories_parent_id ON categories (parent_id);
CREATE INDEX idx_categories_sort ON categories (parent_id, sort_order);

-- 5. test_cases
CREATE TABLE test_cases (
    id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name         VARCHAR(255) NOT NULL,
    priority     priority_enum NOT NULL DEFAULT 'P3',
    steps        TEXT DEFAULT '',
    script_path  VARCHAR(512),
    is_automated BOOLEAN NOT NULL DEFAULT FALSE,
    category_id  UUID REFERENCES categories(id) ON DELETE SET NULL,
    created_by   UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at   TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_test_cases_category    ON test_cases (category_id);
CREATE INDEX idx_test_cases_priority    ON test_cases (priority);
CREATE INDEX idx_test_cases_created_by  ON test_cases (created_by);
CREATE INDEX idx_test_cases_updated     ON test_cases (updated_at DESC);
CREATE INDEX idx_test_cases_name_search ON test_cases USING gin (name gin_trgm_ops);

-- 6. devices
CREATE TABLE devices (
    id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id      VARCHAR(128) NOT NULL,
    platform       platform_enum NOT NULL,
    model          VARCHAR(128) NOT NULL,
    status         device_status_enum NOT NULL DEFAULT 'online',
    last_heartbeat TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE UNIQUE INDEX idx_devices_device_id ON devices (device_id);
CREATE INDEX idx_devices_status ON devices (status);
CREATE INDEX idx_devices_heartbeat ON devices (last_heartbeat);

-- 7. run_groups
CREATE TABLE run_groups (
    id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id    UUID REFERENCES devices(id) ON DELETE SET NULL,
    status       run_group_status_enum NOT NULL DEFAULT 'queued',
    triggered_by UUID NOT NULL REFERENCES users(id) ON DELETE SET NULL,
    created_at   TIMESTAMP NOT NULL DEFAULT NOW(),
    finished_at  TIMESTAMP
);
CREATE INDEX idx_run_groups_device  ON run_groups (device_id);
CREATE INDEX idx_run_groups_status  ON run_groups (status);
CREATE INDEX idx_run_groups_trigger ON run_groups (triggered_by);
CREATE INDEX idx_run_groups_created ON run_groups (created_at DESC);
CREATE INDEX idx_run_groups_queue   ON run_groups (status, created_at);

-- 8. test_runs
CREATE TABLE test_runs (
    id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    run_group_id UUID NOT NULL REFERENCES run_groups(id) ON DELETE CASCADE,
    case_id      UUID NOT NULL REFERENCES test_cases(id) ON DELETE CASCADE,
    status       run_status_enum NOT NULL DEFAULT 'queued',
    log          TEXT DEFAULT '',
    started_at   TIMESTAMP,
    finished_at  TIMESTAMP
);
CREATE INDEX idx_test_runs_run_group   ON test_runs (run_group_id);
CREATE INDEX idx_test_runs_case        ON test_runs (case_id);
CREATE INDEX idx_test_runs_status      ON test_runs (status);
CREATE INDEX idx_test_runs_started     ON test_runs (started_at DESC);
CREATE INDEX idx_test_runs_batch_order ON test_runs (run_group_id, id);

-- 完成
