from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import audit

app = FastAPI(title="India Legal AI — Labour Code Compliance Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(audit.router, prefix="/api/v1")