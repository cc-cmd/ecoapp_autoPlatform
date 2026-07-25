"""init: create users, categories, test_cases, devices, run_groups, test_runs

Revision ID: 0001
Revises:
Create Date: 2026-07-26

This migration creates the complete initial schema matching the DDL in
documents/database-design.md Appendix A.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Apply the initial schema migration."""

    # 1. Enable PostgreSQL extensions
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

    # 2. ENUM types are created automatically by Alembic when first
    # referenced in a create_table() call (create_type=True by default).
    # They are defined here as sa.Enum instances for use in column defs
    # below and for explicit cleanup in downgrade().

    # 3. Create tables in FK dependency order

    # 3a. users (no FK dependencies)
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column("username", sa.String(64), nullable=False),
        sa.Column("password_hash", sa.String(256), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
    )
    op.create_index("idx_users_username", "users", ["username"], unique=True)

    # 3b. categories (self-referencing FK)
    op.create_table(
        "categories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("parent_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("categories.id", ondelete="SET NULL"), nullable=True),
        sa.Column("sort_order", sa.Integer, nullable=False, server_default=sa.text("0")),
    )
    op.create_index("idx_categories_parent_id", "categories", ["parent_id"])
    op.create_index("idx_categories_sort", "categories", ["parent_id", "sort_order"])

    # 3c. test_cases (FK → categories, users)
    op.create_table(
        "test_cases",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("priority", sa.Enum("P0", "P1", "P2", "P3", name="priority_enum"),
                  nullable=False, server_default="P3"),
        sa.Column("steps", sa.Text, server_default=sa.text("''")),
        sa.Column("script_path", sa.String(512), nullable=True),
        sa.Column("is_automated", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("category_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("categories.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
    )
    op.create_index("idx_test_cases_category", "test_cases", ["category_id"])
    op.create_index("idx_test_cases_priority", "test_cases", ["priority"])
    op.create_index("idx_test_cases_created_by", "test_cases", ["created_by"])
    op.create_index("idx_test_cases_updated", "test_cases",
                    [sa.text("updated_at DESC")])
    op.create_index("idx_test_cases_name_search", "test_cases", ["name"],
                    postgresql_using="gin", postgresql_ops={"name": "gin_trgm_ops"})

    # 3d. devices (no FK dependencies)
    op.create_table(
        "devices",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column("device_id", sa.String(128), nullable=False),
        sa.Column("platform", sa.Enum("android", "ios", name="platform_enum"),
                  nullable=False),
        sa.Column("model", sa.String(128), nullable=False),
        sa.Column("status", sa.Enum("online", "busy", "offline",
                  name="device_status_enum"), nullable=False, server_default="online"),
        sa.Column("last_heartbeat", sa.DateTime, server_default=sa.func.now(),
                  nullable=False),
    )
    op.create_index("idx_devices_device_id", "devices", ["device_id"], unique=True)
    op.create_index("idx_devices_status", "devices", ["status"])
    op.create_index("idx_devices_heartbeat", "devices", ["last_heartbeat"])

    # 3e. run_groups (FK → devices, users)
    op.create_table(
        "run_groups",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column("device_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("devices.id", ondelete="SET NULL"), nullable=True),
        sa.Column("status", sa.Enum("queued", "running", "completed",
                  name="run_group_status_enum"), nullable=False, server_default="queued"),
        sa.Column("triggered_by", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("finished_at", sa.DateTime, nullable=True),
    )
    op.create_index("idx_run_groups_device", "run_groups", ["device_id"])
    op.create_index("idx_run_groups_status", "run_groups", ["status"])
    op.create_index("idx_run_groups_trigger", "run_groups", ["triggered_by"])
    op.create_index("idx_run_groups_created", "run_groups",
                    [sa.text("created_at DESC")])
    op.create_index("idx_run_groups_queue", "run_groups", ["status", "created_at"])

    # 3f. test_runs (FK → run_groups, test_cases)
    op.create_table(
        "test_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("uuid_generate_v4()")),
        sa.Column("run_group_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("run_groups.id", ondelete="CASCADE"), nullable=False),
        sa.Column("case_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("test_cases.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.Enum("queued", "running", "passed", "failed", "error",
                  name="run_status_enum"), nullable=False, server_default="queued"),
        sa.Column("log", sa.Text, server_default=sa.text("''")),
        sa.Column("started_at", sa.DateTime, nullable=True),
        sa.Column("finished_at", sa.DateTime, nullable=True),
    )
    op.create_index("idx_test_runs_run_group", "test_runs", ["run_group_id"])
    op.create_index("idx_test_runs_case", "test_runs", ["case_id"])
    op.create_index("idx_test_runs_status", "test_runs", ["status"])
    op.create_index("idx_test_runs_started", "test_runs",
                    [sa.text("started_at DESC")])
    op.create_index("idx_test_runs_batch_order", "test_runs", ["run_group_id", "id"])


def downgrade() -> None:
    """Revert the initial schema migration."""

    # Drop tables in reverse dependency order
    op.drop_table("test_runs")
    op.drop_table("run_groups")
    op.drop_table("devices")
    op.drop_table("test_cases")
    op.drop_table("categories")
    op.drop_table("users")

    # Drop ENUM types in reverse creation order
    sa.Enum(name="run_status_enum").drop(op.get_bind())
    sa.Enum(name="run_group_status_enum").drop(op.get_bind())
    sa.Enum(name="device_status_enum").drop(op.get_bind())
    sa.Enum(name="platform_enum").drop(op.get_bind())
    sa.Enum(name="priority_enum").drop(op.get_bind())

    # Drop extensions (optional — skip if other databases may use them)
    op.execute("DROP EXTENSION IF EXISTS pg_trgm")
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp"')
