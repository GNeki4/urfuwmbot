from datetime import datetime, timedelta
import time


def get_dates_from_now(n):
    list_of_dates = []

    for single_date in (datetime.today() + timedelta(n) for n in range(n)):
        list_of_dates.append(single_date.strftime("%d.%m"))

    return list_of_dates


def merge_cells(sheetId, ss, top, bottom, left, right):
    body = {
        "requests": [
            {
                "mergeCells": {
                    "mergeType": "MERGE_ALL",
                    "range": {  # In this sample script, all cells of "A1:C3" of "Sheet1" are merged.
                        "sheetId": sheetId,
                        "startRowIndex": top - 1,
                        "endRowIndex": bottom - 1,
                        "startColumnIndex": left,
                        "endColumnIndex": right
                    }
                }
            }
        ]
    }

    ss.batch_update(body)


def get_time_hours(*args):
    list_of_hours = []

    for element in args:
        if not (isinstance(element, int)):
            raise TimeIsNotIntException("Ввел хуйню полную а не время")
        else:
            list_of_hours.append(element)

    return sorted(set(list_of_hours))


class TimeIsNotIntException(Exception):
    pass


# get_time_hours(10.6)


def get_days_of_the_week(n):
    list_of_weeks = []

    for single_date in (datetime.today() + timedelta(n) for n in range(n)):
        weekday = single_date.weekday()
        if weekday == 0:
            list_of_weeks.append("Понедельник\nMonday")
        if weekday == 1:
            list_of_weeks.append("Вторник\nTuesday")
        if weekday == 2:
            list_of_weeks.append("Среда\nWednesday")
        if weekday == 3:
            list_of_weeks.append("Четверг\nThursday")
        if weekday == 4:
            list_of_weeks.append("Пятница\nFriday")
        if weekday == 5:
            list_of_weeks.append("Суббота\nSaturday")
        if weekday == 6:
            list_of_weeks.append("Воскресенье\nSunday")

    return list_of_weeks # spizdi


'''
lma1 = get_dates_from_now(2)
for day in lma1:
    print(day)
'''

'''
lmao = get_days_of_the_week(10)
for day in lmao:
    print(day)
'''

#  print(time.strftime("%H:%M"))