import codecs
import logging


def parse_entry(entry: str) -> list[str]:
    temp = []
    data_list = entry.split("\t")
    for data in data_list:
        if data != "":
            temp.append(data.replace("\r", ""))
    return temp


def parse_csv_data_from_string_list(string: list[str]) -> list[list[str]]:
    temp = []
    for entry in string:
        if entry.split("\t") != [""]:
            temp.append(parse_entry(entry))
    return temp


def load_raw_data(path: str) -> list[list[str]]:
    """It does in fact assume file is csv file. I should probably fix in the future."""
    logging.log(logging.INFO, f"Loading teams_data from '{path}'")
    with codecs.open(path, "r", encoding="utf-8") as file:
        temp = file.read().split("\n")
    return parse_csv_data_from_string_list(temp)
