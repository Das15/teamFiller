import objects.beatmap as beatmap
import datetime


class Class(object):
    def __key(self):
        return self.Name, self.Description, self.BestOf, self.Beatmaps, self.StartDate, self.Matches

    def __eq__(self, obj):
        return self.__key() == obj.__key()

    def __hash__(self):
        return hash(self.__key())

    def __init__(self, Name, Description=None, BestOf=9, Beatmaps=None, StartDate=datetime.datetime.now(),
                 Matches=None):
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
