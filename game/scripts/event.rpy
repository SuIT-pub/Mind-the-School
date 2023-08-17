init -3 python:
    import re
    import random
    class EventStorage:
        def __init__(self, name, title, fallback):
            self.name = name
            self.title = title
            self.fallback = fallback
            self.events = {
                1: {},
                2: {},
                3: {},
            }

        def _update(self, title):
            self.title = title

        def get_title(self):
            return self.title

        def add_event(self, event):
            if event.get_name() not in self.events[event.get_priority()].keys():
                self.events[event.get_priority()][event.get_name()] = event

        def count_available_events(self, school = "x", priority = 0):
            if priority == 0 or priority == 1:
                for event in self.events[1].values():
                    if event.is_available(school):
                        return 1
            if priority == 0 or priority == 2:
                output = 0
                for event in self.events[2].values():
                    if event.is_available(school):
                        output += 1
                if output != 0:
                    return output
            if priority == 0 or priority == 3:
                output = 0
                for event in self.events[3].values():
                    if event.is_available(school):
                        output += 1
                return output
            return 0

        def count_available_events_with_fallback(self, school = "x", priority = 0):
            output = self.count_available_events(school, priority)

            if output == 0:
                return 1
            return output

        def get_available_events(self, school = "x", priority = 0):
            if priority == 0 or priority == 1:
                for event in self.events[1].values():
                    if event.is_available(school):
                        return [event]
            if priority == 0 or priority == 2:
                output = []
                for event in self.events[2].values():
                    if event.is_available(school):
                        output.append(event)
                if len(output) != 0:
                    return output
            if priority == 0 or priority == 3:
                output = []
                print("Get Level 3 Event")
                print("check " + str(sum(event.get_event_count() for event in self.events[3].values())) + " possible")
                for event in self.events[3].values():
                    if event.is_available(school):
                        output.append(event)
                print("found " + str(len(output)) + " possible")
                if len(output) != 0:
                    return [random.choice(output)]
            return []

        def get_available_events_with_fallback(self, school = "x", priority = 0):
            output = self.get_available_events(school, priority)

            if len(output) == 0:
                return [self.fallback]
            return output

        def call_available_event(self, school = "x", priority = 0):
            print("Call available events")
            events = self.get_available_events_with_fallback(school, priority)

            for event in events:
                event.call()

    class TempEventStorage(EventStorage):
        def __init__(self, name, title, fallback):
            super().__init__(name, title, fallback)
            self.events = []

        def _update(self, title):
            self.title = title

        def get_title(self):
            return self.title

        def add_event(self, event):
            self.events.append(event)

        def remove_event(self, event_name):
            new_events = []
            for event in self.events:
                if event.get_name() != event_name:
                    new_events.append(event)
            self.events = new_events


        def count_available_events(self, school = "x", _priority = 0):
            output = 0

            for event in self.events:
                if (event.is_available(school)):
                    output += 1

            return output

        def count_available_events_with_fallback(self, school = "x", _priority = 0):
            output = 0

            for event in self.events:
                if (event.is_available(school)):
                    output += 1

            if output == 0:
                return 1
            return output

        def get_available_events(self, school = "x", priority = 0):
            output = []

            for event in self.events:
                if (event.is_available(school)):
                    output.append(event)

            return output

        def get_available_events_with_fallback(self, school = "x", priority = 0):
            output = self.get_available_events(school, priority)

            if len(output) == 0:
                return [self.fallback]
            return output

        def call_available_event(self, school = "x", priority = 0):
            events = self.get_available_events_with_fallback(school, priority)

            for event in events:
                self.events.remove(event)

            for event in events:
                event.call()

    class Event:
        def __init__(self, name, event, priority, *conditions):
            self.name = name
            self.event = event
            if isinstance(self.event, str):
                self.event = [self.event]
            self.conditions = list(conditions)

            # 1 = highest (the first 1 to occur is called blocking all other events)
            # 2 = middle (all 2's are called after each other)
            # 3 = lowest (selected random among 3's)
            self.priority = priority 

        def _update(self, data):
            if not hasattr(self, 'conditions'):
                self.conditions = []

            if not hasattr(self, 'priority'):
                self.priority = 3

            self.__dict__.update(data)

        def get_name(self):
            return self.name

        def add_event(self, *event):
            events = list(event)
            self.event.extend(events)

        def get_event(self):
            if isinstance(self.event, str):
                return [self.event]
            else:
                if self.priority == 1:
                    return [self.event[1]]
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

        def is_available(self, school):
            for condition in self.conditions:
                if not condition.is_fullfilled(school):
                    return False
            return True

        def call(self):

            events = self.get_event()

            print("events: " + str(events))

            renpy.call("call_event", events, self.priority)



    def load_event(events, name, data):
        if name not in events.keys():
            events[name] = Event(name, event)

        events[name]._update(data)

label call_available_event(event_storage, school = "x", priority = 0):
    $ events_list = event_storage.get_available_events_with_fallback(school, priority)

    $ i = 0
    while(len(events_list) > i):
        $ events = events_list[i].get_event()
        $ j = 0
        while (len(events) > j):
            call expression events[j] from _call_expression
            $ j += 1
        $ i += 1
