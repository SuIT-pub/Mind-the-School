init -6 python:
    from typing import Dict, Any
    import math
    class Char:
        """
        A character object that contains all the stats and information about a character

        ### Attributes:
        1. name: str
            - The name of the character
            - The name refers to the id representing the character. The actual name of the character is in title
        2. title: str
            - The title of the character
            - The title is the actual name of the character
        3. level: Stat
            - The level of the character
            - The level is a stat object that contains the level of the character
        4. stats_objects: Dict[str, Stat]
            - A dictionary of all the stats of the character
            - The key is the name of the stat and the value is the stat object

        ### Methods:
        1. _update(data: Dict[str, Any] = None) -> None
            - Is used to supplement new attributes added in a new version for an older game save
        2. get_name() -> str
            - Returns the name of the character
        3. get_title() -> str
            - Returns the title of the character
        4. check_stat_exists(stat: str) -> bool
            - Checks if the stat exists in the character
        5. get_stat_obj(stat: str) -> Stat
            - Returns the stat object of the stat
        6. set_stat(stat: str, value: num) -> None
            - Sets the value of the stat
        7. change_stat(stat: str, delta: num) -> None
            - Changes the value of the stat by delta
        8. get_stat_number(stat: str) -> num
            - Returns the value of the stat
        9. get_stat_string(stat: str) -> str
            - Returns the value of the stat as a string
        10. reset_changed_stats() -> None
            - Resets the change of all the stats
        11. get_stats() -> Dict[str, Stat]
            - Returns the dictionary of all the stats
        12. check_stat(stat: str, value: num | str) -> bool
            - Checks if the stat equals the value
        13. display_stat(stat: str) -> str
            - Returns the stat as a string with the change
        14. get_display_value(stat: str) -> str
            - Returns the value of the stat as a string
        15. get_display_change(stat: str) -> str
            - Returns the change of the stat as a string
        16. get_level() -> int
            - Returns the level of the character
        17. get_level_str() -> str
            - Returns the level of the character as a string
        18. get_level_obj() -> Stat
            - Returns the level object of the character
        19. set_level(level: int) -> None
            - Sets the level of the character
        20. get_nearest_level_delta(level: int) -> int
            - Returns the difference between level and the level of the current character
        21. check_level(value: num | str, test_level: int = None) -> bool
            - Checks if the level equals the value

        ### Parameters:
        1. name: str
            - The name of the character
        2. title: str
            - The title of the character
        """

        def __init__(self, name, title):
            """
            The constructor for the character object

            ### Parameters:
                1. name: str
                    - The name of the character
                2. title: str
                    - The title of the character
            """

            self.name = name
            self.title = title
            self.level = Stat("level", 0)
            self.stats_objects = {}
            
        def _update(self, data: Dict[str, Any] = None):
            """
            Is used to supplement new attributes added in a new version for an older game save

            ### Parameters:
                1. data: Dict[str, Any] (default None)
                    - The data to update the character with
            """

            if data != None:
                self.__dict__.update(data)

            if not hasattr(self, 'level'):
                self.level = Stat("level", 0)
            if not hasattr(self, 'stats_objects'):
                self.stats_objects = {}

        def check_stat_exists(self, stat: str) -> bool:
            """
            Checks if the stat exists in the character

            ### Parameters:
            1. stat: str
                - The name of the stat to check

            ### Returns:
            1. bool
                - True if the stat exists
                - False if the stat does not exist
            """

            return stat in self.stats_objects.keys()

        ##################
        # Attribute getter

        def get_name(self) -> str:
            """
            Returns the name of the character

            ### Returns:
            1. str
                - The name of the character
                - The name refers to the id representing the character. The actual name of the character is in title
            """

            return self.name

        def get_title(self) -> str:
            """
            Returns the title of the character

            ### Returns:
            1. str
                - The title of the character
                - The title is the actual name of the character
            """

            return self.title

        def get_stat_obj(self, stat: str) -> Stat:
            """
            Returns the stat object of the stat

            ### Parameters:
            1. stat: str
                - The name of the stat to get

            ### Returns:
            1. Stat
                - The stat object of the stat
                - None if the stat does not exist
            """

            if stat not in self.stats_objects.keys():
                return None
            return self.stats_objects[stat]

        ##############
        # Stat handler

        def set_stat(self, stat: str, value: num):
            """
            Sets the value of the stat

            ### Parameters:
            1. stat: str
                - The name of the stat to set
            2. value: num
                - The value to set the stat to
            """

            if is_in_replay:
                return

            stat_obj = self.get_stat_obj(stat)
            if stat_obj == None:
                return
            stat_obj.set_value(value, self.get_level())

        def change_stat(self, stat: str, delta: num):
            """
            Changes the value of the stat by delta

            ### Parameters:
            1. stat: str
                - The name of the stat to change
            2. delta: num
                - The value to change the stat by
            """

            if is_in_replay:
                return

            stat_obj = self.get_stat_obj(stat)
            if stat_obj == None:
                return
            stat_obj.change_value(delta, self.get_level())

        def get_stat_number(self, stat: str) -> num:
            """
            Returns the value of the stat

            ### Parameters:
            1. stat: str
                - The name of the stat to get

            ### Returns:
            1. num
                - The value of the stat
                - -1 if the stat does not exist
            """

            stat_obj = self.get_stat_obj(stat)

            if stat_obj == None:
                return -1
            return stat_obj.get_value()

        def get_stat_string(self, stat: str) -> str:
            """
            Returns the value of the stat as a string

            ### Parameters:
            1. stat: str
                - The name of the stat to get

            ### Returns:
            1. str
                - The value of the stat as a string
                - "-1" if the stat does not exist
            """

            return str(self.get_stat_number(stat))

        def reset_changed_stats(self):
            """
            Resets the change of all the stats
            """

            if is_in_replay:
                return

            self.level.reset_change()
            for stat_key in self.stats_objects.keys():
                stat_obj = self.get_stat_obj(stat_key)

                if stat_obj == None:
                    continue

                stat_obj.reset_change()

        def get_stats(self) -> Dict[str, Stat]:
            """
            Returns the dictionary of all the stats

            ### Returns:
            1. Dict[str, Stat]
                - The dictionary of all the stats
            """

            return self.stats_objects

        def check_stat(self, stat: str, value: num | str) -> bool:
            """
            Checks if the stat equals the value

            ### Parameters:
            1. stat: str
                - The name of the stat to check
            2. value: num | str
                - The value to check the stat against
                - value can be a number or a special string representing a set of values

            ### Returns:
            1. bool
                - True if the stat equals the value
                - False if the stat does not equal the value
            """

            if value == "x":
                return True

            return get_value_diff(value, self.get_stat_number(stat)) >= 0

        def display_stat(self, stat: str) -> str:
            """
            Returns the stat as a string with the change

            ### Parameters:
            1. stat: str
                - The name of the stat to get

            ### Returns:
            1. str
                - The stat as a string with the change
                - "NaN" if the stat does not exist
            """

            stat_obj = self.get_stat_obj(stat)

            if stat_obj == None:
                return "NaN"

            return stat_obj.display_stat()

        def get_display_value(self, stat: str) -> str:
            """
            Returns the value of the stat as a string

            ### Parameters:
            1. stat: str
                - The name of the stat to get

            ### Returns:
            1. str
                - The value of the stat as a string
                - "NaN" if the stat does not exist
            """

            stat_obj = self.get_stat_obj(stat)

            if stat_obj == None:
                return "NaN"

            return stat_obj.get_display_value()

        def get_display_change(self, stat: str) -> str:
            """
            Returns the change of the stat as a string

            ### Parameters:
            1. stat: str
                - The name of the stat to get

            ### Returns:
            1. str
                - The change of the stat as a string
                - "NaN" if the stat does not exist
            """

            stat_obj = self.get_stat_obj(stat)

            if stat_obj == None:
                return "NaN"

            return stat_obj.get_display_change()
    
        ###############
        # Level handler

        def get_level(self) -> int:
            """
            Returns the level of the character

            ### Returns:
            1. int
                - The level of the character
            """

            return self.level.get_value()

        def get_level_str(self) -> str:
            """
            Returns the level of the character as a string

            ### Returns:
            1. str
                - The level of the character as a string
            """

            return str(self.get_level())

        def get_level_obj(self) -> Stat:
            """
            Returns the level object of the character

            ### Returns:
            1. Stat
                - The level object of the character
            """

            return self.level

        def set_level(self, level: int):
            """
            Sets the level of the character

            ### Parameters:
            1. level: int
                - The level to set the character to
            """

            if is_in_replay:
                return

            level = clamp_value(level, 0, 10)
            self.level.set_value(level)

        def get_nearest_level_delta(self, level: int) -> int:
            """
            Returns the difference between level and the level of the current character

            ### Parameters:
            1. level: int
                - The level to check against

            ### Returns:
            1. int
                - The difference between level and the level of the current character
            """

            for i in range(self.get_level(), 11):
                if self.check_level(level, i):
                    return self.get_level() - i

        def check_level(self, value: num | str, test_level: int = None) -> bool:
            """
            Checks if the level equals the value

            ### Parameters:
            1. value: num | str
                - The value to check the level against
                - value can be a number or a special string representing a set of values
            2. test_level: int (default None)
                - The level to check against
                - If None, the level of the character is used

            ### Returns:
            1. bool
                - True if the level equals the value
                - False if the level does not equal the value
            """

            if value == "x":
                return True

            if test_level == None:
                test_level = self.get_level()

            return get_value_diff(value, test_level) >= 0
    #################

    #####################
    # School Char Handler

    def get_school() -> Char:
        """
        Gets a random school

        ### Returns:
        1. Char
            - The random school
        """
        
        if 'school' not in charList.keys():
            fix_schools()

        return charList['school']

    def get_school_stat(stat: str) -> num:
        """
        Gets the mean value of a stat from the mean school character

        ### Parameters:
        1. stat: str
            - The stat name for which the mean value is searched

        ### Returns:
        1. num
            - The mean value of the stat for all schools
        """

        if stat == MONEY:
            return money.get_value()
        elif stat == LEVEL:
            return get_level_for_char(stat, get_school())
        else:
            return get_stat_for_char(stat, get_school())

    def display_school_stat(stat: str) -> str:
        """
        Returns the mean value for a stat from all schools as string with the change

        ### Parameters:
        1. stat: str
            - The name of the stat whose mean value with the change from all schools will be returned

        ### Returns:
        1. str
            - The mean value of the stat from all schools as string with the change
        """

        if stat == MONEY:
            return money.display_stat()
        else:
            return get_school().display_stat(stat)

    def get_school_stat_value(stat: str) -> str:
        """
        Returns the mean value for a stat from all schools as string

        ### Parameters:
        1. stat: str
            - The name of the stat whose mean value from all schools will be returned

        ### Returns:
        1. str
            - The mean value of the stat from all schools as string
        """

        if stat == MONEY:
            return re.sub("\..+", "", money.get_display_value())
        else:
            return get_school().get_display_value(stat)

    def get_school_stat_change(stat: str) -> str:
        """
        Returns the mean change for a stat from all schools as string

        ### Parameters:
        1. stat: str
            - The name of the stat whose mean change from all schools will be returned

        ### Returns:
        1. str
            - The mean change of the stat from all schools as string
        """

        if stat == MONEY:
            return money.get_display_change()
        else:
            return get_school().get_display_change(stat)

    ######################
    # General Char Handler

    def get_character(name: str, map: Dict[str, Char | Dict[str, Any]]) -> Char:
        """
        Returns the character object from the map

        ### Parameters:
        1. name: str
            - The name of the character to get
        2. map: Dict[str, Char | Dict[str, Any]]
            - The map of characters to get the character from

        ### Returns:
        1. Char
            - The character object from the map
            - None if the character does not exist
        """

        if name not in map.keys():
            return None

        return map[name]

    def get_character_by_key(key: str) -> Char:
        """
        Returns the character object from the map

        ### Parameters:
        1. key: str
            - The key of the character to get
            - school, parent, teacher, secretary

        ### Returns:
        1. Char
            - The character object from the map
            - None if the character does not exist
            - possible keys: school, parent, teacher, secretary
        """

        if key == "school":
            return get_school()
        elif key == "parent":
            return get_character("parent", charList)
        elif key == "teacher":
            return get_character("teacher", charList['staff'])
        elif key == "secretary":
            return get_character("secretary", charList['staff'])
        return None

    ###################
    # Char Stat Handler

    def get_stat_obj_for_char(stat: str, char: str | Char, map: Dict[str, Char | Dict[str, Any]] = None) -> Stat:
        """
        Returns the stat object for the character

        ### Parameters:
        1. stat: str
            - The name of the stat to get
        2. char: str | Char
            - The name of the character or the character itself to get the stat from
            - If there is no character in map with the name, -1 is returned
        3. map: Dict[str, Char | Dict[str, Any]] (default None)
            - The map of characters to get the character from
            - If None and the name of the character is used instead of the Character-Object itself, -1 is returned

        ### Returns:
        1. Stat
            - The stat object for the character
            - None if the stat does not exist
        """

        if isinstance(char, Char):
            return char.get_stat_obj(stat)
        elif map != None and char in map.keys():
            return map[char].get_stat_obj(stat)
        return None

    def get_stat_for_char(stat: str, char: str | Char = "", map: Dict[str, Char | Dict[str, Any]] = None) -> num:
        """
        Returns the stat value for the character

        ### Parameters:
        1. stat: str
            - The name of the stat to get
        2. char: str | Char (default "")
            - The name of the character to get the stat from
            - If "" or there is no character in map with the name, -1 is returned
        3. map: Dict[str, Char | Dict[str, Any]] (default None)
            - The map of characters to get the character from
            - If None, the name of the character is used instead of the Character-Object itself, -1 is returned

        ### Returns:
        1. num
            - The value of the stat
            - -1 if the stat does not exist
        """

        if stat == MONEY:
            return money.get_value()

        if isinstance(char, Char):
            return char.get_stat_number(stat)
        elif map != None and char in map.keys():
            return map[char].get_stat_number(stat)
        return -1

    def set_stat_for_all(stat: str, value: num, map: Dict[str, Char | Dict[str, Any]]):
        """
        Sets the stat value for all characters in the map

        ### Parameters:
        1. stat: str
            - The name of the stat to set
        2. value: num
            - The value to set the stat to
        3. map: Dict[str, Char | Dict[str, Any]]
            - The map of characters to set the stat for
        """

        for character in map.keys():
            map[character].set_stat(stat, value)

    def set_stat_for_char(stat: str, value: num, char: str | Char, map: Dict[str, Char | Dict[str, Any]] = None):
        """
        Sets the stat value for a character

        ### Parameters:
        1. stat: str
            - The name of the stat to set
        2. value: num
            - The value to set the stat to
        3. char: str | Char
            - The name of the character or the character itself to set the stat for
            - If there is no character in map with the name, -1 is returned
        4. map: Dict[str, Char | Dict[str, Any]] (default None)
            - The map of characters to get the character from
            - If None and the name of the character is used instead of the Character-Object itself, -1 is returned
        """

        if isinstance(char, Char):
            char.set_stat(stat, value)
        elif map != None and char in map.keys():
            map[char].set_stat(stat, value)

    def change_stat(stat: str, change: num, name: str | Char = "", map: Dict[str, Char | Dict[str, Any]] = None):
        """
        Changes the stat value for a character or the money value if the stat is MONEY

        ### Parameters:
        1. stat: str
            - The name of the stat to change
        2. change: num
            - The value to change the stat by
        3. name: str | Char (default "")
            - The name of the character or the character itself to change the stat for
            - If there is no character in map with the name, -1 is returned
            - This parameter is ignored is stat is MONEY
        4. map: Dict[str, Char | Dict[str, Any]] (default None)
            - The map of characters to get the character from
            - If None and the name of the character is used instead of the Character-Object itself, -1 is returned
            - This parameter is ignored is stat is MONEY
        """

        if stat == MONEY:
            money.change_value(change)
        else:
            change_stat_for_char(stat, change, name, map)

    def change_stat_for_all(stat: str, delta: num, map: Dict[str, Char | Dict[str, Any]]):
        """
        Changes the stat value for all characters in the map

        ### Parameters:
        1. stat: str
            - The name of the stat to change
        2. delta: num
            - The value to change the stat by
        3. map: Dict[str, Char | Dict[str, Any]]
            - The map of characters to change the stat for
        """

        for character in map.keys():
            map[character].change_stat(stat, delta)

    def change_stat_for_char(stat: str, value: num, char: str | Char, map: Dict[str, Char | Dict[str, Any]] = None):
        """
        Changes the stat value for a character

        ### Parameters:
        1. stat: str
            - The name of the stat to change
        2. value: num
            - The value to change the stat by
        3. char: str | Char
            - The name of the character or the character itself to change the stat for
            - If there is no character in map with the name, -1 is returned
        """

        if isinstance(char, Char):
            char.change_stat(stat, value)
        elif map != None and char in map.keys():
            map[char].change_stat(stat, value)

    def reset_stats(char: str | Char = "", map: Dict[str, Char | Dict[str, Any]] = None):
        """
        Resets the change of all the stats

        ### Parameters:
        1. char: str | Char (default "")
            - The name of the character or the character itself to reset the stats for
            - If there is no character in map with the name, -1 is returned
            - If "", the stats for all characters in map are reset
        2. map: Dict[str, Char | Dict[str, Any]] (default None)
            - The map of characters to get the character from
            - If None and the name of the character is used instead of the Character-Object itself, -1 is returned
        """

        money.reset_change()
        
        if isinstance(char, Char):
            char.reset_changed_stats()
        elif map != None and char in map.keys():
            map[char].reset_changed_stats()
        elif map != None:
            for keys in map.keys():
                map[keys].reset_changed_stats()

    ####################
    # Char Level Handler

    def get_level_for_char(char: str | Char, map: Dict[str, Char | Dict[str, Any]] = None) -> int:
        """
        Returns the level of the character

        ### Parameters:
        1. char: str | Char
            - The name of the character to get the level from
            - If there is no character in map with the name, -1 is returned
        2. map: Dict[str, Char | Dict[str, Any]] (default None)
            - The map of characters to get the character from
            - If None and the name of the character is used instead of the Character-Object itself, -1 is returned

        ### Returns:
        1. int
            - The level of the character
            - -1 if the character does not exist
        """

        if isinstance(char, Char):
            return char.get_level()
        if map != None and char in map.keys():
            return map[char].get_level()
        return -1

    def set_level_for_char(value: int, char: str | Char, map: Dict[str, Char | Dict[str, Any]] = None):
        """
        Sets the level of the character

        ### Parameters:
        1. value: int
            - The value to set the level to
        2. char: str | Char
            - The name of the character or the character itself to set the level for
            - If there is no character in map with the name, -1 is returned
        3. map: Dict[str, Char | Dict[str, Any]] (default None)
            - The map of characters to get the character from
            - If None and the name of the character is used instead of the Character-Object itself, -1 is returned
        """

        if is_in_replay:
            return

        if isinstance(char, Char):
            char.set_level(value)
        elif map != None and char in map.keys():
            map[char].set_level(value)

    #####################
    # Char Object Handler

    def load_character(name: str, title: str, map: Dict[str, Char | Dict[str, Any]], start_data: Dict[str, Any], runtime_data: Dict[str, Any] = None):
        """
        Loads a character into the game

        ### Parameters:
        1. name: str
            - The name of the character
            - The name refers to the id representing the character. The actual name of the character is in title
        2. title: str
            - The title of the character
            - The title is the actual name of the character
        3. map: Dict[str, Char | Dict[str, Any]]
            - The map of characters to load the character into
        4. start_data: Dict[str, Any]
            - The data to initialize the character with
        5. runtime_data: Dict[str, Any] (default None)
            - The data that can be updated after the first initialization of the character
        """

        if name not in map.keys():
            map[name] = Char(name, title)
            map[name].__dict__.update(start_data)

        map[name]._update(runtime_data)

    def update_character(char: str | Char, data: Dict[str, Any], map: Dict[str, Char | Dict[str, Any]] = None):
        """
        Updates the character with the data

        ### Parameters:
        1. char: str | Char
            - The name of the character or the character itself to update
            - If there is no character in map with the name, -1 is returned
        2. data: Dict[str, Any]
            - The data to update the character with
        """

        if isinstance(char, Char):
            char._update(data)
        elif map != None and char in map.keys():
            map[char]._update(data)

    def remove_character(name: str, map: Dict[str, Char | Dict[str, Any]]):
        """
        Removes the character from the map

        ### Parameters:
        1. name: str
            - The name of the character to remove
        2. map: Dict[str, Char | Dict[str, Any]]
            - The map of characters to remove the character from
        """

        if name in map.keys():
            del(map[name])

    #############
    # Proficiency

    def exists_headmaster_proficiency(subject: str) -> bool:
        """
        Checks if the headmaster proficiency exists

        ### Parameters:
        1. subject: str
            - The subject to check
        """

        return subject in headmaster_proficiencies.keys()

    def set_headmaster_proficiency_level(subject: str, experience: int):
        """
        Sets the headmaster proficiency level

        ### Parameters:
        1. subject: str
            - The subject to set the level for
        2. experience: int
            - The experience to set the level to
        """

        headmaster_proficiencies[subject] = experience
        set_modifier("headmaster_proficiency_" + subject, Modifier_Obj("headmaster_proficiency_" + subject, "*", get_headmaster_proficiency_multiplier(subject)), stat = "all", collection = subject)

    def change_headmaster_proficiency_xp(subject: str, delta: int):
        """
        Changes the headmaster proficiency xp

        ### Parameters:
        1. subject: str
            - The subject to change the xp for
        2. delta: int
            - The value to change the xp by
        """

        if subject not in headmaster_proficiencies.keys():
            headmaster_proficiencies[subject] = 0
        set_headmaster_proficiency_level(subject, headmaster_proficiencies[subject] + delta)

    def get_headmaster_proficiency_level(subject: str) -> int:
        """
        Returns the headmaster proficiency level

        ### Parameters:
        1. subject: str
            - The subject to get the level for

        ### Returns:
        1. int
            - The level of the headmaster proficiency
        """

        if subject not in headmaster_proficiencies.keys():
            return 0
        return  math.floor(headmaster_proficiencies[subject] / 100)

    def get_headmaster_proficiency_levels() -> Dict[str, int]:
        """
        Returns the headmaster proficiency levels

        ### Returns:
        1. Dict[str, int]
            - The dictionary of the headmaster proficiency levels
        """

        return {subject: get_headmaster_proficiency_level(subject) for subject in headmaster_proficiencies.keys()}

    def get_headmaster_proficiency_xps() -> Dict[str, int]:
        """
        Returns the headmaster proficiency xps

        ### Returns:
        1. Dict[str, int]
            - The dictionary of the headmaster proficiency
        """

        return {subject: get_headmaster_proficiency_xp(subject) for subject in headmaster_proficiencies.keys()}

    def get_headmaster_proficiency_xp(subject: str) -> int:
        """
        Returns the headmaster proficiency xp

        ### Parameters:
        1. subject: str
            - The subject to get the xp for

        ### Returns:
        1. int
            - The xp of the headmaster proficiency
        """

        if subject not in headmaster_proficiencies.keys():
            return 0
        return headmaster_proficiencies[subject] % 100

    def get_headmaster_proficiency_xp_until_level(subject: str) -> int:
        """
        Returns the headmaster proficiency xp needed until the next level

        ### Parameters:
        1. subject: str
            - The subject to get the xp for

        ### Returns:
        1. int
            - The xp needed until the next level
        """

        if subject not in headmaster_proficiencies.keys():
            return -1
        return 100 - get_headmaster_proficiency_xp(subject)

    def get_headmaster_proficiency_multiplier(subject: str) -> float:
        """
        Returns the headmaster proficiency multiplier

        ### Parameters:
        1. subject: str
            - The subject to get the multiplier for

        ### Returns:
        1. float
            - The multiplier of the headmaster proficiency
        """

        if get_headmaster_proficiency_level(subject) > 0:
            return get_headmaster_proficiency_level(subject)
        return get_headmaster_proficiency_xp(subject) / 100

label load_schools ():
    # """
    # Loads and updates all the Character-Objects for the game
    # """

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

    $ load_character("parent", "Parents", charList, {
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

    #############################################
    # compatibility with version 0.1.2
    # loading of school is included
    $ fix_schools()

    return