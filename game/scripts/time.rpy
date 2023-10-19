init -6 python:
    import re
    import math
    class Time:
        def __init__(self):
            self.daytime = 0
            self.day = 1
            self.month = 1
            self.year = 2023

        def set_time(self, **kwargs: int | str) -> None:
            if 'day' in kwargs.keys():
                self.day = kwargs['day']
            if 'month' in kwargs.keys():
                self.month = kwargs['month']
            if 'year' in kwargs.keys():
                self.year = kwargs['year']
            if 'daytime' in kwargs.keys():
                self.daytime = kwargs['daytime']
            else:
                self.daytime = 1

            self.correct_time()

        def add_time(self, **kwargs: int) -> None:
            if 'day' in kwargs.keys():
                self.day += kwargs['day']
            if 'month' in kwargs.keys():
                self.month += kwargs['month']
            if 'year' in kwargs.keys():
                self.year += kwargs['year']
            if 'daytime' in kwargs.keys():
                self.daytime += kwargs['daytime']

            self.correct_time()

        def progress_day(self) -> None:
            self.daytime = 1
            self.day += 1
            self.correct_time()

        def progress_time(self) -> bool:
            self.daytime += 1

            if self.daytime == 8:
                self.progress_day()
                return True
            return False
        
        def correct_time(self) -> None:
            while self.daytime > 7:
                self.daytime -= 7
                self.day += 1

            while self.day > 28:
                self.day -= 22
                self.month += 1

            while self.month > 12:
                self.month -= 12
                self.year += 1

        def get_daytime(self) -> int:
            return self.daytime

        def get_day(self) -> int:
            return self.day

        def get_week(self) -> int:
            return int(math.ceil(self.day / 7))

        def get_month(self) -> int:
            return self.month

        def get_year(self) -> int:
            return self.year

        def get_weekday_num(self, day: int = -1) -> int:
            if day == -1:
                day = self.day
            wd = (day + 28) % 7
            if wd == 0:
                return 7
            return wd

        def get_weekday(self, day: int = -1) -> str:
            if isinstance(day, str):
                if day.isdigit():
                    day = int(day)
                else:
                    if day == "d":
                        return "Work Day"
                    if day == "w":
                        return "Weekend"
                    return day
            if day < 1 or day > 7:
                day = self.get_weekday_num()
            weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            
            return weekday[day - 1]

        def check_day(self, value: str | int) -> bool:
            if value == "x":
                return True
                
            return check_in_value(value, self.day)

            # value = str(value)

            # day_split = value.split(',')

            # for split_val in day_split:
            #     split_value = split_val.strip()
            #     val_str = re.findall('\d+', split_value)
            #     if len(val_str) == 0:
            #         return False
            #     if val_str:
            #         day = int(''.join(val_str))

            #         if (day == self.day or
            #             (split_value.endswith('+') and self.day >= day) or
            #             (split_value.endswith('-') and self.day <= day) or
            #             self.day == day
            #         ):
            #             return True
            #         elif '-' in split_value:
            #             split_value = split_value.split('-')
            #             if (len(split_value) == 2 and 
            #                 split_value[0].isdecimal() and
            #                 split_value[1].isdecimal() and
            #                 int(split_value[0]) <= self.day <= int(split_value[1])
            #             ):
            #                 return True

            # return str(value) == str(self.day)

        def check_month(self, value: str | int) -> bool:
            if value == "x":
                return True

            return check_in_value(value, self.month)

            # value = str(value)

            # month_split = value.split(',')

            # for split_val in month_split:
            #     split_value = split_val.strip()
            #     val_str = re.findall('\d+', split_value)
            #     if val_str:
            #         month = int(''.join(val_str))

            #         if (month == self.month or
            #             (split_value.endswith('+') and self.month >= month) or
            #             (split_value.endswith('-') and self.month <= month) or
            #             self.month == month
            #         ):
            #             return True
            #         elif '-' in split_value:
            #             split_value = split_value.split('-')
            #             if (len(split_value) == 2 and 
            #                 split_value[0].isdecimal() and
            #                 split_value[1].isdecimal() and
            #                 int(split_value[0]) <= self.month <= int(split_value[1])
            #             ):
            #                 return True

            # return str(value) == str(self.month)

        def check_year(self, value: str | int) -> bool:
            if value == "x":
                return True

            return check_in_value(value, self.year)

            # value = str(value)

            # year_split = value.split(',')

            # for split_val in year_split:
            #     split_value = split_val.strip()
            #     val_str = re.findall('\d+', split_value)
            #     if val_str:
            #         year = int(''.join(val_str))

            #         if (year == self.year or
            #             (split_value.endswith('+') and self.year >= year) or
            #             (split_value.endswith('-') and self.year <= year) or
            #             self.year == year
            #         ):
            #             return True
            #         elif '-' in split_value:
            #             split_value = split_value.split('-')
            #             if (len(split_value) == 2 and 
            #                 split_value[0].isdecimal() and
            #                 split_value[1].isdecimal() and
            #                 int(split_value[0]) <= self.year <= int(split_value[1])
            #             ):
            #                 return True

            # return str(value) == str(self.year)

        def check_daytime(self, value: str | int) -> bool:
            if value == "x":
                return True

            if (value == self.daytime or
                (value == 'c' and     self.daytime in [2, 4, 5]) or
                (value == 'f' and     self.daytime in [1, 3, 6]) or
                (value == 'd' and     self.daytime in [1, 2, 3, 4, 5, 6]) or
                (value == 'n' and     self.daytime in [7])
            ):
                return True

            return check_in_value(value, self.daytime)

            # value = str(value)

            # daytime_split = value.split(',')

            # for split_val in daytime_split:
            #     split_value = split_val.strip()
            #     val_str = re.findall('\d+', split_value)

            #     if val_str:
            #         daytime = int(''.join(val_str))

            #         if ((split_value.endswith('+') and self.daytime >= daytime) or
            #             (split_value.endswith('-') and self.daytime <= daytime) or
            #             self.daytime == daytime
            #         ):
            #             return True
            #         elif '-' in split_value:
            #             split_value = split_value.split('-')
            #             if (len(split_value) == 2 and 
            #                 split_value[0].isdecimal() and
            #                 split_value[1].isdecimal() and
            #                 int(split_value[0]) <= self.daytime <= int(split_value[1])
            #             ):
            #                 return True

            # return str(value) == str(self.daytime)
        
        def check_week(self, value: str | int) -> bool:
            if value == "x":
                return True

            return check_in_value(value, self.get_week())

            # value = str(value)

            # week_split = value.split(',')

            # for split_val in week_split:
            #     split_value = split_val.strip()
            #     val_str = re.findall('\d+', split_value)
            #     if val_str:
            #         week = int(''.join(val_str))

            #         if (week == self.get_week() or
            #             (split_value.endswith('+') and self.get_week() >= week) or
            #             (split_value.endswith('-') and self.get_week() <= week) or
            #             self.get_week() == week
            #         ):
            #             return True
            #         elif '-' in split_value:
            #             split_value = split_value.split('-')
            #             if (len(split_value) == 2 and 
            #                 split_value[0].isdecimal() and
            #                 split_value[1].isdecimal() and
            #                 int(split_value[0]) <= self.get_week() <= int(split_value[1])
            #             ):
            #                 return True

            # return str(value) == str(time.get_week())

        def check_weekday(self, value: str | int) -> bool:
            if value == "x":
                return True

            if (value == str(self.get_weekday_num()) or
                (value == 'd' and time.get_weekday_num() < 6) or
                (value == 'w' and time.get_weekday_num() > 5)
            ):
                return True

            return check_in_value(value, self.get_weekday_num())

            # value = str(value)

            # weekday_split = value.split(',')

            # for split_val in weekday_split:
            #     split_value = split_val.strip()
            #     val_str = re.findall('\d+', split_value)
            #     if val_str:
            #         weekday = int(''.join(val_str))

            #         if ((split_value.endswith('+') and self.get_weekday() >= weekday) or
            #             (split_value.endswith('-') and self.get_weekday() <= weekday) or
            #             self.get_weekday() == weekday
            #         ):
            #             return True
            #         elif '-' in split_value:
            #             split_value = split_value.split('-')
            #             if (len(split_value) == 2 and 
            #                 split_value[0].isdecimal() and
            #                 split_value[1].isdecimal() and
            #                 int(split_value[0]) <= self.get_weekday() <= int(split_value[1])
            #             ):
            #                 return True

            # return str(value) == time.get_weekday()

        def get_month_name(self, month: int = -1) -> str:
            if isinstance(month, str):
                if not month.isdigit():
                    return month
                month = int(month)

            if month < 1 or month > 12:
                month = self.month
            month_name = ["January", "February", "March", "April", "May", "June", 
                "July", "August", "September", "October", "November", "December"
            ]
            return month_name[month - 1]

        def get_daytime_name(self, daytime: int = -1) -> str:
            if isinstance(daytime, str):
                if daytime.isdigit():
                    daytime = int(daytime)
                else:
                    if daytime == "c":
                        return "Class Time"
                    if daytime == "f":
                        return "Free Time"
                    return daytime
            if daytime < 1 or daytime > 7:
                daytime = self.daytime
            daytime_name = ["Morning", "Early Noon", "Noon", "Early Afternoon", "Afternoon", "Evening", "Night"]
            return daytime_name[daytime - 1]

        def today(self) -> str:
            return str(self.day) + "." + str(self.month) + "." + str(self.year)

        def now(self) -> str:
            return self.today() + "." + str(self.daytime)

        def today_is_after_date(self, day: int, month: int, year: int) -> bool:
            if self.year > year:
                return True
            if self.month > month:
                return True
            if self.day > day:
                return True
            return False

        def now_is_after_time(self, day: int, month: int, year: int, time: int) -> bool:
            if self.today_is_after_date(day, month, year):
                return True
            if self.daytime > time:
                return True
            return False





