from typing import List, Dict, Tuple
from dataclasses import dataclass
import csv


@dataclass
class Song:
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
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def load_songs(csv_path: str) -> List[Dict]:
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    score = 0.0
    reasons = []

    # Genre match: +2.0 points (strongest signal)
    if song.get("genre") == user_prefs.get("genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match: +1.0 point
    if song.get("mood") == user_prefs.get("mood"):
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy similarity: up to 1.5 points (closer = more points)
    target_energy = user_prefs.get("energy", 0.5)
    song_energy = song.get("energy", 0.5)
    energy_score = round((1.0 - abs(target_energy - song_energy)) * 1.5, 2)
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score})")

    return round(score, 2), ", ".join(reasons)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    scored = []
    for song in songs:
        score, explanation = score_song(user_prefs, song)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]


class Recommender:

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        score = 0.0
        reasons = []

        if song.genre == user.favorite_genre:
            score += 2.0
            reasons.append("genre match (+2.0)")

        if song.mood == user.favorite_mood:
            score += 1.0
            reasons.append("mood match (+1.0)")

        energy_score = round((1.0 - abs(user.target_energy - song.energy)) * 1.5, 2)
        score += energy_score
        reasons.append(f"energy similarity (+{energy_score})")

        if user.likes_acoustic and song.acousticness > 0.7:
            score += 0.5
            reasons.append("acoustic preference match (+0.5)")

        return round(score, 2), reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [(song, self._score(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = self._score(user, song)
        return ", ".join(reasons) if reasons else "No strong match found"
