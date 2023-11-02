from dataclasses import dataclass


@dataclass()
class Class(object):
    ShortName: str
    Name: str
    InstantiationInfo: str
    # LastAppliedDifficultyVersion: int
    Available: bool = True
