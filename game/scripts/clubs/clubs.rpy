init python:
    import re
    class Club:
        unlock_conditions = []

        unlocked = {
            "high_school": False,
            "middle_school": False,
            "elementary_school": False
        }

        def __init__(self, name, title):
            self.name = name
            self.title = title
            self.description = ""
            self.image_path = "images/journal/empty_image.png"

        def get_name(self):
            return self.name

        def get_title(self):
            return self.title

        def get_type(self):
            return "club"

        def unlock(self):
            self.unlocked = True

        def is_unlocked(self, school):
            if school not in self.unlocked.keys():
                return False
            return self.unlocked[school]

        def is_visible(self, school):
            for condition in self.unlock_conditions:
                if condition.is_blocking(school):
                    return False
            return True

        def can_be_unlocked(self, school):
            if school not in schools.keys():
                return False

            for condition in self.unlock_conditions:
                if condition.is_fullfilled(school):
                    continue
                return False

            return True

    
    def get_visible_clubs_by_school(school):
        output = []

        for club in clubs.values():
            if (club.is_visible(school) and 
            not club.is_unlocked(school) and
            club.name not in output):
                output.append(club.name)
                continue

        return output

    def get_visible_clubs():
        output = []

        for club in clubs.values():
            if (club.is_visible("high_school") and 
            not club.is_unlocked("high_school") and
            club.name not in output):
                output.append(club.name)
                continue
            
            if loli_content >= 1:
                if (club.is_visible("middle_school") and 
                not club.is_unlocked("middle_school") and
                club.name not in output):
                    output.append(club.name)
                    continue

            if loli_content == 2:
                if (club.is_visible("elementary_school") and 
                not club.is_unlocked("elementary_school") and
                club.name not in output):   
                    output.append(club.name)
                    continue

        return output

    def get_unlockable_clubs():
        output = []

        for club in clubs.values():
            high_unlock = club.can_be_unlocked("high_school")
            high_unlocked = club.is_unlocked("high_school")

            if (high_unlock and 
            not high_unlocked and 
            club.name not in output):
                output.append(club.name)
                continue

            if loli_content >= 1:
                middle_unlock = club.can_be_unlocked("middle_school")
                middle_unlocked = club.is_unlocked("middle_school")

                if (middle_unlock and 
                not middle_unlocked and 
                club.name not in output):
                    output.append(club.name)
                    continue

            if loli_content == 2:
                elementary_unlock = club.can_be_unlocked("elementary_school")
                elementary_unlocked = club.is_unlocked("elementary_school")

                if (elementary_unlock and 
                not elementary_unlocked and 
                club.name not in output):
                    output.append(club.name)
                    continue

        return output

    def get_unlockable_clubs_by_school(school):
        output = []

        for club in clubs.values():
            unlock = club.can_be_unlocked(school)
            unlocked = club.is_unlocked(school)

            if (unlock and not unlocked and club.name not in output):
                output.append(club.name)
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
        
        if data != None:
            clubs[name].__dict__.update(data)

label load_clubs:
    $ load_club("test_club", "Test Club",{
        'description': "A Club for testing",
        'unlock_conditions': [
            StatCondition("1+", "inhibition"),
            # LockCondition(),
        ],
    })

    $ load_club("masturbation_club", "Masturbation Club", {
        'description': "Here students cum together (pun intended) to " +
            "collectively masturbate and explore new ways to satsify " +
            "themselves.\nA nice place for students to socialize and to " +
            "get some time out from the stressy school life.",
        'unlock_conditions': [
            LevelCondition("5+"),
            # LockCondition(),
        ],
    })

    $ load_club("exhibitionism_club", "Exhibitionism Club", {
        'description': "The club to celebrate the art that is the human body. " +
            "Here students come together to engage in the thrill seeking " +
            "activity of presenting their nude bodies in public.",
        'unlock_conditions': [
            LevelCondition("5+"),
            # LockCondition(),
        ],
    })

    $ load_club("cosplay_club", "Cosplay Club", {
        'description': "Here students engage costume crafting and cosplaying.",
        'unlock_conditions': [
            LevelCondition("2+"),
            # LockCondition(),
        ],
    })

    $ load_club("cheerleading_club", "Cheerleading Club", {
        'description': "A sports club for training cheerleading and for" +
            "exploring new ways to cheer and motivate the teams.",
        'unlock_conditions': [
            LevelCondition("2+"),
            # LockCondition(),
        ],
    })

    $ load_club("porn_club", "Porn Club", {
        'description': "An Arts and Crafts Club for shooting Porn and Erotica.\n" +
            "While it starts as an amateur film shooting club, there for sure " +
            "are ways to make money with it.",
        'unlock_conditions': [
            LevelCondition("8+"),
            # LockCondition(),
        ],
    })

    $ load_club("sex_club", "Sex Club", {
        'description': "Like in the masturbation club, the students meet here " +
            "to have fun together in engaging in orgies and other sexual " +
            "activities and to search for new ways to reach new levels of euphoria.",
        'unlock_conditions': [
            LevelCondition("7+"),
            # LockCondition(),
        ],
    })

    $ load_club("service_club", "Service Club", {
        'description': "This club specializes in finding and testing ways " +
            "to optimize and find new ways to achieve optimal customer " +
            "satisfaction.\n\nThis club may also cooperate with other clubs " +
            "to host certain events.",
        'unlock_conditions': [
            LevelCondition("5+"),
            # LockCondition(),
        ],
    })

    $ load_club("swimming_club", "Swimming Club", {
        'description': "A Swimming Club",
        'unlock_conditions': [
            # LockCondition(),
        ],
    })

    $ load_club("sport_club", "Sport Club", {
        'description': "A Sport Club",
        'unlock_conditions': [
            # LockCondition(),
        ],
    })

    $ load_club("literature_club", "Literature Club", {
        'description': "A literature club",
        'unlock_conditions': [
            # LockCondition(),
        ],
    })

    $ load_club("music_club", "Music Club", {
        'description': "A music club",
        'unlock_conditions': [
            # LockCondition(),
        ],
    })

    $ load_club("game_club", "Game Club", {
        'description': "A club where various games are played, developed " +
            "and tested.",
        'unlock_conditions': [
            # LockCondition(),
        ],
    })

    $ load_club("arts_club", "Arts & Crafts Club", {
        'description': "",
        'unlock_conditions': [
            # LockCondition(),
        ],
    })

    $ load_club("outdoor_club", "Outdoor Activities Club", {
        'description': "",
        'unlock_conditions': [
            # LockCondition(),
        ],
    })