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
            self.level = {
                school: Stat("level", 0),
                parent: Stat("level", 0),
                teacher: Stat("level", 0),
                secretary: Stat("level", 0),
            }
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

            if not hasattr(self, 'level') or not isinstance(self.level, dict):
                self.level = {
                    school: Stat("level", 0),
                    parent: Stat("level", 0),
                    teacher: Stat("level", 0),
                    secretary: Stat("level", 0),
                }
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

        def get_level(self, key: str) -> int:
            """
            Returns the level of the character

            ### Returns:
            1. int
                - The level of the character
            """

            if key not in self.level.keys():
                return -1

            return self.level[key].get_value()

        def get_level_str(self, key: str) -> str:
            """
            Returns the level of the character as a string

            ### Returns:
            1. str
                - The level of the character as a string
            """

            return str(self.get_level(key))

        def get_level_obj(self, key: str) -> Stat:
            """
            Returns the level object of the character

            ### Returns:
            1. Stat
                - The level object of the character
            """

            if key not in self.level.keys():
                return None

            return self.level[key]

        def set_level(self, key: str, level: int):
            """
            Sets the level of the character

            ### Parameters:
            1. level: int
                - The level to set the character to
            """

            if is_in_replay:
                return

            if key not in self.level.keys():
                return

            level = clamp_value(level, 0, 10)
            self.level[key].set_value(level)

        def get_nearest_level_delta(self, key: str, level: int) -> int:
            """
            Returns the difference between level and the level of the current character

            ### Parameters:
            1. level: int
                - The level to check against

            ### Returns:
            1. int
                - The difference between level and the level of the current character
            """

            if key not in self.level.keys():
                return -1000

            for i in range(self.get_level(), 11):
                if self.check_level(level, i):
                    return self.get_level(key) - i

        def check_level(self, key: str, value: num | str, test_level: int = None) -> bool:
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

            if key not in self.level.keys():
                return False

            if value == "x":
                return True

            if test_level == None:
                test_level = self.get_level(key)

            return get_value_diff(value, test_level) >= 0
    #################

    ######################
    # General Char Handler

    def get_character() -> Char:
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

        global chara

        return chara

    def get_character_stat(stat: str) -> num:
        if stat == MONEY:
            return money.get_value()
        else:
            return get_character().get_stat_number(stat)

    def display_character_stat(stat: str) -> str:
        if stat == MONEY:
            return money.display_stat()
        else:
            return get_character().display_stat(stat)

    def get_character_stat_value(stat: str) -> str:
        if stat == MONEY:
            return re.sub("\..+", "", money.get_display_value())
        else:
            return get_character().get_display_value(stat)

    def get_character_stat_change(stat: str) -> str:
        if stat == MONEY:
            return money.get_display_change()
        else:
            return get_character().get_display_change(stat)

    def get_character_stat_obj(stat: str) -> Stat:
        if stat == MONEY:
            return money
        else:
            return get_character().get_stat_obj(stat)

    def set_character_stat(stat: str, value: num):
        if stat == MONEY:
            money.set_value(value)
        else:
            get_character().set_stat(stat, value)

    def change_character_stat(stat: str, delta: num):
        if stat == MONEY:
            money.change_value(delta)
        else:
            get_character().change_stat(stat, delta)

    def reset_character_stats():
        money.reset_change()
        get_character().reset_changed_stats()

    def get_character_level(key: str) -> int:
        return get_character().get_level(key)

    def set_character_level(key: str, level: int):
        get_character().set_level(key, level)

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

    #####################
    # Char Object Handler

    def load_character(name: str, title: str, start_data: Dict[str, Any], runtime_data: Dict[str, Any] = None):
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

        global chara

        if chara == None:
            chara = Char(name, title)
            chara.__dict__.update(start_data)

        chara._update(runtime_data)

    def update_character(data: Dict[str, Any]):
        """
        Updates the character with the data

        ### Parameters:
        1. char: str | Char
            - The name of the character or the character itself to update
            - If there is no character in map with the name, -1 is returned
        2. data: Dict[str, Any]
            - The data to update the character with
        """

        global chara

        chara._update(data)

label load_schools ():
    # """
    # Loads and updates all the Character-Objects for the game
    # """
    
    #############################################
    # compatibility with version 0.1.2
    $ fix_schools()

    if charList != None and "school" in charList.keys():
        $ chara = charList["school"]
        $ merge_charas()
        $ charList = None
    else:
        $ load_character("school", "School", {
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

init -99 python:
    def merge_charas():
        global chara

        if charList == None:
            return

        if "staff" in charList.keys():
            if "teacher" in charList["staff"].keys():
                chara.set_level("teacher", charList["staff"]["teacher"].get_level())
            if "secretary" in charList["staff"].keys():
                chara.set_level("secretary", charList["staff"]["secretary"].get_level())
        if "parent" in charList.keys():
            chara.set_level("parent", charList["parent"].get_level())
