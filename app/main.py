from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import auth, tasks, payment

def create_app() -> FastAPI:
    app = FastAPI(title="FocusAI", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGNINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router)
    app.include_router(tasks.router)
    app.include_router(payment.router)

    return app

app = create_app()