# server/app/api/router.py
from fastapi import APIRouter

# Импортируем подмодули v1, каждый должен экспортировать `router`
from .v1 import (
    auth,
    users,
    deals,
    tasks,
    payroll,
    analytics,
    notifications,
    files,
    ai,
    settings,
)

router = APIRouter()

# Подключаем роутеры модулей под версионным префиксом
router.include_router(auth.router,          prefix="/api/v1/auth",          tags=["auth"])
router.include_router(users.router,         prefix="/api/v1/users",         tags=["users"])
router.include_router(deals.router,         prefix="/api/v1/deals",         tags=["deals"])
router.include_router(tasks.router,         prefix="/api/v1/tasks",         tags=["tasks"])
router.include_router(payroll.router,       prefix="/api/v1/payroll",       tags=["payroll"])
router.include_router(analytics.router,     prefix="/api/v1/analytics",     tags=["analytics"])
router.include_router(notifications.router, prefix="/api/v1/notifications", tags=["notifications"])
router.include_router(files.router,         prefix="/api/v1/files",         tags=["files"])
router.include_router(ai.router,            prefix="/api/v1/ai",            tags=["ai"])
router.include_router(settings.router,      prefix="/api/v1/settings",      tags=["settings"])