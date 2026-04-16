"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# User Profiles
# ---------------------------------------------------------------------------

HIGH_ENERGY_POP = {
    "preferred_genre":        "pop",
    "preferred_mood":         "happy",
    "preferred_energy":       0.90,
    "preferred_tempo":        130,
    "preferred_valence":      0.85,
    "preferred_danceability": 0.88,
    "preferred_acousticness": 0.10,
}

CHILL_LOFI = {
    "preferred_genre":        "lofi",
    "preferred_mood":         "chill",
    "preferred_energy":       0.35,
    "preferred_tempo":        75,
    "preferred_valence":      0.58,
    "preferred_danceability": 0.55,
    "preferred_acousticness": 0.80,
}

DEEP_INTENSE_ROCK = {
    "preferred_genre":        "rock",
    "preferred_mood":         "intense",
    "preferred_energy":       0.92,
    "preferred_tempo":        150,
    "preferred_valence":      0.35,
    "preferred_danceability": 0.60,
    "preferred_acousticness": 0.08,
}

# ---------------------------------------------------------------------------
# Adversarial / Edge-Case Profiles
# ---------------------------------------------------------------------------

# Conflicting: extremely high energy but deeply sad/melancholic mood
CONFLICTED_ENERGY = {
    "preferred_genre":        "ambient",
    "preferred_mood":         "melancholic",
    "preferred_energy":       0.95,
    "preferred_tempo":        170,
    "preferred_valence":      0.05,
    "preferred_danceability": 0.90,
    "preferred_acousticness": 0.05,
}

# Extreme low: all numerical features near 0 — the "emptiness" profile
ALL_LOW = {
    "preferred_genre":        "classical",
    "preferred_mood":         "dark",
    "preferred_energy":       0.05,
    "preferred_tempo":        62,
    "preferred_valence":      0.05,
    "preferred_danceability": 0.05,
    "preferred_acousticness": 0.05,
}

# Rare combo: k-pop genre with aggressive mood (genre exists in catalog, mood mismatch likely)
KPOP_AGGRESSIVE = {
    "preferred_genre":        "k-pop",
    "preferred_mood":         "aggressive",
    "preferred_energy":       0.88,
    "preferred_tempo":        145,
    "preferred_valence":      0.60,
    "preferred_danceability": 0.85,
    "preferred_acousticness": 0.12,
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

PROFILES = [
    ("High-Energy Pop",       HIGH_ENERGY_POP),
    ("Chill Lofi",            CHILL_LOFI),
    ("Deep Intense Rock",     DEEP_INTENSE_ROCK),
    ("Conflicted Energy",     CONFLICTED_ENERGY),
    ("All-Low / Dark",        ALL_LOW),
    ("K-Pop Aggressive",      KPOP_AGGRESSIVE),
]


def print_recommendations(label: str, recommendations: list) -> None:
    """Prints a formatted block of recommendations for a single user profile."""
    print(f"\n{'=' * 50}")
    print(f"  {label} Recommendations")
    print(f"{'=' * 50}")

    for rec in recommendations:
        song    = rec["song"]
        score   = rec["score"]
        reasons = rec["reasons"]

        print(f"\n🎵 Song:  {song['title']} - {song['artist']}")
        print(f"⭐ Score: {score:.2f}")
        print("   Reasons:")
        for reason in reasons:
            print(f"     • {reason}")

    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    songs = load_songs("data/songs.csv")

    for label, prefs in PROFILES:
        results = recommend_songs(prefs, songs, k=5)
        print_recommendations(label, results)


if __name__ == "__main__":
    main()
