init -6 python:
    import re
    from abc import ABC, abstractmethod
    from typing import Union, List

    def get_logic_condition_desc_text(is_fulfilled: bool, conditions: List[Condition], key: str, **kwargs):
        prefix = get_kwargs('prefix', "", **kwargs)

        if is_fulfilled:
            prefix += "{color=#0f0}|{/color} "
        else:
            prefix += "{color=#f00}|{/color} "

        kwargs['prefix'] = prefix

        desc_list = []

        for condition in conditions:
            desc_text = condition.to_desc_text(**kwargs)
            add_prefix = ""

            if (not isinstance(condition, AND) and 
                not isinstance(condition, OR) and 
                not isinstance(condition, XOR) and 
                not isinstance(condition, NOR)
            ):
                add_prefix = prefix

            if isinstance(desc_text, str):
                desc_list.append(add_prefix + desc_text)
            else:
                desc_list.extend([add_prefix + desc for desc in desc_text])
            
        return ("\n" + prefix + "   {color=#616161}" + key + "{/color}\n").join(desc_list)

    class ConditionStorage:
        def __init__(self, *conditions: Condition):
            self.conditions = list(conditions)
            self.list_conditions = []
            self.desc_conditions = []
            self.is_locked = False

            for condition in self.conditions:
                if isinstance(condition, LockCondition):
                    self.is_locked = True
                if condition.display_in_list:
                    self.list_conditions.append(condition)
                if condition.display_in_desc:
                    self.desc_conditions.append(condition)

        def get_is_locked(self):
            return self.is_locked

        def get_list_conditions(self):
            return self.list_conditions

        def get_desc_conditions(self):
            return self.desc_conditions

        def get_desc_conditions_desc(self, **kwargs):
            blocking = False
            if 'blocking' in kwargs.keys() and kwargs['blocking']:
                blocking = True

            output = []
            for condition in self.desc_conditions:
                if not blocking or not condition.blocking:
                    desc_text = condition.to_desc_text(**kwargs)
                    if isinstance(desc_text, list):
                        output.extend(desc_text)
                    else:
                        output.append(desc_text)

            return output

        def get_list_conditions_list(self, **kwargs):
            blocking = False
            if 'blocking' in kwargs.keys() and kwargs['blocking']:
                blocking = True

            output = []
            for condition in self.list_conditions:
                if not blocking or not condition.blocking:
                    desc_text = condition.to_list_text(**kwargs)
                    if isinstance(desc_text, list):
                        output.extend(desc_text)
                    else:
                        output.append(desc_text)

            return output

        def get_conditions(self):
            return self.conditions

        def is_fulfilled(self, **kwargs):
            for condition in self.conditions:
                if condition.is_fulfilled(**kwargs):
                    continue
                return False

            return True

        def is_blocking(self, **kwargs):
            for condition in self.conditions:
                if condition.is_blocking(**kwargs):
                    return False
            return True

    class Condition(ABC):
        def __init__(self, blocking: bool = False):
            self.blocking = blocking
            self.display_in_list = False
            self.display_in_desc = False

        @abstractmethod
        def is_fulfilled(self, **kwargs):
            pass

        def is_blocking(self, **kwargs):
            return (not self.is_fulfilled(**kwargs) and self.blocking)

        def is_set_blocking(self):
            return self.blocking

        def to_list_text(self, **kwargs):
            return ("", "")

        def to_desc_text(self, **kwargs):
            return ""

        @abstractmethod
        def get_name(self):
            pass

        @abstractmethod
        def get_diff(self, char_obj: Char):
            pass

    class StatCondition(Condition):
        def __init__(self, blocking: bool = False, **kwargs):
            super().__init__(blocking)
            self.stats = kwargs
            self.display_in_list = True
            self.display_in_desc = True
            
        def is_fulfilled(self, **kwargs):
            char_obj = get_kwargs('char_obj', **kwargs)
            if char_obj == None:
                return False

            for stat in self.stats.keys():
                if not char_obj.check_stat(stat, self.stats[stat]):
                    return False

            return True
        
        def to_list_text(self, **kwargs):            
            char_obj = get_kwargs('char_obj', **kwargs)
            if char_obj == None:
                return ("","")

            output = []
            for stat in self.stats.keys():
                icon = "icons/stat_" + str(stat) + "_icon.png"
                if char_obj.check_stat(stat, self.stats[stat]):
                    output.append(("{image=" + icon + "}", "{color=#0f0}" + str(self.stats[stat]) + "{/color}", Stat_Data[stat].get_title()))
                else:
                    output.append(("{image=" + icon + "}", "{color=#f00}" + str(self.stats[stat]) + "{/color}", Stat_Data[stat].get_title()))
            if len(output) == 0:
                return ("","")
            elif len(output) == 1:
                return output[0]
            else:
                return output

        def to_desc_text(self, **kwargs):
            char_obj = get_kwargs('char_obj', **kwargs)
            if char_obj == None:
                return ""

            output = []
            for stat in self.stats.keys():
                stat_name = Stat_Data[stat].get_title()

                if char_obj.check_stat(stat, self.stats[stat]):
                    output.append(stat_name + ": {color=#0f0}" + str(self.stats[stat]) + "{/color}")
                else:
                    output.append(stat_name + ": {color=#f00}" + str(self.stats[stat]) + "{/color}")

            if len(output) == 0:
                return ""
            elif len(output) == 1:
                return output[0]
            else:
                return output

        def get_name(self):
            return ', '.join([Stat_Data[key].get_title() for key in self.stats.keys()])

        def get_diff(self, char_obj: Char):
            output = 0
            for stat in self.stats.keys():
                obj_stat = char_obj.get_stat_number(stat)
                diff = get_value_diff(self.stats[stat], obj_stat)

                if diff < -20:
                    output += diff * 10
                elif diff < -10:
                    output += diff * 5
                elif diff < -5:
                    output += diff * 2
                else:
                    output += diff
            return output

    class RuleCondition(Condition):
        def __init__(self, value: str, blocking: bool = False):
            super().__init__(blocking)
            self.value = value
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs):
            char_obj = get_kwargs('char_obj', **kwargs)
            if char_obj == None:
                return False

            return get_rule(self.value).is_unlocked(char_obj.get_name())

        def to_list_text(self, **kwargs):
            return ("", "", "")

        def to_desc_text(self, **kwargs):
            if self.is_fulfilled(**kwargs):
                return "Rule {color=#0f0}" + get_rule(self.value).get_title() + "{/color} is unlocked"
            else:
                return "Rule {color=#f00}" + get_rule(self.value).get_title() + "{/color} is unlocked"

        def get_name(self):
            if self.value not in rules.keys():
                return ""
            return get_rule(self.value).get_title()

        def get_diff(self, char_obj: Char):
            if self.is_fulfilled(char_obj = char_obj):
                return 0
            return -100

    class ClubCondition(Condition):
        def __init__(self, value: str, blocking: bool = False):
            super().__init__(blocking)
            self.value = value
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs):
            char_obj = get_kwargs('char_obj', **kwargs)
            if char_obj == None:
                return False

            return get_club(self.value).is_unlocked(char_obj.get_name())

        def to_list_text(self, **kwargs):
            return ("", "", "")

        def to_desc_text(self, **kwargs):
            if self.is_fulfilled(**kwargs):
                return "Club {color=#0f0}" + get_club(self.value).get_title() + "{/color} is unlocked"
            else:
                return "Club {color=#f00}" + get_club(self.value).get_title() + "{/color} is unlocked"

        def get_name(self):
            if self.value not in clubs.keys():
                return ""
            return get_club(self.value).title

        def get_diff(self, char_obj: Char):
            if self.is_fulfilled(char_obj.get_name()):
                return 0
            return -100

    class BuildingCondition(Condition):
        def __init__(self, value: str, blocking: bool = False):
            super().__init__(blocking)
            self.value = value
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs):
            return get_building(self.value).is_building_unlocked(self.value)

        def to_list_text(self, **kwargs):
            return ("", "", "")

        def to_desc_text(self, **kwargs):
            if self.is_fulfilled(**kwargs):
                return "Building {color=#0f0}" + get_building(self.value).get_title() + "{/color} is unlocked"
            else:
                return "Building {color=#f00}" + get_building(self.value).get_title() + "{/color} is unlocked"

        def get_name(self):
            if self.value not in buildings.keys():
                return ""
            return get_building(self.value).title

        def get_diff(self, char_obj: Char):
            if self.is_fulfilled(char_obj.get_name()):
                return 0
            return -100

    class LevelCondition(Condition):
        def __init__(self, value: int, blocking: bool = False):
            super().__init__(blocking)
            self.value = value
            self.display_in_list = True
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs):
            char_obj = get_kwargs('char_obj', **kwargs)
            if char_obj == None:
                return False

            return char_obj.check_level(self.value)

        def to_desc_text(self, **kwargs):
            if self.is_fulfilled(**kwargs):
                return "Level: {color=#0f0}" + self.value + "{/color}"
            else:
                return "Level: {color=#f00}" + self.value + "{/color}"

        def to_list_text(self, **kwargs):
            if self.is_fulfilled(**kwargs):
                return ("{image=icons/stat_level_icon.png}", "{color=#0f0}" + str(self.value) + "{/color}", "Level")
            else:
                return ("{image=icons/stat_level_icon.png}", "{color=#f00}" + str(self.value) + "{/color}", "Level")

        def get_name(self):
            return "Level"

        def get_diff(self, char_obj: Char):
            # return char_obj.get_nearest_level_delta(self.value) * 20

            obj_level = char_obj.get_level()
            diff = get_value_diff(self.value, obj_level)

            if diff < -2:
                return diff * 50
            elif diff < -1:
                return diff * 20
            return diff

    class MoneyCondition(Condition):
        def __init__(self, value: num, blocking = False):
            super().__init__(blocking)
            self.value = value
            self.display_in_list = True
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs):
            return money.get_value() >= self.value

        def to_desc_text(self, **kwargs):
            if self.is_fulfilled():
                return "Money: {color=#0f0}" + str(self.value) + "{/color}"
            else:
                return "Money: {color=#f00}" + str(self.value) + "{/color}"

        def to_list_text(self, **kwargs):
            if self.is_fulfilled():
                return ("{image=icons/stat_money_icon.png}", "{color=#0f0}" + str(self.value) + "{/color}", "Money")
            else:
                return ("{image=icons/stat_money_icon.png}", "{color=#f00}" + str(self.value) + "{/color}", "Money")

        def get_name(self):
            return "Money"

        def get_diff(self, _char_obj):
            output = -20 + (money.get_value() - self.value)
            if output > 0:
                return 0
            return output

    class SchoolCondition(Condition):
        def __init__(self, school: str = "x", blocking: bool = True):
            super().__init__(blocking)
            self.school = school

        def is_fulfilled(self, **kwargs):
            char_obj = get_kwargs('char_obj', **kwargs)
            if char_obj == None:
                return False
            return self.school == "x" or char_obj.get_name() == self.school

        def to_list_text(self, **kwargs):
            return ("", "", "")

        def to_desc_text(self, **kwargs):
            return ""

        def get_name(self):
            char_obj = get_character(school, charList["schools"])
            if char_obj == None:
                return self.school
            return char_obj.get_title()

        def get_diff(self, char_obj: Char):
            if char_obj.name == self.school:
                return 0
            return -100

    class LockCondition(Condition):
        def __init__(self, is_blocking: bool = True):
            super().__init__(is_blocking)

        def is_fulfilled(self, **kwargs):
            return False

        def to_desc_text(self, **kwargs):
            return ""

        def to_list_text(self, **kwargs):
            return ("", "", "")

        def get_name(self):
            return "lock"

        def get_diff(self, _char_obj):
            return -100

    class TimeCondition(Condition):
        def __init__(self, blocking: bool = True, **kwargs: str | int):
            super().__init__(blocking)
            self.day     = "x" if 'day'     not in kwargs.keys() else kwargs['day'    ]
            self.week    = "x" if 'week'    not in kwargs.keys() else kwargs['week'   ]
            self.month   = "x" if 'month'   not in kwargs.keys() else kwargs['month'  ]
            self.year    = "x" if 'year'    not in kwargs.keys() else kwargs['year'   ]
            self.daytime = "x" if 'daytime' not in kwargs.keys() else kwargs['daytime']
            self.weekday = "x" if 'weekday' not in kwargs.keys() else kwargs['weekday']
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs):
            return (
                time.check_day    (self.day    ) and
                time.check_month  (self.month  ) and
                time.check_year   (self.year   ) and
                time.check_week   (self.week   ) and
                time.check_daytime(self.daytime) and
                time.check_weekday(self.weekday))

        def to_list_text(self, **kwargs):
            return ("", "", "")

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

            if self.is_fulfilled(**kwargs):
                return "Time is {color=#0f0}" + text + "{/color}"
            else:
                return "Time is {color=#f00}" + text + "{/color}"

        def get_name(self):
            return f"{self.day}:{self.week}:{self.month}:{self.year}:{self.daytime}:{self.weekday}"

        def get_diff(self, _char_obj):
            if self.is_fulfilled(None):
                return 0
            return -100
            
    class RandomCondition(Condition):
        def __init__(self, amount: num, limit: num, blocking: bool = False):
            super().__init__(blocking)
            self.amount = amount
            self.limit  = limit
            self.display_in_desc = True
            self.display_in_list = True

        def is_fulfilled(self, **kwargs):
            return random.randInt(0, self.limit) < self.amount

        def to_desc_text(self, **kwargs):
            return f"Chance: {str(100 / self.limit * self.amount)}%"

        def to_list_text(self, **kwargs):
            return ("", f"{str(100 / self.limit * self.amount)}%", "Chance")

        def get_name(self):
            return f"Random ({self.amount}/{self.limit})"

        def get_diff(self, _char_obj):
            return 100 / self.limit * self.amount

    class GameDataCondition(Condition):
        def __init__(self, name: str, key: str, value: val | bool, blocking: bool = False):
            super().__init__(blocking)
            self.name = name
            self.key = key
            self.value = value
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs):
            if self.key not in gameData.keys():
                return False
            return gameData[self.key] == self.value

        def to_desc_text(self, **kwargs):
            if self.is_fulfilled():
                return self.name + " is {color=#0f0}" + str(self.value) + "{/color}"
            else:
                return self.name + " is {color=#f00}" + str(self.value) + "{/color}"

        def to_list_text(self, **kwargs):
            return ("", "", "")

        def get_name(self):
            return self.name

        def get_diff(self, _char_obj):
            if self.is_fulfilled():
                return 0
            return -100

    class ProgressCondition(Condition):
        def __init__(self, name: str, key: str, value: int, blocking: bool = False):
            super().__init__(blocking)
            self.name = name
            self.key = key
            self.value = value
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs):
            return check_in_value(self.value, get_progress(self.key))

        def to_desc_text(self, **kwargs):
            if self.is_fulfilled():
                return "Progress-level of {color=#3645e9}" + self.name + "{/color} is {color=#0f0}" + str(self.value) + "{/color}"
            else:
                return "Progress-level of {color=#3645e9}" + self.name + "{/color} is {color=#f00}" + str(self.value) + "{/color}"

        def get_name(self):
            return self.name

        def get_diff(self, _char_obj):
            if self.is_fulfilled():
                return 0
            return -100

    class ValueCondition(Condition):
        def __init__(self, key: str, value: val | bool, blocking: bool = False):
            super().__init__(blocking)
            self.key = key
            self.value = value
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs):
            if self.key not in kwargs.keys():
                return False
            return kwargs[self.key] == self.value

        def to_desc_text(self, **kwargs):
            if self.is_fulfilled():
                return self.key + " is {color=#0f0}" + str(self.value) + "{/color}"
            else:
                return self.key + " is {color=#f00}" + str(self.value) + "{/color}"

        def get_name(self):
            return self.key

        def get_diff(self, _char_obj):
            if self.is_fulfilled():
                return 0
            return -100

    class NumValueCondition(Condition):
        def __init__(self, key: str, value: val, blocking: bool = False):
            super().__init__(blocking)
            self.key = key
            self.value = value
            self.display_in_desc = True
            self.display_in_list = False

        def is_fulfilled(self, **kwargs):
            if self.key not in kwargs.keys():
                return False
            return get_value_diff(self.value, kwargs[self.key]) >= 0

        def to_desc_text(self, **kwargs):
            if self.is_fulfilled():
                return self.key + " is {color=#0f0}" + self.value + "{/color}"
            else:
                return self.key + " is {color=#f00}" + self.value + "{/color}"

        def get_name(self):
            return self.key

        def get_diff(self, _char_obj):
            if self.is_fulfilled():
                return 0
            return -100

    class AND(Condition):
        def __init__(self, *conditions: Condition):
            super().__init__(False)
            self.conditions = list(conditions)
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs):
            for condition in self.conditions:
                if condition.is_fulfilled(**kwargs):
                    continue
                return False

            return True

        def to_desc_text(self, **kwargs):
            return get_logic_condition_desc_text(self.is_fulfilled(**kwargs), self.conditions, "AND", **kwargs)

        def get_name(self):
            output = ""
            for condition in self.conditions:
                if output != "":
                    output += "_AND_"
                output += condition.get_name()

            return output

        def get_diff(self, char_obj: Char):
            diff = 0

            for condition in self.conditions:
                diff += condition.get_diff(char_obj)

            return diff

    class OR(Condition):
        def __init__(self, *conditions: Condition):
            super().__init__(False)
            self.conditions = list(conditions)
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs):
            for condition in self.conditions:
                if condition.is_fulfilled(**kwargs):
                    return True

            return False

        def to_desc_text(self, **kwargs):
            return get_logic_condition_desc_text(self.is_fulfilled(**kwargs), self.conditions, "OR", **kwargs)

        def get_name(self):
            output = ""
            for condition in self.conditions:
                if output != "":
                    output += "_OR_"
                output += condition.get_name()

            return output

        def get_diff(self, char_obj: Char):
            diff = None

            for condition in self.conditions:
                new_diff = condition.get_diff(char_obj)

                if diff == None or abs(diff) > abs(new_diff):
                    diff = new_diff

            return diff

    class NOR(Condition):
        def __init__(self, *conditions: Condition):
            super().__init__(False)
            self.conditions = list(conditions)
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs):
            for condition in self.conditions:
                if condition.is_fulfilled(**kwargs):
                    return False

            return True

        def to_desc_text(self, **kwargs):
            return get_logic_condition_desc_text(self.is_fulfilled(**kwargs), self.conditions, "NOR", **kwargs)
        def get_name(self):
            output = ""
            for condition in self.conditions:
                if output != "":
                    output += "_NOR_"
                output += condition.get_name()

            return output

        def get_diff(self, char_obj: Char):
            diff = None

            for condition in self.conditions:
                new_diff = condition.get_diff(char_obj)

                if diff == None or abs(diff) > abs(new_diff):
                    diff = new_diff

            return diff

    class NOT(Condition):
        def __init__(self, condition: Condition):
            super().__init__(False)
            self.condition = condition
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs):
            return not self.condition.is_fulfilled(**kwargs)

        def to_desc_text(self, **kwargs):
            desc_text = self.condition.to_desc_text(**kwargs)
            if isinstance(desc_text, str):
                return "{color=#616161}NOT{/color} " + desc_text
            else:
                return "\n".join(["{color=#616161}NOT{/color} " + desc for desc in desc_text])

        def get_name(self):
            return "NOT_" + self.condition.get_name()

        def get_diff(self, char_obj: Char):
            diff = self.condition.get_diff(char_obj)

            return clamp_value(100 - diff, -100, 100)

    class XOR(Condition):
        def __init__(self, *conditions: Condition):
            super().__init__(False)
            self.conditions = list(conditions)
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs):
            is_true = False
            
            for condition in self.conditions:
                if condition.is_fulfilled(**kwargs):
                    if is_true:
                        return False
                    is_true = True

            return True

        def to_desc_text(self, **kwargs):
            return get_logic_condition_desc_text(self.is_fulfilled(**kwargs), self.conditions, "XOR", **kwargs)

        def get_name(self):
            output = ""
            for condition in self.conditions:
                if output != "":
                    output += "_XOR_"
                output += condition.get_name()

            return output

        def get_diff(self, char_obj: Char):
            diff = condition.get_diff(char_obj)

            return clamp_value(100 - diff, -100, 100)