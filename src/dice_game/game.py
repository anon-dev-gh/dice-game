from typing import List

from dice_game.player import Player


class DiceGame:
    def __init__(self, players: List[Player]):
        self.players = players
        self.special_players: List[Player] = []
        self.current_turn = 0
        self.total_turns = 0

    def play_turn(self):
        """Simulates a single turn where each player rolls the dice."""
        for player in self.players:
            score = player.roll_dice()
            print(f"{player.name} rolled a total of {score}")

    def reset_game(self):
        """Resets the game state every two turns."""
        for player in self.players:
            player.reset_score()
        self.current_turn = 0

    def select_special_players(self):
        """Selects at least one-third of players as special players based on their scores."""
        sorted_players = sorted(
            self.players, key=lambda p: p.current_score, reverse=True
        )
        num_special = max(1, len(self.players) // 3)
        self.special_players = sorted_players[:num_special]
