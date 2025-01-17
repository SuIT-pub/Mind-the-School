init -6 python:
    import re

    ########################
    # region CLASSES ----- #
    ########################

    class Building(Journal_Obj):
        """
        A subclass of Journal_Obj.
        A class that represents a building in the game.

        ### Attributes:
        1. _level: int
            - The current upgrade level of the building.
            - 0 is building is not yet unlocked.
        2. _max_level: int
            - The maximum upgrade level of the building.
        3. _upgrade_conditions: List[ConditionStorage]
            - A list of ConditionStorage objects that represent the conditions for upgrading the building.
            - Each ConditionStorage represents the upgrade condition for a specific level.
        4. _blocked: bool
            - A boolean that represents if the building is blocked or not.
            - A blocked building can not be accessed.

        ### Methods:
        1. get_type() -> str
            - Returns the type of the object.
            - In this case "building".
        2. get_description(level: int = -1) -> List[str]
            - Returns the description of the building.
            - If level is -1, the description of the current level is returned.
            - If level is not -1, the description of the specified level is returned.
        3. get_description_str(level: int = -1) -> str
            - Returns the description of the building as a string.
            - If level is -1, the description of the current level is returned.
            - If level is not -1, the description of the specified level is returned.
        4. get_image(_school = "x", _level = -1) -> str
            - Returns the image path of the building for the image used in the journal.
        5. get_full_image(_school = "x", _level = -1) -> str
            - Returns the image path of the building for the image used in the journal.
            - If the full image does not exist, None is returned.
        6. get_level() -> int
            - Returns the current upgrade level of the building.
        7. get_max_level() -> int
            - Returns the maximum upgrade level of the building.
        8. set_level(level: int)
            - Sets the current upgrade level of the building to the specified level.
        9. set_max_level(level: int)
            - Sets the maximum upgrade level of the building to the specified level.
        10. is_available() -> bool
            - Returns True if the building is unlocked and not blocked.
        11. set_blocked(is_blocked: bool = True)
            - Sets the blocked status of the building to the specified value.
        12. unlock(unlock: bool = True)
            - Sets the current upgrade level of the building to 1 if unlock is True, else to 0.
        13. is_unlocked(_school) -> bool
            - Returns True if the building is unlocked.
        14. is_blocked() -> bool
            - Returns True if the building is blocked.
        15. can_be_upgraded(**kwargs) -> bool
            - Returns True if the building can be upgraded.
            - The conditions for upgrading the building are checked.
        16. has_higher_level() -> bool
            - Returns True if the building has a higher upgrade level than the one the building is currently at.
        17. get_upgrade_conditions(level: int) -> ConditionStorage
            - Returns the ConditionStorage object that represents the conditions for upgrading the building to the specified level.
            - If the specified level is not valid, None is returned.
        18. get_list_conditions(cond_type: str = UNLOCK, level: int = -1) -> List[Condition]
            - Returns a list of Condition objects that represent the conditions for unlocking or upgrading the building.
            - If level is -1, the conditions for the current level are returned.
            - If level is not -1, the conditions for the specified level are returned.
        19. get_list_conditions_list(cond_type: str = UNLOCK, level: int = -1, **kwargs) -> List[Tuple[str, str]]
            - Returns a list of tuples that represent the conditions for unlocking or upgrading the building.
            - If level is -1, the conditions for the current level are returned.
            - If level is not -1, the conditions for the specified level are returned.
            - The tuples are in the form (condition icon, condition value).
        20. get_desc_conditions(cond_type: str = UNLOCK, level: int = -1) -> List[Condition]
            - Returns a list of Condition objects that represent the conditions for unlocking or upgrading the building.
            - If level is -1, the conditions for the current level are returned.
            - If level is not -1, the conditions for the specified level are returned.
            - The conditions are sorted by their description.
        21. get_desc_conditions_desc(cond_type: str = UNLOCK, level: int = -1, **kwargs) -> List[str]
            - Returns a list of strings that represent the conditions for unlocking or upgrading the building.
            - If level is -1, the conditions for the current level are returned.
            - If level is not -1, the conditions for the specified level are returned.
            - The conditions are sorted by their description.
        """

        def __init__(self, name: str, title: str):
            super().__init__(name, title)
            self._level = 0
            self._max_level = 1
            self._upgrade_conditions = []
            self._blocked = False
            self._construction_time = 0
            self._upgrade_effects = {}

        def _update(self, title: str, data: Dict[str, Any] = None):
            super()._update(title, data)
            if data != None:
                self.__dict__.update(data)
                
            if not hasattr(self, '_level'):
                self._level = 0
            if not hasattr(self, '_max_level'):
                self._max_level = 1
            if not hasattr(self, '_upgrade_conditions'):
                self._upgrade_conditions = []
            if not hasattr(self, '_blocked'):
                self._blocked = False
            if not hasattr(self, '_construction_time'):
                self._construction_time = 0
            if not hasattr(self, '_upgrade_effects'):
                self._upgrade_effects = {}
        
        def is_valid(self):
            """
            Checks if the building is valid.
            """

            super().is_valid()

            if self._construction_time < 0:
                log_error(410, f"|Building:{self.get_name()}|Construction time has to be 0 or positive.")

        def get_type(self) -> str:
            """
            Returns the type of the object.

            ### Returns:
            1. str
                - The type of the object.
                - In this case "building".
            """

            return "building"

        def get_description(self, level: int = -1) -> List[str]:
            """
            Returns the description of the building.

            ### Parameters:
            1. level: int = -1
                - The level of the building for which the description should be returned.
                - If level is -1, the description of the current level is returned.
                - If level is not -1, the description of the specified level is returned.

            ### Returns:
            1. List[str]
                - The description of the building.
            """

            if level == -1:
                level = self._level
            if level < 0 or level >= len(self._description):
                return ""
            return self._description[level]

        def get_description_str(self, level: int = -1) -> str:
            """
            Returns the description of the building as a string.

            ### Parameters:
            1. level: int = -1
                - The level of the building for which the description should be returned.
                - If level is -1, the description of the current level is returned.
                - If level is not -1, the description of the specified level is returned.

            ### Returns:
            1. str
                - The description of the building as a string joined together with an empty row.
            """

            return "\n\n".join(self.get_description(level))

        def get_level(self) -> int:
            """
            Returns the current upgrade level of the building.

            ### Returns:
            1. int
                - The current upgrade level of the building.
            """

            return self._level

        def get_max_level(self) -> int:
            """
            Returns the maximum upgrade level of the building.

            ### Returns:
            1. int
                - The maximum upgrade level of the building.
            """

            return self._max_level

        def set_level(self, level: int):
            """
            Sets the current upgrade level of the building to the specified level.

            ### Parameters:
            1. level: int
                - The level to which the current upgrade level of the building should be set to.
            """

            if level < 0:
                level = 0
            if level > self._max_level:
                level = self._max_level

            self._level = level

        def set_max_level(self, level: int):
            """
            Sets the maximum upgrade level of the building to the specified level.

            ### Parameters:
            1. level: int
                - The level to which the maximum upgrade level of the building should be set to.
            """

            self._max_level = level

        def is_available(self) -> bool:
            """
            Returns True if the building is unlocked and not blocked.

            ### Returns:
            1. bool
                - True if the building is unlocked and not blocked.
            """

            return self.is_unlocked() and not self.is_blocked()

        def set_blocked(self, is_blocked: bool = True):
            """
            Sets the blocked status of the building to the specified value.
            A blocked building can not be accessed by the player.

            ### Parameters:
            1. is_blocked: bool = True
                - The value to which the blocked status of the building should be set to.
            """

            self._blocked = is_blocked

        def unlock(self, unlock: bool = True, apply_effects: bool = False):
            """
            Sets the current upgrade level of the building to 1 if unlock is True, else to 0.

            ### Parameters:
            1. unlock: bool = True
                - If True, the current upgrade level of the building is set to 1.
                - If False, the current upgrade level of the building is set to 0.
            """

            if unlock:
                advance_progress("unlock_" + self.get_name())
                new_time = Time(time.day_to_string())
                new_time.add_time(day = self._construction_time)
                set_game_data(self.get_name() + "_construction_end", new_time.day_to_string())
                self._level = 1
            else:
                self._level = 0

            if unlock and apply_effects:
                self.apply_effects()

            update_quest("journal_unlock", name = self._name, type = self.get_type())

        def upgrade(self, apply_effects: bool = False):
            """
            Upgrades the building to the next level.

            ### Parameters:
            1. apply_effects: bool = False
                - If True, the effects of the upgrade are applied.
            """

            if self._level < self._max_level:
                self._level += 1

            advance_progress("unlock_" + self.get_name())
            new_time = Time(time.day_to_string())
            new_time.add_time(day = self._construction_time)
            set_game_data(self.get_name() + "_construction_end", new_time.day_to_string())

            if apply_effects:
                self.apply_upgrade_effects()

            update_quest("journal_upgrade", name = self._name, type = self.get_type(), old_level = self._level - 1, new_level = self._level)

        def apply_upgrade_effects(self, level: int = -1):
            """
            Applies the effects of the upgrade.

            ### Parameters:
            1. level: int = -1
                - The level to which the effects should be applied.
                - If level is -1, the effects for the current level are applied.
            """

            if level == -1:
                level = self._level

            if level in self._upgrade_effects.keys():
                for effect in self._upgrade_effects[level]:
                    effect.apply()

        def is_unlocked(self) -> bool:
            """
            Returns True if the building is unlocked.

            ### Returns:
            1. bool
                - True if the building is unlocked.
            """

            return self._level != 0

        def is_blocked(self) -> bool:
            """
            Returns True if the building is blocked.

            ### Returns:
            1. bool
                - True if the building is blocked.
            """

            return self._blocked

        def can_be_upgraded(self, **kwargs) -> bool:
            """
            Returns True if the building can be upgraded.
            The conditions for upgrading the building are checked.

            ### Parameters:
            1. **kwargs
                - The values for the variables used in the conditions.

            ### Returns:
            1. bool
                - True if the building can be upgraded.
            """

            conditions = self.get_upgrade_conditions(self._level)
            return conditions != None and conditions.is_fulfilled(**kwargs)

        def has_higher_level(self) -> bool:
            """
            Returns True if the building has a higher upgrade level than the one the building is currently at.

            ### Returns:
            1. bool
                - True if the building has a higher upgrade level than the one the building is currently at.
            """

            return self._level < self._max_level

        def get_upgrade_conditions(self, level: int) -> ConditionStorage:
            """
            Returns the ConditionStorage object that represents the conditions for upgrading the building to the specified level.

            ### Parameters:
            1. level: int
                - The level for which the conditions should be returned.

            ### Returns:
            1. ConditionStorage
                - The ConditionStorage object that represents the conditions for upgrading the building to the specified level.
                - If the specified level is not valid, None is returned.
            """

            if level > len(self._upgrade_conditions) or level <= 0:
                return None
            return self._upgrade_conditions[level - 1]
        
        def get_list_conditions(self, cond_type: str = UNLOCK, level: int = -1) -> List[Condition]:
            """
            Returns a list of Condition objects that represent the conditions for unlocking or upgrading the building.
            If level is -1, the conditions for the current level are returned.

            ### Parameters:
            1. cond_type: str = UNLOCK
                - The type of conditions that should be returned.
                - If cond_type is UNLOCK, the conditions for unlocking the building are returned.
                - If cond_type is UPGRADE, the conditions for upgrading the building are returned.
            2. level: int = -1
                - The level for which the conditions should be returned.
                - If level is -1, the conditions for the current level are returned.
                - only needed if cond_type is UPGRADE.

            ### Returns:
            1. List[Condition]
                - A list of Condition objects that represent the conditions for unlocking or upgrading the building.
            """

            if level == -1:
                level = self._level

            if cond_type == UNLOCK:
                return self._unlock_conditions.get_list_conditions()
            if cond_type == UPGRADE:
                upgrade_conditions = self.get_upgrade_conditions(level)
                if upgrade_conditions == None:
                    return []
                else:
                    return self.get_upgrade_conditions(level).get_list_conditions()
        
        def get_list_conditions_list(self, cond_type: str = UNLOCK, level: int = -1, **kwargs) -> List[Tuple[str, str]]:
            """
            Returns a list of tuples that represent the conditions for unlocking or upgrading the building.
            If level is -1, the conditions for the current level are returned.

            ### Parameters:
            1. cond_type: str = UNLOCK
                - The type of conditions that should be returned.
                - If cond_type is UNLOCK, the conditions for unlocking the building are returned.
                - If cond_type is UPGRADE, the conditions for upgrading the building are returned.
            2. level: int = -1
                - The level for which the conditions should be returned.
                - If level is -1, the conditions for the current level are returned.
                - only needed if cond_type is UPGRADE.

            ### Returns:
            1. List[Tuple[str, str]]
                - A list of tuples that represent the conditions for unlocking or upgrading the building.
                - The tuples are in the form (condition icon, condition value).
            """

            if level == -1:
                level = self._level

            if cond_type == UNLOCK:
                return self._unlock_conditions.get_list_conditions_list(**kwargs)
            if cond_type == UPGRADE:
                upgrade_conditions = self.get_upgrade_conditions(level)
                if upgrade_conditions == None:
                    return []
                else:
                    return self.get_upgrade_conditions(level).get_list_conditions_list(**kwargs)

        def get_desc_conditions(self, cond_type: str = UNLOCK, level: int = -1) -> List[Condition]:
            """
            Returns a list of Condition objects that represent the conditions for unlocking or upgrading the building.
            If level is -1, the conditions for the current level are returned.

            ### Parameters:
            1. cond_type: str = UNLOCK
                - The type of conditions that should be returned.
                - If cond_type is UNLOCK, the conditions for unlocking the building are returned.
                - If cond_type is UPGRADE, the conditions for upgrading the building are returned.
            2. level: int = -1
                - The level for which the conditions should be returned.
                - If level is -1, the conditions for the current level are returned.
                - only needed if cond_type is UPGRADE.

            ### Returns:
            1. List[Condition]
                - A list of Condition objects that represent the conditions for unlocking or upgrading the building.
                - The conditions are sorted by their description.
            """

            if level == -1:
                level = self._level

            if cond_type == UNLOCK:
                return self._unlock_conditions.get_desc_conditions()
            if cond_type == UPGRADE:
                upgrade_conditions = self.get_upgrade_conditions(level)
                if upgrade_conditions == None:
                    return []
                else:
                    return self.get_upgrade_conditions(level).get_desc_conditions()

        def get_desc_conditions_desc(self, cond_type: str = UNLOCK, level: int = -1, **kwargs) -> List[str]:
            """
            Returns a list of strings that represent the conditions for unlocking or upgrading the building.
            If level is -1, the conditions for the current level are returned.

            ### Parameters:
            1. cond_type: str = UNLOCK
                - The type of conditions that should be returned.
                - If cond_type is UNLOCK, the conditions for unlocking the building are returned.
                - If cond_type is UPGRADE, the conditions for upgrading the building are returned.
            2. level: int = -1
                - The level for which the conditions should be returned.
                - If level is -1, the conditions for the current level are returned.
                - only needed if cond_type is UPGRADE.

            ### Returns:
            1. List[str]
                - A list of strings that represent the conditions for unlocking or upgrading the building.
                - The conditions are sorted by their description.
            """

            if level == -1:
                level = self._level

            if cond_type == UNLOCK:
                return self._unlock_conditions.get_desc_conditions_desc(**kwargs)
            if cond_type == UPGRADE:
                upgrade_conditions = self.get_upgrade_conditions(level)
                if upgrade_conditions == None:
                    return []
                else:
                    return self.get_upgrade_conditions(level).get_desc_conditions_desc(**kwargs)

    # endregion
    ########################

    #########################################
    # region Buildings Global Methods ----- #
    #########################################

    ##################
    # Building Handler

    def get_building(building: str) -> Building:
        """
        Returns the Building object with the specified name.
        
        ### Parameters:
        1. building: str
            - The name of the building that should be returned.

        ### Returns:
        1. Building
            - The Building object with the specified name.
            - If no Building object with the specified name exists, None is returned.
        """

        if building in buildings.keys():
            return buildings[building]
        return None

    def get_location_title(key: str) -> str:
        """
        Gets the title of a location

        ### Parameters:
        1. key: str
            - The key of the location

        ### Returns:
        1. str
            - The title of the location
            - If the location does not exist the key is returned
        """

        building = get_building(key)
        if building == None:
            return key
        return building.get_title()

    ########################
    # Building block handler

    def set_building_blocked(building_name: str, is_blocked: bool = True):
        """
        Sets the blocked status of the building with the specified name to the specified value.

        ### Parameters:
        1. building_name: str
            - The name of the building that should be updated.
        2. is_blocked: bool = True
            - The value to which the blocked status of the building should be set to.
        """

        if not is_in_replay and building_name in buildings.keys():
            buildings[building_name].set_blocked(is_blocked)

    def set_all_buildings_blocked(is_blocked: bool = True):
        """
        Sets the blocked status of all buildings to the specified value.

        ### Parameters:
        1. is_blocked: bool = True
            - The value to which the blocked status of the buildings should be set to.
        """

        if is_in_replay:
            return

        for building in buildings.values():
            building.set_blocked(is_blocked)

    ############################
    # Building visibility getter

    def count_locked_buildings() -> int:
        """
        Returns the number of locked buildings.

        ### Returns:
        1. int
            - The number of locked buildings.
        """

        output = 0

        for building in buildings.values():
            if not building.is_unlocked():
                output += 1

        return output

    def get_unlocked_buildings() -> List[str]:
        """
        Returns a list of the names of all unlocked buildings.

        ### Returns:
        1. List[str]
            - A list of the names of all unlocked buildings.
        """

        output = []

        for building in buildings.values():
            if building.is_unlocked() and building.get_name() not in output:
                output.append(building.get_name())

        return output
    
    def is_building_unlocked(building_name: str) -> bool:
        """
        Returns True if the building with the specified name is unlocked.

        ### Parameters:
        1. building_name: str
            - The name of the building that should be checked.

        ### Returns:
        1. bool
            - True if the building with the specified name is unlocked.
        """

        if building_name not in buildings.keys():
            return False
        return buildings[building_name].is_unlocked()

    def is_building_visible(building_name: str) -> bool:
        """
        Returns True if the building with the specified name is visible.
        A building is visible when there is no blocking condition or all blocking conditions are fulfilled.

        ### Parameters:
        1. building_name: str
            - The name of the building that should be checked.
        """

        if building_name not in buildings.keys():
            return False
        return buildings[building_name].is_visible()

    ###############################
    # Building availability handler

    def is_building_available(building_name: str) -> bool:
        """
        Returns True if the building with the specified name is unlocked and not blocked.

        ### Parameters:
        1. building_name: str
            - The name of the building that should be checked.

        ### Returns:
        1. bool
            - True if the building with the specified name is unlocked and not blocked.
        """

        if building_name not in buildings.keys():
            return False
        return buildings[building_name].is_available()

    #########################
    # Building Object Handler

    def load_building(name: str, title: str, runtime_data: Dict[str, Any] = None, starting_data: Dict[str, Any] = None):
        """
        Loads or updates a building with the specified name, title and data.

        ### Parameters:
        1. name: str
            - The name of the building that should be loaded or updated.
        2. title: str
            - The title of the building that should be loaded or updated.
        3. runtime_data: Dict[str, Any] (Default None)
            - The data that should be used to update the building.
            - runtime_data contains data that can be changed in the building during runtime without loosing essential data
        4. starting_data: Dict[str, Any] (Default None)
            - The data that should be used to update the building.
            - starting_data contains data that should not be changed in the building during runtime.
        """

        if not is_mod_active(active_mod_key):
            return

        if name not in buildings.keys():
            buildings[name] = Building(name, title)
            buildings[name]._update(title, starting_data)

        buildings[name]._update(title, runtime_data)

        buildings[name].is_valid()

    def remove_building(name: str):
        """
        Removes the building with the specified name.

        ### Parameters:
        1. name: str
            - The name of the building that should be removed.
        """

        if name in buildings.keys():
            del(buildings[name])

    def compatibility_check():
        # compatibility with save files from 0.1.2
        if 'high_school_building' in buildings.keys():
            high_school_building = buildings['high_school_building']
            high_school_building._name = "school_building"
            high_school_building._title = "School Building"
            buildings['school_building'] = high_school_building

        if 'high_school_dormitory' in buildings.keys():
            high_school_dormitory = buildings['high_school_dormitory']
            high_school_dormitory._name = "school_dormitory"
            high_school_dormitory._title = "School Dormitory"
            buildings['school_dormitory'] = high_school_dormitory

        if 'high_school_building' in buildings.keys():
            buildings.pop("high_school_building")
        if 'high_school_dormitory' in buildings.keys():
            buildings.pop("high_school_dormitory")
        if 'middle_school_building' in buildings.keys():
            buildings.pop("middle_school_building")
        if 'middle_school_dormitory' in buildings.keys():
            buildings.pop("middle_school_dormitory")
        if 'elementary_school_building' in buildings.keys():
            buildings.pop("elementary_school_building")
        if 'elementary_school_dormitory' in buildings.keys():
            buildings.pop("elementary_school_dormitory")

        if 'tennis_court' in buildings.keys():
            buildings.pop("tennis_court")

    # endregion
    #########################################

