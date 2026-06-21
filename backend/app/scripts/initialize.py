"""
数据库初始化与种子数据管理。

简化策略：每张表为空时一次性插入种子数据，已有数据则跳过。
改 JSON → 清空对应表 → 重启即可。
"""

import asyncio
import json
import re
from datetime import datetime, time
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.module_platform.email.model import EmailConfigModel, EmailTemplateModel
from app.api.v1.module_platform.invoice.model import InvoiceModel
from app.api.v1.module_platform.menu.model import MenuModel
from app.api.v1.module_platform.order.model import OrderModel, PaymentRecordModel, RefundModel
from app.api.v1.module_platform.package.model import PackageMenuModel, PackageModel
from app.api.v1.module_platform.plugin.model import PluginModel, TenantPluginModel
from app.api.v1.module_platform.tenant.model import TenantModel, TenantUserModel
from app.api.v1.module_system.dept.model import DeptModel
from app.api.v1.module_system.dict.model import DictDataModel, DictTypeModel
from app.api.v1.module_system.log.model import LoginLogModel, OperationLogModel
from app.api.v1.module_system.notice.model import NoticeModel, NoticeReadModel
from app.api.v1.module_system.params.model import ParamsModel
from app.api.v1.module_system.position.model import PositionModel
from app.api.v1.module_system.role.model import RoleModel
from app.api.v1.module_system.ticket.model import TicketModel
from app.api.v1.module_system.user.model import UserModel, UserRolesModel
from app.config.path_conf import SCRIPT_DIR
from app.core.database import async_db_session, create_tables
from app.core.logger import logger
from app.plugin.module_example.demo.model import DemoModel
from app.plugin.module_task.cronjob.node.model import NodeModel
from app.plugin.module_task.workflow.nodes.model import WorkflowNodeTypeModel


