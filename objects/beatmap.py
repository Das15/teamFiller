import objects.beatmap_info as beatmapInfo
import logging


class Class(object):
    def __key(self):
        return self.ID, self.Mods, self.BeatmapInfo

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, obj):
        return self.ID == obj.ID and self.Mods == obj.Mods

    def __init__(self, ID: int, Mods: str, BeatmapInfo=None):
        self.ID = ID
        self.Mods = Mods
        if BeatmapInfo != {}:
            if BeatmapInfo is None:
                self.BeatmapInfo = BeatmapInfo
            else:
                try:
                    if BeatmapInfo["Metadata"] is not None:
                        if BeatmapInfo["OnlineID"] is not None:
                            self.BeatmapInfo = beatmapInfo.Class(**BeatmapInfo)
                except AttributeError:
                    logging.error(f"Didn't found id {ID} in BeatmapInfo.")
                except TypeError:
                    logging.error(f"Wrong BeatmapInfo found in {ID} OR someone changed json key names again.")
