init python:
    import re
    class Time:
        def __init__(self):
            self.daytime = 0
            self.day = 1
            self.month = 1
            self.year = 2023

        def progress_time(self):
            self.daytime += 1

            if self.daytime == 8:
                game_daytime = 1
                game_day += 1
                if game_day >= 29:
                    game_day = 1
                    game_month += 1
                    if game_month >= 13:
                        game_month = 1
                        game_year += 1

        def get_daytime(self):
            return self.daytime

        def get_day(self):
            return self.day

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
            if day == -1:
                day = self.day
            weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            
            return weekday[self.get_weekday_num() - 1]

        def get_month_name(self, month = -1):
            if month == -1:
                month = self.month
            month_name = ["January", "February", "March", "April", "May", "June", 
                "July", "August", "September", "October", "November", "December"
            ]
            return month_name[month]

        def get_daytime_name(self, daytime = -1):
            if daytime == -1:
                daytime = self.daytime
            daytime_name = ["Morning", "Early Noon", "Noon", "Early Afternoon", "Afternoon", "Evening", "Night"]
            return daytime_name[daytime]

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





