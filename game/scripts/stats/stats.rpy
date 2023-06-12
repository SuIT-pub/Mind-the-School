init python:
    import re
    class Stat:
        def __init__(self, name, value):
            self.name = name;
            self.value = value
            self.changed_value = 0
            self.image_path = "icons/stat_" + name + "_icon.png"

        def get_value(self):
            return self.value
        
        def get_changed_value(self):
            return self.changed_value

        def set_value(self, value):
            self.value = value

        def set_changed_value(self, value):
            self.changed_value = value
        
        def change_value(self, delta):
            change_val = math.ceil(delta * 100) / 100
            self.value = clamp_stat(math.ceil((self.value + change_val) * 100) / 100)
            self.changed_value = change_val

        def reset_change(self):
            self.changed_value = 0

        def get_level(self):
            return get_stat_data(self.name).get_level(self.value)

        def get_image(self):
            return get_stat_data(self.name).get_image(self.get_level())

        def get_description(self):
            return get_stat_data(self.name).get_description(self.get_level())

        def get_full_description(self):
            return get_stat_data(self.name).get_full_description(self.get_level())

        def display_stat(self):

            stat_value = self.get_value()

            if self.name == "inhibition":
                stat_value = 100 - stat_value

            text = str(stat_value)
            global change
            change = self.get_changed_value()

            if (self.name != "inhibition"):
                if change < 0:
                    text += "{color=#ff0000}{size=15}(" + str(change) + "){/size}{/color}"
                elif change > 0:
                    text += "{color=#00ff00}{size=15}(+" + str(change) + "){/size}{/color}"
            else:
                if change < 0:
                    change = -change
                    text += "{color=#ff0000}{size=15}(+" + str(change) + "){/size}{/color}"
                elif change > 0:
                    text += "{color=#00ff00}{size=15}(-" + str(change) + "){/size}{/color}"

            return text

    class Stat_Data:
        levels = [0]
        images = ["images/journal/empty_image.png"]
        descriptions = ["EMPTY"]
        
        def __init__(self, name, title):
            self.name = name
            self.title = title
            self.description = "test"

        def get_level(self, value):
            count = 0
            for l in self.levels:
                if value < l:
                    return count - 1
                count += 1

            if count >= len(self.levels):
                return len(self.levels) - 1

            return 0
        
        def get_image(self, level):
            if level < len(self.images) and level >= 0:
                return self.images[level]
            return "images/journal/empty_image.png"

        def get_description(self, level):
            print(level)
            print(self.descriptions)
            if level < len(self.descriptions) and level >= 0:
                return self.descriptions[level]
            return "Description missing for level:[level]"

        def get_full_description(self, level):
            return self.get_description(level) + "\n\n" + self.description


    def get_stat_data(stat):
        if not stat in stat_data:
            return None
        return stat_data[stat]


label load_stats:
    if not "corruption" in stat_data.keys():
        $ stat_data["corruption"] = Stat_Data("corruption", "Corruption")
    $ stat_data["corruption"].__dict__.update({
        'description': "corruption",
        'levels': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'descriptions': [
            "level 0",
            "level 1",
            "level 2",
            "level 3",
            "level 4",
            "level 5",
            "level 6",
            "level 7",
            "level 8",
            "level 9",
            "level 10",
        ],
        'images': [
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
        ]
    })

    if not "inhibition" in stat_data.keys():
        $ stat_data["inhibition"] = Stat_Data("inhibition", "Inhibition")
    $ stat_data["inhibition"].__dict__.update({
        'description': "inhibition",
        'levels': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'descriptions': [
            "level 0",
            "level 1",
            "level 2",
            "level 3",
            "level 4",
            "level 5",
            "level 6",
            "level 7",
            "level 8",
            "level 9",
            "level 10",
        ],
        'images': [
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
        ]
    })

    if not "happiness" in stat_data.keys():
        $ stat_data["happiness"] = Stat_Data("happiness", "Happiness")
    $ stat_data["happiness"].__dict__.update({
        'description': "happiness",
        'levels': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'descriptions': [
            "level 0",
            "level 1",
            "level 2",
            "level 3",
            "level 4",
            "level 5",
            "level 6",
            "level 7",
            "level 8",
            "level 9",
            "level 10",
        ],
        'images': [
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
        ]
    })

    if not "education" in stat_data.keys():
        $ stat_data["education"] = Stat_Data("education", "Education")
    $ stat_data["education"].__dict__.update({
        'description': "education",
        'levels': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'descriptions': [
            "level 0",
            "level 1",
            "level 2",
            "level 3",
            "level 4",
            "level 5",
            "level 6",
            "level 7",
            "level 8",
            "level 9",
            "level 10",
        ],
        'images': [
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
        ]
    })

    if not "charm" in stat_data.keys():
        $ stat_data["charm"] = Stat_Data("charm", "Charm")
    $ stat_data["charm"].__dict__.update({
        'description': "charm",
        'levels': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'descriptions': [
            "level 0",
            "level 1",
            "level 2",
            "level 3",
            "level 4",
            "level 5",
            "level 6",
            "level 7",
            "level 8",
            "level 9",
            "level 10",
        ],
        'images': [
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
        ]
    })

    if not "reputation" in stat_data.keys():
        $ stat_data["reputation"] = Stat_Data("reputation", "Reputation")
    $ stat_data["reputation"].__dict__.update({
        'description': "repuation",
        'levels': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'descriptions': [
            "level 0",
            "level 1",
            "level 2",
            "level 3",
            "level 4",
            "level 5",
            "level 6",
            "level 7",
            "level 8",
            "level 9",
            "level 10",
        ],
        'images': [
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
        ]
    })

    if not "level" in stat_data.keys():
        $ stat_data["level"] = Stat_Data("level", "Level")
    $ stat_data["level"].__dict__.update({
        'description': "level",
        'levels': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'descriptions': [
            "level 0",
            "level 1",
            "level 2",
            "level 3",
            "level 4",
            "level 5",
            "level 6",
            "level 7",
            "level 8",
            "level 9",
            "level 10",
        ],
        'images': [
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
        ]
    })

    if not "money" in stat_data.keys():
        $ stat_data["money"] = Stat_Data("money", "Money")
    $ stat_data["money"].__dict__.update({
        'description': "money",
        'levels': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'descriptions': [
            "level 0",
            "level 1",
            "level 2",
            "level 3",
            "level 4",
            "level 5",
            "level 6",
            "level 7",
            "level 8",
            "level 9",
            "level 10",
        ],
        'images': [
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
            "images/journal/empty_image.png",
        ]
    })
    