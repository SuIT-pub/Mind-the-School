init -3 python:
    import re
    import random
    import time
    
    class EventStorage:
        """
        EventStorage is a class that stores events and can call them when needed.

        ### Attributes:
        1. name: str
            - The name of the EventStorage. This is used to identify the EventStorage.
        2. title: str
            - The title of the EventStorage. This is used for the GUI.
        3. fallback: Event
            - The fallback event that is called when no other events are available.
        4. events: Dict[int, Dict[str, Event]]
            - The events that are stored in the EventStorage. The events are stored in a dictionary with the priority as the key and the dictionary as a value.
            - The event Dictionary is a dictionary with the event id as the key and the event as the value.
            - Priority 1 represents an event that is called first and blocks all other events.
            - Priority 2 represents an Event that is called together with all other events with priority 2 and then moves on to priority 3.
            - Priority 3 represents a set of events from which one is called randomly.

        ### Methods:
        1. get_name() -> str
            - Returns the name of the EventStorage.
        2. get_title() -> str
            - Returns the title of the EventStorage.
        3. get_type() -> str
            - Returns the type of the EventStorage.
        4. add_event(event: Event)
            - Adds an event to the EventStorage.
        5. remove_event(event_id: str)
            - Removes an event from the EventStorage.
        6. count_available_events(priority: int = 0, **kwargs) -> int
            - Counts the number of events that are available.
            - If priority is 0, all events are counted.
            - Otherwise only the events with the given priority are counted.
        7. count_available_events_with_fallback(priority: int = 0, **kwargs) -> int
            - Counts the number of events that are available.
            - If priority is 0, all events are counted.
            - Otherwise only the events with the given priority are counted.
            - If no events are available, 1 is returned.
        8. get_available_events(priority: int = 0, **kwargs) -> List[Event]
            - Returns a list of all available events.
            - If priority is 0, all events are returned.
            - Otherwise only the events with the given priority are returned.
        9. get_available_events_with_fallback(priority: int = 0, **kwargs) -> List[Event]
            - Returns a list of all available events.
            - If priority is 0, all events are returned.
            - Otherwise only the events with the given priority are returned.
            - If no events are available, the fallback event is returned.
        10. call_available_event(priority: int = 0, **kwargs)
            - Calls all available events depending on the priority.
            - If priority is 0, all events are called.
            - Otherwise only the events with the given priority are called.
        11. check_all_events()
            - Checks if all events are created correctly.
        """

        def __init__(self, name: str, title: str, fallback: Event):
            self.name = name
            self.title = title
            self.fallback = fallback
            self.events = {
                1: {},
                2: {},
                3: {},
            }

        def _update(self, title: str):
            """
            Updates the title of the EventStorage.
            """

            self.title = title

        def get_name(self) -> str:
            """
            Returns the name of the EventStorage.

            ### Returns:
            1. str
                - The name of the EventStorage.
            """

            return self.name

        def get_title(self) -> str:
            """
            Returns the title of the EventStorage.

            ### Returns:
            1. str
                - The title of the EventStorage.
            """

            return self.title

        def get_type(self) -> str:
            """
            Returns the type of the EventStorage.

            ### Returns:
            1. str
                - The type of the EventStorage.
                - In this case "EventStorage"
            """

            return "EventStorage"

        def add_event(self, *events: Event):
            """
            Adds an event to the EventStorage.
            The event gets sorted automatically into the correct priority.

            ### Parameters:
            1. *events: Event
                - The events that are added to the EventStorage.
            """

            for event in events:
                if event.get_id() not in self.events[event.get_priority()].keys():
                    self.events[event.get_priority()][event.get_id()] = event

        def remove_event(self, event_id: str):
            """
            Removes an event from the EventStorage.
            """

            del self.events[1][event_id]
            del self.events[2][event_id]
            del self.events[3][event_id]


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

            if "event_type" not in kwargs.keys():
                kwargs["event_type"] = self.name

            for event in events:
                event.call(**kwargs)

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

    class TempEventStorage(EventStorage):
        """
        Subclass of EventStorage.

        TempEventStorage is a class that stores events and can call them when needed.
        The difference to EventStorage is that TempEventStorage does not store the events permanently.
        Instead the events are removed from the TempEventStorage after they are called.

        ### Attributes:
        1. name: str
            - The name of the EventStorage. This is used to identify the EventStorage.
        2. title: str
            - The title of the EventStorage. This is used for the GUI.
        3. fallback: Event
            - The fallback event that is called when no other events are available.
        4. events: List[Event]
            - The events that are stored in the EventStorage. The events are stored in a list.
        """

        def __init__(self, name: str, title: str, fallback: Event):
            super().__init__(name, title, fallback)
            self.events = []

        def _update(self, title):
            self.title = title

        def get_type(self) -> str:
            """
            Returns the type of the EventStorage.

            ### Returns:
            1. str
                - The type of the EventStorage.
                - In this case "TempEventStorage"
            """

            return "TempEventStorage"

        def add_event(self, *event: Event):
            """
            Adds an event to the EventStorage.

            ### Parameters:
            1. *event: Event
                - The events that are added to the EventStorage.
            """

            self.events.extend(event)

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

            for event in events:
                event.call(**kwargs)

        def check_all_events(self):
            """
            Checks if all events are created correctly.
            If any event is not properly set up, an error message is printed.
            """

            for event in self.events:
                event.check_event()

    class Event:
        """
        This class represents an event that can be called.

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

        def __init__(self, priority: int, event: str | List[str], *conditions: Condition):
            self.event_id = str(id(self))
            self.event = event
            if isinstance(self.event, str):
                self.event = [self.event]
            self.conditions = list(conditions)

            # 1 = highest (the first 1 to occur is called blocking all other events)
            # 2 = middle (all 2's are called after each other)
            # 3 = lowest (selected random among 3's)
            self.priority = priority 
            self.event_type = ""

        def __str__(self):
            return self.event_id

        def __repr__(self):
            return self.event_id

        def _update(self, data: Dict[str, Any]):
            if not hasattr(self, 'conditions'):
                self.conditions = []

            if not hasattr(self, 'priority'):
                self.priority = 3

            if not hasattr(self, 'event_type'):
                self.event_type = ""

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
                log_error(" at Event " + self.id + ": Priority " + str(self.priority) + " is not valid!")

            for event in self.event:
                if not renpy.has_label(event):
                    log_error(" at Event " + self.id + ": Label " + event + " is missing!")

        def get_id(self) -> str:
            """
            Returns the id of the event.

            ### Returns:
            1. str
                - The id of the event.
            """

            return self.event_id

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

        def add_event(self, *event: Event):
            """
            Adds an event to the event.

            ### Parameters:
            1. *event: Event
                - The events that are added to the event.
            """

            events = list(event)

            self.event.extend(events)

        def get_event(self) -> List[str]:
            """
            Returns the events depending on the priority.
            If the priority is 1 a list containing the first event is returned.
            If the priority is 2 a list containing all events is returned.
            If the priority is 3 a list containing a random event is returned.

            ### Returns:
            1. List[str]
                - A list containing the events depending on the priority.
            """

            if isinstance(self.event, str):
                return [self.event]
            else:
                if len(self.event) == 0:
                    return []
                if self.priority == 1:
                    return [self.event[0]]
                elif self.priority == 2:
                    return self.event
                else:
                    return [random.choice(self.event)]

        def get_event_count(self) -> int:
            """
            Returns the number of events stored.

            ### Returns:
            1. int
                - The number of events stored.
            """

            if isinstance(self.event, str):
                return 1
            else:
                return len(self.event)

        def get_priority(self) -> int:
            """
            Returns the priority of the event.

            ### Returns:
            1. int
                - The priority of the event.
            """

            return self.priority

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

            renpy.call("call_event", events, self.priority, **kwargs)

label call_available_event(event_storage, priority = 0, **kwargs):
    """
    Calls all available events depending on the priority.

    ### Parameters:
    1. event_storage: EventStorage | TempEventStorage
        - The event storage that is used to call the events.
        - If the event storage is a TempEventStorage, the events are removed from the storage after they are called.
    2. priority: int (Default 0)
        - The priority of the events that are called.
        - If priority is 0, all events are called.
    3. **kwargs
        - The arguments that are passed to the events.
    """

    $ events_list = event_storage.get_available_events_with_fallback(priority, **kwargs)

    $ i = 0
    while(len(events_list) > i):
        $ events = events_list[i].get_event()
        if "event_type" not in kwargs.keys():
            $ kwargs["event_type"] = events_list[i].event_type

        if event_storage.get_type() == "TempEventStorage":
            $ event_storage.remove_event(events_list[i].get_id())

        $ j = 0
        while (len(events) > j):
            $ renpy.call(events[j], **kwargs)
            $ j += 1
        $ i += 1

    return

label call_event(event_obj, priority = 0, **kwargs):
    """
    Calls all available events depending on the priority.

    ### Parameters:
    1. event_obj: str | List[str] | Event | EventStorage | TempEventStorage
        - The event that is called.
        - If the event is a string, the event is called.
        - If the event is a list of strings, all events in the list are called.
        - If the event is an Event, the event is called.
        - If the event is an EventStorage, all events in the EventStorage are called.
        - If the event is a TempEventStorage, all events in the TempEventStorage are called.
    """

    if isinstance(event_obj, EventStorage):
        $ event_obj.call_available_event(**kwargs)
    if isinstance(event_obj, Event):
        $ event_obj = event_obj.get_event()
    if isinstance(event_obj, str):
        if renpy.has_label(event_obj):
            $ renpy.call(event_obj, from_current="call_event_1", **kwargs)
    
    $ i = 0
    while(len(event_obj) > i):
        if renpy.has_label(event_obj[i]):
            $ renpy.call(event_obj[i], from_current="call_event_2", **kwargs)
        $ i += 1

    return