from dataclasses import dataclass


@dataclass
class Position(object):
    X: int
    Y: int

    def list(self):
        return [self.X, self.Y]