######################
# region LABEL ----- #
######################

label load_buildings ():
    $ set_current_mod('base')

    $ compatibility_check()

    # unlocked
    $ load_building("school_building", "School Building", {
        '_description': [
            [
                "The main school building for those students that attend school.",
            ],
            [
                "The main school building for those students that attend school.",
            ],
        ],
        '_max_level': 1,
        '_unlock_conditions': ConditionStorage(),
        '_upgrade_conditions':[],
        '_image_path': 'images/journal/buildings/school_building <level>.webp',
        '_image_path_alt': 'images/journal/buildings/school_building 1.webp',
    }, {
        '_level': 1,
    })

    # unlocked
    $ load_building("school_dormitory", "School Dormitory", {
        '_description': [
            [
                "The dormitory dedicated to the school students",
            ],
            [
                "The dormitory dedicated to the school students",
            ],
        ],
        '_max_level': 1,
        '_unlock_conditions': ConditionStorage(),
        '_upgrade_conditions':[],
        '_image_path': 'images/journal/buildings/school_dormitory <level>.webp',
        '_image_path_alt': 'images/journal/buildings/school_dormitory 1.webp',
    }, {
        '_level': 1,
    })

    #! locked, currently not implemented
    $ load_building("labs", "Labs", {
        '_description': [
            [
                "A building with various labs and maybe a certain special lab for someone.",
            ],
            [
                "A building with various labs and maybe a certain special lab for someone.",
            ],
            [
                "A building with various labs and maybe a certain special lab for someone.",
            ],
        ],
        '_max_level': 2,
        '_unlock_conditions': ConditionStorage(
            MoneyCondition(1000),
            LockCondition()
        ),
        '_upgrade_conditions':[
            ConditionStorage(
                MoneyCondition(2000),
            ),
        ],
    }, {
        '_level': 0,
    })

    #! locked, currently not implemented
    $ load_building("sports_field", "Sports Field", {
        '_description': [
            [
                "A large area dedicated to various sport activities.",
            ],
            [
                "A large area dedicated to various sport activities.",
            ],
        ],
        '_max_level': 1,
        '_unlock_conditions': ConditionStorage(
            MoneyCondition(1000),
            LockCondition(),
        ),
        '_upgrade_conditions':[],
    }, {
        '_level': 0,
    })

    #! locked, currently not implemented
    $ load_building("beach", "Beach", {
        '_description': [
            [
                "A beautiful beach for the students to relax and have fun.",
            ],
            [
                "A beautiful beach for the students to relax and have fun.",
            ],
        ],
        '_max_level': 1,
        '_unlock_conditions': ConditionStorage(
            MoneyCondition(1000),
            LockCondition()
        ),
        '_upgrade_conditions':[],
    }, {
        '_level': 0,
    })

    #! locked, currently not implemented
    $ load_building("staff_lodges", "Staff Lodges", {
        '_description': [
            [
                "The lodges where the staff members can stay.",
            ],
            [
                "The lodges where the staff members can stay.",
            ],
        ],
        '_max_level': 1,
        '_unlock_conditions': ConditionStorage(
            MoneyCondition(1000),
            LockCondition()
        ),
        '_upgrade_conditions':[],
    }, {
        '_level': 0,
    })

    # unlocked
    $ load_building("gym", "Gym", {
        '_description': [
            [
                "This is the indoor gym used for sports classes and school assemblies.",
            ],
            [
                "This is the indoor gym used for sports classes and school assemblies.",
            ],
        ],
        '_max_level': 1,
        '_unlock_conditions': ConditionStorage(),
        '_upgrade_conditions':[],
        '_image_path': 'images/journal/buildings/gym <level>.webp',
        '_image_path_alt': 'images/journal/buildings/gym 1.webp',
    }, {
        '_level': 1,
    })

    #! locked, currently not implemented
    $ load_building("swimming_pool", "Swimming Pool", {
        '_description': [
            [
                "The schools pool. One of the favorite places of almost every student. Chilling in the cool water, looking at the fellow students in their skimpy bathing suits.",
            ],
            [
                "The schools pool. One of the favorite places of almost every student. Chilling in the cool water, looking at the fellow students in their skimpy bathing suits.",
            ],
        ],
        '_max_level': 1,
        '_unlock_conditions': ConditionStorage(
            MoneyCondition(1000),
            LockCondition()
        ),
        '_upgrade_conditions':[],
    }, {
        '_level': 0,
    })

    $ load_building("cafeteria", "Cafeteria", {
        '_description': [
            [
                "The cafeteria is a place where students can come together to spend their free-time and to eat together.",
                "Here the students will receive free lunch. This helps the students to save money and to have a healthy meal every day.",
                "\nWeekly Costs after unlock: 100$",
            ],
            [
                "Level 1",
                "The cafeteria is a place where students can come together to spend their free-time and to eat together.",
                "Here the students will receive free lunch. This helps the students to save money and to have a healthy meal every day.",
                "Currently the cafeteria can only provide relatively cheap food. But with the right investments, the cafeteria can be upgraded to provide better food and to be more efficient.",
                "\nWeekly Costs: 100$",
                "\nWeekly Costs after upgrade: 250$",
            ],
            [
                "The cafeteria is a place where students can come together to spend their free-time and to eat together.",
                "Here the students will receive free lunch. This helps the students to save money and to have a healthy meal every day.",
                "Currently the cafeteria provides decent food. But with the right investments, the cafeteria can be upgraded to provide better food and to be more efficient.",
                "\nWeekly Costs: 250$",
                "\nWeekly Costs after upgrade: 500$",
            ],
            [
                "The cafeteria is a place where students can come together to spend their free-time and to eat together.",
                "Here the students will receive free lunch. This helps the students to save money and to have a healthy meal every day.",
                "Currently the cafeteria provides expensive, healthy and nutritional food. Maybe we could find a way to upgrade it to have it also make profit for the school.",
                "\nWeekly Costs: 500$",
                "\nWeekly Costs after upgrade: 800$",
            ],
            [
                "The cafeteria is a place where students can come together to spend their free-time and to eat together.",
                "Here the students will receive free lunch. This helps the students to save money and to have a healthy meal every day.",
                "The cafeteria has been prepared to receive guests from outside.",
                "\nWeekly Costs: 800$",
            ],
        ],
        '_max_level': 1,
        '_unlock_conditions': ConditionStorage(
            ProgressCondition("unlock_cafeteria", 1, True),
            MoneyCondition(1500),
            # LockCondition(False),
        ),
        '_unlock_effects': [
            ModifierEffect('weekly_cost_cafeteria', 'money', Modifier_Obj('Cafeteria', "+", -100), collection = 'payroll_weekly'),
        ],
        '_upgrade_conditions':[
            ConditionStorage(
                MoneyCondition(3000),
                LockCondition(True),
            ),
            ConditionStorage(
                MoneyCondition(5000),
            ),
            ConditionStorage(
                MoneyCondition(10000),
            ),
        ],
        '_upgrade_effects': {
            2: [
                ModifierEffect('weekly_cost_cafeteria', 'money', Modifier_Obj('Cafeteria', "+", -250), collection = 'payroll_weekly'),
            ],
            3: [
                ModifierEffect('weekly_cost_cafeteria', 'money', Modifier_Obj('Cafeteria', "+", -500), collection = 'payroll_weekly'),
            ],
            4: [
                ModifierEffect('weekly_cost_cafeteria', 'money', Modifier_Obj('Cafeteria', "+", -800), collection = 'payroll_weekly'),
            ],
        },
        '_image_path': 'images/journal/buildings/cafeteria <level> 0.webp',
        '_image_path_alt': 'images/journal/buildings/cafeteria 1 0.webp',
        '_construction_time': 7,
    }, {
        '_level': 0,
    })

    #! locked, currently not implemented
    $ load_building("bath", "Bath", {
        '_description': [
            [
                "The public bath. Here the students can relax and/or wash after a long school day.",
            ],
            [
                "The public bath. Here the students can relax and/or wash after a long school day.",
            ],
        ],
        '_max_level': 1,
        '_unlock_conditions': ConditionStorage(
            MoneyCondition(1000),
            LockCondition()
        ),
        '_upgrade_conditions':[],
    }, {
        '_level': 0,
    })

    # unlocked
    $ load_building("kiosk", "Kiosk", {
        '_description': [
            [
                "A small vendor that sells food and small utilities necessary for everyday life at the school campus.",
            ],
            [
                "A small vendor that sells food and small utilities necessary for everyday life at the school campus.",
            ],
        ],
        '_max_level': 1,
        '_unlock_conditions': ConditionStorage(),
        '_upgrade_conditions':[],
        '_image_path': 'images/journal/buildings/kiosk <level>.webp',
        '_image_path_alt': 'images/journal/buildings/kiosk 1.webp',
    }, {
        '_level': 1,
    })

    # unlocked
    $ load_building("courtyard", "Courtyard", {
        '_description': [
            [
                "The outside area of the school campus. Here teacher and students can relax and enjoy the nice fresh air of this rather isolated region.",
            ],
            [
                "The outside area of the school campus. Here teacher and students can relax and enjoy the nice fresh air of this rather isolated region.",
            ],
        ],
        '_max_level': 1,
        '_unlock_conditions': ConditionStorage(),
        '_upgrade_conditions':[],
        '_image_path': 'images/journal/buildings/courtyard <level>.webp',
        '_image_path_alt': 'images/journal/buildings/courtyard 1.webp',
    }, {
        '_level': 1,
    })

    # unlocked
    $ load_building("office_building", "Office Building", {
        '_description': [
            [
                "The building that holds all offices needed for the management of the entire school.",
            ],
            [
                "The building that holds all offices needed for the management of the entire school.",
            ],
        ],
        '_max_level': 1,
        '_unlock_conditions': ConditionStorage(),
        '_upgrade_conditions':[],
        '_image_path': 'images/journal/buildings/office <level>.webp',
        '_image_path_alt': 'images/journal/buildings/office 1.webp',
    }, {
        '_level': 1,
    })

    return

# endregion
######################
