from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from backend.routers import store_router, product_router,price_router, province_router, auth_router, user_router
from fastapi.middleware.cors import CORSMiddleware
from backend.core.exceptions import AppError, to_http_exception, setup_exception_handlers
from backend.core.config import get_settings
from backend.middleware.rate_limit import setup_rate_limiting, limiter

app = FastAPI(title="Grocery Scout API", version="2.0.0")
settings = get_settings()

origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
    settings.website_url 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_exception_handlers(app)
setup_rate_limiting(app)

@app.get("/")
async def read_root():
    return {
        "message": "Welcome to the Grocery Price Checker API",
        "version": app.version,
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
@limiter.exempt
async def health():
    return {"status": "ok"}

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    http_exc = to_http_exception(exc)
    return JSONResponse(
        status_code=http_exc.status_code,
        content={"detail": http_exc.detail}
    )

#store endpoints
app.include_router(store_router, prefix="/api")

#product endpoints
app.include_router(product_router, prefix="/api")

#price endpoints for individual stores
app.include_router(price_router, prefix="/api")

#price endpoints for province
app.include_router(province_router, prefix="/api")

#user endpoints
app.include_router(user_router, prefix="/api")

#authentication endpoints
app.include_router(auth_router, prefix="/api")