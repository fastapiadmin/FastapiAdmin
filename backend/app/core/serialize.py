from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class Serialize(Generic[ModelType, SchemaType]):
    """
    序列化工具类，提供模型、Schema 和字典之间的转换功能
    """

    @classmethod
    def schema_to_model(cls, schema: type[SchemaType], model: type[ModelType]) -> ModelType:
        """
        将 Pydantic Schema 转换为 SQLAlchemy 模型

        参数:
        - schema (Type[SchemaType]): Pydantic Schema 实例。
        - model (Type[ModelType]): SQLAlchemy 模型类。

        返回:
        - ModelType: SQLAlchemy 模型实例。

        异常:
        - ValueError: 转换过程中可能抛出的异常。
        """
        try:
            return model(**cls.model_to_dict(model, schema))
        except Exception as e:
            raise ValueError(f"序列化失败: {e!s}")

    @classmethod
    def model_to_dict(cls, model: type[ModelType], schema: type[SchemaType]) -> dict[str, Any]:
        """
        将 SQLAlchemy 模型转换为 Pydantic Schema

        参数:
        - model (Type[ModelType]): SQLAlchemy 模型实例。
        - schema (Type[SchemaType]): Pydantic Schema 类。

        返回:
        - dict[str, Any]: 包含模型数据的字典。

        异常:
        - ValueError: 转换过程中可能抛出的异常。
        """
        try:
            return schema.model_validate(model).model_dump()
        except Exception as e:
            raise ValueError(f"反序列化失败: {e!s}")
