import logging
import os.path
import enum
import requests

import apiRequests.bancho.querries as banchoApi
import apiRequests.challonge.querries as challongeApi

config = {}


@enum.unique
class verificationType(enum.Enum):
    NONE = 0
    BANCHO = 1
    CHALLONGE_KEY = 2
    CHALLONGE_USERNAME = 3


def createConfigFile(configDictionary):
    with open("config.cfg", "w", encoding="utf-8") as file:
        for key, value in configDictionary.items():
            file.write(f"{key} = {value}\n")


def getConfigValue(key):
    if config:
        return config[key]
    else:
        readConfig()
        if config:
            return config[key]
    logging.error("Didn't find config file. Creating one.")


class configItem(object):
    def __init__(self, keyName: str, inputLabel: str, verifyData: verificationType):
        self.keyName = keyName
        self.inputLabel = inputLabel
        self.verifyData = verifyData


# TODO: Verify if API keys are correct
def createConfig():
    # Note to myself: osu key has length of 40
    tempConfig = [configItem("bancho_api_key", "Please paste your bancho API key here: ",
                             verificationType.BANCHO),
                  configItem("challonge_api_key", "Please paste your challonge API key here (can be left empty): ",
                             verificationType.CHALLONGE_KEY),
                  configItem("challonge_username", "Please write your challonge username here (can be left empty): ",
                             verificationType.CHALLONGE_USERNAME)]
    configData = getConfigData(tempConfig)
    createConfigFile(configData)


def getConfigData(tempConfig):
    configData = {}
    isChallongeKeyValid = False
    for item in tempConfig:
        temp = ""
        while True:
            temp = input(item.inputLabel)
            if item.verifyData == verificationType.BANCHO:
                if len(temp) < 40:
                    continue
                banchoApi.APIKEY = temp
                checkResult = banchoApi.checkIfUserIdExists(2)
                if not checkResult:
                    print("Bancho api key is invalid.")
                    continue
                break
            if item.verifyData == verificationType.CHALLONGE_KEY:
                if temp == "":
                    break
                challongeApi.APIKEY = temp
                check = challongeApi.checkChallongeKey(temp)
                if not check:
                    print("Challonge api key is invalid.")
                    continue
                isChallongeKeyValid = True
                break
            if item.verifyData == verificationType.CHALLONGE_USERNAME:
                if not isChallongeKeyValid:
                    break
                try:
                    challongeApi.USERNAME = temp
                    challongeApi.requestTournament("MP5D", False)
                except requests.HTTPError as e:
                    logging.error(f"Username verification failed: {e.args[0]}")
                    print("Username is invalid.")
                    continue
                break
        configData[item.keyName] = temp
    return configData


def readConfig():
    if not os.path.exists("config.cfg"):
        createConfig()
    with open("config.cfg", "r", encoding="utf-8") as file:
        lineCount = 0
        for lineCount, line in enumerate(file):
            if line[0] == "#":
                continue
            temp = line.replace(" ", "").replace("\n", "")
            key, value = temp.split("=")
            config[key] = value
        logging.info(f"Read {lineCount} lines from config.cfg.")
    return config


if __name__ == "__main__":
    print(getConfigValue("challonge_api_key"))


def exists():
    return os.path.exists("config.cfg")
