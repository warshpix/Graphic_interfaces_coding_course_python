from Python.pr1_Main import *
from Python.achievements import giveAchievements
from Python.reports import writeGameLog

#Subtask 1 - interpret the logs of th game as a dictionry
events = [15, -8, 0, 30, -12, 5, 0, -3, 20]
#print(log_analysis(events))

#Subtask 2 - Text log analysis
#text_log = "Player1 entered the dungeon. Player1 attacked the enemy! Enemy attacked Player1! Player1 used healing potion. Player1 defeated the enemy! Player1 exited the dungeon."
#print(text_log_analysis(text_log))

#Subtask 3 - analysis of player data
characters = [
    {"name": "Warrior", "actions": [25, -10, 0, 40, -5]},
    {"name": "Mage", "actions": [35, 0, -20, 50]},
    {"name": "Archer", "actions": [20, -5, 15, 0, 10]}
]
#print(character_log_analysis(characters))

#Subtask 4 - game sum up
#game_sum_up(events, text_log, characters)



writeGameLog(giveAchievements(characters))