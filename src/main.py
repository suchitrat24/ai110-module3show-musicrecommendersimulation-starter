"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print the top k songs for a profile with scores and reasons."""
    print(f"\n=== {label} ===")
    print("Profile: " + ", ".join(f"{key}={value}" for key, value in user_prefs.items()))
    print("-" * 50)
    for rank, (song, score, explanation) in enumerate(recommend_songs(user_prefs, songs, k), start=1):
        print(f"{rank}. {song['title']} by {song['artist']}  (Score: {score:.2f})")
        print(f"   Because: {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Default profile
    pop_happy = {"genre": "pop", "mood": "happy", "energy": 0.8}

    # Taste profile: chill study music
    chill_study = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.4,
        "likes_acoustic": True,
    }

    print_recommendations("Pop / Happy", pop_happy, songs)
    print_recommendations("Chill Study", chill_study, songs)


if __name__ == "__main__":
    main()
