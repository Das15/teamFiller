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
    def __init__(self, bracketMappools: list[mappool.Class], modsFilename: str = "mods.txt",
                 mappoolFilename: str = "mappool.txt"):
        self.bracket_mappools = bracketMappools
        mods = load_raw_data(modsFilename)
        self.mods = []
        for mod in mods:
            self.mods.append(mod[0])
        self.mapEntries = load_raw_data(mappoolFilename)

    def get_mappool(self):
        if self.mapEntries:
            self.fetch_maps()
        else:
            logging.fatal(f"Expected entries from file, got none.")
            exit(-1)

    def fetch_maps(self):
        maps = []
        curr_round_iterator = 0
        for entry in self.mapEntries:
            name = entry[0][0:-1]
            if name not in self.mods:
                if entry[0] in self.mods:
                    maps.append(beatmap.Class(int(entry[1]), entry[0]))
                    continue
                logging.debug(f"'{entry[0][0:-1]}' isn't in mods.csv")
                if entry == self.mapEntries[0]:
                    curr_round_iterator = self.change_current_mappool(curr_round_iterator, entry[0])
                    logging.debug("Skipping first entry from mappool file.")
                    continue

                curr_mappool = self.bracket_mappools[curr_round_iterator]
                logged_name = curr_mappool.Description if curr_mappool.Name == "" else curr_mappool.Name
                logging.debug(f"Writing beatmaps to '{logged_name}'")
                self.bracket_mappools[curr_round_iterator].Beatmaps = maps

                curr_round_iterator = self.change_current_mappool(curr_round_iterator, entry[0])
                maps = []
            else:
                maps.append(beatmap.Class(int(entry[1]), entry[0][0:-1]))
        self.bracket_mappools[curr_round_iterator].Beatmaps = maps

    def change_current_mappool(self, curr_round_iterator: int, name: str) -> int:
        name_exists = False
        bracket_round_names = extract_mappool_names(self.bracket_mappools)
        for i, current_round_name in enumerate(bracket_round_names):
            if name.lower() == current_round_name:
                logging.debug(f"Found '{name}' in rounds.")
                curr_round_iterator = i
                name_exists = True
                break
        if not name_exists:
            logging.warning(f"Didn't find '{name}' in rounds.")

            self.bracket_mappools.append(mappool.Class(name))
            curr_round_iterator = len(self.bracket_mappools) - 1

            assert curr_round_iterator >= 0
        return curr_round_iterator
