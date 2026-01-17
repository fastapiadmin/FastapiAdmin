from fastapi import APIRouter

from app.common.response import ResponseSchema as ResponseSchema

from .auth.controller import AuthRouter
from .dept.controller import DeptRouter
from .dict.controller import DictRouter
from .log.controller import LogRouter
from .menu.controller import MenuRouter
from .notice.controller import NoticeRouter
from .params.controller import ParamsRouter
from .position.controller import PositionRouter
from .role.controller import RoleRouter
from .user.controller import UserRouter

system_router = APIRouter(prefix="/system")

system_router.include_router(AuthRouter)
system_router.include_router(DeptRouter)
system_router.include_router(DictRouter)
system_router.include_router(LogRouter)
system_router.include_router(MenuRouter)
system_router.include_router(NoticeRouter)
system_router.include_router(ParamsRouter)
system_router.include_router(PositionRouter)
system_router.include_router(RoleRouter)
system_router.include_router(UserRouter)
