from Python.pr_1_2_3.Character import Character

class Shaman(Character):
    def __isSupportPillar(self):
        sum = 0
        for i in range(0, len(self._actions)):
            if self._actions[i] == 0:
                sum += 1

        if sum > 3:
            return True
        else:
            return False

    def check_basic_achievements(self):
        if self.__isSupportPillar():
            self.achievements.add("Support Pillar")

        super().check_basic_achievements()