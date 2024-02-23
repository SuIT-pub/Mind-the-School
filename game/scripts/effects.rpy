init -1 python:
    from abc import ABC,abstractmethod

    def call_effects(*effects: Effect, **kwargs):
        """
        Applies all effects passed as arguments.

        ### Parameters:
        1. *effects: Effect
            - Effects to be applied.
        """

        for effect in effects:
            effect.apply(**kwargs)

    class Effect(ABC):
        """
        Abstract class for all effects.

        ### Attributes:
        1. name: str
            - Name of the effect.

        ### Methods:
        1. apply(**kwargs)
            - Applies the effect.
        """

        def __init__(self, name: str):
            self.name = name

        @abstractmethod
        def __str__(self):
            pass

        @abstractmethod
        def apply(self, **kwargs):
            pass

    class RuleEffect(Effect):
        """
        Unlocks a rule.
        """

        def __init__(self, name: str, rule: str | Rule):
            super().__init__(name)
            self.rule = rule

        def __str__(self):
            return f"{self.rule}"

        def apply(self, **kwargs):
            if isinstance(self.rule, str):
                rule = get_rule(self.rule)
                if rule != None:
                    rule.unlock()
            else:
                self.rule.unlock()

    class ClubEffect(Effect):
        """
        Unlocks a club.
        """

        def __init__(self, name: str, club: str | Club):
            super().__init__(name)
            self.club = club

        def __str__(self):
            return f"{self.club}"

        def apply(self, **kwargs):
            if isinstance(self.club, str):
                club = get_club(self.club)
                if club != None:
                    club.unlock()
            else:
                self.club.unlock()

    class BuildingEffect(Effect):
        """
        Unlocks a building.
        """

        def __init__(self, name: str, building: str | Building):
            super().__init__(name)
            self.building = building

        def __str__(self):
            return f"{self.building}"

        def apply(self, **kwargs):
            if isinstance(self.building, str):
                building = get_building(self.building)
                if building != None:
                    building.unlock()
            else:
                self.building.unlock()

    class LevelEffect(Effect):
        """
        Changes the level of a character.

        ### Attributes:
        1. value: int
            - Value to be added to the level.
        2. mode: str (Default "ADD")
            - Mode of the effect. Can be "ADD" or "SET".
            - ADD adds the value to the current level.
            - SET sets the level to the value.
        """

        def __init__(self, name: str, value: int, mode: str = "ADD"):
            super().__init__(name)
            self.mode = mode
            self.value = value

        def __str__(self):
            return f"{self.value}"

        def apply(self, **kwargs):
            char_obj = get_kwargs("char_obj", **kwargs)
            if char_obj == None:
                return

            if self.mode == "SET":
                char_obj.set_level(self.value)
            if self.mode == "ADD":
                char_obj.set_level(char_obj.get_level() + self.value)

    class StatEffect(Effect):
        """
        Changes the value of a stat.

        ### Attributes:
        1. stat: str
            - Name of the stat.
        2. value: num
            - Value to be added to the stat.
        3. mode: str (Default "ADD")
            - Mode of the effect. Can be "ADD" or "SET".
            - ADD adds the value to the current stat.
            - SET sets the stat to the value.
        """

        def __init__(self, name: str, stat: str, value: num, mode: str = "ADD"):
            super().__init__(name)
            self.stat = stat
            self.mode = mode
            self.value = value

        def __str__(self):
            return f"{self.value}"

        def apply(self, **kwargs):
            char_obj = get_kwargs("char_obj", **kwargs)
            if char_obj == None:
                return

            stat_obj = char_obj.get_stat(self.stat)
            if stat_obj == None:
                return

            if self.mode == "SET":
                stat_obj.change_value_to(self.value, char_obj.get_level())
            if self.mode == "ADD":
                stat_obj.change_value(self.value, char_obj.get_level())

    class MoneyEffect(Effect):
        """
        Changes the value of money.

        ### Attributes:
        1. value: num
            - Value to be added to the money.
        2. mode: str (Default "ADD")
            - Mode of the effect. Can be "ADD" or "SET".
            - ADD adds the value to the current money.
            - SET sets the money to the value.
        """

        def __init__(self, name: str, value: num, mode: str = "ADD"):
            super().__init__(name)
            self.mode = mode
            self.value = value

        def __str__(self):
            return f"{self.value}"

        def apply(self, **kwargs):
            if self.mode == "SET":
                money.change_value_to(self.value)
            if self.mode == "ADD":
                money.change_value(self.value)

    class AddTempTimeEventEffect(Effect):
        """
        Adds a temporary time event.

        ### Attributes:
        1. event: Event
            - Event to be added.
        """

        def __init__(self, event: Event):
            super().__init__(event.get_name())
            self.event = event

        def __str__(self):
            return f"{self.event.get_name()}"

        def apply(self, **kwargs):
            add_temp_event(self.event)

    class RemoveTempTimeEventEffect(Effect):
        """
        Removes a temporary time event.

        ### Attributes:
        1. id: str
            - ID of the event to be removed.
        """

        def __init__(self, id: str):
            super().__init__(id)

        def __str__(self):
            return f"{self.id}"

        def apply(self, **kwargs):
            remove_temp_event(self.id)

    class BlockBuildingEffect(Effect):
        """
        Blocks a building.

        ### Attributes:
        1. building_name: str
            - Name of the building to be blocked.
        2. is_blocking: bool (Default True)
            - If True, the building will be blocked.
            - If False, the building will be unblocked.
        """

        def __init__(self, name: str, building_name: str, is_blocking: bool = True):
            super().__init__(name)
            self.building_name = building_name
            self.is_blocking = is_blocking

        def __str__(self):
            return f"{self.building_name}"

        def apply(self, **kwargs):
            set_building_blocked(self.building_name, self.is_blocking)

    class EventEffect(Effect):
        """
        Calls an event.

        ### Attributes:
        1. event: Event | EventStorage | str
            - Event to be called.
            - Event calls just the event.
            - EventStorage calls all available events.
            - str calls the label.
        """

        def __init__(self, event: Event):
            super().__init__(event.get_name())
            self.event = event

        def __str__(self):
            return f"{self.event.get_name()}"

        def apply(self, **kwargs):
            if isinstance(self.event, EventStorage):
                self.event.call_available_event(**kwargs)

            if isinstance(self.event, Event):
                self.event.call(**kwargs)
                # event_obj = self.event.get_event()
                # for event in event_obj:
                #     renpy.call(event, **kwargs)

            if isinstance(self.event, str):
                renpy.call(self.event, **kwargs)

    class ValueEffect(Effect):
        """
        Changes a value in the gameData.

        ### Attributes:
        1. key: str
            - Key of the value.
        2. value: val | bool
            - Value to be added to the key in gameData.
        """

        def __init__(self, key: str, value: val | bool):
            super().__init__(key)
            self.key = key
            self.value = value

        def __str__(self):
            return f"{self.value}"

        def apply(self, **kwargs):
            gameData[self.key] = self.value

    class ProgressEffect(Effect):
        """
        Changes a progress in the Event Series.

        ### Attributes:
        1. key: str
            - Key of the progress.
        2. value: int
            - The progress of the Event Series with the key
        """

        def __init__(self, key: str, value: int = 1):
            super().__init__(key)
            self.key = key
            self.value = value

        def __str__(self):
            return f"{self.value}"

        def apply(self, **kwargs):
            if self.key not in gameData.keys():
                gameData[self.key] = 0
            gameData[self.key] += self.value

    class ModifierEffect(Effect):
        """
        Adds a modifier to a stat.

        ### Attributes:
        1. key: str
            - Key of the modifier.
        2. stat: str
            - Name of the stat.
        3. mod_obj: Modifier_Obj
            - Modifier to be added.
        4. char_obj: Char (Default None)
            - Character to which the modifier will be added.
        5. collection: str (Default "default")
            - Collection of the modifier.
        """

        def __init__(self, key: str, stat: str, mod_obj: Modifier_Obj, char_obj: Char = None, collection: str = 'default'):
            super().__init__(key)
            self.key = key
            self.stat = stat
            self.modifier = mod_obj
            self.char_obj = char_obj
            self.collection = collection

        def __str__(self):
            return f"{self.key}"

        def apply(self, **kwargs):
            set_modifier(self.key, self.stat, self.modifier, char_obj = self.char_obj, collection = self.collection)