import logging
import os.path
import enum
import requests

import apiRequests.bancho.querries as bancho_api
import apiRequests.challonge.querries as challonge_api

config = {}


@enum.unique
class VerificationType(enum.Enum):
    NONE = 0
    BANCHO = 1
    CHALLONGE_KEY = 2
    CHALLONGE_USERNAME = 3


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
    def __init__(self, key_name: str, input_label: str, verify_data: verification_type):
        self.keyName = key_name
        self.inputLabel = input_label
        self.verifyData = verify_data


# TODO: Verify if API keys are correct
def create_config():
    # Note to myself: osu key has length of 40
    temp_config = [ConfigItem("bancho_api_key", "Please paste your bancho API key here: ",
                              verification_type.BANCHO),
                   ConfigItem("challonge_api_key", "Please paste your challonge API key here (can be left empty): ",
                              verification_type.CHALLONGE_KEY),
                   ConfigItem("challonge_username", "Please write your challonge username here (can be left empty): ",
                              verification_type.CHALLONGE_USERNAME)]
    config_data = get_config_data(temp_config)
    create_config_file(config_data)


def get_config_data(temp_config):
    config_data = {}
    is_challonge_key_valid = False
    for item in temp_config:
        while True:
            temp = input(item.inputLabel)
            if item.verifyData == verification_type.BANCHO:
                if len(temp) < 40:
                    continue
                bancho_api.API_KEY = temp
                check_result = bancho_api.check_if_user_id_exists(2)
                if not check_result:
                    print("Bancho api key is invalid.")
                    continue
                break
            if item.verifyData == verification_type.CHALLONGE_KEY:
                if temp == "":
                    break
                challonge_api.APIKEY = temp
                check = challonge_api.check_challonge_key(temp)
                if not check:
                    print("Challonge api key is invalid.")
                    continue
                is_challonge_key_valid = True
                break
            if item.verifyData == verification_type.CHALLONGE_USERNAME:
                if not is_challonge_key_valid:
                    break
                try:
                    challonge_api.USERNAME = temp
                    challonge_api.request_tournament("MP5D", False)
                except requests.HTTPError as e:
                    logging.error(f"Username verification failed: {e.args[0]}")
                    print("Username is invalid.")
                    continue
                break
        config_data[item.keyName] = temp
    return config_data


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


if __name__ == "__main__":
    print(get_config_value("challonge_api_key"))


def exists():
    return os.path.exists("config.cfg")
