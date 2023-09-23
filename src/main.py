from fastapi import FastAPI

import src.database as database_declaration

from .documents.router import router as documents_router


app: FastAPI = FastAPI(
    docs_url="/swagger",
    lifespan=database_declaration.lifespan
)

app.include_router(documents_router)
