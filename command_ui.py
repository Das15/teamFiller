import inquirer
import objects.bracket as bracket
import objects.mappool_data as mappool_data
import objects.teams_data as teams_data
import objects.challonge_response as challonge_response
import apiRequests.challonge.querries as challonge_request
import os
import wx
import logging


def fillMappool(bracketData, modsFilepath="mods.txt"):
    secondaryPath = str(os.path.join(os.getcwd(), "mappool.txt"))
    mappoolPath = getFilePath(os.getcwd(), "Open mappool data", openedFileOnFail=secondaryPath)
    mappool = mappool_data.Class(bracketData.Rounds, modsFilepath, mappoolPath)
    mappool.getMappool()
    return mappool.bracketMappools


def fillLadder(bracketData):
    tourneyChallongeCode = input("Please write challonge tournament id (last part of link): ")

    challongeData = challonge_response.Class(challonge_request.getTournament(tourneyChallongeCode))
    return challongeData.replaceAcronyms(bracketData)


def fillTeams(bracketData, assumeOrderBySeeds=True):
    secondaryPath = str(os.path.join(os.path.join(os.getcwd(), "teams.txt")))
    teamsDataPath = getFilePath(os.getcwd(), "Open teams data", openedFileOnFail=secondaryPath)
    teamsData = teams_data.Class(teamsDataPath, assumeOrderBySeeds)
    for team in teamsData.teams:
        bracketData.append(team)
    logging.info(f"Added {len(teamsData.teams)} teams into bracket file.")
    return bracketData


def getFilePath(defaultDir=None, windowTitle="Open", openedFileOnFail=None):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, windowTitle, style=style)
    if defaultDir:
        dialog.SetDirectory(defaultDir)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        if openedFileOnFail:
            os.startfile(openedFileOnFail)
            input("Press enter when done editing the file.")
            return openedFileOnFail
        path = None
    dialog.Destroy()
    return path


def executeFunctions(answers, bracketData=None):
    bracketPath = None
    if answers:
        while bracketPath is None:
            bracketPath = getFilePath(f"{os.getenv('APPDATA')}\\osu\\tournaments\\", "Open bracket file")
        bracketData = bracket.load_json(bracketPath)

        backupBracketFile(bracketData, bracketPath)

    if "Mappool" in answers:
        bracketData.Rounds = fillMappool(bracketData)
    if "Ladder" in answers:
        bracketData = fillLadder(bracketData)
    if "Teams" in answers:
        bracketData = fillTeams(bracketData)
    bracketData.writeToFile(bracketPath)


def backupBracketFile(bracketData, bracketPath):
    backupPath = "\\".join(bracketPath.split("\\")[:-1]) + "\\backup.json"
    tempPath = backupPath
    i = 1
    while os.path.exists(tempPath):
        splitPath = backupPath.split(".")
        tempPath = f"{splitPath[0]}{i}.{splitPath[1]}"
        i += 1
    bracketData.writeToFile(tempPath)
    logging.info(f"Bracket file backupped at {tempPath}")


def checkApiKeys():
    pass


def initializeUi():
    checkApiKeys()
    questions = [
        inquirer.Checkbox("options",
                          message="What parts of bracket file would you like to update?",
                          choices=["Mappool", "Ladder", "Teams"],
                          carousel=True),
    ]
    answers = inquirer.prompt(questions)["options"]
    logging.info(f"Selected options in ui: {str(answers)}")
    executeFunctions(answers)
