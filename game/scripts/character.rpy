init -6 python:
    from typing import Dict, Any
    import math
    class Char:
        def __init__(self, name, title):
            self.name = name
            self.title = title
            self.level = Stat("level", 0)
            self.stats_objects = {}
            
        def _update(self, data: Dict[str, Any] = None) -> None:
            if data != None:
                self.__dict__.update(data)

            if not hasattr(self, 'level'):
                self.level = Stat("level", 0)
            if not hasattr(self, 'stats_objects'):
                self.stats_objects = {}

        def get_name(self) -> str:
            return self.name

        def get_title(self) -> str:
            return self.title

        def check_stat_exists(self, stat: str) -> bool:
            return stat in self.stats_objects.keys()

        def get_stat_obj(self, stat: str) -> Stat:
            if stat not in self.stats_objects.keys():
                return None
            return self.stats_objects[stat]

        def set_stat(self, stat: str, value: num) -> None:
            stat_obj = self.get_stat_obj(stat)
            if stat_obj == None:
                return
            stat_obj.set_value(value, self.get_level())

        def change_stat(self, stat: str, delta: num) -> None:
            stat_obj = self.get_stat_obj(stat)
            if stat_obj == None:
                return
            stat_obj.change_value(delta, self.get_level())

        def get_stat_number(self, stat: str) -> num:
            stat_obj = self.get_stat_obj(stat)

            if stat_obj == None:
                return -1
            return stat_obj.get_value()

        def get_stat_string(self, stat: str) -> str:
            return str(self.get_stat_number(stat))

        def reset_changed_stats(self) -> None:
            self.level.reset_change()
            for stat_key in self.stats_objects.keys():
                stat_obj = self.get_stat_obj(stat_key)

                if stat_obj == None:
                    continue

                stat_obj.reset_change()

        def get_stats(self) -> Dict[str, Stat]:
            return self.stats_objects

        def check_stat(self, stat: str, value: num | str) -> bool:
            if value == "x":
                return True

            return get_value_diff(value, self.get_stat_number(stat)) >= 0

        def get_level(self) -> int:
            return self.level.get_value()

        def get_level_str(self) -> str:
            return str(self.get_level())

        def set_level(self, level: int) -> None:
            self.level.set_value(level)
            if self.level.get_value() < 0:
                self.level.set_value(0)
            elif self.level.get_value() > 10:
                self.level.set_value(10)

        def get_nearest_level_delta(self, level: int) -> int:
            for i in range(self.get_level(), 11):
                if self.check_level(level, i):
                    return self.get_level() - i

        def check_level(self, value: num | str, test_level: int = None) -> bool:
            if value == "x":
                return True

            if test_level == None:
                test_level = self.get_level()

            return get_value_diff(value, test_level) >= 0

        def display_stat(self, stat: str) -> str:
            stat_obj = self.get_stat_obj(stat)

            if stat_obj == None:
                return "NaN"

            return stat_obj.display_stat()

        def get_display_value(self, stat: str) -> str:
            stat_obj = self.get_stat_obj(stat)

            if stat_obj == None:
                return "NaN"

            return stat_obj.get_display_value()

        def get_display_change(self, stat: str) -> str:
            stat_obj = self.get_stat_obj(stat)

            if stat_obj == None:
                return "NaN"

            return stat_obj.get_display_change()
    
    def get_lowest_level(map: Dict[str, Char | Dict[str, Any]]) -> int:
        level = 100
        for school in map.values():
            if school.get_level() < level:
                level = school.get_level()

        return level

    def update_mean_stats() -> None:
        mean_school = get_character("school_mean_values", charList)
        for stat in mean_school.get_stats().keys():
            mean = 0
            count = 0

            for obj in charList["schools"].values():
                if obj.get_name() == "middle_school" and loli_content == 0:
                    continue
                if obj.get_name() == "elementary_school" and loli_content != 2:
                    continue
                
                mean += obj.get_stat_number(stat)
                count += 1

            if count == 0:
                mean_school.set_stat(stat, 0)
            else:
                mean_school.set_stat(stat, round(mean / count, 2))

        mean_level = 0
        count = 0
        for obj in charList["schools"].values():
            if obj.get_name() == "middle_school" and loli_content == 0:
                continue
            if obj.get_name() == "elementary_school" and loli_content != 2:
                continue

            mean_level += obj.get_level()
            count += 1

        mean_school.set_level(math.ceil(mean_level))

    def get_mean_stat(stat: str) -> num:
        if stat == MONEY:
            return money.get_value()
        elif stat == LEVEL:
            return get_level_for_char(stat, "school_mean_values", map)
        else:
            return get_stat_for_char(stat, "school_mean_values", map)

    def display_mean_stat(stat: str) -> str:
        if stat == MONEY:
            return money.display_stat()
        else:
            return get_character("school_mean_values", charList).display_stat(stat)

    def get_character(
        name: str, 
        map: Dict[str, Char | Dict[str, Any]]
    ) -> Char:
        if name not in map.keys():
            return None

        return map[name]

    def get_stat_for_char(
        stat: str, 
        char: str | Char = "", 
        map: Dict[str, Char | Dict[str, Any]] = None
    ) -> num:

        if stat == MONEY:
            return money.get_value()

        if isinstance('char', Char):
            return char.get_stat_number(stat)
        else:
            if map == None or char not in map.keys():
                return -1
            return map[char].get_stat_number(stat)

    def get_level_for_char(
        char: str | Char, 
        map: Dict[str, Char | Dict[str, Any]] = None
    ) -> int:
        if isinstance(char, Char):
            return char.get_level()
        if map != None and char in map.keys():
            return map[char].get_level()
        return -1

    def set_stat_for_all(
        stat: str, 
        value: num, 
        map: Dict[str, Char | Dict[str, Any]]
    ) -> None:
        for character in map.keys():
            map[character].set_stat(stat, value)

    def set_stat_for_char(
        stat: str, 
        value: num, 
        char: str | Char, 
        map: Dict[str, Char | Dict[str, Any]] = None
    ) -> None:
        if isinstance(char, Char):
            char.set_stat(stat, value)
        elif map != None and char in map.keys():
            map[char].set_stat(stat, value)
        
    def set_level_for_char(
        value: int, 
        char: str | Char, 
        map: Dict[str, Char | Dict[str, Any]] = None
    ) -> None:
        if isinstance(char, Char):
            char.set_level(value)
        elif map != None and char in map.keys():
            map[char].set_level(value)
        
    # changes the stat value
    def change_stat(
        stat: str, 
        change: num, 
        name: str | Char = "", 
        map: Dict[str, Char | Dict[str, Any]] = None
    ) -> None:
        if stat == MONEY:
            money.change_value(change)
        else:
            change_stat_for_char(stat, change, name, map)

    def change_stat_for_all(
        stat: str, 
        delta: num, 
        map: Dict[str, Char | Dict[str, Any]]
    ) -> None:
        for character in map.keys():
            map[character].change_stat(stat, delta)

    def change_stat_for_char(
        stat: str, 
        value: num, 
        char: str | Char, 
        map: Dict[str, Char | Dict[str, Any]] = None
    ) -> None:
        if isinstance(char, Char):
            char.change_stat(stat, value)
        elif map != None and char in map.keys():
            map[char].change_stat(stat, value)

    def reset_stats(
        char: str | Char = "", 
        map: Dict[str, Char | Dict[str, Any]] = None
    ) -> None:
        money.reset_change()
        
        if isinstance(char, Char):
            char.reset_changed_stats()
        elif map != None and char in map.keys():
            map[char].reset_changed_stats()
        elif map != None:
            for keys in map.keys():
                map[keys].reset_changed_stats()

    def load_character(
        name: str, 
        title: str, 
        map: Dict[str, Char | Dict[str, Any]], 
        start_data: Dict[str, Any], 
        runtime_data: Dict[str, Any] = None
    ) -> None:
        if name not in map.keys():
            map[name] = Char(name, title)
            map[name].__dict__.update(start_data)

        map[name]._update(runtime_data)

    def update_character(
        char: str | Char, 
        data: Dict[str, Any], 
        map: Dict[str, Char | Dict[str, Any]] = None
    ) -> None:
        if isinstance(char, Char):
            char._update(data)
        elif map != None and char in map.keys():
            map[char]._update(data)

    def remove_character(
        name: str, 
        map: Dict[str, Char | Dict[str, Any]]
    ) -> None:
        if name in map.keys():
            del(map[name])

