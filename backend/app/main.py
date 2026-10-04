"""
SkillSathi - AI-Enabled Career Counselling & Family Decision-Support Platform
Smart India Hackathon 2026 - Problem Statement 26241

Main FastAPI Application Entry Point
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import get_settings
from app.routers.api_router import api_router
from app.utils.logger import logger
from app.utils.response import error_response, success_response

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and graceful shutdown lifecycle."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION} ({settings.APP_ENV})")
    logger.info(f"Tagline: {settings.APP_TAGLINE}")
    logger.info(f"AI Provider: {settings.AI_PROVIDER} (model: {settings.AI_MODEL})")

    # Ensure tables exist and seed initial dataset if empty
    from app.database import Base, engine, SessionLocal
    from app.models.trade import Trade
    from app.data_sources.sync_engine import sync_engine
    from app.data_sources.demo_users_seed import seed_demo_users

    try:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            trade_count = db.query(Trade).count()
            if trade_count == 0:
                logger.info("Database is empty. Running initial sync across all official adapters...")
                await sync_engine.sync_all(db, triggered_by="AUTO_STARTUP_SEED")
                logger.info("Initial sync completed successfully.")
            
            # Always ensure demo accounts exist
            seed_demo_users(db)
        finally:
            db.close()
    except Exception as exc:
        logger.warning(f"Database startup initialization notice: {exc}")


    yield
    logger.info(f"Shutting down {settings.APP_NAME}...")


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "SkillSathi: AI-Enabled Career Counselling and Family Decision-Support Platform "
        "for Vocational Education. "
        "Treats the entire family as the decision unit to bridge aspirations and parental concerns."
    ),
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Configure Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API v1 routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
async def root():
    """Root entrypoint linking to API diagnostics."""
    return success_response(
        data={
            "app": settings.APP_NAME,
            "tagline": settings.APP_TAGLINE,
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "api_v1": f"{settings.API_V1_STR}/health"
        },
        message="Welcome to SkillSathi API. Visit /docs for API documentation."
    )


# Exception Handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            message=str(exc.detail),
            error=f"HTTP_{exc.status_code}",
            meta={"path": request.url.path}
        )
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response(
            message="Request validation failed",
            error=str(errors),
            meta={"details": errors, "path": request.url.path}
        )
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response(
            message="An unexpected internal server error occurred.",
            error=str(exc) if settings.DEBUG else "Internal Server Error",
            meta={"path": request.url.path}
        )
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG
    )
