# Phone Review Analysis – Web Mining Project

This is a Web Mining university project focused on extracting product characteristics from user reviews (specifically cell phones) and determining overall sentiment for each characteristic.

## Project Overview

The system processes Amazon reviews to identify what users like and dislike about specific mobile phones. It moves from raw text to structured "aspect-based" sentiment analysis.

### The Pipeline
1.  **Normalization**: Normalizes user-inputted phone names (e.g., "s24 ultra") into structured JSON using an LLM.
2.  **Filtering**: Heuristic-based pre-filtering to remove low-quality reviews (short, off-topic, or questions).
3.  **Extraction**: Parallel feature extraction using `langextract` to identify (feature, sentiment) pairs.
4.  **Embeddings**: Converting extracted features into vector embeddings via `sentence-transformers`.
5.  **Clustering**: Semantic grouping of similar expressions (e.g., "fast charging" and "quick to charge" → "battery life").
6.  **Labeling**: LLM-assigned descriptive labels for each cluster.
7.  **Aggregation**: Final counting of positive vs. negative mentions for each aspect.
8.  **API/Caching**: Fast results for repeat queries via a local caching system.

## Project Structure

```
phone-reviews/
├── data/               # Raw datasets and analysis cache
├── src/
│   ├── data/           # Dataset loading and filtering
│   ├── extraction/     # Phone normalization and feature extraction
│   ├── analysis/       # Embeddings, clustering, and labeling
│   ├── cache/          # Cache management
│   └── api/            # FastAPI routes
├── main.py             # Entry point
├── requirements.txt    # Project dependencies
└── .env                # API keys (Gemini / OpenAI)
```

## Tech Stack

-   **Data Source**: [Amazon-Reviews-Unlocked-Mobile-Phones](https://www.kaggle.com/datasets/PromptCloudHQ/amazon-reviews-unlocked-mobile-phones?select=Amazon_Unlocked_Mobile.csv)
-   **Extraction**: `langextract`
-   **Embeddings**: `sentence-transformers`
-   **Clustering**: `scikit-learn`
-   **API**: `FastAPI` + `uvicorn`
-   **LLM**: Gemini or GPT-4o mini (via `google-generativeai` or `openai`)

## Setup & Installation

1.  **Virtual Environment**:
    ```bash
    python -m venv venv
    .\venv\Scripts\Activate
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Environment Variables**:
    Create a `.env` file based on `.env.template` and add your API keys.

## Usage

To start the API:
```bash
python main.py
```
*(Currently in setup phase; core scripts coming soon.)*