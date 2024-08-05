from dataclasses import dataclass


@dataclass()
class Class(object):
    ShortName: str
    OnlineID: int
    Name: str
    InstantiationInfo: str
    LastAppliedDifficultyVersion: int = None
    Available: bool = True
