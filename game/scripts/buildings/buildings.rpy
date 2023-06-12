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

        def is_condition_fullfilled(self, condition):
            if condition["type"] == "stat":
                stat = condition["stat"]
                value = condition["value"]

                needed_stat = get_stat(value, stat, "mean_school")

                if needed_stat != get_school("mean_school").get_stat_string(stat):
                    return False

            elif condition["type"] == "unlocked":
                value = condition["rule"]
                if not rules[value].isUnlocked("mean_school"):
                    return False
            elif condition["type"] == "level":
                stat = condition["school"]
                value = condition["value"]

                print("stat: " + stat + " school: mean_school")

                if stat == school or stat == "x":
                    level = get_level(value, "mean_school")

                    if (level != level_to_string("mean_school")):
                        return False
            elif condition["type"] == "money":
                value = condition["value"]

                if money < value:
                    return False

            return True
    
    def get_building(building):
        if building in buildings.keys():
            return buildings[building]
        return None
    
label load_buildings:
    if "labs" not in buildings.keys():
        $ buildings["labs"] = Building("labs", "Labs")
    $ buildings["labs"].__dict__.update({
        'description': "A building with various labs and maybe a certain special lab for someone.",
        'unlock_conditions': [
            {
                "type": "money",
                "value": "1000"
            }
        ]
    })

    if "sports_field" not in buildings.keys():
        $ buildings["sports_field"] = Building("sports_field", "Sports Field")
    $ buildings["sports_field"].__dict__.update({
        'description': "The sports field",
        'unlock_conditions': [
            {
                "type": "money",
                "value": "1000"
            }
        ]
    })

    if "tennis_court" not in buildings.keys():
        $ buildings["tennis_court"] = Building("tennis_court", "Tennis Court")
    $ buildings["tennis_court"].__dict__.update({
        'description': "Tennis Court",
        'unlock_conditions': [
            {
                "type": "money",
                "value": "1000"
            }
        ]
    })

    if "swimming_pool" not in buildings.keys():
        $ buildings["swimming_pool"] = Building("swimming_pool", "Swimming Pool")
    $ buildings["swimming_pool"].__dict__.update({
        'description': "Swimming Pool",
        'unlock_conditions': [
            {
                "type": "money",
                "value": "1000"
            }
        ]
    })

    if "cafeteria" not in buildings.keys():
        $ buildings["cafeteria"] = Building("cafeteria", "Cafeteria")
    $ buildings["cafeteria"].__dict__.update({
        'description': "Cafeteria",
        'unlock_conditions': [
            {
                "type": "money",
                "value": "1000"
            }
        ]
    })