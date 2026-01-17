from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.sql import expression

from app.config.setting import settings
from app.core.base_model import ModelMixin, UserMixin
from app.utils.common_util import SqlalchemyUtil


class GenTableModel(ModelMixin, UserMixin):
    """
    代码生成表
    """

    __tablename__: str = "gen_table"
    __table_args__: dict[str, str] = {"comment": "代码生成表"}
    __loader_options__: list[str] = ["columns", "created_by", "updated_by"]

    table_name: Mapped[str] = mapped_column(
        String(200), nullable=False, default="", comment="表名称"
    )
    table_comment: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="表描述")

    class_name: Mapped[str] = mapped_column(
        String(100), nullable=False, default="", comment="实体类名称"
    )
    package_name: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="生成包路径"
    )
    module_name: Mapped[str | None] = mapped_column(String(30), nullable=True, comment="生成模块名")
    business_name: Mapped[str | None] = mapped_column(
        String(30), nullable=True, comment="生成业务名"
    )
    function_name: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="生成功能名"
    )

    sub_table_name: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(settings.DATABASE_TYPE),
        comment="关联子表的表名",
    )
    sub_table_fk_name: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(settings.DATABASE_TYPE),
        comment="子表关联的外键名",
    )

    parent_menu_id: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="父菜单ID")

    # 关联关系
    columns: Mapped[list["GenTableColumnModel"]] = relationship(
        order_by="GenTableColumnModel.sort",
        back_populates="table",
        cascade="all, delete-orphan",
    )

    @validates("table_name")
    def validate_table_name(self, key: str, table_name: str) -> str:
        """验证表名不为空"""
        if not table_name or not table_name.strip():
            raise ValueError("表名称不能为空")
        return table_name.strip()

    @validates("class_name")
    def validate_class_name(self, key: str, class_name: str) -> str:
        """验证类名不为空"""
        if not class_name or not class_name.strip():
            raise ValueError("实体类名称不能为空")
        return class_name.strip()


class GenTableColumnModel(ModelMixin, UserMixin):
    """
    代码生成表字段

    数据隔离策略:
    - 继承自GenTableModel的隔离级别
    - 不需要customer_id

    用于存储代码生成器的字段配置
    """

    __tablename__: str = "gen_table_column"
    __table_args__: dict[str, str] = {"comment": "代码生成表字段"}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    # 数据库设计表字段
    column_name: Mapped[str] = mapped_column(String(200), nullable=False, comment="列名称")
    column_comment: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="列描述")
    column_type: Mapped[str] = mapped_column(String(100), nullable=False, comment="列类型")
    column_length: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="列长度")
    column_default: Mapped[str | None] = mapped_column(
        String(200), nullable=True, comment="列默认值"
    )
    is_pk: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=expression.false(),
        comment="是否主键",
    )
    is_increment: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=expression.false(),
        comment="是否自增",
    )
    is_nullable: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=expression.true(),
        comment="是否允许为空",
    )
    is_unique: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=expression.false(),
        comment="是否唯一",
    )

    # Python字段映射
    python_type: Mapped[str | None] = mapped_column(
        String(100), nullable=True, comment="Python类型"
    )
    python_field: Mapped[str | None] = mapped_column(
        String(200), nullable=True, comment="Python字段名"
    )

    # 序列化配置
    is_insert: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=expression.true(),
        comment="是否为新增字段",
    )
    is_edit: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=expression.true(),
        comment="是否编辑字段",
    )
    is_list: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=expression.true(),
        comment="是否列表字段",
    )
    is_query: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=expression.false(),
        comment="是否查询字段",
    )
    query_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True, default=None, comment="查询方式"
    )

    # 前端展示配置
    html_type: Mapped[str | None] = mapped_column(
        String(100), nullable=True, default="input", comment="显示类型"
    )
    dict_type: Mapped[str | None] = mapped_column(
        String(200), nullable=True, default="", comment="字典类型"
    )

    # 排序和扩展配置
    sort: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="排序")

    # 归属关系
    table_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("gen_table.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="归属表编号",
    )

    # 关联关系
    table: Mapped["GenTableModel"] = relationship(back_populates="columns")

    @validates("column_name")
    def validate_column_name(self, key: str, column_name: str) -> str:
        """验证列名不为空"""
        if not column_name or not column_name.strip():
            raise ValueError("列名称不能为空")
        return column_name.strip()

    @validates("column_type")
    def validate_column_type(self, key: str, column_type: str) -> str:
        """验证列类型不为空"""
        if not column_type or not column_type.strip():
            raise ValueError("列类型不能为空")
        return column_type.strip()
