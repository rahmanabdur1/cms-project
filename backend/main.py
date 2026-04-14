from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from database import engine, Base
from routers import contents, categories, upload
from logger import logger
import os

# ─── Create all tables ──────────────────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ─── Ensure upload dir exists ───────────────────────────────────────────────
os.makedirs("static/uploads", exist_ok=True)

# ─── App ────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="CMS API",
    description="Dynamic Interactive Content Management System API",
    version="1.0.0",
)

# ─── CORS ───────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        os.getenv("FRONTEND_URL", "http://localhost:3000"),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Static files ───────────────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory="static"), name="static")

# ─── Routers ────────────────────────────────────────────────────────────────
app.include_router(contents.router)
app.include_router(categories.router)
app.include_router(upload.router)


# ─── Lifecycle ──────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    logger.info("CMS API started successfully")


@app.on_event("shutdown")
async def shutdown():
    logger.info("CMS API shutting down")


# ─── Error handlers ─────────────────────────────────────────────────────────
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"}
    )


@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.exception_handler(422)
async def validation_error_handler(request: Request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)}
    )


# ─── Health ─────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {"message": "CMS API Running", "version": "1.0.0"}


@app.get("/health", tags=["Root"])
def health():
    return {"status": "ok"}