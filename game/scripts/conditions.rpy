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
            prefix += "{color=#00a000}|{/color} "
        else:
            prefix += "{color=#a00000}|{/color} "

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
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether the condition is fulfilled or not.
        2. is_blocking(self, **kwargs) -> bool
            - Returns whether the condition is blocking or not.
        3. is_set_blocking(self) -> bool
            - Returns whether the condition is set to be blocking or not.
        4. to_list_text(self, **kwargs) -> Tuple[str, str] | Tuple[str, str, str] | List[Tuple[str, str] | Tuple[str, str, str]]
            - Returns the description text for the condition that is displayed in the display list.
        5. to_desc_text(self, **kwargs) -> str
            - Returns the description text for the condition that is displayed in the description.
        6. get_name(self) -> str
            - Returns the name of the condition.
        7. get_diff(self, char_obj: Char) -> int
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
            
            check_in_replay = get_kwargs('check_in_replay', False, **kwargs)

            if check_in_replay:
                return True

            global is_in_replay

            in_replay = get_kwargs('in_replay', False, **kwargs)
            in_journal_gallery = get_kwargs('in_journal_gallery', False, **kwargs)

            if is_in_replay or in_replay or in_journal_gallery:
                return True

            return False


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

        def to_list_text(self, **kwargs) -> Tuple[str, str] | Tuple[str, str, str] | List[Tuple[str, str] | Tuple[str, str, str]]:
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

            return self.get_name()

        @abstractmethod
        def get_name(self) -> str:
            """
            Returns the name of the condition.

            ### Returns:
            1. str
                - The name of the condition.
            """

            pass

        def get_diff(self, char_obj: str | Char) -> num:
            """
            Returns the difference between the condition and the given character.

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

    class StatCondition(Condition):
        """
        A class for conditions that check the stats of a character.

        ### Attributes:
        1. stats: Dict[str, int]
            - The stats that are checked.
        2. char_obj: Char
            - The character object that is checked.

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether the stats of the character fulfill the condition.
        2. to_list_text(self, **kwargs) -> Tuple[str, str] | Tuple[str, str, str] | List[Tuple[str, str] | Tuple[str, str, str]]
            - Returns the description text for the condition that is displayed in the display list.
        3. to_desc_text(self, **kwargs) -> str | List[str]
            - Returns the description text for the condition that is displayed in the description.
        4. get_name(self) -> str
            - Returns the name of the condition.
        5. get_diff(self, char_obj: str | Char = None) -> num
            - Returns the difference between the condition and the given character.
            - If the difference is lower than -20, the difference is multiplied by 10.
            - If the difference is lower than -10, the difference is multiplied by 5.
            - If the difference is lower than -5, the difference is multiplied by 2.
            - Otherwise the difference is returned as is.
        """

        def __init__(self, blocking: bool = False, *, char_obj: str | Char = None, **kwargs: str | Selector):
            super().__init__(blocking)
            self.stats = kwargs
            self.display_in_list = True
            self.display_in_desc = True
            self.char_obj = char_obj
            
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

            if super().is_fulfilled(**kwargs):
                return True

            char_obj = None
            if hasattr(self, 'char_obj'):
                char_obj = self.char_obj

            if isinstance(char_obj, str):
                char_obj = get_character_by_key(char_obj)

            if char_obj == None:
                char_obj = get_kwargs('char_obj', get_school(), **kwargs)

            for stat in self.stats.keys():
                stat_key = get_element(stat)
                if not char_obj.check_stat(stat, self.stats[stat]):
                    return False

            return True
        
        def to_list_text(self, **kwargs) -> Tuple[str, str] | Tuple[str, str, str] | List[Tuple[str, str] | Tuple[str, str, str]]:
            """
            Returns the description text for the condition that is displayed in the display list.
            If multiple stats are checked, the condition is displayed as a list.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. Tuple[str, str] | Tuple[str, str, str] | List[Tuple[str, str] | Tuple[str, str, str]]
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
                if char_obj.check_stat(stat, self.stats[stat]):
                    output.append((
                        get_stat_icon(stat, white = False), 
                        "{color=#00a000}" + str(self.stats[stat]) + "{/color}", 
                        Stat_Data[stat].get_title()
                    ))
                else:
                    output.append((
                        get_stat_icon(stat, white = False), 
                        "{color=#a00000}" + str(self.stats[stat]) + "{/color}", 
                        Stat_Data[stat].get_title()
                    ))
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

            char_obj = None
            if hasattr(self, 'char_obj'):
                char_obj = self.char_obj

            if isinstance(char_obj, str):
                char_obj = get_character_by_key(char_obj)

            if char_obj == None:
                char_obj = get_kwargs('char_obj', get_school(), **kwargs)

            output = []
            for stat in self.stats.keys():
                stat_name = Stat_Data[stat].get_title()

                if char_obj.check_stat(stat, self.stats[stat]):
                    output.append(stat_name + ": {color=#00a000}" + str(self.stats[stat]) + "{/color}")
                else:
                    output.append(stat_name + ": {color=#a00000}" + str(self.stats[stat]) + "{/color}")

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

        def get_diff(self, char_obj: str | Char = None) -> num:
            """
            Returns the difference between the condition and the given character.
            If the condition difference is lower than -20, the difference is multiplied by 10.
            If the condition difference is lower than -10, the difference is multiplied by 5.
            If the condition difference is lower than -5, the difference is multiplied by 2.
            Otherwise the difference is returned as is.

            ### Parameters:
            1. char_obj: str | Char
                - The character to compare the condition to.
                - If the character is given as a key, the following keys are possible: school, parent, teacher, secretary
                - If the character is not given, the school character is used.

            ### Returns:
            1. num
                - The difference between the condition and the given character.
            """

            if isinstance(char_obj, str):
                char_obj = get_character_by_key(char_obj)
            if char_obj == None:
                char_obj = get_school()

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

    class StatLimitCondition(Condition):
        """
        A class for conditions that checks if a stat has hit the level cap.

        ### Attributes:
        1. _stat: str
            - The stat that is checked.
            - The stat can be either CORRUPTION or INHIBITION.
        2. _char_obj: Char
            - The character object that is checked.

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether the stat has hit the level cap.
        2. get_name(self) -> str
            - Returns the name of the condition.
        """

        def __init__(self, stat: str, char_obj: str | Char = None, **kwargs):
            super().__init__(**kwargs)
            self._stat = stat
            self._char_obj = char_obj
            self.display_in_list = False
            self.display_in_desc = False

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether the stat has hit the level cap.

            ### Parameters:
            1. **kwargs
                - Additional arguments.
                - Method possibly checks for key 'char_obj' in kwargs looking for a Character Object

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            if super().is_fulfilled(**kwargs):
                return True

            char_obj = None
            if hasattr(self, '_char_obj'):
                char_obj = self._char_obj

            if isinstance(char_obj, str):
                char_obj = get_character_by_key(char_obj)

            if char_obj == None:
                char_obj = get_kwargs('char_obj', get_school(), **kwargs)

            
            if self._stat == CORRUPTION:
                limit_value = clamp_value(100, 0, char_obj.get_level() * 10)
            elif self._stat == INHIBITION:
                limit_value = clamp_value(0, 100 - (char_obj.get_level() * 10), 100)
            else:
                return False

            stat_value = get_stat_for_char(self._stat, char_obj)

            if stat_value == limit_value:
                return True

        def get_name(self) -> str:
            """
            Returns the name of the condition.

            ### Returns:
            1. str
                - The name of the condition.
                - The name is either "Corruption limit" or "Inhibition limit".
            """

            if self._stat == CORRUPTION:
                return "Corruption limit"
            elif self._stat == INHIBITION:
                return "Inhibition limit"
            return ""

    class ProficiencyCondition(Condition):
        """
        A class for conditions that checks the proficiency of the headmaster

        ### Attributes:
        1. _proficiency: str
            - The proficiency that is checked.
        2. _xp: int | str
            - The xp value that is checked.
            - If the value is -1, the xp value is not checked.
        3. _level: int | str
            - The level value that is checked.
            - If the value is -1, the level value is not checked.

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether the proficiency of the headmaster fulfills the condition.
        2. get_name(self) -> str
            - Returns the name of the condition.
        """

        def __init__(self, proficiency: str, *, xp: int | str = -1, level: int | str = -1):
            super().__init__(True)
            self._proficiency = proficiency
            self._xp = xp
            self._level = level

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether the proficiency of the headmaster fulfills the condition.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            if super().is_fulfilled(**kwargs):
                return True

            if self._xp == -1 and self._level == -1:
                return self._proficiency in headmaster_proficiencies.keys()
            
            output = True
            if self._xp != -1:
                curr_xp = get_headmaster_proficiency_xp(self._proficiency)
                if not check_in_value(self._xp, curr_xp):
                    output = False
            if self._level != -1:
                curr_level = get_headmaster_proficiency_level(self._proficiency)
                if not check_in_value(self._level, curr_level):
                    output = False

            return output

        def get_name(self) -> str:
            """
            Returns the name of the condition.

            ### Returns:
            1. str
                - The name of the condition.
                - Example: Math_100_-1
            """

            return self._proficiency + "_" + str(self._xp) + "_" + str(self._level)

    class TutorialCondition(Condition):
        """
        A class for conditions that check if the tutorial is active.

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether the tutorial is active.
        2. get_name(self) -> str
            - Returns the name of the condition.
        """

        def __init__(self):
            super().__init__(True)

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether the tutorial is active.
            """

            return persistent.tutorial

        def get_name(self) -> str:
            """
            Returns the name of the condition.
            """

            return "Is_tutorial_active"

    class RuleCondition(Condition):
        """
        A class for conditions that check if the rules for a character object is active.

        ### Attributes:
        1. value: str
            - The key of the rule that is checked.

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether the rule is active or not.
        2. to_desc_text(self, **kwargs) -> str
            - Returns the description text for the condition that is displayed in the description.
        3. get_name(self) -> str
            - Returns the name of the Rule in the condition.
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

            if super().is_fulfilled(**kwargs):
                return True

            return get_rule(self.value).is_unlocked()

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
                return "Rule {color=#00a000}" + get_rule(self.value).get_title() + "{/color} is unlocked"
            else:
                return "Rule {color=#a00000}" + get_rule(self.value).get_title() + "{/color} is unlocked"

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

    class ClubCondition(Condition):
        """
        A class for conditions that check if the clubs for a character object is active.

        ### Attributes:
        1. value: str
            - The key of the club that is checked.

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether the club is active or not.
        2. to_desc_text(self, **kwargs) -> str
            - Returns the description text for the condition that is displayed in the description.
        3. get_name(self) -> str
            - Returns the name of the Club in the condition.
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

            if super().is_fulfilled(**kwargs):
                return True

            return get_club(self.value).is_unlocked()

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
                return "Club {color=#00a000}" + get_club(self.value).get_title() + "{/color} is unlocked"
            else:
                return "Club {color=#a00000}" + get_club(self.value).get_title() + "{/color} is unlocked"

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

    class BuildingCondition(Condition):
        """
        A class for conditions that check if the buildings for a character object is active.

        ### Attributes:
        1. value: str
            - The key of the building that is checked.

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether the building is active or not.
        2. to_desc_text(self, **kwargs) -> str
            - Returns the description text for the condition that is displayed in the description.
        3. get_name(self) -> str
            - Returns the name of the Building in the condition.
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

            if super().is_fulfilled(**kwargs):
                return True

            return get_building(self.value).is_unlocked()

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
                return "Building {color=#00a000}" + get_building(self.value).get_title() + "{/color} is unlocked"
            else:
                return "Building {color=#a00000}" + get_building(self.value).get_title() + "{/color} is unlocked"

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

    class BuildingLevelCondition(Condition):
        """
        A class for conditions that check the level of a building.

        ### Attributes:
        1. name: str
            - The key of the building that is checked.
        2. level: int
            - The level that is checked.

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether the building level is active or not.
        2. to_desc_text(self, **kwargs) -> str
            - Returns the description text for the condition that is displayed in the description.
        3. get_name(self) -> str
            - Returns the name of the Building in the condition.
        """

        def __init__(self, name: str, level: str | int, blocking: bool = False):
            super().__init__(blocking)
            self.name = name
            self.level = level
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether the building level is active or not.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            if super().is_fulfilled(**kwargs):
                return True

            return check_in_value(self.level, get_building(self.name).get_level())

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
                return "Building {color=#00a000}" + get_building(self.name).get_title() + "{/color} is at level {color=#00a000}" + str(self.level) + "{/color}"
            else:
                return "Building {color=#a00000}" + get_building(self.name).get_title() + "{/color} is at level {color=#a00000}" + str(self.level) + "{/color}"

        def get_name(self) -> str:
            """
            Returns the name of the Building in the condition.

            ### Returns:
            1. str
                - The name of the Building in the condition.
            """

            if self.name not in buildings.keys():
                return ""
            return get_building(self.name).title

    class LevelCondition(Condition):
        """
        A class for conditions that check the level of a character object.

        ### Attributes:
        1. value: int
            - The level that is checked.
        2. char_obj: Char
            - The character object that is checked.
            
        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether the characters level fulfills the condition.
        2. to_desc_text(self, **kwargs) -> str
            - Returns the description text for the condition that is displayed in the description.
        3. to_list_text(self, **kwargs) -> Tuple[str, str, str]
            - Returns the description text for the condition that is displayed in the display list.
        4. get_name(self) -> str
            - Returns "Level".
        5. get_diff(self, char_obj: str | Char = None) -> num
            - Returns the difference between the condition and the given character.
            - If the level difference is lower than -2, the difference is multiplied by 50.
            - If the level difference is lower than -1, the difference is multiplied by 20.
            - Otherwise the difference is returned as is.
        """

        def __init__(self, value: str | int, blocking: bool = False, *, char_obj: str | Char = None):
            super().__init__(blocking)
            self.value = value
            self.display_in_list = True
            self.display_in_desc = True
            self.char_obj = char_obj

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

            if super().is_fulfilled(**kwargs):
                return True

            char_obj = None
            if hasattr(self, 'char_obj'):
                char_obj = self.char_obj

            if isinstance(char_obj, str):
                char_obj = get_character_by_key(char_obj)

            if char_obj == None:
                char_obj = get_kwargs('char_obj', get_school(), **kwargs)

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
                return "Level: {color=#00a000}" + self.value + "{/color}"
            else:
                return "Level: {color=#a00000}" + self.value + "{/color}"

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
                return (
                    get_stat_icon("level", white = False), 
                    "{color=#00a000}" + str(self.value) + "{/color}", "Level"
                )
            else:
                return (
                    get_stat_icon("level", white = False), 
                    "{color=#a00000}" + str(self.value) + "{/color}", "Level"
                )

        def get_name(self):
            """
            Returns "Level".

            ### Returns:
            1. str
                - "Level".
            """

            return "Level"

        def get_diff(self, char_obj: str | Char = None) -> num:
            """
            Returns the difference between the condition and the given characters level.
            If the level difference is lower than -2, the difference is multiplied by 50.
            If the level difference is lower than -1, the difference is multiplied by 20.
            Otherwise the difference is returned as is.

            ### Parameters:
            1. char_obj: str | Char
                - The character to compare the condition to.
                - If the character is given as a key, the following keys are possible: school, parent, teacher, secretary
                - If the character is not given, the school character is used.

            ### Returns:
            1. num
                - The difference between the condition and the given characters level.
            """
            
            if isinstance(char_obj, str):
                char_obj = get_character_by_key(char_obj)
            if char_obj == None:
                char_obj = get_school()

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

        ### Attributes:
        1. value: int
            - The money that is checked.

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether the budget is within the condition.
        2. to_desc_text(self, **kwargs) -> str
            - Returns the description text for the condition that is displayed in the description.
        3. to_list_text(self, **kwargs) -> Tuple[str, str, str]
            - Returns the description text for the condition that is displayed in the display list.
        4. get_name(self) -> str
            - Returns "Money".
        """

        def __init__(self, value: str | num, blocking = False):
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

            if super().is_fulfilled(**kwargs):
                return True

            value = self.value
            if not isinstance(value, str):
                value = str(value) + "+"

            return self.value <= money.get_value()

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
                return "Money: {color=#00a000}" + str(self.value) + "{/color}"
            else:
                return "Money: {color=#a00000}" + str(self.value) + "{/color}"

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
                return (
                    get_stat_icon("money", white = False), 
                    "{color=#00a000}" + str(self.value) + "{/color}", "Money"
                )
            else:
                return (
                    get_stat_icon("money", white = False), 
                    "{color=#a00000}" + str(self.value) + "{/color}", "Money"
                )

        def get_name(self) -> str:
            """
            Returns "Money".

            ### Returns:
            1. str
                - "Money".
            """

            return "Money"

        def get_diff(self, char_obj: str | Char = None) -> num:
            if self.is_fulfilled():
                return 0
            return -5000

    class LockCondition(Condition):
        """
        A class for conditions that lock the object it is used in.
        This class makes unlocking the object impossible.
        If is_blocking is set to True, the object is also hidden.

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns "False" as the condition is never fulfilled.
        2. get_name(self) -> str
            - Returns "lock".
        """

        def __init__(self, is_blocking: bool = True):
            super().__init__(is_blocking)

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns "False" as the condition is never fulfilled.
            """

            if super().is_fulfilled(**kwargs):
                return True

            return False

        def get_name(self) -> str:
            """
            Returns "lock".

            ### Returns:
            1. str
                - "lock".
            """

            return "lock"

    class TimeCondition(Condition):
        """
        A class for conditions that check the time.

        ### Attributes:
        1. day: str
            - The day that is checked.
        2. week: str
            - The week that is checked.
        3. month: str
            - The month that is checked.
        4. year: str
            - The year that is checked.
        5. daytime: str
            - The daytime that is checked.
        6. weekday: str
            - The weekday that is checked.
        7. condition: str
            - The condition that is checked.
            - The condition can be "+", "-"
            - if none is given, the condition is "="

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether the current time fulfills the condition.
        2. to_desc_text(self, **kwargs) -> str
            - Returns the description text for the condition that is displayed in the description.
        3. get_name(self) -> str
            - Returns the time conditions as name.

        ### Parameters:
        1. blocking: bool
            - Whether the condition is blocking or not.
        2. **kwargs
            - Additional arguments.
            - day: str
                - The day that is checked.
            - week: str
                - The week that is checked.
            - month: str
                - The month that is checked.
            - year: str
                - The year that is checked.
            - daytime: str
                - The daytime that is checked.
            - weekday: str
                - The weekday that is checked.
            - condition: str
                - The condition that is checked.
                - The condition can be "+", "-"
                - if none is given, the condition is "="
            - date: datetime
                - The date that is checked.
                - overrides the day, week, month and year.
        """

        def __init__(self, blocking: bool = True, **kwargs: str | int):
            super().__init__(blocking)
            self.day       = "x" if 'day'       not in kwargs.keys() else kwargs['day'      ]
            self.week      = "x" if 'week'      not in kwargs.keys() else kwargs['week'     ]
            self.month     = "x" if 'month'     not in kwargs.keys() else kwargs['month'    ]
            self.year      = "x" if 'year'      not in kwargs.keys() else kwargs['year'     ]
            self.daytime   = "x" if 'daytime'   not in kwargs.keys() else kwargs['daytime'  ]
            self.weekday   = "x" if 'weekday'   not in kwargs.keys() else kwargs['weekday'  ]
            self.condition = ""  if 'condition' not in kwargs.keys() else kwargs['condition']
            
            if 'date' in kwargs.keys():
                date = kwargs['date']
                self.day    = str(date.get_day()) + str(condition)
                self.month  = str(date.get_month()) + str(condition)
                self.year   = str(date.get_year()) + str(condition)

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

            if super().is_fulfilled(**kwargs):
                return True

            return (
                time.check_day    (self.day    ) and
                time.check_month  (self.month  ) and
                time.check_year   (self.year   ) and
                time.check_week   (self.week   ) and
                time.check_daytime(self.daytime) and
                time.check_weekday(self.weekday))

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
                    text += " "
                text += f"{time.get_daytime_name(self.daytime)}"

            if self.is_fulfilled(**kwargs):
                return "Time is {color=#00a000}" + text + "{/color}"
            else:
                return "Time is {color=#a00000}" + text + "{/color}"

        def get_name(self) -> str:
            """
            Returns the time conditions as name.

            ### Returns:
            1. str
                - The time conditions as name.
            """

            return f"{self.day}:{self.week}:{self.month}:{self.year}:{self.daytime}:{self.weekday}"

    class TimerCondition(Condition):
        """
        A class for conditions that check if a timer has finished.

        ### Attributes:
        1. id: str
            - The id of the timer to locate it in the game data
        2. day: str
            - The amount of days that have to pass.
        3. month: str
            - The amount of months that have to pass.
        4. year: str
            - The amount of years that have to pass.
        5. daytime: str
            - The amount of time that has to pass.

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether the timer has finished.
        2. get_name(self) -> str
            - Returns the name of the condition.
        """

        def __init__(self, id: str, **kwargs: int):
            super().__init__(False)
            self.id = id
            self.day       = "x" if 'day'       not in kwargs.keys() else kwargs['day'    ]
            self.month     = "x" if 'month'     not in kwargs.keys() else kwargs['month'  ]
            self.year      = "x" if 'year'      not in kwargs.keys() else kwargs['year'   ]
            self.daytime   = "x" if 'daytime'   not in kwargs.keys() else kwargs['daytime']

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether the timer has finished.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            if super().is_fulfilled(**kwargs):
                return True

            if not contains_game_data(self.id):
                return False

            timer = get_game_data(self.id)
            if not isinstance(timer, Time):
                return False

            aim = Time(timer).add_time(day = self.day, month = self.month, year = self.year, daytime = self.daytime)
            return compare_time(aim, time) >= 0

        def get_name(self) -> str:
            """
            Returns the name of the condition.

            ### Returns:
            1. str
                - The name of the condition.
                - Example: Timer id5: 5:1:0:1
            """

            return f"Timer {self.id}: {self.day}:{self.month}:{self.year}:{self.daytime}"

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

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether the randomizer rolled a number lower than the amount.
        2. to_desc_text(self, **kwargs) -> str
            - Returns the description text for the condition that is displayed in the description.
        3. to_list_text(self, **kwargs) -> Tuple[str, str, str]
            - Returns the description text for the condition that is displayed in the display list.
        4. get_name(self) -> str
            - Returns the relation between the amount and the limit as name.
        5. get_diff(self, _char_obj) -> num
            - Returns the Probability as difference.
        """

        def __init__(self, threshold: num, limit: num = 100, blocking: bool = False):
            """
            The constructor for the RandomCondition class.

            ### Parameters:
            1. threshold: num
                - The value that acts as the border between fulfilled and not fulfilled.
                - If the random value is lower than the amount, the condition is fulfilled.
            2. limit: num
                - The limit of the random value.
                - The random value is generated between 0 and the limit.
            """

            super().__init__(blocking)
            self.amount = threshold
            self.limit  = limit
            self.display_in_desc = True
            self.display_in_list = True

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether the randomizer rolled a number lower than the threshold.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """
            if super().is_fulfilled(**kwargs):
                return True


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
        1. key: str
            - The key of the game data.
        2. value: Any
            - The value the game data has to match.

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether the game data matches the needed value.
        2. to_desc_text(self, **kwargs) -> str
            - Returns the description text for the condition that is displayed in the description.
        3. get_name(self) -> str
            - Returns the name of the condition.
        """

        def __init__(self, key: str, value: Any, blocking: bool = False):
            """
            The constructor for the GameDataCondition class.

            ### Parameters:
            1. key: str
                - The key of the game data.
            2. value: val | bool
                - The value the game data has to match.
            """

            super().__init__(blocking)
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

            if super().is_fulfilled(**kwargs):
                return True

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
                return get_translation(self.key) + " is {color=#00a000}" + str(self.value) + "{/color}"
            else:
                return get_translation(self.key) + " is {color=#a00000}" + str(self.value) + "{/color}"

        def get_name(self) -> str:
            """
            Returns the name of the condition.

            ### Returns:
            1. str
                - The name of the condition.
            """

            return get_translation(self.key)

    class ProgressCondition(Condition):
        """
        A class for conditions that check the progress of an event series.

        ### Attributes:
        1. key: str
            - The key of the progress.
        2. value: int | str
            - The value the progress has to match.

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether an event series has reached the needed progress level.
        2. to_desc_text(self, **kwargs) -> str
            - Returns the description text for the condition that is displayed in the description.
        3. get_name(self) -> str
            - Returns the name of the condition.
        """

        def __init__(self, key: str, value: int | str = "", blocking: bool = False):
            super().__init__(blocking)
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

            if super().is_fulfilled(**kwargs):
                return True

            if self.value == "":
                return get_progress(self.key) != -1

            return check_in_value(self.value, get_progress(self.key))

        def to_desc_text(self, **kwargs) -> str:
            """
            Returns the description text for the condition that is displayed in the description.

            ### Returns:
            1. str
                - The condition text for the description.
            """

            if self.is_fulfilled():
                return "Progress-level of {color=#3645e9}" + get_translation(self.key) + "{/color} is {color=#00a000}" + str(self.value) + "{/color}"
            else:
                return "Progress-level of {color=#3645e9}" + get_translation(self.key) + "{/color} is {color=#a00000}" + str(self.value) + "{/color}"

        def get_name(self) -> str:
            """
            Returns the name of the condition.
            """

            return get_translation(self.key)

    class ValueCondition(Condition):
        """
        A class for conditions that check the value of kwargs.

        ### Attributes:
        1. key: str
            - The key of the value for kwargs.
        2. value: Any
            - The value that is used to compare the value of kwargs.
            - If the value is a bool, the value of kwargs has to be True.
            - If the value is a val, the value of kwargs has to be equal to the given value.

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether a certain value of kwargs matches the needed value.
        2. to_desc_text(self, **kwargs) -> str
            - Returns the description text for the condition that is displayed in the description.
        3. get_name(self) -> str
            - Returns the name of the condition.
        """

        def __init__(self, key: str, value: Any, blocking: bool = False):
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

            if super().is_fulfilled(**kwargs):
                return True

            if "values" in kwargs.keys():
                return self.value == get_kwargs(self.key, **kwargs["values"])
            else:
                return self.value == get_kwargs(self.key, **kwargs)

        def to_desc_text(self, **kwargs) -> str:
            """
            Returns the description text for the condition that is displayed in the description.

            ### Returns:
            1. str
                - The condition text for the description.
            """

            if self.is_fulfilled(**kwargs):
                return get_translation(self.key) + " is {color=#00a000}" + str(self.value) + "{/color}"
            else:
                return get_translation(self.key) + " is {color=#a00000}" + str(self.value) + "{/color}"

        def get_name(self) -> str:
            """
            Returns the name of the condition.

            ### Returns:
            1. str
                - The name of the condition.
            """

            return get_translation(self.key)

    class NumValueCondition(Condition):
        """
        A class for conditions that check the value of kwargs by checking if the value is inside a ranged value.

        ### Attributes:
        1. key: str
            - The key of the value for kwargs.
        2. value: num | str | Selector
            - The value that is used to compare the value of kwargs.
            - If the value is a Selector, the value is rolled for every check.
        
        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether a certain value of kwargs is inside a ranged value.
        2. to_desc_text(self, **kwargs) -> str
            - Returns the description text for the condition that is displayed in the description.
        3. get_name(self) -> str
            - Returns the name of the condition.
        """

        def __init__(self, key: str, value: num | str | Selector, blocking: bool = False):

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

            if super().is_fulfilled(**kwargs):
                return True

            value = get_kwargs(self.key, **kwargs)

            if "values" in kwargs.keys():
                value = get_kwargs(self.key, value, **kwargs["values"])

            check_value = get_element(self.value, **kwargs)

            if not is_float(value):
                return False

            return check_in_value(str(check_value), value)

        def to_desc_text(self, **kwargs) -> str:
            """
            Returns the description text for the condition that is displayed in the description.

            ### Returns:
            1. str
                - The condition text for the description.
            """

            if self.is_fulfilled(**kwargs):
                return get_translation(self.key) + " is {color=#00a000}" + str(self.value) + "{/color}"
            else:
                return get_translation(self.key) + " is {color=#a00000}" + str(self.value) + "{/color}"

        def get_name(self) -> str:
            """
            Returns the name of the condition.

            ### Returns:
            1. str
                - The key of the value for kwargs.
            """

            return get_translation(self.key)

    class NumCompareCondition(Condition):
        """
        A class for conditions that check the value of kwargs by checking if the value comparison is fulfilled.

        ### Attributes:
        1. key: str
            - The key of the value for kwargs.
        2. value: val | Selector
            - The value that is used to compare the value of kwargs.
            - If the value is a Selector, the value is rolled for every check.
        3. operation: str
            - The operation that is used to compare the value of kwargs and the given value.
            - The following operations are available:
                - ">": The value of kwargs has to be larger than the given value.
                - ">=": The value of kwargs has to be larger than or equal to the given value.
                - "<": The value of kwargs has to be smaller than the given value.
                - "<=": The value of kwargs has to be smaller than or equal to the given value.
                - "==": The value of kwargs has to be equal to the given value.
                - "!=": The value of kwargs has to be not equal to the given value.

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether a certain value of kwargs is inside a ranged value.
        2. to_desc_text(self, **kwargs) -> str
            - Returns the description text for the condition that is displayed in the description.
        3. get_name(self) -> str
            - Returns the name of the condition.
        4. get_diff(self, _char_obj) -> num
            - Returns the difference between the condition and the value of kwargs.
            - The difference is based on the operation
            - For any greater or smaller than operator the difference is the difference between the value and the value of kwargs.
            - For the equal operator the difference is 0 if the value of kwargs is equal to the given value, otherwise it is -100.
            - For the not equal operator the difference is 0 if the value of kwargs is not equal to the given value, otherwise it is -100.
        """

        def __init__(self, key: str, value: num | Selector, operation: str, blocking: bool = False):
            """
            The constructor for the NumCompareCondition class.

            ### Parameters:
            1. key: str
                - The key of the value for kwargs.
            2. value: val | Selector
                - The value that is used to compare the value of kwargs.
                - If the value is a Selector, the value is rolled for every check.
            3. operation: str
                - The operation that is used to compare the value of kwargs and the given value.
                - The following operations are available:
                    - ">": The value of kwargs has to be larger than the given value.
                    - ">=": The value of kwargs has to be larger than or equal to the given value.
                    - "<": The value of kwargs has to be smaller than the given value.
                    - "<=": The value of kwargs has to be smaller than or equal to the given value.
                    - "==": The value of kwargs has to be equal to the given value.
                    - "!=": The value of kwargs has to be not equal to the given value.
            4. blocking: bool = False
                - Whether the condition is blocking or not.
            """

            super().__init__(blocking)
            self.key = key
            self.value = value
            self.operation = operation
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

            if super().is_fulfilled(**kwargs):
                return True

            check_value = get_kwargs_value(self.key, **kwargs)

            if check_value == None:
                return False

            value = get_element_num(self.value, **kwargs)

            if self.operation == ">":
                return check_value > value
            elif self.operation == ">=":
                return check_value >= value
            elif self.operation == "<":
                return check_value < value
            elif self.operation == "<=":
                return check_value <= value
            elif self.operation == "==":
                return check_value == value
            elif self.operation == "!=":
                return check_value != value
            return False

        def to_desc_text(self, **kwargs) -> str:
            """
            Returns the description text for the condition that is displayed in the description.

            ### Returns:
            1. str
                - The condition text for the description.
            """

            if self.is_fulfilled():
                return get_translation(self.key) + " " + self.operation + " {color=#00a000}" + self.value + "{/color}"
            else:
                return get_translation(self.key) + " " + self.operation + " {color=#a00000}" + self.value + "{/color}"

        def get_name(self) -> str:
            """
            Returns the name of the condition.

            ### Returns:
            1. str
                - The key of the value for kwargs.
            """

            return get_translation(self.key)

        def get_diff(self, _char_obj) -> num:
            """
            Returns the difference between the condition and the value of kwargs.
            The difference is based on the operation
            For any greater or smaller than operator the difference is the difference between the value and the value of kwargs.
            For the equal operator the difference is 0 if the value of kwargs is equal to the given value, otherwise it is -100.
            For the not equal operator the difference is 0 if the value of kwargs is not equal to the given value, otherwise it is -100.

            ### Returns:
            1. num
                - The difference between the condition and the value of kwargs.
            """

            if "values" not in kwargs.keys() or self.key not in kwargs["values"].keys():
                return -100
            value = self.value
            if isinstance(self.value, Selector):
                value = self.value.roll(**kwargs)
            if self.operation == ">":
                return kwargs["values"][self.key] - value
            elif self.operation == ">=":
                return kwargs["values"][self.key] - value
            elif self.operation == "<":
                return value - kwargs["values"][self.key]
            elif self.operation == "<=":
                return value - kwargs["values"][self.key]
            elif self.operation == "==":
                return 0 if kwargs["values"][self.key] == value else -100
            elif self.operation == "!=":
                return 0 if kwargs["values"][self.key] != value else -100
            return -100

    class CompareCondition(Condition):
        """
        A class for conditions that check the value of kwargs.

        ### Attributes:
        1. key: str
            - The key of the value for kwargs.
        2. value: val | Selector
            - The value that is used to compare the value of kwargs.
            - If the value is a Selector, the value is rolled for every check.

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether a certain value of kwargs is equal to a certain value.
        2. to_desc_text(self, **kwargs) -> str
            - Returns the description text for the condition that is displayed in the description.
        3. get_name(self) -> str
            - Returns the name of the condition.
        4. get_diff(self, _char_obj) -> num
            - Returns the difference between the condition and the value of kwargs.
            - If the condition is fulfilled, the difference is 0.
            - Otherwise the difference is -100.
        """

        def __init__(self, key: str, value: Any | Selector, blocking: bool = False):
            """
            The constructor for the CompareCondition class.

            ### Parameters:
            1. key: str
                - The key of the value for kwargs.
            2. value: Any | Selector
                - The value that is used to compare the value of kwargs.
                - If the value is a Selector, the value is rolled for every check.
            3. blocking: bool (default: False)
                - Whether the condition is blocking or not.
            """

            super().__init__(blocking)
            self.key = key
            self.value = value
            self.display_in_desc = True
            self.display_in_list = False

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether a certain value of kwargs is equal to a certain value.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            if super().is_fulfilled(**kwargs):
                return True

            if "values" not in kwargs.keys() or self.key not in kwargs["values"].keys():
                return False

            value = self.value

            if isinstance(self.value, Selector):
                value = self.value.roll(**kwargs)

            return kwargs["values"][self.key] == value

        def to_desc_text(self, **kwargs) -> str:
            """
            Returns the description text for the condition that is displayed in the description.

            ### Returns:
            1. str
                - The condition text for the description.
            """

            if self.is_fulfilled():
                return get_translation(self.key) + " equals {color=#00a000}" + self.value + "{/color}"
            else:
                return get_translation(self.key) + " equals {color=#a00000}" + self.value + "{/color}"

        def get_name(self) -> str:
            """
            Returns the name of the condition.

            ### Returns:
            1. str
                - The key of the value for kwargs.
            """

            return get_translation(self.key)

        def get_diff(self, _char_obj) -> num:
            """
            Returns the difference between the condition and the value of kwargs.
            If the condition is fulfilled, the difference is 0.
            Otherwise the difference is -100.

            ### Parameters:
            1. char_obj: Char
                - The character to compare the condition to.

            ### Returns:
            1. num
                - The difference between the condition and the value of kwargs.
            """

            if "values" not in kwargs.keys() or self.key not in kwargs["values"].keys():
                return -100
            value = self.value
            return 0 if kwargs["values"][self.key] == value else -100

    class KeyCompareCondition(Condition):
        """
        A class for conditions that check the value of kwargs by checking if the value is inside a ranged value.

        ### Attributes:
        1. key_1: str
            - The key of the value for kwargs.
        2. key_2: str
            - The key of the value for kwargs.
        3. operation: str
            - The operation that is used to compare the value of kwargs and the given value.
            - The following operations are available:
                - ">": The value of kwargs has to be larger than the given value.
                - ">=": The value of kwargs has to be larger than or equal to the given value.
                - "<": The value of kwargs has to be smaller than the given value.
                - "<=": The value of kwargs has to be smaller than or equal to the given value.
                - "==": The value of kwargs has to be equal to the given value.
                - "!=": The value of kwargs has to be not equal to the given value.

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether a certain value of kwargs is inside a ranged value.
        2. to_desc_text(self, **kwargs) -> str
            - Returns the description text for the condition that is displayed in the description.
        3. get_name(self) -> str
            - Returns the name of the condition.
        4. get_diff(self, _char_obj) -> num
            - Returns the difference between the condition and the value of kwargs.
            - The difference is based on the operator.
            - For any greater or smaller than operator the difference is the difference between the value and the value of kwargs.
            - For the equal operator the difference is 0 if the value of kwargs is equal to the given value, otherwise it is -100.
            - For the not equal operator the difference is 0 if the value of kwargs is not equal to the given value, otherwise it is -100.
        """

        def __init__(self, key_1: str, key_2: str, operation: str, blocking: bool = False):

            super().__init__(blocking)
            self.key_1 = key_1
            self.key_2 = key_2
            self.operation = operation
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

            if super().is_fulfilled(**kwargs):
                return True

            if "values" in kwargs.keys():
                kwargs = kwargs["values"]

            value_1 = kwargs["values"][self.key_1]
            value_2 = kwargs["values"][self.key_2]

            if isinstance(value_1, Selector):
                value_1 = value_1.roll(**kwargs)
            if isinstance(value_2, Selector):
                value_2 = value_2.roll(**kwargs)

            if self.operation == ">":
                return value_1 > value_2
            elif self.operation == ">=":
                return value_1 >= value_2
            elif self.operation == "<":
                return value_1 < value_2
            elif self.operation == "<=":
                return value_1 <= value_2
            elif self.operation == "==":
                return value_1 == value_2
            elif self.operation == "!=":
                return value_1 != value_2
            return False

        def get_name(self) -> str:
            """
            Returns the name of the condition.

            ### Returns:
            1. str
                - The key of the value for kwargs.
            """

            return f"{self.key_1} {self.operation} {self.key_2}"

        def get_diff(self, char_obj: Char) -> num:
            """
            Returns the difference between the condition and the value of kwargs.
            The difference is based on the operator.
            For any greater or smaller than operator the difference is the difference between the value and the value of kwargs.
            For the equal operator the difference is 0 if the value of kwargs is equal to the given value, otherwise it is -100.
            For the not equal operator the difference is 0 if the value of kwargs is not equal to the given value, otherwise it is -100.

            ### Returns:
            1. num
                - The difference between the condition and the value of kwargs.
            """

            if "values" not in kwargs.keys() or self.key_1 not in kwargs["values"].keys() or self.key_2 not in kwargs["values"].keys():
                return -100
            value_1 = kwargs["values"][self.key_1]
            value_2 = kwargs["values"][self.key_2]
            if isinstance(value_1, Selector):
                value_1 = value_1.roll(**kwargs)
            if isinstance(value_2, Selector):
                value_2 = value_2.roll(**kwargs)
            if self.operation == ">":
                return value_1 - value_2
            elif self.operation == ">=":
                return value_1 - value_2
            elif self.operation == "<":
                return value_2 - value_1
            elif self.operation == "<=":
                return value_2 - value_1
            elif self.operation == "==":
                return 0 if value_1 == value_2 else -100
            elif self.operation == "!=":
                return 0 if value_1 != value_2 else -100
            return -100

    class LoliContentCondition(Condition):
        """
        A class for conditions that check the value of kwargs by checking if the value is inside a ranged value.

        ### Attributes:
        1. value: int | str
            - The value that is used to compare the value of kwargs.
            - If the value is a Selector, the value is rolled for every check.

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether a certain value of kwargs is inside a ranged value.
        2. to_desc_text(self, **kwargs) -> str
            - Returns the description text for the condition that is displayed in the description.
        3. get_name(self) -> str
            - Returns the name of the condition.
        """

        def __init__(self, value: int | str, blocking: bool = False):
            """
            The constructor for the LoliContentCondition class.

            ### Parameters:
            1. value: int | str
                - The value that is used to compare the value of kwargs.
                - If the value is a Selector, the value is rolled for every check.
            2. blocking: bool (default: False)
                - Whether the condition is blocking or not.
            """

            super().__init__(blocking)
            self.value = value

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

            if super().is_fulfilled(**kwargs):
                return True

            return check_in_value(self.value, loli_content)

        def get_name(self) -> str:
            """
            Returns the name of the condition.

            ### Returns:
            1. str
                - The key of the value for kwargs.
            """

            return f"loli_content: {self.value}"

    class AND(Condition):
        """
        A class for conditions that check if all conditions are fulfilled.

        ### Attributes:
        1. *conditions: Condition
            - A list of all conditions that have to be ful
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

            if super().is_fulfilled(**kwargs):
                return True

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

        def get_diff(self, char_obj: str | Char = None):
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

            if super().is_fulfilled(**kwargs):
                return True

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

        def get_diff(self, char_obj: str | Char = None) -> num:
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

            if super().is_fulfilled(**kwargs):
                return True

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

        def get_diff(self, char_obj: str | Char = None) -> num:
            """
            Returns the difference of the condition with the lowest difference.

            ### Parameters:
            1. char_obj: str | Char
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

            if super().is_fulfilled(**kwargs):
                return True

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

        def get_diff(self, char_obj: str | Char) -> num:
            """
            Returns the difference of the added condition inverted.

            ### Parameters:
            1. char_obj: str | Char
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

            if super().is_fulfilled(**kwargs):
                return True

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

        def get_diff(self, char_obj: str | Char) -> num:
            """
            Returns the difference of the condition inverted.

            ### Parameters:
            1. char_obj: str | Char
                - The character to compare the condition to.

            ### Returns:
            1. num
                - The difference of the condition inverted.
            """

            diff = condition.get_diff(char_obj)

            return clamp_value(100 - diff, -100, 100)

    class IntroCondition(Condition):
        """
        A class for conditions that check if the game is currently in the introduction phase.

        ### Attributes:
        1. is_intro: bool
            - Whether the game is in the introduction phase
            - When True the condition is fulfilled when the game is in the introduction phase.
            - When False the condition is fulfilled when the game is not in the introduction phase.

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether the game is in the introduction phase.
        """

        def __init__(self, is_intro: bool = True):
            super().__init__(False)
            self.is_intro = is_intro

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether the game is in the introduction phase.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not
            """
            
            if super().is_fulfilled(**kwargs):
                return True

            if ((time.compare_today(10, 1, 2023) == -1 and self.is_intro) or
                (time.compare_today(10, 1, 2023) != -1 and not self.is_intro)):
                return True
            return False

        def get_name(self):
            return "IntroCondition"

    class PTAOverride(Condition):
        """
        A class for conditions that overrides all other conditions in the PTA voting.
        """

        def __init__(self, char: str = "", accept: str = "yes"):
            super().__init__(False)
            self.char = char
            self.accept = accept

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

            if super().is_fulfilled(**kwargs):
                return True

            return self.accept == "yes"

        def get_name(self) -> str:
            """
            Returns the name of the condition.
            Logic conditions are displayed in a special way.

            ### Returns:
            1. str
                - The name of the condition.
            """

            return f"PTAOverride({self.char}, {self.accept})"

        def get_diff(self, char_obj: str | Char) -> num:
            """
            Returns the difference of the condition inverted.

            ### Parameters:
            1. char_obj: str | Char
                - The character to compare the condition to.

            ### Returns:
            1. num
                - The difference of the condition inverted.
            """
            
            if isinstance(char_obj, str):
                char_obj = get_character_by_key(char_obj)
            if char_obj == None:
                char_obj = get_school()

            if self.char == "" or self.char == char_obj.get_name():
                if self.accept == "yes":
                    return 5000
                elif self.accept == "no":
                    return -100
                else:
                    return -5000
            return 0

    class CheckReplay(Condition):
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

            kwargs['check_in_replay'] = True

            return self.condition.is_fulfilled(**kwargs)

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

        def get_diff(self, char_obj: str | Char) -> num:
            """
            Returns the difference of the added condition inverted.

            ### Parameters:
            1. char_obj: str | Char
                - The character to compare the condition to.

            ### Returns:
            1. num
                - The difference of the added condition inverted.
            """

            diff = self.condition.get_diff(char_obj)

            return clamp_value(100 - diff, -100, 100)

    class EventSeenCondition(Condition):
        """
        A class for conditions that check if an event has been seen.
        """

        def __init__(self, seen: bool = False):
            super().__init__(False)
            self.seen = seen

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether the event has been seen.

            ### Parameters:
            1. **kwargs
                - Additional arguments.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            if super().is_fulfilled(**kwargs):
                return True

            return self.seen == get_event_seen(get_kwargs('event_name', **kwargs))

        def get_name(self) -> str:
            """
            Returns the name of the condition.

            ### Returns:
            1. str
                - The name of the condition.
            """

            return f"EventSeenCondition({self.event})"

    class JournalVoteCondition(Condition):
        """
        A class for conditions that check if a Journal Object is currently scheduled for voting.
        """

        def __init__(self, journal_obj: name):
            super().__init__(False)
            self._journal_obj = journal_obj
            global registered_vote_events

            registered_vote_events.append(journal_obj)

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Returns whether the Journal Object is currently scheduled for voting.

            ### Returns:
            1. bool
                - Whether the condition is fulfilled or not.
            """

            if super().is_fulfilled(**kwargs):
                return True

            vote_proposal = get_game_data('voteProposal')
            if vote_proposal == None:
                return False

            vote_obj = vote_proposal._journal_obj

            return self._journal_obj == vote_obj.get_name()

        def get_name(self) -> str:
            return f"JournalVoteCondition({self._journal_obj})"

    class JournalNRVoteCondition(Condition):
        """
        A class for conditions that check if a Journal Object has never been scheduled for voting.

        ### Methods:
        1. is_fulfilled(self, **kwargs) -> bool
            - Returns whether the Journal Object has never been scheduled for voting.
        2. get_name(self) -> str
            - Returns "JournalNRVoteCondition".

        ### Returns:
        1. bool
            - Whether the condition is fulfilled or not.
        """

        def __init__(self):
            super().__init__(False)

        def is_fulfilled(self, **kwargs) -> bool:
            if super().is_fulfilled(**kwargs):
                return True

            vote_proposal = get_game_data('voteProposal')
            if vote_proposal == None:
                return False

            vote_obj = vote_proposal._journal_obj

            return vote_obj.get_name() not in registered_vote_events

        def get_name(self) -> str:
            return "JournalNRVoteCondition"