import json
from src.cache.db import get_cached_phone, get_cached_clusters, save_analysis

def get_cached_analysis(brand: str, model: str, top_n: int, max_age_days: int = 3) -> dict | None:
    """
    Higher-level search for cached results. Returns a full dict compatible with the API's response format if found.
    """
    phone = get_cached_phone(brand, model, top_n, max_age_days)
    if not phone:
        return None
        
    clusters_rows = get_cached_clusters(phone['id'])
    
    # Reconstruct the response format
    clusters = []
    for row in clusters_rows:
        clusters.append({
            "representative_name": row['representative_name'],
            "total_mentions": row['total_mentions'],
            "sentiment_summary": {
                "positive": row['positive'],
                "neutral": row['neutral'],
                "negative": row['negative']
            },
            "original_mentions": json.loads(row['original_mentions'])
        })
        
    return {
        "brand": phone['brand'],
        "model": phone['model'],
        "review_count": phone['review_count'],
        "clusters": clusters,
        "_cached": True, # For debugging/visibility
    }

def cache_analysis_result(brand: str, model: str, top_n: int, review_count: int, clusters: list[dict]):
    """
    Saves the clusters to the cache.
    """
    # Simply delegate to DB layer
    save_analysis(brand, model, top_n, review_count, clusters)
