init -6 python:
    import re
    from abc import ABC, abstractmethod
    from typing import Union, List

    def get_logic_condition_desc_text(is_fulfilled: bool, conditions: List[Condition], key: str, **kwargs) -> str:
        """
        Returns a description text for a logic condition.

        ### Parameters:
        1. is_fulfilled: bool
            - Whether the condition is fulfilled or not.
        2. conditions: List[Condition]
            - The conditions that are part of the logic condition.
        3. key: str
            - The key of the logic condition.
        4. **kwargs
            - Additional arguments.

        ### Returns:
        1. str
            - The description text.
        """

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
        """
        A class that stores conditions.

        ### Attributes:
        1. conditions: List[Condition]
            - The conditions that are stored.
        2. list_conditions: List[Condition]
            - The conditions that are displayed in the display list.
        3. desc_conditions: List[Condition]
            - The conditions that are displayed in the description.
        4. is_locked: bool
            - Whether the conditions contain a lock condition or not.

        ### Methods:
        1. get_is_locked(self)
            - Returns whether the conditions contain a lock condition or not.
        2. get_list_conditions(self)
            - Returns the conditions that are displayed in the display list.
        3. get_desc_conditions(self)
            - Returns the conditions that are displayed in the description.
        4. get_desc_conditions_desc(self, **kwargs)
            - Returns the description text for the conditions that are displayed in the description.
        5. get_list_conditions_list(self, **kwargs)
            - Returns the description text for the conditions that are displayed in the display list.
        6. get_conditions(self)
            - Returns the conditions that are stored.
        7. is_fulfilled(self, **kwargs)
            - Returns whether all the conditions are fulfilled or not.
        8. is_blocking(self, **kwargs)
            - Returns whether any of the conditions are blocking or not.
            - If any of the conditions are not fulfilled and blocking, the object where the conditions are used is hidden.

        ### Parameters:
        1. *conditions: Condition
            - The conditions that are to be stored.
        """

        def __init__(self, *conditions: Condition):
            """
            The constructor for the ConditionStorage class.
            The conditions are automatically sorted for display in the description and display list.
            The constructor also checks whether the conditions contain a lock condition.

            ### Parameters:
            1. *conditions: Condition
                - The conditions that are to be stored.
            """
            
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

        def get_is_locked(self) -> bool:
            """
            Returns whether the conditions contain a lock condition or not.

            ### Returns:
            1. bool
                - Whether the conditions contain a lock condition or not.
            """

            return self.is_locked

        def get_list_conditions(self) -> List[Condition]:
            """
            Returns the conditions that are displayed in the display list.

            ### Returns:
            1. List[Condition]
                - The conditions that are displayed in the display list.
            """

            return self.list_conditions

        def get_desc_conditions(self) -> List[Condition]:
            """
            Returns the conditions that are displayed in the description.

            ### Returns:
            1. List[Condition]
                - The conditions that are displayed in the description.
            """

            return self.desc_conditions

        def get_desc_conditions_desc(self, **kwargs) -> str:
            """
            Returns the description text for the conditions that are displayed in the description.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. str
                - The description text.
            """

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

        def get_list_conditions_list(self, **kwargs) -> str:
            """
            Returns the description text for the conditions that are displayed in the display list.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. str
                - The description text.
            """

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

        def get_conditions(self) -> List[Condition]:
            """
            Returns the conditions that are stored.

            ### Returns:
            1. List[Condition]
                - The conditions that are stored.
            """

            return self.conditions

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether all the conditions are fulfilled or not.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether all the conditions are fulfilled or not.
            """

            for condition in self.conditions:
                if condition.is_fulfilled(**kwargs):
                    continue
                return False

            return True

        def is_blocking(self, **kwargs) -> bool:
            """
            Returns whether any of the conditions are blocking or not.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether any of the conditions are blocking or not.
            """

            for condition in self.conditions:
                if condition.is_blocking(**kwargs):
                    return False
            return True

    class Condition(ABC):
        """
        An abstract class for conditions.

        ### Attributes:
        1. blocking: bool
            - Whether the condition is blocking or not.
        2. display_in_list: bool
            - Whether the condition is displayed in the display list or not.
        3. display_in_desc: bool
            - Whether the condition is displayed in the description or not.

        ### Methods:
        1. is_fulfilled(self, **kwargs)
            - Returns whether the condition is fulfilled or not.
        2. is_blocking(self, **kwargs)
            - Returns whether the condition is blocking or not.
        3. is_set_blocking(self)
            - Returns whether the condition is set to be blocking or not.
        4. to_list_text(self, **kwargs)
            - Returns the description text for the condition that is displayed in the display list.
        5. to_desc_text(self, **kwargs)
            - Returns the description text for the condition that is displayed in the description.
        6. get_name(self)
            - Returns the name of the condition.
        7. get_diff(self, char_obj: Char)
            - Returns the difference between the condition and the given character.

        ### Parameters:
        1. blocking: bool
            - Whether the condition is blocking or not.
        """

        def __init__(self, blocking: bool = False):
            """
            The constructor for the Condition class.

            ### Parameters:
            1. blocking: bool
                - Whether the condition is blocking or not.
            """

            self.blocking = blocking
            self.display_in_list = False
            self.display_in_desc = False

        @abstractmethod
        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether the condition is fulfilled or not.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            pass

        def is_blocking(self, **kwargs) -> bool:
            """
            Returns whether the condition is blocking or not.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is blocking or not.
            """

            return (not self.is_fulfilled(**kwargs) and self.blocking)

        def is_set_blocking(self) -> bool:
            """
            Returns whether the condition is set to be blocking or not.

            ### Returns:
            1. bool
                - Whether the condition is set to be blocking or not.
            """

            return self.blocking

        def to_list_text(self, **kwargs) -> Tuple[str, str] | List[Tuple[str, str]]:
            """
            Returns the description text for the condition that is displayed in the display list.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. Tuple[str, str, str] | List[Tuple[str, str, str]]
                - The condition text for the display list.
                - The first element is the icon, the second element is the value and the third element is the title.
                - The title is optional.
                - Multiple conditions can be returned as a list.
            """

            return ("", "")

        def to_desc_text(self, **kwargs) -> str | List[str]:
            """
            Returns the description text for the condition that is displayed in the description.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. str | List[str]
                - The condition text for the description.
                - Multiple conditions can be returned as a list.
            """

            return ""

        @abstractmethod
        def get_name(self) -> str:
            """
            Returns the name of the condition.

            ### Returns:
            1. str
                - The name of the condition.
            """

            pass

        @abstractmethod
        def get_diff(self, char_obj: Char) -> num:
            """
            Returns the difference between the condition and the given character.

            ### Parameters:
            1. char_obj: Char
                - The character to compare the condition to.

            ### Returns:
            1. num
                - The difference between the condition and the given character.
            """

            pass

    class StatCondition(Condition):
        """
        A class for conditions that check the stats of a character.
        """

        def __init__(self, blocking: bool = False, **kwargs):
            super().__init__(blocking)
            self.stats = kwargs
            self.display_in_list = True
            self.display_in_desc = True
            
        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether the stats of the character fulfill the condition.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            char_obj = get_kwargs('char_obj', **kwargs)
            if char_obj == None:
                char_obj = get_character("high_school", charList["schools"])

            for stat in self.stats.keys():
                if not char_obj.check_stat(stat, self.stats[stat]):
                    return False

            return True
        
        def to_list_text(self, **kwargs) -> Tuple[str, str, str] | List[Tuple[str, str, str]]:   
            """
            Returns the description text for the condition that is displayed in the display list.
            If multiple stats are checked, the condition is displayed as a list.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. Tuple[str, str, str] | List[Tuple[str, str, str]]
                - The condition text for the display list.
                - The first element is the icon, the second element is the value and the third element is the title.
                - The title is optional.
                - Multiple conditions can be returned as a list.
            """

            char_obj = get_kwargs('char_obj', **kwargs)
            if char_obj == None:
                return ("","")

            output = []
            for stat in self.stats.keys():
                icon = "icons/stat_" + str(stat) + "_icon.webp"
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

        def to_desc_text(self, **kwargs) -> str | List[str]:
            """
            Returns the description text for the condition that is displayed in the description.
            If multiple stats are checked, the condition is displayed as a list.

            ### Parameters:
            1. **kwargs
                - Additional arguments. 

            ### Returns:
            1. str | List[str]
                - The condition text for the description.
                - Multiple conditions can be returned as a list.
            """

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

        def get_name(self) -> str:
            """
            Returns the name of the condition.
            If multiple stats are checked, the condition is displayed as a comma separated list.

            ### Returns:
            1. str
                - The name of the condition.
                - Multiple stats are separated by commas.
            """

            return ', '.join([Stat_Data[key].get_title() for key in self.stats.keys()])

        def get_diff(self, char_obj: Char) -> num:
            """
            Returns the difference between the condition and the given character.
            If the condition difference is lower than -20, the difference is multiplied by 10.
            If the condition difference is lower than -10, the difference is multiplied by 5.
            If the condition difference is lower than -5, the difference is multiplied by 2.
            Otherwise the difference is returned as is.

            ### Parameters:
            1. char_obj: Char
                - The character to compare the condition to.

            ### Returns:
            1. num
                - The difference between the condition and the given character.
            """

            output = 0
            for stat in self.stats.keys():
                obj_stat = char_obj.get_stat_number(stat)
                diff = get_value_diff(self.stats[stat], obj_stat)

                if diff < -20:
                    output += diff * 20
                elif diff < -10:
                    output += diff * 10
                elif diff < 0:
                    output += diff * 5
                elif diff > 5:
                    output += diff * 2
                else:
                    output += diff
            return output

    class RuleCondition(Condition):
        """
        A class for conditions that check if the rules for a character object is active.
        """

        def __init__(self, value: str, blocking: bool = False):
            super().__init__(blocking)
            self.value = value
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether the rule is active or not.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """
            char_obj = get_character("high_school", charList["schools"])
            # char_obj = get_kwargs('char_obj', **kwargs)
            # if char_obj == None:
            #     return False

            return get_rule(self.value).is_unlocked(char_obj.get_name())

        def to_list_text(self, **kwargs) -> Tuple[str, str, str]:
            """
            Returns an empty tuple as the condition is not displayed in the display list.

            ### Returns:
            1. Tuple[str, str, str]
                - An empty tuple.
            """

            return ("", "", "")

        def to_desc_text(self, **kwargs) -> str:
            """
            Returns the description text for the condition that is displayed in the description.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. str
                - The condition text for the description.
            """

            if self.is_fulfilled(**kwargs):
                return "Rule {color=#0f0}" + get_rule(self.value).get_title() + "{/color} is unlocked"
            else:
                return "Rule {color=#f00}" + get_rule(self.value).get_title() + "{/color} is unlocked"

        def get_name(self) -> str:
            """
            Returns the name of the Rule in the condition.

            ### Returns:
            1. str
                - The name of the Rule in the condition.
            """

            if self.value not in rules.keys():
                return ""
            return get_rule(self.value).get_title()

        def get_diff(self, char_obj: Char) -> num:
            """
            Returns the difference between the condition and the given character.
            If the condition is fulfilled, the difference is 0.
            Otherwise the difference is -100.

            ### Parameters:
            1. char_obj: Char
                - The character to compare the condition to.

            ### Returns:
            1. num
                - The difference between the condition and the given character.
            """

            if self.is_fulfilled(char_obj = char_obj):
                return 0
            return -100

    class ClubCondition(Condition):
        """
        A class for conditions that check if the clubs for a character object is active.
        """

        def __init__(self, value: str, blocking: bool = False):
            super().__init__(blocking)
            self.value = value
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether the club is active or not.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            char_obj = get_kwargs('char_obj', **kwargs)
            if char_obj == None:
                return False

            return get_club(self.value).is_unlocked(char_obj.get_name())

        def to_list_text(self, **kwargs) -> Tuple[str, str, str]:
            """
            Returns an empty tuple as the condition is not displayed in the display list.
            """

            return ("", "", "")

        def to_desc_text(self, **kwargs) -> str:
            """
            Returns the description text for the condition that is displayed in the description.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. str
                - The condition text for the description.
            """

            if self.is_fulfilled(**kwargs):
                return "Club {color=#0f0}" + get_club(self.value).get_title() + "{/color} is unlocked"
            else:
                return "Club {color=#f00}" + get_club(self.value).get_title() + "{/color} is unlocked"

        def get_name(self) -> str:
            """
            Returns the name of the Club in the condition.

            ### Returns:
            1. str
                - The name of the Club in the condition.
            """

            if self.value not in clubs.keys():
                return ""
            return get_club(self.value).title

        def get_diff(self, char_obj: Char) -> num:
            """
            Returns the difference between the condition and the given character.
            If the condition is fulfilled, the difference is 0.
            Otherwise the difference is -100.

            ### Parameters:
            1. char_obj: Char
                - The character to compare the condition to.

            ### Returns:
            1. num
                - The difference between the condition and the given character.
            """

            if self.is_fulfilled(char_obj.get_name()):
                return 0
            return -100

    class BuildingCondition(Condition):
        """
        A class for conditions that check if the buildings for a character object is active.
        """

        def __init__(self, value: str, blocking: bool = False):
            super().__init__(blocking)
            self.value = value
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether the building is active or not.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            return get_building(self.value).is_unlocked(self.value)

        def to_list_text(self, **kwargs) -> Tuple[str, str, str]:
            """
            Returns an empty tuple as the condition is not displayed in the display list.
            """

            return ("", "", "")

        def to_desc_text(self, **kwargs) -> str:
            """
            Returns the description text for the condition that is displayed in the description.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. str
                - The condition text for the description.
            """

            if self.is_fulfilled(**kwargs):
                return "Building {color=#0f0}" + get_building(self.value).get_title() + "{/color} is unlocked"
            else:
                return "Building {color=#f00}" + get_building(self.value).get_title() + "{/color} is unlocked"

        def get_name(self) -> str:
            """
            Returns the name of the Building in the condition.

            ### Returns:
            1. str
                - The name of the Building in the condition.
            """

            if self.value not in buildings.keys():
                return ""
            return get_building(self.value).title

        def get_diff(self, char_obj: Char):
            """
            Returns the difference between the condition and the given character.
            If the condition is fulfilled, the difference is 0.
            Otherwise the difference is -100.

            ### Parameters:
            1. char_obj: Char
                - The character to compare the condition to.

            ### Returns:
            1. num
                - The difference between the condition and the given character.
            """

            if self.is_fulfilled(char_obj.get_name()):
                return 0
            return -100

    class LevelCondition(Condition):
        """
        A class for conditions that check the level of a character object.
        """

        def __init__(self, value: int, blocking: bool = False):
            super().__init__(blocking)
            self.value = value
            self.display_in_list = True
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs):
            """
            Returns whether the characters level fulfills the condition.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            char_obj = get_kwargs('char_obj', **kwargs)
            if char_obj == None:
                return False

            return char_obj.check_level(self.value)

        def to_desc_text(self, **kwargs) -> str:
            """
            Returns the description text for the condition that is displayed in the description.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. str
                - The condition text for the description.
            """

            if self.is_fulfilled(**kwargs):
                return "Level: {color=#0f0}" + self.value + "{/color}"
            else:
                return "Level: {color=#f00}" + self.value + "{/color}"

        def to_list_text(self, **kwargs) -> Tuple[str, str, str]:
            """
            Returns the description text for the condition that is displayed in the display list.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. Tuple[str, str, str]
                - The condition text for the display list.
                - The first element is the icon, the second element is the value and the third element is the title.
                - The title is optional.
            """
            if self.is_fulfilled(**kwargs):
                return ("{image=icons/stat_level_icon.webp}", "{color=#0f0}" + str(self.value) + "{/color}", "Level")
            else:
                return ("{image=icons/stat_level_icon.webp}", "{color=#f00}" + str(self.value) + "{/color}", "Level")

        def get_name(self):
            """
            Returns "Level".

            ### Returns:
            1. str
                - "Level".
            """

            return "Level"

        def get_diff(self, char_obj: Char) -> num:
            """
            Returns the difference between the condition and the given characters level.
            If the level difference is lower than -2, the difference is multiplied by 50.
            If the level difference is lower than -1, the difference is multiplied by 20.
            Otherwise the difference is returned as is.

            ### Parameters:
            1. char_obj: Char
                - The character to compare the condition to.

            ### Returns:
            1. num
                - The difference between the condition and the given characters level.
            """

            # return char_obj.get_nearest_level_delta(self.value) * 20

            obj_level = char_obj.get_level()
            diff = get_value_diff(self.value, obj_level)

            if diff < -2:
                return diff * 50
            elif diff < -1:
                return diff * 20
            return diff

    class MoneyCondition(Condition):
        """
        A class for conditions that check the money.
        """

        def __init__(self, value: num, blocking = False):
            super().__init__(blocking)
            self.value = value
            self.display_in_list = True
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether the budget is within the condition.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            return money.get_value() >= self.value

        def to_desc_text(self, **kwargs) -> str:
            """
            Returns the description text for the condition that is displayed in the description.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. str
                - The condition text for the description.
            """

            if self.is_fulfilled():
                return "Money: {color=#0f0}" + str(self.value) + "{/color}"
            else:
                return "Money: {color=#f00}" + str(self.value) + "{/color}"

        def to_list_text(self, **kwargs) -> Tuple[str, str, str]:
            """
            Returns the description text for the condition that is displayed in the display list.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. Tuple[str, str, str]
                - The condition text for the display list.
                - The first element is the icon, the second element is the value and the third element is the title.
                - The title is optional.
            """

            if self.is_fulfilled():
                return ("{image=icons/stat_money_icon.webp}", "{color=#0f0}" + str(self.value) + "{/color}", "Money")
            else:
                return ("{image=icons/stat_money_icon.webp}", "{color=#f00}" + str(self.value) + "{/color}", "Money")

        def get_name(self) -> str:
            """
            Returns "Money".

            ### Returns:
            1. str
                - "Money".
            """

            return "Money"

        def get_diff(self, _char_obj):
            """
            Returns the difference between the condition and the given characters money.
            The difference is calculated as follows:
                - The difference gets subtracted by 20 to create some kind of buffer.
                - If the difference is lower than 0, the difference is returned as is.
                - If the difference is larger than 0, the difference is returned as 0 to set it as fulfilled but not create a better chance for votes.

            ### Parameters:
            1. char_obj: Char
                - The character to compare the condition to.

            ### Returns:
            1. num
                - The difference between the condition and the given characters money.
            """

            output = -20 + (money.get_value() - self.value)
            if output > 0:
                return 0
            return output

    class SchoolCondition(Condition):
        """
        A class for conditions that check the school of a character object.
        """

        def __init__(self, school: str = "x", blocking: bool = True):
            super().__init__(blocking)
            self.school = school

        def is_fulfilled(self, **kwargs):
            """
            Returns whether the characters school equals the school of the condition.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            char_obj = get_kwargs('char_obj', **kwargs)
            if char_obj == None:
                return False
            return self.school == "x" or char_obj.get_name() == self.school

        def to_list_text(self, **kwargs) -> Tuple[str, str, str]:
            """
            Returns an empty tuple as the condition is not displayed in the display list.
            """

            return ("", "", "")

        def to_desc_text(self, **kwargs) -> str:
            """
            Returns an empty string as the condition is not displayed in the description.
            """

            return ""

        def get_name(self) -> str:
            """
            Returns the name of the school in the condition.

            ### Returns:
            1. str
                - The name of the school in the condition.
            """

            char_obj = get_character(school, charList["schools"])
            if char_obj == None:
                return self.school
            return char_obj.get_title()

        def get_diff(self, char_obj: Char) -> num:
            """
            Returns the difference between the condition and the given character.
            If the condition is fulfilled, the difference is 0.
            Otherwise the difference is -100.

            ### Parameters:
            1. char_obj: Char
                - The character to compare the condition to.
            """

            if char_obj.name == self.school:
                return 0
            return -100

    class LockCondition(Condition):
        """
        A class for conditions that lock the object it is used in.
        This class makes unlocking the object impossible.
        If is_blocking is set to True, the object is also hidden.
        """

        def __init__(self, is_blocking: bool = True):
            super().__init__(is_blocking)

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns "False" as the condition is never fulfilled.
            """

            return False

        def to_desc_text(self, **kwargs) -> str:
            """
            Returns an empty string as the condition is not displayed in the description.
            """

            return ""

        def to_list_text(self, **kwargs) -> Tuple[str, str, str]:
            """
            Returns an empty tuple as the condition is not displayed in the display list.
            """
            
            return ("", "", "")

        def get_name(self) -> str:
            """
            Returns "lock".

            ### Returns:
            1. str
                - "lock".
            """

            return "lock"

        def get_diff(self, _char_obj) -> num:
            """
            Returns -100 as the condition is never fulfilled.

            ### Returns:
            1. num
                - -100
            """

            return -100

    class TimeCondition(Condition):
        """
        A class for conditions that check the time.
        """

        def __init__(self, blocking: bool = True, **kwargs: str | int):
            super().__init__(blocking)
            self.day     = "x" if 'day'     not in kwargs.keys() else kwargs['day'    ]
            self.week    = "x" if 'week'    not in kwargs.keys() else kwargs['week'   ]
            self.month   = "x" if 'month'   not in kwargs.keys() else kwargs['month'  ]
            self.year    = "x" if 'year'    not in kwargs.keys() else kwargs['year'   ]
            self.daytime = "x" if 'daytime' not in kwargs.keys() else kwargs['daytime']
            self.weekday = "x" if 'weekday' not in kwargs.keys() else kwargs['weekday']
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether the current time fulfills the condition.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            return (
                time.check_day    (self.day    ) and
                time.check_month  (self.month  ) and
                time.check_year   (self.year   ) and
                time.check_week   (self.week   ) and
                time.check_daytime(self.daytime) and
                time.check_weekday(self.weekday))

        def to_list_text(self, **kwargs) -> Tuple[str, str, str]:
            """
            Returns an empty tuple as the condition is not displayed in the display list.
            """
            
            return ("", "", "")

        def to_desc_text(self, **kwargs) -> str:
            """
            Returns the description text for the condition that is displayed in the description.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. str
                - The condition text for the description.
            """

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

        def get_name(self) -> str:
            """
            Returns the time conditions as name.

            ### Returns:
            1. str
                - The time conditions as name.
            """

            return f"{self.day}:{self.week}:{self.month}:{self.year}:{self.daytime}:{self.weekday}"

        def get_diff(self, _char_obj) -> num:
            """
            Returns the difference between the condition and the current time.
            If the condition is fulfilled, the difference is 0.
            Otherwise the difference is -100.

            ### Returns:
            1. num
                - The difference between the condition and the current time.
            """

            if self.is_fulfilled(None):
                return 0
            return -100
            
    class RandomCondition(Condition):
        """
        A class for conditions that are fulfilled randomly.

        ### Attributes:
        1. amount: num
            - The value that acts as the border between fulfilled and not fulfilled.
            - If the random value is lower than the amount, the condition is fulfilled.
        2. limit: num
            - The limit of the random value.
            - The random value is generated between 0 and the limit.
        """

        def __init__(self, amount: num, limit: num, blocking: bool = False):
            """
            The constructor for the RandomCondition class.

            ### Parameters:
            1. amount: num
                - The value that acts as the border between fulfilled and not fulfilled.
                - If the random value is lower than the amount, the condition is fulfilled.
            2. limit: num
                - The limit of the random value.
                - The random value is generated between 0 and the limit.
            """

            super().__init__(blocking)
            self.amount = amount
            self.limit  = limit
            self.display_in_desc = True
            self.display_in_list = True

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether the randomizer rolled a number lower than the amount.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            return get_random_int(0, self.limit) < self.amount

        def to_desc_text(self, **kwargs) -> str:
            """
            Returns the description text for the condition that is displayed in the description.

            ### Returns:
            1. str
                - The condition text for the description.
            """

            return f"Chance: {str(100 / self.limit * self.amount)}%"

        def to_list_text(self, **kwargs) -> Tuple[str, str, str]:
            """
            Returns the description text for the condition that is displayed in the display list.

            ### Returns:
            1. Tuple[str, str, str]
                - The condition text for the display list.
                - The first element is the icon, the second element is the value and the third element is the title.
                - The title is optional.
            """
            return ("", f"{str(100 / self.limit * self.amount)}%", "Chance")

        def get_name(self) -> str:
            """
            Returns the relation between the amount and the limit as name.

            ### Returns:
            1. str
                - The relation between the amount and the limit as name.
            """

            return f"Random ({self.amount}/{self.limit})"

        def get_diff(self, _char_obj) -> num:
            """
            Returns the Probability as difference.

            ### Returns:
            1. num
                - The Probability as difference.
            """

            return 100 / self.limit * self.amount

    class GameDataCondition(Condition):
        """
        A class for conditions that check the game data for matching values.

        ### Attributes:
        1. name: str
            - The name of the condition.
        2. key: str
            - The key of the game data.
        3. value: val | bool
            - The value the game data has to match.
        """

        def __init__(self, name: str, key: str, value: val | bool, blocking: bool = False):
            """
            The constructor for the GameDataCondition class.

            ### Parameters:
            1. name: str
                - The name of the condition.
            2. key: str
                - The key of the game data.
            3. value: val | bool
                - The value the game data has to match.
            """

            super().__init__(blocking)
            self.name = name
            self.key = key
            self.value = value
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether the game data matches the needed value.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            if self.key not in gameData.keys():
                return False
            return gameData[self.key] == self.value

        def to_desc_text(self, **kwargs) -> str:
            """
            Returns the description text for the condition that is displayed in the description.

            ### Returns:
            1. str
                - The condition text for the description.
            """

            if self.is_fulfilled():
                return self.name + " is {color=#0f0}" + str(self.value) + "{/color}"
            else:
                return self.name + " is {color=#f00}" + str(self.value) + "{/color}"

        def to_list_text(self, **kwargs) -> Tuple[str, str, str]:
            """
            Returns the description text for the condition that is displayed in the display list.
            """

            return ("", "", "")

        def get_name(self) -> str:
            """
            Returns the name of the condition.

            ### Returns:
            1. str
                - The name of the condition.
            """

            return self.name

        def get_diff(self, _char_obj) -> num:
            """
            Returns the difference between the condition and the game data.
            If the condition is fulfilled, the difference is 0.
            Otherwise the difference is -100.

            ### Returns:
            1. num
                - The difference between the condition and the game data.
            """

            if self.is_fulfilled():
                return 0
            return -100

    class ProgressCondition(Condition):
        """
        A class for conditions that check the progress of an event series.
        """

        def __init__(self, name: str, key: str, value: int, blocking: bool = False):
            super().__init__(blocking)
            self.name = name
            self.key = key
            self.value = value
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs):
            """
            Returns whether an event series has reached the needed progress level.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            return check_in_value(self.value, get_progress(self.key))

        def to_desc_text(self, **kwargs) -> str:
            """
            Returns the description text for the condition that is displayed in the description.

            ### Returns:
            1. str
                - The condition text for the description.
            """

            if self.is_fulfilled():
                return "Progress-level of {color=#3645e9}" + self.name + "{/color} is {color=#0f0}" + str(self.value) + "{/color}"
            else:
                return "Progress-level of {color=#3645e9}" + self.name + "{/color} is {color=#f00}" + str(self.value) + "{/color}"

        def get_name(self) -> str:
            """
            Returns the name of the condition.
            """

            return self.name

        def get_diff(self, _char_obj) -> num:
            """
            Returns the difference between the condition and the progress.
            If the condition is fulfilled, the difference is 0.
            Otherwise the difference is -100.

            ### Returns:
            1. num
                - The difference between the condition and the progress.
            """

            if self.is_fulfilled():
                return 0
            return -100

    class ValueCondition(Condition):
        """
        A class for conditions that check the value of kwargs.
        """

        def __init__(self, key: str, value: val | bool, blocking: bool = False):
            super().__init__(blocking)
            self.key = key
            self.value = value
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether a certain value of kwargs matches the needed value.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            if self.key not in kwargs.keys():
                return False
            return kwargs[self.key] == self.value

        def to_desc_text(self, **kwargs) -> str:
            """
            Returns the description text for the condition that is displayed in the description.

            ### Returns:
            1. str
                - The condition text for the description.
            """

            if self.is_fulfilled():
                return self.key + " is {color=#0f0}" + str(self.value) + "{/color}"
            else:
                return self.key + " is {color=#f00}" + str(self.value) + "{/color}"

        def get_name(self) -> str:
            """
            Returns the name of the condition.

            ### Returns:
            1. str
                - The name of the condition.
            """

            return self.key

        def get_diff(self, _char_obj) -> num:
            """
            Returns the difference between the condition and the value of kwargs.
            If the condition is fulfilled, the difference is 0.
            Otherwise the difference is -100.

            ### Returns:
            1. num
                - The difference between the condition and the value of kwargs.
            """

            if self.is_fulfilled():
                return 0
            return -100

    class NumValueCondition(Condition):
        """
        A class for conditions that check the value of kwargs by checking if the value is inside a ranged value.
        """

        def __init__(self, key: str, value: val, blocking: bool = False):
            super().__init__(blocking)
            self.key = key
            self.value = value
            self.display_in_desc = True
            self.display_in_list = False

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether a certain value of kwargs is inside a ranged value.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            if self.key not in kwargs.keys():
                return False
            return get_value_diff(self.value, kwargs[self.key]) >= 0

        def to_desc_text(self, **kwargs) -> str:
            """
            Returns the description text for the condition that is displayed in the description.

            ### Returns:
            1. str
                - The condition text for the description.
            """

            if self.is_fulfilled():
                return self.key + " is {color=#0f0}" + self.value + "{/color}"
            else:
                return self.key + " is {color=#f00}" + self.value + "{/color}"

        def get_name(self) -> str:
            """
            Returns the name of the condition.

            ### Returns:
            1. str
                - The key of the value for kwargs.
            """

            return self.key

        def get_diff(self, _char_obj) -> num:
            """
            Returns the difference between the condition and the value of kwargs.
            If the condition is fulfilled, the difference is 0.
            Otherwise the difference is -100.

            ### Returns:
            1. num
                - The difference between the condition and the value of kwargs.
            """

            if self.is_fulfilled():
                return 0
            return -100

    class AND(Condition):
        """
        A class for conditions that check if all conditions are fulfilled.
        """

        def __init__(self, *conditions: Condition):
            super().__init__(False)
            self.conditions = list(conditions)
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether all conditions are fulfilled or not.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            for condition in self.conditions:
                if condition.is_fulfilled(**kwargs):
                    continue
                return False

            return True

        def to_desc_text(self, **kwargs) -> str:
            """
            Returns the description text for the condition that is displayed in the description.
            Logic conditions are displayed in a special way.

            ### Returns:
            1. str
                - The condition text for the description.
            """

            return get_logic_condition_desc_text(self.is_fulfilled(**kwargs), self.conditions, "AND", **kwargs)

        def get_name(self) -> str:
            """
            Returns the name of the condition.
            Logic conditions are displayed in a special way.

            ### Returns:
            1. str
                - The name of the condition.
            """

            output = ""
            for condition in self.conditions:
                if output != "":
                    output += "_AND_"
                output += condition.get_name()

            return output

        def get_diff(self, char_obj: Char):
            """
            Returns the added difference of all conditions.

            ### Parameters:
            1. char_obj: Char
                - The character to compare the condition to.
            """

            diff = 0

            for condition in self.conditions:
                diff += condition.get_diff(char_obj)

            return diff

    class OR(Condition):
        """
        A class for conditions that check if at least one condition is fulfilled.
        """

        def __init__(self, *conditions: Condition):
            super().__init__(False)
            self.conditions = list(conditions)
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs):
            """
            Returns whether at least one condition is fulfilled or not.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            for condition in self.conditions:
                if condition.is_fulfilled(**kwargs):
                    return True

            return False

        def to_desc_text(self, **kwargs) -> str | List[str]:
            """
            Returns the description text for the condition that is displayed in the description.
            Logic conditions are displayed in a special way.
            
            ### Returns:
            1. str | List[str]
                - The condition text for the description.
            """

            return get_logic_condition_desc_text(self.is_fulfilled(**kwargs), self.conditions, "OR", **kwargs)

        def get_name(self) -> str:
            """
            Returns the name of the condition.
            Logic conditions are displayed in a special way.

            ### Returns:
            1. str
                - The name of the condition.
            """

            output = ""
            for condition in self.conditions:
                if output != "":
                    output += "_OR_"
                output += condition.get_name()

            return output

        def get_diff(self, char_obj: Char) -> num:
            """
            Returns the difference of the condition with the lowest difference.

            ### Parameters:
            1. char_obj: Char
                - The character to compare the condition to.

            ### Returns:
            1. num
                - The difference of the condition with the lowest difference.
            """

            diff = None

            for condition in self.conditions:
                new_diff = condition.get_diff(char_obj)

                if diff == None or abs(diff) > abs(new_diff):
                    diff = new_diff

            return diff

    class NOR(Condition):
        """
        A class for conditions that check if none of the conditions are fulfilled.
        """

        def __init__(self, *conditions: Condition):
            super().__init__(False)
            self.conditions = list(conditions)
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs):
            """
            Returns whether none of the conditions are fulfilled or not.
            None of the conditions have to be fulfilled for the condition to be fulfilled.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            for condition in self.conditions:
                if condition.is_fulfilled(**kwargs):
                    return False

            return True

        def to_desc_text(self, **kwargs) -> str | List[str]:
            """
            Returns the description text for the condition that is displayed in the description.
            Logic conditions are displayed in a special way.

            ### Returns:
            1. str | List[str]
                - The condition text for the description.
            """

            return get_logic_condition_desc_text(self.is_fulfilled(**kwargs), self.conditions, "NOR", **kwargs)

        def get_name(self) -> str:
            """
            Returns the name of the condition.
            Logic conditions are displayed in a special way.

            ### Returns:
            1. str
                - The name of the condition.
            """

            output = ""
            for condition in self.conditions:
                if output != "":
                    output += "_NOR_"
                output += condition.get_name()

            return output

        def get_diff(self, char_obj: Char) -> num:
            """
            Returns the difference of the condition with the lowest difference.

            ### Parameters:
            1. char_obj: Char
                - The character to compare the condition to.

            ### Returns:
            1. num
                - The difference of the condition with the lowest difference.
            """

            diff = None

            for condition in self.conditions:
                new_diff = condition.get_diff(char_obj)

                if diff == None or abs(diff) > abs(new_diff):
                    diff = new_diff

            return diff

    class NOT(Condition):
        """
        A class for conditions that check if the condition is not fulfilled.
        """

        def __init__(self, condition: Condition):
            super().__init__(False)
            self.condition = condition
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether the condition is not fulfilled.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            return not self.condition.is_fulfilled(**kwargs)

        def to_desc_text(self, **kwargs) -> str | List[str]:
            """
            Returns the description text for the condition that is displayed in the description.
            Logic conditions are displayed in a special way.

            ### Returns:
            1. str | List[str]
                - The condition text for the description.
            """

            desc_text = self.condition.to_desc_text(**kwargs)
            if isinstance(desc_text, str):
                return "{color=#616161}NOT{/color} " + desc_text
            else:
                return "\n".join(["{color=#616161}NOT{/color} " + desc for desc in desc_text])

        def get_name(self) -> str:
            """
            Returns the name of the condition with a "NOT_" prefix.

            ### Returns:
            1. str
                - The name of the condition.
            """

            return "NOT_" + self.condition.get_name()

        def get_diff(self, char_obj: Char) -> num:
            """
            Returns the difference of the added condition inverted.

            ### Parameters:
            1. char_obj: Char
                - The character to compare the condition to.

            ### Returns:
            1. num
                - The difference of the added condition inverted.
            """

            diff = self.condition.get_diff(char_obj)

            return clamp_value(100 - diff, -100, 100)

    class XOR(Condition):
        """
        A class for conditions that check if only one of the conditions is fulfilled.
        """

        def __init__(self, *conditions: Condition):
            super().__init__(False)
            self.conditions = list(conditions)
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether only one of the conditions is fulfilled.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            is_true = False
            
            for condition in self.conditions:
                if condition.is_fulfilled(**kwargs):
                    if is_true:
                        return False
                    is_true = True

            return True

        def to_desc_text(self, **kwargs) -> str:
            """
            Returns the description text for the condition that is displayed in the description.
            Logic conditions are displayed in a special way.

            ### Returns:
            1. str | List[str]
                - The condition text for the description.
            """

            return get_logic_condition_desc_text(self.is_fulfilled(**kwargs), self.conditions, "XOR", **kwargs)

        def get_name(self) -> str:
            """
            Returns the name of the condition.
            Logic conditions are displayed in a special way.

            ### Returns:
            1. str
                - The name of the condition.
            """

            output = ""
            for condition in self.conditions:
                if output != "":
                    output += "_XOR_"
                output += condition.get_name()

            return output

        def get_diff(self, char_obj: Char) -> num:
            """
            Returns the difference of the condition inverted.

            ### Parameters:
            1. char_obj: Char
                - The character to compare the condition to.

            ### Returns:
            1. num
                - The difference of the condition inverted.
            """

            diff = condition.get_diff(char_obj)

            return clamp_value(100 - diff, -100, 100)