import json
import os

SCORE_FILE = "score.json"

def load_scores():
    if not os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "w") as f:
            json.dump({}, f)
    with open(SCORE_FILE, "r") as f:
        return json.load(f)

def save_scores(scores):
    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f, indent=4)

def update_score(user_id, username):
    scores = load_scores()
    if str(user_id) not in scores:
        scores[str(user_id)] = {"username": username, "score": 0}
    scores[str(user_id)]["score"] += 1
    scores[str(user_id)]["username"] = username  # update username if changed
    save_scores(scores)

def get_user_score(user_id):
    scores = load_scores()
    return scores.get(str(user_id), {"score": 0})["score"]

def get_leaderboard(top_n=5):
    scores = load_scores()
    sorted_users = sorted(scores.items(), key=lambda item: item[1]["score"], reverse=True)
    return sorted_users[:top_n]
