from fastapi import FastAPI
from .routers import store_router, product_router,price_router, province_router
# from .routers.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Grocery Scout API", version="1.0.0")

origins = [
    "http://localhost:3000",  # Next.js frontend
    "http://127.0.0.1:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {
        "message": "Welcome to the Grocery Price Checker API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

#store endpoints
app.include_router(store_router)

#product endpoints
app.include_router(product_router)

#price endpoints for individual stores
app.include_router(price_router)

#price endpoints for province
app.include_router(province_router)