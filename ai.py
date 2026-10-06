import random

from board import HIT, SUNK

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class AI:
    """Hunt randomly; after a hit, target untried cells next to it.

    All positions are 0-based (row, col) tuples.
    """

    def __init__(self, size=6, rng=random):
        self.size = size
        self.rng = rng
        self.tried = set()
        self.open_hits = set()  # hits on ships not yet sunk

    def _untried(self, pos):
        r, c = pos
        return 0 <= r < self.size and 0 <= c < self.size and pos not in self.tried

    def _targets(self):
        """Untried cells next to open hits, preferring ones that extend a line of hits."""
        in_line, adjacent = set(), set()
        for r, c in self.open_hits:
            for dr, dc in DIRECTIONS:
                nxt = (r + dr, c + dc)
                if not self._untried(nxt):
                    continue
                adjacent.add(nxt)
                if (r - dr, c - dc) in self.open_hits:
                    in_line.add(nxt)
        return in_line or adjacent

    def choose(self):
        """Return the next shot, or None if every cell has been tried."""
        pool = self._targets() or {(r, c) for r in range(self.size)
                                   for c in range(self.size) if (r, c) not in self.tried}
        if not pool:
            return None
        pos = self.rng.choice(sorted(pool))
        self.tried.add(pos)
        return pos

    def record(self, pos, outcome, ship=None):
        """Tell the AI what its shot at pos did."""
        if outcome in (HIT, SUNK):
            self.open_hits.add(pos)
        if outcome == SUNK and ship is not None:
            self.open_hits -= ship.cells
