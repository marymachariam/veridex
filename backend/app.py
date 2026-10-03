import logging

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from core.config import settings
from database import get_db
from routers.auth_router import router as auth_router
from routers.competitor_router import router as competitor_router
from routers.dashboard_router import router as dashboard_router
from routers.feature_router import router as feature_router
from routers.price_history_router import router as price_history_router
from routers.pricing_router import router as pricing_router
from routers.research_router import router as research_router
from routers.comparison_router import router as comparison_router
from routers.battlecard_router import router as battlecard_router
from routers.change_log_router import router as change_log_router
from routers.billing_router import router as billing_router
from services.scheduler_service import start_scheduler
from routers.review_router import router as review_router
from routers.history_router import router as history_router
from routers.assistant_router import router as assistant_router

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger("veridex")

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url=None if settings.is_production else "/docs",
    redoc_url=None,
    openapi_url=None if settings.is_production else "/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

@app.on_event("startup")
def _start_background_scheduler():
    start_scheduler()


@app.get("/health", tags=["system"])
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "version": settings.API_VERSION}


@app.get("/", tags=["system"])
def root():
    return {"message": "VERIDEX API", "version": settings.API_VERSION}


for router in (
    auth_router,
    dashboard_router,
    competitor_router,
    pricing_router,
    research_router,
    review_router,
    comparison_router,
    battlecard_router,
    change_log_router,
    feature_router,
    billing_router,
    price_history_router,
    history_router,
    assistant_router,
):
    app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=not settings.is_production)