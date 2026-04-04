from sentence_transformers import SentenceTransformer
import numpy as np

class Embedder:
    """
    A service for generating semantic embeddings for aspect strings.
    """
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            # Lazy load the model on first use
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def get_embeddings(self, texts: list[str]) -> np.ndarray:
        """
        Convert a list of strings into a matrix of embeddings.
        Contains optimization to only embed unique strings and map them back.
        """
        if not texts:
            return np.array([])
            
        unique_texts = sorted(list(set(texts)))
        unique_embeddings = self.model.encode(unique_texts)
        
        # Create a mapping from text to its embedding
        text_to_embedding = {text: embedding for text, embedding in zip(unique_texts, unique_embeddings)}
        
        # Build the final array in original order
        return np.array([text_to_embedding[text] for text in texts])
