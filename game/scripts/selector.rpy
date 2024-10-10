init -3 python:
    from abc import ABC, abstractmethod
    import random
    from typing import Any

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

        def roll_values(self, **kwargs):
            """
            Rerolls the values of each stored Selector and caches them in the corresponding Selector.
            """

            for selector in self._selectors:
                selector.update(**kwargs)
                if isinstance(selector, KwargsSelector):
                    values = selector.get_value(**kwargs)
                    for key in values.keys():
                        kwargs[key] = values[key]
                else:
                    key = selector.get_name()
                    value = selector.get_value(**kwargs)
                    kwargs[key] = value

        def get_values(self, **kwargs) -> List[Tuple[str, Any]]:
            """
            Returns a list of tuples containing the name and the value of the values.

            ### Returns:
            1. List[Tuple[str, Any]]
                - A list of tuples containing the name and the value of the values.
                - The return value is formatted in a way, that it can be used to directly update the kwargs of an event.
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
            - If the list contains a Selector and the Selector has been chosen, the Selector will be rolled and the resulting value will be used.
        3. realtime: bool (default: False)
            - A boolean that determines whether the value should be updated on retrieving the value or not.
            - If True, the value will be updated on retrieval.
            - If False, the value will only be updated, when the update()-method is triggered.
        """

        def __init__(self, key: str, *values: Any, realtime: bool = False, alt: Any = None):
            super().__init__(realtime, key)
            self._list = values 
            self._alt = alt

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
            - If the value is a Selector, the Selector will recursively roll its value and then return the resulting value
        4. false_value: Any
            - The value that will be chosen if the condition is not fulfilled.
            - If the value is a Selector, the Selector will recursively roll its value and then return the resulting value
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

        def __init__(self, key: str, stat: str | Selector, char: str | Selector, realtime: bool = True):
            super().__init__(realtime, key)
            self._stat = stat
            self._char = char

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

        def __init__(self, key: str, char: str | Selector):
            super().__init__(True, key)
            self._char = char

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

        def __init__(self, key: str, value: int | float | Selector, *, min_value: int | float | str | Selector = -1, max_value: int | float | str | Selector = -1):
            super().__init__(True, key)
            self._value = value
            self._min_value = min_value
            self._max_value = max_value

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
        
        def __init__(self, key: str, value: Any):
            super().__init__(True, key)
            self._value = value

        

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
        
        def __init__(self, key: str, kwargs_key: str | Selector):
            super().__init__(True, key)
            self._key = kwargs_key

        

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

        def __init__(self, key: str, index: str):
            super().__init__(True, key)
            self._index = index

        def roll(self, **kwargs) -> Any:
            """
            Returns the value from the GameData Storage.
            """

            return get_game_data(self._index)

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

        def __init__(self, **kwargs):
            super().__init__(True, "None")
            self._kwargs = kwargs

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

        def __init__(self, key: str, index: str | Selector):
            super().__init__(True, key)
            self._index = index

        def roll(self, **kwargs) -> Any:
            """
            Returns the progress of the Event Progress Database.
            """

            index = self._index if not isinstance(self._index, Selector) else self._index.get_value(**kwargs)

            return get_progress(index)

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

        def __init__(self, key: str, rule: str | Selector):
            super().__init__(True, key)
            self._rule = rule

        def roll(self, **kwargs) -> Any:

            rule = get_rule(self._rule) if not isinstance(self._rule, Selector) else get_rule(self._rule.get_value(**kwargs))
            if rule == None:
                return None           

            return rule.is_unlocked()

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

        def __init__(self, key: str, club: str | Selector):
            super().__init__(True, key)
            self._club = club

        def roll(self, **kwargs) -> Any:

            club = get_club(self._club) if not isinstance(self._club, Selector) else get_club(self._club.get_value(**kwargs))
            if club == None:
                return None
            return club.is_unlocked()

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

        def __init__(self, key: str, building: str):
            super().__init__(True, key)
            self._building = building

        def roll(self, **kwargs) -> Any:

            building = get_building(self._building) if not isinstance(self._building, Selector) else get_building(self._building.get_value(**kwargs))
            if building == None:
                return None
            return building.is_unlocked()

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

        def __init__(self, key: str, building: str | Selector):
            super().__init__(True, key)
            self._building = building

        def roll(self, **kwargs) -> Any:

            building = get_building(self._building) if not isinstance(self._building, Selector) else get_building(self._building.get_value(**kwargs))
            if building == None:
                return 0
            return building.get_level()

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

        def __init__(self, key: str, char: str | Selector = 'school'):
            super().__init__(True, key)
            self._char = char

        def roll(self, **kwargs) -> Any:

            char = self._char if not isinstance(self._char, Selector) else self._char.get_value(**kwargs)

            return get_character_by_key(char)

    class PTAVoteSelector(Selector):
        def __init__(self, key: str, char: str):
            super().__init__(True, key)
            self._char = char

        def roll(self, **kwargs) -> Any:
            vote_proposal = get_game_data('voteProposal')
            if vote_proposal == None:
                return None

            vote_obj = proposal._journal_obj

            return voteCharacter(vote_obj.get_condition_storage(), get_character_by_key(self._char))

    class PTAObjectSelector(Selector):
        def __init__(self, key: str):
            super().__init__(True, key)

        def roll(self, **kwargs) -> Any:
            return get_game_data('voteProposal')
