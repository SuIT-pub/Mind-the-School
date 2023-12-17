init python:

    from abc import ABC, abstractmethod
    import random
    from typing import Any

    class SelectorSet(ABC):
        def __init__(self, *selectors: Selector):
            self._selectors = selectors

        def roll_values(self, **kwargs):
            """
            Rolls the values of the event.
            """

            for selector in self._selectors:
                selector.update(**kwargs)
                key, value = selector.get_value()
                if key not in kwargs:
                    kwargs[key] = value

        def get_values(self) -> List[Tuple[str, Any]]:
            """
            Returns the values of the event.

            ### Returns:
            1. List[Tuple[str, Any]]
                - A list of tuples containing the name and the value of the values.
            """

            return {value.get_name(): value.get_value() for value in self.values}
            

    class Selector(ABC):
        """
        A class that represents a set of values that can be rolled.
        """

        def __init__(self, realtime: bool, key: str):
            self._key = key
            self._value = None
            self._realtime = realtime

        def update(self, **kwargs):
            """
            Updates the value of the key.
            """

            self._value = self.roll(**kwargs)

        @abstractmethod
        def roll(self, **kwargs) -> Any:
            pass

        def get_value(self):
            """
            Returns a tuple of the key and the value.
            """
            if self._realtime:
                self.update()

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
        A class that represents a set of values that can be rolled.
        """

        def __init__(self, key: str, *values: Any, realtime: bool = True):
            super().__init__(realtime, key)
            self._list = values

        def roll(self, **kwargs) -> Any:
            """
            Returns a random value from the list.
            """

            value = get_random_choice(*self._list)
            if isinstance(value, ValueSet):
                return value.roll(**kwargs)
            return value

    class RandomValueSelector(Selector):
        """
        A class that represents a set of values that can be rolled.
        """

        def __init__(self, key: str, min_value: int, max_value: int, realtime: bool = True):
            super().__init__(realtime, key)
            self._min_value = min_value
            self._max_value = max_value

        def roll(self, **kwargs) -> Any:
            """
            Returns a random value from the list.
            """

            value = get_random_int(self._min_value, self._max_value)
            return value

    class ConditionSelector(Selector):
        """
        A class that represents a set of values that can be rolled.
        """

        def __init__(self, key: str, condition: Condition, true_value: Any, false_value: Any, realtime: bool = True):
            super().__init__(realtime, key)
            self._condition = condition
            self._true_value = true_value
            self._false_value = false_value

        def roll(self, **kwargs) -> Any:
            """
            Returns a random value from the list.
            """

            value = self._true_value if self._condition.is_fulfilled(**kwargs) else self._false_value
            if isinstance(value, ValueSet):
                return value.roll(**kwargs)
            return value

    class StatSelector(Selector):
        """
        A class that represents a set of values that can be rolled.
        """

        def __init__(self, key: str, stat: Stat, realtime: bool = True):
            super().__init__(realtime, key)
            self._stat = stat

        def roll(self, **kwargs) -> Any:
            """
            Returns a random value from the list.
            """

            return self._stat.get_value()

    class ValueSelector(Selector):
        """
        A Selector class that sets a value on initialisation for insertion into the event

        ### Parameters:
        1.key: str
            -The key of the value.
        2.value: Any
            -The value of the value.
        """
        
        def __init__(self, key: str, value: Any):
            super.__init__(True, key)
            self._value = value

        def roll(self, **kwargs) -> Any:
            return self._value

    class KwargsSelector(Selector):
        """
        A Selector class that funnels the value from the inserted kwargs directly into the event.

        ### Parameters:
        1.key: str
            -The key of the value.
        """
        def __init__(self, key: str):
            super.__init__(True, key)

        def roll(self, **kwargs) -> Any:
            return kwargs[self._key]
