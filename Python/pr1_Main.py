import re


def log_analysis(events):
    overall_score = 0
    positive_amount = 0
    negative_amount = 0
    zero_amount = 0
    minimum_amount = events[0]
    maximum_amount = events[0]

    for i in range(len(events)):

        overall_score += events[i]

        if events[i] > 0:
            positive_amount = positive_amount + 1
        elif events[i] < 0:
            negative_amount = negative_amount + 1
        else:
            zero_amount = zero_amount + 1

        if (events[i] < minimum_amount):
            minimum_amount = events[i]
        elif (events[i] > maximum_amount):
            maximum_amount = events[i]


    average_result = overall_score / len(events)

    result = {
        "Кількість подій": len(events),
        "Сумарний результат": overall_score,
        "Середнє значення": average_result,
        "Кількість додатніх значень": positive_amount,
        "Кількість від'ємних значень": negative_amount,
        "Кількість нульових значень": zero_amount,
        "Мінімальне значення": minimum_amount,
        "Максимальне значення": maximum_amount
    }

    return result

def text_log_analysis(text_log_raw):
    text_log_raw = text_log_raw.lower()
    text_log = (re.split(r'(?<=[.!])\s+', text_log_raw))
    amount_of_symbols = len(text_log_raw.replace(' ', ''))
    amount_of_words = len(text_log_raw.split())
    amount_of_rows_player = 0
    amount_of_rows_enemy = 0
    events_list = []
    most_common_event = text_log[0]
    most_common_event_amount = 1;

    for i in range(len(text_log)):
        found = False
        for item in events_list:
            if item["event"] == text_log[i].split()[1]:
                item["amount"] += 1
                found = True
                break

        if not found:
            events_list.append({"event": text_log[i].split()[1], "amount": 1})

        log = text_log[i].split()
        if log[0] == "enemy":
            amount_of_rows_enemy+=1
        else:
            amount_of_rows_player+=1

    for item in events_list:
        if item["amount"] > most_common_event_amount:
            most_common_event_amount = item["amount"]
            most_common_event = item["event"]

    result = {
        "Кількість символів": amount_of_symbols,
        "Кількість слів": amount_of_words,
        "Кількість рядків гравця": amount_of_rows_player,
        "Кількість рядків ворогів": amount_of_rows_enemy,
        "Найчастіше згадана подія": most_common_event
    }

    return result

def character_log_analysis(character_log):
    most_efficient_character_name = character_log[0]["name"]
    most_efficient_character_score = sum(character_log[0]["actions"])

    for i in range(1, len(character_log)):
        if sum(character_log[i]["actions"]) > most_efficient_character_score:
            most_efficient_character_name = character_log[i]["name"]
            most_efficient_character_score = sum(character_log[i]["actions"])

    result = [{"name": most_efficient_character_name, "score": most_efficient_character_score}]

    return result

def game_sum_up(events, text_log, characters):
    print(log_analysis(events))
    print(text_log_analysis(text_log))
    print("Найефективніший персонаж - ", character_log_analysis(characters))


