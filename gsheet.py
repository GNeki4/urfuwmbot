import gspread
import sheet_addition as s_a
from datetime import datetime, timedelta
import time
from oauth2client.service_account import ServiceAccountCredentials

class Kostil(Exception):
    pass


class MySheet:
    def __init__(self, hours_string: str, amount_of_days: int, amount_of_washing_machines: int, time_to_wait):
        self.list_of_hours = hours_string.split(" ")  # список часов
        self.amount_of_days = amount_of_days  # количество дней
        self.amount_of_washing_machines = amount_of_washing_machines  # количество стиральных машинок
        self.hours_count = len(self.list_of_hours)  # количество часов
        self.dates_column = 1  # колонка дат
        self.weekdays_column = 2  # колонка дней недели
        self.times_column = 3  # колонка времени
        self.registration_column = 4  # начало колонки для регистрации
        self.list_of_raw_dates = MySheet.get_days_from_now_raw(self)
        self.list_of_dates = MySheet.stringify_all_dates(self)  # лист с датами
        self.list_of_weekdays = MySheet.stringify_all_dates_to_weekdays(self)  # лист с днями недели
        self.time_to_wait = time_to_wait  # время задержки в секундах
        # preparations
        self.scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            "spreadsheetexample-273115-78e95ad21457.json",
            self.scope)
        self.gc = gspread.authorize(self.credentials)
        # for merging
        self.client = gspread.authorize(self.credentials)
        self.spreadsheetId = "1IQOeMlwpEYU95hyyrIQ09vJiyWaNu1ndFKjuybeT74Q"
        self.sheetName = "Main"
        self.ss = self.client.open_by_key(self.spreadsheetId)
        self.sheetId = self.ss.worksheet(self.sheetName)._properties['sheetId']
        self.wks = self.gc.open("TestSheet").sheet1
        # end of preparations

    def get_days_from_now_raw(self):
        list_of_dates_raw = []

        for single_date in (datetime.today() + timedelta(n) for n in range(self.amount_of_days)):
            list_of_dates_raw.append(single_date)

        return list_of_dates_raw

    def stringify_all_dates(self):
        list_of_dates = []

        for single_date in self.list_of_raw_dates:
            list_of_dates.append(single_date.strftime("%d.%m"))

        return list_of_dates

    def stringify_all_dates_to_weekdays(self, update=False, date=None):
        if update:
            weekday = date.weekday()
            return self.convert_day_to_weekday(weekday)
        else:
            list_of_weeks = []
            for single_date in self.list_of_raw_dates:
                weekday = single_date.weekday()
                list_of_weeks.append(self.convert_day_to_weekday(weekday))

            return list_of_weeks

    @staticmethod
    def convert_day_to_weekday(weekday: int):
        if weekday == 0:
            return "Понедельник\nMonday"
        if weekday == 1:
            return "Вторник\nTuesday"
        if weekday == 2:
            return "Среда\nWednesday"
        if weekday == 3:
            return "Четверг\nThursday"
        if weekday == 4:
            return "Пятница\nFriday"
        if weekday == 5:
            return "Суббота\nSaturday"
        if weekday == 6:
            return "Воскресенье\nSunday"

    @staticmethod
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

    def fill_header(self):
        header = ["Дата\nDate", "День недели\nDay of the week", "Время\nTime"]
        wm = 1
        while wm <= self.amount_of_washing_machines:
            header.append("Машинка #" + str(wm) + "\nWm #" + str(wm))
            wm += 1
        self.wks.append_row(header)
        time.sleep(self.time_to_wait)

    def fill_days(self, row_days=2, update=False):
        if update:
            self.wks.update_cell(row_days, self.dates_column, self.list_of_dates[-1])
            s_a.merge_cells(self.sheetId, self.ss, row_days, row_days + self.hours_count,
                            self.dates_column - 1, self.dates_column)
            time.sleep(self.time_to_wait)
        else:
            for day in self.list_of_dates:
                self.wks.update_cell(row_days, self.dates_column, day)
                s_a.merge_cells(self.sheetId, self.ss, row_days, row_days + self.hours_count,
                                self.dates_column - 1, self.dates_column)
                row_days = row_days + self.hours_count
                time.sleep(self.time_to_wait)

    def fill_weeks(self, row_weeks=2, update=False):
        if update:
            self.wks.update_cell(row_weeks, self.weekdays_column, self.list_of_weekdays[-1])
            s_a.merge_cells(self.sheetId, self.ss, row_weeks, row_weeks + self.hours_count,
                            self.weekdays_column - 1, self.weekdays_column)
            time.sleep(self.time_to_wait)
        else:
            for weekday in self.list_of_weekdays:
                self.wks.update_cell(row_weeks, self.weekdays_column, weekday)
                s_a.merge_cells(self.sheetId, self.ss, row_weeks, row_weeks + self.hours_count,
                                self.weekdays_column - 1, self.weekdays_column)
                row_weeks = row_weeks + self.hours_count
                time.sleep(self.time_to_wait)

    def fill_time(self, row_time=2, update=False):
        if update:
            for i in range(len(self.list_of_hours)):
                self.wks.update_cell(row_time + i, self.times_column, str(self.list_of_hours[i]))
                time.sleep(self.time_to_wait)
        else:
            for day in range(len(self.list_of_dates)):
                for i in range(len(self.list_of_hours)):
                    self.wks.update_cell(row_time + i, self.times_column, str(self.list_of_hours[i]))
                    time.sleep(self.time_to_wait)

                row_time = row_time + self.hours_count

    def update_day(self):
        '''
        for i in range(len(self.list_of_hours)):
            self.wks.delete_row(2)
            time.sleep(self.time_to_wait)
        '''

        self.wks.delete_rows(2, len(self.list_of_hours) + 1)

        start_row = len(self.wks.col_values(1)) + self.hours_count

        new_date = self.list_of_raw_dates[0] + timedelta(days=self.amount_of_days)
        self.list_of_raw_dates.append(new_date)
        self.list_of_raw_dates.pop(0)

        self.list_of_dates.pop(0)
        self.list_of_dates.append(new_date.strftime("%d.%m"))

        self.list_of_weekdays.pop(0)
        new_weekday = self.stringify_all_dates_to_weekdays(True, new_date)
        self.list_of_weekdays.append(new_weekday)

        self.fill_days(start_row, update=True)
        self.fill_weeks(start_row, update=True)
        self.fill_time(start_row, update=True)

    def ban_day(self, day: str):
        day_to_ban = self.wks.find(day)
        top = day_to_ban.row
        bottom = top + len(self.list_of_hours)
        left = day_to_ban.col + 3
        right = left + self.amount_of_washing_machines

        for row in range(top, bottom):
            for col in range(left, right):
                self.wks.update_cell(row, col, "")

        self.wks.update_cell(top, left, "Запись невозможна\nRegistration prohibited")
        self.merge_cells(self.sheetId, self.ss, top, bottom, left - 1, right - 1)

    def change_cell(self, row: int, col: int, msg: str):
        self.wks.update_cell(row, col, msg)

    def register(self, input_string: str, initials: str):
        input_info = input_string.split()
        wms_to_sign = input_info[0]
        date_to_sign = input_info[1]
        time_to_sign = input_info[2]

        # нахождение даты в таблице
        date_to_sign_row = int
        try:
            cell = self.wks.find(date_to_sign)
            date_to_sign_row = cell.row
        except:
            return "Проблема с датой"


        # нахождение времени в таблице
        found_time_cell = False
        final_row = int
        hours_temp = len(self.list_of_hours)
        for row in range(date_to_sign_row, date_to_sign_row + hours_temp):
            if self.wks.cell(row, self.times_column).value == time_to_sign:
                final_row = row
                found_time_cell = True
                break

        if not found_time_cell:
            return "Проблема со временем"

        try:
            wms_to_sign = int(wms_to_sign)
        except:
            return "Неправильный формат количества машинок"

        free_wms_columns = []
        for column in range(self.registration_column, self.registration_column + self.amount_of_washing_machines):
            if self.wks.cell(final_row, column).value == "":
                free_wms_columns.append(column)

        if len(free_wms_columns) >= wms_to_sign:
            for column in range(wms_to_sign):
                self.wks.update_cell(final_row, free_wms_columns[column], initials)
        else:
            return "Нет места для такого количества машинок"

        return "True"


start_time = time.time()

hours = "19:00 20:00 21:00"
sheet = MySheet(hours, 10, 3, 1.5)  # лист с часами, потом количество дней, потом количество машинок, потом таймаут

# testing
#test_string = "1\n05.01\n11:00"
#sheet.register(test_string, "Жмышенко В.А.")
# testing

#sheet.fill_header()
#sheet.fill_days()
#sheet.fill_weeks()
#sheet.fill_time()
'''
#for i in range(2):
    #sheet.update_day()
'''
#sheet.ban_day(sheet.list_of_dates[2])

# sheet.change_cell(3, 4, "nigger")
end_time = time.time()

print("This code took " + "%.2f" % (end_time - start_time) + " seconds to compile")
