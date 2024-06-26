init python:
    gallery_manager = None

    # if persistent.gallery is None:
    #     persistent.gallery = {}

    # def merge_endings(old, new, current):
    #     current = update_dict(current, old)
    #     current = update_dict(current, new)
    #     return current

    # renpy.register_persistent('gallery', merge_endings)

    ############################
    # Gallery Persistent handler

    def prep_gallery(location: str, event: str, *key: str):
        """
        Prepares the gallery database for use.
        This is to ensure that the database is ready for use.

        ### Parameters:
        1. location: str
            - The location of the gallery.
        2. event: str
            - The event of the gallery.
        3. *key: str
            - The keys to create in the database.
            - this is optional.
        """

        # Check if persistent.gallery exists, if not, initialize it
        if persistent.gallery is None:
            persistent.gallery = {}

        # Check if location exists in persistent.gallery, if not, create it
        if location not in persistent.gallery.keys():
            persistent.gallery[location] = {}

        # Check if event exists in persistent.gallery[location], if not, create it
        if event not in persistent.gallery[location].keys():
            persistent.gallery[location][event] = {'values': {}, 'ranges': {}, 'options': {}, 'order': [], 'decisions': {}}

        if 'decisions' not in persistent.gallery[location][event].keys():
            persistent.gallery[location][event]['decisions'] = {}

        # Clear the order list
        # persistent.gallery[location][event]['order'] = []

        # If key arguments are provided, create nested dictionaries in persistent.gallery[location][event]['values']
        if len(key) > 0:
            current = persistent.gallery[location][event]['values']
            for k in key:
                if k not in current.keys():
                    current[k] = {}
                    current = current[k]
                    
    def reset_gallery(location: str = "", event: str = ""):
        """
        Resets the gallery database for a specific location and event.
        This is only used for debug purposes.
        If location and event are left blank, the entire database is reset.

        ### Parameters:
        1. location: str (default: "")
            - The location of the gallery.
            - If left blank together with event, the entire database is reset.
        2. event: str (default: "")
            - The event of the gallery.
            - If left blank together with location, the entire database is reset.
        """

        if location != "":
            if location not in persistent.gallery.keys():
                return
            if event == "" or len(persistent.gallery[location].keys()) == 0:
                persistent.gallery.pop(location, None)
            elif event != "":
                persistent.gallery[location].pop(event, None)
        elif event == "":
            persistent.gallery = {}

    def get_gallery_values(location: str, event: str, values: Dict[str, Any], key: List[str]) -> List:
        current = persistent.gallery[location][event]['values']
        for k in key:
            if values[k] not in current.keys():
                return []
            current = current[values[k]]
        return list(current.keys())

    def get_gallery_topic_title(location: str, event: str, key: str) -> str:
        """
        Gets a title for a topic.
        If the title cannot be found behind that key, the key is returned.

        ### Parameters:
        1. location: str
            - The location of the gallery.
        2. event: str
            - The event of the gallery.
        3. key: str
            - The key to get the title from.

        ### Returns:
        1. str:
            - The title found in the database.
            - The key if the title cannot be found.
        """

        title = get_translation(f"{location}_{event}_{key}")
        if title == f"{location}_{event}_{key}":
            title = get_translation(f"{event}_{key}")
        if title == f"{event}_{key}":
            title = get_translation(key)
        
        return title

    def get_gallery_value_title(title: str, location: str, event: str, key: str) -> str:
        """
        Gets a title for a value.
        If the title cannot be found behind that key, the key is returned.

        ### Parameters:
        1. title: str
            - The title to get the value from.
        2. location: str
            - The location of the gallery.
        3. event: str
            - The event of the gallery.
        4. key: str
            - The key to get the value from.

        ### Returns:
        1. str:
            - The value found in the database.
            - The key if the value cannot be found.
        """

        value = get_translation(f"{location}_{event}_{title}_{key}")
        if value == f"{location}_{event}_{title}_{key}":
            value = get_translation(f"{event}_{title}_{key}")
        if value == f"{event}_{title}_{key}":
            value = get_translation(f"{title}_{key}")
        if value == f"{title}_{key}":
            value = get_translation(key)
        
        return value

    #################
    # Gallery Manager

    class Gallery_Manager:
        """
        A class to manage the gallery database for each event.
        The class has to be initialized in the start label of the event.

        ### Attributes:
        1. event: str
            - The event of the gallery.
        2. location: str
            - The location of the gallery.
        3. current_ranges: dict
            - The current list of ranges in the database.
        4. original_data: dict
            - The original data of the database at the time of initialization.
        5. data: dict
            - The up to date data for the database.
        6. order: list
            - The up to date order of the inserted keys.
        7. count: int
            - the amount of inserted keys
        8. decisions: dict
            - the current database of made decisions

        ### Parameters:
        1. event: str
            - The event to be registered.

        """

        def __init__(self, **kwargs):
            event = get_kwargs('event_name', None, **kwargs)
            if event == None:
                return
            global gallery_manager
            gallery_manager = self
            self.event = event
            self.location = get_event_from_register(event).get_location()

            prep_gallery(self.location, event)
            self.current_ranges = persistent.gallery[self.location][event]['ranges']

            self.original_data = {}
            self.data = self.original_data
            self.order = []
            self.count = 0
            self.decisions = persistent.gallery[self.location][event]['decisions']

    ######################################################
    # Value and Decision registration into persistent data

    def register_value(key: str, value: number | string):
        """
        Registers a value for the use in the gallery database.

        ### Parameters:
        1. key: str
            - The key to register the value under.
        2. value: number | string
            - The value to register.
        """

        global gallery_manager

        if gallery_manager == None:
            return

        if key in gallery_manager.current_ranges.keys() and is_float(value):
            closest_value = 100
            for val in gallery_manager.current_ranges[key]:
                if val > value and val < closest_value:
                    closest_value = val
            value = closest_value

        if value not in gallery_manager.data.keys():
            gallery_manager.data[value] = {}

        gallery_manager.order.append(key)
        if (len(persistent.gallery[gallery_manager.location][gallery_manager.event]['order']) <= gallery_manager.count or 
            persistent.gallery[gallery_manager.location][gallery_manager.event]['order'][gallery_manager.count] != key
        ):
            persistent.gallery[gallery_manager.location][gallery_manager.event]['values'] = {}
            persistent.gallery[gallery_manager.location][gallery_manager.event]['options'].pop('last_order', None)
            persistent.gallery[gallery_manager.location][gallery_manager.event]['options'].pop('last_data', None)
            persistent.gallery[gallery_manager.location][gallery_manager.event]['order'] = gallery_manager.order
            persistent.gallery[gallery_manager.location][gallery_manager.event]['decisions'] = {}
            gallery_manager.decisions = persistent.gallery[gallery_manager.location][gallery_manager.event]['decisions']

        gallery_manager.data = gallery_manager.data[value]
        persistent.gallery[gallery_manager.location][gallery_manager.event]['values'] = update_dict(
            persistent.gallery[gallery_manager.location][gallery_manager.event]['values'], 
            gallery_manager.original_data
        )

        gallery_manager.count = gallery_manager.count + 1

    def register_decision(key: str):
        """
        Registers a decision for the use in the gallery database.

        ### Parameters:
        1. key: str
            - The key to register the decision under.
        """

        global gallery_manager

        if gallery_manager == None:
            return

        if key not in gallery_manager.decisions.keys():
            gallery_manager.decisions[key] = {}
        gallery_manager.decisions = gallery_manager.decisions[key]

    #################################
    # Persistent data Decision getter

    def get_decision_possibilities(decision_data: Dict[str, Any], decisions: List[str]) -> List[str]:
        """
        Gets a list of possibilities for a decision.

        ### Parameters:
        1. decision_data: Dict[str, Any]
            - The data for the decision.
        2. decisions: List[str]
            - The decisions that have been used so far until now.

        ### Returns:
        1. List[str]:
            - The list of possibilities for the decision.
        """

        current_level = decision_data

        for key in decisions:
            current_level = current_level[key]

        return list(current_level.keys())

    ############################
    # Stat Value Gallery Handler

    def set_stat_value(key: str, value: float, ranges: List[float], **kwargs) -> float:
        
        global gallery_manager

        if gallery_manager == None:
            return get_kwargs(key, alt, **kwargs)

        gallery_manager.current_ranges[key] = ranges

        return set_value(key, value, **kwargs)

    def get_stat_value(key: str, ranges: List[float], alt: float = 100, **kwargs) -> float:
        
        global gallery_manager

        if gallery_manager == None:
            return get_kwargs(key, alt, **kwargs)

        gallery_manager.current_ranges[key] = ranges

        return get_value(key, alt, **kwargs)

    ###############################
    # General Value Gallery Handler

    def get_value(key: str, alt: Any = None, **kwargs) -> Any:
        """
        Gets a value from the gallery database.

        ### Parameters:
        1. key: str
            - The key to get the value from.
        2. alt: Any (default: None)
            - The value to return if the key is not found.

        ### Returns:
        1. Any:
            - The value found in the database.
        """

        value = get_kwargs(key, alt, **kwargs)

        return set_value(key, value, **kwargs)

    def set_value(key: str, value: Any, **kwargs):
        """
        Sets a value in the gallery database.

        ### Parameters:
        1. key: str
            - The key to set the value under.
        2. value: Any
            - The value to set.

        ### Returns:
        1. Any:
            - The value set in the database.
        """

        in_replay = get_kwargs('in_replay', False, **kwargs)
        if not in_replay:
            register_value(key, value)

        return value        

    ###########################################
    # Character and Level Value Gallery Handler

    def set_char_value_with_level(char_name: str, char: Char, **kwargs) -> Tuple[Char, int]:
        """
        Sets a character value in the gallery database.

        ### Parameters:
        1. char_name: Char
            - The name of the character to set the value under.
            - possible values: school_obj, teacher_obj, parent_obj, secretary_obj
        2. char: Char
            - The character to set the value under.

        ### Returns:
        1. Tuple[Char, int]:
            - The character set in the database.
            - The level of the character.
        """

        if char == None:
            char_obj_key = get_kwargs(char_name + "_key", None, **kwargs)
            if char_obj_key == None:
                return None
            char = get_character_by_key(char_obj_key)
            if char == None:
                return None

        in_replay = get_kwargs('in_replay', False, **kwargs)

        if not in_replay:
            register_value(char_name + "_key", char.get_name())
            register_value(char_name + "_level", char.get_level())

        return (char, char.get_level())

    def set_char_value(char_name: str, char_objs: Char, **kwargs) -> Char:
        """
        Sets a character value in the gallery database.

        ### Parameters:
        1. char_name: Char
            - The name of the character to set the value under.
            - possible values: school_obj, teacher_obj, parent_obj, secretary_obj
        2. char_obj: Char
            - The character to set the value under.

        ### Returns:
        1. Char:
            - The character set in the database.
        """

        (char_objs, level) = set_char_value_with_level(char_name, char_objs, **kwargs)

        return char_objs

    def get_char_value(char_name: str , **kwargs) -> Char:
        """
        Gets a character from kwargs and sets it in the gallery database.

        ### Parameters:
        1. char_name: str
            - The name of the character to get from the kwargs.
            - possible values: school_obj, teacher_obj, parent_obj, secretary_obj
        2. **kwargs: Any
            - The kwargs to get the value from.

        ### Returns:
        1. Char:
            - The character set in the database.
        """

        char_obj = get_kwargs(char_name, None, **kwargs)
        return set_char_value(char_name, char_obj, **kwargs)

    def get_char_value_with_level(char_name: str, **kwargs) -> Tuple[Char, int]:
        """
        Gets a character from kwargs and sets it in the gallery database.

        ### Parameters:
        1. char_name: str
            - The name of the character to get from the kwargs.
            - possible values: school_obj, teacher_obj, parent_obj, secretary_obj
        2. **kwargs: Any
            - The kwargs to get the value from.

        ### Returns:
        1. Tuple[Char, int]:
            - The character set in the database.
            - The level of the character.
        """

        char_obj = get_kwargs(char_name, None, **kwargs)
        return set_char_value_with_level(char_name, char_obj, **kwargs)

    ################
    # Replay Handler
    
    def is_replay(**kwargs):
        """
        Checks if the game is in replay mode

        ### Parameters:
        1. **kwargs
            - The kwargs to get the character from

        ### Returns:
        1. bool
            - True if the game is in replay mode, False otherwise
        """

        return get_kwargs("in_replay", False, **kwargs)