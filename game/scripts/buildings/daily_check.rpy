init -10 python:
    time_check_events = {}

    print(time_check_events.keys())

    add_event(time_check_events, "1.1.2023.1.x.x:x:x.1", "first_day_introduction")

    add_event(time_check_events, "x.x.x.1.1.x:x:x.1", "weekly_assembly")
    add_event(time_check_events, "5.x.x.1.x.x:x:x.1", "pta_meeting")
    add_event(time_check_events, "8.x.x.1.x.x:x:x.1", "potion_introduction_1")
    add_event(time_check_events, "9.x.x.1.x.x:x:x.1", "potion_introduction_2")
    add_event(time_check_events, "19.x.x.1.x.x:x:x.1", "pta_meeting")

    print(time_check_events)

    temp_time_check_events = []


label time_event_check:

    hide screen school_overview_map
    hide screen school_overview_stats
    hide screen school_overview_buttons

    call temp_event_check(temp_time_check_events)

    call event_check(time_check_events)

    return

