class Player:
    def __init__(self, id: int):
        self.id = id
        self.current_score = 0
        self.turns_taken = 0

    def reset_score(self):
        """Resets the player's current score and turns taken."""
        self.current_score = 0
        self.turns_taken = 0
