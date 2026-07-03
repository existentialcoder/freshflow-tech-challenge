from contextlib import asynccontextmanager
from fastapi import FastAPI

from .api.deps.db import engine, Base
from .api.v1.routes import data_loader, recommendations
from .core.constants import Constants


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()

app = FastAPI(title='Freshflow.ai Recommendation System', lifespan=lifespan)

@app.get('/health', tags=['Health'], include_in_schema=False)
def health():
    return {
        'status': 'ok'
    }

# Routes to be included
app.include_router(
    data_loader.router,
    prefix=Constants.API_PREFIX,
    tags=['Load Data']
)

app.include_router(
    recommendations.router,
    prefix=Constants.API_PREFIX,
    tags=['Recommendations']
)
