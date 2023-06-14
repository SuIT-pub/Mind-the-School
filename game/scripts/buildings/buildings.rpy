init python:
    import re
    class Building:
        unlock_conditions = []
        
        def __init__(self, name, title):
            self.name = name
            self.title = title
            self.description = ""
            self.unlocked = False
            self.image_path = "images/journal/empty_image.png"

        def unlock(self):
            self.unlocked = True

        def isUnlocked(self):
            return self.unlocked
        
        def isVisible(self):
            for condition in self.unlock_conditions:
                if condition.is_blocking(None):
                    return False
            return True

        def canBeUnlocked(self):
            for condition in self.unlock_conditions:
                if condition.is_fullfilled(None):
                    continue
                return False

            return True

    def get_visible_buildings():
        output = []

        for building in buildings.values():
            if (building.isVisible() and 
            not building.isUnlocked() and
            building.name not in output):
                output.append(building.name)
                continue
            
        return output

    def get_unlockable_buildings():
        output = []

        for building in buildings.values():
            unlock = building.canBeUnlocked()
            unlocked = building.isUnlocked()

            if (unlock and not unlocked and building.name not in output):
                output.append(building.name)
                continue

        return output

    def get_building(building):
        if building in buildings.keys():
            return buildings[building]
        return None

    def load_building(name, title, data = None):
        if name not in buildings.keys():
            buildings[name] = Building(name, title)

        if data != None:
            buildings[name].__dict__.update(data)

label load_buildings:
    $ load_building("labs", "Labs", {
        'description': "A building with various labs and maybe a certain special lab for someone.",
        'unlock_conditions': [
            MoneyCondition(1000),
            LockCondition()
        ]
    })

    $ load_building("sports_field", "Sports Field", {
        'description': "The sports field",
        'unlock_conditions': [
            MoneyCondition(1000),
            LockCondition()
        ]
    })

    $ load_building("tennis_court", "Tennis Court", {
        'description': "Tennis Court",
        'unlock_conditions': [
            MoneyCondition(1000),
            LockCondition()
        ]
    })

    $ load_building("swimming_pool", "Swimming Pool", {
        'description': "Swimming Pool",
        'unlock_conditions': [
            MoneyCondition(1000),
            LockCondition()
        ]
    })

    $ load_building("cafeteria", "Cafeteria", {
        'description': "Cafeteria",
        'unlock_conditions': [
            MoneyCondition(1000),
            LockCondition()
        ]
    })