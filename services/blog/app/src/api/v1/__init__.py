from fastapi import APIRouter
from .ping import ping
from .posts import posts

router = APIRouter()
router.include_router(ping.router, prefix="", tags=["ping"])
router.include_router(posts.router, prefix="/posts", tags=["posts"])
