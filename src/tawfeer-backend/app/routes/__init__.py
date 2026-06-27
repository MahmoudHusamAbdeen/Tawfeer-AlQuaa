"""Routes package - exports all route routers."""
from app.routes.auth_routes import router as auth_router
from app.routes.ai_routes import router as ai_router
from app.routes.donation_routes import router as donation_router
from app.routes.admin_routes import router as admin_router
from app.routes.driver_routes import router as driver_router
from app.routes.government_routes import router as government_router

__all__ = [
    "auth_router",
    "ai_router",
    "donation_router",
    "admin_router",
    "driver_router",
    "government_router",
]
