from fastapi import APIRouter

from .portal.controller import PortalRouter

application_router = APIRouter(prefix="/application")

application_router.include_router(PortalRouter)
