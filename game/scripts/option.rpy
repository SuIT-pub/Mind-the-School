init -6 python:
    import re
    from abc import ABC, abstractmethod
    from typing import Union, List

    class OptionSet:
        def __init__(self, *options: Option):
            self.options = {option.get_name(): option for option in set(options)}

        def check_options(self, **kwargs) -> bool:
            if len(self.options) == 0:
                return True
            return all(option.check_option(**kwargs) for option in self.options.values())

        def get_options(self) -> List[Option]:
            return list(self.options.values())

        def get_option(self, name: str) -> Union[Option, None]:
            return self.options.get(name, None)

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

        @abstractmethod
        def check_option(self, **kwargs) -> bool:
            pass
        

    class NoHighlightOption(Option):
        def __init__(self):
            super().__init__("NoHighlight")

        def check_option(self, **kwargs):
            if "highlight" in kwargs:
                return not kwargs["Highlight"]
            if "nohighlight" in kwargs:
                return kwargs["NoHighlight"]
            return True


