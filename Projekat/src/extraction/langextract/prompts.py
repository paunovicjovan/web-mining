import textwrap

EXTRACTION_PROMPT = textwrap.dedent("""\
    Extract aspects (features) and their associated sentiment from the phone review.
    For each extraction, provide:
    - aspect: Name of the feature or characteristic mentioned (e.g., 'battery life', 'camera quality', 'screen brightness', 'price').
    - sentiment: The sentiment expressed toward that aspect (e.g., 'positive', 'negative', 'neutral').
    Return null values if you cannot confidently identify aspects or sentiment.
    Only extract aspects that are actually present in the text.""")
