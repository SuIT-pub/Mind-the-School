init -2 python:
    default_fallback = Event(2, "default_fallback_event")

init -3 python:
    import re
    import random
    import time
    from typing import Any, Dict, List, Tuple, Union
    
    ###############
    # Event classes

    class EventStorage:
        """
        EventStorage is a class that stores events and can call them when needed.

        ### Attributes:
        1. name: str
            - The name of the EventStorage. This is used to identify the EventStorage.
        2. fallback: Event
            - The fallback event that is called when no other events are available.
        3. events: Dict[int, Dict[str, Event]]
            - The events that are stored in the EventStorage. The events are stored in a dictionary with the priority as the key and the dictionary as a value.
            - The event Dictionary is a dictionary with the event id as the key and the event as the value.
            - Priority 1 represents an event that is called first and blocks all other events.
            - Priority 2 represents an Event that is called together with all other events with priority 2 and then moves on to priority 3.
            - Priority 3 represents a set of events from which one is called randomly.
        4. fallback_text: str
            - The text that is displayed when the fallback event is called.

        ### Methods:
        1. get_name() -> str
            - Returns the name of the EventStorage.
        2. get_type() -> str
            - Returns the type of the EventStorage.
        3. add_event(event: Event)
            - Adds an event to the EventStorage.
        4. remove_event(event_id: str)
            - Removes an event from the EventStorage.
        5. count_available_events(priority: int = 0, **kwargs) -> int
            - Counts the number of events that are available.
            - If priority is 0, all events are counted.
            - Otherwise only the events with the given priority are counted.
        6. count_available_events_with_fallback(priority: int = 0, **kwargs) -> int
            - Counts the number of events that are available.
            - If priority is 0, all events are counted.
            - Otherwise only the events with the given priority are counted.
            - If no events are available, 1 is returned.
        7. get_available_events(priority: int = 0, **kwargs) -> List[Event]
            - Returns a list of all available events.
            - If priority is 0, all events are returned.
            - Otherwise only the events with the given priority are returned.
        8. get_available_events_with_fallback(priority: int = 0, **kwargs) -> List[Event]
            - Returns a list of all available events.
            - If priority is 0, all events are returned.
            - Otherwise only the events with the given priority are returned.
            - If no events are available, the fallback event is returned.
        9. call_available_event(priority: int = 0, **kwargs)
            - Calls all available events depending on the priority.
            - If priority is 0, all events are called.
            - Otherwise only the events with the given priority are called.
        10. check_all_events()
            - Checks if all events are created correctly.
        """

        def __init__(self, name: str, location: str, fallback: Event = None, fallback_text: str = "There is nothing to do here."):
            self.name = name
            self.fallback = fallback if fallback != None else default_fallback
            self.fallback_text = fallback_text
            self.events = {
                1: {},
                2: {},
                3: {},
            }
            self.location = location

        def _update(self):
            """
            Updates the title of the EventStorage.
            """

            if not hasattr(self, 'fallback_text'):
                self.fallback_text = "There is nothing to do here."

        def check_all_events(self):
            """
            Checks if all events are created correctly.
            If any event is not properly set up, an error message is printed.
            """

            for event in self.events[1].values():
                event.check_event()
            for event in self.events[2].values():
                event.check_event()
            for event in self.events[3].values():
                event.check_event()

        def register_event_for_location(self, event: Event, location: str):
            """
            Registers an event for a location.
            This is used to make sure that the event is only called when the player is at the location.

            ### Parameters:
            1. event: str
                - The event that is registered.
            2. location: str
                - The location that the event is registered for.
            """

            event.set_location(location)

            if location not in location_event_register.keys():
                location_event_register[location] = set()

            location_event_register[location].add(event)

        ###################
        # Attribute getters

        def get_fallback(self) -> Event:
            """
            Returns the fallback event of the EventStorage.

            ### Returns:
            1. Event
                - The fallback event of the EventStorage.
            """

            return self.fallback

        def get_name(self) -> str:
            """
            Returns the name of the EventStorage.

            ### Returns:
            1. str
                - The name of the EventStorage.
            """

            return self.name

        def get_location(self) -> str:
            """
            Returns the location of the EventStorage.

            ### Returns:
            1. str
                - The location of the EventStorage.
            """

            return self.location

        def get_type(self) -> str:
            """
            Returns the type of the EventStorage.

            ### Returns:
            1. str
                - The type of the EventStorage.
                - In this case "EventStorage"
            """

            return "EventStorage"

        ###############
        # Event Handler

        def add_event(self, *events: Event):
            """
            Adds an event to the EventStorage.
            The event gets sorted automatically into the correct priority.

            ### Parameters:
            1. *events: Event
                - The events that are added to the EventStorage.
            """

            for event in events:
                if event.get_priority() == 3 and event.get_event() not in seenEvents.keys():
                    seenEvents[event.get_event()] = False

                if event.get_id() not in self.events[event.get_priority()].keys():
                    if self.location != "":
                        self.register_event_for_location(event, self.location)
                    self.events[event.get_priority()][event.get_id()] = event

        def remove_event(self, event_id: str):
            """
            Removes an event from the EventStorage.
            """

            del self.events[1][event_id]
            del self.events[2][event_id]
            del self.events[3][event_id]

        ##############
        # Event getter

        def count_available_events(self, priority: int = 0, **kwargs) -> int:
            """
            Counts the number of events that are available.
            If priority is 0, all events are counted.

            ### Parameters:
            1. priority: int (Default 0)
                - The priority of the events that are counted.
                - If priority is 0, all events are counted.

            ### Returns:
            1. int
                - The number of events that are available.
                - If priority is 1 a maximum of 1 is returned.
                - If priority is 2 or 3 all available events of that priority are counted.
            """

            if "event_type" not in kwargs.keys():
                kwargs["event_type"] = self.name

            if priority == 0 or priority == 1:
                for event in self.events[1].values():
                    if event.is_available(**kwargs):
                        return 1
            if priority == 0 or priority == 2:
                output = 0
                for event in self.events[2].values():
                    if event.is_available(**kwargs):
                        output += 1
                if output != 0:
                    return output
            if priority == 0 or priority == 3:
                output = 0
                for event in self.events[3].values():
                    if event.is_available(**kwargs):
                        output += 1
                return output
            return 0

        def count_available_events_with_fallback(self, priority: int = 0, **kwargs) -> int:
            """
            Counts the number of events that are available.
            This method is the same as count_available_events except that if no events are available, 1 is returned representing the fallback event.

            ### Parameters:
            1. priority: int (Default 0)
                - The priority of the events that are counted.
                - If priority is 0, all events are counted.

            ### Returns:
            1. int
                - The number of events that are available.
                - If priority is 1 a maximum of 1 is returned.
                - If priority is 2 or 3 all available events of that priority are counted.
                - If no events are available, 1 is returned.
            """

            output = self.count_available_events(priority, **kwargs)

            if output == 0:
                return 1
            return output

        def get_available_events(self, priority: int = 0, **kwargs) -> List[Event]:
            """
            Returns a list of all available events.
            If priority is 0, all available events are returned.
            Otherwise only the events with the given priority are returned.

            ### Parameters:
            1. priority: int (Default 0)
                - The priority of the events that are returned.
                - If priority is 0, all events are returned.

            ### Returns:
            1. List[Event]
                - A list of all available events.
                - If priority is 1 the first available event is returned.
                - If priority is 2 a list of all available events with priority 2 are returned
                - If priority is 3 a random event from all available priority 3 events is returned
            """
            
            if "event_type" not in kwargs.keys():
                kwargs["event_type"] = self.name

            if priority == 0 or priority == 1:
                for event in self.events[1].values():
                    if event.is_available(**kwargs):
                        return [event]

            if priority == 0 or priority == 2:
                output = []
                for event in self.events[2].values():
                    if event.is_available(**kwargs):
                        output.append(event)
                if len(output) != 0:
                    return output

            if priority == 0 or priority == 3:
                output = []
                for event in self.events[3].values():
                    if event.is_available(**kwargs):
                        output.append(event)
                if len(output) != 0:
                    return [random.choice(output)]

            return []

        def get_available_events_with_fallback(self, priority: int = 0, **kwargs) -> List[Event]:
            """
            Returns a list of all available events.
            This method is the same as get_available_events except that if no events are available, the fallback event is returned.

            ### Parameters:
            1. priority: int (Default 0)
                - The priority of the events that are returned.
                - If priority is 0, all events are returned.

            ### Returns:
            1. List[Event]
                - A list of all available events.
                - If priority is 1 the first available event is returned.
                - If priority is 2 a list of all available events with priority 2 are returned
                - If priority is 3 a random event from all available priority 3 events is returned
                - If no events are available, the fallback event is returned.
            """

            output = self.get_available_events(priority, **kwargs)

            if len(output) == 0:
                return [self.fallback]
            return output

        ##############
        # Event caller

        def call_available_event(self, priority: int = 0, **kwargs):
            """
            Calls all available events depending on the priority.
            If priority is 0, all events are called.
            If priority is 1 the first available priority 1 event is called.
            If priority is 2 all available priority 2 events are called.
            If priority is 3 a random event from all available priority 3 events is called.
            If no events are available, the fallback event is called.

            ### Parameters:
            1. priority: int (Default 0)
                - The priority of the events that are called.
                - If priority is 0, all events are called.
            """

            events = self.get_available_events_with_fallback(priority, **kwargs)

            kwargs["fallback_text"] = self.fallback_text

            if "event_type" not in kwargs.keys():
                kwargs["event_type"] = self.name


            for event in events:
                kwargs["event_name"] = event.get_event()
                event.call(**kwargs)

    class TempEventStorage(EventStorage):
        """
        Subclass of EventStorage.

        TempEventStorage is a class that stores events and can call them when needed.
        The difference to EventStorage is that TempEventStorage does not store the events permanently.
        Instead the events are removed from the TempEventStorage after they are called.

        ### Attributes:
        1. name: str
            - The name of the EventStorage. This is used to identify the EventStorage.
        2. fallback: Event
            - The fallback event that is called when no other events are available.
        3. events: List[Event]
            - The events that are stored in the EventStorage. The events are stored in a list.
        """

        def __init__(self, name: str, location: str = "", fallback: Event = None, fallback_text: str = "How did you end up here? That shouldn't have happened. Better notify the dev about this."):
            super().__init__(name, location, fallback, fallback_text)
            self.events = []

        def _update(self):
            pass

        def check_all_events(self):
            """
            Checks if all events are created correctly.
            If any event is not properly set up, an error message is printed.
            """

            for event in self.events:
                event.check_event()

        ##################
        # Attribute getter

        def get_type(self) -> str:
            """
            Returns the type of the EventStorage.

            ### Returns:
            1. str
                - The type of the EventStorage.
                - In this case "TempEventStorage"
            """

            return "TempEventStorage"

        ###############
        # Event handler

        def add_event(self, *event: Event):
            """
            Adds an event to the EventStorage.

            ### Parameters:
            1. *event: Event
                - The events that are added to the EventStorage.
            """

            if self.location != "":
                for event_obj in event:
                    self.register_event_for_location(event_obj, self.location)

            self.events.extend(event)

        def force_add_event(self, *event: Event):
            """
            Force-adds an event to the EventStorage.

            ### Parameters:
            1. *event: Event
                - The events that are added to the EventStorage.
            """

            if self.location != "":
                for event_obj in event:
                    self.register_event_for_location(event_obj, self.location)

            if not contains_game_data("temp_event_blocker"):
                set_game_data("temp_event_blocker", [])

            for event_obj in event:
                get_game_data("temp_event_blocker").remove(event_obj.get_id())
                self.events.append(event_obj)

        def remove_event(self, event_obj: str | Event):
            """
            Removes an event from the EventStorage.

            ### Parameters:
            1. event_obj: str | Event
                - The event that is removed from the EventStorage.
            """

            new_events = []

            if isinstance(event_obj, Event):
                event_obj = event_obj.get_id()
            self.events = list(filter(lambda event: event.get_id() != event_obj, self.events))

        ##############
        # Event getter

        def count_available_events(self, _priority = 0, **kwargs) -> int:
            """
            Counts the number of events that are available.

            ### Parameters:
            1. _priority: int (Default 0)
                - This parameter is not used

            ### Returns:
            1. int
                - The number of events that are available.
            """

            output = 0

            if "event_type" not in kwargs.keys():
                kwargs["event_type"] = self.name + "_timed"

            for event in self.events:
                if (event.is_available(**kwargs)):
                    output += 1

            return output

        def count_available_events_with_fallback(self, _priority = 0, **kwargs) -> int:
            """
            Counts the number of events that are available.
            This method is the same as count_available_events except that if no events are available, 1 is returned representing the fallback event.

            ### Parameters:
            1. _priority: int (Default 0)
                - This parameter is not used

            ### Returns:
            1. int
                - The number of events that are available.
                - If no events are available, 1 is returned.
            """

            output = 0

            if "event_type" not in kwargs.keys():
                kwargs["event_type"] = self.name + "_timed"

            for event in self.events:
                if (event.is_available(**kwargs)):
                    output += 1

            if output == 0:
                return 1
            return output

        def get_available_events(self, _priority = 0, **kwargs) -> List[Event]:
            """
            Returns a list of all available events.

            ### Parameters:
            1. _priority: int (Default 0)
                - This parameter is not used

            ### Returns:
            1. List[Event]
                - A list of all available events.
            """

            output = []

            if "event_type" not in kwargs.keys():
                kwargs["event_type"] = self.name + "_timed"

            for event in self.events:
                if event.is_available(**kwargs):
                    output.append(event)

            return output

        def get_available_events_with_fallback(self, _priority: int = 0, **kwargs) -> List[Event]:
            """
            Returns a list of all available events.
            This method is the same as get_available_events except that if no events are available, the fallback event is returned.

            ### Parameters:
            1. _priority: int (Default 0)
                - This parameter is not used

            ### Returns:
            1. List[Event]
                - A list of all available events.
                - If no events are available, the fallback event is returned.
            """

            output = self.get_available_events(**kwargs)

            if len(output) == 0:
                return [self.fallback]
            return output

        ##############
        # Event caller

        def call_available_event(self, _priority: int = 0, **kwargs):
            """
            Calls all available events.

            ### Parameters:
            1. _priority: int (Default 0)
                - This parameter is not used
            """

            events = self.get_available_events_with_fallback(**kwargs)

            for event in events:
                self.events.remove(event)

            if "event_type" not in kwargs.keys():
                kwargs["event_type"] = self.name + "_timed"

            if not contains_game_data("temp_event_blocker"):
                set_game_data("temp_event_blocker", [])

            temp_event_blocker = get_game_data("temp_event_blocker")

            for event in events:
                if event.get_id() != self.fallback.get_id():
                    if event.get_id() in temp_event_blocker:
                        continue

                    temp_event_blocker.append(event.get_id())

                event.call(**kwargs)

    class Event:
        """
        This class represents an event that can be called.

        ### Parameters:
        1. priority: int
            - The priority of the event.
            - 1 = highest (the first 1 to occur is called blocking all other events)
            - 2 = middle (all 2's are called after each other)
            - 3 = lowest (selected random among 3's)
        2. event: str
            - The name of the event. This is used to call the event.
        3. values: SelectorSet
            - The values that are passed to the event.
        4. *conditions: Condition
            - The conditions that need to be fulfilled for the event to be available.

        ### Attributes:
        1. event_id: str
            - The id of the event. This is used to identify the event.
        2. event: str | List[str]
            - The name of the event. This is used to call the event.
            - If the event is a single string it gets converted to a list containing this string.
        3. conditions: List[Condition]
            - A list of conditions that need to be fulfilled for the event to be available.
        4. priority: int
            - The priority of the event.
            - 1 = highest (the first 1 to occur is called blocking all other events)
            - 2 = middle (all 2's are called after each other)
            - 3 = lowest (selected random among 3's)
        5. event_type: str
            - The type of the event. This is used to identify the event type.

        ### Methods:
        1. get_id() -> str
            - Returns the id of the event.
        2. set_event_type(event_type: str)
            - Sets the event type of the event.
        3. add_event(*event: Event)
            - Adds an event to the event.
        4. get_event() -> List[str]
            - Returns the events depending on the priority.
        5. get_event_count() -> int
            - Returns the number of events stored.
        6. get_priority() -> int
            - Returns the priority of the event.
        7. is_available(**kwargs) -> bool
            - Returns True if all conditions are fulfilled.
        8. call(**kwargs)
            - Calls the event.
        """

        def __init__(self, priority: int, event: str, *conditions: Condition | Selector, thumbnail: str = ""):
            self.event_id = str(event)
            self.event = event
            self.thumbnail = thumbnail
            self.conditions = [condition for condition in conditions if isinstance(condition, Condition)]
            self.values = SelectorSet(*[condition for condition in conditions if isinstance(condition, Selector)])

            rerollSelectors.append(self.values)

            # self.conditions = list(conditions)

            # 1 = highest (the first 1 to occur is called blocking all other events)
            # 2 = middle (all 2's are called after each other)
            # 3 = lowest (selected random among 3's)
            self.priority = priority 
            self.event_type = ""
            # self.values = values

            

            event_register[self.event_id] = self
            self.location = "misc"

        def __str__(self):
            return self.event_id

        def __repr__(self):
            return self.event_id

        def _update(self, data: Dict[str, Any]):

            if not hasattr(self, 'event'):
                self.event = ""

            if not hasattr(self, 'event_id'):
                self.event_id = str(id(self))

            if not hasattr(self, 'conditions'):
                self.conditions = []

            if not hasattr(self, 'priority'):
                self.priority = 3

            if not hasattr(self, 'event_type'):
                self.event_type = ""

            if not hasattr(self, 'values'):
                self.values = []

            self.__dict__.update(data)

        def check_event(self):
            """
            Checks if the event is created correctly.
            If the event is not properly set up, an error message is printed. 
            It checks the following:
            1. If the priority is valid
            2. If all labels exist           
            """

            if self.priority < 1 or self.priority > 3:
                log_error(301, "Event " + self.event_id + ": Priority " + str(self.priority) + " is not valid!")

            if not renpy.has_label(self.event):
                log_error(302, "Event " + self.event_id + ": Label " + self.event + " is missing!")

        #############################
        # Attribute getter and setter

        def get_thumbnail(self) -> str:
            """
            Returns the thumbnail of the event.

            ### Returns:
            1. str
                - The thumbnail of the event.
            """

            if self.thumbnail == "":
                return "journal/empty_image_wide.webp"

            return self.thumbnail

        def get_id(self) -> str:
            """
            Returns the id of the event.

            ### Returns:
            1. str
                - The id of the event.
            """

            return self.event

        def get_location(self) -> str:
            """
            Returns the location of the event.

            ### Returns:
            1. str
                - The location of the event.
            """

            return self.location

        def set_location(self, location: str):
            """
            Sets the location of the event.

            ### Parameters:
            1. location: str
                - The location of the event.
            """

            self.location = location
            return

        def set_event_type(self, event_type: str):
            """
            Sets the event type of the event.
            DO NOT USE THIS METHOD DIRECTLY!
            This method is used by the EventStorage to set the event type to represent the source of the event.

            ### Parameters:
            1. event_type: str
                - The event type of the event.
            """

            self.event_type = event_type

        def get_event(self) -> str:
            """
            Returns the events depending on the priority.
            If the priority is 1 a list containing the first event is returned.
            If the priority is 2 a list containing all events is returned.
            If the priority is 3 a list containing a random event is returned.

            ### Returns:
            1. List[str]
                - A list containing the events depending on the priority.
            """

            return self.event

        def get_priority(self) -> int:
            """
            Returns the priority of the event.

            ### Returns:
            1. int
                - The priority of the event.
            """

            return self.priority

        ###############
        # Event handler

        def is_available(self, **kwargs) -> bool:
            """
            Checks if the event is available.
            If all conditions are fulfilled, True is returned.

            ### Parameters:
            1. **kwargs
                - The arguments that are passed to the conditions.

            ### Returns:
            1. bool
                - True if all conditions are fulfilled.
                - False if at least one condition is not fulfilled.
            """

            for condition in self.conditions:
                if not condition.is_fulfilled(**kwargs):
                    return False
            return True

        ##############
        # Event caller

        def call(self, **kwargs):
            """
            Calls the event.

            ### Parameters:
            1. **kwargs
                - The arguments that are passed to the event.
            """

            events = self.get_event()
            if "event_type" not in kwargs.keys():
                kwargs["event_type"] = self.event_type

            if self.values != None:
                kwargs.update(self.values.get_values())
                self.values.roll_values()

            kwargs["event_name"] = self.get_event()
            kwargs["in_event"] = True

            renpy.call("call_event", events, self.priority, **kwargs)

    #####################
    # Event label handler

    def begin_event(**kwargs):
        """
        This method is called at the start of an event after choices and topics have been chosen in the event.
        It prevents rollback to before this method and thus prevents changing choices and topics.
        """

        global seenEvents

        event_name = get_kwargs("event_name", "", **kwargs)
        in_replay = get_kwargs("in_replay", False, **kwargs)

        if event_name != "" and not in_replay:
            gallery_manager = Gallery_Manager(**kwargs)

        if contains_game_data("seen_events"):
            seenEvents = get_game_data("seen_events")

        if event_name != "" and event_name in seenEvents.keys():
            seenEvents[event_name] = True
            set_game_data("seen_events", seenEvents)
            if all(seenEvents.values()):
                set_game_data("all_events_seen", True)

        if in_replay:
            char_obj = None

        renpy.block_rollback()

        if event_name != "":
            renpy.call("show_sfw_text", event_name)

    def end_event(return_type: str = "new_daytime", **kwargs):

        global is_in_replay

        is_in_replay = False

        in_replay = get_kwargs("in_replay", False, **kwargs)
        if in_replay:
            is_in_replay = False
            display_journal = get_kwargs("journal_display", "", **kwargs)
            renpy.call("open_journal", 7, display_journal, from_current = False)
            return

        if return_type == "new_daytime":
            renpy.jump("new_daytime")
        elif return_type == "new_day":
            renpy.jump("new_day")
        elif return_type == "none":
            return
        else:
            renpy.jump("map_overview")

    def get_event_from_register(name: str) -> Event:
        """
        Gets an event from the event register

        ### Parameters:
        1. name: str
            - The name of the event

        ### Returns:
        1. Event
            - The event
            - If the event does not exist None is returned
        """

        if name in event_register.keys():
            return event_register[name]
        return None
