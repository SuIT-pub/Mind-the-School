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

            # self.value = clamp_stat(round(value, 2), minLimit, maxLimit)
            self.value = clamp_stat(round(value, 2), minLimit, maxLimit)

            delta = round(self.value - old_value, 2)
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
            self.value = clamp_stat(round(self.value + change_val, 2), minLimit, maxLimit)
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
                if change > 0:
                    text = "{color=#ff0000}{size=15}(+" + str(change) + "){/size}{/color}"
                elif change < 0:
                    change = -change
                    text = "{color=#00ff00}{size=15}(-" + str(change) + "){/size}{/color}"
            return text

        

    class Stat_Data:
        def __init__(self, name, title):
            self.name = name
            self.title = title
            self.levels = [0]
            self.images = ["images/journal/empty_image.webp"]
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
                self.images = ["images/journal/empty_image.webp"]
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
            return "images/journal/empty_image.webp"

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
            "There is rarely anything more pure than these students.",
            "The students are not corrupted.",
            "The students have tasted the light sweetness of corruption.",
            "The students feel a bit more safe to talk about certain topics.",
            "The students don't mind talking about sexual topics.",
            "The students feel more open towards more intimate interactions.",
            "The students like to touch each other more intimately.",
            "The students don't see the need to restrain themself in their sexuality.",
            "The students love to touch each other and play fun games.",
            "The students think of almost nothing but sex.",
            "Sex became the default for the students. There is almost nothing and nobody they wouldn't do.",
        ],
        'images': [
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
        ]
    })

    $ load_stat_data("inhibition", "Inhibition", {
        'description': "The inhibition level shows how the students feel in their own bodies.\n" +
            "The better they feel in their own bodies the more they open up and the less they feel embarrased about showing their bodies.\n" +
            "\n The level can be increased by bringing the student in embarrasing situations that leaves them exposed or" +
            " that presents their bodies in other ways.",
        'levels': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'descriptions': [
            "The students hate to show skin.",
            "The students don't like to show skin.",
            "The students don't mind showing a little bit skin.",
            "The students don't mind showing a little bit more skin.",
            "The students like to show a bit of skin.",
            "The students like to present their bodies.",
            "The students show a bit more of their skin on a regular basis.",
            "The students love to show a bit more skin.",
            "The students love to show a lot of skin.",
            "The students like to barely wear anything.",
            "The students love to be naked all the time.",
        ],
        'images': [
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
        ]
    })

    $ load_stat_data("happiness", "Happiness", {
        'description': "Happiness descripes how happy the students are to be at this school.\n" + 
            "The happier they are, the less likely they are to cause problems.\n"
            "\nEvents that make students happy, raises the overall happiness of all students."
            " It can be the simple things like praising someone or giving them a gift.\n"
            "On the other hand situations that makes the students uncomforable lowers the students happiness.",
        'levels': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'descriptions': [
            "The students are rioting.",
            "The students are very dissatisfied.",
            "The students are unhappy.",
            "The students are rather dissatisfied.",
            "The students are not feeling well.",
            "The students are not unhappy.",
            "The students feel rather good.",
            "The students are quite happy.",
            "The students are happy.",
            "The students are very happy.",
            "For the students, this school is a paradise.",
        ],
        'images': [
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
        ]
    })

    $ load_stat_data("education", "Education", {
        'description': "Education measures how good the students are at school.\n" +
            "The level of education is an important factor and influences the monthly budget the " +
            "goodwill of the authorities and the willingness of potential contractors to establish a contract.\n" +
            "\nThe Education can be raised by making sure the students have a good surrounding where they can learn " +
            "and by making sure the students attend the classes.",
        'levels': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'descriptions': [
            "A shimpanzee is more intelligent than these students.",
            "They fail through most of the exams.",
            "The students are very bad at school.",
            "The students are rather bad at school.",
            "The students are below average.",
            "The academic performance is average.",
            "The students are just above average.",
            "The students are quite good at school.",
            "The students are pretty smart.",
            "The students are very smart.",
            "Albert Einstein? More like your students.",
        ],
        'images': [
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
        ]
    })

    $ load_stat_data("charm", "Charm", {
        'description': "Charm describes how other people percieve a students as a person. " +
            "The charm is influenced by factors like fitness, likability, how gentle they are and looks.\n" +
            "\nThe charm can be improved by working on the fitness, working on the character, " +
            "or by socially interaction with other people.",
        'levels': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'descriptions': [
            "The students are the extreme opposite of charming.",
            "A hobgoblin is more charming than these students.",
            "The students are socially incompetent.",
            "The students are rather unsozial.",
            "The students looks and social interaction are just below average.",
            "The students looks and social interaction are average.",
            "The students looks and social interaction are just above average.",
            "The students are rather social.",
            "The students are socially competent.",
            "The students are very charming.",
            "Nobody is more charming than your students. A bunch of sexy and social gigastacys.",
        ],
        'images': [
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
        ]
    })

    $ load_stat_data("reputation", "Reputation", {
        'description': "This displayes the reputation of you and the school. " +
            "The reputation directly influences the goodwill of the authorities towards you and the school " + 
            "and the monthly budget your school recieves.",
        'levels': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'descriptions': [
            "How the hell are you still in charge of this school?",
            "The school is very unpopular.",
            "The school is pretty unpopular and are very unsatisfied with your work.",
            "The people are very unsatisfied with your work.",
            "The officials are a bit unsatisfied with your work.",
            "You are doing a decent job and the people are aware of it.",
            "The officials are quite satisfied with your work.",
            "The people are satisfied with your job.",
            "The people are very satisfied with your work and like your school.",
            "The public is extremely happy with your work and your school enjoys quite the popularity.",
            "People think you are the best that could have happened to the school.",
        ],
        'images': [
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
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
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
        ],
        'max_limit': 10,
    })

    $ load_stat_data("money", "Money", {
        'description': "money",
        'levels': [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000],
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
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
            "images/journal/empty_image.webp",
        ],
        'max_limit': 1000000000,
    })
    