from dataclasses import dataclass


@dataclass
class Class:
    OnlineID: int
    DifficultyName: str
    BPM: float
    Length: float
    StarRating: int
    Metadata: {}
    Difficulty: {}
    Covers: {}

    def __iter__(self):
        yield "OnlineID", self.OnlineID
        yield "DifficultyName", self.DifficultyName
        yield "BPM", self.BPM
        yield "Length", self.Length
        yield "StarRating", self.StarRating
        yield "Metadata", self.Metadata
        yield "Difficulty", self.Difficulty
        yield "Covers", self.Covers
