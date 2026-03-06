def writeGameLog(textLog):
    file_path = r"C:\Users\warshpixie\Desktop\GameLogs.txt"
    result = "--- Game Session Report ---\n"
    for i in range(0, len(textLog)):
        result += "Character: " + textLog[i]["name"] + "\n"
        result += "Status: Alive" + "\n"
        result += "Achievements: " + str((textLog[i]["achievements"])) + "\n"
        result += "Efficiency:" + str(sum((textLog[i]["actions"]))) + "\n"
        result += "--------------------" + "\n"

    with open(file_path, "w") as file:
        file.write(result)

    print("File saved successfully!")