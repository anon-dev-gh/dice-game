from .game import DiceGame


class GameRunner:
    def __init__(self, game: DiceGame):
        self.game = game

    def run(self):
        # Main game loop
        while not self.game_is_over():
            for player_id in self.game.players.keys():
                self.game.roll_dice(player_id)
                self.game.finish_turn(player_id)
                if self.game_is_over():
                    self.game.end_game()
                    break

    def game_is_over(self) -> bool:
        return False
