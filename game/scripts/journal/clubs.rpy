init -6 python:
    import re
    class Club(Journal_Obj):
        def __init__(self, name, title):
            super().__init__(name, title)
            self._unlocked = {
                "high_school": False,
                "middle_school": False,
                "elementary_school": False,
            }

        def _update(self, title: str, data: Dict[str, Any] = None) -> None:
            super()._update(title, data)
            if data != None:
                self.__dict__.update(data)

            if not hasattr(self, '_unlocked'):
                self._unlocked = {
                    "high_school": False,
                    "middle_school": False,
                    "elementary_school": False,
                }

        def get_type(self) -> str:
            return "club"

    #############################################
    # Clubs Global Methods
    
    def get_club(club: str) -> Club:
        if club in clubs.keys():
            return clubs[club]
        return None
    
    def is_club_unlocked(club_name: str, school: str) -> bool:
        if club_name not in clubs.keys():
            return False
        return clubs[club_name].is_unlocked(school)

    def is_club_visible(club_name: str, **kwargs) -> bool:
        if club_name not in clubs.keys():
            return False
        return clubs[club_name].is_visible(**kwargs)

    def load_club(name: str, title: str, data: Dict[str, Any] = None) -> None:
        if name not in clubs.keys():
            clubs[name] = Club(name, title)

        clubs[name]._update(title, data)

    def remove_club(name: str) -> None:
        if name in clubs.keys():
            del(clubs[name])

label load_clubs ():
    $ load_club("masturbation_club", "Masturbation Club", {
        '_description': [
            "Here students cum together (pun intended) to collectively masturbate and explore new ways to satisfy themselves.\nA nice place for students to socialize and to get some time out from the stressful school life.",
        ],
        '_unlock_conditions': ConditionStorage(
            # LevelCondition("5+"),
            LockCondition(),
        ),
        '_image_path': 'images/journal/clubs/masturbation_club.jpg',
        '_image_path_alt': 'images/journal/clubs/masturbation_club.jpg',
    })

    $ load_club("exhibitionism_club", "Exhibitionism Club", {
        '_description': [
            "The club to celebrate the art that is the human body. Here students come together to engage in the thrill seeking activity of presenting their nude bodies in public.",
        ],
        '_unlock_conditions': ConditionStorage(
            # LevelCondition("5+"),
            LockCondition(),
        ),
        '_image_path': 'images/journal/clubs/exhibitionism_club.jpg',
        '_image_path_alt': 'images/journal/clubs/exhibitionism_club.jpg',
    })

    $ load_club("cosplay_club", "Cosplay Club", {
        '_description': [
            "Here students engage costume crafting and cosplaying.",
        ],
        '_unlock_conditions': ConditionStorage(
            # LevelCondition("2+"),
            LockCondition(),
        ),
        '_image_path': 'images/journal/clubs/cosplay_club.jpg',
        '_image_path_alt': 'images/journal/clubs/cosplay_club.jpg',
    })

    $ load_club("cheerleading_club", "Cheerleading Club", {
        '_description': [
            "A sports club for training cheerleading and for exploring new ways to cheer and motivate the teams.",
        ],
        '_unlock_conditions': ConditionStorage(
            # LevelCondition("2+"),
            # LockCondition(),
        ),
        '_image_path': 'images/journal/clubs/cheerleading_club_<school>_<level>.jpg',
        '_image_path_alt': 'images/journal/clubs/cheerleading_club_high_school_2.jpg',
    })

    $ load_club("porn_club", "Porn Club", {
        '_description': [
            "An Arts and Crafts Club for shooting Porn and Erotica.\nWhile it starts as an amateur film shooting club, there for sure are ways to make money with it.",
        ],
        '_unlock_conditions': ConditionStorage(
            # LevelCondition("8+"),
            LockCondition(),
        ),
    })

    $ load_club("sex_club", "Sex Club", {
        '_description': [
            "Like in the masturbation club, the students meet here to have fun together in engaging in orgies and other sexual activities and to search for new ways to reach new levels of euphoria.",
        ],
        '_unlock_conditions': ConditionStorage(
            # LevelCondition("7+"),
            LockCondition(),
        ),
    })

    $ load_club("service_club", "Service Club", {
        '_description': [
            "This club specializes in finding and testing ways to optimize and find new ways to achieve optimal customer satisfaction.",
            "This club may also cooperate with other clubs to host certain events.",
        ],
        '_unlock_conditions': ConditionStorage(
            # LevelCondition("5+"),
            LockCondition(),
        ),
    })

    $ load_club("swimming_club", "Swimming Club", {
        '_description': [
            "The swimming club provides ways for students to train their condition and also to train their gracefulness in the water.",
        ],
        '_unlock_conditions': ConditionStorage(
            LockCondition(),
        ),
    })

    $ load_club("sport_club", "Sport Club", {
        '_description': [
            "A club where students engage in various sporty activities like track and field or long jump.",
        ],
        '_unlock_conditions': ConditionStorage(
            LockCondition(),
        ),
    })

    $ load_club("literature_club", "Literature Club", {
        '_description': [
            "Here students dedicate the free time to their hobby of reading various books and stories.",
        ],
        '_unlock_conditions': ConditionStorage(
            LockCondition(),
        ),
    })

    $ load_club("music_club", "Music Club", {
        '_description': [
            "A musical club where students came together to form bands and to create possibilities to perform on the big stage.",
        ],
        '_unlock_conditions': ConditionStorage(
            LockCondition(),
        ),
    })

    $ load_club("game_club", "Game Club", {
        '_description': [
            "A club where various games are played, developed and tested.",
        ],
        '_unlock_conditions': ConditionStorage(
            LockCondition(),
        ),
    })

    $ load_club("arts_club", "Arts & Crafts Club", {
        '_description': [
            "A club where students let out their artistic personalities in many different ways. Here they can paint, sculpt or something else they want to do to present themselves.",
        ],
        '_unlock_conditions': ConditionStorage(
            LockCondition(),
        ),
    })

    $ load_club("outdoor_club", "Outdoor Activities Club", {
        '_description': [
            "This club is dedicated to show different activities that can be done out in the nature, like camping or hiking, canoeing. Everything outside- and nature-related.",
        ],
        '_unlock_conditions': ConditionStorage(
            LockCondition(),
        ),
    })

    return