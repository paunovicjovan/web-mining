from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from src.data.loader import get_top_reviews, get_all_brands, get_models_for_brand
from src.extraction.processor import extract_aspects_parallel

router = APIRouter()


class AnalyzeRequest(BaseModel):
    brand: str
    model: str
    top_n: int = 50


@router.get("/brands")
async def brands():
    """Return all distinct phone brands available in the database."""
    result = get_all_brands()
    return {"brands": result}


@router.get("/models")
async def models(brand: str):
    """Return all models for a given brand."""
    if not brand:
        raise HTTPException(status_code=400, detail="brand parameter is required")
    result = get_models_for_brand(brand)
    return {"brand": brand, "models": result}


@router.post("/analyze")
async def analyze(request: Request, body: AnalyzeRequest):
    """
    Run the full analysis pipeline for a given brand and model.
    Fetches top_n reviews, extracts (aspect, sentiment) pairs in parallel,
    clusters them semantically, and returns the ranked clusters.
    """
    # 1. Fetch top reviews from DB (already truncated to 500 words)
    df = get_top_reviews(body.brand, body.model, top_n=body.top_n)
    if df.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No reviews found for {body.brand} {body.model}"
        )

    reviews = df['Reviews'].dropna().tolist()
    actual_count = len(reviews)

    # 2. Extract (aspect, sentiment) pairs — one worker per review for max parallelism
    pairs = extract_aspects_parallel(reviews, max_workers=actual_count)
    if not pairs:
        raise HTTPException(
            status_code=422,
            detail="Extraction returned no aspect-sentiment pairs."
        )

    # 3. Cluster aspects using the pre-loaded singleton from app.state
    clusterer = request.app.state.clusterer
    clusters = clusterer.cluster_aspects(pairs)

    return {
        "brand": body.brand,
        "model": body.model,
        "review_count": actual_count,
        "clusters": clusters
    }
