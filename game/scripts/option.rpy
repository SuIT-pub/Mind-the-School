init -6 python:
    import re
    from abc import ABC, abstractmethod
    from typing import Union, List

    class Option(ABC):
        def __init__(self, name: str):
            self.name = name

        def __repr__(self):
            return self.name

        def __str__(self):
            return self.name

        def __eq__(self, other):
            return self.name == name or (hasattr(other, "name") and self.name == other.name)

        def get_name(self) -> str:
            return self.name

        def check_option(self, **kwargs):
            return True

        def get_values(self) -> Dict[str, Any]:
            return {}

    class OptionSet:
        def __init__(self, *options_list: Option):
            self.options = {option_obj.get_name(): option_obj for option_obj in options_list if isinstance(option_obj, Option)}

        def check_options(self, **kwargs) -> bool:
            if len(self.options) == 0:
                return True
            return all(option.check_option(**kwargs) for option in self.options.values())

        def add_option(self, option: Option):
            self.options[option.get_name()] = option

        def get_options(self) -> List[Option]:
            return list(self.options.values())

        def get_option(self, name: str) -> Union[Option, None]:
            return self.options.get(name, None)

        def has_option(self, name: str) -> bool:
            return name in self.options.keys()

        def has_option_subclass(self, subclass: Type[Option]) -> bool:
            return any(isinstance(option, subclass) for option in self.options.values())

    empty_option_set = OptionSet()

    class NoHighlightOption(Option):
        def __init__(self):
            super().__init__("NoHighlight")

        def check_option(self, **kwargs):
            if "Highlight" in kwargs:
                return not kwargs["Highlight"]
            if "NoHighlight" in kwargs:
                return kwargs["NoHighlight"]
            return True

    class ForceHighlightOption(Option):
        def __init__(self):
            super().__init__("ForceHighlight")
        
    class ShowBlockedOption(Option):
        def __init__(self):
            super().__init__("ShowBlocked")

        def check_option(self, **kwargs):
            if "ShowBlocked" in kwargs:
                return kwargs["ShowBlocked"]
            return True

    class PriorityOption(Option):
        def __init__(self, priority: int):
            super().__init__("Priority")
            self.priority = priority

        def check_option(self, **kwargs):
            if "Priority" in kwargs:
                return kwargs["Priority"] == self.priority
            return True

    class FragmentRepeatOption(Option):
        def __init__(self, number: int, repeatable: bool):
            super().__init__("FragmentRepeat")
            self.number = number
            self.repeatable = repeatable

        def get_values(self) -> Dict[str, Any]:
            if (isinstance(self.number, Selector)):
                return {
                    "number": self.number.roll(),
                    "repeatable": self.repeatable
                }

            return {
                "number": self.number,
                "repeatable": self.repeatable
            }

    class FragmentRerollOption(Option):
        def __init__(self):
            super().__init__("FragmentReroll")

    class OptionalOption(Option):
        def __init__(self):
            super().__init__("Optional")

    class ReplayCategoryOption(Option):
        def __init__(self, category: str):
            super().__init__("ReplayCategory")
            self.category = category

    class EventSeenDebuffOption(Option):
        def __init__(self, debuff: float = 0.25):
            super().__init__("EventSeenDebuff")
            self.debuff = debuff

    class EffectNoRevertOption(Option):
        def __init__(self):
            super().__init__("EffectNoRevert")