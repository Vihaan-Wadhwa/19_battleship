class Board:
    """Cells are always 0-based (row, col) tuples of ints."""
    SIZE = 6

    def __init__(self):
        self.ships = set()
        self.shots = set()

    @staticmethod
    def cell(pos):
        r, c = pos
        return (int(r), int(c))

    def place_ship(self, cells):
        self.ships.update(self.cell(p) for p in cells)

    def fire(self, pos):
        pos = self.cell(pos)
        self.shots.add(pos)
        return pos in self.ships

    def all_sunk(self):
        return self.ships <= self.shots
