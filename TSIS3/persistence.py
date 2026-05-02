import json
import os

LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE = "settings.json"

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return []

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f, indent=2)

def add_score(name, score, distance):
    lb = load_leaderboard()
    lb.append({"name": name, "score": score, "distance": distance})
    lb.sort(key=lambda x: x["score"], reverse=True)
    save_leaderboard(lb[:10])

def load_settings():
    default = {"sound": True, "car_color": "red", "difficulty": "normal"}
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return default

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)