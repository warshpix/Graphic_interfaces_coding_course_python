class Character:
    def __init__(self, name, actions):
        self.name = name
        self._actions = actions
        self.achievements = set()

    def get_efficiency(self):
        return sum(self._actions)

    def add_action(self, action_value):
        if isinstance(action_value, int):
            self._actions.append(action_value)

    def __isBerserker(self):
        sum = 0
        for i in range(0, len(self._actions)):
            if self._actions[i] > 0:
                sum += self._actions[i]

        if sum > 50:
            return True
        else:
            return False

    def __isTank(self):
        sum = 0
        for i in range(0, len(self._actions)):
            if self._actions[i] < 0:
                sum += self._actions[i]

        if sum < -20:
            return True
        else:
            return False

    def __isLucky(self):
        sum = 0
        for i in range(0, len(self._actions)):
            if self._actions[i] < 0:
                sum += self._actions[i]

        if sum == 0:
            return True
        else:
            return False

    def check_basic_achievements(self):
        for i in range(0, len(self._actions)):
            if self.__isBerserker():
                self.achievements.add("Berserker")
            if self.__isTank():
                self.achievements.add("Tank")
            if self.__isLucky():
                self.achievements.add("Lucky")
