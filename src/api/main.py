from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Best-effort startup bootstrap for demo/reviewer convenience."""
    try:
        from src.models.seed_model import seed_demo_model
        seed_demo_model(force=False)
    except Exception:
        pass
    try:
        from src.data.database import init_db
        init_db()
    except Exception:
        pass
    yield


app = FastAPI(
    title="FraudLens AI v2 API",
    description="Real-time fraud detection scoring, alert workflow, and model metadata API",
    version="2.0.0",
    lifespan=lifespan,
)
app.include_router(router)
