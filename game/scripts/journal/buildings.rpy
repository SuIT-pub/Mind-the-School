init -6 python:
    import re
    class Building:
        def __init__(self, name, title):
            self._name = name
            self._title = title
            self._description = ""
            self._image_path_alt = "images/journal/empty_image.png"
            self._image_path = "images/journal/empty_image.png"
            self._unlocked = False
            self._level = 1
            self._max_level = 1
            self._unlock_conditions = []
            self._update_conditions = []
            self._blocked = False

        def _update(self, title, data = None):
            if data != None:
                self.__dict__.update(data)

            self._title = title

            if not hasattr(self, '_description'):
                self._description = ""
            if not hasattr(self, '_image_path'):
                self._image_path = "images/journal/empty_image.png"
            if not hasattr(self, '_image_path_alt'):
                self._image_path_alt = "images/journal/empty_image.png"
            if not hasattr(self, '_level'):
                self._level = 1
            if not hasattr(self, '_max_level'):
                self._max_level = 1
            if not hasattr(self, '_unlocked'):
                self._unlocked = False
            if not hasattr(self, '_unlock_conditions'):
                self._unlock_conditions = []
            if not hasattr(self, '_update_conditions'):
                self._update_conditions = []
            if not hasattr(self, '_blocked'):
                self._blocked = False
        
        def get_name(self):
            return self._name

        def get_title(self):
            return self._title

        def get_type(self):
            return "building"

        def get_description(self):
            return self._description

        def get_image(self):
            level = get_lowest_level()
            for i in reversed(range(0, level + 1)):
                image = self._image_path.replace("{level}", str(i))
                if renpy.exists(image):
                    return image
            return self._image_path_alt

        def get_full_image(self):
            image = self.get_image()
            full_image = image.replace(".", "_full.")

            if renpy.exists(full_image):
                return full_image
            return None

        def get_level(self):
            return self._level

        def get_max_level(self):
            return self._max_level

        def set_level(self, level):
            self._level = level

        def set_max_level(self, level):
            self._max_level = level

        def is_available(self):
            return self.is_unlocked() and not self.is_blocked()

        def set_blocked(self, is_blocked = True):
            self._blocked = is_blocked

        def unlock(self, unlock = True):
            self._unlocked = unlock

        def is_unlocked(self):
            return self._unlocked

        def is_blocked(self):
            return self._blocked

        def is_visible(self):
            for condition in self._unlock_conditions:
                if condition.is_blocking(None):
                    return False
            return True

        def can_be_unlocked(self):
            for condition in self._unlock_conditions:
                if condition.is_fullfilled(None):
                    continue
                return False

            return True

        def can_be_upgraded(self):
            for condition in self._update_conditions:
                if condition.is_fullfilled(None):
                    continue
                return False

            return True

        def has_higher_level(self):
            return self._level < self._max_level

        def get_update_conditions(self, level):
            if level > len(self._update_conditions) or level <= 0:
                return []
            return self._update_conditions[level - 1]

        def get_list_conditions(self, cond_type = "unlock"):
            output = []

            conditions = self._unlock_conditions
            if cond_type == "upgrade":
                conditions = self.get_update_conditions(self._level)

            for condition in conditions:
                if not condition.is_set_blocking() and condition.display_in_list:
                    output.append(condition)

            return output

        def get_desc_conditions(self, cond_type = "unlock"):
            output = []

            conditions = self._unlock_conditions
            if cond_type == "upgrade":
                conditions = self.get_update_conditions(self._level)

            for condition in conditions:
                if not condition.is_set_blocking() and condition.display_in_desc:
                    output.append(condition)

            return output


    #############################################
    # Buildings Global Methods
    
    def count_locked_buildings():
        output = 0

        for building in buildings.values():
            if not building.is_unlocked():
                output += 1
        return output

    def get_unlocked_buildings():
        output = []

        for building in buildings.values():
            if building.is_unlocked() and building.get_name() not in output:
                output.append(building.get_name())
        
        return output
    
    def get_visible_unlocked_buildings():
        output = []

        for building in buildings.values():
            if (building.is_visible() and 
            building.is_unlocked() and
            building.get_name() not in output):
                output.append(building.get_name())
                continue
            
        return output

    def get_visible_locked_buildings():
        output = []

        for building in buildings.values():
            if (building.is_visible() and 
            not building.is_unlocked() and
            building.get_name() not in output):
                output.append(building.get_name())
                continue
            
        return output

    def get_visible_buildings(include_unlocked = False):
        output = []

        for building in buildings.values():
            if (building.is_visible() and 
            (not building.is_unlocked() or include_unlocked) and
            building.get_name() not in output):
                output.append(building.get_name())
                continue
            
        return output

    def get_unlockable_buildings():
        output = []

        for building in buildings.values():
            unlock = building.can_be_unlocked()
            unlocked = building.is_unlocked()

            if (unlock and not unlocked and building.get_name() not in output):
                output.append(building.get_name())
                continue

        return output

    def get_building(building):
        if building in buildings.keys():
            return buildings[building]
        return None

    def set_building_blocked(building_name, is_blocked = True):
        if building_name in buildings.keys():
            buildings[building_name].set_blocked(is_blocked)

    def set_all_buildings_blocked(is_blocked = True):
        for building in buildings.values():
            building.set_blocked(is_blocked)

    def is_building_available(building_name):
        if building_name not in buildings.keys():
            return False
        return buildings[building_name].is_available()

    def is_building_unlocked(building_name):
        if building_name not in buildings.keys():
            return False
        return buildings[building_name].is_unlocked()

    def is_building_visible(building_name):
        if building_name not in buildings.keys():
            return False
        return buildings[building_name].is_visible()

    def load_building(name, title, runtime_data = None, starting_data = None):
        if name not in buildings.keys():
            buildings[name] = Building(name, title)
            buildings[name]._update(title, starting_data)

        buildings[name]._update(title, runtime_data)

    def remove_building(name):
        if name in buildings.keys():
            del(buildings[name])

