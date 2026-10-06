from board import Board, MISS, HIT, SUNK, REPEAT
from ai import AI


def to_label(pos):
    """Format a 0-based (row, col) cell as the 1-based text players type."""
    return f"{pos[0] + 1},{pos[1] + 1}"


def describe(outcome, ship):
    if outcome == SUNK:
        return f"HIT! Sunk the {ship.name}!"
    if outcome == HIT:
        return "HIT!"
    if outcome == MISS:
        return "MISS!"
    raise ValueError(f"no feedback for outcome {outcome!r}")


class Battleship:
    def __init__(self):
        self.player = Board()
        self.enemy = Board()
        self.ai = AI(Board.SIZE)
        self._setup()

    def _setup(self):
        self.player.place_fleet_randomly()
        self.enemy.place_fleet_randomly()

    def show(self):
        print("\nEnemy waters:")
        print(self.enemy.render(reveal_ships=False))
        print("\nYour fleet:")
        print(self.player.render(reveal_ships=True))
        print(f"Enemy ships afloat: {len(self.enemy.ships_afloat())}/{len(self.enemy.ships)}"
              f"   Your ships afloat: {len(self.player.ships_afloat())}/{len(self.player.ships)}")
        print("Enter a shot as row,col (e.g. 2,3) or q to quit.")

    def _shoot(self, board, pos, prefix=""):
        """Fire one real shot and print its hit/miss/sunk feedback exactly once.

        This is the only place shots are resolved and reported. A repeated
        shot is not a real shot, so it gets no hit/miss feedback.
        """
        outcome, ship = board.fire(pos)
        if outcome != REPEAT:
            print(prefix + describe(outcome, ship))
        return outcome, ship

    def run(self):
        print("Battleship")
        while True:
            self.show()
            try:
                raw = input("> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                raw = "q"
            if raw == "q":
                return
            try:
                r, c = map(int, raw.split(","))
                pos = (r - 1, c - 1)
            except ValueError:
                print("Use row,col.")
                continue
            if not Board.in_bounds(pos):
                print("Outside board.")
                continue
            outcome, _ = self._shoot(self.enemy, pos)
            if outcome == REPEAT:
                print("Already fired there.")
                continue
            if self.enemy.all_sunk():
                print("You sank the whole enemy fleet. You win!")
                return

            ai_pos = self.ai.choose()
            if ai_pos is None:
                print("The AI has no cells left to fire at. Game over.")
                return
            outcome, ship = self._shoot(self.player, ai_pos, f"AI fired at {to_label(ai_pos)} - ")
            self.ai.record(ai_pos, outcome, ship)
            if self.player.all_sunk():
                print("The AI sank your whole fleet. You lose.")
                return
