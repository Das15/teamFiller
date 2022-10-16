import logging

import objects.team as team
import objects.player as player
from objects.data import load_raw_data
from apiRequests.bancho.querries import get_user_id, check_if_user_id_exists


class Class(object):
    def __init__(self, file_path, assume_order_by_seeds=False):
        data = parse_raw_data(load_raw_data(file_path))
        self.teams = create_teams_from_parsed_data(data, assume_order_by_seeds)


def check_for_team_name_in_data(team_name, data):
    for i in range(len(data)):
        if team_name == data[i]["teamName"]:
            return i
    return None


def extract_acronyms(teams):
    acronyms = []
    for entry in teams:
        acronyms.append(entry.Acronym)
    return acronyms


# TODO: Extract acronym matching funtion so it can be accessed from other files
def check_for_duplicated_entries(teams):
    acronyms = extract_acronyms(teams)
    duplicated_entries = []
    for i in range(len(teams)):
        if teams[i].Acronym in acronyms:
            tempArray = acronyms.copy()
            tempArray.remove(teams[i].Acronym)
            if teams[i].Acronym in tempArray:
                if acronyms.index(teams[i].Acronym) == i:
                    temp = [tempArray.index(teams[i].Acronym), i]
                    duplicated_entries.append([min(temp), max(temp)+1])
    return duplicated_entries


def parse_player_id(raw_player_id):
    if raw_player_id == "":
        return None
    if raw_player_id.isdigit() and check_if_user_id_exists(raw_player_id):
        return raw_player_id
    else:
        playerId = get_user_id(raw_player_id)
        return playerId


def parse_raw_data(data):
    teams = []
    max_length = len(max(data, key=len))
    for line in data:
        temp = {"teamName": "",
                "players": []}
        for i in range(len(line)):
            if i == 0:
                temp["teamName"] = line[i]
            else:
                player_id = parse_player_id(line[i])
                if player_id is not None:
                    temp["players"].append(player_id)
        check = check_for_team_name_in_data(temp["teamName"], teams)
        if check is not None:
            for entry in temp["players"]:
                teams[check]["players"].append(entry)
        else:
            if temp["teamName"]:
                if not temp["players"] and max_length == 1:
                    temp["players"].append(parse_player_id(temp["teamName"]))
                teams.append(temp)
    return teams


def parse_acronyms(teams):
    duplicated_entries = check_for_duplicated_entries(teams)
    for entry in duplicated_entries:
        old_acronym = teams[entry[1]].Acronym
        teams[entry[1]].parse_acronym(4)
        if old_acronym == teams[entry[1]].Acronym:
            teams[entry[1]].Acronym += " "
        if teams[entry[0]].Acronym == teams[entry[1]]:
            logging.error("Something went wrong and entries {} and {} are the same.".format(*entry))
            pass
    return teams


def create_teams_from_parsed_data(data, assume_order_by_seeds):
    temp = []
    curr_seed = 1
    for entry in data:
        players = []
        for playerId in entry["players"]:
            players.append(player.Class(playerId))
        team_data = team.Class(entry["teamName"], curr_seed) if assume_order_by_seeds else team.Class(entry["teamName"])
        curr_seed += 1
        team_data.Players = players
        temp.append(team_data)
    return temp
