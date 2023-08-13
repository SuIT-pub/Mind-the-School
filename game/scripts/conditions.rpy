init -6 python:
    import re
    from abc import ABC, abstractmethod
    class Condition(ABC):
        def __init__(self):
            self.blocking = False
            self.display_in_list = False
            self.display_in_desc = False

        @abstractmethod
        def is_fullfilled(self, school):
            pass

        def is_blocking(self, school):
            return (not self.is_fullfilled(school) and self.blocking)

        def is_set_blocking(self):
            return self.blocking

        @abstractmethod
        def to_list_text(self, school):
            pass

        @abstractmethod
        def to_desc_text(self, school):
            pass

        @abstractmethod
        def get_name(self):
            pass

    class StatCondition(Condition):
        def __init__(self, value, stat, school = "x", blocking = False):
            super().__init__()
            self.value = value
            self.stat = stat
            self.school = school
            self.blocking = blocking
            self.display_in_list = True
            self.display_in_desc = True
            
        def is_fullfilled(self, school):
            school_obj = get_character(school, charList["schools"])
            if self.school == school or self.school == "x":
                return school_obj.check_stat(self.stat, self.value)

            return True
        
        def to_list_text(self, school):
            icon = "icons/stat_" + self.stat + "_icon.png"
            if self.is_fullfilled(school):
                return ["{image=" + icon + "}", "{color=#0f0}" + str(self.value) + "{/color}"]
            else:
                return ["{image=" + icon + "}", "{color=#f00}" + str(self.value) + "{/color}"]

        def to_desc_text(self, school):
            if self.is_fullfilled(school):
                return self.get_name() + ": {color=#0f0}" + str(self.value) + "{/color}"
            else:
                return self.get_name() + ": {color=#f00}" + str(self.value) + "{/color}"

        def get_name(self):
            stat_data = get_stat_data(self.stat)
            if stat_data == None:
                return ""
            return stat_data.title

    class RuleCondition(Condition):

        def __init__(self, value, school = "x", blocking = False):
            super().__init__()
            self.value = value
            self.school = school
            self.blocking = blocking
            self.display_in_desc = True

        def is_fullfilled(self, school):
            if self.school == school or self.school == "x":
                return is_rule_unlocked(self.value, school)
            return True

        def to_list_text(self, _school):
            return ["", ""]

        def to_desc_text(self, school):
            if self.is_fullfilled(school):
                return "{color=#0f0}" + get_rule(self.value).get_title() + "{/color} is unlocked"
            else:
                return "{color=#f00}" + get_rule(self.value).get_title() + "{/color} is unlocked"

        def get_name(self):
            if self.value not in rules.keys():
                return ""
            return get_rule(self.value).title

    class ClubCondition(Condition):

        def __init__(self, value, school = "x", blocking = False):
            super().__init__()
            self.value = value
            self.school = school
            self.blocking = blocking
            self.display_in_desc = True

        def is_fullfilled(self, school):
            if self.school == school or self.school == "x":
                return get_club(self.value).is_unlocked(school)
            return True

        def to_list_text(self, _school):
            return ["", ""]

        def to_desc_text(self, school):
            if self.is_fullfilled(school):
                return "{color=#0f0}" + get_club(self.value).get_title() + "{/color} is unlocked"
            else:
                return "{color=#f00}" + get_club(self.value).get_title() + "{/color} is unlocked"

        def get_name(self):
            if self.value not in clubs.keys():
                return ""
            return get_club(self.value).title

    class BuildingCondition(Condition):

        def __init__(self, value, blocking = False):
            super().__init__()
            self.value = value
            self.blocking = blocking
            self.display_in_desc = True

        def is_fullfilled(self, _school):
            return get_building(self.value).is_building_unlocked(self.value)

        def to_list_text(self, _school):
            return ["", ""]

        def to_desc_text(self, school):
            if self.is_fullfilled(school):
                return "{color=#0f0}" + get_building(self.value).get_title() + "{/color} is unlocked"
            else:
                return "{color=#f00}" + get_building(self.value).get_title() + "{/color} is unlocked"

        def get_name(self):
            if self.value not in buildings.keys():
                return ""
            return get_building(self.value).title

    class LevelCondition(Condition):

        def __init__(self, value, school = "x", blocking = False):
            super().__init__()
            self.value = value
            self.school = school
            self.blocking = blocking
            self.display_in_list = True
            self.display_in_desc = True

        def is_fullfilled(self, school):

            school_obj = get_character(school, charList["schools"])
            self_school_obj = get_character(self.school, charList["schools"])

            if school != "x" and (self.school == school or self.school == "x"):
                return school_obj.check_level(self.value)

            if self.school != "x" and (self.school == school or school == "x"):
                return self_school_obj.check_level(self.value)

            return True

        def to_desc_text(self, school):
            if self.is_fullfilled(school):
                return "Level: {color=#0f0}" + self.value + "{/color}"
            else:
                return "Level: {color=#f00}" + self.value + "{/color}"

        def to_list_text(self, school):
            if self.is_fullfilled(school):
                return ["{image=icons/stat_level_icon.png}", "{color=#0f0}" + str(self.value) + "{/color}"]
            else:
                return ["{image=icons/stat_level_icon.png}", "{color=#f00}" + str(self.value) + "{/color}"]

        def get_name(self):
            return "Level"

    class MoneyCondition(Condition):

        def __init__(self, value, blocking = False):
            super().__init__()
            self.value = value
            self.blocking = blocking
            self.display_in_list = True
            self.display_in_desc = True

        def is_fullfilled(self, _school):
            return money.get_value() >= self.value

        def to_desc_text(self, school):
            if self.is_fullfilled(school):
                return "Money: {color=#0f0}" + str(self.value) + "{/color}"
            else:
                return "Money: {color=#f00}" + str(self.value) + "{/color}"

        def to_list_text(self, school):
            if self.is_fullfilled(school):
                return ["{image=icons/stat_money_icon.png}", "{color=#0f0}" + str(self.value) + "{/color}"]
            else:
                return ["{image=icons/stat_money_icon.png}", "{color=#f00}" + str(self.value) + "{/color}"]

        def get_name(self):
            return "Money"

    class SchoolCondition(Condition):

        def __init__(self, school = "x", blocking = True):
            super().__init__()
            self.school = school
            self.blocking = blocking

        def is_fullfilled(self, school):
            return self.school == school or self.school == "x"

        def to_list_text(self, _school):
            return ["", ""]

        def to_desc_text(self, _school):
            return ""

        def get_name(self):
            if self.school not in schools.keys():
                return self.school
            return get_character(school, charList["schools"]).get_title()

    class LockCondition(Condition):

        def __init__(self):
            super().__init__()
            self.blocking = True

        def is_fullfilled(self, _school):
            return False

        def to_desc_text(self, _school):
            return ""

        def to_list_text(self, _school):
            return ["", ""]

        def get_name(self):
            return "lock"

    class TimeCondition(Condition):

        def __init__(self, blocking = True, **kwargs):
            super().__init__()
            self.day     = "x" if 'day'     not in kwargs.keys() else kwargs['day'    ]
            self.week    = "x" if 'week'    not in kwargs.keys() else kwargs['week'   ]
            self.month   = "x" if 'month'   not in kwargs.keys() else kwargs['month'  ]
            self.year    = "x" if 'year'    not in kwargs.keys() else kwargs['year'   ]
            self.daytime = "x" if 'daytime' not in kwargs.keys() else kwargs['daytime']
            self.weekday = "x" if 'weekday' not in kwargs.keys() else kwargs['weekday']
            self.blocking = blocking
            self.display_in_desc = True

        def is_fullfilled(self, _school):
            return (
                time.check_day    (self.day    ) and
                time.check_month  (self.month  ) and
                time.check_year   (self.year   ) and
                time.check_week   (self.week   ) and
                time.check_daytime(self.daytime) and
                time.check_weekday(self.weekday))

        def to_list_text(self, _school):
            return ["", ""]

        def to_desc_text(self, _school):
            text = ""

            if ((self.day != "x" or self.week != "x" or self.weekday != "x") or
                self.month != "x" or self.year != "x"
            ):
                if self.day != "x":
                    text = f"{self.day}."
                elif self.week != "x":
                    if self.week.isdigit():
                        text = f"{(int(self.week) - 1) * 7 + 1}.-{(int(self.week) - 1) * 7 + 7}."
                    else:
                        text = f"Week:{self.week}"
                elif self.weekday != "x":
                    text = f"{time.get_weekday(self.weekday)}"
                else:
                    text = f"\"{time.get_day()}\""

                if self.month != "x":
                    text += f" {time.get_month_name(self.month)}"
                elif self.day != "x" or self.week != "x":
                    text += f" \"{time.get_month_name()}\""

                if self.year != "x":
                    text += f" {self.year}"


            if self.daytime != "x":
                if text != "":
                    text = " "
                text += f"{time.get_daytime_name(self.daytime)}"

            if self.is_fullfilled(school):
                return "Time is {color=#0f0}" + text + "{/color}"
            else:
                return "Time is {color=#f00}" + text + "{/color}"

        def get_name(self):
            return f"{self.day}:{self.week}:{self.month}:{self.year}:{self.daytime}:{self.weekday}"
            
    class RandomCondition(Condition):

        def __init__(self, amount, limit, blocking = False):
            super().__init__()
            self.amount = amount
            self.limit  = limit
            self.blocking = blocking
            self.display_in_desc = True
            self.display_in_list = True

        def is_fullfilled(self, _school):
            return random.randInt(0, self.limit) < self.amount

        def to_desc_text(self, _school):
            return f"Chance: {str(100 / self.limit * self.amount)}%"

        def to_list_text(self, _school):
            return ["", f"{str(100 / self.limit * self.amount)}%"]

        def get_name(self):
            return f"Random ({self.amount}/{self.limit})"