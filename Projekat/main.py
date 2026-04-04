import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.analysis.embedder import Embedder
from src.analysis.clusterer import Clusterer
from src.api.routes import router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load heavy resources once at startup, share them across all requests."""
    db_path = os.path.join("data", "reviews.db")
    if not os.path.exists(db_path):
        print(f"CRITICAL ERROR: Database {db_path} not found!")
        raise RuntimeError("reviews.db not found")

    print("Loading SBERT embedding model...")
    embedder = Embedder()
    # Trigger lazy load now so first request is not slow
    _ = embedder.model
    print("Embedding model loaded.")

    app.state.embedder = embedder
    app.state.clusterer = Clusterer(embedder=embedder)

    yield

    # Shutdown: nothing to clean up


app = FastAPI(
    title="Phone Review Analysis API",
    description="Extracts and clusters aspect-sentiment pairs from phone reviews.",
    version="1.0.0",
    lifespan=lifespan
)

# Allow frontend (any origin) during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Phone Review Analysis API is running."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)