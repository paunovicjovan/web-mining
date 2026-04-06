import sqlite3
import os
import json
from dotenv import load_dotenv

load_dotenv()
from datetime import datetime, timedelta

CACHE_DB_PATH = os.getenv("CACHE_DB_PATH", os.path.join("data", "db", "cache.db"))

def get_connection():
    """Get a connection to the cache database."""
    # Ensure data directory exists
    os.makedirs(os.path.dirname(CACHE_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(CACHE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_cache_db():
    """Initialize the cache database schema."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create phones table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS phones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            review_count INTEGER NOT NULL,
            top_n INTEGER NOT NULL,
            last_cached_at TEXT NOT NULL,
            UNIQUE(brand, model, top_n)
        )
    ''')
    
    # Create clusters table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clusters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_id INTEGER NOT NULL,
            representative_name TEXT NOT NULL,
            total_mentions INTEGER NOT NULL,
            positive INTEGER NOT NULL,
            neutral INTEGER NOT NULL,
            negative INTEGER NOT NULL,
            original_mentions TEXT NOT NULL,
            FOREIGN KEY (phone_id) REFERENCES phones (id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

def get_cached_phone(brand: str, model: str, top_n: int, max_age_days: int = 3):
    """
    Retrieve a cached phone entry if it exists and is fresh.
    Returns the phone row as a dictionary or None.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT * FROM phones 
    WHERE brand = ? AND model = ? AND top_n = ?
    """
    cursor.execute(query, (brand, model, top_n))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        last_cached = datetime.fromisoformat(row['last_cached_at'])
        if datetime.now() - last_cached <= timedelta(days=max_age_days):
            return dict(row)
            
    return None

def get_cached_clusters(phone_id: int):
    """Retrieve all clusters for a given phone_id."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM clusters WHERE phone_id = ?", (phone_id,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def save_analysis(brand: str, model: str, top_n: int, review_count: int, clusters: list[dict]):
    """Save analysis results to the cache."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Start transaction
        cursor.execute("BEGIN")
        
        # 1. Clear existing cache for this combo (to ensure clean slate)
        cursor.execute(
            "DELETE FROM phones WHERE brand = ? AND model = ? AND top_n = ?",
            (brand, model, top_n)
        )
        
        # 2. Insert phone metadata
        now_iso = datetime.now().isoformat()
        cursor.execute(
            """
            INSERT INTO phones (brand, model, review_count, top_n, last_cached_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (brand, model, review_count, top_n, now_iso)
        )
        phone_id = cursor.lastrowid
        
        # 3. Insert clusters
        for cluster in clusters:
            # Extract sentiment counts with defaults
            summary = cluster.get('sentiment_summary', {})
            pos = summary.get('positive', 0)
            neu = summary.get('neutral', 0)
            neg = summary.get('negative', 0)
            
            cursor.execute(
                """
                INSERT INTO clusters 
                (phone_id, representative_name, total_mentions, positive, neutral, negative, original_mentions)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    phone_id,
                    cluster['representative_name'],
                    cluster['total_mentions'],
                    pos, neu, neg,
                    json.dumps(cluster['original_mentions'])
                )
            )
            
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error saving to cache: {e}")
        raise
    finally:
        conn.close()
