from Python.GameSession import GameSession
from Python.Mage import Mage
from Python.Shaman import Shaman
from Python.Warrior import Warrior

# Створення об'єктів гравців
player1 = Warrior("Garrosh", [25, -10, 0, 40, -5])
player2 = Mage("Jaina", [35, 0, -20, 50])
player3 = Shaman("Thrall", [0, -5, 15, 0, 10, 0])

# Створення ігрової сесії
session = GameSession("Session_001")
session.add_participant(player1)
session.add_participant(player2)
session.add_participant(player3)

# Генерація звіту
for player in session.participants:
    player.check_basic_achievements()

session.assign_mvp()
session.generate_report("session_report.txt")
