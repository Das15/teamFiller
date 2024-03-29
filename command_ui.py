import inquirer
import os
import logging
import sys
from PySide6 import QtWidgets

import objects.bracket as bracket
import objects.mappool as mappool
import objects.mappool_data as mappool_data
import objects.teams_data as teams_data
import objects.challonge_response as challonge_response
import apiRequests.challonge.querries as challonge_request
import config


# I love singletons, I really do, it's not like im being forced to make global variables or anything
# Long story short, it's necessary to make QT framework word like I want it to.
# Honestly I wonder why not just use web like app interface solution, should be simple enough.
_filepath_app = None


def fill_mappool(bracket_data: bracket.Class, mods_filepath: str = "mods.txt") -> list[mappool.Class]:
    secondary_path = str(os.path.join(os.getcwd(), "mappool.txt"))
    mappool_path = get_file_path(os.getcwd(), "Open mappool data", opened_file_on_fail=secondary_path)
    mappool_output = mappool_data.Class(bracket_data.Rounds, mods_filepath, mappool_path)
    mappool_output.get_mappool()
    return mappool_output.bracket_mappools


def fill_ladder(bracket_data: bracket.Class) -> bracket.Class:
    tourney_challonge_code = input("Please write challonge tournament id (last part of link): ")

    challonge_data = challonge_response.Class(challonge_request.get_tournament(tourney_challonge_code))
    return challonge_data.replace_acronyms(bracket_data)


def fill_teams(bracket_data: bracket.Class, assume_order_by_seeds=True) -> bracket.Class:
    secondary_path = str(os.path.join(os.path.join(os.getcwd(), "teams.txt")))
    teams_data_path = get_file_path(os.getcwd(), "Open teams data", opened_file_on_fail=secondary_path)
    data = teams_data.Class(teams_data_path, assume_order_by_seeds)
    for team in data.teams:
        bracket_data.Teams.append(team)
    logging.info(f"Added {len(data.teams)} teams into bracket file.")
    return bracket_data


def get_file_path(default_dir: str = None, window_title: str = "Open", opened_file_on_fail: str = None,
                  allowed_formats: str = "Text files (*.txt *.csv)") -> str | None:
    dialog = QtWidgets.QFileDialog(None)
    dialog.setWindowTitle(window_title)
    dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
    dialog.setNameFilter(allowed_formats)

    if default_dir:
        dialog.setDirectory(default_dir)

    if dialog.exec():
        return dialog.selectedFiles()[0]
    if opened_file_on_fail:
        if not os.path.exists(opened_file_on_fail):
            with open(opened_file_on_fail, "w"):
                pass
        os.startfile(opened_file_on_fail)
        input("Press enter when done editing the file.")
        return opened_file_on_fail

    dialog.destroy()
    return str(None)


def execute_functions(answers: list[str]):
    bracket_path = None
    if not answers:
        return
    while bracket_path is None:
        bracket_path = get_file_path(f"{os.getenv('APPDATA')}/osu/tournaments/", "Open bracket file", None,
                                     "Bracket file (*.json)")
    bracket_data = bracket.load_json(bracket_path)
    backup_bracket_file(bracket_data, bracket_path)

    if "Mappool" in answers:
        bracket_data.Rounds = fill_mappool(bracket_data)
    if "Ladder" in answers:
        # TODO: Put this check in initialize_ui or something
        if config.get_config_value("challonge_api_key") != "":
            bracket_data = fill_ladder(bracket_data)
        else:
            print("No challonge key in config, add it there first before trying to get ladder from challonge.")
    if "Teams" in answers:
        do_seeding_by_order = inquirer.confirm("Do you want to use seeding based on team order?", default=True)
        bracket_data = fill_teams(bracket_data, do_seeding_by_order)
    bracket_data.write_to_file(bracket_path)


def backup_bracket_file(bracket_data: bracket.Class, bracket_path: str):
    backup_path = "/".join(bracket_path.split("/")[:-1]) + "/backup.json"
    temp_path = backup_path
    i = 1
    while os.path.exists(temp_path):
        split_path = backup_path.split(".")
        temp_path = f"{split_path[0]}{i}.{split_path[1]}"
        i += 1
    bracket_data.write_to_file(temp_path)
    logging.info(f"Bracket file backupped at {temp_path}")


def initialize_ui():
    global _filepath_app
    _filepath_app = QtWidgets.QApplication(sys.argv)
    questions = [
        inquirer.Checkbox("options",
                          message="What parts of bracket file would you like to update?",
                          choices=["Mappool", "Ladder", "Teams"],
                          carousel=True),
    ]
    answers = None
    try:
        answers = inquirer.prompt(questions)["options"]
    except TypeError:
        logging.debug("User cancelled selection, closing the script.")
        exit(0)

    logging.debug(f"Selected options in ui: {str(answers)}")
    execute_functions(answers)
