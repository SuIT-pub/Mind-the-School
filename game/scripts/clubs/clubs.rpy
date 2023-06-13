init python:
    import re
    class Club:
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

        def is_condition_fullfilled(self, condition, school):
            if condition["type"] == "stat":
                stat = condition["stat"]
                value = condition["value"]

                needed_stat = get_stat(value, stat, school)

                if needed_stat != get_school(school).get_stat_string(stat):
                    return False

            elif condition["type"] == "unlocked":
                value = condition["rule"]
                if not rules[value].isUnlocked(school):
                    return False
            elif condition["type"] == "level":
                stat = condition["school"]
                value = condition["value"]

                print("stat: " + stat + " school: " + school)

                if stat == school or stat == "x":
                    level = get_level(value, school)

                    if (level != level_to_string(school)):
                        return False
            elif condition["type"] == "money":
                value = condition["value"]

                if money < value:
                    return False

            return True

    def get_club(club):
        if club in clubs.keys():
            return clubs[club]
        return None
    
    def load_club(name, title):
        if name not in clubs.keys():
            clubs[name] = Club(name, title)

    def load_club(name, title, data):
        load_club(name, title)
        clubs[name].__dict__.update(data)

label load_clubs:
    $ load_club("test_club", "Test Club",{
        'description': "A Club for testing",
        'unlock_conditions': [
            {
                "type": "stat",
                "stat": "inhibition",
                "school": "x",
                "value": "1+",
                "blocking": False,
            },
        ]
    })