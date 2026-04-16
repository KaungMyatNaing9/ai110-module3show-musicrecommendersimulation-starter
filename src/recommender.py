import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        def score(song: Song) -> float:
            s = 0.0
            if song.genre == user.favorite_genre:
                s += 2.0
            if song.mood == user.favorite_mood:
                s += 1.0
            s += 1 - abs(song.energy - user.target_energy)
            # likes_acoustic maps True → prefers 1.0, False → prefers 0.0
            acoustic_pref = 1.0 if user.likes_acoustic else 0.0
            s += 1 - abs(song.acousticness - acoustic_pref)
            return s

        return sorted(self.songs, key=score, reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"genre matches '{user.favorite_genre}'")
        if song.mood == user.favorite_mood:
            reasons.append(f"mood matches '{user.favorite_mood}'")
        energy_sim = round(1 - abs(song.energy - user.target_energy), 2)
        reasons.append(f"energy similarity {energy_sim}")
        return ", ".join(reasons) if reasons else "low overall match"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Reads songs from a CSV file and returns them as a list of dictionaries
    with all numerical fields converted to their appropriate types.

    Args:
        csv_path: Path to the CSV file (e.g. "data/songs.csv").

    Returns:
        A list of song dicts with keys:
        id (int), title, artist, genre, mood (str),
        energy, tempo_bpm, valence, danceability, acousticness (float).
        Returns an empty list if the file is not found.
    """
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            songs = []
            for row in reader:
                songs.append({
                    "id":            int(row["id"]),
                    "title":         row["title"],
                    "artist":        row["artist"],
                    "genre":         row["genre"],
                    "mood":          row["mood"],
                    "energy":        float(row["energy"]),
                    "tempo_bpm":     float(row["tempo_bpm"]),
                    "valence":       float(row["valence"]),
                    "danceability":  float(row["danceability"]),
                    "acousticness":  float(row["acousticness"]),
                })
            print(f"Loaded songs: {len(songs)}")
            return songs
    except FileNotFoundError:
        print(f"Error: songs file not found at '{csv_path}'")
        return []

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using content-based filtering.
    Returns a (score, reasons) tuple where reasons explain each contribution.

    Scoring breakdown (max possible ≈ 9.0 before normalization):
        +2.0  genre match (categorical, binary)
        +1.0  mood match  (categorical, binary)
        +1.0  energy similarity     (distance-based, 0–1)
        +1.0  valence similarity    (distance-based, 0–1)
        +1.0  danceability similarity (distance-based, 0–1)
        +1.0  acousticness similarity (distance-based, 0–1)
        +1.0  tempo similarity      (normalized over 200 BPM range, clamped 0–1)

    Args:
        user_prefs: Dict with keys preferred_genre, preferred_mood,
                    preferred_energy, preferred_tempo, preferred_valence,
                    preferred_danceability, preferred_acousticness.
        song:       A song dict as returned by load_songs().

    Returns:
        (score, reasons) — score is a float, reasons is a list of strings
        describing each feature's contribution.
    """
    score = 0.0
    reasons = []

    # Categorical features: full points for exact match, zero otherwise
    if song["genre"] == user_prefs["preferred_genre"]:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"] == user_prefs["preferred_mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Numerical features: similarity = 1 - |song_value - user_value|
    # Ranges are 0–1, so the difference is already normalized
    for feature in ("energy", "valence", "danceability", "acousticness"):
        similarity = 1 - abs(song[feature] - user_prefs[f"preferred_{feature}"])
        score += similarity
        reasons.append(f"{feature} similarity (+{similarity:.2f})")

    # Tempo uses a 200 BPM normalization window; clamped so it never goes negative
    tempo_similarity = 1 - abs(song["tempo_bpm"] - user_prefs["preferred_tempo"]) / 200
    tempo_similarity = max(0.0, min(1.0, tempo_similarity))
    score += tempo_similarity
    reasons.append(f"tempo similarity (+{tempo_similarity:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Dict]:
    """
    Scores every song against user preferences, then returns the top k results
    sorted by score in descending order.

    Args:
        user_prefs: User preference dict (see score_song for required keys).
        songs:      Full song catalog as returned by load_songs().
        k:          Number of top recommendations to return (default 5).

    Returns:
        A list of up to k dicts, each with keys:
            "song"    — the original song dict
            "score"   — the float compatibility score
            "reasons" — list of strings explaining the score breakdown
        Sorted from highest score to lowest.
    """
    # Score every song; the inner list comprehension unpacks the (score, reasons) tuple
    scored = [
        {"song": song, "score": score, "reasons": reasons}
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    # sorted() returns a new list, leaving the original catalog unchanged
    ranked = sorted(scored, key=lambda x: x["score"], reverse=True)

    return ranked[:k]