label load_buildings:
    $ load_building("high_school_building", "High School Building", {
        '_description': "The main school building for those students that attend high school.",
        '_max_level': 1,
        '_unlock_conditions': [],
        '_update_conditions':[],
    }, {
        '_unlocked': True,
    })

    $ load_building("high_school_dormitory", "High School Dormitory", {
        '_description': "The dormitory dedicated to the high school students",
        '_max_level': 1,
        '_unlock_conditions': [],
        '_update_conditions':[],
    }, {
        '_unlocked': True,
    })

    $ load_building("middle_school_building", "Middle School Building", {
        '_description': "The main school building for those students that attend middle school.",
        '_max_level': 1,
        '_unlock_conditions': [],
        '_update_conditions':[],
    }, {
        '_unlocked': True,
    })

    $ load_building("middle_school_dormitory", "Middle School Dormitory", {
        '_description': "The dormitory dedicated to the middle school students",
        '_max_level': 1,
        '_unlock_conditions': [],
        '_update_conditions':[],
    }, {
        '_unlocked': True,
    })

    $ load_building("elementary_school_building", "Elementary School Building", {
        '_description': "The main school building for those students that attend elementary school.",
        '_max_level': 1,
        '_unlock_conditions': [],
        '_update_conditions':[],
    }, {
        '_unlocked': True,
    })

    $ load_building("elementary_school_dormitory", "Elementary School Dormitory", {
        '_description': "The dormitory dedicated to the elementary school students",
        '_max_level': 1,
        '_unlock_conditions': [],
        '_update_conditions':[],
    }, {
        '_unlocked': True,
    })

    $ load_building("labs", "Labs", {
        '_description': "A building with various labs and maybe a certain special lab for someone.",
        '_max_level': 2,
        '_unlock_conditions': [
            MoneyCondition(1000),
            # LockCondition()
        ],
        '_update_conditions':[
            [
                MoneyCondition(2000),
                # LockCondition()
            ],
        ],
    }, {
        '_unlocked': False,
    })

    $ load_building("sports_field", "Sports Field", {
        '_description': "A large area dedicated to various sport activities.",
        '_max_level': 1,
        '_unlock_conditions': [
            MoneyCondition(1000),
            # LockCondition()
        ],
        '_update_conditions':[],
    }, {
        '_unlocked': False,
    })

    $ load_building("tennis_court", "Tennis Court", {
        '_description': "Something only a reputable school can have. \n" +
            "A tennis court. Of course only used for playing tennis.",
        '_max_level': 1,
        '_unlock_conditions': [
            MoneyCondition(1000),
            # LockCondition()
        ],
        '_update_conditions':[],
    }, {
        '_unlocked': False,
    })

    $ load_building("gym", "Gym", {
        '_description': "This is the indoor gym used for sports classes and school assemblies.",
        '_max_level': 1,
        '_unlock_conditions': [],
        '_update_conditions':[],
    }, {
        '_unlocked': True,
    })

    $ load_building("swimming_pool", "Swimming Pool", {
        '_description': "The schools pool. One of the favorite places of " +
            "almost every student. Chilling in the cool water, looking at " +
            "the fellow students in their skimpy bathing suits.",
        '_max_level': 1,
        '_unlock_conditions': [
            MoneyCondition(1000),
            # LockCondition()
        ],
        '_update_conditions':[],
    }, {
        '_unlocked': False,
    })

    $ load_building("cafeteria", "Cafeteria", {
        '_description': "The cafeteria, the place students come together to " +
            "spend their free-time and to eat together.",
        '_max_level': 1,
        '_unlock_conditions': [
            MoneyCondition(1000),
            # LockCondition()
        ],
        '_update_conditions':[],
    }, {
        '_unlocked': False,
    })

    $ load_building("bath", "Bath", {
        '_description': "The public bath. Here the students can relax and/or wash" +
            "after a long school day.",
        '_max_level': 1,
        '_unlock_conditions': [
            MoneyCondition(1000),
            # LockCondition()
        ],
        '_update_conditions':[],
    }, {
        '_unlocked': False,
    })

    $ load_building("kiosk", "Kiosk", {
        '_description': "A small vendor that sells food and small utilities necessary for everday life at the school campus.",
        '_max_level': 1,
        '_unlock_conditions': [],
        '_update_conditions':[],
    }, {
        '_unlocked': True,
    })

    $ load_building("courtyard", "Courtyard", {
        '_description': "The outside area of the school campus. Here teacher and students can relax and enjoy the nice fresh air of this rather isolated region.",
        '_max_level': 1,
        '_unlock_conditions': [],
        '_update_conditions':[],
    }, {
        '_unlocked': True,
    })

    $ load_building("office_building", "Office Building", {
        '_description': "The building that holds all offices needed for the management of the entire school.",
        '_max_level': 1,
        '_unlock_conditions': [],
        '_update_conditions':[],
    }, {
        '_unlocked': True,
    })

    return