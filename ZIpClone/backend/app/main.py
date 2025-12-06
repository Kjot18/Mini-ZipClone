from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema
from app.database import engine, Base
from app.config import settings
from app.init_db import init_db

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Procurement Workflow API")

@app.on_event("startup")
async def startup_event():
    """Initialize database with default users on startup"""
    init_db()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GraphQL endpoint
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {"message": "Procurement Workflow API", "graphql": "/graphql"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

