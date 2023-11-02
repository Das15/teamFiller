import datetime

import objects.beatmap as beatmap


class Class(object):
    """Used for representing mappool data in bracket."""
    def __key(self):
        return self.Name, self.Description, self.BestOf, self.Beatmaps, self.StartDate, self.Matches

    def __eq__(self, obj):
        return self.__key() == obj.__key()

    def __hash__(self):
        return hash(self.__key())

    # noinspection PyPep8Naming
    def __init__(self, Name, Description: str = None, BestOf: int = 9, Beatmaps: list[dict] = None,
                 StartDate: str = datetime.datetime.now(), Matches=None):
        if Matches is None:
            Matches = []
        if Beatmaps is None:
            Beatmaps = []
        self.Name = Name
        self.Description = Description
        self.BestOf = BestOf
        temp = []
        for Beatmap in Beatmaps:
            temp.append(beatmap.Class(**Beatmap))
        self.Beatmaps = temp
        self.StartDate = StartDate
        self.Matches = Matches
