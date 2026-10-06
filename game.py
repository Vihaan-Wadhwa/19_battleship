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
    return "MISS!"


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

    def run(self):
        print("Battleship")
        while True:
            self.show()
            raw = input("> ").strip().lower()
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
            outcome, ship = self.enemy.fire(pos)
            if outcome == REPEAT:
                print("Already fired there.")
                continue
            print(describe(outcome, ship))
            if self.enemy.all_sunk():
                print("You sank the whole enemy fleet. You win!")
                return

            ai_pos = self.ai.choose()
            outcome, ship = self.player.fire(ai_pos)
            print("AI fired at", to_label(ai_pos), "-", describe(outcome, ship))
            if self.player.all_sunk():
                print("The AI sank your whole fleet. You lose.")
                return
