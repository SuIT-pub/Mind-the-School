init -6 python:
    import re
    from abc import ABC, abstractmethod
    from typing import Union, List, Tuple, Dict

    def get_logic_condition_desc_text(is_fulfilled: bool, conditions: List[Condition], key: str, **kwargs) -> str:
        """Returns a formatted description text for a logic condition.

        Generates a description text for a logic condition (AND, OR, XOR, NOR) that shows
        whether the condition is fulfilled and includes descriptions of all sub-conditions.
        The text is formatted with colors to indicate fulfillment status.

        Args:
            is_fulfilled: Whether the overall logic condition is fulfilled.
            conditions: List of sub-conditions that are part of this logic condition.
            key: The type of logic condition (e.g. "AND", "OR", "XOR", "NOR").
            **kwargs: Additional keyword arguments passed to sub-condition descriptions.

        Returns:
            A formatted string containing the description text with color formatting.
            The text includes the logic condition type and descriptions of all sub-conditions.
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
        """A class that stores and manages a collection of conditions.

        This class handles storing, organizing and checking multiple conditions. It separates conditions
        into those that should be displayed in lists versus descriptions, and tracks whether any
        conditions are "locked".

        Attributes:
            conditions: List of all stored conditions.
            list_conditions: Conditions that should be displayed in UI lists.
            desc_conditions: Conditions that should be displayed in descriptions.
            is_locked: Whether any of the stored conditions is a lock condition.
            ignores: List of characters that should be ignored based on override conditions.

        Methods:
            get_is_locked(): Returns whether any condition is a lock condition.
            get_list_conditions(): Gets conditions meant for list display.
            get_desc_conditions(): Gets conditions meant for description display.
            get_desc_conditions_desc(**kwargs): Gets formatted description text.
            get_list_conditions_list(**kwargs): Gets formatted list text.
            get_conditions(): Gets all stored conditions.
            is_fulfilled(**kwargs): Checks if all conditions are fulfilled.
            is_blocking(**kwargs): Checks if any unfulfilled condition is blocking.
        """

        def __init__(self, *conditions: Condition):
            """Initializes the ConditionStorage with a set of conditions.

            The conditions are automatically sorted into display categories (list vs description)
            and checked for lock conditions.

            Args:
                *conditions: Variable number of Condition objects to store.
            """
            
            self.conditions = list(conditions)
            self.list_conditions = []
            self.desc_conditions = []
            self.ignores = []
            self.is_locked = False

            for condition in self.conditions:
                if isinstance(condition, LockCondition):
                    self.is_locked = True
                if condition.display_in_list:
                    self.list_conditions.append(condition)
                if condition.display_in_desc:
                    self.desc_conditions.append(condition)
                if isinstance(condition, PTAOverride) and condition.accept == 'ignore':
                    self.ignores.append(condition.char)                    

        def get_is_locked(self) -> bool:
            """Returns whether any stored conditions are lock conditions.

            This method checks if any of the conditions in storage are lock conditions,
            which was determined during initialization.

            Returns:
                bool: True if any stored condition is a lock condition, False otherwise.
            """

            return self.is_locked

        def get_list_conditions(self) -> List[Condition]:
            """Returns conditions marked for list display.

            Retrieves all conditions that were designated to be shown in UI lists
            during initialization.

            Returns:
                List[Condition]: List of conditions marked for list display.
            """

            return self.list_conditions

        def get_desc_conditions(self) -> List[Condition]:
            """Returns conditions marked for description display.

            Retrieves all conditions that were designated to be shown in descriptions
            during initialization.

            Returns:
                List[Condition]: List of conditions marked for description display.
            """

            return self.desc_conditions

        def get_desc_conditions_desc(self, **kwargs) -> str:
            """Formats and returns description text for description-type conditions.

            Generates formatted description text for all conditions marked for description display.
            Can optionally filter out blocking conditions.

            Args:
                **kwargs: Arbitrary keyword arguments.
                    blocking (bool): If True, excludes blocking conditions from output.

            Returns:
                list: List of formatted description strings for each relevant condition.
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
            """Formats and returns list text for list-type conditions.

            Generates formatted list text for all conditions marked for list display.
            Can optionally filter out blocking conditions.

            Args:
                **kwargs: Arbitrary keyword arguments.
                    blocking (bool): If True, excludes blocking conditions from output.

            Returns:
                list: List of formatted strings for each relevant condition.
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
            """Returns all stored conditions.

            Retrieves the complete list of all conditions stored in this container,
            regardless of their display type or lock status.

            Returns:
                List[Condition]: List of all stored conditions.
            """

            return self.conditions

        def is_fulfilled(self, **kwargs) -> bool:
            """Checks if all stored conditions are fulfilled.

            Evaluates each condition in storage and returns True only if all
            conditions are fulfilled according to their individual criteria.

            Args:
                **kwargs: Arbitrary keyword arguments passed to each condition's
                    is_fulfilled check.

            Returns:
                bool: True if all conditions are fulfilled, False otherwise.
            """

            for condition in self.conditions:
                if condition.is_fulfilled(**kwargs):
                    continue
                return False

            return True

        def is_blocking(self, **kwargs) -> bool:
            """Checks if any stored conditions are currently blocking.

            Evaluates each condition in storage to determine if any are in a blocking state.
            A blocking condition typically prevents certain actions or progression.

            Args:
                **kwargs: Arbitrary keyword arguments passed to each condition's
                    is_blocking check.

            Returns:
                bool: True if no conditions are blocking, False if any condition is blocking.
            """

            for condition in self.conditions:
                if condition.is_blocking(**kwargs):
                    return False
            return True

    class Condition(ABC):
        """Abstract base class for all condition types in the game.

        This class serves as the foundation for all condition types that can be checked
        in the game. Conditions can be used to control game flow, unlock content,
        and validate game state. Each condition can be marked as blocking, which affects
        whether content is hidden when the condition is not met.

        Attributes:
            blocking: Whether the condition blocks content when not fulfilled.
            display_in_list: Whether the condition should appear in UI lists.
            display_in_desc: Whether the condition should appear in descriptions.

        Methods:
            is_fulfilled(**kwargs): Checks if the condition is met.
            is_blocking(**kwargs): Checks if condition is blocking and unfulfilled.
            is_set_blocking(): Returns whether condition was set as blocking.
            to_list_text(**kwargs): Gets text representation for list display.
            to_desc_text(**kwargs): Gets text representation for description display.
            get_name(): Gets the condition's name.
            get_diff(char_obj): Gets numerical difference from target value.
        """

        def __init__(self, blocking: bool = False, *options: Option):
            """Initializes a new Condition.

            Args:
                blocking: Whether this condition should block content when not fulfilled.
                    Defaults to False.
            """
            self.blocking = blocking
            self.display_in_list = False
            self.display_in_desc = False

            self.options = OptionSet(*options)

        def get_option_set(self):
            if self.options == None:
                return empty_option_set
            return self.options

        def is_fulfilled(self, **kwargs) -> bool:
            """Checks if the condition is currently fulfilled.

            This base implementation handles replay mode checks. Subclasses should
            override this to implement their specific fulfillment logic.

            Args:
                **kwargs: Additional arguments that may affect condition checking.
                    Commonly used kwargs:
                    - check_in_replay: Whether to check during replay mode
                    - in_replay: Whether currently in replay mode
                    - in_journal_gallery: Whether in journal gallery view

            Returns:
                True if condition is fulfilled or in replay mode, False otherwise.
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
            """Checks if the condition is both blocking and unfulfilled.

            A condition is considered blocking if it is both marked as a blocking condition
            and is currently unfulfilled. This is used to determine if content should
            be hidden or inaccessible.

            Args:
                **kwargs: Additional arguments passed to is_fulfilled check.

            Returns:
                bool: True if condition is both blocking and unfulfilled, False otherwise.
            """

            return (not self.is_fulfilled(**kwargs) and self.blocking)

        def is_set_blocking(self) -> bool:
            """Checks if this condition was initialized as a blocking condition.

            This differs from is_blocking() in that it only checks the blocking flag,
            not whether the condition is currently fulfilled.

            Returns:
                bool: True if this condition was set as blocking during initialization,
                    False otherwise.
            """

            return self.blocking

        def to_list_text(self, **kwargs) -> Union[Tuple[str, str], Tuple[str, str, str], List[Union[Tuple[str, str], Tuple[str, str, str]]]]:
            """Generates formatted text for displaying the condition in list form.

            Creates a tuple or list of tuples containing display information for UI lists.
            The base implementation returns an empty tuple. Subclasses should override
            this to provide meaningful list display text.

            Args:
                **kwargs: Additional arguments that may affect text formatting.

            Returns:
                Union[Tuple[str, str], Tuple[str, str, str], List[Union[Tuple[str, str], Tuple[str, str, str]]]]:
                    A tuple or list of tuples containing:
                    - Icon path (str)
                    - Display value (str)
                    - Optional title (str)
                    Base implementation returns ("", "").
            """

            return ("", "")

        def to_desc_text(self, **kwargs) -> Union[str, List[str]]:
            """Generates formatted text for displaying the condition in description form.

            Creates a text representation of the condition suitable for descriptive displays.
            The base implementation returns the condition's name. Subclasses should override
            this to provide more detailed description text.

            Args:
                **kwargs: Additional arguments that may affect text formatting.

            Returns:
                Union[str, List[str]]: A string or list of strings containing the formatted
                    description. Base implementation returns result of get_name().
            """

            return self.get_name()

        @abstractmethod
        def get_name(self) -> str:
            """Gets a human-readable identifier for this condition.

            This abstract method must be implemented by all subclasses to provide
            a meaningful name or identifier for the condition.

            Returns:
                str: A string identifying this condition type.

            Raises:
                NotImplementedError: If the subclass does not implement this method.
            """

            pass

        def get_diff(self, char_obj: Union[str, Char]) -> int:
            """Calculates how far a character is from fulfilling this condition.

            Computes a numerical score representing how close a character is to
            meeting this condition's requirements. The base implementation returns
            0 if fulfilled, -100 if not. Subclasses should override this to provide
            more granular difference calculations.

            Args:
                char_obj (Union[str, Char]): The character to evaluate. Can be either
                    a character object or a character key string.

            Returns:
                int: 0 if the condition is fulfilled for the character, -100 otherwise.
                Subclasses may return other values to indicate partial fulfillment.
            """

            if self.is_fulfilled(char_obj = char_obj):
                return 0
            return -100

    class StatCondition(Condition):
        """A condition class that evaluates character statistics against specified thresholds.

        This class allows for checking one or multiple stats of a character against defined values.
        It supports both single and multiple stat comparisons, with customizable display options
        for UI elements.

        Attributes:
            stats (Dict[str, int]): Dictionary mapping stat names to their required values.
            char_obj (Char): The character object whose stats are being checked. If None,
                defaults to the school character.
            display_in_list (bool): Whether to show this condition in list displays.
            display_in_desc (bool): Whether to show this condition in descriptions.

        Note:
            The class inherits from the base Condition class and extends its functionality
            specifically for stat-based checks.
        """

        def __init__(self, blocking: bool = False, *options: Option, char_obj = None, **kwargs):
            """Initialize a new StatCondition.

            Args:
                blocking (bool, optional): Whether this condition blocks progression.
                    Defaults to False.
                char_obj (Union[str, Char, None]): The character to check stats for. Can be
                    a character object, character key, or None. Defaults to None.
                **kwargs: Stat requirements passed as key-value pairs where keys are stat
                    names and values are the required levels.
            """
            super().__init__(blocking, *options)
            self.stats = kwargs
            self.display_in_list = True
            self.display_in_desc = True

            self.char_obj = char_obj
            if isinstance(char_obj, str):
                self.char_obj = get_character_by_key(char_obj)
            
        def is_fulfilled(self, **kwargs) -> bool:
            """Check if all specified stat conditions are met.

            Verifies that the character's stats meet or exceed all specified thresholds
            defined in self.stats.

            Args:
                **kwargs: Additional arguments. May include 'char_obj' to specify which
                    character to check.

            Returns:
                bool: True if all stat conditions are met, False otherwise.

            Note:
                If self.char_obj is set and doesn't match the provided char_obj,
                the method returns True to skip the check.
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

            if self.char_obj != None and self.char_obj != char_obj:
                return True

            for stat in self.stats.keys():
                stat_key = get_element(stat)
                if not char_obj.check_stat(stat, self.stats[stat]):
                    return False

            return True
        
        def to_list_text(self, **kwargs) -> Union[Tuple[str, str], Tuple[str, str, str], List[Union[Tuple[str, str], Tuple[str, str, str]]]]:
            """Generate formatted text for displaying the condition in a list view.

            Creates color-coded text representations of stat requirements, with green
            for met conditions and red for unmet ones.

            Args:
                **kwargs: Additional arguments. Should include 'char_obj' to specify
                    which character's stats to check against.

            Returns:
                Union[Tuple[str, str], Tuple[str, str, str], List[Union[Tuple[str, str], Tuple[str, str, str]]]]:
                    A tuple or list of tuples containing:
                    - Icon path (str)
                    - Formatted value (str)
                    - Optional title (str)
                    Returns empty tuple if no character object is provided.
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

        def to_desc_text(self, **kwargs) -> Union[str, List[str]]:
            """Generate formatted text for displaying the condition in a description.

            Creates a detailed text representation of stat requirements with color coding:
            green for met conditions and red for unmet ones.

            Args:
                **kwargs: Additional arguments. May include 'char_obj' to specify which
                    character's stats to check against.

            Returns:
                Union[str, List[str]]: A string or list of strings containing the formatted
                    description. Returns empty string if no stats are defined.
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
            """Get a human-readable name for this condition.

            Creates a comma-separated list of all stat names being checked by this condition.

            Returns:
                str: A comma-separated string of stat titles.
            """

            return ', '.join([Stat_Data[key].get_title() for key in self.stats.keys()])

        def get_diff(self, char_obj: Union[str, Char] = None) -> int:
            """Calculate the weighted difference between required and actual stat values.

            Computes a score based on how far the character's stats are from the required values.
            The scoring system applies different multipliers based on the magnitude of the difference:
            - Differences below -20: multiplied by 20
            - Differences between -20 and -10: multiplied by 10
            - Differences between -10 and 0: multiplied by 5
            - Differences between 0 and 5: no multiplier
            - Differences above 5: multiplied by 2

            Args:
                char_obj (Union[str, Char, None]): The character to compare stats against.
                    Can be a character object, character key, or None (defaults to school).

            Returns:
                int: The weighted difference score. Starts at 100 and is modified by
                    the weighted differences. Returns 0 if character objects don't match
                    when self.char_obj is set.
            """

            if isinstance(char_obj, str):
                char_obj = get_character_by_key(char_obj)
            if char_obj == None:
                char_obj = get_school()

            if self.char_obj != None and self.char_obj != char_obj:
                return 0

            output = 100
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
        """A condition class that checks if a character's stat has reached its level-based cap.

        This class specifically handles checking whether Corruption or Inhibition stats
        have reached their maximum/minimum values, which are determined by the character's level.
        For Corruption, the cap is (level * 10) up to 100.
        For Inhibition, the cap is (100 - level * 10) down to 0.

        Attributes:
            _stat (str): The stat to check. Must be either CORRUPTION or INHIBITION.
            _char_obj (Char): The character whose stat cap is being checked.
            display_in_list (bool): Whether to show this condition in list displays.
                Defaults to False.
            display_in_desc (bool): Whether to show this condition in descriptions.
                Defaults to False.
        """

        def __init__(self, stat: str, blocking: bool = False, char_obj: Union[str, Char] = None, *options: Option, **kwargs):
            """Initialize a new StatLimitCondition.

            Args:
                stat (str): The stat to check for limit. Must be either CORRUPTION
                    or INHIBITION.
                char_obj (Union[str, Char, None], optional): The character to check stats for.
                    Can be a character object, character key, or None. Defaults to None.
                **kwargs: Additional arguments passed to parent Condition class.
            """
            super().__init__(blocking, *options)
            self._stat = stat
            self._char_obj = char_obj
            self.display_in_list = False
            self.display_in_desc = False

        def is_fulfilled(self, **kwargs) -> bool:
            """Check if the specified stat has reached its level-based cap.

            For Corruption, checks if the stat has reached (level * 10) up to max 100.
            For Inhibition, checks if the stat has reached (100 - level * 10) down to min 0.

            Args:
                **kwargs: Additional arguments. May include 'char_obj' to specify which
                    character to check if _char_obj is not set.

            Returns:
                bool: True if the stat has reached its level-based cap, False otherwise.
                Also returns True if parent condition is fulfilled, False for invalid stats.
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
            """Get a human-readable name for this condition.

            Returns:
                str: Either "Corruption limit" or "Inhibition limit" based on the
                    stat being checked. Returns empty string for invalid stats.
            """

            if self._stat == CORRUPTION:
                return "Corruption limit"
            elif self._stat == INHIBITION:
                return "Inhibition limit"
            return ""

    class ProficiencyCondition(Condition):
        """A condition class that evaluates the headmaster's proficiency levels and experience.

        This class checks whether the headmaster has achieved specific proficiency requirements,
        which can include both experience points (XP) and level thresholds. The condition can
        check for either or both metrics, or simply verify if a proficiency exists.

        Attributes:
            _proficiency (str): The proficiency type to check (e.g., 'Math', 'Science', etc.).
            _xp (Union[int, str]): The required XP threshold. Can be a specific value or a
                comparison string (e.g., '>=100'). Set to -1 to skip XP check.
            _level (Union[int, str]): The required level threshold. Can be a specific value
                or a comparison string (e.g., '>=3'). Set to -1 to skip level check.
            blocking (bool): Always True for this condition type, making it a blocking
                condition by default.

        Note:
            When both XP and level are set to -1, the condition only checks if the
            proficiency exists in the headmaster's proficiency list.
        """

        def __init__(self, proficiency: str, *options: Option, xp: Union[int, str] = -1, level: Union[int, str] = -1):
            """Initialize a new ProficiencyCondition.

            Args:
                proficiency (str): The proficiency type to check.
                xp (Union[int, str], optional): The required XP threshold. Use -1 to
                    skip XP check. Can be a number or comparison string. Defaults to -1.
                level (Union[int, str], optional): The required level threshold. Use -1 to
                    skip level check. Can be a number or comparison string. Defaults to -1.
            """
            super().__init__(True, *options)
            self._proficiency = proficiency
            self._xp = xp
            self._level = level

        def is_fulfilled(self, **kwargs) -> bool:
            """Check if the headmaster meets the proficiency requirements.

            Evaluates whether the headmaster's proficiency meets the specified conditions:
            1. If both XP and level are -1, only checks if the proficiency exists
            2. If XP is specified, checks if current XP meets the requirement
            3. If level is specified, checks if current level meets the requirement

            Args:
                **kwargs: Additional arguments (unused in this implementation).

            Returns:
                bool: True if all specified conditions are met (proficiency exists and
                    meets any XP/level requirements), False otherwise.
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
            """Generate a string identifier for this proficiency condition.

            Creates a unique identifier string that includes the proficiency type
            and the XP/level requirements.

            Returns:
                str: A string in the format "proficiency_xp_level" where:
                    - proficiency is the proficiency type
                    - xp is the XP requirement or -1
                    - level is the level requirement or -1
                Example: "Math_100_-1" for Math proficiency with XP >= 100 and no level requirement
            """

            return self._proficiency + "_" + str(self._xp) + "_" + str(self._level)

    class TutorialCondition(Condition):
        """A condition class that checks if the game's tutorial mode is active.

        This class provides a simple check for whether the tutorial mode is currently
        enabled in the game. It is always a blocking condition.

        Attributes:
            blocking (bool): Always True for this condition type, making it a blocking
                condition by default.
        """

        def __init__(self, *options: Option):
            """Initialize a new TutorialCondition.

            The condition is always initialized as blocking (True).
            """
            super().__init__(True, *options)

        def is_fulfilled(self, **kwargs) -> bool:
            """Check if the tutorial mode is currently active.

            Args:
                **kwargs: Additional arguments (unused in this implementation).

            Returns:
                bool: True if the tutorial mode is active, False otherwise.
            """
            return persistent.tutorial

        def get_name(self) -> str:
            """Get a human-readable identifier for this condition.

            Returns:
                str: The string "Is_tutorial_active".
            """
            return "Is_tutorial_active"

    class RuleCondition(Condition):
        """A condition class that checks if a specific game rule is active for a character.

        This class verifies whether a particular rule, identified by its key, has been
        unlocked in the game. Rules can be displayed in descriptions and their status
        (locked/unlocked) affects the game's progression.

        Attributes:
            value (str): The unique key identifier for the rule being checked.
            display_in_desc (bool): Whether to show this condition in descriptions.
                Always True for rule conditions.
            blocking (bool): Whether this condition blocks progression when not fulfilled.
                Set during initialization.

        Note:
            Rules must exist in the global rules dictionary to be valid. Invalid rule
            keys will result in empty names and may affect condition fulfillment.
        """

        def __init__(self, value: str, blocking: bool = False, *options: Option):
            """Initialize a new RuleCondition.

            Args:
                value (str): The unique key identifier for the rule to check.
                blocking (bool, optional): Whether this condition should block
                    progression when not fulfilled. Defaults to False.
            """
            super().__init__(blocking, *options)
            self.value = value
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """Check if the specified rule is currently unlocked.

            Args:
                **kwargs: Additional arguments (unused in this implementation).

            Returns:
                bool: True if either:
                    - The parent condition is fulfilled
                    - The specified rule is unlocked
                    False otherwise.
            """
            if super().is_fulfilled(**kwargs):
                return True

            return get_rule(self.value).is_unlocked()

        def to_desc_text(self, **kwargs) -> str:
            """Generate formatted text describing the rule's unlock status.

            Creates a colored text representation of the rule's status:
            - Green text for unlocked rules
            - Red text for locked rules

            Args:
                **kwargs: Additional arguments (unused in this implementation).

            Returns:
                str: A formatted string in the format "Rule {color}RuleName{/color} is unlocked"
                    where the color is green (#00a000) for unlocked rules and red (#a00000)
                    for locked rules.
            """
            if self.is_fulfilled(**kwargs):
                return "Rule {color=#00a000}" + get_rule(self.value).get_title() + "{/color} is unlocked"
            else:
                return "Rule {color=#a00000}" + get_rule(self.value).get_title() + "{/color} is unlocked"

        def get_name(self) -> str:
            """Get the display title of the rule being checked.

            Returns:
                str: The title of the rule if it exists in the rules dictionary,
                    empty string if the rule key is invalid.
            """
            if self.value not in rules.keys():
                return ""
            return get_rule(self.value).get_title()

    class ClubCondition(Condition):
        """A condition that checks if a specific club is unlocked and active.

        This condition validates whether a particular club has been unlocked in the
        current game state. Clubs are identified by their unique keys and can affect
        various aspects of gameplay and student activities when active.

        Attributes:
            value: The unique key identifying the club to check.
            display_in_desc: Always True for club conditions.
            blocking: Whether this club blocks content when not fulfilled.

        Methods:
            is_fulfilled(**kwargs): Checks if the club is unlocked.
            to_desc_text(**kwargs): Gets colored text showing club status.
            get_name(): Gets the club's display title.
        """

        def __init__(self, value: str, blocking: bool = False, *options: Option):
            """Initializes a new ClubCondition.

            Args:
                value: The unique key identifying the club to check.
                blocking: Whether this club should block content when not fulfilled.
                    Defaults to False.
            """
            super().__init__(blocking, *options)
            self.value = value
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """Checks if the club is currently unlocked.

            Args:
                **kwargs: Additional arguments that may affect condition checking.

            Returns:
                True if the club is unlocked, False otherwise.
            """
            if super().is_fulfilled(**kwargs):
                return True
            return get_club(self.value).is_unlocked()

        def to_desc_text(self, **kwargs) -> str:
            """Gets a colored text description of the club's status.

            The text includes the club's title and is colored green if unlocked,
            red if locked.

            Args:
                **kwargs: Additional arguments that may affect text formatting.

            Returns:
                A formatted string with the club's title and colored status indicator.
            """
            if self.is_fulfilled(**kwargs):
                return "Club {color=#00a000}" + get_club(self.value).get_title() + "{/color} is unlocked"
            else:
                return "Club {color=#a00000}" + get_club(self.value).get_title() + "{/color} is unlocked"

        def get_name(self) -> str:
            """Gets the display title of the club.

            Returns:
                The club's title if it exists in the clubs dictionary, empty string otherwise.
            """
            if self.value not in clubs.keys():
                return ""
            return get_club(self.value).title

    class BuildingCondition(Condition):
        """A condition class that checks if a specific building is unlocked.

        This class verifies whether a particular building, identified by its key,
        has been unlocked in the game. Buildings can be displayed in descriptions
        and their unlock status affects game progression.

        Attributes:
            value (str): The unique key identifier for the building to check.
            display_in_desc (bool): Whether to show this condition in descriptions.
                Always True for building conditions.
            blocking (bool): Whether this condition blocks progression when not fulfilled.
                Set during initialization.

        Note:
            Buildings must exist in the global buildings dictionary to be valid.
            Invalid building keys will result in empty names.
        """

        def __init__(self, value: str, blocking: bool = False, *options: Option):
            """Initialize a new BuildingCondition.

            Args:
                value (str): The unique key identifier for the building to check.
                blocking (bool, optional): Whether this condition should block
                    progression when not fulfilled. Defaults to False.
            """
            super().__init__(blocking, *options)
            self.value = value
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """Check if the specified building is currently unlocked.

            Args:
                **kwargs: Additional arguments (unused in this implementation).

            Returns:
                bool: True if either:
                    - The parent condition is fulfilled
                    - The specified building is unlocked
                    False otherwise.
            """
            if super().is_fulfilled(**kwargs):
                return True

            return get_building(self.value).is_unlocked()

        def to_desc_text(self, **kwargs) -> str:
            """Generate formatted text describing the building's unlock status.

            Creates a colored text representation of the building's status:
            - Green text for unlocked buildings
            - Red text for locked buildings

            Args:
                **kwargs: Additional arguments (unused in this implementation).

            Returns:
                str: A formatted string in the format "Building {color}BuildingName{/color} is unlocked"
                    where the color is green (#00a000) for unlocked buildings and red (#a00000)
                    for locked buildings.
            """
            if self.is_fulfilled(**kwargs):
                return "Building {color=#00a000}" + get_building(self.value).get_title() + "{/color} is unlocked"
            else:
                return "Building {color=#a00000}" + get_building(self.value).get_title() + "{/color} is unlocked"

        def get_name(self) -> str:
            """Get the display title of the building being checked.

            Returns:
                str: The title of the building if it exists in the buildings dictionary,
                    empty string if the building key is invalid.
            """
            if self.value not in buildings.keys():
                return ""
            return get_building(self.value).get_title()

    class BuildingLevelCondition(Condition):
        """A condition class that checks if a building has reached a specific level.

        This class verifies whether a particular building has reached or exceeded a
        required level threshold. The level requirement can be specified either as
        an exact value or as a comparison string (e.g., '>=2').

        Attributes:
            name (str): The unique key identifier for the building to check.
            level (Union[str, int]): The required level threshold. Can be a specific
                value or a comparison string.
            display_in_desc (bool): Whether to show this condition in descriptions.
                Always True for building level conditions.
            blocking (bool): Whether this condition blocks progression when not fulfilled.
                Set during initialization.

        Note:
            Buildings must exist in the global buildings dictionary to be valid.
            Invalid building keys will result in empty names.
        """

        def __init__(self, name: str, level: Union[str, int], blocking: bool = False, *options: Option):
            """Initialize a new BuildingLevelCondition.

            Args:
                name (str): The unique key identifier for the building to check.
                level (Union[str, int]): The required level threshold. Can be a number
                    or comparison string (e.g., '>=2', '<4').
                blocking (bool, optional): Whether this condition should block
                    progression when not fulfilled. Defaults to False.
            """
            super().__init__(blocking, *options)
            self.name = name
            self.level = level
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """Check if the building meets the level requirement.

            Args:
                **kwargs: Additional arguments (unused in this implementation).

            Returns:
                bool: True if either:
                    - The parent condition is fulfilled
                    - The building's current level meets the level requirement
                    False otherwise.
            """
            if super().is_fulfilled(**kwargs):
                return True

            return check_in_value(self.level, get_building(self.name).get_level())

        def to_desc_text(self, **kwargs) -> str:
            """Generate formatted text describing the building's level status.

            Creates a colored text representation showing both the building name
            and its level requirement:
            - Green text when level requirement is met
            - Red text when level requirement is not met

            Args:
                **kwargs: Additional arguments (unused in this implementation).

            Returns:
                str: A formatted string showing building name and level requirement,
                    with appropriate color coding (green #00a000 or red #a00000).
            """
            if self.is_fulfilled(**kwargs):
                return "Building {color=#00a000}" + get_building(self.name).get_title() + "{/color} is at level {color=#00a000}" + str(self.level) + "{/color}"
            else:
                return "Building {color=#a00000}" + get_building(self.name).get_title() + "{/color} is at level {color=#a00000}" + str(self.level) + "{/color}"

        def get_name(self) -> str:
            """Get the display title of the building being checked.

            Returns:
                str: The title of the building if it exists in the buildings dictionary,
                    empty string if the building key is invalid.
            """
            if self.name not in buildings.keys():
                return ""
            return get_building(self.name).title

    class LevelCondition(Condition):
        """A condition class that checks if a character has reached a specific level.

        This class verifies whether a character has reached or exceeded a required level
        threshold. The level requirement can be specified either as an exact value or
        as a comparison string (e.g., '>=5'). The condition can be applied to a specific
        character or use a default character from the context.

        Attributes:
            value (Union[str, int]): The required level threshold. Can be a specific
                value or a comparison string.
            char_obj (Union[str, Char, None]): The character whose level is being checked.
                If None, defaults to the school character.
            display_in_list (bool): Whether to show this condition in list displays.
                Always True for level conditions.
            display_in_desc (bool): Whether to show this condition in descriptions.
                Always True for level conditions.
            blocking (bool): Whether this condition blocks progression when not fulfilled.

        Note:
            When calculating differences between levels, larger gaps result in
            increasingly severe penalties to encourage proper level progression.
        """

        def __init__(self, value: Union[str, int], blocking: bool = False, *options: Option, char_obj: Union[str, Char] = None):
            """Initialize a new LevelCondition.

            Args:
                value (Union[str, int]): The required level threshold. Can be a number
                    or comparison string (e.g., '>=5', '<10').
                blocking (bool, optional): Whether this condition should block
                    progression when not fulfilled. Defaults to False.
                char_obj (Union[str, Char, None], optional): The character to check level for.
                    Can be a character object, character key, or None. Defaults to None.
            """
            super().__init__(blocking, *options)
            self.value = value
            self.display_in_list = True
            self.display_in_desc = True
            self.char_obj = char_obj

        def is_fulfilled(self, **kwargs) -> bool:
            """Check if the character meets the level requirement.

            Args:
                **kwargs: Additional arguments. May include 'char_obj' to specify which
                    character to check if self.char_obj is not set.

            Returns:
                bool: True if either:
                    - The parent condition is fulfilled
                    - The character's current level meets the level requirement
                    False otherwise.
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
            """Generate formatted text describing the level requirement status.

            Creates a colored text representation of the level requirement:
            - Green text when level requirement is met
            - Red text when level requirement is not met

            Args:
                **kwargs: Additional arguments (unused in this implementation).

            Returns:
                str: A formatted string in the format "Level: {color}X{/color}"
                    where X is the required level and the color is green (#00a000)
                    when met or red (#a00000) when not met.
            """
            if self.is_fulfilled(**kwargs):
                return "Level: {color=#00a000}" + self.value + "{/color}"
            else:
                return "Level: {color=#a00000}" + self.value + "{/color}"

        def to_list_text(self, **kwargs) -> Tuple[str, str, str]:
            """Generate formatted text for displaying the condition in a list view.

            Creates a tuple containing an icon and colored text representation
            of the level requirement.

            Args:
                **kwargs: Additional arguments (unused in this implementation).

            Returns:
                Tuple[str, str, str]: A tuple containing:
                    - The level icon path
                    - The colored level value (green when met, red when not)
                    - The string "Level"
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

        def get_name(self) -> str:
            """Get a human-readable identifier for this condition.

            Returns:
                str: The string "Level".
            """
            return "Level"

        def get_diff(self, char_obj: Union[str, Char] = None) -> int:
            """Calculate the weighted difference between required and actual level.

            Computes a score based on how far the character's level is from the required level.
            The scoring system applies different multipliers based on the magnitude of the difference:
            - Differences below -2: multiplied by 50
            - Differences below -1: multiplied by 20
            - Other differences: no multiplier

            Args:
                char_obj (Union[str, Char, None]): The character to compare levels against.
                    Can be a character object, character key, or None (defaults to school).

            Returns:
                int: The weighted difference score. Larger negative differences result
                    in more severe penalties to encourage proper level progression.
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
        """A condition class that checks if the available money meets a threshold.

        This class verifies whether the current money/budget meets or exceeds a
        specified threshold. The requirement can be specified either as an exact
        value or as a comparison string (e.g., '>=1000').

        Attributes:
            value (Union[str, num]): The required money threshold. Can be a specific
                value or a comparison string.
            display_in_list (bool): Whether to show this condition in list displays.
                Always True for money conditions.
            display_in_desc (bool): Whether to show this condition in descriptions.
                Always True for money conditions.
            blocking (bool): Whether this condition blocks progression when not fulfilled.

        Note:
            When specified as a number rather than a comparison string, the condition
            automatically treats it as a minimum requirement (value+).
        """

        def __init__(self, value: Union[str, num], blocking: bool = False, *options: Option):
            """Initialize a new MoneyCondition.

            Args:
                value (Union[str, num]): The required money threshold. Can be a number
                    (treated as minimum) or comparison string (e.g., '>=1000').
                blocking (bool, optional): Whether this condition should block
                    progression when not fulfilled. Defaults to False.
            """
            super().__init__(blocking, *options)
            self.value = value
            self.display_in_list = True
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """Check if the current money meets the requirement.

            If the value is specified as a number rather than a comparison string,
            it is treated as a minimum requirement (value+).

            Args:
                **kwargs: Additional arguments (unused in this implementation).

            Returns:
                bool: True if either:
                    - The parent condition is fulfilled
                    - The current money meets or exceeds the requirement
                    False otherwise.
            """
            if super().is_fulfilled(**kwargs):
                return True

            value = self.value
            if not isinstance(value, str):
                value = str(value) + "+"

            return self.value <= money.get_value()

        def to_desc_text(self, **kwargs) -> str:
            """Generate formatted text describing the money requirement status.

            Creates a colored text representation of the money requirement:
            - Green text when money requirement is met
            - Red text when money requirement is not met

            Args:
                **kwargs: Additional arguments (unused in this implementation).

            Returns:
                str: A formatted string in the format "Money: {color}X{/color}"
                    where X is the required amount and the color is green (#00a000)
                    when met or red (#a00000) when not met.
            """
            if self.is_fulfilled():
                return "Money: {color=#00a000}" + str(self.value) + "{/color}"
            else:
                return "Money: {color=#a00000}" + str(self.value) + "{/color}"

        def to_list_text(self, **kwargs) -> Tuple[str, str, str]:
            """Generate formatted text for displaying the condition in a list view.

            Creates a tuple containing an icon and colored text representation
            of the money requirement.

            Args:
                **kwargs: Additional arguments (unused in this implementation).

            Returns:
                Tuple[str, str, str]: A tuple containing:
                    - The money icon path
                    - The colored money value (green when met, red when not)
                    - The string "Money"
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
            """Get a human-readable identifier for this condition.

            Returns:
                str: The string "Money".
            """
            return "Money"

        def get_diff(self, char_obj: Union[str, Char] = None) -> int:
            """Calculate the difference score for money requirements.

            Args:
                char_obj (Union[str, Char, None]): Unused parameter included for
                    compatibility with parent class.

            Returns:
                int: Returns 0 if requirement is met, -5000 otherwise as a
                    significant penalty for insufficient funds.
            """
            if self.is_fulfilled():
                return 0
            return -5000

    class LockCondition(Condition):
        """A condition that permanently locks content from being accessed.

        This special condition type is used to make content permanently inaccessible.
        When applied to game content, it can never be fulfilled, effectively locking
        that content. If blocking is enabled (default), the content will also be
        hidden from view.

        This is useful for:
        - Permanently disabling deprecated features
        - Hiding content that should never be accessible
        - Creating permanent barriers in game progression

        Attributes:
            blocking: Whether the locked content should be hidden. Defaults to True.
            display_in_list: Always False for lock conditions.
            display_in_desc: Always False for lock conditions.

        Methods:
            is_fulfilled(**kwargs): Always returns False.
            get_name(): Returns "lock".
        """

        def __init__(self, is_blocking: bool = True, *options: Option):
            """Initializes a new LockCondition.

            Args:
                is_blocking: Whether the locked content should be hidden from view.
                    Defaults to True.
            """
            super().__init__(is_blocking, *options)
            self.display_in_list = False
            self.display_in_desc = False

        def is_fulfilled(self, **kwargs) -> bool:
            """Checks if the condition is fulfilled (always False).

            This condition can never be fulfilled, as its purpose is to permanently
            lock content.

            Args:
                **kwargs: Additional arguments (not used for lock check).

            Returns:
                Always False, unless parent class check passes.
            """
            if super().is_fulfilled(**kwargs):
                return True
            return False

        def get_name(self) -> str:
            """Gets the condition's name.

            Returns:
                The string "lock".
            """
            return "lock"

    class TimeCondition(Condition):
        """A class for checking time-based conditions in the game.

        This class handles various time-related conditions including day, week, month,
        year, daytime, and weekday checks. It can be used to create time-dependent
        game logic and events.

        Attributes:
            day (str): The specific day to check. Defaults to "x" (any day).
            week (str): The specific week to check. Defaults to "x" (any week).
            month (str): The specific month to check. Defaults to "x" (any month).
            year (str): The specific year to check. Defaults to "x" (any year).
            daytime (str): The specific daytime period to check. Defaults to "x" (any time).
            weekday (str): The specific weekday to check. Defaults to "x" (any weekday).
            condition (str): The comparison operator for time checks. Can be:
                "+" (greater than)
                "-" (less than)
                "" (equals, default)
            display_in_desc (bool): Whether to display this condition in descriptions.

        Note:
            - Using "x" for any time attribute means it won't be checked (wildcard).
            - The condition operators (+, -) modify how the time comparison is performed.
        """

        def __init__(self, blocking: bool = True, *options: Option, **kwargs: Union[str, int]):
            super().__init__(blocking, *options)
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
            """Checks if the current time matches the specified conditions.

            This method verifies if all specified time conditions (day, month, year,
            week, daytime, weekday) are met according to the current game time.

            Args:
                **kwargs: Additional arguments passed to the parent class check.

            Returns:
                bool: True if all specified time conditions are met or if the parent
                    class check passes, False otherwise.
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
            """Generates a formatted description of the time condition.

            Creates a human-readable text representation of the time condition,
            including color coding to indicate whether the condition is currently
            met (green) or not (red).

            Args:
                **kwargs: Additional arguments (not used in this method).

            Returns:
                str: A formatted string containing the time condition description
                    with Ren'Py color tags ({color=#00a000} for met conditions,
                    {color=#a00000} for unmet conditions).
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
            """Returns a unique string identifier for this time condition.

            Creates a colon-separated string of all time components that make up
            this condition.

            Returns:
                str: A string in the format "day:week:month:year:daytime:weekday"
                    representing all time components of this condition.
            """

            return f"{self.day}:{self.week}:{self.month}:{self.year}:{self.daytime}:{self.weekday}"

    class TimerCondition(Condition):
        """A condition that checks if a specified amount of time has passed.

        This condition validates whether enough time has elapsed since a stored
        timestamp. It can check elapsed days, months, years, and/or daytime periods.
        Timers are identified by unique IDs and stored in the game's data.

        Timer conditions can be used to:
        - Create cooldown periods between actions
        - Schedule delayed events
        - Track duration-based game mechanics

        Attributes:
            id: Unique identifier for locating the timer in game data.
            day: Days that must pass or "x" to ignore.
            month: Months that must pass or "x" to ignore.
            year: Years that must pass or "x" to ignore.
            daytime: Daytime periods that must pass or "x" to ignore.
            display_in_list: Always False for timer conditions.
            display_in_desc: Always False for timer conditions.
            blocking: Always False for timer conditions.

        Methods:
            is_fulfilled(**kwargs): Checks if enough time has passed.
            get_name(): Gets string representation of timer requirements.
        """

        def __init__(self, id: str, *options: Option, **kwargs: int):
            """Initializes a new TimerCondition.

            Args:
                id: Unique identifier for locating the timer in game data.
                **kwargs: Time periods to check. Supported keys:
                    - day: Days that must pass
                    - month: Months that must pass
                    - year: Years that must pass
                    - daytime: Daytime periods that must pass
            """
            super().__init__(False, *options)
            self.id = id
            self.day       = "x" if 'day'       not in kwargs.keys() else kwargs['day'    ]
            self.month     = "x" if 'month'     not in kwargs.keys() else kwargs['month'  ]
            self.year      = "x" if 'year'      not in kwargs.keys() else kwargs['year'   ]
            self.daytime   = "x" if 'daytime'   not in kwargs.keys() else kwargs['daytime']
            self.display_in_list = False
            self.display_in_desc = False

        def is_fulfilled(self, **kwargs) -> bool:
            """Checks if enough time has passed since the stored timestamp.

            Validates that the required time periods have elapsed since the timer's
            stored timestamp. The timer must exist in game data and be a valid Time
            object.

            Args:
                **kwargs: Additional arguments that may affect condition checking.

            Returns:
                True if enough time has passed, False if:
                - Timer ID doesn't exist in game data
                - Timer data is not a Time object
                - Not enough time has passed
            """
            if super().is_fulfilled(**kwargs):
                return True

            if not contains_game_data("timer_" + self.id):
                log_error(311, f"TimerCondition id (timer_{self.id}) is not valid")
                return False

            log_val("timer_" + self.id, get_game_data("timer_" + self.id))

            timer = get_game_data("timer_" + self.id)

            if not isinstance(timer, Time):
                log_error(312, f"TimerCondition timer (timer_{self.id}) is not a Time object")
                return False

            aim = Time(timer)
            aim.add_time(day = self.day, month = self.month, year = self.year, daytime = self.daytime)

            log_val("aim", aim.day_to_string())
            log_val("time", time.day_to_string())

            compare = compare_time(aim, time)

            log_val("compare", compare)

            return compare <= 0

        def get_name(self) -> str:
            """Gets a string representation of the timer requirements.

            Returns:
                A formatted string showing timer ID and time requirements in format:
                "Timer <id>: <day>:<month>:<year>:<daytime>"
            """
            return f"Timer {self.id}: {self.day}:{self.month}:{self.year}:{self.daytime}"

    class RandomCondition(Condition):
        """A condition that is fulfilled based on random chance.

        This condition generates a random number and checks if it falls below a
        specified threshold. This creates a probability-based condition that may
        or may not be fulfilled each time it's checked.

        Random conditions can be used to:
        - Create chance-based events
        - Add variety to game content
        - Implement probability-based mechanics

        Attributes:
            amount: The threshold value. If random number is below this, condition is fulfilled.
            limit: The upper limit for random number generation (default 100).
            display_in_desc: Always True for random conditions.
            display_in_list: Always True for random conditions.
            blocking: Whether this condition blocks content when not fulfilled.

        Methods:
            is_fulfilled(**kwargs): Generates random number and checks against threshold.
            to_desc_text(**kwargs): Gets text showing probability percentage.
            to_list_text(**kwargs): Gets icon and probability for list display.
            get_name(): Gets string representation of threshold/limit.
            get_diff(char_obj): Gets probability as a percentage.
        """

        def __init__(self, threshold: num, limit: num = 100, blocking: bool = False, *options: Option):
            """Initializes a new RandomCondition.

            Args:
                threshold: The threshold value. If random number is below this,
                    condition is fulfilled.
                limit: The upper limit for random number generation. Defaults to 100.
                blocking: Whether this condition should block content when not fulfilled.
                    Defaults to False.
            """
            super().__init__(blocking, *options)
            self.amount = threshold
            self.limit  = limit
            self.display_in_desc = True
            self.display_in_list = True

        def is_fulfilled(self, **kwargs) -> bool:
            """Checks if the condition is fulfilled by random chance.

            Generates a random number between 0 and limit, then checks if it's
            below the threshold value.

            Args:
                **kwargs: Additional arguments that may affect condition checking.

            Returns:
                True if random number is below threshold, False otherwise.
            """
            if super().is_fulfilled(**kwargs):
                return True
            return get_random_int(0, self.limit) < self.amount
        def to_desc_text(self, **kwargs) -> str:
            """Gets text showing the probability percentage.

            Args:
                **kwargs: Additional arguments that may affect text formatting.

            Returns:
                A string showing "Chance: X%" where X is the probability percentage.
            """
            return f"Chance: {str(100 / self.limit * self.amount)}%"

        def to_list_text(self, **kwargs) -> Tuple[str, str, str]:
            """Gets icon and probability for list display.

            Returns a tuple containing:
            1. Empty icon string
            2. Probability percentage
            3. "Chance" label

            Args:
                **kwargs: Additional arguments that may affect text formatting.

            Returns:
                Tuple of (icon, value, label) for list display.
            """
            return ("", f"{str(100 / self.limit * self.amount)}%", "Chance")

        def get_name(self) -> str:
            """Gets string representation of threshold/limit values.

            Returns:
                A string in format "Random (threshold/limit)".
            """
            return f"Random ({self.amount}/{self.limit})"

        def get_diff(self, _char_obj) -> num:
            """Gets the probability as a percentage.

            Args:
                _char_obj: Not used for random conditions, included for API compatibility.

            Returns:
                The probability as a percentage (threshold/limit * 100).
            """
            return 100 / self.limit * self.amount

    class GameDataCondition(Condition):
        """A condition class that validates game data against expected values.

        This class extends the base Condition class to provide functionality for checking
        whether specific game data matches expected values. It's used to create conditions
        based on the state of game variables stored in the gameData dictionary.

        Attributes:
            key (str): The dictionary key to look up in gameData.
            value (Any): The expected value that gameData[key] should match.
            display_in_desc (bool): Whether to show this condition in descriptions.
            blocking (bool): Inherited from Condition, determines if condition blocks progress.
        """

        def __init__(self, key: str, value: Any, blocking: bool = False, *options: Option):
            """Initializes a new GameDataCondition instance.

            Args:
                key (str): The dictionary key to look up in gameData.
                value (Any): The expected value that gameData[key] should match.
                blocking (bool, optional): Whether this condition should block progress.
                    Defaults to False.
            """
            super().__init__(blocking, *options)
            self.key = key
            self.value = value
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """Checks if the game data matches the expected value.

            This method first checks the parent class's fulfillment condition. If that
            passes, returns True. Otherwise, verifies if the specified key exists in
            gameData and if its value matches the expected value.

            Args:
                **kwargs: Additional keyword arguments passed to parent class.

            Returns:
                bool: True if either parent condition is fulfilled or if gameData[key]
                    matches the expected value, False otherwise.
            """
            if super().is_fulfilled(**kwargs):
                return True

            if self.key not in gameData.keys():
                return False
            return gameData[self.key] == self.value

        def to_desc_text(self, **kwargs) -> str:
            """Generates a formatted description text for this condition.

            Creates a colored text description showing the condition's key and value.
            The text is green if the condition is fulfilled, red if not.

            Returns:
                str: A formatted string containing the translated key name and colored value,
                    using Ren'Py text tags for coloring.
            """
            if self.is_fulfilled():
                return get_translation(self.key) + " is {color=#00a000}" + str(self.value) + "{/color}"
            else:
                return get_translation(self.key) + " is {color=#a00000}" + str(self.value) + "{/color}"

        def get_name(self) -> str:
            """Gets the display name for this condition.

            Returns:
                str: The translated version of the condition's key.
            """
            return get_translation(self.key)

    class ProgressCondition(Condition):
        """A condition class that checks event series progression levels.

        This class validates whether an event series has reached a specific progress level
        or milestone. Progress can be checked against an exact value or using special
        string formats for range comparisons. If no specific value is provided, the
        condition simply checks if any progress has been made (-1 indicates no progress).

        The value parameter supports the default number pattern format:
        - Simple Number: "5" or 5 (must match exactly)
        - Positive Range: "5+" (value must be 5 or greater)
        - Negative Range: "5-" (value must be 5 or less)
        - Limited Range: "1-5" (value must be between 1 and 5 inclusive)
        - Multiple Values: "1,3,5" (value must match any listed number)

        Attributes:
            key (str): The unique identifier for the event series to check.
            value (Union[int, str]): The required progress level. Can use any of the
                formats described above. Empty string to just check for any progress.
            display_in_desc (bool): Whether to show this condition in descriptions.
                Always True for progress conditions.
            blocking (bool): Whether this condition blocks progression when not fulfilled.
        """

        def __init__(self, key: str, value: Union[int, str] = "", blocking: bool = False, *options: Option):
            """Initialize a new ProgressCondition.

            Args:
                key (str): The unique identifier for the event series to check.
                value (Union[int, str], optional): The required progress level. Can be a
                    specific value or comparison string. Defaults to "" (check for any progress).
                blocking (bool, optional): Whether this condition should block
                    progression when not fulfilled. Defaults to False.
            """
            super().__init__(blocking, *options)
            self.key = key
            self.value = value
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """Check if the event series meets the progress requirement.

            If no specific value is set (empty string), checks if any progress has been
            made (value != -1). Otherwise, compares the current progress against the
            required value using the specified comparison.

            Args:
                **kwargs: Additional arguments (unused in this implementation).

            Returns:
                bool: True if either:
                    - The parent condition is fulfilled
                    - No value is set and any progress has been made
                    - The current progress meets the value requirement
                    False otherwise.
            """
            if super().is_fulfilled(**kwargs):
                return True

            if self.value == "":
                return get_progress(self.key) != -1

            return check_in_value(self.value, get_progress(self.key))

        def to_desc_text(self, **kwargs) -> str:
            """Generate formatted text describing the progress requirement.

            Creates a colored text representation showing both the event series name
            and its progress requirement:
            - Event series name in blue (#3645e9)
            - Progress value in green (#00a000) when met, red (#a00000) when not met

            Args:
                **kwargs: Additional arguments (unused in this implementation).

            Returns:
                str: A formatted string showing the event series name and progress
                    requirement with appropriate color coding.
            """
            if self.is_fulfilled():
                return "Progress-level of {color=#3645e9}" + get_translation(self.key) + "{/color} is {color=#00a000}" + str(self.value) + "{/color}"
            else:
                return "Progress-level of {color=#3645e9}" + get_translation(self.key) + "{/color} is {color=#a00000}" + str(self.value) + "{/color}"

        def get_name(self) -> str:
            """Get a human-readable identifier for this condition.

            Returns:
                str: The translated name/title of the event series being checked.
            """
            return get_translation(self.key)

    class ValueCondition(Condition):
        """A condition class that checks if a value in kwargs matches an expected value.

        This class extends the base Condition class to validate whether a specific key
        in the kwargs dictionary matches an expected value. The comparison is done using
        exact equality (==). For boolean values, the kwargs value must be True to match.

        Attributes:
            key (str): The dictionary key to look up in kwargs.
            value (Any): The expected value that kwargs[key] should match.
            display_in_desc (bool): Whether to show this condition in descriptions.
                Always True for value conditions.
            blocking (bool): Whether this condition blocks progression when not fulfilled.
                Set during initialization.

        Note:
            The condition can check values in either kwargs directly or in a nested
            'values' dictionary within kwargs. If 'values' exists in kwargs, the key
            will be looked up there instead of the top level.
        """

        def __init__(self, key: str, value: Any, blocking: bool = False, *options: Option):
            """Initialize a new ValueCondition.

            Args:
                key (str): The dictionary key to look up in kwargs.
                value (Any): The expected value that kwargs[key] should match.
                blocking (bool, optional): Whether this condition should block
                    progression when not fulfilled. Defaults to False.
            """
            super().__init__(blocking, *options)
            self.key = key
            self.value = value
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """Check if the kwargs value matches the expected value.

            First checks if the parent condition is fulfilled. If not, looks up the key
            in either kwargs directly or kwargs['values'] if it exists, and compares
            the found value with the expected value using exact equality (==).

            Args:
                **kwargs: Additional arguments. May contain a 'values' dictionary
                    for nested value lookup.

            Returns:
                bool: True if either:
                    - The parent condition is fulfilled
                    - The value at kwargs[key] matches self.value
                    - The value at kwargs['values'][key] matches self.value (if 'values' exists)
                    False otherwise.
            """

            if super().is_fulfilled(**kwargs):
                return True

            if "values" in kwargs.keys():
                return self.value == get_kwargs(self.key, **kwargs["values"])
            else:
                return self.value == get_kwargs(self.key, **kwargs)

        def to_desc_text(self, **kwargs) -> str:
            """Generate formatted text describing the value requirement.

            Creates a colored text representation showing both the key name and
            its required value:
            - Green text when value requirement is met
            - Red text when value requirement is not met

            Args:
                **kwargs: Additional arguments that may affect condition checking.

            Returns:
                str: A formatted string showing the translated key name and colored value,
                    using Ren'Py text tags for coloring (green #00a000 or red #a00000).
            """

            if self.is_fulfilled(**kwargs):
                return get_translation(self.key) + " is {color=#00a000}" + str(self.value) + "{/color}"
            else:
                return get_translation(self.key) + " is {color=#a00000}" + str(self.value) + "{/color}"

        def get_name(self) -> str:
            """Get a human-readable identifier for this condition.

            Returns:
                str: The translated version of the condition's key.
            """

            return get_translation(self.key)

    class NumValueCondition(Condition):
        """A condition class that validates numeric values using the Default Number Pattern.

        This class extends the base Condition class to check if a numeric value from kwargs
        matches a pattern specified using the game's Default Number Pattern format. The value
        can be specified as a fixed number, a pattern string, or a dynamic Selector.

        The Default Number Pattern supports these formats:
            - Simple Number: "8", "15" (exact match)
            - Positive Range: "4+", "26+" (value must be ≥ specified number)
            - Negative Range: "6-", "62-" (value must be ≤ specified number)
            - Limited Range: "3-7", "40-49" (value must be within range, inclusive)
            - Multiple Values: "4,35,70-100,1000+" (can combine any of above)

        Attributes:
            key (str): The dictionary key to look up in kwargs.
            value (Union[num, str, Selector]): The value or pattern to compare against.
                Can be:
                - A number for exact comparison
                - A string using Default Number Pattern format
                - A Selector object that generates values dynamically
            display_in_desc (bool): Whether to show in descriptions. Always True.
            display_in_list (bool): Whether to show in lists. Always False.
            blocking (bool): Whether this condition blocks progression when not fulfilled.

        Note:
            The class uses helper functions:
            - get_kwargs(): To retrieve values from kwargs
            - get_element(): To resolve Selector values
            - is_float(): To validate numeric values
            - check_in_value(): To perform pattern matching using Default Number Pattern
        """

        def __init__(self, key: str, value: Union[num, str, Selector], blocking: bool = False, *options: Option):
            """Initialize a new NumValueCondition.

            Args:
                key (str): The dictionary key to look up in kwargs.
                value (Union[num, str, Selector]): The value or pattern to compare against.
                    Can be a number, Default Number Pattern string, or Selector.
                blocking (bool, optional): Whether this condition should block
                    progression when not fulfilled. Defaults to False.
            """
            super().__init__(blocking, *options)
            self.key = key
            self.value = value
            self.display_in_desc = True
            self.display_in_list = False

        def is_fulfilled(self, **kwargs) -> bool:
            """Check if the kwargs value matches the numeric condition pattern.

            This method retrieves the value from kwargs (or kwargs['values'] if it exists),
            resolves any Selector values, validates that the value is numeric, and then
            performs the comparison using the Default Number Pattern format.

            The comparison supports all Default Number Pattern formats:
            - Exact match: "8"
            performs the comparison using the specified pattern.

            Args:
                **kwargs: Additional arguments. May contain:
                    - Direct key-value pairs
                    - A 'values' dictionary for nested lookups
                    - Arguments needed for Selector resolution

            Returns:
                bool: True if either:
                    - The parent condition is fulfilled
                    - The value exists and meets the comparison criteria
                    False if:
                    - The value doesn't exist
                    - The value isn't numeric
                    - The comparison fails
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
            """Generate formatted text describing the numeric condition.

            Creates a colored text representation showing both the key name and
            its required value:
            - Green text when value requirement is met
            - Red text when value requirement is not met

            Args:
                **kwargs: Additional arguments that may affect condition checking.

            Returns:
                str: A formatted string in the format "KeyName is {color}Value{/color}"
                    where the color is green (#00a000) when met or red (#a00000) when not met.
            """
            if self.is_fulfilled(**kwargs):
                return get_translation(self.key) + " is {color=#00a000}" + str(self.value) + "{/color}"
            else:
                return get_translation(self.key) + " is {color=#a00000}" + str(self.value) + "{/color}"

        def get_name(self) -> str:
            """Get a human-readable identifier for this condition.

            Returns:
                str: The translated version of the condition's key.
            """
            return get_translation(self.key)

    class NumCompareCondition(Condition):
        """A condition class that performs direct numeric comparisons using operators.

        This class extends the base Condition class to compare numeric values using standard
        comparison operators (>, >=, <, <=, ==, !=). Unlike NumValueCondition which uses
        the Default Number Pattern, this class performs direct mathematical comparisons.

        Attributes:
            key (str): The dictionary key to look up in kwargs.
            value (Union[int, Selector]): The value to compare against. If a Selector
                is provided, it will be rolled for each check.
            operation (str): The comparison operator to use. Valid operators are:
                ">": Greater than
                ">=": Greater than or equal to
                "<": Less than
                "<=": Less than or equal to
                "==": Equal to
                "!=": Not equal to
            display_in_desc (bool): Whether to show in descriptions. Always True.
            display_in_list (bool): Whether to show in lists. Always False.
            blocking (bool): Whether this condition blocks progression when not fulfilled.

        Note:
            This class is designed for exact numeric comparisons, unlike NumValueCondition
            which handles pattern-based ranges. Use this when you need precise mathematical
            comparisons rather than range-based checks.
        """

        def __init__(self, key: str, value: Union[int, Selector], operation: str, blocking: bool = False, *options: Option):
            """Initialize a new NumCompareCondition.

            Args:
                key (str): The dictionary key to look up in kwargs.
                value (Union[int, Selector]): The value to compare against. If a Selector
                    is provided, it will be rolled for each check.
                operation (str): The comparison operator to use. Must be one of:
                    ">": Greater than
                    ">=": Greater than or equal to
                    "<": Less than
                    "<=": Less than or equal to
                    "==": Equal to
                    "!=": Not equal to
                blocking (bool, optional): Whether this condition should block
                    progression when not fulfilled. Defaults to False.
            """
            super().__init__(blocking, *options)
            self.key = key
            self.value = value
            self.operation = operation
            self.display_in_desc = True
            self.display_in_list = False

        def is_fulfilled(self, **kwargs) -> bool:
            """Check if the numeric comparison condition is met.

            Retrieves the value from kwargs and compares it against the target value
            using the specified operator. If a Selector is used for the target value,
            it is rolled before comparison.

            Args:
                **kwargs: Additional arguments. May contain:
                    - Direct key-value pairs
                    - A 'values' dictionary for nested lookups
                    - Arguments needed for Selector resolution

            Returns:
                bool: True if either:
                    - The parent condition is fulfilled
                    - The comparison evaluates to True
                    False if:
                    - The value doesn't exist
                    - The comparison evaluates to False
                    - Invalid operator is specified
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
            """Generate formatted text describing the numeric comparison.

            Creates a colored text representation showing the key name, operator,
            and comparison value:
            - Green text when comparison is True
            - Red text when comparison is False

            Args:
                **kwargs: Additional arguments that may affect condition checking.

            Returns:
                str: A formatted string in the format "KeyName operator {color}Value{/color}"
                    where the color is green (#00a000) when met or red (#a00000) when not met.
            """
            if self.is_fulfilled(**kwargs):
                return get_translation(self.key) + " " + self.operation + " {color=#00a000}" + str(self.value) + "{/color}"
            else:
                return get_translation(self.key) + " " + self.operation + " {color=#a00000}" + str(self.value) + "{/color}"

        def get_name(self) -> str:
            """Get a human-readable identifier for this condition.

            Returns:
                str: The translated version of the condition's key.
            """
            return get_translation(self.key)

        def get_diff(self, _char_obj) -> num:
            """Calculate the numeric difference between the actual and target values.

            Computes a score representing how far the actual value is from satisfying
            the condition. The calculation varies based on the operator:
            - For >, >=: Returns (actual - target)
            - For <, <=: Returns (target - actual)
            - For ==: Returns 0 if equal, -100 if not
            - For !=: Returns 0 if not equal, -100 if equal

            Args:
                _char_obj: Unused parameter included for API compatibility.

            Returns:
                num: The calculated difference score:
                    - Positive numbers indicate the margin by which the condition is met
                    - Negative numbers indicate how far the value is from meeting the condition
                    - -100 indicates a failed equality/inequality check or missing values
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
        """A condition class that checks if a value in kwargs matches an expected value.

        This class extends the base Condition class to validate whether a specific key
        in the kwargs dictionary matches an expected value. The comparison is done using
        exact equality (==). For Selector values, the selector is rolled before comparison.

        Attributes:
            key (str): The dictionary key to look up in kwargs.
            value (Union[Any, Selector]): The expected value or Selector to compare against.
                If a Selector is provided, it will be rolled for each check.
            display_in_desc (bool): Whether to show this condition in descriptions.
                Always True for compare conditions.
            display_in_list (bool): Whether to show this condition in list displays.
                Always False for compare conditions.
            blocking (bool): Whether this condition blocks progression when not fulfilled.

        Note:
            The condition can check values in either kwargs directly or in a nested
            'values' dictionary within kwargs. If 'values' exists in kwargs, the key
            will be looked up there instead of the top level.
        """

        def __init__(self, key: str, value: Union[Any, Selector], blocking: bool = False, *options: Option):
            """Initialize a new CompareCondition.

            Args:
                key (str): The dictionary key to look up in kwargs.
                value (Union[Any, Selector]): The expected value or Selector to compare against.
                    If a Selector is provided, it will be rolled for each check.
                blocking (bool, optional): Whether this condition should block
                    progression when not fulfilled. Defaults to False.
            """
            super().__init__(blocking, *options)
            self.key = key
            self.value = value
            self.display_in_desc = True
            self.display_in_list = False

        def is_fulfilled(self, **kwargs) -> bool:
            """Check if the kwargs value matches the expected value.

            First checks if the parent condition is fulfilled. If not, looks up the key
            in either kwargs directly or kwargs['values'] if it exists. For Selector values,
            rolls the selector before comparison. The comparison is done using exact 
            equality (==).

            Args:
                **kwargs: Additional arguments. May contain:
                    - Direct key-value pairs
                    - A 'values' dictionary for nested lookups
                    - Arguments needed for Selector resolution

            Returns:
                bool: True if either:
                    - The parent condition is fulfilled
                    - The value at kwargs[key] matches self.value
                    - The value at kwargs['values'][key] matches self.value (if 'values' exists)
                    False otherwise.
            """
            if super().is_fulfilled(**kwargs):
                return True

            if "values" in kwargs.keys():
                kwargs = kwargs["values"]

            if self.key not in kwargs.keys():
                return False

            value = self.value
            if isinstance(self.value, Selector):
                value = self.value.roll(**kwargs)

            return kwargs[self.key] == value

        def to_desc_text(self, **kwargs) -> str:
            """Generate formatted text describing the comparison requirement.

            Creates a colored text representation showing both the key name and
            its required value:
            - Green text when value requirement is met
            - Red text when value requirement is not met

            Args:
                **kwargs: Additional arguments that may affect condition checking.

            Returns:
                str: A formatted string showing the translated key name and colored value,
                    using Ren'Py text tags for coloring (green #00a000 or red #a00000).
            """
            if self.is_fulfilled(**kwargs):
                return get_translation(self.key) + " equals {color=#00a000}" + str(self.value) + "{/color}"
            else:
                return get_translation(self.key) + " equals {color=#a00000}" + str(self.value) + "{/color}"

        def get_name(self) -> str:
            """Get a human-readable identifier for this condition.

            Returns:
                str: The translated version of the condition's key.
            """
            return get_translation(self.key)

        def get_diff(self, _char_obj) -> num:
            """Calculate the difference score for value comparison.

            Args:
                _char_obj: Unused parameter included for API compatibility.

            Returns:
                num: Returns 0 if the values match exactly, -100 otherwise.
                    Also returns -100 if the key doesn't exist in kwargs['values'].
            """
            if "values" not in kwargs.keys() or self.key not in kwargs["values"].keys():
                return -100
            value = self.value
            return 0 if kwargs["values"][self.key] == value else -100

    class KeyCompareCondition(Condition):
        """A condition class that compares two values from kwargs using operators.

        This class extends the base Condition class to compare two values from the kwargs
        dictionary using standard comparison operators. It supports numeric comparisons
        (>, >=, <, <=) and equality checks (==, !=). Values can be direct values or
        Selectors that are rolled during comparison.

        Attributes:
            key_1 (str): The first dictionary key to look up in kwargs.
            key_2 (str): The second dictionary key to look up in kwargs.
            operation (str): The comparison operator to use. Valid operators are:
                ">": Greater than
                ">=": Greater than or equal to
                "<": Less than
                "<=": Less than or equal to
                "==": Equal to
                "!=": Not equal to
            display_in_desc (bool): Whether to show in descriptions. Always True.
            display_in_list (bool): Whether to show in lists. Always False.
            blocking (bool): Whether this condition blocks progression when not fulfilled.

        Note:
            The condition looks for values in kwargs['values'] if it exists, otherwise
            in kwargs directly. For Selector values, they are rolled before comparison.
            The get_diff() method returns meaningful numeric differences for inequality
            comparisons to help gauge how far apart the values are.
        """

        def __init__(self, key_1: str, key_2: str, operation: str, blocking: bool = False, *options: Option):
            """Initialize a new KeyCompareCondition.

            Args:
                key_1 (str): The first dictionary key to look up in kwargs.
                key_2 (str): The second dictionary key to look up in kwargs.
                operation (str): The comparison operator to use. Must be one of:
                    ">": Greater than
                    ">=": Greater than or equal to
                    "<": Less than
                    "<=": Less than or equal to
                    "==": Equal to
                    "!=": Not equal to
                blocking (bool, optional): Whether this condition should block
                    progression when not fulfilled. Defaults to False.
            """
            super().__init__(blocking, *options)
            self.key_1 = key_1
            self.key_2 = key_2
            self.operation = operation
            self.display_in_desc = True
            self.display_in_list = False

        def is_fulfilled(self, **kwargs) -> bool:
            """Check if the comparison between the two kwargs values is satisfied.

            Retrieves both values from kwargs (or kwargs['values'] if it exists) and
            compares them using the specified operator. For Selector values, they are
            rolled before comparison.

            Args:
                **kwargs: Additional arguments. May contain:
                    - Direct key-value pairs
                    - A 'values' dictionary for nested lookups
                    - Arguments needed for Selector resolution

            Returns:
                bool: True if either:
                    - The parent condition is fulfilled
                    - The comparison evaluates to True using the specified operator
                    False if:
                    - Either key is missing
                    - Invalid operator is specified
                    - The comparison evaluates to False
            """
            if super().is_fulfilled(**kwargs):
                return True

            if "values" in kwargs.keys():
                kwargs = kwargs["values"]

            value_1 = kwargs[self.key_1]
            value_2 = kwargs[self.key_2]

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
            """Get a human-readable identifier for this condition.

            Returns:
                str: A string in the format "key1 operator key2" showing the
                    comparison being performed.
            """
            return f"{self.key_1} {self.operation} {self.key_2}"

        def get_diff(self, char_obj: Char) -> num:
            """Calculate the numeric difference between the two values.

            For inequality comparisons (>, >=, <, <=), returns the actual numeric
            difference between the values to indicate how far apart they are.
            For equality comparisons (==, !=), returns either 0 or -100 to indicate
            match/mismatch.

            The difference calculation varies by operator:
            - For > and >=: Returns (value1 - value2)
            - For < and <=: Returns (value2 - value1)
            - For ==: Returns 0 if equal, -100 if not
            - For !=: Returns 0 if not equal, -100 if equal

            Args:
                char_obj (Char): Unused parameter included for API compatibility.

            Returns:
                num: The calculated difference:
                    - For inequalities: The numeric difference between values
                    - For equalities: 0 for match, -100 for mismatch
                    - Returns -100 if keys don't exist or operator is invalid
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
        """A condition class that checks if a value matches the game's loli content setting.

        This class extends the base Condition class to validate whether the current
        loli_content game setting matches a specified value or pattern. The value can be
        a direct number or a pattern string.

        Attributes:
            value (Union[int, str]): The value or pattern to compare against the
                loli_content setting.
            blocking (bool): Whether this condition blocks progression when not fulfilled.
        """

        def __init__(self, value: Union[int, str], blocking: bool = False, *options: Option):
            """Initialize a new LoliContentCondition.

            Args:
                value (Union[int, str]): The value or pattern to compare against the
                    loli_content setting.
                blocking (bool, optional): Whether this condition should block
                    progression when not fulfilled. Defaults to False.
            """
            super().__init__(blocking, *options)
            self.value = value

        def is_fulfilled(self, **kwargs) -> bool:
            """Check if the loli_content setting matches the specified value.

            Uses check_in_value to compare the current loli_content setting against
            the specified value or pattern.

            Args:
                **kwargs: Additional arguments (unused in this implementation).

            Returns:
                bool: True if either:
                    - The parent condition is fulfilled
                    - The loli_content setting matches the specified value/pattern
                    False otherwise.
            """
            if super().is_fulfilled(**kwargs):
                return True

            return check_in_value(self.value, loli_content)

        def get_name(self) -> str:
            """Get a human-readable identifier for this condition.

            Returns:
                str: A string in the format "loli_content: value" showing the
                    value being checked.
            """
            return f"loli_content: {self.value}"

    class AND(Condition):
        """A condition class that requires all sub-conditions to be fulfilled.

        This class implements logical AND behavior, requiring all contained conditions
        to be fulfilled for this condition to be fulfilled. It supports an arbitrary
        number of sub-conditions.

        Attributes:
            conditions (List[Condition]): The list of conditions that must all be fulfilled.
            display_in_desc (bool): Whether to show in descriptions. Always True.
        """

        def __init__(self, *conditions: Condition | Option):
            """Initialize a new AND condition.

            Args:
                *conditions: Variable number of Condition objects that must all be fulfilled.
            """

            self.conditions = []
            options = []
            for condition in conditions:
                if isinstance(condition, Condition):
                    self.conditions.append(condition)
                else:
                    options.append(condition)

            super().__init__(False, *options)
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """Check if all sub-conditions are fulfilled.

            Evaluates each condition in sequence. Returns False as soon as any condition
            is not fulfilled.

            Args:
                **kwargs: Additional arguments passed to each condition's is_fulfilled check.

            Returns:
                bool: True if either:
                    - The parent condition is fulfilled
                    - All sub-conditions are fulfilled
                    False if any condition is not fulfilled.
            """
            if super().is_fulfilled(**kwargs):
                return True

            for condition in self.conditions:
                if condition.is_fulfilled(**kwargs):
                    continue
                return False

            return True

        def to_desc_text(self, **kwargs) -> str:
            """Generate formatted text describing all sub-conditions.

            Creates a special formatted text representation for logical conditions
            using get_logic_condition_desc_text.

            Args:
                **kwargs: Additional arguments that may affect text formatting.

            Returns:
                str: A formatted string showing all sub-conditions and their status.
            """
            return get_logic_condition_desc_text(self.is_fulfilled(**kwargs), self.conditions, "AND", **kwargs)

        def get_name(self) -> str:
            """Get a human-readable identifier for this condition.

            Creates a name by joining all sub-condition names with "_AND_".

            Returns:
                str: A string joining all sub-condition names with "_AND_".
            """
            output = ""
            for condition in self.conditions:
                if output != "":
                    output += "_AND_"
                output += condition.get_name()

            return output

        def get_diff(self, char_obj: Union[str, Char] = None) -> num:
            """Calculate the combined difference score for all sub-conditions.

            Sums the difference scores from all sub-conditions to provide a total
            difference score.

            Args:
                char_obj (Union[str, Char], optional): Character to check conditions
                    against. Defaults to None.

            Returns:
                num: The sum of all sub-condition difference scores.
            """
            diff = 0

            for condition in self.conditions:
                diff += condition.get_diff(char_obj)

            return diff

    class OR(Condition):
        """A condition class that requires at least one sub-condition to be fulfilled.

        This class implements logical OR behavior, requiring at least one of its contained
        conditions to be fulfilled. It supports an arbitrary number of sub-conditions.

        Attributes:
            conditions (List[Condition]): The list of conditions to check.
            display_in_desc (bool): Whether to show in descriptions. Always True.
        """

        def __init__(self, *conditions: Condition | Option):
            """Initialize a new OR condition.

            Args:
                *conditions: Variable number of Condition objects, at least one of which
                    must be fulfilled.
            """

            self.conditions = []
            options = []
            for condition in conditions:
                if isinstance(condition, Condition):
                    self.conditions.append(condition)
                else:
                    options.append(condition)

            super().__init__(False, *options)
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """Check if at least one sub-condition is fulfilled.

            Evaluates each condition in sequence. Returns True as soon as any condition
            is fulfilled.

            Args:
                **kwargs: Additional arguments passed to each condition's is_fulfilled check.

            Returns:
                bool: True if either:
                    - The parent condition is fulfilled
                    - Any sub-condition is fulfilled
                    False if no conditions are fulfilled.
            """
            if super().is_fulfilled(**kwargs):
                return True

            for condition in self.conditions:
                if condition.is_fulfilled(**kwargs):
                    return True

            return False

        def to_desc_text(self, **kwargs) -> Union[str, List[str]]:
            """Generate formatted text describing all sub-conditions.

            Creates a special formatted text representation for logical conditions
            using get_logic_condition_desc_text.

            Args:
                **kwargs: Additional arguments that may affect text formatting.

            Returns:
                Union[str, List[str]]: A formatted string or list of strings showing
                    all sub-conditions and their status.
            """
            return get_logic_condition_desc_text(self.is_fulfilled(**kwargs), self.conditions, "OR", **kwargs)

        def get_name(self) -> str:
            """Get a human-readable identifier for this condition.

            Creates a name by joining all sub-condition names with "_OR_".

            Returns:
                str: A string joining all sub-condition names with "_OR_".
            """
            output = ""
            for condition in self.conditions:
                if output != "":
                    output += "_OR_"
                output += condition.get_name()

            return output

        def get_diff(self, char_obj: Union[str, Char] = None) -> num:
            """Calculate the best difference score among all sub-conditions.

            Finds the sub-condition with the smallest absolute difference score,
            representing how close we are to fulfilling at least one condition.

            Args:
                char_obj (Union[str, Char], optional): Character to check conditions
                    against. Defaults to None.

            Returns:
                num: The smallest absolute difference score among all sub-conditions.
            """
            diff = None

            for condition in self.conditions:
                new_diff = condition.get_diff(char_obj)

                if diff == None or abs(diff) > abs(new_diff):
                    diff = new_diff

            return diff

    class NOR(Condition):
        """
        A class representing a NOR logical condition that evaluates to True only if none of its
        sub-conditions are fulfilled.

        This is equivalent to a NOT(OR(...)) operation in boolean logic. For example, if you have
        conditions A and B, NOR(A,B) is true only if both A and B are false.

        Attributes:
            conditions (List[Condition]): List of sub-conditions to evaluate
            display_in_desc (bool): Whether this condition should be displayed in descriptions
        """

        def __init__(self, *conditions: Condition | Option):
            """
            Initialize a NOR condition with a variable number of sub-conditions.

            Args:
                *conditions (Condition): Variable number of condition objects to evaluate
            """

            self.conditions = []
            options = []
            for condition in conditions:
                if isinstance(condition, Condition):
                    self.conditions.append(condition)
                else:
                    options.append(condition)

            super().__init__(False, *options)
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs):
            """
            Check if none of the sub-conditions are fulfilled.

            The NOR condition is fulfilled in two cases:
            1. If the base condition is fulfilled (determined by super().is_fulfilled())
            2. If none of the sub-conditions are fulfilled

            Args:
                **kwargs: Additional keyword arguments passed to sub-conditions

            Returns:
                bool: True if none of the conditions are fulfilled, False otherwise
            """
            if super().is_fulfilled(**kwargs):
                return True

            for condition in self.conditions:
                if condition.is_fulfilled(**kwargs):
                    return False

            return True

        def to_desc_text(self, **kwargs) -> Union[str, List[str]]:
            """
            Generate a human-readable description of the NOR condition.

            This method uses a special formatting for logic conditions to make them
            easier to understand in the game's UI or descriptions.

            Args:
                **kwargs: Additional keyword arguments for description generation

            Returns:
                Union[str, List[str]]: A formatted description of the condition and its state
            """
            return get_logic_condition_desc_text(self.is_fulfilled(**kwargs), self.conditions, "NOR", **kwargs)

        def get_name(self) -> str:
            """
            Generate a unique identifier name for this NOR condition.

            The name is constructed by joining all sub-condition names with "_NOR_"
            as a separator. For example: "CondA_NOR_CondB_NOR_CondC"

            Returns:
                str: A unique string identifier for this condition
            """
            output = ""
            for condition in self.conditions:
                if output != "":
                    output += "_NOR_"
                output += condition.get_name()

            return output

        def get_diff(self, char_obj: Union[str, Char] = None) -> num:
            """
            Calculate how close this NOR condition is to being fulfilled.

            This method finds the sub-condition that is closest to being fulfilled
            (has the smallest absolute difference score). This helps in determining
            how far we are from the NOR condition changing its state.

            Args:
                char_obj (Union[str, Char], optional): Character object or identifier
                    to evaluate the condition against. Defaults to None.

            Returns:
                num: The smallest absolute difference score among all sub-conditions.
                    A smaller absolute value indicates being closer to fulfillment.
            """
            diff = None

            for condition in self.conditions:
                new_diff = condition.get_diff(char_obj)

                if diff == None or abs(diff) > abs(new_diff):
                    diff = new_diff

            return diff

    class NOT(Condition):
        """
        A class representing a NOT logical condition that inverts the result of its sub-condition.

        This is equivalent to logical negation in boolean logic. For example, if you have
        condition A, NOT(A) is true only if A is false.

        Attributes:
            condition (Condition): The single condition to negate
            display_in_desc (bool): Whether this condition should be displayed in descriptions
        """

        def __init__(self, condition: Condition, *options: Option):
            """
            Initialize a NOT condition with a single condition to negate.

            Args:
                condition (Condition): The condition object whose result will be negated
            """

            super().__init__(False, *options)
            self.condition = condition
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Check if the sub-condition is not fulfilled.

            The NOT condition is fulfilled in two cases:
            1. If the base condition is fulfilled (determined by super().is_fulfilled())
            2. If the sub-condition is not fulfilled

            Args:
                **kwargs: Additional keyword arguments passed to the sub-condition

            Returns:
                bool: True if the condition is not fulfilled, False otherwise
            """
            if super().is_fulfilled(**kwargs):
                return True

            return not self.condition.is_fulfilled(**kwargs)

        def to_desc_text(self, **kwargs) -> Union[str, List[str]]:
            """
            Generate a human-readable description of the NOT condition.

            This method adds a gray-colored "NOT" prefix to the sub-condition's description.
            If the sub-condition returns multiple lines, "NOT" is added to each line.

            Args:
                **kwargs: Additional keyword arguments for description generation

            Returns:
                Union[str, List[str]]: The sub-condition's description prefixed with "NOT",
                    either as a single string or a list of strings for multi-line descriptions
            """
            desc_text = self.condition.to_desc_text(**kwargs)
            if isinstance(desc_text, str):
                return "{color=#616161}NOT{/color} " + desc_text
            else:
                return "\n".join(["{color=#616161}NOT{/color} " + desc for desc in desc_text])

        def get_name(self) -> str:
            """
            Generate a unique identifier name for this NOT condition.

            The name is constructed by adding a "NOT_" prefix to the sub-condition's name.
            For example: "NOT_ConditionA"

            Returns:
                str: A unique string identifier for this condition
            """
            return "NOT_" + self.condition.get_name()

        def get_diff(self, char_obj: Union[str, Char]) -> num:
            """
            Calculate how close this NOT condition is to being fulfilled.

            This method inverts the difference score of the sub-condition and clamps
            it to the range [-100, 100]. For example, if the sub-condition's difference
            is 70, the NOT condition's difference will be 30 (100 - 70).

            Args:
                char_obj (Union[str, Char]): Character object or identifier to evaluate
                    the condition against.

            Returns:
                num: The inverted and clamped difference score. A smaller absolute
                    value indicates being closer to fulfillment.
            """
            diff = self.condition.get_diff(char_obj)
            return clamp_value(100 - diff, -100, 100)

    class XOR(Condition):
        """
        A class representing an XOR (exclusive OR) logical condition that evaluates to True only if
        exactly one of its sub-conditions is fulfilled.

        This is equivalent to ensuring mutual exclusivity in boolean logic. For example, if you have
        conditions A and B, XOR(A,B) is true only if either A is true and B is false, or A is false
        and B is true, but not both.

        Attributes:
            conditions (List[Condition]): List of sub-conditions to evaluate
            display_in_desc (bool): Whether this condition should be displayed in descriptions
        """

        def __init__(self, *conditions: Condition | Option):
            """
            Initialize an XOR condition with a variable number of sub-conditions.

            Args:
                *conditions (Condition): Variable number of condition objects to evaluate,
                    exactly one of which must be fulfilled for the XOR to be true
            """

            self.conditions = []
            options = []
            for condition in conditions:
                if isinstance(condition, Condition):
                    self.conditions.append(condition)
                else:
                    options.append(condition)

            super().__init__(False, *options)
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Check if exactly one of the sub-conditions is fulfilled.

            The XOR condition is fulfilled in two cases:
            1. If the base condition is fulfilled (determined by super().is_fulfilled())
            2. If exactly one sub-condition is fulfilled (no more, no less)

            Args:
                **kwargs: Additional keyword arguments passed to sub-conditions

            Returns:
                bool: True if exactly one condition is fulfilled, False otherwise
            """
            if super().is_fulfilled(**kwargs):
                return True

            is_true = False
            
            for condition in self.conditions:
                if condition.is_fulfilled(**kwargs):
                    if is_true:
                        return False
                    is_true = True
            return is_true  # Changed from True to is_true to handle case where no conditions are fulfilled

        def to_desc_text(self, **kwargs) -> Union[str, List[str]]:
            """
            Generate a human-readable description of the XOR condition.

            This method uses a special formatting for logic conditions to make them
            easier to understand in the game's UI or descriptions. The XOR relationship
            indicates that exactly one of the conditions must be true.

            Args:
                **kwargs: Additional keyword arguments for description generation

            Returns:
                Union[str, List[str]]: A formatted description of the condition and its state
            """
            return get_logic_condition_desc_text(self.is_fulfilled(**kwargs), self.conditions, "XOR", **kwargs)

        def get_name(self) -> str:
            """
            Generate a unique identifier name for this XOR condition.

            The name is constructed by joining all sub-condition names with "_XOR_"
            as a separator. For example: "CondA_XOR_CondB_XOR_CondC"

            Returns:
                str: A unique string identifier for this condition
            """
            output = ""
            for condition in self.conditions:
                if output != "":
                    output += "_XOR_"
                output += condition.get_name()

            return output

        def get_diff(self, char_obj: Union[str, Char] = None) -> num:
            """
            Calculate how close this XOR condition is to being fulfilled.

            This method finds the sub-condition that is closest to being fulfilled
            (has the smallest absolute difference score). For XOR conditions,
            we want to track how close we are to having exactly one condition fulfilled.

            Args:
                char_obj (Union[str, Char], optional): Character object or identifier
                    to evaluate the condition against. Defaults to None.

            Returns:
                num: The smallest absolute difference score among all sub-conditions.
                    A smaller absolute value indicates being closer to fulfillment.
            """
            diff = None

            for condition in self.conditions:
                new_diff = condition.get_diff(char_obj)

                if diff is None or abs(diff) > abs(new_diff):
                    diff = new_diff

            return diff if diff is not None else 0

    class IntroCondition(Condition):
        """
        A class representing a condition that checks if the game is in its introduction phase.

        This condition uses a specific date (October 1, 2023) as the cutoff point between
        the introduction phase and the main game phase. The condition can be configured to
        check for either being in the intro phase or being past it.

        Attributes:
            is_intro (bool): When True, the condition is fulfilled during the intro phase
                (before Oct 1, 2023). When False, it's fulfilled after the intro phase.
        """

        def __init__(self, is_intro: bool = True, *options: Option):
            """
            Initialize an IntroCondition with a specified phase check.

            Args:
                is_intro (bool, optional): Whether to check for being in the intro phase.
                    Defaults to True (checking if we're in the intro phase).
            """
            super().__init__(False, *options)
            self.is_intro = is_intro

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Check if the game is in the desired phase (intro or post-intro).

            The condition is fulfilled in two cases:
            1. If the base condition is fulfilled (determined by super().is_fulfilled())
            2. If the current date's relationship to Oct 1, 2023 matches the desired phase:
                - For intro phase (is_intro=True): Before Oct 1, 2023
                - For post-intro (is_intro=False): On or after Oct 1, 2023

            Args:
                **kwargs: Additional keyword arguments (not used in this condition)

            Returns:
                bool: True if the game is in the desired phase, False otherwise
            """
            if super().is_fulfilled(**kwargs):
                return True

            if ((time.compare_today(10, 1, 2023) == -1 and self.is_intro) or
                (time.compare_today(10, 1, 2023) != -1 and not self.is_intro)):
                return True
            return False

        def get_name(self) -> str:
            """
            Generate a unique identifier name for this condition.

            Returns:
                str: The string "IntroCondition" as the identifier
            """
            return "IntroCondition"

    class PTAOverride(Condition):
        """
        A class representing a condition that can override other conditions in PTA voting.

        This condition allows for special handling of PTA voting based on specific characters
        and acceptance states. It can be used to force accept, reject, or ignore votes for
        specific characters or globally.

        Attributes:
            char (str): The character this override applies to. Empty string means it applies globally.
            accept (str): The override state - "yes" to force accept, "no" to force reject,
                "ignore" to skip/ignore. Defaults to "yes".
            display_in_desc (bool): Whether this condition should be displayed in descriptions
        """

        def __init__(self, char: str = "", accept: str = "yes", *options: Option):
            """
            Initialize a PTAOverride condition with character and acceptance parameters.

            Args:
                char (str, optional): Character identifier this override applies to.
                    Empty string means it applies globally. Defaults to "".
                accept (str, optional): The override state - "yes"/"no"/"ignore".
                    Defaults to "yes".
            """
            super().__init__(False, *options)
            self.char = char
            self.accept = accept

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Check if this override condition is active.

            The condition is fulfilled in two cases:
            1. If the base condition is fulfilled (determined by super().is_fulfilled())
            2. If the accept state is either "yes" or "ignore"

            Args:
                **kwargs: Additional keyword arguments (not used in this condition)

            Returns:
                bool: True if the override should be applied, False otherwise
            """
            if super().is_fulfilled(**kwargs):
                return True

            return self.accept == "yes" or self.accept == "ignore"

        def get_name(self) -> str:
            """
            Generate a unique identifier name for this condition.

            The name includes both the character and acceptance state in the format:
            PTAOverride(character, accept_state)

            Returns:
                str: A string in the format "PTAOverride(char, accept)"
            """
            return f"PTAOverride({self.char}, {self.accept})"

        def get_diff(self, char_obj: Union[str, Char]) -> num:
            """
            Calculate a weighted difference score based on the override settings.

            This method returns different scores based on:
            1. Whether the override applies to the given character
            2. The acceptance state of the override

            Score meanings:
            - 5000: Strong positive override (accept="yes")
            - -100: Negative override (accept="no")
            - -5000: Strong negative override (accept="ignore")
            - 0: Override doesn't apply to this character

            Args:
                char_obj (Union[str, Char]): Character object or identifier to evaluate
                    the override against. If None or invalid, defaults to school.

            Returns:
                num: A difference score indicating how strongly this override applies:
                    5000 for accept, -100 for reject, -5000 for ignore, 0 if not applicable
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
        A class representing a condition that evaluates its sub-condition in replay mode.

        This condition wrapper forces its sub-condition to be evaluated as if in a replay,
        by setting check_in_replay=True in the kwargs. This is useful for checking
        conditions that need to behave differently during replay vs normal gameplay.

        Attributes:
            condition (Condition): The condition to evaluate in replay mode
            display_in_desc (bool): Whether this condition should be displayed in descriptions
        """

        def __init__(self, condition: Condition, *options: Option):
            """
            Initialize a CheckReplay condition with a condition to evaluate.

            Args:
                condition (Condition): The condition object to evaluate in replay mode
            """
            super().__init__(False, *options)
            self.condition = condition
            self.display_in_desc = True

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Check if the sub-condition is fulfilled when evaluated in replay mode.

            This method adds check_in_replay=True to the kwargs before evaluating
            the sub-condition, forcing it to behave as if in replay mode.

            Args:
                **kwargs: Additional keyword arguments passed to the sub-condition,
                    with check_in_replay=True added

            Returns:
                bool: True if the sub-condition is fulfilled in replay mode
            """
            kwargs['check_in_replay'] = True
            return self.condition.is_fulfilled(**kwargs)

        def to_desc_text(self, **kwargs) -> Union[str, List[str]]:
            """
            Generate a human-readable description of the replay check condition.

            This method forwards the description request to the sub-condition,
            adding a visual indicator that this is a replay check.

            Args:
                **kwargs: Additional keyword arguments for description generation

            Returns:
                Union[str, List[str]]: The sub-condition's description with replay
                    indicator, either as a single string or a list of strings
            """
            desc_text = self.condition.to_desc_text(**kwargs)
            if isinstance(desc_text, str):
                return "{color=#616161}REPLAY{/color} " + desc_text
            else:
                return "\n".join(["{color=#616161}REPLAY{/color} " + desc for desc in desc_text])

        def get_name(self) -> str:
            """
            Generate a unique identifier name for this condition.

            The name is constructed by adding a "REPLAY_" prefix to the sub-condition's name.
            For example: "REPLAY_ConditionA"

            Returns:
                str: A unique string identifier for this condition
            """
            return "REPLAY_" + self.condition.get_name()

        def get_diff(self, char_obj: Union[str, Char]) -> num:
            """
            Calculate how close this condition is to being fulfilled in replay mode.

            This method evaluates the sub-condition's difference score as if in
            replay mode. The score is not inverted (unlike the NOT condition),
            as this is just a replay mode wrapper.

            Args:
                char_obj (Union[str, Char]): Character object or identifier to evaluate
                    the condition against.

            Returns:
                num: The difference score from the sub-condition, indicating how close
                    it is to being fulfilled in replay mode
            """
            diff = self.condition.get_diff(char_obj)
            return diff  # No inversion needed, just pass through the sub-condition's diff

    class EventSeenCondition(Condition):
        """
        A class representing a condition that checks if a game event has been seen by the player.

        This condition can be used to check whether specific events have been viewed or not,
        allowing for branching story paths or conditional content based on the player's
        event history.

        Attributes:
            seen (bool): When True, the condition is fulfilled if the event has been seen.
                When False, it's fulfilled if the event has not been seen. Defaults to False.
            display_in_desc (bool): Whether this condition should be displayed in descriptions.
                Inherited from base Condition class.
        """

        def __init__(self, seen: bool = False, *options: Option):
            """
            Initialize an EventSeenCondition with a seen state check.

            Args:
                seen (bool, optional): Whether to check if the event has been seen (True)
                    or not seen (False). Defaults to False.
            """
            super().__init__(True, *options)
            self.seen = seen

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Check if an event's seen status matches the desired state.

            The condition is fulfilled in two cases:
            1. If the base condition is fulfilled (determined by super().is_fulfilled())
            2. If the event's seen status matches the desired state (self.seen)

            The event to check is determined by the 'event_name' parameter in kwargs.

            Args:
                **kwargs: Must contain 'event_name' key specifying which event to check

            Returns:
                bool: True if the event's seen status matches self.seen, False otherwise
            """
            if super().is_fulfilled(**kwargs):
                return True

            return self.seen == get_event_seen(get_kwargs('event_name', **kwargs))

        def get_name(self) -> str:
            """
            Generate a unique identifier name for this condition.

            The name includes whether we're checking for seen or unseen state.
            For example: "EventSeenCondition(seen=True)" or "EventSeenCondition(seen=False)"

            Returns:
                str: A string in the format "EventSeenCondition(seen=X)"
            """
            return f"EventSeenCondition(seen={self.seen})"

    class JournalVoteCondition(Condition):
        """
        A class representing a condition that checks if a specific journal object is
        currently scheduled for voting.

        This condition tracks journal objects that have been scheduled for voting and
        can determine if a specific journal is currently up for vote. When initialized,
        it automatically registers the journal object in the global voting history.

        Attributes:
            _journal_obj (str): The identifier of the journal object to check for voting
            display_in_desc (bool): Whether this condition should be displayed in descriptions.
                Inherited from base Condition class.
        """

        def __init__(self, journal_obj: str, *options: Option):
            """
            Initialize a JournalVoteCondition for a specific journal object.

            This constructor also registers the journal object in the global
            registered_vote_events list to track voting history.

            Args:
                journal_obj (str): The identifier of the journal object to track
            """
            super().__init__(False, *options)
            self._journal_obj = journal_obj
            global registered_vote_events
            registered_vote_events.append(journal_obj)

        def is_fulfilled(self, **kwargs) -> bool:
            """
            Check if the specified journal object is currently scheduled for voting.

            The condition is fulfilled in two cases:
            1. If the base condition is fulfilled (determined by super().is_fulfilled())
            2. If there is an active vote proposal for this journal object

            Args:
                **kwargs: Additional keyword arguments (not used in this condition)

            Returns:
                bool: True if this journal object is currently up for vote, False otherwise
            """
            if super().is_fulfilled(**kwargs):
                return True

            vote_proposal = get_game_data('voteProposal')
            if vote_proposal == None:
                return False

            vote_obj = vote_proposal._journal_obj
            return self._journal_obj == vote_obj.get_name()

        def get_name(self) -> str:
            """
            Generate a unique identifier name for this condition.

            The name includes the journal object identifier in the format:
            JournalVoteCondition(journal_name)

            Returns:
                str: A string in the format "JournalVoteCondition(journal_obj)"
            """
            return f"JournalVoteCondition({self._journal_obj})"

    class JournalNRVoteCondition(Condition):
        """A condition class that checks if a journal object has never been scheduled for voting.

        This class evaluates whether the currently proposed journal object for voting has
        never been scheduled for voting before (i.e., is not in the registered_vote_events).
        It inherits from the base Condition class and provides specific implementation for
        checking the voting history of journal objects.

        Attributes:
            display_in_desc (bool): Whether to show in descriptions. Inherited from Condition,
                defaults to False.
        """

        def __init__(self, *options: Option):
            """Initialize a new JournalNRVoteCondition.

            The condition is initialized with display_in_desc set to False.
            """
            super().__init__(False, *options)

        def is_fulfilled(self, **kwargs) -> bool:
            """Check if the current journal object has never been scheduled for voting.

            This method first checks if the parent condition is fulfilled. If not, it checks
            if there is an active vote proposal and verifies that the journal object in the
            proposal has never been scheduled for voting before.

            Args:
                **kwargs: Additional keyword arguments (unused).

            Returns:
                bool: True if either:
                    - The parent condition is fulfilled
                    - The current journal object has never been scheduled for voting
                    False otherwise.
            """
            if super().is_fulfilled(**kwargs):
                return True

            vote_proposal = get_game_data('voteProposal')
            if vote_proposal == None:
                return False

            vote_obj = vote_proposal._journal_obj

            return vote_obj.get_name() not in registered_vote_events

        def get_name(self) -> str:
            """Get the name of this condition type.

            Returns:
                str: The string "JournalNRVoteCondition".
            """
            return "JournalNRVoteCondition"

    class BoolCondition(Condition):
        """
        A condition class that always returns a boolean value.

        This class is useful for conditions that are always true or false,
        regardless of the game state. It inherits from the base Condition class
        and provides specific implementation for the is_fulfilled and get_name methods.
        
        Attributes:
            value (bool): The boolean value to return for the condition.
        """
        def __init__(self, value: bool, *options: Option):
            super().__init__(True, *options)
            self.value = value

        def is_fulfilled(self, **kwargs) -> bool:
            return self.value

        def get_name(self) -> str:
            return f"BoolCondition({self.value})"
            
