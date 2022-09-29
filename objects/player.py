from dataclasses import dataclass


@dataclass()
class Class(object):
    id: int
    username: str = None
    country: str = None
    Status: str = None
    Activity: str = None
    cover = None
    cover_url: str = None
    statistics = None
