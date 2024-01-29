init -3 python:

    from abc import ABC, abstractmethod
    import random
    from typing import Any

    class SelectorSet():
        """
        A class that stores and maintains a list of Selectors
        A SelectorSet rerolls all of its selectors when roll_values is called, which happens once on initialisation and 
        once every time after the parenting event is called.

        ### Attributes:
        1. _selectors: List[Selector]
            - A list of selectors that are used to define in-event values.

        ### Methods:
        1. add_selector(*selector: Selector)
            - Adds a selector to the list of selectors.
        2. roll_values()
            - Rerolls the values of each stored Selector and caches them in the corresponding Selector.
        3. get_values() -> List[Tuple[str, Any]]
            - Returns a list of tuples containing the name and the value of the values.
            - The return value is formatted in a way, that it can be used to directly update the kwargs of an event.

        ### Parameters:
        1. selectors: Selector
            - A list of selectors that are used to define in-event values.
        """

        def __init__(self, *selectors: Selector):
            self._selectors = list(selectors)

        def add_selector(self, *selector: Selector):
            """
            Adds a selector to the list of selectors.

            ### Parameters:
            1. selector: Selector
                - A list of selectors that are used to define in-event values.
            """

            self._selectors.extend(selector)

        def roll_values(self):
            """
            Rerolls the values of each stored Selector and caches them in the corresponding Selector.
            """

            kwargs = {}

            for selector in self._selectors:
                selector.update(**kwargs)
                key = selector.get_name()
                value = selector.get_value(**kwargs)
                kwargs[key] = value

        def get_values(self) -> List[Tuple[str, Any]]:
            """
            Returns a list of tuples containing the name and the value of the values.

            ### Returns:
            1. List[Tuple[str, Any]]
                - A list of tuples containing the name and the value of the values.
                - The return value is formatted in a way, that it can be used to directly update the kwargs of an event.
            """

            if len(self._selectors) > 0 and (self._selectors[0].get_value() is None or self._selectors[0].get_value() == None):
                self.roll_values()

            kwargs = {}

            for selector in self._selectors:
                key = selector.get_name()
                value = selector.get_value(**kwargs)
                kwargs[key] = value

            return kwargs
            
    class Selector(ABC):
        """
        A base class that represents a set of values that that will be carried into the corresponding event.
        The class is abstract and should be inherited from.

        ### Attributes:
        1. _key: str
            - The key of the value.
            - The key is used to identify the value in the events kwargs.
        2. _value: Any
            - The value of the Selector.
            - This attribute gets filled internally by calling the update() method. 
        3. _realtime: bool
            - A boolean that determines whether the value should be updated on retrieving the value or not.
            - If True, the value will be updated on retrieval.
            - If False, the value will only be updated, when the update()-method is triggered.
        """

        def __init__(self, realtime: bool, key: str):
            self._key = key
            self._value = None
            self._realtime = realtime

        def update(self, **kwargs):
            """
            Updates the value of the Selector.
            """

            self._value = self.roll(**kwargs)

        @abstractmethod
        def roll(self, **kwargs) -> Any:
            pass

        def get_name(self):
            """
            Returns the name of the value.

            ### Returns:
            1. str
                - The key of the Selector.
            """

            return self._key

        def get_value(self, **kwargs):
            """
            Reads the value of the Selector and returns it.
            If realtime is set to True, the value will be updated before returning it.
            """

            if self._realtime or self._value == None:
                self.update(**kwargs)

            return self._value
        
        def get_key_value(self):
            """
            Returns a tuple of the key and the value.
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
        3. realtime: bool (default: False)
            - A boolean that determines whether the value should be updated on retrieving the value or not.
            - If True, the value will be updated on retrieval.
            - If False, the value will only be updated, when the update()-method is triggered.
        """

        def __init__(self, key: str, *values: Any, realtime: bool = False):
            super().__init__(realtime, key)
            self._list = values

        def roll(self, **kwargs) -> Any:
            """
            Returns a random value from the list.
            """

            value = get_random_choice(*self._list, **kwargs)
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

        def __init__(self, key: str, min_value: int, max_value: int, realtime: bool = False):
            super().__init__(realtime, key)
            self._min_value = min_value
            self._max_value = max_value

        def roll(self, **kwargs) -> Any:
            """
            Returns a random value from in between the minimum and maximum value.
            """

            value = get_random_int(self._min_value, self._max_value)
            return value

    class ConditionSelector(Selector):
        """
        A Selector-class that chooses a value based on a condition.
        ConditionSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _condition: Condition
            - The condition that determines which value will be chosen.
        2. _true_value: Any
            - The value that will be chosen if the condition is fulfilled.
        3. _false_value: Any
            - The value that will be chosen if the condition is not fulfilled.

        ### Methods:
        1. roll() -> Any
            - Returns a value based on the condition.
            - if the condition is fulfilled, the true_value will be returned.
            - if the condition is not fulfilled, the false_value will be returned.

        ### Parameters:
        1. key: str
            - The key of the value.
            - The key is used to identify the value in the events kwargs.
        2. condition: Condition
            - The condition that determines which value will be chosen.
        3. true_value: Any
            - The value that will be chosen if the condition is fulfilled.
        4. false_value: Any
            - The value that will be chosen if the condition is not fulfilled.
        5. realtime: bool (default: False)
            - A boolean that determines whether the value should be updated on retrieving the value or not.
            - If True, the value will be updated on retrieval.
            - If False, the value will only be updated, when the update()-method is triggered.
        """

        def __init__(self, key: str, condition: Condition, true_value: Any, false_value: Any, realtime: bool = False):
            super().__init__(realtime, key)
            self._condition = condition
            self._true_value = true_value
            self._false_value = false_value

        def roll(self, **kwargs) -> Any:
            """
            Returns a value based on the condition.
            If the value is a Selector, the Selector will recursively roll its value and then return the resulting value
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
        1. _stat: str
            - The name of the stat.
        2. _char: str
            - The key of the character.
            - The character is used to identify the character in the character dictionary.
            - See method get_character_by_key() in the character module for more information.

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

        def __init__(self, key: str, stat: str, char: str, realtime: bool = True):
            super().__init__(realtime, key)
            self._stat = stat
            self._char = char

        def roll(self, **kwargs) -> Any:
            """
            Returns the value of the stat.
            """

            return get_character_by_key(self._char).get_stat_number(self._stat)

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

        def __init__(self, key: str, time_type: str):
            super().__init__(True, key)
            self._time_type = time_type

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

            if time_type == "day":
                return time.get_day()
            elif time_type == "month":
                return time.get_month()
            elif time_type == "year":
                return time.get_year()
            elif time_type == "daytime":
                return time.get_daytime()
            elif time_type == "weekday":
                return time.get_weekday()
            else:
                return time.day_to_string()

    class ValueSelector(Selector):
        """
        A Selector-class that sets a value on initialisation for insertion into the event
        ValueSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _value: Any
            -The value to be inserted.

        ### Methods:
        1. roll() -> Any
            - Returns the value.

        ### Parameters:
        1. key: str
            -The key of the value.
        2. value: Any
            -The value of the value.
        """
        
        def __init__(self, key: str, value: Any):
            super.__init__(True, key)
            self._value = value

        def roll(self, **kwargs) -> Any:
            """
            Returns the value.
            """

            return self._value

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

        def __init__(self, key: str, index: str, dict: Dict):
            super().__init__(True, key)
            self._index = index
            self._dict = dict

        def roll(self, **kwargs) -> Any:
            """
            Returns the value from the dict.
            """

            if self._index not in kwargs or kwargs[self._index] not in self._dict:
                return None

            return self._dict[kwargs[self._index]]

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

        def __init__(self, key: str, index: str):
            super().__init__(True, key)
            self._index = index

        def roll(self, **kwargs) -> Any:
            """
            Returns the value from the GameData Storage.
            """

            return get_game_data(self._index)

    class ProgressSelector(Selector):
        """
        A Selector-class that chooses a value from the Event Progress Database.
        ProgressSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _index: str
            - The key for the Event Progress Database from where the the value is determined.
            - This parameter takes the value in get_progress(_index) and uses it as the value for the Selector.

        ### Methods:
        1. roll() -> Any
            - Returns the value from the Event Progress Database.

        ### Parameters:
        1. key: str
            - The key of the value.
            - The key is used to identify the value in the events kwargs.
        2. index: str
            - The key for the Event Progress Database from where the the value is determined.
            - This parameter takes the value in get_progress(_index) and uses it as the value for the Selector.
        """

        def __init__(self, key: str, index: str):
            super().__init__(True, key)
            self._index = index

        def roll(self, **kwargs) -> Any:
            """
            Returns the progress of the Event Progress Database.
            """

            return get_progress(self._index)

    class RuleUnlockedSelector(Selector):
        """
        A Selector-class that stores if the rule is unlocked
        RuleUnlockedSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _rule: Rule
            - The rule that is checked for being unlocked.

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

        def __init__(self, key: str, rule: str):
            super().__init__(True, key)
            self._rule = get_rule(rule)

        def roll(self, **kwargs) -> Any:
            return self._rule.is_unlocked()

    class ClubUnlockedSelector(Selector):
        """
        A Selector-class that stores if the club is unlocked
        ClubUnlockedSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _club: Club
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

        def __init__(self, key: str, club: str):
            super().__init__(True, key)
            self._club = get_club(club)

        def roll(self, **kwargs) -> Any:
            return self._club.is_unlocked()

    class BuildingUnlockedSelector(Selector):
        """
        A Selector-class that stores if the building is unlocked
        BuildingUnlockedSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _building: Building
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

        def __init__(self, key: str, building: str):
            super().__init__(True, key)
            self._building = get_building(building)

        def roll(self, **kwargs) -> Any:
            return self._building.is_unlocked()

    class BuildingLevelSelector(Selector):
        """
        A Selector-class that stores the level of the building
        BuildingLevelSelector is a child of Selector and inherits all of its attributes and methods.

        ### Attributes:
        1. _building: Building
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

        def __init__(self, key: str, building: str):
            super().__init__(True, key)
            self._building = get_building(building)

        def roll(self, **kwargs) -> Any:
            return self._building.get_level()
