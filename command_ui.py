import inquirer
import objects.bracket as bracket
import objects.mappool_data as mappool_data
import objects.teams_data as teams_data
import objects.challonge_response as challonge_response
import apiRequests.challonge.querries as challonge_request
import os
import wx
import logging


def fill_mappool(bracket_data, mods_filepath="mods.txt"):
    secondary_path = str(os.path.join(os.getcwd(), "mappool.txt"))
    mappool_path = get_file_path(os.getcwd(), "Open mappool data", opened_file_on_fail=secondary_path)
    mappool = mappool_data.Class(bracket_data.Rounds, mods_filepath, mappool_path)
    mappool.get_mappool()
    return mappool.bracket_mappools


def fill_ladder(bracket_data):
    tourney_challonge_code = input("Please write challonge tournament id (last part of link): ")

    challonge_data = challonge_response.Class(challonge_request.get_tournament(tourney_challonge_code))
    return challonge_data.replace_acronyms(bracket_data)


def fill_teams(bracket_data, assume_order_by_seeds=True):
    secondary_path = str(os.path.join(os.path.join(os.getcwd(), "teams.txt")))
    teams_data_path = get_file_path(os.getcwd(), "Open teams data", opened_file_on_fail=secondary_path)
    data = teams_data.Class(teams_data_path, assume_order_by_seeds)
    for team in data.teams:
        bracket_data.append(team)
    logging.info(f"Added {len(data.teams)} teams into bracket file.")
    return bracket_data


# noinspection PyUnusedLocal
def get_file_path(default_dir=None, window_title="Open", opened_file_on_fail=None):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, window_title, style=style)
    if default_dir:
        dialog.SetDirectory(default_dir)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        if opened_file_on_fail:
            os.startfile(opened_file_on_fail)
            input("Press enter when done editing the file.")
            return opened_file_on_fail
        path = None
    dialog.Destroy()
    return path


def execute_functions(answers, bracket_data=None):
    bracket_path = None
    if answers:
        while bracket_path is None:
            bracket_path = get_file_path(f"{os.getenv('APPDATA')}\\osu\\tournaments\\", "Open bracket file")
        bracket_data = bracket.load_json(bracket_path)

        backup_bracket_file(bracket_data, bracket_path)

    if "Mappool" in answers:
        bracket_data.Rounds = fill_mappool(bracket_data)
    if "Ladder" in answers:
        bracket_data = fill_ladder(bracket_data)
    if "Teams" in answers:
        bracket_data = fill_teams(bracket_data)
    bracket_data.writeToFile(bracket_path)


def backup_bracket_file(bracket_data, bracket_path):
    backup_path = "\\".join(bracket_path.split("\\")[:-1]) + "\\backup.json"
    temp_path = backup_path
    i = 1
    while os.path.exists(temp_path):
        split_path = backup_path.split(".")
        temp_path = f"{split_path[0]}{i}.{split_path[1]}"
        i += 1
    bracket_data.write_to_file(temp_path)
    logging.info(f"Bracket file backupped at {temp_path}")


def initialize_ui():
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
        logging.info("User cancelled selection, closing the script.")
        exit(0)

    logging.info(f"Selected options in ui: {str(answers)}")
    execute_functions(answers)
