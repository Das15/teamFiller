from dataclasses import dataclass


@dataclass
class Class:
    OnlineID: int
    DifficultyName: str
    BPM: float
    Length: float
    StarRating: int
    Metadata: []
    Difficulty: []
    Covers: []
