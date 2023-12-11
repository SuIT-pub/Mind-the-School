init -6 python:
    import re
    class Club(Journal_Obj):
        """
        A sub-class of Journal_Obj.
        A club is a group of students that come together to engage in a certain activity.

        ### Attributes:
        1. _unlocked: Dict[str, bool]
            - A dictionary that stores the unlocked state of the club for each school.

        ### Methods:
        1. get_type() -> str
            - Returns the type of the object.
        """

        def __init__(self, name, title):
            super().__init__(name, title)
            self._unlocked = False

        def _update(self, title: str, data: Dict[str, Any] = None) -> None:
            super()._update(title, data)
            if data != None:
                self.__dict__.update(data)

            if not hasattr(self, '_unlocked'):
                self._unlocked = False

            if not isinstance(self._unlocked, bool):
                self._unlocked = self._unlocked['high_school'] or self._unlocked['middle_school'] or self._unlocked['elementary_school']

        def get_type(self) -> str:
            """
            Returns the type of the object.

            ### Returns:
            1. str
                - The type of the object.
                - In this case "club".
            """

            return "club"

    #############################################
    # Clubs Global Methods
    
    def get_club(club: str) -> Club:
        """
        Returns the club object with the given name.

        ### Parameters:
        1. club: str
            - The name of the club.

        ### Returns:
        1. Club
            - The club object with the given name.
            - If no club with the given name exists, returns None.
        """

        if club in clubs.keys():
            return clubs[club]
        return None
    
    def is_club_unlocked(club_name: str) -> bool:
        """
        Returns whether the club with the given name is unlocked for the given school.

        ### Parameters:
        1. club_name: str
            - The name of the club.
        2. school: str
            - The name of the school.

        ### Returns:
        1. bool
            - Whether the club with the given name is unlocked for the given school.
            - If no club with the given name exists, returns False.
        """

        if club_name not in clubs.keys():
            return False
        return clubs[club_name].is_unlocked()

    def is_club_visible(club_name: str, **kwargs) -> bool:
        """
        Returns whether the club with the given name is visible for the given school.
        A club is visible if it is unlocked for the given school or the conditions for unlocking it are met or no locking conditions are set.

        ### Parameters:
        1. club_name: str
            - The name of the club.

        ### Returns:
        1. bool
            - Whether the club with the given name is visible for the given school.
            - If no club with the given name exists, returns False.
        """

        if club_name not in clubs.keys():
            return False
        return clubs[club_name].is_visible(**kwargs)

    def load_club(name: str, title: str, data: Dict[str, Any] = None) -> None:
        """
        Loads or updates a club with the given name and title and the given data.

        ### Parameters:
        1. name: str
            - The name of the club.
        2. title: str
            - The title of the club.
        3. data: Dict[str, Any]
            - The data of the club.
        """

        if name not in clubs.keys():
            clubs[name] = Club(name, title)

        clubs[name]._update(title, data)

    def remove_club(name: str) -> None:
        """
        Removes the club with the given name.

        ### Parameters:
        1. name: str
            - The name of the club.
        """

        if name in clubs.keys():
            del(clubs[name])

