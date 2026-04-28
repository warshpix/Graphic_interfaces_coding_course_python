from Python.pr_1_2_3.Character import Character


class GameSession:
    def __init__(self, session_name):
        self.session_id = session_name
        self.participants = []

    def add_participant(self, character_obj):
        if isinstance(character_obj, Character):
            self.participants.append(character_obj)

    def assign_mvp(self):
        mvp = 0
        mvp_score = self.participants[0].get_efficiency()

        for i in range (1, len(self.participants)):
            current_score = self.participants[i].get_efficiency()
            if current_score > mvp_score:
                mvp = i
                mvp_score = current_score
        self.participants[mvp].achievements.add("MVP")

    def generate_report(self, filename):
        file_path = r"C:\Users\warshpixie\Desktop\GameLogs.txt"
        result = "--- Game Session Report ---\n"
        for i in range(0, len(self.participants)):
            result += "Character: " + str(self.participants[i].name) + "\n"
            result += "Status: Alive" + "\n"
            if str(self.participants[i].achievements) == "set()":
                result += "Achievements: No achievements" + "\n"
            else:
                result += "Achievements: " + str(self.participants[i].achievements) + "\n"
            result += "Efficiency:" + str(self.participants[i].get_efficiency()) + "\n"
            result += "--------------------" + "\n"
        with open(file_path, "w") as file:
            file.write(result)
        print("File saved successfully!")