label load_schools ():

    $ load_character("secretary", "Secretary", charList['staff'], {
        'stats_objects': {
            "corruption": Stat(CORRUPTION, 35),
            "inhibition": Stat(INHIBITION, 50),
            "happiness": Stat(HAPPINESS, 57),
            "education": Stat(EDUCATION, 28),
            "charm": Stat(CHARM, 35),
            "reputation": Stat(REPUTATION, 79),
        }
    })

    $ load_character("parents", "Parents", charList, {
        'stats_objects': {
            "corruption": Stat(CORRUPTION, 0),
            "inhibition": Stat(INHIBITION, 100),
            "happiness": Stat(HAPPINESS, 15),
            "education": Stat(EDUCATION, 15),
            "charm": Stat(CHARM, 28),
            "reputation": Stat(REPUTATION, 38),
        }
    })

    $ load_character("teacher", "Teacher", charList['staff'], {
        'stats_objects': {
            "corruption": Stat(CORRUPTION, 0),
            "inhibition": Stat(INHIBITION, 100),
            "happiness": Stat(HAPPINESS, 13),
            "education": Stat(EDUCATION, 35),
            "charm": Stat(CHARM, 14),
            "reputation": Stat(REPUTATION, 17),
        }
    })
    $ load_character("high_school", "High School", charList['schools'], {
        'stats_objects': {
            "corruption": Stat(CORRUPTION, 0),
            "inhibition": Stat(INHIBITION, 100),
            "happiness": Stat(HAPPINESS, 12),
            "education": Stat(EDUCATION, 9),
            "charm": Stat(CHARM, 8),
            "reputation": Stat(REPUTATION, 7),
        }
    })

    $ load_character("middle_school", "Middle School", charList['schools'], {
        'stats_objects': {
            "corruption": Stat(CORRUPTION, 0),
            "inhibition": Stat(INHIBITION, 100),
            "happiness": Stat(HAPPINESS, 12),
            "education": Stat(EDUCATION, 9),
            "charm": Stat(CHARM, 8),
            "reputation": Stat(REPUTATION, 7),
        }
    })

    $ load_character("elementary_school", "Elementary School", charList['schools'], {
        'stats_objects': {
            "corruption": Stat(CORRUPTION, 0),
            "inhibition": Stat(INHIBITION, 100),
            "happiness": Stat(HAPPINESS, 12),
            "education": Stat(EDUCATION, 9),
            "charm": Stat(CHARM, 8),
            "reputation": Stat(REPUTATION, 7),
        }
    })

    $ load_character("school_mean_values", "Mean School", charList, {
        'stats_objects': {
            "corruption": Stat(CORRUPTION, 0),
            "inhibition": Stat(INHIBITION, 100),
            "happiness": Stat(HAPPINESS, 12),
            "education": Stat(EDUCATION, 9),
            "charm": Stat(CHARM, 8),
            "reputation": Stat(REPUTATION, 7),
        }
    })

    return