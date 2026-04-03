import sqlite3
import pandas as pd
import os

def get_top_reviews(brand: str, model: str, top_n: int = 5) -> pd.DataFrame:
    """
    Search database for reviews for a specific brand and model.
    Returns the top n reviews as a pandas DataFrame, sorted by 'Review Votes' (helpful votes).
    
    Args:
        brand (str): The phone brand.
        model (str): The phone model.
        top_n (int): Number of reviews to return.
        
    Returns:
        pd.DataFrame: A DataFrame containing the matching reviews.
    """
    # Database path relative to project root
    db_path = os.path.join("data", "reviews.db")

    if not os.path.exists(db_path):
        print(f"Error: Database {db_path} not found.")
        return pd.DataFrame()

    try:
        conn = sqlite3.connect(db_path)
        
        # SQL query using exact column names from the database
        query = """
        SELECT * FROM reviews 
        WHERE \"Brand Name\" = ? AND model = ? 
        ORDER BY \"Review Votes\" DESC 
        LIMIT ?
        """
        
        # Execute query and load into DataFrame
        df = pd.read_sql_query(query, conn, params=(brand, model, top_n))
        
        conn.close()
        return df
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return pd.DataFrame()
