import pandas as pd
from pathlib import Path

# Path to the dataset file relative to this script
DATA_PATH = Path(__file__).parent / "seed_tracks.csv"

def load_tracks():
    """
    Load the seed dataset and ensure numeric columns are valid.
    Returns:
        df (pd.DataFrame): Cleaned track dataframe
        numeric_cols (list): List of numeric feature column names
    """
    df = pd.read_csv(DATA_PATH)

    numeric_cols = [
        "danceability", "energy", "valence", "tempo",
        "acousticness", "instrumentalness", "liveness", "speechiness"
    ]

    # Ensure numeric columns are numeric (convert or drop if needed)
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    df.dropna(subset=numeric_cols, inplace=True)

    return df, numeric_cols

# If run directly, print summary
if __name__ == "__main__":
    df, features = load_tracks()
    print(f"Loaded {len(df)} tracks.")
    print("Feature columns:", features)
    print(df.head())
