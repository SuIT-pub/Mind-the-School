init -1 python:
    from abc import ABC,abstractmethod

    def call_effects(*effects: Effect, **kwargs):
        for effect in effects:
            effect.apply(**kwargs)

    class Effect(ABC):
        def __init__(self, name: str):
            self.name = name

        @abstractmethod
        def apply(self, **kwargs):
            pass

    class RuleEffect(Effect):
        def __init__(self, name: str, rule: str | Rule):
            super().__init__(name)
            self.rule = rule

        def apply(self, **kwargs):
            char_obj = get_kwargs("char_obj", "x", **kwargs)

            if isinstance(self.rule, str):
                rule = get_rule(self.rule)
                if rule != None:
                    rule.unlock(char_obj.get_name())
            else:
                self.rule.unlock(char_obj.get_name())

    class ClubEffect(Effect):
        def __init__(self, name: str, club: str | Club):
            super().__init__(name)
            self.club = club

        def apply(self, **kwargs):            
            char_obj = get_kwargs("char_obj", "x", **kwargs)

            if isinstance(self.club, str):
                club = get_club(self.club)
                if club != None:
                    club.unlock(char_obj.get_name())
            else:
                self.club.unlock(char_obj.get_name())

    class BuildingEffect(Effect):
        def __init__(self, name: str, building: str | Building):
            super().__init__(name)
            self.building = building

        def apply(self, **kwargs):
            if isinstance(self.building, str):
                building = get_building(self.building)
                if building != None:
                    building.unlock()
            else:
                self.building.unlock()

    class LevelEffect(Effect):
        def __init__(self, name: str, value: int, mode: str = "ADD"):
            super().__init__(name)
            self.mode = mode
            self.value = value

        def apply(self, **kwargs):
            char_obj = get_kwargs("char_obj", **kwargs)
            if char_obj == None:
                return

            if self.mode == "SET":
                char_obj.set_level(self.value)
            if self.mode == "ADD":
                char_obj.set_level(char_obj.get_level() + self.value)

    class StatEffect(Effect):
        def __init__(self, name: str, stat: str, value: num, mode: str = "ADD"):
            super().__init__(name)
            self.stat = stat
            self.mode = mode
            self.value = value

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
        def __init__(self, name: str, value: num, mode: str = "ADD"):
            super().__init__(name)
            self.mode = mode
            self.value = value

        def apply(self, **kwargs):
            if self.mode == "SET":
                money.change_value_to(self.value)
            if self.mode == "ADD":
                money.change_value(self.value)

    class AddTempTimeEventEffect(Effect):
        def __init__(self, event: Event):
            super().__init__(event.get_title())
            self.event = event

        def apply(self, **kwargs):
            add_temp_event(self.event)

    class RemoveTempTimeEventEffect(Effect):
        def __init__(self, id: str):
            super().__init__(id)

        def apply(self, **kwargs):
            remove_temp_event(self.id)

    class BlockBuildingEffect(Effect):
        def __init__(self, name: str, building_name: str, is_blocking: bool = True):
            super().__init__(name)
            self.building_name = building_name
            self.is_blocking = is_blocking

        def apply(self, **kwargs):
            set_building_blocked(self.building_name, self.is_blocking)

    class EventEffect(Effect):
        def __init__(self, event: Event):
            super().__init__(event.get_title())
            self.event = event

        def apply(self, **kwargs):
            if isinstance(self.event, EventStorage):
                self.event.call_available_event(**kwargs)

            if isinstance(self.event, Event):
                event_obj = self.event.get_event()
                for event in event_obj:
                    renpy.call(event, **kwargs)

            if isinstance(self.event, str):
                renpy.call(self.event, **kwargs)

    class ValueEffect(Effect):
        def __init__(self, key: str, value: val | bool):
            super().__init__(key)
            self.key = key
            self.value = value

        def apply(self, **kwargs):
            gameData[self.key] = self.value

    class ProgressEffect(Effect):
        def __init__(self, key: str, value: int = 1):
            super().__init__(key)
            self.key = key
            self.value = value

        def apply(self, **kwargs):
            if self.key not in gameData.keys():
                gameData[self.key] = 0
            gameData[self.key] += self.value