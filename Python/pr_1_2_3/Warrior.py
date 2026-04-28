from Python.pr_1_2_3.Character import Character

class Warrior(Character):
    def __isRageMachine(self):
        sum = 0
        for i in range(0, len(self._actions)):
            if self._actions[i] > 0:
                sum += self._actions[i]

        if sum > 80:
            return True
        else:
            return False

    def check_basic_achievements(self):
        if self. __isRageMachine():
            self.achievements.append("Rage Machine")

        super().check_basic_achievements()