from app.core.base_crud import CRUDBase
from app.core.base_schema import AuthSchema

from .model import PositionModel
from .schema import PositionCreateSchema, PositionUpdateSchema


class PositionCRUD(CRUDBase[PositionModel, PositionCreateSchema, PositionUpdateSchema]):
    """岗位模块数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        super().__init__(model=PositionModel, auth=auth)
