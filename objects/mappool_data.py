import logging
import objects.mappool as mappool
import objects.beatmap as beatmap
from objects.data import loadRawData


def extractMappoolNames(bracketMappools):
    mappoolNames = []
    for entry in bracketMappools:
        if entry.Name == "":
            mappoolNames.append(entry.Description.lower())
            continue
        mappoolNames.append(entry.Name.lower())
    return mappoolNames


class Class(object):
    # TODO: Refactor this class
    def __init__(self, bracketMappools, modsFilename="mods.txt", mappoolFilename="mappool.txt"):
        self.current_round = 0
        self.bracketMappools = bracketMappools
        mods = loadRawData(modsFilename)
        self.mods = []
        for mod in mods:
            self.mods.append(mod[0])
        self.mapEntries = loadRawData(mappoolFilename)

    def getMappool(self):
        if self.mapEntries:
            self.bracketMappools[self.current_round].Beatmaps = self.fetchMaps()
        else:
            logging.error(f"General mappool reading error: {self.mapEntries}")

    def fetchMaps(self):
        maps = []
        for entry in self.mapEntries:
            mod = entry[0][0:-1]
            if mod not in self.mods:
                self.writeMapsToMappool(entry, maps)
                maps = []
            else:
                maps.append(beatmap.Class(int(entry[1]), entry[0][0:-1]))
        return maps

    def writeMapsToMappool(self, entry, maps):
        logging.debug(f"'{entry[0][0:-1]}' isn't in mods.csv")
        if entry != self.mapEntries[0]:
            logging.debug("Writing beatmaps to round '{}'".format(self.bracketMappools[self.current_round].Name))
            self.bracketMappools[self.current_round].Beatmaps = maps
        self.checkIfMappoolNameExists(entry[0])

# TODO: Make this non WTF'y
    def checkIfMappoolNameExists(self, name):
        round_names = extractMappoolNames(self.bracketMappools)
        for i in range(len(round_names)):
            if name.lower() == round_names[i]:
                logging.debug(f"Found '{name}' in Rounds")
                self.current_round = i
                return
        logging.warning(f"Didn't find '{name}' in Rounds")
        self.bracketMappools.append(mappool.Class(name))
        self.current_round = len(self.bracketMappools) - 1
        assert self.current_round >= 0
