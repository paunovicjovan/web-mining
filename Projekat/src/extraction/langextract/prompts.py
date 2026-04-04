import textwrap

EXTRACTION_PROMPT = textwrap.dedent("""\
    Extract phone-specific aspects and their sentiment from the review.
    - Normalize aspects: Use concise canonical noun phrases (1-3 words max, e.g., 'battery life', 'price').
    - Focus: Only extract features or characteristics of the phone; ignore other brands or unrelated mentions.
    - Consistency: Merge synonyms and avoid copying long sentences.
    - Alignment: Sentiment must be 'positive', 'negative', or 'neutral' based on the text.
    Only extract aspects actually mentioned in the input.""")
