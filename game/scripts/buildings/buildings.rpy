init python:
    import re
    class Building:
        def __init__(self, name, title):
            self.name = name
            self.title = title
            self.description = ""
            self.unlocked = False
            self.image_path = "images/journal/empty_image.png"
            self.unlock_conditions = []

        def get_name(self):
            return self.name

        def get_title(self):
            return self.title

        def get_type(self):
            return "building"

        def unlock(self):
            self.unlocked = True

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

    
    def get_unlocked_buildings():
        output = []

        for building in buildings.values():
            if building.is_unlocked() and building.get_name() not in output:
                output.append(building.get_name())
        
        return output


    def get_visible_buildings(include_unlocked = False):
        output = []

        for building in buildings.values():
            if (building.is_visible() and 
            ((not building.is_unlocked() and not include_unlocked) or include_unlocked) and
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

    def is_building_unlocked(building_name):
        if building_name not in buildings.keys():
            return False
        return buildings[building_name].is_unlocked()

    def is_building_visible(building_name):
        if building_name not in buildings.keys():
            return False
        return buildings[building_name].is_visible()

    def load_building(name, title, data = None):
        if name not in buildings.keys():
            buildings[name] = Building(name, title)

        buildings[name].title = title

        if data != None:
            buildings[name].__dict__.update(data)

label load_buildings:
    $ load_building("labs", "Labs", {
        'description': "A building with various labs and maybe a certain special lab for someone.",
        'unlock_conditions': [
            MoneyCondition(1000),
            # LockCondition()
        ]
    })

    $ load_building("sports_field", "Sports Field", {
        'description': "A large area dedicated to various sport activities.",
        'unlock_conditions': [
            MoneyCondition(1000),
            # LockCondition()
        ]
    })

    $ load_building("tennis_court", "Tennis Court", {
        'description': "Something only a reputable school can have. \n" +
            "A tennis court. Of course only used for playing tennis.",
        'unlock_conditions': [
            MoneyCondition(1000),
            # LockCondition()
        ]
    })

    $ load_building("swimming_pool", "Swimming Pool", {
        'description': "The schools pool. One of the favorite places of " +
            "almost every student. Chilling in the cool water, looking at " +
            "the fellow students in their skimpy bathing suits.",
        'unlock_conditions': [
            MoneyCondition(1000),
            # LockCondition()
        ]
    })

    $ load_building("cafeteria", "Cafeteria", {
        'description': "The cafeteria, the place students come together to " +
            "spend their free-time and to eat together.",
        'unlock_conditions': [
            MoneyCondition(1000),
            # LockCondition()
        ]
    })

    $ load_building("bath", "Bath", {
        'description': "The public bath. Here the students can relax and/or wash" +
            "after a long school day.",
        'unlock_conditions': [
            MoneyCondition(1000),
            # LockCondition()
        ]
    })