class InitializeData:
    """初始化数据库和基础数据"""

    _DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
    _DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    _TIME_RE = re.compile(r"^\d{2}:\d{2}:\d{2}(\.\d+)?$")

    # 按依赖关系排序：先基础表，再关联表
    prepare_init_models: list[type] = [
        # ── 平台管理：基础表 ──
        PackageModel,
        TenantModel,
        PluginModel,
        MenuModel,
        # ── 系统管理：基础表 ──
        ParamsModel,
        DeptModel,
        RoleModel,
        DictTypeModel,
        DictDataModel,
        PositionModel,
        UserModel,
        # ── 平台管理：依赖用户的表 ──
        EmailConfigModel,
        EmailTemplateModel,
        OrderModel,
        InvoiceModel,
        PaymentRecordModel,
        RefundModel,
        # ── 关联表 ──
        UserRolesModel,
        TenantUserModel,
        PackageMenuModel,
        TenantPluginModel,
        # ── 其他系统/业务表 ──
        NoticeModel,
        NoticeReadModel,
        TicketModel,
        # ── 日志表（追加写入） ──
        LoginLogModel,
        OperationLogModel,
        # ── 插件表 ──
        NodeModel,
        WorkflowNodeTypeModel,
        DemoModel,
    ]

    # 树形模型：JSON 含嵌套 children，需递归创建对象
    _RECURSIVE_TABLES: set[str] = {"platform_menu", "sys_dept"}

    async def init_db(self) -> None:
        """建表并导入种子数据"""
        try:
            await create_tables()
        except asyncio.exceptions.TimeoutError:
            logger.error("❌️ 数据库表结构初始化超时")
            raise

        async with async_db_session() as session:
            async with session.begin():
                await self.__init_data(session)

    async def __init_data(self, db: AsyncSession) -> None:
        """按依赖顺序初始化各表种子数据"""
        dict_type_mapping: dict[str, Any] = {}  # dict_type → DictTypeModel 实例

        for model in self.prepare_init_models:
            table_name = model.__tablename__

            data = await self.__load_json(table_name)
            if not data:
                logger.info(f"⏭️  跳过 {table_name} 表，无初始化数据")
                continue

            try:
                # 树形表（platform_menu / sys_dept）：递归创建含 children 的对象
                if table_name in self._RECURSIVE_TABLES:
                    count = await db.execute(select(func.count()).select_from(model))
                    if count.scalar():
                        logger.info(f"⏭️  跳过 {table_name} 表数据初始化（表已有数据）")
                        continue
                    objs = self.__create_objects_with_children(data, model)
                    db.add_all(objs)
                    await db.flush()
                    logger.info(f"✅️ 已向 {table_name} 写入初始化数据")
                    continue

                # 字典类型表：存储类型映射供字典数据使用
                if table_name == "sys_dict_type":
                    count = await db.execute(select(func.count()).select_from(model))
                    if count.scalar():
                        logger.info(f"⏭️  跳过 {table_name} 表数据初始化（表已有数据）")
                        continue
                    objs = []
                    for item in data:
                        obj = model(**item)
                        objs.append(obj)
                        dict_type_mapping[item["dict_type"]] = obj
                    db.add_all(objs)
                    await db.flush()
                    logger.info(f"✅️ 已向 {table_name} 写入初始化数据")
                    continue

                # 字典数据表：关联 dict_type_id
                if table_name == "sys_dict_data":
                    count = await db.execute(select(func.count()).select_from(model))
                    if count.scalar():
                        logger.info(f"⏭️  跳过 {table_name} 表数据初始化（表已有数据）")
                        continue
                    objs = []
                    for item in data:
                        dict_type_str = item.get("dict_type")
                        if dict_type_str not in dict_type_mapping:
                            logger.warning(f"⚠️  未找到字典类型 {dict_type_str}，跳过")
                            continue
                        item["dict_type_id"] = dict_type_mapping[dict_type_str].id
                        objs.append(model(**item))
                    db.add_all(objs)
                    await db.flush()
                    logger.info(f"✅️ 已向 {table_name} 写入初始化数据")
                    continue

                # 日志表：追加写入，已有数据跳过
                if table_name in ("sys_login_log", "sys_operation_log"):
                    count = await db.execute(select(func.count()).select_from(model))
                    if count.scalar():
                        logger.info(f"⏭️  跳过 {table_name} 表数据初始化（表已有数据）")
                        continue
                    objs = [model(**item) for item in data]
                    db.add_all(objs)
                    await db.flush()
                    logger.info(f"✅️ 已向 {table_name} 写入 {len(objs)} 条")
                    continue

                # 普通表：空表时插入，已有数据跳过
                count = await db.execute(select(func.count()).select_from(model))
                if count.scalar():
                    logger.info(f"⏭️  跳过 {table_name} 表数据初始化（表已有数据）")
                    continue
                objs = [model(**item) for item in data]
                db.add_all(objs)
                await db.flush()
                logger.info(f"✅️ 已向 {table_name} 写入初始化数据")

            except Exception:
                logger.error(f"❌️ 初始化 {table_name} 表数据失败")
                raise

    @staticmethod
    def __create_objects_with_children(data: list[dict], model_class: type) -> list:
        """递归创建树形模型实例，处理嵌套 children 并注入 parent_id"""

        def _create(obj_data: dict) -> Any:
            children_data = obj_data.pop("children", [])

            # JSON 中子节点 parent_id 通常为 null，先按原始值创建
            obj = model_class(**obj_data)

            if children_data:
                obj.children = [_create(child) for child in children_data]

            return obj

        return [_create(item) for item in data]

    async def __load_json(self, filename: str) -> list[dict]:
        """读取并解析种子数据 JSON 文件"""
        json_path = SCRIPT_DIR / f"{filename}.json"
        if not json_path.exists():
            return []

        try:
            with open(json_path, encoding="utf-8") as f:
                raw = json.loads(f.read())
            return [self._parse_date_strings(item) for item in raw]
        except json.JSONDecodeError as e:
            logger.error(f"❌️ 解析 {json_path} 失败: {e!s}")
            raise
        except Exception as e:
            logger.error(f"❌️ 读取 {json_path} 失败: {e!s}")
            raise

    @classmethod
    def _parse_date_strings(cls, data: dict) -> dict:
        """递归转换 JSON 中的日期时间字符串为 datetime 对象（兼容 PostgreSQL）"""
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                if cls._DATETIME_RE.match(value):
                    result[key] = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                elif cls._DATE_RE.match(value):
                    result[key] = datetime.strptime(value, "%Y-%m-%d").date()
                elif cls._TIME_RE.match(value):
                    result[key] = time.fromisoformat(value)
                else:
                    result[key] = value
            elif isinstance(value, dict):
                result[key] = cls._parse_date_strings(value)
            else:
                result[key] = value
        return result
