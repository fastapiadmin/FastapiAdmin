from fastapi import APIRouter

from app.api.v1.module_system.auth.controller import AuthRouter
from app.api.v1.module_system.dept.controller import DeptRouter
from app.api.v1.module_system.dict.controller import DictRouter
from app.api.v1.module_system.log import LogRouter
from app.api.v1.module_system.notice.controller import NoticeRouter
from app.api.v1.module_system.params.controller import ParamsRouter
from app.api.v1.module_system.position.controller import PositionRouter
from app.api.v1.module_system.role.controller import RoleRouter
from app.api.v1.module_system.ticket.controller import TicketRouter
from app.api.v1.module_system.user.controller import UserRouter

system_router = APIRouter(prefix="/system")

system_router.include_router(AuthRouter)
system_router.include_router(DeptRouter)
system_router.include_router(DictRouter)
system_router.include_router(LogRouter)
system_router.include_router(NoticeRouter)
system_router.include_router(ParamsRouter)
system_router.include_router(PositionRouter)
system_router.include_router(RoleRouter)
system_router.include_router(TicketRouter)
system_router.include_router(UserRouter)
