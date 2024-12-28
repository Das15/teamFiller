from dataclasses import dataclass


@dataclass()
class Class(object):
    ShortName: str
    Name: str
    InstantiationInfo: str
    OnlineID: int = 0
    LastAppliedDifficultyVersion: int = None
    Available: bool = True
