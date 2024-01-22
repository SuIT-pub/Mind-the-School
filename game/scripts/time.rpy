init -6 python:
    import re
    import math
    class Time:
        """
        Time class for handling time and date in the game.
        Each class saves its own date and time.

        ### Attributes:
        1. daytime: int
            - the time of the day
            - 1: Morning
            - 2: Early Noon
            - 3: Noon
            - 4: Early Afternoon
            - 5: Afternoon
            - 6: Evening
            - 7: Night
        2. day: int
            - the day in the month
            - from 1 - 28
        3. month: int
            - the month in the year
            - from 1 - 12
        4. year: int
            - the year

        ### Methods:
        1. set_time(self, **kwargs: int | str)
            - sets the time
        2. add_time(self, **kwargs: int)
            - adds time to the current time
        3. progress_day(self)
            - progresses the day to the next day
        4. progress_time(self) -> bool
            - progresses the time to the next time
            - returns True if the day has changed
        5. correct_time(self)
            - corrects the time if it is out of bounds
        6. get_daytime(self) -> int
            - returns the current time of the day
        7. get_day(self) -> int
            - returns the current day
        8. get_week(self) -> int
            - returns the current week
        9. get_month(self) -> int
            - returns the current month
        10. get_year(self) -> int
            - returns the current year
        11. get_weekday_num(self, day: int = -1) -> int
            - returns the current weekday number
            - if day is given, returns the weekday number of that day
        12. get_weekday(self, day: int = -1) -> str
            - returns the current weekday
            - if day is given, returns the weekday of that day
        13. check_day(self, value: str | int) -> bool
            - checks if the current day is equal to the given value
        14. check_month(self, value: str | int) -> bool
            - checks if the current month is equal to the given value
        15. check_year(self, value: str | int) -> bool
            - checks if the current year is equal to the given value
        16. check_daytime(self, value: str | int) -> bool
            - checks if the current time of the day is equal to the given value
        17. check_week(self, value: str | int) -> bool
            - checks if the current week is equal to the given value
        18. check_weekday(self, value: str | int) -> bool
            - checks if the current weekday is equal to the given value
        19. get_month_name(self, month: int = -1) -> str
            - returns the name of the current month
            - if month is given, returns the name of that month
        20. get_daytime_name(self, daytime: int = -1) -> str
            - returns the name of the current time of the day
            - if daytime is given, returns the name of that time of the day
        21. today(self) -> str
            - returns the current date
        22. now(self) -> str
            - returns the current date and time
        23. today_is_after_date(self, day: int, month: int, year: int) -> bool
            - checks if the current date is after the given date
        24. now_is_after_time(self, day: int, month: int, year: int, time: int) -> bool
            - checks if the current date and time is after the given date and time
        """

        def __init__(self):
            self.daytime = 0
            self.day = 1
            self.month = 1
            self.year = 2023

        def set_time(self, **kwargs: int):
            """
            Sets the time.

            ### Parameters:
            1. **kwargs: int
                - day: int
                    - the day in the month
                    - from 1 - 28
                - month: int
                    - the month in the year
                    - from 1 - 12
                - year: int
                    - the year
                - daytime: int
                    - the time of the day
                    - 1: Morning
                    - 2: Early Noon
                    - 3: Noon
                    - 4: Early Afternoon
                    - 5: Afternoon
                    - 6: Evening
                    - 7: Night
            """

            if is_in_replay:
                return

            if 'day' in kwargs.keys() and is_integer(kwargs['day']):
                self.day = kwargs['day']
            if 'month' in kwargs.keys() and is_integer(kwargs['month']):
                self.month = kwargs['month']
            if 'year' in kwargs.keys() and is_integer(kwargs['year']):
                self.year = kwargs['year']
            if 'daytime' in kwargs.keys() and is_integer(kwargs['daytime']):
                self.daytime = kwargs['daytime']
            else:
                self.daytime = 1

            self.correct_time()

        def add_time(self, **kwargs: int):
            """
            Adds time to the current time.

            ### Parameters:
            1. **kwargs: int
                - day: int
                    - the day in the month
                    - from 1 - 28
                - month: int
                    - the month in the year
                    - from 1 - 12
                - year: int
                    - the year
                - daytime: int
                    - the time of the day
                    - 1: Morning
                    - 2: Early Noon
                    - 3: Noon
                    - 4: Early Afternoon
                    - 5: Afternoon
                    - 6: Evening
                    - 7: Night
            """

            if 'day' in kwargs.keys() and is_integer(kwargs['day']):
                self.day += kwargs['day']
            if 'month' in kwargs.keys() and is_integer(kwargs['month']):
                self.month += kwargs['month']
            if 'year' in kwargs.keys() and is_integer(kwargs['year']):
                self.year += kwargs['year']
            if 'daytime' in kwargs.keys() and is_integer(kwargs['daytime']):
                self.daytime += kwargs['daytime']

            self.correct_time()

        def progress_day(self):
            """
            Progresses the day to the next day.
            """

            self.daytime = 1
            self.day += 1
            self.correct_time()

        def progress_time(self) -> bool:
            """
            Progresses the time to the next time.

            ### Returns:
            1. bool
                - True if the day has changed
            """

            self.daytime += 1

            if self.daytime == 8:
                self.progress_day()
                return True
            return False
        
        def correct_time(self):
            """
            Corrects the time if it is out of bounds.
            """

            while self.daytime > 7:
                self.daytime -= 7
                self.day += 1

            while self.day > 28:
                self.day -= 28
                self.month += 1

            while self.month > 12:
                self.month -= 12
                self.year += 1

        def get_daytime(self) -> int:
            """
            Returns the current time of the day.

            ### Returns:
            1. int
                - the current time of the day
                - 1: Morning
                - 2: Early Noon
                - 3: Noon
                - 4: Early Afternoon
                - 5: Afternoon
                - 6: Evening
                - 7: Night
            """

            return self.daytime

        def get_day(self) -> int:
            """
            Returns the current day.

            ### Returns:
            1. int
                - the current day
                - from 1 - 28
            """
            return self.day

        def get_week(self) -> int:
            """
            Returns the current week.

            ### Returns:
            1. int
                - the current week
                - from 1 - 4
            """

            return int(math.ceil(self.day / 7))

        def get_month(self) -> int:
            """
            Returns the current month.

            ### Returns:
            1. int
                - the current month
                - from 1 - 12
            """

            return self.month

        def get_year(self) -> int:
            """
            Returns the current year.

            ### Returns:
            1. int
                - the current year
            """

            return self.year

        def get_weekday_num(self, day: int = -1) -> int:
            """
            Returns the current weekday number.

            ### Parameters:
            1. day: int
                - the day in the month
                - from 1 - 28
                - if day is -1, returns the current weekday number of today

            ### Returns:
            1. int
                - the current weekday number
                - from 1 - 7
            """

            if day == -1:
                day = self.day
            wd = (day + 28) % 7
            if wd == 0:
                return 7
            return wd

        def get_weekday(self, day: int = -1) -> str:
            """
            Returns the current weekday.

            ### Parameters:
            1. day: int
                - the day in the month
                - from 1 - 28 or "d" or "w"

            ### Returns:
            1. str
                - the current weekday
                - if day is -1, returns the current weekday of today
                - if day is "d", returns "Work Day"
                - if day is "w", returns "Weekend"
            """

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
            """
            Checks if the current day is equal to the given value range.
            The range can be defined in multiple ways:
                - as a single value
                - as a range (e.g. 1-5)
                - as a range with a minimum (e.g. 1+)
                - as a range with a maximum (e.g. 5-)
                - as a list of values (e.g. 1,3,5)

            ### Parameters:
            1. value: str | int
                - the value range to check against
                - if value is "x", returns True

            ### Returns:
            1. bool
                - True if the current day is equal to the given value range
            """

            if value == "x":
                return True
                
            return check_in_value(value, self.day)

        def check_month(self, value: str | int) -> bool:
            """
            Checks if the current month is equal to the given value range.
            The range can be defined in multiple ways:
                - as a single value
                - as a range (e.g. 1-5)
                - as a range with a minimum (e.g. 1+)
                - as a range with a maximum (e.g. 5-)
                - as a list of values (e.g. 1,3,5)

            ### Parameters:
            1. value: str | int
                - the value range to check against
                - if value is "x", returns True

            ### Returns:
            1. bool
                - True if the current month is equal to the given value range
            """

            if value == "x":
                return True

            return check_in_value(value, self.month)

        def check_year(self, value: str | int) -> bool:
            """
            Checks if the current year is equal to the given value range.
            The range can be defined in multiple ways:
                - as a single value
                - as a range (e.g. 1-5)
                - as a range with a minimum (e.g. 1+)
                - as a range with a maximum (e.g. 5-)
                - as a list of values (e.g. 1,3,5)

            ### Parameters:
            1. value: str | int
                - the value range to check against
                - if value is "x", returns True

            ### Returns:
            1. bool
                - True if the current year is equal to the given value range
            """

            if value == "x":
                return True

            return check_in_value(value, self.year)

        def check_daytime(self, value: str | int) -> bool:
            """
            Checks if the current time of the day is equal to the given value range.
            The range can be defined in multiple ways:
                - as a single value
                - as a range (e.g. 1-5)
                - as a range with a minimum (e.g. 1+)
                - as a range with a maximum (e.g. 5-)
                - as a list of values (e.g. 1,3,5)

            ### Parameters:
            1. value: str | int
                - the value range to check against
                - if value is "x", returns True
                - if value is "c", returns True if the current time of the day is in class time
                - if value is "f", returns True if the current time of the day is in free time
                - if value is "d", returns True if the current time of the day is in daytime
                - if value is "n", returns True if the current time of the day is in night

            ### Returns:
            1. bool
                - True if the current time of the day is equal to the given value range
            """

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

        def check_week(self, value: str | int) -> bool:
            """
            Checks if the current week is equal to the given value range.
            The range can be defined in multiple ways:
                - as a single value
                - as a range (e.g. 1-5)
                - as a range with a minimum (e.g. 1+)
                - as a range with a maximum (e.g. 5-)
                - as a list of values (e.g. 1,3,5)

            ### Parameters:
            1. value: str | int
                - the value range to check against
                - if value is "x", returns True

            ### Returns:
            1. bool
                - True if the current week is equal to the given value range
            """

            if value == "x":
                return True

            return check_in_value(value, self.get_week())

        def check_weekday(self, value: str | int) -> bool:
            """
            Checks if the current weekday is equal to the given value range.
            The range can be defined in multiple ways:
                - as a single value
                - as a range (e.g. 1-5)
                - as a range with a minimum (e.g. 1+)
                - as a range with a maximum (e.g. 5-)
                - as a list of values (e.g. 1,3,5)

            ### Parameters:
            1. value: str | int
                - the value range to check against
                - if value is "x", returns True
                - if value is "d", returns True if the current weekday is a work day
                - if value is "w", returns True if the current weekday is a weekend

            ### Returns:
            1. bool
                - True if the current weekday is equal to the given value range
            """

            if value == "x":
                return True

            if (value == str(self.get_weekday_num()) or
                (value == 'd' and time.get_weekday_num() < 6) or
                (value == 'w' and time.get_weekday_num() > 5)
            ):
                return True

            return check_in_value(value, self.get_weekday_num())

        def get_month_name(self, month: int = -1) -> str:
            """
            Returns the name of the current month.

            ### Parameters:
            1. month: int | str
                - the month in the year
                - from 1 - 12
                - if month is -1, returns the name of the current month

            ### Returns:
            1. str
                - the name of the current month
            """
            
            if isinstance(month, str):
                if not is_integer(month):
                    return month
                month = int(month)

            if month < 1 or month > 12:
                month = self.month
            month_name = ["January", "February", "March", "April", "May", "June", 
                "July", "August", "September", "October", "November", "December"
            ]
            return month_name[month - 1]

        def get_daytime_name(self, daytime: int = -1) -> str:
            """
            Returns the name of the current time of the day.

            ### Parameters:
            1. daytime: int | str
                - the time of the day
                - 1: Morning
                - 2: Early Noon
                - 3: Noon
                - 4: Early Afternoon
                - 5: Afternoon
                - 6: Evening
                - 7: Night
                - if daytime is -1, returns the name of the current time of the day
                - if daytime is "c", returns "Class Time"
                - if daytime is "f", returns "Free Time"

            ### Returns:
            1. str
                - the name of the current time of the day
            """

            if isinstance(daytime, str):
                if is_integer(daytime):
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
            """
            Returns the current date in the format "day.month.year".

            ### Returns:
            1. str
                - the current date
            """

            return str(self.day) + "." + str(self.month) + "." + str(self.year)

        def now(self) -> str:
            """
            Returns the current date and time in the format "day.month.year.time".

            ### Returns:
            1. str
                - the current date and time
            """

            return self.today() + "." + str(self.daytime)

        def today_is_after_date(self, day: int, month: int, year: int) -> bool:
            """
            Checks if the current date is after the given date.

            ### Parameters:
            1. day: int
                - the day in the month
                - from 1 - 28
            2. month: int
                - the month in the year
                - from 1 - 12
            3. year: int
                - the year

            ### Returns:
            1. bool
                - True if the current date is after the given date
            """

            if self.year > year:
                return True
            if self.month > month:
                return True
            if self.day > day:
                return True
            return False

        def now_is_after_time(self, day: int, month: int, year: int, time: int) -> bool:
            """
            Checks if the current date and time is after the given date and time.

            ### Parameters:
            1. day: int
                - the day in the month
                - from 1 - 28
            2. month: int
                - the month in the year
                - from 1 - 12
            3. year: int
                - the year
            4. time: int
                - the time of the day
                - 1: Morning
                - 2: Early Noon
                - 3: Noon
                - 4: Early Afternoon
                - 5: Afternoon
                - 6: Evening
                - 7: Night
            """

            if self.today_is_after_date(day, month, year):
                return True
            if self.daytime > time:
                return True
            return False