label load_clubs ():

    #! locked, currently not implemented
    $ load_club("masturbation_club", "Masturbation Club", {
        '_description': [
            "Here students cum together (pun intended) to collectively masturbate and explore new ways to satisfy themselves.\nA nice place for students to socialize and to get some time out from the stressful school life.",
        ],
        '_unlock_conditions': ConditionStorage(
            # LevelCondition("5+"),
            LockCondition(),
        ),
        '_image_path': 'images/journal/clubs/masturbation_club.webp',
        '_image_path_alt': 'images/journal/clubs/masturbation_club.webp',
    })

    #! locked, currently not implemented
    $ load_club("exhibitionism_club", "Exhibitionism Club", {
        '_description': [
            "The club to celebrate the art that is the human body. Here students come together to engage in the thrill seeking activity of presenting their nude bodies in public.",
        ],
        '_unlock_conditions': ConditionStorage(
            # LevelCondition("5+"),
            LockCondition(),
        ),
        '_image_path': 'images/journal/clubs/exhibitionism_club.webp',
        '_image_path_alt': 'images/journal/clubs/exhibitionism_club.webp',
    })

    #! locked, currently not implemented
    $ load_club("cosplay_club", "Cosplay Club", {
        '_description': [
            "Here students engage costume crafting and cosplaying.",
        ],
        '_unlock_conditions': ConditionStorage(
            # LevelCondition("2+"),
            LockCondition(),
        ),
        '_image_path': 'images/journal/clubs/cosplay_club.webp',
        '_image_path_alt': 'images/journal/clubs/cosplay_club.webp',
    })

    #! locked, currently not implemented
    $ load_club("cheerleading_club", "Cheerleading Club", {
        '_description': [
            "A sports club for training cheerleading and for exploring new ways to cheer and motivate the teams.",
        ],
        '_unlock_conditions': ConditionStorage(
            # LevelCondition("2+"),
            # LockCondition(),
        ),
        '_image_path': 'images/journal/clubs/cheerleading_club_<variant>_<level>.webp',
        '_image_path_alt': 'images/journal/clubs/cheerleading_club_0_2.webp',
    })

    #! locked, currently not implemented
    $ load_club("porn_club", "Porn Club", {
        '_description': [
            "An Arts and Crafts Club for shooting Porn and Erotica.\nWhile it starts as an amateur film shooting club, there for sure are ways to make money with it.",
        ],
        '_unlock_conditions': ConditionStorage(
            # LevelCondition("8+"),
            LockCondition(),
        ),
    })

    #! locked, currently not implemented
    $ load_club("sex_club", "Sex Club", {
        '_description': [
            "Like in the masturbation club, the students meet here to have fun together in engaging in orgies and other sexual activities and to search for new ways to reach new levels of euphoria.",
        ],
        '_unlock_conditions': ConditionStorage(
            # LevelCondition("7+"),
            LockCondition(),
        ),
    })

    #! locked, currently not implemented
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

    #! locked, currently not implemented
    $ load_club("swimming_club", "Swimming Club", {
        '_description': [
            "The swimming club provides ways for students to train their condition and also to train their gracefulness in the water.",
        ],
        '_unlock_conditions': ConditionStorage(
            LockCondition(),
        ),
    })

    #! locked, currently not implemented
    $ load_club("sport_club", "Sport Club", {
        '_description': [
            "A club where students engage in various sporty activities like track and field or long jump.",
        ],
        '_unlock_conditions': ConditionStorage(
            LockCondition(),
        ),
    })

    #! locked, currently not implemented
    $ load_club("literature_club", "Literature Club", {
        '_description': [
            "Here students dedicate the free time to their hobby of reading various books and stories.",
        ],
        '_unlock_conditions': ConditionStorage(
            LockCondition(),
        ),
    })

    #! locked, currently not implemented
    $ load_club("music_club", "Music Club", {
        '_description': [
            "A musical club where students came together to form bands and to create possibilities to perform on the big stage.",
        ],
        '_unlock_conditions': ConditionStorage(
            LockCondition(),
        ),
    })

    #! locked, currently not implemented
    $ load_club("game_club", "Game Club", {
        '_description': [
            "A club where various games are played, developed and tested.",
        ],
        '_unlock_conditions': ConditionStorage(
            LockCondition(),
        ),
    })

    #! locked, currently not implemented
    $ load_club("arts_club", "Arts & Crafts Club", {
        '_description': [
            "A club where students let out their artistic personalities in many different ways. Here they can paint, sculpt or something else they want to do to present themselves.",
        ],
        '_unlock_conditions': ConditionStorage(
            LockCondition(),
        ),
    })

    #! locked, currently not implemented
    $ load_club("outdoor_club", "Outdoor Activities Club", {
        '_description': [
            "This club is dedicated to show different activities that can be done out in the nature, like camping or hiking, canoeing. Everything outside- and nature-related.",
        ],
        '_unlock_conditions': ConditionStorage(
            LockCondition(),
        ),
    })

    return