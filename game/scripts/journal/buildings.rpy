############################
# ----- PYTHON BLOCK ----- #
############################

init -6 python:
    import re

    #######################
    # ----- CLASSES ----- #
#######################

    class Building(Journal_Obj):
        def __init__(self, name: str, title: str):
            super().__init__(name, title)
            self._level = 0
            self._max_level = 1
            self._update_conditions = []
            self._blocked = False

        def _update(self, title: str, data: Dict[str, Any] = None) -> None:
            super()._update(title, data)
            if data != None:
                self.__dict__.update(data)
                
            if not hasattr(self, '_level'):
                self._level = 0
            if not hasattr(self, '_max_level'):
                self._max_level = 1
            if not hasattr(self, '_update_conditions'):
                self._update_conditions = []
        
        def get_type(self) -> str:
            return "building"

        def get_description(self, level: int = -1) -> List[str]:
            if level == -1:
                level = self._level
            if level < 0 or level >= len(self._description):
                return ""
            return self._description[level]

        def get_description_str(self, level: int = -1) -> str:
            return "\n\n".join(self.get_description(level))

        def get_image(self, _school = "x", _level = -1) -> str:
            level = get_lowest_level(charList["schools"])
            for i in reversed(range(0, level + 1)):
                image = self._image_path.replace("<level>", str(i))
                if renpy.loadable(image):
                    return image
            return self._image_path_alt

        def get_full_image(self, _school = "x", _level = -1) -> str:
            image = self.get_image()
            full_image = image.replace(".", "_full.")

            if renpy.loadable(full_image):
                return full_image
            return None

        def get_level(self) -> int:
            return self._level

        def get_max_level(self) -> int:
            return self._max_level

        def set_level(self, level: int) -> None:
            if level < 0:
                level = 0
            if level > self._max_level:
                level = self._max_level

            self._level = level

        def set_max_level(self, level: int) -> None:
            self._max_level = level

        def is_available(self) -> bool:
            return self.is_unlocked("x") and not self.is_blocked()

        def set_blocked(self, is_blocked: bool = True) -> None:
            self._blocked = is_blocked

        def unlock(self, unlock: bool = True) -> None:
            self._level = 1 if unlock else 0

        def is_unlocked(self, _school) -> bool:
            return self._level != 0

        def is_blocked(self) -> bool:
            return self._blocked

        def can_be_upgraded(self, **kwargs) -> bool:
            conditions = self.get_update_conditions(self._level)
            return conditions != None and conditions.is_fulfilled(**kwargs)

        def has_higher_level(self) -> bool:
            return self._level < self._max_level

        def get_upgrade_condition_storage(self, level: int) -> ConditionStorage:
            if level > len(self._update_conditions) or level <= 0:
                return None
            return self._update_conditions[level - 1]

        def get_update_conditions(self, level: int) -> ConditionStorage:
            if level > len(self._update_conditions) or level <= 0:
                return None
            return self._update_conditions[level - 1]
        
        def get_list_conditions(self, cond_type: str = UNLOCK, level: int = -1) -> List[Condition]:
            if level == -1:
                level = self._level

            if cond_type == UNLOCK:
                return self._unlock_conditions.get_list_conditions()
            if cond_type == UPGRADE:
                update_conditions = self.get_update_conditions(level)
                if update_conditions == None:
                    return []
                else:
                    return self.get_update_conditions(level).get_list_conditions()
        
        def get_list_conditions_list(self, cond_type: str = UNLOCK, level: int = -1, **kwargs) -> List[Tuple[str, str]]:
            if level == -1:
                level = self._level

            if cond_type == UNLOCK:
                return self._unlock_conditions.get_list_conditions_list(**kwargs)
            if cond_type == UPGRADE:
                update_conditions = self.get_update_conditions(level)
                if update_conditions == None:
                    return []
                else:
                    return self.get_update_conditions(level).get_list_conditions_list(**kwargs)

        def get_desc_conditions(self, cond_type: str = UNLOCK, level: int = -1) -> List[Condition]:
            if level == -1:
                level = self._level

            if cond_type == UNLOCK:
                return self._unlock_conditions.get_desc_conditions()
            if cond_type == UPGRADE:
                update_conditions = self.get_update_conditions(level)
                if update_conditions == None:
                    return []
                else:
                    return self.get_update_conditions(level).get_desc_conditions()

        
        def get_desc_conditions_desc(self, cond_type: str = UNLOCK, level: int = -1, **kwargs) -> List[str]:
            if level == -1:
                level = self._level

            if cond_type == UNLOCK:
                return self._unlock_conditions.get_desc_conditions_desc(**kwargs)
            if cond_type == UPGRADE:
                update_conditions = self.get_update_conditions(level)
                if update_conditions == None:
                    return []
                else:
                    return self.get_update_conditions(level).get_desc_conditions_desc(**kwargs)

    #######################

    ########################################
    # ----- Buildings Global Methods ----- #
    ########################################
    
    def count_locked_buildings() -> int:
        output = 0

        for building in buildings.values():
            if not building.is_unlocked("x"):
                output += 1
        return output

    def get_unlocked_buildings() -> List[str]:
        output = []

        for building in buildings.values():
            if building.is_unlocked("x") and building.get_name() not in output:
                output.append(building.get_name())
        
        return output
    
    def get_building(building: str) -> Building:
        if building in buildings.keys():
            return buildings[building]
        return None

    def set_building_blocked(building_name: str, is_blocked: bool = True) -> None:
        if building_name in buildings.keys():
            buildings[building_name].set_blocked(is_blocked)

    def set_all_buildings_blocked(is_blocked: bool = True) -> None:
        for building in buildings.values():
            building.set_blocked(is_blocked)

    def is_building_available(building_name: str) -> bool:
        if building_name not in buildings.keys():
            return False
        return buildings[building_name].is_available()

    def is_building_unlocked(building_name: str) -> bool:
        if building_name not in buildings.keys():
            return False
        return buildings[building_name].is_unlocked("x")

    def is_building_visible(building_name: str) -> bool:
        if building_name not in buildings.keys():
            return False
        return buildings[building_name].is_visible()

    def load_building(name: str, title: str, runtime_data: Dict[str, Any] = None, starting_data: Dict[str, Any] = None) -> None:
        if name not in buildings.keys():
            buildings[name] = Building(name, title)
            buildings[name]._update(title, starting_data)

        buildings[name]._update(title, runtime_data)

    def remove_building(name: str) -> None:
        if name in buildings.keys():
            del(buildings[name])

    
    ########################################

