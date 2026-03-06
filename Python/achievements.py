from Python.pr1_Main import character_log_analysis

def isBerserker(textLog):
    sum = 0
    for i in range(0, len(textLog["actions"])):
        if textLog["actions"][i] > 0:
            sum += textLog["actions"][i]

    if sum > 50:
        return True
    else:
        return False

def isTank(textLog):
    sum = 0
    for i in range(0, len(textLog["actions"])):
        if textLog["actions"][i] < 0:
            sum += textLog["actions"][i]

    if sum < -20:
        return True
    else:
        return False

def isLucky(textLog):
    sum = 0
    for i in range(0, len(textLog["actions"])):
        if textLog["actions"][i] < 0:
            sum += textLog["actions"][i]

    if sum == 0:
        return True
    else:
        return False


def giveAchievements(textLog):
    result = []
    mvp = character_log_analysis(textLog)

    for i in range(0, len(textLog)):
        achievements = set()
        if isBerserker(textLog[i]):
            achievements.add("Berserker")
        if isTank(textLog[i]):
            achievements.add("Tank")
        if isLucky(textLog[i]):
            achievements.add("Lucky")
        if textLog[i]["name"] == mvp[0]["name"]:
            achievements.add("MVP")

        if len(achievements) != 0:
            result.append({"name":textLog[i]["name"], "actions": textLog[i]["actions"], "achievements":achievements})
        else:
            result.append({"name":textLog[i]["name"], "actions": textLog[i]["actions"], "achievements": "None"})

    return result

