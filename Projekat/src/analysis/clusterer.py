from sklearn.cluster import AgglomerativeClustering
from collections import Counter
import numpy as np
import nltk
from nltk.corpus import stopwords as nltk_stopwords
from src.analysis.embedder import Embedder

# Download NLTK stopwords on first use (no-op if already downloaded)
nltk.download('stopwords', quiet=True)
_STOPWORDS = set(nltk_stopwords.words('english'))

class Clusterer:
    """
    Groups semantically similar aspects into unified features through clustering.
    """
    def __init__(self, embedder: Embedder = None):
        if embedder is None:
            self.embedder = Embedder()
        else:
            self.embedder = embedder

    def _find_dominant_word(self, mentions: list[str], min_coverage: float = 0.5) -> str | None:
        """
        If a single non-stopword appears in >= min_coverage of all mentions,
        return it as the cluster name. Otherwise return None.
        """
        total = len(mentions)
        # Tokenize all mentions, flatten words, count how many *mentions* each word appears in
        word_mention_count = Counter()
        for mention in mentions:
            words_in_mention = set(mention.lower().split())
            for word in words_in_mention:
                if word not in _STOPWORDS and len(word) > 2:
                    word_mention_count[word] += 1

        if not word_mention_count:
            return None

        best_word, best_count = word_mention_count.most_common(1)[0]
        if best_count / total >= min_coverage:
            return best_word
        return None

    def _pick_representative_name(self, mentions: list[str], embeddings_map: dict) -> str:
        """
        Strategy:
        1. If a single word dominates >=50% of all mentions → use that word.
        2. Otherwise prefer the most frequent full phrase.
        3. Tie-break using cosine similarity to cluster centroid.
        """
        # Strategy 1: dominant shared word
        dominant = self._find_dominant_word(mentions)
        if dominant:
            return dominant

        # Strategy 2: most frequent phrase
        counts = Counter(mentions)
        most_common_count = counts.most_common(1)[0][1]
        most_common_aspects = [a for a, c in counts.items() if c == most_common_count]

        if len(most_common_aspects) == 1:
            return most_common_aspects[0]

        # Strategy 3: centroid-based tie-break
        candidate_embeddings = np.array([embeddings_map[a] for a in most_common_aspects])
        centroid = np.mean(candidate_embeddings, axis=0)

        best_name = most_common_aspects[0]
        best_similarity = -1.0
        for aspect, emb in zip(most_common_aspects, candidate_embeddings):
            sim = np.dot(emb, centroid) / (np.linalg.norm(emb) * np.linalg.norm(centroid) + 1e-8)
            if sim > best_similarity:
                best_similarity = sim
                best_name = aspect

        return best_name

    def cluster_aspects(self, aspect_sentiment_pairs: list[tuple[str, str]], threshold: float = 0.5) -> list[dict]:
        """
        Takes raw extraction pairs and returns a list of consolidated "Aspect Objects".
        """
        if not aspect_sentiment_pairs:
            return []

        # 1. Prepare data
        aspects = [pair[0] for pair in aspect_sentiment_pairs]

        # 2. Get embeddings
        embeddings = self.embedder.get_embeddings(aspects)

        # Build map of unique aspect -> embedding for centroid lookups
        unique_aspects = list(set(aspects))
        unique_embeddings = self.embedder.get_embeddings(unique_aspects)
        embeddings_map = {a: e for a, e in zip(unique_aspects, unique_embeddings)}

        # 3. Perform Clustering using Agglomerative Clustering with cosine distance
        clustering = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=threshold,
            metric='cosine',
            linkage='average'
        )
        labels = clustering.fit_predict(embeddings)

        # 4. Group results by cluster label
        clusters = {}
        for idx, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = {'mentions': [], 'sentiments': []}
            clusters[label]['mentions'].append(aspects[idx])
            clusters[label]['sentiments'].append(aspect_sentiment_pairs[idx][1])

        # 5. Process and normalize clusters
        final_clusters = []
        for label, data in clusters.items():
            # Discard single-mention clusters (outliers)
            if len(data['mentions']) <= 1:
                continue

            representative_name = self._pick_representative_name(data['mentions'], embeddings_map)
            sentiment_counts = Counter(data['sentiments'])

            final_clusters.append({
                'representative_name': representative_name,
                'total_mentions': len(data['mentions']),
                'sentiment_summary': dict(sentiment_counts),
                'original_mentions': list(set(data['mentions']))
            })

        # 6. Sort by popularity
        final_clusters.sort(key=lambda x: x['total_mentions'], reverse=True)

        return final_clusters
