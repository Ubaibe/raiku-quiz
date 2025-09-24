# username.py
class Username:
    def __init__(self):
        self.username = None

    def set_username(self, name: str):
        """Save username once collected"""
        if name.strip():
            self.username = name.strip()
            return True
        return False

    def get_username(self):
        return self.username
