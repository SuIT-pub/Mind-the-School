init -6 python:
    import re
    class Club:
        def __init__(self, name, title):
            self._name = name
            self._title = title
            self._description = ""
            self._image_path_alt = "images/journal/empty_image.png"
            self._image_path = "images/journal/empty_image.png"
            self._unlocked = {
                "high_school": False,
                "middle_school": False,
                "elementary_school": False
            }
            self._unlock_conditions = []

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
            if not hasattr(self, '_unlocked'):
                self._unlocked = {
                    "high_school": False,
                    "middle_school": False,
                    "elementary_school": False,
                }
            if not hasattr(self, '_unlock_conditions'):
                self._unlock_conditions = []

        def get_name(self):
            return self._name

        def get_title(self):
            return self._title

        def get_type(self):
            return "club"

        def get_description(self):
            return self._description

        def get_image(self, school, level):
            for i in reversed(range(0, level + 1)):
                image = self._image_path.replace("{school}", school).replace("{level}", str(i))
                if renpy.exists(image):
                    return image
            for i in range(0, 10):
                image = self._image_path.replace("{school}", school).replace("{level}", str(i))
                if renpy.exists(image):
                    return image
            return self._image_path_alt

        def get_full_image(self, school, level):
            image = self.get_image(school, level)
            full_image = image.replace(".", "_full.")

            if renpy.exists(full_image):
                return full_image
            return None


        def unlock(self, school, unlock = True):
            if school in self._unlocked:
                self._unlocked[school] = unlock

        def is_unlocked(self, school):
            if school not in self._unlocked.keys():
                return False
            return self._unlocked[school]

        def is_visible(self, school):
            for condition in self._unlock_conditions:
                if condition.is_blocking(school):
                    return False
            return True

        def can_be_unlocked(self, school):
            if school not in schools.keys():
                return False

            for condition in self._unlock_conditions:
                if condition.is_fullfilled(school):
                    continue
                return False

            return True

        def get_list_conditions(self):
            output = []
            for condition in self._unlock_conditions:
                if not condition.is_set_blocking() and condition.display_in_list:
                    output.append(condition)

            return output

        def get_desc_conditions(self):
            output = []
            for condition in self._unlock_conditions:
                if not condition.is_set_blocking() and condition.display_in_desc:
                    output.append(condition)

            return output


    #############################################
    # Clubs Global Methods
    
    def get_unlocked_clubs_by_school(school):
        output = []

        for club in clubs.values():
            if club.is_unlocked(school) and club.get_name() not in output:
                output.append(club.get_name())
        
        return output


    def get_visible_locked_clubs_by_school(school):
        output = []

        for club in clubs.values():
            if (club.is_visible(school) and 
            not club.is_unlocked(school) and
            club.get_name() not in output):
                output.append(club.get_name())
                continue

        return output

    def get_visible_unlocked_clubs_by_school(school):
        output = []

        for club in clubs.values():
            if (club.is_visible(school) and 
            club.is_unlocked(school) and
            club.get_name() not in output):
                output.append(club.get_name())
                continue

        return output

    def get_visible_clubs_by_school(school, include_unlocked = False):
        output = []

        for club in clubs.values():
            if (club.is_visible(school) and 
            ((not club.is_unlocked(school) and not include_unlocked) or include_unlocked) and
            club.get_name() not in output):
                output.append(club.get_name())
                continue

        return output

    def get_visible_unlocked_clubs():
        output = []

        for club in clubs.values():
            if (club.is_visible("high_school") and 
            club.is_unlocked("high_school") and
            club.get_name() not in output):
                output.append(club.get_name())
                continue
            
            if loli_content >= 1:
                if (club.is_visible("middle_school") and 
                club.is_unlocked("middle_school") and
                club.get_name() not in output):
                    output.append(club.get_name())
                    continue

            if loli_content == 2:
                if (club.is_visible("elementary_school") and 
                club.is_unlocked("elementary_school") and
                club.get_name() not in output):   
                    output.append(club.get_name())
                    continue

        return output

    def get_visible_locked_clubs():
        output = []

        for club in clubs.values():
            if (club.is_visible("high_school") and 
            not club.is_unlocked("high_school") and
            club.get_name() not in output):
                output.append(club.get_name())
                continue
            
            if loli_content >= 1:
                if (club.is_visible("middle_school") and 
                not club.is_unlocked("middle_school") and
                club.get_name() not in output):
                    output.append(club.get_name())
                    continue

            if loli_content == 2:
                if (club.is_visible("elementary_school") and 
                not club.is_unlocked("elementary_school") and
                club.get_name() not in output):   
                    output.append(club.get_name())
                    continue

        return output

    def get_visible_clubs(include_unlocked = False):
        output = []

        for club in clubs.values():
            if (club.is_visible("high_school") and 
            ((not club.is_unlocked("high_school") and not include_unlocked) or include_unlocked) and
            club.get_name() not in output):
                output.append(club.get_name())
                continue
            
            if loli_content >= 1:
                if (club.is_visible("middle_school") and 
                ((not club.is_unlocked("middle_school") and not include_unlocked) or include_unlocked) and
                club.get_name() not in output):
                    output.append(club.get_name())
                    continue

            if loli_content == 2:
                if (club.is_visible("elementary_school") and 
                ((not club.is_unlocked("elementary_school") and not include_unlocked) or include_unlocked) and
                club.get_name() not in output):   
                    output.append(club.get_name())
                    continue

        return output

    def get_unlockable_clubs():
        output = []

        for club in clubs.values():
            high_unlock = club.can_be_unlocked("high_school")
            high_unlocked = club.is_unlocked("high_school")

            if (high_unlock and 
            not high_unlocked and 
            club.get_name() not in output):
                output.append(club.get_name())
                continue

            if loli_content >= 1:
                middle_unlock = club.can_be_unlocked("middle_school")
                middle_unlocked = club.is_unlocked("middle_school")

                if (middle_unlock and 
                not middle_unlocked and 
                club.get_name() not in output):
                    output.append(club.get_name())
                    continue

            if loli_content == 2:
                elementary_unlock = club.can_be_unlocked("elementary_school")
                elementary_unlocked = club.is_unlocked("elementary_school")

                if (elementary_unlock and 
                not elementary_unlocked and 
                club.get_name() not in output):
                    output.append(club.get_name())
                    continue

        return output

    def get_unlockable_clubs_by_school(school):
        output = []

        for club in clubs.values():
            unlock = club.can_be_unlocked(school)
            unlocked = club.is_unlocked(school)

            if (unlock and not unlocked and club.get_name() not in output):
                output.append(club.get_name())
                continue

        return output

    def get_club(club):
        if club in clubs.keys():
            return clubs[club]
        return None
    
    def is_club_unlocked(club_name, school):
        if club_name not in clubs.keys():
            return False
        return clubs[club_name].is_unlocked(school)

    def is_club_visible(club_name, school):
        if club_name not in clubs.keys():
            return False
        return clubs[club_name].is_visible(school)

    def load_club(name, title, data = None):
        if name not in clubs.keys():
            clubs[name] = Club(name, title)

        clubs[name]._update(title, data)

    def remove_club(name):
        if name in clubs.keys():
            del(clubs[name])

