init -6 python:
    import re
    class Building:
        def __init__(self, name, title):
            self.name = name
            self.title = title
            self.description = ""
            self.image_path_alt = "images/journal/empty_image.png"
            self.image_path = "images/journal/empty_image.png"
            self.unlocked = False
            self.unlock_conditions = []
            self.blocked = False

        def _update(self, title, data = None):
            if data != None:
                self.__dict__.update(data)

            self.title = title

            if not hasattr(self, 'description'):
                self.description = ""
            if not hasattr(self, 'image_path'):
                self.image_path = "images/journal/empty_image.png"
            if not hasattr(self, 'image_path_alt'):
                self.image_path_alt = "images/journal/empty_image.png"
            if not hasattr(self, 'unlocked'):
                self.unlocked = False
            if not hasattr(self, 'unlock_conditions'):
                self.unlock_conditions = []
            if not hasattr(self, 'blocked'):
                self.blocked = False
        

        def get_name(self):
            return self.name

        def get_title(self):
            return self.title

        def get_type(self):
            return "building"

        def get_image(self):
            level = get_lowest_level()
            for i in reversed(range(0, level + 1)):
                image = self.image_path.replace("{level}", str(i))
                if renpy.exists(image):
                    return image
            return self.image_path_alt

        def get_full_image(self):
            image = self.get_image()
            full_image = image.replace(".", "_full.")

            if renpy.exists(full_image):
                return full_image
            return None

        def is_available(self):
            return self.unlocked and not self.blocked

        def set_blocked(self, is_blocked = True):
            self.blocked = is_blocked

        def unlock(self, unlock = True):
            self.unlocked = unlock

        def is_unlocked(self):
            return self.unlocked
        
        def is_visible(self):
            for condition in self.unlock_conditions:
                if condition.is_blocking(None):
                    return False
            return True

        def can_be_unlocked(self):
            for condition in self.unlock_conditions:
                if condition.is_fullfilled(None):
                    continue
                return False

            return True

        def get_list_conditions(self):
            output = []
            for condition in self.unlock_conditions:
                if not condition.is_set_blocking() and condition.display_in_list:
                    output.append(condition)

            return output

        def get_desc_conditions(self):
            output = []
            for condition in self.unlock_conditions:
                if not condition.is_set_blocking() and condition.display_in_desc:
                    output.append(condition)

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
            building.name not in output):
                output.append(building.name)
                continue
            
        return output

    def get_visible_locked_buildings():
        output = []

        for building in buildings.values():
            if (building.is_visible() and 
            not building.is_unlocked() and
            building.name not in output):
                output.append(building.name)
                continue
            
        return output

    def get_visible_buildings(include_unlocked = False):
        output = []

        for building in buildings.values():
            if (building.is_visible() and 
            (not building.is_unlocked() or include_unlocked) and
            building.name not in output):
                output.append(building.name)
                continue
            
        return output

    def get_unlockable_buildings():
        output = []

        for building in buildings.values():
            unlock = building.can_be_unlocked()
            unlocked = building.is_unlocked()

            if (unlock and not unlocked and building.name not in output):
                output.append(building.name)
                continue

        return output

    def get_building(building):
        if building in buildings.keys():
            return buildings[building]
        return None

    def set_building_blocked(building_name, is_blocked):
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

        set_all_buildings_blocked(False)
        buildings[name]._update(title, runtime_data)

    def remove_building(name):
        if name in buildings.keys():
            del(buildings[name])

label load_buildings:
    $ load_building("high_school_building", "High School Building", {
        'description': "The main school building for those students that attend high school.",
        'unlock_conditions': []
    }, {
        'unlocked': True,
    })

    $ load_building("high_school_dormitory", "High School Dormitory", {
        'description': "The dormitory dedicated to the high school students",
        'unlock_conditions': []
    }, {
        'unlocked': True,
    })

    $ load_building("middle_school_building", "Middle School Building", {
        'description': "The main school building for those students that attend middle school.",
        'unlock_conditions': []
    }, {
        'unlocked': True,
    })

    $ load_building("middle_school_dormitory", "Middle School Dormitory", {
        'description': "The dormitory dedicated to the middle school students",
        'unlock_conditions': []
    }, {
        'unlocked': True,
    })

    $ load_building("elementary_school_building", "Elementary School Building", {
        'description': "The main school building for those students that attend elementary school.",
        'unlock_conditions': []
    }, {
        'unlocked': True,
    })

    $ load_building("elementary_school_dormitory", "Elementary School Dormitory", {
        'description': "The dormitory dedicated to the elementary school students",
        'unlock_conditions': []
    }, {
        'unlocked': True,
    })

    $ load_building("labs", "Labs", {
        'description': "A building with various labs and maybe a certain special lab for someone.",
        'unlock_conditions': [
            MoneyCondition(1000),
            # LockCondition()
        ]
    }, {
        'unlocked': False,
    })

    $ load_building("sports_field", "Sports Field", {
        'description': "A large area dedicated to various sport activities.",
        'unlock_conditions': [
            MoneyCondition(1000),
            # LockCondition()
        ]
    }, {
        'unlocked': False,
    })

    $ load_building("tennis_court", "Tennis Court", {
        'description': "Something only a reputable school can have. \n" +
            "A tennis court. Of course only used for playing tennis.",
        'unlock_conditions': [
            MoneyCondition(1000),
            # LockCondition()
        ]
    }, {
        'unlocked': False,
    })

    $ load_building("gym", "Gym", {
        'description': "This is the indoor gym used for sports classes and school assemblies.",
        'unlock_conditions': []
    }, {
        'unlocked': True,
    })

    $ load_building("swimming_pool", "Swimming Pool", {
        'description': "The schools pool. One of the favorite places of " +
            "almost every student. Chilling in the cool water, looking at " +
            "the fellow students in their skimpy bathing suits.",
        'unlock_conditions': [
            MoneyCondition(1000),
            # LockCondition()
        ]
    }, {
        'unlocked': False,
    })

    $ load_building("cafeteria", "Cafeteria", {
        'description': "The cafeteria, the place students come together to " +
            "spend their free-time and to eat together.",
        'unlock_conditions': [
            MoneyCondition(1000),
            # LockCondition()
        ]
    }, {
        'unlocked': False,
    })

    $ load_building("bath", "Bath", {
        'description': "The public bath. Here the students can relax and/or wash" +
            "after a long school day.",
        'unlock_conditions': [
            MoneyCondition(1000),
            # LockCondition()
        ]
    }, {
        'unlocked': False,
    })

    $ load_building("kiosk", "Kiosk", {
        'description': "A small vendor that sells food and small utilities necessary for everday life at the school campus.",
        'unlock_conditions': []
    }, {
        'unlocked': True,
    })

    $ load_building("courtyard", "Courtyard", {
        'description': "The outside area of the school campus. Here teacher and students can relax and enjoy the nice fresh air of this rather isolated region.",
        'unlock_conditions': []
    }, {
        'unlocked': True,
    })

    $ load_building("office_building", "Office Building", {
        'description': "The building that holds all offices needed for the management of the entire school.",
        'unlock_conditions': []
    }, {
        'unlocked': True,
    })

    return