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

    def prep_gallery(location: str, event: str, event_form: str, *key: str):
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
            persistent.gallery[location][event] = {'values': {}, 'ranges': {}, 'options': {'event_form': event_form}, 'order': [], 'decisions': {}}

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
        """
        Gets a list of values from the gallery database.

        ### Parameters:
        1. location: str
            - The location of the gallery.
        2. event: str
            - The event of the gallery.
        3. values: Dict[str, Any]
            - The values to get the list from.
        4. key: List[str]
            - The keys to get the list from.

        ### Returns:
        1. List:
            - The list of values found in the database.
        """

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
            event_form = get_kwargs('event_form', 'event', **kwargs)
            if event == None:
                return
            global gallery_manager
            gallery_manager = self
            self.event = event

            self.location = get_kwargs('location', 'misc', **kwargs)
            if is_event_registered(event):
                self.location = get_event_from_register(event).get_location()

            prep_gallery(self.location, event, event_form)
            self.current_ranges = persistent.gallery[self.location][event]['ranges']

            self.original_data = {}
            self.data = self.original_data
            self.order = []
            self.count = 0
            self.decisions = persistent.gallery[self.location][event]['decisions']

        def set_option(self, key: str, value: Any):
            """
            Sets an option for the gallery database.

            ### Parameters:
            1. key: str
                - The key to set the option under.
            2. value: Any
                - The value to set the option to.
            """

            persistent.gallery[self.location][self.event]['options'][key] = value

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

        if 'last_data' not in persistent.gallery[gallery_manager.location][gallery_manager.event]['options'].keys():
            persistent.gallery[gallery_manager.location][gallery_manager.event]['options']['last_data'] = {}

        if key not in persistent.gallery[gallery_manager.location][gallery_manager.event]['options']['last_data'].keys():
            persistent.gallery[gallery_manager.location][gallery_manager.event]['options']['last_data'][key] = value

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
            if key not in current_level.keys():
                continue
            current_level = current_level[key]

        return list(current_level.keys())

    ############################
    # Stat Value Gallery Handler

    def set_stat_value(key: str, value: float, ranges: List[float], **kwargs) -> float:
        """
        Sets a value normalized to set values in the gallery database.
        Values get changed to the next higher value in the ranges.

        ### Parameters:
        1. key: str
            - The key to set the value under.
        2. value: float
            - The value to set.
        3. ranges: List[float]
            - The ranges to normalize the value.

        ### Returns:
        1. float:
            - The value set in the database.
        """
        
        global gallery_manager

        if gallery_manager == None:
            return get_kwargs(key, alt, **kwargs)

        gallery_manager.current_ranges[key] = ranges

        return set_value(key, value, **kwargs)

    def get_stat_value(key: str, ranges: List[float], alt: float = 100, **kwargs) -> float:
        """
        Gets a value normalized to set values in the gallery database.
        Values get changed to the next higher value in the ranges.

        ### Parameters:
        1. key: str
            - The key to get the value from.
        2. ranges: List[float]
            - The ranges to normalize the value.
        3. alt: float (default: 100)
            - The value to return if the key is not found.

        ### Returns:
        1. float:
            - The value found in the database.
        """
        
        global gallery_manager

        if gallery_manager == None:
            if is_replay(**kwargs):
                event_name = get_kwargs('event_name', None, **kwargs)
                if event_name == None:
                    return alt
                event_obj = get_event_from_register(event_name)
                if event_obj == None:
                    return alt
                if event_obj.get_form() == 'fragment':
                    new_key = event_obj.get_id() + '.' + key
                    return get_kwargs(new_key, get_kwargs(key, alt, **kwargs), **kwargs)
        
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

        if is_replay(**kwargs):
            event_name = get_kwargs('event_name', None, **kwargs)
            if event_name == None:
                return alt
            event_obj = get_event_from_register(event_name)
            if event_obj == None:
                return alt
            if event_obj.get_form() == 'fragment':
                new_key = event_obj.get_id() + '.' + key
                value = get_kwargs(new_key, get_kwargs(key, alt, **kwargs), **kwargs)
                return set_value(key, value, **kwargs)                
        
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

        if not is_replay(**kwargs) and not get_kwargs('no_register', False, **kwargs):
            register_value(key, value)

        return value        

    ###############################
    # Fragment Gallery Handler

    def get_frag_list(**kwargs) -> List[EventFragment]:
        """
        Gets a list of fragments from the event object.

        ### Parameters:
        1. **kwargs
            - The kwargs to get the character from
            - if is_replay is True, method only returns the list of fragments supplied by kwargs with key: replay_frag_list

        ### Returns:
        1. List[EventFragment]:
            - The list of fragments from the event object.
        """

        if is_replay(**kwargs):
            return get_kwargs('replay_frag_list', [], **kwargs)

        event_obj = get_kwargs('event_obj', None, **kwargs)
        if event_obj == None:
            return []

        if not is_replay(**kwargs):
            fragments = event_obj.select_fragments(**kwargs)
            gallery_manager.set_option("Frag_Storage", [storage.get_name() for storage in event_obj.get_fragment_storages()])
            
            for i, storage in enumerate(event_obj.get_fragment_storages()):
                Gallery_Manager(event_name = storage.get_name(), event_form = 'FragStorage', location = "FragStorage")
                register_value("fragment", str(fragments[i]))


        return fragments

    def get_last_data(location: str, event: str) -> Dict[str, Any]:
        """
        Gets the last data from the gallery database.

        ### Parameters:
        1. location: str
            - The location of the gallery.
        2. event: str
            - The event of the gallery.

        ### Returns:
        1. Dict[str, Any]:
            - The last data from the gallery database.
        """

        if 'last_data' not in persistent.gallery[location][event]['options'].keys():
            persistent.gallery[location][event]['options']['last_data'] = {}

        return persistent.gallery[location][event]['options']['last_data']

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