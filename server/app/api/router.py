from fastapi import APIRouter
from .v1 import auth, users, deals, tasks, payroll, analytics, notifications, files, ai, settings

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
# TODO: подключить остальные модули