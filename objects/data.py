import codecs
import logging


def parseEntry(entry):
    temp = []
    dataList = entry.split("\t")
    for data in dataList:
        if data != "":
            temp.append(data.replace("\r", ""))
    return temp


def parseCsvDataFromStringList(string):
    temp = []
    for entry in string:
        if entry.split("\t") != [""]:
            temp.append(parseEntry(entry))
    return temp


def loadRawData(path):
    logging.log(logging.INFO, f"Loading teams_data from '{path}'")
    with codecs.open(path, "r", encoding="utf-8") as file:
        temp = file.read().split("\n")
    return parseCsvDataFromStringList(temp)
