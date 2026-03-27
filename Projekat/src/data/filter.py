import re

def is_too_short(text: str, min_words: int = 8) -> bool:
    """Check if the review is too short to be useful for feature extraction."""
    if not isinstance(text, str):
        return True
    return len(text.split()) < min_words

def is_question(text: str) -> bool:
    """Check if the review text is a question, which is typically not useful for feedback."""
    if not isinstance(text, str):
        return False
    
    text = text.strip()
    # Ends with a question mark
    if text.endswith('?'):
        return True
    
    # Starts with a common question word
    question_words = ('how', 'why', 'can', 'does', 'is', 'what', 'will', 'where', 'when', 'who')
    if text.lower().startswith(question_words):
        return True
        
    return False

def clean_text(text: str) -> str:
    """Basic text cleanup."""
    if not isinstance(text, str):
        return ""
    # Remove multiple spaces/newlines
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def should_keep_review(text: str) -> bool:
    """Combine heuristics to determine if a review should be kept for analysis."""
    if not text or not isinstance(text, str):
        return False
    
    if is_too_short(text):
        return False
    
    if is_question(text):
        return False
    
    return True