label load_clubs:
    $ load_club("masturbation_club", "Masturbation Club", {
        '_description': "Here students cum together (pun intended) to " +
            "collectively masturbate and explore new ways to satsify " +
            "themselves.\nA nice place for students to socialize and to " +
            "get some time out from the stressy school life.",
        '_unlock_conditions': [
            # LevelCondition("5+"),
            LockCondition(),
        ],
        '_image_path': 'images/journal/clubs/masturbation_club.png',
        '_image_path_alt': 'images/journal/clubs/masturbation_club.png',
    })

    $ load_club("exhibitionism_club", "Exhibitionism Club", {
        '_description': "The club to celebrate the art that is the human body. " +
            "Here students come together to engage in the thrill seeking " +
            "activity of presenting their nude bodies in public.",
        '_unlock_conditions': [
            # LevelCondition("5+"),
            LockCondition(),
        ],
        '_image_path': 'images/journal/clubs/exhibitionism_club.png',
        '_image_path_alt': 'images/journal/clubs/exhibitionism_club.png',
    })

    $ load_club("cosplay_club", "Cosplay Club", {
        '_description': "Here students engage costume crafting and cosplaying.",
        '_unlock_conditions': [
            # LevelCondition("2+"),
            LockCondition(),
        ],
        '_image_path': 'images/journal/clubs/cosplay_club.png',
        '_image_path_alt': 'images/journal/clubs/cosplay_club.png',
    })

    $ load_club("cheerleading_club", "Cheerleading Club", {
        '_description': "A sports club for training cheerleading and for" +
            "exploring new ways to cheer and motivate the teams.",
        '_unlock_conditions': [
            # LevelCondition("2+"),
            LockCondition(),
        ],
        '_image_path': 'images/journal/clubs/cheerleading_club_{school}_{level}.png',
        '_image_path_alt': 'images/journal/clubs/cheerleading_club_high_school_2.png',
    })

    $ load_club("porn_club", "Porn Club", {
        '_description': "An Arts and Crafts Club for shooting Porn and Erotica.\n" +
            "While it starts as an amateur film shooting club, there for sure " +
            "are ways to make money with it.",
        '_unlock_conditions': [
            # LevelCondition("8+"),
            LockCondition(),
        ],
    })

    $ load_club("sex_club", "Sex Club", {
        '_description': "Like in the masturbation club, the students meet here " +
            "to have fun together in engaging in orgies and other sexual " +
            "activities and to search for new ways to reach new levels of euphoria.",
        '_unlock_conditions': [
            # LevelCondition("7+"),
            LockCondition(),
        ],
    })

    $ load_club("service_club", "Service Club", {
        '_description': "This club specializes in finding and testing ways " +
            "to optimize and find new ways to achieve optimal customer " +
            "satisfaction.\n\nThis club may also cooperate with other clubs " +
            "to host certain events.",
        '_unlock_conditions': [
            # LevelCondition("5+"),
            LockCondition(),
        ],
    })

    $ load_club("swimming_club", "Swimming Club", {
        '_description': "The swimming club provides ways for students to train " +
            "their condition and also to train their gracefulness in the water.",
        '_unlock_conditions': [
            LockCondition(),
        ],
    })

    $ load_club("sport_club", "Sport Club", {
        '_description': "A club where students engage in various sporty " +
            "activities like track and field or long jump.",
        '_unlock_conditions': [
            LockCondition(),
        ],
    })

    $ load_club("literature_club", "Literature Club", {
        '_description': "Here students dedicate the free time to their hobby " +
            "of reading various books and stories.",
        '_unlock_conditions': [
            LockCondition(),
        ],
    })

    $ load_club("music_club", "Music Club", {
        '_description': "A musical club where students came together to form " +
            "bands and to create possibilities to perform on the big stage.",
        '_unlock_conditions': [
            LockCondition(),
        ],
    })

    $ load_club("game_club", "Game Club", {
        '_description': "A club where various games are played, developed " +
            "and tested.",
        '_unlock_conditions': [
            LockCondition(),
        ],
    })

    $ load_club("arts_club", "Arts & Crafts Club", {
        '_description': "A club where students let out their artistic " +
            "personalities in many different ways. Here they can paint, " +
            "sculpt or something else they want to do to present themselves.",
        '_unlock_conditions': [
            LockCondition(),
        ],
    })

    $ load_club("outdoor_club", "Outdoor Activities Club", {
        '_description': "This club is dedicated to show different activities " +
            "that can be done out in the nature, like camping or hiking, " +
            "canoeing. Everything outside- and nature-related.",
        '_unlock_conditions': [
            LockCondition(),
        ],
    })

    return