############################

#####################
# ----- LABEL ----- #
#####################

label load_buildings ():
    $ load_building("high_school_building", "High School Building", {
        '_description': [
            [
                "The main school building for those students that attend high school.",
            ],
            [
                "The main school building for those students that attend high school.",
            ],
        ],
        '_max_level': 1,
        '_unlock_conditions': ConditionStorage(),
        '_update_conditions':[],
    }, {
        '_level': 1,
    })

    $ load_building("high_school_dormitory", "High School Dormitory", {
        '_description': [
            [
                "The dormitory dedicated to the high school students",
            ],
            [
                "The dormitory dedicated to the high school students",
            ],
        ],
        '_max_level': 1,
        '_unlock_conditions': ConditionStorage(),
        '_update_conditions':[],
    }, {
        '_level': 1,
    })

    $ load_building("middle_school_building", "Middle School Building", {
        '_description': [
            [
                "The main school building for those students that attend middle school.",
            ],
            [
                "The main school building for those students that attend middle school.",
            ],
        ],
        '_max_level': 1,
        '_unlock_conditions': ConditionStorage(),
        '_update_conditions':[],
    }, {
        '_level': 1,
    })

    $ load_building("middle_school_dormitory", "Middle School Dormitory", {
        '_description': [
            [
                "The dormitory dedicated to the middle school students",
            ],
            [
                "The dormitory dedicated to the middle school students",
            ],
        ],
        '_max_level': 1,
        '_unlock_conditions': ConditionStorage(),
        '_update_conditions':[],
    }, {
        '_level': 1,
    })

    $ load_building("elementary_school_building", "Elementary School Building", {
        '_description': [
            [
                "The main school building for those students that attend elementary school.",
            ],
            [
                "The main school building for those students that attend elementary school.",
            ],
        ],
        '_max_level': 1,
        '_unlock_conditions': ConditionStorage(),
        '_update_conditions':[],
    }, {
        '_level': 1,
    })

    $ load_building("elementary_school_dormitory", "Elementary School Dormitory", {
        '_description': [
            [
                "The dormitory dedicated to the elementary school students",
            ],
            [
                "The dormitory dedicated to the elementary school students",
            ],
        ],
        '_max_level': 1,
        '_unlock_conditions': ConditionStorage(),
        '_update_conditions':[],
    }, {
        '_level': 1,
    })

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
            # LockCondition()
        ),
        '_update_conditions':[
            ConditionStorage(
                MoneyCondition(2000),
            ),
        ],
    }, {
        '_level': 0,
    })

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
        ),
        '_update_conditions':[],
    }, {
        '_level': 0,
    })

    $ load_building("tennis_court", "Tennis Court", {
        '_description': [
            [
                "Something only a reputable school can have.\nA tennis court. Of course only used for playing tennis.",
            ],
            [
                "Something only a reputable school can have.\nA tennis court. Of course only used for playing tennis.",
            ],
        ],
        '_max_level': 1,
        '_unlock_conditions': ConditionStorage(
            MoneyCondition(1000),
            LockCondition()
        ),
        '_update_conditions':[],
    }, {
        '_level': 0,
    })

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
        '_update_conditions':[],
    }, {
        '_level': 1,
    })

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
        '_update_conditions':[],
    }, {
        '_level': 0,
    })

    $ load_building("cafeteria", "Cafeteria", {
        '_description': [
            [
                "The cafeteria, the place students come together to spend their free-time and to eat together.",
            ],
            [
                "The cafeteria, the place students come together to spend their free-time and to eat together.",
            ],
        ],
        '_max_level': 1,
        '_unlock_conditions': ConditionStorage(
            MoneyCondition(1000),
            LockCondition()
        ),
        '_update_conditions':[],
    }, {
        '_level': 0,
    })

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
        '_update_conditions':[],
    }, {
        '_level': 0,
    })

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
        '_update_conditions':[],
    }, {
        '_level': 1,
    })

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
        '_update_conditions':[],
    }, {
        '_level': 1,
    })

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
        '_update_conditions':[],
    }, {
        '_level': 1,
    })

    return

#####################
