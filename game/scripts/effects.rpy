init -1 python:
    from abc import ABC,abstractmethod
    class Effect(ABC):
        def __init__(self, name):
            self.name = name

        @abstractmethod
        def apply(self, school):
            pass

    class RuleEffect(Effect):
        def __init__(self, name, rule):
            super().__init__(name)
            self.rule = rule

        def apply(self, school):
            rule = get_rule(self.rule)
            if rule != None:
                rule.unlock(school)

    class ClubEffect(Effect):
        def __init__(self, name, club):
            super().__init__(name)
            self.club = club

        def apply(self, school):
            club = get_club(self.club)
            if club != None:
                club.unlock(school)

    class BuildingEffect(Effect):
        def __init__(self, name, building):
            super().__init__(name)
            self.building = building

        def apply(self, _school):
            building = get_building(self.building)
            if building != None:
                building.unlock()

    class LevelEffect(Effect):
        def __init__(self, name, value, mode = "ADD"):
            super().__init__(name)
            self.mode = mode
            self.value = value

        def apply(self, school):
            if self.mode == "SET":
                school.set_level(self.value)
            if self.mode == "ADD":
                school.set_level(school.get_level() + self.value)

    class StatEffect(Effect):
        def __init__(self, name, stat, value, mode = "ADD"):
            super().__init__(name)
            self.stat = stat
            self.mode = mode
            self.value = value

        def apply(self, school):
            school_obj = get_school(school)
            if school_obj == None:
                return
            stat_obj = school_obj.get_stat(self.stat)
            if stat_obj == None:
                return

            if self.mode == "SET":
                stat_obj.change_value_to(self.value)
            if self.mode == "ADD":
                stat_obj.change_value(self.value)

    class MoneyEffect(Effect):
        def __init__(self, name, value, mode = "ADD"):
            super().__init__(name)
            self.mode = mode
            self.value = value

        def apply(self, school):
            if self.mode == "SET":
                money.change_value_to(self.value)
            if self.mode == "ADD":
                money.change_value(self.value)

    class AddTempTimeEventEffect(Effect):
        def __init__(self, name, event):
            super().__init__(name)
            self.event = event

        def apply(self, _school):
            add_temp_event(self.event)

    class RemoveTempTimeEventEffect(Effect):
        def __init__(self, name):
            super().__init__(name)

        def apply(self, _school):
            remove_temp_event(self.name)

    class BlockBuildingEffect(Effect):
        def __init(self, name, building_name, is_blocking = True):
            super().__init__(name)
            self.building_name = building_name
            self.is_blocking = is_blocking

        def apply(self, _school):
            set_building_blocked(self.building_name, self.is_blocking)
