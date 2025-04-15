init -2 python:
    default_fallback = Event(2, "default_fallback_event")

init -3 python:
    import re
    import random
    import time
    from typing import Any, Dict, List, Tuple, Union
    
    seenEvents = {}
    highlight_register = {}

    ###########################
    # region Register Methods #

    def register_highlighting(*storages: EventStorage):
        for storage in storages:
            if storage.get_location() == "fragment":
                continue
            if storage.get_location() not in highlight_register.keys():
                highlight_register[storage.get_location()] = {}
            highlight_register[storage.get_location()][storage.get_name()] = storage

    def is_highlight_for_location_available(location: str) -> bool:
        if location not in highlight_register.keys():
            return False
        return any(storage.has_available_highlight_events() for storage in highlight_register[location].values())

    def is_event_for_location_available(location: str) -> bool:
        if location not in highlight_register.keys():
            return False
        return any(storage.has_available_events() for storage in highlight_register[location].values())

    def update_available_highlights():
        for location in highlight_register.keys():
            overview_highlight_available[location] = is_highlight_for_location_available(location)

    def update_available_events():
        for location in highlight_register.keys():
            overview_events_available[location] = is_event_for_location_available(location)

    def get_available_highlight(location: str) -> bool:
        if location not in overview_highlight_available.keys():
            return False
        return overview_highlight_available[location]

    def get_available_event(location: str) -> bool:
        if location not in overview_events_available.keys():
            return False
        return overview_events_available[location]

    # endregion
    ###########################

    ######################
    # region Seen Events #

    def register_seen_event(event: str):
        global seenEvents
        if seenEvents == None:
            seenEvents = {}
        if event not in seenEvents.keys():
            seenEvents[event] = False

    def set_event_seen(event_name: str):
        if not is_event_registered(event_name):
            return

        global seenEvents

        seen_events = get_game_data("seen_events")
        if seen_events == None:
            seen_events = {}
        for event, seen in seen_events.items():
            if event in seenEvents:
                seenEvents[event] = seenEvents[event] or seen
            else:
                seenEvents[event] = seen
        
        seenEvents[event_name] = True
        set_game_data("seen_events", seenEvents)

        if all(seenEvents.values()):
            set_game_data("all_events_seen", True)

    def get_event_seen(event_name: str) -> bool:
        if not is_event_registered(event_name):
            return False

        global seenEvents

        if event_name not in seenEvents.keys():
            return False
        return seenEvents[event_name]

    # endregion
    ######################

    ########################
    # region Event classes #
    ########################

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

        def __init__(self, name: str, location: str, *options: Option, fallback: Event = None, fallback_text: str = "There is nothing to do here."):
            self.name = name
            self.fallback = fallback if fallback != None else default_fallback
            self.fallback_text = fallback_text
            self.events = {
                1: {},
                2: {},
                3: {},
            }
            self.location = location
            options = list(options)
            self.options = {option.get_name(): option for option in options if isinstance(option, Option)}

        def _update(self):
            """
            Updates the title of the EventStorage.
            """

            if not hasattr(self, 'fallback_text'):
                self.fallback_text = "There is nothing to do here."

            if not hasattr(self, 'options'):
                self.options = {}

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

            if event.override_location != None:
                location = event.override_location

            event.set_location(location)

            if location not in location_event_register.keys():
                location_event_register[location] = set()

            location_event_register[location].add(event)

        def check_all_options(self, **kwargs):
            for key in self.options.keys():
                if not self.options[key].check_option(**kwargs):
                    return False
            return True
        
        def check_for_option(self, name: str, **kwargs):
            if name not in self.options.keys():
                return False
            return self.options[name].check_option(**kwargs)

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

        ###################

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

            if not is_mod_active(active_mod_key):
                return

            for event in events:
                register_seen_event(event.get_event())

                if event.get_id() not in self.events[event.get_select_type()].keys():
                    self.register_event_for_location(event, self.location)    
                    self.events[event.get_select_type()][event.get_id()] = event

        def overwrite_event(self, *event: Event):
            """
            Adds an event to the EventStorage.
            Overwrites the event if it already exists.
            The event gets sorted automatically into the correct priority.

            ### Parameters:
            1. *events: Event
                - The events that are added to the EventStorage.
            """

            if not is_mod_active(active_mod_key):
                return

            for event in events:
                register_seen_event(event.get_event())

                self.register_event_for_location(event, self.location)    
                self.events[event.get_select_type()][event.get_id()] = event

        def remove_event(self, event_id: str):
            """
            Removes an event from the EventStorage.
            """

            del self.events[1][event_id]
            del self.events[2][event_id]
            del self.events[3][event_id]

        ###############

        ##############
        # Event getter

        def get_events(self, priority: int = 0) -> List[Event]:
            """
            Returns a list of all events.
            If priority is 0, all events are returned.
            Otherwise only the events with the given priority are returned.

            ### Parameters:
            1. priority: int (Default 0)
                - The priority of the events that are returned.
                - If priority is 0, all events are returned.

            ### Returns:
            1. List[Event]
                - A list of all events.
                - If priority is 1 all events with priority 1 are returned.
                - If priority is 2 all events with priority 2 are returned.
                - If priority is 3 all events with priority 3 are returned.
            """

            if priority == 1:
                return list(self.events[1].values())
            if priority == 2:
                return list(self.events[2].values())
            if priority == 3:
                return list(self.events[3].values())
            return list(self.events[1].values()) + list(self.events[2].values()) + list(self.events[3].values())

        def get_event_by_index(self, index: int, priority: int = 0) -> Event:
            """
            Returns an event by its index.
            If priority is 0, all events are considered.
            Otherwise only the events with the given priority are considered.

            ### Parameters:
            1. index: int
                - The index of the event.
            2. priority: int (Default 0)
                - The priority of the events that are considered.
                - If priority is 0, all events are considered.

            ### Returns:
            1. Event
                - The event with the given index.
            """

            event_list = self.get_events(priority)

            if index < 0 or index >= len(event_list):
                return None
            else:
                return event_list[index]

        def has_available_highlight_events(self, **kwargs) -> bool:
            """
            Returns True if there are any events with priority 1 or 2 that are available.

            ### Returns:
            1. bool
                - True if there are any events with priority 1 or 2 that are available.
                - False if there are no events with priority 1 or 2 that are available.
            """

            return any(event.is_highlighted(**kwargs) for priority in self.events.values() for event in priority.values())

        def has_available_high_prio_events(self, **kwargs) -> bool:
            """
            Returns True if there are any events with priority 1 or 2 that are available.

            ### Returns:
            1. bool
                - True if there are any events with priority 1 or 2 that are available.
                - False if there are no events with priority 1 or 2 that are available.
            """

            for event in self.events[1].values():
                if event.is_available(**kwargs):
                    return True
            for event in self.events[2].values():
                if event.is_available(**kwargs):
                    return True
            return False

        def has_available_events(self, priority: int = 0, **kwargs) -> bool:
            return self.count_available_events(priority, **kwargs) > 0

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

            return self.count_available_events_and_prio(priority, **kwargs)[0]

        def count_available_events_and_prio(self, priority: int = 0, **kwargs) -> Tuple[int, bool]:
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
                        return 1, True
            if priority == 0 or priority == 2:
                output = 0
                for event in self.events[2].values():
                    if event.is_available(**kwargs):
                        output += 1
                if output != 0:
                    return output, True
            if priority == 0 or priority == 3:
                output = 0
                for event in self.events[3].values():
                    if event.is_available(**kwargs):
                        output += 1
                return output, False
            return 0, False

        def count_available_events_and_highlight(self, priority: int = 0, **kwargs) -> Tuple[int, bool]:
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
                    if event.is_available(**kwargs) and event.check_options(Highlight = True, **kwargs):
                        return 1, True
            if priority == 0 or priority == 2:
                output = 0
                for event in self.events[2].values():
                    if event.is_available(**kwargs) and event.check_options(Highlight = True, **kwargs):
                        output += 1
                if output != 0:
                    return output, True
            if priority == 0 or priority == 3:
                output = 0
                with_highlight = False
                for event in self.events[3].values():
                    if event.force_highlight:
                        with_highlight = True
                    if event.is_available(**kwargs) and event.check_options(Highlight = True, **kwargs):
                        output += 1
                return output, with_highlight
            return 0, False

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

            return self.count_available_events_with_fallback_and_prio(priority, **kwargs)[0]

        def count_available_events_with_fallback_and_prio(self, priority: int = 0, **kwargs) -> Tuple[int, bool]:
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

            output, prio = self.count_available_events_and_prio(priority, **kwargs)

            if output == 0:
                return 1, False
            return output, prio

        def count_available_events_with_fallback_and_highlight(self, priority: int = 0, **kwargs) -> Tuple[int, bool]:
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

            output, prio = self.count_available_events_and_highlight(priority, **kwargs)

            if output == 0:
                return 1, False
            return output, prio

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
                events = get_highest_priority_available_events(*self.events[1].values(), **kwargs)
                if len(events) != 0:
                    return [events[0]]
                # for event in self.events[1].values():
                #     if event.is_available(**kwargs):
                #         return [event]

            if priority == 0 or priority == 2:
                output = get_highest_priority_available_events(*self.events[2].values(), **kwargs)
                if len(output) != 0:
                    return output
                # output = []
                # for event in self.events[2].values():
                #     if event.is_available(**kwargs):
                #         output.append(event)
                # if len(output) != 0:
                #     return output

            if priority == 0 or priority == 3:
                output = get_highest_priority_available_events(*self.events[3].values(), **kwargs)
                # for event in self.events[3].values():
                #     if event.is_available(**kwargs):
                #         output.append(event)
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

        def get_one_possible_event(self, priority: int = 0, **kwargs) -> Event:
            """
            Returns a random event from the available events.
            If no events are available, the fallback event is returned.

            ### Parameters:
            1. priority: int (Default 0)
                - The priority of the events that are returned.
                - If priority is 0, all events are returned.

            ### Returns:
            1. Event
                - A random event from the available events.
                - If no events are available, the fallback event is returned.
            """

            repeatable = get_kwargs("repeatable", False, **kwargs)
            used_events = get_kwargs("used_events_repeatable", [], **kwargs)

            events = self.get_available_events(priority, **kwargs)
            if not repeatable:
                events = [event for event in events if event not in used_events]
            if len(events) == 0:
                return None
            return random.choice(events)

        def get_one_possible_event_with_fallback(self, priority: int = 0, **kwargs) -> Event:
            """
            Returns a random event from the available events.
            If no events are available, the fallback event is returned.

            ### Parameters:
            1. priority: int (Default 0)
                - The priority of the events that are returned.
                - If priority is 0, all events are returned.

            ### Returns:
            1. Event
                - A random event from the available events.
                - If no events are available, the fallback event is returned.
            """

            events = self.get_available_events_with_fallback(priority, **kwargs)
            if len(events) == 0 and self.fallback == None:
                return None
            elif len(events) == 0:
                return self.fallback
            return random.choice(events)

        ##############

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

        ##############

    class FragmentStorage(EventStorage):
        def __init__(self, name: str, *options: Option):
            super().__init__(name, "fragment", *options, None, "")

            # FragmentRepeatOption handling
            self.repeat_amount = 1
            self.repeat_repeatable = False # determines if a fragment can occur multiple times during repeating
            for option in options:
                if isinstance(option, FragmentRepeatOption):
                    option_data = option.get_values()
                    self.repeat_amount = get_kwargs("number", 1, **option_data)
                    self.repeat_repeatable = get_kwargs("repeatable", False, **option_data)
                    break

            self.register_storage_as_fragment()
        
        def add_event(self, *events: EventFragment):
            """
            Adds an event to the EventStorage.
            The event gets sorted automatically into the correct priority.

            ### Parameters:
            1. *events: Event
                - The events that are added to the EventStorage.
            """

            for event in events:
                register_seen_event(event.get_event())

                if event.get_id() not in self.events[event.get_select_type()].keys():
                    self.register_event_for_location(event, 'fragment')
                    self.events[event.get_select_type()][event.get_id()] = event
        
        def register_storage_as_fragment(self):
            """
            Registers the EventStorage as a fragment.
            This is used to make sure that the EventStorage is not saved in the save file.
            """

            if self.get_name() not in fragment_storage_register.keys():
                fragment_storage_register[self.get_name()] = self

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

        def __init__(self, name: str, location: str, *options: Option, fallback: Event = None, fallback_text: str = "How did you end up here? That shouldn't have happened. Better notify the dev about this."):
            super().__init__(name, location, *options, fallback = fallback, fallback_text = fallback_text)
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

        def has_available_highlight_events(self, **kwargs) -> bool:
            """
            Returns True if there are any events with priority 1 or 2 that are available.

            ### Returns:
            1. bool
                - True if there are any events with priority 1 or 2 that are available.
                - False if there are no events with priority 1 or 2 that are available.
            """

            for event in self.events:
                if event.is_available(**kwargs) and event.check_options(Highlight = True, **kwargs):
                    return True
            return False

        def has_available_high_prio_events(self, **kwargs) -> bool:
            """
            Returns True if there are any events with priority 1 or 2 that are available.

            ### Returns:
            1. bool
                - True if there are any events with priority 1 or 2 that are available.
                - False if there are no events with priority 1 or 2 that are available.
            """

            for event in self.events:
                if event.is_available(**kwargs):
                    return True
            return False

        def has_available_events(self, _priority = 0, **kwargs) -> bool:
            return self.count_available_events(_priority, **kwargs) > 0

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

            return self.count_available_events_and_prio(**kwargs)[0]

        def count_available_events_and_prio(self, _priority = 0, **kwargs) -> Tuple[int, bool]:
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

            return output, output != 0

        def count_available_events_and_highlight(self, _priority = 0, **kwargs) -> Tuple[int, bool]:
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
                if event.is_available(**kwargs) and event.check_options(Highlight = True, **kwargs):
                    output += 1

            return output, output != 0
        

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

            return self.count_available_events_with_fallback_and_prio(**kwargs)[0]

        def count_available_events_with_fallback_and_prio(self, _priority = 0, **kwargs) -> Tuple[int, bool]:
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
                return 1, False
            return output, True

        def count_available_events_with_fallback_and_highlight(self, _priority = 0, **kwargs) -> Tuple[int, bool]:
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
                if event.is_available(**kwargs) and event.check_options(Highlight = True, **kwargs):
                    output += 1

            if output == 0:
                return 1, False
            return output, True

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
        3. *conditions: Condition | Selector | Option
            - A list of conditions, Selectors or Options
            - The conditions need to be fulfilled for the event to be available.
            - The Selectors are used to store values that can be used in the event.
            - The Options are used to apply options to the event
        4. thumbnail: str (Default "")
            - The thumbnail of the event.
        5. register_self: bool (Default True)
            - If True, the event is registered in the event_register.
        6. override_intro: bool (Default False)
            - If True, the intro condition is ignored.
        7. override_location: str (Default None)
            - If set, the location of the event is set to this value.

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
        6. get_select_type() -> int
            - Returns the select type of the event.
        7. is_available(**kwargs) -> bool
            - Returns True if all conditions are fulfilled.
        8. call(**kwargs)
            - Calls the event.
        """

        def __init__(self, select_type: int, event: str, *options: Condition | Selector | Option | Pattern, thumbnail: str = "", register_self = True, override_intro = False, override_location = None):
            self.event_id = str(event)
            self.event = event
            self.thumbnail = thumbnail

            self.conditions = []
            self.values = SelectorSet()
            self.options = OptionSet()
            self.patterns = {}
            self.priority = 1
            self.force_highlight = False

            has_intro_condition = False
            for value in options:
                if isinstance(value, Condition):
                    if isinstance(value, IntroCondition):
                        has_intro_condition = True
                    self.conditions.append(value)
                elif isinstance(value, Selector):
                    self.values.add_selector(value)
                elif isinstance(value, Option):
                    if isinstance(value, ForceHighlightOption):
                        self.force_highlight = True
                    if isinstance(value, PriorityOption):
                        self.priority = value.priority
                    else:
                        self.options.add_option(value)
                elif isinstance(value, Pattern):
                    self.patterns[value.get_name()] = value

            if not has_intro_condition and not override_intro:
                self.conditions.append(IntroCondition(False))

            rerollSelectors.append(self.values)

            # 1 = highest (the first 1 to occur is called blocking all other events)
            # 2 = middle (all 2's are called after each other)
            # 3 = lowest (selected random among 3's)
            self.select_type = select_type

            self.event_type = ""

            change_mod_event_count(active_mod_key, 1)

            if register_self and is_mod_active(active_mod_key):
                event_register[self.event_id] = self
            self.location = "misc"
            self.override_location = override_location
            if self.override_location != None:
                self.location = override_location

            self.event_form = "event"
            self._invalid = False

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
                self.priority = 1

            if not hasattr(self, 'select_type'):
                self.select_type = 3

            if not hasattr(self, 'event_type'):
                self.event_type = ""

            if not hasattr(self, 'values'):
                self.values = []

            if not hasattr(self, 'event_form'):
                self.event_form = "event"

            if not hasattr(self, 'patterns'):
                self.patterns = {}

            self.__dict__.update(data)

        def check_event(self):
            """
            Checks if the event is created correctly.
            If the event is not properly set up, an error message is printed. 
            It checks the following:
            301. If the priority is valid
            302. If all labels exist           
            """

            if self.select_type < 1 or self.select_type > 3:
                log_error(301, "Event " + self.event_id + ": Select Type " + str(self.select_type) + " is not valid!")
                self._invalid = True

            if not renpy.has_label(self.event):
                log_error(302, "Event " + self.event_id + ": Label " + self.event + " is missing!")
                self._invalid = True

        def check_options(self, **kwargs) -> bool:
            """
            Checks if all options are available.
            If an option is not available, it is removed from the event.
            """

            return self.options.check_options(**kwargs)

        def is_highlighted(self, **kwargs) -> bool:
            return self.is_available(**kwargs) and (self.select_type != 3 or self.force_highlight) and self.check_options(Highlight = True, parent_event = self, **kwargs)

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

        def get_form(self) -> str:
            """
            Returns the form of the event.

            ### Returns:
            1. str
                - The form of the event.
            """

            return self.event_form

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

        def set_pattern(self, name: str, pattern: Pattern):
            self.patterns[name] = pattern

        def get_pattern(self) -> Dict[str, Pattern]:
            return self.patterns

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

        def get_event_label(self) -> str:
            return self.get_event()

        def get_select_type(self) -> int:
            """
            Returns the select type of the event.

            ### Returns:
            1. int
                - The select type of the event.
            """

            return self.select_type

        def get_priority(self) -> int:
            """
            Returns the priority of the event.

            ### Returns:
            1. int
                - The priority of the event.
            """

            return self.priority

        def get_name(self) -> str:
            """
            Returns the name of the event.

            ### Returns:
            1. str
                - The name of the event.
            """

            return self.event

        #############################

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

            if self._invalid:
                return False

            kwargs["event_name"] = self.get_name()
            
            if "values" not in kwargs.keys():
                kwargs["values"] = {}

            kwargs["values"].update(self.values.get_values())

            for condition in self.conditions:
                if not condition.is_fulfilled(**kwargs):
                    return False
            return True

        ###############

        ##############
        # Event caller

        def call(self, **kwargs):
            """
            Calls the event.

            ### Parameters:
            1. **kwargs
                - The arguments that are passed to the event.
            """

            events = self.get_event_label()
            if "event_type" not in kwargs.keys():
                kwargs["event_type"] = self.event_type

            kwargs["event_form"] = self.event_form

            if "values" not in kwargs.keys():
                kwargs["values"] = {}



            if self.values != None:
                kwargs["values"].update(self.values.get_values())
                self.values.roll_values()

            kwargs["event_name"] = self.get_event()
            kwargs["in_event"] = True
            kwargs["event_obj"] = self

            kwargs['image_patterns'] = self.patterns

            renpy.call("call_event", events, self.select_type, self.get_event(), **kwargs)

        ##############

    class EventComposite(Event):
        """
        Subclass of Event.
        This class represents a composite event that is made up of multiple events.
        It takes a list of EventStorages and calls them in order.

        ### Parameters:
        1. priority: int
            - The priority of the event.
            - 1 = highest (the first 1 to occur is called blocking all other events)
            - 2 = middle (all 2's are called after each other)
            - 3 = lowest (selected random among 3's)
        2. event: str
            - The name of the event. This is used to call the event.
        3. fragments: List[EventStorage]
            - The fragments that are part of the composite event.
        4. *conditions: Condition
            - The conditions that need to be fulfilled for the event to be available.
        5. thumbnail: str
            - The thumbnail of the event.
        """

        def __init__(self, priority: int, event: str, fragments: List[FragmentStorage], *conditions: Condition | Selector | Option, thumbnail: str = ""):
            super().__init__(priority, event, *conditions, thumbnail = thumbnail)

            self.fragments = [fragment for fragment in fragments if isinstance(fragment, FragmentStorage)]
            
            if self.values == None:
                self.has_fragment_reroll_option = []
            else:
                self.has_fragment_reroll_option = [selector for selector in self.values._selectors if selector.get_option_set().has_option("FragmentReroll")]

            self.event_form = "composite"

        def _update(self, data: Dict[str, Any]):
            super()._update(data)

            if not hasattr(self, 'fragments'):
                self.fragments = []
            self.event_form = "composite"

        def check_event(self):
            """
            Checks if the event is created correctly.
            If the event is not properly set up, an error message is printed.
            It checks the following:
            301. If the priority is valid
            302. If all labels exist
            303. If there are fragments added
            304. If the fragments are EventStorages
            """

            super().check_event()

            if len(self.fragments) == 0:
                log_error(303, "Composite Event " + self.event_id + ": No fragments are added!")

            if any(not isinstance(fragment, EventStorage) or isinstance(fragment, TempEventStorage) for fragment in self.fragments):
                log_error(304, "Composite Event " + self.event_id + ": Fragments have to be EventStorages!")

        def get_event(self) -> str:
            """
            Returns the event.

            ### Returns:
            1. str
                - The event.
            """

            return self.event

        def get_event_label(self) -> str:
            """
            Returns the event label.
            """

            return self.event

        def get_length(self) -> int:
            """
            Returns the number of fragments.

            ### Returns:
            1. int
                - The number of fragments.
            """

            return len(self.fragments)

        def get_fragment_storages(self):
            """
            Returns the fragments.

            ### Returns:
            1. List[EventStorage]
                - The fragments.
            """

            return self.fragments

        def call_fragment(self, index: int, events: Event = None, **kwargs):
            """
            Calls a fragment.
            It selects the EventStorage at the index and gets one random event that fulfills the conditions from it.

            ### Parameters:
            1. **kwargs
                - The arguments that are passed to the event.
            """

            if index >= len(self.fragments):
                log_error(303, "Composite Event " + self.event_id + ": Index (" + str(index) + ") out of range!")
                return

            if events == None:
                events = self.fragments[index].get_one_possible_event(**kwargs)
            if events == None:
                log_error(304, "Composite Event " + self.event_id + ": No events available in fragment at index " + str(index) + "!")
                return

            if "event_type" not in kwargs.keys():
                kwargs["event_type"] = self.event_type

            kwargs["event_form"] = "fragment"

            if "values" not in kwargs.keys():
                kwargs["values"] = {}

            for selector in self.has_fragment_reroll_option:
                if not selector._realtime:
                    selector.update(**kwargs)

            if events.values != None:
                kwargs["values"].update(events.values.get_values())
                events.values.roll_values()

            kwargs["event_name"] = events.get_event()
            kwargs["in_event"] = True

            event_obj = get_event_from_register(events.get_event())

            kwargs["event_obj"] = event_obj

            kwargs['frag_image_patterns'] = event_obj.get_pattern()

            kwargs["frag_index"] = index
            kwargs["frag_parent"] = self
            kwargs["is_fragment"] = True

            if is_replay(**kwargs):
                kwargs['decision_data'] = persistent.gallery['fragment'][events.get_id()]['decisions']
                last_data = get_last_data('fragment', events.get_id())
                data_keys = list(last_data.keys())
                j = 0

                if "values" not in kwargs.keys():
                    kwargs["values"] = {}

                while j < len(data_keys):
                    data_key = data_keys[j]
                    kwargs["values"][data_key] = last_data[data_key]
                    j += 1
    
            renpy.call("call_event", events.get_event_label(), self.select_type, **kwargs)

        def select_fragments(self, **kwargs) -> List[Event]:
            """
            Selects all fragments that are available.
            It selects all fragments that have at least one event that fulfills the conditions.

            ### Parameters:
            1. **kwargs
                - The arguments that are passed to the conditions.

            ### Returns:
            1. List[Event]
                - A list of all fragments that are available.
            """

            output = []

            for i in range(len(self.fragments)):
                repeatable = self.fragments[i].repeat_repeatable
                repeat_count = self.fragments[i].repeat_amount
                kwargs["repeatable"] = repeatable
                if repeat_count == 1:
                    kwargs["used_events_repeatable"] = output
                    selected_event = self.fragments[i].get_one_possible_event(**kwargs)

                    if selected_event != None:
                        output.append(selected_event)
                    else:
                        log_error(304, "Composite Event " + self.event_id + ": No events available in fragment at index " + str(i) + "!")
                else:
                    count = 0
                    for j in range(repeat_count):
                        kwargs["used_events_repeatable"] = output
                        selected_event = self.fragments[i].get_one_possible_event(**kwargs)

                        if selected_event != None:
                            output.append(selected_event)
                            count += 1

                    if count == 0:
                        log_error(304, "Composite Event " + self.event_id + ": Not all events could be selected in fragment at index " + str(i) + "!")

            return output

    class EventSelect(Event):
        def __init__(self, priority: int, event: str, text: str, event_list: Dict[str, EventStorage], *conditions: Condition | Selector | Option, thumbnail: str = "", override_menu_exit: str = "map_overview", fallback: str = None, person: Person = None):
            super().__init__(priority, event, *conditions, thumbnail = thumbnail)

            self.text = text
            self.event_list = event_list
            self.override_menu_exit = override_menu_exit
            self.fallback = fallback or default_fallback
            self.person = person or character.subtitles
            self.event_form = "select"
            self.set_location("select")
            
        def _update(self, data: Dict[str, Any]):
            super()._update(data)

            self.event_form = "select"

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

            if self._invalid:
                return False

            if not super().is_available(**kwargs):
                return False
            
            for storage in self.event_list.values():
                if storage.has_available_events(**kwargs):
                    return True

            return False

        def get_event_label(self) -> str:
            return 'select_event_runner'
        
        def is_highlighted(self, **kwargs) -> bool:
            return any(e.has_available_highlight_events() for e in self.event_list.values())
        
        def call(self, **kwargs):
            
            if "values" not in kwargs.keys():
                kwargs["values"] = {}

            if self.values != None:
                kwargs.update(self.values.get_values())
                self.values.roll_values()

            renpy.call(
                "call_event", 
                self.get_event_label(), 
                self.select_type, 
                self.get_event_label(), 
                from_current="event_select_call_1",
                select_text = self.text,
                select_event_list = self.event_list, 
                select_override_menu_exit = self.override_menu_exit,
                select_fallback = self.fallback,
                select_person = self.person,
            **kwargs)

    class EventFragment(Event):
        def __init__(self, select_type: int, event: str, *conditions: Condition | Selector | Option, thumbnail: str = ""):
            super().__init__(select_type, event, *conditions, thumbnail = thumbnail)

            self.event_form = "fragment"
            self.set_location("fragment")

    # endregion
    ########################

    def get_highest_priority_events(*events: Event) -> List[Event]:
        curr_priority = 1
        output = []
        for event in events:
            if event.get_priority() == curr_priority:
                output.append(event)
            elif event.get_priority() > curr_priority:
                curr_priority = event.get_priority()
                output = [event]

        return output

    def get_highest_priority_available_events(*events: Event, **kwargs) -> List[Event]:
        curr_priority = 1
        output = []
        for event in events:
            if event.is_available(**kwargs):
                if event.get_priority() == curr_priority:
                    output.append(event)
                elif event.get_priority() > curr_priority:
                    curr_priority = event.get_priority()
                    output = [event]

        return output

    ##############################
    # region Event label handler #
    ##############################

    def get_event_menu_title(location: str, option: str) -> str:
        """
        Returns the title of the event menu.

        ### Parameters:
        1. location: str
            - The location of the event.
        2. option: str
            - The option of the event.

        ### Returns:
        1. str
            - The title of the event menu.
        """

        title = get_translation(f"event_{location}_{option}")
        if title == f"event_{location}_{option}":
            title = get_translation(f"event_{option}")
        if title == f"event_{option}":
            title = get_translation(option)
        return title

    def add_storage(event_dict: Dict[str, EventStorage], event_storage: EventStorage):
        """
        Adds an event storage to the event dictionary.

        ### Parameters:
        1. event_dict: Dict[str, EventStorage]
            - The event dictionary that the event storage is added to.
        2. event_storage: EventStorage
            - The event storage that is added to the event dictionary.
        """
        
        if not is_mod_active(active_mod_key):
            return

        register_highlighting(event_storage)

        event_dict[event_storage.get_name()] = event_storage

    def begin_event(version: str = "1", **kwargs):
        """
        This method is called at the start of an event after choices and topics have been chosen in the event.
        It prevents rollback to before this method and thus prevents changing choices and topics.
        It also starts the Gallery_Manager if the event is not in replay which is used to track and register 
        the used variables and decisions in the event.

        # Options:
            1. no_gallery = True
                - Gallery_Manager will not be initiated and event will not be registered into the gallery
        """

        global seenEvents
        global gallery_manager

        hide_all()

        event_name = get_kwargs("event_name", "", **kwargs)
        in_replay = get_kwargs("in_replay", False, **kwargs)
        no_gallery = get_kwargs("no_gallery", False, **kwargs)
        is_fragment = get_kwargs("is_fragment", False, **kwargs)
        is_decision_call = get_kwargs("is_decision_call", False, **kwargs)

        if in_replay:
            event = get_kwargs('event_name', None, **kwargs)
            event_form = get_kwargs('event_form', 'event', **kwargs)
            location = get_kwargs('location', 'misc', **kwargs)
            if is_event_registered(event):
                location = get_event_from_register(event).get_location()

            if not is_decision_call:
                if 'version' not in persistent.gallery[location][event]['options'].keys():
                    persistent.gallery[location][event]['options']['version'] = "1"
                
                if version != persistent.gallery[location][event]['options']['version']:
                    reset_gallery(location, event)
                    
                    if location not in persistent.gallery.keys():
                        location = ""

                    renpy.call("failed_replay_invalid_gallery", location)

        if not is_decision_call:
            gallery_manager = None
            if event_name != "" and not in_replay and not no_gallery:
                gallery_manager = Gallery_Manager(version = version, **kwargs)

        if not in_replay:
            set_event_seen(event_name)

        if in_replay:
            char_obj = None

        if not is_fragment:
            renpy.block_rollback()

        if not in_replay:
            update_quest("event", **kwargs)

        if event_name != "":
            renpy.call("show_sfw_text", event_name)

    def end_event(return_type: str = "new_daytime", **kwargs):
        """
        This method is called at the end of an event.
        It returns to the map overview or calls a new daytime event.
        In case of a replay, it returns to the journal.

        ### Parameters:
        1. return_type: str (Default "new_daytime")
            - The type of the return.
            - If return_type is "new_daytime", a new daytime event is called.
            - If return_type is "new_day", a new day event is called.
            - If return_type is "none", nothing is called.
        """

        global is_in_replay

        frags = get_kwargs("frag_order", [], **kwargs)
        frag_index = get_kwargs("frag_index", 0, **kwargs)
        frag_parent = get_kwargs("frag_parent", None, **kwargs)

        if len(frags) > 0 and frag_index + 1 < len(frags) and frag_index + 1 < len(frag_parent.fragments):
            kwargs["frag_index"] = frag_index + 1
            if frag_parent != None:
                frag_parent.call_fragment(frag_index + 1, frags[frag_index + 1], **kwargs)

        is_in_replay = False

        in_replay = get_kwargs("in_replay", False, **kwargs)
        if in_replay:
            is_in_replay = False
            display_journal = get_kwargs("journal_display", "", **kwargs)
            renpy.call("open_journal", 7, display_journal, from_current = False)
            return
        
        update_quest("event_end", **kwargs)

        if return_type == "new_daytime":
            renpy.jump("new_daytime")
        elif return_type == "new_day":
            renpy.jump("new_day")
        elif return_type == "none":
            return
        elif return_type == "custom":
            renpy.call(get_value_ng('return_label', 'map_overview', **kwargs))
        else:
            renpy.jump("map_overview")

    def is_event_registered(name: str) -> bool:
        """
        Checks if an event is registered.

        ### Parameters:
        1. name: str
            - The name of the event

        ### Returns:
        1. bool
            - True if the event is registered.
            - False if the event is not registered.
        """

        return name in event_register.keys()

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

    def get_fragment_storage_from_register(id: str) -> EventStorage:
        """
        Gets an event storage from the event register

        ### Parameters:
        1. id: str
            - The id of the event storage

        ### Returns:
        1. EventStorage
            - The event storage
            - If the event storage does not exist None is returned
        """

        if id in fragment_storage_register.keys():
            return fragment_storage_register[id]
        return None

    # endregion
    ##############################

#######################
# region Event caller #
#######################

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

    if not contains_game_data("temp_event_blocker"):
        $ set_game_data("temp_event_blocker", [])

    $ temp_event_blocker = get_game_data("temp_event_blocker")

    $ i = 0
    while(len(events_list) > i):
        $ continue_loop = False
        $ event_obj = events_list[i]
        $ events = event_obj.get_event_label()
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
            $ kwargs["event_obj"] = event_obj
            $ kwargs['image_patterns'] = event_obj.patterns

            if "values" not in kwargs.keys():
                $ kwargs["values"] = {}

            if event_obj.values != None:
                $ kwargs["values"].update(event_obj.values.get_values())
                $ event_obj.values.roll_values()

            $ renpy.call(events, **kwargs)
        $ i += 1

    return

label call_event(event_obj_var, priority = 0, event_obj_name = "", **kwargs):
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

    if isinstance(event_obj_var, EventStorage):
        $ event_obj_var.call_available_event(**kwargs)
    if isinstance(event_obj_var, Event):
        $ event_obj_var.call(**kwargs)
    if isinstance(event_obj_var, str):
        if renpy.has_label(event_obj_var):
            $ gallery_manager = None
            if event_obj_name == "":
                $ event_obj_name = event_obj_var
            $ kwargs["event_name"] = event_obj_name
            $ kwargs["in_event"] = True
            $ renpy.call(event_obj_var, from_current="call_event_1", **kwargs)
    if isinstance(event_obj_var, list):
        $ i = 0
        while(len(event_obj_var) > i):
            if renpy.has_label(event_obj_var[i]):
                $ gallery_manager = None
                if event_obj_name == "":
                    $ event_obj_name = event_obj_var[i]
                $ kwargs["event_name"] = event_obj_name
                $ kwargs["in_event"] = True
                $ renpy.call(event_obj_var[i], from_current="call_event_2", **kwargs)
            $ i += 1

    return

# endregion
#######################

################################
# region Default event handler #
################################

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

label test_normal_test_event(**kwargs):
    $ begin_event(**kwargs)

    $ test = get_value('test', **kwargs)
    $ test2 = get_value('test2', **kwargs)

    subtitles "Test Event [test] [test2]"

    call composite_event_runner(**kwargs) from _call_composite_event_runner_3

label select_event_runner(**kwargs):

    $ text = get_kwargs('select_text', "What do you want to do?", **kwargs)
    $ event_list = get_kwargs('select_event_list', None, **kwargs)
    $ override_menu_exit = get_kwargs('select_override_menu_exit', 'map_overview', **kwargs)
    $ fallback = get_kwargs('select_fallback', default_fallback, **kwargs)
    $ person = get_kwargs('select_person', character.subtitles, **kwargs)

    if len(event_list) != 0:
        call call_event_menu (
            text, 
            event_list,
            fallback,
            person,
            override_menu_exit = override_menu_exit,
            **kwargs
        ) from select_event_runner_1

    call expression override_menu_exit from select_event_runner_2

label composite_event_runner(**kwargs):

    $ event_obj = get_kwargs('event_obj', None, **kwargs)
    if event_obj == None:
        $ log_error(304, "Composite Event: No event object available!")
        $ end_event("map_overview", **kwargs)

    $ events = get_frag_list(**kwargs)

    if len(events) == 0:
        $ log_error(304, "Composite Event " + event_obj.event_id + ": No events available in fragments!")
        $ end_event("map_overview", **kwargs)

    $ kwargs["frag_order"] = events

    $ event_obj.call_fragment(0, events[0], **kwargs)
        
    $ end_event("map_overview", **kwargs)

# endregion
################################

########################
# region Movie Sandbox #
########################

init -1 python:
    sandbox_after_event_check      = Event(2, "start_sandbox.after_check")
    sandbox_check_events = EventStorage("sandbox_check_events", "misc", fallback = sandbox_after_event_check)

label start_sandbox (**kwargs):
    # """
    # This label starts the sandbox movie mode
    #
    # ### Parameters:
    # 1. naughty_map: Dict[str, Dict[str, List[str]]]
    #     - A mapping that defines what actions can be performed in what locations and what clothing can be worn.
    #    - The first key is the location, the second key is the position, and the value is a list of clothing options.
    # 2. level: int
    #     - The level of the character during the act.
    # 3. file_preset: str
    #     - The preset for the file name. It should contain the following placeholders: <location>, <position>, <clothing>, <variant>.
    # 4. movie_preset: str
    #     - The preset for the movie name. It should contain the following placeholders: <location>, <position>, <clothing>, <variant>.
    # 5. character: Character
    #     - The character that is involved in the act.
    # 6. kwargs: Dict[str, Any]
    #     - Additional keyword arguments.
    # """

    $ sandbox_data = kwargs

    call call_available_event(sandbox_check_events, **kwargs) from _call_call_available_event

label .after_check (**kwargs):

    $ kwargs = sandbox_data

    $ naughty_map = get_kwargs('naughty_map', **kwargs)
    $ cum_map = get_kwargs('cum_map', **kwargs)
    $ level = get_kwargs('level', **kwargs)

    $ kwargs['naughty_location'] = list(naughty_map.keys())[0]
    $ kwargs['naughty_position'] = list(naughty_map[get_kwargs('naughty_location', **kwargs)].keys())[0]
    $ kwargs['naughty_clothing'] = naughty_map[get_kwargs('naughty_location', **kwargs)][get_kwargs('naughty_position', **kwargs)][0]
    $ kwargs['is_cumming'] = False
    $ kwargs['naughty_variant'] = 0
    $ kwargs['no_gallery'] = True
    $ kwargs['override_menu_exit'] = None
    $ kwargs['override_menu_exit_with_kwargs'] = "start_sandbox.start"
    $ kwargs['naughty_level'] = level


    call .start( **kwargs) from _call_start_sandbox_start

label .start (**kwargs):

    $ location = get_kwargs('naughty_location', **kwargs)
    $ position = get_kwargs('naughty_position', **kwargs)
    $ clothing = get_kwargs('naughty_clothing', **kwargs)
    $ variant = get_kwargs('naughty_variant', **kwargs)
    $ is_cumming = get_kwargs('is_cumming', **kwargs)
    $ mapping = get_kwargs('naughty_map', **kwargs)
    $ cum_map = get_kwargs('cum_map', **kwargs)


    if position not in mapping[location]:
        $ position = list(mapping[location].keys())[0]

    if clothing not in mapping[location][position]:
        $ clothing = mapping[location][position][0]

    $ file_preset = get_kwargs('file_preset', **kwargs)
    if is_cumming:
        $ file_preset = file_preset.replace('.webm', '_cum.webm')

    $ file = file_preset.replace('<location>', location).replace('<position>', position).replace('<clothing>', clothing)
    $ max_variant = get_file_max_value('variant', file, 0, 100)
    
    if variant > max_variant:
        $ variant = 0

    $ movie_preset = get_kwargs('movie_preset', **kwargs)
    if is_cumming:
        $ movie_preset = movie_preset + "_cum_idle"

    $ movie = movie_preset.replace('<location>', location).replace('<position>', position).replace('<clothing>', clothing).replace('<variant>', str(variant))

    if is_cumming:
        $ idle_movie = movie.replace('cum_idle', 'cum')
        $ idle_file = file.replace('cum', 'cum_idle').replace('<variant>', str(variant))
        $ hide_all()
        # $ renpy.movie_cutscene(idle_file, None, 0)
        scene expression idle_movie with dissolveM
        $ renpy.pause(cum_map[location][position][clothing])
        $ hide_all()

    # play movies
    scene expression movie with dissolveM
    

    $ icons = []

    if len(mapping.keys()) > 1:
        $ icons.append("location")

    if len(mapping[location].keys()) > 1:
        $ icons.append("position")

    if len(mapping[location][position]) > 1:
        $ icons.append("clothing")

    if max_variant > 0:
        $ icons.append("variant")

    if location in cum_map.keys() and position in cum_map[location].keys() and clothing in cum_map[location][position].keys() and not is_cumming:
        $ icons.append("cumming")

    if location in cum_map.keys() and position in cum_map[location].keys() and clothing in cum_map[location][position].keys() and is_cumming:
        $ icons.append("return")

    call screen naughty_scene_icons(*icons)
    if _return == "change_location":
        call .change_location (**kwargs) from _call_start_sandbox_change_location
    elif _return == "change_position":
        call .change_position (**kwargs) from _call_start_sandbox_change_position
    elif _return == "change_clothing":
        call .change_clothing (**kwargs) from _call_start_sandbox_change_clothing
    elif _return == "change_variant":
        call .change_variant (**kwargs) from _call_start_sandbox_change_variant
    elif _return == "cum":
        call .trigger_cum (**kwargs) from _call_start_sandbox_trigger_cum
    elif _return == "return":
        call .return_cum (**kwargs) from _call_start_sandbox_return_cum
    elif _return == "stop":
        $ end_event('new_daytime', **kwargs)

label .change_location (**kwargs):
    $ elements = []

    $ kwargs['is_cumming'] = False

    python:
        for location in mapping.keys():
            elements.append((get_translation(location), ChangeKwargsEffect('naughty_location', location)))

    $ call_custom_menu_with_text("Where do you want to move to?", get_kwargs('character', character.subtitles, **kwargs), False, *elements, **kwargs)

label .change_position (**kwargs):
    $ location = get_kwargs('naughty_location', **kwargs)
    $ mapping = get_kwargs('naughty_map', **kwargs)

    $ kwargs['is_cumming'] = False

    $ elements = []
    python:
        for position in mapping[location].keys():
            elements.append((get_translation(position), ChangeKwargsEffect('naughty_position', position)))

    $ call_custom_menu_with_text("What do you want to do next?", get_kwargs('character', character.subtitles, **kwargs), False, *elements, **kwargs)

label .change_clothing (**kwargs):
    $ location = get_kwargs('naughty_location', **kwargs)
    $ position = get_kwargs('naughty_position', **kwargs)
    $ mapping = get_kwargs('naughty_map', **kwargs)

    $ kwargs['is_cumming'] = False

    $ elements = []
    python:
        for clothing in mapping[location][position]:
            # check if clothing string ends with "_[number]" and if yes extract the number
            if clothing[-1].isdigit():
                clothing_level = int(clothing.split('_')[-1])
                if level < clothing_level:
                    continue

            elements.append((get_translation(clothing), ChangeKwargsEffect('naughty_clothing', clothing)))

    $ call_custom_menu_with_text("What do you want me to wear?", get_kwargs('character', character.subtitles, **kwargs), False, *elements, **kwargs)

label .change_variant (**kwargs):
    $ location = get_kwargs('naughty_location', **kwargs)
    $ position = get_kwargs('naughty_position', **kwargs)
    $ clothing = get_kwargs('naughty_clothing', **kwargs)
    $ variant = get_kwargs('naughty_variant', **kwargs)

    $ kwargs['is_cumming'] = False

    $ file = get_kwargs('file_preset', **kwargs).replace('<location>', location).replace('<position>', position).replace('<clothing>', clothing)
    $ max_variant = get_file_max_value('variant', file, 0, 100)
    $ variant += 1
    if variant > max_variant:
        $ variant = 0
    $ kwargs['naughty_variant'] = variant
    call .start(**kwargs) from _call_start_sandbox_start_1

label .trigger_cum (**kwargs):
    $ location = get_kwargs('naughty_location', **kwargs)
    $ position = get_kwargs('naughty_position', **kwargs)
    $ clothing = get_kwargs('naughty_clothing', **kwargs)
    $ variant = get_kwargs('naughty_variant', **kwargs)
    $ kwargs["is_cumming"] = True

    $ file = get_kwargs('file_preset', **kwargs).replace('<location>', location).replace('<position>', position).replace('<clothing>', clothing).replace('.webm', '_cum.webm')
    $ max_variant = get_file_max_value('variant', file, 0, 100)
    if variant > max_variant:
        $ variant = max_variant
    call .start(**kwargs) from _call_start_sandbox_start_2

label .return_cum (**kwargs):
    $ location = get_kwargs('naughty_location', **kwargs)
    $ position = get_kwargs('naughty_position', **kwargs)
    $ clothing = get_kwargs('naughty_clothing', **kwargs)
    $ variant = get_kwargs('naughty_variant', **kwargs)
    $ kwargs["is_cumming"] = False

    $ file = get_kwargs('file_preset', **kwargs).replace('<location>', location).replace('<position>', position).replace('<clothing>', clothing)
    $ max_variant = get_file_max_value('variant', file, 0, 100)
    if variant > max_variant:
        $ variant = max_variant
    call .start(**kwargs) from _call_start_sandbox_start_3

screen naughty_scene_icons(*icons):
    if "clothing" in icons:
        imagebutton:
            idle "icons/change_clothing_idle.webp"
            hover "icons/change_clothing_hover.webp"
            xalign 1.0 yalign 0.0
            action Return("change_clothing")
    if "position" in icons:
        imagebutton:
            idle "icons/change_position_idle.webp"
            hover "icons/change_position_hover.webp"
            xalign 1.0 yalign 0.2
            action Return("change_position")
    if "location" in icons:
        imagebutton:
            idle "icons/change_location_idle.webp"
            hover "icons/change_location_hover.webp"
            xalign 1.0 yalign 0.4
            action Return("change_location")
    if "variant" in icons:
        imagebutton:
            idle "icons/change_variant_idle.webp"
            hover "icons/change_variant_hover.webp"
            xalign 1.0 yalign 0.6
            action Return("change_variant")
    if "cumming" in icons:
        imagebutton:
            idle "icons/cum_idle.webp"
            hover "icons/cum_hover.webp"
            xalign 1.0 yalign 0.8
            action Return("cum")
    if "return" in icons:
        imagebutton:
            idle "icons/return_idle.webp"
            hover "icons/return_hover.webp"
            xalign 1.0 yalign 0.8
            action Return("return")
    imagebutton:
        idle "icons/stop_idle.webp"
        hover "icons/stop_hover.webp"
        xalign 1.0 yalign 1.0
        action Return("stop")

# endregion
########################

label failed_replay_invalid_gallery (display_journal):
    dev "Sorry, it seems the event you want to replay has been reworked and the gallery in the data is not valid anymore."
    dev "The gallery data for this event will now be reset, so it will continue to work in the future."
    dev "Unfortunately you'll have to unlock the event and it's variants again."
    dev "I apologize for the inconvenience!"

    $ is_in_replay = False
    $ renpy.call("open_journal", 7, display_journal, from_current = False)