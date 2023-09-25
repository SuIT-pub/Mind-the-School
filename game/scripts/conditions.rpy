init -6 python:
    import re
    from abc import ABC, abstractmethod

    class ConditionStorage:
        def __init__(self, *conditions):
            self.conditions = list(conditions)
            self.list_conditions = []
            self.desc_conditions = []

            for condition in self.conditions:
                if condition.display_in_list:
                    self.list_conditions.append(condition)
                if condition.display_in_desc:
                    self.desc_conditions.append(condition)

        def get_list_conditions(self):
            return self.list_conditions

        def get_desc_conditions(self):
            return self.desc_conditions

        def get_desc_conditions_desc(self, **kwargs):
            blocking = False
            if 'blocking' in kwargs.keys() and kwargs['blocking']:
                blocking = True
            output = []
            print("blocking: " + str(blocking))
            for condition in self.desc_conditions:
                print("condition: " + condition.get_name())
                if not blocking or not condition.blocking:
                    output.append(condition.to_desc_text(**kwargs))
            return output

        def get_conditions(self):
            return self.conditions

        def is_fullfilled(self, **kwargs):
            for condition in self.conditions:
                if condition.is_fullfilled(**kwargs):
                    continue
                return False

            return True

        def is_blocking(self, **kwargs):
            for condition in self.conditions:
                if condition.is_blocking(**kwargs):
                    return False
            return True

    class Condition(ABC):
        def __init__(self):
            self.blocking = False
            self.display_in_list = False
            self.display_in_desc = False

        @abstractmethod
        def is_fullfilled(self, **kwargs):
            pass

        def is_blocking(self, **kwargs):
            return (not self.is_fullfilled(**kwargs) and self.blocking)

        def is_set_blocking(self):
            return self.blocking

        @abstractmethod
        def to_list_text(self, **kwargs):
            pass

        @abstractmethod
        def to_desc_text(self, **kwargs):
            pass

        @abstractmethod
        def get_name(self):
            pass

        @abstractmethod
        def get_diff(self, char_obj):
            pass

    class StatCondition(Condition):
        def __init__(self, value, stat, blocking = False):
            super().__init__()
            self.value = value
            self.stat = stat
            self.blocking = blocking
            self.display_in_list = True
            self.display_in_desc = True
            
        def is_fullfilled(self, **kwargs):
            char_obj = get_kwargs('char_obj', **kwargs)
            if char_obj == None:
                return False

            return char_obj.check_stat(self.stat, self.value)
        
        def to_list_text(self, **kwargs):
            icon = "icons/stat_" + self.stat + "_icon.png"
            if self.is_fullfilled(**kwargs):
                return ["{image=" + icon + "}", "{color=#0f0}" + str(self.value) + "{/color}"]
            else:
                return ["{image=" + icon + "}", "{color=#f00}" + str(self.value) + "{/color}"]

        def to_desc_text(self, **kwargs):
            if self.is_fullfilled(**kwargs):
                return self.get_name() + ": {color=#0f0}" + str(self.value) + "{/color}"
            else:
                return self.get_name() + ": {color=#f00}" + str(self.value) + "{/color}"

        def get_name(self):
            stat_data = get_stat_data(self.stat)
            if stat_data == None:
                return ""
            return stat_data.title

        def get_diff(self, char_obj):
            obj_stat = char_obj.get_stat_number(self.stat)
            print("stat:")
            diff = get_value_diff(self.value, obj_stat)

            if diff < -20:
                return diff * 10
            elif diff < -10:
                return diff * 5
            elif diff < -5:
                return diff * 2
            return diff

    class RuleCondition(Condition):
        def __init__(self, value, school = "x", blocking = False):
            super().__init__()
            self.value = value
            self.school = school
            self.blocking = blocking
            self.display_in_desc = True

        def is_fullfilled(self, **kwargs):
            char_obj = get_kwargs('char_obj', **kwargs)
            if char_obj == None:
                return False

            return get_rule(self.value).is_unlocked(char_obj.get_name())

        def to_list_text(self, **kwargs):
            return ["", ""]

        def to_desc_text(self, **kwargs):
            if self.is_fullfilled(**kwargs):
                return "{color=#0f0}" + get_rule(self.value).get_title() + "{/color} is unlocked"
            else:
                return "{color=#f00}" + get_rule(self.value).get_title() + "{/color} is unlocked"

        def get_name(self):
            if self.value not in rules.keys():
                return ""
            return get_rule(self.value).get_title()

        def get_diff(self, char_obj):
            if self.is_fullfilled(char_obj = char_obj):
                return 0
            return -100

    class ClubCondition(Condition):
        def __init__(self, value, blocking = False):
            super().__init__()
            self.value = value
            self.blocking = blocking
            self.display_in_desc = True

        def is_fullfilled(self, **kwargs):
            char_obj = get_kwargs('char_obj', **kwargs)
            if char_obj == None:
                return False

            return get_club(self.value).is_unlocked(char_obj.get_name())

        def to_list_text(self, **kwargs):
            return ["", ""]

        def to_desc_text(self, **kwargs):
            if self.is_fullfilled(**kwargs):
                return "{color=#0f0}" + get_club(self.value).get_title() + "{/color} is unlocked"
            else:
                return "{color=#f00}" + get_club(self.value).get_title() + "{/color} is unlocked"

        def get_name(self):
            if self.value not in clubs.keys():
                return ""
            return get_club(self.value).title

        def get_diff(self, char_obj):
            if self.is_fullfilled(char_obj.get_name()):
                return 0
            return -100

    class BuildingCondition(Condition):
        def __init__(self, value, blocking = False):
            super().__init__()
            self.value = value
            self.blocking = blocking
            self.display_in_desc = True

        def is_fullfilled(self, **kwargs):
            return get_building(self.value).is_building_unlocked(self.value)

        def to_list_text(self, **kwargs):
            return ["", ""]

        def to_desc_text(self, **kwargs):
            if self.is_fullfilled(**kwargs):
                return "{color=#0f0}" + get_building(self.value).get_title() + "{/color} is unlocked"
            else:
                return "{color=#f00}" + get_building(self.value).get_title() + "{/color} is unlocked"

        def get_name(self):
            if self.value not in buildings.keys():
                return ""
            return get_building(self.value).title

        def get_diff(self, char_obj):
            if self.is_fullfilled(char_obj.get_name()):
                return 0
            return -100

    class LevelCondition(Condition):
        def __init__(self, value, blocking = False):
            super().__init__()
            self.value = value
            self.blocking = blocking
            self.display_in_list = True
            self.display_in_desc = True

        def is_fullfilled(self, **kwargs):
            char_obj = get_kwargs('char_obj', **kwargs)
            if char_obj == None:
                return False

            return char_obj.check_level(self.value)

        def to_desc_text(self, **kwargs):
            if self.is_fullfilled(**kwargs):
                return "Level: {color=#0f0}" + self.value + "{/color}"
            else:
                return "Level: {color=#f00}" + self.value + "{/color}"

        def to_list_text(self, **kwargs):
            if self.is_fullfilled(**kwargs):
                return ["{image=icons/stat_level_icon.png}", "{color=#0f0}" + str(self.value) + "{/color}"]
            else:
                return ["{image=icons/stat_level_icon.png}", "{color=#f00}" + str(self.value) + "{/color}"]

        def get_name(self):
            return "Level"

        def get_diff(self, char_obj):
            # return char_obj.get_nearest_level_delta(self.value) * 20

            obj_level = char_obj.get_level()
            print("level:")
            diff = get_value_diff(self.value, obj_level)

            if diff < -2:
                return diff * 50
            elif diff < -1:
                return diff * 20
            return diff

    class MoneyCondition(Condition):
        def __init__(self, value, blocking = False):
            super().__init__()
            self.value = value
            self.blocking = blocking
            self.display_in_list = True
            self.display_in_desc = True

        def is_fullfilled(self, **kwargs):
            return money.get_value() >= self.value

        def to_desc_text(self, **kwargs):
            if self.is_fullfilled():
                return "Money: {color=#0f0}" + str(self.value) + "{/color}"
            else:
                return "Money: {color=#f00}" + str(self.value) + "{/color}"

        def to_list_text(self, **kwargs):
            if self.is_fullfilled():
                return ["{image=icons/stat_money_icon.png}", "{color=#0f0}" + str(self.value) + "{/color}"]
            else:
                return ["{image=icons/stat_money_icon.png}", "{color=#f00}" + str(self.value) + "{/color}"]

        def get_name(self):
            return "Money"

        def get_diff(self, char_obj):
            output = -20 + (money.get_value() - self.value)
            if output > 0:
                return 0
            return output


    class SchoolCondition(Condition):
        def __init__(self, school = "x", blocking = True):
            super().__init__()
            self.school = school
            self.blocking = blocking

        def is_fullfilled(self, **kwargs):
            return 'school' in kwargs.keys() and (self.school == kwargs['school'] or self.school == "x")

        def to_list_text(self, **kwargs):
            return ["", ""]

        def to_desc_text(self, **kwargs):
            return ""

        def get_name(self):
            if self.school not in schools.keys():
                return self.school
            return get_character(school, charList["schools"]).get_title()

        def get_diff(self, char_obj):
            if char_obj.name == self.school:
                return 0
            return -100


    class LockCondition(Condition):
        def __init__(self):
            super().__init__()
            self.blocking = True

        def is_fullfilled(self, **kwargs):
            return False

        def to_desc_text(self, **kwargs):
            return ""

        def to_list_text(self, **kwargs):
            return ["", ""]

        def get_name(self):
            return "lock"

        def get_diff(self, char_obj):
            return -100


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

        def is_fullfilled(self, **kwargs):
            return (
                time.check_day    (self.day    ) and
                time.check_month  (self.month  ) and
                time.check_year   (self.year   ) and
                time.check_week   (self.week   ) and
                time.check_daytime(self.daytime) and
                time.check_weekday(self.weekday))

        def to_list_text(self, **kwargs):
            return ["", ""]

        def to_desc_text(self, **kwargs):
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

            if self.is_fullfilled(school = school):
                return "Time is {color=#0f0}" + text + "{/color}"
            else:
                return "Time is {color=#f00}" + text + "{/color}"

        def get_name(self):
            return f"{self.day}:{self.week}:{self.month}:{self.year}:{self.daytime}:{self.weekday}"

        def get_diff(self, char_obj):
            if self.is_fullfilled(None):
                return 0
            return -100
            

    class RandomCondition(Condition):
        def __init__(self, amount, limit, blocking = False):
            super().__init__()
            self.amount = amount
            self.limit  = limit
            self.blocking = blocking
            self.display_in_desc = True
            self.display_in_list = True

        def is_fullfilled(self, **kwargs):
            return random.randInt(0, self.limit) < self.amount

        def to_desc_text(self, **kwargs):
            return f"Chance: {str(100 / self.limit * self.amount)}%"

        def to_list_text(self, **kwargs):
            return ["", f"{str(100 / self.limit * self.amount)}%"]

        def get_name(self):
            return f"Random ({self.amount}/{self.limit})"

        def get_diff(self, char_obj):
            return 0


    class GameDataCondition(Condition):
        def __init__(self, name, key, value, blocking = False):
            super().__init__()
            self.name = name
            self.key = key
            self.value = value
            self.blocking = blocking
            self.display_in_desc = True
            self.display_in_list = False

        def is_fullfilled(self, **kwargs):
            if self.key not in gameData.keys():
                return False
            return gameData[self.key] == self.value

        def to_desc_text(self, **kwargs):
            if self.is_fullfilled():
                return self.name + " is {color=#0f0}" + self.value + "{/color}"
            else:
                return self.name + " is {color=#f00}" + self.value + "{/color}"

        def to_list_text(self, **kwargs):
            return ["", ""]

        def get_name(self):
            return self.name

        def get_diff(self, char_obj):
            if aelf.is_fullfilled():
                return 0
            return -100

    class ValueCondition(Condition):
        def __init__(self, key, value, blocking = False):
            super().__init__()
            self.key = key
            self.value = value
            self.blocking = blocking
            self.display_in_desc = True
            self.display_in_list = False

        def is_fullfilled(self, **kwargs):
            if self.key not in kwargs.keys():
                return False
            return kwargs[self.key] == self.value

        def to_desc_text(self, **kwargs):
            if self.is_fullfilled():
                return self.key + " is {color=#0f0}" + self.value + "{/color}"
            else:
                return self.key + " is {color=#f00}" + self.value + "{/color}"

        def to_list_text(self, **kwargs):
            return ["", ""]

        def get_name(self):
            return self.key

        def get_diff(self, char_obj):
            if self.is_fullfilled():
                return 0
            return -100

    class NumValueCondition(Condition):
        def __init__(self, key, value, blocking = False):
            super().__init__()
            self.key = key
            self.value = value
            self.blocking = blocking
            self.display_in_desc = True
            self.display_in_list = False

        def is_fullfilled(self, **kwargs):
            if self.key not in kwargs.keys():
                return False
            return get_value_diff(self.value, kwargs[self.key]) >= 0

        def to_desc_text(self, **kwargs):
            if self.is_fullfilled():
                return self.key + " is {color=#0f0}" + self.value + "{/color}"
            else:
                return self.key + " is {color=#f00}" + self.value + "{/color}"

        def to_list_text(self, **kwargs):
            return ["", ""]

        def get_name(self):
            return self.key

        def get_diff(self, char_obj):
            if self.is_fullfilled():
                return 0
            return -100