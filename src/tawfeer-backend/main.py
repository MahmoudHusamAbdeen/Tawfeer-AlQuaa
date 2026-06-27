"""
Tawfeer Backend - Main Application Entry Point
FastAPI application with MongoDB and OpenAI integration.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import connect_to_mongo, close_mongo_connection
from app.routes import (
    auth_router, ai_router, donation_router,
    admin_router, driver_router, government_router
)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    # Startup
    await connect_to_mongo()
    print("=" * 50)
    print("  Tawfeer Backend Server Started")
    print(f"  MongoDB: {settings.MONGODB_URI}")
    print(f"  Database: {settings.MONGODB_DB_NAME}")
    print(f"  OpenAI Key: {'Configured' if settings.OPENAI_API_KEY else 'NOT SET - AI features will use fallback'}")
    print(f"  Docs: http://localhost:{settings.PORT}/docs")
    print("=" * 50)
    yield
    # Shutdown
    await close_mongo_connection()


# Create FastAPI app
app = FastAPI(
    title="Tawfeer API",
    description="""
    Tawfeer Backend API - A smart food waste reduction platform built in the UAE.

    ## Features
    - **Authentication**: User signup, login, driver login, admin login
    - **AI Assistant**: OpenAI-powered recipe suggestions and food Q&A
    - **Donations**: Submit and manage food donations
    - **Food Requests**: Submit and manage food requests
    - **Admin Dashboard**: User management, order approval, driver management
    - **Driver Dashboard**: View and update delivery orders, award points
    - **Government Dashboard**: Analytics, charts, environmental impact

    ## Authentication
    Most endpoints require a JWT token. Include it in the Authorization header:
    `Authorization: Bearer <your_token>`
    """,
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware - allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router)
app.include_router(ai_router)
app.include_router(donation_router)
app.include_router(admin_router)
app.include_router(driver_router)
app.include_router(government_router)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API health check."""
    return {
        "app": "Tawfeer API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Root"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
