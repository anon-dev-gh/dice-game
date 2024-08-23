import random


class Player:
    def __init__(self, player_id: int, name: str):
        self.player_id = player_id
        self.name = name
        self.current_score = 0
        self.turns_taken = 0

    def roll_dice(self) -> int:
        """Simulates rolling two six-sided dice."""
        roll1 = random.randint(1, 6)
        roll2 = random.randint(1, 6)
        self.current_score += roll1 + roll2
        self.turns_taken += 1
        return roll1 + roll2

    def reset_score(self):
        """Resets the player's current score and turns taken."""
        self.current_score = 0
        self.turns_taken = 0
