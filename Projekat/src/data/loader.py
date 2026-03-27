import pandas as pd
import os
from src.data.filter import should_keep_review, clean_text

def run_offline_preprocessing(input_path: str, output_path: str):
    """
    Loads raw CSV, cleans text, applies heuristic filters, and saves cleaned data.
    """
    print(f"Loading raw data from {input_path}...")
    # Read CSV
    df = pd.read_csv(input_path)
    initial_count = len(df)
    
    # Drop rows with missing reviews
    df = df.dropna(subset=['Reviews'])
    
    print("Normalizing text and filtering...")
    # Pre-clean the text column
    df['Reviews'] = df['Reviews'].apply(clean_text)
    
    # Filter by heuristics
    mask = df['Reviews'].apply(should_keep_review)
    df_cleaned = df[mask].copy()
    
    final_count = len(df_cleaned)
    removed_count = initial_count - final_count
    
    print(f"Processed complete.")
    print(f"- Initial reviews: {initial_count}")
    print(f"- Cleaned reviews: {final_count}")
    print(f"- Removed: {removed_count} ({100*removed_count/initial_count:.1f}%)")
    
    # Save cleaned dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_cleaned.to_csv(output_path, index=False)
    print(f"Cleaned dataset saved to: {output_path}")
