"""rename api docs menu to official site

Revision ID: d8e9f0a1b2c3
Revises: c7d8e9f0a1b2
Create Date: 2026-11-28 23:10:00
"""

import sqlalchemy as sa
from alembic import op

revision = "d8e9f0a1b2c3"
down_revision = "c7d8e9f0a1b2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
            UPDATE sys_menu
            SET name = '项目官网',
                title = '项目官网',
                icon = 'ri:global-line',
                route_name = 'OfficialSite',
                route_path = '/official-site',
                link = 'https://service.fastapiadmin.com/',
                description = 'FastapiAdmin 项目官网（type=4 外链菜单）',
                updated_time = NOW()
            WHERE route_name = 'ApiDocs'
            """
        )
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            """
            UPDATE sys_menu
            SET name = 'API 文档',
                title = 'API 文档',
                icon = 'ri:book-open-line',
                route_name = 'ApiDocs',
                route_path = '/api-docs',
                link = 'https://service.fastapiadmin.com/docs',
                description = 'FastAPI Swagger 文档外链示例（type=4 外链菜单）',
                updated_time = NOW()
            WHERE route_name = 'OfficialSite'
            """
        )
    )
