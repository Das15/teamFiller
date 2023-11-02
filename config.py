import logging
import os.path
import enum

import apiRequests.bancho.querries as bancho_api
import apiRequests.challonge.querries as challonge_api

config = {}


@enum.unique
class VerificationType(enum.Enum):
    """Range from 0 to 2."""
    NONE = 0
    BANCHO = 1
    CHALLONGE_KEY = 2


def create_config_file(config_dictionary):
    with open("config.cfg", "w", encoding="utf-8") as file:
        for key, value in config_dictionary.items():
            file.write(f"{key} = {value}\n")


def get_config_value(key):
    if config:
        return config[key]
    else:
        read_config()
        if config:
            return config[key]
    logging.error("Didn't find config file. Creating one.")


class ConfigItem(object):
    def __init__(self, key_name: str, input_label: str, verify_data: VerificationType):
        self.keyName = key_name
        self.inputLabel = input_label
        self.verifyData = verify_data


def create_config():
    # Note to myself: osu key has length of 40
    # Inspired by inquirer's solution.
    temp_config = [ConfigItem("bancho_api_key", "Please paste your bancho API key here: ",
                              VerificationType.BANCHO),
                   ConfigItem("challonge_api_key", "Please paste your challonge API key here (can be left empty): ",
                              VerificationType.CHALLONGE_KEY)]
    config_data = get_and_verify_config_data(temp_config)
    create_config_file(config_data)


def get_and_verify_config_data(temp_config):
    """Verifies data using the APIs."""
    config_data = {}
    for item in temp_config:
        while True:
            temp = input(item.inputLabel)
            if item.verifyData == VerificationType.BANCHO:
                if len(temp) < 40:
                    print("API key is too short.")
                    continue
                bancho_api.API_KEY = temp
                check_result = bancho_api.check_if_user_id_exists("2")
                if not check_result:
                    print("Bancho api key is invalid.")
                    continue
                break
            if item.verifyData == VerificationType.CHALLONGE_KEY:
                if temp == "":
                    break
                challonge_api.APIKEY = temp
                check = challonge_api.check_challonge_key(temp)
                if not check:
                    print("Challonge api key is invalid.")
                    continue
                break
        config_data[item.keyName] = temp
    return config_data


# Another fancy csv reader function, redundancy approved
# TODO: Remove redundant code in reading files.
def read_config():
    if not os.path.exists("config.cfg"):
        create_config()
    with open("config.cfg", "r", encoding="utf-8") as file:
        line_count = 0
        for line_count, line in enumerate(file):
            if line[0] == "#":
                continue
            temp = line.replace(" ", "").replace("\n", "")
            key, value = temp.split("=")
            config[key] = value
        logging.info(f"Read {line_count} lines from config.cfg.")
    return config


# Used for config testing.
if __name__ == "__main__":
    print(get_config_value("challonge_api_key"))
