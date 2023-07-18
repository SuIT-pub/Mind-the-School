init -6 python:
    import re
    import math
    class Time:
        def __init__(self):
            self.daytime = 0
            self.day = 1
            self.month = 1
            self.year = 2023

        def progress_day(self):
            self.daytime = 1
            self.day += 1
            if self.day >= 29:
                self.day = 1
                self.month += 1
                if self.month >= 13:
                    self.month = 1
                    self.year += 1

        def progress_time(self):
            self.daytime += 1

            if self.daytime == 8:
                self.progress_day()

        def get_daytime(self):
            return self.daytime

        def get_day(self):
            return self.day

        def get_week(self):
            return int(math.ceil(self.day / 7))

        def get_month(self):
            return self.month

        def get_year(self):
            return self.year

        def get_weekday_num(self, day = -1):
            if day == -1:
                day = self.day
            wd = (day + 28) % 7
            if wd == 0:
                return 7
            return wd

        def get_weekday(self, day = -1):
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

        def check_day(self, value):
            if value == "x":
                return True
                
            value = str(value)

            day_split = value.split(',')

            for split_val in day_split:
                split_value = split_val.strip()
                val_str = re.findall('\d+', split_value)
                if val_str:
                    day = int(''.join(val_str))

                    if (day == self.day or
                        (split_value.endswith('+') and self.day >= day) or
                        (split_value.endswith('-') and self.day <= day)
                    ):
                        return True
                    elif '-' in split_value:
                        split_value = split_value.split('-')
                        if (len(split_value) == 2 and 
                            split_value[0].isdecimal() and
                            split_value[1].isdecimal() and
                            int(split_value[0]) <= self.day <= int(split_value[1])
                        ):
                            return True

            return str(value) == str(self.day)

        def check_month(self, value):
            if value == "x":
                return True

            value = str(value)

            month_split = value.split(',')

            for split_val in month_split:
                split_value = split_val.strip()
                val_str = re.findall('\d+', split_value)
                if val_str:
                    month = int(''.join(val_str))

                    if (month == self.month or
                        (split_value.endswith('+') and self.month >= month )or
                        (split_value.endswith('-') and self.month <= month)
                    ):
                        return True
                    elif '-' in split_value:
                        split_value = split_value.split('-')
                        if (len(split_value) == 2 and 
                            split_value[0].isdecimal() and
                            split_value[1].isdecimal() and
                            int(split_value[0]) <= self.month <= int(split_value[1])
                        ):
                            return True

            return str(value) == str(self.month)

        def check_year(self, value):
            if value == "x":
                return True

            value = str(value)

            year_split = value.split(',')

            for split_val in year_split:
                split_value = split_val.strip()
                val_str = re.findall('\d+', split_value)
                if val_str:
                    year = int(''.join(val_str))

                    if (year == self.year or
                        (split_value.endswith('+') and self.year >= year) or
                        (split_value.endswith('-') and self.year <= year)
                    ):
                        return True
                    elif '-' in split_value:
                        split_value = split_value.split('-')
                        if (len(split_value) == 2 and 
                            split_value[0].isdecimal() and
                            split_value[1].isdecimal() and
                            int(split_value[0]) <= self.year <= int(split_value[1])
                        ):
                            return True

            return str(value) == str(self.year)

        def check_daytime(self, value):
            if value == "x":
                return True

            value = str(value)

            if (value == self.daytime or
                (value == 'c' and     self.daytime in [2, 4, 5]) or
                (value == 'f' and     self.daytime in [1, 3, 6])
            ):
                return True

            daytime_split = value.split(',')

            for split_val in daytime_split:
                split_value = split_val.strip()
                val_str = re.findall('\d+', split_value)
                if val_str:
                    daytime = int(''.join(val_str))

                    if ((split_value.endswith('+') and self.daytime >= daytime) or
                        (split_value.endswith('-') and self.daytime <= daytime)
                    ):
                        return True
                    elif '-' in split_value:
                        split_value = split_value.split('-')
                        if (len(split_value) == 2 and 
                            split_value[0].isdecimal() and
                            split_value[1].isdecimal() and
                            int(split_value[0]) <= self.daytime <= int(split_value[1])
                        ):
                            return self.daytime

            return str(value) == str(self.daytime)
        
        def check_week(self, value):
            if value == "x":
                return True

            value = str(value)

            week_split = value.split(',')

            for split_val in week_split:
                split_value = split_val.strip()
                val_str = re.findall('\d+', split_value)
                if val_str:
                    week = int(''.join(val_str))

                    if (week == self.get_week() or
                        (split_value.endswith('+') and self.get_week() >= week) or
                        (split_value.endswith('-') and self.get_week() <= week)
                    ):
                        return True
                    elif '-' in split_value:
                        split_value = split_value.split('-')
                        if (len(split_value) == 2 and 
                            split_value[0].isdecimal() and
                            split_value[1].isdecimal() and
                            int(split_value[0]) <= self.get_week() <= int(split_value[1])
                        ):
                            return True

            return str(value) == str(time.get_week())

        def check_weekday(self, value):
            if value == "x":
                return True

            value = str(value)

            print("value:" + value + " weekday:" + str(self.get_weekday_num()))

            if (value == str(self.get_weekday_num()) or
                (value == 'd' and time.get_weekday_num() < 6) or
                (value == 'w' and time.get_weekday_num() > 5)
            ):
                return True

            weekday_split = value.split(',')

            for split_val in weekday_split:
                split_value = split_val.strip()
                val_str = re.findall('\d+', split_value)
                if val_str:
                    weekday = int(''.join(val_str))

                    if ((split_value.endswith('+') and self.get_weekday() >= weekday) or
                        (split_value.endswith('-') and self.get_weekday() <= weekday)
                    ):
                        return True
                    elif '-' in split_value:
                        split_value = split_value.split('-')
                        if (len(split_value) == 2 and 
                            split_value[0].isdecimal() and
                            split_value[1].isdecimal() and
                            int(split_value[0]) <= self.get_weekday() <= int(split_value[1])
                        ):
                            return True

            return str(value) == time.get_weekday()

        def get_month_name(self, month = -1):
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

        def get_daytime_name(self, daytime = -1):
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

        def today(self):
            return str(self.day) + "." + str(self.month) + "." + str(self.year)

        def now(self):
            return self.today() + "." + str(self.daytime)

        def today_is_after_date(self, day, month, year):
            if self.year > year:
                return True
            if self.month > month:
                return True
            if self.day > day:
                return True
            return False

        def now_is_after_time(self, day, month, year, time):
            if self.today_is_after_date(day, month, year):
                return True
            if self.daytime > time:
                return True
            return False





