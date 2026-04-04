import sqlite3
import pandas as pd
import os


def truncate_review(text: str, max_words: int = 500) -> str:
    """Truncate a review to a maximum number of words."""
    if not isinstance(text, str):
        return ""
    words = text.split()
    return ' '.join(words[:max_words])


def get_top_reviews(brand: str, model: str, top_n: int = 50) -> pd.DataFrame:
    """
    Search database for reviews for a specific brand and model.
    Returns the top n reviews as a pandas DataFrame, sorted by 'Review Votes' (helpful votes).
    Each review is truncated to 500 words.

    Args:
        brand (str): The phone brand.
        model (str): The phone model.
        top_n (int): Number of reviews to return (default 50).

    Returns:
        pd.DataFrame: A DataFrame containing the matching reviews.
    """
    db_path = os.path.join("data", "reviews.db")

    if not os.path.exists(db_path):
        print(f"Error: Database {db_path} not found.")
        return pd.DataFrame()

    try:
        conn = sqlite3.connect(db_path)

        query = """
        SELECT * FROM reviews 
        WHERE "Brand Name" = ? AND model = ? 
        ORDER BY "Review Votes" DESC 
        LIMIT ?
        """

        df = pd.read_sql_query(query, conn, params=(brand, model, top_n))
        conn.close()

        # Truncate each review to 500 words
        if not df.empty and 'Reviews' in df.columns:
            df['Reviews'] = df['Reviews'].apply(truncate_review)

        return df

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return pd.DataFrame()


def get_all_brands() -> list[str]:
    """Return a sorted list of all distinct brands in the database."""
    db_path = os.path.join("data", "reviews.db")
    if not os.path.exists(db_path):
        return []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT "Brand Name" FROM reviews WHERE "Brand Name" IS NOT NULL ORDER BY "Brand Name"')
        brands = [row[0] for row in cursor.fetchall()]
        conn.close()
        return brands
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []


def get_models_for_brand(brand: str) -> list[str]:
    """Return a sorted list of all distinct models for a given brand."""
    db_path = os.path.join("data", "reviews.db")
    if not os.path.exists(db_path):
        return []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT DISTINCT model FROM reviews WHERE "Brand Name" = ? AND model IS NOT NULL ORDER BY model',
            (brand,)
        )
        models = [row[0] for row in cursor.fetchall()]
        conn.close()
        return models
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
