init python:
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
            persistent.gallery[location][event] = {'values': {}, 'ranges': {}, 'options': {}, 'order': []}

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
        persistent.gallery[location][event] = {'values': {}, 'ranges': {}, 'options': {}, 'order': []}

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

        if location not in persistent.gallery.keys():
            return key
        if event not in persistent.gallery[location].keys():
            return key
        if 'options' not in persistent.gallery[location][event].keys():
            return key
        if 'titles' not in persistent.gallery[location][event]['options'].keys():
            return key
        if key not in persistent.gallery[location][event]['options']['titles'].keys():
            return key
        return persistent.gallery[location][event]['options']['titles'][key]

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

        def __init__(self, event: str):
            self.event = event
            self.location = get_event_from_register(event).get_location()

            prep_gallery(self.location, event)
            self.current_ranges = persistent.gallery[self.location][event]['ranges']

            self.original_data = {}
            self.data = self.original_data
            self.order = []
            self.count = 0
            renpy.call_screen("black_screen_text", event)

        def set_stat_ranges(self, **max_limits: List[float]):
            """
            Sets up steps for stats.
            This is to normalize stat value to reduce the amount of values that need to be stored.

            ### Parameters:
            1. **max_limits: List[float]
                - The value steps for each stat.
            """

            for key in max_limits.keys():
                    self.current_ranges[key] = list(max_limits[key])

        def set_topic_titles(self, **titles: str):
            """
            Sets up titles for topics.

            ### Parameters:
            1. **titles: str
                - The titles for each topic.
            """

            if 'titles' not in persistent.gallery[self.location][self.event]['options'].keys():
                persistent.gallery[self.location][self.event]['options']['titles'] = {}
            for key in titles.keys():
                persistent.gallery[self.location][self.event]['options']['titles'][key] = titles[key]

        def register_value(self, key: str, value: number | string):
            """
            Registers a value for the use in the gallery database.

            ### Parameters:
            1. key: str
                - The key to register the value under.
            2. value: number | string
                - The value to register.
            """
            
            if key in self.current_ranges.keys() and is_float(value):
                value = min(filter(lambda x: x > float(value), self.current_ranges[key]))                

            if value not in self.data.keys():
                self.data[value] = {}

            self.order.append(key)
            if (len(persistent.gallery[self.location][self.event]['order']) <= self.count or 
                persistent.gallery[self.location][self.event]['order'][self.count] != key
            ):
                persistent.gallery[self.location][self.event]['values'] = {}

            persistent.gallery[self.location][self.event]['order'] = self.order

            self.data = self.data[value]
            persistent.gallery[self.location][self.event]['values'].update(self.original_data)
            self.count = self.count + 1

        def get_value(self, key: str, alt: Any = None, **kwargs) -> Any:
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
            if not _in_replay:
                self.register_value(key, value)
            return value

        