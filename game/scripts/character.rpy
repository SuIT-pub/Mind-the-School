init -6 python:
    from typing import Dict, Any, Union, Tuple
    import math

    ########################
    # region CLASSES ----- #
    ########################

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
        6. set_stat(stat: str, value) -> None
            - Sets the value of the stat
        7. change_stat(stat: str, delta) -> None
            - Changes the value of the stat by delta
        8. get_stat_number(stat: str)
            - Returns the value of the stat
        9. get_stat_string(stat: str) -> str
            - Returns the value of the stat as a string
        10. reset_changed_stats() -> None
            - Resets the change of all the stats
        11. get_stats() -> Dict[str, Stat]
            - Returns the dictionary of all the stats
        12. check_stat(stat: str, value | str) -> bool
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
        21. check_level(value | str, test_level: int = None) -> bool
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

        def __str__(self):
            return self.get_name()

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

        ###########################
        # region Attribute getter #

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

        def get_stat_obj(self, stat: str):
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

        # endregion
        ###########################

        #######################
        # region Stat handler #

        def set_stat(self, stat: str, value):
            """
            Sets the value of the stat

            ### Parameters:
            1. stat: str
                - The name of the stat to set
            2. value
                - The value to set the stat to
            """

            if is_in_replay:
                return

            stat_obj = self.get_stat_obj(stat)
            if stat_obj == None:
                return
            stat_obj.set_value(value, self.get_level())

        def change_stat(self, stat: str, delta):
            """
            Changes the value of the stat by delta

            ### Parameters:
            1. stat: str
                - The name of the stat to change
            2. delta
                - The value to change the stat by
            """

            if is_in_replay:
                return

            stat_obj = self.get_stat_obj(stat)
            if stat_obj == None:
                return
            stat_obj.change_value(delta, self.get_level())

        def get_stat_number(self, stat: str):
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

        def get_stats(self):
            """
            Returns the dictionary of all the stats

            ### Returns:
            1. Dict[str, Stat]
                - The dictionary of all the stats
            """

            return self.stats_objects

        def check_stat(self, stat: str, value) -> bool:
            """
            Checks if the stat equals the value

            ### Parameters:
            1. stat: str
                - The name of the stat to check
            2. value | str
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
    
        # endregion
        #######################

        ########################
        # region Level handler #

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

        def get_level_obj(self):
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

        def check_level(self, value, test_level: int = None) -> bool:
            """
            Checks if the level equals the value

            ### Parameters:
            1. value | str
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
    
        # endregion
        ########################

    # endregion
    ########################

    ##############################
    # region School Char Handler #

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

    def get_school_stat(stat: str):
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
            return get_stat_number(stat)

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

    # endregion
    ##############################

    ###############################
    # region General Char Handler #

    def get_character(name: str, map: Dict[str, Union[Char, Dict[str, Any]]]) -> Char:
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

    # endregion
    ###############################

    ############################
    # region Char Stat Handler #

    def get_stat_number(stat: str) -> float:
        return get_school().get_stat_number(stat)

    def change_stat(stat: str, change):
        """
        Changes the stat value for a character or the money value if the stat is MONEY

        ### Parameters:
        1. stat: str
            - The name of the stat to change
        2. change
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
        elif stat.startswith("situation:"):
            situation_manager.apply_progress_change(stat, change)
        else:
            get_school().change_stat(stat, change)

    def reset_stats():
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
        
        get_school().reset_changed_stats()

    # endregion
    ############################

    #############################
    # region Char Level Handler #

    def get_level_for_char(char: Union[str, Char], map: Dict[str, Union[Char, Dict[str, Any]]] = None) -> int:
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

    def set_level_for_char(value: int, char: Union[str, Char], map: Dict[str, Union[Char, Dict[str, Any]]] = None):
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

    # endregion
    #############################

    ##############################
    # region Char Object Handler #

    def load_character(name: str, title: str, map: Dict[str, Union[Char, Dict[str, Any]]], start_data: Dict[str, Any], runtime_data: Dict[str, Any] = None):
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

    def update_character(char: Union[str, Char], data: Dict[str, Any], map: Dict[str, Union[Char, Dict[str, Any]]] = None):
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

    def remove_character(name: str, map: Dict[str, Union[Char, Dict[str, Any]]]):
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

    # endregion
    ##############################

    ######################
    # region Proficiency #

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

    # endregion
    ######################

    #################
    # region Person #

    @deprecated(version='0.2.2', reason="Use class Person instead")
    class PersonObj:
        def __init__(self, name: str, first_name: str, last_name: str, char: Char, description: List[Union[str, Tuple[str, Condition]]], portraits: Dict[str, Union[str, Tuple[str, Condition]]] = {}, thumbnail = ""):
            pass

    class Person():
        """
        A person object that contains all the information about a person

        ### Attributes:
        1. name: str
            - The name of the person
        2. first_name: str
            - The first name of the person
        3. last_name: str
            - The last name of the person
        4. description: List[Union[str, Tuple[str, Condition]]]
            - The description of the person
        5. portraits: Dict[str, Union[str, Tuple[str, Condition]]]
            - The portraits of the person
        6. character: Char
            - The character of the person
        7. basePath: str
            - The base path of the person
        8. thumbnail: str
            - The thumbnail of the person
        9. paperdollOverrides: List[:class:`PaperdollOverride`]
            - The paperdoll overrides of the person
        10. paperdollPresets: List[:class:`PaperdollPreset`]
            - Object-scoped paperdoll presets registered as `"{name}:{key}"` on `register_paperdoll`
        11. paperdollDefaults: Dict[str, Any]
            - Per-person paperdoll value defaults (pose, outfit, level, mood, …)
            - Applied on `register_paperdoll` after the house defaults, before call-time kwargs

        ### Parameters:
        1. name: str
            - The name of the person
        2. first_name: str
            - The first name of the person
        3. last_name: str
            - The last name of the person
        4. char: Char
            - The character of the person
        5. description: List[Union[str, Tuple[str, Condition]]]
            - The description of the person
        6. portraits: Dict[str, Union[str, Tuple[str, Condition]]]
            - The portraits of the person
        7. paperdollOverrides: List[:class:`PaperdollOverride`]
            - The paperdoll overrides of the person
        8. thumbnail: str
            - The thumbnail of the person
        9. paperdollPresets: List[:class:`PaperdollPreset`]
            - Character-specific paperdoll presets registered as temp `"name:key"` entries
        10. paperdollDefaults: Dict[str, Any]
            - Optional value defaults that replace the house paperdoll seeds for this person
            - e.g. `{"level": 5}` when the character has no level-1 uniform
        """

        def __init__(self, name: str, first_name: str, last_name: str, char: Char, description: List[Union[str, Tuple[str, Condition]]], portraits: Dict[str, Union[str, Tuple[str, Condition]]] = {}, paperdollOverrides: List[PaperdollOverride] = [], thumbnail = "", paperdollPresets = None, paperdollDefaults = None):
            self.name = name
            self.first_name = first_name
            self.last_name = last_name
            self.description = description
            self.portraits = portraits
            self.character = char
            self.basePath = get_current_mod_path()
            if thumbnail == "":
                self.thumbnail = f"{self.basePath}images/characters/{self.name}/level_1.webp"
            else:
                self.thumbnail = thumbnail
            self.paperdollOverrides = list(paperdollOverrides)
            self.paperdollPresets = list(paperdollPresets) if paperdollPresets is not None else []
            self.paperdollDefaults = dict(paperdollDefaults) if paperdollDefaults is not None else {}

        @classmethod
        def __class_getitem__(cls, key):
            """
            Returns the person object with the given key

            ### Parameters:
            1. key: str
                - The key of the person to get
            """
            return find_person(key)

        def _update(self, data):
            
            if not hasattr(data, 'name'):
                self.name = ""
            if not hasattr(data, 'first_name'):
                self.first_name = ""
            if not hasattr(data, 'last_name'):
                self.last_name = ""
            if not hasattr(data, 'description'):
                self.description = []
            if not hasattr(data, 'portraits'):
                self.portraits = {}
            if not hasattr(data, 'thumbnail'):
                self.thumbnail = ""
            if not hasattr(data, 'paperdollOverrides'):
                self.paperdollOverrides = []
            if not hasattr(data, 'paperdollPresets'):
                self.paperdollPresets = []
            if not hasattr(data, 'paperdollDefaults'):
                self.paperdollDefaults = {}

            if data != None:
                self.name = data.name
                self.first_name = data.first_name
                self.last_name = data.last_name
                self.description = data.description
                self.portraits = data.portraits
                self.paperdollOverrides = data.paperdollOverrides
                if hasattr(data, 'paperdollPresets'):
                    self.paperdollPresets = data.paperdollPresets
                if hasattr(data, 'paperdollDefaults'):
                    self.paperdollDefaults = dict(data.paperdollDefaults) if data.paperdollDefaults else {}

        def get_name(self) -> str:
            return self.name

        def get_description(self, **kwargs) -> List[str]:
            output = []
            for desc in self.description:
                data = desc
                if isinstance(desc, Tuple):
                    if desc[1].is_fulfilled(**kwargs):
                        continue
                    else:
                        data = desc[0]
                
                if isinstance(data, str):
                    output.append(data)
                elif isinstance(data, list):
                    output.extend(data)
                else:
                    output.append(data)
            return output

        def get_description_str(self, **kwargs) -> str:
            return "\n".join(self.get_description(**kwargs))

        def get_portraits(self) -> Dict[str, str]:
            output = {}
            for level in range(1, get_school().get_level() + 1):
                resolved = find_loadable_image(f"{self.basePath}images/characters/{self.name}/level_{level}.webp")
                if resolved:
                    output[f"Level {level}"] = resolved

            resolved_nude = find_loadable_image(f"{self.basePath}images/characters/{self.name}/nude.webp")
            if resolved_nude:
                output["nude"] = resolved_nude

            for portrait_key in self.portraits.keys():
                portrait = self.portraits[portrait_key]
                if isinstance(portrait, str):
                    resolved = find_loadable_image(f"{self.basePath}images/characters/{self.name}/{portrait}.webp")
                    if resolved:
                        output[portrait_key] = resolved
                elif portrait[1].is_fulfilled(**kwargs):
                    if "images/" not in portrait[0]:
                        resolved = find_loadable_image(f"{self.basePath}images/characters/{self.name}/{portrait[0]}.webp")
                        if resolved:
                            output[portrait_key] = resolved
                    else:
                        resolved = find_loadable_image(portrait[0])
                        output[portrait_key] = resolved if resolved else portrait[0]

            return output

        def get_thumbnail(self) -> str:
            resolved = find_loadable_image(self.thumbnail)
            if not resolved:
                return "images/journal/empty_image.webp"
            return resolved

        def get_first_name(self) -> str:
            if self.first_name == "":
                if self.last_name != "":
                    return self.last_name
                return self.name 

            return self.first_name
        def get_last_name(self) -> str:
            if self.last_name == "":
                if self.first_name != "":
                    return self.first_name
                return self.name

            return self.last_name
        def get_full_name(self) -> str:
            if self.first_name == "" and self.last_name != "":
                return self.last_name
            if self.last_name == "" and self.first_name != "":
                return self.first_name

            return f"{self.first_name} {self.last_name}"

        def set_thumbnail(self, thumbnail: str):
            self.thumbnail = thumbnail

        @property
        def say(self):
            return self.get_renpy_char()

        @property
        def think(self):
            return self.get_renpy_char(char_type = "thought")

        @property
        def whisper(self):
            return self.get_renpy_char(char_type = "whisper")

        @property
        def shout(self):
            return self.get_renpy_char(char_type = "shout")

        def get_renpy_char(self, char_type: string = "") -> Character:

            char_kind = character.subtitles

            if self.character == get_character_by_key('school'):
                char_kind = character.sgirl
            elif self.character == get_character_by_key('parent'):
                char_kind = character.parent
            elif self.character == get_character_by_key('teacher'):
                char_kind = character.teacher
            elif self.character == get_character_by_key('secretary'):
                char_kind = character.secretary

            if char_type == "shout":
                return Character(self.get_full_name(), kind = char_kind, retain = False, who_suffix = " (shouting)", what_bold = True)
            elif char_type == "whisper":
                return Character(self.get_full_name(), kind = char_kind, retain = False, who_suffix = " (whispering)", what_italic = True)
            elif char_type == "thought":
                return Character(self.get_full_name(), kind = char_kind, retain = False, who_suffix = " (thinking)", what_italic = True, what_prefix = "(  ", what_suffix = "  )")
            else:
                return Character(self.get_full_name(), kind = char_kind, retain = False)

        def register_paperdoll(self, *overrides: PaperdollOverride, **kwargs):
            # House defaults ← Person.paperdollDefaults ← call-time kwargs
            data = update_dict(
                {"alt_keys": ["level", "mouth", "state", "char_var", "extra1", "extra2"], "mood": "neutral", "pose": 1, "outfit": "uniform", "level": 1, "mouth": "closed", "state": "", "blur": 0.0, "char_var": 1, "look": "follow", "extra1": "", "extra2": ""},
                getattr(self, "paperdollDefaults", None) or {},
            )
            data = update_dict(data, kwargs)
            global paperdoll_manager
            log_val("register paperdoll_manager", paperdoll_manager)
            overrides = list(overrides) + self.paperdollOverrides
            log_val("overrides", overrides)
            paperdoll_manager.register_obj(
                self.name, 
                f"{self.basePath}images/paperdoll/{self.name}/bottom/{self.name} <char_var> <pose> <outfit> <level> <state> <extra1>.png", 
                f"{self.basePath}images/paperdoll/{self.name}/top/{self.name} <char_var> <pose> <mood> <mouth> <look> <extra2>.png", 
                display_size = (600, 1080),
                overrides = list(overrides) + self.paperdollOverrides,
                presets = list(self.paperdollPresets),
                **data
            )

        def display(self, *actions: Dict[str, Any]):
            paperdoll_manager.display(self.name, *actions)

        def clear_display(self):
            if paperdoll_manager is not None:
                paperdoll_manager.clear()

    def find_person(name: str):
        for key in person_storage.keys():
            if name in person_storage[key].keys():

                return person_storage[key][name]
        return None

    def get_person(key: str, name: str):
        """
        Returns the person object with the given key and name

        ### Parameters:
        1. key: str
            - The key of the person
            - Possible keys: "class_3a", "staff", "parents"
        2. name: str
            - The name of the person

        ### Returns:
        1. Person
            - The person object with the given key and name
        """

        if key not in person_storage.keys():
            log(f"Person with key {key} not found", log_type="error", category="character")
            return None
        if name not in person_storage[key].keys():
            log(f"Person with name {name} not found", log_type="error", category="character")
            return None
        return person_storage[key][name]

    def get_person_char_with_key(key: str, name: str, char_type: string = ""):
        """
        Returns the character object of the person with the given key and name

        ### Parameters:
        1. key: str
            - The key of the person
            - Possible keys: "class_3a", "staff", "parents"
        2. name: str
            - The name of the person

        ### Returns:
        1. Character
            - The character object of the person with the given key and name
        """

        if key not in person_storage.keys():
            log(f"Person with key {key} not found", log_type="error", category="character")
            return None
        if name not in person_storage[key].keys():
            log(f"Person with name {name} not found", log_type="error", category="character")
            return None
        return person_storage[key][name].get_character(char_type)

    def load_person(key: str, person: Person):
        # Gated on the current mod being active (like event `add_event`): a disabled
        # mod's persons are not registered. Base loaders set `set_current_mod('base')`,
        # and base is always active.
        if not is_mod_active(active_mod_key):
            return

        if key not in person_storage.keys():
            person_storage[key] = {}

        if person.name not in person_storage[key].keys() or isinstance(person_storage[key][person.name], PersonObj):
            person_storage[key][person.name] = person
        else:
            person_storage[key][person.name]._update(person)

    # endregion
    #################

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

label load_characters ():
    $ set_current_mod('base')
    $ school_char = get_character_by_key('school')
    $ parent_char = get_character_by_key('parent')
    $ teacher_char = get_character_by_key('teacher')
    $ secretary_char = get_character_by_key('secretary')

    $ load_person("NoView", Person("default", "", "Person", school_char, []))
    $ load_person("NoView", Person("default_school", "", "School Girl", school_char, []))
    $ load_person("NoView", Person("default_parent", "", "Parent", parent_char, []))
    $ load_person("NoView", Person("default_teacher", "", "Teacher", teacher_char, []))
    $ load_person("NoView", Person("default_secretary", "", "Secretary", secretary_char, []))

    $ load_person("class_3a", Person("aona_komuro", "Aona", "Komuro", school_char, [
            "• Height: 172.5 cm",
            "Tall and strongly hourglass, with long wavy pale-blonde hair loose past her shoulders and pale blue eyes in a soft, youthful face.",
            (["", "{b}Measurements{/b}", "• Bra Size 75F (DDD)", "• B-W-H: 89-74-98 cm", "• Waist-to-Hips: 0.756"], EventSeenCondition(False, "new_yoga_outfit_9")),
            (["", "{b}Breasts{/b}", "Big and full, round and soft with a natural weight, projecting forward and wide-set with a soft gap between them. The standout is the areolae: large, pale-pink and puffy, swelling out as raised domes that push each whole nipple forward in a soft protruding mound, the little nipple tipped at the centre. Smooth, poreless, milk-pale skin, heavy enough to explain the back trouble she complains about."], NOT(GameDataCondition("seen_breasts_aona_komuro", True))),
            (["", "{b}Ass{/b}", "Big, soft, and heavy — a full bottom that hangs low and plush, the pale cheeks soft and spreading wide over thick, full thighs. Broad hips carry it, and from the side it swells out deep and soft. A generous, fleshy backside, all soft curves."], NOT(GameDataCondition("seen_ass_aona_komuro", True))),
            (["", "{b}Pussy{/b}", "Between her thick thighs she's smooth and clean-shaven, a soft, plump, puffy mound with a neat closed slit tucked at the join. Bare, pale, and simple — no hair, the lips pressed shut and tidy, framed by the full inner curves of her heavy thighs."], NOT(GameDataCondition("seen_pussy_aona_komuro", True))),
            (["", "{b}Personality{/b}", "Loud, brash, and hungry for attention — she needs to be the center of the room and works for it through boasting, teasing, or sheer volume. She competes at everything and can't give a short answer when a long story will hold the floor.", "Quick to anger and quick to envy: let someone outshine her and the temper flares, all wounded pride."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "For all the bravado she's more fragile than she lets on, and specifically insecure about her own body — that very large chest gives her real back pain and embarrassment, and early on she'd rather cover up than show off. As the school opens up her craving for eyes reroutes from cruelty into sex: first to volunteer, the one who wants to be watched, in time a full exhibitionist. The engine never changes, only where she points it."], NOT(LevelCondition("5+"))),
        ]
    ))
    $ load_person("class_3a", Person("easkey_tanaka", "Easkey", "Tanaka", school_char, [
            "• Height: 168.8 cm",
            "In a relationship with Sakura Mori.",
            "Coppery auburn-red hair, wavy and tousled in a loose low side-tail with face-framing bangs; blue-green eyes, fair freckled skin, and a soft, curvy figure.",
            (["", "{b}Measurements{/b}", "• Bra Size 65DD (E)", "• B-W-H: 78-68-98 cm", "• Waist-to-Hips: 0.689"], EventSeenCondition(False, "new_yoga_outfit_9")),
            (["", "{b}Breasts{/b}", "Full and round, sitting up firm on her chest with an upturned set. Her nipples are the standout: prominent and protruding, a dusky pinkish-mauve, pushed forward and pointing up and out from medium tan-mauve areolae. The freckling from her face carries right down over her shoulders and the tops of her breasts, a coppery dusting scattered across the pale skin."], NOT(GameDataCondition("seen_breasts_easkey_tanaka", True))),
            (["", "{b}Ass{/b}", "Round and full, soft and smooth — a plump bottom that sits out in a full curve over soft, wide thighs, the cheeks generous and rounded. Her hips are broad and soft, a gently rounded little tummy above. Freckles carry over her shoulders and down her back, and the skin is fair and pale, soft to look at all over."], NOT(GameDataCondition("seen_ass_easkey_tanaka", True))),
            (["", "{b}Pussy{/b}", "Smooth and clean-shaven between her soft, full thighs, a plump bare mound with a neat closed slit at the join. Fair pale skin, a little soft roll of belly just above. Simple and bare, framed by the soft inner curves of her wide thighs."], NOT(GameDataCondition("seen_pussy_easkey_tanaka", True))),
            (["", "{b}Personality{/b}", "Shy, gentle, and easily flustered — she stammers when she's put on the spot and would rather not be noticed. Frank about disliking schoolwork, and not much driven by it."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "In a steady relationship with Sakura Mori, who's the more capable, grounded half of the pair. As the campus opens up she loosens in Sakura's company but stays one of the softer, more retiring girls — her shyness never quite becomes boldness."], NOT(LevelCondition("5+"))),
        ],
    ))
    $ load_person("class_3a", Person("elsie_johnson", "Elsie", "Johnson", school_char, [
            "• Height: 168.0 cm",
            "In a relationship with Yuriko Oshima.",
            "Short platinum-blonde hair in a blunt chin-length bob with a straight fringe, round black-framed glasses she wears constantly, pale skin freckled over her whole body, blue-grey eyes, and a curvy hourglass figure.",
            (["", "{b}Measurements{/b}", "• Bra Size 65D", "• B-W-H: 76-63-105 cm", "• Waist-to-Hips: 0.689"], EventSeenCondition(False, "new_yoga_outfit_9")),
            (["", "{b}Breasts{/b}", "Full and round, soft and heavy with a natural fullness, the lower curve full and the nipples pointing down and slightly out. They're small and pale-pink, a little puffy, on medium pale-pink areolae. And the freckles cover them too: the dense all-over speckling that marks her whole body scatters right across her breasts and chest, dark flecks over porcelain-pale skin, freckled to the areolae."], NOT(GameDataCondition("seen_breasts_elsie_johnson", True))),
            (["", "{b}Ass{/b}", "Round and full, projecting in a firm curve from very wide hips, the cheeks smooth and full over thick, heavy thighs. Freckles cover every inch — the same dense speckling runs over her back, her ass, her hips, and all the way down her thighs, dark flecks scattered thick across pale skin. A curvy, wide-hipped bottom, freckled top to bottom."], NOT(GameDataCondition("seen_ass_elsie_johnson", True))),
            (["", "{b}Pussy{/b}", "Smooth and clean-shaven between her thick, freckled thighs, a bare mound with a neat closed slit at the join. Even here the skin is dusted — the all-over freckling carries down over her lower belly, hips, and the insides of her thighs, framing the bare, pale mound in speckled skin. Simple and bare, freckled all around."], NOT(GameDataCondition("seen_pussy_elsie_johnson", True))),
            (["", "{b}Personality{/b}", "Gentle, modest, and quietly bookish — calm and studious, soft-spoken and easy to overlook around people she doesn't know well."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "But she's an ambivert, not an introvert: with the few she trusts — above all her girlfriend Yuriko Oshima — she's warm, chatty and openly affectionate, the steady anchor Yuriko leans on. Where Yuriko is prickly and withdrawn, Elsie is patient and kind; the split between reserved-in-the-open and open-with-her-own never changes."], NOT(LevelCondition("5+"))),
        ],
    ))
    $ load_person("class_3a", Person("gloria_goto", "Gloria", "Goto", school_char, [
            "• Height: 160.4 cm",
            "Petite and slim, one of the smaller girls in class, with a short tousled ash-blonde bob, wispy bangs, and a small green flower clip pinned above her right ear that she never takes off. Blue-grey eyes, a modest bust, a girlish figure.",
            (["", "{b}Measurements{/b}", "• Bra Size 65C", "• B-W-H: 73-57-82 cm", "• Waist-to-Hips: 0.693"], EventSeenCondition(False, "new_yoga_outfit_9")),
            (["", "{b}Breasts{/b}", "Full and round, a substantial handful sitting up firm on her slim frame, the rounded shape projecting forward in a smooth full curve. Her nipples are small and pink, a little puffy, neat on small pale-pink areolae. Porcelain-pale, smooth skin drawn taut over the full swell."], NOT(GameDataCondition("seen_breasts_gloria_goto", True))),
            (["", "{b}Ass{/b}", "Round and perky, a smooth full bottom that sits up high and pushes out in a clean bubble curve from a slender waist and narrow hips. The cheeks are firm and rounded, pale and smooth, projecting neatly on her slight frame, slim thighs running down below."], NOT(GameDataCondition("seen_ass_gloria_goto", True))),
            (["", "{b}Pussy{/b}", "Smooth and clean-shaven between slim, pale thighs, a small neat mound with a closed slit and just the tip of her inner lips showing at the base. Bare and pink, small and tidy, tucked between the tops of her slender thighs. Porcelain-pale skin all around."], NOT(GameDataCondition("seen_pussy_gloria_goto", True))),
            (["", "{b}Personality{/b}", "An analytical nerd, endlessly and bluntly curious — she treats bodies, sex, and other people's private lives as fascinating subject matter to catalogue. Her default is a flat, clinical deadpan that cracks into eager over-explaining the moment something genuinely interests her."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "Her curiosity has no brakes, and that's the unsettling part: ethics come a distant second to knowing, and she can treat the people she studies as data points rather than friends. As the campus opens up the same detached lens turns to sex directly — she surveys, records, experiments, narrating even her own arousal as calmly as anyone else's."], NOT(LevelCondition("5+"))),
        ],
    ))
    $ load_person("class_3a", Person("luna_clark", "Luna", "Clark", school_char, [
            "• Height: 144.8 cm",
            "Twin sister of Seraphina Clark.",
            "Very petite yet curvy, with silver-white hair in short low pigtails, bold red-framed glasses she never takes off, and heterochromatic eyes — right blue, left green.",
            (["", "{b}Measurements{/b}", "• Bra Size 55D", "• B-W-H: 65-48-81 cm", "• Waist-to-Hips: 0.587"], EventSeenCondition(False, "new_yoga_outfit_9")),
            (["", "{b}Breasts{/b}", "Big and heavy for so small a girl, and startlingly so — full, rounded globes that sit high and firm on her chest, with a soft, full weight to the underside and deep cleavage when her arms come down. From the side they push out well past her slim ribs, the undersides curving full and plump. Her nipples are small and neat, protruding as pointed little nubs, a pale rose barely deeper than her ivory skin, set a touch high and pointing faintly outward; the areolae are small and smooth, the palest pink. Flawless, poreless skin over all of it."], NOT(GameDataCondition("seen_breasts_luna_clark", True))),
            (["", "{b}Ass{/b}", "Round, full, and out of all proportion to her tiny frame. From behind it's a heavy heart: the cheeks smooth and taut and plump, projecting well past the line of her lower back, which curves in sharply above them to shelf the whole thing out. Wide hips frame it and a clean thigh gap opens beneath; the skin is flawless and pale, catching the light across each full curve. Far too much bottom for so small a body."], NOT(GameDataCondition("seen_ass_luna_clark", True))),
            (["", "{b}Pussy{/b}", "Between her thighs she's smooth and completely bare — a soft, plump mound with a gentle rise and not a trace of hair. The full outer lips are tucked shut into a clean, closed cleft, just a thin pink line down the centre with the faintest tip of the inner lips at the very base. With her thighs pressed the whole of it reads small, neat, and pristine — a smooth pale seam framed by the full inner curves of her legs."], NOT(GameDataCondition("seen_pussy_luna_clark", True))),
            (["", "{b}Personality{/b}", "The quieter Clark twin — shy and reserved on the surface, timid on her own and happy to hang back."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "Beneath the shyness runs a sly, mischievous streak deeper than anyone expects. With Seraphina she's one half of the class's chaos-and-pranks duo — and often the real schemer behind it, the innocent-looking one nobody suspects until the trap is already sprung. She lags half a step behind her sister at every stage, needing Sera's cover before she'll open up; the higher the school climbs, the more that trickster shows."], NOT(LevelCondition("5+"))),
        ],
        thumbnail = "images/characters/luna_clark/level_1.webp",
    ))
    $ load_person("class_3a", Person("seraphina_clark", "Seraphina", "Clark", school_char, [
            "• Height: 144.8 cm",
            "Twin sister of Luna Clark.",
            "Very petite yet curvy, silver-white hair in a short blunt bob with low tails, black-framed glasses she never removes, and mirror-swapped heterochromia — right green, left blue. The glasses tell the twins apart: hers black, Luna's red.",
            (["", "{b}Measurements{/b}", "• Bra Size 55DD (E)", "• B-W-H: 68-48-81 cm", "• Waist-to-Hips: 0.587"], EventSeenCondition(False, "new_yoga_outfit_9")),
            (["", "{b}Breasts{/b}", "Big and heavy on so tiny a body — full, rounded globes that sit high and firm with deep cleavage, wildly out of scale with her little frame. Her nipples are small and neat, protruding as pointed pink nubs a shade deeper than her ivory skin, set a touch high and pointing faintly outward; the areolae are small and smooth, the palest pink. From the side each pushes out full and round well past her slim ribs, the underside curving plump. Flawless, poreless skin over all of it."], NOT(GameDataCondition("seen_breasts_seraphina_clark", True))),
            (["", "{b}Ass{/b}", "Round, full, and out of all proportion to her tiny waist. From behind it's a heavy heart — smooth, taut, plump cheeks projecting well past the sharp inward curve of her lower back; from the side it swells out in a big, clean arc over the top of her thighs. Wide hips frame a waist cinched startlingly narrow. Flawless pale skin, catching the light across each full curve."], NOT(GameDataCondition("seen_ass_seraphina_clark", True))),
            (["", "{b}Pussy{/b}", "Between her thighs she's smooth and completely clean-shaven — a soft, plump mound with not a trace of hair. The full outer lips part to a slim pink centre where the inner lips just show, a small clit tucked at the top of the cleft and the faintest tip at the base. Framed by the full inner curves of her thighs, the whole of it reads small, neat, and pink."], NOT(GameDataCondition("seen_pussy_seraphina_clark", True))),
            (["", "{b}Personality{/b}", "The forward Clark twin — active, socially confident, and a prankster at heart. She's the loud, visible half of the chaos-and-pranks duo, happy to be the grinning face of a scheme."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "Precocious and quick with a teasing joke, she fronts the mischief while quiet Luna plots behind her. Even at the lowest levels she reads as more open and curious than her peers — though open isn't explicit; at level 1 she's still fundamentally innocent, just less shy about it. She reaches each new stage of the campus a little early, pulling hesitant Luna along after her."], NOT(LevelCondition("5+"))),
        ],
    ))
    $ load_person("class_3a", Person("hatano_miwa", "Hatano", "Miwa", school_char, [
            "• Height: 165.7 cm",
            "Petite and youthful, long brown hair in high twin-tails with a straight fringe, fair skin, blue eyes, a slim small frame with a modest bust — a cute, trend-conscious look.",
            (["", "{b}Measurements{/b}", "• Bra Size 70A", "• B-W-H: 73-63-87 cm", "• Waist-to-Hips: 0.725"], EventSeenCondition(False, "new_yoga_outfit_9")),
            (["", "{b}Breasts{/b}", "Small and neat, sitting a little low on her slim chest with a soft rounded fullness, the nipples clearly angled down and out. They're a dusky pink-mauve and slightly puffy on small mauve areolae. Fair, pale, smooth skin; a small, girlish chest with downward-tilted nipples."], NOT(GameDataCondition("seen_breasts_hatano_miwa", True))),
            (["", "{b}Ass{/b}", "Round and full, a smooth bubble of a bottom that projects out in a firm curve from her slim waist and narrow hips. The cheeks are plump and rounded, pale and smooth, sitting up round on her slight frame, slim thighs running below."], NOT(GameDataCondition("seen_ass_hatano_miwa", True))),
            (["", "{b}Pussy{/b}", "Smooth and clean-shaven between slim, pale thighs, a small neat mound with a closed slit and just the tip of her inner lips peeking at the base. Bare and pink, small and tidy, tucked high between the tops of her slender thighs. Porcelain-pale skin around it."], NOT(GameDataCondition("seen_pussy_hatano_miwa", True))),
            (["", "{b}Personality{/b}", "A fashionista through and through — loves shopping, turns up in on-trend outfits, and carries a real gyaru (gal) attitude. Vain and a little arrogant about it, sure she has the best taste in the room and quick with a catty remark about a bad outfit."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "Hers is loud, in-your-face superiority rather than cold snobbery (that is Soyoon Yamamoto's lane) — still sociable and high-energy, just convinced she is a cut above on style. Her love of showing off makes her an early adopter of each new look as the campus opens up. (Not to be confused with Miwa Igarashi — different girl, shared first name.)"], NOT(LevelCondition("5+"))),
        ],
    ))
    $ load_person("class_3a", Person("ikushi_ito", "Ikushi", "Ito", school_char, [
            "• Height: 164.3 cm",
            "Silver-grey hair in a short bob with a fringe and striking golden-amber eyes — an unusual, eye-catching pair. Fair skin, a notably full bust on an otherwise slim frame.",
            (["", "{b}Measurements{/b}", "• Bra Size 65G (DDDD)", "• B-W-H: 82-62-92 cm", "• Waist-to-Hips: 0.678"], EventSeenCondition(False, "new_yoga_outfit_9")),
            (["", "{b}Breasts{/b}", "The standout on an otherwise slim frame — big, full, heavy breasts that look all the larger for the narrow body carrying them. Round and soft with real weight, a deep valley of cleavage between them, projecting forward and full from the side with heavy, rounded undersides. Her nipples are a soft pink and lightly puffy, set on medium pink areolae a touch darker than her fair skin and pointing gently up and out. Smooth, pale, poreless skin over the generous swell."], NOT(GameDataCondition("seen_breasts_ikushi_ito", True))),
            (["", "{b}Ass{/b}", "Round and full — smooth, plump cheeks that sit high and push out in a clean curve over the backs of her thighs, framed by curvy hips that flare from a slim waist. From behind it's a full, rounded heart in pale skin; from the side it swells out soft and firm. Flawless, poreless skin catching the light across it."], NOT(GameDataCondition("seen_ass_ikushi_ito", True))),
            (["", "{b}Pussy{/b}", "Not quite bare — she keeps a small, neat patch of pale silver-grey hair, a soft trimmed little tuft above the cleft that matches the colour of the hair on her head, so faint against her fair skin it's easy to miss at a glance. The mound around it is smooth, the slit below closed and tidy between slim inner thighs."], NOT(GameDataCondition("seen_pussy_ikushi_ito", True))),
            (["", "{b}Personality{/b}", "Shy but game — bashful about intimate questions yet fundamentally honest, she caves to peer pressure only to own it a beat later ('Fine, I'll do it!'). Stoic about small hurts, quietly curious."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "Openly a little smitten with the Headmaster. At low levels her shyness fights her curiosity and the group has to talk her into things; as the campus opens up the hesitation thins and she goes along more freely — still more follower than instigator."], NOT(LevelCondition("5+"))),
        ],
    ))
    $ load_person("class_3a", Person("ishimaru_maki", "Ishimaru", "Maki", school_char, [
            "• Height: 170.8 cm",
            "A sleek blue-black bob with blunt straight bangs, dark eyes, fair skin; one of the taller, leaner girls with a slim build and a moderate bust.",
            (["", "{b}Measurements{/b}", "• Bra Size 70B", "• B-W-H: 75-68-91 cm", "• Waist-to-Hips: 0.743"], EventSeenCondition(False, "new_yoga_outfit_9")),
            (["", "{b}Breasts{/b}", "Moderate and round, sitting full and firm on her lean chest, holding a rounded shape. The nipples are the feature: fairly large and prominent, puffy and pushed forward on broad mauve-pink areolae that swell out from the breast. Fair, porcelain-pale skin, smooth over the full curve."], NOT(GameDataCondition("seen_breasts_ishimaru_maki", True))),
            (["", "{b}Ass{/b}", "Round and full, projecting out in a smooth bubble curve from her lean waist and hips, the cheeks plump and rounded on her slim, tall frame. Pale and smooth, sitting up round and firm, long lean legs running down below."], NOT(GameDataCondition("seen_ass_ishimaru_maki", True))),
            (["", "{b}Pussy{/b}", "Smooth and clean-shaven between lean, pale thighs, a small neat mound with a closed slit and the tip of her inner lips showing at the base. Bare and pink, tucked between the tops of her slim thighs, porcelain-pale skin all around."], NOT(GameDataCondition("seen_pussy_ishimaru_maki", True))),
            (["", "{b}Personality{/b}", "Enthusiastic, fun-loving, and a little clumsy — a dedicated guitarist (her instant answer to 'favourite hobby'), the one who brings the card game and keeps the group entertained. Warm and quick to apologise when she bumps into things."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "There's a faintly edgy, band-girl streak under the wholesome fun — the guitarist, not just the nice girl. Her upbeat, game-for-anything energy carries her along as the campus opens up; she joins in readily without ever being the one leading it."], NOT(LevelCondition("5+"))),
        ],
    ))
    $ load_person("class_3a", Person("kokoro_nakamura", "Kokoro", "Nakamura", school_char, [
            "• Height: 163.4 cm",
            "Long auburn-red hair in a voluminous, glamorous side-swept style cascading over one shoulder; blue-grey eyes, fair skin, soft pink lips, and a slim, elegant figure with a moderate bust.",
            (["", "{b}Measurements{/b}", "• Bra Size 70B", "• B-W-H: 76-66-89 cm", "• Waist-to-Hips: 0.739"], EventSeenCondition(False, "new_yoga_outfit_9")),
            (["", "{b}Breasts{/b}", "Small and firm, sitting high and round on her slim chest, upturned and perky, the curve projecting forward. The nipples are prominent and puffy, pushed out from small mauve areolae and tilted slightly up. Fair, porcelain-pale skin, smooth and taut over the round little swell."], NOT(GameDataCondition("seen_breasts_kokoro_nakamura", True))),
            (["", "{b}Ass{/b}", "Round and full, a smooth shapely bottom that projects out in a deep curve from her slim waist and hips. The cheeks are plump and rounded, pale and smooth, sitting up round and firm on her slim, elegant frame, slim thighs running down below."], NOT(GameDataCondition("seen_ass_kokoro_nakamura", True))),
            (["", "{b}Pussy{/b}", "Smooth and clean-shaven between slim, pale thighs, a small neat mound with a closed slit and the tip of her inner lips at the base. Bare and pink, tucked between the tops of her slender thighs, porcelain-pale skin around it."], NOT(GameDataCondition("seen_pussy_kokoro_nakamura", True))),
            (["", "{b}Personality{/b}", "Shy, modest, and quick to fluster — pushed out of her comfort zone she wells up rather than pushes back. Yet she carries a quiet, grown-up sense of style and a poise that read as more composed than she actually feels."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "Underneath it all she's genuinely curious, asking frank, almost clinical questions about sex and the body once the subject is opened. As the campus climbs, that curiosity and understated elegance win out over the embarrassment — though she never becomes brazen about it."], NOT(LevelCondition("5+"))),
        ],
    ))
    $ load_person("class_3a", Person("lin_kato", "Lin", "Kato", school_char, [
            "• Height: 167.6 cm",
            "Black hair with a faint blue sheen in a high side ponytail with a swept fringe, bright green eyes, freckles across nose and cheeks; a slim, athletic figure with a toned midriff, smaller bust, and curvy hips.",
            (["", "{b}Measurements{/b}", "• Bra Size 65B", "• B-W-H: 70-63-94 cm", "• Waist-to-Hips: 0.663"], EventSeenCondition(False, "new_yoga_outfit_9")),
            (["", "{b}Breasts{/b}", "Small and firm on her slim frame — neat, round, upturned handfuls that sit high and hold their shape, barely more than a B-cup. The standout is the nipples: a vivid bright pink, puffy and prominently protruding, sticking well out as bright little nubs from small, matching pink areolae. From the side they perk up firm and round, the bright nipple pushed forward. Smooth, fair skin over the youthful swell."], NOT(GameDataCondition("seen_breasts_lin_kato", True))),
            (["", "{b}Ass{/b}", "Round, full, and firm, carried on curvy hips. From behind it's a smooth, rounded heart — the pale cheeks plump and taut and well-shaped; from the side it projects back in a clean, generous curve with a firm underside. Flawless fair skin over each rounded plane."], NOT(GameDataCondition("seen_ass_lin_kato", True))),
            (["", "{b}Pussy{/b}", "Between her thighs she keeps a small, neat triangle of dark pubic hair — groomed and tidy, a soft dark tuft high on an otherwise smooth pale mound. Below it the slit is close and neat, with just the tip of the inner lips showing pink at the base. Slim thighs frame it, a clean gap beneath."], NOT(GameDataCondition("seen_pussy_lin_kato", True))),
            (["", "{b}Personality{/b}", "Sociable, easygoing, and funny — the one who keeps the fun going, organises the games, eggs everyone on, and loves dumb internet cat videos. Practical, unpretentious, a bit of a ringleader."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "She'll deflect with a quick 'I'm not that kind of person' when a dare cuts too close, but as the campus opens up the ringleader energy carries straight over — game, loud about it, and the one daring everyone else on, without much hang-up."], NOT(LevelCondition("5+"))),
        ],
    ))
    $ load_person("class_3a", Person("miwa_igarashi", "Miwa", "Igarashi", school_char, [
            "• Height: 158.9 cm",
            "Likes dancing.",
            "Brown hair up in a messy high bun with loose framing strands, dark brown eyes, fair skin; slim and lightly athletic — a dancer's build with a small bust — and a stack of colourful friendship bracelets always on one wrist.",
            (["", "{b}Measurements{/b}", "• Bra Size 65B", "• B-W-H: 69-62-84 cm", "• Waist-to-Hips: 0.739"], EventSeenCondition(False, "new_yoga_outfit_9")),
            (["", "{b}Breasts{/b}", "Small and soft — genuinely modest, gentle little mounds that sit slightly apart and hold a soft, natural shape with the faintest downward tilt. Her nipples are small and a touch puffy, a soft pinkish-mauve on small, close areolae, pointing forward and a little down. From the side each is a soft, low little swell. Pale, poreless skin over the delicate rise. This is the small chest she was teased over — small, soft, and neat."], NOT(GameDataCondition("seen_breasts_miwa_igarashi", True))),
            (["", "{b}Ass{/b}", "Round, full, and firm on her slim dancer's frame. From behind it's a smooth, well-rounded heart, the pale cheeks plump and taut; from the side it projects back in a clean, generous curve with a firm underside. A trim waist runs down into it. Flawless porcelain-pale skin over every rounded plane."], NOT(GameDataCondition("seen_ass_miwa_igarashi", True))),
            (["", "{b}Pussy{/b}", "Between her thighs she keeps a soft, natural bush of brown pubic hair — full and fluffy over the mound, untrimmed and left to grow in a proper triangle. Below it the slit shows the pink tip of the inner lips peeking out. Slim thighs frame it, pale skin all around."], NOT(GameDataCondition("seen_pussy_miwa_igarashi", True))),
            (["", "{b}Personality{/b}", "Cheerful and expressive, with a real love of dancing that doubles as her main outlet for confidence."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "Early on she's self-conscious about her body — specifically her small chest, after Aona Komuro teased her over it — and that conflict is one of her defining early arcs, live and stinging at the low levels. Once it's resolved (around level 3–4) she grows steadily surer in her own skin, using her body and her dancing more and more boldly. Her arc is insecurity turning into self-possession."], NOT(LevelCondition("5+"))),
        ],
    ))
    $ load_person("class_3a", Person("sakura_mori", "Sakura", "Mori", school_char, [
            "• Height: 163.7 cm",
            "In a relationship with Easkey Tanaka.",
            "Vivid red hair with a striking white-blonde section through the front fringe, worn in a high ponytail; dark eyes, fair skin, a slim athletic build with a moderate bust.",
            (["", "{b}Measurements{/b}", "• Bra Size 65C", "• B-W-H: 74-65-88 cm", "• Waist-to-Hips: 0.737"], EventSeenCondition(False, "new_yoga_outfit_9")),
            (["", "{b}Breasts{/b}", "Full and round on her slim frame — a firm, well-shaped handful that sits high and holds its shape, with a soft, rounded underside and a natural gap between them. Her nipples are small and a touch puffy, a soft pale pink on medium, gently domed areolae barely darker than her skin, pointing forward and slightly up. From the side they curve full and firm, projecting out past her slim ribs. Fair, poreless skin over the smooth swell."], NOT(GameDataCondition("seen_breasts_sakura_mori", True))),
            (["", "{b}Ass{/b}", "Round, full, and firm — a well-shaped heart that projects back in a clean, generous curve. From behind the pale cheeks sit high and taut and smooth; from the side it pushes out past her lower back with a firm, rounded underside. A trim athletic waist runs down into it. Flawless fair skin over each full plane."], NOT(GameDataCondition("seen_ass_sakura_mori", True))),
            (["", "{b}Pussy{/b}", "Between her thighs she's smooth and completely clean-shaven — a soft, pale mound with no hair at all. The slit is neat and mostly closed, with just the pink tip of the inner lips peeking out at the base. Over a flat, faintly toned lower belly and framed by slim thighs, the whole of it reads clean and tidy."], NOT(GameDataCondition("seen_pussy_sakura_mori", True))),
            (["", "{b}Personality{/b}", "Diligent, bright, and practical — she pays attention, gives clear well-reasoned answers, and notices the sensible problem everyone else missed. Works hard even when it's uncomfortable and cooperates readily."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "In a steady relationship with Easkey Tanaka, and the more capable, level-headed of the two. Under the calm runs a fierce, burning ambition — she needs to be the best and a loss genuinely gnaws at her, though it's about clearing her own bar, not tearing anyone down. She approaches sex the way she approaches schoolwork: willing, practical, unflustered."], NOT(LevelCondition("5+"))),
        ],
    ))
    $ load_person("class_3a", Person("soyoon_yamamoto", "Soyoon", "Yamamoto", school_char, [
            "• Height: 161.0 cm",
            "Daughter of Yuki Yamamoto.",
            "A sleek jet-black bob with blunt straight bangs, pale blue-grey eyes, and very fair, almost porcelain skin; slender and willowy, long-legged with a moderate bust — one of the more model-like builds in class.",
            (["", "{b}Measurements{/b}", "• Bra Size 60C", "• B-W-H: 68-91-92 cm", "• Waist-to-Hips: 0.664"], EventSeenCondition(False, "new_yoga_outfit_9")),
            (["", "{b}Breasts{/b}", "Full and round on her slender frame — a soft, well-shaped handful sitting fairly high with a natural gap between them. Their standout is the nipples: a vivid pink, puffy and protruding, doming up from soft pink areolae that stand out plainly against her near-white porcelain skin. From the side each curves full and round, the puffy pink tip pushed forward. Flawless, pearl-pale skin over the smooth swell."], NOT(GameDataCondition("seen_breasts_soyoon_yamamoto", True))),
            (["", "{b}Ass{/b}", "Round, full, and firm — a smooth, well-shaped heart that projects back in a clean, generous curve. From behind the pale cheeks sit high and taut; from the side it swells out past her lower back with a firm underside. A slim, willowy waist runs down into it. Poreless, near-white porcelain skin over each full plane."], NOT(GameDataCondition("seen_ass_soyoon_yamamoto", True))),
            (["", "{b}Pussy{/b}", "Between her thighs she's smooth and completely clean-shaven — a soft, pale mound with no hair at all. The cleft parts open to show the inner lips as slim pink folds, a small clit at the top and a glistening pink centre between them — the flush of colour vivid against her near-white porcelain skin. Framed by slim, long thighs over a flat lower belly, the whole of it reads delicate and openly pink."], NOT(GameDataCondition("seen_pussy_soyoon_yamamoto", True))),
            (["", "{b}Personality{/b}", "A haughty, fashionable ice queen — cool, composed, and image-conscious, with a distinct air of looking down her nose at everyone. She keeps most people at arm's length and is hard to fluster or read."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "Where Hatano Miwa's superiority is loud and style-obsessed, Soyoon's is cold and snobbish — quiet condescension, not catty commentary. The chill is partly a front, but she doesn't let it drop easily, or for just anyone; as the campus opens up the poise holds, slipping only rarely and on her own terms."], NOT(LevelCondition("5+"))),
        ],
    ))
    $ load_person("class_3a", Person("yuriko_oshima", "Yuriko", "Oshima", school_char, [
            "• Height: 159.5 cm",
            "In a relationship with Elsie Johnson.",
            "Soft, tousled dark-brown hair in a chin-length wavy bob with side-swept bangs, dark eyes, a small beauty mark under one eye; a slim, petite, softly curved figure with a moderate bust, and a red scarf looped at her neck through every change.",
            (["", "{b}Measurements{/b}", "• Bra Size 65C", "• B-W-H: 72-65-85 cm", "• Waist-to-Hips: 0.768"], EventSeenCondition(False, "new_yoga_outfit_9")),
            (["", "{b}Breasts{/b}", "Small and soft on her petite frame — gently conical, tapering to a soft point and sitting a little apart with a natural, youthful shape. Her nipples are small and a touch protruding, a soft pink on small, close areolae just a shade darker than her fair skin, pointing forward and slightly out. From the side each tapers to a neat point, the little nipple pushed forward. Smooth, pale skin over the modest swell."], NOT(GameDataCondition("seen_breasts_yuriko_oshima", True))),
            (["", "{b}Ass{/b}", "Round, full, and firm on her slim, petite build. From behind it's a smooth, well-rounded heart, the pale cheeks plump and taut; from the side it projects back in a clean, generous curve with a firm underside. A trim waist runs down into it. Flawless, pale skin over each rounded plane."], NOT(GameDataCondition("seen_ass_yuriko_oshima", True))),
            (["", "{b}Pussy{/b}", "Between her thighs she's smooth and completely clean-shaven — a soft, pale mound with no hair at all. The slit is neat and mostly closed, with just the pink tip of the inner lips peeking out at the base. Framed by slim thighs over a flat lower belly, the whole of it reads clean and delicate."], NOT(GameDataCondition("seen_pussy_yuriko_oshima", True))),
            (["", "{b}Personality{/b}", "Mostly a loner — guarded, with a slight depressive, withdrawn streak. Early on she's the reluctant holdout on anything sexual: prickly, easily embarrassed, sure the whole subject is unnecessary."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "Her relationship with Elsie Johnson is her one warm, open anchor; with everyone else she keeps her distance, and there's a real cynical, bitter edge to her — she finds most classmates shallow and says so, dry and sardonic. She thaws slowly: at higher levels she turns casual and matter-of-fact about sex, but flatly, unbothered rather than eager — graphic candour landing in that bored deadpan is the whole effect."], NOT(LevelCondition("5+"))),
        ],
    ))

    $ load_person("parents", Person("adelaide_hall", "Adelaide", "Hall", parent_char, [
            "• Height: 157.8 cm",
            "Works in the cafeteria as Kitchen Mother.",
            "Long glossy black hair in a high ponytail tied with a red-and-white striped ribbon, blunt side-swept bangs; fair freckled skin, pale grey-blue eyes, deep-red lips, a dramatically hourglass figure, and a small silver heart pendant always at her throat.",
            (["", "{b}Measurements{/b}", "• Bra Size 55J", "• B-W-H: 80-60-93 cm", "• Waist-to-Hips: 0.645"], EventSeenCondition(False, "measured_adelaide_hall")),
            (["", "{b}Breasts{/b}", "Big, heavy, and full — a mature, generous bust that hangs with real weight, round and soft, sitting a touch lower on her chest. Deep cleavage between them; from the side they project forward and heavy, the undersides rounded and full. Her nipples are a soft pink-mauve and lightly puffy, set on broad, spread areolae a shade or two deeper than her pale skin — the fuller of the two wide and puffed. Smooth, poreless skin over all of it."], NOT(GameDataCondition("seen_breasts_adelaide_hall", True))),
            (["", "{b}Ass{/b}", "A big, round, heavy ass — full mature cheeks, smooth and plump, projecting in a deep curve out of the small of her back and framed by wide, generous hips. From behind it reads broad and weighty, a clean thigh gap opening beneath; from the side it swells out round over full thighs. Pale, flawless skin catching the light across every soft curve."], NOT(GameDataCondition("seen_ass_adelaide_hall", True))),
            (["", "{b}Pussy{/b}", "She keeps a neat, groomed triangle of dark pubic hair, a small tuft of black curls above the cleft, the mound around it smooth and pale. Below the little patch the slit is closed and tidy, the lips tucked together. Framed by wide hips and the soft inner curves of full thighs, it reads mature and womanly."], NOT(GameDataCondition("seen_pussy_adelaide_hall", True))),
            (["", "{b}Personality{/b}", "Warm and maternal at work — she runs the cafeteria as the school's 'Kitchen Mother,' friendly and helpful in her kitchen."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "At the PTA table she's a socially conservative voice who objects to anything risqué before grudgingly letting it come to a vote. As the campus opens up the maternal warmth stays while her conservatism is worn down slowly, against her first instinct — unfussy and hardworking through all of it."], NOT(LevelCondition("5+"))),
        ],
    ))
    $ load_person("parents", Person("nubia_davis", "Nubia", "Davis", parent_char, [
            "• Height: 169.3 cm",
            "Short choppy white-silver hair with side-swept bangs, tanned bronze skin, blue eyes, small blue gem earrings kept on throughout; tall and curvy-athletic. (One of two tanned characters, alongside nurse Linh Nguyen — but Nubia's hair is short and white where Linh's is a black bob.)",
            (["", "{b}Measurements{/b}", "• Bra Size 75DD (E)", "• B-W-H: 88-68-97 cm", "• Waist-to-Hips: 0.697"], EventSeenCondition(False, "measured_nubia_davis")),
            (["", "{b}Breasts{/b}", "Full and firm on her curvy-athletic frame — big, round breasts that sit high and proud with a taut heaviness, deep cleavage between them. Against her tanned bronze skin the nipples read a soft pink-mauve, puffy and standing proud on light-pink areolae that show up pink against the bronze. From the side they push out full and rounded, firm underneath. Smooth, sun-bronzed skin over the swell."], NOT(GameDataCondition("seen_breasts_nubia_davis", True))),
            (["", "{b}Ass{/b}", "A big, round, gorgeous ass — full and firm, the tanned bronze cheeks smooth and plump, pushing out in a deep proud curve from her toned waist and wide hips. From behind it's a broad, rounded heart in warm bronze; from the side it swells out heavy and shapely over strong thighs. The standout of a tall, curvy-athletic build, catching the light across sun-kissed skin."], NOT(GameDataCondition("seen_ass_nubia_davis", True))),
            (["", "{b}Pussy{/b}", "Not bare — she keeps a small, neat little triangle of dark pubic hair, a trimmed tuft above the cleft, tidy and compact against her bronze skin. The mound around it is smooth, the slit below closed between strong inner thighs. A small, deliberate patch, dark against the tan and easy to spot."], NOT(GameDataCondition("seen_pussy_nubia_davis", True))),
            (["", "{b}Personality{/b}", "A very direct, strong-willed woman with a big personality and a rocker attitude — she says what she thinks without softening it and doesn't back down easily. Short fuse: push her or waste her time and the bluntness turns confrontational fast."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "At the PTA that bluntness cuts through the dithering — she's the one who'll weigh a contested question and then just move it toward a decision rather than let it circle. Her forthright, unshakeable streak stays constant as the campus opens up; she meets whatever comes head-on rather than clutching her pearls."], NOT(LevelCondition("5+"))),
        ],
    ))
    $ load_person("parents", Person("yuki_yamamoto", "Yuki", "Yamamoto", parent_char, [
            "• Height: 170.9 cm",
            "Mother of Soyoon Yamamoto.",
            "Long blue-black hair with a faint blue sheen, worn side-swept with a loose braid, and striking reddish-pink eyes; very fair skin and a slim, elegant hourglass. She shares her daughter Soyoon's black hair and pale colouring in a longer, more mature form.",
            (["", "{b}Measurements{/b}", "• Bra Size 65DD (E)", "• B-W-H: 77-67-94 cm", "• Waist-to-Hips: 0.713"], EventSeenCondition(False, "measured_yuki_yamamoto")),
            (["", "{b}Breasts{/b}", "Full and round on her elegant hourglass — a heavy, well-shaped handful sitting high with a full, rounded underside and deep cleavage. Like her daughter's, her nipples are the standout: a soft pink, puffy and protruding, doming up from pink areolae that stand out against her near-white porcelain skin. From the side each curves full and heavy, projecting forward with the puffy tip pushed proud. Flawless, pearl-pale skin over the smooth swell."], NOT(GameDataCondition("seen_breasts_yuki_yamamoto", True))),
            (["", "{b}Ass{/b}", "Round, full, and firm — a smooth, heavy heart that projects back in a clean, generous curve. From behind the pale cheeks sit full and taut; from the side it swells out well past her narrow waist with a firm, rounded underside. Wide hips carry it below a sharply cinched middle. Poreless, near-white porcelain skin over each full plane."], NOT(GameDataCondition("seen_ass_yuki_yamamoto", True))),
            (["", "{b}Pussy{/b}", "Between her thighs she's smooth and completely clean-shaven — a soft, pale mound with no hair at all. The slit is neat and mostly closed, with just the pink tip of the inner lips peeking out at the base. Framed by long, slim thighs below a flat lower belly, the whole of it reads clean and refined against the pearl-pale skin."], NOT(GameDataCondition("seen_pussy_yuki_yamamoto", True))),
            (["", "{b}Personality{/b}", "A protective, conservative parent — her reflex is that these things belong at home with the parents, and she voices her doubts plainly."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "But she can see the benefits when they're laid out and comes around rather than digging in. As the campus opens up she's persuadable, following rather than resisting once the argument is made."], NOT(LevelCondition("5+"))),
        ],
    ))

    $ load_person("staff", Person("chloe_garcia", "Chloe", "Garcia", teacher_char, [
            "• Height: 168.8 cm",
            "Subjects: Art, Music",
            "Medium-brown hair in a high ponytail with loose framing strands, pale blue eyes, a slim toned figure with defined abs — and heavily tattooed, pointedly on-theme: blackwork forearm sleeves, script and stars across hip and stomach, a musical piece down one leg. Black choker and drop earrings always on.",
            (["", "{b}Measurements{/b}", "• Bra Size 65C", "• B-W-H: 72-61-91 cm", "• Waist-to-Hips: 0.675"], EventSeenCondition(False, "measured_chloe_garcia")),
            (["", "{b}Breasts{/b}", "Small and neat on her slim, toned chest — modest little breasts set wide, the flat toned span of her ribs and stomach on show between and beneath them. The nipples are the feature: each a prominent, protruding nub standing well out from a flat, moderate reddish-pink areola, sticking forward off the small breast. Fair skin, with the edge of her ink — script lettering and small stars — creeping across the upper stomach below."], NOT(GameDataCondition("seen_breasts_chloe_garcia", True))),
            (["", "{b}Ass{/b}", "Firm and compact on her lean frame — a toned bottom that sits high and holds a tight curve, the cheeks smooth and taut over slim thighs. A band of black floral ink, a lotus wreathed in filigree, arcs across her lower back just above the cleft, and more tattoos run down onto the backs of her thighs. Fair, smooth skin wherever the ink leaves it bare."], NOT(GameDataCondition("seen_ass_chloe_garcia", True))),
            (["", "{b}Pussy{/b}", "Smooth and clean-shaven between her lean thighs, the mound bare and neat with a closed, tidy slit at the join. The skin here is fair and unmarked, though tattoos crawl across the hip and down the thigh on either side, framing it in ink. Small, simple, and bare."], NOT(GameDataCondition("seen_pussy_chloe_garcia", True))),
            (["", "{b}Personality{/b}", "Creative, expressive, and quietly rebellious under a careful professional surface — the tattoos and rocker wardrobe are the real Chloe, an artist through and through."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "In front of parents and colleagues her first instinct is decorum and 'what will the community think,' but that caution is a professional reflex, not her true self — she's rarely as scandalised as she lets on. At low levels she plays the propriety card as one of the brakes on anything explicit; as the campus opens up she needs the front less and less, and her unbothered real self comes through fast."], NOT(LevelCondition("5+"))),
        ],
    ))
    $ load_person("staff", Person("emiko_langley", "Emiko", "Langley", secretary_char, [
            "• Height: 180.7 cm",
            "Secretary",
            "Tall and statuesque, very long straight black hair in a high ponytail with a blunt fringe, slim rectangular glasses always on, striking teal-green eyes, fair skin, a full hourglass figure. Two things never leave her at any level: the glasses and tall black riding boots.",
            (["", "{b}Measurements{/b}", "• Bra Size 75F (DDD)", "• B-W-H: 91-66-99 cm", "• Waist-to-Hips: 0.665"], EventSeenCondition(False, "measured_emiko_langley")),
            (["", "{b}Breasts{/b}", "Full, generous, and heavy — the statuesque secretary carries a big, round bust with real weight, sitting proud on her chest, full and heavy and round, with deep cleavage. From the side they swell out full and rounded, the undersides heavy. Her nipples are a warm pink-mauve and prominent, standing out puffy and proud from medium areolae a shade or two darker than her fair skin, tilted slightly up and out. Smooth, flawless skin over the generous swell."], NOT(GameDataCondition("seen_breasts_emiko_langley", True))),
            (["", "{b}Ass{/b}", "The full hourglass pays off from behind — a big, round, gorgeously shaped ass, smooth and plump, projecting in a deep proud curve from her defined waist and wide hips. Long legs run down from it; the cheeks are full and heavy and firm, catching the light across flawless pale skin. From the side it swells out round and generous, the standout of a statuesque, womanly frame."], NOT(GameDataCondition("seen_ass_emiko_langley", True))),
            (["", "{b}Pussy{/b}", "Between her long legs she's smooth and bare, the mound clean and neat with a closed, tidy slit tucked between the tops of her thighs. Not a trace of hair, just smooth pale skin and the clean line of her sex, framed by the wide sweep of her hips. On such a tall, full-figured woman it reads composed and immaculate — the same put-together polish she keeps everywhere else."], NOT(GameDataCondition("seen_pussy_emiko_langley", True))),
            (["", "{b}Personality{/b}", "Warm, teasing, and utterly devoted to the Headmaster — competent and always on top of his schedule, but in private playful, forward, and sexually confident, quick with a caretaking gesture and quicker with a tease."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "His closest ally and confidante, she slips easily between dry professionalism, flirtation, and open devotion. She starts well ahead of the student body (around level 5) and is consistently the most openly, warmly forward figure in his orbit — not someone who has to be brought along, but the one already there."], NOT(LevelCondition("5+"))),
        ],
        paperdollOverrides = [PaperdollOverride(1, {"outfit": "bunny"}, x_override = -0.0014, y_override = -0.026132)],
        paperdollDefaults = {"level": 5},
        thumbnail = "images/characters/emiko_langley/level_5.webp"
    ))
    $ load_person("staff", Person("finola_ryan", "Finola", "Ryan", teacher_char, [
            "• Height: 169.0 cm",
            "Subjects: English, Geography",
            "Short auburn-red hair in a tousled chin-length bob with side-swept bangs, fair freckled skin, blue eyes, pale-blue teardrop earrings always on; an athletic, toned figure that looks younger and sportier than her role suggests (she's only 28). Shares the red hair and freckles with student Easkey Tanaka but wears hers much shorter and is far more toned.",
            (["", "{b}Measurements{/b}", "• Bra Size 65DD (E)", "• B-W-H: 78-65-88 cm", "• Waist-to-Hips: 0.745"], EventSeenCondition(False, "measured_finola_ryan")),
            (["", "{b}Breasts{/b}", "A moderate-full, round handful with a natural soft fullness and a modest gap between them. Her nipples protrude prominently — warm pink puffy nubs pushed forward and pointing slightly down, on medium areolae a touch darker than her fair skin. What sets them apart is the freckling — the same light scatter that dusts her face carries down over her chest and the upper swell, faint across the pale skin."], NOT(GameDataCondition("seen_breasts_finola_ryan", True))),
            (["", "{b}Ass{/b}", "Round, firm, and athletic — a toned bottom that sits high and holds its shape, the cheeks tight and full, projecting in a clean curve over strong thighs. Freckles carry down over the small of her back and dust across the cheeks. From behind it reads compact and lifted, the trained backside of a woman who keeps fit; from the side it rounds out firm and taut."], NOT(GameDataCondition("seen_ass_finola_ryan", True))),
            (["", "{b}Pussy{/b}", "Smooth and bare between her thighs, the mound clean-shaven and neat over the flat plane of a toned, faintly defined lower belly. The slit is closed and tidy, a simple clean cleft framed by firm inner thighs. On her athletic, hard-trained frame it reads trim and unfussy — no hair, nothing extra, just smooth pale skin and the neat line of her sex."], NOT(GameDataCondition("seen_pussy_finola_ryan", True))),
            (["", "{b}Personality{/b}", "Dutiful, methodical, and conscientious — she takes her teaching seriously and does things properly. A touch reserved and easily embarrassed, but fundamentally honest; she won't lie even when the truthful answer costs her composure."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "At low levels she's prim and proper and blushes at the subject, but answers straight when pressed. As the campus opens up the primness erodes while the diligence stays — she'll participate and demonstrate because it's her job and she's thorough about it, the reserve giving way to a matter-of-fact, almost clinical thoroughness."], NOT(LevelCondition("5+"))),
        ],
    ))
    $ load_person("staff", Person("lily_anderson", "Lily", "Anderson", teacher_char, [
            "• Height: 167.0 cm",
            "Subjects: Math, Sciences",
            "Long soft auburn hair, wavy and centre-parted past her shoulders, blue eyes, fair skin (no freckles), a slim figure with a moderate bust. Of the several staff redheads she's the one with the longest, softest waves — distinct from Finola Ryan's short freckled bob.",
            (["", "{b}Measurements{/b}", "• Bra Size 70B", "• B-W-H: 76-64-90 cm", "• Waist-to-Hips: 0.705"], EventSeenCondition(False, "measured_lily_anderson")),
            (["", "{b}Breasts{/b}", "A medium, round handful on her slim frame — full and natural, set a little wide with a soft gap between them, sitting fairly high with a full, rounded underside. Their standout is the nipples: they protrude prominently, pointed nubs pushed well forward from soft, faintly puffy pale-pink areolae of medium size. From the side they curve full and round, the nipple standing proud. Fair, clear skin over the soft swell."], NOT(GameDataCondition("seen_breasts_lily_anderson", True))),
            (["", "{b}Ass{/b}", "Round, full, and firm for her slim build. From behind it's a neat heart — smooth pale cheeks, full and well-shaped, sitting high and taut; from the side it projects back in a clean, rounded curve with a firm lower swell. A slim waist runs down into it, a small gap opening at the top of her thighs. Flawless pale skin over every rounded plane."], NOT(GameDataCondition("seen_ass_lily_anderson", True))),
            (["", "{b}Pussy{/b}", "Between her thighs she's smooth and completely clean-shaven — a soft, pale mound with no hair at all. The slit is neat and mostly closed, tidy and simple, with just the tip of the inner lips peeking out at the base of the cleft. Over a flat lower belly and framed by slim thighs, the whole of it reads clean and delicate."], NOT(GameDataCondition("seen_pussy_lily_anderson", True))),
            (["", "{b}Personality{/b}", "Conscientious, anxious, and overworked — she grades past midnight, runs herself toward burnout, and worries. Her instinct on sex ed is a conservative 'won't this just make them worse?' She cares deeply about her students and carries it heavily."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "The composed professional register is distinct from how frayed she is underneath; stretched too thin, the composure cracks into snappishness and a quiet bitterness — a sense that nobody sees how much she carries — before she catches herself. As the campus opens up she's pulled along anxiously rather than eagerly, still fretting over consequences the others have stopped noticing."], NOT(LevelCondition("5+"))),
        ],
    ))
    $ load_person("staff", Person("yulan_chen", "Yulan", "Chen", teacher_char, [
            "• Height: 167.0 cm",
            "Subjects: History, Politics",
            "Long black hair with a faint blue sheen, side-swept with a braid and dressed with a blue floral ornament and tassel pins; pale blue-grey eyes, fair skin, an elegant mature hourglass. Her whole wardrobe is the qipao (cheongsam).",
            (["", "{b}Measurements{/b}", "• Bra Size 65F (DDD)", "• B-W-H: 81-67-90 cm", "• Waist-to-Hips: 0.751"], EventSeenCondition(False, "measured_yulan_chen")),
            (["", "{b}Breasts{/b}", "Full and round on her elegant hourglass — a heavy, well-shaped handful sitting high with a full, rounded underside and a natural gap between them. Their standout is the nipples: prominent and protruding, a warm rosy pink pushed well forward as pointed nubs on medium rosy-pink areolae. From the side each curves full and firm, projecting forward with the nipple standing proud. Smooth, warm-fair skin over the swell."], NOT(GameDataCondition("seen_breasts_yulan_chen", True))),
            (["", "{b}Ass{/b}", "Round, full, and firm — a smooth, well-shaped heart that projects back in a clean, generous curve. From behind the cheeks sit full and taut; from the side it swells out past her slim waist with a firm, rounded underside. Slim, elegant hips carry it below a cinched middle. Warm, poreless fair skin over each full plane."], NOT(GameDataCondition("seen_ass_yulan_chen", True))),
            (["", "{b}Pussy{/b}", "Between her thighs she keeps a small, neat triangle of dark pubic hair — a defined natural tuft high on an otherwise smooth mound. Below it the slit is close and neat, with just the pink tip of the inner lips peeking out at the base. Slim thighs frame it, warm-fair skin all around."], NOT(GameDataCondition("seen_pussy_yulan_chen", True))),
            (["", "{b}Personality{/b}", "Precise, guarded, and rule-minded — she asks the procedural question everyone else skips (is attendance mandatory? how do we handle the backlash?), respects hard evidence and competence, and keeps her distance until someone earns it."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "She thaws slowly, and only to demonstrated competence; as the campus opens up her guard comes down by degrees, on her own terms rather than the crowd's."], NOT(LevelCondition("5+"))),
        ],
    ))
    $ load_person("staff", Person("zoe_parker", "Zoe", "Parker", teacher_char, [
            "• Height: 167.3 cm",
            "Subjects: Physical Education, Health",
            "Short choppy blonde hair with side-swept bangs, blue eyes, freckles across nose and cheeks; a fit, athletic figure, and a large black tattoo across her stomach — a butterfly wreathed in baroque filigree.",
            (["", "{b}Measurements{/b}", "• Bra Size 65C", "• B-W-H: 73-63-91 cm", "• Waist-to-Hips: 0.692"], EventSeenCondition(False, "measured_zoe_parker")),
            (["", "{b}Breasts{/b}", "Firm and moderate on her athletic frame — neat, conical, and upturned, tapering forward to a point. The standout is the nipples: prominent, puffy, and protruding, sticking well out as soft pink cones from medium pinkish areolae. From the side each juts up firm and pointed, the puffy nipple pushed proud. High on her left chest a small inked script reads 'Dirty Girl,' and below her breasts begins the black butterfly-and-filigree piece that sweeps down her stomach. Smooth, lightly-tanned skin over the taut swell."], NOT(GameDataCondition("seen_breasts_zoe_parker", True))),
            (["", "{b}Ass{/b}", "Round, full, and firm on her toned, athletic build. From behind it's a smooth, well-rounded heart over a defined, muscled back; from the side it projects back in a clean, generous curve with a tight, firm underside. Curvy hips carry it below a trim waist. Warm, lightly-tanned skin over each taut plane."], NOT(GameDataCondition("seen_ass_zoe_parker", True))),
            (["", "{b}Pussy{/b}", "Between her thighs she keeps a narrow landing-strip of dark-blonde pubic hair — a neat vertical stripe on the upper mound, otherwise smooth. Below it the outer lips are full and plump, a soft pad to either side pressed together into a clean, closed cleft, the inner lips tucked away and showing only as a thin pink seam down the centre. Slim, athletic thighs frame it, warm-fair skin all around."], NOT(GameDataCondition("seen_pussy_zoe_parker", True))),
            (["", "{b}Personality{/b}", "The conscience of the staff — caring, protective, and safety-first with her students; she'll push back on the Headmaster directly when she thinks he's gone too far. Professional and proactive."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "She runs her PE and yoga classes with real duty of care and solves problems by reaching out — she's the one who brought in her nurse friend Linh Nguyen for the students' checkups, arranged for free. Her protective instinct is the constant: as the campus opens up she's the staff member most likely to keep worrying about the girls' wellbeing even as the culture around her stops."], NOT(LevelCondition("5+"))),
        ],
    ))
    $ load_person("staff", Person("linh_nguyen", "Linh", "Nguyen", teacher_char, [
            "• Height: 165.6 cm",
            "Nurse at the hospital in the city.",
            "Tanned, olive skin — one of only two sun-kissed characters (the other being parent Nubia Davis) — with a short blue-black bob, side-swept bangs, warm amber-brown eyes, freckles across nose and cheeks, and red tasselled earrings kept on throughout. Slim and athletic with a smaller bust and curvy hips.",
            (["", "{b}Measurements{/b}", "• Bra Size 60C", "• B-W-H: 68-70-95 cm", "• Waist-to-Hips: 0.738"], EventSeenCondition(False, "measured_linh_nguyen")),
            (["", "{b}Breasts{/b}", "On the small side — modest, firm little breasts that sit high and hold a soft round shape, barely more than a handful. Against her tanned, olive skin the nipples stand out: small but prominently protruding, sticking well out as warm brown-mauve nubs from neat, compact areolae a shade darker than the surrounding tan. Smooth, sun-kissed skin over the gentle swell."], NOT(GameDataCondition("seen_breasts_linh_nguyen", True))),
            (["", "{b}Ass{/b}", "Round and full on her slim frame — a firm, shapely bottom that sits high and pushes out in a clean bubble curve, the tanned cheeks smooth and taut over toned thighs. Her waist stays trim while her hips flare soft and curvy into it. From behind it's a neat, lifted heart in warm olive skin; from the side it rounds out full and firm."], NOT(GameDataCondition("seen_ass_linh_nguyen", True))),
            (["", "{b}Pussy{/b}", "Smooth and clean-shaven between her thighs, the tanned mound bare and neat with a closed, tidy slit tucked between firm inner thighs. On her slim, athletic frame and warm olive skin it reads trim and unfussy — no hair, the same sun-kissed tone all the way down, just the clean line of her sex."], NOT(GameDataCondition("seen_pussy_linh_nguyen", True))),
            (["", "{b}Personality{/b}", "Often grumpy and short-spoken, but with a heart of gold — quite shy and not one for social niceties. What she lacks in people skills she more than makes up for in sheer sense of duty."], NOT(LevelCondition("3+"))),
            (["", "{b}Under the surface{/b}", "She gives her absolute all treating her patients and steps up without fuss when needed — she's the one who comes in to run the students' health checkups, doing the first round for free. A nurse at the city hospital and a friend of Zoe Parker; if there's one person you can truly trust, it's her."], NOT(LevelCondition("5+"))),
        ],
    ))

    return