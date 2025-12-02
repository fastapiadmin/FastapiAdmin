# -*- coding: utf-8 -*-

import asyncio
import json
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.path_conf import SCRIPT_DIR
from app.core.logger import log
from app.core.database import async_db_session, async_engine
from app.core.base_model import MappedBase

from app.api.v1.module_system.user.model import UserModel, UserRolesModel
from app.api.v1.module_system.role.model import RoleModel
from app.api.v1.module_system.dept.model import DeptModel
from app.api.v1.module_system.menu.model import MenuModel
from app.api.v1.module_system.params.model import ParamsModel
from app.api.v1.module_system.dict.model import DictTypeModel, DictDataModel


class InitializeData:
    """
    初始化数据库和基础数据
    """

    def __init__(self) -> None:
        """
        初始化数据库和基础数据
        """
        # 按照依赖关系排序：先创建基础表，再创建关联表
        self.prepare_init_models = [
            MenuModel,
            ParamsModel,
            DeptModel,
            DictTypeModel,
            DictDataModel,
            UserModel,
            RoleModel,
            UserRolesModel,
        ]
    
    async def __init_create_table(self) -> None:
        """
        初始化表结构（第一阶段）
        """
        try:
            # 使用引擎创建所有表
            async with async_engine.begin() as conn:
                await conn.run_sync(MappedBase.metadata.create_all)
            log.info("✅️ 数据库表结构初始化完成")
        except asyncio.exceptions.TimeoutError:
            log.error("❌️ 数据库表结构初始化超时")
            raise
        except Exception as e:
            log.error(f"❌️ 数据库表结构初始化失败: {str(e)}")
            raise

    async def __init_data(self, db: AsyncSession) -> None:
        """
        初始化基础数据

        参数:
        - db (AsyncSession): 异步数据库会话。
        """
        # 存储字典类型数据的映射，用于后续字典数据的初始化
        dict_type_mapping = {}
        
        for model in self.prepare_init_models:
            table_name = model.__tablename__
            
            # 检查表中是否已经有数据
            count_result = await db.execute(select(func.count()).select_from(model))
            existing_count = count_result.scalar()
            if existing_count and existing_count > 0:
                log.warning(f"⚠️  跳过 {table_name} 表数据初始化（表已存在 {existing_count} 条记录）")
                continue

            data = await self.__get_data(table_name)
            if not data:
                log.warning(f"⚠️  跳过 {table_name} 表，无初始化数据")
                continue
            
            try:
                # 特殊处理具有嵌套 children 数据的表
                if table_name in ["sys_dept", "sys_menu"]:
                    # 获取对应的模型类
                    model_class = DeptModel if table_name == "sys_dept" else MenuModel
                    objs = self.__create_objects_with_children(data, model_class)
                # 处理字典类型表，保存类型映射
                elif table_name == "sys_dict_type":
                    objs = []
                    for item in data:
                        obj = model(**item)
                        objs.append(obj)
                        dict_type_mapping[item['dict_type']] = obj
                # 处理字典数据表，添加dict_type_id关联
                elif table_name == "sys_dict_data":
                    objs = []
                    for item in data:
                        dict_type = item.get('dict_type')
                        if dict_type in dict_type_mapping:
                            # 添加dict_type_id关联
                            item['dict_type_id'] = dict_type_mapping[dict_type].id
                        else:
                            log.warning(f"⚠️  未找到字典类型 {dict_type}，跳过该字典数据")
                            continue
                        objs.append(model(**item))
                else:
                    # 表为空，直接插入全部数据
                    objs = [model(**item) for item in data]
                
                db.add_all(objs)
                await db.flush()
                log.info(f"✅️ 已向 {table_name} 表写入初始化数据")

            except Exception as e:
                log.error(f"❌️ 初始化 {table_name} 表数据失败: {str(e)}")
                raise

    def __create_objects_with_children(self, data: list[dict], model_class) -> list:
        """
        通用递归创建对象函数，处理嵌套的 children 数据

        参数:
        - data (list[dict]): 包含嵌套 children 数据的列表。
        - model_class: 对应的 SQLAlchemy 模型类。

        返回:
        - list: 包含创建的对象的列表。
        """
        objs = []
        
        def create_object(obj_data: dict):
            # 分离 children 数据
            children_data = obj_data.pop('children', [])
            
            # 创建当前对象
            obj = model_class(**obj_data)
            
            # 递归处理子对象
            if children_data:
                obj.children = [create_object(child) for child in children_data]
                
            return obj
        
        for item in data:
            objs.append(create_object(item))
            
        return objs

    async def __get_data(self, filename: str) -> list[dict]:
        """
        读取初始化数据文件

        参数:
        - filename (str): 文件名（不包含扩展名）。

        返回:
        - list[dict]: 解析后的 JSON 数据列表。
        """
        json_path = SCRIPT_DIR / f'{filename}.json'
        if not json_path.exists():
            return []

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.loads(f.read())
        except json.JSONDecodeError as e:
            log.error(f"❌️ 解析 {json_path} 失败: {str(e)}")
            raise
        except Exception as e:
            log.error(f"❌️ 读取 {json_path} 失败: {str(e)}")
            raise

    async def init_db(self) -> None:
        """
        执行完整初始化流程
        """
        # 先创建表结构
        await self.__init_create_table()
        
        # 再初始化数据
        async with async_db_session() as session:
            async with session.begin():
                await self.__init_data(session)
                # 确保提交事务
                await session.commit()
    