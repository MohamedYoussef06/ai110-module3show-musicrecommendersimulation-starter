

from src.recommender import load_songs, recommend_songs


# ── User profiles ──────────────────────────────────────────────────────────────

PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.95,
    },
}


def print_recommendations(profile_name: str, recommendations) -> None:
    print(f"\n{'=' * 55}")
    print(f"  Profile: {profile_name}")
    print(f"{'=' * 55}")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  {rank}. {song['title']} by {song['artist']}")
        print(f"     Score : {score:.2f}")
        print(f"     Because: {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile_name, user_prefs in PROFILES.items():
        recs = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(profile_name, recs)


if __name__ == "__main__":
    main()
