init -3 python:
    from abc import ABC, abstractmethod
    import random
    from typing import Any
    from deprecated import deprecated

    rerollSelectors = []

    ##################
    # Selector Handler

    def reroll_selectors():
        """
        Rerolls all selectors
        """

        global rerollSelectors

        for selector in rerollSelectors:
            selector.roll_values()

        rerollSelectors.clear()

    ##################
    # Selector Classes

    class SelectorSet():
        """A class that manages a collection of Selectors for dynamic value generation in events.

        This class maintains a list of Selector objects that are used to generate dynamic values
        for events. Each Selector in the set can be rolled to generate new values, which happens
        automatically during initialization and after each parenting event.

        Args:
            *selectors: Variable number of Selector objects to initialize the set with.

        Attributes:
            _selectors (List[Selector]): Internal list storing all Selector objects.

        Example:
            ```python
            # Create selectors
            stat_selector = StatSelector("strength", "strength", "player", [0, 100])
            time_selector = TimeSelector("current_time", "day")
            
            # Create a selector set with initial selectors
            selector_set = SelectorSet(stat_selector, time_selector)
            
            # Add more selectors later if needed
            level_selector = LevelSelector("player_level", "player")
            selector_set.add_selector(level_selector)
            
            # Get all values as kwargs for an event
            event_kwargs = selector_set.get_values()
            ```

        Notes:
            - The class handles special cases for KwargsSelector and StatSelector differently 
                during value rolling and retrieval.
            - Values are cached within each Selector after rolling until the next roll.
            - The get_values method ensures values are rolled at least once before retrieval.
        """

        def __init__(self, *selectors: Selector):
            self._selectors = list(selectors)

        def add_selector(self, *selector: Selector):
            """Adds one or more selectors to the set.

            Args:
                *selector: Variable number of Selector objects to add to the set.
                    Each selector will be used to generate values for events.

            Example:
                ```python
                # Add a single selector
                selector_set.add_selector(TimeSelector("day", "day"))
                
                # Add multiple selectors at once
                selector_set.add_selector(
                    StatSelector("strength", "str", "player", [0, 100]),
                    LevelSelector("level", "player")
                )
                ```
            """
            self._selectors.extend(selector)

        def roll_values(self, **kwargs):
            """Rerolls and caches values for all selectors in the set.

            This method updates all selectors in the set, handling special cases for
            KwargsSelector and StatSelector differently. For KwargsSelector, all its
            key-value pairs are added to kwargs. For StatSelector, both the value
            and its range are added to kwargs.

            Args:
                **kwargs: Arbitrary keyword arguments passed to each selector's
                    update() and get_value() methods. These kwargs are also updated
                    with the new values from each selector.

            Notes:
                - KwargsSelector values are added directly to kwargs with their original keys
                - StatSelector adds both the value and its range (with "_range" suffix)
                - All other selectors add their value using their key name
            """
            for selector in self._selectors:
                selector.update(**kwargs)
                if isinstance(selector, KwargsSelector):
                    values = selector.get_value(**kwargs)
                    for key in values.keys():
                        kwargs[key] = values[key]
                elif isinstance(selector, StatSelector):
                    key = selector.get_name()
                    value = selector.get_value(**kwargs)
                    kwargs[key + "_range"] = selector._range
                    kwargs[key] = value
                else:
                    key = selector.get_name()
                    value = selector.get_value(**kwargs)
                    kwargs[key] = value

        def get_values(self, **kwargs) -> dict:
            """Retrieves current values from all selectors in the set.

            If the first selector's value is None, all selectors are rerolled first.
            This ensures we always have valid values when returning.

            Args:
                **kwargs: Arbitrary keyword arguments passed to each selector's
                    get_value() method. These kwargs are also updated with the
                    values from each selector.

            Returns:
                dict: A dictionary containing all selector values, where keys are
                    the selector names and values are their current values. For
                    KwargsSelector, multiple key-value pairs may be added.

            Example:
                ```python
                # Get all values as kwargs for an event
                kwargs = selector_set.get_values()
                # kwargs might look like:
                # {
                #     'strength': 75,
                #     'strength_range': [0, 100],
                #     'current_time': 'day',
                #     'player_level': 5
                # }
                ```
            """
            if len(self._selectors) > 0 and (self._selectors[0].get_value(**kwargs) is None or self._selectors[0].get_value(**kwargs) == None):
                self.roll_values(**kwargs)

            for selector in self._selectors:
                if isinstance(selector, KwargsSelector):
                    values = selector.get_value(**kwargs)
                    for key in values.keys():
                        kwargs[key] = values[key]
                else:
                    key = selector.get_name()
                    value = selector.get_value(**kwargs)
                    kwargs[key] = value

            return kwargs

        def find_by_type(self, type: type) -> List[Selector]:
            output = []

            for selector in self._selectors:
                output.extend(selector.find_by_type(type))
            return output

    class Selector(ABC):
        """Abstract base class for dynamic value selection in events.

        This class serves as the foundation for all selector types in the event system.
        Each selector is responsible for providing a dynamic value that can be used as
        a parameter in events. Values can be updated in real-time or cached based on
        configuration.

        Args:
            realtime (bool): If True, value is recalculated on each get_value() call.
                If False, value is cached until explicitly updated.
            key (str): Unique identifier for this selector's value in event kwargs.

        Attributes:
            _key (str): Identifier used to store this selector's value in event kwargs.
            _value (Any): Currently cached value. None if not yet calculated.
            _realtime (bool): Whether to recalculate value on each retrieval.

        Example:
            ```python
            class MySelector(Selector):
                def __init__(self, key: str):
                    super().__init__(realtime=False, key=key)
                
                def roll(self, **kwargs) -> Any:
                    return random.choice([1, 2, 3])
            
            # Usage
            selector = MySelector("random_number")
            value = selector.get_value()  # Gets cached value
            selector.update()  # Force value update
            ```

        Notes:
            - Subclasses must implement the roll() method to define value generation logic
            - Values are lazily calculated on first access if not in realtime mode
            - The update() method can be called to force a value recalculation
            - All value access should go through get_value() to respect realtime setting
        """

        def __init__(self, realtime: bool, key: str, *options: Option):
            self._key = key
            self._value = None
            self._realtime = realtime
            self.options = OptionSet(*options)

        def get_option_set(self):
            if self.options == None:
                return empty_option_set
            return self.options

        @property
        def _type(self) -> str:
            return "selector"

        def find_by_type(self, type: type) -> List[Selector]:
            if self._type == type:
                return [self]
            return []

        def __str__(self):
            return self.get_name()  # Fixed the method call

        def update(self, **kwargs):
            """Forces an update of the selector's value.

            Calls the roll() method and caches the new value.

            Args:
                **kwargs: Arbitrary keyword arguments passed to roll().
            """
            self._value = self.roll(**kwargs)

        @abstractmethod
        def roll(self, **kwargs) -> Any:
            """Generates a new value for this selector.

            This abstract method must be implemented by all subclasses to define
            their specific value generation logic.

            Args:
                **kwargs: Arbitrary keyword arguments that may influence value generation.

            Returns:
                Any: The newly generated value.
            """
            pass

        def get_name(self) -> str:
            """Returns the selector's key identifier.

            Returns:
                str: The key used to identify this selector's value in event kwargs.
            """
            return self._key

        def get_value(self, **kwargs) -> Any:
            """Retrieves the selector's current value.

            If in realtime mode or value hasn't been calculated yet,
            triggers a new value calculation via update().

            Args:
                **kwargs: Arbitrary keyword arguments passed to roll() if update needed.

            Returns:
                Any: The selector's current value.
            """
            if self._realtime or self._value == None:
                self.update(**kwargs)
            return self._value
        
        def get_key_value(self) -> tuple:
            """Returns the selector's key and current value as a tuple.

            If in realtime mode, triggers a value update before returning.

            Returns:
                tuple: A (key, value) pair where key is the selector's identifier
                    and value is its current value.
            """
            if self._realtime:
                self.update()
            return self._key, self._value

    class RandomListSelector(Selector):
        """
        A Selector-class that chooses a random value from a list of values.
        RandomListSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _list: List[Any]
            - A list of values that can be chosen from.
            - The list can contain everything the get_random_choice()-function can handle.

        ### Methods:
        1. roll() -> Any
            - Returns a random value from the list.
            - If the chosen value is a Selector, the Selector will recursively roll its value and then return the resulting value
        
        ### Parameters:
        1. key: str
            - The key of the value.
            - The key is used to identify the value in the events kwargs.
        2. values: Any
            - A list of values that can be chosen from.
            - The list can contain everything the get_random_choice()-function can handle.
            - If the list contains a Selector and the Selector has been chosen, the Selector will be rolled and the resulting value will be used.
        3. realtime: bool (default: False)
            - A boolean that determines whether the value should be updated on retrieving the value or not.
            - If True, the value will be updated on retrieval.
            - If False, the value will only be updated, when the update()-method is triggered.
        """

        def __init__(self, key: str, *values: Any, realtime: bool = False, alt: Any = None, options: List[Option] = []):
            super().__init__(realtime, key, *options)
            self._list = values 
            self._alt = alt

        @property
        def _type(self) -> str:
            return "random_list"

        def find_by_type(self, type: type) -> List[Selector]:
            output = []
            if self._type == type:
                output.append(self)
            
            for value in self._list:
                if isinstance(value, Selector):
                    output.extend(value.find_by_type(type))

            return output

        def roll(self, **kwargs) -> Any:
            """
            Returns a random value from the list.
            """

            value = get_random_choice(*self._list, **kwargs)
            if value == None:
                value = self._alt
            while isinstance(value, Selector):
                value = value.roll(**kwargs)
            return value

    class IterativeListSelector(Selector):
        """
        A Selector-class that chooses a value from a list in an iterative manner.
        IterativeListSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _list: List[Any]
            - A list of values that can be chosen from.
            - The list can contain everything the get_random_choice()-function can handle.
        2. _old_value: Any
            - The last chosen value.
            - If the value is a Selector, the Selector will recursively roll its value and then return the resulting value

        ### Methods:
        1. roll() -> Any
            - Returns the next value in the list.
            - If the list is empty, the value will be None.
            - If the value is a Selector, the Selector will recursively roll its value and then return the resulting value
        
        ### Parameters:
        1. key: str
            - The key of the value.
            - The key is used to identify the value in the events kwargs.
        2. values: Any
            - A list of values that can be chosen from.
        3. realtime: bool (default: False)
            - A boolean that determines whether the value should be updated on retrieving the value or not.
            - If True, the value will be updated on retrieval.
            - If False, the value will only be updated, when the update()-method is triggered.
        """

        def __init__(self, key: str, *values: Any, realtime: bool = False, options: List[Option] = []):
            super().__init__(realtime, key, *options)
            self._list = values
            self._old_value = None

        @property
        def _type(self) -> str:
            return "iterative_list"

        def find_by_type(self, type: type) -> List[Selector]:
            output = []
            if self._type == type:
                output.append(self)
            
            for value in self._list:
                if isinstance(value, Selector):
                    output.extend(value.find_by_type(type))

            return output

        def roll(self, **kwargs) -> Any:
            """
            Returns the next value in the list.
            """

            if self._old_value == None:
                self._old_value = self._list[0]
            else:
                current_index = self._list.index(self._old_value)
                next_index = (current_index + 1) % len(self._list)
                self._old_value = self._list[next_index]
            value = self._old_value
            while isinstance(value, Selector):
                value = value.roll(**kwargs)
            return value
            

    class RandomValueSelector(Selector):
        """
        A Selector-class that chooses a random integer between a minimum and a maximum value.
        RandomValueSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _min_value: int
            - The minimum value that can be rolled. (inclusive)
        2. _max_value: int
            - The maximum value that can be rolled. (inclusive)

        ### Methods:
        1. roll() -> Any
            - Returns a random value from in between the minimum and maximum value.

        ### Parameters:
        1. key: str
            - The key of the value.
            - The key is used to identify the value in the events kwargs.
        2. min_value: int
            - The minimum value that can be rolled. (inclusive)
        3. max_value: int
            - The maximum value that can be rolled. (inclusive)
        4. realtime: bool (default: False)
            - A boolean that determines whether the value should be updated on retrieving the value or not.
            - If True, the value will be updated on retrieval.
            - If False, the value will only be updated, when the update()-method is triggered.
        """

        def __init__(self, key: str, min_value: int, max_value: int, realtime: bool = False, *options):
            super().__init__(realtime, key, *options)
            self._min_value = min_value
            self._max_value = max_value

        @property
        def _type(self) -> str:
            return "random_value"

        def roll(self, **kwargs) -> Any:
            """
            Returns a random value from in between the minimum and maximum value.
            """

            value = get_random_int(self._min_value, self._max_value)
            return value

    class ConditionSelector(Selector):
        """A selector that returns different values based on a condition's state.

        This selector evaluates a condition and returns either a true_value or false_value
        based on whether the condition is fulfilled. Both true and false values can be
        other Selectors, in which case their values will be recursively evaluated.

        Args:
            key (str): Unique identifier for this selector's value in event kwargs.
            condition (Condition): The condition object that determines which value to return.
            true_value (Any): Value to return when condition is fulfilled. Can be another Selector.
            false_value (Any): Value to return when condition is not fulfilled. Can be another Selector.
            realtime (bool, optional): Whether to re-evaluate on each value retrieval.
                Defaults to False.

        Attributes:
            _condition (Condition): Stored condition that determines value selection.
            _true_value (Any): Value returned when condition is fulfilled.
            _false_value (Any): Value returned when condition is not fulfilled.

        Example:
            ```python
            # Create a condition that checks if player level is above 5
            level_condition = LevelCondition("player", 5)
            
            # Return different messages based on level
            message_selector = ConditionSelector(
                key="level_message",
                condition=level_condition,
                true_value="You're experienced enough!",
                false_value="You need more experience."
            )
            
            # Can also use other selectors as values
            reward_selector = ConditionSelector(
                key="reward",
                condition=level_condition,
                true_value=RandomListSelector("item", ["rare_sword", "magic_staff"]),
                false_value=RandomListSelector("item", ["training_sword", "wooden_staff"])
            )
            ```

        Notes:
            - The condition is evaluated each time roll() is called
            - If true_value or false_value is a Selector, its roll() method is called
            - Nested selectors inherit the kwargs passed to roll()
        """

        def __init__(self, key: str, condition: Condition, true_value: Any, false_value: Any, realtime: bool = False, *options: Option):
            super().__init__(realtime, key, *options)
            self._condition = condition
            self._true_value = true_value
            self._false_value = false_value

        @property
        def _type(self) -> str:
            return "condition"

        def find_by_type(self, type: type) -> List[Selector]:
            output = []
            if self._type == type:
                output.append(self)
            if isinstance(self._true_value, Selector):
                output.extend(self._true_value.find_by_type(type))
            if isinstance(self._false_value, Selector):
                output.extend(self._false_value.find_by_type(type))
            return output

        def roll(self, **kwargs) -> Any:
            """Evaluates the condition and returns the appropriate value.

            First checks if the condition is fulfilled, then returns either
            true_value or false_value accordingly. If the chosen value is itself
            a Selector, its roll() method is called recursively.

            Args:
                **kwargs: Arbitrary keyword arguments passed to both the condition
                    evaluation and any nested selector's roll() method.

            Returns:
                Any: Either true_value or false_value, depending on the condition.
                    If the chosen value is a Selector, returns its rolled value.

            Example:
                ```python
                # Simple condition selector
                selector = ConditionSelector(
                    "message",
                    TimeCondition("day"),
                    "Good morning!",
                    "Good evening!"
                )
                
                # The value will depend on the time of day
                message = selector.roll()
                ```
            """
            value = self._true_value if self._condition.is_fulfilled(**kwargs) else self._false_value
            if isinstance(value, Selector):
                return value.roll(**kwargs)
            return value

    class StatSelector(Selector):
        """
        A Selector-class that sets a stat-value.
        StatSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _stat: str | Selector
            - The name of the stat.
            - if the stat is a Selector, the Selector will recursively roll its value and then return the resulting value
        2. _char: str | Selector
            - The key of the character.
            - The character is used to identify the character in the character dictionary.
            - See method get_character_by_key() in the character module for more information.
            - if the character is a Selector, the Selector will recursively roll its value and then return the resulting value

        ### Methods:
        1. roll() -> Any
            - Returns the value of the stat.

        ### Parameters:
        1. key: str
            - The key of the value.
            - The key is used to identify the value in the events kwargs.
        2. stat: str
            - The name of the stat.
        3. char: str
            - The key of the character.
            - The character is used to identify the character in the character dictionary.
            - See method get_character_by_key() in the character module for more information.
        4. realtime: bool (default: True)
            - A boolean that determines whether the value should be updated on retrieving the value or not.
            - If True, the value will be updated on retrieval.
            - If False, the value will only be updated, when the update()-method is triggered.
            - Realtime should be set to True, otherwise the event could work with out of date stat information
        """

        def __init__(self, key: str, stat: str | Selector, char: str | Selector, stat_range: List[int], realtime: bool = True, *options: Option):
            super().__init__(realtime, key)
            self._stat = stat
            self._char = char
            self._range = stat_range

        @property
        def _type(self) -> str:
            return "stat"

        def find_by_type(self, type: type) -> List[Selector]:
            output = []
            if self._type == type:
                output.append(self)
            if isinstance(self._stat, Selector):
                output.extend(self._stat.find_by_type(type))
            if isinstance(self._char, Selector):
                output.extend(self._char.find_by_type(type))
            return output

        def roll(self, **kwargs) -> Any:
            """
            Returns the value of the stat.
            """

            char = self._char if not isinstance(self._char, Selector) else self._char.get_value(**kwargs)
            stat = self._stat if not isinstance(self._stat, Selector) else self._stat.get_value(**kwargs)

            return get_character_by_key(char).get_stat_number(stat)

    class LevelSelector(Selector):
        """
        A Selector-class that sets a level-value.
        LevelSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _char: str
            - The key of the character.
            - The character is used to identify the character in the character dictionary.
            - See method get_character_by_key() in the character module for more information.

        ### Methods:
        1. roll() -> Any
            - Returns the value of the level.

        ### Parameters:
        1. key: str
            - The key of the value.
            - The key is used to identify the value in the events kwargs.
        2. char_key: str
            - The key of the character.
            - The character is used to identify the character in the character dictionary.
            - See method get_character_by_key() in the character module for more information.
        3. realtime: bool (default: True)
            - A boolean that determines whether the value should be updated on retrieving the value or not.
            - If True, the value will be updated on retrieval.
            - If False, the value will only be updated, when the update()-method is triggered.
            - Realtime should be set to True, otherwise the event could work with out of date stat information
        """

        def __init__(self, key: str, char: str | Selector, *options: Option):
            super().__init__(True, key, *options)
            self._char = char

        @property
        def _type(self) -> str:
            return "level"

        def find_by_type(self, type: type) -> List[Selector]:
            output = []
            if self._type == type:
                output.append(self)
            if isinstance(self._char, Selector):
                output.extend(self._char.find_by_type(type))
            return output

        def roll(self, **kwargs) -> Any:
            """
            Returns the value of the level.
            """

            char = self._char if not isinstance(self._char, Selector) else self._char.get_value(**kwargs)

            return get_character_by_key(char).get_level()

    class TimeSelector(Selector):
        """
        A Selector-class that sets a time-value.
        TimeSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _time_type: str
            - The type of the time.
            - The time_type is used to identify the time in the time module.

        ### Methods:
        1. roll() -> Any
            - Returns the value of the time.

        ### Parameters:
        1. key: str
            - The key of the value.
            - The key is used to identify the value in the events kwargs.
        2. time_type: str
            - The type of the time.
            - The time_type is used to identify the time in the time module.
            - See the roll() method for more information.
        """

        def __init__(self, key: str, time_type: str, *options: Option):
            super().__init__(True, key, *options)
            self._time_type = time_type

        @property
        def _type(self) -> str:
            return "time"

        def roll(self, **kwargs) -> Any:
            """
            Returns the value of the time.
            The time_type is used to identify the time in the time module.
            The following time_types are available:
                1. "day": The day of the month.
                2. "month": The month of the year.
                3. "year": The year.
                4. "daytime": The daytime.
                5. "weekday": The weekday.
            If none of these are specified, the time will be returned as a string.
            """

            if self._time_type == "day":
                return time.get_day()
            elif self._time_type == "month":
                return time.get_month()
            elif self._time_type == "year":
                return time.get_year()
            elif self._time_type == "daytime":
                return time.get_daytime()
            elif self._time_type == "weekday":
                return time.get_weekday()
            else:
                return time.day_to_string()

    class NumClampSelector(Selector):
        """
        A Selector-class that sets a value between a minimum and a maximum value.
        NumClampSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _value: int | float | Selector
            - The value to be inserted.
            - If the value is a Selector, the Selector will recursively roll its value and then return the resulting value
        2. _min_value: int | float | str | Selector
            - The minimum value that can be rolled. (inclusive)
            - If the value is a Selector, the Selector will recursively roll its value and then return the resulting value
        3. _max_value: int | float | str | Selector
            - The maximum value that can be rolled. (inclusive)
            - If the value is a Selector, the Selector will recursively roll its value and then return the resulting value
        """

        def __init__(self, key: str, value: int | float | Selector, *options: Option, min_value: int | float | str | Selector = -1, max_value: int | float | str | Selector = -1):
            super().__init__(True, key, *options)
            self._value = value
            self._min_value = min_value
            self._max_value = max_value

        @property
        def _type(self) -> str:
            return "num_clamp"

        def find_by_type(self, type: type) -> List[Selector]:
            output = []
            if self._type == type:
                output.append(self)
            if isinstance(self._value, Selector):
                output.extend(self._value.find_by_type(type))
            if isinstance(self._min_value, Selector):
                output.extend(self._min_value.find_by_type(type))
            if isinstance(self._max_value, Selector):
                output.extend(self._max_value.find_by_type(type))
            return output

        def roll(self, **kwargs) -> Any:
            value = self._value if not isinstance(self._value, Selector) else self._value.get_value(**kwargs)
            min_value = self._min_value if not isinstance(self._min_value, Selector) else self._min_value.get_value(**kwargs)
            max_value = self._max_value if not isinstance(self._max_value, Selector) else self._max_value.get_value(**kwargs)

            value = float(value) if isinstance(value, str) and value.is_float() else -1
            min_value = float(min_value) if isinstance(min_value, str) and min_value.is_float() else -1
            max_value = float(max_value) if isinstance(max_value, str) and max_value.is_float() else -1

            min_value = min_value if min_value != -1 else value
            max_value = max_value if max_value != -1 else value

            value = clamp_value(value, min_value, max_value)

            return value

    class ValueSelector(Selector):
        """
        A Selector-class that sets a value on initialisation for insertion into the event
        ValueSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _value: Any
            - The value to be inserted.
            - If the value is a Selector, the Selector will recursively roll its value and then return the resulting value

        ### Methods:
        1. roll() -> Any
            - Returns the value.

        ### Parameters:
        1. key: str
            -The key of the value.
        2. value: Any
            -The value of the value.
        """
        
        def __init__(self, key: str, value: Any, *options: Option):
            super().__init__(True, key, *options)
            self._value = value

        @property
        def _type(self) -> str:
            return "value"

        def find_by_type(self, type: type) -> List[Selector]:
            output = []
            if self._type == type:
                output.append(self)
            if isinstance(self._value, Selector):
                output.extend(self._value.find_by_type(type))
            return output

        def roll(self, **kwargs) -> Any:
            """
            Returns the value.
            """

            value = self._value

            if isinstance(value, Selector):
                value = value.get_value(**kwargs)

            return value

    class KwargsValueSelector(Selector):
        """
        A Selector-class that gets a value from the supplied kwargs via key and returns it
        KwargsValueSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _key: str | Selector
            - The key of the value in the kwargs.

        ### Methods:
        1. roll() -> Any
            - Returns the value.

        ### Parameters:
        1. key: str
            -The key of the value.
        2. kwargs_key: str | Selector
            - The key of the value in the kwargs.
        """
        
        def __init__(self, key: str, kwargs_key: str | Selector, *options: Option):
            super().__init__(True, key, *options)
            self._key = kwargs_key

        @property
        def _type(self) -> str:
            return "kwargs_value"

        def find_by_type(self, type: type) -> List[Selector]:
            output = []
            if self._type == type:
                output.append(self)
            if isinstance(self._key, Selector):
                output.extend(self._key.find_by_type(type))
            return output

        def roll(self, **kwargs) -> Any:
            """
            Returns the value.
            """

            key = self._key

            if isinstance(key, Selector):
                key = key.get_value(**kwargs)

            return get_kwargs(key, None, **kwargs)

    class DictSelector(Selector):
        """
        A Selector-class that chooses a value from a dictionary.
        DictSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _index: str
            - The key for the kwargs from where the the index for the dict is determined.
            - This parameter takes the value in kwargs[_index] and uses it as the index for the dict.
        2. _dict: Dict
            - The dictionary from which the value is chosen.

        ### Methods:
        1. roll() -> Any
            - Returns the value from the dict.

        ### Parameters:
        1. key: str
            - The key of the value.
            - The key is used to identify the value in the events kwargs.
        2. index: str
            - The key for the kwargs from where the the index for the dict is determined.
            - This parameter takes the value in kwargs[_index] and uses it as the index for the dict.
        """

        def __init__(self, key: str, index: str, dict: Dict, *options: Option):
            super().__init__(True, key, *options)
            self._index = index
            self._dict = dict

        @property
        def _type(self) -> str:
            return "dict"

        def find_by_type(self, type: type) -> List[Selector]:
            output = []
            if self._type == type:
                output.append(self)
            if isinstance(self._index, Selector):
                output.extend(self._index.find_by_type(type))
            return output

        def roll(self, **kwargs) -> Any:
            """
            Returns the value from the dict.
            """

            if self._index not in kwargs or kwargs[self._index] not in self._dict:
                return None

            value = self._dict[kwargs[self._index]]
            if isinstance(value, Selector):
                return value.get_value(**kwargs)

            return value

    class GameDataSelector(Selector):
        """
        A Selector-class that chooses a value from the GameData Storage.
        GameDataSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _index: str
            - The key for the GameData Storage from where the the value is determined.
            - This parameter takes the value in get_game_data(_index) and uses it as the value for the Selector.

        ### Methods:
        1. roll() -> Any
            - Returns the value from the GameData Storage.

        ### Parameters:
        1. key: str
            - The key of the value.
            - The key is used to identify the value in the events kwargs.
        2. index: str
            - The key for the GameData Storage from where the the value is determined.
            - This parameter takes the value in get_game_data(_index) and uses it as the value for the Selector.
        """

        def __init__(self, key: str, index: str, alt: Any = None, *options: Option):
            super().__init__(True, key, *options)
            self._index = index
            self._alt = alt

        @property
        def _type(self) -> str:
            return "game_data"

        def roll(self, **kwargs) -> Any:
            """
            Returns the value from the GameData Storage.
            """

            output = get_game_data(self._index)
            if output == None:
                return self._alt
            return output

    class KwargsSelector(Selector):
        """
        A Selector-class that supplies fixed values to the event.
        KwargsSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _kwargs: Dict
            - A dictionary that contains the values to be supplied to the event.

        ### Methods:
        1. roll() -> Any
            - Returns the supplied values.

        ### Parameters:
        1. kwargs: Dict
            - A dictionary that contains the values to be supplied to the event.
        """

        def __init__(self, *options: Option, **kwargs):
            super().__init__(True, "None", *options)
            self._kwargs = kwargs

        @property
        def _type(self) -> str:
            return "kwargs"

        def roll(self, **kwargs) -> Any:
            """
            Returns the supplied values.
            """
            return self._kwargs

    class ProgressSelector(Selector):
        """
        A Selector-class that chooses a value from the Event Progress Database.
        ProgressSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _index: str | Selector
            - The key for the Event Progress Database from where the the value is determined.
            - This parameter takes the value in get_progress(_index) and uses it as the value for the Selector.
            - If the index is a Selector, the Selector will recursively roll its value and then return the resulting value

        ### Methods:
        1. roll() -> Any
            - Returns the value from the Event Progress Database.
            - If the index is not found in the Event Progress Database, -1 will be returned.

        ### Parameters:
        1. key: str
            - The key of the value.
            - The key is used to identify the value in the events kwargs.
        2. index: str
            - The key for the Event Progress Database from where the the value is determined.
            - This parameter takes the value in get_progress(_index) and uses it as the value for the Selector.
        """

        def __init__(self, key: str, index: str | Selector, *options: Option):
            super().__init__(True, key, *options)
            self._index = index

        @property
        def _type(self) -> str:
            return "progress"

        def find_by_type(self, type: type) -> List[Selector]:
            output = []
            if self._type == type:
                output.append(self)
            if isinstance(self._index, Selector):
                output.extend(self._index.find_by_type(type))
            return output

        def roll(self, **kwargs) -> Any:
            """
            Returns the progress of the Event Progress Database.
            """

            index = self._index if not isinstance(self._index, Selector) else self._index.get_value(**kwargs)

            return get_progress(index)

    @deprecated(version='0.2.3', reason="Rules merged into Unlockables; use BuildingUnlockedSelector (any unlockable key) or an UnlockableCondition. Kept for save compatibility.")
    class RuleUnlockedSelector(Selector):
        """
        A Selector-class that stores if the rule is unlocked
        RuleUnlockedSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _rule: str | Selector
            - The rule that is checked for being unlocked.
            - if the rule is a Selector, the Selector will recursively roll its value and then return the resulting value

        ### Methods:
        1. roll() -> Any
            - Returns the value of the rule.

        ### Parameters:
        1. key: str
            - The key of the value.
            - The key is used to identify the value in the events kwargs.
        2. rule: str
            - The key of the rule.
            - The rule is used to identify the rule in the rule dictionary.
        """

        def __init__(self, key: str, rule: str | Selector, *options: Option):
            super().__init__(True, key, *options)
            self._rule = rule

        @property
        def _type(self) -> str:
            return "rule_unlocked"

        def roll(self, **kwargs) -> Any:
            rule_key = self._rule if not isinstance(self._rule, Selector) else self._rule.get_value(**kwargs)
            return is_unlockable_unlocked(rule_key)

    @deprecated(version='0.2.3', reason="Clubs merged into Unlockables; use BuildingUnlockedSelector (any unlockable key) or an UnlockableCondition. Kept for save compatibility.")
    class ClubUnlockedSelector(Selector):
        """
        A Selector-class that stores if the club is unlocked
        ClubUnlockedSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _club: str | Selector
            - The club that is checked for being unlocked.

        ### Methods:
        1. roll() -> Any
            - Returns the value of the club.

        ### Parameters:
        1. key: str
            - The key of the value.
            - The key is used to identify the value in the events kwargs.
        2. club: str
            - The key of the club.
            - The club is used to identify the club in the club dictionary.
        """

        def __init__(self, key: str, club: str | Selector, *options: Option):
            super().__init__(True, key, *options)
            self._club = club

        @property
        def _type(self) -> str:
            return "club_unlocked"

        def roll(self, **kwargs) -> Any:
            club_key = self._club if not isinstance(self._club, Selector) else self._club.get_value(**kwargs)
            return is_unlockable_unlocked(club_key)

    class BuildingUnlockedSelector(Selector):
        """
        A Selector-class that stores if the building is unlocked
        BuildingUnlockedSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _building: str | Selector
            - The building that is checked for being unlocked.

        ### Methods:
        1. roll() -> Any
            - Returns the value of the building.

        ### Parameters:
        1. key: str
            - The key of the value.
            - The key is used to identify the value in the events kwargs.
        2. building: str
            - The key of the building.
            - The building is used to identify the building in the building dictionary.
        """

        def __init__(self, key: str, building: str | Selector, *options: Option):
            super().__init__(True, key, *options)
            self._building = building

        @property
        def _type(self) -> str:
            return "building_unlocked"

        def find_by_type(self, type: type) -> List[Selector]:
            output = []
            if self._type == type:
                output.append(self)
            if isinstance(self._building, Selector):
                output.extend(self._building.find_by_type(type))
            return output

        def roll(self, **kwargs) -> Any:
            building_key = self._building if not isinstance(self._building, Selector) else self._building.get_value(**kwargs)
            return building_manager.is_open(building_key)

    class BuildingLevelSelector(Selector):
        """
        A Selector-class that stores the level of the building
        BuildingLevelSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _building: str | Selector
            - The building that is checked for being unlocked.

        ### Methods:
        1. roll() -> Any
            - Returns the level of the building.

        ### Parameters:
        1. key: str
            - The key of the value.
            - The key is used to identify the value in the events kwargs.
        2. building: str
            - The key of the building.
            - The building is used to identify the building in the building dictionary.
        """

        def __init__(self, key: str, building: str | Selector, *options: Option):
            super().__init__(True, key, *options)
            self._building = building

        @property
        def _type(self) -> str:
            return "building_level"

        def find_by_type(self, type: type) -> List[Selector]:
            output = []
            if self._type == type:
                output.append(self)
            if isinstance(self._building, Selector):
                output.extend(self._building.find_by_type(type))
            return output

        def roll(self, **kwargs) -> Any:
            building = self._building if not isinstance(self._building, Selector) else self._building.get_value(**kwargs)

            return unlockable_manager.get_current_level_of_unlockable(building)

    class CharacterSelector(Selector):
        """
        A Selector-class that stores the character
        CharacterSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _char: str
            - The key of the character.
            - The character is used to identify the character in the character dictionary.
            - See method get_character_by_key() in the character module for more information.

        ### Methods:
        1. roll() -> Any
            - Returns the character.

        ### Parameters:
        1. key: str
            - The key of the value.
            - The key is used to identify the value in the events kwargs.
        2. char: str
            - The key of the character.
            - The character is used to identify the character in the character dictionary.
            - See method get_character_by_key() in the character module for more information.
            - possible keys: school, parent, teacher, secretary
        """

        def __init__(self, key: str, char: str | Selector = 'school', *options: Option):
            super().__init__(True, key, *options)
            self._char = char

        @property
        def _type(self) -> str:
            return "character"

        def find_by_type(self, type: type) -> List[Selector]:
            output = []
            if self._type == type:
                output.append(self)
            if isinstance(self._char, Selector):
                output.extend(self._char.find_by_type(type))
            return output

        def roll(self, **kwargs) -> Any:

            char = self._char if not isinstance(self._char, Selector) else self._char.get_value(**kwargs)

            return get_character_by_key(char)

    @deprecated(version='0.2.3', reason="Replaced by Unlockable.roll_votes(); kept for save compatibility.")
    class PTAVoteSelector(Selector):
        """
        Legacy PTA vote selector referenced by old event definitions and saves.
        """

        def __init__(self, key: str, condition_type: str = 'misc', *options: Option):
            super().__init__(True, key, *options)
            self._condition_type = condition_type

        @property
        def _type(self) -> str:
            return "pta_vote"

        def roll(self, **kwargs) -> Any:
            return None

    class PTAObjectSelector(Selector):
        """
        Loads the scheduled Unlockable from ``voteProposal`` into event kwargs.
        """

        def __init__(self, key: str, *options: Option):
            super().__init__(True, key, *options)

        @property
        def _type(self) -> str:
            return "pta_object"

        def roll(self, **kwargs) -> Any:
            return get_game_data('voteProposal')

    class SituationBarSelector(Selector):
        """
        A Selector-class that chooses a value from the Situation Bar.
        SituationBarSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _situation_key: str
            - The key of the situation.
        """

        def __init__(self, key: str, situation_key: str, bar_key: str, *options: Option):
            super().__init__(True, key, *options)
            self._situation_key = situation_key
            self._bar_key = bar_key

        @property
        def _type(self) -> str:
            return "situation_bar"

        def roll(self, **kwargs) -> Any:
            situation = situation_manager.get_situation(self._situation_key)
            if situation == None:
                return 0
            bar = situation.get_bar(self._bar_key)
            if bar == None:
                return 0
            return bar.value

    class ModifierSelector(Selector):
        def __init__(self, key: str, modifier: Modifier_Obj, stat: str, *options: Option, collection: str = "default"):
            super().__init__(True, key, *options)
            self._modifier = modifier
            self._stat = stat
            self._collection = collection

        @property
        def _type(self) -> str:
            return "modifier"

        def roll(self, **kwargs) -> Any:
            return (self._modifier, self._stat, self._collection)