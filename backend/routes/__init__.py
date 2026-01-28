# Routes module
from .admin import router as admin_router
from .appointments import router as appointments_router
from .export import router as export_router
from .notifications import router as notifications_router
from .analytics import router as analytics_router

__all__ = [
    'admin_router',
    'appointments_router',
    'export_router',
    'notifications_router',
    'analytics_router'
]
