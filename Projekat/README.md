# Phone Review Analysis

Web Mining university project for aspect-based sentiment analysis on mobile phone reviews.

The app lets users choose a phone brand and model, then analyzes review texts to surface the most discussed aspects (for example battery, screen, camera) with sentiment breakdowns.

## What Is Implemented

- FastAPI backend with endpoints for brand/model lookup and full analysis
- Streamlit frontend for interactive selection and results display
- Parallel aspect extraction with `langextract`
- Semantic clustering with SBERT embeddings + agglomerative clustering
- SQLite-based caching of analysis responses

## How The Pipeline Works

1. Fetch top `N` reviews for selected brand/model from `reviews.db`
2. Truncate each review to 500 words
3. Extract `(aspect, sentiment)` pairs in parallel using `langextract`
4. Generate sentence embeddings with `sentence-transformers`
5. Cluster similar aspects using cosine-distance agglomerative clustering
6. Build final cluster objects with representative names and sentiment counts
7. Cache results in `cache.db` for faster repeated requests

## Project Structure

```text
Projekat/
├── data/
│   ├── csv/                    # Source/prepared CSV data
│   └── db/
│       ├── reviews.db          # Main reviews database
│       └── cache.db            # Analysis cache database
├── src/
│   ├── analysis/               # Embeddings + clustering logic
│   ├── api/                    # FastAPI routes
│   ├── cache/                  # Cache DB init + read/write services
│   ├── data/                   # Review/brand/model loaders from SQLite
│   └── extraction/             # LLM extraction logic + prompts/examples
├── streamlit_app.py            # Streamlit UI (frontend)
├── main.py                     # FastAPI app entrypoint (backend)
├── requirements.txt
└── .env.template
```

## Requirements

- Python 3.10+
- Local SQLite database file at `data/db/reviews.db`
- API key for `langextract` provider (configured through `.env`)

## Dataset

The project is based on the Kaggle dataset:

- [Amazon Reviews: Unlocked Mobile Phones](https://www.kaggle.com/datasets/PromptCloudHQ/amazon-reviews-unlocked-mobile-phones)

## Environment Variables

Copy `.env.template` to `.env` and set values:

```env
LANGEXTRACT_API_KEY=your_gemini_api_key_here
LANGEXTRACT_MODEL_ID=gemini-2.5-flash
BACKEND_URL=http://127.0.0.1:8000
REVIEWS_DB_PATH=data/db/reviews.db
CACHE_DB_PATH=data/db/cache.db
```

## Installation

```bash
python -m venv venv
```

Windows PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running The Project

Open two terminals (both with virtual environment activated).

1) Start backend API:

```bash
uvicorn main:app
```

2) Start Streamlit frontend:

```bash
streamlit run streamlit_app.py
```

Then open the Streamlit URL shown in terminal (typically `http://localhost:8501`).

## API Endpoints

- `GET /` - health/info message
- `GET /brands` - list available brands
- `GET /models?brand=<brand>` - list models for selected brand
- `POST /analyze` - run full analysis

Example analyze payload:

```json
{
  "brand": "Samsung",
  "model": "Galaxy S24 Ultra",
  "top_n": 50,
  "force_refresh": false,
  "max_age_days": 3
}
```

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) + `uvicorn`
- [Streamlit](https://streamlit.io/)
- [langextract](https://github.com/google/langextract)
- [sentence-transformers](https://www.sbert.net/)
- `scikit-learn`, `pandas`, `nltk`, `rapidfuzz`
- SQLite for review data and cache