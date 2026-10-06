import random

MISS, HIT, SUNK, REPEAT = "miss", "hit", "sunk", "repeat"

FLEET = [("Cruiser", 3), ("Destroyer", 2), ("Patrol Boat", 2)]


class Ship:
    def __init__(self, name, cells):
        self.name = name
        self.cells = frozenset(cells)
        self.hits = set()

    def take_hit(self, pos):
        self.hits.add(pos)

    def is_sunk(self):
        return self.hits >= self.cells


class Board:
    """Cells are always 0-based (row, col) tuples of ints."""
    SIZE = 6

    def __init__(self):
        self.ships = []
        self.shots = set()

    @staticmethod
    def cell(pos):
        r, c = pos
        return (int(r), int(c))

    @classmethod
    def in_bounds(cls, pos):
        r, c = pos
        return 0 <= r < cls.SIZE and 0 <= c < cls.SIZE

    def occupied(self):
        return {p for ship in self.ships for p in ship.cells}

    def ship_at(self, pos):
        for ship in self.ships:
            if pos in ship.cells:
                return ship
        return None

    def place_ship(self, name, cells):
        cells = {self.cell(p) for p in cells}
        if not cells or not all(self.in_bounds(p) for p in cells):
            raise ValueError(f"{name} does not fit on the board")
        if cells & self.occupied():
            raise ValueError(f"{name} overlaps another ship")
        ship = Ship(name, cells)
        self.ships.append(ship)
        return ship

    def place_fleet_randomly(self, fleet=FLEET, rng=random):
        for name, length in fleet:
            while True:
                horizontal = rng.random() < 0.5
                r = rng.randrange(self.SIZE - (0 if horizontal else length - 1))
                c = rng.randrange(self.SIZE - (length - 1 if horizontal else 0))
                cells = {(r, c + i) if horizontal else (r + i, c) for i in range(length)}
                if not cells & self.occupied():
                    self.place_ship(name, cells)
                    break

    def fire(self, pos):
        """Resolve a shot. Returns (outcome, ship); ship is None on a miss or repeat."""
        pos = self.cell(pos)
        if pos in self.shots:
            return REPEAT, None
        self.shots.add(pos)
        ship = self.ship_at(pos)
        if ship is None:
            return MISS, None
        ship.take_hit(pos)
        return (SUNK if ship.is_sunk() else HIT), ship

    def ships_afloat(self):
        return [ship for ship in self.ships if not ship.is_sunk()]

    def all_sunk(self):
        return not self.ships_afloat()

    def render(self, reveal_ships):
        rows = ["  " + " ".join(str(c + 1) for c in range(self.SIZE))]
        for r in range(self.SIZE):
            line = []
            for c in range(self.SIZE):
                pos = (r, c)
                if pos in self.shots:
                    line.append("X" if self.ship_at(pos) else "o")
                elif reveal_ships and self.ship_at(pos):
                    line.append("S")
                else:
                    line.append(".")
            rows.append(f"{r + 1} " + " ".join(line))
        return "\n".join(rows)
