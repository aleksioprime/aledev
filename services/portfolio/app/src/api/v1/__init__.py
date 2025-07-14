from fastapi import APIRouter
from .ping import ping
from .projects import project
from .experiences import experience

router = APIRouter()
router.include_router(ping.router, prefix="", tags=["ping"])
router.include_router(project.router, prefix="/projects", tags=["projects"])
router.include_router(experience.router, prefix="/experiences", tags=["experiences"])
