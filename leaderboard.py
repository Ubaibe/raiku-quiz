# leaderboard.py
import json
import os

class Leaderboard:
    def __init__(self, filename="leaderboard.json"):
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        """Load scores from JSON file, return empty dict if file doesn't exist."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error reading {self.filename}. Starting with empty leaderboard.")
                return {}
        return {}

    def save_scores(self):
        """Save scores to JSON file."""
        try:
            with open(self.filename, "w") as f:
                json.dump(self.scores, f, indent=4)
        except IOError as e:
            print(f"Error saving leaderboard: {e}")

    def update_score(self, username: str, score: int):
        """Update user's highest score and cumulative score."""
        if not username:
            username = "Anonymous"
        if username in self.scores:
            # Update high score if new score is higher
            self.scores[username]["high_score"] = max(self.scores[username]["high_score"], score)
            # Add to cumulative score
            self.scores[username]["cumulative_score"] += score
        else:
            # Initialize new user with high and cumulative scores
            self.scores[username] = {"high_score": score, "cumulative_score": score}
        self.save_scores()

    def get_sorted_scores(self):
        """Return scores sorted by highest score first."""
        return sorted(
            self.scores.items(),
            key=lambda x: x[1]["high_score"],
            reverse=True
        )