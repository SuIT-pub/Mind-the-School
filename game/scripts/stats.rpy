init -6 python:
    import re
    class Stat:
        def __init__(self, name, value):
            self.name = name
            self.value = value
            self.changed_value = 0
            self.image_path = "icons/stat_" + name + "_icon.png"

        def get_value(self):
            return self.value
        
        def get_changed_value(self):
            return self.changed_value

        def set_value(self, value):
            old_value = self.value

            minLimit = get_stat_data(self.name).get_min_limit()
            maxLimit = get_stat_data(self.name).get_max_limit()

            self.value = value
            if self.value < minLimit:
                self.value = minLimit
            if self.value > maxLimit:
                self.value = maxLimit

            delta = math.ceil((self.value - old_value) * 100.0) / 100.0
            self.set_changed_value(delta)

        def set_changed_value(self, value):
            self.changed_value = value
        
        def change_value(self, delta):
            minLimit = get_stat_data(self.name).get_min_limit()
            maxLimit = get_stat_data(self.name).get_max_limit()

            if self.value + delta < minLimit:
                delta = -(self.value - minLimit)
            elif self.value + delta > maxLimit:
                delta = maxLimit - self.value
            change_val = math.ceil(delta * 100.0) / 100.0
            self.value = clamp_stat(math.ceil((self.value + change_val) * 100.0) / 100.0, minLimit, maxLimit)
            self.set_changed_value(change_val)

        def change_value_to(self, value):
            delta = value - self.value
            change_value(delta)

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
            return self.get_display_value() + self.get_display_change()

        def get_display_value(self):
            stat_value = self.get_value() + 0

            if self.name == "inhibition":
                stat_value = 100.0 - stat_value

            return str(stat_value)

        def get_display_change(self):
            global change
            change = self.get_changed_value()

            text = ""

            if (self.name != "inhibition"):
                if change < 0:
                    text = "{color=#ff0000}{size=15}(" + str(change) + "){/size}{/color}"
                elif change > 0:
                    text = "{color=#00ff00}{size=15}(+" + str(change) + "){/size}{/color}"
            else:
                if change < 0:
                    change = -change
                    text = "{color=#ff0000}{size=15}(+" + str(change) + "){/size}{/color}"
                elif change > 0:
                    text = "{color=#00ff00}{size=15}(-" + str(change) + "){/size}{/color}"
            return text

    class Stat_Data:
        def __init__(self, name, title):
            self.name = name
            self.title = title
            self.levels = [0]
            self.images = ["images/journal/empty_image.png"]
            self.descriptions = ["EMPTY"]
            self.description = "test"
            self.min_limit = 0
            self.max_limit = 100

        def _update(self, title, data = None):
            if data != None:
                self.__dict__.update(data)

            self.title = title
            
            if not hasattr(self, 'levels'):
                self.levels = [0]
            if not hasattr(self, 'images'):
                self.images = ["images/journal/empty_image.png"]
            if not hasattr(self, 'descriptions'):
                self.descriptions = ["EMPTY"]
            if not hasattr(self, 'description'):
                self.description = "test"
            if not hasattr(self, 'min_limit'):
                self.min_limit = 0
            if not hasattr(self, 'max_limit'):
                self.max_limit = 100

        def get_min_limit(self):
            return self.min_limit

        def get_max_limit(self):
            return self.max_limit

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
            if level < len(self.descriptions) and level >= 0:
                return self.descriptions[level]
            return "Description missing for level:[level]"

        def get_full_description(self, level):
            return (self.get_description(level) + 
                "\n-------------------------------------------------------\n" + 
                self.description)


    def get_stat_data(stat):
        if not stat in stat_data:
            return None
        return stat_data[stat]
    
    def clamp_stat(value, min = 0, max = 100):
        if (value < min):
            return min
        if (value > max):
            return max
        return value

    def load_stat_data(name, title, data):
        if name not in stat_data.keys():
            stat_data[name] = Stat_Data(name, title)

        stat_data[name]._update(title, data)

label load_stats:
    
    $ load_stat_data("corruption", "Corruption", {
        'description': "The corruption level is a measure of how corrupt the" +
            " students' minds are and how open they are to sexual activity.\n" +
            "\nThe level can be increased by performing sexual activities with" +
            " the students or by using indirect measures like drugs etc.",
        'levels': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'descriptions': [
            "The students are not corrupted.",
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

    $ load_stat_data("inhibition", "Inhibition", {
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

    $ load_stat_data("happiness", "Happiness", {
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

    $ load_stat_data("education", "Education", {
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

    $ load_stat_data("charm", "Charm", {
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

    $ load_stat_data("reputation", "Reputation", {
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

    $ load_stat_data("level", "Level", {
        'description': "The level of the school represents the overall " +
            "progress of the school. Every new level unlocks new "
            "possibilities.\n\nTo increase the level of a school you need to " +
            "fullfill certain criteria like adopting certain rules or " +
            "running certain events.",
        'levels': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'descriptions': [
            "The school has not made any progress yet. You are currently in " +
                "the phase of scouting the school and finding the correct " +
                "measure to start the process.",
            "You unlocked the potential of sexual heaven to the students.\n" +
                "Being prude and absolute unaccepting of the topic before, " +
                "they now opened their mind to new heights even though they " +
                "are still new and fearful of it.",
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
        ],
        'max_limit': 10,
    })

    $ load_stat_data("money", "Money", {
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
        ],
        'max_limit': 1000000000,
    })
    