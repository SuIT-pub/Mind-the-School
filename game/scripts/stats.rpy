init -6 python:
    from typing import Dict, Any
    import re

    class Stat:
        """
        This class represents a stat of a Character Object.

        ### Attributes:
        1. type: str
            - The type of the stat.
        2. value: num
            - The current value of the stat.
        3. changed_value: num
            - The change of the stat since the last update.
        4. image_path: str
            - The path to the icon image of the stat.

        ### Methods:
        1. get_name() -> str
            - Returns the name of the stat.
        2. get_value() -> num
            - Returns the current value of the stat.
        3. get_changed_value() -> num
            - Returns the change of the stat since the last update.
        4. set_value(value: num, level: int = 10)
            - Sets the value of the stat to the given value.
            - The value is clamped between the min and max limit of the stat.
            - The change of the stat is calculated and saved.
        5. set_changed_value(value: num)
            - Sets the change of the stat to the given value.
        6. change_value(delta: num, level: int = 10)
            - Changes the value of the stat by the given delta.
            - The value is clamped between the min and max limit of the stat.
            - The change of the stat is calculated and saved.
        7. change_value_to(value: num, level: int = 10)
            - Changes the value of the stat to the given value.
            - The value is clamped between the min and max limit of the stat.
            - The change of the stat is calculated and saved.
        8. reset_change()
            - Resets the change of the stat to 0.
        9. get_level() -> int
            - Returns the data level of the stat. See Stat_Data for more information.
        10. get_image() -> str
            - Returns the path to the image representing the stat for overview in the journal. See Stat_Data for more information.
        11. get_description() -> str
            - Returns the description of the stat for overview in the journal. See Stat_Data for more information.
        12. get_full_description() -> str
            - Returns the full description of the stat for the journal. See Stat_Data for more information.
        13. display_stat() -> str
            - Returns the stat as a string for display in the journal.
        14. get_display_value() -> str
            - Returns the value of the stat as a string for display in the journal.
        15. get_display_change() -> str
            - Returns the change of the stat as a string for display in the journal.

        ### Parameters:
        1. type: str
            - The type of the stat.
        2. value: num
            - The current value of the stat.
        """

        def __init__(self, type: str, value: num):
            self.type = type
            self.value = value
            self.changed_value = 0
            self.image_path = "icons/stat_" + str(type) + "_icon.webp"

        def _repair(self) -> bool:
            if not hasattr(self, 'type') and hasattr(self, 'image_path'):
                stat_type = re.sub(r'icons/stat_', '', self.image_path)
                stat_type = re.sub(r'_icon.webp', '', stat_type)
                self.type = stat_type
                return True
            return False

        def get_image_path(self):
            if self.image_path.endswith('.png'):
                self.image_path = re.sub(r'\.png$', '.webp', self.image_path)
            return self.image_path


        def get_name(self) -> str:
            """
            Returns the name of the stat.

            ### Returns:
            1. str
                - The name of the stat.
            """

            if not hasattr(self, 'type'):
                self.type = ""

            return self.type

        def get_value(self) -> num:
            """
            Returns the current value of the stat.

            ### Returns:
            1. num
                - The current value of the stat.
            """

            return self.value
        
        def get_changed_value(self) -> num:
            """
            Returns the change of the stat since the last update.

            ### Returns:
            1. num
                - The change of the stat since the last update.
            """

            return self.changed_value

        def set_value(self, value: num, level: int = 10):
            """
            Sets the value of the stat to the given value.

            ### Parameters:
            1. value: num
                - The value to set the stat to.
            2. level: int (default 10)
                - The level of the school. This is used to calculate the min and max limit of the stat.
            """

            old_value = self.value

            minLimit = Stat_Data[self.type].get_min_limit()
            maxLimit = Stat_Data[self.type].get_max_limit()

            # self.value = clamp_value(round(value, 2), minLimit, maxLimit)
            self.value = clamp_stat_value(round(value, 2), self.type, level, minLimit, maxLimit)

            delta = round(self.value - old_value, 2)
            self.set_changed_value(delta)

        def set_changed_value(self, value: num):
            """
            Sets the change of the stat to the given value.

            ### Parameters:
            1. value: num
                - The value to set the change of the stat to.
            """

            self.changed_value = value

        def add_changed_value(self, value: num):
            """
            Adds the given value to the change of the stat.

            ### Parameters:
            1. value: num
                - The value to add to the change of the stat.
            """

            self.changed_value += value
        
        def change_value(self, delta: num, level: int = 10):
            """
            Changes the value of the stat by the given delta.

            ### Parameters:
            1. delta: num
                - The value to change the stat by.
            2. level: int (default 10)
                - The level of the school. This is used to calculate the min and max limit of the stat.
            """

            minLimit = Stat_Data[self.type].get_min_limit()
            maxLimit = Stat_Data[self.type].get_max_limit()

            if self.value + delta < minLimit:
                delta = -(self.value - minLimit)
            elif self.value + delta > maxLimit:
                delta = maxLimit - self.value

            old_value = self.value

            change_val = math.ceil(delta * 100.0) / 100.0
            self.value = clamp_stat_value(round(self.value + change_val, 2), self.type, level, minLimit, maxLimit)

            change_val = round(self.value - old_value, 2)

            self.add_changed_value(change_val)

        def change_value_to(self, value: num, level: int = 10):
            """
            Changes the value of the stat to the given value.

            ### Parameters:
            1. value: num
                - The value to change the stat to.
            2. level: int (default 10)
                - The level of the school. This is used to calculate the min and max limit of the stat.
            """

            delta = value - self.value
            change_value(delta, level)

        def reset_change(self):
            """
            Resets the change of the stat to 0.
            """

            self.changed_value = 0

        def get_level(self) -> int:
            """
            Returns the data level of the stat. See Stat_Data for more information.

            ### Returns:
            1. int
                - The data level of the stat.
            """

            return Stat_Data[self.type].get_level(self.value)

        def get_image(self) -> str:
            """
            Returns the path to the image representing the stat for overview in the journal. See Stat_Data for more information.

            ### Returns:
            1. str
                - The path to the image representing the stat for overview in the journal.
            """

            return Stat_Data[self.type].get_image(self.get_level())

        def get_description(self) -> str:
            """
            Returns the description of the stat for overview in the journal. See Stat_Data for more information.

            ### Returns:
            1. str
                - The description of the stat for overview in the journal.
            """

            return Stat_Data[self.type].get_description(self.get_level())

        def get_full_description(self) -> str:
            """
            Returns the full description of the stat for the journal. See Stat_Data for more information.

            ### Returns:
            1. str
                - The full description of the stat for the journal.
                - The full description consists of the description for the current level and the general description of the stat.
            """

            return Stat_Data[self.type].get_full_description(self.get_level())

        def display_stat(self) -> str:
            """
            Returns the stat as a string for display in the journal.

            ### Returns:
            1. str
                - The stat as a string for display in the journal.
                - The string consists of the value of the stat and the change of the stat.
            """

            return self.get_display_value() + self.get_display_change()

        def get_display_value(self) -> str:
            """
            Returns the value of the stat as a string for display in the journal.

            ### Returns:
            1. str
                - The value of the stat as a string for display in the journal.
            """

            stat_value = self.get_value() + 0

            if self.get_name() == MONEY:
                stat_value = int(stat_value)

            return str(stat_value)

        def get_display_change(self) -> str:
            """
            Returns the change of the stat as a string for display in the journal.

            ### Returns:
            1. str
                - The change of the stat as a string for display in the journal.
            """

            global change
            change = self.get_changed_value()

            if self.get_name() == MONEY:
                change = int(change)

            text = ""

            if (self.get_name() != INHIBITION):
                if change < 0:
                    text = "{color=#a00000}{size=15}(" + str(change) + "){/size}{/color}"
                elif change > 0:
                    text = "{color=#00a000}{size=15}(+" + str(change) + "){/size}{/color}"
            else:
                if change > 0:
                    text = "{color=#a00000}{size=15}(+" + str(change) + "){/size}{/color}"
                elif change < 0:
                    change = -change
                    text = "{color=#00a000}{size=15}(-" + str(change) + "){/size}{/color}"
            return text

    class Stat_Data:
        """
        This class represents the data of a stat.
        This class is used to store background information about a stat.
        To make it changeable for existing save games and centralised for all stats, the data has been extracted from the stat-class.

        ### Attributes:
        1. type: str
            - The type of the stat.
        2. title: str
            - The title of the stat. This is the name that is used on displayables
        3. levels: List[int]
            - The levels of the stat.
            - Stats are separated into different levels. Each level has a different image and description.
        4. images: List[str]
            - The images of the stat. Depending on the level of the stat, a different image is used.
        5. descriptions: List[str]
            - The descriptions of the stat. Depending on the level of the stat, a different description is used.
        6. description: str
            - The general description of the stat.
        7. min_limit: num
            - The minimum limit of the stat.
        8. max_limit: num
            - The maximum limit of the stat.

        ### Methods:
        1. __class_getitem__(key: str) -> Stat_Data
            - Returns the Stat_Data object with the given key.
        2. _update(title: str, data: Dict[str, Any] = None)
            - Updates the data of the stat.
            - If data is None, the data is not updated.
        3. get_title() -> str
            - Returns the title of the stat.
        4. get_min_limit() -> int
            - Returns the minimum limit of the stat.
        5. get_max_limit() -> int
            - Returns the maximum limit of the stat.
        6. get_level(value: int) -> int
            - Returns the level of the stat for the given value.
        7. get_image(level: int) -> str
            - Returns the image of the stat for the given level.
        8. get_description(level: int) -> str
            - Returns the description of the stat for the given level.
        9. get_full_description(level: int) -> str
            - Returns the full description of the stat for the given level.
        10. clamp_stat_value(value: num, stat: str, level: int, min: num = 0, max: num = 100) -> num
            - Clamps the given value between the min and max limit of the stat.
        11. clamp_value(value: num, min: num = 0, max: num = 100) -> num
            - Clamps the given value between the given min and max value.
        12. load_stat_data(name: str, title: str, data: Dict[str, Any])
            - Loads and updates the data of the stat.
            - If the stat does not exist, a new stat is created.
        13. get_stat_levels(value: str) -> num
            - Returns the level of the stat for the given value.
        """

        def __init__(self, type: str, title: str):
            self.type = type
            self.title = title
            self.levels = [0]
            self.images = ["images/journal/empty_image.webp"]
            self.descriptions = ["EMPTY"]
            self.description = "test"
            self.min_limit = 0
            self.max_limit = 100

        def __class_getitem__(cls, key: str) -> Stat_Data:
            if not key in stat_data.keys():
                return None
            return stat_data[key]

        def _update(self, title: str, data: Dict[str, Any] = None):
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

        def get_title(self) -> str:
            """
            Returns the title of the stat.
            The title is the name that is used on displayables.

            ### Returns:
            1. str
                - The title of the stat.
            """

            return self.title

        def get_min_limit(self) -> int:
            """
            Returns the minimum limit of the stat.

            ### Returns:
            1. int
                - The minimum limit of the stat.
            """

            return self.min_limit

        def get_max_limit(self) -> int:
            """
            Returns the maximum limit of the stat.

            ### Returns:
            1. int
                - The maximum limit of the stat.
            """
            return self.max_limit

        def get_level(self, value: int) -> int:
            """
            Returns the level of the stat for the given value.

            ### Parameters:
            1. value: int
                - The value to get the level for.

            ### Returns:
            1. int
                - The level of the stat for the given value.
            """

            
            closest_value = len(self.levels) - 1
            for i, val in enumerate(self.levels):
                if val >= value and val < self.levels[closest_value]:
                    closest_value = i

            # count = 0
            # for l in self.levels:
            #     if value <= l:
            #         return count - 1
            #     count += 1

            # if count >= len(self.levels):
            #     return len(self.levels) - 1

            return closest_value
        
        def get_image(self, level: int) -> str:
            """
            Returns the image of the stat for the given level.

            ### Parameters:
            1. level: int
                - The level to get the image for.

            ### Returns:
            1. str
                - The image of the stat for the given level.
            """

            if level < len(self.images) and level >= 0:
                return self.images[level]
            return "images/journal/empty_image.webp"

        def get_description(self, level: int) -> str:
            """
            Returns the description of the stat for the given level.

            ### Parameters:
            1. level: int
                - The level to get the description for.

            ### Returns:
            1. str
                - The description of the stat for the given level.
            """

            if level < len(self.descriptions) and level >= 0:
                return self.descriptions[level]
            return "Description missing for level:" + str(level)

        def get_full_description(self, level: int) -> str:
            """
            Returns the full description of the stat for the given level.
            The full description consists of the description for the current level and the general description of the stat.

            ### Parameters:
            1. level: int
                - The level to get the full description for.

            ### Returns:
            1. str
                - The full description of the stat for the given level.
            """

            return (self.get_description(level) + 
                "\n-------------------------------------------------------\n" + 
                self.description)

    def get_stat_icon(stat: str, is_white: bool = False) -> str:
        """
        Returns the path to the icon image of the stat.

        ### Parameters:
        1. stat: str
            - The type of the stat.

        ### Returns:
        1. str
            - The path to the icon image of the stat.
        """

        if is_white:
            return "{image=icons/stat_" + str(stat) + "_icon_white.webp}"
        else:
            return "{image=icons/stat_" + str(stat) + "_icon.webp}"

    def clamp_stat_value(value: num, stat: str, level: int, min: num = 0, max: num = 100) -> num:
        """
        Clamps the given value between the min and max limit of the stat.
        The min and max limit are calculated based on the level of the school.
        Exceptions are the corruption and inhibition stat. 
        For these stats the min and max limit are calculated based on the level of the school.

        ### Parameters:
        1. value: num
            - The value to clamp.
        2. stat: str
            - The type of the stat.
        3. level: int
            - The level of the school. This is used to calculate the min and max limit of the stat.
        4. min: num (default 0)
            - The minimum limit of the stat.
        5. max: num (default 100)
            - The maximum limit of the stat.

        ### Returns:
        1. num
            - The clamped value.
        """

        if stat == CORRUPTION:
            return clamp_value(value, min, max - level * (max / 10))
        elif stat == INHIBITION:
            return clamp_value(value, 100 - (level * (max / 10)), max)
        else:
            return clamp_value(value, min, max)


    def clamp_value(value: num, min: num = 0, max: num = 100) -> num:
        """
        Clamps the given value between the given min and max value.

        ### Parameters:
        1. value: num
            - The value to clamp.
        2. min: num (default 0)
            - The minimum limit of the stat.
        3. max: num (default 100)
            - The maximum limit of the stat.

        ### Returns:
        1. num
            - The clamped value.
        """

        if (value < min):
            return min
        if (value > max):
            return max
        return value

    def load_stat_data(name: str, title: str, data: Dict[str, Any]):
        """
        Loads and updates the data of the stat.
        If the stat does not exist, a new stat is created.

        ### Parameters:
        1. name: str
            - The type of the stat.
        2. title: str
            - The title of the stat. This is the name that is used on displayables
        3. data: Dict[str, Any]
            - The data of the stat.
        """

        if name not in stat_data.keys():
            stat_data[name] = Stat_Data(name, title)
        stat_data[name]._update(title, data)

    def get_stat_levels(value: str) -> num:
        """
        Returns a value based on the different constants inserted.

        ### Parameters:
        1. value: str
            - The value to get the level for.
            - The value can be a constant or a string with the format "dec_[constant]".
            - The constant can be "tiny", "small", "medium", "large" or "giant".
            - The dec_ prefix can be used to invert the value into its negative equivalent.

        ### Returns:
        1. num
            - The value based on the different constants inserted.
        """

        neg = 1

        if "dec_" in value:
            value = value.replace("dec_", "")
            neg = -1

        if value == "tiny":
            return round(random.uniform(0.1, 0.3), 2) * neg
        elif value == "small":
            return round(random.uniform(0.3, 0.5), 2) * neg
        elif value == "medium":
            return round(random.uniform(0.5, 1.0), 2) * neg
        elif value == "large":
            return round(random.uniform(1.0, 3.0), 2) * neg
        elif value == "giant":
            return round(random.uniform(3.0, 7.0), 2) * neg
        else:
            return round(random.uniform(0.1, 0.8), 2) * neg

