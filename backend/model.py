import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from .data import load_tracks

class ContentRecommender:
    def __init__(self):
        """
        Initialize recommender by loading tracks and pre-scaling features.
        """
        self.df, self.feats = load_tracks()
        self.scaler = StandardScaler()
        X = self.df[self.feats].values
        self.X_scaled = self.scaler.fit_transform(X)

    def recommend_by_title(self, title: str, top_k: int = 10):
        """
        Recommend top_k songs similar to the one matching the title.
        Args:
            title (str): part or full name of a song
            top_k (int): number of recommendations to return
        Returns:
            list[dict]: recommended tracks with similarity scores
        """
        # Match the title (case-insensitive)
        mask = self.df["title"].str.lower().str.contains(title.lower())
        if not mask.any():
            return []

        # Get index of the first matching track
        idx = self.df[mask].index[0]
        v = self.X_scaled[idx:idx + 1]

        # Compute cosine similarity between this and all others
        sims = cosine_similarity(v, self.X_scaled).ravel()

        # Sort by similarity descending, skip the song itself
        order = np.argsort(-sims)
        recs = []
        for j in order:
            if j == idx:
                continue
            item = self.df.iloc[j].to_dict()
            item["score"] = float(sims[j])
            recs.append(item)
            if len(recs) >= top_k:
                break

        return recs


# Test the recommender when run directly
if __name__ == "__main__":
    rec = ContentRecommender()
    results = rec.recommend_by_title("Believer", top_k=5)
    for r in results:
        print(f"{r['title']} by {r['artist']} -> score: {r['score']:.3f}")
