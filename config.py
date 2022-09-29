import logging
import os.path

config = {}


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


# TODO: Verify if API keys are correct
def createConfig():
    # Note to myself: osu key has length of 40
    tempConfig = {"bancho_api_key": input("Please paste your bancho API key here (no verification): "),
                  "challonge_api_key": input("Please paste your challonge API key here (can be left empty): "),
                  "challonge_username": input("Please write your challonge username here (can be left empty): ")}
    createConfigFile(tempConfig)


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
