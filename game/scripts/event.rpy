init -3 python:
    import re
    import random
    import time
    
    class EventStorage:
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
            self.title = title

        def get_name(self):
            return self.name

        def get_title(self):
            return self.title

        def get_type(self):
            return "EventStorage"

        def add_event(self, event: Event):
            if event.get_id() not in self.events[event.get_priority()].keys():
                self.events[event.get_priority()][event.get_id()] = event

        def remove_event(self, event_id: str):
            del self.events[1][event_id]
            del self.events[2][event_id]
            del self.events[3][event_id]


        def count_available_events(self, priority: int = 0, **kwargs):
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

        def count_available_events_with_fallback(self, priority: int = 0, **kwargs):
            output = self.count_available_events(priority, **kwargs)

            if output == 0:
                return 1
            return output

        def get_available_events(self, priority: int = 0, **kwargs):
            
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

        def get_available_events_with_fallback(self, priority: int = 0, **kwargs):
            output = self.get_available_events(priority, **kwargs)

            if len(output) == 0:
                return [self.fallback]
            return output

        def call_available_event(self, priority: int = 0, **kwargs):
            events = self.get_available_events_with_fallback(priority, **kwargs)

            if "event_type" not in kwargs.keys():
                kwargs["event_type"] = self.name

            for event in events:
                event.call(**kwargs)

        def check_all_events(self):
            for event in self.events[1].values():
                event.check_event()
            for event in self.events[2].values():
                event.check_event()
            for event in self.events[3].values():
                event.check_event()

    class TempEventStorage(EventStorage):
        def __init__(self, name: str, title: str, fallback: Event):
            super().__init__(name, title, fallback)
            self.events = []

        def _update(self, title):
            self.title = title

        def get_name(self):
            return self.name

        def get_title(self):
            return self.title

        def get_type(self):
            return "TempEventStorage"

        def add_event(self, event: Event):
            self.events.append(event)

        def remove_event(self, event_obj: str | Event):
            new_events = []

            if isinstance(event_obj, Event):
                event_obj = event_obj.get_id()
            self.events = list(filter(lambda event: event.get_id() != event_obj, self.events))

        def count_available_events(self, _priority = 0, **kwargs):
            output = 0

            if "event_type" not in kwargs.keys():
                kwargs["event_type"] = self.name + "_timed"

            for event in self.events:
                if (event.is_available(**kwargs)):
                    output += 1

            return output

        def count_available_events_with_fallback(self, _priority = 0, **kwargs):
            output = 0

            if "event_type" not in kwargs.keys():
                kwargs["event_type"] = self.name + "_timed"

            for event in self.events:
                if (event.is_available(**kwargs)):
                    output += 1

            if output == 0:
                return 1
            return output

        def get_available_events(self, _priority = 0, **kwargs):
            output = []

            if "event_type" not in kwargs.keys():
                kwargs["event_type"] = self.name + "_timed"

            for event in self.events:
                if event.is_available(**kwargs):
                    output.append(event)

            return output

        def get_available_events_with_fallback(self, priority: int = 0, **kwargs):
            output = self.get_available_events(priority, **kwargs)

            if len(output) == 0:
                return [self.fallback]
            return output

        def call_available_event(self, priority: int = 0, **kwargs):
            events = self.get_available_events_with_fallback(priority, **kwargs)

            for event in events:
                self.events.remove(event)

            if "event_type" not in kwargs.keys():
                kwargs["event_type"] = self.name + "_timed"

            for event in events:
                event.call(**kwargs)

        def check_all_events(self):
            for event in self.events:
                event.check_event()

    class Event:
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
            for event in self.event:
                if not renpy.has_label(event):
                    log("|ERROR| at " + self.id + ": Label " + event + " is missing!")

        def get_id(self):
            return self.event_id

        def set_event_type(self, event_type: str):
            self.event_type = event_type

        def add_event(self, *event: Event):
            events = list(event)

            self.event.extend(events)

        def get_event(self):
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

        def get_event_count(self):
            if isinstance(self.event, str):
                return 1
            else:
                return len(self.event)

        def get_priority(self):
            return self.priority

        def is_available(self, **kwargs):
            for condition in self.conditions:
                if not condition.is_fulfilled(**kwargs):
                    return False
            return True

        def call(self, **kwargs):
            events = self.get_event()
            if "event_type" not in kwargs.keys():
                kwargs["event_type"] = self.event_type

            renpy.call("call_event", events, self.priority, **kwargs)

label call_available_event(event_storage, priority = 0, **kwargs):

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