from importlib import reload
from apiRequests.general import initialize_api_keys

import command_ui
import objects.bracket as bracket
import objects.teams_data as teams_data
import logging
import objects.mappool_data as mappool_data
import objects.challonge_response as challonge_response
import apiRequests.challonge.querries as challonge_request


def load_teams_from_file(bracket_file, filepath, assume_order_by_seeds):
    teams = teams_data.Class(filepath, assume_order_by_seeds).teams
    for team in teams:
        bracket_file.Teams.append(team)
    return bracket_file


def load_mappool_from_file(bracket_file):
    mappool = mappool_data.Class(bracket_file.Rounds, "mods.txt", "mappool.txt")
    mappool.get_mappool()
    return mappool.bracket_mappools


def download_ladder_from_challonge(bracket_file):
    challonge_data = challonge_response.Class(challonge_request.get_tournament("N2VC"))
    return challonge_data.replace_acronyms(bracket_file)


def legacy_edit_bracket():
    bracket_data = bracket.load_json("bracket.json")
    bracket_data.Rounds = load_mappool_from_file(bracket_data)
    bracket_data = load_teams_from_file(bracket_data, "teams.txt", assume_order_by_seeds=True)
    bracket_data = download_ladder_from_challonge(bracket_data)

    bracket_data.write_to_file("output.json")


def main():
    reload(logging)
    logging.basicConfig(level=logging.DEBUG, filename="logs.log", filemode="w",
                        format='%(asctime)s %(levelname)s - %(message)s', datefmt="%d-%m-%y %H:%M:%S")
    initialize_api_keys()
    command_ui.initialize_ui()


if __name__ == "__main__":
    main()