label load_stats ():
    
    $ load_stat_data(CORRUPTION, "Corruption", {
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

    $ load_stat_data(INHIBITION, "Inhibition", {
        'description': "The inhibition level shows how the students feel in their own bodies.\n" +
            "The better they feel in their own bodies the more they open up and the less they feel embarrassed about showing their bodies.\n" +
            "\n The level can be increased by bringing the student in embarrassing situations that leaves them exposed or" +
            " that presents their bodies in other ways.",
        'levels': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'descriptions': [
            "The students love to be naked all the time.",
            "The students like to barely wear anything.",
            "The students love to show a lot of skin.",
            "The students love to show a bit more skin.",
            "The students show a bit more of their skin on a regular basis.",
            "The students like to present their bodies.",
            "The students like to show a bit of skin.",
            "The students don't mind showing a little bit more skin.",
            "The students don't mind showing a little bit skin.",
            "The students don't like to show skin.",
            "The students hate to show skin.",
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

    $ load_stat_data(HAPPINESS, "Happiness", {
        'description': "Happiness describes how happy the students are to be at this school.\n" + 
            "The happier they are, the less likely they are to cause problems.\n"
            "\nEvents that make students happy, raises the overall happiness of all students."
            " It can be the simple things like praising someone or giving them a gift.\n"
            "On the other hand situations that makes the students uncomfortable lowers the students happiness.",
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

    $ load_stat_data(EDUCATION, "Education", {
        'description': "Education measures how good the students are at school.\n" +
            "The level of education is an important factor and influences the monthly budget the " +
            "goodwill of the authorities and the willingness of potential contractors to establish a contract.\n" +
            "\nThe Education can be raised by making sure the students have a good surrounding where they can learn " +
            "and by making sure the students attend the classes.",
        'levels': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'descriptions': [
            "A chimpanzee is more intelligent than these students.",
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

    $ load_stat_data(CHARM, "Charm", {
        'description': "Charm describes how other people perceive a students as a person. " +
            "The charm is influenced by factors like fitness, likability, looks and how gentle they are.\n" +
            "\nThe charm can be improved by working on the fitness, working on the character, " +
            "or by social interaction with other people.",
        'levels': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'descriptions': [
            "The students are the extreme opposite of charming.",
            "A hobgoblin is more charming than these students.",
            "The students are socially incompetent.",
            "The students are rather unsocial.",
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

    $ load_stat_data(REPUTATION, "Reputation", {
        'description': "This displays the reputation of you and the school. " +
            "The reputation directly influences the goodwill of the authorities towards you and the school " + 
            "and the monthly budget your school receives.",
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

    $ load_stat_data(LEVEL, "Level", {
        'description': "The level of the school represents the overall " +
            "progress of the school. Every new level unlocks new "
            "possibilities.\n\nTo increase the level of a school you need to " +
            "fulfil certain criteria like adopting certain rules or " +
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

    $ load_stat_data(MONEY, "Money", {
        'description': "The money is used to purchase upgrade for the school and to pay for expenses.\n" +
            "You have to pay for all of that with your own budget, but you get a monthly budget from the authorities.\n\n" +
            "Of course, you don't get much. You have to make sure that you don't run out of money. "+
            "You can also earn money by working in your office. Maybe you find another way...",
        'max_limit': 1000000000,
    })
    