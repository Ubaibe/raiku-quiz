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
        def get_user_stats(self, username: str):
        """Get detailed statistics for a specific user."""
        if username in self.scores:
            return self.scores[username]
        return None

    def get_leaderboard_stats(self):
        """Get overall leaderboard statistics."""
        if not self.scores:
            return {
                "total_players": 0,
                "total_games": 0,
                "avg_high_score": 0,
                "max_high_score": 0,
                "total_points": 0
            }

        total_players = len(self.scores)
        total_points = sum(user_data["cumulative_score"] for user_data in self.scores.values())
        high_scores = [user_data["high_score"] for user_data in self.scores.values()]

        return {
            "total_players": total_players,
            "total_games": total_points,
            "avg_high_score": sum(high_scores) / total_players,
            "max_high_score": max(high_scores),
            "total_points": total_points
        }

    def get_user_rank(self, username: str):
        """Get the rank of a specific user (1-based)."""
        scores = self.get_sorted_scores()
        for i, (name, _) in enumerate(scores, 1):
            if name == username:
                return i
        return len(scores) + 1  # If user not found, return rank after last
