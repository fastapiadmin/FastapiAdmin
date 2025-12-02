# -*- coding: utf-8 -*-

import importlib
import re
import uuid
from pathlib import Path
from typing import Any, Literal, Sequence, Generator
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.engine.row import Row
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.sql.expression import TextClause, null

from app.config.setting import settings
from app.core.logger import log
from app.core.exceptions import CustomException


def import_module(module: str, desc: str) -> Any:
    """
    动态导入模块

    参数:
    - module (str): 模块名称。
    - desc (str): 模块描述。

    返回:
    - Any: 模块对象。
    """
    try:
        module_path, module_class = module.rsplit(".", 1)
        module = importlib.import_module(module_path)
        return getattr(module, module_class)
    except ModuleNotFoundError:
        log.error(f"❗️ 导入{desc}失败,未找到模块:{module}")
        raise
    except AttributeError:
        log.error(f"❗ ️导入{desc}失败,未找到模块方法:{module}")
        raise


async def import_modules_async(modules: list, desc: str, **kwargs) -> None:
    """
    异步导入模块列表

    参数:
    - modules (list[str]): 模块列表。
    - desc (str): 模块描述。
    - kwargs: 额外参数。

    返回:
    - None
    """
    for module in modules:
        if not module:
            continue
        try:
            module_path = module[0:module.rindex(".")]
            module_name = module[module.rindex(".") + 1:]
            module_obj = importlib.import_module(module_path)
            await getattr(module_obj, module_name)(**kwargs)
        except ModuleNotFoundError:
            log.error(f"❌️ 导入{desc}失败,未找到模块:{module}")
            raise
        except AttributeError:
            log.error(f"❌️ 导入{desc}失败,未找到模块方法:{module}")
            raise


def get_random_character() -> str:
    """
    生成随机字符串

    返回:
    - str: 随机字符串。
    """
    return uuid.uuid4().hex


def uuid4_str() -> str:
    """数据库引擎 UUID 类型兼容性解决方案"""
    return str(uuid.uuid4())


def get_parent_id_map(model_list: Sequence[DeclarativeBase]) -> dict[int, int]:
    """
    获取父级 ID 映射字典

    参数:
    - model_list (Sequence[DeclarativeBase]): 模型列表。

    返回:
    - Dict[int, int]: {id: parent_id} 映射字典。
    """
    return {item.id: item.parent_id for item in model_list}


def get_parent_recursion(id: int, id_map: dict[int, int], ids: list[int] | None = None) -> list[int]:
    """
    递归获取所有父级 ID

    参数:
    - id (int): 当前 ID。
    - id_map (dict[int, int]): ID 映射字典。
    - ids (list[int] | None): 已收集的 ID 列表。

    返回:
    - list[int]: 所有父级 ID 列表。
    """
    ids = ids or []
    if id in ids:
        raise CustomException(msg="递归获取父级ID失败,不可以自引用")
    ids.append(id)
    parent_id = id_map.get(id)
    if parent_id:
        get_parent_recursion(parent_id, id_map, ids)
    return ids


def get_child_id_map(model_list: Sequence[DeclarativeBase]) -> dict[int, list[int]]:
    """
    获取子级 ID 映射字典

    参数:
    - model_list (Sequence[DeclarativeBase]): 模型列表。

    返回:
    - Dict[int, List[int]]: {id: [child_ids]} 映射字典。
    """
    data_map = {}
    for model in model_list:
        data_map.setdefault(model.id, [])
        if model.parent_id:
            data_map.setdefault(model.parent_id, []).append(model.id)
    return data_map


def get_child_recursion(id: int, id_map: dict[int, list[int]], ids: list[int] | None= None) -> list[int]:
    """
    递归获取所有子级 ID

    参数:
    - id (int): 当前 ID。
    - id_map (dict[int, list[int]]): ID 映射字典。
    - ids (list[int] | None): 已收集的 ID 列表。

    返回:
    - list[int]: 所有子级 ID 列表。
    """
    ids = ids or []
    ids.append(id)
    for child in id_map.get(id, []):
        get_child_recursion(child, id_map, ids)
    return ids


