init -1 python:
    def add_temp_event(event):
        temp_time_check_events.add_event(event)
    def remove_temp_event(event):
        temp_time_check_events.remove_event(event)

    after_temp_event_check = Event("after_temp_event_check", "time_event_check.after_temp_event_check", 2)
    after_event_check      = Event("after_event_check",      "time_event_check.after_event_check",      2)

    temp_check_events      = EventStorage("temp_check_events",      "", after_event_check     )
    temp_time_check_events = TempEventStorage("temp_time_check_events", "", after_temp_event_check)

    temp_check_events.add_event(Event("first_day_introduction", "first_day_introduction", 2,
        TimeCondition(day = 1, month = 1, year = 2023, daytime = 1)
    ))

    temp_check_events.add_event(Event("weekly_assembly_first", "weekly_assembly_first", 2,
        TimeCondition(day = 1, month = 1, year = 2023, daytime = 1)
    ))

    temp_check_events.add_event(Event("weekly_assembly", "weekly_assembly", 2,
        TimeCondition(weekday = 1, daytime = 1)
    ))

    temp_check_events.add_event(Event("first_pta_meeting", "first_pta_meeting", 1,
        TimeCondition(day = 5, month = 1, year = 2023, daytime = 1)
    ))

    temp_check_events.add_event(Event("pta_meeting1", "pta_meeting", 2,
        TimeCondition(day = 5, daytime = 1)
    ))

    temp_check_events.add_event(Event("pta_meeting2", "pta_meeting", 2,
        TimeCondition(day = 19, daytime = 1)
    ))

    temp_check_events.add_event(Event("potion_introduction_1", "potion_introduction_1", 2,
        TimeCondition(day = 8, daytime = 1)
    ))

    temp_check_events.add_event(Event("potion_introduction_2", "potion_introduction_2", 2,
        TimeCondition(day = 9, daytime = 1)
    ))


label time_event_check:

    hide screen school_overview_map
    hide screen school_overview_stats
    hide screen school_overview_buttons

    call call_available_event(temp_time_check_events) from _call_call_available_event_16

label .after_temp_event_check:

    call call_available_event(temp_check_events) from _call_call_available_event_17

label .after_event_check:
    return

