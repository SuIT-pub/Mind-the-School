init python:

    if persistent.gallery is None:
        persistent.gallery = {}

    def merge_endings(old, new, current):
        current = update_dict(current, old)
        current = update_dict(current, new)
        return current

    # renpy.register_persistent('gallery', merge_endings)

    gallery_manager = None
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

        if location == "" and event == "":
            persistent.gallery = {}
            return

        if location not in persistent.gallery.keys():
            persistent.gallery[location] = {}
        
        persistent.gallery[location].pop(event, None)

        if len(persistent.gallery[location].keys()) == 0:
            persistent.gallery.pop(location, None)
        # persistent.gallery[location][event] = {'values': {}, 'ranges': {}, 'options': {}, 'order': [], 'decisions': {}}

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

        if (location in persistent.gallery.keys() and
            event in persistent.gallery[location].keys() and
            'options' in persistent.gallery[location][event].keys() and 
            'titles' in persistent.gallery[location][event]['options'].keys() and
            key in persistent.gallery[location][event]['options']['titles'].keys()
        ):
            return persistent.gallery[location][event]['options']['titles'][key]

        return get_translation(key)

    class Gallery_Manager:
        """
        A class to manage the gallery database for each event.
        The class has to be initialized in the start label of the event.

        ### Methods:
        1. set_stat_ranges(**max_limits: List[float])
            - Sets up steps for stats.
            - This is to normalize stat value to reduce the amount of values that need to be stored.
        2. set_topic_titles(**titles: str)
            - Sets up titles for topics.
        3. register_value(key: str, value: number | string)
            - Registers a value for the use in the gallery database.
        4. get_value(key: str, alt: Any = None, **kwargs) -> Any
            - Gets a value from the gallery database.

        ### Attributes:
        1. event: str
            - The event of the gallery.
        2. location: str
            - The location of the gallery.
        3. current_list: dict
            - The current list of values in the database.
        4. current_ranges: dict
            - The current list of ranges in the database.

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

    def set_stat_ranges(**max_limits: List[float]):
        """
        Sets up steps for stats.
        This is to normalize stat value to reduce the amount of values that need to be stored.

        ### Parameters:
        1. **max_limits: List[float]
            - The value steps for each stat.
        """

        global gallery_manager

        if gallery_manager == None:
            return

        for key in max_limits.keys():
                gallery_manager.current_ranges[key] = list(max_limits[key])

    def set_topic_titles(**titles: str):
        """
        Sets up titles for topics.

        ### Parameters:
        1. **titles: str
            - The titles for each topic.
        """

        global gallery_manager

        if gallery_manager == None:
            return

        if 'titles' not in persistent.gallery[gallery_manager.location][gallery_manager.event]['options'].keys():
            persistent.gallery[gallery_manager.location][gallery_manager.event]['options']['titles'] = {}
        for key in titles.keys():
            persistent.gallery[gallery_manager.location][gallery_manager.event]['options']['titles'][key] = titles[key]

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
            log_val('pre-range value', value)
            closest_value = 100
            for val in gallery_manager.current_ranges[key]:
                if val > value and val < closest_value:
                    closest_value = val
            value = closest_value
            log_val('post-range value', value)

        if value not in gallery_manager.data.keys():
            gallery_manager.data[value] = {}

        gallery_manager.order.append(key)
        log_val('gallery_manager.order', gallery_manager.order)
        log_val('gallery order', persistent.gallery[gallery_manager.location][gallery_manager.event]['order'])
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
        in_replay = get_kwargs('in_replay', False, **kwargs)
        if not in_replay:
            register_value(key, value)

        return value

    def get_char_value(**kwargs) -> Char:
        char_obj = get_kwargs("char_obj", None, **kwargs)
        if char_obj == None:
            char_obj_key = get_kwargs("char_obj_key", None, **kwargs)
            if char_obj_key == None:
                return None
            char_obj = get_character_by_key(char_obj_key)
            if char_obj == None:
                return None

        in_replay = get_kwargs('in_replay', False, **kwargs)

        if not in_replay:
            register_value("char_obj_key", char_obj.get_name())
            register_value("level", char_obj.get_level())

        return char_obj

    
    def get_char_value_with_level(**kwargs) -> Char:
        char_obj = get_kwargs("char_obj", None, **kwargs)
        if char_obj == None:
            char_obj_key = get_kwargs("char_obj_key", None, **kwargs)
            if char_obj_key == None:
                return None
            char_obj = get_character_by_key(char_obj_key)
            if char_obj == None:
                return None

        in_replay = get_kwargs('in_replay', False, **kwargs)

        if not in_replay:
            register_value("char_obj_key", char_obj.get_name())
            register_value("level", char_obj.get_level())

        return char_obj, char_obj.get_level()
    