def traversal_to_tree(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    通过遍历算法构造树形结构

    参数:
    - nodes (list[dict[str, Any]]): 树节点列表。

    返回:
    - list[dict[str, Any]]: 构造后的树形结构列表。
    """
    tree: list[dict[str, Any]] = []
    node_dict = {node['id']: node for node in nodes}

    for node in nodes:
        # 确保每个节点都有children字段，即使没有子节点也设置为null
        if 'children' not in node:
            node['children'] = None
            
        parent_id = node['parent_id']
        if parent_id is None:
            tree.append(node)
        else:
            parent_node = node_dict.get(parent_id)
            if parent_node is not None:
                if 'children' not in parent_node or parent_node['children'] is None:
                    parent_node['children'] = []
                if node not in parent_node['children']:
                    parent_node['children'].append(node)
            else:
                if node not in tree:
                    tree.append(node)
    
    # 确保所有节点都有children字段
    for node in tree:
        if 'children' not in node:
            node['children'] = None

    return tree


def recursive_to_tree(nodes: list[dict[str, Any]], *, parent_id: int | None = None) -> list[dict[str, Any]]:
    """
    通过递归算法构造树形结构（性能影响较大）

    参数:
    - nodes (list[dict[str, Any]]): 树节点列表。
    - parent_id (int | None): 父节点 ID,默认为 None 表示根节点。

    返回:
    - list[dict[str, Any]]: 构造后的树形结构列表。
    """
    tree: list[dict[str, Any]] = []
    for node in nodes:
        if node['parent_id'] == parent_id:
            child_nodes = recursive_to_tree(nodes, parent_id=node['id'])
            if child_nodes:
                node['children'] = child_nodes
            tree.append(node)
    return tree


def bytes2human(n: int, format_str: str = '%(value).1f%(symbol)s') -> str:
    """
    字节数转人类可读格式
    Used by various scripts. See:
    http://goo.gl/zeJZl

    >>> bytes2human(10000)
    '9.8K'
    >>> bytes2human(100001221)
    '95.4M'

    参数:
    - n (int): 字节数。
    - format_str (str): 格式化字符串，默认 '%(value).1f%(symbol)s'。

    返回:
    - str: 可读的字节字符串，如 '1.5MB'。
    """
    symbols = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    prefix = {s: 1 << (i + 1) * 10 for i, s in enumerate(symbols[1:])}
    for symbol in reversed(symbols[1:]):
        if n >= prefix[symbol]:
            value = float(n) / prefix[symbol]
            return format_str % locals()
    return format_str % dict(symbol=symbols[0], value=n)


def bytes2file_response(bytes_info: bytes) -> Generator[bytes, Any, None]:
    """生成文件响应"""
    yield bytes_info


def get_filepath_from_url(url: str) -> Path:
    """
    工具方法：根据请求参数获取文件路径

    参数:
    - url (str): 请求参数中的 url 参数。

    返回:
    - Path: 文件路径。
    """
    file_info = url.split('?')[1].split('&')
    task_id = file_info[0].split('=')[1]
    file_name = file_info[1].split('=')[1]
    task_path = file_info[2].split('=')[1]
    filepath = settings.STATIC_ROOT.joinpath(task_path, task_id, file_name)

    return filepath


class SqlalchemyUtil:
    """
    sqlalchemy工具类
    """

    @classmethod
    def base_to_dict(
        cls, obj: DeclarativeBase | dict[str, Any], transform_case: Literal['no_case', 'snake_to_camel', 'camel_to_snake'] = 'no_case'
    ):
        """
        将sqlalchemy模型对象转换为字典

        :param obj: sqlalchemy模型对象或普通字典
        :param transform_case: 转换得到的结果形式，可选的有'no_case'(不转换)、'snake_to_camel'(下划线转小驼峰)、'camel_to_snake'(小驼峰转下划线)，默认为'no_case'
        :return: 字典结果
        """
        if isinstance(obj, DeclarativeBase):
            base_dict = obj.__dict__.copy()
            base_dict.pop('_sa_instance_state', None)
            for name, value in base_dict.items():
                if isinstance(value, InstrumentedList):
                    base_dict[name] = cls.serialize_result(value, 'snake_to_camel')
        elif isinstance(obj, dict):
            base_dict = obj.copy()
        if transform_case == 'snake_to_camel':
            return {CamelCaseUtil.snake_to_camel(k): v for k, v in base_dict.items()}
        elif transform_case == 'camel_to_snake':
            return {SnakeCaseUtil.camel_to_snake(k): v for k, v in base_dict.items()}

        return base_dict

    @classmethod
    def serialize_result(
        cls, result: Any, transform_case: Literal['no_case', 'snake_to_camel', 'camel_to_snake'] = 'no_case'
    ):
        """
        将sqlalchemy查询结果序列化

        :param result: sqlalchemy查询结果
        :param transform_case: 转换得到的结果形式，可选的有'no_case'(不转换)、'snake_to_camel'(下划线转小驼峰)、'camel_to_snake'(小驼峰转下划线)，默认为'no_case'
        :return: 序列化结果
        """
        if isinstance(result, (DeclarativeBase, dict)):
            return cls.base_to_dict(result, transform_case)
        elif isinstance(result, list):
            return [cls.serialize_result(row, transform_case) for row in result]
        elif isinstance(result, Row):
            if all([isinstance(row, DeclarativeBase) for row in result]):
                return [cls.base_to_dict(row, transform_case) for row in result]
            elif any([isinstance(row, DeclarativeBase) for row in result]):
                return [cls.serialize_result(row, transform_case) for row in result]
            else:
                result_dict = result._asdict()
                if transform_case == 'snake_to_camel':
                    return {CamelCaseUtil.snake_to_camel(k): v for k, v in result_dict.items()}
                elif transform_case == 'camel_to_snake':
                    return {SnakeCaseUtil.camel_to_snake(k): v for k, v in result_dict.items()}
                return result_dict
        return result

    @classmethod
    def get_server_default_null(cls, dialect_name: str, need_explicit_null: bool = True) -> TextClause | None:
        """
        根据数据库方言动态返回值为null的server_default

        :param dialect_name: 数据库方言名称
        :param need_explicit_null: 是否需要显式DEFAULT NULL
        :return: 不同数据库方言对应的null_server_default
        """
        if need_explicit_null and dialect_name == 'postgres':
            return null()
        return None


class CamelCaseUtil:
    """
    下划线形式(snake_case)转小驼峰形式(camelCase)工具方法
    """

    @classmethod
    def snake_to_camel(cls, snake_str: str):
        """
        下划线形式字符串(snake_case)转换为小驼峰形式字符串(camelCase)

        :param snake_str: 下划线形式字符串
        :return: 小驼峰形式字符串
        """
        # 分割字符串
        words = snake_str.split('_')
        # 小驼峰命名，第一个词首字母小写，其余词首字母大写
        # return words[0] + ''.join(word.capitalize() for word in words[1:])
        # 大驼峰命名，所有词首字母大写
        return ''.join(word.capitalize() for word in words)

    @classmethod
    def transform_result(cls, result: Any):
        """
        针对不同类型将下划线形式(snake_case)批量转换为小驼峰形式(camelCase)方法

        :param result: 输入数据
        :return: 小驼峰形式结果
        """
        return SqlalchemyUtil.serialize_result(result=result, transform_case='snake_to_camel')


class SnakeCaseUtil:
    """
    小驼峰形式(camelCase)转下划线形式(snake_case)工具方法
    """

    @classmethod
    def camel_to_snake(cls, camel_str: str):
        """
        小驼峰形式字符串(camelCase)转换为下划线形式字符串(snake_case)

        :param camel_str: 小驼峰形式字符串
        :return: 下划线形式字符串
        """
        # 在大写字母前添加一个下划线，然后将整个字符串转为小写
        words = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', words).lower()

    @classmethod
    def transform_result(cls, result: Any):
        """
        针对不同类型将下划线形式(snake_case)批量转换为小驼峰形式(camelCase)方法

        :param result: 输入数据
        :return: 小驼峰形式结果
        """
        return SqlalchemyUtil.serialize_result(result=result, transform_case='camel_to_snake')

