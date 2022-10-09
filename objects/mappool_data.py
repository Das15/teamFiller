import logging
import objects.mappool as mappool
import objects.beatmap as beatmap
from objects.data import load_raw_data


def extract_mappool_names(bracket_mappools: list[mappool.Class]) -> list[str]:
    mappool_names = []
    for entry in bracket_mappools:
        if entry.Name == "":
            mappool_names.append(entry.Description.lower())
            continue
        mappool_names.append(entry.Name.lower())
    return mappool_names


# noinspection PyPep8Naming
class Class(object):
    # TODO: Refactor this class
    def __init__(self, bracketMappools: list[mappool.Class], modsFilename: str = "mods.txt",
                 mappoolFilename: str = "mappool.txt"):
        self.current_round = 0
        self.bracket_mappools = bracketMappools
        mods = load_raw_data(modsFilename)
        self.mods = []
        for mod in mods:
            self.mods.append(mod[0])
        self.mapEntries = load_raw_data(mappoolFilename)

    def get_mappool(self):
        if self.mapEntries:
            self.bracket_mappools[self.current_round].Beatmaps = self.fetch_maps()
        else:
            logging.error(f"Expected non null value at mapEntries, instead got null.")

    def fetch_maps(self):
        maps = []
        for entry in self.mapEntries:
            mod = entry[0][0:-1]
            if mod not in self.mods:
                self.write_maps_to_mappool(entry, maps)
                maps = []
            else:
                maps.append(beatmap.Class(int(entry[1]), entry[0][0:-1]))
        return maps

    def write_maps_to_mappool(self, entry, maps):
        logging.debug(f"'{entry[0][0:-1]}' isn't in mods.csv")
        if entry != self.mapEntries[0]:
            logging.debug("Writing beatmaps to round '{}'".format(self.bracket_mappools[self.current_round].Name))
            self.bracket_mappools[self.current_round].Beatmaps = maps
        self.check_if_mappool_name_exists(entry[0])

# TODO: Make this non WTF'y
    def check_if_mappool_name_exists(self, name):
        round_names = extract_mappool_names(self.bracket_mappools)
        for i in range(len(round_names)):
            if name.lower() == round_names[i]:
                logging.debug(f"Found '{name}' in rounds.")
                self.current_round = i
                return
        logging.warning(f"Didn't find '{name}' in rounds.")
        self.bracket_mappools.append(mappool.Class(name))
        self.current_round = len(self.bracket_mappools) - 1
        assert self.current_round >= 0
