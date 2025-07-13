from fastapi import APIRouter
from .ping import ping
from .projects import project

router = APIRouter()
router.include_router(ping.router, prefix="", tags=["ping"])
# router.include_router(project.router, prefix="projects", tags=["projects"])