#################

##############
# Event caller

label call_available_event(event_storage, priority = 0, no_fallback = False, **kwargs):
    # """
    # Calls all available events depending on the priority.

    # ### Parameters:
    # 1. event_storage: EventStorage | TempEventStorage
    #     - The event storage that is used to call the events.
    #     - If the event storage is a TempEventStorage, the events are removed from the storage after they are called.
    # 2. priority: int (Default 0)
    #     - The priority of the events that are called.
    #     - If priority is 0, all events are called.
    # 3. **kwargs
    #     - The arguments that are passed to the events.
    # """

    $ events_list = []

    if no_fallback:
        $ events_list = event_storage.get_available_events(priority, **kwargs)
    else:
        $ events_list = event_storage.get_available_events_with_fallback(priority, **kwargs)

    $ log_val('event_list', events_list)

    if not contains_game_data("temp_event_blocker"):
        $ set_game_data("temp_event_blocker", [])

    $ temp_event_blocker = get_game_data("temp_event_blocker")

    $ i = 0
    while(len(events_list) > i):
        $ continue_loop = False
        $ event_obj = events_list[i]
        $ events = event_obj.get_event()
        if "event_type" not in kwargs.keys():
            $ kwargs["event_type"] = event_obj.event_type

        if event_storage.get_type() == "TempEventStorage":
            $ event_storage.remove_event(event_obj.get_id())

            if event_obj.get_id() in temp_event_blocker:
                $ continue_loop = True
            else:
                $ temp_event_blocker.append(event_obj.get_id())

        if not continue_loop or event_obj.get_id() == event_storage.get_fallback().get_id():
            $ kwargs["event_name"] = event_obj.get_event()
            $ kwargs["in_event"] = True

            $ renpy.call(events, **kwargs)
        $ i += 1

    return

