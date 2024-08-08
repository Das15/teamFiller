from dataclasses import dataclass


@dataclass
class Class:
    """Simple dataclass used for parsing."""
    OnlineID: int
    DifficultyName: str
    BPM: float
    Length: float
    StarRating: float
    TotalObjectCount: int
    Metadata: {}
    Difficulty: {}
    Covers: {}
    EndTimeObjectCount: int = 0

    def __iter__(self):
        yield "OnlineID", self.OnlineID
        yield "DifficultyName", self.DifficultyName
        yield "BPM", self.BPM
        yield "Length", self.Length
        yield "StarRating", self.StarRating
        yield "EndTimeObjectCount", self.EndTimeObjectCount
        yield "TotalObjectCount", self.TotalObjectCount
        yield "Metadata", self.Metadata
        yield "Difficulty", self.Difficulty
        yield "Covers", self.Covers
