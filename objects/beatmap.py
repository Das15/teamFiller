import logging

import objects.beatmap_info as beatmap_info


# noinspection PyPep8Naming
class Class(object):
    """I'm sure this isn't confusing scheme at all, as in beatmap class is actually objects.beatmap.Class."""
    def __key(self):
        return self.ID, self.Mods, self.BeatmapInfo

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, obj):
        return self.ID == obj.ID and self.Mods == obj.Mods

    def __init__(self, ID: int, Mods: str, BeatmapInfo: dict = None) -> None:
        """Mainly used for parsing bracket file."""
        self.ID = ID
        self.Mods = Mods
        if BeatmapInfo != {}:
            if BeatmapInfo is None:
                self.BeatmapInfo = BeatmapInfo
            else:
                try:
                    if BeatmapInfo["Metadata"] is not None:
                        if BeatmapInfo["Metadata"] is not None:
                            self.BeatmapInfo = beatmap_info.Class(**BeatmapInfo)
                except AttributeError:
                    logging.error(f"Didn't find id {ID} in BeatmapInfo.")
                except TypeError:
                    logging.error(f"Wrong BeatmapInfo found in {ID} OR someone changed json key names again.")

    def __iter__(self):
        """Forgot why it's here, but it's probably important."""
        yield "ID", self.ID
        yield "Mods", self.Mods
        yield "BeatmapInfo", self.BeatmapInfo