label call_event(event_obj, priority = 0, **kwargs):
    # """
    # Calls all available events depending on the priority.

    # ### Parameters:
    # 1. event_obj: str | List[str] | Event | EventStorage | TempEventStorage
    #     - The event that is called.
    #     - If the event is a string, the event is called.
    #     - If the event is a list of strings, all events in the list are called.
    #     - If the event is an Event, the event is called.
    #     - If the event is an EventStorage, all events in the EventStorage are called.
    #     - If the event is a TempEventStorage, all events in the TempEventStorage are called.
    # """

    if isinstance(event_obj, EventStorage):
        $ event_obj.call_available_event(**kwargs)
    if isinstance(event_obj, Event):
        $ event_obj.call(**kwargs)
    if isinstance(event_obj, str):
        if renpy.has_label(event_obj):
            $ gallery_manager = None
            $ kwargs["event_name"] = event_obj
            $ kwargs["in_event"] = True
            $ renpy.call(event_obj, from_current="call_event_1", **kwargs)
    if isinstance(event_obj, list):
        $ i = 0
        while(len(event_obj) > i):
            if renpy.has_label(event_obj[i]):
                $ gallery_manager = None
                $ kwargs["event_name"] = event_obj[i]
                $ kwargs["in_event"] = True
                $ renpy.call(event_obj[i], from_current="call_event_2", **kwargs)
            $ i += 1

    return

#######################
# Default event handler

label default_fallback_event (**kwargs):

    $ local_subtitles = Character(
        None,
        window_background = None,
        what_color = "#ffffff",
        what_size = 28,
        what_outlines = [( 1, "#000000", 0, 0 )],
        what_xalign = 0.5,
        what_textalign = 0,
        what_layout = 'subtitle'
    )

    $ text = "There is nothing to do here."

    if "fallback_text" in kwargs.keys():
        $ text = kwargs["fallback_text"]

    $ local_subtitles(text)
    jump map_overview
