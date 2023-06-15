init python:
    import re
    from abc import ABC, abstractmethod
    class Condition(ABC):
        blocking = False

        @abstractmethod
        def is_fullfilled(self, school):
            pass

        def is_blocking(self, school):
            return (not self.is_fullfilled(school) and self.is_blocking)

        def is_set_blocking(self):
            return self.blocking

        @abstractmethod
        def to_text(self, school):
            pass

        @abstractmethod
        def get_name(self):
            pass

    class StatCondition(Condition):

        def __init__(self, value, stat, school = "x", blocking = False):
            self.value = value
            self.stat = stat
            self.school = school
            self.blocking = blocking
            
        def is_fullfilled(self, school):
            if self.school == school or self.school == "x":
                needed_stat = get_stat(self.value, self.stat, school)

                print(self.stat + ": " + needed_stat + " current: " + get_school(school).get_stat_string(self.stat))

                return needed_stat == get_school(school).get_stat_string(self.stat)

            return True
        
        def to_text(self, school):
            icon = "icons/stat_" + self.stat + "_icon.png"
            if self.is_fullfilled(school):
                return ["{image=" + icon + "}", " {color=#0f0}" + self.value + "{/color}"]
            else:
                return ["{image=" + icon + "}", " {color=#f00}" + self.value + "{/color}"]

        def get_name(self):
            stat_data = get_stat_data(self.stat)
            if stat_data == None:
                return ""
            return stat_data.title

    class RuleCondition(Condition):

        def __init__(self, value, school = "x", blocking = False):
            self.value = value
            self.school = school
            self.blocking = blocking

        def is_fullfilled(self, school):
            if self.school == school or self.school == "x":
                return is_rule_unlocked(self.value, school)
            return True

        def to_text(self, school):
            if self.is_fullfilled(school):
                return ["", "{color=#0f0}" + self.value + "{/color}"]
            else:
                return ["", "{color=#f00}" + self.value + "{/color}"]

        def get_name(self):
            if self.value not in rules.keys():
                return ""
            return get_rule(self.value).title

    class ClubCondition(Condition):

        def __init__(self, value, school = "x", blocking = False):
            self.value = value
            self.school = school
            self.blocking = blocking

        def is_fullfilled(self, school):
            if self.school == school or self.school == "x":
                return get_club(self.value).is_nlocked(school)
            return True

        def to_text(self, school):
            if self.is_fullfilled(school):
                return ["", "{color=#0f0}" + self.value + "{/color}"]
            else:
                return ["", "{color=#f00}" + self.value + "{/color}"]

        def get_name(self):
            if self.value not in clubs.keys():
                return ""
            return get_club(self.value).title

    class BuildingCondition(Condition):

        def __init__(self, value, blocking = False):
            self.value = value
            self.blocking = blocking

        def is_fullfilled(self, _school):
            return get_building(self.value).is_building_unlocked(self.value)

        def to_text(self, _school):
            if self.is_fullfilled(None):
                return ["", "{color=#0f0}" + self.value + "{/color}"]
            else:
                return ["", "{color=#f00}" + self.value + "{/color}"]

        def get_name(self):
            if self.value not in buildings.keys():
                return ""
            return get_building(self.value).title

    class LevelCondition(Condition):

        def __init__(self, value, school = "x", blocking = False):
            self.value = value
            self.school = school
            self.blocking = blocking

        def is_fullfilled(self, school):
            if self.school == school or self.school == "x":
                level = get_level(self.value, school)

                print("level: " + level + " current: " + level_to_string(school))

                return level == level_to_string(school)

        def to_text(self, school):
            if self.is_fullfilled(school):
                return ["{image=icons/stat_level_icon.png}", " {color=#0f0}" + self.value + "{/color}"]
            else:
                return ["{image=icons/stat_level_icon.png}", " {color=#f00}" + self.value + "{/color}"]

        def get_name(self):
            return "Level"

    class MoneyCondition(Condition):

        def __init__(self, value, blocking = False):
            self.value = value
            self.blocking = blocking

        def is_fullfilled(self, _school):
            return money.get_value() >= self.value

        def to_text(self, school):
            if self.is_fullfilled(school):
                return ["{image=icons/stat_money_icon.png}", " {color=#0f0}" + str(self.value) + "{/color}"]
            else:
                return ["{image=icons/stat_money_icon.png}", " {color=#f00}" + str(self.value) + "{/color}"]

        def get_name(self):
            return "Money"

    class SchoolCondition(Condition):

        def __init__(self, school = "x", blocking = False):
            self.school = school
            self.blocking = blocking

        def is_fullfilled(self, school):
            return self.school == school or self.school == "x"

        def to_text(self, school):
            if self.is_fullfilled(school):
                return ["", "{color=#0f0}" + self.school + "{/color}"]
            else:
                return ["", "{color=#f00}" + self.school + "{/color}"]

        def get_name(self):
            if self.school not in schools.keys():
                return self.school
            return get_school(school).title

    class LockCondition(Condition):

        def __init__(self):
            self.blocking = True

        def is_fullfilled(self, _school):
            return False

        def to_text(self, _school):
            return ["", "{color=#f00}LOCKED{/color}"]

        def get_name(self):
            return "lock"


        