import os
import langextract as lx
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.extraction.langextract.prompts import EXTRACTION_PROMPT
from src.extraction.langextract.examples import EXTRACTION_EXAMPLES
from dotenv import load_dotenv

# Load API key from .env if present
load_dotenv()

def extract_review_aspects(review_text: str, model_id: str = "gemini-2.5-flash") -> list[tuple[str, str]]:
    """
    Extract (aspect, sentiment) pairs from a single review text.
    """
    try:
        result = lx.extract(
            text_or_documents=review_text,
            prompt_description=EXTRACTION_PROMPT,
            examples=EXTRACTION_EXAMPLES,
            model_id=model_id,
        )
        
        pairs = []
        for extraction in result.extractions:
            if extraction.extraction_class == 'aspect':
                sentiment = extraction.attributes.get('sentiment', 'neutral')
                aspect = extraction.extraction_text
                pairs.append((aspect, sentiment))
        
        return pairs
    except Exception as e:
        print(f"Error extracting from review: {e}")
        return []

def extract_aspects_parallel(reviews: list[str], max_workers: int = 20, model_id: str = "gemini-2.5-flash") -> list[tuple[str, str]]:
    """
    Process an array of reviews in parallel and return a combined list of (aspect, sentiment) pairs.
    """
    all_pairs = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all extraction tasks
        future_to_review = {
            executor.submit(extract_review_aspects, review, model_id): review 
            for review in reviews
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_review):
            try:
                pairs = future.result()
                all_pairs.extend(pairs)
            except Exception as e:
                review = future_to_review[future]
                print(f"Extraction failed for review: {review[:50]}... -> {e}")
                
    return all_pairs
